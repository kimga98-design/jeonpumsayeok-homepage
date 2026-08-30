#!/usr/bin/env python3
"""PDF -> Markdown 변환기.

하나 이상의 PDF 파일(또는 폴더)을 읽어서 Markdown(.md) 파일로 변환한다.
글자 크기/굵기를 기준으로 제목(H1~H3)을 추론하고, 글머리 기호/번호 목록을
감지하며, --images 옵션으로 PDF에 포함된 이미지를 추출해 함께 저장할 수 있다.
--tables 옵션(pdfplumber 필요)으로 표를 Markdown 표로 변환할 수 있다.

사용 예:
    python pdf_to_markdown.py document.pdf
    python pdf_to_markdown.py document.pdf -o out.md
    python pdf_to_markdown.py ./pdfs -o ./markdown -r
    python pdf_to_markdown.py document.pdf --images --tables
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import pymupdf as fitz  # PyMuPDF
except ImportError:
    try:
        import fitz  # PyMuPDF (older package name)
    except ImportError:
        fitz = None
if fitz is None:
    print(
        "PyMuPDF가 설치되어 있지 않습니다. 먼저 다음을 실행하세요:\n"
        "    pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


BULLET_RE = re.compile(r"^\s*([•‣◦∙·▪○●-]|\*)\s+")
NUMBERED_RE = re.compile(r"^\s*(\d+[.)]|[a-zA-Z][.)])\s+")


def escape_markdown(text: str) -> str:
    """Markdown 특수문자를 이스케이프한다 (제목/목록 기호는 별도 처리하므로 제외)."""
    return re.sub(r"([\\`*_{}\[\]()#+!])", r"\\\1", text)


def get_body_font_size(doc: "fitz.Document") -> float:
    """문서에서 가장 흔하게 쓰인 글자 크기(본문 크기)를 추정한다."""
    sizes = []
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if span["text"].strip():
                        sizes.append(round(span["size"], 1))
    if not sizes:
        return 11.0
    return Counter(sizes).most_common(1)[0][0]


def classify_heading(size: float, body_size: float, is_bold: bool) -> int:
    """글자 크기 비율로 제목 레벨(1~3)을 추정한다. 본문이면 0을 반환한다."""
    ratio = size / body_size if body_size else 1.0
    if ratio >= 1.45:
        return 1
    if ratio >= 1.25:
        return 2
    if ratio >= 1.1 or (is_bold and ratio >= 1.02):
        return 3
    return 0


def line_text_and_style(line: dict) -> tuple[str, float, bool]:
    """한 줄의 텍스트, 평균 글자 크기, 굵은 글씨 여부를 반환한다."""
    spans = line.get("spans", [])
    text = "".join(span["text"] for span in spans)
    sizes = [span["size"] for span in spans if span["text"].strip()]
    avg_size = sum(sizes) / len(sizes) if sizes else 0.0
    is_bold = any(span["flags"] & 2**4 for span in spans)  # bit 4 = bold
    return text, avg_size, is_bold


def extract_page_images(page: "fitz.Page", doc: "fitz.Document", images_dir: Path, prefix: str) -> list[str]:
    """페이지에 포함된 이미지를 저장하고, 저장된 파일명 목록을 반환한다."""
    saved = []
    for idx, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        try:
            base_image = doc.extract_image(xref)
        except Exception:
            continue
        ext = base_image.get("ext", "png")
        filename = f"{prefix}_p{page.number + 1}_{idx}.{ext}"
        (images_dir / filename).write_bytes(base_image["image"])
        saved.append(filename)
    return saved


def extract_page_tables(page, page_number: int) -> list[str]:
    """pdfplumber로 표를 찾아 Markdown 표 문자열 목록으로 반환한다."""
    tables_md = []
    for table in page.extract_tables():
        if not table or not any(any(cell for cell in row) for row in table):
            continue
        rows = [[("" if cell is None else str(cell).strip()) for cell in row] for row in table]
        header, *body = rows
        lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
        for row in body:
            lines.append("| " + " | ".join(row) + " |")
        tables_md.append("\n".join(lines))
    return tables_md


def pdf_to_markdown(
    pdf_path: Path,
    extract_images: bool = False,
    extract_tables: bool = False,
    images_dirname: str | None = None,
) -> str:
    """PDF 파일 하나를 Markdown 텍스트로 변환한다."""
    doc = fitz.open(pdf_path)
    body_size = get_body_font_size(doc)

    images_dir = None
    if extract_images:
        images_dir = pdf_path.parent / (images_dirname or f"{pdf_path.stem}_images")
        images_dir.mkdir(parents=True, exist_ok=True)

    plumber_pages = None
    if extract_tables:
        try:
            import pdfplumber

            plumber_pages = pdfplumber.open(pdf_path).pages
        except ImportError:
            print(
                "--tables 옵션을 쓰려면 pdfplumber가 필요합니다: pip install pdfplumber",
                file=sys.stderr,
            )
        except Exception as exc:
            print(f"표 추출을 건너뜁니다 (pdfplumber 오류: {exc})", file=sys.stderr)

    md_lines: list[str] = [f"# {pdf_path.stem}\n"]

    for page_index, page in enumerate(doc):
        blocks = sorted(page.get_text("dict")["blocks"], key=lambda b: (b["bbox"][1], b["bbox"][0]))

        for block in blocks:
            if block.get("type") != 0:  # 텍스트 블록만 처리 (이미지 블록 제외)
                continue

            paragraph_buf: list[str] = []

            def flush_paragraph():
                if paragraph_buf:
                    md_lines.append(" ".join(paragraph_buf).strip())
                    md_lines.append("")
                    paragraph_buf.clear()

            for line in block.get("lines", []):
                text, avg_size, is_bold = line_text_and_style(line)
                stripped = text.strip()
                if not stripped:
                    continue

                heading_level = classify_heading(avg_size, body_size, is_bold)

                if heading_level:
                    flush_paragraph()
                    if md_lines and md_lines[-1] != "":
                        md_lines.append("")
                    md_lines.append(f"{'#' * (heading_level + 1)} {escape_markdown(stripped)}")
                    md_lines.append("")
                    continue

                if BULLET_RE.match(stripped):
                    flush_paragraph()
                    content = BULLET_RE.sub("", stripped)
                    md_lines.append(f"- {escape_markdown(content)}")
                    continue

                if NUMBERED_RE.match(stripped):
                    flush_paragraph()
                    match = NUMBERED_RE.match(stripped)
                    content = stripped[match.end():]
                    md_lines.append(f"{match.group(1)} {escape_markdown(content)}")
                    continue

                if is_bold:
                    paragraph_buf.append(f"**{escape_markdown(stripped)}**")
                else:
                    paragraph_buf.append(escape_markdown(stripped))

            flush_paragraph()

        if extract_images and images_dir is not None:
            saved = extract_page_images(page, doc, images_dir, pdf_path.stem)
            for filename in saved:
                md_lines.append(f"![{filename}]({images_dir.name}/{filename})")
                md_lines.append("")

        if plumber_pages is not None and page_index < len(plumber_pages):
            for table_md in extract_page_tables(plumber_pages[page_index], page_index + 1):
                md_lines.append(table_md)
                md_lines.append("")

    doc.close()

    # 연속된 빈 줄 정리
    text = "\n".join(md_lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text


def resolve_output_path(pdf_path: Path, output: Path | None, input_root: Path | None) -> Path:
    if output is None:
        return pdf_path.with_suffix(".md")
    if output.suffix.lower() == ".md":
        return output
    # output이 디렉터리인 경우: 입력 폴더 구조를 유지해서 저장
    rel = pdf_path.relative_to(input_root) if input_root else Path(pdf_path.name)
    return output / rel.with_suffix(".md")


def collect_pdf_files(input_path: Path, recursive: bool) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    pattern = "**/*.pdf" if recursive else "*.pdf"
    return sorted(input_path.glob(pattern))


def main():
    parser = argparse.ArgumentParser(
        description="PDF 파일을 Markdown으로 변환합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="변환할 PDF 파일 또는 PDF가 들어있는 폴더")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="출력 파일(.md) 또는 폴더 경로. 지정하지 않으면 입력과 같은 위치에 .md로 저장",
    )
    parser.add_argument("-r", "--recursive", action="store_true", help="폴더를 재귀적으로 탐색")
    parser.add_argument("--images", action="store_true", help="PDF에 포함된 이미지를 추출해 함께 저장")
    parser.add_argument("--tables", action="store_true", help="표를 Markdown 표로 변환 (pdfplumber 필요)")
    args = parser.parse_args()

    if not args.input.exists():
        parser.error(f"입력 경로를 찾을 수 없습니다: {args.input}")

    pdf_files = collect_pdf_files(args.input, args.recursive)
    if not pdf_files:
        parser.error(f"PDF 파일을 찾지 못했습니다: {args.input}")

    input_root = args.input if args.input.is_dir() else None

    converted = 0
    for pdf_path in pdf_files:
        out_path = resolve_output_path(pdf_path, args.output, input_root)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"변환 중: {pdf_path} -> {out_path}")
        try:
            markdown = pdf_to_markdown(
                pdf_path,
                extract_images=args.images,
                extract_tables=args.tables,
            )
        except Exception as exc:
            print(f"실패: {pdf_path} ({exc})", file=sys.stderr)
            continue
        out_path.write_text(markdown, encoding="utf-8")
        converted += 1

    print(f"완료: {converted}/{len(pdf_files)}개 파일 변환")


if __name__ == "__main__":
    main()

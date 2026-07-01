#!/usr/bin/env python3
"""
PDF → Markdown 변환기
사용법:
  python pdf_to_md.py 파일.pdf
  python pdf_to_md.py 폴더/          # 폴더 내 모든 PDF 일괄 변환
  python pdf_to_md.py 파일.pdf -o 출력폴더/
"""

import sys
import re
from pathlib import Path
from datetime import date


def extract_with_pymupdf(pdf_path: Path) -> str:
    import fitz  # pymupdf
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc, 1):
        text = page.get_text("text")
        if text.strip():
            pages.append(f"<!-- page {i} -->\n{text.strip()}")
    doc.close()
    return "\n\n".join(pages)


def extract_with_pdfplumber(pdf_path: Path) -> str:
    import pdfplumber
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text and text.strip():
                pages.append(f"<!-- page {i} -->\n{text.strip()}")
    return "\n\n".join(pages)


def extract_text(pdf_path: Path) -> str:
    try:
        return extract_with_pymupdf(pdf_path)
    except ImportError:
        pass
    try:
        return extract_with_pdfplumber(pdf_path)
    except ImportError:
        sys.exit("pymupdf 또는 pdfplumber 설치 필요:\n  pip install pymupdf\n  또는\n  pip install pdfplumber")


def clean_text(text: str) -> str:
    # 연속 빈줄 정리
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 줄 끝 공백 제거
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip()


def build_markdown(title: str, text: str) -> str:
    today = date.today().isoformat()
    frontmatter = f"""---
date: {today}
source: pdf
tags: [원자료]
---

# {title}

"""
    return frontmatter + text


def convert(pdf_path: Path, output_dir: Path):
    print(f"변환 중: {pdf_path.name}")
    raw = extract_text(pdf_path)
    cleaned = clean_text(raw)
    title = pdf_path.stem
    md = build_markdown(title, cleaned)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / (pdf_path.stem + ".md")
    out_file.write_text(md, encoding="utf-8")
    print(f"  저장: {out_file}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="PDF 파일 또는 폴더")
    parser.add_argument("-o", "--output", default=None, help="출력 폴더 (기본: 입력과 같은 위치)")
    args = parser.parse_args()

    input_path = Path(args.input)

    if input_path.is_dir():
        pdfs = list(input_path.glob("**/*.pdf"))
        if not pdfs:
            sys.exit("PDF 파일이 없습니다.")
        for pdf in pdfs:
            out_dir = Path(args.output) if args.output else pdf.parent
            convert(pdf, out_dir)
    elif input_path.is_file() and input_path.suffix.lower() == ".pdf":
        out_dir = Path(args.output) if args.output else input_path.parent
        convert(input_path, out_dir)
    else:
        sys.exit(f"파일을 찾을 수 없습니다: {input_path}")

    print("완료.")


if __name__ == "__main__":
    main()

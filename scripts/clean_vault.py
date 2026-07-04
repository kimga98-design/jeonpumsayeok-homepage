#!/usr/bin/env python3
"""
Obsidian 볼트 변환 파일 정리 스크립트

기능:
  1. 인라인 #태그 이스케이프 (변환 과정에서 생긴 단어 태그 제거)
  2. Excel 오류값 태그 제거 (#DIV/0, #N/A, #REF 등)
  3. 빈 노드 생성 원인 제거

사용법:
  python3 clean_vault.py VAULT_PATH
  python3 clean_vault.py ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Pastor_OS_v2/20-원자료/인박스
"""

import re
import sys
from pathlib import Path

# 보존할 의도적 태그 (이 목록에 있으면 이스케이프하지 않음)
KEEP_TAGS = {
    "설교소재", "위기", "핵심", "처리중", "보류",
    "설교", "돌봄", "질환이해", "위기대응", "돌봄체계",
    "회복프로그램", "기분장애", "즉각대응", "구조", "절차",
}

# Excel/변환 오류 태그 패턴
EXCEL_ERROR = re.compile(
    r'\\?#(DIV[/\\]0|N[/\\]A|REF|NAME|VALUE|NULL|NUM|ERROR)!?',
    re.IGNORECASE
)


def clean_file(path: Path) -> bool:
    """파일 정리. 변경된 경우 True 반환."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  읽기 실패: {path.name} — {e}")
        return False

    original = text
    lines = []
    in_frontmatter = False
    frontmatter_done = False
    fm_count = 0

    for line in text.splitlines():
        stripped = line.rstrip()

        # 프론트매터 구간 감지
        if stripped == "---":
            fm_count += 1
            if fm_count == 1:
                in_frontmatter = True
            elif fm_count == 2:
                in_frontmatter = False
                frontmatter_done = True
            lines.append(stripped)
            continue

        if in_frontmatter:
            lines.append(stripped)
            continue

        # 본문 처리
        if stripped.startswith('#'):
            # 마크다운 헤딩 — 그대로 유지
            lines.append(stripped)
        else:
            # 인라인 #태그 이스케이프 (보존 목록 제외)
            def escape_tag(m):
                tag = m.group(1)
                if tag in KEEP_TAGS:
                    return m.group(0)  # 보존
                return '\\#' + tag

            cleaned = re.sub(r'#([^\s#\[\](){}<>]+)', escape_tag, stripped)
            # Excel 오류값 이스케이프
            cleaned = EXCEL_ERROR.sub(lambda m: '\\#' + m.group(1), cleaned)
            lines.append(cleaned)

    result = "\n".join(lines)
    if result != original:
        path.write_text(result, encoding="utf-8")
        return True
    return False


def main():
    if len(sys.argv) < 2:
        vault_path = Path.home() / "Library" / "Mobile Documents" / \
                     "iCloud~md~obsidian" / "Documents" / "Pastor_OS_v2" / \
                     "20-원자료" / "인박스"
    else:
        vault_path = Path(sys.argv[1]).expanduser()

    if not vault_path.exists():
        print(f"경로 없음: {vault_path}")
        sys.exit(1)

    files = list(vault_path.rglob("*.md"))
    print(f"파일 {len(files)}개 스캔 중: {vault_path}\n")

    changed = 0
    for f in files:
        if clean_file(f):
            print(f"  정리: {f.name}")
            changed += 1

    print(f"\n완료: {changed}/{len(files)}개 파일 수정됨")


if __name__ == "__main__":
    main()

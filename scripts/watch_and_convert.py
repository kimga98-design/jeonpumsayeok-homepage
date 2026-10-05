#!/usr/bin/env python3
"""
폴더 감시 → 자동 Markdown 변환

설치:
  pip install watchdog pymupdf python-docx python-pptx openpyxl beautifulsoup4

사용법:
  python watch_and_convert.py                         # 기본 경로 사용
  python watch_and_convert.py --watch ~/Desktop/변환대기 --out ~/obsidian/20-원자료/인박스

동작:
  감시 폴더에 파일을 넣으면 자동으로 MD로 변환해서 출력 폴더에 저장
  변환 완료된 원본 파일은 감시 폴더 내 _done/ 으로 이동
"""

import sys
import time
import shutil
import argparse
import logging
from pathlib import Path

# to_md.py 와 같은 폴더에 있어야 함
sys.path.insert(0, str(Path(__file__).parent))
from to_md import EXTRACTORS, convert_local

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    sys.exit("pip install watchdog")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# 기본 경로 (필요 시 수정)
DEFAULT_WATCH = Path.home() / "Desktop" / "변환대기"
DEFAULT_OUT   = Path.home() / "Documents" / "jeonpumsayeok-homepage" / "obsidian" / "20-원자료" / "인박스"


class ConvertHandler(FileSystemEventHandler):
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.processing: set = set()

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() not in EXTRACTORS:
            return
        if path in self.processing:
            return
        if path.parent.name == "_done":
            return

        self.processing.add(path)
        # 파일 쓰기 완료 대기 (복사 중인 파일 방지)
        time.sleep(1)
        self._handle(path)
        self.processing.discard(path)

    def _handle(self, path: Path):
        try:
            convert_local(path, self.output_dir)
            done_dir = path.parent / "_done"
            done_dir.mkdir(exist_ok=True)
            shutil.move(str(path), done_dir / path.name)
            log.info(f"완료: {path.name} → {self.output_dir.name}/")
        except Exception as e:
            log.error(f"오류 ({path.name}): {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", default=str(DEFAULT_WATCH), help="감시할 폴더")
    parser.add_argument("--out",   default=str(DEFAULT_OUT),   help="MD 출력 폴더")
    args = parser.parse_args()

    watch_dir = Path(args.watch)
    output_dir = Path(args.out)

    watch_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    log.info(f"감시 폴더: {watch_dir}")
    log.info(f"출력 폴더: {output_dir}")
    log.info("파일을 감시 폴더에 넣으면 자동 변환됩니다. 종료: Ctrl+C\n")

    handler = ConvertHandler(output_dir)
    observer = Observer()
    observer.schedule(handler, str(watch_dir), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    log.info("종료.")


if __name__ == "__main__":
    main()

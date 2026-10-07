# PDF to Markdown 변환기

PDF 파일을 Markdown(.md)으로 변환하는 파이썬 스크립트입니다. 글자 크기/굵기를
기준으로 제목(H1~H3)을 자동으로 추론하고, 글머리 기호·번호 목록을 인식하며,
이미지와 표(옵션)까지 함께 뽑아낼 수 있습니다.

## 설치

Python 3.9 이상이 필요합니다.

```bash
cd tools/pdf-to-markdown
pip install -r requirements.txt
```

- 표 변환(`--tables`) 기능을 쓰지 않을 거라면 `PyMuPDF`만 설치해도 됩니다:
  `pip install PyMuPDF`

## 사용법

```bash
# 파일 하나 변환 (같은 위치에 document.md 생성)
python pdf_to_markdown.py document.pdf

# 출력 파일명 지정
python pdf_to_markdown.py document.pdf -o result.md

# 폴더 안의 모든 PDF를 변환해서 다른 폴더에 저장 (하위 폴더까지 재귀 탐색)
python pdf_to_markdown.py ./pdfs -o ./markdown -r

# 이미지와 표까지 함께 추출
python pdf_to_markdown.py document.pdf --images --tables
```

### 옵션

| 옵션 | 설명 |
| --- | --- |
| `input` | 변환할 PDF 파일 또는 PDF들이 들어있는 폴더 (필수) |
| `-o`, `--output` | 출력 `.md` 파일 또는 출력 폴더. 생략 시 입력과 같은 위치에 저장 |
| `-r`, `--recursive` | 폴더 입력 시 하위 폴더까지 재귀적으로 탐색 |
| `--images` | PDF에 포함된 이미지를 추출해 `<파일명>_images/` 폴더에 저장하고 Markdown에 링크 삽입 |
| `--tables` | 표를 Markdown 표로 변환 (`pdfplumber` 필요) |

## 동작 방식 / 한계

- 제목은 문서에서 가장 흔한 글자 크기(본문 크기) 대비 상대적인 크기 비율로 추정합니다.
  디자인이 특이한 PDF(제목에 별도 스타일이 없는 경우 등)에서는 완벽하지 않을 수 있습니다.
- 스캔한 이미지 PDF(텍스트 레이어가 없는 경우)는 텍스트를 추출할 수 없습니다.
  OCR이 필요한 경우 `ocrmypdf` 등으로 먼저 텍스트 레이어를 만든 뒤 사용하세요.
- 표 변환은 `pdfplumber`의 표 탐지 결과에 의존하므로, 선이 없는 표는 인식이 어려울 수 있습니다.

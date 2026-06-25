#!/usr/bin/env python3
"""
단어 자동 노트 생성기
사용법:
  python3 add_word.py                  # 대화형 모드
  python3 add_word.py describe hajin   # 단어 + 볼트 지정
  python3 add_word.py school haon
"""

import sys
import json
import pathlib
import urllib.request
import urllib.parse
import urllib.error

# ─────────────────────────────────────────────
# 볼트 경로
# ─────────────────────────────────────────────
ICLOUD = pathlib.Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/영어볼트_공유"
LOCAL  = pathlib.Path.home() / "Desktop"

VAULTS = {
    "haon":  (ICLOUD if ICLOUD.exists() else LOCAL) / "하온_영어볼트",
    "hajin": (ICLOUD if ICLOUD.exists() else LOCAL) / "하진_영어볼트",
}

# ─────────────────────────────────────────────
# 어원(어근) 자동 감지 데이터베이스
# ─────────────────────────────────────────────
ROOTS = {
    "scrib": {"meaning": "쓰다 (write)", "origin": "라틴어 scribere",
              "keywords": ["scrib", "scrip", "script"]},
    "port":  {"meaning": "나르다 (carry)", "origin": "라틴어 portare",
              "keywords": ["port", "porting"]},
    "dict":  {"meaning": "말하다 (say)", "origin": "라틴어 dicere",
              "keywords": ["dict", "dic"]},
    "aud":   {"meaning": "듣다 (hear)", "origin": "라틴어 audire",
              "keywords": ["aud", "audit"]},
    "vis":   {"meaning": "보다 (see)", "origin": "라틴어 videre",
              "keywords": ["vis", "vid", "view"]},
    "duc":   {"meaning": "이끌다 (lead)", "origin": "라틴어 ducere",
              "keywords": ["duc", "duct", "duce"]},
    "mit":   {"meaning": "보내다 (send)", "origin": "라틴어 mittere",
              "keywords": ["mit", "miss", "mis"]},
    "rupt":  {"meaning": "깨다 (break)", "origin": "라틴어 rumpere",
              "keywords": ["rupt"]},
    "sect":  {"meaning": "자르다 (cut)", "origin": "라틴어 secare",
              "keywords": ["sect", "sec"]},
    "spect": {"meaning": "보다 (look)", "origin": "라틴어 specere",
              "keywords": ["spect", "spec", "spic"]},
    "struct": {"meaning": "쌓다 (build)", "origin": "라틴어 struere",
               "keywords": ["struct", "stru"]},
    "tract": {"meaning": "끌다 (pull/draw)", "origin": "라틴어 trahere",
              "keywords": ["tract", "trac"]},
    "vert":  {"meaning": "돌리다 (turn)", "origin": "라틴어 vertere",
              "keywords": ["vert", "vers"]},
    "voc":   {"meaning": "목소리/부르다 (voice/call)", "origin": "라틴어 vocare",
              "keywords": ["voc", "voke", "voice"]},
    "gen":   {"meaning": "태어나다/종류 (birth/kind)", "origin": "라틴어 genus",
              "keywords": ["gen"]},
    "graph": {"meaning": "쓰다/그리다 (write/draw)", "origin": "그리스어 graphein",
              "keywords": ["graph", "gram"]},
    "log":   {"meaning": "말/이성 (word/reason)", "origin": "그리스어 logos",
              "keywords": ["log", "logue", "logy"]},
    "phon":  {"meaning": "소리 (sound)", "origin": "그리스어 phone",
              "keywords": ["phon", "phone"]},
    "photo": {"meaning": "빛 (light)", "origin": "그리스어 phos",
              "keywords": ["photo", "phot"]},
    "bio":   {"meaning": "생명 (life)", "origin": "그리스어 bios",
              "keywords": ["bio"]},
    "geo":   {"meaning": "땅 (earth)", "origin": "그리스어 ge",
              "keywords": ["geo"]},
    "tele":  {"meaning": "멀리 (far)", "origin": "그리스어 tele",
              "keywords": ["tele"]},
    "-er":   {"meaning": "~하는 사람/것", "origin": "고대 영어",
              "keywords": ["er"]},
    "-tion": {"meaning": "~하는 행위/상태 (명사화)", "origin": "라틴어",
              "keywords": ["tion", "sion"]},
    "-able": {"meaning": "~할 수 있는 (형용사화)", "origin": "라틴어",
              "keywords": ["able", "ible"]},
}

PREFIXES = {
    "de":     "완전히 / 아래로",
    "sub":    "아래에",
    "pre":    "미리 / 앞에",
    "trans":  "가로질러 / 넘어서",
    "ex":     "밖으로",
    "im":     "안으로",
    "in":     "안에 / 부정",
    "re":     "다시 / 뒤로",
    "con":    "함께",
    "com":    "함께",
    "pro":    "앞으로",
    "inter":  "사이에",
    "super":  "위에 / 초월",
    "anti":   "반대",
    "un":     "부정",
    "dis":    "부정 / 반대",
    "over":   "지나치게 / 위에",
    "under":  "아래에 / 부족하게",
    "out":    "밖으로 / 능가",
    "mis":    "잘못",
}


def detect_root(word):
    word_lower = word.lower()
    found = []
    for root_name, info in ROOTS.items():
        for kw in info["keywords"]:
            if kw in word_lower:
                found.append(root_name)
                break
    return found[0] if found else None


def detect_prefix(word):
    word_lower = word.lower()
    for prefix, meaning in PREFIXES.items():
        if word_lower.startswith(prefix) and len(word_lower) > len(prefix) + 2:
            return prefix, meaning
    return None, None


# ─────────────────────────────────────────────
# API 호출
# ─────────────────────────────────────────────
def fetch_english(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word)}"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json.loads(r.read())
        return data[0] if data else None
    except Exception:
        return None


def fetch_korean(word):
    url = (
        "https://api.mymemory.translated.net/get?"
        + urllib.parse.urlencode({"q": word, "langpair": "en|ko"})
    )
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json.loads(r.read())
        kr = data.get("responseData", {}).get("translatedText", "")
        return kr if kr and kr != word else ""
    except Exception:
        return ""


# ─────────────────────────────────────────────
# 노트 생성
# ─────────────────────────────────────────────
def build_note(word, grade, en_data, kr_meaning, root_name, prefix_name, prefix_meaning):
    pronunciation = ""
    pos = ""
    meaning_en = ""
    synonyms = []
    antonyms = []
    example_en = ""

    if en_data:
        # 발음
        for ph in en_data.get("phonetics", []):
            if ph.get("text"):
                pronunciation = ph["text"]
                break

        # 품사 + 뜻 + 예문 + 유의어 + 반의어
        for meaning in en_data.get("meanings", []):
            if not pos:
                pos = meaning.get("partOfSpeech", "")
            for defn in meaning.get("definitions", []):
                if not meaning_en:
                    meaning_en = defn.get("definition", "")
                if not example_en:
                    example_en = defn.get("example", "")
                synonyms += defn.get("synonyms", [])
                antonyms += defn.get("antonyms", [])
            synonyms += meaning.get("synonyms", [])
            antonyms += meaning.get("antonyms", [])

    synonyms = list(dict.fromkeys(synonyms))[:4]
    antonyms = list(dict.fromkeys(antonyms))[:4]

    # 어원 분석 텍스트 구성
    root_info = ROOTS.get(root_name, {})
    prefix_text = f"{prefix_name}({prefix_meaning}) + " if prefix_name else ""
    root_text = f"{root_name}({root_info.get('meaning', '')}) " if root_name else ""
    hint = kr_meaning or (meaning_en[:30] + "..." if meaning_en else word)
    if prefix_name or root_name:
        etymology_text = f"{prefix_text}{root_text}→ '{hint}'의 의미가 됩니다"
    else:
        etymology_text = "직접 어원을 찾아 써보세요!"

    root_field = f"[[{root_name}]]" if root_name else "없음"
    synonyms_str = ", ".join([f"[[{s}]]" for s in synonyms]) if synonyms else "없음"
    antonyms_str = ", ".join([f"[[{a}]]" for a in antonyms]) if antonyms else "없음"

    # 관련 단어 링크 (어원 + 유의어 첫번째)
    related = []
    if root_name:
        related.append(f"- [[{root_name}]]")
    for s in synonyms[:2]:
        related.append(f"- [[{s}]]")
    related_str = "\n".join(related) if related else "- (직접 추가해보세요)"

    pos_map = {
        "noun": "명사", "verb": "동사", "adjective": "형용사",
        "adverb": "부사", "preposition": "전치사", "conjunction": "접속사",
    }
    pos_kr = pos_map.get(pos, pos)

    return f"""\
---
단어: {word}
발음: {pronunciation}
품사: {pos_kr}
학년: {grade}
어원: {root_field}
유의어: [{synonyms_str}]
반의어: [{antonyms_str}]
---

# 📖 뜻
> **{word}** : {kr_meaning or "(번역 실패 — 직접 입력)"}
> (영어) {meaning_en}

# 🌱 어원으로 추측하기
> {etymology_text}

# 📌 예문
| 영어 | 한국어 |
|------|--------|
| {example_en or "(예문 없음 — 직접 입력)"} | |

# ✏️ 나만의 예문 (직접 써보세요!)
> 예문 1:
> 예문 2:

# 🔗 꼬리에 꼬리를 무는 단어
{related_str}
"""


def save_note(vault_path, word, content):
    note_path = vault_path / "02_단어" / f"{word}.md"
    note_path.parent.mkdir(parents=True, exist_ok=True)
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(content)
    return note_path


# ─────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────
def process_word(word, vault_key):
    vault_path = VAULTS[vault_key]
    grade = "중1" if vault_key == "haon" else "중3"

    print(f"\n🔍 '{word}' 정보 가져오는 중...")

    en_data   = fetch_english(word)
    kr_meaning = fetch_korean(word)
    root_name  = detect_root(word)
    prefix_name, prefix_meaning = detect_prefix(word)

    if not en_data:
        print("  ⚠️  영어 사전 정보를 가져오지 못했습니다. 기본 틀로 생성합니다.")

    note = build_note(word, grade, en_data, kr_meaning, root_name, prefix_name, prefix_meaning)
    path = save_note(vault_path, word, note)

    print(f"  ✅ 노트 생성 완료: {path}")
    if root_name:
        print(f"  🌱 감지된 어원: [[{root_name}]] — {ROOTS[root_name]['meaning']}")
    if prefix_name:
        print(f"  🔤 감지된 접두사: {prefix_name} ({prefix_meaning})")
    if kr_meaning:
        print(f"  🇰🇷 한국어 뜻: {kr_meaning}")


def main():
    args = sys.argv[1:]

    # 인자로 실행: python3 add_word.py describe hajin
    if len(args) >= 2:
        word, vault_key = args[0].lower(), args[1].lower()
        if vault_key not in VAULTS:
            print(f"❌ 볼트 이름 오류: '{vault_key}' → haon 또는 hajin 입력")
            sys.exit(1)
        process_word(word, vault_key)
        return

    # 대화형 모드
    print("=" * 45)
    print("  📖 단어 자동 노트 생성기")
    print("=" * 45)
    print("종료하려면 Ctrl+C 또는 빈 줄에서 Enter\n")

    while True:
        try:
            word = input("단어 입력 > ").strip().lower()
            if not word:
                break
            print("볼트 선택:")
            print("  1. 하온 (중1)")
            print("  2. 하진 (중3)")
            print("  3. 둘 다")
            choice = input("선택 (1/2/3) > ").strip()

            if choice == "1":
                process_word(word, "haon")
            elif choice == "2":
                process_word(word, "hajin")
            elif choice == "3":
                process_word(word, "haon")
                process_word(word, "hajin")
            else:
                print("1, 2, 3 중에 선택해주세요.")
            print()
        except KeyboardInterrupt:
            print("\n\n👋 종료합니다.")
            break


if __name__ == "__main__":
    main()

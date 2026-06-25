#!/usr/bin/env python3
"""
옵시디언 볼트 생성 스크립트 - 하진 버전 (중3)
실행 방법: python3 setup_hajin.py
실행 후 생성된 '하진_영어볼트' 폴더를 옵시디언에서 열면 됩니다.
"""

import pathlib

VAULT = "하진_영어볼트"

WORDS = [
    {
        "word": "describe",
        "pronunciation": "디스크라이브",
        "pos": "동사",
        "grade": "중3",
        "meaning": "묘사하다, 설명하다",
        "root": "scrib",
        "root_meaning": "de(완전히) + scrib(쓰다) + e → '완전히 써내다' → 묘사하다",
        "synonyms": ["explain", "depict", "portray"],
        "antonyms": [],
        "example_en": "Can you describe what you saw?",
        "example_kr": "당신이 본 것을 묘사할 수 있나요?",
        "related": ["scrib", "subscribe", "prescribe"],
    },
    {
        "word": "subscribe",
        "pronunciation": "섭스크라이브",
        "pos": "동사",
        "grade": "중3",
        "meaning": "구독하다, 서명하다",
        "root": "scrib",
        "root_meaning": "sub(아래에) + scrib(쓰다) + e → '아래에 이름을 쓰다' → 구독/서명하다",
        "synonyms": ["sign up", "register"],
        "antonyms": ["unsubscribe", "cancel"],
        "example_en": "Please subscribe to our channel.",
        "example_kr": "우리 채널을 구독해 주세요.",
        "related": ["scrib", "describe", "prescribe"],
    },
    {
        "word": "prescribe",
        "pronunciation": "프리스크라이브",
        "pos": "동사",
        "grade": "중3",
        "meaning": "처방하다, 규정하다",
        "root": "scrib",
        "root_meaning": "pre(미리) + scrib(쓰다) + e → '미리 써두다' → 처방하다",
        "synonyms": ["recommend", "order"],
        "antonyms": [],
        "example_en": "The doctor prescribed medicine for my cold.",
        "example_kr": "의사는 내 감기를 위해 약을 처방했습니다.",
        "related": ["scrib", "describe", "subscribe"],
    },
    {
        "word": "transport",
        "pronunciation": "트랜스포트",
        "pos": "동사/명사",
        "grade": "중3",
        "meaning": "수송하다 / 교통수단",
        "root": "port",
        "root_meaning": "trans(가로질러) + port(나르다) → '한 곳에서 다른 곳으로 나르다' → 수송",
        "synonyms": ["carry", "ship", "transfer"],
        "antonyms": [],
        "example_en": "Ships transport goods across the ocean.",
        "example_kr": "배는 물건들을 바다를 건너 수송합니다.",
        "related": ["port", "export", "import", "support"],
    },
    {
        "word": "export",
        "pronunciation": "엑스포트",
        "pos": "동사/명사",
        "grade": "중3",
        "meaning": "수출하다 / 수출",
        "root": "port",
        "root_meaning": "ex(밖으로) + port(나르다) → '밖으로 내보내다' → 수출",
        "synonyms": ["ship out", "send abroad"],
        "antonyms": ["import"],
        "example_en": "Korea exports many electronic products.",
        "example_kr": "한국은 많은 전자 제품을 수출합니다.",
        "related": ["port", "import", "transport", "support"],
    },
    {
        "word": "import",
        "pronunciation": "임포트",
        "pos": "동사/명사",
        "grade": "중3",
        "meaning": "수입하다 / 수입",
        "root": "port",
        "root_meaning": "im(안으로) + port(나르다) → '안으로 들여오다' → 수입",
        "synonyms": ["bring in"],
        "antonyms": ["export"],
        "example_en": "We import oil from other countries.",
        "example_kr": "우리는 다른 나라에서 석유를 수입합니다.",
        "related": ["port", "export", "transport", "support"],
    },
    {
        "word": "predict",
        "pronunciation": "프리딕트",
        "pos": "동사",
        "grade": "중3",
        "meaning": "예측하다, 예언하다",
        "root": "dict",
        "root_meaning": "pre(미리) + dict(말하다) → '미리 말하다' → 예측하다",
        "synonyms": ["forecast", "anticipate", "foresee"],
        "antonyms": [],
        "example_en": "Scientists predict the weather using data.",
        "example_kr": "과학자들은 데이터를 사용해 날씨를 예측합니다.",
        "related": ["dict", "verdict", "dictate"],
    },
    {
        "word": "verdict",
        "pronunciation": "버딕트",
        "pos": "명사",
        "grade": "중3",
        "meaning": "평결, 판결",
        "root": "dict",
        "root_meaning": "ver(진실) + dict(말하다) → '진실을 말하다' → 판결",
        "synonyms": ["judgment", "decision", "ruling"],
        "antonyms": [],
        "example_en": "The jury delivered a not-guilty verdict.",
        "example_kr": "배심원단은 무죄 평결을 내렸습니다.",
        "related": ["dict", "predict", "dictate"],
    },
    {
        "word": "audience",
        "pronunciation": "오디언스",
        "pos": "명사",
        "grade": "중3",
        "meaning": "청중, 관중",
        "root": "aud",
        "root_meaning": "aud(듣다) + ience(상태/집합) → '듣는 사람들의 집합' → 청중",
        "synonyms": ["spectators", "viewers", "crowd"],
        "antonyms": [],
        "example_en": "The audience applauded after the performance.",
        "example_kr": "공연이 끝난 후 청중이 박수를 쳤습니다.",
        "related": ["aud", "audible", "audio"],
    },
    {
        "word": "audible",
        "pronunciation": "오디블",
        "pos": "형용사",
        "grade": "중3",
        "meaning": "들을 수 있는",
        "root": "aud",
        "root_meaning": "aud(듣다) + ible(~할 수 있는) → '들을 수 있는'",
        "synonyms": ["hearable", "perceptible"],
        "antonyms": ["inaudible", "silent"],
        "example_en": "His voice was barely audible in the crowd.",
        "example_kr": "군중 속에서 그의 목소리는 거의 들리지 않았습니다.",
        "related": ["aud", "audience", "audio"],
    },
]

ETYMOLOGIES = [
    {
        "root": "scrib",
        "origin": "라틴어 scribere",
        "meaning": "쓰다 (to write)",
        "examples": ["describe", "subscribe", "prescribe", "inscribe", "manuscript"],
        "explanation": (
            "**scrib/scrip** 은 '쓰다(write)'를 의미하는 라틴어 어근입니다.\n\n"
            "| 접두사 | + scrib | = 단어 | 뜻 |\n"
            "|--------|---------|--------|----|\n"
            "| de (완전히) | + scrib | = describe | 묘사하다 |\n"
            "| sub (아래) | + scrib | = subscribe | 구독하다 |\n"
            "| pre (미리) | + scrib | = prescribe | 처방하다 |\n"
            "| in (안에) | + scrib | = inscribe | 새기다 |\n\n"
            "💡 **script(대본, 스크립트)** 도 같은 어근! '쓰여진 것'이라는 뜻이에요."
        ),
    },
    {
        "root": "port",
        "origin": "라틴어 portare",
        "meaning": "나르다, 운반하다 (to carry)",
        "examples": ["transport", "export", "import", "support", "report", "portable"],
        "explanation": (
            "**port** 는 '나르다, 운반하다(carry)'를 의미하는 라틴어 어근입니다.\n\n"
            "| 접두사 | + port | = 단어 | 뜻 |\n"
            "|--------|--------|--------|----|\n"
            "| trans (가로질러) | + port | = transport | 수송하다 |\n"
            "| ex (밖으로) | + port | = export | 수출하다 |\n"
            "| im (안으로) | + port | = import | 수입하다 |\n"
            "| sup (아래서) | + port | = support | 지지하다 |\n"
            "| re (다시/뒤로) | + port | = report | 보고하다 |\n\n"
            "💡 **portable(휴대용의)** 도 같은 어근! '들고 다닐 수 있는'이라는 뜻이에요."
        ),
    },
    {
        "root": "dict",
        "origin": "라틴어 dicere",
        "meaning": "말하다 (to say, to speak)",
        "examples": ["predict", "verdict", "dictate", "indicate", "contradict"],
        "explanation": (
            "**dict** 는 '말하다(say/speak)'를 의미하는 라틴어 어근입니다.\n\n"
            "| 접두사 | + dict | = 단어 | 뜻 |\n"
            "|--------|--------|--------|----|\n"
            "| pre (미리) | + dict | = predict | 예측하다 |\n"
            "| ver (진실) | + dict | = verdict | 평결 |\n"
            "| contra (반대로) | + dict | = contradict | 반박하다 |\n"
            "| in (향하여) | + dict | = indicate | 나타내다 |\n\n"
            "💡 **dictionary(사전)** 도 같은 어근! '말들을 모아둔 책'이라는 뜻이에요."
        ),
    },
    {
        "root": "aud",
        "origin": "라틴어 audire",
        "meaning": "듣다 (to hear)",
        "examples": ["audience", "audible", "audio", "audit", "auditorium"],
        "explanation": (
            "**aud** 는 '듣다(hear)'를 의미하는 라틴어 어근입니다.\n\n"
            "| 어근 + 접미사 | = 단어 | 뜻 |\n"
            "|--------------|--------|----|\n"
            "| aud + ience | = audience | 청중 (듣는 사람들) |\n"
            "| aud + ible | = audible | 들을 수 있는 |\n"
            "| aud + io | = audio | 음성, 오디오 |\n"
            "| aud + it | = audit | 감사하다 (들어보다) |\n"
            "| aud + itorium | = auditorium | 강당 (듣는 공간) |\n\n"
            "💡 **auditorium(강당)** 은 '소리를 듣는 공간'이라는 뜻이에요!"
        ),
    },
]

SENTENCES = [
    {
        "title": "어원 scrib - 쓰기의 다양한 표현",
        "level": "중3",
        "sentences": [
            ("Can you describe your hometown?", "당신의 고향을 묘사할 수 있나요?"),
            ("I subscribe to an English podcast.", "나는 영어 팟캐스트를 구독합니다."),
            ("The doctor prescribed rest and medicine.", "의사는 휴식과 약을 처방했습니다."),
        ],
        "related_words": ["describe", "subscribe", "prescribe", "scrib"],
        "tip": "scrib(쓰다) 어근 하나만 알면 세 단어의 뜻을 한번에 유추할 수 있어요!",
    },
    {
        "title": "어원 port - 운반의 다양한 표현",
        "level": "중3",
        "sentences": [
            ("Ships transport goods across the ocean.", "배는 바다를 건너 물건들을 수송합니다."),
            ("Korea exports semiconductors worldwide.", "한국은 전 세계에 반도체를 수출합니다."),
            ("We import coffee beans from Brazil.", "우리는 브라질에서 커피 원두를 수입합니다."),
        ],
        "related_words": ["transport", "export", "import", "port"],
        "tip": "trans(가로질러), ex(밖으로), im(안으로) - 방향을 나타내는 접두사를 외우면 단어가 보여요!",
    },
    {
        "title": "독해 연습 - 과학 기사",
        "level": "중3",
        "sentences": [
            ("Scientists predict a rise in global temperature.", "과학자들은 지구 온도 상승을 예측합니다."),
            ("The audience listened carefully to the lecture.", "청중들은 강의를 주의 깊게 들었습니다."),
            ("His voice was barely audible in the large hall.", "그의 목소리는 큰 홀에서 거의 들리지 않았습니다."),
        ],
        "related_words": ["predict", "audience", "audible", "dict", "aud"],
        "tip": "barely(거의 ~않다)는 부정의 뉘앙스를 가진 부사예요. hardly와 같은 의미!",
    },
]


def w(path, content):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def make_word_template():
    return """\
---
단어:
발음:
품사:
학년: 중3
어원:
유의어: []
반의어: []
---

# 📖 뜻
>

# 🌱 어원 분석 (접두사 + 어근 + 접미사)
> 접두사:
> 어근:
> 접미사:
> 합쳐서 추측:

# 📌 예문
| 영어 | 한국어 |
|------|--------|
|  |  |

# ✏️ 나만의 예문 (직접 써보세요!)
> 예문 1:
> 예문 2:

# 🔗 꼬리에 꼬리를 무는 단어

"""


def make_root_template():
    return """\
---
어원:
출처언어:
뜻:
포함단어: []
---

# 🌳 어원 설명
>

# 📊 어원 활용 표
| 접두사/접미사 | + 어근 | = 단어 | 뜻 |
|--------------|--------|--------|-----|
|  |  |  |  |

# 💡 기억 팁
>

"""


def make_sentence_template():
    return """\
---
제목:
레벨: 중3
관련단어: []
주제:
---

# 📝 문장 모음

| 영어 문장 | 한국어 해석 |
|-----------|-------------|
|  |  |

# 🔍 어휘/문법 분석
>

# ✏️ 내가 만든 문장 (직접 써보세요!)
>

# 📖 독해 포인트
>
"""


def make_word_note(d):
    synonyms = ", ".join([f"[[{s}]]" for s in d["synonyms"]]) if d["synonyms"] else "없음"
    antonyms = ", ".join([f"[[{a}]]" for a in d["antonyms"]]) if d["antonyms"] else "없음"
    related_links = "\n".join([f"- [[{r}]]" for r in d["related"]])

    return f"""\
---
단어: {d['word']}
발음: {d['pronunciation']}
품사: {d['pos']}
학년: {d['grade']}
어원: [[{d['root']}]]
유의어: [{synonyms}]
반의어: [{antonyms}]
---

# 📖 뜻
> **{d['word']}** : {d['meaning']}

# 🌱 어원 분석
> {d['root_meaning']}

# 📌 예문
| 영어 | 한국어 |
|------|--------|
| {d['example_en']} | {d['example_kr']} |

# ✏️ 나만의 예문 (직접 써보세요!)
> 예문 1:
> 예문 2:

# 🔗 꼬리에 꼬리를 무는 단어
{related_links}
"""


def make_root_note(r):
    examples_links = ", ".join([f"[[{e}]]" for e in r["examples"]])
    return f"""\
---
어원: {r['root']}
출처언어: {r['origin']}
뜻: {r['meaning']}
포함단어: [{examples_links}]
---

# 🌳 어원: **{r['root']}** ({r['meaning']})

{r['explanation']}

# 🔗 이 어원이 들어간 모든 단어
{chr(10).join([f'- [[{e}]]' for e in r['examples']])}
"""


def make_sentence_note(s):
    table_rows = "\n".join([f"| {en} | {kr} |" for en, kr in s["sentences"]])
    related_links = ", ".join([f"[[{r}]]" for r in s["related_words"]])
    return f"""\
---
제목: {s['title']}
레벨: {s['level']}
관련단어: [{related_links}]
---

# 📝 {s['title']}

| 영어 문장 | 한국어 해석 |
|-----------|-------------|
{table_rows}

# 💡 어휘/문법 팁
> {s['tip']}

# ✏️ 내가 만든 문장 (직접 써보세요!)
>

"""


def make_home_note():
    return f"""\
# 🏠 하진의 영어 단어 공부 볼트

안녕, 하진아! 👋 이 볼트는 영어 단어를 **어원(어근 + 접두사 + 접미사)으로** 이해하는 공간이야.

## 📁 폴더 구성
- **01_어원** - 단어의 뿌리(어근)를 체계적으로 정리한 곳
- **02_단어** - 어원 연결 단어장 (중3 수준)
- **03_문장** - 어원별 문장 모음 + 독해 연습
- **99_Templates** - 새 노트 만들 때 쓰는 틀

## 🎯 어원 학습의 핵심 원리
> 단어 하나를 외우면 1개를 알지만,
> **어원 하나를 익히면 10개 이상의 단어를 유추할 수 있어!**

## 📚 현재 학습 어원
| 어원 | 뜻 | 예시 단어 |
|------|-----|----------|
| [[scrib]] | 쓰다 | describe, subscribe, prescribe |
| [[port]] | 나르다 | transport, export, import |
| [[dict]] | 말하다 | predict, verdict, dictate |
| [[aud]] | 듣다 | audience, audible, audio |

## 📊 현재 단어 수
- 중3 어원 연결 단어: {len(WORDS)}개

## 🌟 오늘의 목표
> 어원 하나 + 연결 단어 3개 + 나만의 예문 2줄!

"""


def main():
    base = VAULT
    print(f"✅ '{base}' 볼트 생성 시작...")

    for folder in ["01_어원", "02_단어", "03_문장", "99_Templates"]:
        pathlib.Path(f"{base}/{folder}").mkdir(parents=True, exist_ok=True)

    w(f"{base}/🏠 홈.md", make_home_note())

    w(f"{base}/99_Templates/단어_템플릿.md", make_word_template())
    w(f"{base}/99_Templates/어원_템플릿.md", make_root_template())
    w(f"{base}/99_Templates/문장_템플릿.md", make_sentence_template())

    for r in ETYMOLOGIES:
        w(f"{base}/01_어원/{r['root']}.md", make_root_note(r))
        print(f"  📌 어원 노트 생성: {r['root']}")

    for d in WORDS:
        w(f"{base}/02_단어/{d['word']}.md", make_word_note(d))
        print(f"  📖 단어 노트 생성: {d['word']}")

    for s in SENTENCES:
        filename = s["title"].replace(" ", "_")
        w(f"{base}/03_문장/{filename}.md", make_sentence_note(s))
        print(f"  📝 문장 노트 생성: {s['title']}")

    print(f"\n🎉 완료! '{base}' 폴더를 옵시디언에서 'Open folder as vault'로 열어주세요.")
    print("💡 팁: 이 폴더를 iCloud에 복사하면 아이폰에서도 접근할 수 있어요!")


if __name__ == "__main__":
    main()

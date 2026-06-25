#!/usr/bin/env python3
"""
옵시디언 볼트 생성 스크립트 - 하온 버전 (중1)
실행 방법: python3 setup_haon.py
실행 후 생성된 '하온_영어볼트' 폴더를 옵시디언에서 열면 됩니다.
"""

import os
import pathlib

VAULT = "하온_영어볼트"

WORDS = [
    {
        "word": "school",
        "pronunciation": "스쿨",
        "pos": "명사",
        "grade": "중1",
        "meaning": "학교",
        "root": "-er",
        "root_meaning": "어원: 라틴어 schola (토론하는 여가 시간 → 배움의 장소)",
        "synonyms": ["academy", "institute"],
        "antonyms": [],
        "example_en": "I go to school every day.",
        "example_kr": "나는 매일 학교에 갑니다.",
        "related": ["teacher", "study", "book"],
    },
    {
        "word": "book",
        "pronunciation": "북",
        "pos": "명사",
        "grade": "중1",
        "meaning": "책",
        "root": "",
        "root_meaning": "어원: 고대 영어 bōc (너도밤나무 껍질 → 글을 쓰는 재료)",
        "synonyms": ["volume", "text"],
        "antonyms": [],
        "example_en": "She reads a book every night.",
        "example_kr": "그녀는 매일 밤 책을 읽습니다.",
        "related": ["study", "school"],
    },
    {
        "word": "friend",
        "pronunciation": "프렌드",
        "pos": "명사",
        "grade": "중1",
        "meaning": "친구",
        "root": "",
        "root_meaning": "어원: 고대 영어 frēond (사랑하는 사람)",
        "synonyms": ["pal", "buddy", "companion"],
        "antonyms": ["enemy", "foe"],
        "example_en": "My friend and I play soccer after school.",
        "example_kr": "내 친구와 나는 방과 후에 축구를 합니다.",
        "related": ["school", "play"],
    },
    {
        "word": "teacher",
        "pronunciation": "티처",
        "pos": "명사",
        "grade": "중1",
        "meaning": "선생님",
        "root": "-er",
        "root_meaning": "어원: teach(가르치다) + -er(~하는 사람). -er이 붙으면 '~하는 사람'이 됩니다.",
        "synonyms": ["instructor", "educator"],
        "antonyms": ["student", "pupil"],
        "example_en": "Our teacher explains the lesson clearly.",
        "example_kr": "우리 선생님은 수업을 명확하게 설명합니다.",
        "related": ["-er", "school", "study"],
    },
    {
        "word": "study",
        "pronunciation": "스터디",
        "pos": "동사/명사",
        "grade": "중1",
        "meaning": "공부하다 / 공부",
        "root": "",
        "root_meaning": "어원: 라틴어 studium (열심히 노력하다, 열중하다)",
        "synonyms": ["learn", "review"],
        "antonyms": ["ignore", "neglect"],
        "example_en": "I study English every day.",
        "example_kr": "나는 매일 영어를 공부합니다.",
        "related": ["school", "book", "teacher"],
    },
    {
        "word": "eat",
        "pronunciation": "잇",
        "pos": "동사",
        "grade": "중1",
        "meaning": "먹다",
        "root": "",
        "root_meaning": "어원: 고대 영어 etan (음식을 먹다)",
        "synonyms": ["have", "consume"],
        "antonyms": ["fast", "starve"],
        "example_en": "We eat lunch together at school.",
        "example_kr": "우리는 학교에서 함께 점심을 먹습니다.",
        "related": ["drink", "friend"],
    },
    {
        "word": "drink",
        "pronunciation": "드링크",
        "pos": "동사/명사",
        "grade": "중1",
        "meaning": "마시다 / 음료",
        "root": "",
        "root_meaning": "어원: 고대 영어 drincan (액체를 마시다)",
        "synonyms": ["sip", "consume"],
        "antonyms": ["fast"],
        "example_en": "I drink water after exercise.",
        "example_kr": "나는 운동 후에 물을 마십니다.",
        "related": ["eat"],
    },
    {
        "word": "walk",
        "pronunciation": "워크",
        "pos": "동사/명사",
        "grade": "중1",
        "meaning": "걷다 / 걷기",
        "root": "",
        "root_meaning": "어원: 고대 영어 wealcan (구르다, 걷다)",
        "synonyms": ["stroll", "march"],
        "antonyms": ["run", "drive"],
        "example_en": "I walk to school with my friend.",
        "example_kr": "나는 친구와 함께 걸어서 학교에 갑니다.",
        "related": ["school", "friend"],
    },
    {
        "word": "play",
        "pronunciation": "플레이",
        "pos": "동사/명사",
        "grade": "중1",
        "meaning": "놀다 / 경기하다",
        "root": "-er",
        "root_meaning": "어원: 고대 영어 plegian (운동하다, 즐기다). play + -er = player(선수)",
        "synonyms": ["enjoy", "have fun"],
        "antonyms": ["work", "study"],
        "related": ["-er", "friend", "happy"],
        "example_en": "We play soccer every weekend.",
        "example_kr": "우리는 매주 주말에 축구를 합니다.",
    },
    {
        "word": "happy",
        "pronunciation": "해피",
        "pos": "형용사",
        "grade": "중1",
        "meaning": "행복한, 기쁜",
        "root": "",
        "root_meaning": "어원: 중세 영어 hap (운, 행운) + -py. '운이 좋은 상태'에서 '행복한'으로 의미가 확장",
        "synonyms": ["glad", "joyful", "pleased"],
        "antonyms": ["sad", "unhappy", "upset"],
        "example_en": "I feel happy when I play with my friends.",
        "example_kr": "나는 친구들과 놀 때 행복함을 느낍니다.",
        "related": ["friend", "play"],
    },
]

ETYMOLOGIES = [
    {
        "root": "-er",
        "origin": "고대 영어 / 라틴어",
        "meaning": "~하는 사람, ~하는 것",
        "examples": ["teacher", "player", "runner", "writer", "singer"],
        "explanation": (
            "-er은 동사 뒤에 붙어 '~하는 사람' 또는 '~하는 것'을 만드는 접미사입니다.\n"
            "teach(가르치다) → teacher(선생님)\n"
            "play(놀다) → player(선수)\n"
            "run(달리다) → runner(달리기 선수)\n"
            "write(쓰다) → writer(작가)\n"
            "이 규칙을 알면 모르는 단어도 뜻을 추측할 수 있어요!"
        ),
    },
]

SENTENCES = [
    {
        "title": "학교 가는 아침",
        "level": "중1",
        "sentences": [
            ("I walk to school with my friend.", "나는 친구와 함께 걸어서 학교에 갑니다."),
            ("We eat breakfast before school.", "우리는 학교 가기 전에 아침을 먹습니다."),
            ("My teacher is very kind.", "우리 선생님은 매우 친절합니다."),
        ],
        "related_words": ["walk", "school", "friend", "eat", "teacher"],
        "tip": "before(~하기 전에)는 시간을 나타낼 때 자주 쓰여요!",
    },
    {
        "title": "방과 후 시간",
        "level": "중1",
        "sentences": [
            ("After school, I play soccer with my friends.", "방과 후, 나는 친구들과 축구를 합니다."),
            ("Then we drink water and feel happy.", "그러고 나서 우리는 물을 마시고 행복함을 느낍니다."),
            ("I study English at home.", "나는 집에서 영어를 공부합니다."),
        ],
        "related_words": ["play", "friend", "drink", "happy", "study"],
        "tip": "Then(그러고 나서)을 쓰면 이야기의 순서를 자연스럽게 연결할 수 있어요!",
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
학년: 중1
어원:
유의어: []
반의어: []
---

# 📖 뜻
>

# 🌱 어원으로 추측하기
>

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

# 📚 이 어원이 들어간 단어들
>

# 💡 어원 활용 팁
>

"""


def make_sentence_template():
    return """\
---
제목:
레벨: 중1
관련단어: []
---

# 📝 문장 모음

| 영어 문장 | 한국어 해석 |
|-----------|-------------|
|  |  |

# 💡 문법/표현 팁
>

# ✏️ 내가 만든 문장 (직접 써보세요!)
>

"""


def make_word_note(w_data):
    synonyms = ", ".join([f"[[{s}]]" for s in w_data["synonyms"]]) if w_data["synonyms"] else "없음"
    antonyms = ", ".join([f"[[{a}]]" for a in w_data["antonyms"]]) if w_data["antonyms"] else "없음"
    related_links = "\n".join([f"- [[{r}]]" for r in w_data["related"]])
    root_field = f"[[{w_data['root']}]]" if w_data["root"] else "없음"

    return f"""\
---
단어: {w_data['word']}
발음: {w_data['pronunciation']}
품사: {w_data['pos']}
학년: {w_data['grade']}
어원: {root_field}
유의어: [{synonyms}]
반의어: [{antonyms}]
---

# 📖 뜻
> **{w_data['word']}** : {w_data['meaning']}

# 🌱 어원으로 추측하기
> {w_data['root_meaning']}

# 📌 예문
| 영어 | 한국어 |
|------|--------|
| {w_data['example_en']} | {w_data['example_kr']} |

# ✏️ 나만의 예문 (직접 써보세요!)
> 예문 1:
> 예문 2:

# 🔗 꼬리에 꼬리를 무는 단어
{related_links}
"""


def make_root_note(r_data):
    examples_links = ", ".join([f"[[{e}]]" for e in r_data["examples"]])
    return f"""\
---
어원: {r_data['root']}
출처언어: {r_data['origin']}
뜻: {r_data['meaning']}
포함단어: [{examples_links}]
---

# 🌳 어원 설명
> **{r_data['root']}** 은(는) "{r_data['meaning']}"을(를) 뜻합니다.

# 📚 이 어원이 들어간 단어들
{chr(10).join([f'- [[{e}]]' for e in r_data['examples']])}

# 💡 어원 활용 팁
{r_data['explanation']}
"""


def make_sentence_note(s_data):
    table_rows = "\n".join([f"| {en} | {kr} |" for en, kr in s_data["sentences"]])
    related_links = ", ".join([f"[[{r}]]" for r in s_data["related_words"]])
    return f"""\
---
제목: {s_data['title']}
레벨: {s_data['level']}
관련단어: [{related_links}]
---

# 📝 {s_data['title']}

| 영어 문장 | 한국어 해석 |
|-----------|-------------|
{table_rows}

# 💡 문법/표현 팁
> {s_data['tip']}

# ✏️ 내가 만든 문장 (직접 써보세요!)
>

"""


def make_home_note():
    return f"""\
# 🏠 하온의 영어 단어 공부 볼트

안녕, 하온아! 👋 이 볼트는 영어 단어를 **뿌리부터** 이해하며 익히는 공간이야.

## 📁 폴더 구성
- **[[01_어원]]** - 단어의 뿌리(어원)를 모아놓은 곳
- **[[02_단어]]** - 단어장 (중1 기초 단어부터!)
- **[[03_문장]]** - 단어가 쓰인 실제 문장 모음
- **[[99_Templates]]** - 새 노트 만들 때 쓰는 틀

## 🎯 이 볼트 사용법
1. 새 단어를 배우면 `02_단어` 폴더에 노트를 만들어
2. 어원이 연결되면 `01_어원` 노트로 링크를 걸어
3. 문장을 만들면 `03_문장` 폴더에 추가해
4. 그래프 뷰(Graph view)를 열면 단어들이 어떻게 연결되는지 한눈에 볼 수 있어!

## 📊 현재 단어 수
- 중1 기초 단어: {len(WORDS)}개

## 🌟 오늘의 목표
> 하루에 단어 하나씩, 나만의 예문 한 줄씩!

"""


def main():
    base = VAULT
    print(f"✅ '{base}' 볼트 생성 시작...")

    # 폴더 구조 생성
    for folder in ["01_어원", "02_단어", "03_문장", "99_Templates"]:
        pathlib.Path(f"{base}/{folder}").mkdir(parents=True, exist_ok=True)

    # 홈 노트
    w(f"{base}/🏠 홈.md", make_home_note())

    # 템플릿 파일
    w(f"{base}/99_Templates/단어_템플릿.md", make_word_template())
    w(f"{base}/99_Templates/어원_템플릿.md", make_root_template())
    w(f"{base}/99_Templates/문장_템플릿.md", make_sentence_template())

    # 어원 노트 생성
    for r in ETYMOLOGIES:
        w(f"{base}/01_어원/{r['root']}.md", make_root_note(r))
        print(f"  📌 어원 노트 생성: {r['root']}")

    # 단어 노트 생성
    for word_data in WORDS:
        w(f"{base}/02_단어/{word_data['word']}.md", make_word_note(word_data))
        print(f"  📖 단어 노트 생성: {word_data['word']}")

    # 문장 노트 생성
    for s in SENTENCES:
        filename = s["title"].replace(" ", "_")
        w(f"{base}/03_문장/{filename}.md", make_sentence_note(s))
        print(f"  📝 문장 노트 생성: {s['title']}")

    print(f"\n🎉 완료! '{base}' 폴더를 옵시디언에서 'Open folder as vault'로 열어주세요.")
    print("💡 팁: 이 폴더를 iCloud에 복사하면 아이폰에서도 접근할 수 있어요!")


if __name__ == "__main__":
    main()

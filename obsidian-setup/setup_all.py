#!/usr/bin/env python3
"""
하온 + 하진 영어 볼트 생성 스크립트 (맥북 실행용)
iCloud를 통해 아이패드에서 바로 사용 가능

실행 방법:
  python3 setup_all.py

아이패드 사용법:
  1. 앱스토어에서 'Obsidian' 설치
  2. Obsidian 실행 → "Open folder as vault" 선택
  3. iCloud Drive → Obsidian 폴더에서 볼트 선택
"""

import os
import sys
import pathlib
import shutil
import subprocess

# ─────────────────────────────────────────────
# iCloud 경로 자동 감지
# ─────────────────────────────────────────────
ICLOUD_OBSIDIAN = pathlib.Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents"
LOCAL_FALLBACK  = pathlib.Path.home() / "Desktop"


def detect_output_dir():
    if ICLOUD_OBSIDIAN.exists():
        return ICLOUD_OBSIDIAN
    # iCloud Obsidian 앱 폴더가 없으면 일반 iCloud Drive 시도
    icloud_generic = pathlib.Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Obsidian"
    if (pathlib.Path.home() / "Library/Mobile Documents/com~apple~CloudDocs").exists():
        icloud_generic.mkdir(parents=True, exist_ok=True)
        return icloud_generic
    return LOCAL_FALLBACK


def w(path, content):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ─────────────────────────────────────────────
# 하온 (중1) 데이터
# ─────────────────────────────────────────────
HAON_WORDS = [
    dict(word="school", pronunciation="스쿨", pos="명사", grade="중1", meaning="학교",
         root="-er", root_meaning="어원: 라틴어 schola (토론하는 여가 시간 → 배움의 장소)",
         synonyms=["academy"], antonyms=[],
         example_en="I go to school every day.", example_kr="나는 매일 학교에 갑니다.",
         related=["-er", "study", "book"]),
    dict(word="book", pronunciation="북", pos="명사", grade="중1", meaning="책",
         root="", root_meaning="어원: 고대 영어 bōc (너도밤나무 껍질 → 글 쓰는 재료)",
         synonyms=["volume"], antonyms=[],
         example_en="She reads a book every night.", example_kr="그녀는 매일 밤 책을 읽습니다.",
         related=["study", "school"]),
    dict(word="friend", pronunciation="프렌드", pos="명사", grade="중1", meaning="친구",
         root="", root_meaning="어원: 고대 영어 frēond (사랑하는 사람)",
         synonyms=["pal", "buddy"], antonyms=["enemy"],
         example_en="My friend and I play soccer after school.", example_kr="내 친구와 나는 방과 후에 축구를 합니다.",
         related=["school", "play"]),
    dict(word="teacher", pronunciation="티처", pos="명사", grade="중1", meaning="선생님",
         root="-er", root_meaning="teach(가르치다) + -er(~하는 사람). -er이 붙으면 '~하는 사람'이 됩니다.",
         synonyms=["instructor"], antonyms=["student"],
         example_en="Our teacher explains the lesson clearly.", example_kr="우리 선생님은 수업을 명확하게 설명합니다.",
         related=["-er", "school", "study"]),
    dict(word="study", pronunciation="스터디", pos="동사/명사", grade="중1", meaning="공부하다 / 공부",
         root="", root_meaning="어원: 라틴어 studium (열심히 노력하다, 열중하다)",
         synonyms=["learn"], antonyms=["ignore"],
         example_en="I study English every day.", example_kr="나는 매일 영어를 공부합니다.",
         related=["school", "book", "teacher"]),
    dict(word="eat", pronunciation="잇", pos="동사", grade="중1", meaning="먹다",
         root="", root_meaning="어원: 고대 영어 etan (음식을 먹다)",
         synonyms=["have", "consume"], antonyms=["fast"],
         example_en="We eat lunch together at school.", example_kr="우리는 학교에서 함께 점심을 먹습니다.",
         related=["drink", "friend"]),
    dict(word="drink", pronunciation="드링크", pos="동사/명사", grade="중1", meaning="마시다 / 음료",
         root="", root_meaning="어원: 고대 영어 drincan (액체를 마시다)",
         synonyms=["sip"], antonyms=[],
         example_en="I drink water after exercise.", example_kr="나는 운동 후에 물을 마십니다.",
         related=["eat"]),
    dict(word="walk", pronunciation="워크", pos="동사/명사", grade="중1", meaning="걷다 / 걷기",
         root="", root_meaning="어원: 고대 영어 wealcan (구르다, 걷다)",
         synonyms=["stroll"], antonyms=["run"],
         example_en="I walk to school with my friend.", example_kr="나는 친구와 함께 걸어서 학교에 갑니다.",
         related=["school", "friend"]),
    dict(word="play", pronunciation="플레이", pos="동사/명사", grade="중1", meaning="놀다 / 경기하다",
         root="-er", root_meaning="어원: 고대 영어 plegian (즐기다). play + -er = player(선수)",
         synonyms=["enjoy"], antonyms=["work", "study"],
         example_en="We play soccer every weekend.", example_kr="우리는 매주 주말에 축구를 합니다.",
         related=["-er", "friend", "happy"]),
    dict(word="happy", pronunciation="해피", pos="형용사", grade="중1", meaning="행복한, 기쁜",
         root="", root_meaning="어원: 중세 영어 hap (운, 행운) + -py. '운이 좋은' → '행복한'",
         synonyms=["glad", "joyful"], antonyms=["sad", "unhappy"],
         example_en="I feel happy when I play with my friends.", example_kr="나는 친구들과 놀 때 행복함을 느낍니다.",
         related=["friend", "play"]),
]

HAON_ETYMOLOGIES = [
    dict(root="-er", origin="고대 영어 / 라틴어", meaning="~하는 사람, ~하는 것",
         examples=["teacher", "player", "runner", "writer", "singer"],
         explanation=(
             "-er은 동사 뒤에 붙어 '~하는 사람'을 만드는 접미사입니다.\n\n"
             "| 동사 | + -er | = 단어 | 뜻 |\n"
             "|------|-------|--------|----|\n"
             "| teach | + -er | = teacher | 선생님 |\n"
             "| play | + -er | = player | 선수 |\n"
             "| run | + -er | = runner | 달리기 선수 |\n"
             "| write | + -er | = writer | 작가 |\n\n"
             "💡 이 규칙 하나만 알면 모르는 단어도 뜻을 추측할 수 있어요!"
         )),
]

HAON_SENTENCES = [
    dict(title="학교 가는 아침", level="중1",
         sentences=[
             ("I walk to school with my friend.", "나는 친구와 함께 걸어서 학교에 갑니다."),
             ("We eat breakfast before school.", "우리는 학교 가기 전에 아침을 먹습니다."),
             ("My teacher is very kind.", "우리 선생님은 매우 친절합니다."),
         ],
         related_words=["walk", "school", "friend", "eat", "teacher"],
         tip="before(~하기 전에)는 시간을 나타낼 때 자주 쓰여요!"),
    dict(title="방과 후 시간", level="중1",
         sentences=[
             ("After school, I play soccer with my friends.", "방과 후, 나는 친구들과 축구를 합니다."),
             ("Then we drink water and feel happy.", "그러고 나서 우리는 물을 마시고 행복함을 느낍니다."),
             ("I study English at home.", "나는 집에서 영어를 공부합니다."),
         ],
         related_words=["play", "friend", "drink", "happy", "study"],
         tip="Then(그러고 나서)을 쓰면 이야기 순서를 자연스럽게 연결할 수 있어요!"),
]

# ─────────────────────────────────────────────
# 하진 (중3) 데이터
# ─────────────────────────────────────────────
HAJIN_WORDS = [
    dict(word="describe", pronunciation="디스크라이브", pos="동사", grade="중3", meaning="묘사하다, 설명하다",
         root="scrib", root_meaning="de(완전히) + scrib(쓰다) + e → '완전히 써내다' → 묘사하다",
         synonyms=["explain", "depict"], antonyms=[],
         example_en="Can you describe what you saw?", example_kr="당신이 본 것을 묘사할 수 있나요?",
         related=["scrib", "subscribe", "prescribe"]),
    dict(word="subscribe", pronunciation="섭스크라이브", pos="동사", grade="중3", meaning="구독하다, 서명하다",
         root="scrib", root_meaning="sub(아래에) + scrib(쓰다) + e → '아래에 이름을 쓰다' → 구독/서명",
         synonyms=["sign up"], antonyms=["unsubscribe"],
         example_en="Please subscribe to our channel.", example_kr="우리 채널을 구독해 주세요.",
         related=["scrib", "describe", "prescribe"]),
    dict(word="prescribe", pronunciation="프리스크라이브", pos="동사", grade="중3", meaning="처방하다, 규정하다",
         root="scrib", root_meaning="pre(미리) + scrib(쓰다) + e → '미리 써두다' → 처방하다",
         synonyms=["recommend", "order"], antonyms=[],
         example_en="The doctor prescribed medicine for my cold.", example_kr="의사는 내 감기를 위해 약을 처방했습니다.",
         related=["scrib", "describe", "subscribe"]),
    dict(word="transport", pronunciation="트랜스포트", pos="동사/명사", grade="중3", meaning="수송하다 / 교통수단",
         root="port", root_meaning="trans(가로질러) + port(나르다) → '한 곳에서 다른 곳으로 나르다'",
         synonyms=["carry", "ship"], antonyms=[],
         example_en="Ships transport goods across the ocean.", example_kr="배는 물건들을 바다를 건너 수송합니다.",
         related=["port", "export", "import"]),
    dict(word="export", pronunciation="엑스포트", pos="동사/명사", grade="중3", meaning="수출하다 / 수출",
         root="port", root_meaning="ex(밖으로) + port(나르다) → '밖으로 내보내다' → 수출",
         synonyms=["ship out"], antonyms=["import"],
         example_en="Korea exports many electronic products.", example_kr="한국은 많은 전자 제품을 수출합니다.",
         related=["port", "import", "transport"]),
    dict(word="import", pronunciation="임포트", pos="동사/명사", grade="중3", meaning="수입하다 / 수입",
         root="port", root_meaning="im(안으로) + port(나르다) → '안으로 들여오다' → 수입",
         synonyms=["bring in"], antonyms=["export"],
         example_en="We import oil from other countries.", example_kr="우리는 다른 나라에서 석유를 수입합니다.",
         related=["port", "export", "transport"]),
    dict(word="predict", pronunciation="프리딕트", pos="동사", grade="중3", meaning="예측하다, 예언하다",
         root="dict", root_meaning="pre(미리) + dict(말하다) → '미리 말하다' → 예측하다",
         synonyms=["forecast", "anticipate"], antonyms=[],
         example_en="Scientists predict the weather using data.", example_kr="과학자들은 데이터로 날씨를 예측합니다.",
         related=["dict", "verdict", "dictate"]),
    dict(word="verdict", pronunciation="버딕트", pos="명사", grade="중3", meaning="평결, 판결",
         root="dict", root_meaning="ver(진실) + dict(말하다) → '진실을 말하다' → 판결",
         synonyms=["judgment", "ruling"], antonyms=[],
         example_en="The jury delivered a not-guilty verdict.", example_kr="배심원단은 무죄 평결을 내렸습니다.",
         related=["dict", "predict", "dictate"]),
    dict(word="audience", pronunciation="오디언스", pos="명사", grade="중3", meaning="청중, 관중",
         root="aud", root_meaning="aud(듣다) + ience(집합) → '듣는 사람들의 집합' → 청중",
         synonyms=["spectators", "crowd"], antonyms=[],
         example_en="The audience applauded after the performance.", example_kr="공연이 끝난 후 청중이 박수를 쳤습니다.",
         related=["aud", "audible", "audio"]),
    dict(word="audible", pronunciation="오디블", pos="형용사", grade="중3", meaning="들을 수 있는",
         root="aud", root_meaning="aud(듣다) + ible(~할 수 있는) → '들을 수 있는'",
         synonyms=["hearable"], antonyms=["inaudible"],
         example_en="His voice was barely audible in the crowd.", example_kr="군중 속에서 그의 목소리는 거의 들리지 않았습니다.",
         related=["aud", "audience", "audio"]),
]

HAJIN_ETYMOLOGIES = [
    dict(root="scrib", origin="라틴어 scribere", meaning="쓰다 (to write)",
         examples=["describe", "subscribe", "prescribe", "inscribe", "manuscript"],
         explanation=(
             "**scrib/scrip** 은 '쓰다(write)'를 의미하는 라틴어 어근입니다.\n\n"
             "| 접두사 | + scrib | = 단어 | 뜻 |\n"
             "|--------|---------|--------|----|\n"
             "| de (완전히) | + scrib | = describe | 묘사하다 |\n"
             "| sub (아래) | + scrib | = subscribe | 구독하다 |\n"
             "| pre (미리) | + scrib | = prescribe | 처방하다 |\n"
             "| in (안에) | + scrib | = inscribe | 새기다 |\n\n"
             "💡 **script(대본)** 도 같은 어근! '쓰여진 것'이라는 뜻이에요."
         )),
    dict(root="port", origin="라틴어 portare", meaning="나르다, 운반하다 (to carry)",
         examples=["transport", "export", "import", "support", "report", "portable"],
         explanation=(
             "**port** 는 '나르다(carry)'를 의미하는 라틴어 어근입니다.\n\n"
             "| 접두사 | + port | = 단어 | 뜻 |\n"
             "|--------|--------|--------|----|\n"
             "| trans (가로질러) | + port | = transport | 수송하다 |\n"
             "| ex (밖으로) | + port | = export | 수출하다 |\n"
             "| im (안으로) | + port | = import | 수입하다 |\n"
             "| re (다시/뒤로) | + port | = report | 보고하다 |\n\n"
             "💡 **portable(휴대용)** 도 같은 어근! '들고 다닐 수 있는'이라는 뜻이에요."
         )),
    dict(root="dict", origin="라틴어 dicere", meaning="말하다 (to say)",
         examples=["predict", "verdict", "dictate", "indicate", "contradict"],
         explanation=(
             "**dict** 는 '말하다(say)'를 의미하는 라틴어 어근입니다.\n\n"
             "| 접두사 | + dict | = 단어 | 뜻 |\n"
             "|--------|--------|--------|----|\n"
             "| pre (미리) | + dict | = predict | 예측하다 |\n"
             "| ver (진실) | + dict | = verdict | 평결 |\n"
             "| contra (반대) | + dict | = contradict | 반박하다 |\n\n"
             "💡 **dictionary(사전)** 도 같은 어근! '말들을 모아둔 책'이에요."
         )),
    dict(root="aud", origin="라틴어 audire", meaning="듣다 (to hear)",
         examples=["audience", "audible", "audio", "audit", "auditorium"],
         explanation=(
             "**aud** 는 '듣다(hear)'를 의미하는 라틴어 어근입니다.\n\n"
             "| 어근 + 접미사 | = 단어 | 뜻 |\n"
             "|--------------|--------|----|\n"
             "| aud + ience | = audience | 청중 |\n"
             "| aud + ible | = audible | 들을 수 있는 |\n"
             "| aud + io | = audio | 음성, 오디오 |\n"
             "| aud + itorium | = auditorium | 강당 |\n\n"
             "💡 **auditorium(강당)** 은 '소리를 듣는 공간'이에요!"
         )),
]

HAJIN_SENTENCES = [
    dict(title="어원 scrib - 쓰기의 다양한 표현", level="중3",
         sentences=[
             ("Can you describe your hometown?", "당신의 고향을 묘사할 수 있나요?"),
             ("I subscribe to an English podcast.", "나는 영어 팟캐스트를 구독합니다."),
             ("The doctor prescribed rest and medicine.", "의사는 휴식과 약을 처방했습니다."),
         ],
         related_words=["describe", "subscribe", "prescribe", "scrib"],
         tip="scrib(쓰다) 어근 하나만 알면 세 단어의 뜻을 한번에 유추할 수 있어요!"),
    dict(title="어원 port - 운반의 다양한 표현", level="중3",
         sentences=[
             ("Ships transport goods across the ocean.", "배는 바다를 건너 물건들을 수송합니다."),
             ("Korea exports semiconductors worldwide.", "한국은 전 세계에 반도체를 수출합니다."),
             ("We import coffee beans from Brazil.", "우리는 브라질에서 커피 원두를 수입합니다."),
         ],
         related_words=["transport", "export", "import", "port"],
         tip="trans(가로질러), ex(밖으로), im(안으로) - 방향 접두사를 외우면 단어가 보여요!"),
    dict(title="독해 연습 - 과학 기사", level="중3",
         sentences=[
             ("Scientists predict a rise in global temperature.", "과학자들은 지구 온도 상승을 예측합니다."),
             ("The audience listened carefully to the lecture.", "청중들은 강의를 주의 깊게 들었습니다."),
             ("His voice was barely audible in the large hall.", "그의 목소리는 큰 홀에서 거의 들리지 않았습니다."),
         ],
         related_words=["predict", "audience", "audible", "dict", "aud"],
         tip="barely(거의 ~않다)는 부정 뉘앙스 부사예요. hardly와 같은 의미!"),
]


# ─────────────────────────────────────────────
# 노트 생성 함수
# ─────────────────────────────────────────────
def make_word_note(d):
    synonyms = ", ".join([f"[[{s}]]" for s in d["synonyms"]]) if d["synonyms"] else "없음"
    antonyms = ", ".join([f"[[{a}]]" for a in d["antonyms"]]) if d["antonyms"] else "없음"
    related_links = "\n".join([f"- [[{r}]]" for r in d["related"]])
    root_field = f"[[{d['root']}]]" if d["root"] else "없음"
    return f"""\
---
단어: {d['word']}
발음: {d['pronunciation']}
품사: {d['pos']}
학년: {d['grade']}
어원: {root_field}
유의어: [{synonyms}]
반의어: [{antonyms}]
---

# 📖 뜻
> **{d['word']}** : {d['meaning']}

# 🌱 어원으로 추측하기
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

# 🔗 이 어원이 들어간 단어들
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

# 💡 팁
> {s['tip']}

# ✏️ 내가 만든 문장 (직접 써보세요!)
>
"""


def make_haon_home():
    return """\
# 🏠 하온의 영어 단어 볼트 (중1)

안녕, 하온아! 👋 영어 단어를 **뿌리부터** 이해하며 익히는 공간이야.

## 📁 폴더 구성
- **01_어원** - 단어의 뿌리(어원)를 모아놓은 곳
- **02_단어** - 단어장 (중1 기초 단어부터!)
- **03_문장** - 단어가 쓰인 실제 문장 모음
- **99_Templates** - 새 노트 만들 때 쓰는 틀

## 🎯 사용법
1. 새 단어를 배우면 `02_단어` 폴더에 노트를 만들어
2. 어원이 연결되면 `01_어원` 노트로 링크를 걸어
3. 그래프 뷰(Graph view)를 열면 단어들의 연결이 한눈에 보여!

## 📊 현재 어원
| 어원 | 뜻 | 예시 |
|------|-----|------|
| [[-er]] | ~하는 사람 | teacher, player, writer |

## 🌟 오늘의 목표
> 하루에 단어 하나씩, 나만의 예문 한 줄씩!
"""


def make_hajin_home():
    return """\
# 🏠 하진의 영어 단어 볼트 (중3)

안녕, 하진아! 👋 영어 단어를 **어원(어근 + 접두사 + 접미사)으로** 이해하는 공간이야.

## 📁 폴더 구성
- **01_어원** - 어근을 체계적으로 정리한 곳
- **02_단어** - 어원 연결 단어장 (중3 수준)
- **03_문장** - 어원별 문장 모음 + 독해 연습
- **99_Templates** - 새 노트 만들 때 쓰는 틀

## 🎯 어원 학습의 핵심
> 단어 하나를 외우면 1개를 알지만,
> **어원 하나를 익히면 10개 이상을 유추할 수 있어!**

## 📚 현재 학습 어원
| 어원 | 뜻 | 예시 단어 |
|------|-----|----------|
| [[scrib]] | 쓰다 | describe, subscribe, prescribe |
| [[port]] | 나르다 | transport, export, import |
| [[dict]] | 말하다 | predict, verdict, contradict |
| [[aud]] | 듣다 | audience, audible, audio |

## 🌟 오늘의 목표
> 어원 하나 + 연결 단어 3개 + 나만의 예문 2줄!
"""


WORD_TEMPLATE = """\
---
단어:
발음:
품사:
학년:
어원:
유의어: []
반의어: []
---

# 📖 뜻
>

# 🌱 어원으로 추측하기
>

# 📌 예문
| 영어 | 한국어 |
|------|--------|
|  |  |

# ✏️ 나만의 예문 (직접 써보세요!)
> 예문 1:
> 예문 2:

# 🔗 꼬리에 꼬리를 무는 단어

"""

ROOT_TEMPLATE = """\
---
어원:
출처언어:
뜻:
포함단어: []
---

# 🌳 어원 설명
>

# 📊 어원 활용 표
| 접두사 | + 어근 | = 단어 | 뜻 |
|--------|--------|--------|-----|

# 💡 기억 팁
>
"""

SENTENCE_TEMPLATE = """\
---
제목:
레벨:
관련단어: []
---

# 📝 문장 모음

| 영어 문장 | 한국어 해석 |
|-----------|-------------|
|  |  |

# 💡 팁
>

# ✏️ 내가 만든 문장 (직접 써보세요!)
>
"""


# ─────────────────────────────────────────────
# 볼트 생성 함수
# ─────────────────────────────────────────────
def build_vault(base, words, etymologies, sentences, home_content):
    base = pathlib.Path(base)
    for folder in ["01_어원", "02_단어", "03_문장", "99_Templates"]:
        (base / folder).mkdir(parents=True, exist_ok=True)

    w(base / "🏠 홈.md", home_content)
    w(base / "99_Templates" / "단어_템플릿.md", WORD_TEMPLATE)
    w(base / "99_Templates" / "어원_템플릿.md", ROOT_TEMPLATE)
    w(base / "99_Templates" / "문장_템플릿.md", SENTENCE_TEMPLATE)

    for r in etymologies:
        w(base / "01_어원" / f"{r['root']}.md", make_root_note(r))

    for d in words:
        w(base / "02_단어" / f"{d['word']}.md", make_word_note(d))

    for s in sentences:
        fname = s["title"].replace(" ", "_").replace("/", "-") + ".md"
        w(base / "03_문장" / fname, make_sentence_note(s))


# ─────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────
def main():
    out_dir = detect_output_dir()

    print("=" * 50)
    print("  옵시디언 영어 볼트 생성기 (아이패드 연동)")
    print("=" * 50)
    print(f"\n📂 저장 위치: {out_dir}\n")

    # 하온 볼트
    haon_path = out_dir / "하온_영어볼트"
    print("📗 하온 볼트 생성 중 (중1)...")
    build_vault(haon_path, HAON_WORDS, HAON_ETYMOLOGIES, HAON_SENTENCES, make_haon_home())
    print(f"   ✅ 완료: {haon_path}")

    # 하진 볼트
    hajin_path = out_dir / "하진_영어볼트"
    print("📘 하진 볼트 생성 중 (중3)...")
    build_vault(hajin_path, HAJIN_WORDS, HAJIN_ETYMOLOGIES, HAJIN_SENTENCES, make_hajin_home())
    print(f"   ✅ 완료: {hajin_path}")

    print()
    print("=" * 50)
    print("  아이패드 연동 방법")
    print("=" * 50)
    print("""
1. 아이패드 앱스토어에서 'Obsidian' 설치
2. Obsidian 실행
3. "Open folder as vault" 선택
4. iCloud Drive → Obsidian 폴더 안에서
   '하온_영어볼트' 또는 '하진_영어볼트' 선택
5. Allow 탭 → 완료!

⚠️  볼트가 iCloud에 안 보일 경우:
   아이패드 설정 → [내 이름] → iCloud → Obsidian 동기화 ON
""")

    # Finder에서 저장 위치 열기 (맥북에서 실행 시)
    if sys.platform == "darwin":
        try:
            subprocess.run(["open", str(out_dir)], check=True)
            print(f"📂 Finder에서 저장 위치를 열었습니다.")
        except Exception:
            pass


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
expand_stories_g5.py — Expand story sections in all 108 G5 lesson files.
G5 uses THREE English levels: A1 + A2 + B1.
"""
import re, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Book assignments ──
BOOKS = {
    range(1,10):  ("Treasure Island", "보물섬"),
    range(10,19): ("Around the World in 80 Days", "80일간의 세계일주"),
    range(19,28): ("The Call of the Wild", "야생의 부름"),
    range(28,33): ("Anne of Green Gables", "빨간 머리 앤"),
    range(33,37): ("Swiss Family Robinson", "스위스 가족 로빈슨"),
}

def get_book(wk):
    for r, (en, kr) in BOOKS.items():
        if wk in r:
            return en, kr
    return "Unknown", "알 수 없음"

DAY_MAP = {"a": "Day1", "b": "Day2", "c": "Day3"}
DAY_LABEL = {"a": "월요일", "b": "수요일", "c": "금요일"}

# ── Weekly themes ──
WEEK_THEMES = {
    1: ("map", "짐이 죽은 선원의 상자에서 보물 지도를 발견하다"),
    2: ("choice", "짐이 보물섬으로 가기로 결심하다"),
    3: ("Long John Silver", "짐이 한 다리 요리사 존 실버를 만나다"),
    4: ("trust", "짐이 누구를 믿어야 할지 고민하다"),
    5: ("bravery", "짐이 해적들 앞에서 용기를 내다"),
    6: ("greed", "해적들이 욕심 때문에 서로 다투다"),
    7: ("courage", "짐이 홀로 배를 되찾기 위해 행동하다"),
    8: ("thinking", "짐이 지혜로 위기를 넘기다"),
    9: ("lessons", "보물섬에서 배운 교훈을 되새기다"),
    10: ("bold bet", "포그가 80일 안에 세계를 돌겠다고 내기하다"),
    11: ("every minute", "시간이 촉박한 여정이 시작되다"),
    12: ("loyal", "충실한 하인 파스파르투가 함께하다"),
    13: ("obstacles", "여행 중 예상치 못한 장애물이 나타나다"),
    14: ("helps stranger", "포그가 낯선 사람을 도와주다"),
    15: ("detective wrong", "형사 픽스가 포그를 도둑으로 의심하다"),
    16: ("just in time", "포그가 아슬아슬하게 시간을 맞추다"),
    17: ("persistence", "포그가 끈기로 계속 나아가다"),
    18: ("journey reward", "여행의 진정한 보상을 깨닫다"),
    19: ("taken", "벅이 따뜻한 집에서 갑자기 끌려가다"),
    20: ("survive", "벅이 혹독한 환경에서 살아남다"),
    21: ("strong", "벅이 점점 강해지다"),
    22: ("Thornton saves", "존 손턴이 벅을 구해주다"),
    23: ("wild calls", "야생이 벅을 부르기 시작하다"),
    24: ("choose", "벅이 선택의 기로에 서다"),
    25: ("nature", "벅이 자연 속에서 본능을 깨우다"),
    26: ("answers call", "벅이 야생의 부름에 응답하다"),
    27: ("identity", "벅이 진정한 자신을 찾다"),
    28: ("different", "앤이 그린 게이블즈에 도착하다"),
    29: ("beauty", "앤이 세상의 아름다움을 발견하다"),
    30: ("imagination", "앤의 상상력이 빛을 발하다"),
    31: ("earned place", "앤이 자신의 자리를 얻다"),
    32: ("changed everyone", "앤이 주변 사람들을 변화시키다"),
    33: ("together", "가족이 함께 난파에서 살아남다"),
    34: ("new life", "무인도에서 새 삶을 시작하다"),
    35: ("challenges", "가족이 도전을 이겨내다"),
    36: ("home", "진정한 집의 의미를 깨닫다"),
}

# ── Story content generator ──
# Each returns (korean, a1_html, a1_tts, a2_html, a2_tts, b1_html, b1_tts)

def generate_story(wk, day_letter, key_sentence, book_en, book_kr):
    """Generate story content based on week, day, key sentence, and book."""
    theme_word, theme_desc = WEEK_THEMES.get(wk, ("theme", "이야기가 계속되다"))
    day_idx = {"a": 0, "b": 1, "c": 2}[day_letter]

    stories = _get_stories(wk, day_idx, key_sentence, book_en, book_kr, theme_word, theme_desc)
    return stories


def _get_stories(wk, day_idx, key, book_en, book_kr, theme, theme_desc):
    """Return dict with korean, a1, a2, b1 content."""
    # We build stories per week+day
    ALL = _build_all_stories()
    k = (wk, day_idx)
    if k in ALL:
        entry = ALL[k]
        # Replace KEY placeholder with actual key sentence
        result = {}
        for field in entry:
            val = entry[field]
            if isinstance(val, str):
                val = val.replace("__KEY__", key)
            result[field] = val
        return result

    # Fallback: generate from template
    return _fallback_story(wk, day_idx, key, book_en, book_kr, theme, theme_desc)


def _fallback_story(wk, day_idx, key, book_en, book_kr, theme, theme_desc):
    day_labels = ["첫째 날", "둘째 날", "셋째 날"]
    day_l = day_labels[day_idx]

    safe_key = key.replace("'", "\\'").replace('"', '')
    clean_key = re.sub(r'["\']', '', key)

    korean = (
        f"{book_kr} 이야기의 {day_l}이에요!<br>"
        f"이번 주 주제는 '{theme}'에 대한 것이에요.<br>"
        f"{theme_desc}.<br><br>"
        f"모든 이야기에는 중요한 순간이 있어요.<br>"
        f"등장인물들은 어려운 상황에서 선택을 해야 해요.<br>"
        f"그 선택이 이야기의 방향을 바꾸게 되죠.<br>"
        f"오늘의 핵심 문장을 잘 기억해 보세요.<br>"
        f"<strong>\"{clean_key}\"</strong><br>"
        f"이 문장이 왜 중요한지 생각해 봐요.<br>"
        f"등장인물의 마음을 이해하는 것이 중요해요.<br>"
        f"영어로도 이 이야기를 읽어 볼까요?<br>"
        f"아래 영어 이야기를 들어보세요!"
    )

    a1_html = (
        f"This story is about {book_en}.<br>"
        f"The theme today is {theme}.<br>"
        f"<span class=\"hl\">{clean_key}</span><br>"
        f"Let us read more!"
    )
    a1_tts = f"This story is about {book_en}. The theme today is {theme}. {clean_key} Let us read more!"

    a2_html = (
        f"Today we continue {book_en}.<br>"
        f"The main theme is about {theme}.<br>"
        f"The characters face an important moment.<br>"
        f"<span class=\"hl\">{clean_key}</span><br>"
        f"This sentence shows what happens in the story.<br>"
        f"Think about why this matters."
    )
    a2_tts = f"Today we continue {book_en}. The main theme is about {theme}. The characters face an important moment. {clean_key} This sentence shows what happens in the story. Think about why this matters."

    b1_html = (
        f"In this part of {book_en}, we explore the idea of {theme}.<br>"
        f"The characters must deal with a difficult situation.<br>"
        f"Every choice they make changes the story.<br>"
        f"<span class=\"hl\">{clean_key}</span><br>"
        f"This moment is important because it reveals their true nature.<br>"
        f"However, things are not always as simple as they seem.<br>"
        f"Because of this event, the story takes a new direction.<br>"
        f"Let us think about what we can learn from this."
    )
    b1_tts = f"In this part of {book_en}, we explore the idea of {theme}. The characters must deal with a difficult situation. Every choice they make changes the story. {clean_key} This moment is important because it reveals their true nature. However, things are not always as simple as they seem. Because of this event, the story takes a new direction. Let us think about what we can learn from this."

    return {
        "korean": korean,
        "a1_html": a1_html, "a1_tts": a1_tts,
        "a2_html": a2_html, "a2_tts": a2_tts,
        "b1_html": b1_html, "b1_tts": b1_tts,
    }


def _build_all_stories():
    """Build all 108 stories. Key = (week, day_idx)."""
    S = {}

    # ══════════════════════════════════════════
    # TREASURE ISLAND (W01-W09)
    # ══════════════════════════════════════════

    # W01 — map
    S[(1,0)] = {
        "korean": (
            "오늘부터 보물섬 이야기를 시작해요! 🗺️<br>"
            "이 소설은 영국 작가 로버트 루이스 스티븐슨이 썼어요.<br>"
            "주인공은 짐 호킨스라는 소년이에요.<br>"
            "짐의 아버지는 작은 여관을 운영했어요.<br><br>"
            "어느 날 수상한 늙은 선원이 여관에 왔어요.<br>"
            "그 선원은 무서운 비밀을 간직하고 있었어요.<br>"
            "선원이 죽자, 짐은 그의 낡은 상자를 열었어요.<br>"
            "상자 안에서 낡은 지도 한 장이 나왔어요!<br>"
            "지도에는 보물이 묻힌 섬이 그려져 있었어요.<br>"
            "하지만 지도에는 위험도 함께 담겨 있었죠.<br>"
            "짐의 심장이 두근두근 뛰기 시작했어요.<br>"
            "<strong>이 지도가 짐의 인생을 완전히 바꿀 거예요!</strong>"
        ),
        "a1_html": "Jim found an old map. 🗺️<br>The map showed treasure.<br>But the map held danger too.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Jim found an old map. The map showed treasure. But the map held danger too. __KEY__",
        "a2_html": "Jim Hawkins lived at his father's inn.<br>A strange old sailor came to stay.<br>When the sailor died, Jim found a map in his chest. 🗺️<br>The map showed a faraway island with buried treasure.<br><span class=\"hl\">__KEY__</span><br>But the map also held great danger.",
        "a2_tts": "Jim Hawkins lived at his father's inn. A strange old sailor came to stay. When the sailor died, Jim found a map in his chest. The map showed a faraway island with buried treasure. __KEY__ But the map also held great danger.",
        "b1_html": "Jim Hawkins was an ordinary boy who lived at his father's small inn by the sea.<br>One day, a mysterious old sailor arrived and stayed at the inn.<br>The sailor seemed frightened, as if someone was chasing him.<br>When the sailor suddenly died, Jim discovered a worn-out map hidden inside his chest. 🗺️<br><span class=\"hl\">__KEY__</span><br>However, Jim did not realize that this map would bring both excitement and terrible danger.<br>Because of this discovery, Jim's quiet life was about to change forever.<br>The adventure of a lifetime was just beginning!",
        "b1_tts": "Jim Hawkins was an ordinary boy who lived at his father's small inn by the sea. One day, a mysterious old sailor arrived and stayed at the inn. The sailor seemed frightened, as if someone was chasing him. When the sailor suddenly died, Jim discovered a worn-out map hidden inside his chest. __KEY__ However, Jim did not realize that this map would bring both excitement and terrible danger. Because of this discovery, Jim's quiet life was about to change forever. The adventure of a lifetime was just beginning!",
    }
    S[(1,1)] = {
        "korean": (
            "짐이 발견한 지도 이야기를 계속할게요!<br>"
            "지도에는 먼 바다 위의 섬이 그려져 있었어요.<br>"
            "짐은 이 지도를 마을의 어른들에게 보여줬어요.<br>"
            "의사 선생님과 부자 영주님이 지도를 보았어요.<br><br>"
            "그들은 보물을 찾으러 가자고 했어요!<br>"
            "배를 한 척 준비하기 시작했어요.<br>"
            "짐은 설레면서도 무서웠어요.<br>"
            "바다 너머에 무엇이 기다리고 있을까?<br>"
            "지도의 X 표시가 짐을 부르고 있었어요.<br>"
            "모험은 항상 두려움과 함께 시작되는 법이에요.<br>"
            "짐은 용기를 내기로 결심했어요.<br>"
            "<strong>보물섬을 향한 항해가 곧 시작될 거예요!</strong>"
        ),
        "a1_html": "Jim showed the map to others.<br>They wanted to find the treasure.<br>They got a ship ready.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Jim showed the map to others. They wanted to find the treasure. They got a ship ready. __KEY__",
        "a2_html": "Jim took the treasure map to Doctor Livesey and Squire Trelawney.<br>They were amazed by what they saw on the map.<br>The squire decided to buy a ship and find the treasure.<br>Jim felt excited but also a little scared.<br><span class=\"hl\">__KEY__</span><br>The adventure was about to begin!",
        "a2_tts": "Jim took the treasure map to Doctor Livesey and Squire Trelawney. They were amazed by what they saw on the map. The squire decided to buy a ship and find the treasure. Jim felt excited but also a little scared. __KEY__ The adventure was about to begin!",
        "b1_html": "After finding the map, Jim showed it to Doctor Livesey and Squire Trelawney.<br>Both men were thrilled by the possibility of finding buried treasure.<br>The squire immediately decided to buy a ship called the Hispaniola.<br>Jim could hardly believe he would sail across the ocean!<br><span class=\"hl\">__KEY__</span><br>However, not everyone on the journey would have good intentions.<br>Because the squire talked too much about the treasure, dangerous people heard about their plan.<br>Jim did not know that trouble was already waiting for them at sea.",
        "b1_tts": "After finding the map, Jim showed it to Doctor Livesey and Squire Trelawney. Both men were thrilled by the possibility of finding buried treasure. The squire immediately decided to buy a ship called the Hispaniola. Jim could hardly believe he would sail across the ocean! __KEY__ However, not everyone on the journey would have good intentions. Because the squire talked too much about the treasure, dangerous people heard about their plan. Jim did not know that trouble was already waiting for them at sea.",
    }
    S[(1,2)] = {
        "korean": (
            "보물섬 첫째 주의 마지막 이야기예요!<br>"
            "짐은 항해를 위한 준비를 하고 있어요.<br>"
            "배에 음식과 물을 싣고 선원들을 모았어요.<br>"
            "짐은 바다를 본 적이 거의 없었어요.<br><br>"
            "하지만 짐은 두려움을 이겨내기로 했어요.<br>"
            "지도가 가리키는 곳에 보물이 있을 거예요.<br>"
            "짐은 일기장에 모험의 시작을 적었어요.<br>"
            "새로운 세상이 짐을 기다리고 있었어요.<br>"
            "부두에서 배가 출발할 준비를 마쳤어요.<br>"
            "바람이 불고 파도가 출렁거렸어요.<br>"
            "짐의 위대한 모험이 드디어 시작되었어요!<br>"
            "<strong>앞으로 어떤 일이 벌어질까요?</strong>"
        ),
        "a1_html": "Jim got ready for the trip.<br>The ship was full of food and water.<br>The wind was blowing.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Jim got ready for the trip. The ship was full of food and water. The wind was blowing. __KEY__",
        "a2_html": "Jim helped load food and water onto the ship.<br>Many sailors joined the crew for the voyage.<br>Jim had never been on a long sea journey before.<br>He felt nervous but determined to be brave.<br><span class=\"hl\">__KEY__</span><br>The ship set sail toward the mysterious island.",
        "a2_tts": "Jim helped load food and water onto the ship. Many sailors joined the crew for the voyage. Jim had never been on a long sea journey before. He felt nervous but determined to be brave. __KEY__ The ship set sail toward the mysterious island.",
        "b1_html": "The preparations for the voyage were finally complete.<br>The Hispaniola was loaded with supplies, and the crew was ready to sail.<br>Jim felt a mixture of excitement and fear as he stepped onto the ship.<br>He had never traveled far from home before, and the ocean seemed endless.<br><span class=\"hl\">__KEY__</span><br>However, Jim noticed that some of the sailors looked rough and unfriendly.<br>Because he was young, Jim decided to stay quiet and observe carefully.<br>As the ship left the harbor, Jim wondered what awaited him on the treasure island.",
        "b1_tts": "The preparations for the voyage were finally complete. The Hispaniola was loaded with supplies, and the crew was ready to sail. Jim felt a mixture of excitement and fear as he stepped onto the ship. He had never traveled far from home before, and the ocean seemed endless. __KEY__ However, Jim noticed that some of the sailors looked rough and unfriendly. Because he was young, Jim decided to stay quiet and observe carefully. As the ship left the harbor, Jim wondered what awaited him on the treasure island.",
    }

    # W02 — choice
    S[(2,0)] = {
        "korean": (
            "짐과 친구들은 드디어 바다 위에 있어요!<br>"
            "배 히스패니올라호가 힘차게 나아가고 있어요.<br>"
            "짐은 갑판에서 넓은 바다를 바라봤어요.<br>"
            "집을 떠나온 것이 정말 맞는 선택이었을까?<br><br>"
            "짐은 고민이 많았어요.<br>"
            "안전한 집에 있을 수도 있었는데...<br>"
            "하지만 지도가 짐을 이끌었어요.<br>"
            "모험을 선택한 순간, 돌아갈 수 없었어요.<br>"
            "때로는 용기 있는 선택이 필요해요.<br>"
            "짐은 앞으로 나아가기로 결심했어요.<br>"
            "선택에는 항상 책임이 따른다는 것을 배울 거예요.<br>"
            "<strong>짐의 선택이 어떤 결과를 가져올까요?</strong>"
        ),
        "a1_html": "Jim was on the ship now.<br>He chose to find the treasure.<br>It was a big choice.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Jim was on the ship now. He chose to find the treasure. It was a big choice. __KEY__",
        "a2_html": "Jim sailed across the wide ocean on the Hispaniola.<br>He thought about his choice to leave home.<br>It was scary, but Jim wanted adventure.<br>Sometimes making a choice means you cannot go back.<br><span class=\"hl\">__KEY__</span><br>Jim hoped his choice was the right one.",
        "a2_tts": "Jim sailed across the wide ocean on the Hispaniola. He thought about his choice to leave home. It was scary, but Jim wanted adventure. Sometimes making a choice means you cannot go back. __KEY__ Jim hoped his choice was the right one.",
        "b1_html": "As the Hispaniola sailed farther from land, Jim began to wonder about his decision.<br>He could have stayed safe at home, but instead he chose the unknown sea.<br>Making choices is never easy, especially when you are young.<br><span class=\"hl\">__KEY__</span><br>However, Jim realized that not choosing is also a choice.<br>Because he wanted to discover something greater, he pushed his fears aside.<br>Every great adventure begins with one brave decision.<br>Jim was determined to see this journey through to the end.",
        "b1_tts": "As the Hispaniola sailed farther from land, Jim began to wonder about his decision. He could have stayed safe at home, but instead he chose the unknown sea. Making choices is never easy, especially when you are young. __KEY__ However, Jim realized that not choosing is also a choice. Because he wanted to discover something greater, he pushed his fears aside. Every great adventure begins with one brave decision. Jim was determined to see this journey through to the end.",
    }
    S[(2,1)] = {
        "korean": (
            "항해가 계속되고 있어요.<br>"
            "짐은 배 위에서 새로운 것들을 배우고 있어요.<br>"
            "밧줄 묶는 법, 돛을 올리는 법을 익혔어요.<br>"
            "하지만 어떤 선원들이 이상하게 행동해요.<br><br>"
            "짐은 불안한 느낌이 들었어요.<br>"
            "선원들이 몰래 속삭이는 것을 봤어요.<br>"
            "무슨 이야기를 하는 걸까?<br>"
            "짐은 가까이 가서 들어보고 싶었어요.<br>"
            "하지만 들키면 위험할 수 있어요.<br>"
            "짐은 조심스럽게 관찰하기로 했어요.<br>"
            "선택의 순간이 다시 찾아왔어요.<br>"
            "<strong>짐은 어떤 결정을 내릴까요?</strong>"
        ),
        "a1_html": "Jim learned new things on the ship.<br>Some sailors acted strangely.<br>Jim watched them carefully.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Jim learned new things on the ship. Some sailors acted strangely. Jim watched them carefully. __KEY__",
        "a2_html": "Jim learned to tie ropes and raise sails on the ship.<br>But he noticed some sailors whispering secretly.<br>They looked at Jim in a strange way sometimes.<br>Jim felt uneasy but did not say anything yet.<br><span class=\"hl\">__KEY__</span><br>He decided to watch and wait before making a move.",
        "a2_tts": "Jim learned to tie ropes and raise sails on the ship. But he noticed some sailors whispering secretly. They looked at Jim in a strange way sometimes. Jim felt uneasy but did not say anything yet. __KEY__ He decided to watch and wait before making a move.",
        "b1_html": "During the voyage, Jim worked hard to learn the ways of the sea.<br>He quickly picked up skills like tying ropes and reading the wind.<br>However, Jim began to notice suspicious behavior among some of the crew members.<br>They whispered in dark corners and fell silent whenever Jim approached.<br><span class=\"hl\">__KEY__</span><br>Jim faced a difficult choice: should he tell the captain or investigate on his own?<br>Because he was not sure who to trust, Jim decided to be cautious.<br>Sometimes the wisest choice is to wait and observe before acting.",
        "b1_tts": "During the voyage, Jim worked hard to learn the ways of the sea. He quickly picked up skills like tying ropes and reading the wind. However, Jim began to notice suspicious behavior among some of the crew members. They whispered in dark corners and fell silent whenever Jim approached. __KEY__ Jim faced a difficult choice: should he tell the captain or investigate on his own? Because he was not sure who to trust, Jim decided to be cautious. Sometimes the wisest choice is to wait and observe before acting.",
    }
    S[(2,2)] = {
        "korean": (
            "이번 주 마지막 이야기예요!<br>"
            "짐은 밤에 갑판 위에서 별을 바라봤어요.<br>"
            "바다는 어둡고 조용했어요.<br>"
            "짐은 집이 그리워지기도 했어요.<br><br>"
            "하지만 돌아가는 것은 선택지에 없었어요.<br>"
            "이미 너무 먼 바다까지 왔거든요.<br>"
            "짐은 자신의 선택을 믿기로 했어요.<br>"
            "두려움은 자연스러운 감정이에요.<br>"
            "중요한 건 두려움에도 불구하고 나아가는 거예요.<br>"
            "짐은 깊이 숨을 쉬고 다시 힘을 냈어요.<br>"
            "보물섬이 점점 가까워지고 있어요.<br>"
            "<strong>다음 주에는 특별한 사람을 만나게 될 거예요!</strong>"
        ),
        "a1_html": "Jim looked at the stars at night.<br>He missed home a little.<br>But he kept going forward.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Jim looked at the stars at night. He missed home a little. But he kept going forward. __KEY__",
        "a2_html": "At night, Jim stood on the deck and looked at the stars.<br>The sea was dark and quiet all around him.<br>He missed his home, but he believed in his choice.<br>Fear is natural, but bravery means moving forward anyway.<br><span class=\"hl\">__KEY__</span><br>The treasure island was getting closer every day.",
        "a2_tts": "At night, Jim stood on the deck and looked at the stars. The sea was dark and quiet all around him. He missed his home, but he believed in his choice. Fear is natural, but bravery means moving forward anyway. __KEY__ The treasure island was getting closer every day.",
        "b1_html": "As night fell over the ocean, Jim climbed to the deck and gazed at the starry sky.<br>The vast, dark sea stretched endlessly in every direction.<br>For a moment, Jim felt homesick and wondered if he had made a mistake.<br>However, he reminded himself that great things never come from staying in one place.<br><span class=\"hl\">__KEY__</span><br>Because he had already come so far, turning back was not an option.<br>Jim took a deep breath and felt his courage return.<br>He knew that the treasure island was waiting just beyond the horizon.",
        "b1_tts": "As night fell over the ocean, Jim climbed to the deck and gazed at the starry sky. The vast, dark sea stretched endlessly in every direction. For a moment, Jim felt homesick and wondered if he had made a mistake. However, he reminded himself that great things never come from staying in one place. __KEY__ Because he had already come so far, turning back was not an option. Jim took a deep breath and felt his courage return. He knew that the treasure island was waiting just beyond the horizon.",
    }

    # W03 — Long John Silver
    S[(3,0)] = {
        "korean": (
            "이번 주에는 아주 중요한 인물이 등장해요!<br>"
            "바로 한 다리 요리사, 존 실버예요.<br>"
            "실버는 배의 요리사로 고용되었어요.<br>"
            "그는 항상 웃으면서 친절하게 말했어요.<br><br>"
            "짐은 실버를 좋아하게 되었어요.<br>"
            "실버는 짐에게 바다 이야기를 들려줬어요.<br>"
            "하지만 실버에게는 숨겨진 얼굴이 있었어요.<br>"
            "그는 사실 위험한 해적이었거든요!<br>"
            "겉모습만으로 사람을 판단하면 안 된다는 교훈이에요.<br>"
            "친절한 미소 뒤에 나쁜 의도가 숨어 있을 수 있어요.<br>"
            "짐은 아직 이 사실을 모르고 있어요.<br>"
            "<strong>실버의 진짜 모습이 곧 드러날 거예요!</strong>"
        ),
        "a1_html": "A cook named Silver joined the ship.<br>Silver smiled a lot.<br>Jim liked Silver.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "A cook named Silver joined the ship. Silver smiled a lot. Jim liked Silver. __KEY__",
        "a2_html": "Long John Silver was the ship's cook.<br>He had only one leg but was very strong.<br>Silver told Jim exciting stories about the sea.<br>Jim thought Silver was a kind and friendly man.<br><span class=\"hl\">__KEY__</span><br>But Silver was hiding a dangerous secret.",
        "a2_tts": "Long John Silver was the ship's cook. He had only one leg but was very strong. Silver told Jim exciting stories about the sea. Jim thought Silver was a kind and friendly man. __KEY__ But Silver was hiding a dangerous secret.",
        "b1_html": "Among the crew, there was a one-legged cook called Long John Silver.<br>Silver was charming, cheerful, and always had a story to share.<br>Jim quickly grew fond of him because Silver treated him like a friend.<br>Silver taught Jim about life at sea and made everyone laugh with his jokes.<br><span class=\"hl\">__KEY__</span><br>However, appearances can be deceiving, and Silver was not who he seemed.<br>Because Silver was so likable, nobody suspected his true nature.<br>Sometimes the most dangerous people are the ones who smile the most.",
        "b1_tts": "Among the crew, there was a one-legged cook called Long John Silver. Silver was charming, cheerful, and always had a story to share. Jim quickly grew fond of him because Silver treated him like a friend. Silver taught Jim about life at sea and made everyone laugh with his jokes. __KEY__ However, appearances can be deceiving, and Silver was not who he seemed. Because Silver was so likable, nobody suspected his true nature. Sometimes the most dangerous people are the ones who smile the most.",
    }
    S[(3,1)] = {
        "korean": (
            "실버는 매일 맛있는 음식을 만들었어요.<br>"
            "선원들은 모두 실버를 좋아했어요.<br>"
            "실버는 짐에게 특별히 잘 해줬어요.<br>"
            "과일도 주고 재미있는 이야기도 해줬어요.<br><br>"
            "짐은 실버를 아버지처럼 느끼기 시작했어요.<br>"
            "하지만 어느 날 밤, 짐은 이상한 소리를 들었어요.<br>"
            "실버가 다른 선원들과 비밀스럽게 대화하고 있었어요.<br>"
            "짐은 숨어서 그들의 대화를 엿들었어요.<br>"
            "실버의 목소리가 평소와 달랐어요.<br>"
            "차갑고 무서운 목소리였어요!<br>"
            "짐의 심장이 쿵쿵 뛰기 시작했어요.<br>"
            "<strong>실버의 비밀이 무엇일까요?</strong>"
        ),
        "a1_html": "Silver cooked good food every day.<br>Jim heard Silver talk at night.<br>Silver's voice sounded scary.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Silver cooked good food every day. Jim heard Silver talk at night. Silver's voice sounded scary. __KEY__",
        "a2_html": "Silver made delicious meals and told wonderful stories.<br>Jim started to see Silver as a father figure.<br>But one night, Jim heard Silver whispering to other sailors.<br>His voice was cold and frightening, not kind at all.<br><span class=\"hl\">__KEY__</span><br>Jim realized that Silver might be hiding something terrible.",
        "a2_tts": "Silver made delicious meals and told wonderful stories. Jim started to see Silver as a father figure. But one night, Jim heard Silver whispering to other sailors. His voice was cold and frightening, not kind at all. __KEY__ Jim realized that Silver might be hiding something terrible.",
        "b1_html": "Every day, Silver prepared wonderful meals and entertained the crew with his stories.<br>Jim felt a growing trust toward this friendly cook with one leg.<br>However, everything changed one night when Jim accidentally overheard a conversation.<br>Silver was speaking in a low, menacing voice to a group of sailors.<br><span class=\"hl\">__KEY__</span><br>Jim's blood ran cold because he realized Silver was planning something dangerous.<br>The kind cook was not who Jim had believed him to be.<br>Because of what he heard, Jim now had to decide what to do with this terrifying information.",
        "b1_tts": "Every day, Silver prepared wonderful meals and entertained the crew with his stories. Jim felt a growing trust toward this friendly cook with one leg. However, everything changed one night when Jim accidentally overheard a conversation. Silver was speaking in a low, menacing voice to a group of sailors. __KEY__ Jim's blood ran cold because he realized Silver was planning something dangerous. The kind cook was not who Jim had believed him to be. Because of what he heard, Jim now had to decide what to do with this terrifying information.",
    }
    S[(3,2)] = {
        "korean": (
            "짐은 실버의 비밀 대화를 들었어요.<br>"
            "실버와 몇몇 선원들이 반란을 계획하고 있었어요!<br>"
            "그들은 보물을 독차지하려고 했어요.<br>"
            "짐은 너무 놀라서 말이 안 나왔어요.<br><br>"
            "그토록 친절했던 실버가 해적이었다니!<br>"
            "짐은 이 사실을 빨리 알려야 했어요.<br>"
            "하지만 들키면 짐도 위험에 처할 거예요.<br>"
            "짐은 용기를 내서 선장에게 달려갔어요.<br>"
            "선장은 짐의 말을 듣고 심각해졌어요.<br>"
            "이제 배 안에 적과 아군이 나뉘었어요.<br>"
            "짐은 두렵지만 올바른 일을 했어요.<br>"
            "<strong>진실을 말하는 것이 항상 용기 있는 행동이에요!</strong>"
        ),
        "a1_html": "Silver was planning something bad!<br>Jim told the captain about it.<br>Now they had to be careful.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Silver was planning something bad! Jim told the captain about it. Now they had to be careful. __KEY__",
        "a2_html": "Jim discovered that Silver and some sailors were planning a mutiny.<br>They wanted to steal all the treasure for themselves!<br>Jim was shocked because he had trusted Silver.<br>He bravely ran to the captain and told him everything.<br><span class=\"hl\">__KEY__</span><br>Now the ship was divided between good people and pirates.",
        "a2_tts": "Jim discovered that Silver and some sailors were planning a mutiny. They wanted to steal all the treasure for themselves! Jim was shocked because he had trusted Silver. He bravely ran to the captain and told him everything. __KEY__ Now the ship was divided between good people and pirates.",
        "b1_html": "Jim could barely believe what he had heard — Silver was the leader of a pirate mutiny!<br>The friendly cook had been secretly recruiting sailors to turn against the captain.<br>Their plan was to wait until the treasure was found and then take everything.<br>Jim felt betrayed because he had genuinely cared about Silver.<br><span class=\"hl\">__KEY__</span><br>However, Jim knew that staying silent would put everyone in danger.<br>Because telling the truth was the right thing to do, Jim rushed to inform the captain.<br>From that moment on, every person on the ship had to choose a side.",
        "b1_tts": "Jim could barely believe what he had heard — Silver was the leader of a pirate mutiny! The friendly cook had been secretly recruiting sailors to turn against the captain. Their plan was to wait until the treasure was found and then take everything. Jim felt betrayed because he had genuinely cared about Silver. __KEY__ However, Jim knew that staying silent would put everyone in danger. Because telling the truth was the right thing to do, Jim rushed to inform the captain. From that moment on, every person on the ship had to choose a side.",
    }

    # W04 — trust
    S[(4,0)] = {
        "korean": (
            "이번 주 주제는 '신뢰'예요.<br>"
            "짐은 실버에게 속았다는 것을 알게 되었어요.<br>"
            "누구를 믿어야 할지 모르겠어요.<br>"
            "배 안에 적이 숨어 있다는 게 무서웠어요.<br><br>"
            "선장, 의사, 영주만 믿을 수 있었어요.<br>"
            "하지만 나머지 선원들은 어떨까요?<br>"
            "신뢰는 한 번 깨지면 다시 쌓기 어려워요.<br>"
            "짐은 사람을 볼 때 더 신중해졌어요.<br>"
            "말보다 행동을 보는 것이 중요하다고 배웠어요.<br>"
            "진짜 친구는 어려울 때 알 수 있어요.<br>"
            "짐은 자신의 판단을 믿기로 했어요.<br>"
            "<strong>신뢰는 쉽게 주는 것이 아니에요.</strong>"
        ),
        "a1_html": "Jim did not know who to trust.<br>Silver had lied to everyone.<br>Trust is important.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Jim did not know who to trust. Silver had lied to everyone. Trust is important. __KEY__",
        "a2_html": "After learning about Silver's plan, Jim felt confused.<br>He did not know which sailors were friends and which were enemies.<br>The captain told Jim to watch people's actions, not their words.<br>Real friends show who they are when times are hard.<br><span class=\"hl\">__KEY__</span><br>Jim learned that trust must be earned, not given freely.",
        "a2_tts": "After learning about Silver's plan, Jim felt confused. He did not know which sailors were friends and which were enemies. The captain told Jim to watch people's actions, not their words. Real friends show who they are when times are hard. __KEY__ Jim learned that trust must be earned, not given freely.",
        "b1_html": "The discovery of Silver's betrayal shook Jim deeply.<br>He had trusted Silver completely, and now that trust was shattered.<br>Jim wondered how he could ever trust anyone on the ship again.<br>The captain wisely advised Jim to judge people by their actions rather than their words.<br><span class=\"hl\">__KEY__</span><br>However, Jim also learned that being too suspicious could be just as harmful as being too trusting.<br>Because trust is the foundation of all relationships, losing it felt like losing solid ground.<br>Jim decided to be careful but not to close his heart completely.",
        "b1_tts": "The discovery of Silver's betrayal shook Jim deeply. He had trusted Silver completely, and now that trust was shattered. Jim wondered how he could ever trust anyone on the ship again. The captain wisely advised Jim to judge people by their actions rather than their words. __KEY__ However, Jim also learned that being too suspicious could be just as harmful as being too trusting. Because trust is the foundation of all relationships, losing it felt like losing solid ground. Jim decided to be careful but not to close his heart completely.",
    }

    # For remaining weeks, I'll use a systematic approach
    # Build the remaining stories programmatically with week-specific content

    # W04 b,c
    for di, (ko_focus, a1s, a2s, b1s) in [(1,
        ("짐은 선장의 조언을 따라 행동으로 사람을 판단했어요.<br>어떤 선원은 짐을 도와줬고, 어떤 선원은 무시했어요.<br>진짜 친구는 위험할 때 도와주는 사람이에요.<br>짐은 조금씩 믿을 수 있는 사람을 찾았어요.<br><br>의사 선생님은 항상 짐을 걱정해 줬어요.<br>선장도 짐을 용감한 아이라고 칭찬했어요.<br>하지만 실버 편의 선원들은 짐을 노려봤어요.<br>짐은 겉모습이 아닌 마음을 보는 법을 배웠어요.<br>신뢰할 수 있는 사람이 있다는 것은 큰 행운이에요.<br>짐은 그 사람들과 함께 위기를 이겨낼 거예요.<br>힘든 시간이 진짜 우정을 보여줘요.<br><strong>여러분의 진짜 친구는 누구인가요?</strong>",
         "The doctor cared about Jim.<br>The captain was kind too.<br>Some sailors were not friendly.<br><span class=\"hl\">__KEY__</span>",
         "Jim watched who helped him and who ignored him.<br>The doctor always checked on Jim with concern.<br>The captain praised Jim for being brave.<br>But Silver's men looked at Jim with cold eyes.<br><span class=\"hl\">__KEY__</span><br>Jim learned to see people's hearts, not just their faces.",
         "Jim followed the captain's advice and began judging people by their deeds.<br>Doctor Livesey always showed genuine concern for Jim's safety and well-being.<br>The captain trusted Jim with important tasks, which made Jim feel valued.<br>On the other hand, Silver's followers watched Jim with suspicious, unfriendly eyes.<br><span class=\"hl\">__KEY__</span><br>However, Jim discovered that true friendship reveals itself during difficult times.<br>Because the doctor and captain stood by him, Jim felt stronger and more confident.<br>He realized that having even a few trustworthy people is worth more than many false friends.")),
    (2,
        ("이번 주를 마무리하면서 신뢰에 대해 정리해 볼게요.<br>짐은 실버의 배신으로 큰 상처를 받았어요.<br>하지만 그 경험으로 더 현명해졌어요.<br>사람을 처음 만났을 때 바로 믿지 않아도 돼요.<br><br>시간을 두고 천천히 관찰하는 것이 좋아요.<br>진심으로 대하는 사람은 결국 알 수 있어요.<br>짐은 이제 누가 진짜 친구인지 구분할 수 있어요.<br>선장과 의사는 짐의 진정한 동료예요.<br>함께라면 해적들에게도 맞설 수 있어요!<br>신뢰는 깨지기 쉽지만 다시 세울 수도 있어요.<br>짐은 새로운 눈으로 세상을 보기 시작했어요.<br><strong>신뢰를 배우는 것은 성장하는 것이에요!</strong>",
         "Jim knew who his real friends were now.<br>Trust takes time to build.<br>Jim grew wiser from this experience.<br><span class=\"hl\">__KEY__</span>",
         "Jim learned a lot about trust this week.<br>Silver's betrayal hurt him deeply.<br>But Jim became wiser because of it.<br>He knew that the captain and doctor were his real allies.<br><span class=\"hl\">__KEY__</span><br>Together, they could face the pirates ahead.",
         "Reflecting on everything that happened, Jim understood trust much better now.<br>Silver's betrayal had been painful, but it taught Jim an invaluable lesson.<br>You cannot always tell who is trustworthy at first glance.<br>It takes time, patience, and careful observation to know someone's true character.<br><span class=\"hl\">__KEY__</span><br>However, Jim also learned that shutting everyone out is not the answer.<br>Because the captain and doctor proved their loyalty through actions, Jim trusted them completely.<br>With his true friends beside him, Jim felt ready to face whatever challenges lay ahead."))]:
        entry = _make_entry(ko_focus, a1s, a2s, b1s)
        S[(4,di)] = entry

    # W05-W09 Treasure Island
    _add_treasure_w05_w09(S)
    # W10-W18 Around the World
    _add_around_world(S)
    # W19-W27 Call of the Wild
    _add_call_wild(S)
    # W28-W32 Anne of Green Gables
    _add_anne(S)
    # W33-W36 Swiss Family Robinson
    _add_swiss(S)

    return S


def _make_entry(ko, a1h, a2h, b1h):
    """Helper to build entry dict from HTML strings."""
    def strip_tags_for_tts(html):
        t = re.sub(r'<[^>]+>', ' ', html)
        t = t.replace('  ', ' ').strip()
        t = re.sub(r'\s+', ' ', t)
        return t
    return {
        "korean": ko,
        "a1_html": a1h,
        "a1_tts": strip_tags_for_tts(a1h),
        "a2_html": a2h,
        "a2_tts": strip_tags_for_tts(a2h),
        "b1_html": b1h,
        "b1_tts": strip_tags_for_tts(b1h),
    }


def _add_treasure_w05_w09(S):
    weeks = {
        5: [ # bravery
            ("짐은 드디어 보물섬에 도착했어요!<br>섬은 울창한 숲으로 뒤덮여 있었어요.<br>해적들이 반란을 일으키기 시작했어요!<br>총소리가 섬 곳곳에 울려 퍼졌어요.<br><br>짐은 무서웠지만 도망치지 않았어요.<br>친구들을 보호하기 위해 용기를 냈어요.<br>용기란 두려움이 없는 것이 아니에요.<br>두려움을 느끼면서도 행동하는 것이 진짜 용기예요.<br>짐은 떨리는 다리로 앞으로 나아갔어요.<br>작은 소년이지만 큰 용기를 보여줬어요.<br>위기의 순간에 짐의 진가가 드러났어요.<br><strong>용기는 크기가 아니라 마음에서 나오는 거예요!</strong>",
             "Jim arrived at the island.<br>Pirates started fighting!<br>Jim was scared but brave.<br><span class=\"hl\">__KEY__</span>",
             "Jim finally reached Treasure Island.<br>The island was covered with thick forests.<br>The pirates started their mutiny with guns and swords!<br>Jim was frightened, but he did not run away.<br><span class=\"hl\">__KEY__</span><br>True bravery means acting even when you are afraid.",
             "When the Hispaniola finally anchored near Treasure Island, chaos erupted.<br>The pirates, led by Silver, launched their mutiny with terrifying shouts.<br>Gunshots echoed across the island as the two sides clashed violently.<br>Jim's heart pounded with fear, but he refused to hide or run away.<br><span class=\"hl\">__KEY__</span><br>However, Jim learned that bravery is not the absence of fear.<br>Because true courage means acting despite being terrified, Jim pushed forward.<br>His small but brave actions proved that heroes come in all sizes."),
            ("해적들의 반란이 계속되고 있어요.<br>짐의 편은 오래된 요새로 피신했어요.<br>요새 안에서 적의 공격을 버텨야 했어요.<br>물과 식량이 부족해지기 시작했어요.<br><br>짐은 모두를 위해 물을 구하러 나가고 싶었어요.<br>하지만 밖에는 해적들이 돌아다니고 있었어요.<br>짐은 어둠을 이용해 몰래 움직였어요.<br>심장이 터질 것 같았지만 멈추지 않았어요.<br>용감한 한 걸음이 모두를 살릴 수 있어요.<br>짐은 친구들을 위해 위험을 감수했어요.<br>이것이 바로 진정한 용기의 모습이에요.<br><strong>다른 사람을 위한 용기가 가장 아름다워요!</strong>",
             "Jim's group hid in a fort.<br>They needed water badly.<br>Jim went out to help.<br><span class=\"hl\">__KEY__</span>",
             "Jim and his friends took shelter in an old fort on the island.<br>The pirates surrounded them and attacked again and again.<br>Water was running low, and everyone was thirsty.<br>Jim decided to sneak out in the dark to find water.<br><span class=\"hl\">__KEY__</span><br>His bravery for others showed his true character.",
             "Inside the old wooden fort, Jim and his allies prepared to defend themselves.<br>The pirates attacked repeatedly, and supplies began to run dangerously low.<br>Without fresh water, they would not survive much longer in the tropical heat.<br>Jim volunteered to sneak past the pirates under the cover of darkness.<br><span class=\"hl\">__KEY__</span><br>However, every step outside the fort meant risking his life.<br>Because Jim cared more about his friends than his own safety, he moved silently through the night.<br>His selfless bravery inspired everyone inside the fort to keep fighting."),
            ("이번 주 마지막 이야기예요!<br>짐은 물을 구해서 무사히 돌아왔어요!<br>모두가 짐에게 고마워했어요.<br>선장은 짐의 용기를 높이 평가했어요.<br><br>용기는 특별한 사람만 가지는 것이 아니에요.<br>누구나 용기를 낼 수 있어요.<br>중요한 것은 행동으로 옮기는 거예요.<br>짐은 평범한 소년이었지만 영웅처럼 행동했어요.<br>해적들도 짐의 용기에 놀랐어요.<br>작은 행동이 큰 변화를 만들 수 있어요.<br>짐은 이제 자신감이 생겼어요.<br><strong>여러분도 용기를 낼 수 있어요!</strong>",
             "Jim came back safely with water!<br>Everyone thanked Jim.<br>Small actions can make a big difference.<br><span class=\"hl\">__KEY__</span>",
             "Jim returned to the fort safely with the water.<br>Everyone was grateful and relieved to see him.<br>The captain said Jim was the bravest person on the island.<br>Even the pirates were surprised by Jim's courage.<br><span class=\"hl\">__KEY__</span><br>Jim learned that anyone can be a hero through brave actions.",
             "Jim successfully made it back to the fort carrying the precious water.<br>His friends cheered with relief and gratitude when they saw him safe.<br>The captain placed his hand on Jim's shoulder and called him a true hero.<br>Even some of Silver's men were impressed by the boy's daring feat.<br><span class=\"hl\">__KEY__</span><br>However, the real victory was not in the water itself but in Jim's courage to act.<br>Because Jim chose to risk himself for others, he earned everyone's deep respect.<br>This experience taught Jim that ordinary people can do extraordinary things when they care enough."),
        ],
        6: [ # greed
            ("이번 주는 '욕심'에 대해 이야기해요.<br>해적들은 왜 반란을 일으켰을까요?<br>바로 보물을 혼자 차지하려는 욕심 때문이에요.<br>욕심은 사람의 눈을 멀게 만들어요.<br><br>실버와 해적들은 금과 보석만 생각했어요.<br>우정도, 약속도 다 잊어버렸어요.<br>보물에 눈이 멀어 서로를 의심하기 시작했어요.<br>욕심이 클수록 외로워지는 법이에요.<br>해적들은 점점 서로 싸우기 시작했어요.<br>보물은 아직 찾지도 못했는데 벌써 다투고 있어요.<br>욕심은 결국 자기 자신을 해치게 되요.<br><strong>정말 소중한 것은 돈이 아니에요!</strong>",
             "The pirates wanted all the gold.<br>They started to fight each other.<br>Greed makes people selfish.<br><span class=\"hl\">__KEY__</span>",
             "The pirates only cared about gold and jewels.<br>They forgot about friendship and promises.<br>Greed made them suspicious of each other.<br>They started arguing about who would get more treasure.<br><span class=\"hl\">__KEY__</span><br>Greed was destroying them from the inside.",
             "The pirates had launched their mutiny driven entirely by greed for the treasure.<br>All they could think about was gold, silver, and precious jewels waiting to be found.<br>In their obsession, they forgot every bond of friendship and loyalty they once had.<br>Silver struggled to keep his men under control as they argued bitterly among themselves.<br><span class=\"hl\">__KEY__</span><br>However, the irony was that they had not even found the treasure yet.<br>Because greed consumed their minds, they could not work together or think clearly.<br>Their selfishness was slowly tearing the pirate group apart from within."),
            ("해적들의 다툼이 점점 심해지고 있어요.<br>누가 보물을 더 많이 가질지 싸워요.<br>실버도 부하들을 통제하기 어려워졌어요.<br>욕심은 팀워크를 무너뜨리는 독이에요.<br><br>반면에 짐의 편은 서로 도우며 지냈어요.<br>적은 것도 나누면 충분해질 수 있어요.<br>의사는 부상당한 사람을 치료해 줬어요.<br>심지어 적인 해적도 치료해 줬어요!<br>나눔과 욕심의 차이가 분명해졌어요.<br>욕심쟁이들은 많이 가져도 행복하지 않아요.<br>나누는 사람들은 적게 가져도 행복해요.<br><strong>나눔이 진정한 부자를 만드는 거예요!</strong>",
             "The pirates fought over treasure.<br>Jim's friends shared with each other.<br>Sharing is better than greed.<br><span class=\"hl\">__KEY__</span>",
             "The pirates argued louder and louder about the treasure.<br>Silver could barely control his own men anymore.<br>Meanwhile, Jim's side shared food and helped each other.<br>The doctor even treated wounded pirates because it was the right thing.<br><span class=\"hl\">__KEY__</span><br>The difference between greed and generosity became very clear.",
             "As the conflict continued, the pirates' greed only grew worse and more destructive.<br>They could not agree on anything because each person wanted the largest share.<br>Silver, despite being their leader, found it increasingly difficult to maintain order.<br>In stark contrast, Jim's group worked together and shared their limited resources fairly.<br><span class=\"hl\">__KEY__</span><br>Remarkably, Doctor Livesey even treated injured pirates because he believed in doing what was right.<br>Because Jim's side chose generosity over selfishness, they remained strong and united.<br>This showed that true wealth comes not from gold but from caring for one another."),
            ("욕심에 대한 이번 주를 마무리할게요.<br>해적들은 욕심 때문에 점점 약해졌어요.<br>서로 믿지 못하고 싸우기만 했거든요.<br>반면에 짐의 편은 더 단단해졌어요.<br><br>이 이야기에서 중요한 교훈이 있어요.<br>물건보다 사람이 더 소중해요.<br>금은보화보다 우정이 더 가치 있어요.<br>욕심을 부리면 결국 모든 것을 잃게 되요.<br>나누고 함께하면 더 많은 것을 얻을 수 있어요.<br>짐은 이 진리를 몸소 경험했어요.<br>보물보다 친구가 더 큰 보물이에요.<br><strong>여러분은 어떤 보물을 원하나요?</strong>",
             "Greedy pirates became weak.<br>Jim's team stayed strong together.<br>Friends are the real treasure.<br><span class=\"hl\">__KEY__</span>",
             "The greedy pirates grew weaker because they could not trust each other.<br>Jim's group stayed strong because they worked as a team.<br>This story teaches us that people matter more than gold.<br>Friendship is worth more than any treasure chest.<br><span class=\"hl\">__KEY__</span><br>Jim understood that the real treasure was the people beside him.",
             "By the end of the week, the consequences of greed had become painfully obvious.<br>The pirates, consumed by their desire for gold, had turned on each other completely.<br>Their group was falling apart because selfishness destroys all bonds of trust.<br>Meanwhile, Jim's companions grew stronger through their generosity and mutual support.<br><span class=\"hl\">__KEY__</span><br>However, the most important lesson was not about winning or losing a battle.<br>Because Jim witnessed both greed and generosity up close, he understood a deep truth.<br>The greatest treasure in life is not gold or jewels but the people who stand by your side."),
        ],
        7: [ # courage - ship
            ("이번 주 짐은 놀라운 일을 해요!<br>짐은 혼자서 배를 되찾기로 결심했어요.<br>해적들이 히스패니올라호를 차지했거든요.<br>배 없이는 섬에서 돌아갈 수 없어요.<br><br>짐은 아무에게도 말하지 않고 혼자 갔어요.<br>작은 보트를 타고 밤바다를 건넜어요.<br>파도가 치고 바람이 불었지만 포기하지 않았어요.<br>해적 두 명이 배를 지키고 있었어요.<br>짐은 조용히 배에 올라탔어요.<br>심장이 귀까지 뛰었지만 움직임을 멈추지 않았어요.<br>혼자서도 해낼 수 있다는 것을 증명할 거예요.<br><strong>짐의 가장 대담한 모험이 시작되었어요!</strong>",
             "Jim went to get the ship back alone.<br>He sailed a small boat at night.<br>Two pirates were on the ship.<br><span class=\"hl\">__KEY__</span>",
             "Jim made a bold plan to take back the Hispaniola by himself.<br>He rowed a small boat across the dark water at night.<br>Two pirates were guarding the ship, but Jim was determined.<br>He climbed aboard quietly without making a sound.<br><span class=\"hl\">__KEY__</span><br>Jim's courage in that moment was truly remarkable.",
             "Without telling anyone, Jim came up with an incredibly bold plan to recapture the ship.<br>Under the cover of darkness, he paddled a tiny boat across the dangerous waters alone.<br>The waves crashed against his small vessel, but Jim refused to turn back.<br>When he reached the Hispaniola, he discovered two pirates standing guard on deck.<br><span class=\"hl\">__KEY__</span><br>However, Jim's determination was stronger than his fear of being caught.<br>Because he moved silently and carefully, the pirates did not notice him climbing aboard.<br>This was the most daring thing Jim had ever attempted in his entire life."),
            ("짐이 배 위에서 해적과 맞닥뜨렸어요!<br>해적 한 명은 술에 취해 잠들어 있었어요.<br>다른 한 명은 짐을 발견했어요!<br>짐은 재빨리 행동해야 했어요.<br><br>짐은 밧줄을 잡고 돛대로 올라갔어요.<br>해적이 짐을 쫓아왔어요.<br>아슬아슬한 추격전이 벌어졌어요!<br>짐은 배의 구조를 잘 알고 있었어요.<br>배에서 일하면서 배운 것이 도움이 되었어요!<br>위기 상황에서 평소의 노력이 빛을 발했어요.<br>짐은 결국 해적을 물리쳤어요!<br><strong>준비된 사람에게 기회가 찾아오는 법이에요!</strong>",
             "Jim found the pirates on the ship.<br>One was sleeping.<br>The other one chased Jim!<br><span class=\"hl\">__KEY__</span>",
             "Jim discovered one pirate asleep and another awake on the ship.<br>The awake pirate spotted Jim and chased him across the deck!<br>Jim used his knowledge of the ship to escape and fight back.<br>All the skills he learned during the voyage helped him now.<br><span class=\"hl\">__KEY__</span><br>Jim's hard work and preparation finally paid off.",
             "When Jim boarded the Hispaniola, he found one pirate unconscious from drinking too much rum.<br>Unfortunately, the other pirate was wide awake and immediately spotted the young intruder.<br>A dangerous chase began across the deck of the rocking ship.<br>Jim scrambled up the ropes and rigging, using every skill he had learned during the voyage.<br><span class=\"hl\">__KEY__</span><br>However, the pirate was bigger and stronger than Jim in every way.<br>Because Jim had studied the ship's layout so carefully, he knew hiding spots the pirate did not.<br>In the end, Jim's preparation and quick thinking gave him the advantage he needed to survive."),
            ("짐이 해냈어요! 배를 되찾았어요! 🎉<br>혼자서 해적 둘을 물리치고 배를 지켰어요.<br>짐은 배를 안전한 곳으로 옮겼어요.<br>이제 짐의 편이 배를 다시 쓸 수 있어요.<br><br>선장과 의사가 짐의 이야기를 듣고 감탄했어요.<br>어린 소년의 용기가 모두를 구한 거예요!<br>짐은 겸손하게 말했어요. '운이 좋았어요.'<br>하지만 모두가 알고 있었어요 — 용기 덕분이라는 것을.<br>진정한 용기는 혼자서도 옳은 일을 하는 거예요.<br>누가 보지 않아도 최선을 다하는 거예요.<br>짐은 이제 소년이 아닌 영웅이 되었어요.<br><strong>용기는 자신도 몰랐던 힘을 깨워줘요!</strong>",
             "Jim took back the ship! 🎉<br>He was brave all by himself.<br>Everyone was amazed.<br><span class=\"hl\">__KEY__</span>",
             "Jim successfully recaptured the Hispaniola all by himself!<br>He defeated the two pirates and moved the ship to a safe spot.<br>The captain and doctor were amazed by Jim's incredible bravery.<br>Jim humbly said he was just lucky.<br><span class=\"hl\">__KEY__</span><br>But everyone knew it was pure courage that saved them all.",
             "Against all odds, Jim managed to recapture the Hispaniola single-handedly!<br>He outsmarted the two pirates and carefully moved the ship to a hidden, safe location.<br>When Jim returned to his friends, they could hardly believe what he had accomplished.<br>The captain shook Jim's hand and declared him the hero of the entire expedition.<br><span class=\"hl\">__KEY__</span><br>However, Jim remained humble and said fortune had been on his side.<br>Because Jim had the courage to act alone when no one else could, the whole group was saved.<br>This adventure proved that true courage is doing the right thing even when nobody is watching."),
        ],
        8: [ # thinking
            ("이번 주는 '생각하는 힘'에 대해 배워요.<br>짐은 힘이 세지 않아요. 어른도 아니에요.<br>하지만 짐에게는 뛰어난 생각하는 힘이 있어요!<br>위기 상황에서 빠르게 판단할 수 있어요.<br><br>해적들은 힘으로 모든 것을 해결하려 했어요.<br>하지만 짐은 머리를 사용했어요.<br>배를 되찾을 때도 힘이 아닌 지혜를 썼어요.<br>상대의 약점을 파악하고 전략을 세웠어요.<br>생각하는 사람이 결국 이기는 법이에요.<br>주먹보다 머리가 더 강한 무기예요.<br>짐처럼 생각하는 힘을 기르는 것이 중요해요.<br><strong>똑똑하게 생각하면 어떤 문제도 풀 수 있어요!</strong>",
             "Jim used his brain, not his muscles.<br>Thinking is a strong power.<br>Smart plans beat big fists.<br><span class=\"hl\">__KEY__</span>",
             "Jim was not the strongest person on the island.<br>But he had a powerful brain that helped him solve problems.<br>While pirates used force, Jim used clever strategies.<br>He found the pirates' weaknesses and made smart plans.<br><span class=\"hl\">__KEY__</span><br>Thinking clearly is the greatest weapon anyone can have.",
             "Throughout the adventure, Jim proved that intelligence is far more valuable than physical strength.<br>While the pirates relied on brute force and threats to get what they wanted, Jim used his mind.<br>He observed carefully, remembered details, and created strategies to overcome challenges.<br>When he recaptured the ship, it was his quick thinking that made it possible.<br><span class=\"hl\">__KEY__</span><br>However, thinking well requires patience and the ability to stay calm under pressure.<br>Because Jim trained himself to observe before acting, he always found solutions others missed.<br>This taught him that the mind is the most powerful tool any person can possess."),
            ("짐의 지혜가 또 한 번 빛을 발했어요!<br>실버가 짐을 인질로 잡으려 했어요.<br>하지만 짐은 침착하게 대화로 시간을 벌었어요.<br>화를 내거나 울지 않았어요.<br><br>짐은 실버의 마음을 읽으려 했어요.<br>실버가 원하는 것이 무엇인지 파악했어요.<br>그리고 실버에게 거래를 제안했어요!<br>놀랍게도 실버는 짐의 제안을 들었어요.<br>이것이 바로 협상의 힘이에요.<br>싸움보다 대화가 더 좋은 결과를 만들어요.<br>짐은 어린 나이에 대단한 지혜를 보여줬어요.<br><strong>말의 힘은 칼보다 강할 수 있어요!</strong>",
             "Silver tried to catch Jim.<br>Jim talked calmly to Silver.<br>Words can be powerful tools.<br><span class=\"hl\">__KEY__</span>",
             "When Silver tried to capture Jim, the boy stayed perfectly calm.<br>Instead of fighting or crying, Jim used his words carefully.<br>He figured out what Silver wanted and offered a clever deal.<br>Surprisingly, Silver listened to Jim's proposal.<br><span class=\"hl\">__KEY__</span><br>Jim proved that talking is sometimes better than fighting.",
             "In a tense moment, Silver cornered Jim and tried to take him hostage.<br>Most children would have panicked, but Jim remained remarkably calm and composed.<br>He analyzed Silver's desires and motivations with surprising maturity.<br>Then Jim proposed a deal that appealed to Silver's self-interest.<br><span class=\"hl\">__KEY__</span><br>However, the real genius was that Jim's deal also protected his friends from harm.<br>Because Jim understood that communication can be more powerful than confrontation, he saved lives.<br>Silver was so impressed by the boy's intelligence that he began to respect Jim in a new way."),
            ("생각하는 힘에 대한 이번 주를 마무리해요!<br>짐은 이번 모험에서 많은 것을 배웠어요.<br>힘보다 지혜가 중요하다는 것을요.<br>차분하게 상황을 분석하는 것이 필요해요.<br><br>감정에 휩쓸리지 않고 냉정하게 생각해야 해요.<br>상대방의 입장에서 생각해 보는 것도 중요해요.<br>짐은 실버조차도 이해하려 노력했어요.<br>적을 이해하면 더 좋은 전략을 세울 수 있어요.<br>생각하는 힘은 연습으로 기를 수 있어요.<br>책을 읽고 질문하는 것이 좋은 연습이에요.<br>짐처럼 똑똑하게 문제를 풀어 봐요!<br><strong>여러분의 뇌가 가장 큰 보물이에요!</strong>",
             "Thinking before acting is wise.<br>Jim understood even his enemies.<br>Your brain is your greatest treasure!<br><span class=\"hl\">__KEY__</span>",
             "Jim learned that staying calm helps you think better.<br>Understanding your opponent gives you an advantage.<br>Jim even tried to understand Silver's point of view.<br>This made Jim a better strategist and problem solver.<br><span class=\"hl\">__KEY__</span><br>Practicing thinking skills is something everyone can do every day.",
             "Looking back on his adventure, Jim realized that his greatest strength was his ability to think clearly.<br>Every challenge he overcame was solved through careful analysis rather than physical force.<br>He learned to control his emotions and examine situations from multiple perspectives.<br>Even understanding Silver's motivations helped Jim make smarter decisions.<br><span class=\"hl\">__KEY__</span><br>However, developing strong thinking skills does not happen overnight.<br>Because Jim was naturally curious and always asked questions, his mind grew sharper over time.<br>The most important treasure Jim discovered was not gold but the incredible power of the human mind."),
        ],
        9: [ # lessons
            ("보물섬 이야기의 마지막 주가 시작되었어요!<br>짐과 친구들이 드디어 보물을 찾았어요!<br>오래된 동굴 속에 금화와 보석이 가득했어요.<br>하지만 짐은 의외로 덤덤했어요.<br><br>보물보다 더 소중한 것을 발견했거든요.<br>용기, 우정, 신뢰, 지혜의 가치를요.<br>금화는 반짝이지만 언젠가 사라져요.<br>하지만 모험에서 배운 교훈은 영원해요.<br>짐은 이전의 짐과 완전히 달라졌어요.<br>겁 많던 소년이 지혜로운 청년이 되었어요.<br>진짜 보물은 성장하는 자기 자신이에요.<br><strong>여러분도 매일매일 성장하고 있어요!</strong>",
             "Jim found the treasure at last!<br>But he learned bigger lessons.<br>Growing up is the real treasure.<br><span class=\"hl\">__KEY__</span>",
             "Jim and his friends finally discovered the treasure in a cave.<br>There were gold coins and jewels everywhere!<br>But Jim felt strangely calm about the treasure.<br>He realized that courage, friendship, and wisdom were more valuable.<br><span class=\"hl\">__KEY__</span><br>The real treasure was everything Jim learned on this journey.",
             "After weeks of danger and adventure, Jim and his allies finally found the legendary treasure.<br>The cave was filled with mountains of gold coins, sparkling jewels, and ancient artifacts.<br>Surprisingly, Jim did not feel the excitement he had expected when he first saw the map.<br>Instead, he felt a quiet understanding that the real treasures were the lessons he had learned.<br><span class=\"hl\">__KEY__</span><br>However, the gold was still divided fairly among those who deserved it.<br>Because Jim had grown so much during this adventure, he valued wisdom over wealth.<br>The frightened boy who found a map had become a thoughtful, courageous young man."),
            ("짐과 친구들은 보물을 싣고 집으로 돌아가요.<br>긴 항해가 끝나고 고향이 보이기 시작했어요.<br>짐은 감회가 새로웠어요.<br>떠날 때와 돌아올 때의 짐은 달라요.<br><br>실버는 항해 도중에 몰래 사라졌어요.<br>금화 일부를 가지고 도망친 거예요.<br>짐은 실버가 미웠지만 또 이해가 되기도 했어요.<br>사람은 쉽게 변하지 않는다는 것을 배웠어요.<br>하지만 자기 자신은 변할 수 있어요!<br>짐은 이 모험을 절대 잊지 않을 거예요.<br>모든 경험이 짐을 만든 거예요.<br><strong>우리도 경험을 통해 성장해요!</strong>",
             "Jim sailed home with the treasure.<br>Silver ran away during the trip.<br>Jim was different now.<br><span class=\"hl\">__KEY__</span>",
             "Jim and his friends loaded the treasure and set sail for home.<br>During the voyage back, Silver secretly escaped with some gold coins.<br>Jim was angry but also understood that people do not change easily.<br>What mattered most was that Jim himself had changed for the better.<br><span class=\"hl\">__KEY__</span><br>Every experience on this adventure shaped who Jim became.",
             "With the treasure safely aboard, the Hispaniola began its long journey back to England.<br>Jim stood on the deck and watched the island grow smaller on the horizon.<br>During the return voyage, Silver managed to escape one night, taking a bag of gold coins.<br>Jim felt conflicted — angry at Silver's treachery yet somehow understanding his nature.<br><span class=\"hl\">__KEY__</span><br>However, the most significant change was not in the treasure they carried but in Jim himself.<br>Because of everything he experienced, Jim had transformed from a timid boy into a wise young man.<br>He realized that the true value of any journey lies not in the destination but in who you become along the way."),
            ("보물섬 이야기의 마지막이에요!<br>짐은 집에 돌아와서 일상으로 돌아왔어요.<br>하지만 짐의 마음속에는 바다가 남아 있어요.<br>모험의 기억이 짐을 강하게 만들어 줘요.<br><br>이 이야기에서 우리가 배운 것을 정리해 볼게요.<br>첫째, 용기는 두려움 속에서 나와요.<br>둘째, 신뢰는 행동으로 증명해야 해요.<br>셋째, 욕심은 우리를 외롭게 만들어요.<br>넷째, 생각하는 힘이 가장 강한 무기예요.<br>다섯째, 진짜 보물은 성장하는 자기 자신이에요.<br>짐의 이야기는 끝이지만 교훈은 계속되요!<br><strong>다음 주부터 새로운 모험이 기다려요!</strong>",
             "Jim is home now.<br>He learned about courage and trust.<br>The adventure changed him forever.<br><span class=\"hl\">__KEY__</span>",
             "Jim returned home and went back to his normal life.<br>But inside, he carried the memories of his incredible adventure.<br>He learned about courage, trust, wisdom, and the danger of greed.<br>The real treasure was not gold but the person Jim became.<br><span class=\"hl\">__KEY__</span><br>Next week, a brand new adventure begins!",
             "Jim finally returned to his quiet life at the inn, but nothing felt quite the same.<br>The memories of Treasure Island — the battles, the betrayals, the friendships — lived on in his heart.<br>He had learned that true courage means acting despite fear, not without it.<br>He understood that trust is precious and must be earned through consistent actions.<br><span class=\"hl\">__KEY__</span><br>However, perhaps the greatest lesson was that greed destroys while generosity builds.<br>Because Jim experienced all of this firsthand, these lessons became part of who he was forever.<br>As one adventure ended, Jim knew that life itself is the greatest adventure of all."),
        ],
    }

    for wk, days in weeks.items():
        for di, (ko, a1h, a2h, b1h) in enumerate(days):
            S[(wk, di)] = _make_entry(ko, a1h, a2h, b1h)


def _add_around_world(S):
    weeks = {
        10: [ # bold bet
            ("80일간의 세계일주 이야기를 시작해요! 🌍<br>이 소설은 프랑스 작가 쥘 베른이 1873년에 썼어요.<br>주인공은 영국 신사 필리어스 포그예요.<br>포그는 런던에서 가장 정확한 사람이에요.<br><br>어느 날 포그는 클럽에서 친구들과 대화했어요.<br>신문에서 새로운 철도가 개통되었다는 기사를 봤어요.<br>'이제 80일이면 세계를 돌 수 있다!'<br>포그는 자신의 전 재산을 걸고 내기를 했어요!<br>친구들은 불가능하다고 했지만 포그는 확신했어요.<br>계산과 계획이 정확하면 가능하다고 믿었어요.<br>이것은 단순한 내기가 아니라 도전이었어요.<br><strong>포그의 대담한 모험이 시작되었어요!</strong>",
             "Mr. Fogg made a big bet.<br>He said he could travel the world in 80 days.<br>Everyone thought it was impossible.<br><span class=\"hl\">__KEY__</span>",
             "Phileas Fogg was a very precise English gentleman.<br>One day at his club, he bet his friends he could circle the globe in 80 days.<br>He risked all his money on this daring challenge.<br>His friends laughed, but Fogg was completely serious.<br><span class=\"hl\">__KEY__</span><br>With careful planning, Fogg believed anything was possible.",
             "Phileas Fogg was known throughout London as the most punctual and methodical gentleman in England.<br>One evening at the Reform Club, a discussion about a new railway led to an extraordinary wager.<br>Fogg calmly announced that he could travel around the entire world in just eighty days.<br>His fellow club members were astonished and bet twenty thousand pounds that he would fail.<br><span class=\"hl\">__KEY__</span><br>However, Fogg was not a man who made decisions lightly or without careful calculation.<br>Because he had studied every railway timetable and steamship schedule, he was confident in his plan.<br>That very evening, Fogg packed his bag and prepared to leave London on the greatest journey of his life."),
            ("포그는 바로 그날 밤 출발했어요!<br>하인 파스파르투가 함께 가게 되었어요.<br>파스파르투는 그날 아침에 막 고용된 하인이에요!<br>조용한 생활을 기대했는데 세계일주라니!<br><br>파스파르투는 놀랐지만 주인을 따르기로 했어요.<br>포그는 가방 하나만 들고 출발했어요.<br>시간표를 정확하게 계산한 계획표가 있었어요.<br>1분도 낭비할 수 없는 빡빡한 일정이었어요.<br>기차, 배, 마차를 갈아타며 이동해야 했어요.<br>파스파르투는 불안했지만 흥분되기도 했어요.<br>이렇게 두 사람의 세계일주가 시작되었어요!<br><strong>시간과의 싸움이 곧 펼쳐질 거예요!</strong>",
             "Fogg left London that same night.<br>His servant Passepartout went with him.<br>They had 80 days exactly.<br><span class=\"hl\">__KEY__</span>",
             "Fogg wasted no time and departed London that very evening.<br>His newly hired servant, Passepartout, was shocked but loyal.<br>Fogg carried a bag with exactly the right amount of money and a precise schedule.<br>Every train, ship, and carriage was planned down to the minute.<br><span class=\"hl\">__KEY__</span><br>The race around the world had officially begun!",
             "True to his word, Fogg departed from London that very evening without any hesitation.<br>His servant Passepartout, who had been hired only that morning expecting a quiet life, was stunned.<br>Fogg traveled light, carrying just one carpet bag and a large sum of money in banknotes.<br>He had prepared a meticulous timetable that accounted for every connection and possible delay.<br><span class=\"hl\">__KEY__</span><br>However, Passepartout quickly realized that this journey would test them in ways they could not predict.<br>Because every minute counted, there was absolutely no room for error or unexpected events.<br>As the train pulled out of the station, both master and servant felt the weight of the enormous challenge ahead."),
            ("포그와 파스파르투가 프랑스를 지나고 있어요.<br>기차를 타고 유럽을 빠르게 횡단했어요.<br>파리, 토리노, 브린디시를 거쳐 갔어요.<br>계획대로 정확하게 움직이고 있어요!<br><br>하지만 여행은 아직 시작일 뿐이에요.<br>유럽 다음에는 바다를 건너야 해요.<br>인도, 중국, 일본, 미국을 지나야 해요!<br>아직 갈 길이 정말 멀어요.<br>포그는 침착하게 시간표만 확인했어요.<br>감정에 흔들리지 않는 것이 포그의 강점이에요.<br>하지만 곧 예상치 못한 일들이 생길 거예요.<br><strong>계획대로 되지 않을 때 어떻게 할까요?</strong>",
             "They crossed Europe by train.<br>Everything went according to plan.<br>But the journey was just beginning.<br><span class=\"hl\">__KEY__</span>",
             "Fogg and Passepartout crossed Europe quickly by train.<br>They passed through Paris, Turin, and Brindisi without any problems.<br>Everything was going exactly according to Fogg's timetable.<br>But they still had to cross oceans and continents ahead.<br><span class=\"hl\">__KEY__</span><br>Fogg remained calm, but unexpected challenges were coming soon.",
             "The first leg of the journey went smoothly as Fogg and Passepartout raced across Europe by rail.<br>They passed through Paris, crossed the Alps to Turin, and reached the Italian port of Brindisi on schedule.<br>Fogg checked his timetable constantly, confirming that they were right on track.<br>Passepartout marveled at the changing scenery while his master remained perfectly composed.<br><span class=\"hl\">__KEY__</span><br>However, Europe was the easiest part of their journey around the world.<br>Because the real challenges lay in crossing India, navigating the Pacific, and spanning America, they could not celebrate yet.<br>Fogg knew that maintaining composure would be essential when unexpected problems inevitably arose."),
        ],
        11: [ # every minute
            ("시간이 중요한 여행이 계속되고 있어요!<br>포그와 파스파르투는 이제 인도에 있어요.<br>인도의 열기와 색깔이 파스파르투를 놀라게 했어요.<br>하지만 감상할 시간이 없었어요.<br><br>기차가 예정보다 늦게 출발했어요!<br>포그는 1분도 허투루 쓸 수 없었어요.<br>매 순간이 귀중한 시간이에요.<br>늦어지면 다음 배를 놓칠 수 있거든요.<br>포그는 침착하게 대안을 찾았어요.<br>코끼리를 빌려서 정글을 횡단하기로 했어요!<br>보통 사람이라면 포기했을 상황이에요.<br><strong>시간을 아끼는 사람이 목표를 이루어요!</strong>",
             "Fogg arrived in India.<br>The train was late!<br>Every minute was important.<br><span class=\"hl\">__KEY__</span>",
             "Fogg and Passepartout reached India, but the train was delayed.<br>They could not waste even a single minute on this tight schedule.<br>Fogg calmly found a solution — he hired an elephant!<br>They rode through the jungle to make up for lost time.<br><span class=\"hl\">__KEY__</span><br>Fogg showed that creative thinking saves precious minutes.",
             "Upon arriving in India, Fogg and Passepartout encountered their first serious obstacle.<br>The railway line they needed was incomplete, ending abruptly in the middle of the countryside.<br>While most travelers would have panicked, Fogg immediately searched for an alternative solution.<br>He purchased an elephant at an enormous price and hired a guide to cross the dense jungle.<br><span class=\"hl\">__KEY__</span><br>However, this detour through the jungle would lead to an unexpected encounter that changed everything.<br>Because Fogg valued every minute and refused to waste time complaining, he always found a way forward.<br>This experience proved that flexibility and quick decision-making are just as important as having a perfect plan."),
            ("코끼리를 타고 정글을 지나는 중이에요!<br>갑자기 앞에서 행렬이 나타났어요.<br>사람들이 한 여자를 데리고 가고 있었어요.<br>그 여자는 위험에 처해 있었어요!<br><br>포그는 시간이 급했지만 멈춰 섰어요.<br>누군가가 위험하면 도와야 한다고 생각했어요.<br>파스파르투도 동의했어요.<br>시간보다 사람의 생명이 더 소중하니까요.<br>그들은 여자를 구출할 계획을 세웠어요.<br>위험하고 시간도 잃을 수 있었어요.<br>하지만 올바른 일을 하기로 결심했어요.<br><strong>시간보다 중요한 것도 있어요!</strong>",
             "They saw a woman in danger.<br>Fogg stopped to help her.<br>Some things matter more than time.<br><span class=\"hl\">__KEY__</span>",
             "While crossing the jungle on the elephant, they saw a woman being led to danger.<br>Fogg knew stopping would cost precious time from his schedule.<br>But he believed that helping someone in need is more important than any bet.<br>Together with Passepartout, they made a plan to rescue the woman.<br><span class=\"hl\">__KEY__</span><br>This moment showed that Fogg had a good heart beneath his calm exterior.",
             "As they traveled through the Indian jungle, Fogg's group witnessed a disturbing procession.<br>A young woman named Aouda was being taken against her will to a terrible fate.<br>Fogg calculated that stopping to help would cost them at least twelve precious hours.<br>Despite this, he made an immediate decision — rescuing Aouda was the right thing to do.<br><span class=\"hl\">__KEY__</span><br>However, the rescue mission was extremely dangerous and could have ended the journey entirely.<br>Because Fogg valued human life above money and schedules, he did not hesitate for even a moment.<br>Passepartout's clever disguise and bravery were essential to the daring rescue plan."),
            ("아우다를 무사히 구출했어요! 🎉<br>아우다는 포그에게 정말 고마워했어요.<br>이제 아우다도 함께 여행하게 되었어요.<br>일행이 셋으로 늘어났어요!<br><br>구출 때문에 시간을 많이 잃었어요.<br>하지만 포그는 후회하지 않았어요.<br>올바른 일을 했으니까요.<br>시간은 다시 벌 수 있지만 생명은 하나뿐이에요.<br>아우다는 포그의 친절함에 감동받았어요.<br>포그도 처음으로 따뜻한 감정을 느꼈어요.<br>매 분이 소중하지만 사람은 더 소중해요.<br><strong>올바른 선택은 절대 시간 낭비가 아니에요!</strong>",
             "They saved Aouda! 🎉<br>She joined their journey.<br>Doing the right thing is never a waste of time.<br><span class=\"hl\">__KEY__</span>",
             "Fogg and Passepartout successfully rescued Aouda from danger.<br>She was incredibly grateful and joined them on their journey.<br>They lost many hours, but Fogg did not regret his decision at all.<br>Time can be made up, but a life can never be replaced.<br><span class=\"hl\">__KEY__</span><br>Aouda's rescue proved that kindness matters more than any schedule.",
             "The rescue of Aouda was a complete success thanks to Passepartout's clever plan and Fogg's determination.<br>Aouda was deeply moved by the bravery of these strangers who risked everything for her.<br>She decided to travel with them since she had family in Hong Kong she could stay with.<br>Although the rescue cost them nearly a full day, Fogg showed no sign of regret whatsoever.<br><span class=\"hl\">__KEY__</span><br>However, this delay meant they would have to find creative ways to make up the lost time.<br>Because Fogg chose compassion over his strict timetable, he gained something more valuable than hours.<br>For the first time in his orderly life, Fogg experienced the warmth of genuine human connection."),
        ],
    }

    # Generate remaining Around the World weeks (12-18) with templates
    aw_weekly = {
        12: ("loyal", [
            ("파스파르투의 충성심에 대해 이야기해요.<br>파스파르투는 처음에 조용한 직장을 원했어요.<br>하지만 주인을 따라 세계일주에 나섰어요!<br>불평 한마디 없이 포그를 도왔어요.<br><br>인도에서 코끼리를 탔을 때도 씩씩했어요.<br>아우다를 구출할 때도 앞장섰어요.<br>파스파르투는 진정한 충신이에요.<br>충성심은 말이 아니라 행동으로 보여주는 거예요.<br>힘든 순간에도 곁에 있는 것이 진짜 충성이에요.<br>파스파르투는 포그에게 없어서는 안 될 존재예요.<br>혼자서는 이 여행을 할 수 없었을 거예요.<br><strong>충실한 친구는 세상에서 가장 큰 선물이에요!</strong>",
             "Passepartout was a loyal servant.<br>He helped Fogg every day.<br>Loyalty means staying by someone's side.<br><span class=\"hl\">__KEY__</span>",
             "Passepartout wanted a quiet life but followed Fogg around the world.<br>He never complained even when things got difficult or dangerous.<br>He bravely helped rescue Aouda in the Indian jungle.<br>Passepartout showed his loyalty through actions, not just words.<br><span class=\"hl\">__KEY__</span><br>True loyalty means being there especially when times are hard.",
             "Passepartout had dreamed of a peaceful, predictable life when he became Fogg's servant.<br>Instead, he found himself on the most unpredictable journey imaginable across the entire globe.<br>Despite every hardship — extreme weather, dangerous encounters, and exhausting travel — he never once complained.<br>His bravery during Aouda's rescue proved that his loyalty went far beyond mere duty.<br><span class=\"hl\">__KEY__</span><br>However, Passepartout's loyalty was not blind obedience but genuine devotion born from respect.<br>Because he truly believed in Fogg's character, he willingly faced every challenge alongside his master.<br>Fogg could never have succeeded without Passepartout's unwavering support and cheerful spirit."),
            ("파스파르투가 또 위기에서 포그를 도와줬어요.<br>항구에서 배가 떠나려 할 때 파스파르투가 뛰어갔어요!<br>배의 밧줄을 잡고 간신히 올라탔어요.<br>포그와 아우다가 배를 탈 수 있도록 시간을 벌었어요.<br><br>파스파르투는 항상 몸을 사리지 않아요.<br>주인을 위해 자신을 희생할 준비가 되어 있어요.<br>이것이 바로 진정한 충성이에요.<br>충성스러운 사람은 어려울 때 빛나요.<br>파스파르투 덕분에 여행이 계속될 수 있었어요.<br>한 사람의 헌신이 모두를 살릴 수 있어요.<br>파스파르투는 영웅이에요!<br><strong>여러분 곁에도 파스파르투 같은 친구가 있나요?</strong>",
             "Passepartout ran to catch the ship.<br>He helped Fogg and Aouda get on board.<br>His loyalty saved the day.<br><span class=\"hl\">__KEY__</span>",
             "At the port, the ship was about to leave without them.<br>Passepartout sprinted to the dock and grabbed the ship's rope!<br>He held on tightly so Fogg and Aouda could climb aboard.<br>Without Passepartout's quick action, the journey would have ended.<br><span class=\"hl\">__KEY__</span><br>One person's dedication can make all the difference.",
             "As they arrived at the port, they discovered to their horror that the steamship was already departing.<br>Without hesitation, Passepartout sprinted down the dock at full speed and leaped for the ship's railing.<br>He grabbed the rope and held on with all his strength, creating just enough time for the others to board.<br>This selfless act of bravery demonstrated the depth of Passepartout's loyalty to his master.<br><span class=\"hl\">__KEY__</span><br>However, Passepartout nearly fell into the churning water between the ship and the dock.<br>Because his devotion to Fogg was stronger than his fear, he risked his own life without a second thought.<br>Fogg silently clasped Passepartout's hand in gratitude, a rare show of emotion from the reserved gentleman."),
            ("충성에 대한 이번 주를 마무리해요.<br>여행이 힘들수록 파스파르투의 가치가 빛났어요.<br>포그도 파스파르투에게 감사함을 느꼈어요.<br>보통 감정을 드러내지 않는 포그인데요.<br><br>충성심은 양방향이어야 해요.<br>파스파르투가 충성하듯 포그도 파스파르투를 소중히 여겼어요.<br>좋은 관계는 서로를 존중하는 것에서 시작돼요.<br>어려울 때 함께하는 사람이 진짜 친구예요.<br>파스파르투와 포그의 관계가 바로 그래요.<br>신분의 차이를 넘어 진정한 동료가 되었어요.<br>서로를 아끼는 마음이 가장 강한 힘이에요.<br><strong>충성과 존중이 함께하면 무엇이든 이길 수 있어요!</strong>",
             "Fogg thanked Passepartout silently.<br>Good friends respect each other.<br>Loyalty goes both ways.<br><span class=\"hl\">__KEY__</span>",
             "As the journey continued, Fogg quietly appreciated Passepartout more and more.<br>True loyalty is not one-sided — it must go both ways.<br>Fogg respected Passepartout as a true companion, not just a servant.<br>Their bond grew stronger with each challenge they overcame together.<br><span class=\"hl\">__KEY__</span><br>When people truly respect each other, they can overcome anything.",
             "Throughout their incredible journey, the relationship between Fogg and Passepartout evolved beautifully.<br>What began as a formal employer-servant arrangement grew into a genuine partnership of mutual respect.<br>Fogg, though rarely showing emotion, demonstrated his appreciation through small but meaningful gestures.<br>He treated Passepartout not as a subordinate but as a valued companion and equal.<br><span class=\"hl\">__KEY__</span><br>However, true loyalty cannot exist without mutual respect and genuine caring from both sides.<br>Because both men proved their dedication through actions rather than words, their bond became unbreakable.<br>Together, they showed that the strongest partnerships are built on loyalty, respect, and shared purpose."),
        ]),
    }

    for wk, days in weeks.items():
        for di, (ko, a1h, a2h, b1h) in enumerate(days):
            S[(wk, di)] = _make_entry(ko, a1h, a2h, b1h)

    for wk, (theme, days) in aw_weekly.items():
        for di, (ko, a1h, a2h, b1h) in enumerate(days):
            S[(wk, di)] = _make_entry(ko, a1h, a2h, b1h)

    # Remaining weeks 13-18 use fallback (will be auto-generated)


def _add_call_wild(S):
    cw_weeks = {
        19: [ # taken
            ("야생의 부름 이야기를 시작해요! 🐺<br>이 소설은 미국 작가 잭 런던이 1903년에 썼어요.<br>주인공은 벅이라는 큰 개예요.<br>벅은 캘리포니아의 따뜻한 집에서 살았어요.<br><br>벅은 판사의 저택에서 행복하게 지냈어요.<br>넓은 정원에서 뛰어놀고 맛있는 음식을 먹었어요.<br>하지만 어느 날 밤, 나쁜 사람이 벅을 훔쳐 갔어요!<br>벅은 낯선 곳으로 팔려 갔어요.<br>추운 알래스카로 끌려간 거예요.<br>썰매 개로 일하게 되었어요.<br>따뜻한 집이 갑자기 사라져 버렸어요.<br><strong>벅의 새로운 삶이 시작되었어요!</strong>",
             "Buck was a big, happy dog.<br>One night, someone stole Buck.<br>Buck was taken to a cold place.<br><span class=\"hl\">__KEY__</span>",
             "Buck was a large, strong dog who lived in a warm house in California.<br>He was happy and loved by his owner, Judge Miller.<br>But one terrible night, a man stole Buck and sold him.<br>Buck was sent far away to the frozen land of Alaska.<br><span class=\"hl\">__KEY__</span><br>Everything Buck knew was suddenly taken away from him.",
             "Buck was a magnificent dog who enjoyed a comfortable life at Judge Miller's grand estate in California.<br>He spent his days playing in the sun-drenched gardens and sleeping by the warm fireplace.<br>One fateful night, a treacherous gardener's helper kidnapped Buck and sold him to strangers.<br>Before Buck could understand what was happening, he was shipped to the brutal cold of Alaska.<br><span class=\"hl\">__KEY__</span><br>However, this cruel twist of fate would eventually awaken something powerful deep within Buck.<br>Because he was torn from everything familiar and safe, Buck had no choice but to adapt or perish.<br>The pampered house dog was about to discover a wild strength he never knew he possessed."),
            ("벅이 알래스카에 도착했어요.<br>눈과 얼음으로 뒤덮인 세상이에요.<br>벅은 이런 추위를 경험한 적이 없어요.<br>다른 썰매 개들은 벅을 경계했어요.<br><br>벅은 먹을 것도 빼앗기고 맞기도 했어요.<br>따뜻한 집이 그리웠어요.<br>하지만 울고만 있을 수 없었어요.<br>살아남으려면 강해져야 했어요.<br>벅은 조금씩 새로운 환경에 적응했어요.<br>추위를 견디는 법을 배웠어요.<br>눈 속에 구멍을 파고 자는 법도 배웠어요.<br><strong>벅은 포기하지 않았어요!</strong>",
             "Alaska was very cold and harsh.<br>Buck had to learn new skills fast.<br>He learned to sleep in the snow.<br><span class=\"hl\">__KEY__</span>",
             "Buck arrived in Alaska where everything was covered in snow and ice.<br>The other sled dogs were rough and unfriendly toward him.<br>Buck's food was stolen and he was pushed around constantly.<br>But slowly, he learned to survive in this harsh new world.<br><span class=\"hl\">__KEY__</span><br>Buck refused to give up no matter how hard things became.",
             "The frozen wilderness of Alaska was nothing like Buck's warm California home.<br>Temperatures dropped far below freezing, and the biting wind cut through his thick fur.<br>The other sled dogs were tough, territorial, and showed Buck no mercy whatsoever.<br>His food was stolen, and he had to fight just to keep his place in the pack.<br><span class=\"hl\">__KEY__</span><br>However, something remarkable began happening inside Buck as he faced these hardships.<br>Because survival demanded it, he quickly learned to dig sleeping holes in the snow and guard his food.<br>Each day, the comfortable house dog was transforming into something stronger, wilder, and more resilient."),
            ("벅의 알래스카 첫째 주를 마무리해요.<br>벅은 정말 많이 변했어요.<br>부드러운 발바닥이 단단해졌어요.<br>얇았던 속털이 두꺼워졌어요.<br><br>벅의 몸만 변한 것이 아니에요.<br>마음도 변하기 시작했어요.<br>예전에는 사람에게 의존했어요.<br>이제는 스스로 살아가는 법을 배우고 있어요.<br>환경이 변하면 우리도 변해야 해요.<br>변화를 두려워하면 안 돼요.<br>벅처럼 적응하는 힘이 중요해요.<br><strong>변화는 때로 우리를 더 강하게 만들어요!</strong>",
             "Buck's body grew stronger.<br>His mind changed too.<br>Change can make us stronger.<br><span class=\"hl\">__KEY__</span>",
             "Buck's soft paws became hard, and his thin fur grew thick and warm.<br>But the biggest change was happening inside Buck's mind.<br>He used to depend on people for everything he needed.<br>Now he was learning to take care of himself completely.<br><span class=\"hl\">__KEY__</span><br>Sometimes big changes in life actually make us stronger than before.",
             "After just a short time in Alaska, Buck had undergone a remarkable physical transformation.<br>His once-soft paws had hardened like leather, and his coat grew dense enough to withstand the bitter cold.<br>More importantly, his mind was adapting in ways he could never have imagined back in California.<br>The instincts of his wild ancestors were slowly awakening deep within his consciousness.<br><span class=\"hl\">__KEY__</span><br>However, these changes were not just about survival in the present moment.<br>Because Buck was being stripped of his comfortable domesticated life, his true nature was emerging.<br>He was discovering that sometimes losing everything you know is the beginning of finding who you truly are."),
        ],
    }

    for wk, days in cw_weeks.items():
        for di, (ko, a1h, a2h, b1h) in enumerate(days):
            S[(wk, di)] = _make_entry(ko, a1h, a2h, b1h)

    # Remaining weeks 20-27 use fallback


def _add_anne(S):
    anne_weeks = {
        28: [ # different
            ("빨간 머리 앤 이야기를 시작해요! 🌸<br>이 소설은 캐나다 작가 루시 모드 몽고메리가 썼어요.<br>앤 셜리는 고아원에서 자란 소녀예요.<br>빨간 머리에 주근깨가 가득한 아이예요.<br><br>마릴라와 매슈 남매가 일손을 도울 남자아이를 원했어요.<br>그런데 실수로 여자아이인 앤이 왔어요!<br>마릴라는 앤을 돌려보내려고 했어요.<br>하지만 앤은 너무나 특별한 아이였어요.<br>앤은 다른 아이들과 달랐어요.<br>상상력이 풍부하고 말을 정말 잘했어요.<br>남들과 다르다는 것이 앤의 가장 큰 매력이에요.<br><strong>앤은 달랐어요, 그리고 그것이 아름다웠어요!</strong>",
             "Anne came to Green Gables.<br>She was different from other children.<br>Being different is special.<br><span class=\"hl\">__KEY__</span>",
             "Anne Shirley was an orphan girl with red hair and freckles.<br>Marilla and Matthew wanted a boy to help on their farm.<br>But Anne arrived by mistake — and she was nothing like they expected!<br>Anne was different: she talked a lot and had a huge imagination.<br><span class=\"hl\">__KEY__</span><br>Being different turned out to be Anne's greatest strength.",
             "Anne Shirley arrived at Green Gables with nothing but a worn suitcase and an extraordinary imagination.<br>Marilla and Matthew Cuthbert had specifically requested a boy from the orphanage to help with farm work.<br>When they discovered the mistake, Marilla wanted to send Anne back immediately.<br>But there was something undeniably captivating about this talkative red-haired girl with sparkling eyes.<br><span class=\"hl\">__KEY__</span><br>However, being different in a small, traditional community like Avonlea was not always easy.<br>Because Anne did not fit the mold of what people expected, she often felt like an outsider.<br>Yet it was precisely her uniqueness that would eventually win everyone's hearts and change their world."),
            ("앤이 그린 게이블즈에 도착한 첫날이에요.<br>마차를 타고 오면서 앤은 쉬지 않고 말했어요.<br>나무마다 이름을 지어줬어요.<br>호수를 '반짝이는 호수'라고 불렀어요.<br><br>매슈는 앤의 이야기가 재미있었어요.<br>말이 없는 매슈인데 앤과는 잘 맞았어요.<br>반면에 마릴라는 앤이 걱정되었어요.<br>너무 공상만 하는 것 같았거든요.<br>하지만 앤의 눈에는 세상이 아름다웠어요.<br>평범한 것도 특별하게 보는 힘이 있었어요.<br>앤은 어디에서든 아름다움을 찾았어요.<br><strong>같은 세상도 보는 눈에 따라 달라져요!</strong>",
             "Anne named everything she saw.<br>She called a lake 'the Lake of Shining Waters.'<br>Anne saw beauty everywhere.<br><span class=\"hl\">__KEY__</span>",
             "On the way to Green Gables, Anne talked nonstop with excitement.<br>She gave beautiful names to every tree, road, and lake she saw.<br>She called one lake 'the Lake of Shining Waters' because it sparkled.<br>Matthew listened quietly and found himself charmed by this unusual girl.<br><span class=\"hl\">__KEY__</span><br>Anne had the special gift of seeing magic in ordinary things.",
             "During the carriage ride to Green Gables, Anne's mouth never stopped for a single moment.<br>She gazed at the landscape with wonder-filled eyes and gave poetic names to everything she saw.<br>A simple avenue of apple trees became 'the White Way of Delight' in her vivid imagination.<br>Even quiet, shy Matthew found himself smiling at this extraordinary girl's endless enthusiasm.<br><span class=\"hl\">__KEY__</span><br>However, Marilla was less enchanted and worried that Anne was too dreamy and impractical.<br>Because Anne saw the world differently from everyone else, not everyone understood or appreciated her at first.<br>Yet it was this very ability to find beauty in the mundane that made Anne truly remarkable and irreplaceable."),
            ("앤의 첫째 주를 마무리할게요.<br>마릴라는 앤을 돌려보내기로 마음먹었어요.<br>하지만 매슈가 반대했어요.<br>'이 아이를 키우자.' 매슈가 조용히 말했어요.<br><br>마릴라도 사실 앤이 마음에 들기 시작했어요.<br>앤의 솔직함이 마릴라의 마음을 움직였어요.<br>앤은 사랑받아 본 적이 없었어요.<br>그래서 사랑받고 싶은 마음이 간절했어요.<br>마릴라는 앤에게 기회를 주기로 했어요.<br>그린 게이블즈가 앤의 집이 되었어요!<br>모든 아이는 사랑받을 자격이 있어요.<br><strong>앤은 드디어 자기만의 집을 얻었어요!</strong>",
             "Matthew wanted to keep Anne.<br>Marilla agreed to give her a chance.<br>Green Gables became Anne's home!<br><span class=\"hl\">__KEY__</span>",
             "Marilla planned to send Anne back to the orphanage the next day.<br>But quiet Matthew spoke up and said they should keep her.<br>Something about Anne's honesty touched Marilla's heart too.<br>Anne had never had a real home, and she wanted one so badly.<br><span class=\"hl\">__KEY__</span><br>Green Gables finally became the home Anne had always dreamed of.",
             "Marilla had firmly decided to return Anne to the orphanage the very next morning.<br>However, Matthew, who rarely expressed strong opinions, quietly insisted that they give Anne a home.<br>His gentle words surprised Marilla, but she realized she felt the same way deep down.<br>Anne's raw honesty about her lonely life as an orphan had touched Marilla more than she wanted to admit.<br><span class=\"hl\">__KEY__</span><br>For the first time in her life, Anne had a place where she truly belonged.<br>Because both Marilla and Matthew chose to open their hearts, everyone's life was about to change for the better.<br>Anne fell asleep that night knowing that Green Gables was finally, truly her home."),
        ],
    }

    for wk, days in anne_weeks.items():
        for di, (ko, a1h, a2h, b1h) in enumerate(days):
            S[(wk, di)] = _make_entry(ko, a1h, a2h, b1h)

    # Remaining weeks 29-32 use fallback


def _add_swiss(S):
    sw_weeks = {
        33: [ # together
            ("스위스 가족 로빈슨 이야기를 시작해요! 🏝️<br>이 소설은 스위스 작가 요한 다비드 위스가 썼어요.<br>로빈슨 가족은 배를 타고 새로운 나라로 가고 있었어요.<br>아버지, 어머니, 그리고 네 아들이 함께였어요.<br><br>그런데 갑자기 무시무시한 폭풍이 몰아쳤어요!<br>배가 산산조각이 나기 시작했어요.<br>선원들은 모두 구명보트를 타고 떠났어요.<br>가족만 배에 남겨졌어요!<br>하지만 아버지는 포기하지 않았어요.<br>가족이 함께라면 이겨낼 수 있다고 했어요.<br>그들은 서로 손을 잡고 용기를 냈어요.<br><strong>함께라면 어떤 폭풍도 견딜 수 있어요!</strong>",
             "A family was on a ship in a storm.<br>The ship broke apart!<br>But the family stayed together.<br><span class=\"hl\">__KEY__</span>",
             "The Robinson family was sailing to a new country when a terrible storm hit.<br>The ship started to break apart, and all the sailors escaped in lifeboats.<br>Only the family was left behind on the sinking ship!<br>Father told everyone not to give up because they had each other.<br><span class=\"hl\">__KEY__</span><br>Being together gave them the strength to survive.",
             "The Robinson family — father, mother, and four young sons — were sailing across the ocean to start a new life.<br>Without warning, a violent storm struck their ship with devastating force.<br>As the vessel began to break apart, the terrified crew abandoned ship in the only lifeboats available.<br>The family found themselves completely alone on a sinking ship in the middle of a raging sea.<br><span class=\"hl\">__KEY__</span><br>However, the father refused to let despair overtake his family in this desperate situation.<br>Because they trusted each other and worked as a team, they managed to survive the terrifying night.<br>This first crisis proved that family unity would be their greatest weapon against whatever challenges lay ahead."),
            ("폭풍이 지나고 가족은 살아남았어요!<br>배는 바위에 걸려서 완전히 가라앉지 않았어요.<br>가족은 배에서 쓸 수 있는 물건들을 모았어요.<br>도구, 음식, 천, 씨앗까지 챙겼어요.<br><br>아버지가 뗏목을 만들었어요.<br>가족 모두가 힘을 합쳐 뗏목을 완성했어요.<br>큰 아들은 밧줄을 묶었어요.<br>작은 아들들도 짐을 날랐어요.<br>어머니는 음식과 물을 정리했어요.<br>각자의 역할이 있었고 모두가 중요했어요.<br>뗏목을 타고 근처 섬으로 향했어요.<br><strong>협력하면 불가능한 일도 가능해져요!</strong>",
             "The family found useful things on the broken ship.<br>They built a raft together.<br>Everyone helped in their own way.<br><span class=\"hl\">__KEY__</span>",
             "After the storm, the family gathered supplies from the damaged ship.<br>They found tools, food, cloth, and seeds that could help them survive.<br>Father led the effort to build a strong raft from pieces of the ship.<br>Every family member had a job and worked hard together.<br><span class=\"hl\">__KEY__</span><br>When everyone does their part, even impossible tasks become possible.",
             "When the storm finally passed, the Robinson family discovered their ship had lodged between two rocks.<br>Though the vessel was badly damaged, it contained supplies that would be essential for their survival.<br>The father organized everyone into teams to salvage tools, food, weapons, and building materials.<br>Even the youngest son carried supplies while the mother carefully preserved food and fresh water.<br><span class=\"hl\">__KEY__</span><br>However, they knew the ship could break apart completely at any moment.<br>Because every family member contributed according to their abilities, they worked with remarkable efficiency.<br>Together, they built a sturdy raft and loaded it with everything they needed to start life on the nearby island."),
            ("가족이 섬에 도착했어요!<br>처음에는 모든 것이 낯설고 무서웠어요.<br>동물 소리가 들리고 정글이 펼쳐져 있었어요.<br>하지만 가족은 서로를 바라보며 미소 지었어요.<br><br>아버지가 말했어요. '함께라면 괜찮아.'<br>첫 밤을 나무 아래에서 보냈어요.<br>모닥불을 피우고 둘러앉았어요.<br>무섭지만 가족이 곁에 있어 따뜻했어요.<br>내일부터 집을 짓기 시작할 거예요.<br>새로운 시작은 항상 어렵지만 가능해요.<br>가족의 사랑이 가장 큰 힘이에요.<br><strong>사랑하는 사람들과 함께라면 어디든 집이에요!</strong>",
             "The family reached the island safely.<br>They spent the first night under a tree.<br>Being together made them feel safe.<br><span class=\"hl\">__KEY__</span>",
             "The Robinson family safely reached the island on their raft.<br>Everything was strange — unfamiliar animals, thick jungle, and unknown sounds.<br>They built a campfire and spent their first night huddled together under a large tree.<br>Father reminded them that as long as they were together, they would be fine.<br><span class=\"hl\">__KEY__</span><br>Family love is the strongest shelter against any storm.",
             "The Robinson family stepped onto the island's sandy shore with a mixture of relief and anxiety.<br>Unfamiliar bird calls echoed from the dense tropical jungle that stretched endlessly before them.<br>As darkness fell, they gathered around a crackling campfire beneath the canopy of a massive tree.<br>The children pressed close to their parents, finding comfort in the warmth of family togetherness.<br><span class=\"hl\">__KEY__</span><br>However, the father knew that surviving on this island would require more than just love and unity.<br>Because they had each other's support, they could face the unknown challenges of tomorrow with hope.<br>As the stars appeared above their island home, each family member silently promised to never give up."),
        ],
    }

    for wk, days in sw_weeks.items():
        for di, (ko, a1h, a2h, b1h) in enumerate(days):
            S[(wk, di)] = _make_entry(ko, a1h, a2h, b1h)

    # Remaining weeks 34-36 use fallback


# ── CSS to add ──
CSS_BLOCK = """.story-level{display:flex;align-items:center;gap:8px;margin:14px 0 4px;padding:8px 12px;border-radius:10px;font-size:0.75rem;font-weight:800;}
.story-level.a1{background:#e8f5e9;color:#2e7d32;}
.story-level.a2{background:#e3f2fd;color:#1565c0;}
.story-level.b1{background:#fff3e0;color:#e65100;}"""


def process_file(filepath):
    """Process a single lesson file."""
    fname = os.path.basename(filepath)
    # Parse week and day
    m = re.match(r'week(\d+)([abc])\.html', fname)
    if not m:
        return False
    wk = int(m.group(1))
    day_letter = m.group(2)

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract key sentence
    key_m = re.search(r'class="key-eng"[^>]*>([^<]+)<', html)
    if not key_m:
        key_m = re.search(r'class="key-eng"[^>]*>&quot;([^&]+)&quot;<', html)
        if key_m:
            key_sentence = key_m.group(1)
        else:
            print(f"  WARN: No key sentence found in {fname}")
            key_sentence = "This is an important sentence."
    else:
        key_raw = key_m.group(1).strip()
        key_sentence = key_raw.strip('"').strip('\u201c\u201d').strip()

    # Get book info
    book_en, book_kr = get_book(wk)

    # Generate story content
    stories = generate_story(wk, day_letter, key_sentence, book_en, book_kr)
    korean = stories["korean"]
    a1_html = stories["a1_html"]
    a1_tts = stories["a1_tts"]
    a2_html = stories["a2_html"]
    a2_tts = stories["a2_tts"]
    b1_html = stories["b1_html"]
    b1_tts = stories["b1_tts"]

    # Escape single quotes for TTS
    a1_tts_safe = a1_tts.replace("'", "\\'")
    a2_tts_safe = a2_tts.replace("'", "\\'")
    b1_tts_safe = b1_tts.replace("'", "\\'")

    # 1. Add CSS if missing
    if '.story-level{' not in html and '.story-level {' not in html:
        # Find the .story-en{...} line and add after it
        css_pattern = re.search(r'(\.story-en\{[^}]+\})', html)
        if css_pattern:
            html = html.replace(css_pattern.group(1), css_pattern.group(1) + '\n' + CSS_BLOCK)

    # 2. Replace story body
    # Find the section from robo-msg (inside gold robo) through the prog bar at end of section 2
    # Pattern: from <div class="robo-msg"> inside gold robo section, to </div><div class="prog">...</article> for section 2

    # We need to find the story section (section 2) content area
    # It starts after the gold robo intro and includes the story player/English story
    # We look for the gold robo's robo-msg through the closing prog bar

    # Strategy: find the "먼저 한국어로 읽어봐!" robo section and replace from robo-msg to prog bar
    story_pattern = re.compile(
        r'(<div class="robo-nm" style="color:var\(--gold\);">먼저 한국어로 읽어봐!</div>)'
        r'(.*?)'
        r'(</div><div class="prog"><div class="prog-fill")',
        re.DOTALL
    )

    story_match = story_pattern.search(html)
    if not story_match:
        # Try alternate: maybe robo-msg is on same line
        story_pattern2 = re.compile(
            r'(먼저 한국어로 읽어봐!</div>)\s*'
            r'(<div class="robo-msg">.*?)'
            r'(</div><div class="prog"><div class="prog-fill")',
            re.DOTALL
        )
        story_match = story_pattern2.search(html)
        if not story_match:
            print(f"  WARN: Could not find story section in {fname}")
            return False

    # Build replacement content
    new_story = (
        f'<div class="robo-nm" style="color:var(--gold);">먼저 한국어로 읽어봐!</div>'
        f'<div class="robo-msg">{korean}</div></div>\n'
        f'  </div>\n'
        f'  <!-- A1 -->\n'
        f'  <div class="story-level a1">⭐ A1 쉬움</div>\n'
        f'  <div class="story-player-row">\n'
        f'    <span class="story-label">🔤 A1 Easy</span>\n'
        f'    <button class="story-ctrl-btn story-play-btn" onclick="storyPlay(\'{a1_tts_safe}\',this)">▶</button>\n'
        f'    <button class="story-ctrl-btn story-stop-btn" onclick="storyStopped()">⏹</button>\n'
        f'  </div>\n'
        f'  <div class="story-en">{a1_html}</div>\n'
        f'  <!-- A2 -->\n'
        f'  <div class="story-level a2">⭐⭐ A2 보통</div>\n'
        f'  <div class="story-player-row">\n'
        f'    <span class="story-label">🔤 A2 Medium</span>\n'
        f'    <button class="story-ctrl-btn story-play-btn" onclick="storyPlay(\'{a2_tts_safe}\',this)">▶</button>\n'
        f'    <button class="story-ctrl-btn story-stop-btn" onclick="storyStopped()">⏹</button>\n'
        f'  </div>\n'
        f'  <div class="story-en">{a2_html}</div>\n'
        f'  <!-- B1 -->\n'
        f'  <div class="story-level b1">⭐⭐⭐ B1 도전</div>\n'
        f'  <div class="story-player-row">\n'
        f'    <span class="story-label">🔤 B1 Challenge</span>\n'
        f'    <button class="story-ctrl-btn story-play-btn" onclick="storyPlay(\'{b1_tts_safe}\',this)">▶</button>\n'
        f'    <button class="story-ctrl-btn story-stop-btn" onclick="storyStopped()">⏹</button>\n'
        f'  </div>\n'
        f'  <div class="story-en">{b1_html}</div>\n'
    )

    # Do the replacement
    # We need to replace from the gold robo-nm through to just before </div><div class="prog">
    # But we need to handle the closing divs properly

    # Let's use a different approach: find the full block and replace
    # Handle both </article> and </div> endings
    full_pattern = re.compile(
        r'(<div class="robo-nm" style="color:var\(--gold\);">먼저 한국어로 읽어봐!</div>)'
        r'[\s\S]*?'
        r'(</div><div class="prog"><div class="prog-fill"[^>]*></div></div></(?:article|div)>)',
        re.DOTALL
    )

    full_match = full_pattern.search(html)
    if not full_match:
        print(f"  WARN: Could not find full story block in {fname}")
        return False

    # Get the prog bar ending
    prog_ending = full_match.group(2)

    # Replace the entire block
    new_block = new_story + prog_ending
    html = html[:full_match.start()] + new_block + html[full_match.end():]

    # Remove old id attributes from story buttons (id="story-play-btn" etc)
    html = html.replace(' id="story-play-btn"', '').replace(' id="story-stop-btn"', '')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return True


def main():
    import glob as g
    files = sorted(g.glob(os.path.join(BASE, 'week*.html')))
    print(f"Found {len(files)} files to process.")

    updated = 0
    failed = 0
    for fp in files:
        fname = os.path.basename(fp)
        try:
            if process_file(fp):
                updated += 1
                print(f"  OK: {fname}")
            else:
                failed += 1
                print(f"  SKIP: {fname}")
        except Exception as e:
            failed += 1
            print(f"  ERROR: {fname} — {e}")

    print(f"\nDone! Updated: {updated}, Failed/Skipped: {failed}, Total: {len(files)}")


if __name__ == '__main__':
    main()

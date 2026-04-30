"""Fix G4 W05/06/10/12/22 story content per G4_fix_spec.md.

Per spec:
- Don't touch: <title>, top-bar header, hero overlay <h2>/<p>, PAGE_DATA constant
- DO replace: key-eng/key-kr, Robo welcome msg, Day-pill previews,
  Korean intro story, A1/A2 stories, vocab cards, all 3 games,
  listening, dictation, quiz, writing exercise, completion card,
  next-title preview link
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Users\cecsu\cecenglishcamp.github.io\camp-a\grade4")


def replace_block(text: str, anchor_open: str, anchor_close: str, new_inner: str) -> tuple[str, bool]:
    """Replace text between (and including) anchor_open and the LAST anchor_close
    that closes the matching block. Returns (new_text, replaced)."""
    i = text.find(anchor_open)
    if i < 0:
        return text, False
    j = text.find(anchor_close, i + len(anchor_open))
    if j < 0:
        return text, False
    j += len(anchor_close)
    return text[:i] + new_inner + text[j:], True


def replace_first(text: str, find: str, repl: str) -> tuple[str, bool]:
    if find in text:
        return text.replace(find, repl, 1), True
    return text, False


# =========================================================================
# Section template builders — same shape across all Day files
# =========================================================================

VOCAB_EMOJIS = {
    "wanted": "💭", "missed": "💔", "home": "🏠", "family": "👨‍👩‍👧", "longing": "😢",
    "followed": "👣", "yellow": "💛", "brick": "🧱", "road": "🛣️", "wizard": "🧙",
    "kindness": "💝", "nature": "🌷", "character": "✨", "generous": "🤲", "habit": "🔄",
    "changed": "🔄", "positivity": "☀️", "contagious": "🤗", "spread": "🌊", "influence": "🌟",
    "cared": "🌿", "joy": "😊", "purpose": "🎯", "routine": "📅", "growth": "🌱",
}

VOCAB_KR = {
    "wanted": "원했다", "missed": "그리워했다", "home": "집", "family": "가족", "longing": "간절함",
    "followed": "따라갔다", "yellow": "노란", "brick": "벽돌", "road": "길", "wizard": "마법사",
    "kindness": "친절함", "nature": "본성", "character": "성품", "generous": "너그러운", "habit": "습관",
    "changed": "변화시켰다", "positivity": "긍정", "contagious": "전염되는", "spread": "퍼졌다", "influence": "영향",
    "cared": "돌봤다", "joy": "기쁨", "purpose": "목적", "routine": "일과", "growth": "성장",
}


def vocab_card_html(word: str, ex: str) -> str:
    em = VOCAB_EMOJIS.get(word, "💡")
    kr = VOCAB_KR.get(word, "")
    return (
        f'<div class="v-card" onclick="speak(\'{word}\')">'
        f'<div class="v-emoji">{em}</div>'
        f'<div class="v-eng">{word}</div>'
        f'<div class="v-kr">{kr}</div>'
        f'<div class="v-ex">"{ex}"</div>'
        f'<button class="v-play" onclick="event.stopPropagation();speak(\'{word}\')">🔊 듣기</button>'
        f'</div>'
    )


# =========================================================================
# Per-file specifications (from G4_fix_spec.md)
# =========================================================================

SPEC = {
    # =====================================================================
    # WEEK 05 — Wizard of Oz
    # =====================================================================
    "week05a.html": dict(
        prev_kr=None, prev_en=None,
        today_en="Dorothy wanted to go home.",
        today_kr="도로시는 집에 가고 싶었어요.",
        next_en_pill="Dorothy wanted to go home more than anything.",
        robo_msg=(
            "wanted는 원했다! 🌪️<br>"
            "도로시가 캔자스 집을 그리워하고 있어요!<br>"
            "<b>\"Dorothy wanted to go home.\"</b>"
        ),
        story_robo_kr=(
            "거대한 토네이도가 도로시를 캔자스에서 먼 곳으로 데려갔어요. 🌪️<br>"
            "도로시는 아름답지만 낯선 땅에 도착했어요.<br>"
            "엠 이모와 헨리 아저씨, 토토가 그리웠어요. 😢<br>"
            "도로시는 무엇보다 집에 돌아가고 싶었어요.<br>"
            "<strong>도로시는 집에 가고 싶었어요!</strong>"
        ),
        story_a1_text=(
            "Dorothy was not in Kansas anymore.<br>"
            "A big tornado took her far away.<br>"
            "She saw strange colors and new places.<br>"
            "But Dorothy only wanted one thing.<br>"
            "<span class=\"hl\">She wanted to go home.</span>"
        ),
        story_a2_text=(
            "A huge tornado carried Dorothy far from her home in Kansas.<br>"
            "She landed in a colorful land she had never seen before.<br>"
            "Everything looked beautiful, but Dorothy felt scared and confused.<br>"
            "More than anything in the world, Dorothy wanted to go home.<br>"
            "<span class=\"hl\">Dorothy wanted to go home.</span>"
        ),
        vocab=[("wanted", "Dorothy wanted to go home."),
               ("missed", "She missed her family."),
               ("home", "Home is in Kansas."),
               ("family", "Her family loved her.")],
        game1_q='"Dorothy wanted to go ___."',
        game1_answer="home", game1_distractors=["wanted", "Kansas"],
        game2_kr='"도로시는 집에 가고 싶었어요."를 영어로 만들어봐!',
        game2_words=["Dorothy", "wanted", "to", "go", "home"],
        game2_answer="Dorothy wanted to go home",
        match_pairs=[("wanted", "원했다"), ("home", "집"), ("family", "가족"), ("missed", "그리워했다")],
        listen_sentence="Dorothy wanted to go home.",
        listen_emoji_label_ok=("🏠", "집에 가고 싶었다"),
        listen_distractors=[("👑", "왕이 되고 싶었다"), ("🍰", "케이크를 먹고 싶었다")],
        dict_word="wanted", dict_hint="w _ n t e d",
        quiz=[
            ("Q1. 도로시가 가장 원했던 것은 무엇인가요?",
             "🏠 집에 돌아가는 것",
             ["🧙 오즈의 마법사가 되는 것", "🦁 사자와 친구가 되는 것"]),
            ("Q2. 도로시를 집에서 데려간 것은 무엇인가요?",
             "🌪️ 토네이도",
             ["🧙 마법사", "🦁 사자"]),
        ],
        write_q='"Dorothy wanted to go ___."',
        write_answer="home",
        write_distractors=["Kansas", "school"],
        write_prompt="🖊️ 내가 집을 떠난다면 가장 그리울 것은? 영어로 써봐!",
        complete_emoji="🌪️🎉🏠",
        complete_sub='핵심 표현: <strong>"Dorothy wanted to go home."</strong> ✅<br>단어 4개 완성! ✅',
        complete_robo="수요일 Day 2에서 계속해요! 💪",
    ),

    "week05b.html": dict(
        prev_en="Dorothy wanted to go home.",
        today_en="Dorothy wanted to go home more than anything.",
        today_kr="도로시는 무엇보다 집에 가고 싶었어요.",
        next_en_pill="Dorothy wanted to go home because she missed her family.",
        robo_msg=(
            "more than anything은 무엇보다! 🌈<br>"
            "도로시의 간절한 마음을 느껴봐요!<br>"
            "<b>\"Dorothy wanted to go home more than anything.\"</b>"
        ),
        story_robo_kr=(
            "도로시는 새 친구들과 오즈의 나라를 여행했어요. 🌈<br>"
            "에메랄드 시티가 저 멀리 반짝였어요. ✨<br>"
            "하지만 도로시의 마음속에는 항상 고향 캔자스가 있었어요.<br>"
            "<strong>도로시는 무엇보다 집에 가고 싶었어요!</strong>"
        ),
        story_a1_text=(
            "Dorothy was in a strange and colorful land.<br>"
            "She saw many amazing things around her.<br>"
            "But she did not feel happy. She felt very sad.<br>"
            "<span class=\"hl\">Dorothy wanted to go home more than anything.</span>"
        ),
        story_a2_text=(
            "Dorothy traveled through the magical Land of Oz with her new friends.<br>"
            "She saw the Emerald City shining in the distance.<br>"
            "Everything was wonderful and exciting, but her heart ached for home.<br>"
            "No beautiful sight could make her forget Kansas.<br>"
            "<span class=\"hl\">Dorothy wanted to go home more than anything in the world.</span>"
        ),
        vocab=[("wanted", "She wanted to go home."),
               ("missed", "She missed her aunt."),
               ("home", "Home was far away."),
               ("family", "Her family was waiting.")],
        game1_q='"Dorothy wanted to go home ___ anything."',
        game1_answer="more than", game1_distractors=["less than", "as much as"],
        game2_kr='"도로시는 무엇보다 집에 가고 싶었어요."를 영어로 만들어봐!',
        game2_words=["Dorothy", "wanted", "to", "go", "home", "more", "than", "anything"],
        game2_answer="Dorothy wanted to go home more than anything",
        match_pairs=[("more than", "무엇보다"), ("anything", "무엇이든"),
                     ("home", "집"), ("missed", "그리워했다")],
        listen_sentence="Dorothy wanted to go home more than anything.",
        listen_emoji_label_ok=("🌈", "무엇보다 집에 가고 싶었다"),
        listen_distractors=[("🍩", "도넛을 먹고 싶었다"), ("👑", "왕관을 쓰고 싶었다")],
        dict_word="anything", dict_hint="a n y _ h i n g",
        quiz=[
            ("Q1. 도로시가 오즈에서도 행복하지 않은 이유는?",
             "💔 집이 너무 그리워서",
             ["🍰 음식이 맛없어서", "👟 신발이 작아서"]),
            ("Q2. \"more than anything\"의 뜻은?",
             "🌈 무엇보다",
             ["⏰ 잠깐만", "🔄 다시"]),
        ],
        write_q='"Dorothy wanted to go home ___ anything."',
        write_answer="more than",
        write_distractors=["less than", "without"],
        write_prompt="🖊️ I want ______ more than anything. (영어로 써봐!)",
        complete_emoji="🌈💛✨",
        complete_sub='핵심 표현: <strong>"Dorothy wanted to go home more than anything."</strong> ✅',
        complete_robo="금요일 Day 3에서 완성해요! 💪",
    ),

    "week05c.html": dict(
        prev_en="Dorothy wanted to go home more than anything.",
        today_en="Dorothy wanted to go home because she missed her family.",
        today_kr="도로시는 가족이 그리워서 집에 가고 싶었어요.",
        next_en_pill="She followed the road.",  # W06a
        next_week_label="다음 주(W6) Day 1",
        robo_msg=(
            "because는 왜냐하면! 💛<br>"
            "도로시가 집에 가고 싶은 이유를 because로 말해봐요!<br>"
            "<b>\"Dorothy wanted to go home because she missed her family.\"</b>"
        ),
        story_robo_kr=(
            "도로시는 오즈에서 허수아비, 양철 나무꾼, 사자와 친구가 됐어요. 🦁<br>"
            "하지만 매일 밤 엠 이모와 헨리 아저씨가 생각났어요. 💭<br>"
            "도로시는 가족이 그리워서 집에 가고 싶었어요.<br>"
            "<strong>사랑하는 사람이 가장 소중하다는 것을 배웠어요!</strong>"
        ),
        story_a1_text=(
            "Dorothy made new friends in Oz.<br>"
            "But she still thought about her family every night.<br>"
            "She missed Auntie Em and Uncle Henry.<br>"
            "<span class=\"hl\">Dorothy wanted to go home because she missed her family.</span>"
        ),
        story_a2_text=(
            "Dorothy had seen so many wonders in the Land of Oz.<br>"
            "She had made friends with a Scarecrow, a Tin Man, and a Lion.<br>"
            "They were kind and brave, and she loved them dearly.<br>"
            "But every night, Dorothy thought of Auntie Em and Uncle Henry.<br>"
            "<span class=\"hl\">Dorothy wanted to go home because she missed her family so much.</span>"
        ),
        vocab=[("wanted", "She wanted to go home."),
               ("missed", "She missed her family."),
               ("home", "Home was Kansas."),
               ("family", "Her family was everything.")],
        game1_q='"Dorothy wanted to go home ___ she missed her family."',
        game1_answer="because", game1_distractors=["but", "or"],
        game2_kr='"도로시는 가족이 그리워서 집에 가고 싶었어요."를 영어로 만들어봐!',
        game2_words=["Dorothy", "wanted", "to", "go", "home", "because", "she", "missed", "her", "family"],
        game2_answer="Dorothy wanted to go home because she missed her family",
        match_pairs=[("because", "왜냐하면"), ("missed", "그리워했다"),
                     ("family", "가족"), ("home", "집")],
        listen_sentence="Dorothy wanted to go home because she missed her family.",
        listen_emoji_label_ok=("👨‍👩‍👧", "가족이 그리워서"),
        listen_distractors=[("🍰", "케이크가 먹고 싶어서"), ("💰", "돈을 벌고 싶어서")],
        dict_word="because", dict_hint="b _ c a u s e",
        quiz=[
            ("Q1. 도로시가 집에 가고 싶은 이유는?",
             "👨‍👩‍👧 가족이 그리워서",
             ["🦁 사자가 무서워서", "🌧️ 비가 와서"]),
            ("Q2. because 뒤에 오는 것은?",
             "💡 이유 (reason)",
             ["⏰ 시간 (time)", "📍 장소 (place)"]),
        ],
        write_q='"Dorothy wanted to go home ___ she missed her family."',
        write_answer="because",
        write_distractors=["but", "and"],
        write_prompt="🖊️ I want to ______ because I miss ______. (영어로 써봐!)",
        complete_emoji="💛🦁🏠",
        complete_sub='핵심 표현: <strong>"Dorothy wanted to go home because she missed her family."</strong> ✅<br>Week 5 완성! ✅',
        complete_robo="다음 주에 새 표현으로 만나요! 💪",
    ),

    # =====================================================================
    # WEEK 06 — Wizard of Oz (Day 2 only)
    # =====================================================================
    "week06b.html": dict(
        prev_en="She followed the road.",
        today_en="She followed the yellow brick road.",
        today_kr="그녀는 노란 벽돌 길을 따라갔어요.",
        next_en_pill="She followed the yellow brick road to find the Wizard.",
        robo_msg=(
            "followed는 따라갔다! 🟡<br>"
            "노란 벽돌 길이 어디로 이어질까요?<br>"
            "<b>\"She followed the yellow brick road.\"</b>"
        ),
        story_robo_kr=(
            "착한 마녀 글린다가 반짝이는 노란 벽돌 길을 가리켰어요. ✨<br>"
            "\"노란 벽돌 길을 따라가세요\"라고 말했어요.<br>"
            "도로시는 토토와 함께 그 길을 따라갔어요. 🐕<br>"
            "<strong>그녀는 노란 벽돌 길을 따라갔어요!</strong>"
        ),
        story_a1_text=(
            "Dorothy saw a long road made of yellow bricks.<br>"
            "The road went far, far away.<br>"
            "A good witch told her to follow it.<br>"
            "<span class=\"hl\">She followed the yellow brick road.</span>"
        ),
        story_a2_text=(
            "Glinda the Good Witch pointed to a winding road of golden bricks.<br>"
            "\"Follow the yellow brick road,\" she said with a smile.<br>"
            "Dorothy did not know where it led, but she trusted the kind witch.<br>"
            "She stepped onto the bright path with Toto by her side.<br>"
            "<span class=\"hl\">She followed the yellow brick road all the way to the Emerald City.</span>"
        ),
        vocab=[("followed", "She followed the road."),
               ("yellow", "Yellow is bright."),
               ("brick", "The bricks were gold."),
               ("road", "The road was long.")],
        game1_q='"She followed the ___ brick road."',
        game1_answer="yellow", game1_distractors=["red", "blue"],
        game2_kr='"그녀는 노란 벽돌 길을 따라갔어요."를 영어로 만들어봐!',
        game2_words=["She", "followed", "the", "yellow", "brick", "road"],
        game2_answer="She followed the yellow brick road",
        match_pairs=[("yellow", "노란"), ("brick", "벽돌"),
                     ("road", "길"), ("followed", "따라갔다")],
        listen_sentence="She followed the yellow brick road.",
        listen_emoji_label_ok=("🟡", "노란 벽돌 길을 따라갔다"),
        listen_distractors=[("🌊", "강을 건넜다"), ("⛰️", "산을 올라갔다")],
        dict_word="yellow", dict_hint="y _ l l o w",
        quiz=[
            ("Q1. 도로시가 따라간 길은 어떤 색인가요?",
             "🟡 노란색 (yellow)",
             ["🔴 빨간색 (red)", "🔵 파란색 (blue)"]),
            ("Q2. 누가 도로시에게 길을 알려줬나요?",
             "🧙‍♀️ 착한 마녀 글린다",
             ["🦁 사자", "🦅 독수리"]),
        ],
        write_q='"She followed the ___ brick road."',
        write_answer="yellow",
        write_distractors=["green", "white"],
        write_prompt="🖊️ I followed the ______ to ______. (영어로 써봐!)",
        complete_emoji="🟡🧱🛣️",
        complete_sub='핵심 표현: <strong>"She followed the yellow brick road."</strong> ✅',
        complete_robo="금요일 Day 3에서 완성해요! 💪",
    ),

    # =====================================================================
    # WEEK 10 — Pollyanna (Day 2 only)
    # =====================================================================
    "week10b.html": dict(
        prev_en="She was kind and found good.",
        today_en="She always found good because she was kind.",
        today_kr="그녀는 친절했기 때문에 항상 좋은 것을 찾았어요.",
        next_en_pill="She always found something good because kindness was her nature.",
        robo_msg=(
            "always는 항상! 🌸<br>"
            "폴리아나는 어떤 상황에서도 좋은 점을 찾았어요!<br>"
            "<b>\"She always found good because she was kind.\"</b>"
        ),
        story_robo_kr=(
            "폴리아나는 엄격한 폴리 이모 집에 이사했어요. 🏠<br>"
            "어려운 상황에서도 항상 좋은 점을 찾는 '기쁨 게임'을 했어요. 😊<br>"
            "그녀는 친절했기 때문에 항상 좋은 것을 발견할 수 있었어요.<br>"
            "<strong>친절한 마음이 있으면 어디서든 좋은 점이 보여요!</strong>"
        ),
        story_a1_text=(
            "Pollyanna was a happy girl. She smiled every day.<br>"
            "When bad things happened, she looked for the good part.<br>"
            "She was always kind to everyone she met.<br>"
            "<span class=\"hl\">She always found good because she was kind.</span>"
        ),
        story_a2_text=(
            "Pollyanna moved to live with her strict Aunt Polly.<br>"
            "Life was not easy, but Pollyanna never complained.<br>"
            "She played the \"Glad Game\" — always finding something to be happy about.<br>"
            "Even when people were rude, she saw the best in them.<br>"
            "<span class=\"hl\">She always found good because she was kind at heart.</span>"
        ),
        vocab=[("kindness", "Her kindness shone."),
               ("nature", "Kindness was her nature."),
               ("character", "Her character was strong."),
               ("generous", "She was generous to all.")],
        game1_q='"She ___ found good because she was kind."',
        game1_answer="always", game1_distractors=["never", "sometimes"],
        game2_kr='"그녀는 친절했기 때문에 항상 좋은 것을 찾았어요."를 영어로 만들어봐!',
        game2_words=["She", "always", "found", "good", "because", "she", "was", "kind"],
        game2_answer="She always found good because she was kind",
        match_pairs=[("kindness", "친절함"), ("nature", "본성"),
                     ("character", "성품"), ("generous", "너그러운")],
        listen_sentence="She always found good because she was kind.",
        listen_emoji_label_ok=("🌸", "친절했기 때문에 좋은 것을 찾았다"),
        listen_distractors=[("😢", "슬퍼서 울었다"), ("😴", "피곤해서 잤다")],
        dict_word="kindness", dict_hint="k _ n d n e s s",
        quiz=[
            ("Q1. 폴리아나가 항상 하는 게임 이름은?",
             "😊 기쁨 게임 (Glad Game)",
             ["🎮 비디오 게임", "🏃 술래잡기"]),
            ("Q2. 폴리아나가 좋은 것을 찾을 수 있는 이유는?",
             "💝 친절한 마음을 가지고 있어서",
             ["💰 돈이 많아서", "📚 책을 많이 읽어서"]),
        ],
        write_q='"She always found good because she was ___."',
        write_answer="kind",
        write_distractors=["mean", "sad"],
        write_prompt="🖊️ I am kind to ______. (영어로 써봐!)",
        complete_emoji="🌸💝😊",
        complete_sub='핵심 표현: <strong>"She always found good because she was kind."</strong> ✅',
        complete_robo="금요일 Day 3에서 완성해요! 💪",
    ),

    # =====================================================================
    # WEEK 12 — Pollyanna
    # =====================================================================
    "week12a.html": dict(
        prev_en=None,
        today_en="Her kindness changed people.",
        today_kr="그녀의 친절함이 사람들을 변화시켰어요.",
        next_en_pill="Her kindness slowly changed everyone around her.",
        robo_msg=(
            "changed는 변화시켰다! 🌸<br>"
            "폴리아나의 친절함이 마을 전체를 바꿨어요!<br>"
            "<b>\"Her kindness changed people.\"</b>"
        ),
        story_robo_kr=(
            "처음에 마을 사람들은 폴리아나가 너무 밝다고 생각했어요. 😅<br>"
            "하지만 그녀의 따뜻한 말과 미소가 사람들의 마음을 움직였어요. 💛<br>"
            "결국 그녀의 친절함이 사람들을 변화시켰어요.<br>"
            "<strong>친절은 사람을 바꾸는 힘이 있어요!</strong>"
        ),
        story_a1_text=(
            "Pollyanna smiled at everyone in town.<br>"
            "She said kind words to sad people. They felt better.<br>"
            "She helped people feel happy again.<br>"
            "<span class=\"hl\">Her kindness changed people.</span>"
        ),
        story_a2_text=(
            "At first, many people in town thought Pollyanna was too cheerful.<br>"
            "But slowly, her warm words and bright smile touched their hearts.<br>"
            "The grumpy old man began to laugh. The lonely woman made new friends.<br>"
            "One by one, the townspeople changed.<br>"
            "<span class=\"hl\">Her kindness changed people in ways nobody expected.</span>"
        ),
        vocab=[("changed", "Kindness changed people."),
               ("positivity", "Her positivity shone."),
               ("contagious", "Smiles are contagious."),
               ("spread", "Her joy spread fast.")],
        game1_q='"Her ___ changed people."',
        game1_answer="kindness", game1_distractors=["anger", "fear"],
        game2_kr='"그녀의 친절함이 사람들을 변화시켰어요."를 영어로 만들어봐!',
        game2_words=["Her", "kindness", "changed", "people"],
        game2_answer="Her kindness changed people",
        match_pairs=[("changed", "변화시켰다"), ("positivity", "긍정"),
                     ("contagious", "전염되는"), ("spread", "퍼졌다")],
        listen_sentence="Her kindness changed people.",
        listen_emoji_label_ok=("🌸", "친절함이 사람들을 변화시켰다"),
        listen_distractors=[("⚡", "충격이 사람들을 놀라게 했다"), ("🌧️", "비가 사람들을 슬프게 했다")],
        dict_word="changed", dict_hint="c h _ n g e d",
        quiz=[
            ("Q1. 폴리아나의 어떤 점이 마을 사람들을 변화시켰나요?",
             "💝 친절함 (kindness)",
             ["💰 돈 (money)", "💪 힘 (power)"]),
            ("Q2. \"changed\"의 뜻은?",
             "🔄 변화시켰다",
             ["📤 보냈다", "📥 받았다"]),
        ],
        write_q='"Her ___ changed people."',
        write_answer="kindness",
        write_distractors=["smile", "voice"],
        write_prompt="🖊️ My ______ can change ______. (영어로 써봐!)",
        complete_emoji="🌸💛✨",
        complete_sub='핵심 표현: <strong>"Her kindness changed people."</strong> ✅',
        complete_robo="수요일 Day 2에서 계속해요! 💪",
    ),

    "week12b.html": dict(
        prev_en="Her kindness changed people.",
        today_en="Her kindness slowly changed everyone around her.",
        today_kr="그녀의 친절함이 주변 모든 사람을 천천히 변화시켰어요.",
        next_en_pill="Her kindness changed everyone she met — positivity is contagious.",
        robo_msg=(
            "slowly는 천천히! 🌸<br>"
            "변화는 항상 조금씩 일어나요!<br>"
            "<b>\"Her kindness slowly changed everyone around her.\"</b>"
        ),
        story_robo_kr=(
            "폴리아나는 그냥 매일 기쁨과 친절함을 나눴어요. ☀️<br>"
            "엄격했던 이모도, 화났던 이웃들도 조금씩 변해갔어요.<br>"
            "<strong>그녀의 친절함이 주변 모든 사람을 천천히 변화시켰어요.</strong>"
        ),
        story_a1_text=(
            "Pollyanna shared kindness every day.<br>"
            "Slowly, the people around her felt happier.<br>"
            "Aunt Polly began to smile. The neighbors became friendly.<br>"
            "<span class=\"hl\">Her kindness slowly changed everyone around her.</span>"
        ),
        story_a2_text=(
            "Pollyanna did not try to change anyone.<br>"
            "She simply shared her joy and kindness every day.<br>"
            "But people could not help but feel different around her.<br>"
            "The strict aunt began to soften. The angry neighbors started to wave.<br>"
            "<span class=\"hl\">Her kindness slowly changed everyone around her, one heart at a time.</span>"
        ),
        vocab=[("changed", "She changed them slowly."),
               ("positivity", "Her positivity helped."),
               ("contagious", "Kindness is contagious."),
               ("spread", "Joy spread to all.")],
        game1_q='"Her kindness ___ changed everyone around her."',
        game1_answer="slowly", game1_distractors=["quickly", "loudly"],
        game2_kr='"그녀의 친절함이 주변 모든 사람을 천천히 변화시켰어요."를 영어로 만들어봐!',
        game2_words=["Her", "kindness", "slowly", "changed", "everyone", "around", "her"],
        game2_answer="Her kindness slowly changed everyone around her",
        match_pairs=[("slowly", "천천히"), ("everyone", "모든 사람"),
                     ("around", "주변"), ("changed", "변화시켰다")],
        listen_sentence="Her kindness slowly changed everyone around her.",
        listen_emoji_label_ok=("🌸", "친절함이 모두를 천천히 변화시켰다"),
        listen_distractors=[("⚡", "갑자기 충격을 줬다"), ("🌪️", "한순간에 휩쓸었다")],
        dict_word="slowly", dict_hint="s l _ w l y",
        quiz=[
            ("Q1. 폴리아나의 친절함은 어떻게 사람들을 변화시켰나요?",
             "🌸 천천히 (slowly)",
             ["⚡ 빠르게 (quickly)", "💥 한꺼번에 (suddenly)"]),
            ("Q2. \"around her\"의 뜻은?",
             "👥 그녀 주변의",
             ["🌍 세계의", "📚 학교의"]),
        ],
        write_q='"Her kindness ___ changed everyone around her."',
        write_answer="slowly",
        write_distractors=["quickly", "never"],
        write_prompt="🖊️ ______ slowly changed ______. (영어로 써봐!)",
        complete_emoji="🌸⏳💛",
        complete_sub='핵심 표현: <strong>"Her kindness slowly changed everyone around her."</strong> ✅',
        complete_robo="금요일 Day 3에서 완성해요! 💪",
    ),

    "week12c.html": dict(
        prev_en="Her kindness slowly changed everyone around her.",
        today_en="Her kindness changed everyone she met — positivity is contagious.",
        today_kr="그녀의 친절함은 그녀가 만난 모든 사람을 변화시켰어요 — 긍정은 전염돼요.",
        next_en_pill="Mary Poppins arrived.",  # W13a
        next_week_label="다음 주(W13) Day 1",
        robo_msg=(
            "contagious는 전염되는! 😊<br>"
            "웃음과 친절함은 옮아가요!<br>"
            "<b>\"Her kindness changed everyone she met — positivity is contagious.\"</b>"
        ),
        story_robo_kr=(
            "폴리아나의 친절함은 햇살처럼 마을 전체에 퍼져나갔어요. ☀️<br>"
            "폴리아나가 다쳐서 걸을 수 없게 되자 마을 전체가 슬퍼했어요.<br>"
            "그들은 자신들이 얼마나 변했는지 깨달았어요.<br>"
            "<strong>긍정적인 마음은 정말로 전염된다는 것을 배웠어요!</strong>"
        ),
        story_a1_text=(
            "Pollyanna gave kindness to all the people she met.<br>"
            "Her smile passed from one heart to another.<br>"
            "Soon the whole town felt warm and happy.<br>"
            "<span class=\"hl\">Her kindness changed everyone she met — positivity is contagious.</span>"
        ),
        story_a2_text=(
            "Pollyanna's kindness spread through the town like sunlight.<br>"
            "She never asked for anything in return. She just gave her warmth freely.<br>"
            "One smile led to another. One kind word opened a closed heart.<br>"
            "When Pollyanna was injured and could not walk, the whole town wept.<br>"
            "<span class=\"hl\">Her kindness changed everyone she met. Positivity is truly contagious.</span>"
        ),
        vocab=[("changed", "She changed them all."),
               ("positivity", "Positivity is power."),
               ("contagious", "Kindness is contagious."),
               ("spread", "Her joy spread far.")],
        game1_q='"Her kindness changed everyone she met — positivity is ___."',
        game1_answer="contagious", game1_distractors=["dangerous", "boring"],
        game2_kr='"긍정은 전염돼요."를 영어로 만들어봐!',
        game2_words=["positivity", "is", "contagious"],
        game2_answer="positivity is contagious",
        match_pairs=[("contagious", "전염되는"), ("positivity", "긍정"),
                     ("changed", "변화시켰다"), ("spread", "퍼졌다")],
        listen_sentence="Her kindness changed everyone she met. Positivity is contagious.",
        listen_emoji_label_ok=("🤗", "친절은 전염된다"),
        listen_distractors=[("⛔", "친절은 위험하다"), ("💤", "친절은 지루하다")],
        dict_word="contagious", dict_hint="c o n t _ g i o u s",
        quiz=[
            ("Q1. \"contagious\"의 뜻은?",
             "🤗 전염되는",
             ["⛔ 위험한", "💤 지루한"]),
            ("Q2. 폴리아나의 친절함은 어떻게 퍼져나갔나요?",
             "💝 사람에서 사람으로 천천히",
             ["📺 TV로", "📨 편지로"]),
        ],
        write_q='"Positivity is ___."',
        write_answer="contagious",
        write_distractors=["selfish", "secret"],
        write_prompt="🖊️ I can spread positivity by ______. (영어로 써봐!)",
        complete_emoji="🤗💛✨",
        complete_sub='핵심 표현: <strong>"Her kindness changed everyone she met — positivity is contagious."</strong> ✅<br>Week 12 완성! ✅',
        complete_robo="다음 주에 새 표현으로 만나요! 💪",
    ),

    # =====================================================================
    # WEEK 22 — Secret Garden
    # =====================================================================
    "week22a.html": dict(
        prev_en=None,
        today_en="She cared for the garden.",
        today_kr="그녀는 정원을 돌봤어요.",
        next_en_pill="She cared for the garden every day.",
        robo_msg=(
            "cared for는 돌봤다! 🌿<br>"
            "메리가 비밀 정원을 가꾸기 시작해요!<br>"
            "<b>\"She cared for the garden.\"</b>"
        ),
        story_robo_kr=(
            "메리 레녹스는 전에는 아무것도 돌본 적이 없었어요. 🌧️<br>"
            "하지만 비밀 정원이 메리를 바꾸었어요. 🌿<br>"
            "매일 아침 메리는 정원에 물을 주고 땅을 파고 식물을 돌봤어요.<br>"
            "<strong>그녀는 정원을 살아있는 친구처럼 돌봤어요!</strong>"
        ),
        story_a1_text=(
            "Mary found a secret garden behind a wall.<br>"
            "It was old and quiet.<br>"
            "Mary went there every day. She pulled weeds and planted seeds.<br>"
            "<span class=\"hl\">She cared for the garden.</span>"
        ),
        story_a2_text=(
            "Mary Lennox had never cared for anything before.<br>"
            "But the secret garden changed her.<br>"
            "She found the hidden door and stepped inside.<br>"
            "The garden was old and full of dead branches, but Mary saw hope in it.<br>"
            "<span class=\"hl\">She cared for the garden as if it were a living friend.</span>"
        ),
        vocab=[("cared", "She cared for it."),
               ("joy", "Joy filled her heart."),
               ("purpose", "She had a purpose."),
               ("routine", "It became her routine.")],
        game1_q='"She cared for the ___."',
        game1_answer="garden", game1_distractors=["castle", "river"],
        game2_kr='"그녀는 정원을 돌봤어요."를 영어로 만들어봐!',
        game2_words=["She", "cared", "for", "the", "garden"],
        game2_answer="She cared for the garden",
        match_pairs=[("cared", "돌봤다"), ("joy", "기쁨"),
                     ("purpose", "목적"), ("routine", "일과")],
        listen_sentence="She cared for the garden.",
        listen_emoji_label_ok=("🌿", "정원을 돌봤다"),
        listen_distractors=[("🏰", "성을 지었다"), ("📚", "책을 읽었다")],
        dict_word="cared", dict_hint="c _ r e d",
        quiz=[
            ("Q1. 메리가 발견한 것은 무엇인가요?",
             "🌿 비밀 정원 (secret garden)",
             ["🏰 비밀 성", "📚 비밀 도서관"]),
            ("Q2. 메리가 정원에서 한 일은?",
             "💧 물 주기, 잡초 제거, 씨앗 심기",
             ["🍳 요리하기", "📺 TV 보기"]),
        ],
        write_q='"She cared for the ___."',
        write_answer="garden",
        write_distractors=["mountain", "city"],
        write_prompt="🖊️ I care for ______ every day. (영어로 써봐!)",
        complete_emoji="🌿🌷💚",
        complete_sub='핵심 표현: <strong>"She cared for the garden."</strong> ✅',
        complete_robo="수요일 Day 2에서 계속해요! 💪",
    ),

    "week22c.html": dict(
        prev_en="She cared for the garden every day.",
        today_en="She cared for it every day because it gave her joy.",
        today_kr="그녀는 정원이 기쁨을 주었기 때문에 매일 돌봤어요.",
        next_en_pill="Colin was afraid to go outside.",  # W23a
        next_week_label="다음 주(W23) Day 1",
        robo_msg=(
            "because는 왜냐하면! 🌷<br>"
            "메리가 정원을 돌보는 이유를 because로 말해봐요!<br>"
            "<b>\"She cared for it every day because it gave her joy.\"</b>"
        ),
        story_robo_kr=(
            "매일 아침 메리는 일찍 일어나 비밀 정원으로 달려갔어요. 🌅<br>"
            "아무도 시키지 않았지만 정원이 메리를 끌어당겼어요.<br>"
            "새 꽃봉오리가 보일 때 메리의 마음이 기뻐서 뛰었어요. 💚<br>"
            "<strong>그녀는 정원이 기쁨을 주었기 때문에 매일 돌봤어요!</strong>"
        ),
        story_a1_text=(
            "Mary went to the garden every morning.<br>"
            "She pulled weeds and watered the flowers.<br>"
            "The garden made her smile.<br>"
            "<span class=\"hl\">She cared for it every day because it gave her joy.</span>"
        ),
        story_a2_text=(
            "Every morning, Mary woke up early and ran to the secret garden.<br>"
            "She didn't have to — nobody told her to go.<br>"
            "But something pulled her there. The garden made her feel alive.<br>"
            "When she saw a new bud appear, her heart leapt with happiness.<br>"
            "<span class=\"hl\">She cared for it every day because it gave her joy.</span>"
        ),
        vocab=[("cared", "She cared for it daily."),
               ("joy", "Joy filled her days."),
               ("purpose", "Her purpose was clear."),
               ("routine", "Caring became routine.")],
        game1_q='"She cared for it every day ___ it gave her joy."',
        game1_answer="because", game1_distractors=["but", "or"],
        game2_kr='"그녀는 정원이 기쁨을 주었기 때문에 매일 돌봤어요."를 영어로 만들어봐!',
        game2_words=["She", "cared", "for", "it", "every", "day", "because", "it", "gave", "her", "joy"],
        game2_answer="She cared for it every day because it gave her joy",
        match_pairs=[("because", "왜냐하면"), ("joy", "기쁨"),
                     ("cared", "돌봤다"), ("routine", "일과")],
        listen_sentence="She cared for it every day because it gave her joy.",
        listen_emoji_label_ok=("🌷", "기쁨을 주어서 매일 돌봤다"),
        listen_distractors=[("💰", "돈을 받아서 돌봤다"), ("👻", "무서워서 돌봤다")],
        dict_word="because", dict_hint="b _ c a u s e",
        quiz=[
            ("Q1. 메리가 매일 정원을 돌보는 이유는?",
             "💚 기쁨을 주어서 (because it gave her joy)",
             ["💰 돈을 받아서", "📚 숙제라서"]),
            ("Q2. because 뒤에 오는 것은?",
             "💡 이유 (reason)",
             ["⏰ 시간 (time)", "📍 장소 (place)"]),
        ],
        write_q='"She cared for it every day ___ it gave her joy."',
        write_answer="because",
        write_distractors=["but", "and"],
        write_prompt="🖊️ I do ______ every day because it gives me ______. (영어로 써봐!)",
        complete_emoji="🌷💚🌱",
        complete_sub='핵심 표현: <strong>"She cared for it every day because it gave her joy."</strong> ✅<br>Week 22 완성! ✅',
        complete_robo="다음 주에 콜린의 이야기를 만나요! 💪",
    ),
}


# =========================================================================
# Generic builders for full HTML blocks (sections 1-9)
# =========================================================================

def build_day_pills_block(s: dict, day: int) -> str:
    """day = 1, 2, or 3 (this file's day)"""
    today = s["today_en"]; nxt = s["next_en_pill"]
    if day == 1:
        return (
            f'<span class="day-pill today">● Day 1 (월) "{today}"</span>\n'
            f'      <span class="day-pill future">○ Day 2 (수) "{nxt}"</span>\n'
            f'      <span class="day-pill future">○ Day 3 (금) 완성!</span>'
        )
    if day == 2:
        prev = s["prev_en"]
        return (
            f'<span class="day-pill done">● Day 1 (월) "{prev}"</span>\n'
            f'      <span class="day-pill today">● Day 2 (수) "{today}"</span>\n'
            f'      <span class="day-pill future">○ Day 3 (금) 완성!</span>'
        )
    if day == 3:
        prev = s["prev_en"]
        return (
            f'<span class="day-pill done">● Day 1 (월) "처음 표현"</span>\n'
            f'      <span class="day-pill done">● Day 2 (수) "{prev}"</span>\n'
            f'      <span class="day-pill today">● Day 3 (금) 완성!</span>'
        )
    return ""


def build_vocab_grid(s: dict) -> str:
    cards = "".join(vocab_card_html(w, ex) for w, ex in s["vocab"])
    return f'<div class="vocab-grid">{cards}</div>'


def build_game1(s: dict) -> str:
    """Word pick — fill blank."""
    answer = s["game1_answer"]
    choices = [answer] + s["game1_distractors"]
    btns = "".join(
        f'<button class="ch" onclick="pick(this,\'{c}\',\'{answer}\',\'b1\',\'f1\')">{c}</button>'
        for c in choices
    )
    blank_html = '<span class="blank" id="b1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'
    q_html = s["game1_q"].replace("___", blank_html)
    return (
        '<div class="game-box">\n'
        '    <div class="game-q">빈칸에 알맞은 단어를 골라봐!</div>\n'
        f'    <div style="text-align:center;font-size:1.2rem;font-weight:900;margin-bottom:14px;line-height:2;">{q_html}</div>\n'
        f'    <div class="choices">\n'
        f'      {btns}\n'
        '    </div>\n'
        '    <div class="fb" id="f1"></div>\n'
        '  </div>'
    )


def build_game2(s: dict) -> str:
    """Sentence build."""
    answer = s["game2_answer"]
    chips = "".join(
        f'<button class="wchip" onclick="woAdd(\'wo1\',this,\'{w}\')">{w}</button>'
        for w in s["game2_words"]
    )
    return (
        '<div class="game-box" style="background:linear-gradient(135deg,#fdf6e3,#fdf8f0);">\n'
        f'    <div class="game-q">{s["game2_kr"]}</div>\n'
        '    <div class="build-zone" id="wo1-zone"><span class="build-ph" id="wo1-ph">👆 아래 단어를 눌러봐!</span></div>\n'
        f'    <div class="wpool" id="wo1-pool">{chips}</div>\n'
        '    <div class="game-btns">\n'
        f'      <button class="btn-ok" onclick="woChk(\'wo1\',\'{answer}\',\'wo1-fb\')">✓ 확인!</button>\n'
        '      <button class="btn-rst" onclick="woRst(\'wo1\')">↩ 다시</button>\n'
        '    </div>\n'
        '    <div class="fb" id="wo1-fb"></div>\n'
        '  </div>'
    )


def build_match(s: dict) -> str:
    """Matching game — 4 pairs."""
    pairs = s["match_pairs"]
    left = "".join(f'<button class="m-btn" onclick="mClick(this,\'{en}\')">{en}</button>' for en, _ in pairs)
    # right column: 4 Korean meanings, scrambled (rotate by 1 for variety)
    rt_pairs = pairs[1:] + pairs[:1]
    right = "".join(f'<button class="m-btn" onclick="mClick(this,\'{en}\')">{kr}</button>' for en, kr in rt_pairs)
    return (
        '<div class="game-box">\n'
        '    <div style="text-align:center;font-size:0.85rem;font-weight:700;margin-bottom:12px;">👆 왼쪽 → 오른쪽 뜻!</div>\n'
        '    <div class="match-grid">\n'
        f'      <div class="match-col" id="ml">{left}</div>\n'
        f'      <div class="match-col" id="mr">{right}</div>\n'
        '    </div>\n'
        '    <div class="fb" id="mfb"></div>\n'
        '  </div>'
    )


def build_listen(s: dict) -> str:
    sent = s["listen_sentence"]
    ok_em, ok_lab = s["listen_emoji_label_ok"]
    ds = s["listen_distractors"]
    opts = (
        f'<button class="listen-opt" onclick="listenChk(this,\'ok\')">\n'
        f'      <div class="lo-emoji">{ok_em}</div>\n'
        f'      <div class="lo-label">{ok_lab}</div>\n'
        f'    </button>\n'
        + "\n".join(
            f'    <button class="listen-opt" onclick="listenChk(this,\'no\')">\n'
            f'      <div class="lo-emoji">{em}</div>\n'
            f'      <div class="lo-label">{lab}</div>\n'
            f'    </button>'
            for em, lab in ds
        )
    )
    return (
        f'<button class="listen-play" onclick="speak(\'{sent}\')">🔊 듣기!</button>\n'
        f'  <div class="listen-opts">\n'
        f'    {opts}\n'
        f'  </div>\n'
        f'  <div class="fb" id="listen-fb" style="margin-top:10px;"></div>'
    )


def build_dict(s: dict) -> str:
    w = s["dict_word"]; hint = s["dict_hint"]
    return (
        f'<button class="dict-play" onclick="speak(\'{w}\')">🔊 단어 듣기</button>\n'
        f'  <div class="dict-hint">{hint}</div>\n'
        f'  <input class="dict-input" id="dictIn" placeholder="단어를 써봐!" onkeydown="if(event.key===\'Enter\')chkDict(\'{w}\')">\n'
        f'  <button class="dict-check" onclick="chkDict(\'{w}\')">✓ 확인</button>\n'
        f'  <div class="fb" id="dict-fb" style="margin-top:10px;"></div>'
    )


def build_quiz(s: dict) -> str:
    blocks = []
    for q, ok, distractors in s["quiz"]:
        opts = (
            f'<button class="qo" onclick="qChk(this,\'ok\')">{ok}</button>'
            + "".join(f'<button class="qo" onclick="qChk(this,\'no\')">{d}</button>' for d in distractors)
        )
        blocks.append(
            f'<div class="quiz-box">\n'
            f'    <div class="quiz-q">{q}</div>\n'
            f'    <div class="quiz-opts">{opts}</div>\n'
            f'  </div>'
        )
    return "\n  ".join(blocks)


def build_write(s: dict) -> str:
    answer = s["write_answer"]
    choices = [answer] + s["write_distractors"]
    btns = "".join(
        f'<button class="ch" onclick="pick(this,\'{c}\',\'{answer}\',\'bw\',\'fw\')">{c}</button>'
        for c in choices
    )
    return (
        '<div class="game-box">\n'
        '    <div class="game-q">📝 빈칸에 알맞은 말을 골라봐!</div>\n'
        f'    <div style="text-align:center;font-size:1.1rem;font-weight:900;margin-bottom:12px;line-height:2;">{s["write_q"]}</div>\n'
        f'    <div class="choices">{btns}</div>\n'
        '    <div class="fb" id="fw"></div>\n'
        '  </div>\n'
        '  <div class="write-box">\n'
        f'    <div style="font-size:0.82rem;color:var(--text3);margin-bottom:8px;">{s["write_prompt"]}</div>\n'
        '    <input class="write-input" id="wInput" placeholder="영어로 써봐!">\n'
        '    <button class="write-btn" onclick="chkWrite()">✓ 제출!</button>\n'
        '    <div class="fb" id="wfb" style="margin-top:8px;"></div>\n'
        '  </div>'
    )


def build_complete(s: dict, day: int, file_stem: str) -> str:
    em = s["complete_emoji"]
    sub = s["complete_sub"]
    robo = s["complete_robo"]
    next_en = s["next_en_pill"]
    # Determine next href
    if day == 3:
        # next-week first day — guess by file_stem week+1 a
        m = re.match(r"week(\d{2})c", file_stem)
        if m:
            nxt_week = int(m.group(1)) + 1
            nxt_href = f"week{nxt_week:02d}a.html"
            nxt_label = f"W{nxt_week} Day 1 →"
            label_text = "📅 다음 주 첫 수업"
        else:
            nxt_href = "../index.html"; nxt_label = "Camp A"; label_text = "📅 다음"
    else:
        m = re.match(r"week(\d{2})([abc])", file_stem)
        if m:
            wk = m.group(1); next_letter = chr(ord(m.group(2)) + 1)
            nxt_href = f"week{wk}{next_letter}.html"
            nxt_label = f"Day {day+1} →"
            label_text = "📅 다음 수업"
        else:
            nxt_href = "../index.html"; nxt_label = "Camp A"; label_text = "📅 다음"
    day_dots = ['●○○', '●●○', '●●●'][day-1]
    return (
        f'<div class="complete-emoji">{em}</div>\n'
        f'  <div class="complete-title">Day {day} 완료! {day_dots}</div>\n'
        f'  <div class="complete-sub">{sub}</div>\n'
        f'  <div class="xp-big">🏆 총 <span id="fxp">0</span> XP!</div>\n'
        f'  <div class="robo" style="text-align:left;">\n'
        f'    <div class="robo-av"><img src="https://pub-a418b5aad0bd4c3fb41cf7159403fc12.r2.dev/images/robo/robo.webp" alt="Robo"></div>\n'
        f'    <div><div class="robo-nm">Robo</div><div class="robo-msg">{robo}</div></div>\n'
        f'  </div>\n'
        f'  <div style="margin-top:14px;"><div class="next-card">\n'
        f'    <div style="flex:1;">\n'
        f'      <div class="next-label">{label_text}</div>\n'
        f'      <div class="next-title">Day {day+1 if day<3 else 1} — "{next_en}"</div>\n'
        f'    </div>\n'
        f'    <a href="{nxt_href}" class="next-btn">{nxt_label}</a>\n'
        f'  </div></div>'
    )


# =========================================================================
# Main loop — apply replacements to each file
# =========================================================================

def fix_file(path: Path, s: dict) -> dict:
    text = path.read_text(encoding="utf-8")
    log = {"file": path.name, "applied": [], "missed": []}

    fname = path.stem  # "week05a", etc.
    m = re.match(r"week\d{2}([abc])", fname)
    day = "abc".index(m.group(1)) + 1 if m else 1

    # ---- 1) Day pills (replace entire <div class="day-badge"> inner) ----
    new_pills = build_day_pills_block(s, day)
    new_text, ok = replace_block(
        text,
        '<div class="day-badge">',
        '</div>\n    </div>\n  </div>\n</div></div>',  # closing of hero-overlay+wrap
        f'<div class="day-badge">\n      {new_pills}\n    </div>\n    </div>\n  </div>\n</div></div>',
    )
    if ok:
        text = new_text; log["applied"].append("day-pills")
    else:
        # try simpler anchor
        m_pills = re.search(r'<div class="day-badge">.*?</div>', text, re.S)
        if m_pills:
            text = text[:m_pills.start()] + f'<div class="day-badge">\n      {new_pills}\n    </div>' + text[m_pills.end():]
            log["applied"].append("day-pills(re)")
        else:
            log["missed"].append("day-pills")

    # ---- 2) Robo welcome msg (first <div class="robo-msg">…</div>) ----
    rm = re.search(r'<div class="robo-msg">.*?</div>', text, re.S)
    if rm:
        text = text[:rm.start()] + f'<div class="robo-msg">{s["robo_msg"]}</div>' + text[rm.end():]
        log["applied"].append("robo-msg")
    else:
        log["missed"].append("robo-msg")

    # ---- 3) key-eng / key-kr ----
    new_text, ok = re.subn(r'<div class="key-eng">.*?</div>',
                           f'<div class="key-eng">&quot;{s["today_en"]}&quot;</div>',
                           text, count=1)
    if ok: text = new_text; log["applied"].append("key-eng")
    new_text, ok = re.subn(r'<div class="key-kr">.*?</div>',
                           f'<div class="key-kr">{s["today_kr"]}</div>',
                           text, count=1)
    if ok: text = new_text; log["applied"].append("key-kr")

    # ---- 3b) key-play-row + play-btn speak() ----
    text = re.sub(r'speak\(\'[^\']*\'\)', lambda m: m.group(0), text, count=0)  # noop placeholder
    text = re.sub(r'<div class="key-play-row" onclick="speak\(\'[^\']*\'\)">',
                  f'<div class="key-play-row" onclick="speak(\'{s["today_en"]}\')">', text)
    text = re.sub(r'<button class="play-btn" onclick="event\.stopPropagation\(\);speak\(\'[^\']*\'\)">',
                  f'<button class="play-btn" onclick="event.stopPropagation();speak(\'{s["today_en"]}\')">', text)

    # ---- 4) Korean intro (story robo-msg = 2nd robo-msg) ----
    rms = list(re.finditer(r'<div class="robo-msg">(.*?)</div>', text, re.S))
    if len(rms) >= 2:
        m_intro = rms[1]
        text = text[:m_intro.start()] + f'<div class="robo-msg">{s["story_robo_kr"]}</div>' + text[m_intro.end():]
        log["applied"].append("intro-kr")
    else:
        log["missed"].append("intro-kr")

    # ---- 5) A1 + A2 story-en-text (in order) ----
    sets = list(re.finditer(r'<div class="story-en-text">(.*?)</div>', text, re.S))
    if len(sets) >= 2:
        text = (text[:sets[1].start()] +
                f'<div class="story-en-text">{s["story_a2_text"]}</div>' +
                text[sets[1].end():])
        # re-find for a1 (now indices shifted)
        sets = list(re.finditer(r'<div class="story-en-text">(.*?)</div>', text, re.S))
        text = (text[:sets[0].start()] +
                f'<div class="story-en-text">{s["story_a1_text"]}</div>' +
                text[sets[0].end():])
        log["applied"].append("story-a1+a2")
    elif len(sets) == 1:
        text = text[:sets[0].start()] + f'<div class="story-en-text">{s["story_a1_text"]}</div>' + text[sets[0].end():]
        log["applied"].append("story-a1-only")
    else:
        log["missed"].append("story-en-text")

    # ---- 6) Vocab grid ----
    vg = re.search(r'<div class="vocab-grid">.*?</div>\s*\n\s*</div><div class="prog">', text, re.S)
    if vg:
        # Find just the vocab-grid block precisely
        start = vg.start()
        # Find matching closing </div> (the card body close happens after vocab-grid)
        v_close = re.search(r'</div>\s*\n?\s*</div><div class="prog">', text[start:])
        if v_close:
            # Replace just the vocab-grid block
            vg_match = re.search(r'<div class="vocab-grid">.*?</div>', text[start:start+v_close.end()], re.S)
            # Use simple regex first/lazy
            new_text, ok = re.subn(r'<div class="vocab-grid">.*?</div>(?=\s*\n?\s*</div><div class="prog">)',
                                    build_vocab_grid(s),
                                    text, count=1, flags=re.S)
            if ok:
                text = new_text; log["applied"].append("vocab")
            else:
                log["missed"].append("vocab")
        else:
            log["missed"].append("vocab-close")
    else:
        log["missed"].append("vocab")

    # ---- 7) Game 1 (game-box inside Section 4) ----
    g1_pat = re.compile(r'(<div class="card"><div class="sec-hdr"><div class="sec-num"[^>]*>4</div>.*?<div class="sec-body">\s*)<div class="game-box">.*?</div>\s*</div>\s*<div class="prog">', re.S)
    new_text, ok = g1_pat.subn(lambda m: f'{m.group(1)}{build_game1(s)}\n</div><div class="prog">', text, count=1)
    if ok: text = new_text; log["applied"].append("game1")
    else: log["missed"].append("game1")

    # ---- 8) Game 2 (Section 5) ----
    g2_pat = re.compile(r'(<div class="card"><div class="sec-hdr"><div class="sec-num"[^>]*>5</div>.*?<div class="sec-body">\s*)<div class="game-box"[^>]*>.*?</div>\s*</div>\s*<div class="prog">', re.S)
    new_text, ok = g2_pat.subn(lambda m: f'{m.group(1)}{build_game2(s)}\n</div><div class="prog">', text, count=1)
    if ok: text = new_text; log["applied"].append("game2")
    else: log["missed"].append("game2")

    # ---- 9) Match (Section 6) ----
    m_pat = re.compile(r'(<div class="card"><div class="sec-hdr"><div class="sec-num"[^>]*>6</div>.*?<div class="sec-body">\s*)<div class="game-box">.*?</div>\s*</div>\s*<div class="prog">', re.S)
    new_text, ok = m_pat.subn(lambda m: f'{m.group(1)}{build_match(s)}\n</div><div class="prog">', text, count=1)
    if ok: text = new_text; log["applied"].append("match")
    else: log["missed"].append("match")

    # ---- 10) Listening (♪ section) ----
    l_pat = re.compile(r'(<div class="card"><div class="sec-hdr"><div class="sec-num"[^>]*>♪</div>.*?<div class="sec-body">\s*)<button class="listen-play".*?<div class="fb" id="listen-fb"[^>]*></div>', re.S)
    new_text, ok = l_pat.subn(lambda m: f'{m.group(1)}{build_listen(s)}', text, count=1)
    if ok: text = new_text; log["applied"].append("listen")
    else: log["missed"].append("listen")

    # ---- 11) Dictation (✎ section) ----
    d_pat = re.compile(r'(<div class="card"><div class="sec-hdr"><div class="sec-num"[^>]*>✎</div>.*?<div class="sec-body">\s*)<button class="dict-play".*?<div class="fb" id="dict-fb"[^>]*></div>', re.S)
    new_text, ok = d_pat.subn(lambda m: f'{m.group(1)}{build_dict(s)}', text, count=1)
    if ok: text = new_text; log["applied"].append("dict")
    else: log["missed"].append("dict")

    # ---- 12) Quiz (Section 7) ----
    q_pat = re.compile(r'(<div class="card"><div class="sec-hdr"><div class="sec-num"[^>]*>7</div>.*?<div class="sec-body">\s*)(<div class="quiz-box">.*?</div>\s*){1,3}\s*</div>\s*<div class="prog">', re.S)
    new_text, ok = q_pat.subn(lambda m: f'{m.group(1)}{build_quiz(s)}\n</div><div class="prog">', text, count=1)
    if ok: text = new_text; log["applied"].append("quiz")
    else: log["missed"].append("quiz")

    # ---- 13) Writing (Section 8) ----
    w_pat = re.compile(r'(<div class="card"><div class="sec-hdr"><div class="sec-num"[^>]*>8</div>.*?<div class="sec-body">\s*)<div class="game-box">.*?</div>\s*<div class="write-box">.*?</div>\s*</div>\s*<div class="prog">', re.S)
    new_text, ok = w_pat.subn(lambda m: f'{m.group(1)}{build_write(s)}\n</div><div class="prog">', text, count=1)
    if ok: text = new_text; log["applied"].append("write")
    else: log["missed"].append("write")

    # ---- 14) Completion card (<div class="complete" …>) — ends just before </main> ----
    c_pat = re.compile(r'<div class="complete" id="done-card">.*?</div>\s*\n\s*</main>', re.S)
    new_text, ok = c_pat.subn(
        f'<div class="complete" id="done-card">\n  {build_complete(s, day, fname)}\n</div>\n\n</main>',
        text, count=1
    )
    if ok: text = new_text; log["applied"].append("complete")
    else: log["missed"].append("complete")

    # ---- 15) Bottom navigation next-link ----
    if day < 3:
        m_bnav = re.search(r'<a class="bn" href="week\d{2}[abc]\.html">[^<]*</a>', text)
        if m_bnav:
            wk = re.match(r"week(\d{2})", fname).group(1)
            next_letter = "abc"["abc".index(m.group(1)) + 1] if 'abc'.index(m.group(1)) < 2 else 'c'
            # Recompute: we know day, next file = week{wk}{abc[day]}
            next_letter = "abc"[day]  # 0->a (day=1->b is index 1)
            new_link = f'<a class="bn" href="week{wk}{next_letter}.html">Day {day+1} →</a>'
            text = text[:m_bnav.start()] + new_link + text[m_bnav.end():]
            log["applied"].append("bnav")

    path.write_text(text, encoding="utf-8")
    return log


def main():
    for fname in sorted(SPEC):
        path = ROOT / fname
        if not path.exists():
            print(f"MISSING {fname}"); continue
        log = fix_file(path, SPEC[fname])
        applied = ", ".join(log["applied"])
        missed = ", ".join(log["missed"])
        flag = "✓" if not log["missed"] else "⚠️"
        print(f"{flag} {fname}: applied=[{applied}]  missed=[{missed}]")


if __name__ == "__main__":
    main()

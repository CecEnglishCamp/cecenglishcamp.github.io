#!/usr/bin/env python3
"""Fix G4 Mary Poppins W13-W16: enrich stories + fix v-play buttons."""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
R2 = "https://pub-a418b5aad0bd4c3fb41cf7159403fc12.r2.dev"

# ─── ENRICHED CONTENT per week/day ────────────────────────────
# Each entry: story_kr (8-10 lines), story_en (7-8 lines), story_play_text
DATA = {
    # ══════════ W13: Mary Poppins arrived ══════════
    "week13a": {
        "story_kr": (
            "오늘부터 메리 포핀스를 공부해요! ☂️<br>"
            "이 이야기는 영국 작가 P.L. 트래버스가 쓴 동화예요.<br>"
            "뱅크스 가족에게는 네 명의 아이들이 있어요!<br><br>"
            "런던 벚꽃길 17번지에 뱅크스 가족이 살았어요.<br>"
            "아이들은 말썽꾸러기였어요. 유모가 자꾸 바뀌었거든요!<br>"
            "어느 바람 부는 날, 하늘에서 우산을 든 여자가 내려왔어요.<br>"
            "\"저는 메리 포핀스예요.\" 아이들은 깜짝 놀랐어요!<br>"
            "<strong>메리 포핀스가 도착했어요.</strong>"
        ),
        "story_en": (
            "Today we start Mary Poppins! ☂️<br>"
            "This story was written by P.L. Travers from England.<br>"
            "The Banks family has four children!<br><br>"
            "The Banks family lived at 17 Cherry Tree Lane in London.<br>"
            "The children were naughty. Their nannies kept leaving!<br>"
            "On a windy day, a woman with an umbrella came down from the sky.<br>"
            "\"I am Mary Poppins.\" The children were amazed!<br>"
            "<span class=\"hl\">Mary Poppins arrived.</span>"
        ),
        "story_play": "Today we start Mary Poppins! This story was written by P.L. Travers from England. The Banks family has four children! The Banks family lived at 17 Cherry Tree Lane in London. The children were naughty. Their nannies kept leaving! On a windy day, a woman with an umbrella came down from the sky. I am Mary Poppins. The children were amazed! Mary Poppins arrived."
    },
    "week13b": {
        "story_kr": (
            "메리 포핀스는 보통 유모가 아니었어요! ☂️<br>"
            "가방에서 끝없이 물건이 나왔어요.<br>"
            "거울, 모자, 약병, 심지어 세면대까지!<br><br>"
            "뱅크스 가족의 아이들은 유모가 필요했어요.<br>"
            "엄마 아빠는 바빴고, 아이들은 돌봐줄 사람이 없었거든요.<br>"
            "그래서 메리 포핀스가 온 거예요!<br>"
            "아이들에게 도움이 필요해서 도착한 거예요.<br>"
            "<strong>아이들이 도움이 필요해서 메리 포핀스가 도착했어요.</strong>"
        ),
        "story_en": (
            "Mary Poppins was no ordinary nanny! ☂️<br>"
            "Things kept coming out of her bag endlessly.<br>"
            "A mirror, a hat, medicine, even a washstand!<br><br>"
            "The Banks children needed a nanny.<br>"
            "Mum and Dad were busy, and no one looked after the children.<br>"
            "That is why Mary Poppins came!<br>"
            "She arrived because the children needed help.<br>"
            "<span class=\"hl\">Mary Poppins arrived because the children needed help.</span>"
        ),
        "story_play": "Mary Poppins was no ordinary nanny! Things kept coming out of her bag endlessly. A mirror, a hat, medicine, even a washstand! The Banks children needed a nanny. Mum and Dad were busy, and no one looked after the children. That is why Mary Poppins came! She arrived because the children needed help. Mary Poppins arrived because the children needed help."
    },
    "week13c": {
        "story_kr": (
            "Week 13 마지막 수업이에요! 완성 문장을 배워봐요! 🎉<br>"
            "뱅크스 가족의 아이들은 평범한 유모가 아니라<br>"
            "정말 특별한 사람이 필요했어요.<br><br>"
            "보통 유모들은 오래 버티지 못했어요.<br>"
            "아이들이 너무 말썽꾸러기였거든요!<br>"
            "하지만 메리 포핀스는 달랐어요. 마법 같은 사람이었어요!<br>"
            "아이들은 처음으로 유모를 좋아하게 되었어요.<br>"
            "진짜 마법 같은 사람이 필요했기에 메리 포핀스가 온 거예요!<br>"
            "<strong>아이들에게 정말 마법 같은 사람이 필요했기에 메리 포핀스가 도착했어요.</strong>"
        ),
        "story_en": (
            "This is the final lesson of Week 13! Let's learn the complete sentence! 🎉<br>"
            "The Banks children did not need an ordinary nanny.<br>"
            "They needed someone truly special.<br><br>"
            "Normal nannies could not last long.<br>"
            "The children were too naughty!<br>"
            "But Mary Poppins was different. She was like magic!<br>"
            "For the first time, the children liked their nanny.<br>"
            "They needed someone truly magical — that is why Mary Poppins came!<br>"
            "<span class=\"hl\">Mary Poppins arrived because the children needed someone truly magical.</span>"
        ),
        "story_play": "This is the final lesson of Week 13! Let us learn the complete sentence! The Banks children did not need an ordinary nanny. They needed someone truly special. Normal nannies could not last long. The children were too naughty! But Mary Poppins was different. She was like magic! For the first time, the children liked their nanny. They needed someone truly magical. That is why Mary Poppins came! Mary Poppins arrived because the children needed someone truly magical."
    },
    # ══════════ W14: She was strict but kind ══════════
    "week14a": {
        "story_kr": (
            "메리 포핀스와의 첫 날이에요! 📏<br>"
            "메리 포핀스는 아침부터 규칙을 정했어요.<br>"
            "\"방을 정리해! 옷을 깨끗이 입어!\"<br><br>"
            "아이들은 처음에 깜짝 놀랐어요.<br>"
            "이전 유모들은 이렇게 엄격하지 않았거든요!<br>"
            "하지만 메리 포핀스는 혼내기만 한 게 아니었어요.<br>"
            "자기 전에 노래를 불러주고, 따뜻하게 이불을 덮어줬어요.<br>"
            "<strong>그녀는 엄격하지만 다정했어요.</strong>"
        ),
        "story_en": (
            "It is the first day with Mary Poppins! 📏<br>"
            "Mary Poppins set rules from the morning.<br>"
            "\"Tidy your room! Wear clean clothes!\"<br><br>"
            "The children were surprised at first.<br>"
            "The other nannies were never this strict!<br>"
            "But Mary Poppins did not only scold.<br>"
            "She sang songs at bedtime and tucked them in warmly.<br>"
            "<span class=\"hl\">She was strict but kind.</span>"
        ),
        "story_play": "It is the first day with Mary Poppins! Mary Poppins set rules from the morning. Tidy your room! Wear clean clothes! The children were surprised at first. The other nannies were never this strict! But Mary Poppins did not only scold. She sang songs at bedtime and tucked them in warmly. She was strict but kind."
    },
    "week14b": {
        "story_kr": (
            "왜 메리 포핀스는 엄격했을까요? 🤔<br>"
            "메리 포핀스에게는 이유가 있었어요.<br>"
            "아이들을 정말 사랑했거든요!<br><br>"
            "사랑하니까 규칙을 만든 거예요.<br>"
            "안전하게 지키고 싶었고, 바르게 자라길 원했어요.<br>"
            "Jane이 넘어졌을 때 달려와서 안아줬어요.<br>"
            "Michael이 울 때 조용히 옆에 앉아줬어요.<br>"
            "관심이 있었기에 엄격하지만 다정할 수 있었어요.<br>"
            "<strong>그녀는 관심이 있었기에 엄격하지만 다정했어요.</strong>"
        ),
        "story_en": (
            "Why was Mary Poppins so strict? 🤔<br>"
            "Mary Poppins had a reason.<br>"
            "She truly loved the children!<br><br>"
            "Because she loved them, she made rules.<br>"
            "She wanted to keep them safe and help them grow well.<br>"
            "When Jane fell down, Mary ran to hug her.<br>"
            "When Michael cried, she sat quietly beside him.<br>"
            "Because she cared, she could be strict but kind.<br>"
            "<span class=\"hl\">She was strict but kind because she cared.</span>"
        ),
        "story_play": "Why was Mary Poppins so strict? Mary Poppins had a reason. She truly loved the children! Because she loved them, she made rules. She wanted to keep them safe and help them grow well. When Jane fell down, Mary ran to hug her. When Michael cried, she sat quietly beside him. Because she cared, she could be strict but kind. She was strict but kind because she cared."
    },
    "week14c": {
        "story_kr": (
            "Week 14 완성! 메리 포핀스가 가르쳐준 것은? 🌟<br>"
            "아이들은 드디어 깨달았어요.<br>"
            "규칙이 있다고 사랑이 없는 게 아니에요!<br><br>"
            "메리 포핀스의 규칙 덕분에 방은 깨끗해졌어요.<br>"
            "시간 약속도 잘 지키게 되었어요.<br>"
            "동시에 메리 포핀스는 매일 밤 이야기를 해줬어요.<br>"
            "엄격함 속에 따뜻한 사랑이 있었어요.<br>"
            "규칙과 사랑은 함께할 수 있다는 걸 배웠어요!<br>"
            "<strong>규칙과 사랑은 함께할 수 있기에 그녀는 엄격하지만 다정했어요.</strong>"
        ),
        "story_en": (
            "Week 14 complete! What did Mary Poppins teach? 🌟<br>"
            "The children finally understood.<br>"
            "Having rules does not mean there is no love!<br><br>"
            "Thanks to Mary Poppins's rules, the room was always tidy.<br>"
            "They learned to be on time.<br>"
            "At the same time, Mary told them stories every night.<br>"
            "There was warm love inside her strictness.<br>"
            "They learned that rules and love can exist together!<br>"
            "<span class=\"hl\">She was strict but kind because rules and love can exist together.</span>"
        ),
        "story_play": "Week 14 complete! What did Mary Poppins teach? The children finally understood. Having rules does not mean there is no love! Thanks to Mary Poppins rules, the room was always tidy. They learned to be on time. At the same time, Mary told them stories every night. There was warm love inside her strictness. They learned that rules and love can exist together! She was strict but kind because rules and love can exist together."
    },
    # ══════════ W15: The children felt joy ══════════
    "week15a": {
        "story_kr": (
            "메리 포핀스와 함께한 마법의 순간들! ✨<br>"
            "어느 날 메리 포핀스가 말했어요.<br>"
            "\"오늘은 특별한 소풍을 갈 거야!\"<br><br>"
            "아이들은 메리 포핀스를 따라갔어요.<br>"
            "갑자기 천장까지 둥둥 떠올랐어요!<br>"
            "\"와! 우리가 날고 있어!\" Jane이 소리쳤어요.<br>"
            "Michael은 웃음이 멈추지 않았어요.<br>"
            "이렇게 행복한 건 처음이었어요.<br>"
            "<strong>아이들은 기쁨을 느꼈어요.</strong>"
        ),
        "story_en": (
            "Magical moments with Mary Poppins! ✨<br>"
            "One day Mary Poppins said,<br>"
            "\"Today we go on a special outing!\"<br><br>"
            "The children followed Mary Poppins.<br>"
            "Suddenly they floated up to the ceiling!<br>"
            "\"Wow! We are flying!\" Jane shouted.<br>"
            "Michael could not stop laughing.<br>"
            "They had never been this happy before.<br>"
            "<span class=\"hl\">The children felt joy.</span>"
        ),
        "story_play": "Magical moments with Mary Poppins! One day Mary Poppins said, Today we go on a special outing! The children followed Mary Poppins. Suddenly they floated up to the ceiling! Wow! We are flying! Jane shouted. Michael could not stop laughing. They had never been this happy before. The children felt joy."
    },
    "week15b": {
        "story_kr": (
            "메리 포핀스의 마법은 어디에서 올까요? 🪄<br>"
            "메리 포핀스는 특별한 주문을 외우지 않았어요.<br>"
            "평범한 것에서 마법을 찾았어요!<br><br>"
            "쓴 약을 먹으면 달콤한 딸기 맛이 났어요.<br>"
            "계단 난간을 타면 위로 미끄러져 올라갔어요!<br>"
            "그림 속으로 뛰어들어 소풍을 갈 수도 있었어요.<br>"
            "평범한 것이 특별해지는 마법이었어요!<br>"
            "메리가 마법을 보여줘서 아이들은 기쁨을 느꼈어요.<br>"
            "<strong>메리가 마법을 보여줘서 아이들은 기쁨을 느꼈어요.</strong>"
        ),
        "story_en": (
            "Where does Mary Poppins's magic come from? 🪄<br>"
            "Mary Poppins did not say special spells.<br>"
            "She found magic in ordinary things!<br><br>"
            "Bitter medicine tasted like sweet strawberry.<br>"
            "Sliding up the banister was possible!<br>"
            "They could even jump into a painting for a picnic.<br>"
            "Ordinary things became extraordinary!<br>"
            "The children felt joy because Mary showed them magic.<br>"
            "<span class=\"hl\">The children felt joy because Mary showed them magic.</span>"
        ),
        "story_play": "Where does Mary Poppins magic come from? Mary Poppins did not say special spells. She found magic in ordinary things! Bitter medicine tasted like sweet strawberry. Sliding up the banister was possible! They could even jump into a painting for a picnic. Ordinary things became extraordinary! The children felt joy because Mary showed them magic."
    },
    "week15c": {
        "story_kr": (
            "Week 15 완성! 메리 포핀스의 진짜 마법! 💫<br>"
            "메리 포핀스의 진짜 마법은 무엇이었을까요?<br>"
            "특별한 마법 지팡이가 아니었어요.<br><br>"
            "평범한 것 속에서 놀라운 것을 찾는 능력이었어요!<br>"
            "비 오는 날도 우산과 함께라면 모험이 되었어요.<br>"
            "지루한 청소 시간도 노래와 함께라면 즐거웠어요.<br>"
            "아이들은 세상을 새로운 눈으로 보게 되었어요.<br>"
            "평범한 것이 특별해지는 마법!<br>"
            "<strong>메리가 평범한 것 속에서 마법을 보여줬기에 아이들은 기쁨을 느꼈어요.</strong>"
        ),
        "story_en": (
            "Week 15 complete! Mary Poppins's real magic! 💫<br>"
            "What was Mary Poppins's real magic?<br>"
            "It was not a special magic wand.<br><br>"
            "It was the ability to find wonder in ordinary things!<br>"
            "A rainy day became an adventure with an umbrella.<br>"
            "Boring cleaning time became fun with a song.<br>"
            "The children began to see the world with new eyes.<br>"
            "The magic of making ordinary things extraordinary!<br>"
            "<span class=\"hl\">The children felt joy because Mary showed them magic in ordinary things.</span>"
        ),
        "story_play": "Week 15 complete! Mary Poppins real magic! What was Mary Poppins real magic? It was not a special magic wand. It was the ability to find wonder in ordinary things! A rainy day became an adventure with an umbrella. Boring cleaning time became fun with a song. The children began to see the world with new eyes. The magic of making ordinary things extraordinary! The children felt joy because Mary showed them magic in ordinary things."
    },
    # ══════════ W16: She left because her work was done ══════════
    "week16a": {
        "story_kr": (
            "메리 포핀스가 떠나는 날이 다가왔어요. 👋<br>"
            "어느 날 아침, 바람의 방향이 바뀌었어요.<br>"
            "메리 포핀스는 조용히 가방을 챙겼어요.<br><br>"
            "\"어디 가세요?\" Jane이 물었어요.<br>"
            "\"바람이 바뀌었으니까.\" 메리 포핀스가 대답했어요.<br>"
            "아이들은 이미 많이 자랐어요.<br>"
            "스스로 방을 정리하고, 서로를 도와줄 줄 알게 되었어요.<br>"
            "메리 포핀스의 할 일이 끝난 거예요.<br>"
            "<strong>그녀는 할 일을 마쳤기에 떠났어요.</strong>"
        ),
        "story_en": (
            "The day came for Mary Poppins to leave. 👋<br>"
            "One morning, the wind changed direction.<br>"
            "Mary Poppins quietly packed her bag.<br><br>"
            "\"Where are you going?\" asked Jane.<br>"
            "\"The wind has changed,\" Mary Poppins answered.<br>"
            "The children had already grown so much.<br>"
            "They could tidy their rooms and help each other.<br>"
            "Mary Poppins's work was done.<br>"
            "<span class=\"hl\">She left because her work was done.</span>"
        ),
        "story_play": "The day came for Mary Poppins to leave. One morning, the wind changed direction. Mary Poppins quietly packed her bag. Where are you going? asked Jane. The wind has changed, Mary Poppins answered. The children had already grown so much. They could tidy their rooms and help each other. Mary Poppins work was done. She left because her work was done."
    },
    "week16b": {
        "story_kr": (
            "메리 포핀스가 떠난 후... 🏠<br>"
            "아이들은 처음에 많이 슬펐어요.<br>"
            "\"메리 포핀스 없이 어떻게 해?\" Michael이 울었어요.<br><br>"
            "하지만 시간이 지나면서 깨달았어요.<br>"
            "우산 없이도 비 오는 날이 모험이 될 수 있었어요!<br>"
            "약을 먹을 때 달콤한 맛을 상상할 수 있었어요.<br>"
            "메리 포핀스는 떠났지만, 마법은 아이들 안에 남았어요.<br>"
            "<strong>그녀는 떠났지만 마법은 남았어요.</strong>"
        ),
        "story_en": (
            "After Mary Poppins left... 🏠<br>"
            "The children were very sad at first.<br>"
            "\"How can we live without Mary Poppins?\" Michael cried.<br><br>"
            "But as time passed, they realized something.<br>"
            "A rainy day could still be an adventure — even without the umbrella!<br>"
            "They could imagine sweet flavors when taking medicine.<br>"
            "Mary Poppins was gone, but the magic stayed inside the children.<br>"
            "<span class=\"hl\">She left, but the magic stayed.</span>"
        ),
        "story_play": "After Mary Poppins left. The children were very sad at first. How can we live without Mary Poppins? Michael cried. But as time passed, they realized something. A rainy day could still be an adventure, even without the umbrella! They could imagine sweet flavors when taking medicine. Mary Poppins was gone, but the magic stayed inside the children. She left, but the magic stayed."
    },
    "week16c": {
        "story_kr": (
            "Week 16 & 메리 포핀스 완결! 🎉☂️<br>"
            "메리 포핀스는 영원히 함께할 수 없었어요.<br>"
            "하지만 그녀가 남긴 것은 영원했어요.<br><br>"
            "아이들은 평범한 것에서 마법을 찾는 법을 배웠어요.<br>"
            "규칙과 사랑이 함께할 수 있다는 걸 알게 됐어요.<br>"
            "서로를 돕고 배려하는 법도 배웠어요.<br>"
            "메리 포핀스의 마법은 아이들의 마음에 영원히 남았어요.<br>"
            "할 일을 마쳤기에 떠났지만, 마법은 영원히!<br>"
            "<strong>할 일을 마쳤기에 떠났지만 — 마법은 영원히 남았어요.</strong>"
        ),
        "story_en": (
            "Week 16 &amp; Mary Poppins — The End! 🎉☂️<br>"
            "Mary Poppins could not stay forever.<br>"
            "But what she left behind was eternal.<br><br>"
            "The children learned to find magic in ordinary things.<br>"
            "They learned that rules and love can exist together.<br>"
            "They learned to help and care for each other.<br>"
            "Mary Poppins's magic lived forever in the children's hearts.<br>"
            "She left because her work was done — but the magic lasted!<br>"
            "<span class=\"hl\">She left because her work was done — but the magic stayed forever.</span>"
        ),
        "story_play": "Week 16 and Mary Poppins, The End! Mary Poppins could not stay forever. But what she left behind was eternal. The children learned to find magic in ordinary things. They learned that rules and love can exist together. They learned to help and care for each other. Mary Poppins magic lived forever in the children hearts. She left because her work was done, but the magic stayed forever."
    },
}


def fix_file(filename):
    filepath = os.path.join(BASE, "grade4", filename + ".html")
    if not os.path.exists(filepath):
        print(f"  SKIP {filepath} (not found)")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    d = DATA[filename]

    # 1) Replace Korean story block
    html = re.sub(
        r'(<div class="robo-nm" style="color:var\(--gold\);">먼저 한국어로 읽어봐!</div>\s*<div class="robo-msg">)(.*?)(</div></div>\s*</div>)',
        lambda m: m.group(1) + d["story_kr"] + m.group(3),
        html, count=1, flags=re.DOTALL
    )

    # 2) Replace storyPlay() call text
    html = re.sub(
        r"(onclick=\"storyPlay\(')[^']*('\)\")",
        lambda m: m.group(1) + d["story_play"].replace("'", "\\'") + m.group(2),
        html, count=1
    )

    # 3) Replace English story block
    html = re.sub(
        r'(<div class="story-en">)(.*?)(</div>\s*</div><div class="prog">.*?width:22%)',
        lambda m: m.group(1) + d["story_en"] + m.group(3),
        html, count=1, flags=re.DOTALL
    )

    # 4) Fix v-play buttons: "듣기" → "🔊 듣기"
    html = html.replace('>듣기</button></div>', '>🔊 듣기</button></div>')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  OK {filepath}")


def main():
    for key in sorted(DATA.keys()):
        fix_file(key)
    print(f"\nDone! {len(DATA)} files fixed.")


if __name__ == "__main__":
    main()

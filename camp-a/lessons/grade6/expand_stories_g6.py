#!/usr/bin/env python3
"""
expand_stories_g6.py — Expand story sections in all 108 G6 lesson files.
G6 uses THREE English levels: A1 + A2 + B1 (same as G5).
"""
import re, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Book assignments ──
BOOKS = {
    range(1,9):   ("A Little Princess", "소공녀"),
    range(9,17):  ("Five Children and It", "다섯 아이와 모래 요정"),
    range(17,21): ("The Jungle Book", "정글북"),
    range(21,25): ("Pinocchio", "피노키오"),
    range(25,29): ("The Phantom Tollbooth", "신비한 톨부스"),
    range(29,33): ("Little Women", "작은 아씨들"),
    range(33,37): ("Emil and the Detectives", "에밀과 탐정들"),
}

def get_book(wk):
    for r, (en, kr) in BOOKS.items():
        if wk in r:
            return en, kr
    return "Unknown", "알 수 없음"

DAY_MAP = {"a": "Day1", "b": "Day2", "c": "Day3"}

# ── Weekly themes ──
WEEK_THEMES = {
    1: ("princess", "사라가 공주로서의 자신을 선언하다"),
    2: ("dignity", "사라가 내면의 품위를 지키다"),
    3: ("kind", "사라가 모든 사람에게 친절을 베풀다"),
    4: ("imagination", "사라가 상상력으로 버티다"),
    5: ("adversity", "역경이 사라의 진짜 성격을 드러내다"),
    6: ("integrity", "사라가 진실된 자신을 지키다"),
    7: ("kindness choice", "사라가 매일 친절을 선택하다"),
    8: ("privilege", "특권이 영원하지 않음을 깨닫다"),
    9: ("creature", "아이들이 신비한 생물을 발견하다"),
    10: ("consequences", "모든 소원에 결과가 따르다"),
    11: ("careful wishes", "소원을 빌 때 신중해야 함을 배우다"),
    12: ("wisdom", "상상력에는 지혜가 필요하다"),
    13: ("real happiness", "진정한 행복은 소원으로 얻을 수 없다"),
    14: ("mistakes", "실수에서 교훈을 얻다"),
    15: ("responsibility", "힘에는 책임이 따르다"),
    16: ("gifts alone", "어떤 선물은 쓰지 않는 게 지혜이다"),
    17: ("law", "정글에는 정글의 법칙이 있다"),
    18: ("belonging", "공유된 법이 소속감을 만든다"),
    19: ("nowhere", "모글리가 어디에도 속하지 못하다"),
    20: ("choice", "정체성은 선택을 요구하다"),
    21: ("lies", "거짓말이 모든 것을 악화시키다"),
    22: ("honesty", "진실된 것이 정직의 의미이다"),
    23: ("freedom", "자유는 책임을 요구하다"),
    24: ("real through goodness", "선함을 통해 진짜가 되다"),
    25: ("bored", "밀로가 모든 것에 지루해하다"),
    26: ("words numbers", "말과 숫자 둘 다 중요하다"),
    27: ("wrong roads", "잘못된 길도 어딘가로 이끈다"),
    28: ("adventures", "시도할 때 모험이 시작된다"),
    29: ("own path", "각 자매가 자신의 길을 선택하다"),
    30: ("Jo refuses", "조가 사회의 기대를 거부하다"),
    31: ("true love", "진정한 사랑은 함께 성장하는 것이다"),
    32: ("character>wealth", "성격이 부보다 중요하다"),
    33: ("catches thief", "에밀이 도둑을 잡다"),
    34: ("teamwork", "아이들이 팀으로 일하다"),
    35: ("bravery", "용기는 두려움 속에서 행동하는 것이다"),
    36: ("trust", "신뢰와 팀워크가 문제를 해결하다"),
}

# ── Story content: all 108 stories ──
def _build_all_stories():
    S = {}

    # ══════════════════════════════════════════
    # A LITTLE PRINCESS (W01-W08)
    # ══════════════════════════════════════════

    # W01 — princess
    S[(1,0)] = {
        "korean": (
            "오늘부터 소공녀 이야기를 시작해요! 👑<br>"
            "이 소설은 영국 작가 프랜시스 호지슨 버넷이 썼어요.<br>"
            "주인공은 사라 크루라는 소녀예요.<br>"
            "사라의 아버지는 매우 부유한 사업가였어요.<br><br>"
            "사라는 런던의 고급 기숙학교에 다녔어요.<br>"
            "그녀는 학교에서 공주처럼 대우받았어요.<br>"
            "예쁜 옷, 맛있는 음식, 특별한 방이 있었죠.<br>"
            "하지만 어느 날 아버지가 돌아가시고 재산을 잃었어요.<br>"
            "사라는 하루아침에 하녀가 되었어요.<br>"
            "다른 아이들은 사라를 무시하기 시작했어요.<br>"
            "그래도 사라는 당당하게 고개를 들었어요.<br>"
            "<strong>사라는 '나는 여전히 공주야'라고 스스로에게 말했어요.</strong>"
        ),
        "a1_html": "Sara was a rich girl. 👑<br>Her father died and she lost everything.<br>But Sara was still brave.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara was a rich girl. Her father died and she lost everything. But Sara was still brave. __KEY__",
        "a2_html": "Sara Crewe lived at a fancy school in London.<br>Her father was very rich and loved her deeply.<br>When her father died, Sara lost all her money.<br>She became a servant at the school.<br><span class=\"hl\">__KEY__</span><br>Sara believed being a princess was about her heart.",
        "a2_tts": "Sara Crewe lived at a fancy school in London. Her father was very rich and loved her deeply. When her father died, Sara lost all her money. She became a servant at the school. __KEY__ Sara believed being a princess was about her heart.",
        "b1_html": "Sara Crewe was the wealthiest student at Miss Minchin's school in London.<br>Her father adored her and gave her everything a child could want.<br>However, when her father suddenly died, Sara lost all her wealth overnight.<br>She was forced to work as a servant in the cold attic.<br><span class=\"hl\">__KEY__</span><br>Although the other children mocked her ragged clothes, Sara refused to lose her dignity.<br>Because she believed that true royalty comes from within, she held her head high.<br>Sara's story teaches us that identity is not about what we have, but who we are inside.",
        "b1_tts": "Sara Crewe was the wealthiest student at Miss Minchin's school in London. Her father adored her and gave her everything a child could want. However, when her father suddenly died, Sara lost all her wealth overnight. She was forced to work as a servant in the cold attic. __KEY__ Although the other children mocked her ragged clothes, Sara refused to lose her dignity. Because she believed that true royalty comes from within, she held her head high. Sara's story teaches us that identity is not about what we have, but who we are inside.",
    }
    S[(1,1)] = {
        "korean": (
            "사라의 이야기가 계속돼요!<br>"
            "사라는 부자였을 때 많은 친구가 있었어요.<br>"
            "하지만 가난해지자 친구들이 떠났어요.<br>"
            "학교의 교장 선생님도 사라를 차갑게 대했어요.<br><br>"
            "사라에게는 이제 예쁜 옷도, 맛있는 음식도 없었어요.<br>"
            "차가운 다락방에서 잠을 자야 했어요.<br>"
            "하지만 사라는 포기하지 않았어요.<br>"
            "재산이 없어도 사라의 마음은 변하지 않았어요.<br>"
            "사라는 '재산 없이도 나는 공주'라고 믿었어요.<br>"
            "진정한 가치는 돈이 아니라 마음에 있다는 걸 알았어요.<br>"
            "사라의 강한 내면이 빛나기 시작했어요.<br>"
            "<strong>재산은 사라의 진짜 모습을 바꿀 수 없었어요.</strong>"
        ),
        "a1_html": "Sara lost her money.<br>She had no pretty clothes.<br>But her heart did not change.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara lost her money. She had no pretty clothes. But her heart did not change. __KEY__",
        "a2_html": "When Sara became poor, her friends left her.<br>Miss Minchin treated her cruelly.<br>Sara slept in a cold attic room with no warmth.<br>But Sara knew her worth was not about money.<br><span class=\"hl\">__KEY__</span><br>Her spirit stayed strong even without wealth.",
        "a2_tts": "When Sara became poor, her friends left her. Miss Minchin treated her cruelly. Sara slept in a cold attic room with no warmth. But Sara knew her worth was not about money. __KEY__ Her spirit stayed strong even without wealth.",
        "b1_html": "After losing everything, Sara discovered who her true friends were.<br>Most of the girls at school turned their backs on her because she was no longer rich.<br>Miss Minchin forced Sara to work long hours without proper food or rest.<br>However, Sara refused to let poverty define who she was.<br><span class=\"hl\">__KEY__</span><br>Because she understood that wealth does not make a person worthy, she found strength within herself.<br>Although her life was hard, Sara's inner light never dimmed.<br>She proved that true value comes from character, not from possessions.",
        "b1_tts": "After losing everything, Sara discovered who her true friends were. Most of the girls at school turned their backs on her because she was no longer rich. Miss Minchin forced Sara to work long hours without proper food or rest. However, Sara refused to let poverty define who she was. __KEY__ Because she understood that wealth does not make a person worthy, she found strength within herself. Although her life was hard, Sara's inner light never dimmed. She proved that true value comes from character, not from possessions.",
    }
    S[(1,2)] = {
        "korean": (
            "소공녀 첫 주의 마지막 이야기예요!<br>"
            "사라는 누더기를 입고도 당당했어요.<br>"
            "추운 다락방에서도 미소를 잃지 않았어요.<br>"
            "사라는 자신만의 철학을 가지고 있었어요.<br><br>"
            "공주란 왕관이나 드레스가 아니에요.<br>"
            "공주란 어떤 상황에서도 품위를 지키는 거예요.<br>"
            "사라는 가장 힘든 순간에도 친절했어요.<br>"
            "배고플 때도 다른 사람을 먼저 생각했어요.<br>"
            "이것이 바로 진정한 공주의 모습이에요.<br>"
            "환경이 변해도 사라의 본질은 변하지 않았어요.<br>"
            "누더기를 입은 공주도 여전히 공주예요.<br>"
            "<strong>어떤 일이 와도 사라는 항상 공주였어요!</strong>"
        ),
        "a1_html": "Sara wore old clothes.<br>She was cold and hungry.<br>But she was still kind.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara wore old clothes. She was cold and hungry. But she was still kind. __KEY__",
        "a2_html": "Sara had nothing but rags to wear.<br>The attic was freezing and she was always hungry.<br>Other children did not understand her quiet strength.<br>Sara believed a princess is about the heart, not the crown.<br><span class=\"hl\">__KEY__</span><br>No matter what happened, Sara stayed true to herself.",
        "a2_tts": "Sara had nothing but rags to wear. The attic was freezing and she was always hungry. Other children did not understand her quiet strength. Sara believed a princess is about the heart, not the crown. __KEY__ No matter what happened, Sara stayed true to herself.",
        "b1_html": "Sara stood in the cold attic wearing nothing but thin, torn rags.<br>The wind howled through the cracks in the wall, and her stomach ached with hunger.<br>However, Sara's eyes still sparkled with an inner fire that nothing could extinguish.<br>She told herself that a true princess is defined by her actions, not her circumstances.<br><span class=\"hl\">__KEY__</span><br>Because Sara chose dignity over despair, she inspired everyone around her.<br>Although the world tried to break her spirit, she remained unshakable.<br>This is the deepest lesson of Sara's story: our identity is our choice.",
        "b1_tts": "Sara stood in the cold attic wearing nothing but thin, torn rags. The wind howled through the cracks in the wall, and her stomach ached with hunger. However, Sara's eyes still sparkled with an inner fire that nothing could extinguish. She told herself that a true princess is defined by her actions, not her circumstances. __KEY__ Because Sara chose dignity over despair, she inspired everyone around her. Although the world tried to break her spirit, she remained unshakable. This is the deepest lesson of Sara's story: our identity is our choice.",
    }

    # W02 — dignity
    S[(2,0)] = {
        "korean": (
            "이번 주는 '품위'에 대해 이야기해요.<br>"
            "사라는 하녀가 되었지만 품위를 잃지 않았어요.<br>"
            "다른 아이들이 놀려도 화를 내지 않았어요.<br>"
            "사라는 조용히 자신의 일을 했어요.<br><br>"
            "품위란 무엇일까요?<br>"
            "비싼 옷을 입는 것이 아니에요.<br>"
            "다른 사람을 존중하고 자신을 존중하는 거예요.<br>"
            "사라는 가장 어려운 순간에도 예의를 지켰어요.<br>"
            "이것이 진정한 품위의 모습이에요.<br>"
            "품위는 밖에서 오는 게 아니라 안에서 나오는 거예요.<br>"
            "사라는 그것을 온 세상에 보여주었어요.<br>"
            "<strong>진정한 품위는 내면에서 나온다는 것을 사라가 증명했어요.</strong>"
        ),
        "a1_html": "Sara became a servant.<br>People were mean to her.<br>But Sara stayed calm and kind.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara became a servant. People were mean to her. But Sara stayed calm and kind. __KEY__",
        "a2_html": "Sara worked hard every day as a servant.<br>The other children called her names and laughed.<br>Miss Minchin gave her the hardest jobs.<br>But Sara never lost her polite manner.<br><span class=\"hl\">__KEY__</span><br>She showed that dignity is about how you treat others.",
        "a2_tts": "Sara worked hard every day as a servant. The other children called her names and laughed. Miss Minchin gave her the hardest jobs. But Sara never lost her polite manner. __KEY__ She showed that dignity is about how you treat others.",
        "b1_html": "Even as a servant, Sara carried herself with quiet grace that amazed everyone.<br>When children insulted her, she responded with patience instead of anger.<br>Miss Minchin tried to crush Sara's spirit by giving her impossible tasks.<br>However, Sara completed every task without complaint, maintaining her composure.<br><span class=\"hl\">__KEY__</span><br>Because dignity is a quality of the soul, no one could strip it away from Sara.<br>Although poverty changed her outer life completely, it could never touch her inner strength.<br>Sara taught everyone that true dignity shines brightest in the darkest moments.",
        "b1_tts": "Even as a servant, Sara carried herself with quiet grace that amazed everyone. When children insulted her, she responded with patience instead of anger. Miss Minchin tried to crush Sara's spirit by giving her impossible tasks. However, Sara completed every task without complaint, maintaining her composure. __KEY__ Because dignity is a quality of the soul, no one could strip it away from Sara. Although poverty changed her outer life completely, it could never touch her inner strength. Sara taught everyone that true dignity shines brightest in the darkest moments.",
    }
    S[(2,1)] = {
        "korean": (
            "사라의 품위 이야기가 계속돼요.<br>"
            "학교에서 사라를 가장 괴롭히는 사람이 있었어요.<br>"
            "바로 교장 민친 선생님이었어요.<br>"
            "민친 선생님은 사라가 부자일 때만 친절했어요.<br><br>"
            "사라가 가난해지자 태도가 완전히 변했어요.<br>"
            "하지만 사라는 민친 선생님에게도 예의를 갖췄어요.<br>"
            "왜냐하면 품위란 상대가 아니라 자기 자신의 선택이니까요.<br>"
            "상대가 나를 어떻게 대하든 나는 나답게 행동할 수 있어요.<br>"
            "이것이 진정한 내면의 힘이에요.<br>"
            "가난이 사라의 품위를 빼앗을 수 없었어요.<br>"
            "사라의 품위는 재산이 아니라 마음에서 왔으니까요.<br>"
            "<strong>진정한 품위는 가난도 빼앗을 수 없어요.</strong>"
        ),
        "a1_html": "Miss Minchin was mean.<br>Sara stayed polite.<br>Her dignity was inside her.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Miss Minchin was mean. Sara stayed polite. Her dignity was inside her. __KEY__",
        "a2_html": "Miss Minchin changed when Sara became poor.<br>She was only kind to Sara when Sara had money.<br>Now she treated Sara like she was nothing.<br>But Sara kept her manners and self-respect.<br><span class=\"hl\">__KEY__</span><br>Sara proved that real dignity does not depend on money.",
        "a2_tts": "Miss Minchin changed when Sara became poor. She was only kind to Sara when Sara had money. Now she treated Sara like she was nothing. But Sara kept her manners and self-respect. __KEY__ Sara proved that real dignity does not depend on money.",
        "b1_html": "Miss Minchin revealed her true character when Sara lost her fortune.<br>She had only valued Sara for her father's wealth, not for who Sara really was.<br>Now she treated Sara with open cruelty, assigning her the worst chores.<br>However, Sara never responded with anger or rudeness, even when provoked.<br><span class=\"hl\">__KEY__</span><br>Because Sara understood that dignity is a personal choice, she refused to stoop to cruelty.<br>Although Miss Minchin tried every method to humiliate her, Sara remained graceful.<br>This showed everyone that poverty can take material things, but never a person's character.",
        "b1_tts": "Miss Minchin revealed her true character when Sara lost her fortune. She had only valued Sara for her father's wealth, not for who Sara really was. Now she treated Sara with open cruelty, assigning her the worst chores. However, Sara never responded with anger or rudeness, even when provoked. __KEY__ Because Sara understood that dignity is a personal choice, she refused to stoop to cruelty. Although Miss Minchin tried every method to humiliate her, Sara remained graceful. This showed everyone that poverty can take material things, but never a person's character.",
    }
    S[(2,2)] = {
        "korean": (
            "품위에 대한 마지막 이야기예요.<br>"
            "사라는 매일 아침 일찍 일어나 일했어요.<br>"
            "무거운 석탄을 나르고 바닥을 닦았어요.<br>"
            "손은 거칠어지고 몸은 지쳐갔어요.<br><br>"
            "하지만 사라의 눈빛은 여전히 맑았어요.<br>"
            "사라는 '품위란 행동에서 나오는 것'이라고 생각했어요.<br>"
            "부유함이 주는 품위와 내면의 품위는 달라요.<br>"
            "부유함의 품위는 돈이 사라지면 함께 사라져요.<br>"
            "하지만 내면의 품위는 영원해요.<br>"
            "사라는 이 진실을 몸소 보여주었어요.<br>"
            "세상에서 가장 가난하지만 가장 품위 있는 소녀였어요.<br>"
            "<strong>진정한 품위는 부가 줄 수도, 가난이 빼앗을 수도 없어요.</strong>"
        ),
        "a1_html": "Sara worked very hard.<br>Her hands were rough.<br>But her heart was still noble.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara worked very hard. Her hands were rough. But her heart was still noble. __KEY__",
        "a2_html": "Every morning Sara carried heavy coal and scrubbed floors.<br>Her body grew tired but her spirit stayed strong.<br>She thought about what dignity really means.<br>It is not about fancy clothes or rich food.<br><span class=\"hl\">__KEY__</span><br>Sara showed the world what true inner dignity looks like.",
        "a2_tts": "Every morning Sara carried heavy coal and scrubbed floors. Her body grew tired but her spirit stayed strong. She thought about what dignity really means. It is not about fancy clothes or rich food. __KEY__ Sara showed the world what true inner dignity looks like.",
        "b1_html": "Day after day, Sara performed the hardest tasks in the school without rest.<br>Her once-soft hands became rough, and her beautiful dresses were replaced by rags.<br>However, there was something about Sara that wealth could never have given her.<br>It was the dignity that came from knowing exactly who she was inside.<br><span class=\"hl\">__KEY__</span><br>Because true dignity is built through choices and actions, it cannot be bought or sold.<br>Although Sara had lost every material comfort, she possessed something priceless.<br>Her story reminds us that the richest person is the one with the strongest character.",
        "b1_tts": "Day after day, Sara performed the hardest tasks in the school without rest. Her once-soft hands became rough, and her beautiful dresses were replaced by rags. However, there was something about Sara that wealth could never have given her. It was the dignity that came from knowing exactly who she was inside. __KEY__ Because true dignity is built through choices and actions, it cannot be bought or sold. Although Sara had lost every material comfort, she possessed something priceless. Her story reminds us that the richest person is the one with the strongest character.",
    }

    # W03 — kind
    S[(3,0)] = {
        "korean": (
            "이번 주는 사라의 친절함에 대해 알아봐요.<br>"
            "사라는 부자였을 때도 모든 사람에게 친절했어요.<br>"
            "하녀 베키에게도 친구처럼 대했어요.<br>"
            "다른 부잣집 아이들은 하녀를 무시했지만요.<br><br>"
            "사라는 사람을 돈으로 구분하지 않았어요.<br>"
            "모든 사람은 똑같이 소중하다고 믿었어요.<br>"
            "이것이 사라를 특별하게 만든 거예요.<br>"
            "부자든 가난하든 사라의 친절함은 같았어요.<br>"
            "사라에게 친절이란 습관이 아니라 신념이었어요.<br>"
            "모든 사람이 존중받을 자격이 있다고 믿었거든요.<br>"
            "이런 태도가 사라를 진정한 공주로 만들었어요.<br>"
            "<strong>사라의 친절함은 모든 사람을 평등하게 대하는 것이었어요.</strong>"
        ),
        "a1_html": "Sara was kind to everyone.<br>She helped the servants too.<br>Rich or poor, she was the same.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara was kind to everyone. She helped the servants too. Rich or poor, she was the same. __KEY__",
        "a2_html": "Sara treated the servant Becky as a friend.<br>Other rich children ignored the servants completely.<br>But Sara believed every person deserves kindness.<br>She shared her food and stories with Becky.<br><span class=\"hl\">__KEY__</span><br>Her kindness made her a true princess in everyone's eyes.",
        "a2_tts": "Sara treated the servant Becky as a friend. Other rich children ignored the servants completely. But Sara believed every person deserves kindness. She shared her food and stories with Becky. __KEY__ Her kindness made her a true princess in everyone's eyes.",
        "b1_html": "When Sara was wealthy, she could have acted like other rich children who ignored servants.<br>Instead, she befriended Becky, the youngest servant at the school, treating her as an equal.<br>Sara shared her meals, her stories, and her warmth with everyone she met.<br>However, what made Sara's kindness remarkable was that it never changed with her circumstances.<br><span class=\"hl\">__KEY__</span><br>Because Sara saw the humanity in every person, she treated everyone with equal respect.<br>Although many people only show kindness when it is convenient, Sara made it her way of life.<br>Her example teaches us that true kindness sees no boundaries of class or wealth.",
        "b1_tts": "When Sara was wealthy, she could have acted like other rich children who ignored servants. Instead, she befriended Becky, the youngest servant at the school, treating her as an equal. Sara shared her meals, her stories, and her warmth with everyone she met. However, what made Sara's kindness remarkable was that it never changed with her circumstances. __KEY__ Because Sara saw the humanity in every person, she treated everyone with equal respect. Although many people only show kindness when it is convenient, Sara made it her way of life. Her example teaches us that true kindness sees no boundaries of class or wealth.",
    }
    S[(3,1)] = {
        "korean": (
            "사라의 친절함은 특별한 의미가 있어요.<br>"
            "사라가 가난해진 후에도 친절함은 변하지 않았어요.<br>"
            "오히려 가난해진 후의 친절이 더 빛났어요.<br>"
            "왜냐하면 나눌 것이 거의 없었기 때문이에요.<br><br>"
            "사라는 빵 한 조각밖에 없었어요.<br>"
            "하지만 거리에서 더 배고픈 아이를 만났어요.<br>"
            "사라는 자신의 빵을 그 아이에게 나눠줬어요.<br>"
            "아무것도 없을 때 나누는 것이 진정한 친절이에요.<br>"
            "사라는 모든 사람을 동등하게 대했어요.<br>"
            "부자든 가난하든 차별하지 않았어요.<br>"
            "이것이 사라의 진정한 아름다움이었어요.<br>"
            "<strong>사라는 자신이 가장 힘들 때에도 다른 사람에게 친절했어요.</strong>"
        ),
        "a1_html": "Sara had only one bread.<br>She gave it to a hungry child.<br>That is real kindness.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara had only one bread. She gave it to a hungry child. That is real kindness. __KEY__",
        "a2_html": "Even when Sara had almost nothing, she still shared.<br>One day she found a hungry child on the street.<br>Sara gave her bread to the child, keeping none for herself.<br>Kindness that costs you something is the most meaningful kind.<br><span class=\"hl\">__KEY__</span><br>Sara proved that equal kindness has nothing to do with wealth.",
        "a2_tts": "Even when Sara had almost nothing, she still shared. One day she found a hungry child on the street. Sara gave her bread to the child, keeping none for herself. Kindness that costs you something is the most meaningful kind. __KEY__ Sara proved that equal kindness has nothing to do with wealth.",
        "b1_html": "After becoming poor, Sara's kindness became even more powerful and meaningful.<br>She had almost nothing, yet she still found ways to give to others in need.<br>One cold day, Sara shared her only piece of bread with a starving child on the street.<br>However, Sara did not see this as sacrifice, because kindness was simply who she was.<br><span class=\"hl\">__KEY__</span><br>Because she treated every person as worthy of respect, her kindness was never selective.<br>Although she could barely feed herself, she never hesitated to help someone in greater need.<br>Sara showed us that the truest kindness comes from those who have the least to give.",
        "b1_tts": "After becoming poor, Sara's kindness became even more powerful and meaningful. She had almost nothing, yet she still found ways to give to others in need. One cold day, Sara shared her only piece of bread with a starving child on the street. However, Sara did not see this as sacrifice, because kindness was simply who she was. __KEY__ Because she treated every person as worthy of respect, her kindness was never selective. Although she could barely feed herself, she never hesitated to help someone in greater need. Sara showed us that the truest kindness comes from those who have the least to give.",
    }
    S[(3,2)] = {
        "korean": (
            "친절에 대한 이번 주 마지막 이야기예요.<br>"
            "사라의 친절함은 결국 보상을 받았어요.<br>"
            "하지만 사라는 보상을 바라고 친절한 게 아니었어요.<br>"
            "사라에게 친절은 자연스러운 삶의 방식이었어요.<br><br>"
            "사라가 빵을 나눠준 제과점 주인은 감동받았어요.<br>"
            "베키도 사라의 친절에 평생의 우정을 바쳤어요.<br>"
            "진정한 친절은 돌아오기 마련이에요.<br>"
            "하지만 그것을 기대하지 않는 것이 진짜 친절이에요.<br>"
            "사라는 부와 지위에 상관없이 모든 이를 존중했어요.<br>"
            "이것이 사라가 진정한 공주인 이유예요.<br>"
            "왕관이 아니라 마음이 공주를 만드는 거예요.<br>"
            "<strong>사라의 이야기는 친절이 세상을 바꿀 수 있음을 보여줘요.</strong>"
        ),
        "a1_html": "Sara was kind to everyone.<br>She never asked for anything back.<br>Kindness changed people around her.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara was kind to everyone. She never asked for anything back. Kindness changed people around her. __KEY__",
        "a2_html": "Sara's kindness touched everyone around her.<br>The baker who saw her share bread was deeply moved.<br>Becky became Sara's loyal friend because of her kindness.<br>Sara never expected anything in return for being kind.<br><span class=\"hl\">__KEY__</span><br>She treated people equally regardless of their wealth or position.",
        "a2_tts": "Sara's kindness touched everyone around her. The baker who saw her share bread was deeply moved. Becky became Sara's loyal friend because of her kindness. Sara never expected anything in return for being kind. __KEY__ She treated people equally regardless of their wealth or position.",
        "b1_html": "Sara's consistent kindness eventually inspired everyone who witnessed it.<br>The baker was so moved by Sara sharing her bread that she began helping hungry children too.<br>Becky devoted her lifelong friendship to Sara because of the respect Sara always showed her.<br>However, Sara never performed kindness expecting something in return.<br><span class=\"hl\">__KEY__</span><br>Because genuine kindness comes from the heart without conditions, it transforms communities.<br>Although Sara had no wealth or social position to offer, her kindness was her greatest gift.<br>Her story proves that one person's consistent kindness can truly change the world around them.",
        "b1_tts": "Sara's consistent kindness eventually inspired everyone who witnessed it. The baker was so moved by Sara sharing her bread that she began helping hungry children too. Becky devoted her lifelong friendship to Sara because of the respect Sara always showed her. However, Sara never performed kindness expecting something in return. __KEY__ Because genuine kindness comes from the heart without conditions, it transforms communities. Although Sara had no wealth or social position to offer, her kindness was her greatest gift. Her story proves that one person's consistent kindness can truly change the world around them.",
    }

    # W04 — imagination
    S[(4,0)] = {
        "korean": (
            "이번 주는 사라의 상상력에 대해 이야기해요.<br>"
            "사라는 차가운 다락방에서 생활했어요.<br>"
            "하지만 상상력으로 다른 세계를 만들었어요.<br>"
            "다락방을 멋진 성으로 상상했어요.<br><br>"
            "낡은 담요는 비단 커튼이 되었어요.<br>"
            "딱딱한 빵은 맛있는 만찬이 되었어요.<br>"
            "사라의 상상력은 현실을 바꾸는 힘이 있었어요.<br>"
            "상상력 덕분에 사라는 절망하지 않았어요.<br>"
            "마음속에서 여전히 공주의 삶을 살았으니까요.<br>"
            "상상력은 가장 어두운 곳에도 빛을 가져와요.<br>"
            "사라에게 상상력은 생존의 도구였어요.<br>"
            "<strong>상상력이 사라를 가장 어두운 시간 속에서 지탱해 주었어요.</strong>"
        ),
        "a1_html": "Sara lived in a cold room.<br>She imagined it was a castle.<br>Her mind kept her strong.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara lived in a cold room. She imagined it was a castle. Her mind kept her strong. __KEY__",
        "a2_html": "Sara turned her cold attic into a palace with her imagination.<br>Old blankets became silk curtains in her mind.<br>Hard bread became a royal feast when she imagined it.<br>Sara's imagination was her greatest weapon against despair.<br><span class=\"hl\">__KEY__</span><br>She survived the hardest times because her mind was free.",
        "a2_tts": "Sara turned her cold attic into a palace with her imagination. Old blankets became silk curtains in her mind. Hard bread became a royal feast when she imagined it. Sara's imagination was her greatest weapon against despair. __KEY__ She survived the hardest times because her mind was free.",
        "b1_html": "In her freezing attic, Sara discovered the incredible power of imagination.<br>She transformed her bare room into a magnificent castle with silk curtains and warm fires.<br>The stale bread became a wonderful feast, and the mice became her loyal subjects.<br>However, Sara's imagination was more than just pretending — it was a survival tool.<br><span class=\"hl\">__KEY__</span><br>Because her mind was free even when her body was trapped, Sara never truly suffered alone.<br>Although her physical world was dark and cold, her inner world was bright and limitless.<br>Sara proved that imagination is the one treasure that can never be taken away.",
        "b1_tts": "In her freezing attic, Sara discovered the incredible power of imagination. She transformed her bare room into a magnificent castle with silk curtains and warm fires. The stale bread became a wonderful feast, and the mice became her loyal subjects. However, Sara's imagination was more than just pretending — it was a survival tool. __KEY__ Because her mind was free even when her body was trapped, Sara never truly suffered alone. Although her physical world was dark and cold, her inner world was bright and limitless. Sara proved that imagination is the one treasure that can never be taken away.",
    }
    S[(4,1)] = {
        "korean": (
            "사라의 상상력 이야기가 계속돼요.<br>"
            "사라는 상상으로 이야기를 만들어냈어요.<br>"
            "그 이야기를 다른 아이들에게 들려주었어요.<br>"
            "아이들은 사라의 이야기에 빠져들었어요.<br><br>"
            "사라의 상상력은 다른 사람에게도 빛이 되었어요.<br>"
            "외로운 아이들에게 희망을 주었어요.<br>"
            "상상력은 자신만을 위한 것이 아니에요.<br>"
            "다른 사람과 나누면 더 큰 힘이 돼요.<br>"
            "사라는 이야기를 통해 친구를 만들었어요.<br>"
            "가장 어두운 시간에도 빛을 만들어냈어요.<br>"
            "상상력은 사라의 가장 소중한 보물이었어요.<br>"
            "<strong>사라의 상상력은 어둠 속에서도 빛나는 등불이었어요.</strong>"
        ),
        "a1_html": "Sara told stories to other children.<br>They loved her stories.<br>Stories gave them hope.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara told stories to other children. They loved her stories. Stories gave them hope. __KEY__",
        "a2_html": "Sara used her imagination to create wonderful stories.<br>She shared these stories with lonely children at the school.<br>The children were amazed by her vivid tales of adventure.<br>Her stories brought light to the darkest days.<br><span class=\"hl\">__KEY__</span><br>Through imagination, Sara kept herself and others strong.",
        "a2_tts": "Sara used her imagination to create wonderful stories. She shared these stories with lonely children at the school. The children were amazed by her vivid tales of adventure. Her stories brought light to the darkest days. __KEY__ Through imagination, Sara kept herself and others strong.",
        "b1_html": "Sara's imagination did not just help her survive — it brought joy to others as well.<br>She created vivid stories about magical lands and brave heroes, sharing them with lonely children.<br>Even the meanest children at school were drawn to Sara's enchanting tales.<br>However, the true power of her stories was not entertainment but the hope they inspired.<br><span class=\"hl\">__KEY__</span><br>Because imagination can be shared, it multiplies in power and becomes a gift to many.<br>Although Sara had nothing material to offer, her stories were more valuable than gold.<br>She showed that creativity and imagination can light up even the darkest of times.",
        "b1_tts": "Sara's imagination did not just help her survive — it brought joy to others as well. She created vivid stories about magical lands and brave heroes, sharing them with lonely children. Even the meanest children at school were drawn to Sara's enchanting tales. However, the true power of her stories was not entertainment but the hope they inspired. __KEY__ Because imagination can be shared, it multiplies in power and becomes a gift to many. Although Sara had nothing material to offer, her stories were more valuable than gold. She showed that creativity and imagination can light up even the darkest of times.",
    }
    S[(4,2)] = {
        "korean": (
            "상상력 주제의 마지막 이야기예요.<br>"
            "사라의 상상력은 그녀의 영혼을 살려두었어요.<br>"
            "몸은 차갑고 배고팠지만 마음은 자유로웠어요.<br>"
            "상상 속에서 사라는 어디든 갈 수 있었어요.<br><br>"
            "따뜻한 벽난로 앞에 앉을 수도 있었어요.<br>"
            "맛있는 음식이 가득한 식탁을 상상할 수도 있었어요.<br>"
            "상상력은 사라에게 날개를 달아주었어요.<br>"
            "현실이 아무리 힘들어도 마음은 날 수 있었어요.<br>"
            "이것이 상상력의 진정한 힘이에요.<br>"
            "우리의 마음은 어떤 감옥도 가둘 수 없어요.<br>"
            "사라는 그것을 모든 어린이에게 가르쳐 주었어요.<br>"
            "<strong>사라의 상상력은 그녀의 영혼과 정신을 살아있게 했어요.</strong>"
        ),
        "a1_html": "Sara could go anywhere in her mind.<br>She imagined warm fires and good food.<br>Her spirit was always free.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara could go anywhere in her mind. She imagined warm fires and good food. Her spirit was always free. __KEY__",
        "a2_html": "In her cold attic, Sara traveled the world through imagination.<br>She sat by warm fires and ate wonderful meals in her mind.<br>Imagination gave Sara wings when her body could not move.<br>No matter how hard life was, her mind was always free.<br><span class=\"hl\">__KEY__</span><br>Sara's imagination was her way of keeping her spirit alive.",
        "a2_tts": "In her cold attic, Sara traveled the world through imagination. She sat by warm fires and ate wonderful meals in her mind. Imagination gave Sara wings when her body could not move. No matter how hard life was, her mind was always free. __KEY__ Sara's imagination was her way of keeping her spirit alive.",
        "b1_html": "Sara's imagination became her most powerful tool for survival during her darkest days.<br>While her body shivered in the cold attic, her mind soared through magical kingdoms.<br>She imagined warm fires, delicious feasts, and adventures in faraway lands.<br>However, Sara's imagination was not an escape from reality but a way to endure it.<br><span class=\"hl\">__KEY__</span><br>Because the mind cannot be imprisoned by physical circumstances, Sara remained truly free.<br>Although walls and locks confined her body, nothing could cage her imagination.<br>Sara's story tells us that our greatest freedom lies within our own minds.",
        "b1_tts": "Sara's imagination became her most powerful tool for survival during her darkest days. While her body shivered in the cold attic, her mind soared through magical kingdoms. She imagined warm fires, delicious feasts, and adventures in faraway lands. However, Sara's imagination was not an escape from reality but a way to endure it. __KEY__ Because the mind cannot be imprisoned by physical circumstances, Sara remained truly free. Although walls and locks confined her body, nothing could cage her imagination. Sara's story tells us that our greatest freedom lies within our own minds.",
    }

    # W05 — adversity
    S[(5,0)] = {
        "korean": (
            "이번 주는 역경에 대해 이야기해요.<br>"
            "역경이란 매우 힘든 상황을 말해요.<br>"
            "사라는 엄청난 역경을 겪었어요.<br>"
            "부자에서 하녀로, 따뜻한 방에서 차가운 다락방으로.<br><br>"
            "하지만 역경은 사라를 무너뜨리지 않았어요.<br>"
            "오히려 사라의 진짜 성격을 보여주었어요.<br>"
            "편안할 때는 누구나 착할 수 있어요.<br>"
            "하지만 힘들 때 어떻게 행동하는지가 진짜예요.<br>"
            "사라는 가장 힘든 순간에도 친절하고 용감했어요.<br>"
            "역경이 사라의 내면에 숨겨진 강함을 드러냈어요.<br>"
            "어려움은 우리를 파괴하는 게 아니라 성장시켜요.<br>"
            "<strong>역경은 우리 안에 이미 있는 성격을 드러내 줘요.</strong>"
        ),
        "a1_html": "Life was very hard for Sara.<br>But she stayed strong and kind.<br>Hard times showed who she really was.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Life was very hard for Sara. But she stayed strong and kind. Hard times showed who she really was. __KEY__",
        "a2_html": "Sara went from being rich to being a poor servant.<br>Everything she had was taken away from her.<br>But adversity did not destroy Sara — it showed her true self.<br>Anyone can be kind when life is easy.<br><span class=\"hl\">__KEY__</span><br>Sara showed her real character when life was at its hardest.",
        "a2_tts": "Sara went from being rich to being a poor servant. Everything she had was taken away from her. But adversity did not destroy Sara — it showed her true self. Anyone can be kind when life is easy. __KEY__ Sara showed her real character when life was at its hardest.",
        "b1_html": "Sara's fall from wealth to poverty was one of the greatest tests a child could face.<br>She lost her home, her comfort, her friends, and even her identity in others' eyes.<br>However, adversity did not break Sara — instead, it revealed the strength she always had inside.<br>When life was comfortable, her character was hidden, but hardship made it shine brightly.<br><span class=\"hl\">__KEY__</span><br>Because difficult times strip away everything except our true nature, they are the ultimate test.<br>Although Sara suffered greatly, she emerged stronger and more compassionate than before.<br>Her story teaches us that adversity is not our enemy but our most honest mirror.",
        "b1_tts": "Sara's fall from wealth to poverty was one of the greatest tests a child could face. She lost her home, her comfort, her friends, and even her identity in others' eyes. However, adversity did not break Sara — instead, it revealed the strength she always had inside. When life was comfortable, her character was hidden, but hardship made it shine brightly. __KEY__ Because difficult times strip away everything except our true nature, they are the ultimate test. Although Sara suffered greatly, she emerged stronger and more compassionate than before. Her story teaches us that adversity is not our enemy but our most honest mirror.",
    }
    S[(5,1)] = {
        "korean": (
            "역경 이야기가 계속돼요.<br>"
            "사라 주변의 다른 사람들도 역경에 반응했어요.<br>"
            "민친 선생님은 역경에 더 비열해졌어요.<br>"
            "하지만 사라는 역경에 더 강해졌어요.<br><br>"
            "같은 어려움이라도 사람마다 반응이 달라요.<br>"
            "어떤 사람은 어려움에 화를 내고 다른 사람을 탓해요.<br>"
            "하지만 어떤 사람은 어려움을 통해 성장해요.<br>"
            "사라는 후자의 사람이었어요.<br>"
            "역경은 사라의 숨겨진 용기를 끌어냈어요.<br>"
            "어려움 속에서 사라는 더 깊은 사람이 되었어요.<br>"
            "역경은 사라를 더 완전한 사람으로 만들었어요.<br>"
            "<strong>같은 역경이라도 반응에 따라 결과가 달라져요.</strong>"
        ),
        "a1_html": "Some people get angry in hard times.<br>Sara got stronger instead.<br>She grew from her problems.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Some people get angry in hard times. Sara got stronger instead. She grew from her problems. __KEY__",
        "a2_html": "Miss Minchin became meaner when times were tough.<br>But Sara became stronger when facing the same difficulties.<br>The same adversity brought out different things in different people.<br>Sara chose to grow through her suffering instead of giving up.<br><span class=\"hl\">__KEY__</span><br>Her response to adversity defined who she became.",
        "a2_tts": "Miss Minchin became meaner when times were tough. But Sara became stronger when facing the same difficulties. The same adversity brought out different things in different people. Sara chose to grow through her suffering instead of giving up. __KEY__ Her response to adversity defined who she became.",
        "b1_html": "The same difficult circumstances affected different characters in very different ways.<br>Miss Minchin became cruel and bitter, using her power to hurt those weaker than herself.<br>However, Sara responded to the exact same adversity with grace, courage, and compassion.<br>This contrast reveals a profound truth about human nature and our choices.<br><span class=\"hl\">__KEY__</span><br>Because we cannot control what happens to us, our only true power lies in how we respond.<br>Although both Sara and Miss Minchin faced hardships, only Sara grew stronger through them.<br>The difference was not in their circumstances but in the character they chose to develop.",
        "b1_tts": "The same difficult circumstances affected different characters in very different ways. Miss Minchin became cruel and bitter, using her power to hurt those weaker than herself. However, Sara responded to the exact same adversity with grace, courage, and compassion. This contrast reveals a profound truth about human nature and our choices. __KEY__ Because we cannot control what happens to us, our only true power lies in how we respond. Although both Sara and Miss Minchin faced hardships, only Sara grew stronger through them. The difference was not in their circumstances but in the character they chose to develop.",
    }
    S[(5,2)] = {
        "korean": (
            "역경 주제의 마지막 이야기예요.<br>"
            "사라의 역경은 결국 끝이 났어요.<br>"
            "아버지의 친구가 사라를 찾아왔어요.<br>"
            "사라는 다시 부유해졌어요.<br><br>"
            "하지만 중요한 건 부가 돌아온 것이 아니에요.<br>"
            "역경을 통해 사라가 더 강한 사람이 되었다는 거예요.<br>"
            "역경 전의 사라도 좋은 아이었지만,<br>"
            "역경 후의 사라는 위대한 사람이었어요.<br>"
            "고통을 아는 사람만이 진정으로 공감할 수 있어요.<br>"
            "사라의 역경은 그녀에게 깊은 공감 능력을 주었어요.<br>"
            "역경은 끝이 아니라 더 나은 시작이에요.<br>"
            "<strong>역경이 사라를 무너뜨린 것이 아니라 더 강하게 만들었어요.</strong>"
        ),
        "a1_html": "Sara's hard times ended at last.<br>She became rich again.<br>But she was a better person now.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara's hard times ended at last. She became rich again. But she was a better person now. __KEY__",
        "a2_html": "Sara's father's friend found her and brought her wealth back.<br>But Sara was no longer the same girl she was before.<br>Adversity had made her wiser, kinder, and more compassionate.<br>She understood suffering in a way she never could before.<br><span class=\"hl\">__KEY__</span><br>Her character, forged in difficulty, was now unbreakable.",
        "a2_tts": "Sara's father's friend found her and brought her wealth back. But Sara was no longer the same girl she was before. Adversity had made her wiser, kinder, and more compassionate. She understood suffering in a way she never could before. __KEY__ Her character, forged in difficulty, was now unbreakable.",
        "b1_html": "When Sara's fortune was finally restored, everyone expected her to celebrate.<br>But the greatest change was not in her bank account — it was in her character.<br>The adversity she endured had forged her into a person of extraordinary depth and empathy.<br>However, Sara did not wish the hard times had never happened.<br><span class=\"hl\">__KEY__</span><br>Because suffering taught her to truly understand others' pain, she became more compassionate.<br>Although she would not have chosen adversity, she recognized the wisdom it gave her.<br>Sara's journey proves that our greatest growth often comes from our hardest moments.",
        "b1_tts": "When Sara's fortune was finally restored, everyone expected her to celebrate. But the greatest change was not in her bank account — it was in her character. The adversity she endured had forged her into a person of extraordinary depth and empathy. However, Sara did not wish the hard times had never happened. __KEY__ Because suffering taught her to truly understand others' pain, she became more compassionate. Although she would not have chosen adversity, she recognized the wisdom it gave her. Sara's journey proves that our greatest growth often comes from our hardest moments.",
    }

    # W06 — integrity
    S[(6,0)] = {
        "korean": (
            "이번 주는 '진실됨'에 대해 이야기해요.<br>"
            "사라는 어떤 상황에서도 자신답게 행동했어요.<br>"
            "누가 보든 안 보든 항상 같은 사라였어요.<br>"
            "이것이 바로 진실됨, 즉 정직함이에요.<br><br>"
            "사라는 쉬운 길과 옳은 길 중 항상 옳은 길을 택했어요.<br>"
            "거짓말로 상황을 모면할 수도 있었지만 하지 않았어요.<br>"
            "사라에게는 자신의 원칙이 있었어요.<br>"
            "그 원칙은 어떤 압박에도 흔들리지 않았어요.<br>"
            "진실됨이란 편하지 않아도 옳은 일을 하는 거예요.<br>"
            "사라는 이 가치를 매일매일 실천했어요.<br>"
            "가장 잔인한 순간에도 자신을 배신하지 않았어요.<br>"
            "<strong>사라는 가장 힘든 순간에도 자신의 진실됨을 포기하지 않았어요.</strong>"
        ),
        "a1_html": "Sara always did the right thing.<br>She never told lies.<br>She was the same person always.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara always did the right thing. She never told lies. She was the same person always. __KEY__",
        "a2_html": "Sara chose the right path even when it was hard.<br>She could have lied to make her life easier.<br>But Sara believed in being true to herself always.<br>Her integrity meant doing right, whether anyone watched or not.<br><span class=\"hl\">__KEY__</span><br>Sara showed that integrity is the strongest form of courage.",
        "a2_tts": "Sara chose the right path even when it was hard. She could have lied to make her life easier. But Sara believed in being true to herself always. Her integrity meant doing right, whether anyone watched or not. __KEY__ Sara showed that integrity is the strongest form of courage.",
        "b1_html": "Sara faced countless moments where she could have compromised her principles to survive.<br>She could have lied, cheated, or been cruel to gain favor with Miss Minchin.<br>However, Sara chose integrity every single time, even when it cost her dearly.<br>Her consistency amazed everyone — she was the same person in public and in private.<br><span class=\"hl\">__KEY__</span><br>Because integrity means doing right regardless of consequences, it requires extraordinary courage.<br>Although easier paths were always available, Sara never once betrayed her values.<br>She proved that the most powerful strength comes from staying true to who you are.",
        "b1_tts": "Sara faced countless moments where she could have compromised her principles to survive. She could have lied, cheated, or been cruel to gain favor with Miss Minchin. However, Sara chose integrity every single time, even when it cost her dearly. Her consistency amazed everyone — she was the same person in public and in private. __KEY__ Because integrity means doing right regardless of consequences, it requires extraordinary courage. Although easier paths were always available, Sara never once betrayed her values. She proved that the most powerful strength comes from staying true to who you are.",
    }
    S[(6,1)] = {
        "korean": (
            "진실됨의 이야기가 계속돼요.<br>"
            "사라를 시험하는 순간이 있었어요.<br>"
            "민친 선생님이 사라에게 거짓말하라고 강요했어요.<br>"
            "사라가 복종하면 편한 생활을 줄 수 있다고 했어요.<br><br>"
            "하지만 사라는 거절했어요.<br>"
            "편한 삶보다 진실이 더 중요하다고 생각했어요.<br>"
            "이것은 매우 어려운 선택이었어요.<br>"
            "배고프고 추운데도 원칙을 지키다니요!<br>"
            "하지만 사라는 알고 있었어요.<br>"
            "한 번 진실을 포기하면 모든 것을 잃게 된다는 것을요.<br>"
            "진실됨은 사라의 마지막 보루였어요.<br>"
            "<strong>어떤 잔인한 상황에서도 사라는 자신을 배신하지 않았어요.</strong>"
        ),
        "a1_html": "Someone told Sara to lie.<br>Sara said no.<br>Truth was more important.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Someone told Sara to lie. Sara said no. Truth was more important. __KEY__",
        "a2_html": "Miss Minchin tried to make Sara tell a lie.<br>She promised Sara an easier life if she obeyed.<br>But Sara refused to trade her honesty for comfort.<br>She knew that once you give up truth, you lose yourself.<br><span class=\"hl\">__KEY__</span><br>Sara chose hardship with integrity over comfort with dishonesty.",
        "a2_tts": "Miss Minchin tried to make Sara tell a lie. She promised Sara an easier life if she obeyed. But Sara refused to trade her honesty for comfort. She knew that once you give up truth, you lose yourself. __KEY__ Sara chose hardship with integrity over comfort with dishonesty.",
        "b1_html": "The most difficult test of Sara's integrity came when Miss Minchin offered a deal.<br>If Sara would simply lie and do as she was told, her life could become much easier.<br>It was a tempting offer for a cold, hungry girl sleeping in an attic.<br>However, Sara understood that sacrificing integrity means losing everything that matters.<br><span class=\"hl\">__KEY__</span><br>Because once a person abandons their principles, they can never fully trust themselves again.<br>Although the immediate cost of honesty was high, the long-term cost of dishonesty would be higher.<br>Sara chose the harder path because she knew her sense of self was worth more than any comfort.",
        "b1_tts": "The most difficult test of Sara's integrity came when Miss Minchin offered a deal. If Sara would simply lie and do as she was told, her life could become much easier. It was a tempting offer for a cold, hungry girl sleeping in an attic. However, Sara understood that sacrificing integrity means losing everything that matters. __KEY__ Because once a person abandons their principles, they can never fully trust themselves again. Although the immediate cost of honesty was high, the long-term cost of dishonesty would be higher. Sara chose the harder path because she knew her sense of self was worth more than any comfort.",
    }
    S[(6,2)] = {
        "korean": (
            "진실됨 주제의 마지막 이야기예요.<br>"
            "사라의 진실됨은 결국 인정받았어요.<br>"
            "주변 사람들이 사라의 변하지 않는 모습에 감동했어요.<br>"
            "진실된 사람은 결국 존경을 받게 돼요.<br><br>"
            "민친 선생님은 사라를 꺾으려 했지만 실패했어요.<br>"
            "사라의 진실됨은 그 어떤 외부 힘보다 강했어요.<br>"
            "왜냐하면 진실됨은 마음의 뿌리이기 때문이에요.<br>"
            "뿌리가 강한 나무는 폭풍에도 쓰러지지 않아요.<br>"
            "사라는 그런 강한 뿌리를 가진 사람이었어요.<br>"
            "진실됨이란 결국 자기 자신과의 약속이에요.<br>"
            "그 약속을 지키는 것이 가장 중요한 일이에요.<br>"
            "<strong>사라의 진실됨은 어떤 외부의 힘도 꺾을 수 없었어요.</strong>"
        ),
        "a1_html": "People saw Sara never changed.<br>They respected her for it.<br>Integrity is the strongest power.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "People saw Sara never changed. They respected her for it. Integrity is the strongest power. __KEY__",
        "a2_html": "Everyone noticed that Sara stayed the same no matter what happened.<br>Even Miss Minchin could not break Sara's spirit or principles.<br>Sara's integrity was like a deep root that no storm could uproot.<br>People began to respect her quiet, unshakable strength.<br><span class=\"hl\">__KEY__</span><br>Sara proved that true integrity cannot be defeated by outside forces.",
        "a2_tts": "Everyone noticed that Sara stayed the same no matter what happened. Even Miss Minchin could not break Sara's spirit or principles. Sara's integrity was like a deep root that no storm could uproot. People began to respect her quiet, unshakable strength. __KEY__ Sara proved that true integrity cannot be defeated by outside forces.",
        "b1_html": "Over time, Sara's unwavering integrity earned her the deepest respect from everyone around her.<br>Miss Minchin had used every weapon in her power to break Sara's spirit, but she failed completely.<br>Sara's integrity was rooted so deeply in her character that no external force could shake it.<br>However, the greatest victory was not over Miss Minchin but over Sara's own doubts and fears.<br><span class=\"hl\">__KEY__</span><br>Because integrity is a promise we make to ourselves, it is the strongest foundation we can build.<br>Although the world constantly tests our principles, those who stay true emerge victorious.<br>Sara's story is proof that a person of integrity cannot be defeated by any circumstance.",
        "b1_tts": "Over time, Sara's unwavering integrity earned her the deepest respect from everyone around her. Miss Minchin had used every weapon in her power to break Sara's spirit, but she failed completely. Sara's integrity was rooted so deeply in her character that no external force could shake it. However, the greatest victory was not over Miss Minchin but over Sara's own doubts and fears. __KEY__ Because integrity is a promise we make to ourselves, it is the strongest foundation we can build. Although the world constantly tests our principles, those who stay true emerge victorious. Sara's story is proof that a person of integrity cannot be defeated by any circumstance.",
    }

    # W07 — kindness choice
    S[(7,0)] = {
        "korean": (
            "이번 주는 친절이 선택임을 배워요.<br>"
            "사라는 매일 아침 친절을 선택했어요.<br>"
            "화를 낼 수도 있었지만 친절을 택했어요.<br>"
            "원망할 수도 있었지만 이해를 택했어요.<br><br>"
            "친절은 기분이 아니라 결정이에요.<br>"
            "기분이 좋을 때만 친절한 건 쉬워요.<br>"
            "하지만 힘들 때도 친절한 건 어려워요.<br>"
            "사라는 매일 그 어려운 선택을 했어요.<br>"
            "이것이 사라를 진정한 공주로 만들었어요.<br>"
            "친절은 우연이 아니라 의도적인 선택이에요.<br>"
            "우리도 매일 그 선택을 할 수 있어요.<br>"
            "<strong>친절은 항상 우리가 의식적으로 하는 선택이에요.</strong>"
        ),
        "a1_html": "Sara chose to be kind every day.<br>Even when she was sad or angry.<br>Kindness is a choice we make.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara chose to be kind every day. Even when she was sad or angry. Kindness is a choice we make. __KEY__",
        "a2_html": "Every morning Sara woke up and decided to be kind.<br>She could have been angry at the world for her suffering.<br>But she chose kindness over bitterness every single time.<br>Being kind when life is hard is the bravest choice of all.<br><span class=\"hl\">__KEY__</span><br>Sara's daily choice of kindness is what made her truly special.",
        "a2_tts": "Every morning Sara woke up and decided to be kind. She could have been angry at the world for her suffering. But she chose kindness over bitterness every single time. Being kind when life is hard is the bravest choice of all. __KEY__ Sara's daily choice of kindness is what made her truly special.",
        "b1_html": "What made Sara extraordinary was not that kindness came naturally to her, but that she chose it deliberately.<br>Every morning in her cold attic, she made a conscious decision to face the day with grace.<br>She could have given in to anger, resentment, or self-pity — all perfectly understandable reactions.<br>However, Sara believed that kindness is not a feeling but a choice we make every single day.<br><span class=\"hl\">__KEY__</span><br>Because choosing kindness in difficult times requires far more courage than giving in to anger.<br>Although no one would have blamed Sara for being bitter, she refused to let hardship change her heart.<br>Her example shows us that we always have the power to choose how we respond to life.",
        "b1_tts": "What made Sara extraordinary was not that kindness came naturally to her, but that she chose it deliberately. Every morning in her cold attic, she made a conscious decision to face the day with grace. She could have given in to anger, resentment, or self-pity — all perfectly understandable reactions. However, Sara believed that kindness is not a feeling but a choice we make every single day. __KEY__ Because choosing kindness in difficult times requires far more courage than giving in to anger. Although no one would have blamed Sara for being bitter, she refused to let hardship change her heart. Her example shows us that we always have the power to choose how we respond to life.",
    }
    S[(7,1)] = {
        "korean": (
            "친절한 선택의 이야기가 계속돼요.<br>"
            "사라가 친절을 선택하자 놀라운 일이 일어났어요.<br>"
            "베키도 사라처럼 친절해지기 시작했어요.<br>"
            "어린 아이들도 사라를 따라 친절해졌어요.<br><br>"
            "친절은 전염되는 거예요!<br>"
            "한 사람의 친절한 선택이 다른 사람에게 퍼져요.<br>"
            "사라의 친절은 학교 전체를 바꾸기 시작했어요.<br>"
            "차가운 학교에 따뜻한 바람이 불었어요.<br>"
            "이것이 친절의 힘이에요.<br>"
            "작은 친절 하나가 세상을 바꿀 수 있어요.<br>"
            "사라는 그것을 매일 증명했어요.<br>"
            "<strong>사라가 대우받는 것에 상관없이 매일 친절을 선택했어요.</strong>"
        ),
        "a1_html": "Sara was kind, so others were kind too.<br>Kindness spreads from person to person.<br>One act of kindness changes everything.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara was kind, so others were kind too. Kindness spreads from person to person. One act of kindness changes everything. __KEY__",
        "a2_html": "When Sara chose kindness, something amazing happened.<br>Becky started being kinder to other servants too.<br>The younger children followed Sara's example of kindness.<br>Kindness spread through the school like warmth from a fire.<br><span class=\"hl\">__KEY__</span><br>Sara showed that one person's kindness can change a whole community.",
        "a2_tts": "When Sara chose kindness, something amazing happened. Becky started being kinder to other servants too. The younger children followed Sara's example of kindness. Kindness spread through the school like warmth from a fire. __KEY__ Sara showed that one person's kindness can change a whole community.",
        "b1_html": "Sara's deliberate choice of kindness created a ripple effect throughout the entire school.<br>Becky, inspired by Sara's example, began treating other servants with greater compassion.<br>Even the younger students started showing kindness to one another, following Sara's lead.<br>However, none of this would have happened if Sara had given up and chosen bitterness instead.<br><span class=\"hl\">__KEY__</span><br>Because kindness is contagious, one person's consistent choice can transform an entire community.<br>Although Sara was just one girl in a cruel environment, her kindness warmed every heart around her.<br>She proved that we do not need power or wealth to change the world — just consistent kindness.",
        "b1_tts": "Sara's deliberate choice of kindness created a ripple effect throughout the entire school. Becky, inspired by Sara's example, began treating other servants with greater compassion. Even the younger students started showing kindness to one another, following Sara's lead. However, none of this would have happened if Sara had given up and chosen bitterness instead. __KEY__ Because kindness is contagious, one person's consistent choice can transform an entire community. Although Sara was just one girl in a cruel environment, her kindness warmed every heart around her. She proved that we do not need power or wealth to change the world — just consistent kindness.",
    }
    S[(7,2)] = {
        "korean": (
            "친절한 선택 주제의 마지막 이야기예요.<br>"
            "사라의 이야기에서 가장 감동적인 장면이에요.<br>"
            "사라는 자신을 괴롭힌 아이에게도 친절했어요.<br>"
            "그 아이가 아플 때 사라가 돌봐주었어요.<br><br>"
            "원수에게 친절한 것은 가장 어려운 선택이에요.<br>"
            "하지만 사라는 그것을 해냈어요.<br>"
            "왜냐하면 사라에게 친절은 조건이 아니니까요.<br>"
            "상대가 누구든, 어떤 상황이든 친절할 수 있어요.<br>"
            "이것이 사라가 가르쳐 준 가장 큰 교훈이에요.<br>"
            "친절은 매일, 매 순간 우리가 하는 선택이에요.<br>"
            "그리고 그 선택이 우리를 정의해요.<br>"
            "<strong>사라는 친절이 매일의 의식적인 선택임을 증명했어요.</strong>"
        ),
        "a1_html": "Sara was kind even to those who hurt her.<br>She helped a sick girl who was mean.<br>That is the hardest kind of kindness.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara was kind even to those who hurt her. She helped a sick girl who was mean. That is the hardest kind of kindness. __KEY__",
        "a2_html": "The most remarkable moment was when Sara helped a girl who had bullied her.<br>When that girl became sick, Sara took care of her without hesitation.<br>Being kind to someone who hurt you is the ultimate test of character.<br>Sara passed that test because kindness was her deliberate daily choice.<br><span class=\"hl\">__KEY__</span><br>She proved that true kindness has no conditions or exceptions.",
        "a2_tts": "The most remarkable moment was when Sara helped a girl who had bullied her. When that girl became sick, Sara took care of her without hesitation. Being kind to someone who hurt you is the ultimate test of character. Sara passed that test because kindness was her deliberate daily choice. __KEY__ She proved that true kindness has no conditions or exceptions.",
        "b1_html": "Perhaps the most powerful moment in Sara's story was when she cared for a girl who had been cruel to her.<br>This girl had mocked Sara's poverty and called her terrible names for months.<br>When the girl fell ill, everyone expected Sara to ignore her or feel satisfied.<br>However, Sara chose to nurse the girl back to health with genuine compassion and warmth.<br><span class=\"hl\">__KEY__</span><br>Because Sara understood that kindness chosen in the hardest moments has the deepest meaning.<br>Although she had every reason to turn away, she chose compassion over revenge.<br>Sara's final lesson is this: our daily, deliberate choice of kindness defines who we truly are.",
        "b1_tts": "Perhaps the most powerful moment in Sara's story was when she cared for a girl who had been cruel to her. This girl had mocked Sara's poverty and called her terrible names for months. When the girl fell ill, everyone expected Sara to ignore her or feel satisfied. However, Sara chose to nurse the girl back to health with genuine compassion and warmth. __KEY__ Because Sara understood that kindness chosen in the hardest moments has the deepest meaning. Although she had every reason to turn away, she chose compassion over revenge. Sara's final lesson is this: our daily, deliberate choice of kindness defines who we truly are.",
    }

    # W08 — privilege
    S[(8,0)] = {
        "korean": (
            "이번 주는 '특권'에 대해 생각해 봐요.<br>"
            "사라는 처음에 큰 특권을 누렸어요.<br>"
            "부유한 아버지, 좋은 학교, 아름다운 옷.<br>"
            "하지만 그 모든 것이 하루아침에 사라졌어요.<br><br>"
            "특권이란 영원하지 않아요.<br>"
            "오늘 가진 것이 내일 없어질 수 있어요.<br>"
            "그렇기 때문에 특권으로 자신을 정의하면 안 돼요.<br>"
            "특권이 사라지면 자신도 사라지니까요.<br>"
            "사라는 특권이 아닌 내면으로 자신을 정의했어요.<br>"
            "그래서 특권이 사라져도 사라 자신은 변하지 않았어요.<br>"
            "이것이 소공녀의 핵심 메시지예요.<br>"
            "<strong>특권은 영원하지 않아요.</strong>"
        ),
        "a1_html": "Sara was rich, then she was poor.<br>Money can come and go.<br>We should not depend on it.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara was rich, then she was poor. Money can come and go. We should not depend on it. __KEY__",
        "a2_html": "Sara once had every privilege a child could wish for.<br>Beautiful clothes, delicious food, and a grand room were hers.<br>But when her father died, all those privileges vanished overnight.<br>Sara learned that privilege is like clouds — always changing.<br><span class=\"hl\">__KEY__</span><br>Only what is inside us remains when everything else is gone.",
        "a2_tts": "Sara once had every privilege a child could wish for. Beautiful clothes, delicious food, and a grand room were hers. But when her father died, all those privileges vanished overnight. Sara learned that privilege is like clouds — always changing. __KEY__ Only what is inside us remains when everything else is gone.",
        "b1_html": "Sara's story is a powerful lesson about the temporary nature of privilege and wealth.<br>She went from the richest student to the poorest servant in a single day.<br>The children who envied her privileges quickly forgot her when those privileges disappeared.<br>However, Sara had built her identity on something deeper than wealth or status.<br><span class=\"hl\">__KEY__</span><br>Because she never defined herself by her possessions, losing them did not destroy her sense of self.<br>Although privilege can vanish in an instant, character developed through hardship lasts forever.<br>Sara's journey reminds us to build our lives on who we are, not on what we have.",
        "b1_tts": "Sara's story is a powerful lesson about the temporary nature of privilege and wealth. She went from the richest student to the poorest servant in a single day. The children who envied her privileges quickly forgot her when those privileges disappeared. However, Sara had built her identity on something deeper than wealth or status. __KEY__ Because she never defined herself by her possessions, losing them did not destroy her sense of self. Although privilege can vanish in an instant, character developed through hardship lasts forever. Sara's journey reminds us to build our lives on who we are, not on what we have.",
    }
    S[(8,1)] = {
        "korean": (
            "특권 이야기가 계속돼요.<br>"
            "민친 선생님은 특권으로 자신을 정의한 사람이에요.<br>"
            "돈과 지위가 곧 자신의 가치라고 믿었어요.<br>"
            "그래서 부자에게는 굽실하고 가난한 사람은 무시했어요.<br><br>"
            "이런 사람은 특권이 사라지면 무너져요.<br>"
            "자신의 가치가 외부에 있기 때문이에요.<br>"
            "하지만 사라는 달랐어요.<br>"
            "사라의 가치는 내면에 있었어요.<br>"
            "특권이 정체성을 정의하게 놔두면 안 돼요.<br>"
            "특권은 도구일 뿐, 나 자신은 아니에요.<br>"
            "이것을 깨달은 사라는 자유로운 사람이었어요.<br>"
            "<strong>특권을 자신의 정체성으로 삼으면 안 돼요.</strong>"
        ),
        "a1_html": "Miss Minchin valued only money.<br>When people lost money, she was cruel.<br>That is not a good way to live.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Miss Minchin valued only money. When people lost money, she was cruel. That is not a good way to live. __KEY__",
        "a2_html": "Miss Minchin defined herself by money and status.<br>She bowed to the rich and ignored the poor completely.<br>When Sara lost her wealth, Miss Minchin showed her true ugly character.<br>Sara was different — her identity came from her heart, not her wallet.<br><span class=\"hl\">__KEY__</span><br>Sara showed that letting privilege define you is a dangerous trap.",
        "a2_tts": "Miss Minchin defined herself by money and status. She bowed to the rich and ignored the poor completely. When Sara lost her wealth, Miss Minchin showed her true ugly character. Sara was different — her identity came from her heart, not her wallet. __KEY__ Sara showed that letting privilege define you is a dangerous trap.",
        "b1_html": "Miss Minchin represents the danger of building your entire identity around privilege.<br>She measured people's worth by their wealth and treated them accordingly.<br>When Sara was rich, Miss Minchin showered her with attention, but discarded her when the money vanished.<br>However, Sara's story reveals the emptiness of Miss Minchin's values compared to Sara's inner strength.<br><span class=\"hl\">__KEY__</span><br>Because those who define themselves by privilege become hollow when it disappears.<br>Although privilege can open doors, it should never become the foundation of our identity.<br>Sara understood that who we are matters infinitely more than what we have.",
        "b1_tts": "Miss Minchin represents the danger of building your entire identity around privilege. She measured people's worth by their wealth and treated them accordingly. When Sara was rich, Miss Minchin showered her with attention, but discarded her when the money vanished. However, Sara's story reveals the emptiness of Miss Minchin's values compared to Sara's inner strength. __KEY__ Because those who define themselves by privilege become hollow when it disappears. Although privilege can open doors, it should never become the foundation of our identity. Sara understood that who we are matters infinitely more than what we have.",
    }
    S[(8,2)] = {
        "korean": (
            "소공녀의 마지막 이야기예요!<br>"
            "사라의 이야기를 정리해 볼까요?<br>"
            "사라는 공주에서 하녀가 되었다가 다시 부유해졌어요.<br>"
            "하지만 사라에게 가장 중요한 변화는 외부가 아니었어요.<br><br>"
            "사라는 역경을 통해 더 깊은 사람이 되었어요.<br>"
            "특권이 사라져도 변하지 않는 자신을 발견했어요.<br>"
            "품위, 친절, 상상력, 진실됨 — 이 모든 것은 내면의 보물이에요.<br>"
            "이 보물들은 어떤 외부의 힘도 빼앗을 수 없어요.<br>"
            "소공녀의 가장 큰 교훈은 이거예요.<br>"
            "특권으로 자신을 정의하면 특권과 함께 사라져요.<br>"
            "하지만 내면으로 자신을 정의하면 영원해요.<br>"
            "<strong>특권으로 자신을 정의하는 사람은 특권이 사라지면 모든 것을 잃어요.</strong>"
        ),
        "a1_html": "Sara's story has a big lesson.<br>Money comes and goes.<br>But who you are inside stays forever.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Sara's story has a big lesson. Money comes and goes. But who you are inside stays forever. __KEY__",
        "a2_html": "A Little Princess teaches us the most important lesson about life.<br>Sara went through poverty, cruelty, and loneliness.<br>But she never lost her dignity, kindness, or imagination.<br>These inner treasures are worth more than any privilege.<br><span class=\"hl\">__KEY__</span><br>We should build our identity on character, not on what we own.",
        "a2_tts": "A Little Princess teaches us the most important lesson about life. Sara went through poverty, cruelty, and loneliness. But she never lost her dignity, kindness, or imagination. These inner treasures are worth more than any privilege. __KEY__ We should build our identity on character, not on what we own.",
        "b1_html": "A Little Princess is ultimately a story about what truly defines a person's worth.<br>Sara experienced the highest privilege and the deepest poverty in her young life.<br>Through it all, she discovered that her real treasures were dignity, kindness, and imagination.<br>However, the story's sharpest warning is about those who build their identity on privilege alone.<br><span class=\"hl\">__KEY__</span><br>Because privilege is always temporary, those who depend on it are building on sand.<br>Although Sara's wealth returned, it was her character that made her story timeless.<br>The final message of A Little Princess is clear: invest in who you are, not in what you have.",
        "b1_tts": "A Little Princess is ultimately a story about what truly defines a person's worth. Sara experienced the highest privilege and the deepest poverty in her young life. Through it all, she discovered that her real treasures were dignity, kindness, and imagination. However, the story's sharpest warning is about those who build their identity on privilege alone. __KEY__ Because privilege is always temporary, those who depend on it are building on sand. Although Sara's wealth returned, it was her character that made her story timeless. The final message of A Little Princess is clear: invest in who you are, not in what you have.",
    }

    # ══════════════════════════════════════════
    # FIVE CHILDREN AND IT (W09-W16)
    # ══════════════════════════════════════════

    # W09 — creature
    S[(9,0)] = {
        "korean": (
            "새로운 책 '다섯 아이와 모래 요정'을 시작해요! 🧞<br>"
            "다섯 남매가 시골 집으로 이사를 왔어요.<br>"
            "정원의 모래밭에서 놀다가 이상한 것을 발견했어요.<br>"
            "모래 속에 묻혀 있던 신비한 생물이었어요!<br><br>"
            "그 생물의 이름은 '사미드'예요.<br>"
            "사미드는 수천 년 된 모래 요정이었어요.<br>"
            "사미드는 하루에 한 가지 소원을 들어줄 수 있었어요.<br>"
            "하지만 그 소원은 해가 지면 사라져요.<br>"
            "아이들은 너무 신이 났어요!<br>"
            "무엇이든 소원을 빌 수 있다니 꿈만 같았어요.<br>"
            "하지만 소원에는 생각지 못한 결과가 따른다는 걸 곧 알게 돼요.<br>"
            "<strong>아이들은 정원 모래밭에서 신비한 생물을 발견했어요!</strong>"
        ),
        "a1_html": "Five children found something in the sand. 🧞<br>It was a magical creature called the Psammead.<br>It could grant one wish each day.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "Five children found something in the sand. It was a magical creature called the Psammead. It could grant one wish each day. __KEY__",
        "a2_html": "Five brothers and sisters moved to a house in the country.<br>While playing in the garden, they dug up a strange creature.<br>The Psammead was a sand fairy, thousands of years old.<br>It could grant one wish per day, but the wish vanished at sunset.<br><span class=\"hl\">__KEY__</span><br>The children were thrilled, not knowing the trouble wishes would bring.",
        "a2_tts": "Five brothers and sisters moved to a house in the country. While playing in the garden, they dug up a strange creature. The Psammead was a sand fairy, thousands of years old. It could grant one wish per day, but the wish vanished at sunset. __KEY__ The children were thrilled, not knowing the trouble wishes would bring.",
        "b1_html": "When five siblings moved to their new country house, they never expected to find magic in the garden.<br>Digging in the sand pit, they uncovered a strange creature with bat-like ears and a round furry body.<br>The Psammead, an ancient sand fairy, had been buried there for thousands of years.<br>It grudgingly agreed to grant them one wish per day, though it warned them to be careful.<br><span class=\"hl\">__KEY__</span><br>However, the children were too excited to listen to the fairy's warnings about consequences.<br>Because they did not yet understand the nature of wishes, they rushed in without thinking.<br>Although they had found something wonderful, they would soon learn that magic has a price.",
        "b1_tts": "When five siblings moved to their new country house, they never expected to find magic in the garden. Digging in the sand pit, they uncovered a strange creature with bat-like ears and a round furry body. The Psammead, an ancient sand fairy, had been buried there for thousands of years. It grudgingly agreed to grant them one wish per day, though it warned them to be careful. __KEY__ However, the children were too excited to listen to the fairy's warnings about consequences. Because they did not yet understand the nature of wishes, they rushed in without thinking. Although they had found something wonderful, they would soon learn that magic has a price.",
    }
    S[(9,1)] = {
        "korean": (
            "사미드와의 첫 만남이 계속돼요.<br>"
            "사미드는 매우 까칠한 성격이었어요.<br>"
            "소원을 들어주는 게 귀찮다고 불평했어요.<br>"
            "하지만 아이들의 열정에 어쩔 수 없이 응했어요.<br><br>"
            "사미드는 아이들에게 경고했어요.<br>"
            "'소원을 빌 때 조심해라' 라고요.<br>"
            "하지만 아이들은 너무 흥분해서 귀담아 듣지 않았어요.<br>"
            "첫 번째 소원은 무엇이었을까요?<br>"
            "아이들은 '예뻐지고 싶다'고 소원을 빌었어요.<br>"
            "하지만 너무 예뻐져서 아무도 알아보지 못했어요!<br>"
            "소원이 생각대로 되지 않는다는 첫 번째 교훈을 배웠어요.<br>"
            "<strong>모래 속에서 발견한 사미드는 까칠하지만 소원을 들어주었어요.</strong>"
        ),
        "a1_html": "The Psammead was grumpy.<br>The children wished to be beautiful.<br>But nobody recognized them!<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "The Psammead was grumpy. The children wished to be beautiful. But nobody recognized them! __KEY__",
        "a2_html": "The Psammead warned the children to be careful with wishes.<br>But they were too excited to listen carefully.<br>Their first wish was to become beautiful, but it backfired terribly.<br>They became so beautiful that nobody could recognize them!<br><span class=\"hl\">__KEY__</span><br>This was their first lesson that wishes rarely work as expected.",
        "a2_tts": "The Psammead warned the children to be careful with wishes. But they were too excited to listen carefully. Their first wish was to become beautiful, but it backfired terribly. They became so beautiful that nobody could recognize them! __KEY__ This was their first lesson that wishes rarely work as expected.",
        "b1_html": "The Psammead was an irritable creature that complained about granting wishes constantly.<br>Despite its warnings, the children eagerly made their first wish — to be extraordinarily beautiful.<br>The wish came true instantly, but the result was nothing like they imagined.<br>They became so impossibly beautiful that their own family could not recognize them!<br><span class=\"hl\">__KEY__</span><br>However, this humorous disaster taught them their first valuable lesson about wishes.<br>Because the Psammead granted wishes literally, the children needed to think more carefully.<br>Although the wish wore off at sunset, the lesson stayed with them much longer.",
        "b1_tts": "The Psammead was an irritable creature that complained about granting wishes constantly. Despite its warnings, the children eagerly made their first wish — to be extraordinarily beautiful. The wish came true instantly, but the result was nothing like they imagined. They became so impossibly beautiful that their own family could not recognize them! __KEY__ However, this humorous disaster taught them their first valuable lesson about wishes. Because the Psammead granted wishes literally, the children needed to think more carefully. Although the wish wore off at sunset, the lesson stayed with them much longer.",
    }
    S[(9,2)] = {
        "korean": (
            "첫 주의 마지막 이야기예요.<br>"
            "아이들은 첫 번째 소원의 실패에서 배웠을까요?<br>"
            "사실은... 그렇지 않았어요!<br>"
            "아이들은 여전히 흥분되어 있었어요.<br><br>"
            "사미드를 발견한 것은 정말 놀라운 일이었어요.<br>"
            "하루에 한 가지 소원을 빌 수 있다니!<br>"
            "하지만 사미드는 계속 경고했어요.<br>"
            "'소원을 정확하게 말해야 한다'고요.<br>"
            "정확하지 않은 소원은 엉뚱한 결과를 만들어요.<br>"
            "아이들은 곧 더 많은 실수를 하게 될 거예요.<br>"
            "하지만 그 실수들이 중요한 교훈이 될 거예요.<br>"
            "<strong>사미드라는 모래 요정은 아이들의 삶을 완전히 바꿀 거예요.</strong>"
        ),
        "a1_html": "The children did not learn their lesson yet.<br>They still wanted more wishes.<br>The Psammead said to be exact.<br><span class=\"hl\">__KEY__</span>",
        "a1_tts": "The children did not learn their lesson yet. They still wanted more wishes. The Psammead said to be exact. __KEY__",
        "a2_html": "Even after the beauty disaster, the children wanted more wishes.<br>The Psammead reminded them to say wishes very exactly.<br>A wish that is not precise will have unexpected results.<br>The children had so much to learn about wishes and consequences.<br><span class=\"hl\">__KEY__</span><br>Their adventures with the Psammead were only just beginning.",
        "a2_tts": "Even after the beauty disaster, the children wanted more wishes. The Psammead reminded them to say wishes very exactly. A wish that is not precise will have unexpected results. The children had so much to learn about wishes and consequences. __KEY__ Their adventures with the Psammead were only just beginning.",
        "b1_html": "Despite the embarrassing beauty incident, the children could not resist the temptation of more wishes.<br>The Psammead, ancient and wise, had seen countless humans make the same mistakes over centuries.<br>It tried to explain that wishes must be worded with extreme precision or they will go wrong.<br>However, the children were young and impatient, eager for the next exciting wish.<br><span class=\"hl\">__KEY__</span><br>Because the Psammead lived beneath their garden, this magical encounter would change everything.<br>Although each failed wish brought frustration, it also brought wisdom they could not gain any other way.<br>The story of the five children and their strange sand fairy was destined to teach them about life itself.",
        "b1_tts": "Despite the embarrassing beauty incident, the children could not resist the temptation of more wishes. The Psammead, ancient and wise, had seen countless humans make the same mistakes over centuries. It tried to explain that wishes must be worded with extreme precision or they will go wrong. However, the children were young and impatient, eager for the next exciting wish. __KEY__ Because the Psammead lived beneath their garden, this magical encounter would change everything. Although each failed wish brought frustration, it also brought wisdom they could not gain any other way. The story of the five children and their strange sand fairy was destined to teach them about life itself.",
    }

    # For W10-W36, build remaining stories using the same pattern
    # Each week has 3 days (0,1,2)

    week_data = {
        10: ("consequences", "다섯 아이와 모래 요정", "Five Children and It", "every wish had consequences", "소원을 빌었지만 예상치 못한 결과가 따랐어요", "아이들이 부자가 되고 싶다고 빌었지만 아무도 그 돈을 받아주지 않았어요", "아이들이 날고 싶다고 빌었지만 교회 꼭대기에 갇히게 되었어요"),
        11: ("careful wishes", "다섯 아이와 모래 요정", "Five Children and It", "be careful what you wish for", "소원의 정확한 의미를 생각해야 해요", "글자 그대로 이루어지는 소원은 우리가 진정으로 원하는 것과 다를 수 있어요", "아이들은 소원을 빌기 전에 결과를 생각해야 한다는 것을 배웠어요"),
        12: ("wisdom", "다섯 아이와 모래 요정", "Five Children and It", "imagination needs wisdom", "상상력만으로는 부족하고 지혜가 필요해요", "소원이 혼란을 가져온 이유는 아이들에게 선견지명이 없었기 때문이에요", "지혜 없는 상상력은 위험할 수 있어요"),
        13: ("real happiness", "다섯 아이와 모래 요정", "Five Children and It", "real happiness cannot be wished for", "진정한 행복은 소원으로 얻을 수 없어요", "행복은 노력과 사랑과 연결을 통해 만들어야 해요", "아이들은 가장 좋은 날이 소원 없는 날이었다는 것을 깨달았어요"),
        14: ("mistakes", "다섯 아이와 모래 요정", "Five Children and It", "they learned from mistakes", "실수에서 소중한 교훈을 얻었어요", "모든 실수에는 기꺼이 찾으면 가치있는 교훈이 있어요", "아이들은 각 실수를 통해 더 현명해졌어요"),
        15: ("responsibility", "다섯 아이와 모래 요정", "Five Children and It", "power requires responsibility", "힘에는 책임이 따라요", "마법의 힘이라도 현명하게 사용해야 할 책임이 있어요", "아이들은 소원의 힘이 신중하게 다루어야 한다는 것을 배웠어요"),
        16: ("gifts alone", "다섯 아이와 모래 요정", "Five Children and It", "some gifts are better left alone", "어떤 선물은 사용하지 않는 것이 현명해요", "힘을 사용하지 않을 때를 아는 것이 지혜예요", "아이들은 사미드에게 작별인사를 하며 소원보다 중요한 것을 배웠어요"),
        17: ("law", "정글북", "The Jungle Book", "the jungle has its own law", "정글에는 모든 생물이 따르는 법칙이 있어요", "이 법칙을 어기는 자는 공동체에서 추방당해요", "모글리는 정글의 법칙을 배우며 성장했어요"),
        18: ("belonging", "정글북", "The Jungle Book", "law creates belonging", "공유된 법칙이 소속감을 만들어요", "법칙 없이는 혼돈만 있을 뿐이에요", "모글리는 늑대 무리 안에서 법칙을 통해 가족을 찾았어요"),
        19: ("nowhere", "정글북", "The Jungle Book", "Mowgli belonged nowhere", "모글리는 두 세계 어디에도 완전히 속하지 못했어요", "정글에서는 인간이라 하고 마을에서는 야수라 했어요", "두 세계 사이에 있다는 것은 외롭지만 독특한 관점을 줘요"),
        20: ("choice", "정글북", "The Jungle Book", "identity requires a choice", "진정한 정체성은 선택을 요구해요", "모든 곳에 속하려 하면 어디에도 속하지 못해요", "모글리는 자신이 누구인지 선택해야 했어요"),
        21: ("lies", "피노키오", "Pinocchio", "lies always made things worse", "거짓말은 항상 상황을 악화시켰어요", "피노키오는 결과를 피하려고 거짓말했지만 더 큰 문제를 만들었어요", "거짓말할 때마다 코가 길어지는 것은 눈에 보이는 결과였어요"),
        22: ("honesty", "피노키오", "Pinocchio", "integrity means honesty", "진실됨은 고통스러워도 정직한 것을 의미해요", "피노키오는 정직의 대가가 크다는 것을 배웠어요", "정직은 때때로 아프지만 항상 옳은 길이에요"),
        23: ("freedom", "피노키오", "Pinocchio", "freedom requires responsibility", "진정한 자유는 책임을 요구해요", "하고 싶은 대로 하는 것이 자유가 아니에요", "피노키오는 놀이 나라에서 자유가 결과와 함께 온다는 것을 배웠어요"),
        24: ("real through goodness", "피노키오", "Pinocchio", "he became real through goodness", "피노키오는 마법이 아니라 선함을 통해 진짜가 되었어요", "용기와 자기 희생이 피노키오를 변화시켰어요", "진짜가 된다는 것은 외모가 아니라 마음의 문제예요"),
        25: ("bored", "신비한 톨부스", "The Phantom Tollbooth", "Milo was bored with everything", "밀로는 모든 것에 지루해했어요", "신비한 요금소가 나타나기 전까지 밀로는 아무것에도 흥미가 없었어요", "지루함은 세상이 아니라 우리의 태도에서 오는 거예요"),
        26: ("words numbers", "신비한 톨부스", "The Phantom Tollbooth", "words and numbers both matter", "말과 숫자 모두 중요해요", "딕셔너폴리스와 디지토폴리스는 서로 적대적이었지만 둘 다 필요해요", "세상은 말과 숫자 둘 다 없이는 이해할 수 없어요"),
        27: ("wrong roads", "신비한 톨부스", "The Phantom Tollbooth", "even wrong roads lead somewhere", "잘못된 길도 어딘가로 이끌어요", "아무것도 하지 않는 것이 가장 큰 시간 낭비예요", "실수와 잘못된 길도 우리에게 새로운 것을 가르쳐 줘요"),
        28: ("adventures", "신비한 톨부스", "The Phantom Tollbooth", "adventures begin when you try", "모험은 시도할 때 시작돼요", "밀로는 지루함을 멈추는 순간 가장 신나는 모험을 발견했어요", "세상은 호기심으로 바라볼 때 가장 흥미로워요"),
        29: ("own path", "작은 아씨들", "Little Women", "each sister chose her path", "각 자매는 자신만의 길을 선택했어요", "마치 네 자매는 모두 다른 꿈을 가지고 있었어요", "여성의 가치는 관습이 아니라 성격에 있다는 것을 증명했어요"),
        30: ("Jo refuses", "작은 아씨들", "Little Women", "Jo refused expectations", "조는 사회의 기대를 거부했어요", "글쓰기가 조의 진정한 정체성이자 목적이었어요", "조는 자신의 열정을 따르기로 용감하게 결정했어요"),
        31: ("true love", "작은 아씨들", "Little Women", "true love means growing together", "진정한 사랑은 함께 성장하는 것이에요", "완벽함이 아니라 어려움을 통해 더 현명하고 친절해지는 거예요", "마치 자매들의 사랑은 시련을 통해 더 깊어졌어요"),
        32: ("character>wealth", "작은 아씨들", "Little Women", "character matters more than wealth", "성격이 부보다 중요해요", "가족과 진실됨과 목적이 부와 사회적 지위보다 중요해요", "작은 아씨들은 진정한 가치가 무엇인지 보여줘요"),
        33: ("catches thief", "에밀과 탐정들", "Emil and the Detectives", "Emil caught the thief", "에밀이 기차에서 돈을 잃고 도둑을 직접 잡기로 했어요", "에밀은 경찰에 갈 수 없었어요 — 자신도 문제가 될 수 있었거든요", "에밀은 혼자 행동하기로 용감한 결정을 내렸어요"),
        34: ("teamwork", "에밀과 탐정들", "Emil and the Detectives", "they worked as a team", "아이들이 팀으로 함께 일했어요", "모든 아이가 유용한 것을 가지고 있었어요", "혼자서는 할 수 없는 일도 함께하면 가능해요"),
        35: ("bravery", "에밀과 탐정들", "Emil and the Detectives", "bravery means acting despite fear", "용기란 두려움이 없는 게 아니라 두려움 속에서 행동하는 거예요", "에밀은 무서웠지만 옳은 일을 했어요", "진정한 용기는 두려움을 느끼면서도 행동하는 것이에요"),
        36: ("trust", "에밀과 탐정들", "Emil and the Detectives", "trust and teamwork solve problems", "신뢰와 팀워크가 문제를 해결해요", "서로 믿고 명확하게 생각하면 아이들도 큰 문제를 해결할 수 있어요", "에밀의 이야기는 협력의 힘을 보여줘요"),
    }

    for wk, (theme, book_kr, book_en, eng_theme, kr_desc1, kr_desc2, kr_desc3) in week_data.items():
        for day_idx in range(3):
            if (wk, day_idx) in S:
                continue  # already manually defined
            day_labels_kr = ["첫째 날", "둘째 날", "셋째 날"]
            day_label = day_labels_kr[day_idx]
            day_aspects = [
                ("이야기를 시작해요", "소개", "introduction"),
                ("이야기가 깊어져요", "심화", "deepening"),
                ("이야기를 마무리해요", "결론", "conclusion"),
            ]
            aspect_kr, aspect_tag, aspect_en = day_aspects[day_idx]

            if day_idx == 0:
                korean = (
                    f"{book_kr} 이야기의 {day_label}이에요!<br>"
                    f"이번 주의 주제는 '{theme}'에 대한 것이에요.<br>"
                    f"{kr_desc1}.<br>"
                    f"이 이야기는 깊은 의미를 담고 있어요.<br><br>"
                    f"등장인물들은 중요한 순간을 맞이해요.<br>"
                    f"{kr_desc2}.<br>"
                    f"우리도 비슷한 상황을 겪을 수 있어요.<br>"
                    f"그때 어떤 선택을 할 건가요?<br>"
                    f"이 이야기를 통해 함께 생각해 봐요.<br>"
                    f"오늘의 핵심 문장을 잘 기억하세요.<br>"
                    f"영어로도 이야기를 읽어 볼까요?<br>"
                    f"<strong>{kr_desc3}.</strong>"
                )
                a1_html = f"This is a story from {book_en}.<br>Today's theme is about {theme}.<br>Something important happens.<br><span class=\"hl\">__KEY__</span>"
                a1_tts = f"This is a story from {book_en}. Today's theme is about {theme}. Something important happens. __KEY__"
                a2_html = (
                    f"Today we begin a new part of {book_en}.<br>"
                    f"The theme this week is {theme}.<br>"
                    f"The characters face a moment that changes everything.<br>"
                    f"They must think carefully about what to do.<br>"
                    f"<span class=\"hl\">__KEY__</span><br>"
                    f"This is just the beginning of their journey this week."
                )
                a2_tts = f"Today we begin a new part of {book_en}. The theme this week is {theme}. The characters face a moment that changes everything. They must think carefully about what to do. __KEY__ This is just the beginning of their journey this week."
                b1_html = (
                    f"In this chapter of {book_en}, we explore the powerful theme of {theme}.<br>"
                    f"The characters find themselves in a situation that tests their beliefs and values.<br>"
                    f"Every decision they make will have consequences they cannot predict.<br>"
                    f"However, this is what makes the story so meaningful and relatable to our own lives.<br>"
                    f"<span class=\"hl\">__KEY__</span><br>"
                    f"Because great stories mirror real life, we can learn from these characters' experiences.<br>"
                    f"Although the situation seems simple at first, deeper layers of meaning reveal themselves.<br>"
                    f"Let us explore what this part of the story teaches us about {theme}."
                )
                b1_tts = f"In this chapter of {book_en}, we explore the powerful theme of {theme}. The characters find themselves in a situation that tests their beliefs and values. Every decision they make will have consequences they cannot predict. However, this is what makes the story so meaningful and relatable to our own lives. __KEY__ Because great stories mirror real life, we can learn from these characters' experiences. Although the situation seems simple at first, deeper layers of meaning reveal themselves. Let us explore what this part of the story teaches us about {theme}."
            elif day_idx == 1:
                korean = (
                    f"{book_kr} 이야기의 {day_label}이에요.<br>"
                    f"'{theme}' 주제가 더 깊어지고 있어요.<br>"
                    f"{kr_desc2}.<br>"
                    f"등장인물들의 감정이 복잡해지고 있어요.<br><br>"
                    f"쉬운 답은 없어요.<br>"
                    f"하지만 그래서 이 이야기가 가치 있는 거예요.<br>"
                    f"어려운 상황에서 우리는 성장하니까요.<br>"
                    f"등장인물들도 이 과정을 겪고 있어요.<br>"
                    f"그들의 선택이 이야기의 방향을 바꿔요.<br>"
                    f"우리의 선택도 우리 삶의 방향을 바꾸죠.<br>"
                    f"오늘의 핵심 문장이 그 의미를 담고 있어요.<br>"
                    f"<strong>{kr_desc3}.</strong>"
                )
                a1_html = f"The story of {theme} continues.<br>The characters face a harder choice.<br>They are learning and growing.<br><span class=\"hl\">__KEY__</span>"
                a1_tts = f"The story of {theme} continues. The characters face a harder choice. They are learning and growing. __KEY__"
                a2_html = (
                    f"The theme of {theme} grows deeper in today's story.<br>"
                    f"The characters' feelings become more complex and real.<br>"
                    f"There are no easy answers in this situation.<br>"
                    f"But that is exactly what makes this story valuable.<br>"
                    f"<span class=\"hl\">__KEY__</span><br>"
                    f"Their choices in this moment will shape everything that follows."
                )
                a2_tts = f"The theme of {theme} grows deeper in today's story. The characters' feelings become more complex and real. There are no easy answers in this situation. But that is exactly what makes this story valuable. __KEY__ Their choices in this moment will shape everything that follows."
                b1_html = (
                    f"As the story of {book_en} continues, the theme of {theme} reveals its full complexity.<br>"
                    f"The characters struggle with difficult emotions and impossible choices.<br>"
                    f"What seemed clear before is now uncertain, and easy answers have vanished.<br>"
                    f"However, it is precisely in these moments of confusion that real wisdom is born.<br>"
                    f"<span class=\"hl\">__KEY__</span><br>"
                    f"Because growth always comes through challenge, these difficult moments are the most important.<br>"
                    f"Although the characters cannot see it yet, their struggles are shaping them into better people.<br>"
                    f"The story teaches us that understanding {theme} requires patience and experience."
                )
                b1_tts = f"As the story of {book_en} continues, the theme of {theme} reveals its full complexity. The characters struggle with difficult emotions and impossible choices. What seemed clear before is now uncertain, and easy answers have vanished. However, it is precisely in these moments of confusion that real wisdom is born. __KEY__ Because growth always comes through challenge, these difficult moments are the most important. Although the characters cannot see it yet, their struggles are shaping them into better people. The story teaches us that understanding {theme} requires patience and experience."
            else:  # day_idx == 2
                korean = (
                    f"{book_kr} 이야기의 {day_label}이에요!<br>"
                    f"'{theme}' 주제의 마지막 이야기예요.<br>"
                    f"{kr_desc3}.<br>"
                    f"이번 주의 이야기를 정리해 볼까요?<br><br>"
                    f"등장인물들은 중요한 교훈을 배웠어요.<br>"
                    f"그리고 우리도 함께 배웠어요.<br>"
                    f"{theme}에 대해 더 깊이 이해하게 되었어요.<br>"
                    f"이 교훈은 우리 일상에서도 적용할 수 있어요.<br>"
                    f"이야기 속 인물들처럼 우리도 선택해야 해요.<br>"
                    f"매일 조금씩 더 나은 사람이 될 수 있어요.<br>"
                    f"이번 주의 핵심 메시지를 기억하세요.<br>"
                    f"<strong>이 이야기의 교훈을 마음에 간직하세요!</strong>"
                )
                a1_html = f"This is the last story about {theme}.<br>The characters learned something important.<br>We learned it too.<br><span class=\"hl\">__KEY__</span>"
                a1_tts = f"This is the last story about {theme}. The characters learned something important. We learned it too. __KEY__"
                a2_html = (
                    f"Today we finish the story about {theme} in {book_en}.<br>"
                    f"The characters have learned a valuable lesson this week.<br>"
                    f"And we have learned it together with them.<br>"
                    f"This lesson can help us in our own daily lives.<br>"
                    f"<span class=\"hl\">__KEY__</span><br>"
                    f"Remember this week's message as you go forward."
                )
                a2_tts = f"Today we finish the story about {theme} in {book_en}. The characters have learned a valuable lesson this week. And we have learned it together with them. This lesson can help us in our own daily lives. __KEY__ Remember this week's message as you go forward."
                b1_html = (
                    f"As we conclude this week's exploration of {theme} in {book_en}, the full meaning becomes clear.<br>"
                    f"The characters have been transformed by their experiences, gaining wisdom they did not have before.<br>"
                    f"Their journey through {theme} mirrors the challenges we all face in our own lives.<br>"
                    f"However, the most powerful lesson is not just understanding {theme} but applying it to our daily choices.<br>"
                    f"<span class=\"hl\">__KEY__</span><br>"
                    f"Because stories teach us about life, every lesson we learn here can make us better people.<br>"
                    f"Although the characters' adventure is ending, the wisdom they gained will stay with them forever.<br>"
                    f"Let us carry this week's message forward and remember what {theme} truly means."
                )
                b1_tts = f"As we conclude this week's exploration of {theme} in {book_en}, the full meaning becomes clear. The characters have been transformed by their experiences, gaining wisdom they did not have before. Their journey through {theme} mirrors the challenges we all face in our own lives. However, the most powerful lesson is not just understanding {theme} but applying it to our daily choices. __KEY__ Because stories teach us about life, every lesson we learn here can make us better people. Although the characters' adventure is ending, the wisdom they gained will stay with them forever. Let us carry this week's message forward and remember what {theme} truly means."

            S[(wk, day_idx)] = {
                "korean": korean,
                "a1_html": a1_html, "a1_tts": a1_tts,
                "a2_html": a2_html, "a2_tts": a2_tts,
                "b1_html": b1_html, "b1_tts": b1_tts,
            }

    return S


def generate_story(wk, day_letter, key_sentence, book_en, book_kr):
    theme_word, theme_desc = WEEK_THEMES.get(wk, ("theme", "이야기가 계속되다"))
    day_idx = {"a": 0, "b": 1, "c": 2}[day_letter]

    ALL = _build_all_stories()
    k = (wk, day_idx)
    if k in ALL:
        entry = ALL[k]
        result = {}
        for field in entry:
            val = entry[field]
            if isinstance(val, str):
                val = val.replace("__KEY__", key_sentence)
            result[field] = val
        return result

    # Fallback
    return _fallback_story(wk, day_idx, key_sentence, book_en, book_kr, theme_word, theme_desc)


def _fallback_story(wk, day_idx, key, book_en, book_kr, theme, theme_desc):
    day_labels = ["첫째 날", "둘째 날", "셋째 날"]
    day_l = day_labels[day_idx]
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
    a1_html = f"This story is about {book_en}.<br>The theme today is {theme}.<br><span class=\"hl\">{clean_key}</span><br>Let us read more!"
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


# ── CSS to add ──
CSS_BLOCK = """.story-level{display:flex;align-items:center;gap:8px;margin:14px 0 4px;padding:8px 12px;border-radius:10px;font-size:0.75rem;font-weight:800;}
.story-level.a1{background:#e8f5e9;color:#2e7d32;}
.story-level.a2{background:#e3f2fd;color:#1565c0;}
.story-level.b1{background:#fff3e0;color:#e65100;}"""


def process_file(filepath):
    """Process a single lesson file."""
    fname = os.path.basename(filepath)
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
            # Try with smart quotes
            key_m = re.search(r'class="key-eng"[^>]*>\u201c([^\u201d]+)\u201d<', html)
            if key_m:
                key_sentence = key_m.group(1)
            else:
                print(f"  WARN: No key sentence found in {fname}")
                key_sentence = "This is an important sentence."
    else:
        key_raw = key_m.group(1).strip()
        key_sentence = key_raw.strip('"').strip('\u201c\u201d').strip()

    # Remove &quot; wrappers if present
    key_sentence = key_sentence.replace('&quot;', '').strip('"').strip()

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

    # Escape single quotes for TTS (storyPlay onclick)
    a1_tts_safe = a1_tts.replace("'", "\\'")
    a2_tts_safe = a2_tts.replace("'", "\\'")
    b1_tts_safe = b1_tts.replace("'", "\\'")

    # 1. Add CSS if missing
    if '.story-level{' not in html and '.story-level {' not in html:
        css_pattern = re.search(r'(\.story-en\{[^}]+\})', html)
        if css_pattern:
            html = html.replace(css_pattern.group(1), css_pattern.group(1) + '\n' + CSS_BLOCK)

    # 2. Replace story body
    # Strategy: find "먼저 한국어로 읽어봐!" robo-nm, then replace from there to the prog bar
    # Handle both </article> and </div> ending styles

    full_pattern = re.compile(
        r'(<div class="robo-nm" style="color:var\(--gold\);">먼저 한국어로 읽어봐!</div>)'
        r'[\s\S]*?'
        r'(</div>\s*<div class="prog"><div class="prog-fill"[^>]*></div></div>\s*</(?:article|div)>)',
        re.DOTALL
    )

    full_match = full_pattern.search(html)
    if not full_match:
        # Try alternate pattern — some files might have different whitespace
        full_pattern2 = re.compile(
            r'(먼저 한국어로 읽어봐!</div>)'
            r'[\s\S]*?'
            r'(<div class="prog"><div class="prog-fill")',
            re.DOTALL
        )
        full_match2 = full_pattern2.search(html)
        if not full_match2:
            print(f"  WARN: Could not find story section in {fname}")
            return False
        # Use a wider match
        # Find from the robo-nm through prog bar
        start = html.find('먼저 한국어로 읽어봐!</div>')
        if start == -1:
            print(f"  WARN: No Korean robo section in {fname}")
            return False
        # Find the robo-nm div start
        robo_nm_start = html.rfind('<div class="robo-nm"', 0, start)
        # Find the prog bar end
        prog_start = html.find('<div class="prog"><div class="prog-fill"', start)
        if prog_start == -1:
            print(f"  WARN: No prog bar after story in {fname}")
            return False
        # Find end of the article/div after prog
        prog_line_end = html.find('>', prog_start)
        # Find the closing </div></div></article> or </div></div></div>
        close_end = html.find('</article>', prog_start)
        if close_end == -1:
            close_end = html.find('</div>', prog_start + 50)
            if close_end != -1:
                # Need to find the right closing pattern
                remaining = html[prog_start:]
                close_m = re.search(r'<div class="prog"><div class="prog-fill"[^>]*></div></div></(?:article|div)>', remaining)
                if close_m:
                    actual_end = prog_start + close_m.end()
                else:
                    print(f"  WARN: Could not find section end in {fname}")
                    return False
            else:
                print(f"  WARN: Could not find section end in {fname}")
                return False
        else:
            # Find end including </article>
            actual_end = close_end + len('</article>')

        # Build replacement
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

        # Find the prog ending to preserve
        remaining = html[prog_start:]
        close_m = re.search(r'(<div class="prog"><div class="prog-fill"[^>]*></div></div></(?:article|div)>)', remaining)
        if close_m:
            prog_ending = close_m.group(1)
        else:
            prog_ending = '<div class="prog"><div class="prog-fill" style="width:18%;"></div></div></article>'

        html = html[:robo_nm_start] + new_story + prog_ending + html[actual_end:]
    else:
        prog_ending = full_match.group(2)

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

        new_block = new_story + prog_ending
        html = html[:full_match.start()] + new_block + html[full_match.end():]

    # Remove old id attributes from story buttons
    html = html.replace(' id="story-play-btn"', '').replace(' id="story-stop-btn"', '')
    # Remove old story-data div if present
    html = re.sub(r'\s*<div id="story-data"[^>]*></div>', '', html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return True


def main():
    import glob as g
    files = sorted(g.glob(os.path.join(BASE, 'week*[abc].html')))
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
            import traceback
            traceback.print_exc()

    print(f"\nDone! Updated: {updated}, Failed/Skipped: {failed}, Total: {len(files)}")


if __name__ == '__main__':
    main()

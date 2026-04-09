#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expand Section 2 stories for all G3 lesson files (skip week01a, week02a)."""

import re, glob, html, os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Book assignments by week ──
def get_book(w):
    if w <= 4: return ("Peter Rabbit", "피터 래빗")
    if w <= 9: return ("Little Red Riding Hood", "빨간 모자")
    if w <= 13: return ("Jack and the Beanstalk", "잭과 콩나무")
    if w <= 18: return ("The Frog Prince", "개구리 왕자")
    if w <= 21: return ("The Elves and the Shoemaker", "요정과 구두장이")
    if w <= 24: return ("Thumbelina", "엄지공주")
    if w <= 27: return ("The Emperor's New Clothes", "임금님의 새 옷")
    if w <= 31: return ("Lucky Hans", "행운의 한스")
    return ("The Velveteen Rabbit", "벨벳 토끼")

# ── Story data: Korean stories, A1, A2 for each file ──
# Format: { "weekXXd": (korean_story, a1_text, a2_text) }
# korean_story uses \n for <br>, a1/a2 use \n for <br>
# KEY_SENT placeholder will be replaced with actual key sentence
# HL_SENT placeholder marks where to put <span class="hl"> in A2

STORIES = {}

# ─── W01b: He ran away fast. ───
STORIES["week01b"] = (
    "피터는 계속 달리고 있어요! 🏃\n"
    "맥그리거 할아버지가 뒤에서 소리쳤어요.\n"
    "\"거기 서! 이 나쁜 토끼야!\"\n"
    "피터의 심장이 쿵쿵쿵 뛰었어요.\n"
    "당근 밭을 지나고, 양배추 밭도 지나갔어요.\n"
    "피터의 작은 다리가 아팠지만 멈출 수 없었어요.\n"
    "할아버지의 발소리가 점점 가까워졌어요! 😱\n"
    "피터는 더 빨리 달렸어요.\n"
    "바람처럼 빠르게, 정말 빠르게!\n"
    "드디어 할아버지가 멀어지기 시작했어요.\n"
    "<strong>피터는 정말 빠르게 도망쳤어요! ⚡</strong>",
    # A1
    "Mr. McGregor shouted at Peter.\n"
    "Peter was very scared.\n"
    "He ran and ran.\n"
    "He ran away fast.",
    # A2
    "Mr. McGregor chased Peter through the garden.\n"
    "Peter ran past the carrots and the cabbages.\n"
    "His little heart was beating so hard.\n"
    "His legs hurt but he could not stop.\n"
    "He ran away fast and did not look back.\n"
    "Finally, Mr. McGregor fell behind."
)

STORIES["week01c"] = (
    "피터는 지금 가장 무서운 순간을 보내고 있어요! 😰\n"
    "맥그리거 할아버지가 삽을 들고 달려오고 있었어요.\n"
    "피터는 눈물이 날 것 같았어요.\n"
    "\"엄마 말을 들을 걸...\" 피터는 후회했어요.\n"
    "하지만 지금은 도망치는 것이 가장 중요해요!\n"
    "피터는 온 힘을 다해서 달렸어요.\n"
    "넘어질 뻔했지만 다시 일어났어요.\n"
    "다리가 떨리고 숨이 찼지만 포기하지 않았어요.\n"
    "마침내 정원 문이 보였어요! 🚪\n"
    "피터는 문틈으로 빠져나갔어요.\n"
    "할아버지는 더 이상 따라올 수 없었어요!\n"
    "<strong>피터는 있는 힘껏 도망쳤어요! 💨</strong>",
    # A1
    "Peter was so afraid.\n"
    "He ran very very fast.\n"
    "He saw the garden gate.\n"
    "He ran away as fast as he could.",
    # A2
    "Peter was terrified of Mr. McGregor.\n"
    "He wished he had listened to his mother.\n"
    "But now he had to escape with all his strength.\n"
    "He ran past the tool shed and the flower pots.\n"
    "He ran away as fast as he could toward the gate.\n"
    "He squeezed through the gate and was finally free."
)

# ─── W02b: He hid under a basket. ───
STORIES["week02b"] = (
    "피터는 아직 정원 안에 있어요! 😱\n"
    "맥그리거 할아버지가 어디에 있는지 모르겠어요.\n"
    "피터는 조용히 주위를 둘러봤어요.\n"
    "저기 큰 바구니가 보여요!\n"
    "피터는 재빨리 바구니 아래로 들어갔어요.\n"
    "어둡고 좁았지만 안전했어요.\n"
    "할아버지의 발소리가 들렸어요... 쿵, 쿵, 쿵!\n"
    "피터는 숨을 참았어요. 💓\n"
    "할아버지가 바구니 옆을 지나갔어요!\n"
    "\"휴...\" 피터는 작은 소리로 한숨을 쉬었어요.\n"
    "<strong>피터는 바구니 아래에 숨었어요! 🙈</strong>",
    # A1
    "Peter looked around.\n"
    "He saw a big basket.\n"
    "He went under it.\n"
    "He hid under a basket.",
    # A2
    "Peter was still stuck inside the garden.\n"
    "He needed a safe place to hide from Mr. McGregor.\n"
    "He spotted a large basket near the flower pots.\n"
    "He hid under a basket and held his breath.\n"
    "Mr. McGregor walked right past him.\n"
    "Peter stayed very still until the footsteps were gone."
)

STORIES["week02c"] = (
    "피터는 바구니 아래에서 떨고 있었어요. 😨\n"
    "온몸이 부들부들 떨렸어요.\n"
    "추워서가 아니라 너무 무서워서 그랬어요.\n"
    "할아버지가 다시 돌아오는 것 같았어요!\n"
    "\"어디 갔지, 그 토끼?\" 할아버지가 중얼거렸어요.\n"
    "피터의 귀가 쫑긋 세워졌어요. 👂\n"
    "심장이 너무 빠르게 뛰었어요.\n"
    "하지만 바구니 안은 어둡고 좁아서 보이지 않았어요.\n"
    "할아버지가 다시 멀어졌어요.\n"
    "피터는 바구니를 꽉 잡고 떨었어요.\n"
    "<strong>피터는 바구니 아래에 숨어서 부들부들 떨었어요! 😰</strong>",
    # A1
    "Peter was under the basket.\n"
    "He was so scared.\n"
    "His body was shaking.\n"
    "He hid under a basket and shook.",
    # A2
    "Peter crouched under the basket in the dark.\n"
    "His whole body was trembling with fear.\n"
    "He could hear Mr. McGregor searching nearby.\n"
    "He hid under a basket and shook with terror.\n"
    "The old man muttered and walked away slowly.\n"
    "Peter stayed hidden, too afraid to move."
)

# ─── W03a: Mother helped him. ───
STORIES["week03a"] = (
    "피터는 겨우겨우 집에 돌아왔어요. 🏠\n"
    "온몸이 축 처져 있었어요.\n"
    "재킷도 잃어버리고, 신발도 잃어버렸어요.\n"
    "배도 아프고 다리도 아팠어요.\n"
    "엄마 토끼가 피터를 보았어요.\n"
    "\"어머나, 피터야! 무슨 일이야?\" 😢\n"
    "엄마는 피터를 안아줬어요.\n"
    "따뜻한 물로 피터를 씻겨줬어요.\n"
    "엄마의 손은 부드럽고 따뜻했어요.\n"
    "피터는 엄마가 있어서 다행이라고 생각했어요.\n"
    "<strong>엄마가 피터를 도와줬어요! 💕</strong>",
    # A1
    "Peter came home.\n"
    "He was tired and sick.\n"
    "Mother Rabbit saw him.\n"
    "Mother helped him.",
    # A2
    "Peter finally arrived home, tired and scared.\n"
    "He had lost his jacket and his shoes in the garden.\n"
    "His stomach hurt from eating too many vegetables.\n"
    "Mother Rabbit saw poor little Peter at the door.\n"
    "She held him gently in her warm arms.\n"
    "Mother helped him feel safe and warm again."
)

STORIES["week03b"] = (
    "엄마는 피터를 따뜻하게 돌봐줬어요. 🤗\n"
    "피터의 이마를 만져보니 열이 있었어요.\n"
    "\"피터야, 오늘은 푹 쉬어야 해.\"\n"
    "엄마는 부드러운 이불을 가져왔어요.\n"
    "피터를 침대에 눕혔어요.\n"
    "베개도 폭신하게 놓아줬어요.\n"
    "피터는 눈이 감기기 시작했어요. 😴\n"
    "\"고마워요, 엄마...\" 피터가 작은 목소리로 말했어요.\n"
    "엄마는 피터의 머리를 쓰다듬어줬어요.\n"
    "피터는 따뜻한 침대에서 평화로웠어요.\n"
    "<strong>엄마가 피터를 침대에 눕혀줬어요! 🛏️</strong>",
    # A1
    "Peter felt sick.\n"
    "Mother brought a blanket.\n"
    "She was very kind.\n"
    "Mother put him to bed.",
    # A2
    "Peter was not feeling well after his big adventure.\n"
    "Mother Rabbit checked his temperature and looked worried.\n"
    "She brought a soft blanket and a fluffy pillow.\n"
    "Mother put him to bed and tucked him in gently.\n"
    "Peter whispered thank you as his eyes closed.\n"
    "He felt safe and warm in his cozy bed."
)

STORIES["week03c"] = (
    "피터는 침대에 누워 있었어요. 🛏️\n"
    "아직 배가 아프고 몸이 힘들었어요.\n"
    "엄마 토끼가 부엌에서 무언가를 만들고 있었어요.\n"
    "좋은 냄새가 솔솔 나왔어요.\n"
    "\"피터야, 이거 마시면 나을 거야.\" 🍵\n"
    "엄마가 따뜻한 카모마일 차를 가져왔어요.\n"
    "피터가 차를 조금씩 마셨어요.\n"
    "배가 따뜻해지고 편안해졌어요.\n"
    "엄마가 이불을 가지런히 덮어줬어요.\n"
    "피터는 엄마 품에서 스르르 잠이 들었어요. 😴\n"
    "엄마의 사랑이 최고의 약이었어요.\n"
    "<strong>엄마가 카모마일 차를 주고 이불을 덮어줬어요! 💝</strong>",
    # A1
    "Mother made warm tea.\n"
    "Peter drank the tea.\n"
    "She covered him with a blanket.\n"
    "Mother gave him camomile tea and tucked him in.",
    # A2
    "Peter was lying in bed still feeling very sick.\n"
    "Mother Rabbit went to the kitchen to make something special.\n"
    "She brought a warm cup of camomile tea to his bedside.\n"
    "Peter sipped the tea slowly and his tummy felt better.\n"
    "Mother gave him camomile tea and tucked him in lovingly.\n"
    "Peter fell asleep feeling safe in his mother's care."
)

# ─── W04: Sisters went out ───
STORIES["week04a"] = (
    "다음 날 아침이 밝았어요. ☀️\n"
    "피터는 아직 침대에 누워 있었어요.\n"
    "배가 아파서 밖에 나갈 수 없었어요.\n"
    "하지만 언니들은 기분이 좋았어요!\n"
    "플롭시, 몹시, 코튼테일은 착한 토끼들이에요.\n"
    "엄마 말씀을 항상 잘 들었거든요.\n"
    "\"우리 산책 가자!\" 언니들이 말했어요.\n"
    "밝은 햇살 아래 오솔길로 나갔어요.\n"
    "피터는 창문 밖을 쳐다보며 부러워했어요. 😔\n"
    "\"나도 착하게 할 걸...\" 피터는 생각했어요.\n"
    "<strong>언니들은 밖으로 나갔어요! 🌿</strong>",
    # A1
    "Peter was in bed.\n"
    "His sisters were happy.\n"
    "They went outside.\n"
    "His sisters went out.",
    # A2
    "The next morning, Peter was still sick in bed.\n"
    "But his three sisters were feeling very happy.\n"
    "Flopsy, Mopsy, and Cotton-tail always listened to Mother.\n"
    "His sisters went out for a walk down the lane.\n"
    "Peter watched from his window and felt a little sad.\n"
    "He wished he had been a good rabbit like them."
)

STORIES["week04b"] = (
    "플롭시, 몹시, 코튼테일은 오솔길을 걸었어요. 🚶\n"
    "날씨가 정말 좋았어요.\n"
    "새들이 노래하고, 나비가 날아다녔어요. 🦋\n"
    "\"저기 봐! 딸기가 있어!\" 몹시가 말했어요.\n"
    "오솔길 옆에 예쁜 딸기 덤불이 있었어요.\n"
    "빨간 딸기가 반짝반짝 빛나고 있었어요.\n"
    "언니들은 신나서 딸기를 땄어요.\n"
    "\"엄마한테 가져다 드리자!\" 코튼테일이 말했어요.\n"
    "바구니 가득 딸기를 담았어요. 🍓\n"
    "피터는 집에서 혼자 쉬고 있었어요.\n"
    "<strong>언니들은 딸기를 따러 갔어요! 🍓</strong>",
    # A1
    "The sisters walked together.\n"
    "They found berries.\n"
    "They picked many berries.\n"
    "His sisters went to pick berries.",
    # A2
    "Flopsy, Mopsy, and Cotton-tail walked down the sunny lane.\n"
    "The birds were singing and butterflies flew around them.\n"
    "They found a beautiful berry bush by the path.\n"
    "His sisters went to pick berries and fill their basket.\n"
    "They wanted to bring the berries home for Mother.\n"
    "Meanwhile, poor Peter was resting alone in his bed."
)

STORIES["week04c"] = (
    "언니들은 오솔길을 따라 더 멀리 걸어갔어요. 🌳\n"
    "큰 나무 아래에 블랙베리 덤불이 있었어요!\n"
    "까만 블랙베리가 탐스럽게 열려 있었어요.\n"
    "\"우와, 정말 맛있겠다!\" 플롭시가 소리쳤어요. 😋\n"
    "언니들은 하나씩 따서 먹었어요.\n"
    "달콤하고 새콤한 맛이었어요!\n"
    "바구니도 가득 채웠어요.\n"
    "집에 돌아와서 엄마에게 드렸어요.\n"
    "\"착한 아이들이구나!\" 엄마가 웃으셨어요. 😊\n"
    "피터는 저녁에 차만 마셨어요.\n"
    "착한 토끼들은 맛있는 간식을 먹었어요.\n"
    "<strong>언니들은 오솔길에서 블랙베리를 땄어요! 🫐</strong>",
    # A1
    "The sisters walked down the lane.\n"
    "They found blackberries.\n"
    "They picked and ate them.\n"
    "His sisters picked blackberries down the lane.",
    # A2
    "The three sisters walked further down the lane together.\n"
    "Under a big tree, they found a blackberry bush.\n"
    "The berries looked ripe and delicious in the sunshine.\n"
    "His sisters picked blackberries down the lane happily.\n"
    "They brought a full basket home to share with Mother.\n"
    "Peter only had camomile tea while they enjoyed the sweet berries."
)

# ─── W05: She walked alone (Red Riding Hood begins) ───
STORIES["week05a"] = (
    "옛날 옛날에 빨간 모자를 쓴 소녀가 살았어요. 🏡\n"
    "모두가 이 소녀를 '빨간 모자'라고 불렀어요.\n"
    "어느 날 엄마가 말했어요.\n"
    "\"할머니가 아프시단다. 이 바구니를 가져다 드리렴.\"\n"
    "바구니 안에는 빵과 과일이 있었어요. 🧺\n"
    "빨간 모자는 씩씩하게 대답했어요.\n"
    "\"네, 엄마! 다녀올게요!\"\n"
    "할머니 집은 숲을 지나가야 했어요.\n"
    "빨간 모자는 혼자서 길을 떠났어요.\n"
    "숲은 조용하고 조금 어두웠어요. 🌲\n"
    "<strong>빨간 모자는 혼자서 걸어갔어요! 👧</strong>",
    # A1
    "A girl wore a red hood.\n"
    "Grandmother was sick.\n"
    "She took a basket.\n"
    "She walked alone.",
    # A2
    "Once upon a time, there was a girl called Red Riding Hood.\n"
    "Her grandmother was sick, so Mother packed a basket of food.\n"
    "She walked alone through the forest to visit Grandmother.\n"
    "The forest was quiet and a little bit dark.\n"
    "She was brave but also a little scared.\n"
    "She kept walking on the path all by herself."
)

STORIES["week05b"] = (
    "빨간 모자는 숲길을 걷고 있었어요. 🌲\n"
    "나무들이 높이 솟아 있었어요.\n"
    "햇빛이 나뭇잎 사이로 살짝 들어왔어요.\n"
    "새소리가 들렸지만 조금 무서웠어요.\n"
    "\"빨리 가야지, 할머니가 기다리고 계시니까.\"\n"
    "빨간 모자는 용기를 내서 걸었어요. 💪\n"
    "숲이 점점 더 어두워졌어요.\n"
    "나뭇가지가 바스락 소리를 냈어요.\n"
    "빨간 모자의 심장이 두근두근 뛰었어요.\n"
    "하지만 할머니를 생각하며 계속 걸었어요.\n"
    "<strong>빨간 모자는 어두운 숲을 지나갔어요! 🌑</strong>",
    # A1
    "The forest was dark.\n"
    "She was a little scared.\n"
    "But she kept walking.\n"
    "She walked through the dark forest.",
    # A2
    "Red Riding Hood continued deeper into the forest.\n"
    "The trees were tall and blocked most of the sunlight.\n"
    "She walked through the dark forest feeling brave.\n"
    "Strange sounds came from behind the bushes.\n"
    "Her heart was beating fast but she thought of Grandmother.\n"
    "She held her basket tightly and walked on."
)

STORIES["week05c"] = (
    "빨간 모자는 이제 숲 깊은 곳에 있었어요. 🌲\n"
    "처음에는 무서웠지만 점점 용기가 났어요.\n"
    "예쁜 꽃들이 숲길 옆에 피어 있었어요. 🌸\n"
    "\"할머니가 좋아하실 꽃도 가져가야지!\"\n"
    "하지만 엄마의 말이 생각났어요.\n"
    "\"길에서 벗어나면 안 돼, 알았지?\"\n"
    "빨간 모자는 다시 정신을 차렸어요.\n"
    "바구니를 꼭 잡고 할머니 집을 향해 걸었어요.\n"
    "할머니가 아프시니까 빨리 가야 해요.\n"
    "빨간 모자는 꿋꿋하게 숲을 지나갔어요. 💕\n"
    "<strong>빨간 모자는 할머니를 만나러 숲을 지나갔어요! 🏡</strong>",
    # A1
    "She had to visit Grandmother.\n"
    "The forest was long.\n"
    "She was brave and strong.\n"
    "She walked through the forest to visit Grandmother.",
    # A2
    "Red Riding Hood was deep inside the forest now.\n"
    "She saw pretty flowers but remembered Mother's warning.\n"
    "She walked through the forest to visit Grandmother without stopping.\n"
    "She held her basket of bread and fruit tightly.\n"
    "The path was long but she thought of Grandmother's smile.\n"
    "She was brave enough to walk the whole way alone."
)

# ─── W06: The wolf spoke ───
STORIES["week06a"] = (
    "빨간 모자가 숲길을 걷고 있을 때였어요. 🌲\n"
    "갑자기 덤불 뒤에서 무언가가 나타났어요!\n"
    "커다란 눈, 뾰족한 귀... 늑대였어요! 🐺\n"
    "빨간 모자는 깜짝 놀랐어요.\n"
    "하지만 늑대는 무섭지 않은 척했어요.\n"
    "부드러운 목소리로 말을 걸었어요.\n"
    "\"안녕, 꼬마야. 어디 가니?\"\n"
    "빨간 모자는 조금 경계했어요.\n"
    "하지만 늑대가 너무 친절하게 말해서 대답했어요.\n"
    "\"할머니 집에 가요.\"\n"
    "<strong>늑대가 말을 걸었어요! 🗣️</strong>",
    # A1
    "A wolf appeared.\n"
    "He looked friendly.\n"
    "He talked to the girl.\n"
    "The wolf spoke.",
    # A2
    "Red Riding Hood was walking when a big wolf appeared.\n"
    "The wolf had big eyes and pointy ears.\n"
    "But he pretended to be friendly and kind.\n"
    "The wolf spoke to her in a soft, gentle voice.\n"
    "He asked where she was going with her basket.\n"
    "Red Riding Hood told him about Grandmother's house."
)

STORIES["week06b"] = (
    "늑대는 아주 교활했어요. 🦊\n"
    "겉으로는 친절한 척했지만 속으로는 나쁜 생각을 하고 있었어요.\n"
    "\"할머니 집에 간다고? 어디 있는데?\" 🐺\n"
    "늑대는 부드러운 목소리로 물어봤어요.\n"
    "빨간 모자는 순진하게 대답했어요.\n"
    "\"숲 끝에 있는 빨간 지붕 집이에요.\"\n"
    "늑대는 속으로 웃었어요.\n"
    "\"좋아, 나에게 좋은 생각이 있지...\"\n"
    "빨간 모자는 늑대의 나쁜 마음을 몰랐어요.\n"
    "늑대의 친절한 말에 속고 말았어요. 😟\n"
    "<strong>늑대는 친절한 목소리로 말했어요! 🎭</strong>",
    # A1
    "The wolf smiled.\n"
    "He was not really kind.\n"
    "He had a bad plan.\n"
    "The wolf spoke in a kind voice.",
    # A2
    "The wolf was very sly and had a secret plan.\n"
    "He pretended to be nice to trick the little girl.\n"
    "The wolf spoke in a kind voice and asked about Grandmother.\n"
    "Red Riding Hood told him where the house was.\n"
    "The wolf grinned because now he knew the way.\n"
    "Poor Red Riding Hood did not know she was being tricked."
)

STORIES["week06c"] = (
    "늑대는 빨간 모자에게 계속 말을 걸었어요. 🐺\n"
    "\"이 숲에 예쁜 꽃이 많지 않니?\"\n"
    "\"할머니한테 꽃을 가져가면 좋아하실 거야.\"\n"
    "빨간 모자는 잠깐 생각했어요. 🤔\n"
    "\"할머니가 정말 좋아하시겠다!\"\n"
    "빨간 모자가 꽃을 따는 동안\n"
    "늑대는 몰래 할머니 집으로 달려갔어요!\n"
    "늑대는 아주 빠르게 움직였어요. 💨\n"
    "빨간 모자는 늑대가 어디로 갔는지 몰랐어요.\n"
    "꽃을 다 따고 나서 다시 길을 걸었어요.\n"
    "<strong>늑대는 친절하게 말하며 빨간 모자가 어디에 가는지 물었어요! 😈</strong>",
    # A1
    "The wolf asked many questions.\n"
    "He tricked the girl.\n"
    "She stopped to pick flowers.\n"
    "The wolf spoke kindly and asked where she went.",
    # A2
    "The wolf kept talking to Red Riding Hood sweetly.\n"
    "He suggested she pick flowers for her grandmother.\n"
    "The wolf spoke kindly and asked where she went.\n"
    "While she was busy picking flowers in the forest,\n"
    "the wolf ran ahead to Grandmother's house.\n"
    "Red Riding Hood did not realize the wolf's evil plan."
)

# ─── W07: Something was wrong ───
STORIES["week07a"] = (
    "빨간 모자가 할머니 집에 도착했어요. 🏠\n"
    "문을 똑똑 두드렸어요.\n"
    "\"할머니, 저예요! 빨간 모자!\"\n"
    "안에서 이상한 목소리가 들렸어요.\n"
    "\"들어오렴, 얘야...\"\n"
    "목소리가 할머니 같지 않았어요. 🤨\n"
    "빨간 모자가 문을 열고 들어갔어요.\n"
    "침대에 할머니가 이불을 뒤집어쓰고 있었어요.\n"
    "뭔가 이상했어요.\n"
    "빨간 모자는 묘한 느낌이 들었어요.\n"
    "<strong>뭔가 이상했어요! 😰</strong>",
    # A1
    "She opened the door.\n"
    "Grandmother looked different.\n"
    "She felt strange.\n"
    "Something was wrong.",
    # A2
    "Red Riding Hood arrived at Grandmother's cottage.\n"
    "She knocked on the door and heard a strange voice.\n"
    "When she went inside, Grandmother was in bed.\n"
    "But something was wrong with the way she looked.\n"
    "Her voice sounded deep and her eyes looked too big.\n"
    "Red Riding Hood felt a chill run down her back."
)

STORIES["week07b"] = (
    "빨간 모자는 침대 옆으로 다가갔어요. 🛏️\n"
    "할머니를 자세히 보았어요.\n"
    "\"할머니, 귀가 왜 이렇게 커요?\"\n"
    "\"잘 들으려고 그렇단다, 얘야.\"\n"
    "\"할머니, 눈이 왜 이렇게 커요?\" 👀\n"
    "\"잘 보려고 그렇단다.\"\n"
    "빨간 모자의 마음이 두근두근 뛰기 시작했어요.\n"
    "분명히 뭔가 이상해요.\n"
    "할머니의 코도 크고, 입도 아주 컸어요.\n"
    "빨간 모자는 점점 불안해졌어요. 😨\n"
    "<strong>빨간 모자는 뭔가 이상하다고 느꼈어요! 😟</strong>",
    # A1
    "Grandmother had big ears.\n"
    "She had big eyes too.\n"
    "Something was not right.\n"
    "She felt something was wrong.",
    # A2
    "Red Riding Hood walked closer to the bed.\n"
    "She asked why Grandmother's ears were so big.\n"
    "She asked why Grandmother's eyes were so large.\n"
    "Each answer made her feel more and more worried.\n"
    "She felt something was wrong but did not know what.\n"
    "Her heart was beating faster with every question."
)

STORIES["week07c"] = (
    "빨간 모자는 마지막 질문을 했어요.\n"
    "\"할머니, 입이 왜 이렇게 커요?\" 😱\n"
    "그 순간 이불이 확 벗겨졌어요!\n"
    "할머니가 아니었어요... 늑대였어요! 🐺\n"
    "\"너를 잡아먹으려고!\" 늑대가 소리쳤어요.\n"
    "빨간 모자는 비명을 질렀어요.\n"
    "\"살려주세요!!\" 😭\n"
    "늑대가 침대에서 벌떡 일어났어요.\n"
    "빨간 모자는 너무 무서웠어요.\n"
    "할머니는 어디에 계신 걸까요?\n"
    "빨간 모자는 걱정이 가득했어요.\n"
    "<strong>빨간 모자는 할머니가 아주 이상하게 보여서 걱정했어요! 😰</strong>",
    # A1
    "The mouth was too big.\n"
    "It was the wolf!\n"
    "She was very scared.\n"
    "She felt worried because Grandmother looked very strange.",
    # A2
    "Red Riding Hood asked about the big mouth.\n"
    "Suddenly the wolf jumped out of the bed.\n"
    "She felt worried because Grandmother looked very strange.\n"
    "The wolf had been wearing Grandmother's clothes all along.\n"
    "Red Riding Hood screamed and tried to run away.\n"
    "She was terrified and did not know where Grandmother was."
)

# ─── W08: The hunter came ───
STORIES["week08a"] = (
    "빨간 모자가 크게 소리를 질렀어요! 😱\n"
    "\"도와주세요! 누구 없어요?!\"\n"
    "늑대가 빨간 모자에게 다가오고 있었어요. 🐺\n"
    "바로 그때! 밖에서 발소리가 들렸어요.\n"
    "쿵! 쿵! 쿵! 문이 열렸어요!\n"
    "숲속 사냥꾼 아저씨가 나타났어요! 🪓\n"
    "사냥꾼은 크고 힘이 셌어요.\n"
    "\"이 늑대 놈!\" 사냥꾼이 소리쳤어요.\n"
    "빨간 모자는 너무 기뻤어요.\n"
    "드디어 도움이 왔어요!\n"
    "<strong>사냥꾼이 왔어요! 🦸</strong>",
    # A1
    "She screamed for help.\n"
    "A hunter was nearby.\n"
    "He heard her voice.\n"
    "The hunter came.",
    # A2
    "Red Riding Hood screamed as loud as she could.\n"
    "The wolf was getting closer and closer to her.\n"
    "Luckily, a brave hunter was walking in the forest.\n"
    "He heard the screaming and ran to the cottage.\n"
    "The hunter came and burst through the door.\n"
    "The wolf froze when he saw the strong hunter."
)

STORIES["week08b"] = (
    "사냥꾼이 늑대 앞에 섰어요! 🪓\n"
    "늑대는 사냥꾼을 보고 깜짝 놀랐어요.\n"
    "\"이런... 사냥꾼이라니!\" 🐺\n"
    "사냥꾼은 늑대를 꼼짝 못 하게 했어요.\n"
    "빨간 모자는 구석에서 떨고 있었어요.\n"
    "\"할머니는요?!\" 빨간 모자가 물었어요.\n"
    "사냥꾼이 할머니를 찾아냈어요.\n"
    "할머니는 옷장 안에 갇혀 있었어요! 😮\n"
    "사냥꾼 덕분에 모두가 안전해졌어요.\n"
    "빨간 모자는 사냥꾼에게 감사했어요. 💕\n"
    "<strong>사냥꾼이 와서 그들을 구해줬어요! 🦸</strong>",
    # A1
    "The hunter was brave.\n"
    "He stopped the wolf.\n"
    "He found Grandmother.\n"
    "The hunter came and saved her.",
    # A2
    "The hunter stood between the wolf and Red Riding Hood.\n"
    "The wolf tried to run but the hunter was too strong.\n"
    "The hunter came and saved her from the dangerous wolf.\n"
    "He searched the house and found Grandmother in the closet.\n"
    "She was scared but safe and sound.\n"
    "Red Riding Hood hugged Grandmother and cried with joy."
)

STORIES["week08c"] = (
    "그날의 이야기를 되돌아봐요. 📖\n"
    "빨간 모자는 정말 위험했어요.\n"
    "늑대가 할머니인 척 속였어요. 🐺\n"
    "빨간 모자는 겁에 질려서 소리를 질렀어요.\n"
    "하지만 하늘이 도왔어요!\n"
    "사냥꾼 아저씨가 딱 그 순간에 도착했어요! 🪓\n"
    "1초만 더 늦었으면 큰일이 났을 거예요.\n"
    "사냥꾼이 늑대를 물리치고 할머니도 구해냈어요.\n"
    "빨간 모자는 안도의 눈물을 흘렸어요. 😭\n"
    "\"고마워요, 아저씨!\" 빨간 모자가 말했어요.\n"
    "용감한 사냥꾼 덕분에 모두가 살았어요.\n"
    "<strong>사냥꾼이 딱 맞는 시간에 와서 그들을 구해줬어요! ⏰</strong>",
    # A1
    "The hunter came just in time.\n"
    "He was very strong.\n"
    "Everyone was safe.\n"
    "The hunter arrived just in time and saved them.",
    # A2
    "The situation was very dangerous for Red Riding Hood.\n"
    "The wolf had tricked everyone with his disguise.\n"
    "But the hunter arrived just in time and saved them.\n"
    "One more second and it would have been too late.\n"
    "The hunter chased the wolf far away into the forest.\n"
    "Red Riding Hood and Grandmother hugged each other tightly."
)

# ─── W09: She was safe ───
STORIES["week09a"] = (
    "모든 것이 끝났어요. 🌈\n"
    "늑대는 멀리 도망갔어요.\n"
    "사냥꾼이 늑대를 쫓아냈거든요.\n"
    "빨간 모자는 할머니를 꼭 안았어요. 🤗\n"
    "\"할머니, 괜찮으세요?\"\n"
    "\"괜찮단다, 얘야. 네가 와줘서 고마워.\"\n"
    "빨간 모자는 눈물을 닦았어요.\n"
    "더 이상 무서운 일은 없었어요.\n"
    "따뜻한 할머니 집에서 함께 쉬었어요.\n"
    "빨간 모자는 안전했어요. 💕\n"
    "<strong>빨간 모자는 안전했어요! 😊</strong>",
    # A1
    "The wolf was gone.\n"
    "She hugged Grandmother.\n"
    "Everything was okay.\n"
    "She was safe.",
    # A2
    "The wolf ran far away and never came back.\n"
    "Red Riding Hood held Grandmother's hand tightly.\n"
    "They sat together in the warm cottage.\n"
    "She was safe and sound thanks to the brave hunter.\n"
    "Grandmother smiled and said everything would be fine.\n"
    "Red Riding Hood felt so happy and relieved."
)

STORIES["week09b"] = (
    "빨간 모자는 할머니 옆에 앉아 있었어요. 👵\n"
    "할머니가 따뜻한 차를 끓여주셨어요. ☕\n"
    "\"많이 무서웠지?\" 할머니가 물었어요.\n"
    "\"네, 정말 무서웠어요...\" 빨간 모자가 말했어요.\n"
    "하지만 지금은 안전하니까 괜찮아요.\n"
    "할머니의 손을 잡으니 마음이 따뜻해졌어요.\n"
    "사냥꾼 아저씨도 차를 한 잔 마셨어요. 🍵\n"
    "\"다음부터는 조심하렴.\" 사냥꾼이 말했어요.\n"
    "빨간 모자는 고개를 끄덕였어요.\n"
    "안전해서 정말 다행이에요.\n"
    "<strong>빨간 모자는 안전해서 너무 기뻤어요! 😄</strong>",
    # A1
    "She sat with Grandmother.\n"
    "They had warm tea.\n"
    "She smiled again.\n"
    "She was so happy to be safe.",
    # A2
    "Red Riding Hood sat beside Grandmother in the cottage.\n"
    "Grandmother made warm tea for everyone.\n"
    "The hunter joined them for a cup of tea too.\n"
    "She was so happy to be safe with Grandmother.\n"
    "The scary adventure was finally over.\n"
    "Red Riding Hood promised to be more careful next time."
)

STORIES["week09c"] = (
    "빨간 모자는 집에 돌아왔어요. 🏠\n"
    "엄마가 빨간 모자를 꼭 안아줬어요.\n"
    "\"무슨 일이 있었니?\" 엄마가 걱정했어요.\n"
    "빨간 모자는 모든 이야기를 해줬어요.\n"
    "늑대를 만난 것, 사냥꾼이 구해준 것...\n"
    "엄마는 눈물을 글썽였어요. 😢\n"
    "빨간 모자는 중요한 약속을 했어요.\n"
    "\"엄마, 다시는 낯선 사람과 이야기하지 않을게요.\"\n"
    "이 이야기에서 우리는 배워요.\n"
    "모르는 사람을 조심해야 한다는 것을요. ⚠️\n"
    "빨간 모자는 더 현명한 아이가 되었어요.\n"
    "<strong>빨간 모자는 다시는 낯선 사람과 이야기하지 않겠다고 약속했어요! 🤝</strong>",
    # A1
    "She went home.\n"
    "She told Mother everything.\n"
    "She learned a lesson.\n"
    "She promised never to talk to strangers again.",
    # A2
    "Red Riding Hood returned home and told Mother everything.\n"
    "Mother was worried but glad her daughter was safe.\n"
    "Red Riding Hood learned a very important lesson that day.\n"
    "She promised never to talk to strangers again.\n"
    "From that day on, she always listened to Mother's advice.\n"
    "She became a wiser and more careful girl."
)

# ─── W10: Jack traded the cow ───
STORIES["week10a"] = (
    "새로운 이야기가 시작돼요! 잭과 콩나무! 🌱\n"
    "잭은 가난한 소년이었어요.\n"
    "엄마와 함께 작은 집에 살았어요.\n"
    "먹을 것이 거의 없었어요. 😢\n"
    "엄마가 말했어요. \"소를 팔고 와라.\"\n"
    "잭은 소를 데리고 시장에 갔어요.\n"
    "길에서 이상한 할아버지를 만났어요.\n"
    "\"이 마법 콩이랑 소를 바꾸지 않을래?\" 🫘\n"
    "잭은 마법 콩이라는 말에 신이 났어요.\n"
    "잭은 소를 콩과 바꿨어요!\n"
    "<strong>잭은 소를 바꿨어요! 🐄</strong>",
    # A1
    "Jack was poor.\n"
    "He had a cow.\n"
    "He met an old man.\n"
    "Jack traded the cow.",
    # A2
    "Jack lived in a small house with his mother.\n"
    "They were very poor and had no food left.\n"
    "Mother told Jack to sell their only cow at the market.\n"
    "On the way, Jack met a strange old man.\n"
    "Jack traded the cow for some magic beans.\n"
    "He was excited but Mother would not be happy."
)

STORIES["week10b"] = (
    "잭은 신나서 집으로 돌아왔어요. 🏃\n"
    "\"엄마, 마법 콩을 받았어요!\"\n"
    "하지만 엄마는 화가 많이 났어요. 😡\n"
    "\"뭐?! 콩이라고?! 소를 콩이랑 바꿨어?!\"\n"
    "엄마는 콩을 창밖으로 던져버렸어요.\n"
    "잭은 슬펐어요.\n"
    "\"정말 마법 콩이라고 했는데...\"\n"
    "잭은 저녁도 못 먹고 잠자리에 들었어요. 😔\n"
    "그날 밤, 콩에서 뭔가가 일어나기 시작했어요.\n"
    "아무도 모르게 땅에서 싹이 나왔어요. 🌱\n"
    "<strong>잭은 소를 콩과 바꿨어요! 🫘</strong>",
    # A1
    "Jack came home happy.\n"
    "Mother was angry.\n"
    "She threw the beans.\n"
    "Jack traded the cow for beans.",
    # A2
    "Jack ran home to show Mother the magic beans.\n"
    "But Mother was furious and threw the beans outside.\n"
    "Jack traded the cow for beans and Mother was upset.\n"
    "Jack went to bed without any dinner that night.\n"
    "He felt sad and worried about what he had done.\n"
    "But something magical was growing outside his window."
)

STORIES["week10c"] = (
    "잭의 이야기를 다시 생각해봐요. 📖\n"
    "잭은 착하지만 조금 순진한 소년이에요.\n"
    "시장에 가서 소를 팔아야 했어요.\n"
    "하지만 이상한 할아버지의 말을 믿었어요.\n"
    "\"이 콩은 마법 콩이란다!\" 🫘\n"
    "반짝반짝 빛나는 콩이 너무 신기했어요.\n"
    "잭은 소를 마법 콩과 바꿨어요.\n"
    "집에 와서 엄마한테 혼이 많이 났어요. 😢\n"
    "하지만 잭은 몰랐어요.\n"
    "그 콩이 정말로 마법 콩이었다는 것을요!\n"
    "곧 놀라운 일이 일어날 거예요! ✨\n"
    "<strong>잭은 소를 마법 콩과 바꿨어요! 🌟</strong>",
    # A1
    "Jack met a man.\n"
    "The beans were shiny.\n"
    "He wanted them.\n"
    "Jack traded the cow for magic beans.",
    # A2
    "Jack was supposed to sell the cow at the market.\n"
    "Instead he met a strange man with sparkling beans.\n"
    "Jack traded the cow for magic beans without thinking.\n"
    "Mother was so angry she threw the beans out the window.\n"
    "Jack did not know those beans were truly magical.\n"
    "Something amazing was about to happen very soon."
)

# ─── W11: The beanstalk grew tall ───
STORIES["week11a"] = (
    "다음 날 아침, 잭이 눈을 떴어요. ☀️\n"
    "창밖을 보고 깜짝 놀랐어요!\n"
    "어마어마하게 큰 콩나무가 자라 있었어요! 🌱\n"
    "콩나무는 하늘 높이까지 올라가 있었어요.\n"
    "구름 위까지 닿아 있는 것 같았어요. ☁️\n"
    "잭은 눈을 비비며 다시 봤어요.\n"
    "\"꿈이 아니야?!\"\n"
    "정말로 마법 콩이었어요!\n"
    "엄마도 깜짝 놀라서 입을 벌렸어요.\n"
    "잭은 콩나무를 올려다보며 신이 났어요.\n"
    "<strong>콩나무가 높이 자랐어요! 🌿</strong>",
    # A1
    "Jack woke up.\n"
    "He saw something big.\n"
    "It was a beanstalk.\n"
    "The beanstalk grew tall.",
    # A2
    "The next morning, Jack looked out the window in surprise.\n"
    "A giant beanstalk had grown where Mother threw the beans.\n"
    "The beanstalk grew tall, reaching high above the clouds.\n"
    "Jack could not believe his eyes.\n"
    "The magic beans were real after all.\n"
    "Jack wanted to climb the beanstalk and see what was up there."
)

STORIES["week11b"] = (
    "잭은 콩나무를 올려다봤어요. 🌿\n"
    "너무너무 높았어요!\n"
    "구름 속으로 들어가는 것 같았어요. ☁️\n"
    "\"저 위에는 뭐가 있을까?\"\n"
    "잭은 호기심이 폭발했어요.\n"
    "용기를 내서 콩나무를 타기 시작했어요.\n"
    "한 발 한 발 올라갔어요.\n"
    "바람이 쌩쌩 불었어요. 💨\n"
    "아래를 보니 집이 점처럼 작게 보였어요.\n"
    "잭은 무서웠지만 계속 올라갔어요.\n"
    "<strong>콩나무가 아주 높이 자랐어요! ☁️</strong>",
    # A1
    "The beanstalk was huge.\n"
    "Jack started to climb.\n"
    "He went up and up.\n"
    "The beanstalk grew up very high.",
    # A2
    "Jack decided to climb the enormous beanstalk.\n"
    "The beanstalk grew up very high into the clouds.\n"
    "He climbed one step at a time, holding on tightly.\n"
    "The wind was blowing hard and his house looked tiny below.\n"
    "Jack was scared but his curiosity was even stronger.\n"
    "He kept climbing toward the mysterious cloud above."
)

STORIES["week11c"] = (
    "잭은 계속 올라갔어요. 🧗\n"
    "콩나무는 끝이 없는 것 같았어요.\n"
    "구름 속을 지나니 세상이 달라졌어요!\n"
    "하얀 구름 위에 거대한 성이 있었어요! 🏰\n"
    "잭은 놀라서 입이 떡 벌어졌어요.\n"
    "\"이런 곳이 있다니!\"\n"
    "하지만 아래를 보니 어지러웠어요. 😵\n"
    "너무 높아서 다리가 후들후들 떨렸어요.\n"
    "잭은 잠깐 쉬며 숨을 골랐어요.\n"
    "그리고 용기를 내서 성을 향해 걸었어요.\n"
    "무엇이 기다리고 있을까요?\n"
    "<strong>콩나무가 너무 높이 자라서 잭은 어지러웠어요! 😵‍💫</strong>",
    # A1
    "Jack climbed very high.\n"
    "He saw a castle.\n"
    "He felt dizzy.\n"
    "The beanstalk grew so tall Jack felt dizzy.",
    # A2
    "Jack climbed through the clouds and saw an amazing sight.\n"
    "There was a huge castle sitting on top of the clouds.\n"
    "The beanstalk grew so tall Jack felt dizzy looking down.\n"
    "His legs were shaking but he stepped onto the cloud.\n"
    "The castle was bigger than anything he had ever seen.\n"
    "Jack took a deep breath and walked toward the giant door."
)

# ─── W12: The giant was angry ───
STORIES["week12a"] = (
    "잭은 거대한 성 안으로 들어갔어요. 🏰\n"
    "모든 것이 엄청나게 컸어요!\n"
    "의자도 크고, 탁자도 크고, 접시도 컸어요.\n"
    "탁자 위에 금화가 잔뜩 있었어요! 💰\n"
    "\"우와!\" 잭은 금화를 주머니에 넣었어요.\n"
    "그때! 쿵! 쿵! 쿵! 발소리가 들렸어요!\n"
    "거인이 나타났어요! 👹\n"
    "\"누가 내 금화를 만졌어?!\"\n"
    "거인은 코를 벌렁거리며 소리쳤어요.\n"
    "잭은 탁자 아래에 숨었어요. 😱\n"
    "<strong>거인은 화가 났어요! 😡</strong>",
    # A1
    "Jack went inside the castle.\n"
    "He took some gold.\n"
    "A giant found him.\n"
    "The giant was angry.",
    # A2
    "Jack entered the enormous castle on top of the clouds.\n"
    "Everything inside was huge, built for a giant.\n"
    "Jack saw gold coins on the table and took some.\n"
    "Suddenly, a giant stomped into the room.\n"
    "The giant was angry and shouted with a booming voice.\n"
    "Jack quickly hid under the giant table in fear."
)

STORIES["week12b"] = (
    "거인이 잭을 발견했어요! 😱\n"
    "\"거기 있었구나, 작은 도둑!\"\n"
    "잭은 재빨리 탁자 아래에서 뛰어나왔어요.\n"
    "금화를 꽉 잡고 성 밖으로 달렸어요! 🏃\n"
    "거인이 쿵쿵거리며 뒤쫓아왔어요.\n"
    "\"못 도망간다!\" 거인이 소리쳤어요.\n"
    "잭은 콩나무를 향해 달렸어요.\n"
    "콩나무를 잡고 내려가기 시작했어요.\n"
    "거인도 콩나무를 타고 내려오기 시작했어요! 😨\n"
    "쿵쿵쿵! 콩나무가 흔들렸어요.\n"
    "<strong>거인이 잭을 빠르게 쫓아왔어요! 👹</strong>",
    # A1
    "The giant saw Jack.\n"
    "Jack ran away.\n"
    "The giant followed him.\n"
    "The giant chased Jack down fast.",
    # A2
    "The giant spotted Jack hiding under the table.\n"
    "Jack grabbed the gold coins and ran for the door.\n"
    "The giant chased Jack down fast through the castle.\n"
    "Jack reached the beanstalk and started climbing down.\n"
    "The giant followed him down the shaking beanstalk.\n"
    "Jack could feel the giant getting closer and closer."
)

STORIES["week12c"] = (
    "잭은 있는 힘껏 콩나무를 내려갔어요! 🧗\n"
    "거인이 바로 위에서 쫓아오고 있었어요.\n"
    "콩나무가 거인의 무게로 흔들흔들! 🌿\n"
    "잭의 손이 미끄러웠어요.\n"
    "\"빨리, 더 빨리!\" 잭은 스스로에게 말했어요.\n"
    "아래를 보니 집이 점점 가까워졌어요.\n"
    "엄마가 밖에서 걱정하고 있었어요.\n"
    "\"잭아! 빨리 내려와!\" 엄마가 소리쳤어요. 😰\n"
    "거인의 큰 손이 가까이 보였어요.\n"
    "잭은 마지막 힘을 다해서 내려갔어요.\n"
    "<strong>화가 난 거인이 잭을 끝까지 쫓아왔어요! 😡</strong>",
    # A1
    "The giant followed Jack.\n"
    "Jack climbed down fast.\n"
    "Mother was waiting.\n"
    "The angry giant chased Jack all the way down.",
    # A2
    "Jack climbed down the beanstalk as fast as he could.\n"
    "The angry giant chased Jack all the way down the beanstalk.\n"
    "The beanstalk was shaking from the giant's heavy weight.\n"
    "Jack's hands were slippery but he did not let go.\n"
    "Mother was waiting below, shouting for Jack to hurry.\n"
    "The giant's enormous hands were reaching closer and closer."
)

# ─── W13: Jack chopped it down ───
STORIES["week13a"] = (
    "잭이 드디어 땅에 도착했어요! 🏃\n"
    "하지만 거인도 콩나무를 타고 내려오고 있었어요!\n"
    "\"엄마, 도끼 주세요!\" 잭이 소리쳤어요.\n"
    "엄마가 재빨리 도끼를 가져왔어요. 🪓\n"
    "잭은 콩나무를 향해 도끼를 들었어요.\n"
    "찍! 찍! 찍!\n"
    "콩나무가 흔들리기 시작했어요.\n"
    "거인이 \"안 돼!\" 소리쳤어요. 👹\n"
    "콩나무가 쓰러지기 시작했어요!\n"
    "거인은 구름 위로 떨어졌어요.\n"
    "<strong>잭이 콩나무를 찍어 쓰러뜨렸어요! 🪓</strong>",
    # A1
    "Jack reached the ground.\n"
    "He got an axe.\n"
    "He chopped the beanstalk.\n"
    "Jack chopped it down.",
    # A2
    "Jack finally reached the ground safely.\n"
    "But the giant was still climbing down after him.\n"
    "Jack grabbed a sharp axe from his mother.\n"
    "He swung the axe at the beanstalk with all his strength.\n"
    "Jack chopped it down and it crashed to the ground.\n"
    "The giant fell back up into the clouds and was gone."
)

STORIES["week13b"] = (
    "잭은 도끼로 콩나무를 계속 찍었어요! 🪓\n"
    "찍! 찍! 찍! 나무가 갈라지기 시작했어요.\n"
    "거인이 위에서 소리를 질렀어요.\n"
    "\"멈춰! 내려가게 해 줘!\" 👹\n"
    "하지만 잭은 멈출 수 없었어요.\n"
    "거인이 내려오면 큰일이니까요.\n"
    "잭은 더 세게, 더 빠르게 찍었어요.\n"
    "드디어 우드득! 큰 소리가 나면서\n"
    "콩나무가 쓰러지기 시작했어요! 🌲💥\n"
    "엄마가 잭을 안전한 곳으로 끌어당겼어요.\n"
    "<strong>잭이 콩나무를 찍어 넘어뜨렸어요! 💪</strong>",
    # A1
    "Jack swung the axe.\n"
    "The beanstalk cracked.\n"
    "It started to fall.\n"
    "Jack chopped the beanstalk down.",
    # A2
    "Jack kept swinging the axe with all his might.\n"
    "The giant was screaming from high up on the beanstalk.\n"
    "Jack chopped the beanstalk down with one final swing.\n"
    "The enormous beanstalk cracked and began to fall.\n"
    "Mother pulled Jack to safety just in time.\n"
    "The beanstalk crashed to the ground with a thundering sound."
)

STORIES["week13c"] = (
    "콩나무가 거대한 소리를 내며 쓰러졌어요! 💥\n"
    "쿵! 땅이 흔들렸어요.\n"
    "거인은 구름 위로 다시 올라갔어요.\n"
    "더 이상 내려올 수 없었어요.\n"
    "잭과 엄마는 서로 꼭 안았어요. 🤗\n"
    "\"잘했어, 잭!\" 엄마가 울면서 말했어요.\n"
    "잭은 금화로 음식을 사고 좋은 옷도 샀어요.\n"
    "더 이상 가난하지 않았어요! 💰\n"
    "잭은 엄마를 위해 용감하게 행동했어요.\n"
    "엄마를 지키기 위해 콩나무를 베었어요.\n"
    "잭은 진짜 영웅이 되었어요! 🦸\n"
    "<strong>잭은 엄마를 구하기 위해 콩나무를 찍어 넘어뜨렸어요! ❤️</strong>",
    # A1
    "The beanstalk fell down.\n"
    "The giant was gone.\n"
    "Jack saved his mother.\n"
    "Jack chopped it down to save his mother.",
    # A2
    "The beanstalk crashed and the ground shook like an earthquake.\n"
    "The giant could never come down again.\n"
    "Jack and Mother hugged each other and cried with joy.\n"
    "Jack chopped it down to save his mother from danger.\n"
    "With the gold coins, they were never poor again.\n"
    "Jack became a true hero who protected his family."
)

# ─── W14: She dropped her ball (Frog Prince begins) ───
STORIES["week14a"] = (
    "새로운 이야기! 개구리 왕자! 🐸\n"
    "옛날에 아름다운 공주가 살았어요.\n"
    "공주는 황금 공을 가지고 있었어요. ✨\n"
    "매일 성 옆 우물가에서 공놀이를 했어요.\n"
    "공을 높이 던지고 받는 것이 재미있었어요.\n"
    "어느 날 공주가 공을 던졌어요.\n"
    "그런데 공이 손에서 미끄러졌어요!\n"
    "통통통... 공이 우물 안으로 빠졌어요! 😱\n"
    "공주는 깜짝 놀랐어요.\n"
    "소중한 황금 공이 물속으로 사라졌어요.\n"
    "<strong>공주가 공을 떨어뜨렸어요! 😢</strong>",
    # A1
    "A princess had a golden ball.\n"
    "She played by the well.\n"
    "The ball fell in.\n"
    "She dropped her ball.",
    # A2
    "Once upon a time, a beautiful princess lived in a castle.\n"
    "She loved playing with her golden ball by the well.\n"
    "One day, the ball slipped out of her hands.\n"
    "She dropped her ball and it fell into the deep well.\n"
    "The princess was shocked and started to cry.\n"
    "Her precious golden ball disappeared into the dark water."
)

STORIES["week14b"] = (
    "공주는 우물가에 앉아서 울었어요. 😭\n"
    "\"내 황금 공... 어떡하지?\"\n"
    "우물은 너무 깊어서 손이 닿지 않았어요.\n"
    "눈물이 뚝뚝 떨어졌어요.\n"
    "황금 공은 세상에서 가장 소중한 보물이었어요. ✨\n"
    "아버지 왕이 선물로 주신 거였거든요.\n"
    "\"어떻게 하면 좋을까...\" 공주는 슬퍼했어요.\n"
    "아무도 도와줄 사람이 없었어요.\n"
    "우물 속은 깜깜하고 깊었어요.\n"
    "공주는 더 크게 울기 시작했어요.\n"
    "<strong>공주가 황금 공을 떨어뜨렸어요! 💔</strong>",
    # A1
    "The princess cried.\n"
    "The well was deep.\n"
    "She could not reach it.\n"
    "She dropped her golden ball.",
    # A2
    "The princess sat by the well and cried bitterly.\n"
    "She dropped her golden ball into the deep dark well.\n"
    "The well was too deep for her to reach the bottom.\n"
    "The golden ball was a special gift from her father.\n"
    "She did not know what to do without her treasure.\n"
    "Her tears fell into the water like little rain drops."
)

STORIES["week14c"] = (
    "공주는 하염없이 울고 있었어요. 😢\n"
    "눈물이 뺨을 타고 흘러내렸어요.\n"
    "\"내 소중한 공... 다시 볼 수 없는 걸까?\"\n"
    "우물 속은 깜깜했어요.\n"
    "공이 얼마나 깊이 빠졌는지 알 수 없었어요.\n"
    "공주의 울음소리가 숲속까지 퍼졌어요.\n"
    "새들도 슬퍼 보였어요. 🐦\n"
    "공주는 주저앉아서 계속 울었어요.\n"
    "혼자서는 아무것도 할 수 없었어요.\n"
    "바로 그때, 우물에서 작은 소리가 들렸어요...\n"
    "\"뭐지?\" 공주가 눈물을 닦았어요.\n"
    "<strong>공주가 공을 우물에 떨어뜨리고 울었어요! 💧</strong>",
    # A1
    "The ball fell in the well.\n"
    "She could not get it.\n"
    "She cried and cried.\n"
    "She dropped her ball into the well and cried.",
    # A2
    "The princess could not stop crying by the well.\n"
    "She dropped her ball into the well and cried for a long time.\n"
    "The well was dark and there was no way to reach the bottom.\n"
    "She felt helpless and alone in the garden.\n"
    "Then she heard a tiny splash from inside the well.\n"
    "Someone was about to come and help her."
)

# ─── W15: A frog came up ───
STORIES["week15a"] = (
    "공주가 울고 있을 때 우물에서 소리가 났어요. 🐸\n"
    "첨벙! 물이 튀었어요.\n"
    "작은 초록 개구리가 우물 위로 올라왔어요!\n"
    "\"왜 울고 있니, 공주님?\" 개구리가 물었어요.\n"
    "공주는 깜짝 놀랐어요. 😮\n"
    "\"개구리가 말을 하다니!\"\n"
    "개구리는 커다란 눈으로 공주를 바라봤어요.\n"
    "\"내가 도와줄 수 있어.\" 개구리가 말했어요.\n"
    "공주는 반가웠어요.\n"
    "드디어 도움을 줄 수 있는 누군가가 나타났어요!\n"
    "<strong>개구리가 나타났어요! 🐸</strong>",
    # A1
    "She heard a sound.\n"
    "It was a frog.\n"
    "The frog could talk.\n"
    "A frog came up.",
    # A2
    "While the princess was crying, she heard a splash.\n"
    "A small green frog climbed up from inside the well.\n"
    "A frog came up and asked why she was so sad.\n"
    "The princess was surprised that a frog could talk.\n"
    "The frog offered to help her get the golden ball back.\n"
    "The princess felt a tiny spark of hope in her heart."
)

STORIES["week15b"] = (
    "개구리가 우물 가장자리에 앉았어요. 🐸\n"
    "\"공주님, 나는 이 우물에 사는 개구리야.\"\n"
    "\"네 황금 공을 찾아줄 수 있어.\"\n"
    "공주는 눈이 반짝였어요. ✨\n"
    "\"정말? 내 공을 찾아줄 수 있어?\"\n"
    "\"그럼, 물론이지! 하지만...\" 개구리가 말했어요.\n"
    "개구리는 잠깐 멈추고 공주를 바라봤어요.\n"
    "\"한 가지 부탁이 있어.\"\n"
    "공주는 궁금해졌어요.\n"
    "\"뭔데?\" 공주가 물었어요.\n"
    "<strong>개구리가 나타나서 공주에게 말했어요! 💬</strong>",
    # A1
    "The frog sat by the well.\n"
    "He could find the ball.\n"
    "He wanted something.\n"
    "A frog came up and spoke to her.",
    # A2
    "The frog sat on the edge of the well and smiled.\n"
    "A frog came up and spoke to her about the golden ball.\n"
    "He said he could dive deep and bring it back.\n"
    "But the frog wanted something in return.\n"
    "The princess listened carefully to the little frog.\n"
    "She was willing to do anything to get her ball back."
)

STORIES["week15c"] = (
    "개구리는 천천히 말했어요. 🐸\n"
    "\"나는 이 어두운 우물에서 오래 살았어.\"\n"
    "\"외로웠어. 친구가 없었거든.\"\n"
    "공주는 개구리가 조금 불쌍했어요. 😔\n"
    "\"네 공을 찾아줄게. 대신...\"\n"
    "\"나의 친구가 되어줘.\"\n"
    "개구리의 눈이 반짝였어요.\n"
    "공주는 생각했어요.\n"
    "\"개구리가 친구라니... 조금 이상하지만...\"\n"
    "하지만 공이 너무 갖고 싶었어요! ✨\n"
    "개구리는 공주를 도와주려고 했어요.\n"
    "<strong>개구리가 물에서 나타나서 도와주겠다고 했어요! 🤝</strong>",
    # A1
    "The frog was lonely.\n"
    "He wanted a friend.\n"
    "He offered to help.\n"
    "A frog popped up and offered to help her.",
    # A2
    "The frog had lived alone in the dark well for a long time.\n"
    "He was lonely and wished for a friend more than anything.\n"
    "A frog popped up and offered to help her get the ball.\n"
    "In return, he asked the princess to be his friend.\n"
    "The princess thought it was strange but she wanted her ball.\n"
    "She needed to make a decision right away."
)

# ─── W16: She made a promise ───
STORIES["week16a"] = (
    "개구리가 말했어요. 🐸\n"
    "\"내가 공을 찾아줄게. 대신 약속해 줘.\"\n"
    "\"나의 친구가 되어줘. 밥도 같이 먹고, 함께 놀자.\"\n"
    "공주는 잠깐 망설였어요. 🤔\n"
    "\"개구리랑 밥을 같이 먹는다고?\"\n"
    "하지만 황금 공이 너무너무 갖고 싶었어요!\n"
    "\"알겠어! 약속할게!\" 공주가 말했어요.\n"
    "개구리는 기뻐하며 우물 속으로 풍덩 뛰어들었어요.\n"
    "공주는 약속을 했지만...\n"
    "정말로 지킬 마음이 있었을까요?\n"
    "<strong>공주가 약속을 했어요! 🤝</strong>",
    # A1
    "The frog asked for a promise.\n"
    "He wanted to be friends.\n"
    "She said yes.\n"
    "She made a promise.",
    # A2
    "The frog asked the princess to make a special promise.\n"
    "He wanted to eat with her and play with her every day.\n"
    "The princess really wanted her golden ball back.\n"
    "She made a promise to be the frog's friend.\n"
    "The frog happily jumped into the well to get the ball.\n"
    "But did the princess really mean her promise?"
)

STORIES["week16b"] = (
    "공주는 약속을 했어요. 🤝\n"
    "\"좋아, 네 친구가 되어줄게.\"\n"
    "개구리는 신이 나서 우물로 다이빙했어요! 💦\n"
    "첨벙! 물속으로 들어갔어요.\n"
    "한참 뒤에 개구리가 올라왔어요.\n"
    "입에 황금 공을 물고 있었어요! ✨\n"
    "\"여기! 네 공이야!\" 개구리가 말했어요.\n"
    "공주는 너무 기뻤어요.\n"
    "공을 잡자마자 성으로 뛰어갔어요. 🏃‍♀️\n"
    "\"기다려!\" 개구리가 소리쳤지만...\n"
    "<strong>공주는 개구리의 친구가 되겠다고 약속했어요! 💕</strong>",
    # A1
    "She promised the frog.\n"
    "The frog found the ball.\n"
    "She was happy.\n"
    "She promised to be his friend.",
    # A2
    "The princess agreed and made a deal with the frog.\n"
    "She promised to be his friend if he found the ball.\n"
    "The frog dived deep into the well and came back with it.\n"
    "The princess grabbed her golden ball and ran to the castle.\n"
    "She forgot about her promise to the little frog.\n"
    "The frog called after her but she did not look back."
)

STORIES["week16c"] = (
    "공주는 공을 받고 기뻐서 성으로 달려갔어요. 🏰\n"
    "\"잠깐! 약속은 어떡해!\" 개구리가 소리쳤어요. 🐸\n"
    "하지만 공주는 듣지 않았어요.\n"
    "\"개구리가 성까지 올 수 있겠어?\" 공주는 생각했어요.\n"
    "저녁 시간이 되었어요. 🍽️\n"
    "똑똑똑! 성 문을 두드리는 소리가 났어요.\n"
    "\"공주님! 약속을 지켜줘!\" 개구리였어요!\n"
    "왕이 물었어요. \"무슨 약속이니?\"\n"
    "공주는 얼굴이 빨개졌어요. 😳\n"
    "왕이 말했어요. \"약속은 꼭 지켜야 한단다.\"\n"
    "공주는 할 수 없이 문을 열어야 했어요.\n"
    "<strong>공주는 황금 공을 위해 개구리의 친구가 되겠다고 약속했어요! 🏅</strong>",
    # A1
    "She ran away.\n"
    "The frog came to the castle.\n"
    "The king said keep your promise.\n"
    "She promised to be his friend for her ball.",
    # A2
    "The princess took her ball and ran back to the castle.\n"
    "She forgot her promise but the frog followed her there.\n"
    "She promised to be his friend for her ball back.\n"
    "The frog knocked on the castle door at dinner time.\n"
    "The king told the princess she must keep her word.\n"
    "The princess had to let the frog come inside."
)

# ─── W17: The frog helped her ───
STORIES["week17a"] = (
    "개구리가 성 안에 들어왔어요. 🏰\n"
    "공주는 아직 개구리가 싫었어요.\n"
    "하지만 왕이 말했어요.\n"
    "\"약속은 꼭 지켜야 한다.\"\n"
    "개구리는 공주와 함께 밥을 먹었어요. 🍽️\n"
    "공주의 접시에서 조금씩 먹었어요.\n"
    "처음에는 불편했어요.\n"
    "하지만 개구리가 \"고마워\" 라고 말할 때\n"
    "공주의 마음이 조금 따뜻해졌어요. 💕\n"
    "개구리는 진심으로 고마워하고 있었어요.\n"
    "<strong>개구리가 공주를 도와줬어요! 🐸</strong>",
    # A1
    "The frog came inside.\n"
    "He ate with the princess.\n"
    "She started to like him.\n"
    "The frog helped her.",
    # A2
    "The frog entered the castle and sat at the dinner table.\n"
    "The princess did not like it at first.\n"
    "But the king reminded her about keeping promises.\n"
    "The frog helped her understand the meaning of kindness.\n"
    "He was polite and thankful for every small thing.\n"
    "Slowly, the princess started to feel warm toward the frog."
)

STORIES["week17b"] = (
    "날이 지나면서 공주는 변하기 시작했어요. 🌸\n"
    "개구리는 항상 친절하고 예의 바랐어요.\n"
    "\"좋은 아침이야, 공주님!\" 🐸\n"
    "\"오늘 기분이 어때?\"\n"
    "공주는 처음으로 개구리에게 미소를 지었어요.\n"
    "\"고마워, 개구리야.\"\n"
    "개구리와 함께 시간을 보내는 것이 나쁘지 않았어요.\n"
    "개구리는 재미있는 이야기도 해줬어요.\n"
    "공주는 약속을 지키는 것이 중요하다는 걸 배웠어요. 💡\n"
    "개구리 덕분에 더 좋은 사람이 되어가고 있었어요.\n"
    "<strong>개구리가 약속을 지키도록 도와줬어요! 🤝</strong>",
    # A1
    "The frog was kind.\n"
    "They spent time together.\n"
    "She learned about promises.\n"
    "The frog helped her keep the promise.",
    # A2
    "Days passed and the princess started changing her heart.\n"
    "The frog was always kind, polite, and cheerful.\n"
    "The frog helped her keep the promise she had made.\n"
    "He showed her what real friendship means.\n"
    "The princess smiled at the frog for the first time.\n"
    "She was becoming a better person thanks to the frog."
)

STORIES["week17c"] = (
    "공주와 개구리는 이제 진짜 친구가 되었어요. 🐸💕\n"
    "매일 함께 놀고, 함께 이야기했어요.\n"
    "공주는 이제 개구리를 좋아했어요.\n"
    "\"너 없으면 심심할 것 같아.\"\n"
    "개구리의 눈에 눈물이 고였어요.\n"
    "\"정말? 나를 진짜 친구로 생각해?\" 😊\n"
    "\"응, 진짜야. 네가 약속을 지키라고 도와줘서 고마워.\"\n"
    "공주는 깨달았어요.\n"
    "약속을 지켰기 때문에 진짜 친구를 얻은 거예요.\n"
    "개구리가 약속의 소중함을 가르쳐줬어요.\n"
    "<strong>개구리가 도와준 이유는 공주가 약속을 지켰기 때문이에요! 💝</strong>",
    # A1
    "They became friends.\n"
    "She kept her promise.\n"
    "The frog was happy.\n"
    "The frog helped because she kept her promise.",
    # A2
    "The princess and the frog became true friends over time.\n"
    "They played together and talked every single day.\n"
    "The frog helped because she kept her promise to him.\n"
    "The princess learned that keeping promises brings real friends.\n"
    "She was grateful to the frog for teaching her this lesson.\n"
    "Something magical was about to happen because of her kindness."
)

# ─── W18: He became a prince ───
STORIES["week18a"] = (
    "어느 날 저녁, 놀라운 일이 일어났어요! ✨\n"
    "공주가 개구리에게 진심으로 말했어요.\n"
    "\"넌 나의 소중한 친구야.\"\n"
    "그 순간! 반짝! 빛이 번쩍였어요! 💫\n"
    "개구리의 몸이 변하기 시작했어요.\n"
    "초록색 피부가 사라지고...\n"
    "멋진 왕자가 나타났어요! 👑\n"
    "공주는 눈이 휘둥그레졌어요.\n"
    "\"어... 어떻게 된 거야?!\"\n"
    "왕자가 미소를 지었어요.\n"
    "<strong>개구리가 왕자가 되었어요! 🤴</strong>",
    # A1
    "A light flashed.\n"
    "The frog changed.\n"
    "He was a prince.\n"
    "He became a prince.",
    # A2
    "One evening, the princess said something kind from her heart.\n"
    "Suddenly, a bright light surrounded the little frog.\n"
    "His body started changing right before her eyes.\n"
    "He became a prince, tall and handsome.\n"
    "The princess could not believe what was happening.\n"
    "The magic spell was finally broken by her true kindness."
)

STORIES["week18b"] = (
    "왕자가 이야기를 해줬어요. 🤴\n"
    "\"나는 원래 이웃 나라의 왕자였어.\"\n"
    "\"나쁜 마녀가 저주를 걸어서 개구리가 되었지.\" 🐸\n"
    "\"진심 어린 친절을 받아야 저주가 풀리는 거였어.\"\n"
    "공주는 놀라서 물었어요.\n"
    "\"내가 친절했기 때문에 저주가 풀린 거야?\"\n"
    "\"그래, 네 진심이 나를 구해줬어.\" ✨\n"
    "왕자는 정말 잘생기고 마음도 따뜻했어요.\n"
    "공주의 친절이 마법을 깨뜨린 거예요.\n"
    "두 사람은 활짝 웃었어요. 😊\n"
    "<strong>개구리가 잘생긴 왕자가 되었어요! 👑</strong>",
    # A1
    "The prince told his story.\n"
    "A witch cursed him.\n"
    "Kindness broke the spell.\n"
    "He became a handsome prince.",
    # A2
    "The prince explained that a witch had cursed him long ago.\n"
    "Only true kindness could break the magic spell.\n"
    "He became a handsome prince thanks to the princess.\n"
    "Her genuine friendship melted the witch's dark magic.\n"
    "The prince was from a kingdom far away.\n"
    "He thanked the princess for giving him a second chance."
)

STORIES["week18c"] = (
    "왕자와 공주는 행복하게 살았어요. 💕\n"
    "온 나라가 기뻐했어요.\n"
    "왕도 왕비도 미소를 지었어요. 👑\n"
    "\"우리 딸이 약속을 지켜서 좋은 일이 생겼구나.\"\n"
    "공주는 중요한 것을 배웠어요.\n"
    "약속을 지키면 좋은 일이 생긴다는 거예요.\n"
    "친절은 마법처럼 놀라운 힘이 있어요. ✨\n"
    "작은 개구리에게도 친절하면\n"
    "놀라운 변화가 일어날 수 있어요.\n"
    "이것이 개구리 왕자 이야기의 교훈이에요.\n"
    "친절이 세상을 바꿔요! 🌈\n"
    "<strong>개구리가 친절 덕분에 왕자가 되었어요! 🐸➡️🤴</strong>",
    # A1
    "They lived happily.\n"
    "Kindness was the magic.\n"
    "The frog was now a prince.\n"
    "The frog became a prince because of kindness.",
    # A2
    "The prince and princess became the best of friends.\n"
    "The whole kingdom celebrated the magical transformation.\n"
    "The frog became a prince because of kindness and love.\n"
    "The princess learned that keeping promises is very important.\n"
    "She also learned that kindness can create real magic.\n"
    "They all lived happily ever after in the castle."
)

# ─── W19: He cut the leather (Elves & Shoemaker) ───
STORIES["week19a"] = (
    "새로운 이야기! 요정과 구두장이! 🧵\n"
    "옛날에 가난한 구두장이가 살았어요.\n"
    "구두를 만들어서 팔았지만 돈이 부족했어요.\n"
    "이제 가죽이 딱 한 장만 남았어요. 😔\n"
    "\"이 가죽으로 마지막 구두를 만들어야 해.\"\n"
    "구두장이는 가위를 들었어요. ✂️\n"
    "조심조심 가죽을 잘랐어요.\n"
    "예쁜 구두 모양으로 잘랐어요.\n"
    "\"내일 아침에 꿰매야겠다.\"\n"
    "구두장이는 잘라놓은 가죽을 탁자 위에 놓고 잠들었어요.\n"
    "<strong>구두장이가 가죽을 잘랐어요! ✂️</strong>",
    # A1
    "A shoemaker was poor.\n"
    "He had one piece of leather.\n"
    "He used scissors.\n"
    "He cut the leather.",
    # A2
    "Once upon a time, a poor shoemaker lived in a small shop.\n"
    "He only had one last piece of leather left.\n"
    "He cut the leather carefully into the shape of shoes.\n"
    "He planned to finish sewing them the next morning.\n"
    "He left the pieces on his workbench and went to sleep.\n"
    "He did not know something magical would happen that night."
)

STORIES["week19b"] = (
    "구두장이는 피곤했어요. 😴\n"
    "온종일 일해서 눈이 감겼어요.\n"
    "\"내일 아침에 꿰매면 돼.\"\n"
    "구두장이는 가죽을 잘라놓고 생각했어요.\n"
    "\"이 구두가 팔리면 빵을 살 수 있을 거야.\" 🍞\n"
    "가죽을 꼼꼼하게 잘랐어요.\n"
    "밤이 깊어지고 달이 떠올랐어요. 🌙\n"
    "구두장이는 잠에 빠졌어요.\n"
    "조용한 밤, 작업대 위에 가죽만 남아 있었어요.\n"
    "그런데 그날 밤 무슨 일이 일어날 거예요.\n"
    "<strong>구두장이가 밤에 가죽을 잘랐어요! 🌙</strong>",
    # A1
    "The shoemaker was tired.\n"
    "He cut the leather.\n"
    "He went to sleep.\n"
    "He cut the leather at night.",
    # A2
    "The tired shoemaker worked until late in the evening.\n"
    "He cut the leather at night under the dim candlelight.\n"
    "He shaped the pieces perfectly for a pair of shoes.\n"
    "He hoped someone would buy them the next day.\n"
    "The moon was bright as he placed the leather on the table.\n"
    "He fell asleep not knowing a surprise was waiting for him."
)

STORIES["week19c"] = (
    "구두장이의 하루를 돌아봐요. 📖\n"
    "아침부터 가게를 열었지만 손님이 없었어요.\n"
    "남은 가죽은 딱 한 장뿐이에요.\n"
    "\"이걸로 마지막이구나...\" 구두장이는 한숨을 쉬었어요. 😔\n"
    "하지만 포기하지 않았어요!\n"
    "가위를 들고 정성스럽게 가죽을 잘랐어요. ✂️\n"
    "\"최선을 다하자.\"\n"
    "구두 모양으로 예쁘게 잘라놓았어요.\n"
    "내일 꿰매서 완성할 준비를 했어요.\n"
    "그리고 가죽을 탁자 위에 올려놓았어요.\n"
    "작은 소망을 가지고 잠이 들었어요. 🌟\n"
    "<strong>먼저, 구두장이가 가죽을 잘라서 준비해 놓았어요! 🧵</strong>",
    # A1
    "The shoemaker did not give up.\n"
    "He prepared the leather.\n"
    "He left it on the table.\n"
    "First, he cut the leather and left it ready.",
    # A2
    "The shoemaker had only one chance left to make shoes.\n"
    "He did not give up even though he was very poor.\n"
    "First, he cut the leather and left it ready on the table.\n"
    "He shaped each piece with great care and love.\n"
    "He placed everything neatly and went to bed.\n"
    "Something wonderful was about to happen while he slept."
)

# ─── W20: Elves came at night ───
STORIES["week20a"] = (
    "다음 날 아침, 구두장이가 일어났어요. ☀️\n"
    "작업대로 갔더니... 세상에! 😮\n"
    "구두가 이미 완성되어 있었어요!\n"
    "바느질도 완벽하고, 모양도 예뻤어요.\n"
    "\"이게 어떻게 된 거지?!\"\n"
    "구두장이는 눈을 비비며 다시 봤어요.\n"
    "정말로 아름다운 구두 한 켤레가 있었어요! 👞✨\n"
    "\"누가 만든 거지?\"\n"
    "구두장이는 이해할 수 없었어요.\n"
    "그날 구두가 바로 팔렸어요! 💰\n"
    "<strong>요정들이 밤에 왔어요! 🧝</strong>",
    # A1
    "He woke up.\n"
    "The shoes were done.\n"
    "He was surprised.\n"
    "Elves came at night.",
    # A2
    "The next morning, the shoemaker found a beautiful surprise.\n"
    "The shoes were already finished perfectly on the table.\n"
    "He could not believe his eyes because the work was amazing.\n"
    "Elves came at night and made the shoes while he slept.\n"
    "A customer came and bought the shoes right away.\n"
    "The shoemaker was so happy and bought more leather."
)

STORIES["week20b"] = (
    "구두장이는 너무 궁금했어요. 🤔\n"
    "\"밤에 누가 구두를 만든 거지?\"\n"
    "다음 날도 가죽을 잘라놓고 잠을 잤어요.\n"
    "아침에 일어나보니 또 구두가 완성되어 있었어요! 😮\n"
    "이번에는 두 켤레나!\n"
    "\"정말 신기하다!\"\n"
    "구두장이의 아내가 말했어요.\n"
    "\"오늘 밤에 몰래 보자!\" 👀\n"
    "밤에 두 사람은 옷장 뒤에 숨었어요.\n"
    "자정이 되자 작은 요정 두 명이 나타났어요! 🧝✨\n"
    "<strong>요정들이 와서 구두를 만들었어요! 👞</strong>",
    # A1
    "He left leather again.\n"
    "More shoes appeared.\n"
    "He hid and watched.\n"
    "The elves came and made shoes.",
    # A2
    "The shoemaker was curious about who helped him.\n"
    "He left leather out again and the same thing happened.\n"
    "The elves came and made shoes every single night.\n"
    "He and his wife decided to hide and watch one night.\n"
    "At midnight, two tiny elves appeared and started sewing.\n"
    "They worked quickly with their tiny hands until dawn."
)

STORIES["week20c"] = (
    "요정들은 정말 대단했어요! 🧝\n"
    "손이 작지만 엄청나게 빠르게 일했어요.\n"
    "바느질도 완벽하고 구두도 아름다웠어요.\n"
    "구두장이와 아내는 감동했어요. 😢\n"
    "\"이 작은 요정들 덕분에 우리가 살았어.\"\n"
    "요정들은 아무 말 없이 구두를 만들었어요.\n"
    "새벽이 되면 조용히 사라졌어요. ✨\n"
    "밤마다 찾아와서 열심히 일해줬어요.\n"
    "구두장이는 감사한 마음이 가득했어요.\n"
    "요정들을 위해 무언가 해주고 싶었어요. 💕\n"
    "<strong>그리고 작은 요정들이 구두장이가 자는 동안 구두를 만들었어요! 🌙</strong>",
    # A1
    "The elves were tiny.\n"
    "They sewed very fast.\n"
    "The shoes were perfect.\n"
    "Then, the little elves made shoes while he slept.",
    # A2
    "The shoemaker and his wife watched the elves with amazement.\n"
    "The tiny elves had no shoes or warm clothes of their own.\n"
    "Then, the little elves made shoes while he slept peacefully.\n"
    "Their tiny fingers moved quickly and skillfully all night.\n"
    "The shoemaker felt grateful and wanted to thank them.\n"
    "He decided to make something special for the elves."
)

# ─── W21: He became rich ───
STORIES["week21a"] = (
    "요정들 덕분에 구두장이의 가게가 유명해졌어요! 👞\n"
    "사람들이 구두를 사러 줄을 섰어요.\n"
    "\"이 구두 정말 멋있어요!\" 💰\n"
    "구두장이는 돈을 많이 벌었어요.\n"
    "가죽도 더 많이 살 수 있었어요.\n"
    "가게도 더 크게 만들었어요.\n"
    "예전에는 가난했지만 이제는 부자가 되었어요! 🎉\n"
    "구두장이는 행복했어요.\n"
    "하지만 요정들이 제일 고마웠어요.\n"
    "요정들이 없었으면 이런 일은 없었을 거예요.\n"
    "<strong>구두장이가 부자가 되었어요! 💎</strong>",
    # A1
    "Many people came.\n"
    "They bought the shoes.\n"
    "He made a lot of money.\n"
    "He became rich.",
    # A2
    "The shoemaker's shop became famous in the whole town.\n"
    "People lined up every day to buy his beautiful shoes.\n"
    "He earned more money than he ever imagined.\n"
    "He became rich and could buy anything he needed.\n"
    "But he never forgot the little elves who helped him.\n"
    "He was thankful every single day for their kindness."
)

STORIES["week21b"] = (
    "구두장이는 부자가 되었지만 욕심부리지 않았어요. 😊\n"
    "\"요정들에게 감사해야 해.\"\n"
    "아내와 함께 요정들을 위한 선물을 만들었어요.\n"
    "작고 예쁜 옷과 작은 구두를 만들었어요! 👗👞\n"
    "밤에 선물을 탁자 위에 놓았어요.\n"
    "요정들이 와서 선물을 발견했어요.\n"
    "\"우와! 우리한테 옷이다!\" 요정들이 기뻐했어요. 🎉\n"
    "예쁜 옷을 입고 춤을 추었어요.\n"
    "요정들은 행복하게 숲으로 돌아갔어요.\n"
    "구두장이도 행복했어요.\n"
    "<strong>구두장이는 부자가 되었고 행복했어요! 😄</strong>",
    # A1
    "He made gifts for the elves.\n"
    "The elves were happy.\n"
    "Everyone was glad.\n"
    "He became rich and happy.",
    # A2
    "The shoemaker wanted to thank the elves for everything.\n"
    "He and his wife made tiny clothes and shoes for them.\n"
    "The elves found the gifts and danced with pure joy.\n"
    "He became rich and happy because he was grateful.\n"
    "The elves never came back, but he always remembered them.\n"
    "His kindness and gratitude filled his heart with warmth."
)

STORIES["week21c"] = (
    "구두장이의 이야기에서 우리는 배워요. 📖\n"
    "처음에 구두장이는 매우 가난했어요.\n"
    "하지만 포기하지 않고 최선을 다했어요.\n"
    "작은 요정들이 몰래 도와줬어요. 🧝\n"
    "구두장이는 감사하는 마음을 잊지 않았어요.\n"
    "요정들에게 선물을 만들어줬어요. 🎁\n"
    "도움을 받으면 감사해야 해요.\n"
    "남에게 도움을 주면 좋은 일이 생겨요.\n"
    "구두장이는 부자가 되었지만\n"
    "가장 소중한 것은 감사하는 마음이었어요.\n"
    "이것이 이 이야기의 교훈이에요! 💕\n"
    "<strong>마침내, 요정들이 도와준 덕분에 구두장이는 부자가 되었어요! 🌟</strong>",
    # A1
    "The elves helped him.\n"
    "He thanked them.\n"
    "He was rich now.\n"
    "Finally, he was rich because the elves helped him.",
    # A2
    "The shoemaker started with nothing but one piece of leather.\n"
    "The elves came every night and helped him make shoes.\n"
    "Finally, he was rich because the elves helped him.\n"
    "He showed his gratitude by making gifts for them.\n"
    "The lesson of this story is about kindness and thankfulness.\n"
    "When we help others, wonderful things happen in return."
)

# ─── W22: Thumbelina — She was very small ───
STORIES["week22a"] = (
    "새로운 이야기! 엄지공주! 🌸\n"
    "옛날에 아이를 원하는 여자가 살았어요.\n"
    "마법사에게 씨앗을 하나 받았어요.\n"
    "씨앗을 화분에 심었더니 꽃이 피었어요! 🌷\n"
    "꽃잎이 하나씩 벌어지자...\n"
    "그 안에 아주 작은 소녀가 있었어요!\n"
    "엄지손가락보다 더 작았어요. 👍\n"
    "\"어머나! 정말 작구나!\"\n"
    "여자는 소녀를 '엄지공주'라고 불렀어요.\n"
    "엄지공주는 작지만 아름다웠어요. ✨\n"
    "<strong>엄지공주는 아주 작았어요! 🌸</strong>",
    # A1
    "A flower opened.\n"
    "A tiny girl was inside.\n"
    "She was so small.\n"
    "She was very small.",
    # A2
    "A woman planted a magic seed in a flower pot.\n"
    "A beautiful flower bloomed and a tiny girl was inside.\n"
    "She was very small, even smaller than a thumb.\n"
    "The woman named her Thumbelina and loved her dearly.\n"
    "Thumbelina slept in a walnut shell every night.\n"
    "She was tiny but she had a brave and kind heart."
)

STORIES["week22b"] = (
    "엄지공주는 정말 작은 세상에서 살았어요. 🏠\n"
    "침대는 호두 껍데기였어요.\n"
    "이불은 꽃잎이었어요. 🌺\n"
    "접시는 단추만큼 작았어요.\n"
    "엄지공주는 엄지손가락만 했어요.\n"
    "하지만 목소리는 아름다웠어요.\n"
    "매일 노래를 불렀어요. 🎵\n"
    "새들도 엄지공주의 노래를 좋아했어요.\n"
    "엄마는 엄지공주를 너무 사랑했어요.\n"
    "작지만 특별한 소녀였어요.\n"
    "<strong>엄지공주는 엄지손가락만큼 작았어요! 👍</strong>",
    # A1
    "Thumbelina was tiny.\n"
    "Her bed was a walnut.\n"
    "She sang pretty songs.\n"
    "She was as small as a thumb.",
    # A2
    "Thumbelina lived in a tiny world made just for her.\n"
    "She was as small as a thumb and slept in a walnut shell.\n"
    "Her blanket was a soft flower petal from the garden.\n"
    "She loved to sing and the birds listened to her songs.\n"
    "Her mother cared for her and kept her warm and safe.\n"
    "But Thumbelina dreamed of seeing the big world outside."
)

STORIES["week22c"] = (
    "엄지공주는 매일 행복하게 지냈어요. 😊\n"
    "꽃잎 위에서 놀고, 이슬방울로 세수했어요. 💧\n"
    "나비와 친구가 되었어요. 🦋\n"
    "하지만 밤이 되면 조금 외로웠어요.\n"
    "\"세상에는 나만큼 작은 친구가 있을까?\"\n"
    "엄지공주는 궁금했어요.\n"
    "작은 몸이지만 꿈은 컸어요.\n"
    "언젠가 넓은 세상을 보고 싶었어요.\n"
    "엄지공주의 모험이 곧 시작될 거예요.\n"
    "작지만 용감한 소녀의 이야기!\n"
    "<strong>엄지공주는 정말 작았어요 — 엄지손가락보다도 작았어요! 🌷</strong>",
    # A1
    "Thumbelina played with butterflies.\n"
    "She was very very tiny.\n"
    "She dreamed of adventure.\n"
    "She was tiny, no bigger than a thumb.",
    # A2
    "Thumbelina spent happy days playing with butterflies.\n"
    "She washed her face with morning dew drops.\n"
    "She was tiny, no bigger than a thumb in the garden.\n"
    "At night, she wondered if there were others like her.\n"
    "She dreamed of exploring the wide, beautiful world.\n"
    "Soon, an unexpected adventure would find the tiny girl."
)

# ─── W23: She floated away ───
STORIES["week23a"] = (
    "어느 날 밤, 무서운 일이 일어났어요! 😱\n"
    "커다란 두꺼비가 창문으로 들어왔어요. 🐸\n"
    "엄지공주가 자고 있을 때\n"
    "두꺼비가 엄지공주를 데리고 갔어요!\n"
    "연못 한가운데 연잎 위에 놓았어요.\n"
    "\"내 아들의 신부로 딱이야!\" 두꺼비가 말했어요.\n"
    "아침에 엄지공주가 눈을 떴어요.\n"
    "\"여기가 어디야?!\" 😰\n"
    "주위에 물만 있었어요.\n"
    "엄지공주는 울기 시작했어요.\n"
    "<strong>엄지공주는 떠내려갔어요! 🍃</strong>",
    # A1
    "A toad took her.\n"
    "She was on a leaf.\n"
    "She was scared.\n"
    "She floated away.",
    # A2
    "One night, a big ugly toad stole little Thumbelina.\n"
    "She woke up on a lily pad in the middle of a pond.\n"
    "The toad wanted her to marry her son.\n"
    "She floated away on the lily pad crying for help.\n"
    "Tiny fish felt sorry for her and nibbled the stem.\n"
    "The lily pad broke free and carried her down the stream."
)

STORIES["week23b"] = (
    "엄지공주는 연잎 위에서 떠내려가고 있었어요. 🍃\n"
    "물고기들이 줄기를 끊어줘서 자유로워졌어요.\n"
    "하지만 어디로 가는지 몰랐어요.\n"
    "물살이 엄지공주를 계속 데려갔어요. 🌊\n"
    "\"엄마... 보고 싶어...\" 엄지공주가 울었어요. 😢\n"
    "나비가 날아와서 위로해줬어요. 🦋\n"
    "\"울지 마. 괜찮을 거야.\"\n"
    "하지만 엄지공주는 너무 외로웠어요.\n"
    "혼자서 연잎 위에 떠 있었어요.\n"
    "어디로 가는지 아무도 몰랐어요.\n"
    "<strong>엄지공주는 혼자서 연잎 위에 떠 있었어요! 😔</strong>",
    # A1
    "She was on the water.\n"
    "She missed her home.\n"
    "A butterfly came.\n"
    "She floated on a leaf alone.",
    # A2
    "The lily pad carried Thumbelina down the winding stream.\n"
    "She floated on a leaf alone, missing her mother.\n"
    "A kind butterfly flew beside her to keep her company.\n"
    "The water moved slowly and the world seemed so big.\n"
    "Thumbelina felt small and lonely on the open water.\n"
    "She did not know where the stream would take her."
)

STORIES["week23c"] = (
    "엄지공주는 계속 물 위를 떠다녔어요. 🍃\n"
    "개울이 강이 되고, 강은 더 넓어졌어요.\n"
    "예쁜 풍경이 지나갔어요.\n"
    "꽃도 보이고 나무도 보였어요. 🌿\n"
    "하지만 엄지공주는 슬펐어요.\n"
    "집으로 돌아가고 싶었거든요.\n"
    "해가 지고 어두워지기 시작했어요. 🌅\n"
    "추워지기 시작했어요.\n"
    "엄지공주는 연잎을 꼭 잡았어요.\n"
    "\"포기하지 않을 거야!\"\n"
    "작은 소녀의 큰 용기!\n"
    "<strong>엄지공주는 연잎을 타고 강을 따라 떠내려갔어요! 🌊</strong>",
    # A1
    "She went down the river.\n"
    "It was getting cold.\n"
    "She held on tight.\n"
    "She floated down the river on a lily leaf.",
    # A2
    "The stream carried Thumbelina further and further from home.\n"
    "She floated down the river on a lily leaf all day.\n"
    "Beautiful flowers and tall trees passed by on both sides.\n"
    "As the sun set, the air became cold and dark.\n"
    "Thumbelina held onto the leaf and refused to give up.\n"
    "She was tiny but her courage was bigger than her size."
)

# ─── W24: She found a home ───
STORIES["week24a"] = (
    "엄지공주는 오래 떠돌아다녔어요. 😔\n"
    "겨울이 다가오고 있었어요. ❄️\n"
    "춥고 배고프고 지쳤어요.\n"
    "그때 작은 들쥐 아주머니를 만났어요. 🐭\n"
    "들쥐는 친절했어요.\n"
    "\"이 추운 날에 혼자 있으면 안 되지!\"\n"
    "따뜻한 땅속 집으로 데려가줬어요.\n"
    "따뜻한 수프도 줬어요. 🍲\n"
    "엄지공주는 감사했어요.\n"
    "드디어 쉴 곳을 찾았어요.\n"
    "<strong>엄지공주는 집을 찾았어요! 🏠</strong>",
    # A1
    "Winter was coming.\n"
    "She met a kind mouse.\n"
    "The mouse helped her.\n"
    "She found a home.",
    # A2
    "Thumbelina wandered alone until winter was near.\n"
    "She was cold, hungry, and very tired.\n"
    "A kind field mouse invited her into her warm home.\n"
    "She found a home and ate warm soup for the first time.\n"
    "The field mouse took care of her through the cold days.\n"
    "Thumbelina was grateful to finally have a safe place."
)

STORIES["week24b"] = (
    "들쥐 아주머니의 집은 따뜻했어요. 🏠\n"
    "엄지공주는 겨울 동안 편안하게 지냈어요.\n"
    "봄이 오자 다친 제비를 발견했어요. 🐦\n"
    "엄지공주는 제비를 정성껏 돌봐줬어요.\n"
    "\"고마워!\" 제비가 나으면서 말했어요.\n"
    "\"네가 원하면 따뜻한 나라로 데려갈게.\"\n"
    "엄지공주는 제비의 등에 올라탔어요! ✨\n"
    "높이높이 하늘을 날았어요.\n"
    "따뜻한 나라에 도착했어요! ☀️\n"
    "그곳에는 꽃이 가득했어요.\n"
    "<strong>엄지공주는 따뜻하고 안전한 집을 찾았어요! 🌞</strong>",
    # A1
    "She helped a bird.\n"
    "The bird flew her away.\n"
    "They went to a warm land.\n"
    "She found a warm and safe home.",
    # A2
    "Thumbelina spent the winter in the field mouse's warm home.\n"
    "In spring, she found a hurt swallow and nursed him.\n"
    "The swallow promised to take her somewhere beautiful.\n"
    "She found a warm and safe home in a sunny land.\n"
    "The swallow carried her on his back over mountains.\n"
    "They arrived in a land full of sunshine and flowers."
)

STORIES["week24c"] = (
    "따뜻한 나라에서 놀라운 일이 일어났어요! 🌺\n"
    "꽃 속에서 작은 왕자가 나타났어요! 👑\n"
    "엄지공주만큼 작았어요.\n"
    "\"나는 꽃 나라의 왕자야. 함께 살지 않을래?\"\n"
    "엄지공주는 너무 기뻤어요. 😊\n"
    "드디어 자기처럼 작은 친구를 만났어요!\n"
    "왕자가 예쁜 날개를 선물해줬어요. 🦋\n"
    "엄지공주는 이제 행복하게 살 수 있어요.\n"
    "오랜 모험 끝에 찾은 진짜 집!\n"
    "엄지공주는 더 이상 외롭지 않아요. 💕\n"
    "작은 소녀의 큰 모험이 행복한 결말을 맞이했어요!\n"
    "<strong>마침내, 엄지공주는 안전하고 행복한 집을 찾았어요! 🌈</strong>",
    # A1
    "She met a tiny prince.\n"
    "They became friends.\n"
    "She was finally happy.\n"
    "At last, she found a safe and happy home.",
    # A2
    "In the warm land, Thumbelina met a tiny flower prince.\n"
    "He was exactly her size and gave her beautiful wings.\n"
    "At last, she found a safe and happy home forever.\n"
    "She was no longer alone or cold or afraid.\n"
    "Her long adventure taught her about courage and kindness.\n"
    "Thumbelina lived happily ever after with her new friends."
)

# ─── W25: He loved fine clothes (Emperor's New Clothes) ───
STORIES["week25a"] = (
    "새로운 이야기! 임금님의 새 옷! 👑\n"
    "옛날에 옷을 아주 좋아하는 임금님이 살았어요.\n"
    "매일 새 옷을 입었어요.\n"
    "옷장이 방 세 개만큼 컸어요! 👔\n"
    "비단옷, 금실옷, 보석 달린 옷...\n"
    "나라를 다스리는 것보다 옷이 더 중요했어요.\n"
    "\"오늘은 어떤 옷을 입을까?\"\n"
    "매일 아침 거울 앞에서 시간을 보냈어요. 🪞\n"
    "신하들은 한숨을 쉬었어요.\n"
    "임금님은 옷에만 관심이 있었거든요.\n"
    "<strong>임금님은 좋은 옷을 사랑했어요! 👑</strong>",
    # A1
    "A king loved clothes.\n"
    "He had many outfits.\n"
    "Clothes were his favorite.\n"
    "He loved fine clothes.",
    # A2
    "Once upon a time, there was an emperor who loved fashion.\n"
    "He spent all his money on beautiful new clothes.\n"
    "He loved fine clothes more than ruling his kingdom.\n"
    "His wardrobe was bigger than most people's houses.\n"
    "Every morning, he tried on outfit after outfit.\n"
    "The people wished he would care more about the kingdom."
)

STORIES["week25b"] = (
    "어느 날 두 사기꾼이 나라에 왔어요. 🎭\n"
    "\"저희는 세계 최고의 직물공이에요!\"\n"
    "\"마법의 천을 짤 수 있어요.\"\n"
    "임금님의 귀가 쫑긋 세워졌어요. 👂\n"
    "\"마법의 천? 그게 뭐야?\"\n"
    "\"어리석은 사람에게는 보이지 않는 천이에요!\" 🪄\n"
    "임금님은 너무 신이 났어요.\n"
    "\"당장 만들어라!\"\n"
    "사기꾼들은 빈 베틀 앞에서 일하는 척했어요.\n"
    "실은 아무것도 짜지 않았어요!\n"
    "<strong>임금님은 아름다운 옷을 누구보다 사랑했어요! 💎</strong>",
    # A1
    "Two men came.\n"
    "They said they could weave magic cloth.\n"
    "The emperor was excited.\n"
    "The emperor loved beautiful clothes very much.",
    # A2
    "Two swindlers came to the kingdom with a clever trick.\n"
    "They said they could weave cloth invisible to fools.\n"
    "The emperor loved beautiful clothes very much and got excited.\n"
    "He gave them gold and silk to make the special fabric.\n"
    "The swindlers pretended to weave but made nothing at all.\n"
    "Everyone was too afraid to say they could not see anything."
)

STORIES["week25c"] = (
    "사기꾼들은 계속 일하는 척했어요. 🧵\n"
    "빈 베틀 앞에서 손을 움직였어요.\n"
    "임금님이 신하를 보내서 확인하게 했어요.\n"
    "신하가 갔더니... 아무것도 안 보였어요! 😰\n"
    "\"나는 어리석은 사람인가?\" 신하는 겁이 났어요.\n"
    "\"아주 아름다운 천이네요!\" 거짓말을 했어요.\n"
    "또 다른 신하도 같은 거짓말을 했어요.\n"
    "임금님도 직접 보러 갔어요. 👑\n"
    "역시 아무것도 안 보였어요!\n"
    "하지만 임금님도 어리석어 보이기 싫었어요.\n"
    "\"훌륭하다!\" 임금님도 거짓말을 했어요.\n"
    "<strong>임금님은 무엇보다 좋은 옷을 사랑했어요! 🏆</strong>",
    # A1
    "The cloth was invisible.\n"
    "No one could see it.\n"
    "But they all lied.\n"
    "The emperor loved fine clothes more than anything.",
    # A2
    "The swindlers pretended to weave on an empty loom.\n"
    "The emperor sent his best minister to check the cloth.\n"
    "The minister saw nothing but was too afraid to say so.\n"
    "The emperor loved fine clothes more than anything in the world.\n"
    "He visited the weavers himself and also saw nothing.\n"
    "But nobody dared to tell the truth about the invisible cloth."
)

# ─── W26: No one spoke up ───
STORIES["week26a"] = (
    "드디어 옷이 완성되었다고 사기꾼들이 말했어요! 🎭\n"
    "\"임금님, 새 옷이 완성되었습니다!\"\n"
    "사기꾼들은 빈 손으로 옷을 입혀주는 척했어요.\n"
    "임금님은 거울 앞에 섰어요. 🪞\n"
    "아무것도 안 보이지만...\n"
    "\"어리석어 보일 순 없어!\" 임금님은 생각했어요.\n"
    "\"정말 아름답구나!\" 임금님이 말했어요.\n"
    "신하들도 모두 칭찬했어요.\n"
    "하지만 모두 진실을 알고 있었어요. 😶\n"
    "아무도 솔직하게 말하지 못했어요.\n"
    "<strong>아무도 사실대로 말하지 않았어요! 🤐</strong>",
    # A1
    "The emperor wore nothing.\n"
    "Everyone pretended.\n"
    "They were all afraid.\n"
    "No one spoke up.",
    # A2
    "The swindlers pretended to dress the emperor in new clothes.\n"
    "The emperor stood in front of the mirror wearing nothing.\n"
    "All the ministers praised the beautiful invisible cloth.\n"
    "No one spoke up because they were afraid of looking foolish.\n"
    "Everyone kept the secret and told the same lie.\n"
    "The emperor decided to parade through the town."
)

STORIES["week26b"] = (
    "임금님이 행진을 시작했어요! 🎺\n"
    "온 나라 사람들이 거리에 모였어요.\n"
    "임금님은 당당하게 걸었어요.\n"
    "사실은 아무것도 안 입고 있었는데! 😳\n"
    "사람들은 서로 쳐다봤어요.\n"
    "\"옷이 안 보이는데... 나만 그런 건가?\"\n"
    "하지만 아무도 말하지 못했어요.\n"
    "\"어리석다고 생각되면 어쩌지?\" 🤫\n"
    "모두가 거짓 칭찬을 했어요.\n"
    "\"아름다운 옷이네요!\" \"정말 멋져요!\"\n"
    "<strong>아무도 용감하게 말하지 못했어요! 😶</strong>",
    # A1
    "The emperor walked.\n"
    "People watched him.\n"
    "They were all scared.\n"
    "No one was brave enough to speak.",
    # A2
    "The emperor marched proudly through the town streets.\n"
    "All the people gathered to see the new clothes.\n"
    "Everyone could see the emperor was wearing nothing.\n"
    "No one was brave enough to speak the truth out loud.\n"
    "They all pretended to admire the beautiful invisible cloth.\n"
    "Fear of looking foolish kept everyone silent."
)

STORIES["week26c"] = (
    "거리는 사람들로 가득 찼어요. 👥\n"
    "임금님은 머리를 높이 들고 걸었어요.\n"
    "\"나의 새 옷이 정말 멋지지?\" 👑\n"
    "수천 명의 사람들이 보고 있었어요.\n"
    "모든 사람이 진실을 알고 있었어요.\n"
    "하지만 입을 꽉 다물었어요. 🤐\n"
    "\"바보로 보이면 어쩌지?\"\n"
    "\"다른 사람도 다 칭찬하잖아.\"\n"
    "두려움이 진실을 막았어요.\n"
    "이렇게 모두가 거짓말을 할 때\n"
    "용기 있는 한 마디가 필요해요.\n"
    "<strong>모든 사람이 간단한 진실을 말하기를 두려워했어요! 😰</strong>",
    # A1
    "Thousands of people watched.\n"
    "They all knew the truth.\n"
    "But fear stopped them.\n"
    "Everyone was afraid to tell the simple truth.",
    # A2
    "The whole kingdom watched the emperor march through town.\n"
    "Thousands of people lined the streets and stayed silent.\n"
    "Everyone was afraid to tell the simple truth to the emperor.\n"
    "They thought they would be called foolish if they spoke.\n"
    "The swindlers had tricked the entire kingdom with one lie.\n"
    "But one small voice was about to change everything."
)

# ─── W27: A child told the truth ───
STORIES["week27a"] = (
    "행진이 계속되고 있었어요. 🎺\n"
    "모든 어른들이 거짓말을 하고 있을 때\n"
    "군중 속에서 작은 목소리가 들렸어요.\n"
    "\"엄마, 임금님이 아무것도 안 입었어!\" 👦\n"
    "어린 아이가 소리쳤어요!\n"
    "주위가 조용해졌어요. 🤫\n"
    "사람들이 서로 쳐다봤어요.\n"
    "\"그래... 맞아. 아이가 맞아!\"\n"
    "한 명, 두 명... 사람들이 진실을 말하기 시작했어요.\n"
    "어린아이의 용기가 모두를 깨웠어요!\n"
    "<strong>아이가 진실을 말했어요! 💡</strong>",
    # A1
    "A child saw the truth.\n"
    "He shouted it out.\n"
    "People started to agree.\n"
    "A child told the truth.",
    # A2
    "While all the adults pretended, a small child spoke up.\n"
    "The child shouted that the emperor was wearing nothing.\n"
    "A child told the truth that everyone was afraid to say.\n"
    "The crowd became quiet, then started whispering.\n"
    "One by one, people agreed with the brave child.\n"
    "The truth spread through the crowd like wildfire."
)

STORIES["week27b"] = (
    "아이의 목소리가 거리에 울려 퍼졌어요! 📢\n"
    "\"임금님이 아무것도 안 입었어!\"\n"
    "처음에 사람들은 놀랐어요. 😮\n"
    "하지만 곧 고개를 끄덕이기 시작했어요.\n"
    "\"맞아! 정말 아무것도 안 입었어!\"\n"
    "\"우리가 왜 거짓말을 했지?\"\n"
    "웅성웅성... 소리가 점점 커졌어요. 📣\n"
    "\"임금님! 옷이 없어요!\"\n"
    "임금님의 얼굴이 빨개졌어요. 😳\n"
    "사기꾼들은 이미 도망가고 없었어요!\n"
    "<strong>용감한 아이가 크게 소리쳤어요! 🗣️</strong>",
    # A1
    "The child was brave.\n"
    "People agreed with him.\n"
    "The truth was out.\n"
    "A brave child spoke up loudly.",
    # A2
    "The brave child's voice echoed through the street.\n"
    "A brave child spoke up loudly and everyone heard.\n"
    "People started nodding and repeating the same words.\n"
    "The emperor's face turned red with embarrassment.\n"
    "He realized everyone had been lying to him all along.\n"
    "The swindlers had already run away with the gold."
)

STORIES["week27c"] = (
    "임금님은 그날 큰 교훈을 얻었어요. 📖\n"
    "거짓말에 속았다는 것을 깨달았어요.\n"
    "\"나도 진실을 볼 수 있었는데...\"\n"
    "임금님은 부끄러웠지만 반성했어요. 😔\n"
    "어린 아이 한 명이 모두를 깨웠어요.\n"
    "어른들은 두려움 때문에 진실을 숨겼어요.\n"
    "하지만 아이는 두려움 없이 말했어요! 💪\n"
    "진실을 말하는 것은 용기가 필요해요.\n"
    "하지만 그것이 가장 중요한 일이에요.\n"
    "이 이야기의 교훈: 진실을 말할 용기를 가져요! 🌟\n"
    "솔직함이 세상을 바꿀 수 있어요!\n"
    "<strong>용감한 아이가 아무도 못 한 말을 했어요! 🦸</strong>",
    # A1
    "The child was honest.\n"
    "Truth is important.\n"
    "Be brave like the child.\n"
    "A brave child said what no one else dared.",
    # A2
    "The emperor learned a big lesson about honesty that day.\n"
    "All the adults were too scared to speak the truth.\n"
    "A brave child said what no one else dared to say.\n"
    "It takes courage to be honest when everyone is lying.\n"
    "The child showed that truth is more important than fear.\n"
    "From that day on, the emperor became a wiser ruler."
)

# ─── W28: Hans got gold (Lucky Hans) ───
STORIES["week28a"] = (
    "새로운 이야기! 행운의 한스! 🎉\n"
    "한스는 7년 동안 열심히 일한 청년이에요.\n"
    "드디어 일을 마치고 집으로 갈 시간이에요.\n"
    "주인이 말했어요. \"한스, 고마웠다.\"\n"
    "\"여기 네 품삯이야.\" 💰\n"
    "머리만큼 큰 금덩이를 줬어요!\n"
    "한스는 너무너무 기뻤어요.\n"
    "\"우와! 금이다!\" 😄\n"
    "무거운 금덩이를 짊어지고 길을 떠났어요.\n"
    "엄마가 집에서 기다리고 있거든요.\n"
    "<strong>한스가 금을 받았어요! 💰</strong>",
    # A1
    "Hans worked for seven years.\n"
    "His boss gave him gold.\n"
    "He was very happy.\n"
    "Hans got gold.",
    # A2
    "Hans was a young man who worked hard for seven years.\n"
    "When his work was done, his master gave him payment.\n"
    "Hans got gold, a lump as big as his head.\n"
    "He was so happy and excited to go home to Mother.\n"
    "He put the heavy gold on his shoulder and started walking.\n"
    "But the gold was very heavy and the road was very long."
)

STORIES["week28b"] = (
    "한스는 금덩이를 지고 걸었어요. 🚶\n"
    "하지만 너무 무거웠어요!\n"
    "어깨가 아프고 다리가 후들후들했어요. 😓\n"
    "\"이 금이 정말 무겁구나...\"\n"
    "한스는 힘들었지만 기분은 좋았어요.\n"
    "7년 동안 열심히 일한 보상이니까요!\n"
    "\"엄마한테 가져다 드려야지.\"\n"
    "한스는 천천히 걸었어요.\n"
    "금덩이가 반짝반짝 빛났어요. ✨\n"
    "한스의 얼굴에도 미소가 가득했어요.\n"
    "<strong>한스는 큰 금덩이를 받았어요! 🏆</strong>",
    # A1
    "The gold was heavy.\n"
    "His shoulders hurt.\n"
    "But he was happy.\n"
    "Hans got a big lump of gold.",
    # A2
    "Hans carried the gold on his shoulder down the road.\n"
    "Hans got a big lump of gold but it was terribly heavy.\n"
    "His shoulders ached and his legs were getting tired.\n"
    "He thought about his mother waiting for him at home.\n"
    "Even though it was hard, he smiled the whole way.\n"
    "Soon he would meet someone who would change everything."
)

STORIES["week28c"] = (
    "한스는 계속 길을 걸었어요. 🛤️\n"
    "금덩이의 무게가 점점 더 느껴졌어요.\n"
    "\"7년이나 일했으니 이 정도는 괜찮아!\" 💪\n"
    "한스는 긍정적인 사람이었어요.\n"
    "무거워도 불평하지 않았어요.\n"
    "\"엄마가 얼마나 기뻐하실까?\"\n"
    "한스는 엄마 생각을 하며 걸었어요.\n"
    "금은 무거웠지만 한스의 마음은 가벼웠어요. 😊\n"
    "그때 저 앞에서 말을 탄 사람이 보였어요. 🐴\n"
    "한스의 눈이 반짝였어요.\n"
    "<strong>한스는 열심히 일한 대가로 금덩이를 받았어요! ⭐</strong>",
    # A1
    "Hans worked hard.\n"
    "He earned his reward.\n"
    "He started walking home.\n"
    "Hans got a lump of gold for his work.",
    # A2
    "Hans was proud of the gold he earned from seven years of work.\n"
    "Hans got a lump of gold for his work and felt very proud.\n"
    "The road home was long and the gold grew heavier each step.\n"
    "But Hans was cheerful and thought about seeing Mother.\n"
    "He spotted a man riding a horse coming toward him.\n"
    "This meeting would begin a surprising chain of trades."
)

# ─── W29: He traded it away ───
STORIES["week29a"] = (
    "한스가 걷고 있는데 말을 탄 사람이 왔어요. 🐴\n"
    "\"야, 넌 왜 그렇게 힘들게 걸어?\"\n"
    "한스가 말했어요. \"이 금이 너무 무거워서요.\"\n"
    "\"그럼 내 말이랑 바꾸지 않을래?\" 🤝\n"
    "한스는 생각했어요.\n"
    "\"말을 타면 편하게 갈 수 있겠다!\"\n"
    "한스는 기뻐하며 금을 주고 말을 받았어요.\n"
    "말 위에 올라타니 정말 좋았어요!\n"
    "\"이야! 나는 정말 운이 좋아!\" 😄\n"
    "한스는 기분이 최고였어요.\n"
    "<strong>한스는 금을 바꿔버렸어요! 🔄</strong>",
    # A1
    "A man had a horse.\n"
    "Hans liked the horse.\n"
    "He gave his gold.\n"
    "He traded it away.",
    # A2
    "A man on a horse stopped and asked about the heavy gold.\n"
    "Hans said the gold was too heavy to carry all the way.\n"
    "He traded it away, giving the gold for a horse.\n"
    "Hans was thrilled because riding was so much easier.\n"
    "He did not realize the gold was worth much more.\n"
    "But Hans felt happy and that was all that mattered."
)

STORIES["week29b"] = (
    "한스는 신나서 말을 타고 갔어요. 🐴\n"
    "\"이야! 빠르다! 걷는 것보다 훨씬 좋아!\"\n"
    "하지만 말이 갑자기 빨리 달리기 시작했어요!\n"
    "한스는 꽉 잡았지만 결국 떨어졌어요. 😵\n"
    "\"아야!\"\n"
    "마침 소를 끌고 가는 농부가 있었어요. 🐄\n"
    "\"말보다 소가 더 좋지 않겠니?\"\n"
    "\"소에서 우유도 나오잖아!\"\n"
    "한스는 말을 소와 바꿨어요.\n"
    "\"나는 정말 운이 좋아!\" 한스가 웃었어요. 😊\n"
    "<strong>한스는 금을 말과 바꿨어요! 🐎</strong>",
    # A1
    "Hans fell off the horse.\n"
    "He met a farmer.\n"
    "He traded for a cow.\n"
    "He traded the gold for a horse.",
    # A2
    "Hans rode the horse happily but then fell off.\n"
    "A farmer came by with a cow and offered to trade.\n"
    "He traded the gold for a horse and now the horse for a cow.\n"
    "Hans thought the cow was even better than a horse.\n"
    "He could get fresh milk from the cow every day.\n"
    "Hans always saw the bright side of everything."
)

STORIES["week29c"] = (
    "한스는 소를 끌고 기분 좋게 걸었어요. 🐄\n"
    "\"우유도 마시고, 버터도 만들 수 있어!\"\n"
    "한스는 항상 긍정적이었어요.\n"
    "처음에는 머리만큼 큰 금덩이가 있었어요. 💰\n"
    "그걸 말과 바꿨어요.\n"
    "무거운 짐을 안 들어도 되니까 기뻤어요.\n"
    "말에서 떨어져서 소와 바꿨어요.\n"
    "소에서 우유가 나오니까 더 기뻤어요! 🥛\n"
    "한스는 뭘 바꾸든 항상 행복했어요.\n"
    "이것이 한스의 특별한 점이에요.\n"
    "<strong>한스는 무거운 금을 기꺼이 말과 바꿨어요! 😊</strong>",
    # A1
    "First he had gold.\n"
    "Then he had a horse.\n"
    "Now he has a cow.\n"
    "He happily traded his heavy gold for a horse.",
    # A2
    "Hans started his journey with a huge lump of gold.\n"
    "He happily traded his heavy gold for a horse on the road.\n"
    "When the horse threw him off, he traded it for a cow.\n"
    "Each time he traded, he found a new reason to smile.\n"
    "Most people would be upset losing their gold.\n"
    "But Hans always looked at the positive side of things."
)

# ─── W30: He kept trading ───
STORIES["week30a"] = (
    "한스는 소를 끌고 계속 걸었어요. 🐄\n"
    "목이 말라서 우유를 짜려고 했어요.\n"
    "하지만 소가 움직이지 않았어요! 😅\n"
    "돼지를 데리고 가는 사람이 지나갔어요. 🐷\n"
    "\"소보다 돼지가 더 좋지 않겠니?\"\n"
    "한스는 소를 돼지와 바꿨어요!\n"
    "조금 후에 거위를 든 사람을 만났어요. 🪿\n"
    "\"돼지보다 거위가 더 좋아!\"\n"
    "또 바꿨어요!\n"
    "한스는 계속 바꾸고 있었어요!\n"
    "<strong>한스는 계속 바꿨어요! 🔄</strong>",
    # A1
    "He traded the cow.\n"
    "Then the pig.\n"
    "Then the goose.\n"
    "He kept trading.",
    # A2
    "Hans traded the cow for a pig on the road.\n"
    "Then someone offered a goose for his pig.\n"
    "He kept trading one thing for another happily.\n"
    "Each trade made him feel like the luckiest person alive.\n"
    "Other people thought he was being foolish.\n"
    "But Hans smiled brighter with every single trade he made."
)

STORIES["week30b"] = (
    "한스는 거위를 안고 걸었어요. 🪿\n"
    "\"거위 깃털로 베개를 만들 수 있어!\"\n"
    "숫돌 가는 사람이 지나갔어요.\n"
    "\"그 거위랑 내 숫돌 바꾸자!\" 🪨\n"
    "한스는 또 바꿨어요!\n"
    "\"숫돌이 있으면 칼을 갈 수 있으니까!\"\n"
    "한스는 계속해서 바꾸고 또 바꿨어요.\n"
    "금에서 말, 말에서 소, 소에서 돼지,\n"
    "돼지에서 거위, 거위에서 숫돌! 🔄\n"
    "한스의 교환 여행은 끝이 없었어요.\n"
    "<strong>한스는 계속해서 바꾸고 또 바꿨어요! ♻️</strong>",
    # A1
    "He got a goose.\n"
    "Then a stone.\n"
    "He kept swapping.\n"
    "He traded again and again.",
    # A2
    "Hans held the goose and walked with a big smile.\n"
    "He met a man who wanted the goose for a grinding stone.\n"
    "He traded again and again without a single worry.\n"
    "From gold to horse to cow to pig to goose to stone.\n"
    "Each trade left him with something less valuable.\n"
    "But Hans never stopped smiling through it all."
)

STORIES["week30c"] = (
    "한스가 가진 것을 세어봐요. 📋\n"
    "처음에: 머리만큼 큰 금덩이 💰\n"
    "다음에: 말 🐴\n"
    "그다음: 소 🐄\n"
    "그다음: 돼지 🐷\n"
    "그다음: 거위 🪿\n"
    "그다음: 숫돌 🪨\n"
    "그리고... 숫돌이 우물에 빠져버렸어요!\n"
    "이제 한스에게는 아무것도 없었어요! 😯\n"
    "하지만 놀랍게도...\n"
    "한스는 웃고 있었어요!\n"
    "<strong>한스는 아무것도 남지 않을 때까지 계속 바꿨어요! 🔄</strong>",
    # A1
    "Gold, horse, cow, pig, goose, stone.\n"
    "The stone fell in a well.\n"
    "He had nothing.\n"
    "He kept trading until he had nothing left.",
    # A2
    "Hans had traded from gold all the way down to a stone.\n"
    "Then the heavy stone fell into a well and was gone.\n"
    "He kept trading until he had nothing left at all.\n"
    "Most people would cry about losing everything.\n"
    "But Hans looked at the sky and laughed out loud.\n"
    "He felt lighter and happier than ever before."
)

# ─── W31: Hans felt free ───
STORIES["week31a"] = (
    "한스에게는 이제 아무것도 없었어요. 😯\n"
    "금도 없고, 말도 없고, 아무것도요.\n"
    "하지만 한스는 활짝 웃었어요!\n"
    "\"아! 너무 자유롭다!\" 🎉\n"
    "무거운 것을 안 들어도 되니까요.\n"
    "걱정할 것도 없어요.\n"
    "한스는 팔랑팔랑 팔을 흔들며 걸었어요.\n"
    "몸이 깃털처럼 가벼웠어요. 🪶\n"
    "\"이것이 진짜 행복이구나!\"\n"
    "한스의 마음은 세상에서 가장 가벼웠어요.\n"
    "<strong>한스는 자유로웠어요! 🕊️</strong>",
    # A1
    "Hans had nothing.\n"
    "But he was happy.\n"
    "He felt light.\n"
    "Hans felt free.",
    # A2
    "Hans had nothing left but he was smiling brightly.\n"
    "He stretched his arms and looked up at the blue sky.\n"
    "Hans felt free without anything heavy to carry.\n"
    "He danced and sang as he walked down the road.\n"
    "No gold, no horse, no cow, but pure happiness.\n"
    "He realized that freedom was the greatest treasure."
)

STORIES["week31b"] = (
    "한스는 노래를 부르며 집으로 걸었어요. 🎵\n"
    "\"라라라! 나는 세상에서 가장 행복한 사람!\"\n"
    "지나가는 사람들이 이상하게 쳐다봤어요.\n"
    "\"아무것도 없으면서 왜 행복하지?\" 🤔\n"
    "한스는 대답했어요.\n"
    "\"무거운 금보다 가벼운 마음이 더 좋거든요!\"\n"
    "한스는 드디어 집에 도착했어요. 🏠\n"
    "엄마가 문을 열었어요.\n"
    "\"한스야!\" 엄마가 한스를 꼭 안았어요. 🤗\n"
    "한스는 엄마 품에서 가장 행복했어요.\n"
    "<strong>한스는 자유롭고 행복했어요! 😄</strong>",
    # A1
    "Hans walked home.\n"
    "He sang a song.\n"
    "Mother hugged him.\n"
    "Hans felt free and happy.",
    # A2
    "Hans walked home singing without a care in the world.\n"
    "People stared at him wondering why he was so joyful.\n"
    "Hans felt free and happy with nothing to weigh him down.\n"
    "When he reached home, Mother hugged him at the door.\n"
    "He told her about every trade he made on the road.\n"
    "Mother just smiled because her son was home safe."
)

STORIES["week31c"] = (
    "한스의 이야기에서 우리는 배워요. 📖\n"
    "한스는 금을 잃어도 행복했어요.\n"
    "왜일까요? 🤔\n"
    "한스는 물건이 행복을 만든다고 생각하지 않았어요.\n"
    "자유로운 마음이 진짜 행복이라고 생각했어요.\n"
    "무거운 짐을 내려놓으면 마음이 가벼워져요. 🪶\n"
    "진짜 소중한 것은 돈이 아니에요.\n"
    "가족, 자유, 행복한 마음이에요. 💕\n"
    "한스는 아무것도 없었지만\n"
    "세상에서 가장 부자였어요.\n"
    "가벼운 마음이 금보다 더 값지기 때문이에요!\n"
    "<strong>한스는 자유로웠어요 — 가벼운 마음이 금보다 좋아요! 🌟</strong>",
    # A1
    "Things do not make you happy.\n"
    "Freedom does.\n"
    "Hans knew this.\n"
    "Hans felt free, a light heart beats gold.",
    # A2
    "Hans lost everything on his journey but gained something more.\n"
    "He discovered that happiness does not come from things.\n"
    "Hans felt free because a light heart beats gold.\n"
    "A free and happy heart is worth more than any treasure.\n"
    "He learned that the best things in life are not things.\n"
    "Family and freedom are the greatest treasures of all."
)

# ─── W32: The boy loved him (Velveteen Rabbit) ───
STORIES["week32a"] = (
    "새로운 이야기! 벨벳 토끼! 🐰\n"
    "크리스마스에 한 소년이 선물을 받았어요. 🎄\n"
    "상자 안에 부드러운 벨벳 토끼 인형이 있었어요.\n"
    "갈색 털에 반짝이는 눈을 가진 토끼!\n"
    "소년은 토끼를 보자마자 좋아했어요.\n"
    "\"내 토끼!\" 소년이 안아줬어요. 🤗\n"
    "다른 장난감들은 비싸고 화려했지만\n"
    "소년은 벨벳 토끼가 제일 좋았어요.\n"
    "매일 밤 토끼와 함께 잠을 잤어요. 🌙\n"
    "토끼는 소년의 사랑을 느꼈어요.\n"
    "<strong>소년은 토끼를 사랑했어요! ❤️</strong>",
    # A1
    "A boy got a toy rabbit.\n"
    "It was soft and brown.\n"
    "He loved it so much.\n"
    "The boy loved him.",
    # A2
    "On Christmas morning, a boy found a velveteen rabbit.\n"
    "The rabbit was soft, brown, and had shiny button eyes.\n"
    "The boy loved him from the very first moment.\n"
    "He slept with the rabbit every single night.\n"
    "The other toys were fancier but the rabbit was special.\n"
    "The boy held the rabbit close and whispered goodnight."
)

STORIES["week32b"] = (
    "소년과 벨벳 토끼는 항상 함께였어요. 🐰\n"
    "아침에 일어나면 \"좋은 아침!\" 인사했어요.\n"
    "밥 먹을 때도 옆에 앉혔어요.\n"
    "산책할 때도 꼭 안고 갔어요. 🚶\n"
    "소년의 손이 닿는 곳에 항상 토끼가 있었어요.\n"
    "다른 장난감들은 놀림을 했어요.\n"
    "\"넌 진짜가 아니잖아!\" 🤖\n"
    "하지만 소년은 토끼를 아주 많이 사랑했어요.\n"
    "토끼의 벨벳 털이 닳아가도 괜찮았어요.\n"
    "소년에게 토끼는 세상에서 가장 소중했어요.\n"
    "<strong>소년은 토끼를 아주 많이 사랑했어요! 💕</strong>",
    # A1
    "They did everything together.\n"
    "Other toys made fun.\n"
    "But the boy did not care.\n"
    "The boy loved the rabbit very much.",
    # A2
    "The boy and the rabbit were inseparable every day.\n"
    "The boy loved the rabbit very much and took him everywhere.\n"
    "The other toys laughed because the rabbit was not fancy.\n"
    "But the boy did not care about what they said.\n"
    "The rabbit's fur was getting worn from all the love.\n"
    "To the boy, the rabbit was more precious than any toy."
)

STORIES["week32c"] = (
    "벨벳 토끼는 오래된 말 인형에게 물어봤어요. 🐴\n"
    "\"'진짜'가 된다는 건 뭐야?\"\n"
    "말 인형이 대답했어요.\n"
    "\"누군가가 너를 오래오래 사랑하면 진짜가 되는 거야.\"\n"
    "\"아프지 않아?\" 토끼가 물었어요.\n"
    "\"때로는 아프지. 하지만 진짜가 되면 상관없어.\" 💕\n"
    "토끼는 생각했어요.\n"
    "\"소년이 나를 정말 사랑하니까...\"\n"
    "\"나도 언젠가 진짜가 될 수 있을까?\"\n"
    "소년의 사랑은 매일 더 깊어지고 있었어요.\n"
    "<strong>소년은 다른 어떤 장난감보다 토끼를 사랑했어요! 🧸</strong>",
    # A1
    "The rabbit asked about being real.\n"
    "Love makes you real.\n"
    "The boy's love was strong.\n"
    "The boy loved the rabbit more than any toy.",
    # A2
    "The rabbit asked an old toy horse about becoming real.\n"
    "The horse said love is what makes a toy become real.\n"
    "The boy loved the rabbit more than any toy in the room.\n"
    "His love was gentle, warm, and grew stronger every day.\n"
    "The rabbit's fur became thin but the boy loved him still.\n"
    "Real magic was happening through the boy's true love."
)

# ─── W33: He wanted to be real ───
STORIES["week33a"] = (
    "벨벳 토끼는 '진짜'가 되고 싶었어요. 🐰\n"
    "말 인형의 이야기를 듣고 나서\n"
    "토끼는 매일 생각했어요.\n"
    "\"진짜 토끼가 되면 어떤 느낌일까?\"\n"
    "진짜 토끼처럼 뛰어다니고 싶었어요. 🏃\n"
    "풀밭에서 놀고, 다른 토끼들과 친구가 되고 싶었어요.\n"
    "소년이 토끼를 안아줄 때마다\n"
    "토끼의 마음이 두근두근 뛰는 것 같았어요. 💓\n"
    "\"소년아, 고마워. 너의 사랑이 느껴져.\"\n"
    "토끼는 진짜가 되는 꿈을 꿨어요.\n"
    "<strong>토끼는 진짜가 되고 싶었어요! 🌟</strong>",
    # A1
    "The rabbit had a dream.\n"
    "He wanted to hop.\n"
    "He wanted to play.\n"
    "He wanted to be real.",
    # A2
    "After hearing the old horse's story, the rabbit had a dream.\n"
    "He wanted to be real so he could hop and play.\n"
    "He imagined running through the green grass freely.\n"
    "Every night, the boy hugged him tight before sleeping.\n"
    "The rabbit felt warm and loved in the boy's arms.\n"
    "He believed that love would make his dream come true."
)

STORIES["week33b"] = (
    "소년이 아팠을 때 토끼가 함께 있었어요. 🤒\n"
    "의사 선생님이 왔어요.\n"
    "\"이 아이에게 이 인형이 필요합니다.\"\n"
    "소년은 토끼를 꼭 안고 있었어요.\n"
    "\"내 토끼... 나를 떠나지 마.\" 😢\n"
    "토끼는 소년 곁에서 떠나지 않았어요.\n"
    "밤새 소년을 지켜봤어요. 🌙\n"
    "토끼는 더욱 간절하게 진짜가 되고 싶었어요.\n"
    "소년을 진짜로 안아주고 싶었으니까요.\n"
    "사랑이 이렇게 깊으면 기적이 일어날 수 있을까요?\n"
    "<strong>토끼는 진짜가 되고 싶었어요! 💫</strong>",
    # A1
    "The boy was sick.\n"
    "The rabbit stayed close.\n"
    "He wished to be real.\n"
    "The rabbit wanted to become real.",
    # A2
    "The boy became very sick and stayed in bed for days.\n"
    "The rabbit never left his side through the long nights.\n"
    "The rabbit wanted to become real to truly comfort the boy.\n"
    "The boy held the rabbit and would not let go.\n"
    "Their bond grew deeper during those difficult days.\n"
    "The rabbit wished with all his heart to become alive."
)

STORIES["week33c"] = (
    "소년이 점점 나아지기 시작했어요. 😊\n"
    "하지만 의사가 말했어요.\n"
    "\"낡은 장난감을 다 버려야 합니다.\"\n"
    "\"병균이 있을 수 있어요.\" 🦠\n"
    "토끼는 쓰레기 봉투에 담겼어요.\n"
    "정원 구석에 놓여졌어요. 😢\n"
    "토끼의 눈에서 진짜 눈물이 한 방울 흘렀어요.\n"
    "\"소년아... 안녕...\"\n"
    "토끼는 너무 슬펐어요.\n"
    "하지만 토끼는 포기하지 않았어요.\n"
    "진짜가 되고 싶은 마음은 더 강해졌어요.\n"
    "<strong>토끼는 무엇보다도 진짜가 되고 싶었어요! 😭</strong>",
    # A1
    "The rabbit was thrown away.\n"
    "He cried a real tear.\n"
    "He wanted to be real so badly.\n"
    "The rabbit wanted to be real more than anything.",
    # A2
    "The doctor said all the old toys must be thrown away.\n"
    "The rabbit was placed in a bag in the garden.\n"
    "A real tear fell from the rabbit's button eye.\n"
    "The rabbit wanted to be real more than anything in the world.\n"
    "He remembered all the happy days with his beloved boy.\n"
    "But something magical was about to happen because of that tear."
)

# ─── W34: Love made him real ───
STORIES["week34a"] = (
    "토끼의 눈물이 땅에 떨어졌어요. 💧\n"
    "그 자리에서 아름다운 꽃이 피었어요! 🌸\n"
    "꽃잎이 열리자 요정이 나타났어요. ✨\n"
    "\"나는 장난감 요정이야.\"\n"
    "\"아이들이 진심으로 사랑한 장난감을 진짜로 만들어주지.\"\n"
    "토끼는 눈이 커졌어요.\n"
    "\"진짜요?!\"\n"
    "요정이 토끼에게 키스했어요. 💋\n"
    "반짝! 빛이 토끼를 감쌌어요!\n"
    "사랑의 힘이 마법을 만들었어요!\n"
    "<strong>사랑이 토끼를 진짜로 만들었어요! 💕</strong>",
    # A1
    "A tear fell.\n"
    "A fairy appeared.\n"
    "She made him real.\n"
    "Love made him real.",
    # A2
    "The rabbit's tear fell to the ground and a flower grew.\n"
    "A beautiful fairy appeared from inside the flower.\n"
    "She was the fairy who makes loved toys become real.\n"
    "Love made him real because the boy's love was true.\n"
    "The fairy kissed the rabbit and light surrounded him.\n"
    "Something wonderful was happening to the velveteen rabbit."
)

STORIES["week34b"] = (
    "빛이 사라지자 토끼가 변해 있었어요! 🐰✨\n"
    "벨벳 털이 부드러운 진짜 털이 되었어요.\n"
    "단추 눈이 반짝이는 진짜 눈이 되었어요.\n"
    "다리가 움직였어요!\n"
    "토끼가 깡충! 뛰었어요! 🏃\n"
    "\"나... 나 진짜가 됐어!\"\n"
    "토끼는 너무 기뻐서 펄쩍펄쩍 뛰었어요.\n"
    "풀밭을 달리고, 바람을 느꼈어요. 🌿\n"
    "이 모든 것이 소년의 사랑 덕분이에요.\n"
    "사랑은 천천히, 하지만 확실하게 마법을 만들어요.\n"
    "<strong>사랑이 천천히 토끼를 진짜로 만들었어요! 🌟</strong>",
    # A1
    "The rabbit changed.\n"
    "He could hop now.\n"
    "He was alive.\n"
    "Love slowly made the rabbit real.",
    # A2
    "The light faded and the rabbit looked completely different.\n"
    "He had real fur, real eyes, and real legs that could hop.\n"
    "Love slowly made the rabbit real after all those years.\n"
    "He jumped and ran through the garden with pure joy.\n"
    "He could feel the wind and the grass for the first time.\n"
    "The boy's love had created the most beautiful miracle."
)

STORIES["week34c"] = (
    "진짜 토끼가 된 벨벳 토끼! 🐰\n"
    "정원에서 다른 진짜 토끼들을 만났어요.\n"
    "\"안녕! 나도 이제 진짜야!\" 🎉\n"
    "다른 토끼들이 반겨줬어요.\n"
    "함께 뛰어놀고, 풀을 먹고, 행복했어요.\n"
    "토끼는 가끔 소년의 창문을 보았어요. 🪟\n"
    "\"고마워, 나의 소년. 너의 사랑이 나를 진짜로 만들었어.\"\n"
    "사랑은 마법이에요.\n"
    "진심으로 사랑하면 불가능도 가능해져요. ✨\n"
    "이것이 사랑의 힘이에요.\n"
    "사랑이야말로 진짜 마법이에요!\n"
    "<strong>사랑이 토끼를 진짜로 만들었어요 — 사랑이 마법이에요! 💖</strong>",
    # A1
    "He met real rabbits.\n"
    "They played together.\n"
    "Love is magic.\n"
    "Love made him real, love is the magic.",
    # A2
    "The real rabbit met other rabbits in the garden.\n"
    "They welcomed him and played together in the sunshine.\n"
    "Love made him real because love is the truest magic.\n"
    "He sometimes looked at the boy's window and smiled.\n"
    "The boy's love had given him the gift of life.\n"
    "True love can make the impossible become possible."
)

# ─── W35: Real comes from love ───
STORIES["week35a"] = (
    "어느 날 소년이 정원에서 놀고 있었어요. 🌿\n"
    "저 멀리 토끼 한 마리가 보였어요.\n"
    "갈색 털에 반짝이는 눈... 🐰\n"
    "\"저 토끼... 내 벨벳 토끼 같아!\"\n"
    "소년은 눈을 크게 떴어요.\n"
    "토끼는 소년을 바라보며 살짝 웃은 것 같았어요.\n"
    "소년의 마음이 따뜻해졌어요. 💕\n"
    "사랑으로 진짜가 된 토끼.\n"
    "진짜가 되는 것은 사랑에서 시작돼요.\n"
    "이것이 이 이야기가 전하는 메시지예요.\n"
    "<strong>진짜가 되는 것은 사랑에서 시작돼요! 🌟</strong>",
    # A1
    "The boy saw a rabbit.\n"
    "It looked familiar.\n"
    "Love starts everything.\n"
    "Real comes from love.",
    # A2
    "One day, the boy saw a brown rabbit in the garden.\n"
    "The rabbit looked just like his old velveteen toy.\n"
    "Real comes from love, and the boy felt it in his heart.\n"
    "The rabbit paused and looked at the boy with warm eyes.\n"
    "A smile spread across the boy's face.\n"
    "He knew that his love had made something truly magical."
)

STORIES["week35b"] = (
    "소년은 토끼를 바라보며 생각했어요. 🤔\n"
    "\"진짜가 된다는 건 뭘까?\"\n"
    "토끼의 눈이 옛날 벨벳 토끼와 똑같았어요.\n"
    "따뜻하고 부드러운 눈빛이었어요. 👀\n"
    "소년은 깨달았어요.\n"
    "진짜가 된다는 것은 사랑받는 거예요.\n"
    "누군가가 진심으로 사랑해주면\n"
    "우리 모두 진짜가 되는 거예요. 💕\n"
    "소년의 사랑이 토끼에게 생명을 줬어요.\n"
    "그리고 토끼의 존재가 소년에게 사랑을 가르쳐줬어요.\n"
    "<strong>진짜가 되는 것은 사랑이 주는 선물이에요! 🎁</strong>",
    # A1
    "The boy understood.\n"
    "Love makes us real.\n"
    "The rabbit taught him.\n"
    "Real is what love gives you.",
    # A2
    "The boy looked into the rabbit's warm, familiar eyes.\n"
    "He remembered all the nights they spent together.\n"
    "Real is what love gives you when it is true and deep.\n"
    "The boy learned this lesson from his velveteen rabbit.\n"
    "Love had made the toy real and taught the boy about life.\n"
    "They both became real through the power of their love."
)

STORIES["week35c"] = (
    "이것이 벨벳 토끼의 이야기예요. 📖\n"
    "장난감 토끼가 소년의 사랑으로 진짜가 되었어요.\n"
    "처음에 토끼는 그냥 인형이었어요. 🧸\n"
    "하지만 소년이 매일 안아주고, 함께 자고,\n"
    "아플 때도 곁에 있어줬어요.\n"
    "그 사랑이 토끼를 진짜로 만들었어요. ✨\n"
    "진짜 사랑은 시간이 걸려요.\n"
    "하지만 진심으로 사랑하면\n"
    "가장 놀라운 일이 일어나요.\n"
    "누군가를 진심으로 사랑하면 진짜가 돼요. 💕\n"
    "그것이 사랑의 마법이에요!\n"
    "<strong>누군가가 진심으로 사랑하면 진짜가 되는 거예요! 🌈</strong>",
    # A1
    "Love takes time.\n"
    "But it is real.\n"
    "The rabbit became real.\n"
    "Real is what happens when someone truly loves you.",
    # A2
    "The velveteen rabbit started as just a simple toy.\n"
    "But the boy loved him every day without stopping.\n"
    "Real is what happens when someone truly loves you.\n"
    "It takes time and patience but it is worth waiting for.\n"
    "The rabbit became real because of the boy's endless love.\n"
    "True love is the most powerful magic in the whole world."
)

# ─── W36: Love is the lesson ───
STORIES["week36a"] = (
    "벨벳 토끼의 마지막 이야기예요. 🐰\n"
    "우리는 이 이야기에서 무엇을 배웠을까요?\n"
    "사랑은 가장 강한 힘이에요. 💪\n"
    "사랑은 불가능을 가능하게 만들어요.\n"
    "장난감 토끼도 진짜가 될 수 있었어요.\n"
    "왜냐하면 소년의 사랑이 있었으니까요.\n"
    "우리도 누군가를 사랑하면\n"
    "놀라운 일이 일어날 수 있어요. ✨\n"
    "사랑이 이 이야기의 교훈이에요.\n"
    "사랑하는 마음을 잊지 마세요!\n"
    "<strong>사랑이 이 이야기의 교훈이에요! 💕</strong>",
    # A1
    "Love is powerful.\n"
    "It changes everything.\n"
    "This is the lesson.\n"
    "Love is the lesson.",
    # A2
    "The story of the velveteen rabbit teaches us about love.\n"
    "Love is the most powerful force in the whole world.\n"
    "Love is the lesson we should always remember.\n"
    "It can turn something ordinary into something magical.\n"
    "The boy's love made a simple toy into a living rabbit.\n"
    "We should love with all our heart every single day."
)

STORIES["week36b"] = (
    "3학년 수업이 거의 끝나가요! 📚\n"
    "처음에 피터 래빗의 모험을 배웠어요.\n"
    "빨간 모자, 잭과 콩나무, 개구리 왕자...\n"
    "요정과 구두장이, 엄지공주, 임금님의 새 옷...\n"
    "행운의 한스, 그리고 벨벳 토끼! 🐰\n"
    "모든 이야기에서 사랑과 용기를 배웠어요.\n"
    "진짜 사랑은 우리를 진짜로 만들어요. 💕\n"
    "소년의 사랑처럼 진심이 중요해요.\n"
    "사랑으로 우리도 진짜가 될 수 있어요.\n"
    "이제 마지막 수업이에요! 🌟\n"
    "<strong>사랑이 우리를 진짜로 만들어준다고 생각해요! 🌈</strong>",
    # A1
    "We learned many stories.\n"
    "Love was in every one.\n"
    "Love makes us real.\n"
    "I think love makes us real.",
    # A2
    "We have read so many wonderful stories this year.\n"
    "Every story taught us about love, courage, and kindness.\n"
    "I think love makes us real, just like the velveteen rabbit.\n"
    "When we love someone truly, amazing things can happen.\n"
    "The boy's love turned a simple toy into a living rabbit.\n"
    "Let us carry this lesson with us forever in our hearts."
)

STORIES["week36c"] = (
    "3학년 수업을 모두 마쳤어요! 🎉🌟\n"
    "피터 래빗부터 벨벳 토끼까지!\n"
    "아홉 개의 이야기를 함께 읽었어요. 📚\n"
    "매 이야기에서 새로운 것을 배웠어요.\n"
    "용기, 약속, 감사, 진실, 자유...\n"
    "그리고 가장 중요한 것은 사랑이에요. 💕\n"
    "사랑은 진짜 마법이에요.\n"
    "사랑으로 우리 모두 진짜가 될 수 있어요.\n"
    "여러분은 정말 대단해요!\n"
    "영어를 열심히 배운 여러분이 자랑스러워요!\n"
    "사랑은 우리를 진정으로 진짜로 만들어줘요! 🐰❤️\n"
    "<strong>사랑이 우리를 진정으로 진짜로 만들어주는 것이라고 생각해요! 🌈</strong>",
    # A1
    "We finished all the stories.\n"
    "Love was the biggest lesson.\n"
    "Love makes us truly real.\n"
    "I think love is what makes us truly real.",
    # A2
    "Congratulations on finishing all the Grade 3 stories.\n"
    "From Peter Rabbit to the Velveteen Rabbit, we learned so much.\n"
    "I think love is what makes us truly real in this world.\n"
    "Every story showed us that love, courage, and kindness matter.\n"
    "The velveteen rabbit became real because of a boy's love.\n"
    "Let us remember that true love is the greatest magic of all."
)


# ── CSS to add if missing ──
CSS_ADDITION = """.story-level{display:flex;align-items:center;gap:8px;margin:14px 0 4px;padding:8px 12px;border-radius:10px;font-size:0.75rem;font-weight:800;}
.story-level.a1{background:#e8f5e9;color:#2e7d32;}
.story-level.a2{background:#e3f2fd;color:#1565c0;}"""

def extract_key_sentence(content):
    m = re.search(r'class="key-eng"[^>]*>(.*?)</div>', content)
    if not m:
        return ""
    raw = m.group(1).strip()
    raw = html.unescape(raw)
    raw = raw.strip('"').strip('"').strip('"')
    return raw

def extract_vocab(content):
    return re.findall(r'class="v-eng"[^>]*>(.*?)</div>', content)[:4]

def escape_for_storyplay(text):
    """Remove HTML tags and escape for onclick attribute."""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('\n', ' ').replace('  ', ' ')
    text = text.replace("'", "\\'")
    text = text.replace('"', '')
    return text.strip()

def build_section2_body(korean, a1_lines, a2_lines, key_sentence):
    """Build the new section 2 body HTML."""
    # Korean story with <br>
    kr_html = korean.replace('\n', '<br>')

    # A1: build display HTML and storyPlay text
    a1_parts = a1_lines.split('\n')
    a1_display = '<br>'.join(a1_parts)
    # highlight key sentence in A1 if found
    for p in a1_parts:
        stripped = p.strip().rstrip('.')
        ks = key_sentence.rstrip('.')
        if stripped.lower() == ks.lower() or ks.lower() in stripped.lower():
            a1_display = a1_display.replace(p, f'<span class="hl">{p}</span>')
            break
    a1_plain = escape_for_storyplay(a1_lines)

    # A2: build display HTML and storyPlay text
    a2_parts = a2_lines.split('\n')
    a2_display = '<br>'.join(a2_parts)
    # highlight key sentence in A2
    for p in a2_parts:
        stripped = p.strip().rstrip('.')
        ks = key_sentence.rstrip('.')
        if stripped.lower() == ks.lower() or ks.lower() in stripped.lower():
            a2_display = a2_display.replace(p, f'<span class="hl">{p}</span>')
            break
    a2_plain = escape_for_storyplay(a2_lines)

    return f'''  <div><div class="robo-nm" style="color:var(--gold);">먼저 한국어로 읽어봐!</div><div class="robo-msg">{kr_html}</div></div>
  </div>
  <!-- A1 스토리 -->
  <div class="story-level a1">⭐ A1 쉬움</div>
  <div class="story-player-row">
    <span class="story-label">🔤 A1 Easy</span>
    <button class="story-ctrl-btn story-play-btn" onclick="storyPlay('{a1_plain}',this)">▶</button>
    <button class="story-ctrl-btn story-stop-btn" onclick="storyStopped()">⏹</button>
  </div>
  <div class="story-en">{a1_display}</div>
  <!-- A2 스토리 -->
  <div class="story-level a2">⭐⭐ A2 보통</div>
  <div class="story-player-row">
    <span class="story-label">🔤 A2 Medium</span>
    <button class="story-ctrl-btn story-play-btn" onclick="storyPlay('{a2_plain}',this)">▶</button>
    <button class="story-ctrl-btn story-stop-btn" onclick="storyStopped()">⏹</button>
  </div>
  <div class="story-en">{a2_display}</div>'''


def process_file(filepath):
    fname = os.path.basename(filepath)
    key = fname.replace('.html', '')  # e.g., "week01b"

    if key not in STORIES:
        print(f"  SKIP {fname}: no story data")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    key_sentence = extract_key_sentence(content)
    if not key_sentence:
        print(f"  SKIP {fname}: no key-eng found")
        return False

    korean, a1, a2 = STORIES[key]
    new_body = build_section2_body(korean, a1, a2, key_sentence)

    # 1. Add CSS if not present
    if '.story-level{' not in content and '.story-level {' not in content:
        # Insert after .story-en{...} line
        story_en_match = re.search(r'(\.story-en\{[^}]+\})', content)
        if story_en_match:
            insert_after = story_en_match.group(0)
            content = content.replace(insert_after, insert_after + '\n' + CSS_ADDITION)

    # 2. Replace section 2 body
    # Find the section 2 body: starts after sec-body div, contains robo-msg and story-en
    # Pattern: from the robo inside section 2 through the closing story-en div
    # We need to find section 2 specifically (sec-num with coral/2)

    # Strategy: find the sec-body after section 2 header, replace content up to the prog div
    # Look for pattern: section 2 header -> sec-body -> ... -> </div><div class="prog">

    # Find section 2 marker
    sec2_pattern = re.compile(
        r'(<div class="sec-hdr"><div class="sec-num" style="background:var\(--coral\);">2</div>.*?</div>\s*</div>\s*)'
        r'(.*?)'  # optional image/extra divs before sec-body
        r'(<div class="sec-body">.*?)'  # sec-body start
        r'(.*?)'  # THE CONTENT WE REPLACE
        r'(</div><div class="prog"><div class="prog-fill" style="width:22)',
        re.DOTALL
    )

    # Simpler approach: find everything between sec-body of section2 and the prog bar
    # Section 2 is identified by coral background and number 2

    # Find the sec-body that belongs to section 2
    # Pattern: after the sec-hdr with "2", find sec-body content

    # Let's try a different approach: find the robo content in section 2 and replace it
    # We know section 2 has coral background

    # Most reliable: find from after "<div class="sec-body">" (section 2's) to before "</div><div class="prog"><div class="prog-fill" style="width:22"

    # Find section 2 start
    sec2_hdr = re.search(
        r'<div class="sec-hdr"><div class="sec-num" style="background:var\(--coral\);">2</div>',
        content
    )
    if not sec2_hdr:
        print(f"  SKIP {fname}: no section 2 header found")
        return False

    sec2_start = sec2_hdr.start()

    # Find the sec-body after section 2
    sec_body_match = re.search(r'<div class="sec-body">', content[sec2_start:])
    if not sec_body_match:
        print(f"  SKIP {fname}: no sec-body in section 2")
        return False

    body_start = sec2_start + sec_body_match.end()

    # Find the prog bar after section 2's content
    # Look for </div><div class="prog"> after body_start
    prog_match = re.search(r'</div><div class="prog"><div class="prog-fill" style="width:22', content[body_start:])
    if not prog_match:
        print(f"  SKIP {fname}: no prog bar found after section 2")
        return False

    body_end = body_start + prog_match.start()

    old_body = content[body_start:body_end]

    # Also handle any image div or extra styling that may be between sec-hdr and sec-body
    # We want to remove the inline image if present and any extra robo divs before sec-body

    # Check if there's extra content between sec2_hdr and sec-body (like an image)
    between_hdr_body = content[sec2_hdr.end():sec2_start + sec_body_match.start()]

    # Build replacement: we keep from sec2_hdr to sec-body start, then insert new content
    # But we want to remove any inline image between header and sec-body

    # Simplify: replace from after </div></div> (header) to just before prog
    # Let me reconstruct the entire section 2 body

    # Find everything from after section 2 header closing to prog bar
    # Section 2 header ends with </div></div>
    hdr_end_search = content[sec2_start:]
    # find </div></div> after the sec-hdr
    hdr_close = re.search(r'</div>\s*</div>\s*</div>', hdr_end_search)
    if not hdr_close:
        # Try simpler pattern
        hdr_close = re.search(r'SHORT STORY</div></div>\s*</div>', hdr_end_search)

    # OK let's just replace the body content between <div class="sec-body"> and the next prog bar
    # New approach: replace the old_body with new_body, wrapping properly

    # Build new: starts with \n, then robo wrapper, content, close
    new_content_block = f'''
<div class="robo">
  <div class="robo-av"><img src="https://pub-a418b5aad0bd4c3fb41cf7159403fc12.r2.dev/images/robo/robo.png" alt="Robo"></div>
{new_body}
'''

    content = content[:body_start] + new_content_block + content[body_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK {fname}: key=\"{key_sentence[:40]}...\"")
    return True


def main():
    files = sorted(glob.glob(os.path.join(BASE, 'week*.html')))
    skip = {'week01a.html', 'week02a.html'}

    updated = 0
    skipped = 0
    errors = 0

    for f in files:
        fname = os.path.basename(f)
        if fname in skip:
            print(f"  SKIP {fname}: already done")
            skipped += 1
            continue

        try:
            if process_file(f):
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR {fname}: {e}")
            errors += 1

    print(f"\n=== DONE: {updated} updated, {skipped} skipped, {errors} errors ===")


if __name__ == '__main__':
    main()

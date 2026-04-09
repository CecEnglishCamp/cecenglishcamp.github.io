#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expand Section 2 stories for all G4 lesson files (108 files)."""

import re, glob, html, os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Book assignments by week ──
def get_book(w):
    if w <= 4: return ("Wind in the Willows", "버드나무에 부는 바람")
    if w <= 8: return ("The Wizard of Oz", "오즈의 마법사")
    if w <= 12: return ("Pollyanna", "폴리아나")
    if w <= 16: return ("Mary Poppins", "메리 포핀스")
    if w <= 20: return ("Charlotte's Web", "샬롯의 거미줄")
    if w <= 24: return ("The Secret Garden", "비밀의 정원")
    if w <= 27: return ("A Christmas Carol", "크리스마스 캐럴")
    if w <= 31: return ("Alice in Wonderland", "이상한 나라의 앨리스")
    return ("Tom Sawyer", "톰 소여")

# ── Story data ──
STORIES = {}

# ═══════════════════════════════════════════════
# W01: Wind in the Willows — Mole goes up/outside
# ═══════════════════════════════════════════════
STORIES["week01a"] = (
    "안녕, 친구들! 오늘부터 새로운 이야기가 시작돼요! 📖\n"
    "이 이야기는 '버드나무에 부는 바람'이에요.\n"
    "영국 작가 케네스 그레이엄이 쓴 아름다운 동화예요.\n"
    "주인공은 두더지, 쥐, 두꺼비, 오소리예요.\n"
    "두더지는 땅 속 깊은 곳에서 살았어요.\n"
    "어둡고 좁은 집이었지만 두더지의 집이었어요. 🏠\n"
    "어느 봄날, 따뜻한 바람이 땅 속까지 들어왔어요.\n"
    "두더지는 갑자기 밖이 궁금해졌어요.\n"
    "두더지는 앞발로 흙을 파기 시작했어요.\n"
    "점점 위로, 위로, 위로 올라갔어요!\n"
    "마침내 밝은 햇빛이 보였어요! ☀️\n"
    "<strong>두더지가 위로 올라갔어요!</strong>",
    # A1
    "Mole lived under the ground.\n"
    "It was dark down there.\n"
    "One spring day, he wanted to go outside.\n"
    "Mole went up.",
    # A2
    "Mole had always lived deep underground in his little home.\n"
    "One beautiful spring day, warm air came down into his tunnel.\n"
    "He felt excited and started digging upward.\n"
    "He dug and dug until he saw bright sunlight.\n"
    "Mole went up into the fresh air for the first time.\n"
    "The whole world was green and beautiful above him."
)

STORIES["week01b"] = (
    "두더지가 땅 위로 올라왔어요! 🌿\n"
    "세상은 정말 놀라웠어요.\n"
    "초록색 풀이 반짝이고 있었어요.\n"
    "꽃들이 알록달록 피어 있었어요. 🌸\n"
    "나비가 날아다니고 새들이 노래했어요.\n"
    "두더지는 너무 신이 났어요!\n"
    "\"이게 바로 세상이구나!\" 두더지가 외쳤어요.\n"
    "두더지는 걷고 또 걸었어요.\n"
    "모든 것이 새롭고 신기했어요.\n"
    "두더지는 밖으로 나가기로 결심했어요! 💪\n"
    "<strong>두더지는 밖으로 나가기로 결심했어요!</strong>",
    # A1
    "Mole came out of the ground.\n"
    "Everything was green and beautiful.\n"
    "He was so happy and excited.\n"
    "Mole decided to go up outside.",
    # A2
    "Mole stepped into the sunlight for the very first time.\n"
    "Green grass stretched out everywhere around him.\n"
    "Flowers bloomed in every color he could imagine.\n"
    "Mole decided to go up outside and never go back.\n"
    "He walked and walked, feeling the warm breeze.\n"
    "Everything was new and wonderful to his eyes."
)

STORIES["week01c"] = (
    "두더지는 이제 완전히 밖에 나왔어요! 🌍\n"
    "땅 속 집은 이제 까맣게 잊어버렸어요.\n"
    "넓은 들판이 펼쳐져 있었어요.\n"
    "강물이 반짝반짝 빛나고 있었어요. ✨\n"
    "두더지는 숲도 보고 언덕도 보았어요.\n"
    "\"세상은 정말 크고 넓구나!\"\n"
    "두더지는 두근두근 가슴이 뛰었어요.\n"
    "무서웠지만 용기를 냈어요.\n"
    "새로운 곳을 탐험하고 싶었어요.\n"
    "두더지는 집을 떠나 세상을 탐험하기로 했어요! 🗺️\n"
    "<strong>두더지는 집을 떠나 세상을 탐험하기로 했어요!</strong>",
    # A1
    "Mole saw the big world outside.\n"
    "There were fields and rivers.\n"
    "He was brave and curious.\n"
    "Mole decided to leave home and explore the world.",
    # A2
    "Mole had never seen anything so beautiful before.\n"
    "Wide fields and a shining river stretched before him.\n"
    "He saw forests and hills he had never known about.\n"
    "Mole decided to leave home and explore the world bravely.\n"
    "His heart was beating fast with excitement and a little fear.\n"
    "But he knew he could not stay underground forever."
)

# ═══════════════════════════════════════════════
# W02: Meets Rat
# ═══════════════════════════════════════════════
STORIES["week02a"] = (
    "두더지는 강가를 걷고 있었어요. 🌊\n"
    "물이 졸졸졸 흐르는 소리가 들렸어요.\n"
    "갑자기 강 건너편에서 누군가가 손을 흔들었어요!\n"
    "작은 동물이 배 위에 앉아 있었어요. 🛶\n"
    "\"안녕! 나는 강쥐야!\" 그 동물이 말했어요.\n"
    "강쥐는 친절한 미소를 지었어요.\n"
    "두더지는 처음 보는 친구가 반가웠어요.\n"
    "강쥐가 배를 저어서 이쪽으로 왔어요.\n"
    "두더지는 강쥐를 만나서 기뻤어요.\n"
    "새 친구가 생겼어요! 🤝\n"
    "<strong>두더지는 강쥐를 만났어요!</strong>",
    # A1
    "Mole walked by the river.\n"
    "He saw someone waving.\n"
    "It was a kind animal called Rat.\n"
    "He met Rat.",
    # A2
    "Mole was walking along the beautiful riverbank.\n"
    "He heard the sound of water flowing gently.\n"
    "Suddenly, a friendly animal waved from across the river.\n"
    "He met Rat, who was sitting on a small boat.\n"
    "Rat rowed his boat over and smiled at Mole.\n"
    "It was the beginning of a wonderful friendship."
)

STORIES["week02b"] = (
    "두더지와 강쥐는 강가에서 이야기를 나눴어요. 💬\n"
    "강쥐는 강에 대해 많은 것을 알고 있었어요.\n"
    "\"강은 정말 멋진 곳이야!\" 강쥐가 말했어요.\n"
    "두더지는 강을 처음 봤어요.\n"
    "물이 반짝반짝 빛나서 너무 예뻤어요. ✨\n"
    "강쥐는 두더지에게 배 타는 법을 알려줬어요.\n"
    "두더지는 무서웠지만 용기를 냈어요.\n"
    "배 위에서 바람이 불었어요.\n"
    "두더지는 강 옆에서 친절한 강쥐를 만났어요!\n"
    "정말 좋은 친구예요! 😊\n"
    "<strong>두더지는 강 옆에서 친절한 강쥐를 만났어요!</strong>",
    # A1
    "Mole and Rat talked by the river.\n"
    "Rat knew many things about the river.\n"
    "They rode in a boat together.\n"
    "He met a friendly Rat by the river.",
    # A2
    "Mole and Rat sat together and talked for a long time.\n"
    "Rat told Mole about the wonderful life on the river.\n"
    "He met a friendly Rat by the river that sunny day.\n"
    "Rat showed Mole how to ride in a boat safely.\n"
    "The water sparkled and the wind blew gently.\n"
    "Mole felt happy to have found such a kind new friend."
)

STORIES["week02c"] = (
    "두더지와 강쥐는 배를 타고 강을 내려갔어요. 🛶\n"
    "햇빛이 물 위에서 반짝반짝 빛났어요.\n"
    "강쥐가 맛있는 점심 바구니를 가져왔어요! 🧺\n"
    "빵, 치즈, 레모네이드가 있었어요.\n"
    "두더지는 이렇게 행복한 적이 없었어요.\n"
    "\"고마워, 강쥐야. 넌 정말 좋은 친구야.\"\n"
    "강쥐가 웃으며 말했어요.\n"
    "\"우리 앞으로 매일 함께 놀자!\"\n"
    "두더지는 강쥐를 만나서 친구가 되었어요.\n"
    "세상에 나온 보람이 있었어요! 🌟\n"
    "<strong>두더지는 강가에서 강쥐를 만나 친구가 되었어요!</strong>",
    # A1
    "Mole and Rat had a picnic on the river.\n"
    "They ate bread and cheese together.\n"
    "They became very good friends.\n"
    "He met Rat by the river and they became friends.",
    # A2
    "Mole and Rat floated down the river in a little boat.\n"
    "Rat brought a basket full of delicious food for lunch.\n"
    "They ate bread, cheese, and drank cold lemonade.\n"
    "He met Rat by the river and they became friends forever.\n"
    "Mole had never felt so happy in his whole life.\n"
    "Coming out of his underground home was the best decision ever."
)

# ═══════════════════════════════════════════════
# W03: Toad loves cars
# ═══════════════════════════════════════════════
STORIES["week03a"] = (
    "두더지와 강쥐에게 새로운 친구가 있어요! 🐸\n"
    "그 친구는 바로 두꺼비예요.\n"
    "두꺼비는 강가 마을에서 가장 부자였어요.\n"
    "큰 저택에 살았어요. 🏰\n"
    "두꺼비는 항상 새로운 것에 빠졌어요.\n"
    "보트를 좋아하다가, 말을 좋아하다가...\n"
    "어느 날 자동차를 발견했어요! 🚗\n"
    "\"와아! 이게 뭐야!\" 두꺼비가 소리쳤어요.\n"
    "두꺼비의 눈이 커졌어요.\n"
    "두꺼비는 자동차를 너무너무 좋아했어요!\n"
    "<strong>두꺼비는 자동차를 너무 좋아했어요!</strong>",
    # A1
    "Toad was a rich animal.\n"
    "He loved new things.\n"
    "One day he saw a car.\n"
    "Toad loved cars.",
    # A2
    "Toad was the richest animal living by the river.\n"
    "He lived in a beautiful big house called Toad Hall.\n"
    "One day a motor car drove past him on the road.\n"
    "Toad loved cars from the very first moment he saw one.\n"
    "His eyes grew wide and he could not stop staring.\n"
    "He forgot about boats and horses and only wanted cars."
)

STORIES["week03b"] = (
    "두꺼비는 자동차에 완전히 빠졌어요! 🚗💨\n"
    "매일 자동차만 생각했어요.\n"
    "\"빠르게 달리는 건 정말 최고야!\"\n"
    "두꺼비는 자동차를 한 대 샀어요.\n"
    "그리고 또 한 대 샀어요.\n"
    "벌써 다섯 대째예요! 😱\n"
    "강쥐와 두더지가 걱정했어요.\n"
    "\"두꺼비야, 너무 위험해!\"\n"
    "하지만 두꺼비는 듣지 않았어요.\n"
    "빠른 자동차를 너무너무 좋아했어요!\n"
    "<strong>두꺼비는 빠른 자동차를 너무 좋아했어요!</strong>",
    # A1
    "Toad bought many cars.\n"
    "He drove very fast.\n"
    "His friends were worried.\n"
    "Toad loved fast motor cars too much.",
    # A2
    "Toad could not stop thinking about motor cars.\n"
    "He bought one car after another, spending lots of money.\n"
    "Toad loved fast motor cars too much for his own good.\n"
    "He drove faster and faster every single day.\n"
    "Rat and Mole tried to warn him about the danger.\n"
    "But Toad just laughed and drove even faster."
)

STORIES["week03c"] = (
    "두꺼비는 또 새 차를 사러 갔어요. 🚗\n"
    "이번에는 가장 빠른 차를 골랐어요.\n"
    "\"이 차가 제일 빠르다고? 좋아!\"\n"
    "두꺼비는 신나서 운전을 시작했어요.\n"
    "점점 더 빠르게, 더 빠르게! 💨\n"
    "나무가 쌩쌩 지나갔어요.\n"
    "동물 친구들이 깜짝 놀라서 피했어요.\n"
    "강쥐가 한숨을 쉬었어요.\n"
    "\"두꺼비는 자기가 주체를 못 해...\"\n"
    "두꺼비는 빠른 차를 조절할 수 없을 만큼 좋아했어요.\n"
    "<strong>두꺼비는 빠른 차를 조절할 수 없을 만큼 좋아했어요!</strong>",
    # A1
    "Toad bought the fastest car.\n"
    "He drove too fast.\n"
    "His friends were very worried.\n"
    "Toad loved fast cars more than he could control.",
    # A2
    "Toad went out and bought the fastest car he could find.\n"
    "He drove it through the countryside at amazing speed.\n"
    "Trees and houses flew past in a blur.\n"
    "Toad loved fast cars more than he could control or stop.\n"
    "Other animals had to jump out of the way when he passed.\n"
    "Rat shook his head sadly, knowing trouble was coming."
)

# ═══════════════════════════════════════════════
# W04: Toad gets in trouble
# ═══════════════════════════════════════════════
STORIES["week04a"] = (
    "두꺼비가 또 사고를 쳤어요! 💥\n"
    "이번에는 정말 큰 사고였어요.\n"
    "두꺼비는 너무 빠르게 운전했어요.\n"
    "다른 차와 부딪힐 뻔했어요!\n"
    "경찰이 두꺼비를 잡았어요. 👮\n"
    "\"너는 너무 빠르게 운전했어!\"\n"
    "두꺼비는 벌금을 내야 했어요.\n"
    "하지만 두꺼비는 반성하지 않았어요.\n"
    "\"에이, 별거 아니야!\" 두꺼비가 말했어요.\n"
    "두꺼비는 결국 문제에 빠졌어요! 😰\n"
    "<strong>두꺼비는 결국 문제에 빠졌어요!</strong>",
    # A1
    "Toad drove too fast again.\n"
    "The police caught him.\n"
    "He had to pay money.\n"
    "Toad got in trouble.",
    # A2
    "Toad was driving his car much too fast as usual.\n"
    "He almost crashed into another car on the road.\n"
    "A policeman stopped him and was very angry.\n"
    "Toad got in trouble and had to pay a fine.\n"
    "But Toad did not feel sorry at all about what happened.\n"
    "His friends worried that worse trouble was coming soon."
)

STORIES["week04b"] = (
    "두꺼비는 또 차를 몰았어요. 🚗\n"
    "이번에는 남의 차를 가져갔어요!\n"
    "\"이 차 정말 멋지다!\" 두꺼비가 외쳤어요.\n"
    "두꺼비는 그 차를 타고 달렸어요.\n"
    "경찰이 다시 두꺼비를 잡았어요! 🚔\n"
    "이번에는 정말 큰 벌을 받았어요.\n"
    "감옥에 갇히게 되었어요. 😱\n"
    "강쥐와 두더지가 슬퍼했어요.\n"
    "\"우리가 더 말렸어야 했는데...\"\n"
    "두꺼비는 나쁜 습관 때문에 곤란해졌어요.\n"
    "<strong>두꺼비는 나쁜 습관 때문에 곤란해졌어요!</strong>",
    # A1
    "Toad took someone else's car.\n"
    "The police caught him again.\n"
    "He went to prison.\n"
    "Toad got in trouble because of his habits.",
    # A2
    "Toad could not resist when he saw a beautiful new car.\n"
    "He took it without asking and drove it away fast.\n"
    "The police chased him and caught him right away.\n"
    "Toad got in trouble because of his habits and bad choices.\n"
    "This time the punishment was very serious indeed.\n"
    "Poor Toad was sent to prison for a very long time."
)

STORIES["week04c"] = (
    "두꺼비는 감옥에 갇혀 있었어요. 😔\n"
    "차가운 감옥 안에서 두꺼비는 후회했어요.\n"
    "\"내가 왜 말을 안 들었을까...\"\n"
    "강쥐와 두더지의 충고가 생각났어요.\n"
    "\"조심해!\" \"그만해!\" 친구들이 말했었죠.\n"
    "하지만 두꺼비는 듣지 않았어요.\n"
    "감옥 창밖으로 하늘이 보였어요. 🌅\n"
    "두꺼비는 눈물이 났어요.\n"
    "\"다시 돌아가면 꼭 말을 들을 거야.\"\n"
    "두꺼비는 말을 듣지 않아서 문제에 빠졌어요.\n"
    "<strong>두꺼비는 절대 말을 듣지 않아서 문제에 빠졌어요!</strong>",
    # A1
    "Toad was in prison now.\n"
    "He felt very sorry.\n"
    "He wished he had listened.\n"
    "Toad got into trouble because he never listened.",
    # A2
    "Toad sat alone in his cold, dark prison cell.\n"
    "He remembered how his friends had warned him many times.\n"
    "They told him to stop driving so fast and so recklessly.\n"
    "Toad got into trouble because he never listened to anyone.\n"
    "Now he had tears in his eyes and felt truly sorry.\n"
    "He promised himself he would change if he ever got out."
)

# ═══════════════════════════════════════════════
# W05: Wizard of Oz — Dorothy misses home
# ═══════════════════════════════════════════════
STORIES["week05a"] = (
    "새로운 이야기가 시작돼요! 🌪️\n"
    "오즈의 마법사를 만나볼 시간이에요.\n"
    "도로시는 캔자스에서 살고 있었어요.\n"
    "엠 이모와 헨리 아저씨와 함께요.\n"
    "그리고 작은 강아지 토토도 있었어요! 🐕\n"
    "어느 날 엄청난 회오리바람이 왔어요.\n"
    "집이 빙글빙글 돌았어요!\n"
    "도로시는 정신을 차려보니 낯선 곳에 있었어요.\n"
    "\"여기가 어디야? 집에 가고 싶어!\"\n"
    "도로시는 집이 그리웠어요. 😢\n"
    "<strong>도로시는 집이 그리웠어요!</strong>",
    # A1
    "Dorothy lived in Kansas.\n"
    "A big storm took her away.\n"
    "She was in a strange place.\n"
    "Dorothy missed home.",
    # A2
    "Dorothy lived on a farm in Kansas with her aunt and uncle.\n"
    "One day a terrible tornado picked up her whole house.\n"
    "When she woke up, she was in a strange colorful land.\n"
    "Dorothy missed home and wanted to go back to Kansas.\n"
    "She hugged her little dog Toto and tried not to cry.\n"
    "She wondered if she would ever see her family again."
)

STORIES["week05b"] = (
    "도로시는 낯선 나라에서 울고 있었어요. 😢\n"
    "예쁜 꽃들이 피어 있었지만 마음이 아팠어요.\n"
    "\"우리 집에 있는 엠 이모가 보고 싶어.\"\n"
    "토토가 도로시 곁에서 꼬리를 흔들었어요. 🐕\n"
    "도로시는 토토를 꼭 안았어요.\n"
    "\"걱정 마, 토토. 꼭 집에 갈 거야.\"\n"
    "하지만 어떻게 집에 가는지 몰랐어요.\n"
    "도로시는 집에 가는 게 세상에서 가장 하고 싶었어요.\n"
    "좋은 마녀가 나타나 도와주겠다고 했어요.\n"
    "도로시에게 희망이 생겼어요! 🌟\n"
    "<strong>도로시는 무엇보다 집에 가고 싶었어요!</strong>",
    # A1
    "Dorothy was in a strange land.\n"
    "She cried because she missed her aunt.\n"
    "A good witch came to help.\n"
    "Dorothy wanted to go home more than anything.",
    # A2
    "Dorothy looked around at the strange and beautiful land.\n"
    "But all she could think about was her home in Kansas.\n"
    "She missed Aunt Em and Uncle Henry so very much.\n"
    "Dorothy wanted to go home more than anything in the world.\n"
    "A kind witch appeared and told her about the Wizard of Oz.\n"
    "Maybe the great Wizard could help her find her way home."
)

STORIES["week05c"] = (
    "도로시는 좋은 마녀에게 이야기를 들었어요. 🧙‍♀️\n"
    "\"오즈의 마법사를 찾아가면 집에 갈 수 있어.\"\n"
    "도로시의 눈이 반짝였어요!\n"
    "\"정말요? 어디로 가면 되나요?\"\n"
    "\"노란 벽돌길을 따라가렴.\"\n"
    "도로시는 토토와 함께 출발했어요. 🐕\n"
    "걸으면서 가족 생각을 했어요.\n"
    "엠 이모의 따뜻한 미소가 떠올랐어요.\n"
    "도로시는 가족이 그리워서 집에 가고 싶었어요.\n"
    "꼭 마법사를 만나서 집에 돌아갈 거예요! 🏠\n"
    "<strong>도로시는 가족이 그리워서 집에 가고 싶었어요!</strong>",
    # A1
    "A witch told Dorothy about the Wizard.\n"
    "Dorothy started walking.\n"
    "She thought about her family.\n"
    "Dorothy wanted to go home because she missed her family.",
    # A2
    "The good witch told Dorothy to follow the yellow brick road.\n"
    "At the end of the road, the great Wizard of Oz lived.\n"
    "Dorothy wanted to go home because she missed her family dearly.\n"
    "She started her journey with Toto by her side.\n"
    "Every step she took, she thought of Aunt Em's warm smile.\n"
    "She was determined to find the Wizard no matter what."
)

# ═══════════════════════════════════════════════
# W06: Follows yellow brick road
# ═══════════════════════════════════════════════
STORIES["week06a"] = (
    "도로시는 노란 벽돌길 위에 서 있었어요. 🟡\n"
    "길이 멀리멀리 이어져 있었어요.\n"
    "반짝반짝 빛나는 노란 벽돌이었어요.\n"
    "\"이 길을 따라가면 마법사를 만날 수 있어!\"\n"
    "도로시는 첫 걸음을 내디뎠어요. 👣\n"
    "토토도 옆에서 함께 걸었어요.\n"
    "길 양쪽에는 예쁜 꽃들이 피어 있었어요.\n"
    "하지만 길은 아주 멀었어요.\n"
    "도로시는 용기를 내서 걸었어요.\n"
    "도로시는 길을 따라갔어요! 🚶‍♀️\n"
    "<strong>도로시는 길을 따라갔어요!</strong>",
    # A1
    "Dorothy saw a yellow road.\n"
    "She started walking on it.\n"
    "Toto walked with her.\n"
    "She followed the road.",
    # A2
    "Dorothy stood at the beginning of the yellow brick road.\n"
    "The golden bricks sparkled in the bright sunshine.\n"
    "She followed the road with Toto running beside her.\n"
    "Beautiful flowers and tall trees lined both sides of the path.\n"
    "The road was very long but Dorothy did not give up.\n"
    "She knew the Wizard was waiting at the end."
)

STORIES["week06b"] = (
    "도로시는 노란 벽돌길을 계속 걸었어요. 🟡\n"
    "길 위에서 허수아비를 만났어요! 🤠\n"
    "\"안녕! 나는 뇌가 없어서 슬퍼.\"\n"
    "도로시는 허수아비에게 말했어요.\n"
    "\"같이 마법사를 찾으러 가자!\"\n"
    "허수아비가 기뻐했어요!\n"
    "다음에는 양철 나무꾼도 만났어요. 🤖\n"
    "\"나는 심장이 없어...\" 양철 나무꾼이 말했어요.\n"
    "도로시는 노란 벽돌길을 따라갔어요.\n"
    "새 친구들과 함께요! 🤝\n"
    "<strong>도로시는 노란 벽돌길을 따라갔어요!</strong>",
    # A1
    "Dorothy met a scarecrow.\n"
    "She also met a tin man.\n"
    "They walked together.\n"
    "She followed the yellow brick road.",
    # A2
    "Dorothy met a scarecrow who wanted a brain to think.\n"
    "Then she met a tin woodman who wished for a heart.\n"
    "She followed the yellow brick road with her new friends.\n"
    "They talked and laughed as they walked along the path.\n"
    "Each friend had something they wanted from the Wizard.\n"
    "Together they were braver than they were alone."
)

STORIES["week06c"] = (
    "도로시와 친구들은 계속 걸었어요. 🚶‍♀️🚶‍♂️🚶\n"
    "그때 숲에서 무서운 소리가 들렸어요!\n"
    "\"으르렁!\" 사자가 나타났어요! 🦁\n"
    "하지만 이 사자는 겁쟁이 사자였어요.\n"
    "\"나는 용기가 없어서 부끄러워...\"\n"
    "도로시가 사자에게 말했어요.\n"
    "\"같이 마법사를 찾으러 가자!\"\n"
    "이제 네 명의 친구가 함께 걸어요.\n"
    "도로시는 마법사를 찾기 위해 노란 벽돌길을 따라갔어요.\n"
    "모두 함께라서 무섭지 않았어요! 💪\n"
    "<strong>도로시는 마법사를 찾기 위해 노란 벽돌길을 따라갔어요!</strong>",
    # A1
    "They met a cowardly lion.\n"
    "He wanted courage.\n"
    "All four walked together.\n"
    "She followed the yellow brick road to find the Wizard.",
    # A2
    "A big lion jumped out from the forest with a loud roar.\n"
    "But he was actually scared of almost everything around him.\n"
    "The lion wanted the Wizard to give him courage.\n"
    "She followed the yellow brick road to find the Wizard of Oz.\n"
    "Now Dorothy, Scarecrow, Tin Man, and Lion walked together.\n"
    "They were not afraid because they had each other."
)

# ═══════════════════════════════════════════════
# W07: Friends need things
# ═══════════════════════════════════════════════
STORIES["week07a"] = (
    "도로시와 친구들이 마법사 앞에 섰어요! 🏰\n"
    "마법사는 크고 무서운 목소리로 말했어요.\n"
    "\"무엇을 원하느냐?\"\n"
    "허수아비가 말했어요. \"뇌를 주세요!\"\n"
    "양철 나무꾼이 말했어요. \"심장을 주세요!\" 💕\n"
    "사자가 말했어요. \"용기를 주세요!\"\n"
    "도로시가 말했어요. \"집에 보내주세요!\"\n"
    "모두 자기에게 없는 것이 필요했어요.\n"
    "친구들은 각자 필요한 것이 있었어요.\n"
    "마법사가 도와줄 수 있을까요? 🤔\n"
    "<strong>친구들은 각자 필요한 것이 있었어요!</strong>",
    # A1
    "Scarecrow wanted a brain.\n"
    "Tin Man wanted a heart.\n"
    "Lion wanted courage.\n"
    "Her friends needed things.",
    # A2
    "Dorothy and her friends finally stood before the great Wizard.\n"
    "The Wizard's voice was loud and powerful in the big room.\n"
    "Each friend asked for what they believed they were missing.\n"
    "Her friends needed things they thought they did not have.\n"
    "Scarecrow wanted a brain, Tin Man wanted a heart.\n"
    "Lion wanted courage, and Dorothy just wanted to go home."
)

STORIES["week07b"] = (
    "마법사가 친구들에게 비밀을 알려줬어요! 🤫\n"
    "\"허수아비야, 넌 이미 똑똒해!\"\n"
    "허수아비는 길을 잘 찾아줬잖아요.\n"
    "\"양철 나무꾼아, 넌 이미 따뜻한 마음이 있어!\" 💗\n"
    "양철 나무꾼은 항상 친구를 걱정했어요.\n"
    "\"사자야, 넌 이미 용감해!\"\n"
    "사자는 무서워도 친구를 지켰어요.\n"
    "친구들은 각자 안에 필요한 것이 있었어요.\n"
    "그걸 몰랐을 뿐이에요!\n"
    "정말 놀라운 발견이었어요! ✨\n"
    "<strong>친구들은 각자 안에 필요한 것이 있었어요!</strong>",
    # A1
    "The Wizard told them a secret.\n"
    "They already had what they needed.\n"
    "They just did not know it.\n"
    "Her friends each needed something inside.",
    # A2
    "The Wizard shared an important secret with each friend.\n"
    "Scarecrow had been smart the whole time on their journey.\n"
    "Tin Man had shown a warm heart by caring for others.\n"
    "Her friends each needed something inside that they already had.\n"
    "Lion had been brave whenever his friends were in danger.\n"
    "They just needed someone to tell them the truth."
)

STORIES["week07c"] = (
    "친구들은 마법사의 말을 듣고 눈물이 났어요. 😢\n"
    "허수아비는 자기가 똑똑하다는 걸 알았어요.\n"
    "양철 나무꾼은 이미 사랑할 줄 알았어요.\n"
    "사자는 이미 용감했어요.\n"
    "\"우리 안에 이미 있었구나!\" 💡\n"
    "도로시도 깨달았어요.\n"
    "친구들이 함께해서 여기까지 올 수 있었어요.\n"
    "친구들에게 필요한 것은 마음과 용기였어요.\n"
    "그것은 이미 그들 안에 있었어요!\n"
    "정말 감동적인 순간이었어요! 🌈\n"
    "<strong>친구들에게 필요한 것은 마음과 용기, 이미 그들 안에 있었어요!</strong>",
    # A1
    "Scarecrow was already smart.\n"
    "Tin Man already had love.\n"
    "Lion was already brave.\n"
    "Her friends needed heart and courage already inside them.",
    # A2
    "The friends finally understood the Wizard's wonderful lesson.\n"
    "Scarecrow had solved every problem on their long journey.\n"
    "Tin Man had cried real tears when his friends were hurt.\n"
    "Lion had fought enemies even when he was terrified inside.\n"
    "Her friends needed heart and courage already inside them all along.\n"
    "Sometimes we already have what we are looking for."
)

# ═══════════════════════════════════════════════
# W08: Home is best
# ═══════════════════════════════════════════════
STORIES["week08a"] = (
    "친구들의 문제는 해결되었어요! 🎉\n"
    "이제 도로시 차례예요.\n"
    "\"마법사님, 저를 집에 보내주세요!\"\n"
    "마법사가 고개를 숙였어요.\n"
    "\"사실 나는 진짜 마법사가 아니란다.\"\n"
    "도로시는 실망했어요. 😔\n"
    "하지만 좋은 마녀가 나타났어요!\n"
    "\"도로시야, 네 은색 신발을 세 번 부딪쳐봐.\"\n"
    "도로시는 눈을 감고 말했어요.\n"
    "\"집이 최고야! 집이 최고야!\" 🏠\n"
    "<strong>집이 최고예요!</strong>",
    # A1
    "Dorothy wanted to go home.\n"
    "The Wizard could not help her.\n"
    "A good witch helped her.\n"
    "Home is the best.",
    # A2
    "Dorothy's friends all got what they needed at last.\n"
    "Now it was Dorothy's turn to get help from the Wizard.\n"
    "But the Wizard admitted he was not really magical at all.\n"
    "Home is the best place in the world, Dorothy believed.\n"
    "The good witch told her to click her silver shoes together.\n"
    "Dorothy closed her eyes and wished to go home."
)

STORIES["week08b"] = (
    "도로시는 은색 신발을 세 번 부딪쳤어요! ✨\n"
    "\"집 같은 곳은 없어! 집 같은 곳은 없어!\"\n"
    "바람이 불고 세상이 빙글빙글 돌았어요. 🌀\n"
    "도로시는 눈을 떴어요.\n"
    "캔자스의 농장이 보였어요!\n"
    "엠 이모가 달려왔어요! 🤗\n"
    "\"도로시야! 어디 갔었니!\"\n"
    "도로시는 이모를 꼭 안았어요.\n"
    "집 같은 곳은 세상에 없어요.\n"
    "도로시는 그걸 알았어요! 💕\n"
    "<strong>집 같은 곳은 세상에 없어요!</strong>",
    # A1
    "Dorothy clicked her shoes.\n"
    "She was back in Kansas.\n"
    "She hugged Aunt Em.\n"
    "There is no place like home.",
    # A2
    "Dorothy clicked her silver shoes together three times.\n"
    "Everything spun around her like a whirlwind.\n"
    "When she opened her eyes, she was back on the farm.\n"
    "There is no place like home, Dorothy said with happy tears.\n"
    "Aunt Em ran to her and they hugged each other tightly.\n"
    "Dorothy knew she would never take her home for granted again."
)

STORIES["week08c"] = (
    "도로시는 캔자스의 집으로 돌아왔어요! 🏠\n"
    "엠 이모와 헨리 아저씨가 기뻐했어요.\n"
    "토토도 꼬리를 흔들었어요! 🐕\n"
    "도로시는 오즈 나라에서 많은 것을 배웠어요.\n"
    "뇌, 심장, 용기... 모두 이미 안에 있었어요.\n"
    "그리고 가장 중요한 것도 배웠어요.\n"
    "세상에서 가장 좋은 곳은 바로 집이에요.\n"
    "가족이 있는 곳이 진짜 집이에요. 💕\n"
    "도로시는 집만큼 좋은 곳은 정말 없다는 걸 배웠어요.\n"
    "오즈의 마법사 이야기가 끝났어요! 🌈\n"
    "<strong>도로시는 집만큼 좋은 곳은 정말 없다는 걸 배웠어요!</strong>",
    # A1
    "Dorothy was finally home.\n"
    "She learned many things.\n"
    "Family is the most important.\n"
    "She learned there is truly no place like home.",
    # A2
    "Dorothy was finally back in Kansas with her loving family.\n"
    "She thought about her amazing adventure in the Land of Oz.\n"
    "Her friends taught her about brains, hearts, and courage.\n"
    "She learned there is truly no place like home in the world.\n"
    "The most important thing was the love of her family.\n"
    "Dorothy smiled and knew she was exactly where she belonged."
)

# ═══════════════════════════════════════════════
# W09: Pollyanna — Plays glad game
# ═══════════════════════════════════════════════
STORIES["week09a"] = (
    "새로운 이야기를 시작해요! 🌸\n"
    "폴리아나라는 소녀를 만나볼 거예요.\n"
    "폴리아나의 부모님은 돌아가셨어요.\n"
    "그래서 폴리 이모 집에서 살게 되었어요.\n"
    "폴리 이모는 매우 엄격한 사람이었어요. 😐\n"
    "하지만 폴리아나는 늘 밝게 웃었어요!\n"
    "아빠가 가르쳐준 특별한 놀이가 있었거든요.\n"
    "그것은 바로 기쁨 찾기 놀이예요! 🎮\n"
    "어떤 일이 있어도 기뻐할 것을 찾는 거예요.\n"
    "폴리아나는 기쁨 찾기 놀이를 했어요!\n"
    "<strong>폴리아나는 기쁨 찾기 놀이를 했어요!</strong>",
    # A1
    "Pollyanna lost her parents.\n"
    "She went to live with her aunt.\n"
    "But she always smiled.\n"
    "She played the glad game.",
    # A2
    "Pollyanna was a young girl whose parents had passed away.\n"
    "She went to live with her strict Aunt Polly in a big house.\n"
    "Her father had taught her a special game before he died.\n"
    "She played the glad game to find something happy every day.\n"
    "No matter what happened, she looked for the bright side.\n"
    "This simple game changed the way she saw the world."
)

STORIES["week09b"] = (
    "폴리 이모가 폴리아나에게 다락방을 줬어요. 🏠\n"
    "다락방은 덥고 가구도 없었어요.\n"
    "보통 아이라면 슬퍼했을 거예요.\n"
    "하지만 폴리아나는 달랐어요! 😊\n"
    "\"거울이 없어서 다행이야! 내 주근깨를 안 봐도 돼!\"\n"
    "폴리아나는 항상 좋은 면을 찾았어요.\n"
    "이것이 바로 기쁨 찾기 놀이예요!\n"
    "폴리아나는 항상 기쁨 찾기 놀이를 했어요.\n"
    "어떤 상황에서도 기뻐할 이유를 찾았어요.\n"
    "정말 대단한 아이예요! 🌟\n"
    "<strong>폴리아나는 항상 기쁨 찾기 놀이를 했어요!</strong>",
    # A1
    "Aunt gave her a hot attic room.\n"
    "Pollyanna did not cry.\n"
    "She found something good about it.\n"
    "Pollyanna always played the glad game.",
    # A2
    "Aunt Polly gave Pollyanna a small, hot room in the attic.\n"
    "There was no mirror, no pictures, and very little furniture.\n"
    "But Pollyanna smiled and found something to be happy about.\n"
    "Pollyanna always played the glad game in every situation.\n"
    "She said she was glad there was no mirror to see her freckles.\n"
    "Her positive attitude amazed everyone who met her."
)

STORIES["week09c"] = (
    "폴리아나는 새 마을에서 살기 시작했어요. 🏘️\n"
    "마을 사람들은 처음에 이상하게 생각했어요.\n"
    "\"왜 저 아이는 항상 웃지?\"\n"
    "폴리아나가 아픈 할머니를 만났어요.\n"
    "할머니는 매일 불평했어요. 😩\n"
    "폴리아나가 말했어요.\n"
    "\"할머니, 오늘 햇빛이 정말 따뜻하잖아요!\"\n"
    "할머니가 처음으로 미소를 지었어요. 😊\n"
    "폴리아나는 항상 기뻐할 것을 찾았어요.\n"
    "그것이 폴리아나의 특별한 힘이었어요! ✨\n"
    "<strong>폴리아나는 항상 기뻐할 것을 찾았어요!</strong>",
    # A1
    "Pollyanna moved to a new town.\n"
    "She met many people.\n"
    "She made them smile.\n"
    "Pollyanna always found something to be glad about.",
    # A2
    "Pollyanna started her new life in the small town.\n"
    "The townspeople were surprised by her endless happiness.\n"
    "She visited a sick old woman who complained about everything.\n"
    "Pollyanna always found something to be glad about around her.\n"
    "She told the woman to enjoy the warm sunshine through the window.\n"
    "For the first time in years, the old woman smiled."
)

# ═══════════════════════════════════════════════
# W10: Finds good things
# ═══════════════════════════════════════════════
STORIES["week10a"] = (
    "폴리아나는 마을 사람들을 하나씩 바꾸고 있었어요! 🌟\n"
    "화가 나 있던 할아버지를 만났어요.\n"
    "\"세상은 나빠!\" 할아버지가 말했어요.\n"
    "폴리아나가 웃으며 말했어요.\n"
    "\"할아버지, 저 예쁜 꽃을 보세요! 🌻\"\n"
    "할아버지가 꽃을 보고 조금 웃었어요.\n"
    "폴리아나는 어디서나 좋은 것을 찾았어요.\n"
    "비가 와도 기뻐했어요.\n"
    "\"비 온 뒤에 무지개가 뜨잖아요!\" 🌈\n"
    "폴리아나는 좋은 것을 찾았어요!\n"
    "<strong>폴리아나는 좋은 것을 찾았어요!</strong>",
    # A1
    "Pollyanna met an angry old man.\n"
    "She showed him a flower.\n"
    "He smiled a little.\n"
    "She found good things.",
    # A2
    "Pollyanna met an old man who was angry at the world.\n"
    "He said everything was bad and nothing was worth smiling for.\n"
    "Pollyanna pointed to a beautiful flower in his garden.\n"
    "She found good things everywhere she looked around her.\n"
    "Even when it rained, she said rainbows would come soon.\n"
    "Slowly, the old man started to see the world differently."
)

STORIES["week10b"] = (
    "마을에 불평이 많은 아주머니가 있었어요. 😤\n"
    "\"날씨가 너무 더워! 음식도 맛없어!\"\n"
    "폴리아나가 아주머니를 찾아갔어요.\n"
    "\"아주머니, 오늘 새가 정말 예쁘게 노래해요! 🐦\"\n"
    "아주머니가 귀를 기울였어요.\n"
    "정말 새 소리가 아름다웠어요.\n"
    "\"음... 그건 그렇네.\"\n"
    "아주머니가 처음으로 미소를 지었어요!\n"
    "폴리아나는 모든 상황에서 좋은 것을 찾았어요.\n"
    "그것이 마법 같은 힘이었어요! ✨\n"
    "<strong>폴리아나는 모든 상황에서 좋은 것을 찾았어요!</strong>",
    # A1
    "A woman in town always complained.\n"
    "Pollyanna visited her.\n"
    "She showed her the bird song.\n"
    "She found good in every situation.",
    # A2
    "There was a woman in town who complained about everything.\n"
    "The weather was too hot, the food was too cold, nothing was right.\n"
    "Pollyanna visited her and pointed out a singing bird outside.\n"
    "She found good in every situation no matter how bad it seemed.\n"
    "The woman listened and heard the beautiful song for the first time.\n"
    "A small smile appeared on her face and she felt a little better."
)

STORIES["week10c"] = (
    "폴리아나의 기쁨 찾기 놀이가 마을에 퍼졌어요! 🌍\n"
    "사람들이 하나둘씩 기쁨을 찾기 시작했어요.\n"
    "빵집 아저씨는 매일 빵을 나눠줬어요. 🍞\n"
    "의사 선생님은 무료로 치료해줬어요.\n"
    "모두가 서로에게 친절해졌어요.\n"
    "폴리아나가 마을을 바꾸고 있었어요! 💕\n"
    "친절함은 폴리아나의 타고난 성격이었어요.\n"
    "그래서 항상 좋은 것을 찾을 수 있었어요.\n"
    "폴리아나 덕분에 마을이 밝아졌어요.\n"
    "친절함이 세상을 바꿔요! 🌈\n"
    "<strong>친절함이 타고난 성격이라서 항상 좋은 것을 찾았어요!</strong>",
    # A1
    "The whole town started changing.\n"
    "People became kinder.\n"
    "It was because of Pollyanna.\n"
    "She always found something good because kindness was her nature.",
    # A2
    "The glad game spread through the whole town like magic.\n"
    "The baker started sharing bread with his neighbors.\n"
    "The doctor treated sick people for free with a kind smile.\n"
    "She always found something good because kindness was her nature.\n"
    "People learned to look for the bright side from Pollyanna.\n"
    "The whole town became a warmer and happier place."
)

# ═══════════════════════════════════════════════
# W11: Gets badly hurt
# ═══════════════════════════════════════════════
STORIES["week11a"] = (
    "어느 날 끔찍한 일이 일어났어요. 😱\n"
    "폴리아나가 길을 건너다가 사고가 났어요.\n"
    "자동차에 부딪혔어요!\n"
    "마을 사람들이 달려왔어요.\n"
    "\"폴리아나! 괜찮아?\" 😢\n"
    "폴리아나는 심하게 다쳤어요.\n"
    "다리를 움직일 수 없었어요.\n"
    "의사 선생님이 고개를 저었어요.\n"
    "\"다리가 많이 다쳤습니다.\"\n"
    "폴리아나는 심하게 다쳤어요.\n"
    "<strong>폴리아나는 심하게 다쳤어요.</strong>",
    # A1
    "Pollyanna had an accident.\n"
    "A car hit her.\n"
    "She could not move her legs.\n"
    "She was badly hurt.",
    # A2
    "One terrible day, Pollyanna was crossing the road.\n"
    "A car came too fast and hit her very hard.\n"
    "The townspeople rushed over, crying and calling her name.\n"
    "She was badly hurt and could not move her legs at all.\n"
    "The doctor examined her and looked very worried.\n"
    "Everyone in town was heartbroken about their sunny girl."
)

STORIES["week11b"] = (
    "폴리아나는 침대에 누워 있었어요. 🛏️\n"
    "다리가 아프고 움직일 수 없었어요.\n"
    "폴리아나도 처음으로 슬펐어요. 😢\n"
    "\"기쁨 찾기 놀이를 못 하겠어...\"\n"
    "하지만 곧 마음을 다잡았어요.\n"
    "\"다리가 아프지만... 손은 움직일 수 있잖아!\"\n"
    "\"눈도 볼 수 있고, 귀로 들을 수도 있어!\"\n"
    "폴리아나는 다쳤지만 기쁨을 찾으려 했어요.\n"
    "정말 용감한 아이예요.\n"
    "포기하지 않는 마음이 아름다워요! 💪\n"
    "<strong>폴리아나는 다쳤지만 기쁨을 찾으려 했어요!</strong>",
    # A1
    "Pollyanna was in bed.\n"
    "She could not walk.\n"
    "But she tried to be happy.\n"
    "She was hurt but tried to stay glad.",
    # A2
    "Pollyanna lay in bed feeling sad for the very first time.\n"
    "She could not walk or run or play outside anymore.\n"
    "For a moment, she thought the glad game was impossible.\n"
    "She was hurt but tried to stay glad by counting her blessings.\n"
    "She could still see, hear, and hold her friends' hands.\n"
    "Even in pain, she looked for something to be thankful for."
)

STORIES["week11c"] = (
    "의사 선생님이 폴리아나를 다시 검사했어요. 🏥\n"
    "\"폴리아나, 네 다리는... 걷기 어려울 수 있어.\"\n"
    "폴리아나의 눈에서 눈물이 흘렀어요. 😭\n"
    "걸을 수 없다니... 정말 슬픈 소식이었어요.\n"
    "폴리아나는 창밖을 바라봤어요.\n"
    "나비가 날아다니고 있었어요. 🦋\n"
    "\"나는 걸을 수 없지만... 여전히 기쁨을 찾을 수 있어.\"\n"
    "폴리아나는 걸을 수 없었지만 여전히 기뻐하려 했어요.\n"
    "이것이 진정한 용기예요.\n"
    "폴리아나의 마음은 여전히 강했어요! 💖\n"
    "<strong>폴리아나는 걸을 수 없었지만 여전히 기뻐하려 했어요!</strong>",
    # A1
    "The doctor had bad news.\n"
    "Pollyanna could not walk.\n"
    "She cried but stayed strong.\n"
    "She could not walk but still tried to be glad.",
    # A2
    "The doctor came back with very sad news for everyone.\n"
    "Pollyanna might never be able to walk again on her own.\n"
    "Tears rolled down her cheeks when she heard the truth.\n"
    "She could not walk but still tried to be glad about life.\n"
    "She looked at a butterfly outside and smiled through her tears.\n"
    "Her brave spirit inspired everyone who came to visit her."
)

# ═══════════════════════════════════════════════
# W12: Changes people
# ═══════════════════════════════════════════════
STORIES["week12a"] = (
    "폴리아나가 다쳤다는 소식이 마을에 퍼졌어요. 📢\n"
    "마을 사람들이 하나둘씩 찾아왔어요.\n"
    "\"폴리아나야, 네 덕분에 나는 행복해졌어.\"\n"
    "화가 나있던 할아버지가 꽃을 가져왔어요. 🌷\n"
    "불평하던 아주머니가 케이크를 구워왔어요. 🎂\n"
    "모두가 폴리아나에게 감사했어요.\n"
    "폴리아나는 사람들을 변하게 했어요.\n"
    "기쁨 찾기 놀이의 힘이었어요!\n"
    "한 작은 소녀가 온 마을을 바꿨어요.\n"
    "사랑의 힘은 정말 놀라워요! 💕\n"
    "<strong>폴리아나는 사람들을 변하게 했어요!</strong>",
    # A1
    "The town heard the news.\n"
    "Everyone came to visit.\n"
    "They all thanked her.\n"
    "She changed people.",
    # A2
    "When the town heard about Pollyanna, everyone was very sad.\n"
    "The angry old man brought flowers to her bedside.\n"
    "The complaining woman baked her favorite cake.\n"
    "She changed people with her glad game and warm heart.\n"
    "Everyone realized how much Pollyanna had done for them.\n"
    "One small girl had changed an entire town with kindness."
)

STORIES["week12b"] = (
    "마을 사람들이 매일 폴리아나를 찾아왔어요. 🏥\n"
    "\"우리가 이번엔 널 기쁘게 해줄게!\"\n"
    "할아버지가 재미있는 이야기를 해줬어요. 📖\n"
    "아이들이 노래를 불러줬어요. 🎵\n"
    "심지어 엄격한 폴리 이모도 변했어요!\n"
    "\"폴리아나야, 사랑한다.\" 이모가 처음으로 말했어요. 😢\n"
    "폴리아나의 친절함이 모든 사람을 서서히 바꿨어요.\n"
    "기쁨 찾기 놀이는 다른 사람에게도 전해졌어요.\n"
    "사랑은 돌고 돌아 돌아와요.\n"
    "폴리아나가 뿌린 씨앗이 꽃을 피웠어요! 🌸\n"
    "<strong>폴리아나의 친절함이 서서히 모든 사람을 바꿨어요!</strong>",
    # A1
    "People visited Pollyanna every day.\n"
    "They sang and told stories.\n"
    "Even Aunt Polly changed.\n"
    "Her kindness slowly changed everyone around her.",
    # A2
    "Every day, more and more people came to visit Pollyanna.\n"
    "They brought gifts, told funny stories, and sang happy songs.\n"
    "Even strict Aunt Polly said she loved Pollyanna for the first time.\n"
    "Her kindness slowly changed everyone around her over time.\n"
    "The glad game had spread from one little girl to a whole town.\n"
    "Love given freely always comes back when you need it most."
)

STORIES["week12c"] = (
    "시간이 지나고 놀라운 일이 일어났어요! ✨\n"
    "특별한 의사 선생님이 폴리아나를 치료해줬어요.\n"
    "폴리아나가 조금씩 다리를 움직이기 시작했어요!\n"
    "\"나... 움직일 수 있어!\" 😊\n"
    "마을 사람들이 모두 기뻐했어요.\n"
    "폴리아나의 긍정적인 마음이 기적을 만들었어요.\n"
    "폴리아나의 친절함이 모든 사람을 변화시켰어요.\n"
    "긍정적인 마음은 전염되는 거예요! 🌟\n"
    "우리도 기쁨 찾기 놀이를 해볼까요?\n"
    "오늘 기쁜 일 하나를 찾아봐요! 🌈\n"
    "<strong>폴리아나의 친절함이 모든 사람을 바꿨어요, 긍정은 전염돼요!</strong>",
    # A1
    "A special doctor helped Pollyanna.\n"
    "She started to move her legs.\n"
    "Everyone was so happy.\n"
    "Her kindness changed everyone she met positivity is contagious.",
    # A2
    "A wonderful miracle happened after many weeks of waiting.\n"
    "A special doctor came and treated Pollyanna with great care.\n"
    "Slowly, she began to move her legs again little by little.\n"
    "Her kindness changed everyone she met because positivity is contagious.\n"
    "The whole town celebrated together with tears of joy.\n"
    "Pollyanna proved that a positive heart can overcome anything."
)

# ═══════════════════════════════════════════════
# W13: Mary Poppins — Arrives
# ═══════════════════════════════════════════════
STORIES["week13a"] = (
    "새로운 이야기가 시작돼요! ☂️\n"
    "뱅크스 가족에게는 문제가 있었어요.\n"
    "아이들이 너무 말을 안 들었거든요!\n"
    "제인과 마이클은 유모를 괴롭혔어요. 😱\n"
    "유모가 다 도망갔어요.\n"
    "그때 하늘에서 누군가 내려왔어요!\n"
    "우산을 들고 바람을 타고 온 여자였어요. 🌂\n"
    "\"저는 메리 포핀스예요.\"\n"
    "아이들은 깜짝 놀랐어요.\n"
    "메리 포핀스가 도착했어요! ✨\n"
    "<strong>메리 포핀스가 도착했어요!</strong>",
    # A1
    "The children were naughty.\n"
    "All nannies ran away.\n"
    "A woman flew down from the sky.\n"
    "Mary Poppins arrived.",
    # A2
    "The Banks family had two children, Jane and Michael.\n"
    "They were so naughty that every nanny ran away from them.\n"
    "One windy day, a woman floated down from the sky with an umbrella.\n"
    "Mary Poppins arrived at the Banks house looking very proper.\n"
    "She carried a large carpetbag and a parrot-headed umbrella.\n"
    "The children stared at her with wide eyes full of wonder."
)

STORIES["week13b"] = (
    "메리 포핀스는 보통 유모가 아니었어요! ✨\n"
    "가방에서 큰 거울이 나왔어요.\n"
    "그리고 큰 식물도 나왔어요! 🌿\n"
    "\"어떻게 저 작은 가방에서...?\" 아이들이 놀랐어요.\n"
    "메리 포핀스는 마법을 부리는 것 같았어요.\n"
    "하지만 물어보면 이렇게 대답했어요.\n"
    "\"당연한 거예요.\" 😊\n"
    "아이들에게 도움이 필요해서 메리 포핀스가 왔어요.\n"
    "아이들은 신기하고 두근거렸어요.\n"
    "메리 포핀스와 함께라면 뭐든 가능할 것 같았어요! 🌟\n"
    "<strong>아이들에게 도움이 필요해서 메리 포핀스가 왔어요!</strong>",
    # A1
    "Mary Poppins had a magic bag.\n"
    "Big things came out of it.\n"
    "The children were amazed.\n"
    "Mary Poppins arrived because the children needed help.",
    # A2
    "Mary Poppins opened her small carpetbag in the nursery room.\n"
    "A large mirror and tall plants came out of the tiny bag.\n"
    "The children could not believe their own eyes at all.\n"
    "Mary Poppins arrived because the children needed help and magic.\n"
    "When they asked how she did it, she just said it was obvious.\n"
    "Jane and Michael knew their new nanny was very special."
)

STORIES["week13c"] = (
    "메리 포핀스가 처음 온 날 밤이에요. 🌙\n"
    "아이들은 잠자리에 누웠어요.\n"
    "메리 포핀스가 노래를 불러줬어요.\n"
    "부드럽고 따뜻한 목소리였어요. 🎵\n"
    "아이들은 평화롭게 잠이 들었어요.\n"
    "이전 유모들은 이렇게 해주지 않았어요.\n"
    "메리 포핀스는 정말 마법 같은 사람이었어요.\n"
    "진정으로 마법 같은 사람이 필요했던 아이들이에요.\n"
    "메리 포핀스가 왔으니 모든 게 달라질 거예요.\n"
    "새로운 모험이 기다리고 있어요! ✨\n"
    "<strong>진정으로 마법 같은 사람이 필요해서 메리 포핀스가 왔어요!</strong>",
    # A1
    "Mary Poppins sang to the children.\n"
    "They fell asleep peacefully.\n"
    "She was truly magical.\n"
    "Mary Poppins arrived because the children needed someone truly magical.",
    # A2
    "On her first night, Mary Poppins sang a gentle lullaby.\n"
    "The children closed their eyes and fell asleep peacefully.\n"
    "No nanny had ever made them feel so safe and calm before.\n"
    "Mary Poppins arrived because the children needed someone truly magical.\n"
    "She was strict about manners but gentle in her own special way.\n"
    "The Banks children knew their lives were about to change forever."
)

# ═══════════════════════════════════════════════
# W14: Strict but kind
# ═══════════════════════════════════════════════
STORIES["week14a"] = (
    "메리 포핀스는 규칙이 많았어요. 📋\n"
    "\"방을 깨끗이 치워라!\" \"일찍 자라!\"\n"
    "제인과 마이클은 처음에 싫었어요. 😤\n"
    "하지만 메리 포핀스의 규칙을 따르면...\n"
    "놀라운 마법이 일어났어요! ✨\n"
    "방을 치우면 장난감이 춤을 췄어요!\n"
    "일찍 자면 별나라 여행을 했어요! ⭐\n"
    "메리 포핀스는 엄격하지만 친절했어요.\n"
    "규칙 속에 사랑이 있었어요.\n"
    "아이들은 조금씩 이해하기 시작했어요. 💕\n"
    "<strong>메리 포핀스는 엄격하지만 친절했어요!</strong>",
    # A1
    "Mary Poppins had many rules.\n"
    "The children did not like rules.\n"
    "But magic happened when they listened.\n"
    "She was strict but kind.",
    # A2
    "Mary Poppins gave the children many strict rules to follow.\n"
    "They had to clean their room and go to bed on time.\n"
    "Jane and Michael were annoyed at first and did not understand.\n"
    "She was strict but kind and there was love behind every rule.\n"
    "When they cleaned their room, the toys magically danced.\n"
    "They learned that following rules could lead to amazing adventures."
)

STORIES["week14b"] = (
    "오늘 메리 포핀스가 아이들을 공원에 데려갔어요. 🌳\n"
    "\"바르게 걸어라. 뛰지 마라.\"\n"
    "아이들이 투덜거렸어요.\n"
    "하지만 공원에 도착하자... 🎠\n"
    "그림 속으로 들어갔어요!\n"
    "말을 타고 하늘을 날았어요!\n"
    "\"와아! 이게 뭐야!\" 아이들이 외쳤어요.\n"
    "메리 포핀스는 엄격하지만 친절했어요.\n"
    "그녀가 신경 쓰기 때문이에요.\n"
    "규칙 뒤에 마법이 숨어 있었어요! 🌟\n"
    "<strong>메리 포핀스는 엄격하지만 신경 쓰기 때문에 친절했어요!</strong>",
    # A1
    "Mary Poppins took them to the park.\n"
    "They went inside a painting.\n"
    "They flew on horses.\n"
    "She was strict but kind because she cared.",
    # A2
    "Mary Poppins marched the children to the park very properly.\n"
    "She told them to walk straight and not to run around.\n"
    "But when they reached a painting, she jumped right into it.\n"
    "She was strict but kind because she cared about them deeply.\n"
    "Inside the painting, they rode horses and flew through the sky.\n"
    "The children understood that her strictness was full of love."
)

STORIES["week14c"] = (
    "메리 포핀스와 함께한 지 여러 날이 지났어요. 📅\n"
    "아이들은 많이 변했어요.\n"
    "방도 스스로 치우고, 일찍 잠자리에 들었어요. 🛏️\n"
    "예의 바르게 인사도 했어요.\n"
    "하지만 메리 포핀스는 여전히 엄격했어요.\n"
    "\"칭찬은 하지 않을 거야.\"\n"
    "하지만 밤에 이불을 꼭 덮어줬어요. 💕\n"
    "규칙과 사랑은 함께할 수 있어요.\n"
    "메리 포핀스는 그것을 보여줬어요.\n"
    "엄격함과 친절함이 함께였어요! ✨\n"
    "<strong>규칙과 사랑은 함께할 수 있다고 메리 포핀스가 보여줬어요!</strong>",
    # A1
    "The children changed a lot.\n"
    "They became good and polite.\n"
    "Mary Poppins still tucked them in.\n"
    "She was strict but kind because rules and love can exist together.",
    # A2
    "Days passed and the children became well-behaved and polite.\n"
    "They cleaned their rooms and said please and thank you.\n"
    "Mary Poppins never gave compliments but always tucked them in.\n"
    "She was strict but kind because rules and love can exist together.\n"
    "The children felt safe knowing someone cared enough to be firm.\n"
    "They learned that true kindness sometimes looks like discipline."
)

# ═══════════════════════════════════════════════
# W15: Children feel joy
# ═══════════════════════════════════════════════
STORIES["week15a"] = (
    "오늘은 특별한 날이에요! 🎪\n"
    "메리 포핀스가 아이들을 천장으로 데려갔어요.\n"
    "\"위를 봐!\" 메리 포핀스가 말했어요.\n"
    "아이들이 웃기 시작하자 몸이 둥둥 떠올랐어요! 😂\n"
    "\"웃으면 위로 올라가는 거야!\"\n"
    "아이들은 천장에서 차를 마셨어요! ☕\n"
    "너무 재미있어서 배꼽이 빠질 뻔했어요.\n"
    "아이들은 기쁨을 느꼈어요.\n"
    "메리 포핀스와 함께라서 매일이 놀라웠어요.\n"
    "웃음은 마법이에요! ✨\n"
    "<strong>아이들은 기쁨을 느꼈어요!</strong>",
    # A1
    "The children laughed a lot.\n"
    "They floated to the ceiling.\n"
    "They had tea up there.\n"
    "The children felt joy.",
    # A2
    "Mary Poppins took the children to visit her uncle one day.\n"
    "When they started laughing, their bodies floated up to the ceiling.\n"
    "They had a wonderful tea party way up in the air.\n"
    "The children felt joy and happiness they had never known before.\n"
    "The more they laughed, the higher they floated up.\n"
    "Mary Poppins had shown them that laughter is the best magic."
)

STORIES["week15b"] = (
    "또 다른 모험이에요! 🌟\n"
    "메리 포핀스가 별을 사러 간다고 했어요.\n"
    "\"별을 산다고요?\" 아이들이 놀랐어요. ⭐\n"
    "밤하늘에서 내려온 별이 반짝이고 있었어요.\n"
    "메리 포핀스는 별을 손에 올려놨어요.\n"
    "\"보렴, 이것이 마법이란다.\"\n"
    "아이들의 눈이 반짝반짝 빛났어요. 🤩\n"
    "메리 포핀스가 보여주는 마법 때문에 기쁨을 느꼈어요.\n"
    "평범한 것 속에 마법이 숨어 있었어요.\n"
    "메리 포핀스는 그것을 보여줬어요! 💫\n"
    "<strong>메리 포핀스가 보여주는 마법 때문에 아이들은 기쁨을 느꼈어요!</strong>",
    # A1
    "Mary Poppins bought stars.\n"
    "The children were amazed.\n"
    "They saw magic everywhere.\n"
    "The children felt joy because Mary showed them magic.",
    # A2
    "Mary Poppins said she was going shopping for stars in the sky.\n"
    "The children could not believe what they heard at all.\n"
    "She reached up and caught a twinkling star in her hand.\n"
    "The children felt joy because Mary showed them magic was real.\n"
    "She taught them to look for wonder in everyday things.\n"
    "The children realized that magic was all around them."
)

STORIES["week15c"] = (
    "비 오는 날이었어요. ☔\n"
    "아이들은 집에서 심심해했어요.\n"
    "메리 포핀스가 거울을 가리켰어요. 🪞\n"
    "\"거울 속을 보렴.\"\n"
    "아이들이 거울을 봤더니... 동물 나라가 보였어요!\n"
    "강아지가 노래하고, 고양이가 춤을 췄어요! 🐱🎵\n"
    "\"와! 평범한 거울인 줄 알았는데!\"\n"
    "메리 포핀스가 평범한 것 속의 마법을 보여줬어요.\n"
    "아이들은 일상의 마법에서 기쁨을 느꼈어요.\n"
    "세상은 보는 눈에 따라 달라져요! 🌈\n"
    "<strong>메리 포핀스가 평범한 것 속의 마법을 보여줘서 기쁨을 느꼈어요!</strong>",
    # A1
    "It was a rainy day.\n"
    "Mary Poppins showed them a mirror.\n"
    "They saw a magical world inside.\n"
    "The children felt joy because Mary showed them magic in ordinary things.",
    # A2
    "It was a boring rainy day and the children had nothing to do.\n"
    "Mary Poppins pointed to an ordinary mirror on the wall.\n"
    "Inside the mirror, animals were singing and dancing together.\n"
    "The children felt joy because Mary showed them magic in ordinary things.\n"
    "They learned that wonder can be found in the most common places.\n"
    "From that day, they looked at everyday objects with new eyes."
)

# ═══════════════════════════════════════════════
# W16: Leaves, magic stays
# ═══════════════════════════════════════════════
STORIES["week16a"] = (
    "바람이 바뀌었어요. 🌬️\n"
    "메리 포핀스가 가방을 싸기 시작했어요.\n"
    "\"메리 포핀스, 어디 가요?\" 제인이 물었어요.\n"
    "\"바람이 바뀌면 가야 해.\"\n"
    "아이들은 눈물이 났어요. 😢\n"
    "\"가지 마세요!\"\n"
    "하지만 메리 포핀스는 웃으며 말했어요.\n"
    "\"할 일을 다 했으니까 가는 거야.\"\n"
    "메리 포핀스는 할 일을 다 했기 때문에 떠났어요.\n"
    "아이들의 마음은 아팠지만 이해했어요. 💔\n"
    "<strong>메리 포핀스는 할 일을 다 했기 때문에 떠났어요!</strong>",
    # A1
    "The wind changed direction.\n"
    "Mary Poppins packed her bag.\n"
    "The children cried.\n"
    "She left because her work was done.",
    # A2
    "One morning, the wind changed direction and blew from the east.\n"
    "Mary Poppins began to pack her carpetbag without a word.\n"
    "The children begged her to stay, with tears in their eyes.\n"
    "She left because her work was done and the children were ready.\n"
    "She smiled and opened her umbrella to catch the wind.\n"
    "The children watched her float up into the cloudy sky."
)

STORIES["week16b"] = (
    "메리 포핀스가 하늘로 날아갔어요. ☂️\n"
    "우산을 펼치고 바람을 타고 올라갔어요.\n"
    "아이들은 창문에서 바라봤어요.\n"
    "\"안녕, 메리 포핀스...\" 😢\n"
    "하지만 아이들은 슬프지만은 않았어요.\n"
    "방 안을 보니 장난감이 반짝이고 있었어요. ✨\n"
    "거울에는 아직 마법 세계가 보였어요.\n"
    "메리 포핀스는 떠났지만 마법은 남아 있었어요.\n"
    "아이들은 미소를 지었어요.\n"
    "메리 포핀스가 남긴 선물이에요! 🎁\n"
    "<strong>메리 포핀스는 떠났지만 마법은 남아 있었어요!</strong>",
    # A1
    "Mary Poppins flew away.\n"
    "The children were sad.\n"
    "But the magic was still there.\n"
    "She left, but the magic stayed.",
    # A2
    "Mary Poppins floated up and up into the grey sky above.\n"
    "The children pressed their faces against the cold window glass.\n"
    "But when they turned around, something magical was still there.\n"
    "She left, but the magic stayed in every corner of the house.\n"
    "The toys still sparkled and the mirror still showed wonders.\n"
    "Mary Poppins had given them a gift that would last forever."
)

STORIES["week16c"] = (
    "시간이 지났어요. 📅\n"
    "아이들은 메리 포핀스를 많이 그리워했어요.\n"
    "하지만 이상한 일이 일어났어요!\n"
    "웃으면 여전히 몸이 가벼워졌어요. 😊\n"
    "비 오는 날에도 마법을 찾을 수 있었어요.\n"
    "평범한 것이 특별하게 보였어요. ✨\n"
    "메리 포핀스가 가르쳐준 거예요.\n"
    "마법은 항상 우리 안에 있었어요.\n"
    "메리 포핀스는 떠났지만 마법은 영원히 남았어요.\n"
    "메리 포핀스, 고마워요! 💖\n"
    "<strong>메리 포핀스는 떠났지만 마법은 영원히 남았어요!</strong>",
    # A1
    "The children missed Mary Poppins.\n"
    "But they could still find magic.\n"
    "The magic lived inside them now.\n"
    "She left because her work was done but the magic stayed forever.",
    # A2
    "Days passed but the children never forgot Mary Poppins.\n"
    "When they laughed hard, they still felt lighter than air.\n"
    "Rainy days felt magical and ordinary things seemed wonderful.\n"
    "She left because her work was done but the magic stayed forever.\n"
    "Mary Poppins had taught them to see wonder in the world.\n"
    "The magic was never in her umbrella but in their own hearts."
)

# ═══════════════════════════════════════════════
# W17: Charlotte's Web — Wilbur saved
# ═══════════════════════════════════════════════
STORIES["week17a"] = (
    "새 이야기를 시작해요! 🐷\n"
    "샬롯의 거미줄이라는 이야기예요.\n"
    "농장에 작은 아기 돼지가 태어났어요.\n"
    "이 돼지는 다른 돼지보다 작았어요.\n"
    "농부 아저씨가 이 돼지를 없애려 했어요. 😱\n"
    "그때 펀이라는 소녀가 달려왔어요!\n"
    "\"아빠! 이 돼지를 살려주세요!\" 😢\n"
    "펀은 작은 돼지를 안아줬어요.\n"
    "이름을 윌버라고 지었어요.\n"
    "윌버는 구해졌어요! 💕\n"
    "<strong>윌버는 구해졌어요!</strong>",
    # A1
    "A small pig was born.\n"
    "The farmer wanted to get rid of it.\n"
    "A girl named Fern saved it.\n"
    "Wilbur was saved.",
    # A2
    "A tiny runt pig was born on a farm one cold morning.\n"
    "The farmer did not think the small pig would survive at all.\n"
    "He took an axe and went to the barn to get rid of it.\n"
    "Wilbur was saved because a kind girl named Fern begged her father.\n"
    "She promised to take care of the little pig herself.\n"
    "Fern named him Wilbur and loved him with all her heart."
)

STORIES["week17b"] = (
    "윌버는 펀의 사랑을 받으며 자랐어요. 🐷💕\n"
    "매일 우유를 마시고 점점 커졌어요.\n"
    "하지만 윌버가 너무 커져서 농장으로 보내졌어요.\n"
    "농장에서 윌버는 외로웠어요. 😔\n"
    "다른 동물들은 윌버를 무시했어요.\n"
    "그때 헛간 천장에서 작은 목소리가 들렸어요.\n"
    "\"안녕, 윌버. 나는 샬롯이야.\" 🕷️\n"
    "거미 샬롯이 윌버의 친구가 되어줬어요!\n"
    "샬롯이 윌버를 믿었기 때문에 구해질 수 있었어요.\n"
    "진짜 친구를 만났어요! 🤝\n"
    "<strong>샬롯이 윌버를 믿었기 때문에 구해질 수 있었어요!</strong>",
    # A1
    "Wilbur went to a farm.\n"
    "He was lonely there.\n"
    "A spider named Charlotte became his friend.\n"
    "Wilbur was saved because Charlotte believed in him.",
    # A2
    "Wilbur grew too big to stay with Fern at her house.\n"
    "He was sent to a nearby farm where he felt very lonely.\n"
    "None of the other farm animals wanted to be his friend.\n"
    "Wilbur was saved because Charlotte believed in him completely.\n"
    "Charlotte was a grey spider who lived in the barn doorway.\n"
    "She promised Wilbur she would be his true and loyal friend."
)

STORIES["week17c"] = (
    "윌버는 무서운 소식을 들었어요. 😰\n"
    "\"너는 크리스마스에 소시지가 될 거야!\"\n"
    "양이 윌버에게 알려줬어요.\n"
    "윌버는 너무 무서워서 울었어요. 😢\n"
    "\"살려줘! 나 소시지가 되기 싫어!\"\n"
    "샬롯이 윌버를 위해 나섰어요.\n"
    "\"걱정 마, 윌버. 내가 방법을 찾을게.\"\n"
    "샬롯은 작은 생명 하나가 싸울 가치가 있다고 믿었어요.\n"
    "윌버는 샬롯 덕분에 구해질 수 있었어요.\n"
    "진정한 우정이에요! 💪\n"
    "<strong>작은 생명 하나가 싸울 가치가 있다고 샬롯이 믿었기에 윌버는 구해졌어요!</strong>",
    # A1
    "Wilbur learned he would become food.\n"
    "He cried and was very scared.\n"
    "Charlotte promised to save him.\n"
    "Wilbur was saved because Charlotte believed one small life was worth fighting for.",
    # A2
    "The old sheep told Wilbur terrible news about Christmas.\n"
    "Wilbur was going to be turned into sausage and ham.\n"
    "He cried and screamed because he was so terrified.\n"
    "Wilbur was saved because Charlotte believed one small life was worth fighting for.\n"
    "Charlotte stayed up all night thinking of a plan to help.\n"
    "She would do anything to protect her dear friend Wilbur."
)

# ═══════════════════════════════════════════════
# W18: Charlotte works quietly
# ═══════════════════════════════════════════════
STORIES["week18a"] = (
    "샬롯은 밤새 일했어요. 🕷️\n"
    "달빛 아래에서 거미줄을 쳤어요. 🌙\n"
    "보통 거미줄이 아니었어요.\n"
    "거미줄에 글자가 있었어요!\n"
    "\"대단한 돼지\" 라고 썼어요.\n"
    "아침에 농부가 이것을 봤어요.\n"
    "\"세상에! 기적이야!\" 😲\n"
    "사람들이 몰려왔어요.\n"
    "모두 윌버를 특별한 돼지라고 생각했어요.\n"
    "샬롯은 조용히 일했어요. ✨\n"
    "<strong>샬롯은 조용히 일했어요!</strong>",
    # A1
    "Charlotte made a web at night.\n"
    "She wrote words in it.\n"
    "People thought Wilbur was special.\n"
    "Charlotte worked quietly.",
    # A2
    "While everyone slept, Charlotte began spinning her web.\n"
    "She carefully wove the words Some Pig into the silk.\n"
    "When the farmer saw it the next morning, he was amazed.\n"
    "Charlotte worked quietly through the night to save Wilbur.\n"
    "People came from everywhere to see the miraculous pig.\n"
    "Nobody knew that a tiny spider had done all the work."
)

STORIES["week18b"] = (
    "사람들이 매일 농장에 왔어요! 👨‍👩‍👧‍👦\n"
    "\"대단한 돼지가 있대!\" \"기적이야!\"\n"
    "샬롯은 또 거미줄에 새로운 글자를 썼어요.\n"
    "\"멋진\" \"빛나는\" \"겸손한\" 🕸️\n"
    "매번 새로운 단어가 나타났어요.\n"
    "샬롯은 윌버를 사랑하기 때문에 조용히 일했어요.\n"
    "아무도 샬롯을 몰랐어요.\n"
    "거미줄을 치는 건 힘든 일이었어요.\n"
    "하지만 친구를 위해서 열심히 했어요.\n"
    "조용한 사랑은 가장 큰 사랑이에요. 💕\n"
    "<strong>샬롯은 윌버를 사랑하기 때문에 조용히 일했어요!</strong>",
    # A1
    "Charlotte wrote new words each time.\n"
    "More people came to the farm.\n"
    "No one knew about Charlotte.\n"
    "Charlotte worked quietly because she loved Wilbur.",
    # A2
    "Charlotte kept writing new words in her web every few days.\n"
    "She wrote Terrific, then Radiant, then Humble in her silk.\n"
    "Charlotte worked quietly because she loved Wilbur with all her heart.\n"
    "More and more people visited the farm to see the famous pig.\n"
    "Spinning the web was exhausting work for the little spider.\n"
    "But she never complained because Wilbur was worth every effort."
)

STORIES["week18c"] = (
    "농장 축제 날이 다가왔어요! 🎪\n"
    "윌버는 축제에 나가게 되었어요.\n"
    "샬롯도 함께 갔어요.\n"
    "하지만 샬롯은 많이 지쳐 있었어요. 😔\n"
    "거미줄을 너무 많이 쳐서 힘이 없었어요.\n"
    "그래도 마지막 힘을 내서 거미줄을 쳤어요.\n"
    "\"겸손한\" 이라고 쓴 거미줄이었어요.\n"
    "샬롯은 윌버를 그가 알지 못할 만큼 사랑했어요.\n"
    "조용히 모든 것을 바쳤어요.\n"
    "이것이 진정한 사랑이에요. 💖\n"
    "<strong>샬롯은 윌버가 알지 못할 만큼 그를 사랑하며 조용히 일했어요!</strong>",
    # A1
    "The fair was coming soon.\n"
    "Charlotte was getting tired.\n"
    "She still wrote one more word.\n"
    "Charlotte worked quietly because she loved Wilbur more than he ever knew.",
    # A2
    "The county fair was finally here and Wilbur was entered.\n"
    "Charlotte went with him even though she was very weak.\n"
    "She used her last strength to spin one more beautiful web.\n"
    "Charlotte worked quietly because she loved Wilbur more than he ever knew.\n"
    "She never asked for thanks or praise from anyone at all.\n"
    "Her silent love was the greatest gift she could ever give."
)

# ═══════════════════════════════════════════════
# W19: Charlotte gone
# ═══════════════════════════════════════════════
STORIES["week19a"] = (
    "축제가 끝났어요. 🎪\n"
    "윌버는 특별상을 받았어요! 🏆\n"
    "이제 윌버는 안전해요.\n"
    "더 이상 소시지가 되지 않아요.\n"
    "하지만 슬픈 일이 일어났어요. 😢\n"
    "샬롯이 아주 약해졌어요.\n"
    "\"윌버야, 나는 이제 갈 시간이야.\"\n"
    "윌버는 눈물이 났어요.\n"
    "\"안 돼! 샬롯! 가지 마!\"\n"
    "윌버는 샬롯이 떠나서 울었어요. 😭\n"
    "<strong>윌버는 샬롯이 떠나서 울었어요!</strong>",
    # A1
    "Wilbur won a prize.\n"
    "He was safe now.\n"
    "But Charlotte was very weak.\n"
    "Wilbur cried because Charlotte was gone.",
    # A2
    "Wilbur won a special prize at the fair and was finally safe.\n"
    "The farmer would never turn him into food after this honor.\n"
    "But Charlotte had used all her strength to save her friend.\n"
    "Wilbur cried because Charlotte was gone and he missed her terribly.\n"
    "She had given everything she had for one small pig.\n"
    "Wilbur had never felt such sadness in his whole life."
)

STORIES["week19b"] = (
    "샬롯이 마지막으로 윌버에게 말했어요. 🕷️\n"
    "\"윌버야, 네가 내 가장 좋은 친구였어.\"\n"
    "\"고마워, 샬롯...\" 윌버가 울며 말했어요. 😭\n"
    "샬롯은 조용히 눈을 감았어요.\n"
    "하지만 샬롯은 선물을 남겼어요.\n"
    "작은 알주머니 안에 아기 거미들이 있었어요! 🥚\n"
    "윌버는 그 알주머니를 소중히 가져왔어요.\n"
    "샬롯은 떠났지만 선물은 남았어요.\n"
    "윌버는 울었지만 샬롯의 선물이 남아 있었어요.\n"
    "사랑은 사라지지 않아요. 💕\n"
    "<strong>윌버는 울었지만 샬롯의 선물이 남아 있었어요!</strong>",
    # A1
    "Charlotte said goodbye.\n"
    "She left a bag of eggs.\n"
    "Wilbur took the eggs home.\n"
    "Wilbur cried, but Charlotte's gift stayed.",
    # A2
    "Charlotte whispered her last goodbye to her dearest friend.\n"
    "She told Wilbur that he was the best friend she ever had.\n"
    "Before she closed her eyes, she showed him her egg sac.\n"
    "Wilbur cried, but Charlotte's gift stayed with him forever.\n"
    "He carefully carried the precious eggs back to the barn.\n"
    "Charlotte's love would live on through her baby spiders."
)

STORIES["week19c"] = (
    "봄이 왔어요. 🌸\n"
    "샬롯의 알에서 아기 거미들이 태어났어요!\n"
    "작고 예쁜 거미 수백 마리! 🕷️\n"
    "윌버는 너무 기뻐서 울었어요. 😊\n"
    "\"안녕, 꼬마들아! 나는 윌버야.\"\n"
    "대부분의 아기 거미는 바람을 타고 떠났어요.\n"
    "하지만 세 마리가 남았어요.\n"
    "\"우리가 여기 있을게요, 윌버 아저씨!\"\n"
    "윌버는 샬롯이 떠났지만 그녀의 말과 선물이 남았다는 걸 알았어요.\n"
    "사랑은 영원해요. 💖\n"
    "<strong>샬롯은 떠났지만 그녀의 말과 선물은 윌버와 함께 남았어요!</strong>",
    # A1
    "Baby spiders were born.\n"
    "Most of them flew away.\n"
    "Three stayed with Wilbur.\n"
    "Wilbur cried because Charlotte was gone but her words and gift stayed with him.",
    # A2
    "Spring came and hundreds of tiny baby spiders hatched from the eggs.\n"
    "Wilbur was overjoyed to see them crawling out into the sunlight.\n"
    "Most baby spiders flew away on the wind to start new lives.\n"
    "Wilbur cried because Charlotte was gone but her words and gift stayed with him.\n"
    "Three little spiders decided to stay and live in the barn.\n"
    "Charlotte's love continued through her children forever and ever."
)

# ═══════════════════════════════════════════════
# W20: True friendship
# ═══════════════════════════════════════════════
STORIES["week20a"] = (
    "윌버는 샬롯을 생각했어요. 🐷💭\n"
    "샬롯은 아무것도 바라지 않았어요.\n"
    "그냥 윌버를 도와줬어요.\n"
    "밤새 거미줄을 치고, 힘이 다할 때까지 일했어요.\n"
    "\"왜 나를 도와줬어?\" 윌버가 물었었어요.\n"
    "\"넌 내 친구니까.\" 샬롯이 대답했었어요. 💕\n"
    "진정한 우정은 주는 것이에요.\n"
    "받는 것을 기대하지 않는 거예요.\n"
    "샬롯이 바로 그런 친구였어요.\n"
    "이것이 진정한 우정이에요! 🌟\n"
    "<strong>진정한 우정은 주는 것이에요!</strong>",
    # A1
    "Charlotte gave everything.\n"
    "She never asked for anything.\n"
    "She helped because Wilbur was her friend.\n"
    "True friendship means giving.",
    # A2
    "Wilbur often thought about Charlotte and everything she did.\n"
    "She had worked all night spinning webs without any complaint.\n"
    "She never once asked Wilbur to do anything in return for her.\n"
    "True friendship means giving your whole heart to someone else.\n"
    "Charlotte showed that real friends sacrifice without being asked.\n"
    "Wilbur learned the most important lesson about love and giving."
)

STORIES["week20b"] = (
    "윌버는 샬롯의 아이들을 돌봐줬어요. 🕷️\n"
    "조이, 넬리, 아라네아라는 이름이에요.\n"
    "윌버는 매일 아이들에게 이야기를 해줬어요. 📖\n"
    "\"너희 엄마는 정말 대단한 분이셨어.\"\n"
    "아이들이 물었어요.\n"
    "\"엄마가 왜 그렇게 열심히 했어요?\"\n"
    "\"사랑은 아무것도 요구하지 않는 거란다.\"\n"
    "진정한 우정은 요구하지 않고 주는 것이에요.\n"
    "윌버는 샬롯이 가르쳐준 대로 살았어요.\n"
    "사랑을 나누며 살았어요. 💕\n"
    "<strong>진정한 우정은 요구하지 않고 주는 것이에요!</strong>",
    # A1
    "Wilbur took care of Charlotte's babies.\n"
    "He told them about their mother.\n"
    "Love asks for nothing.\n"
    "True friendship means giving without asking.",
    # A2
    "Wilbur watched over Charlotte's three children with great care.\n"
    "He told them stories about their brave and loving mother.\n"
    "They asked why their mother worked so hard for just one pig.\n"
    "True friendship means giving without asking for anything back.\n"
    "Charlotte had shown this truth with her very own life.\n"
    "Wilbur passed on her lesson of selfless love every single day."
)

STORIES["week20c"] = (
    "이야기가 끝나가요. 📖\n"
    "윌버는 행복하게 농장에서 살았어요.\n"
    "샬롯의 아이들, 손자들이 항상 함께였어요. 🕷️\n"
    "매년 봄마다 새로운 거미가 태어났어요.\n"
    "윌버는 늙었지만 행복했어요.\n"
    "샬롯을 절대 잊지 않았어요.\n"
    "\"샬롯, 고마워. 넌 최고의 친구야.\" 💕\n"
    "샬롯은 자기 삶으로 우정이 무엇인지 보여줬어요.\n"
    "진정한 우정은 요구하지 않고 주는 것이에요.\n"
    "이 이야기를 영원히 기억해요! 🌈\n"
    "<strong>진정한 우정은 요구하지 않고 주는 것, 샬롯이 자기 삶으로 보여줬어요!</strong>",
    # A1
    "Wilbur lived a happy life.\n"
    "He never forgot Charlotte.\n"
    "Charlotte showed what true friendship is.\n"
    "True friendship means giving without asking Charlotte showed this with her life.",
    # A2
    "Wilbur grew old on the farm, surrounded by Charlotte's family.\n"
    "Every spring, new baby spiders were born and kept him company.\n"
    "He told each new generation the story of their amazing ancestor.\n"
    "True friendship means giving without asking, and Charlotte showed this with her life.\n"
    "She never wanted praise or thanks for her silent sacrifice.\n"
    "Her love lived on in every web spun in the old barn doorway."
)

# ═══════════════════════════════════════════════
# W21: Secret Garden — Mary finds garden
# ═══════════════════════════════════════════════
STORIES["week21a"] = (
    "새 이야기를 시작해요! 🏡\n"
    "비밀의 정원이라는 이야기예요.\n"
    "메리 레녹스는 인도에서 영국으로 왔어요.\n"
    "부모님이 돌아가셔서 삼촌 집에 살게 되었어요.\n"
    "삼촌의 저택은 크고 어두웠어요. 🏰\n"
    "메리는 심심하고 외로웠어요.\n"
    "어느 날 정원을 돌아다니다가...\n"
    "담벼락 뒤에 숨겨진 문을 발견했어요! 🚪\n"
    "열쇠로 문을 열자 아름다운 정원이 나타났어요!\n"
    "메리는 정원을 발견했어요! 🌿\n"
    "<strong>메리는 정원을 발견했어요!</strong>",
    # A1
    "Mary came to live in a big house.\n"
    "She was lonely and bored.\n"
    "She found a hidden door.\n"
    "Mary found a garden.",
    # A2
    "Mary Lennox came from India to live in her uncle's big house.\n"
    "The house was dark and cold, and she felt very lonely.\n"
    "One day she wandered around the grounds and found a hidden wall.\n"
    "Mary found a garden behind a locked door in the old wall.\n"
    "She turned the rusty key and pushed the door open slowly.\n"
    "Inside was the most beautiful garden she had ever seen."
)

STORIES["week21b"] = (
    "메리가 문을 열었어요! 🚪\n"
    "정원 안은 마치 마법의 세계 같았어요.\n"
    "하지만 오랫동안 아무도 돌보지 않았어요.\n"
    "잡초가 많고 꽃은 시들어 있었어요. 🥀\n"
    "그래도 메리의 눈은 반짝였어요.\n"
    "\"이 정원을 살릴 수 있을 거야!\"\n"
    "메리는 비밀스럽고 잠긴 정원을 발견했어요.\n"
    "이 정원은 왜 숨겨져 있었을까요?\n"
    "메리는 비밀을 알고 싶었어요.\n"
    "신비로운 모험이 시작되었어요! ✨\n"
    "<strong>메리는 비밀스럽고 잠긴 정원을 발견했어요!</strong>",
    # A1
    "Mary opened the hidden door.\n"
    "The garden was wild and messy.\n"
    "But Mary was excited.\n"
    "Mary found a secret and locked garden.",
    # A2
    "Mary pushed open the old door and stepped inside carefully.\n"
    "The garden had been locked and forgotten for ten long years.\n"
    "Weeds grew everywhere and the roses had stopped blooming.\n"
    "Mary found a secret and locked garden that needed her help.\n"
    "She wondered why someone had locked this beautiful place away.\n"
    "Mary decided right then that she would bring it back to life."
)

STORIES["week21c"] = (
    "메리는 정원의 비밀을 알게 되었어요. 🤫\n"
    "삼촌의 아내가 이 정원을 사랑했어요.\n"
    "하지만 이모가 돌아가신 후 삼촌이 정원을 잠갔어요. 🔒\n"
    "아무도 들어갈 수 없게 열쇠를 숨겼어요.\n"
    "메리는 그 열쇠를 찾은 거예요!\n"
    "오래된 벽 뒤에 숨겨진 비밀의 정원이었어요.\n"
    "메리는 이것을 비밀로 간직하기로 했어요.\n"
    "\"이 정원은 나만의 비밀이야.\"\n"
    "메리는 정원을 되살리기로 했어요.\n"
    "새로운 시작이에요! 🌱\n"
    "<strong>메리는 오래된 벽 뒤에 숨겨진 비밀의 정원을 발견했어요!</strong>",
    # A1
    "The garden was locked for ten years.\n"
    "Mary found the hidden key.\n"
    "She kept it a secret.\n"
    "Mary found a hidden secret garden behind the old wall.",
    # A2
    "Mary learned the sad story behind the locked garden door.\n"
    "Her uncle's wife had loved this garden more than anything.\n"
    "After she died, the uncle locked the garden and hid the key.\n"
    "Mary found a hidden secret garden behind the old wall years later.\n"
    "She decided to keep it as her own special secret.\n"
    "She would bring the garden back to life all by herself."
)

# ═══════════════════════════════════════════════
# W22: Cares for it
# ═══════════════════════════════════════════════
STORIES["week22a"] = (
    "메리는 매일 비밀 정원에 갔어요. 🌿\n"
    "잡초를 뽑고 흙을 파줬어요.\n"
    "물도 주고 햇빛이 잘 들게 해줬어요. ☀️\n"
    "메리의 손은 흙으로 더러웠어요.\n"
    "하지만 행복했어요!\n"
    "디콘이라는 소년도 도와줬어요. 👦\n"
    "디콘은 동물과 식물을 잘 알았어요.\n"
    "함께 정원을 돌봤어요.\n"
    "메리는 정원을 돌봤어요.\n"
    "정원이 조금씩 살아나기 시작했어요! 🌱\n"
    "<strong>메리는 정원을 돌봤어요!</strong>",
    # A1
    "Mary went to the garden every day.\n"
    "She pulled weeds and watered plants.\n"
    "A boy named Dickon helped her.\n"
    "She cared for it.",
    # A2
    "Every morning, Mary snuck away to work in the secret garden.\n"
    "She pulled out weeds and gave the dry soil fresh water.\n"
    "A kind boy named Dickon taught her about plants and flowers.\n"
    "She cared for it with her hands and her whole heart.\n"
    "Together they dug in the dirt and planted new seeds.\n"
    "Slowly, green shoots began to push up through the dark earth."
)

STORIES["week22b"] = (
    "정원이 변하고 있었어요! 🌸\n"
    "마른 가지에서 새싹이 나왔어요.\n"
    "꽃봉오리가 하나 둘 생겼어요.\n"
    "메리는 매일 정원을 돌봤어요. 🌹\n"
    "\"좀 더 물을 줘야겠어.\"\n"
    "\"이 잡초를 뽑아야 해.\"\n"
    "메리는 정원에 오는 게 매일 기다려졌어요.\n"
    "정원을 돌보면서 메리도 변하고 있었어요. 😊\n"
    "예전에는 심술궂었는데 이제 웃는 일이 많아졌어요.\n"
    "정원이 메리를 치유하고 있었어요! 💚\n"
    "<strong>메리는 매일 정원을 돌봤어요!</strong>",
    # A1
    "The garden was coming alive.\n"
    "New buds appeared on branches.\n"
    "Mary was changing too.\n"
    "She cared for the garden every day.",
    # A2
    "The secret garden was slowly waking up from its long sleep.\n"
    "New green buds appeared on the old brown branches.\n"
    "She cared for the garden every day with love and patience.\n"
    "Mary was changing too, becoming kinder and happier each day.\n"
    "She had been a grumpy, lonely girl when she first arrived.\n"
    "Now she smiled and laughed while working in the warm sunshine."
)

STORIES["week22c"] = (
    "봄이 왔어요! 🌷\n"
    "정원에 꽃이 피기 시작했어요!\n"
    "빨간 장미, 노란 수선화, 보라색 크로커스! 🌺\n"
    "메리는 너무 행복했어요.\n"
    "\"내가 이렇게 만들었어!\" 😊\n"
    "디콘과 함께 더 많은 꽃을 심었어요.\n"
    "정원은 매일 더 아름다워졌어요.\n"
    "메리가 정원을 돌본 이유는 기쁨을 주기 때문이었어요.\n"
    "정원을 돌보는 것은 사랑을 주는 것이에요.\n"
    "사랑을 주면 사랑이 돌아와요! 💕\n"
    "<strong>기쁨을 주기 때문에 매일 정원을 돌봤어요!</strong>",
    # A1
    "Spring came to the garden.\n"
    "Flowers bloomed everywhere.\n"
    "Mary was so happy.\n"
    "She cared for it every day because it gave her joy.",
    # A2
    "Spring arrived and the garden burst into beautiful colors.\n"
    "Red roses, yellow daffodils, and purple crocuses bloomed together.\n"
    "She cared for it every day because it gave her joy and purpose.\n"
    "Mary and Dickon planted even more flowers and trimmed the hedges.\n"
    "The garden grew more beautiful with each passing sunny day.\n"
    "Taking care of something with love always brings happiness back."
)

# ═══════════════════════════════════════════════
# W23: Colin afraid
# ═══════════════════════════════════════════════
STORIES["week23a"] = (
    "어느 밤, 메리는 이상한 소리를 들었어요. 👂\n"
    "누군가 울고 있었어요!\n"
    "메리가 소리를 따라갔어요.\n"
    "어두운 방에 소년이 누워 있었어요. 🛏️\n"
    "\"너 누구야?\" 메리가 물었어요.\n"
    "\"나는 콜린이야. 삼촌의 아들이야.\"\n"
    "콜린은 항상 침대에만 있었어요.\n"
    "\"나는 아파서 밖에 나갈 수 없어.\" 😢\n"
    "콜린은 무서워했어요.\n"
    "밖이 무서웠어요.\n"
    "<strong>콜린은 무서워했어요!</strong>",
    # A1
    "Mary heard crying at night.\n"
    "She found a boy named Colin.\n"
    "He stayed in bed all day.\n"
    "Colin was afraid.",
    # A2
    "One night Mary followed the sound of someone crying loudly.\n"
    "She found a pale boy lying alone in a dark, cold room.\n"
    "His name was Colin and he was her uncle's only son.\n"
    "Colin was afraid of going outside and believed he was dying.\n"
    "He had stayed in his bed for years without seeing the sun.\n"
    "Everyone in the house treated him like he was made of glass."
)

STORIES["week23b"] = (
    "콜린은 매일 울고 화를 냈어요. 😤\n"
    "\"나는 죽을 거야! 아무도 나를 못 도와!\"\n"
    "하인들이 무서워서 말을 못 했어요.\n"
    "하지만 메리는 달랐어요!\n"
    "\"너는 약하지 않아! 그냥 겁이 많은 거야!\" 😠\n"
    "콜린이 깜짝 놀랐어요.\n"
    "아무도 그렇게 말한 적이 없었거든요.\n"
    "콜린은 자기가 너무 약해서 살 수 없다고 믿었어요.\n"
    "하지만 메리는 그것이 사실이 아니라는 걸 알았어요.\n"
    "콜린에게는 용기가 필요했어요! 💪\n"
    "<strong>콜린은 자기가 너무 약해서 살 수 없다고 믿었어요!</strong>",
    # A1
    "Colin cried and got angry.\n"
    "He thought he would die.\n"
    "Mary told him he was not weak.\n"
    "Colin believed he was too weak to live.",
    # A2
    "Colin spent his days crying and shouting at everyone around him.\n"
    "He truly believed that he was too sick to ever get better.\n"
    "Colin believed he was too weak to live a normal life.\n"
    "Mary refused to feel sorry for him like everyone else did.\n"
    "She told him he was just scared, not actually sick at all.\n"
    "For the first time, someone challenged Colin to be brave."
)

STORIES["week23c"] = (
    "메리가 콜린에게 비밀을 알려줬어요. 🤫\n"
    "\"콜린, 내가 비밀 정원을 찾았어!\"\n"
    "콜린의 눈이 커졌어요.\n"
    "\"정원? 엄마의 정원?\"\n"
    "\"응! 같이 가자!\" 🌿\n"
    "콜린은 무서워했어요.\n"
    "\"나는 밖에 나가면 안 돼...\"\n"
    "하지만 메리가 말했어요.\n"
    "\"정원이 널 변하게 해줄 거야!\"\n"
    "콜린은 아프다고 생각했지만 정원이 그를 변화시켰어요.\n"
    "<strong>콜린은 아프다고 생각했지만 정원이 그를 변화시켰어요!</strong>",
    # A1
    "Mary told Colin about the garden.\n"
    "Colin was scared to go outside.\n"
    "But Mary encouraged him.\n"
    "Colin thought he was sick but the garden changed him.",
    # A2
    "Mary whispered to Colin about the beautiful secret garden.\n"
    "Colin could not believe his mother's garden still existed.\n"
    "He was terrified of going outside for the very first time.\n"
    "Colin thought he was sick but the garden changed him completely.\n"
    "Mary and Dickon pushed his wheelchair through the hidden door.\n"
    "When Colin saw the garden, tears of wonder filled his eyes."
)

# ═══════════════════════════════════════════════
# W24: Garden heals
# ═══════════════════════════════════════════════
STORIES["week24a"] = (
    "콜린이 드디어 정원에 왔어요! 🌿\n"
    "햇빛이 콜린의 얼굴에 닿았어요. ☀️\n"
    "\"이게... 햇빛이야?\" 콜린이 놀랐어요.\n"
    "오랫동안 방에만 있었던 콜린에게 모든 게 새로웠어요.\n"
    "꽃 향기, 바람 소리, 새 노래... 🐦\n"
    "콜린의 얼굴에 미소가 번졌어요!\n"
    "\"여기가 엄마의 정원이야...\"\n"
    "콜린은 감동받았어요.\n"
    "정원이 그들을 치유했어요.\n"
    "자연의 힘은 놀라워요! 💚\n"
    "<strong>정원이 그들을 치유했어요!</strong>",
    # A1
    "Colin came to the garden.\n"
    "He felt the warm sun.\n"
    "He smiled for the first time.\n"
    "The garden healed them.",
    # A2
    "Colin was finally pushed into the secret garden in his wheelchair.\n"
    "Warm sunshine touched his pale face for the first time in years.\n"
    "He could smell flowers and hear birds singing all around him.\n"
    "The garden healed them both, giving them strength and hope.\n"
    "Colin felt something he had never felt before in his dark room.\n"
    "He felt alive and knew that he wanted to get better."
)

STORIES["week24b"] = (
    "콜린이 정원에서 변하기 시작했어요! 💪\n"
    "처음에는 휠체어에 앉아 있었어요.\n"
    "하지만 매일 조금씩 일어나려고 했어요.\n"
    "\"내가 서볼게!\" 콜린이 말했어요.\n"
    "메리와 디콘이 도와줬어요. 🤝\n"
    "콜린의 다리가 떨렸지만 일어났어요!\n"
    "\"서있어! 내가 서있어!\" 😊\n"
    "정원이 콜린에게 삶을 돌려줬어요.\n"
    "신선한 공기와 사랑이 기적을 만들었어요.\n"
    "정원의 마법이에요! 🌿\n"
    "<strong>정원이 그들에게 삶을 돌려줬어요!</strong>",
    # A1
    "Colin tried to stand up.\n"
    "Mary and Dickon helped him.\n"
    "He stood for the first time.\n"
    "The garden brought them back to life.",
    # A2
    "Colin came to the garden every day and grew a little stronger.\n"
    "One day he decided he would try to stand up on his own.\n"
    "Mary and Dickon held his arms as he pushed himself up.\n"
    "The garden brought them back to life with fresh air and love.\n"
    "Colin's legs shook but he stood there, smiling with tears of joy.\n"
    "The boy who thought he would die was learning to live again."
)

STORIES["week24c"] = (
    "콜린이 걸을 수 있게 되었어요! 🚶\n"
    "정원에서 뛰어다니기도 했어요!\n"
    "\"봐! 나 뛰고 있어!\" 콜린이 외쳤어요. 😄\n"
    "삼촌이 이것을 보고 울었어요.\n"
    "\"내 아들이... 걷고 있다!\" 😢\n"
    "메리도 많이 변했어요.\n"
    "예전의 심술궂은 소녀는 없어요.\n"
    "신선한 공기와 돌봄이 아이들을 살렸어요.\n"
    "정원이 모든 사람을 치유했어요.\n"
    "사랑과 자연이 기적을 만들었어요! 🌈\n"
    "<strong>신선한 공기와 돌봄이 아이들을 살렸어요!</strong>",
    # A1
    "Colin could walk and run.\n"
    "His father was so happy.\n"
    "Mary also changed.\n"
    "Fresh air and care brought the children back to life.",
    # A2
    "Colin could now walk and even run around the beautiful garden.\n"
    "His father came home and could not believe what he was seeing.\n"
    "The sick boy was now strong, healthy, and laughing with joy.\n"
    "Fresh air and care brought the children back to life completely.\n"
    "Mary had also changed from a grumpy girl into a kind friend.\n"
    "The secret garden had healed everyone with nature and love."
)

# ═══════════════════════════════════════════════
# W25: Christmas Carol — Scrooge mean
# ═══════════════════════════════════════════════
STORIES["week25a"] = (
    "새 이야기예요! ❄️\n"
    "크리스마스 캐럴이라는 이야기를 만나요.\n"
    "에베네저 스크루지라는 노인이 있었어요.\n"
    "스크루지는 런던에서 돈을 빌려주는 일을 했어요. 💰\n"
    "하지만 스크루지는 누구에게도 친절하지 않았어요.\n"
    "직원 밥에게 월급도 적게 줬어요.\n"
    "\"크리스마스? 쓸데없는 날이야!\" 😤\n"
    "스크루지는 크리스마스도 싫어했어요.\n"
    "사람들이 즐겁게 노래하면 화를 냈어요.\n"
    "스크루지는 의지가 세고 심술궂었어요!\n"
    "<strong>스크루지는 심술궂었어요!</strong>",
    # A1
    "Scrooge was an old man.\n"
    "He was not kind to anyone.\n"
    "He hated Christmas.\n"
    "Scrooge was mean.",
    # A2
    "Ebenezer Scrooge was an old man who lived alone in London.\n"
    "He worked counting money but never shared any of it.\n"
    "He paid his worker Bob very little and had no friends at all.\n"
    "Scrooge was mean and did not care about anyone but himself.\n"
    "He hated Christmas and thought celebrations were a waste.\n"
    "Everyone in town was afraid of the cold, grumpy old man."
)

STORIES["week25b"] = (
    "크리스마스 이브였어요. 🎄\n"
    "거리는 즐거운 사람들로 가득했어요.\n"
    "하지만 스크루지는 혼자 집에 있었어요.\n"
    "조카가 크리스마스 저녁에 오라고 했어요.\n"
    "\"됐어! 크리스마스는 쓸데없어!\" 😠\n"
    "가난한 사람을 돕자는 사람도 쫓아냈어요.\n"
    "\"가난한 건 자기 탓이야!\"\n"
    "스크루지는 차갑고 매우 이기적이었어요.\n"
    "아무도 스크루지를 좋아하지 않았어요.\n"
    "하지만 스크루지는 신경 쓰지 않았어요. 💔\n"
    "<strong>스크루지는 차갑고 매우 이기적이었어요!</strong>",
    # A1
    "It was Christmas Eve.\n"
    "Scrooge said no to everyone.\n"
    "He did not care about others.\n"
    "Scrooge was cold and very selfish.",
    # A2
    "It was Christmas Eve and the streets were full of happy people.\n"
    "Scrooge refused his nephew's kind invitation to Christmas dinner.\n"
    "He turned away men who asked for money to help the poor.\n"
    "Scrooge was cold and very selfish, caring only about money.\n"
    "He went home alone to his dark, cold house without any joy.\n"
    "That night, something very strange was about to happen to him."
)

STORIES["week25c"] = (
    "스크루지가 집에 왔어요. 🏠\n"
    "갑자기 문에서 이상한 소리가 났어요!\n"
    "쇠사슬 소리가 들렸어요. ⛓️\n"
    "죽은 친구 제이콥 말리의 유령이 나타났어요! 👻\n"
    "\"스크루지! 너는 변해야 해!\"\n"
    "\"오늘 밤 세 명의 유령이 올 거야!\"\n"
    "스크루지는 무서웠어요. 😱\n"
    "\"유령? 거짓말이지!\"\n"
    "하지만 스크루지는 돈만 좋아하고 다른 건 신경 쓰지 않았어요.\n"
    "유령이 정말 올까요? 👀\n"
    "<strong>스크루지는 돈만 좋아하고 다른 건 아무것도 신경 쓰지 않았어요!</strong>",
    # A1
    "A ghost visited Scrooge.\n"
    "It was his old friend Marley.\n"
    "Three more ghosts would come.\n"
    "Scrooge cared only for money and nothing else.",
    # A2
    "When Scrooge got home, the ghost of Jacob Marley appeared.\n"
    "Marley dragged heavy chains that he made when he was alive.\n"
    "He warned Scrooge that three ghosts would visit him that night.\n"
    "Scrooge cared only for money and nothing else in his life.\n"
    "The ghost said Scrooge must change or face a terrible fate.\n"
    "Scrooge was frightened but still did not believe it was real."
)

# ═══════════════════════════════════════════════
# W26: Three ghosts
# ═══════════════════════════════════════════════
STORIES["week26a"] = (
    "첫 번째 유령이 왔어요! 👻\n"
    "\"나는 과거 크리스마스의 유령이야.\"\n"
    "유령이 스크루지를 과거로 데려갔어요.\n"
    "어린 시절의 스크루지가 보였어요. 👦\n"
    "학교에서 혼자 앉아 있는 소년이었어요.\n"
    "외롭고 슬펐어요. 😢\n"
    "그리고 젊은 시절도 보였어요.\n"
    "좋아하던 여자 친구를 돈 때문에 잃었어요.\n"
    "스크루지의 눈에서 눈물이 흘렀어요.\n"
    "세 명의 유령이 왔어요!\n"
    "<strong>세 명의 유령이 왔어요!</strong>",
    # A1
    "The first ghost came.\n"
    "It showed Scrooge his past.\n"
    "He was lonely as a boy.\n"
    "Three ghosts came.",
    # A2
    "The Ghost of Christmas Past appeared at one o'clock that night.\n"
    "It took Scrooge flying through the air to see his own past.\n"
    "He saw himself as a lonely boy sitting alone at school.\n"
    "Three ghosts came to show Scrooge the truth about his life.\n"
    "He also saw how he lost the woman he loved because of greed.\n"
    "Tears rolled down Scrooge's old wrinkled cheeks for the first time."
)

STORIES["week26b"] = (
    "두 번째 유령이 왔어요! 👻\n"
    "\"나는 현재 크리스마스의 유령이야.\"\n"
    "유령이 밥의 집을 보여줬어요. 🏠\n"
    "밥의 가족은 가난했지만 행복했어요.\n"
    "작은 팀이라는 아들은 다리가 아팠어요.\n"
    "\"하나님 감사합니다!\" 작은 팀이 웃으며 말했어요. 😊\n"
    "스크루지는 마음이 아팠어요.\n"
    "세 번째 유령은 미래를 보여줬어요.\n"
    "스크루지의 무덤이 보였어요. ⚰️\n"
    "세 유령이 진실을 보여줬어요.\n"
    "<strong>세 유령이 진실을 보여줬어요!</strong>",
    # A1
    "The second ghost showed the present.\n"
    "Bob's family was poor but happy.\n"
    "The third ghost showed the future.\n"
    "Three ghosts showed him the truth.",
    # A2
    "The Ghost of Christmas Present showed Scrooge the world today.\n"
    "He saw Bob's poor family sharing a tiny Christmas dinner.\n"
    "Little Tim was sick but still smiled and thanked God for everything.\n"
    "Three ghosts showed him the truth about his cold, lonely life.\n"
    "The Ghost of Christmas Future showed Scrooge his own grave.\n"
    "No one cared that he had died because he had loved no one."
)

STORIES["week26c"] = (
    "미래의 유령이 보여준 것은 끔찍했어요. 😱\n"
    "스크루지가 죽었지만 아무도 슬퍼하지 않았어요.\n"
    "\"저 늙은이 드디어 갔군.\" 사람들이 말했어요.\n"
    "작은 팀도 죽어 있었어요. 😢\n"
    "스크루지가 월급을 더 줬다면...\n"
    "약을 사줄 수 있었을 텐데...\n"
    "스크루지는 무릎을 꿇었어요.\n"
    "\"제발! 바꿀 기회를 주세요!\"\n"
    "세 유령이 스크루지의 과거와 어두운 미래를 보여줬어요.\n"
    "스크루지는 드디어 깨달았어요! 💡\n"
    "<strong>세 유령이 스크루지의 과거와 어두운 미래를 보여줬어요!</strong>",
    # A1
    "Nobody was sad when Scrooge died.\n"
    "Tiny Tim was also dead.\n"
    "Scrooge begged for another chance.\n"
    "Three ghosts showed Scrooge his past and dark future.",
    # A2
    "The Ghost of Christmas Future showed a world without hope.\n"
    "When Scrooge died in the future, nobody shed a single tear.\n"
    "Little Tim had died too because his family had no money.\n"
    "Three ghosts showed Scrooge his past and dark future that night.\n"
    "Scrooge fell to his knees and begged for a chance to change.\n"
    "He finally understood that his greed had destroyed everything."
)

# ═══════════════════════════════════════════════
# W27: Changes completely
# ═══════════════════════════════════════════════
STORIES["week27a"] = (
    "스크루지가 아침에 눈을 떴어요! ☀️\n"
    "\"살아있어! 오늘이 크리스마스야!\"\n"
    "스크루지는 창문을 열었어요.\n"
    "눈이 내리고 있었어요. ❄️\n"
    "\"크리스마스 축하해!\" 스크루지가 소리쳤어요.\n"
    "지나가는 사람들이 깜짝 놀랐어요. 😲\n"
    "스크루지가 웃고 있다니!\n"
    "스크루지는 완전히 변했어요!\n"
    "어제까지의 심술궂은 스크루지는 없어요.\n"
    "새로운 스크루지가 태어났어요! 🎉\n"
    "<strong>스크루지는 완전히 변했어요!</strong>",
    # A1
    "Scrooge woke up on Christmas Day.\n"
    "He was alive and happy.\n"
    "He opened the window and shouted.\n"
    "He changed completely.",
    # A2
    "Scrooge woke up on Christmas morning feeling completely new.\n"
    "He jumped out of bed with a big smile on his old face.\n"
    "He opened the window and shouted Merry Christmas to everyone.\n"
    "He changed completely and became a different person overnight.\n"
    "People on the street could not believe their eyes and ears.\n"
    "The mean old Scrooge was gone and a kind man had taken his place."
)

STORIES["week27b"] = (
    "스크루지는 바로 행동하기 시작했어요! 🏃\n"
    "가장 큰 칠면조를 사서 밥의 집에 보냈어요. 🦃\n"
    "\"메리 크리스마스, 밥!\" 😊\n"
    "밥의 가족은 너무 놀랐어요.\n"
    "스크루지가 밥의 월급도 올려줬어요! 💰\n"
    "조카의 크리스마스 파티에도 갔어요.\n"
    "\"늦어서 미안해!\" 스크루지가 웃었어요.\n"
    "스크루지는 변해서 너그러운 사람이 되었어요.\n"
    "가난한 사람들에게도 도움을 줬어요.\n"
    "사랑을 나누기 시작했어요! 💕\n"
    "<strong>스크루지는 변해서 너그러운 사람이 되었어요!</strong>",
    # A1
    "Scrooge bought a big turkey.\n"
    "He sent it to Bob's family.\n"
    "He raised Bob's pay.\n"
    "He changed and became a generous man.",
    # A2
    "Scrooge bought the biggest turkey at the market for Bob's family.\n"
    "He gave Bob a huge raise and wished him a Merry Christmas.\n"
    "He went to his nephew's party and everyone welcomed him warmly.\n"
    "He changed and became a generous man who shared with everyone.\n"
    "He donated money to help the poor people of London.\n"
    "Scrooge discovered that giving made him happier than getting."
)

STORIES["week27c"] = (
    "크리스마스가 지났지만 스크루지는 계속 변했어요. 📅\n"
    "매일 사람들에게 친절했어요.\n"
    "작은 팀의 병원비도 내줬어요. 🏥\n"
    "작은 팀이 건강해졌어요!\n"
    "마을 사람들이 스크루지를 좋아하기 시작했어요. 😊\n"
    "\"스크루지 아저씨, 감사합니다!\"\n"
    "스크루지는 눈물을 흘리며 말했어요.\n"
    "\"나도 고맙다. 바뀔 기회를 줘서.\"\n"
    "누구든 변할 수 있어요.\n"
    "변하기에 늦은 때는 없어요! 🌟\n"
    "<strong>변하기에 늦은 때는 없어요!</strong>",
    # A1
    "Scrooge helped Tiny Tim.\n"
    "Tim got better.\n"
    "Everyone liked the new Scrooge.\n"
    "It is never too late to change who you are.",
    # A2
    "Scrooge kept being kind and generous even after Christmas.\n"
    "He paid for Tiny Tim's medicine and the boy got much better.\n"
    "The people of London grew to love the new, kind Scrooge.\n"
    "It is never too late to change who you are for the better.\n"
    "Scrooge became like a second father to little Tiny Tim.\n"
    "He proved that anyone can change when they open their heart."
)

# ═══════════════════════════════════════════════
# W28: Alice — Falls down
# ═══════════════════════════════════════════════
STORIES["week28a"] = (
    "새 이야기를 만나요! 🐰\n"
    "이상한 나라의 앨리스라는 이야기예요.\n"
    "앨리스는 언니와 함께 강가에 앉아 있었어요.\n"
    "심심하고 졸렸어요. 😴\n"
    "그때 하얀 토끼가 지나갔어요!\n"
    "\"늦었어! 늦었어!\" 토끼가 외쳤어요. 🐇\n"
    "앨리스는 토끼를 따라갔어요.\n"
    "토끼가 구멍 안으로 들어갔어요.\n"
    "앨리스도 따라 들어갔어요!\n"
    "앨리스가 떨어졌어요! 🕳️\n"
    "<strong>앨리스가 떨어졌어요!</strong>",
    # A1
    "Alice saw a white rabbit.\n"
    "She followed it into a hole.\n"
    "She fell down very deep.\n"
    "Alice fell down.",
    # A2
    "Alice was sitting by the river with her sister one boring day.\n"
    "Suddenly a white rabbit wearing a coat ran past her quickly.\n"
    "The rabbit was shouting that he was late for something important.\n"
    "Alice fell down after the rabbit into a very deep dark hole.\n"
    "She fell and fell for what seemed like a very long time.\n"
    "When she landed, she was in a strange and wonderful place."
)

STORIES["week28b"] = (
    "앨리스는 아래로 아래로 떨어졌어요! ⬇️\n"
    "떨어지는 동안 이상한 것들이 보였어요.\n"
    "책장이 있고, 지도가 있고, 잼 병이 있었어요! 🍯\n"
    "\"이게 다 뭐지?\" 앨리스가 놀랐어요.\n"
    "한참을 떨어지다가 드디어 바닥에 닿았어요.\n"
    "작은 방에 도착했어요.\n"
    "작은 문이 있었어요. 🚪\n"
    "앨리스가 토끼 구멍으로 떨어졌어요!\n"
    "여기는 어디일까요?\n"
    "이상한 모험이 시작되었어요! 🌀\n"
    "<strong>앨리스가 토끼 구멍으로 떨어졌어요!</strong>",
    # A1
    "Alice fell down and down.\n"
    "She saw strange things.\n"
    "She landed in a small room.\n"
    "Alice fell down the rabbit hole.",
    # A2
    "Alice tumbled down the rabbit hole for a very long time.\n"
    "She passed shelves full of books, maps, and jars of jam.\n"
    "Alice fell down the rabbit hole into a mysterious world below.\n"
    "She landed softly in a small room with many locked doors.\n"
    "There was a tiny golden key on a glass table in the middle.\n"
    "Alice picked it up and wondered which door it would open."
)

STORIES["week28c"] = (
    "앨리스는 작은 방에 있었어요. 🚪\n"
    "작은 문 뒤에 아름다운 정원이 보였어요.\n"
    "하지만 앨리스는 문에 들어갈 수 없었어요. 😔\n"
    "너무 컸거든요!\n"
    "테이블에 병이 있었어요.\n"
    "\"나를 마셔\" 라고 적혀 있었어요. 🧪\n"
    "앨리스가 마시자 몸이 작아졌어요!\n"
    "앨리스는 깊은 구멍으로 떨어져 이상한 세계에 왔어요.\n"
    "모든 것이 이상했어요.\n"
    "놀라운 세계가 펼쳐졌어요! ✨\n"
    "<strong>앨리스는 깊은 구멍으로 떨어져 이상한 세계에 왔어요!</strong>",
    # A1
    "Alice found a small door.\n"
    "She drank something and got small.\n"
    "She entered a strange world.\n"
    "Alice fell down a deep hole into a strange world.",
    # A2
    "Alice saw a beautiful garden through a tiny door but was too big.\n"
    "She found a bottle on the table that said Drink Me on it.\n"
    "She drank it and her body shrank down to just ten inches tall.\n"
    "Alice fell down a deep hole into a strange world full of wonders.\n"
    "Everything in this new place followed different rules entirely.\n"
    "Alice did not know what would happen to her next."
)

# ═══════════════════════════════════════════════
# W29: Everything strange
# ═══════════════════════════════════════════════
STORIES["week29a"] = (
    "앨리스는 이상한 나라를 걷고 있었어요. 🌀\n"
    "커졌다 작아졌다를 반복했어요.\n"
    "케이크를 먹으면 커지고, 약을 마시면 작아졌어요.\n"
    "\"이상해! 규칙이 없잖아!\" 😵\n"
    "웃는 고양이를 만났어요. 🐱\n"
    "\"여기서는 모두가 미쳤어!\" 고양이가 웃으며 말했어요.\n"
    "앨리스는 어리둥절했어요.\n"
    "모든 것이 이상했어요.\n"
    "상식이 통하지 않는 세계였어요.\n"
    "앨리스는 혼란스러웠어요! 😰\n"
    "<strong>모든 것이 이상했어요!</strong>",
    # A1
    "Alice grew big and then small.\n"
    "She met a smiling cat.\n"
    "Nothing made sense here.\n"
    "Everything was strange.",
    # A2
    "Alice kept changing size by eating and drinking strange things.\n"
    "She met a Cheshire Cat with a huge grin floating in the air.\n"
    "The cat told her that everyone in Wonderland was completely mad.\n"
    "Everything was strange and nothing followed the rules she knew.\n"
    "Cakes made her grow tall and drinks made her shrink down.\n"
    "Alice felt confused but curious about this upside-down world."
)

STORIES["week29b"] = (
    "앨리스는 모자 장수의 티 파티에 갔어요. 🎩☕\n"
    "모자 장수, 3월 토끼, 겨울잠쥐가 있었어요.\n"
    "\"수수께끼를 내줄게!\" 모자 장수가 말했어요.\n"
    "\"까마귀가 책상과 비슷한 점은?\"\n"
    "앨리스가 생각했어요. 🤔\n"
    "\"모르겠어요. 정답이 뭐예요?\"\n"
    "\"나도 몰라!\" 모자 장수가 웃었어요. 😂\n"
    "이상한 나라의 모든 것은 매우 혼란스러웠어요.\n"
    "답이 없는 수수께끼, 끝나지 않는 파티...\n"
    "정말 이상한 세계예요! 🌀\n"
    "<strong>이상한 나라의 모든 것은 매우 혼란스러웠어요!</strong>",
    # A1
    "Alice went to a tea party.\n"
    "The Mad Hatter asked riddles.\n"
    "Nothing had an answer.\n"
    "Everything in Wonderland was very confusing.",
    # A2
    "Alice sat down at the Mad Hatter's strange tea party.\n"
    "The Hatter asked riddles that had no answers at all.\n"
    "The March Hare poured tea everywhere and nobody minded.\n"
    "Everything in Wonderland was very confusing and made no sense.\n"
    "Time had stopped at six o'clock and the party never ended.\n"
    "Alice wondered if anything in this world would ever be normal."
)

STORIES["week29c"] = (
    "앨리스는 계속 이상한 사람들을 만났어요. 🌀\n"
    "버섯 위에 앉은 애벌레를 만났어요. 🐛\n"
    "\"넌 누구야?\" 애벌레가 물었어요.\n"
    "앨리스는 대답할 수 없었어요.\n"
    "\"모르겠어요... 나는 오늘 아침에는 알았는데...\"\n"
    "앨리스는 자기가 누구인지도 헷갈렸어요. 😰\n"
    "모든 것이 너무 이상해서 앨리스는 자기가 누구인지 물었어요.\n"
    "이상한 나라에서는 자기 자신도 잊게 돼요.\n"
    "앨리스의 모험은 계속되었어요.\n"
    "이 세계에서 빠져나갈 수 있을까요? 🤔\n"
    "<strong>모든 것이 너무 이상해서 앨리스는 자기가 누구인지 물었어요!</strong>",
    # A1
    "Alice met a caterpillar.\n"
    "It asked her who she was.\n"
    "Alice did not know anymore.\n"
    "Everything was so strange that Alice asked who she was.",
    # A2
    "Alice met a blue caterpillar smoking on top of a mushroom.\n"
    "The caterpillar asked her a simple question about her identity.\n"
    "But Alice could not answer because she had changed so many times.\n"
    "Everything was so strange that Alice asked who she was inside.\n"
    "She had been big, small, and everything in between that day.\n"
    "In Wonderland, even knowing yourself became a great puzzle."
)

# ═══════════════════════════════════════════════
# W30: Questions rules
# ═══════════════════════════════════════════════
STORIES["week30a"] = (
    "앨리스는 하트 여왕의 정원에 왔어요. 🌹\n"
    "카드 병사들이 장미를 빨갛게 칠하고 있었어요!\n"
    "\"왜 장미를 칠해요?\" 앨리스가 물었어요.\n"
    "\"여왕이 빨간 장미를 좋아하거든!\" 😰\n"
    "하얀 장미를 심으면 목이 잘려요!\n"
    "앨리스는 이해할 수 없었어요.\n"
    "\"이게 무슨 규칙이야?\"\n"
    "앨리스는 규칙에 의문을 품었어요.\n"
    "이상한 나라의 규칙은 불공평했어요.\n"
    "앨리스는 용감하게 질문했어요! 🤔\n"
    "<strong>앨리스는 규칙에 의문을 품었어요!</strong>",
    # A1
    "Alice went to the Queen's garden.\n"
    "The rules did not make sense.\n"
    "Alice asked why.\n"
    "She questioned rules.",
    # A2
    "Alice arrived at the Queen of Hearts' beautiful rose garden.\n"
    "Card soldiers were painting white roses red in a big hurry.\n"
    "The Queen would be angry if she saw any white roses at all.\n"
    "She questioned rules that seemed unfair and did not make sense.\n"
    "Alice could not understand why everyone was so afraid.\n"
    "She bravely asked the soldiers why they followed such silly rules."
)

STORIES["week30b"] = (
    "하트 여왕이 나타났어요! 👑\n"
    "\"저 장미는 빨간색이야?\" 여왕이 물었어요.\n"
    "\"목을 잘라!\" 여왕이 외쳤어요. 😱\n"
    "앨리스가 나섰어요.\n"
    "\"그건 너무해요! 장미 색이 뭐가 중요해요?\"\n"
    "여왕이 화를 냈어요.\n"
    "\"누가 감히 나에게 반대해!\"\n"
    "하지만 앨리스는 물러서지 않았어요.\n"
    "앨리스는 자기가 믿는 모든 것에 의문을 품었어요.\n"
    "옳지 않은 것에 용감하게 맞섰어요! 💪\n"
    "<strong>앨리스는 자기가 믿는 모든 것에 의문을 품었어요!</strong>",
    # A1
    "The Queen shouted angry orders.\n"
    "Alice stood up to the Queen.\n"
    "She was not afraid.\n"
    "She questioned everything she believed.",
    # A2
    "The Queen of Hearts screamed and ordered everyone's head cut off.\n"
    "Alice stepped forward bravely and told the Queen she was wrong.\n"
    "She questioned everything she believed about following rules blindly.\n"
    "Why should everyone obey rules that are cruel and unfair?\n"
    "The other creatures were shocked that someone stood up to the Queen.\n"
    "Alice was the only one brave enough to speak the truth."
)

STORIES["week30c"] = (
    "앨리스는 이상한 나라의 재판에 참석했어요. ⚖️\n"
    "잭이 여왕의 타르트를 훔쳤다는 재판이었어요. 🥧\n"
    "하지만 증거가 하나도 없었어요!\n"
    "\"먼저 판결을 하고, 나중에 증거를 찾아!\" 여왕이 말했어요.\n"
    "앨리스가 외쳤어요.\n"
    "\"그건 말이 안 돼요! 증거 없이 벌을 줄 수 없어요!\"\n"
    "앨리스는 모든 것에 의문을 품었어요.\n"
    "이상한 나라에는 보통 규칙이 없었기 때문이에요.\n"
    "용감하게 질문하는 것이 중요해요! 🗣️\n"
    "앨리스처럼 불공평한 것에 맞서요! ✊\n"
    "<strong>앨리스는 모든 것에 의문을 품었어요. 이상한 나라에는 보통 규칙이 없었기 때문이에요!</strong>",
    # A1
    "There was a trial in Wonderland.\n"
    "The Queen wanted to punish first.\n"
    "Alice said that was not fair.\n"
    "She questioned everything because Wonderland had no ordinary rules.",
    # A2
    "Alice attended a trial where the Knave was accused of stealing.\n"
    "The Queen demanded a verdict before hearing any evidence at all.\n"
    "Alice stood up and said that was completely wrong and unfair.\n"
    "She questioned everything because Wonderland had no ordinary rules.\n"
    "You cannot punish someone without proof no matter who you are.\n"
    "Alice showed that asking questions is the bravest thing we can do."
)

# ═══════════════════════════════════════════════
# W31: Children see differently
# ═══════════════════════════════════════════════
STORIES["week31a"] = (
    "앨리스는 드디어 이상한 나라에서 깨어났어요! 😊\n"
    "언니 옆에서 잠이 들었던 거예요.\n"
    "\"꿈이었구나!\" 앨리스가 말했어요.\n"
    "하지만 꿈에서 많은 것을 배웠어요.\n"
    "이상한 나라는 어른들이 잊은 세계였어요.\n"
    "규칙에 질문하고, 신기한 것을 찾는 세계요.\n"
    "아이들은 다르게 봐요. 👀\n"
    "어른들이 그냥 지나치는 것을 아이들은 발견해요.\n"
    "그것이 앨리스의 힘이었어요.\n"
    "앨리스처럼 세상을 다르게 봐요! 🌟\n"
    "<strong>아이들은 다르게 봐요!</strong>",
    # A1
    "Alice woke up from her dream.\n"
    "She learned many things.\n"
    "Children notice what adults miss.\n"
    "Children see differently.",
    # A2
    "Alice finally woke up from her dream under the big tree.\n"
    "She told her sister about all the amazing things she saw.\n"
    "Wonderland was a place where nothing followed the usual rules.\n"
    "Children see differently and notice things that adults walk past.\n"
    "Alice had questioned everything because she saw with fresh eyes.\n"
    "Sometimes the youngest person in the room is the wisest one."
)

STORIES["week31b"] = (
    "앨리스의 언니는 앨리스의 이야기를 들었어요. 📖\n"
    "토끼 이야기, 모자 장수 이야기, 여왕 이야기...\n"
    "언니는 미소를 지었어요. 😊\n"
    "\"앨리스야, 너는 특별한 아이야.\"\n"
    "\"어른들은 이런 꿈을 꾸지 못해.\"\n"
    "아이들은 어른들이 종종 잊는 것을 볼 수 있어요.\n"
    "신기함, 궁금함, 질문하는 마음...\n"
    "이것들을 잃지 않는 것이 중요해요.\n"
    "어른이 되어서도 질문할 수 있어야 해요.\n"
    "아이의 눈으로 세상을 봐요! 👁️\n"
    "<strong>아이들은 어른들이 종종 잊는 것을 볼 수 있어요!</strong>",
    # A1
    "Alice's sister listened to her story.\n"
    "Children have special eyes.\n"
    "They see wonder and ask questions.\n"
    "Children see what adults often forget.",
    # A2
    "Alice's older sister listened carefully to every strange detail.\n"
    "She wished she could dream such wonderful dreams like Alice.\n"
    "Children see what adults often forget about the magical world.\n"
    "They ask why the sky is blue and where the stars go at dawn.\n"
    "Alice's adventure reminded her sister of her own childhood wonder.\n"
    "We should never stop seeing the world through curious young eyes."
)

STORIES["week31c"] = (
    "앨리스의 이야기가 끝났어요. 📚\n"
    "이상한 나라는 사라졌지만 앨리스는 변했어요.\n"
    "이제 앨리스는 질문을 두려워하지 않아요.\n"
    "\"왜?\" \"어떻게?\" \"정말?\" 🤔\n"
    "어른들은 \"그냥 그런 거야\" 라고 말하지만\n"
    "아이들은 \"정말 그런 거야?\" 라고 물어요.\n"
    "아이들은 어른들이 잊은 것을 봐요.\n"
    "세상은 놀라운 곳이라는 것을요! 🌍\n"
    "앨리스처럼 용감하게 질문해요.\n"
    "세상을 아이의 눈으로 보면 놀라운 것이 많아요! ✨\n"
    "<strong>아이들은 어른들이 잊은 것을 봐요, 세상은 놀라운 곳이라는 것을요!</strong>",
    # A1
    "Alice's adventure ended.\n"
    "She was not afraid to ask why.\n"
    "The world is full of wonder.\n"
    "Children see what grown-ups forget the world is wonderful.",
    # A2
    "Alice's adventure in Wonderland was over but its lessons stayed.\n"
    "She learned to question rules and never accept unfair things.\n"
    "Adults say that is just how things are without thinking deeply.\n"
    "Children see what grown-ups forget, that the world is wonderful.\n"
    "Alice showed us that asking why is the beginning of all wisdom.\n"
    "Let us keep our curious eyes open and never stop wondering."
)

# ═══════════════════════════════════════════════
# W32: Tom Sawyer — Hates work
# ═══════════════════════════════════════════════
STORIES["week32a"] = (
    "새 이야기를 시작해요! 🎨\n"
    "톰 소여라는 소년을 만나요.\n"
    "톰은 미국 미시시피 강가 마을에 살아요.\n"
    "폴리 이모와 함께 살아요.\n"
    "톰은 장난꾸러기예요! 😜\n"
    "학교를 빼먹고, 싸우고, 말썽을 피워요.\n"
    "어느 토요일 아침, 이모가 말했어요.\n"
    "\"톰! 울타리를 칠해!\" 🎨\n"
    "톰은 일하기 싫었어요.\n"
    "\"아, 일하기 싫다!\" 😩\n"
    "<strong>톰은 일하기 싫었어요!</strong>",
    # A1
    "Tom lived with Aunt Polly.\n"
    "She told him to paint a fence.\n"
    "Tom did not want to work.\n"
    "Tom hated work.",
    # A2
    "Tom Sawyer was a clever boy who lived by the Mississippi River.\n"
    "His Aunt Polly took care of him and often got annoyed with him.\n"
    "One Saturday morning, she told him to paint the long white fence.\n"
    "Tom hated work and did not want to paint the fence at all.\n"
    "He looked at the long fence and felt very sorry for himself.\n"
    "All his friends were playing while he was stuck with a paintbrush."
)

STORIES["week32b"] = (
    "톰은 울타리 앞에 서 있었어요. 🎨\n"
    "울타리가 너무 길었어요.\n"
    "\"이걸 언제 다 칠해!\" 😫\n"
    "페인트 통과 붓을 보니 한숨이 나왔어요.\n"
    "친구들은 강에서 수영하고 있었어요. 🏊\n"
    "재미있는 소리가 들렸어요.\n"
    "\"나도 놀고 싶다!\"\n"
    "톰은 오늘 일하고 싶지 않았어요.\n"
    "하지만 이모에게 혼나기 싫었어요.\n"
    "톰은 기발한 생각을 하기 시작했어요! 💡\n"
    "<strong>톰은 오늘 일하고 싶지 않았어요!</strong>",
    # A1
    "The fence was very long.\n"
    "Tom's friends were playing.\n"
    "He did not want to paint.\n"
    "Tom did not want to work today.",
    # A2
    "Tom stared at the long white fence that stretched on and on.\n"
    "He could hear his friends laughing and swimming in the river.\n"
    "The paint bucket felt heavy and the brush was old and worn.\n"
    "Tom did not want to work today but he had no choice at all.\n"
    "If he ran away, Aunt Polly would be very angry with him.\n"
    "Tom started thinking of a clever plan to escape his chore."
)

STORIES["week32c"] = (
    "톰은 울타리를 칠하기 시작했어요. 🎨\n"
    "하지만 아주 천천히 칠했어요.\n"
    "\"한 번 칠하고... 쉬고... 또 칠하고...\" 😴\n"
    "아침 해가 뜨겁게 내리쬐었어요. ☀️\n"
    "땀이 흘렀어요.\n"
    "\"토요일인데 왜 일해야 하지?\"\n"
    "톰은 그 아침 울타리를 칠하고 싶지 않았어요.\n"
    "다른 아이들은 자유로웠어요.\n"
    "톰만 여기서 일하고 있었어요.\n"
    "톰은 무언가 좋은 방법을 생각해냈어요! 🧠\n"
    "<strong>톰은 그 아침 울타리를 칠하고 싶지 않았어요!</strong>",
    # A1
    "Tom painted very slowly.\n"
    "The sun was hot.\n"
    "He wanted to play.\n"
    "Tom did not want to paint the fence that morning.",
    # A2
    "Tom dipped his brush and painted one slow stroke on the fence.\n"
    "The hot morning sun beat down on him as he worked alone.\n"
    "Sweat dripped from his face and he kept looking at the river.\n"
    "Tom did not want to paint the fence that morning at all.\n"
    "Every other boy in town was free to play and have fun.\n"
    "But then a brilliant idea suddenly popped into Tom's head."
)

# ═══════════════════════════════════════════════
# W33: Tricks friends
# ═══════════════════════════════════════════════
STORIES["week33a"] = (
    "톰에게 기발한 생각이 떠올랐어요! 💡\n"
    "친구 벤이 사과를 먹으며 지나갔어요. 🍎\n"
    "\"하하! 톰이 일해야 하네!\" 벤이 놀렸어요.\n"
    "하지만 톰은 슬픈 척 하지 않았어요.\n"
    "오히려 즐겁게 칠하는 척 했어요! 😊\n"
    "\"와, 이거 너무 재미있다!\"\n"
    "벤이 궁금해졌어요.\n"
    "\"나도 해봐도 돼?\" 벤이 물었어요.\n"
    "톰은 친구를 속였어요!\n"
    "기발한 방법이었어요! 😄\n"
    "<strong>톰은 친구를 속였어요!</strong>",
    # A1
    "Tom's friend Ben came by.\n"
    "Tom pretended painting was fun.\n"
    "Ben wanted to try too.\n"
    "He tricked his friends.",
    # A2
    "Tom's friend Ben walked by eating a juicy red apple.\n"
    "Ben laughed at Tom for having to work on a Saturday morning.\n"
    "But Tom pretended that painting the fence was incredibly fun.\n"
    "He tricked his friends into wanting to paint the fence too.\n"
    "Ben begged Tom to let him try and even gave his apple.\n"
    "Tom's clever plan was working perfectly just as he hoped."
)

STORIES["week33b"] = (
    "벤이 울타리를 칠하기 시작했어요! 🎨\n"
    "톰은 나무 그늘에서 사과를 먹었어요. 🍎\n"
    "다른 친구들도 왔어요.\n"
    "\"나도 칠하고 싶어!\" 짐이 말했어요.\n"
    "\"나도!\" \"나도!\" 모두가 원했어요.\n"
    "톰은 미끼를 던졌어요.\n"
    "\"음... 이건 아무나 할 수 없는 일인데...\"\n"
    "친구들이 선물을 가져왔어요! 🎁\n"
    "구슬, 연, 죽은 고양이까지!\n"
    "톰은 영리하게 친구들을 속여서 일을 시켰어요! 😏\n"
    "<strong>톰은 영리하게 친구들을 속여서 일을 시켰어요!</strong>",
    # A1
    "More friends came and wanted to paint.\n"
    "They gave Tom gifts.\n"
    "Tom sat and watched.\n"
    "He cleverly tricked friends into working.",
    # A2
    "One by one, more boys from the neighborhood came to watch.\n"
    "Each one begged for a chance to paint the beautiful fence.\n"
    "He cleverly tricked friends into working by making it look special.\n"
    "They even paid Tom with marbles, kites, and other treasures.\n"
    "Tom sat under the tree enjoying his pile of new presents.\n"
    "By afternoon, the whole fence was painted three coats thick."
)

STORIES["week33c"] = (
    "울타리가 완벽하게 칠해졌어요! 🎨✨\n"
    "세 번이나 칠해졌어요!\n"
    "톰은 한 번도 안 칠했어요. 😎\n"
    "이모가 나와서 깜짝 놀랐어요.\n"
    "\"어머나! 이렇게 잘 칠하다니!\"\n"
    "이모가 톰에게 사과를 줬어요. 🍎\n"
    "톰은 친구들에게 재미있게 보이게 해서 일을 시켰어요.\n"
    "톰은 세상에서 가장 영리한 소년이었어요.\n"
    "일을 놀이로 바꿨어요!\n"
    "톰의 천재적인 방법이에요! 🧠\n"
    "<strong>톰은 재미있게 보이게 해서 친구들에게 일을 시켰어요!</strong>",
    # A1
    "The fence was perfectly painted.\n"
    "Tom did not paint at all.\n"
    "Aunt Polly was impressed.\n"
    "He made his friends do his work by making it fun.",
    # A2
    "The fence was painted so beautifully that Aunt Polly was amazed.\n"
    "Tom had not painted a single stroke himself the whole day.\n"
    "He made his friends do his work by making it fun and special.\n"
    "The boys did not even realize they had been tricked at all.\n"
    "Tom learned that people want things more when they seem rare.\n"
    "It was the cleverest trick any boy in town had ever played."
)

# ═══════════════════════════════════════════════
# W34: Tells truth
# ═══════════════════════════════════════════════
STORIES["week34a"] = (
    "어느 날 마을에서 끔찍한 일이 일어났어요. 😱\n"
    "묘지에서 살인 사건이 일어났어요!\n"
    "인디언 조가 범인이었어요.\n"
    "하지만 조는 거짓말을 했어요.\n"
    "\"머프 포터가 했어!\" 🤥\n"
    "가난한 머프 포터가 감옥에 갇혔어요.\n"
    "톰은 그날 밤 묘지에 있었어요.\n"
    "톰은 진실을 알고 있었어요. 😰\n"
    "톰은 진실을 말했어요.\n"
    "하지만 무서웠어요.\n"
    "<strong>톰은 진실을 말했어요!</strong>",
    # A1
    "A bad thing happened in town.\n"
    "Tom saw the truth.\n"
    "He was very scared.\n"
    "He told the truth.",
    # A2
    "Something terrible happened at the graveyard one dark night.\n"
    "Injun Joe committed a crime but blamed poor Muff Potter for it.\n"
    "Tom had been hiding in the graveyard and saw everything happen.\n"
    "He told the truth even though he was shaking with fear inside.\n"
    "He knew the real criminal and could save an innocent man.\n"
    "But telling the truth meant making a dangerous enemy."
)

STORIES["week34b"] = (
    "톰은 매일 무서웠어요. 😰\n"
    "인디언 조가 보복할까 봐 걱정했어요.\n"
    "하지만 머프 포터가 감옥에서 울고 있었어요.\n"
    "\"나는 아무것도 안 했는데...\" 😢\n"
    "톰의 마음이 아팠어요.\n"
    "\"내가 진실을 말해야 해!\"\n"
    "재판이 열렸어요. ⚖️\n"
    "톰은 용기를 내서 법정에 섰어요.\n"
    "\"인디언 조가 했어요! 제가 봤어요!\"\n"
    "톰은 진실을 말할 만큼 용감했어요! 💪\n"
    "<strong>톰은 진실을 말할 만큼 용감했어요!</strong>",
    # A1
    "Tom was afraid of Injun Joe.\n"
    "But Muff Potter was innocent.\n"
    "Tom went to court.\n"
    "He was brave enough to tell the truth.",
    # A2
    "Tom was terrified because Injun Joe was a very dangerous man.\n"
    "But innocent Muff Potter was suffering in prison for nothing.\n"
    "Tom gathered all his courage and went to the courtroom.\n"
    "He was brave enough to tell the truth in front of everyone.\n"
    "He pointed at Injun Joe and told the judge what really happened.\n"
    "The whole courtroom gasped when they heard Tom's brave words."
)

STORIES["week34c"] = (
    "톰이 법정에서 진실을 말했어요! ⚖️\n"
    "\"그날 밤 묘지에서 인디언 조를 봤어요!\"\n"
    "판사님과 사람들이 놀랐어요. 😲\n"
    "인디언 조는 도망쳤어요!\n"
    "머프 포터는 자유가 되었어요. 🎉\n"
    "\"고맙다, 톰!\" 포터 아저씨가 울었어요.\n"
    "마을 사람들이 톰을 영웅이라고 했어요.\n"
    "톰은 용감하게 법정에서 누군가를 살리기 위해 진실을 말했어요.\n"
    "진실을 말하는 것은 어렵지만 중요해요.\n"
    "톰은 진짜 용감한 소년이에요! 🌟\n"
    "<strong>톰은 용감하게 법정에서 누군가를 살리기 위해 진실을 말했어요!</strong>",
    # A1
    "Tom told the court what he saw.\n"
    "Muff Potter was set free.\n"
    "Tom was called a hero.\n"
    "He bravely told the truth in court to save someone.",
    # A2
    "Tom stood before the judge and told everything he had seen.\n"
    "Injun Joe jumped through a window and escaped into the night.\n"
    "Muff Potter was freed and cried tears of joy and thanks.\n"
    "He bravely told the truth in court to save someone innocent.\n"
    "The whole town praised Tom for his incredible courage.\n"
    "Tom learned that doing the right thing is always worth the fear."
)

# ═══════════════════════════════════════════════
# W35: Adventure needs courage
# ═══════════════════════════════════════════════
STORIES["week35a"] = (
    "톰과 허크는 보물을 찾으러 갔어요! 💰\n"
    "인디언 조가 보물을 숨겼다는 소문이 있었어요.\n"
    "\"보물을 찾으러 가자!\" 톰이 말했어요.\n"
    "허크는 무서웠어요. 😰\n"
    "\"인디언 조가 위험해...\"\n"
    "하지만 톰은 포기하지 않았어요.\n"
    "동굴 안으로 들어갔어요. 🕯️\n"
    "어둡고 무서웠어요.\n"
    "모험에는 용기가 필요해요.\n"
    "톰은 용감했어요! 💪\n"
    "<strong>모험에는 용기가 필요해요!</strong>",
    # A1
    "Tom and Huck went to find treasure.\n"
    "They went into a dark cave.\n"
    "It was scary but exciting.\n"
    "Adventure needs courage.",
    # A2
    "Tom and his friend Huck decided to search for hidden treasure.\n"
    "They heard Injun Joe had buried gold coins somewhere nearby.\n"
    "Tom led the way into a deep, dark cave with just a candle.\n"
    "Adventure needs courage, and Tom had plenty of it inside him.\n"
    "Huck was shaking but followed his brave friend into the dark.\n"
    "Together they faced their fears and walked deeper underground."
)

STORIES["week35b"] = (
    "동굴 안은 정말 무서웠어요. 🕯️\n"
    "박쥐가 날아다니고, 물소리가 들렸어요. 🦇\n"
    "톰과 허크는 점점 더 깊이 들어갔어요.\n"
    "갑자기 촛불이 꺼졌어요!\n"
    "\"톰! 어떡해!\" 허크가 소리쳤어요. 😱\n"
    "칠흑 같은 어둠이었어요.\n"
    "하지만 톰은 침착했어요.\n"
    "\"걱정 마, 허크. 길을 찾을 거야.\"\n"
    "진짜 모험에는 항상 약간의 용기가 필요해요.\n"
    "톰은 포기하지 않았어요! 💪\n"
    "<strong>진짜 모험에는 항상 약간의 용기가 필요해요!</strong>",
    # A1
    "The cave was very dark.\n"
    "Their candle went out.\n"
    "Huck was scared.\n"
    "Real adventure always requires a little courage.",
    # A2
    "The cave was pitch black and full of strange, scary sounds.\n"
    "Bats flew around their heads and cold water dripped from above.\n"
    "When their candle went out, Huck started to panic in the dark.\n"
    "Real adventure always requires a little courage to keep going.\n"
    "Tom stayed calm and used his hands to feel along the walls.\n"
    "He knew they would find the way out if they did not give up."
)

STORIES["week35c"] = (
    "톰은 동굴에서 빛을 찾았어요! 🕯️\n"
    "그리고 놀라운 것을 발견했어요.\n"
    "인디언 조의 보물 상자가 있었어요! 💰\n"
    "금화가 가득했어요!\n"
    "톰과 허크는 보물을 찾았어요! 🎉\n"
    "마을로 돌아오자 모두가 축하해줬어요.\n"
    "\"톰, 넌 정말 대단해!\"\n"
    "진짜 모험에는 용기가 필요해요.\n"
    "톰에게는 아무도 몰랐던 용기가 있었어요.\n"
    "용기가 톰을 영웅으로 만들었어요! 🌟\n"
    "<strong>진짜 모험에는 용기가 필요해요, 톰에게는 아무도 몰랐던 용기가 있었어요!</strong>",
    # A1
    "Tom found light in the cave.\n"
    "They found the treasure.\n"
    "Tom was a hero.\n"
    "Real adventure needs courage Tom had more than anyone knew.",
    # A2
    "Tom spotted a tiny beam of light deep inside the dark cave.\n"
    "Following it, they discovered Injun Joe's treasure chest of gold.\n"
    "The boys carried the heavy chest out into the bright sunshine.\n"
    "Real adventure needs courage and Tom had more than anyone knew.\n"
    "The whole town celebrated the two brave boys and their treasure.\n"
    "Tom proved that courage and determination can lead to great things."
)

# ═══════════════════════════════════════════════
# W36: Work feels like play
# ═══════════════════════════════════════════════
STORIES["week36a"] = (
    "톰은 이제 마을의 영웅이에요! 🌟\n"
    "보물도 찾고, 진실도 말하고, 모험도 했어요.\n"
    "하지만 톰이 처음에 한 일이 뭐였죠?\n"
    "맞아요, 울타리 칠하기! 🎨\n"
    "톰은 울타리를 재미있게 만들었어요.\n"
    "싫은 일도 재미있게 바꿀 수 있어요.\n"
    "일이 놀이처럼 느껴질 수 있어요.\n"
    "태도가 모든 것을 바꿔요.\n"
    "톰이 그것을 보여줬어요.\n"
    "일도 놀이가 될 수 있어요! 🎉\n"
    "<strong>일이 놀이처럼 느껴질 수 있어요!</strong>",
    # A1
    "Tom was now a hero.\n"
    "He made fence painting fun.\n"
    "Attitude changes everything.\n"
    "Work can feel like play.",
    # A2
    "Tom Sawyer had become the most famous boy in the whole town.\n"
    "He found treasure, saved a man, and had amazing adventures.\n"
    "But his greatest trick was making fence painting seem like fun.\n"
    "Work can feel like play when you change the way you see it.\n"
    "Tom taught everyone that attitude is more important than the task.\n"
    "A boring chore can become an adventure with the right mindset."
)

STORIES["week36b"] = (
    "톰 소여 이야기에서 무엇을 배웠나요? 📖\n"
    "톰은 영리함으로 친구들에게 일을 시켰어요.\n"
    "용기로 진실을 말했어요.\n"
    "모험심으로 보물을 찾았어요! 💰\n"
    "하지만 가장 큰 교훈은 뭘까요?\n"
    "바로 이거예요.\n"
    "가장 좋은 방법은 일을 놀이처럼 느끼게 하는 거예요.\n"
    "싫어하는 일도 재미있게 만들면 즐거워져요! 😊\n"
    "이것이 톰 소여의 가장 큰 비밀이에요.\n"
    "우리도 시도해 봐요! 🌟\n"
    "<strong>가장 좋은 방법은 일을 놀이처럼 느끼게 하는 거예요!</strong>",
    # A1
    "Tom was clever, brave, and fun.\n"
    "He made work seem like play.\n"
    "This was his best trick.\n"
    "The best trick is making work feel like play.",
    # A2
    "Tom Sawyer taught us many important lessons about life.\n"
    "He showed that cleverness can solve problems in surprising ways.\n"
    "He proved that courage matters when truth needs to be told.\n"
    "The best trick is making work feel like play for everyone.\n"
    "When we enjoy what we do, we do it much better.\n"
    "Tom's secret was always seeing fun where others saw boredom."
)

STORIES["week36c"] = (
    "톰 소여 이야기가 끝났어요! 📚\n"
    "그리고 4학년 영어 이야기도 끝이에요.\n"
    "우리는 많은 이야기를 읽었어요.\n"
    "두더지의 용기, 도로시의 집 사랑... 🏠\n"
    "폴리아나의 기쁨 찾기, 메리 포핀스의 마법... ✨\n"
    "샬롯의 우정, 비밀 정원의 치유... 🌿\n"
    "스크루지의 변화, 앨리스의 질문... 🤔\n"
    "그리고 톰의 재미있는 모험! 🎉\n"
    "가장 좋은 방법은 힘든 일도 놀이처럼 느끼게 하는 거예요.\n"
    "여러분, 영어 공부도 놀이처럼 즐겨요! 🌈\n"
    "<strong>가장 좋은 방법은 힘든 일도 놀이처럼 느끼게 하는 거예요!</strong>",
    # A1
    "We finished all the G4 stories.\n"
    "We learned many lessons.\n"
    "Make hard work fun.\n"
    "The best trick is making hard work feel like play.",
    # A2
    "Congratulations on finishing all the Grade 4 English stories.\n"
    "From Wind in the Willows to Tom Sawyer, we learned so much.\n"
    "Every story taught us about courage, love, and seeing differently.\n"
    "The best trick is making hard work feel like play every day.\n"
    "Tom Sawyer showed us that attitude can change everything.\n"
    "Keep learning English with joy, just like playing a wonderful game."
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
    raw = raw.strip('"').strip('\u201c\u201d')
    return raw

def escape_for_storyplay(text):
    """Remove HTML tags and escape for onclick attribute."""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('\n', ' ').replace('  ', ' ')
    text = text.replace("'", "\\'")
    text = text.replace('"', '')
    return text.strip()

def build_section2_body(korean, a1_lines, a2_lines, key_sentence):
    """Build the new section 2 body HTML."""
    kr_html = korean.replace('\n', '<br>')

    # A1
    a1_parts = a1_lines.split('\n')
    a1_display = '<br>'.join(a1_parts)
    for p in a1_parts:
        stripped = p.strip().rstrip('.')
        ks = key_sentence.rstrip('.')
        if stripped.lower() == ks.lower() or ks.lower() in stripped.lower():
            a1_display = a1_display.replace(p, f'<span class="hl">{p}</span>')
            break
    a1_plain = escape_for_storyplay(a1_lines)

    # A2
    a2_parts = a2_lines.split('\n')
    a2_display = '<br>'.join(a2_parts)
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
    key = fname.replace('.html', '')

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
        story_en_match = re.search(r'(\.story-en\{[^}]+\})', content)
        if story_en_match:
            insert_after = story_en_match.group(0)
            content = content.replace(insert_after, insert_after + '\n' + CSS_ADDITION)

    # 2. Replace section 2 body
    sec2_hdr = re.search(
        r'<div class="sec-hdr"><div class="sec-num" style="background:var\(--coral\);">2</div>',
        content
    )
    if not sec2_hdr:
        print(f"  SKIP {fname}: no section 2 header found")
        return False

    sec2_start = sec2_hdr.start()

    sec_body_match = re.search(r'<div class="sec-body">', content[sec2_start:])
    if not sec_body_match:
        print(f"  SKIP {fname}: no sec-body in section 2")
        return False

    body_start = sec2_start + sec_body_match.end()

    prog_match = re.search(r'</div><div class="prog"><div class="prog-fill" style="width:22', content[body_start:])
    if not prog_match:
        print(f"  SKIP {fname}: no prog bar found after section 2")
        return False

    body_end = body_start + prog_match.start()

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
    updated = 0
    skipped = 0
    errors = 0

    for f in files:
        fname = os.path.basename(f)
        # Only process weekXXa/b/c files
        if not re.match(r'week\d{2}[abc]\.html', fname):
            continue

        try:
            if process_file(f):
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR {fname}: {e}")
            import traceback
            traceback.print_exc()
            errors += 1

    print(f"\n=== DONE: {updated} updated, {skipped} skipped, {errors} errors ===")


if __name__ == '__main__':
    main()

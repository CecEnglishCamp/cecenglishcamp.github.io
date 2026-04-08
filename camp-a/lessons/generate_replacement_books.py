#!/usr/bin/env python3
"""Generate 48 HTML lesson files for replacement books."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
R2 = "https://pub-a418b5aad0bd4c3fb41cf7159403fc12.r2.dev"
GPT_URL = "https://chatgpt.com/g/g-69b4931ba6d4819194bb864aed20723b"

# ─── BOOK DATA ───────────────────────────────────────────────
BOOKS = {
    # G4 Mary Poppins W13-W16
    "g4_mary": {
        "grade": 4, "quarter": "Q2", "book": "Mary Poppins",
        "book_kr": "메리 포핀스", "emoji": "☂️",
        "img": f"{R2}/images/mary-poppins/w13_new.png",
        "ratio": "영어 50% / 한국어 50%", "level": "B1",
        "weeks": {
            13: {
                "d1": {"key_en": "Mary Poppins arrived.", "key_kr": "메리 포핀스가 도착했어요.",
                       "story_kr": "어느 바람 부는 날,\n우산을 든 여자가 하늘에서 내려왔어요.\n\"저는 메리 포핀스예요.\"\n메리 포핀스가 도착했어요.",
                       "story_en": "On a windy day,\na woman with an umbrella came down from the sky.\n\"I am Mary Poppins.\"\nMary Poppins arrived.",
                       "vocab": [("arrived","도착했다","🌬️","\"She arrived.\""),("umbrella","우산","☂️","\"An umbrella.\""),("windy","바람 부는","💨","\"A windy day.\""),("sky","하늘","🌤️","\"From the sky.\"")],
                       "pick_blank": "Mary Poppins ___.", "pick_ans": "arrived", "pick_choices": ["arrived","left","cried"],
                       "wo_kr": "\"메리 포핀스가 도착했어요.\"를 영어로!", "wo_words": ["Mary","Poppins","arrived"], "wo_ans": "Mary Poppins arrived",
                       "listen_text": "Mary Poppins arrived on a windy day.", "listen_ok": "메리 포핀스가 도착했다", "listen_no1": "메리 포핀스가 떠났다", "listen_no2": "아무도 오지 않았다",
                       "dict_word": "arrived", "dict_hint": "a r r i v e _",
                       "q1": "메리 포핀스는 어떻게 왔나요?", "q1_ok": "☂️ 하늘에서 우산을 타고", "q1_no1": "🚗 자동차로", "q1_no2": "🚶 걸어서",
                       "q2": "\"arrived\"의 뜻은?", "q2_ok": "🌬️ 도착했다", "q2_no1": "😢 울었다", "q2_no2": "😴 잠들었다",
                       "write_blank": "Mary Poppins ___.", "write_ans": "arrived", "write_c1": "arrived", "write_c2": "left", "write_c3": "slept",
                       "write_prompt": "바람 부는 날 경험을 영어로 써봐!"},
                "d2": {"key_en": "Mary Poppins arrived because the children needed help.", "key_kr": "아이들이 도움이 필요해서 메리 포핀스가 도착했어요.",
                       "story_kr": "뱅크스 가족의 아이들은 슬펐어요.\n유모가 자꾸 바뀌었거든요.\n그때 메리 포핀스가 왔어요!\n아이들이 도움이 필요해서 메리 포핀스가 도착했어요.",
                       "story_en": "The Banks children were sad.\nTheir nannies kept changing.\nThen Mary Poppins came!\nMary Poppins arrived because the children needed help.",
                       "vocab": [("children","아이들","👧","\"The children needed help.\""),("needed","필요했다","🆘","\"They needed help.\""),("help","도움","🤝","\"She came to help.\""),("because","왜냐하면","💡","\"Because they needed.\"")],
                       "pick_blank": "She arrived ___ the children needed help.", "pick_ans": "because", "pick_choices": ["because","but","and"],
                       "wo_kr": "\"아이들이 도움이 필요해서 도착했어요.\"를 영어로!", "wo_words": ["Mary","Poppins","arrived","because","the","children","needed","help"], "wo_ans": "Mary Poppins arrived because the children needed help",
                       "listen_text": "Mary Poppins arrived because the children needed help.", "listen_ok": "아이들에게 도움이 필요해서", "listen_no1": "메리가 놀고 싶어서", "listen_no2": "날씨가 좋아서",
                       "dict_word": "because", "dict_hint": "b e c a u s _",
                       "q1": "왜 메리 포핀스가 왔나요?", "q1_ok": "🆘 아이들이 도움이 필요해서", "q1_no1": "🎉 파티 때문에", "q1_no2": "😴 잠을 자려고",
                       "q2": "\"because\"의 뜻은?", "q2_ok": "💡 왜냐하면/~때문에", "q2_no1": "🔄 하지만", "q2_no2": "➕ 그리고",
                       "write_blank": "She arrived ___ the children needed help.", "write_ans": "because", "write_c1": "because", "write_c2": "but", "write_c3": "or",
                       "write_prompt": "\"because\"를 사용해서 문장을 만들어봐!"},
                "d3": {"key_en": "Mary Poppins arrived because the children needed someone truly magical.", "key_kr": "아이들에게 정말 마법 같은 사람이 필요했기에 메리 포핀스가 도착했어요.",
                       "story_kr": "뱅크스 가족의 아이들은 평범한 유모가 아니라\n정말 특별한 사람이 필요했어요.\n그래서 메리 포핀스가 온 거예요!\n아이들에게 정말 마법 같은 사람이 필요했기에 메리 포핀스가 도착했어요.",
                       "story_en": "The Banks children did not need an ordinary nanny.\nThey needed someone truly special.\nThat is why Mary Poppins came!\nMary Poppins arrived because the children needed someone truly magical.",
                       "vocab": [("someone","누군가","👤","\"Someone truly magical.\""),("truly","정말로","✨","\"Truly magical.\""),("magical","마법 같은","🪄","\"Someone magical.\""),("arrived","도착했다","🌬️","\"She arrived.\"")],
                       "pick_blank": "The children needed someone truly ___.", "pick_ans": "magical", "pick_choices": ["magical","boring","angry"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["Mary","Poppins","arrived","because","the","children","needed","someone","truly","magical"], "wo_ans": "Mary Poppins arrived because the children needed someone truly magical",
                       "listen_text": "Mary Poppins arrived because the children needed someone truly magical.", "listen_ok": "마법 같은 사람이 필요해서 왔다", "listen_no1": "아이들이 착해서 왔다", "listen_no2": "날씨가 좋아서 왔다",
                       "dict_word": "magical", "dict_hint": "m a g i c a _",
                       "q1": "아이들에게 어떤 사람이 필요했나요?", "q1_ok": "🪄 정말 마법 같은 사람", "q1_no1": "👨‍🍳 요리사", "q1_no2": "🧹 청소부",
                       "q2": "\"truly\"의 뜻은?", "q2_ok": "✨ 정말로", "q2_no1": "😢 슬프게", "q2_no2": "🏃 빠르게",
                       "write_blank": "The children needed someone ___ magical.", "write_ans": "truly", "write_c1": "truly", "write_c2": "never", "write_c3": "badly",
                       "write_prompt": "Week 13 완료! 마법 같은 경험을 영어로 써봐!"}
            },
            14: {
                "d1": {"key_en": "She was strict but kind.", "key_kr": "그녀는 엄격하지만 다정했어요.",
                       "story_kr": "메리 포핀스는 규칙이 많았어요.\n\"정리정돈은 기본이야!\"\n하지만 아이들에게 항상 따뜻했어요.\n그녀는 엄격하지만 다정했어요.",
                       "story_en": "Mary Poppins had many rules.\n\"Tidiness is important!\"\nBut she was always warm to the children.\nShe was strict but kind.",
                       "vocab": [("strict","엄격한","📏","\"She was strict.\""),("kind","다정한","💕","\"She was kind.\""),("rules","규칙","📋","\"Many rules.\""),("warm","따뜻한","🤗","\"Always warm.\"")],
                       "pick_blank": "She was strict ___ kind.", "pick_ans": "but", "pick_choices": ["but","and","or"],
                       "wo_kr": "\"그녀는 엄격하지만 다정했어요.\"를 영어로!", "wo_words": ["She","was","strict","but","kind"], "wo_ans": "She was strict but kind",
                       "listen_text": "Mary Poppins was strict but kind to the children.", "listen_ok": "엄격하지만 다정했다", "listen_no1": "항상 화났다", "listen_no2": "규칙이 없었다",
                       "dict_word": "strict", "dict_hint": "s t r i c _",
                       "q1": "메리 포핀스는 어떤 성격이었나요?", "q1_ok": "📏 엄격하지만 다정했다", "q1_no1": "😡 무섭기만 했다", "q1_no2": "😴 게으럿다",
                       "q2": "\"strict\"의 뜻은?", "q2_ok": "📏 엄격한", "q2_no1": "😊 재미있는", "q2_no2": "😢 슬픈",
                       "write_blank": "She was ___ but kind.", "write_ans": "strict", "write_c1": "strict", "write_c2": "lazy", "write_c3": "tall",
                       "write_prompt": "엄격하지만 좋은 사람을 영어로 설명해봐!"},
                "d2": {"key_en": "She was strict but kind because she cared.", "key_kr": "그녀는 관심이 있었기에 엄격하지만 다정했어요.",
                       "story_kr": "메리 포핀스가 엄격한 이유가 있었어요.\n아이들을 정말 사랑했거든요.\n사랑하니까 규칙도 만든 거예요.\n그녀는 관심이 있었기에 엄격하지만 다정했어요.",
                       "story_en": "There was a reason Mary Poppins was strict.\nShe truly loved the children.\nBecause she loved them, she made rules.\nShe was strict but kind because she cared.",
                       "vocab": [("cared","관심을 가졌다","❤️","\"She cared.\""),("reason","이유","🤔","\"There was a reason.\""),("loved","사랑했다","💗","\"She loved them.\""),("made","만들었다","🛠️","\"She made rules.\"")],
                       "pick_blank": "She was strict but kind because she ___.", "pick_ans": "cared", "pick_choices": ["cared","slept","ran"],
                       "wo_kr": "\"관심이 있었기에 엄격하지만 다정했어요.\"를 영어로!", "wo_words": ["She","was","strict","but","kind","because","she","cared"], "wo_ans": "She was strict but kind because she cared",
                       "listen_text": "She was strict but kind because she cared about the children.", "listen_ok": "관심이 있어서 엄격하지만 다정했다", "listen_no1": "화가 나서 엄격했다", "listen_no2": "관심이 없어서 떠났다",
                       "dict_word": "cared", "dict_hint": "c a r e _",
                       "q1": "왜 메리 포핀스는 엄격했나요?", "q1_ok": "❤️ 아이들을 사랑해서", "q1_no1": "😡 화가 나서", "q1_no2": "😴 졸려서",
                       "q2": "\"cared\"의 뜻은?", "q2_ok": "❤️ 관심을 가졌다", "q2_no1": "🏃 달렸다", "q2_no2": "😢 울었다",
                       "write_blank": "She was strict because she ___.", "write_ans": "cared", "write_c1": "cared", "write_c2": "forgot", "write_c3": "hated",
                       "write_prompt": "\"because\"로 이유를 설명하는 문장을 써봐!"},
                "d3": {"key_en": "She was strict but kind because rules and love can exist together.", "key_kr": "규칙과 사랑은 함께할 수 있기에 그녀는 엄격하지만 다정했어요.",
                       "story_kr": "메리 포핀스는 가르쳐 줬어요.\n규칙이 있다고 사랑이 없는 게 아니에요.\n규칙과 사랑은 함께할 수 있어요!\n규칙과 사랑은 함께할 수 있기에 그녀는 엄격하지만 다정했어요.",
                       "story_en": "Mary Poppins taught the children something important.\nHaving rules does not mean there is no love.\nRules and love can exist together!\nShe was strict but kind because rules and love can exist together.",
                       "vocab": [("rules","규칙","📋","\"Rules and love.\""),("love","사랑","💕","\"Love can exist.\""),("exist","존재하다","🌟","\"Can exist together.\""),("together","함께","🤝","\"Together.\"")],
                       "pick_blank": "Rules and love can ___ together.", "pick_ans": "exist", "pick_choices": ["exist","fight","sleep"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["She","was","strict","but","kind","because","rules","and","love","can","exist","together"], "wo_ans": "She was strict but kind because rules and love can exist together",
                       "listen_text": "She was strict but kind because rules and love can exist together.", "listen_ok": "규칙과 사랑은 함께할 수 있다", "listen_no1": "규칙은 사랑과 반대다", "listen_no2": "규칙은 필요 없다",
                       "dict_word": "together", "dict_hint": "t o g e t h e _",
                       "q1": "메리 포핀스가 가르친 것은?", "q1_ok": "🤝 규칙과 사랑은 함께할 수 있다", "q1_no1": "😡 규칙이 제일 중요하다", "q1_no2": "🎉 규칙은 필요 없다",
                       "q2": "\"exist\"의 뜻은?", "q2_ok": "🌟 존재하다", "q2_no1": "🏃 달리다", "q2_no2": "😢 울다",
                       "write_blank": "Rules and love can exist ___.", "write_ans": "together", "write_c1": "together", "write_c2": "apart", "write_c3": "never",
                       "write_prompt": "Week 14 완료! 규칙과 사랑에 대해 영어로 써봐!"}
            },
            15: {
                "d1": {"key_en": "The children felt joy.", "key_kr": "아이들은 기쁨을 느꼈어요.",
                       "story_kr": "메리 포핀스와 함께한 날들은 특별했어요.\n천장에서 떠다니고, 그림 속으로 들어갔어요!\n아이들의 마음이 행복으로 가득 찼어요.\n아이들은 기쁨을 느꼈어요.",
                       "story_en": "The days with Mary Poppins were special.\nThey floated on the ceiling and jumped into paintings!\nThe children's hearts were full of happiness.\nThe children felt joy.",
                       "vocab": [("felt","느꼈다","😊","\"They felt joy.\""),("joy","기쁨","🎉","\"Felt joy.\""),("special","특별한","⭐","\"Special days.\""),("happiness","행복","💛","\"Full of happiness.\"")],
                       "pick_blank": "The children ___ joy.", "pick_ans": "felt", "pick_choices": ["felt","lost","broke"],
                       "wo_kr": "\"아이들은 기쁨을 느꼈어요.\"를 영어로!", "wo_words": ["The","children","felt","joy"], "wo_ans": "The children felt joy",
                       "listen_text": "The children felt great joy with Mary Poppins.", "listen_ok": "아이들이 기쁨을 느꼈다", "listen_no1": "아이들이 울었다", "listen_no2": "아이들이 잠들었다",
                       "dict_word": "joy", "dict_hint": "j o _",
                       "q1": "아이들은 무엇을 느꼈나요?", "q1_ok": "🎉 기쁨", "q1_no1": "😢 슬픔", "q1_no2": "😡 화",
                       "q2": "\"felt\"의 뜻은?", "q2_ok": "😊 느꼈다", "q2_no1": "🏃 달렸다", "q2_no2": "😴 잠들었다",
                       "write_blank": "The children felt ___.", "write_ans": "joy", "write_c1": "joy", "write_c2": "anger", "write_c3": "fear",
                       "write_prompt": "기쁨을 느꼈던 경험을 영어로 써봐!"},
                "d2": {"key_en": "The children felt joy because Mary showed them magic.", "key_kr": "메리가 마법을 보여줘서 아이들은 기쁨을 느꼈어요.",
                       "story_kr": "메리 포핀스는 평범한 것에서 마법을 찾았어요.\n약을 먹으면 달콤한 맛이 나고,\n계단 난간을 타면 위로 올라갔어요!\n메리가 마법을 보여줘서 아이들은 기쁨을 느꼈어요.",
                       "story_en": "Mary Poppins found magic in ordinary things.\nMedicine tasted sweet,\nand sliding up the banister was possible!\nThe children felt joy because Mary showed them magic.",
                       "vocab": [("showed","보여줬다","👀","\"She showed them.\""),("magic","마법","🪄","\"Showed them magic.\""),("ordinary","평범한","📦","\"Ordinary things.\""),("possible","가능한","✅","\"It was possible!\"")],
                       "pick_blank": "The children felt joy because Mary ___ them magic.", "pick_ans": "showed", "pick_choices": ["showed","hid","forgot"],
                       "wo_kr": "\"메리가 마법을 보여줘서 기쁨을 느꼈어요.\"를 영어로!", "wo_words": ["The","children","felt","joy","because","Mary","showed","them","magic"], "wo_ans": "The children felt joy because Mary showed them magic",
                       "listen_text": "The children felt joy because Mary showed them magic.", "listen_ok": "마법을 보여줘서 기뻤다", "listen_no1": "마법이 무서웠다", "listen_no2": "마법이 없었다",
                       "dict_word": "showed", "dict_hint": "s h o w e _",
                       "q1": "메리는 아이들에게 무엇을 보여줬나요?", "q1_ok": "🪄 마법", "q1_no1": "📖 책", "q1_no2": "🎵 노래",
                       "q2": "\"ordinary\"의 뜻은?", "q2_ok": "📦 평범한", "q2_no1": "✨ 특별한", "q2_no2": "😡 화난",
                       "write_blank": "Mary ___ them magic.", "write_ans": "showed", "write_c1": "showed", "write_c2": "hid", "write_c3": "sold",
                       "write_prompt": "\"because\"로 기쁜 이유를 영어로 써봐!"},
                "d3": {"key_en": "The children felt joy because Mary showed them magic in ordinary things.", "key_kr": "메리가 평범한 것 속에서 마법을 보여줬기에 아이들은 기쁨을 느꼈어요.",
                       "story_kr": "메리 포핀스의 진짜 마법은\n특별한 주문이 아니었어요.\n평범한 것 속에서 놀라운 것을 찾는 거였어요!\n메리가 평범한 것 속에서 마법을 보여줬기에 아이들은 기쁨을 느꼈어요.",
                       "story_en": "Mary Poppins's real magic\nwas not about special spells.\nIt was about finding wonder in ordinary things!\nThe children felt joy because Mary showed them magic in ordinary things.",
                       "vocab": [("ordinary","평범한","📦","\"Ordinary things.\""),("things","것들","🔮","\"In ordinary things.\""),("wonder","놀라움","🌟","\"Finding wonder.\""),("real","진짜의","💎","\"Real magic.\"")],
                       "pick_blank": "Mary showed them magic in ___ things.", "pick_ans": "ordinary", "pick_choices": ["ordinary","scary","angry"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["The","children","felt","joy","because","Mary","showed","them","magic","in","ordinary","things"], "wo_ans": "The children felt joy because Mary showed them magic in ordinary things",
                       "listen_text": "The children felt joy because Mary showed them magic in ordinary things.", "listen_ok": "평범한 것 속에서 마법을 보여줬다", "listen_no1": "특별한 주문을 외웠다", "listen_no2": "마법은 없었다",
                       "dict_word": "ordinary", "dict_hint": "o r d i n a r _",
                       "q1": "메리의 진짜 마법은?", "q1_ok": "📦 평범한 것에서 놀라움을 찾는 것", "q1_no1": "🪄 주문을 외우는 것", "q1_no2": "✈️ 하늘을 나는 것",
                       "q2": "\"ordinary\"의 뜻은?", "q2_ok": "📦 평범한", "q2_no1": "✨ 마법의", "q2_no2": "😡 화난",
                       "write_blank": "Magic in ___ things.", "write_ans": "ordinary", "write_c1": "ordinary", "write_c2": "terrible", "write_c3": "invisible",
                       "write_prompt": "Week 15 완료! 평범한 것에서 찾은 특별함을 써봐!"}
            },
            16: {
                "d1": {"key_en": "She left because her work was done.", "key_kr": "그녀는 할 일을 마쳤기에 떠났어요.",
                       "story_kr": "어느 날 바람이 바뀌었어요.\n메리 포핀스는 가방을 챙겼어요.\n아이들은 이미 많이 자랐거든요.\n그녀는 할 일을 마쳤기에 떠났어요.",
                       "story_en": "One day the wind changed.\nMary Poppins packed her bag.\nThe children had already grown so much.\nShe left because her work was done.",
                       "vocab": [("left","떠났다","👋","\"She left.\""),("work","일","💼","\"Her work.\""),("done","끝난","✅","\"Work was done.\""),("packed","챙겼다","🧳","\"Packed her bag.\"")],
                       "pick_blank": "She left because her work was ___.", "pick_ans": "done", "pick_choices": ["done","fun","new"],
                       "wo_kr": "\"할 일을 마쳤기에 떠났어요.\"를 영어로!", "wo_words": ["She","left","because","her","work","was","done"], "wo_ans": "She left because her work was done",
                       "listen_text": "She left because her work was done.", "listen_ok": "할 일을 마쳐서 떠났다", "listen_no1": "화가 나서 떠났다", "listen_no2": "아이들이 싫어서 떠났다",
                       "dict_word": "done", "dict_hint": "d o n _",
                       "q1": "왜 메리 포핀스는 떠났나요?", "q1_ok": "✅ 할 일을 마쳐서", "q1_no1": "😡 화가 나서", "q1_no2": "😴 피곤해서",
                       "q2": "\"done\"의 뜻은?", "q2_ok": "✅ 끝난", "q2_no1": "🆕 새로운", "q2_no2": "😊 재미있는",
                       "write_blank": "Her work was ___.", "write_ans": "done", "write_c1": "done", "write_c2": "fun", "write_c3": "lost",
                       "write_prompt": "일을 끝냈을 때의 느낌을 영어로 써봐!"},
                "d2": {"key_en": "She left, but the magic stayed.", "key_kr": "그녀는 떠났지만 마법은 남았어요.",
                       "story_kr": "메리 포핀스가 떠난 후에도\n아이들은 달라졌어요.\n평범한 것에서 마법을 찾을 수 있게 됐거든요.\n그녀는 떠났지만 마법은 남았어요.",
                       "story_en": "Even after Mary Poppins left,\nthe children were different.\nThey could find magic in ordinary things.\nShe left, but the magic stayed.",
                       "vocab": [("stayed","남았다","🏠","\"The magic stayed.\""),("different","달라진","🔄","\"They were different.\""),("even","~조차/~도","➕","\"Even after.\""),("after","~후에","⏰","\"After she left.\"")],
                       "pick_blank": "She left, but the magic ___.", "pick_ans": "stayed", "pick_choices": ["stayed","disappeared","broke"],
                       "wo_kr": "\"떠났지만 마법은 남았어요.\"를 영어로!", "wo_words": ["She","left","but","the","magic","stayed"], "wo_ans": "She left but the magic stayed",
                       "listen_text": "She left, but the magic stayed with the children.", "listen_ok": "떠났지만 마법은 남았다", "listen_no1": "마법도 사라졌다", "listen_no2": "아이들도 떠났다",
                       "dict_word": "stayed", "dict_hint": "s t a y e _",
                       "q1": "메리가 떠난 후 마법은?", "q1_ok": "🏠 남았다", "q1_no1": "💨 사라졌다", "q1_no2": "❌ 처음부터 없었다",
                       "q2": "\"stayed\"의 뜻은?", "q2_ok": "🏠 남았다", "q2_no1": "🏃 달렸다", "q2_no2": "😢 울었다",
                       "write_blank": "The magic ___ with the children.", "write_ans": "stayed", "write_c1": "stayed", "write_c2": "vanished", "write_c3": "exploded",
                       "write_prompt": "\"but\"을 사용해서 대비 문장을 써봐!"},
                "d3": {"key_en": "She left because her work was done — but the magic stayed forever.", "key_kr": "할 일을 마쳤기에 떠났지만 — 마법은 영원히 남았어요.",
                       "story_kr": "메리 포핀스는 영원히 함께할 수 없었어요.\n하지만 그녀가 남긴 것은 영원했어요.\n마법은 아이들의 마음에 영원히 남았어요.\n할 일을 마쳤기에 떠났지만 — 마법은 영원히 남았어요.",
                       "story_en": "Mary Poppins could not stay forever.\nBut what she left behind was eternal.\nThe magic lived forever in the children's hearts.\nShe left because her work was done — but the magic stayed forever.",
                       "vocab": [("forever","영원히","♾️","\"Stayed forever.\""),("hearts","마음","❤️","\"In their hearts.\""),("eternal","영원한","🌟","\"Eternal magic.\""),("behind","뒤에","↩️","\"Left behind.\"")],
                       "pick_blank": "The magic stayed ___.", "pick_ans": "forever", "pick_choices": ["forever","never","sometimes"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["She","left","because","her","work","was","done","but","the","magic","stayed","forever"], "wo_ans": "She left because her work was done but the magic stayed forever",
                       "listen_text": "She left because her work was done, but the magic stayed forever.", "listen_ok": "떠났지만 마법은 영원히 남았다", "listen_no1": "마법도 함께 떠났다", "listen_no2": "일이 끝나지 않았다",
                       "dict_word": "forever", "dict_hint": "f o r e v e _",
                       "q1": "마법은 얼마나 오래 남았나요?", "q1_ok": "♾️ 영원히", "q1_no1": "⏰ 하루만", "q1_no2": "❌ 남지 않았다",
                       "q2": "\"forever\"의 뜻은?", "q2_ok": "♾️ 영원히", "q2_no1": "⏰ 잠깐", "q2_no2": "❌ 절대 안",
                       "write_blank": "The magic stayed ___.", "write_ans": "forever", "write_c1": "forever", "write_c2": "nowhere", "write_c3": "yesterday",
                       "write_prompt": "Week 16 & Mary Poppins 완료! 영원히 기억하고 싶은 것을 써봐!"}
            }
        }
    },
    # G4 Charlotte's Web W17-W20
    "g4_charlotte": {
        "grade": 4, "quarter": "Q2", "book": "Charlotte's Web",
        "book_kr": "샬롯의 거미줄", "emoji": "🕷️",
        "img": f"{R2}/images/charlottes-web/w17_new.png",
        "ratio": "영어 50% / 한국어 50%", "level": "B1",
        "weeks": {
            17: {
                "d1": {"key_en": "Wilbur was saved.", "key_kr": "윌버는 구해졌어요.",
                       "story_kr": "아기 돼지 윌버는 위험했어요.\n농부가 윌버를 없애려고 했거든요.\n하지만 누군가가 윌버를 구했어요!\n윌버는 구해졌어요.",
                       "story_en": "Baby pig Wilbur was in danger.\nThe farmer wanted to get rid of Wilbur.\nBut someone saved Wilbur!\nWilbur was saved.",
                       "vocab": [("saved","구해졌다","🆘","\"Wilbur was saved.\""),("danger","위험","⚠️","\"In danger.\""),("farmer","농부","👨‍🌾","\"The farmer.\""),("pig","돼지","🐷","\"Baby pig.\"")],
                       "pick_blank": "Wilbur was ___.", "pick_ans": "saved", "pick_choices": ["saved","lost","angry"],
                       "wo_kr": "\"윌버는 구해졌어요.\"를 영어로!", "wo_words": ["Wilbur","was","saved"], "wo_ans": "Wilbur was saved",
                       "listen_text": "Wilbur the pig was saved from danger.", "listen_ok": "윌버가 구해졌다", "listen_no1": "윌버가 도망갔다", "listen_no2": "윌버가 잠들었다",
                       "dict_word": "saved", "dict_hint": "s a v e _",
                       "q1": "윌버에게 무슨 일이 있었나요?", "q1_ok": "🆘 구해졌다", "q1_no1": "😴 잠들었다", "q1_no2": "🏃 도망갔다",
                       "q2": "\"saved\"의 뜻은?", "q2_ok": "🆘 구해졌다", "q2_no1": "😡 화났다", "q2_no2": "😴 졸렸다",
                       "write_blank": "Wilbur was ___.", "write_ans": "saved", "write_c1": "saved", "write_c2": "hungry", "write_c3": "cold",
                       "write_prompt": "누군가를 도와준 경험을 영어로 써봐!"},
                "d2": {"key_en": "Wilbur was saved because Charlotte believed in him.", "key_kr": "샬롯이 윌버를 믿었기에 윌버는 구해졌어요.",
                       "story_kr": "거미 샬롯은 윌버의 친구였어요.\n샬롯은 윌버가 특별하다고 믿었어요.\n거미줄에 글자를 써서 윌버를 구했어요!\n샬롯이 윌버를 믿었기에 윌버는 구해졌어요.",
                       "story_en": "Charlotte the spider was Wilbur's friend.\nCharlotte believed Wilbur was special.\nShe wrote words in her web to save him!\nWilbur was saved because Charlotte believed in him.",
                       "vocab": [("believed","믿었다","🌟","\"Charlotte believed.\""),("spider","거미","🕷️","\"Charlotte the spider.\""),("web","거미줄","🕸️","\"In her web.\""),("wrote","썼다","✍️","\"She wrote words.\"")],
                       "pick_blank": "Wilbur was saved because Charlotte ___ in him.", "pick_ans": "believed", "pick_choices": ["believed","laughed","forgot"],
                       "wo_kr": "\"샬롯이 믿었기에 구해졌어요.\"를 영어로!", "wo_words": ["Wilbur","was","saved","because","Charlotte","believed","in","him"], "wo_ans": "Wilbur was saved because Charlotte believed in him",
                       "listen_text": "Wilbur was saved because Charlotte believed in him.", "listen_ok": "샬롯이 믿어서 구해졌다", "listen_no1": "농부가 구해줬다", "listen_no2": "혼자서 도망갔다",
                       "dict_word": "believed", "dict_hint": "b e l i e v e _",
                       "q1": "누가 윌버를 구했나요?", "q1_ok": "🕷️ 거미 샬롯", "q1_no1": "👨‍🌾 농부", "q1_no2": "🐷 다른 돼지",
                       "q2": "\"believed\"의 뜻은?", "q2_ok": "🌟 믿었다", "q2_no1": "🏃 달렸다", "q2_no2": "😢 울었다",
                       "write_blank": "Charlotte ___ in him.", "write_ans": "believed", "write_c1": "believed", "write_c2": "laughed", "write_c3": "slept",
                       "write_prompt": "\"because\"로 이유를 설명하는 문장을 써봐!"},
                "d3": {"key_en": "Wilbur was saved because Charlotte believed one small life was worth fighting for.", "key_kr": "샬롯은 작은 생명 하나도 지킬 가치가 있다고 믿었기에 윌버는 구해졌어요.",
                       "story_kr": "샬롯은 윌버가 작은 돼지라도\n그 생명은 소중하다고 생각했어요.\n지킬 가치가 있다고 믿었어요!\n샬롯은 작은 생명 하나도 지킬 가치가 있다고 믿었기에 윌버는 구해졌어요.",
                       "story_en": "Charlotte thought that even though Wilbur was a small pig,\nhis life was precious.\nShe believed it was worth fighting for!\nWilbur was saved because Charlotte believed one small life was worth fighting for.",
                       "vocab": [("life","생명","💗","\"One small life.\""),("worth","가치가 있는","💎","\"Worth fighting for.\""),("fighting","싸우는/지키는","💪","\"Fighting for.\""),("small","작은","🐷","\"One small life.\"")],
                       "pick_blank": "One small life was ___ fighting for.", "pick_ans": "worth", "pick_choices": ["worth","not","always"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["Wilbur","was","saved","because","Charlotte","believed","one","small","life","was","worth","fighting","for"], "wo_ans": "Wilbur was saved because Charlotte believed one small life was worth fighting for",
                       "listen_text": "Wilbur was saved because Charlotte believed one small life was worth fighting for.", "listen_ok": "작은 생명도 지킬 가치가 있다", "listen_no1": "큰 동물만 중요하다", "listen_no2": "싸우면 안 된다",
                       "dict_word": "worth", "dict_hint": "w o r t _",
                       "q1": "샬롯은 무엇을 믿었나요?", "q1_ok": "💎 작은 생명도 지킬 가치가 있다", "q1_no1": "😡 돼지는 쓸모없다", "q1_no2": "😴 잠이 최고다",
                       "q2": "\"worth\"의 뜻은?", "q2_ok": "💎 가치가 있는", "q2_no1": "😢 슬픈", "q2_no2": "😡 화난",
                       "write_blank": "One small life was ___ fighting for.", "write_ans": "worth", "write_c1": "worth", "write_c2": "never", "write_c3": "hardly",
                       "write_prompt": "Week 17 완료! 소중한 것을 지키는 것에 대해 써봐!"}
            },
            18: {
                "d1": {"key_en": "Charlotte worked quietly.", "key_kr": "샬롯은 조용히 일했어요.",
                       "story_kr": "밤이 되면 샬롯은 거미줄을 짰어요.\n아무도 모르게 조용히 일했어요.\n윌버를 위해 열심히 준비했어요.\n샬롯은 조용히 일했어요.",
                       "story_en": "At night, Charlotte wove her web.\nShe worked quietly when no one was watching.\nShe prepared hard for Wilbur.\nCharlotte worked quietly.",
                       "vocab": [("worked","일했다","💪","\"She worked.\""),("quietly","조용히","🤫","\"Worked quietly.\""),("night","밤","🌙","\"At night.\""),("wove","짰다","🕸️","\"Wove her web.\"")],
                       "pick_blank": "Charlotte worked ___.", "pick_ans": "quietly", "pick_choices": ["quietly","loudly","angrily"],
                       "wo_kr": "\"샬롯은 조용히 일했어요.\"를 영어로!", "wo_words": ["Charlotte","worked","quietly"], "wo_ans": "Charlotte worked quietly",
                       "listen_text": "Charlotte worked quietly through the night.", "listen_ok": "샬롯이 조용히 일했다", "listen_no1": "샬롯이 크게 소리쳤다", "listen_no2": "샬롯이 잠들었다",
                       "dict_word": "quietly", "dict_hint": "q u i e t l _",
                       "q1": "샬롯은 어떻게 일했나요?", "q1_ok": "🤫 조용히", "q1_no1": "📢 시끄럽게", "q1_no2": "😴 잠자면서",
                       "q2": "\"quietly\"의 뜻은?", "q2_ok": "🤫 조용히", "q2_no1": "📢 시끄럽게", "q2_no2": "🏃 빠르게",
                       "write_blank": "Charlotte worked ___.", "write_ans": "quietly", "write_c1": "quietly", "write_c2": "loudly", "write_c3": "never",
                       "write_prompt": "조용히 노력한 경험을 영어로 써봐!"},
                "d2": {"key_en": "Charlotte worked quietly because she loved Wilbur.", "key_kr": "윌버를 사랑했기에 샬롯은 조용히 일했어요.",
                       "story_kr": "샬롯은 보상을 바라지 않았어요.\n윌버를 진심으로 사랑했거든요.\n사랑하니까 밤새 조용히 일한 거예요.\n윌버를 사랑했기에 샬롯은 조용히 일했어요.",
                       "story_en": "Charlotte did not want any reward.\nShe truly loved Wilbur.\nBecause of love, she worked all night quietly.\nCharlotte worked quietly because she loved Wilbur.",
                       "vocab": [("loved","사랑했다","❤️","\"She loved Wilbur.\""),("reward","보상","🏆","\"No reward.\""),("truly","진심으로","💕","\"Truly loved.\""),("all night","밤새","🌙","\"Worked all night.\"")],
                       "pick_blank": "She worked quietly because she ___ Wilbur.", "pick_ans": "loved", "pick_choices": ["loved","forgot","hated"],
                       "wo_kr": "\"사랑했기에 조용히 일했어요.\"를 영어로!", "wo_words": ["Charlotte","worked","quietly","because","she","loved","Wilbur"], "wo_ans": "Charlotte worked quietly because she loved Wilbur",
                       "listen_text": "Charlotte worked quietly because she loved Wilbur.", "listen_ok": "윌버를 사랑해서 조용히 일했다", "listen_no1": "보상을 원해서 일했다", "listen_no2": "잠이 안 와서 일했다",
                       "dict_word": "loved", "dict_hint": "l o v e _",
                       "q1": "샬롯은 왜 밤새 일했나요?", "q1_ok": "❤️ 윌버를 사랑해서", "q1_no1": "🏆 보상을 원해서", "q1_no2": "😴 잠이 안 와서",
                       "q2": "\"reward\"의 뜻은?", "q2_ok": "🏆 보상", "q2_no1": "😢 벌", "q2_no2": "🎵 노래",
                       "write_blank": "She worked because she ___ Wilbur.", "write_ans": "loved", "write_c1": "loved", "write_c2": "feared", "write_c3": "ignored",
                       "write_prompt": "사랑하는 사람을 위해 한 일을 영어로 써봐!"},
                "d3": {"key_en": "Charlotte worked quietly because she loved Wilbur more than he ever knew.", "key_kr": "윌버가 알지 못할 만큼 사랑했기에 샬롯은 조용히 일했어요.",
                       "story_kr": "샬롯의 사랑은 윌버의 상상 이상이었어요.\n윌버가 알지 못할 정도로 깊었어요.\n그래서 조용히, 헌신적으로 일한 거예요.\n윌버가 알지 못할 만큼 사랑했기에 샬롯은 조용히 일했어요.",
                       "story_en": "Charlotte's love was beyond Wilbur's imagination.\nIt was deeper than he ever knew.\nThat is why she worked so quietly and devotedly.\nCharlotte worked quietly because she loved Wilbur more than he ever knew.",
                       "vocab": [("more","더","➕","\"More than he knew.\""),("ever","여태껏","⏳","\"He ever knew.\""),("knew","알았다","🧠","\"He ever knew.\""),("deeply","깊이","💗","\"Loved deeply.\"")],
                       "pick_blank": "She loved Wilbur more than he ___ knew.", "pick_ans": "ever", "pick_choices": ["ever","never","always"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["Charlotte","worked","quietly","because","she","loved","Wilbur","more","than","he","ever","knew"], "wo_ans": "Charlotte worked quietly because she loved Wilbur more than he ever knew",
                       "listen_text": "Charlotte worked quietly because she loved Wilbur more than he ever knew.", "listen_ok": "윌버가 모를 만큼 사랑해서 조용히 일했다", "listen_no1": "윌버가 시켜서 일했다", "listen_no2": "샬롯은 일을 싫어했다",
                       "dict_word": "knew", "dict_hint": "k n e _",
                       "q1": "샬롯의 사랑은 어느 정도였나요?", "q1_ok": "💗 윌버가 모를 만큼 깊었다", "q1_no1": "😐 보통이었다", "q1_no2": "❌ 사랑하지 않았다",
                       "q2": "\"ever\"의 뜻은?", "q2_ok": "⏳ 여태껏", "q2_no1": "❌ 절대 안", "q2_no2": "🔄 항상",
                       "write_blank": "More than he ___ knew.", "write_ans": "ever", "write_c1": "ever", "write_c2": "never", "write_c3": "still",
                       "write_prompt": "Week 18 완료! 조용한 사랑에 대해 영어로 써봐!"}
            },
            19: {
                "d1": {"key_en": "Wilbur cried because Charlotte was gone.", "key_kr": "샬롯이 떠나서 윌버는 울었어요.",
                       "story_kr": "박람회가 끝난 후,\n샬롯은 더 이상 움직이지 않았어요.\n윌버는 친구를 잃었다는 걸 알았어요.\n샬롯이 떠나서 윌버는 울었어요.",
                       "story_en": "After the fair ended,\nCharlotte could no longer move.\nWilbur knew he had lost his friend.\nWilbur cried because Charlotte was gone.",
                       "vocab": [("cried","울었다","😢","\"Wilbur cried.\""),("gone","떠난/사라진","💔","\"Charlotte was gone.\""),("fair","박람회","🎪","\"The fair ended.\""),("lost","잃었다","😞","\"Lost his friend.\"")],
                       "pick_blank": "Wilbur cried because Charlotte was ___.", "pick_ans": "gone", "pick_choices": ["gone","happy","sleeping"],
                       "wo_kr": "\"샬롯이 떠나서 울었어요.\"를 영어로!", "wo_words": ["Wilbur","cried","because","Charlotte","was","gone"], "wo_ans": "Wilbur cried because Charlotte was gone",
                       "listen_text": "Wilbur cried because Charlotte was gone.", "listen_ok": "샬롯이 떠나서 울었다", "listen_no1": "기뻐서 울었다", "listen_no2": "배고파서 울었다",
                       "dict_word": "gone", "dict_hint": "g o n _",
                       "q1": "윌버는 왜 울었나요?", "q1_ok": "💔 샬롯이 떠나서", "q1_no1": "🎉 기뻐서", "q1_no2": "😡 화나서",
                       "q2": "\"gone\"의 뜻은?", "q2_ok": "💔 떠난/사라진", "q2_no1": "😊 행복한", "q2_no2": "😴 졸린",
                       "write_blank": "Charlotte was ___.", "write_ans": "gone", "write_c1": "gone", "write_c2": "here", "write_c3": "hungry",
                       "write_prompt": "슬펐던 이별 경험을 영어로 써봐!"},
                "d2": {"key_en": "Wilbur cried, but Charlotte's gift stayed.", "key_kr": "윌버는 울었지만, 샬롯의 선물은 남았어요.",
                       "story_kr": "윌버는 슬펐지만 희망이 있었어요.\n샬롯이 남긴 알주머니가 있었거든요!\n새로운 생명이 태어날 거예요.\n윌버는 울었지만, 샬롯의 선물은 남았어요.",
                       "story_en": "Wilbur was sad, but there was hope.\nCharlotte had left behind her egg sac!\nNew life would be born.\nWilbur cried, but Charlotte's gift stayed.",
                       "vocab": [("gift","선물","🎁","\"Charlotte's gift.\""),("hope","희망","🌈","\"There was hope.\""),("egg sac","알주머니","🥚","\"Her egg sac.\""),("born","태어난","👶","\"Would be born.\"")],
                       "pick_blank": "Wilbur cried, but Charlotte's ___ stayed.", "pick_ans": "gift", "pick_choices": ["gift","web","voice"],
                       "wo_kr": "\"울었지만 선물은 남았어요.\"를 영어로!", "wo_words": ["Wilbur","cried","but","Charlotte's","gift","stayed"], "wo_ans": "Wilbur cried but Charlotte's gift stayed",
                       "listen_text": "Wilbur cried, but Charlotte's gift stayed with him.", "listen_ok": "울었지만 선물은 남았다", "listen_no1": "모든 것이 사라졌다", "listen_no2": "윌버가 선물을 버렸다",
                       "dict_word": "gift", "dict_hint": "g i f _",
                       "q1": "샬롯이 남긴 것은?", "q1_ok": "🥚 알주머니(선물)", "q1_no1": "📖 책", "q1_no2": "🎵 노래",
                       "q2": "\"gift\"의 뜻은?", "q2_ok": "🎁 선물", "q2_no1": "😢 눈물", "q2_no2": "🕸️ 거미줄",
                       "write_blank": "Charlotte's ___ stayed.", "write_ans": "gift", "write_c1": "gift", "write_c2": "anger", "write_c3": "shadow",
                       "write_prompt": "\"but\"을 사용해서 대비 문장을 써봐!"},
                "d3": {"key_en": "Wilbur cried because Charlotte was gone — but her words and gift stayed with him.", "key_kr": "샬롯이 떠나서 윌버는 울었지만 — 그녀의 말과 선물은 함께 남았어요.",
                       "story_kr": "샬롯은 떠났지만\n거미줄에 쓴 말들은 윌버의 마음에 남았어요.\n그리고 알주머니에서 새 생명이 태어났어요!\n샬롯이 떠나서 윌버는 울었지만 — 그녀의 말과 선물은 함께 남았어요.",
                       "story_en": "Charlotte was gone,\nbut the words she wrote in her web stayed in Wilbur's heart.\nAnd new life was born from her egg sac!\nWilbur cried because Charlotte was gone — but her words and gift stayed with him.",
                       "vocab": [("words","말/단어","💬","\"Her words stayed.\""),("heart","마음","❤️","\"In his heart.\""),("stayed","남았다","🏠","\"Stayed with him.\""),("new","새로운","🌱","\"New life.\"")],
                       "pick_blank": "Her words and gift ___ with him.", "pick_ans": "stayed", "pick_choices": ["stayed","disappeared","broke"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["Wilbur","cried","because","Charlotte","was","gone","but","her","words","and","gift","stayed","with","him"], "wo_ans": "Wilbur cried because Charlotte was gone but her words and gift stayed with him",
                       "listen_text": "Wilbur cried because Charlotte was gone, but her words and gift stayed with him.", "listen_ok": "울었지만 말과 선물은 남았다", "listen_no1": "모든 것이 사라졌다", "listen_no2": "윌버가 잊었다",
                       "dict_word": "words", "dict_hint": "w o r d _",
                       "q1": "샬롯이 남긴 것은?", "q1_ok": "💬 말과 선물(알주머니)", "q1_no1": "💰 돈", "q1_no2": "❌ 아무것도 없다",
                       "q2": "\"stayed\"의 뜻은?", "q2_ok": "🏠 남았다", "q2_no1": "🏃 달렸다", "q2_no2": "💨 사라졌다",
                       "write_blank": "Her words ___ with him.", "write_ans": "stayed", "write_c1": "stayed", "write_c2": "vanished", "write_c3": "fought",
                       "write_prompt": "Week 19 완료! 소중한 기억에 대해 영어로 써봐!"}
            },
            20: {
                "d1": {"key_en": "True friendship means giving.", "key_kr": "진정한 우정은 주는 거예요.",
                       "story_kr": "샬롯은 윌버에게 모든 것을 줬어요.\n시간, 재능, 그리고 사랑을요.\n아무것도 돌려받지 않았어요.\n진정한 우정은 주는 거예요.",
                       "story_en": "Charlotte gave everything to Wilbur.\nHer time, talent, and love.\nShe never asked for anything back.\nTrue friendship means giving.",
                       "vocab": [("true","진정한","💎","\"True friendship.\""),("friendship","우정","🤝","\"True friendship.\""),("means","의미하다","📖","\"Friendship means.\""),("giving","주는 것","🎁","\"Means giving.\"")],
                       "pick_blank": "True friendship ___ giving.", "pick_ans": "means", "pick_choices": ["means","stops","breaks"],
                       "wo_kr": "\"진정한 우정은 주는 거예요.\"를 영어로!", "wo_words": ["True","friendship","means","giving"], "wo_ans": "True friendship means giving",
                       "listen_text": "True friendship means giving without expecting anything back.", "listen_ok": "진정한 우정은 주는 것이다", "listen_no1": "우정은 받는 것이다", "listen_no2": "우정은 필요 없다",
                       "dict_word": "friendship", "dict_hint": "f r i e n d s h i _",
                       "q1": "진정한 우정의 의미는?", "q1_ok": "🎁 주는 것", "q1_no1": "💰 받는 것", "q1_no2": "😴 쉬는 것",
                       "q2": "\"means\"의 뜻은?", "q2_ok": "📖 의미하다", "q2_no1": "🏃 달리다", "q2_no2": "😢 울다",
                       "write_blank": "True friendship ___ giving.", "write_ans": "means", "write_c1": "means", "write_c2": "hates", "write_c3": "fears",
                       "write_prompt": "진정한 우정에 대해 영어로 써봐!"},
                "d2": {"key_en": "True friendship means giving without asking.", "key_kr": "진정한 우정은 바라지 않고 주는 거예요.",
                       "story_kr": "샬롯은 한 번도 \"고마워\" 해달라고 안 했어요.\n돌려받을 것을 바라지 않았어요.\n그냥 주었어요.\n진정한 우정은 바라지 않고 주는 거예요.",
                       "story_en": "Charlotte never asked for a \"thank you.\"\nShe never expected anything in return.\nShe just gave.\nTrue friendship means giving without asking.",
                       "vocab": [("without","~없이","🚫","\"Without asking.\""),("asking","요구하는","🙋","\"Without asking.\""),("expected","기대했다","🤞","\"Never expected.\""),("return","보답","↩️","\"In return.\"")],
                       "pick_blank": "True friendship means giving ___ asking.", "pick_ans": "without", "pick_choices": ["without","with","for"],
                       "wo_kr": "\"바라지 않고 주는 것\"을 영어로!", "wo_words": ["True","friendship","means","giving","without","asking"], "wo_ans": "True friendship means giving without asking",
                       "listen_text": "True friendship means giving without asking for anything.", "listen_ok": "바라지 않고 주는 것이 우정이다", "listen_no1": "항상 대가를 바라야 한다", "listen_no2": "친구는 필요 없다",
                       "dict_word": "without", "dict_hint": "w i t h o u _",
                       "q1": "샬롯은 보답을 바랐나요?", "q1_ok": "🚫 아니요, 바라지 않았어요", "q1_no1": "💰 네, 돈을 원했어요", "q1_no2": "🎁 네, 선물을 원했어요",
                       "q2": "\"without\"의 뜻은?", "q2_ok": "🚫 ~없이", "q2_no1": "➕ ~와 함께", "q2_no2": "🔄 ~때문에",
                       "write_blank": "Giving ___ asking.", "write_ans": "without", "write_c1": "without", "write_c2": "with", "write_c3": "before",
                       "write_prompt": "바라지 않고 준 경험을 영어로 써봐!"},
                "d3": {"key_en": "True friendship means giving without asking — Charlotte showed this with her life.", "key_kr": "진정한 우정은 바라지 않고 주는 것 — 샬롯은 자신의 삶으로 이를 보여줬어요.",
                       "story_kr": "샬롯의 이야기는 끝났지만\n그 교훈은 영원해요.\n진짜 친구는 대가 없이 줘요.\n진정한 우정은 바라지 않고 주는 것 — 샬롯은 자신의 삶으로 이를 보여줬어요.",
                       "story_en": "Charlotte's story ended,\nbut her lesson lives forever.\nA true friend gives without expecting anything.\nTrue friendship means giving without asking — Charlotte showed this with her life.",
                       "vocab": [("showed","보여줬다","👀","\"Charlotte showed this.\""),("life","삶/생명","💗","\"With her life.\""),("lesson","교훈","📚","\"Her lesson.\""),("forever","영원히","♾️","\"Lives forever.\"")],
                       "pick_blank": "Charlotte showed this with her ___.", "pick_ans": "life", "pick_choices": ["life","web","name"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["True","friendship","means","giving","without","asking","Charlotte","showed","this","with","her","life"], "wo_ans": "True friendship means giving without asking Charlotte showed this with her life",
                       "listen_text": "True friendship means giving without asking. Charlotte showed this with her life.", "listen_ok": "바라지 않고 주는 것을 삶으로 보여줬다", "listen_no1": "우정은 받는 것이다", "listen_no2": "샬롯은 이기적이었다",
                       "dict_word": "showed", "dict_hint": "s h o w e _",
                       "q1": "샬롯은 무엇을 보여줬나요?", "q1_ok": "💗 진정한 우정을 삶으로", "q1_no1": "💰 부자가 되는 법을", "q1_no2": "🏃 달리는 법을",
                       "q2": "\"life\"의 뜻은?", "q2_ok": "💗 삶/생명", "q2_no1": "📖 책", "q2_no2": "🎵 노래",
                       "write_blank": "Charlotte showed this with her ___.", "write_ans": "life", "write_c1": "life", "write_c2": "money", "write_c3": "anger",
                       "write_prompt": "Week 20 & Charlotte's Web 완료! 진정한 친구에 대해 써봐!"}
            }
        }
    },
    # G5 Swiss Family Robinson W33-W36
    "g5_swiss": {
        "grade": 5, "quarter": "Q4", "book": "Swiss Family Robinson",
        "book_kr": "스위스 가족 로빈슨", "emoji": "🏝️",
        "img": f"{R2}/images/swiss-family/w33_new.png",
        "ratio": "영어 60% / 한국어 40%", "level": "B1+",
        "weeks": {
            33: {
                "d1": {"key_en": "The family worked together for survival.", "key_kr": "가족은 생존을 위해 함께 일했어요.",
                       "story_kr": "폭풍으로 배가 난파됐어요.\n무인도에 도착한 가족은 살아남아야 했어요.\n모두 힘을 합쳐 일했어요.\n가족은 생존을 위해 함께 일했어요.",
                       "story_en": "A terrible storm wrecked their ship.\nThe family arrived on a deserted island and had to survive.\nEveryone worked hard together.\nThe family worked together for survival.",
                       "vocab": [("survival","생존","🏝️","\"Worked for survival.\""),("together","함께","🤝","\"Worked together.\""),("storm","폭풍","🌊","\"A terrible storm.\""),("island","섬","🏝️","\"A deserted island.\"")],
                       "pick_blank": "The family worked together for ___.", "pick_ans": "survival", "pick_choices": ["survival","fun","rest"],
                       "wo_kr": "\"가족은 생존을 위해 함께 일했어요.\"를 영어로!", "wo_words": ["The","family","worked","together","for","survival"], "wo_ans": "The family worked together for survival",
                       "listen_text": "The family worked together for survival on the island.", "listen_ok": "생존을 위해 함께 일했다", "listen_no1": "놀기 위해 모였다", "listen_no2": "혼자서 생존했다",
                       "dict_word": "survival", "dict_hint": "s u r v i v a _",
                       "q1": "가족은 왜 함께 일했나요?", "q1_ok": "🏝️ 생존을 위해", "q1_no1": "🎉 파티를 위해", "q1_no2": "😴 쉬기 위해",
                       "q2": "\"survival\"의 뜻은?", "q2_ok": "🏝️ 생존", "q2_no1": "🎉 축제", "q2_no2": "😴 휴식",
                       "write_blank": "The family worked for ___.", "write_ans": "survival", "write_c1": "survival", "write_c2": "vacation", "write_c3": "nothing",
                       "write_prompt": "팀워크가 중요했던 경험을 영어로 써봐!"},
                "d2": {"key_en": "The family worked together because survival needed everyone's effort.", "key_kr": "생존에는 모두의 노력이 필요했기에 가족은 함께 일했어요.",
                       "story_kr": "아버지 혼자서는 불가능했어요.\n어머니, 형제들 모두가 각자 역할을 했어요.\n물 찾기, 집 짓기, 음식 구하기!\n생존에는 모두의 노력이 필요했기에 가족은 함께 일했어요.",
                       "story_en": "Father alone could not do it all.\nMother and all the brothers had their own roles.\nFinding water, building shelter, gathering food!\nThe family worked together because survival needed everyone's effort.",
                       "vocab": [("effort","노력","💪","\"Everyone's effort.\""),("everyone","모두","👨‍👩‍👧‍👦","\"Everyone's effort.\""),("roles","역할","🎭","\"Their own roles.\""),("shelter","대피소","🏠","\"Building shelter.\"")],
                       "pick_blank": "Survival needed everyone's ___.", "pick_ans": "effort", "pick_choices": ["effort","sleep","money"],
                       "wo_kr": "\"모두의 노력이 필요했기에 함께 일했어요.\"를 영어로!", "wo_words": ["The","family","worked","together","because","survival","needed","everyone's","effort"], "wo_ans": "The family worked together because survival needed everyone's effort",
                       "listen_text": "The family worked together because survival needed everyone's effort.", "listen_ok": "모두의 노력이 필요해서 함께 일했다", "listen_no1": "혼자서도 충분했다", "listen_no2": "아무도 일하지 않았다",
                       "dict_word": "effort", "dict_hint": "e f f o r _",
                       "q1": "생존에 왜 모두가 필요했나요?", "q1_ok": "💪 각자 역할이 있었기에", "q1_no1": "😴 다들 잠만 자서", "q1_no2": "🎉 놀기 위해서",
                       "q2": "\"effort\"의 뜻은?", "q2_ok": "💪 노력", "q2_no1": "😴 휴식", "q2_no2": "🎉 축제",
                       "write_blank": "Survival needed everyone's ___.", "write_ans": "effort", "write_c1": "effort", "write_c2": "silence", "write_c3": "anger",
                       "write_prompt": "모두의 노력이 필요했던 경험을 영어로 써봐!"},
                "d3": {"key_en": "The family worked together because survival in the wild needed every member's effort.", "key_kr": "야생에서의 생존은 모든 구성원의 노력이 필요했기에 가족은 함께 일했어요.",
                       "story_kr": "야생에서는 혼자 살 수 없어요.\n모든 가족 구성원이 중요한 역할을 했어요.\n아버지는 건설, 어머니는 요리, 아이들은 탐험!\n야생에서의 생존은 모든 구성원의 노력이 필요했기에 가족은 함께 일했어요.",
                       "story_en": "In the wild, no one can survive alone.\nEvery family member played an important role.\nFather built, Mother cooked, the children explored!\nThe family worked together because survival in the wild needed every member's effort.",
                       "vocab": [("wild","야생","🌿","\"In the wild.\""),("member","구성원","👤","\"Every member.\""),("played","했다","🎭","\"Played a role.\""),("important","중요한","⭐","\"An important role.\"")],
                       "pick_blank": "Survival in the ___ needed every member's effort.", "pick_ans": "wild", "pick_choices": ["wild","city","school"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["The","family","worked","together","because","survival","in","the","wild","needed","every","member's","effort"], "wo_ans": "The family worked together because survival in the wild needed every member's effort",
                       "listen_text": "The family worked together because survival in the wild needed every member's effort.", "listen_ok": "야생 생존에 모든 구성원의 노력이 필요했다", "listen_no1": "야생은 쉬웠다", "listen_no2": "한 명만 일했다",
                       "dict_word": "wild", "dict_hint": "w i l _",
                       "q1": "야생에서의 생존에 무엇이 필요했나요?", "q1_ok": "💪 모든 구성원의 노력", "q1_no1": "💰 돈", "q1_no2": "📱 핸드폰",
                       "q2": "\"member\"의 뜻은?", "q2_ok": "👤 구성원", "q2_no1": "🎵 노래", "q2_no2": "📖 책",
                       "write_blank": "Survival in the ___ needed effort.", "write_ans": "wild", "write_c1": "wild", "write_c2": "park", "write_c3": "mall",
                       "write_prompt": "Week 33 완료! 팀워크의 중요성에 대해 써봐!"}
            },
            34: {
                "d1": {"key_en": "They built a new life from nothing.", "key_kr": "그들은 아무것도 없는 곳에서 새 삶을 만들었어요.",
                       "story_kr": "난파선에서 건진 도구들로\n집을 짓고, 밭을 만들고, 울타리를 세웠어요.\n진짜 아무것도 없는 곳에서 시작했어요.\n그들은 아무것도 없는 곳에서 새 삶을 만들었어요.",
                       "story_en": "With tools saved from the shipwreck,\nthey built a house, created a garden, and made fences.\nThey started from absolutely nothing.\nThey built a new life from nothing.",
                       "vocab": [("built","지었다","🏗️","\"They built a house.\""),("nothing","아무것도 없음","0️⃣","\"From nothing.\""),("new","새로운","🌱","\"A new life.\""),("tools","도구","🔧","\"Tools from the ship.\"")],
                       "pick_blank": "They built a new life from ___.", "pick_ans": "nothing", "pick_choices": ["nothing","money","magic"],
                       "wo_kr": "\"아무것도 없는 곳에서 새 삶을 만들었어요.\"를 영어로!", "wo_words": ["They","built","a","new","life","from","nothing"], "wo_ans": "They built a new life from nothing",
                       "listen_text": "They built a new life from nothing on the island.", "listen_ok": "아무것도 없는 곳에서 새 삶을 만들었다", "listen_no1": "도시에서 편하게 살았다", "listen_no2": "아무것도 하지 않았다",
                       "dict_word": "built", "dict_hint": "b u i l _",
                       "q1": "가족은 무엇에서 시작했나요?", "q1_ok": "0️⃣ 아무것도 없는 곳에서", "q1_no1": "🏠 멋진 집에서", "q1_no2": "🏫 학교에서",
                       "q2": "\"built\"의 뜻은?", "q2_ok": "🏗️ 지었다", "q2_no1": "💔 부쉈다", "q2_no2": "😴 잤다",
                       "write_blank": "They ___ a new life.", "write_ans": "built", "write_c1": "built", "write_c2": "broke", "write_c3": "lost",
                       "write_prompt": "새로 시작한 경험을 영어로 써봐!"},
                "d2": {"key_en": "Necessity became their greatest teacher.", "key_kr": "필요가 그들의 가장 위대한 선생님이 되었어요.",
                       "story_kr": "가족은 학교 없이도 많이 배웠어요.\n물이 필요하니 우물을 파고,\n비가 오니 지붕을 만들었어요.\n필요가 그들의 가장 위대한 선생님이 되었어요.",
                       "story_en": "The family learned so much without any school.\nThey needed water, so they dug a well.\nIt rained, so they made a roof.\nNecessity became their greatest teacher.",
                       "vocab": [("necessity","필요","📌","\"Necessity became.\""),("greatest","가장 위대한","🏆","\"Greatest teacher.\""),("teacher","선생님","👨‍🏫","\"Their teacher.\""),("learned","배웠다","📚","\"They learned.\"")],
                       "pick_blank": "Necessity became their ___ teacher.", "pick_ans": "greatest", "pick_choices": ["greatest","worst","laziest"],
                       "wo_kr": "\"필요가 가장 위대한 선생님이 되었어요.\"를 영어로!", "wo_words": ["Necessity","became","their","greatest","teacher"], "wo_ans": "Necessity became their greatest teacher",
                       "listen_text": "Necessity became their greatest teacher on the island.", "listen_ok": "필요가 최고의 선생님이 되었다", "listen_no1": "학교에서 배웠다", "listen_no2": "아무것도 배우지 않았다",
                       "dict_word": "necessity", "dict_hint": "n e c e s s i t _",
                       "q1": "가족의 가장 위대한 선생님은?", "q1_ok": "📌 필요(necessity)", "q1_no1": "👨‍🏫 학교 선생님", "q1_no2": "📖 교과서",
                       "q2": "\"greatest\"의 뜻은?", "q2_ok": "🏆 가장 위대한", "q2_no1": "😢 가장 슬픈", "q2_no2": "😡 가장 화난",
                       "write_blank": "___ became their greatest teacher.", "write_ans": "Necessity", "write_c1": "Necessity", "write_c2": "Laziness", "write_c3": "Fear",
                       "write_prompt": "필요에 의해 배운 경험을 영어로 써봐!"},
                "d3": {"key_en": "They built a new life from nothing — necessity became their greatest teacher.", "key_kr": "아무것도 없는 곳에서 새 삶을 만들었어요 — 필요가 그들의 가장 위대한 선생님이 되었어요.",
                       "story_kr": "가족 로빈슨은 증명했어요.\n아무것도 없어도 의지가 있으면 무엇이든 만들 수 있다는 걸.\n필요가 창의력을 낳았고, 그것이 최고의 수업이었어요.\n아무것도 없는 곳에서 새 삶을 만들었어요 — 필요가 그들의 가장 위대한 선생님이 되었어요.",
                       "story_en": "The Robinson family proved something important.\nEven with nothing, willpower can create anything.\nNecessity sparked creativity, and that was the greatest lesson.\nThey built a new life from nothing — necessity became their greatest teacher.",
                       "vocab": [("proved","증명했다","✅","\"They proved.\""),("willpower","의지","💪","\"With willpower.\""),("creativity","창의력","🎨","\"Sparked creativity.\""),("lesson","교훈","📚","\"The greatest lesson.\"")],
                       "pick_blank": "Necessity sparked ___.", "pick_ans": "creativity", "pick_choices": ["creativity","laziness","anger"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["They","built","a","new","life","from","nothing","necessity","became","their","greatest","teacher"], "wo_ans": "They built a new life from nothing necessity became their greatest teacher",
                       "listen_text": "They built a new life from nothing. Necessity became their greatest teacher.", "listen_ok": "아무것도 없이 새 삶, 필요가 최고의 스승", "listen_no1": "쉽게 살았다", "listen_no2": "아무것도 배우지 않았다",
                       "dict_word": "creativity", "dict_hint": "c r e a t i v i t _",
                       "q1": "가족이 증명한 것은?", "q1_ok": "💪 의지가 있으면 무엇이든 가능하다", "q1_no1": "💰 돈이 제일 중요하다", "q1_no2": "😴 포기해야 한다",
                       "q2": "\"creativity\"의 뜻은?", "q2_ok": "🎨 창의력", "q2_no1": "😴 게으름", "q2_no2": "😡 분노",
                       "write_blank": "Necessity sparked ___.", "write_ans": "creativity", "write_c1": "creativity", "write_c2": "boredom", "write_c3": "sadness",
                       "write_prompt": "Week 34 완료! 어려움에서 배운 교훈을 써봐!"}
            },
            35: {
                "d1": {"key_en": "Every challenge made them stronger.", "key_kr": "모든 도전이 그들을 더 강하게 만들었어요.",
                       "story_kr": "야생 동물, 폭풍, 식량 부족...\n매번 어려움이 닥쳤어요.\n하지만 극복할 때마다 더 강해졌어요.\n모든 도전이 그들을 더 강하게 만들었어요.",
                       "story_en": "Wild animals, storms, food shortages...\nDifficulties came again and again.\nBut every time they overcame one, they grew stronger.\nEvery challenge made them stronger.",
                       "vocab": [("challenge","도전","🏔️","\"Every challenge.\""),("stronger","더 강한","💪","\"Made them stronger.\""),("overcame","극복했다","🏆","\"They overcame.\""),("difficulties","어려움","⛰️","\"Difficulties came.\"")],
                       "pick_blank": "Every challenge made them ___.", "pick_ans": "stronger", "pick_choices": ["stronger","weaker","smaller"],
                       "wo_kr": "\"모든 도전이 더 강하게 만들었어요.\"를 영어로!", "wo_words": ["Every","challenge","made","them","stronger"], "wo_ans": "Every challenge made them stronger",
                       "listen_text": "Every challenge made them stronger and braver.", "listen_ok": "모든 도전이 더 강하게 만들었다", "listen_no1": "도전이 그들을 약하게 만들었다", "listen_no2": "도전이 없었다",
                       "dict_word": "challenge", "dict_hint": "c h a l l e n g _",
                       "q1": "도전의 결과는?", "q1_ok": "💪 더 강해졌다", "q1_no1": "😢 포기했다", "q1_no2": "😴 잠들었다",
                       "q2": "\"challenge\"의 뜻은?", "q2_ok": "🏔️ 도전", "q2_no1": "🎉 축제", "q2_no2": "😴 휴식",
                       "write_blank": "Every ___ made them stronger.", "write_ans": "challenge", "write_c1": "challenge", "write_c2": "holiday", "write_c3": "dream",
                       "write_prompt": "도전을 극복한 경험을 영어로 써봐!"},
                "d2": {"key_en": "Every challenge they solved together made them closer.", "key_kr": "함께 해결한 모든 도전이 그들을 더 가깝게 만들었어요.",
                       "story_kr": "혼자 해결할 수 없는 문제도\n가족이 함께하면 가능했어요.\n함께 극복할 때마다 사이가 더 좋아졌어요.\n함께 해결한 모든 도전이 그들을 더 가깝게 만들었어요.",
                       "story_en": "Problems that seemed impossible alone\nbecame possible when the family worked together.\nEvery time they overcame something together, their bond grew.\nEvery challenge they solved together made them closer.",
                       "vocab": [("solved","해결했다","🧩","\"They solved together.\""),("closer","더 가까운","🤗","\"Made them closer.\""),("bond","유대","🔗","\"Their bond grew.\""),("impossible","불가능한","❌","\"Seemed impossible.\"")],
                       "pick_blank": "Every challenge they solved together made them ___.", "pick_ans": "closer", "pick_choices": ["closer","angrier","lonelier"],
                       "wo_kr": "\"함께 해결한 도전이 더 가깝게 만들었어요.\"를 영어로!", "wo_words": ["Every","challenge","they","solved","together","made","them","closer"], "wo_ans": "Every challenge they solved together made them closer",
                       "listen_text": "Every challenge they solved together made them closer as a family.", "listen_ok": "함께 해결한 도전이 더 가깝게 만들었다", "listen_no1": "도전이 가족을 갈라놓았다", "listen_no2": "혼자서 해결했다",
                       "dict_word": "closer", "dict_hint": "c l o s e _",
                       "q1": "함께 도전을 해결하면?", "q1_ok": "🤗 더 가까워진다", "q1_no1": "😡 더 멀어진다", "q1_no2": "😴 변화없다",
                       "q2": "\"solved\"의 뜻은?", "q2_ok": "🧩 해결했다", "q2_no1": "💔 부쉈다", "q2_no2": "😢 울었다",
                       "write_blank": "They ___ challenges together.", "write_ans": "solved", "write_c1": "solved", "write_c2": "avoided", "write_c3": "ignored",
                       "write_prompt": "함께 문제를 해결한 경험을 영어로 써봐!"},
                "d3": {"key_en": "Every challenge they solved together made them stronger and closer as a family.", "key_kr": "함께 해결한 모든 도전이 가족으로서 더 강하고 가까워지게 만들었어요.",
                       "story_kr": "로빈슨 가족은 깨달았어요.\n어려움이 축복이 될 수 있다는 걸.\n함께 이겨낼 때마다 더 강해지고 사랑도 깊어졌어요.\n함께 해결한 모든 도전이 가족으로서 더 강하고 가까워지게 만들었어요.",
                       "story_en": "The Robinson family realized something.\nDifficulties can become blessings.\nEvery time they overcame something, they grew stronger and their love deeper.\nEvery challenge they solved together made them stronger and closer as a family.",
                       "vocab": [("family","가족","👨‍👩‍👧‍👦","\"As a family.\""),("realized","깨달았다","💡","\"They realized.\""),("blessings","축복","🙏","\"Can become blessings.\""),("deeper","더 깊은","💗","\"Love grew deeper.\"")],
                       "pick_blank": "Every challenge made them stronger and closer as a ___.", "pick_ans": "family", "pick_choices": ["family","team","class"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["Every","challenge","they","solved","together","made","them","stronger","and","closer","as","a","family"], "wo_ans": "Every challenge they solved together made them stronger and closer as a family",
                       "listen_text": "Every challenge they solved together made them stronger and closer as a family.", "listen_ok": "함께 해결한 도전이 강하고 가깝게 만들었다", "listen_no1": "도전이 가족을 갈라놓았다", "listen_no2": "아무 변화가 없었다",
                       "dict_word": "stronger", "dict_hint": "s t r o n g e _",
                       "q1": "함께 도전을 이기면 어떻게 되나요?", "q1_ok": "💪 더 강하고 가까워진다", "q1_no1": "😡 더 싸운다", "q1_no2": "😴 아무 변화 없다",
                       "q2": "\"closer\"의 뜻은?", "q2_ok": "🤗 더 가까운", "q2_no1": "😡 더 먼", "q2_no2": "😴 더 졸린",
                       "write_blank": "They became ___ as a family.", "write_ans": "closer", "write_c1": "closer", "write_c2": "angrier", "write_c3": "lonelier",
                       "write_prompt": "Week 35 완료! 가족의 힘에 대해 써봐!"}
            },
            36: {
                "d1": {"key_en": "Home is not just a place.", "key_kr": "집은 단지 장소가 아니에요.",
                       "story_kr": "로빈슨 가족에게 집이란\n건물이 아니었어요.\n가족이 함께하는 곳이 집이었어요.\n집은 단지 장소가 아니에요.",
                       "story_en": "For the Robinson family, home\nwas not a building.\nHome was wherever the family was together.\nHome is not just a place.",
                       "vocab": [("home","집","🏠","\"Home is.\""),("place","장소","📍","\"Not just a place.\""),("building","건물","🏗️","\"Not a building.\""),("wherever","어디든","🌍","\"Wherever.\"")],
                       "pick_blank": "Home is not just a ___.", "pick_ans": "place", "pick_choices": ["place","game","song"],
                       "wo_kr": "\"집은 단지 장소가 아니에요.\"를 영어로!", "wo_words": ["Home","is","not","just","a","place"], "wo_ans": "Home is not just a place",
                       "listen_text": "Home is not just a place. It is more than that.", "listen_ok": "집은 단지 장소가 아니다", "listen_no1": "집은 건물이다", "listen_no2": "집은 필요 없다",
                       "dict_word": "place", "dict_hint": "p l a c _",
                       "q1": "집은 무엇인가요?", "q1_ok": "🏠 단순한 장소 이상", "q1_no1": "🏗️ 건물일 뿐", "q1_no2": "❌ 필요 없는 것",
                       "q2": "\"place\"의 뜻은?", "q2_ok": "📍 장소", "q2_no1": "🎵 노래", "q2_no2": "📖 책",
                       "write_blank": "Home is not just a ___.", "write_ans": "place", "write_c1": "place", "write_c2": "game", "write_c3": "joke",
                       "write_prompt": "\"집\"의 의미에 대해 영어로 써봐!"},
                "d2": {"key_en": "Home is built by the people who love each other.", "key_kr": "집은 서로 사랑하는 사람들이 만드는 거예요.",
                       "story_kr": "로빈슨 가족은 나무 위에 집을 지었어요.\n하지만 진짜 \"집\"은 나무집이 아니었어요.\n서로를 사랑하는 마음이 진짜 집이었어요.\n집은 서로 사랑하는 사람들이 만드는 거예요.",
                       "story_en": "The Robinson family built a treehouse.\nBut the real \"home\" was not the treehouse.\nIt was the love they shared for each other.\nHome is built by the people who love each other.",
                       "vocab": [("people","사람들","👫","\"By the people.\""),("love","사랑하다","❤️","\"Who love.\""),("each other","서로","🤝","\"Love each other.\""),("real","진짜의","💎","\"The real home.\"")],
                       "pick_blank": "Home is built by the people who ___ each other.", "pick_ans": "love", "pick_choices": ["love","hate","forget"],
                       "wo_kr": "\"서로 사랑하는 사람들이 집을 만든다\"를 영어로!", "wo_words": ["Home","is","built","by","the","people","who","love","each","other"], "wo_ans": "Home is built by the people who love each other",
                       "listen_text": "Home is built by the people who love each other.", "listen_ok": "서로 사랑하는 사람들이 집을 만든다", "listen_no1": "돈이 많아야 집이 있다", "listen_no2": "집은 건물이다",
                       "dict_word": "people", "dict_hint": "p e o p l _",
                       "q1": "진짜 \"집\"은 무엇인가요?", "q1_ok": "❤️ 서로 사랑하는 마음", "q1_no1": "🏗️ 큰 건물", "q1_no2": "💰 비싼 가구",
                       "q2": "\"each other\"의 뜻은?", "q2_ok": "🤝 서로", "q2_no1": "👤 혼자", "q2_no2": "❌ 아무도",
                       "write_blank": "People who ___ each other.", "write_ans": "love", "write_c1": "love", "write_c2": "ignore", "write_c3": "fight",
                       "write_prompt": "사랑하는 사람들과의 경험을 영어로 써봐!"},
                "d3": {"key_en": "Home is not a place — it is built by the people who love and protect each other.", "key_kr": "집은 장소가 아니에요 — 서로 사랑하고 지켜주는 사람들이 만드는 거예요.",
                       "story_kr": "로빈슨 가족의 여행이 끝나가고 있어요.\n가장 큰 교훈은:\n집은 건물이 아니라 사랑과 보호의 공간이에요.\n집은 장소가 아니에요 — 서로 사랑하고 지켜주는 사람들이 만드는 거예요.",
                       "story_en": "The Robinson family's journey was coming to an end.\nThe greatest lesson was:\nHome is not a building but a space of love and protection.\nHome is not a place — it is built by the people who love and protect each other.",
                       "vocab": [("protect","지키다","🛡️","\"Love and protect.\""),("built","만든","🏗️","\"It is built.\""),("journey","여행","🗺️","\"Their journey.\""),("greatest","가장 큰","🏆","\"The greatest lesson.\"")],
                       "pick_blank": "Home is built by people who love and ___ each other.", "pick_ans": "protect", "pick_choices": ["protect","abandon","forget"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["Home","is","not","a","place","it","is","built","by","the","people","who","love","and","protect","each","other"], "wo_ans": "Home is not a place it is built by the people who love and protect each other",
                       "listen_text": "Home is not a place. It is built by the people who love and protect each other.", "listen_ok": "사랑하고 지켜주는 사람들이 집을 만든다", "listen_no1": "집은 큰 건물이다", "listen_no2": "혼자 사는 것이 최고다",
                       "dict_word": "protect", "dict_hint": "p r o t e c _",
                       "q1": "집의 진정한 의미는?", "q1_ok": "🛡️ 사랑하고 지켜주는 사람들", "q1_no1": "🏗️ 비싼 건물", "q1_no2": "📍 특정 장소",
                       "q2": "\"protect\"의 뜻은?", "q2_ok": "🛡️ 지키다", "q2_no1": "💔 부수다", "q2_no2": "🏃 도망치다",
                       "write_blank": "Love and ___ each other.", "write_ans": "protect", "write_c1": "protect", "write_c2": "abandon", "write_c3": "trick",
                       "write_prompt": "Week 36 & Swiss Family Robinson 완료! 집의 의미에 대해 써봐!"}
            }
        }
    },
    # G6 Little Women W29-W32
    "g6_little": {
        "grade": 6, "quarter": "Q4", "book": "Little Women",
        "book_kr": "작은 아씨들", "emoji": "📚",
        "img": f"{R2}/images/little-women/w29_new.png",
        "ratio": "영어 70% / 한국어 30%", "level": "B2",
        "weeks": {
            29: {
                "d1": {"key_en": "Each sister chose her own path in life.", "key_kr": "각 자매는 인생에서 자신만의 길을 선택했어요.",
                       "story_kr": "마치 가족의 네 자매는 모두 달랐어요.\nMeg은 가정, Jo는 글쓰기, Beth는 음악, Amy는 예술.\n각자 다른 꿈을 가졌어요.\n각 자매는 인생에서 자신만의 길을 선택했어요.",
                       "story_en": "The four March sisters were all different.\nMeg chose family, Jo chose writing, Beth chose music, Amy chose art.\nEach had a different dream.\nEach sister chose her own path in life.",
                       "vocab": [("chose","선택했다","🔀","\"Each sister chose.\""),("path","길","🛤️","\"Her own path.\""),("sister","자매","👭","\"Each sister.\""),("own","자신만의","⭐","\"Her own path.\"")],
                       "pick_blank": "Each sister ___ her own path.", "pick_ans": "chose", "pick_choices": ["chose","lost","forgot"],
                       "wo_kr": "\"각 자매는 자신만의 길을 선택했어요.\"를 영어로!", "wo_words": ["Each","sister","chose","her","own","path","in","life"], "wo_ans": "Each sister chose her own path in life",
                       "listen_text": "Each sister chose her own path in life.", "listen_ok": "각 자매가 자신만의 길을 선택했다", "listen_no1": "모두 같은 길을 갔다", "listen_no2": "아무도 선택하지 않았다",
                       "dict_word": "chose", "dict_hint": "c h o s _",
                       "q1": "네 자매의 공통점은?", "q1_ok": "🔀 각자 자신만의 길을 선택", "q1_no1": "👯 모두 같은 꿈", "q1_no2": "😴 아무 꿈도 없음",
                       "q2": "\"path\"의 뜻은?", "q2_ok": "🛤️ 길", "q2_no1": "🎵 노래", "q2_no2": "📖 책",
                       "write_blank": "Each sister chose her own ___.", "write_ans": "path", "write_c1": "path", "write_c2": "food", "write_c3": "pet",
                       "write_prompt": "너의 꿈의 길은 무엇인지 영어로 써봐!"},
                "d2": {"key_en": "A woman's worth lies in her character, not convention.", "key_kr": "여성의 가치는 관습이 아닌 인격에 있어요.",
                       "story_kr": "1860년대에는 여성의 역할이 정해져 있었어요.\n하지만 마치 자매들은 달랐어요.\n자신의 인격과 꿈으로 가치를 증명했어요.\n여성의 가치는 관습이 아닌 인격에 있어요.",
                       "story_en": "In the 1860s, women's roles were strictly defined.\nBut the March sisters were different.\nThey proved their worth through character and dreams.\nA woman's worth lies in her character, not convention.",
                       "vocab": [("worth","가치","💎","\"A woman's worth.\""),("character","인격","🌟","\"In her character.\""),("convention","관습","📜","\"Not convention.\""),("proved","증명했다","✅","\"They proved.\"")],
                       "pick_blank": "A woman's worth lies in her ___, not convention.", "pick_ans": "character", "pick_choices": ["character","appearance","wealth"],
                       "wo_kr": "\"여성의 가치는 인격에 있다\"를 영어로!", "wo_words": ["A","woman's","worth","lies","in","her","character","not","convention"], "wo_ans": "A woman's worth lies in her character not convention",
                       "listen_text": "A woman's worth lies in her character, not convention.", "listen_ok": "가치는 인격에 있다", "listen_no1": "외모가 가장 중요하다", "listen_no2": "관습을 따라야 한다",
                       "dict_word": "character", "dict_hint": "c h a r a c t e _",
                       "q1": "여성의 진정한 가치는 어디에 있나요?", "q1_ok": "🌟 인격(character)", "q1_no1": "👗 외모", "q1_no2": "💰 재산",
                       "q2": "\"convention\"의 뜻은?", "q2_ok": "📜 관습", "q2_no1": "🎉 축제", "q2_no2": "📖 소설",
                       "write_blank": "Worth lies in ___, not convention.", "write_ans": "character", "write_c1": "character", "write_c2": "money", "write_c3": "fashion",
                       "write_prompt": "인격의 중요성에 대해 영어로 써봐!"},
                "d3": {"key_en": "Each sister chose her own path — proving that a woman's worth lies in her character, not convention.", "key_kr": "각 자매는 자신만의 길을 선택하며 — 여성의 가치가 관습이 아닌 인격에 있음을 증명했어요.",
                       "story_kr": "네 자매는 각자의 길을 걸으며\n사회가 정한 틀을 깨뜨렸어요.\n자신의 선택으로 가치를 보여줬어요.\n각 자매는 자신만의 길을 선택하며 — 여성의 가치가 관습이 아닌 인격에 있음을 증명했어요.",
                       "story_en": "The four sisters walked their own paths\nand broke the mold society had set.\nThey showed their worth through their choices.\nEach sister chose her own path — proving that a woman's worth lies in her character, not convention.",
                       "vocab": [("proving","증명하며","✅","\"Proving that.\""),("lies","있다","📍","\"Worth lies in.\""),("broke","깨뜨렸다","💥","\"Broke the mold.\""),("choices","선택들","🔀","\"Through their choices.\"")],
                       "pick_blank": "Each sister chose her own path — ___ that a woman's worth lies in character.", "pick_ans": "proving", "pick_choices": ["proving","forgetting","hiding"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["Each","sister","chose","her","own","path","proving","that","a","woman's","worth","lies","in","her","character","not","convention"], "wo_ans": "Each sister chose her own path proving that a woman's worth lies in her character not convention",
                       "listen_text": "Each sister chose her own path, proving that a woman's worth lies in her character, not convention.", "listen_ok": "자신만의 길로 인격의 가치를 증명했다", "listen_no1": "관습을 따랐다", "listen_no2": "모두 같은 길을 갔다",
                       "dict_word": "proving", "dict_hint": "p r o v i n _",
                       "q1": "자매들이 증명한 것은?", "q1_ok": "🌟 여성의 가치는 인격에 있다", "q1_no1": "💰 돈이 가장 중요하다", "q1_no2": "📜 관습을 따라야 한다",
                       "q2": "\"proving\"의 뜻은?", "q2_ok": "✅ 증명하며", "q2_no1": "❌ 숨기며", "q2_no2": "😴 자며",
                       "write_blank": "Each sister chose her own path, ___ her worth.", "write_ans": "proving", "write_c1": "proving", "write_c2": "hiding", "write_c3": "denying",
                       "write_prompt": "Week 29 완료! 자신만의 길에 대해 영어로 써봐!"}
            },
            30: {
                "d1": {"key_en": "Jo refused to be defined by society.", "key_kr": "Jo는 사회에 의해 규정되기를 거부했어요.",
                       "story_kr": "Jo는 당시 여성에게 기대되는 것을 거부했어요.\n결혼과 가사만이 전부가 아니었어요.\n자신만의 꿈을 추구했어요.\nJo는 사회에 의해 규정되기를 거부했어요.",
                       "story_en": "Jo rejected what society expected of women.\nMarriage and housework were not everything.\nShe pursued her own dreams.\nJo refused to be defined by society.",
                       "vocab": [("refused","거부했다","✋","\"Jo refused.\""),("defined","규정된","📏","\"To be defined.\""),("society","사회","🏛️","\"Defined by society.\""),("pursued","추구했다","🏃‍♀️","\"Pursued her dreams.\"")],
                       "pick_blank": "Jo ___ to be defined by society.", "pick_ans": "refused", "pick_choices": ["refused","wanted","loved"],
                       "wo_kr": "\"Jo는 사회에 의해 규정되기를 거부했어요.\"를 영어로!", "wo_words": ["Jo","refused","to","be","defined","by","society"], "wo_ans": "Jo refused to be defined by society",
                       "listen_text": "Jo refused to be defined by society's expectations.", "listen_ok": "사회의 규정을 거부했다", "listen_no1": "사회의 기대를 따랐다", "listen_no2": "아무것도 하지 않았다",
                       "dict_word": "refused", "dict_hint": "r e f u s e _",
                       "q1": "Jo는 무엇을 거부했나요?", "q1_ok": "✋ 사회에 의해 규정되는 것", "q1_no1": "🎁 선물을", "q1_no2": "🍽️ 음식을",
                       "q2": "\"society\"의 뜻은?", "q2_ok": "🏛️ 사회", "q2_no1": "🎵 음악", "q2_no2": "📖 소설",
                       "write_blank": "Jo ___ to be defined.", "write_ans": "refused", "write_c1": "refused", "write_c2": "wanted", "write_c3": "tried",
                       "write_prompt": "자신을 규정하지 않은 경험을 영어로 써봐!"},
                "d2": {"key_en": "Writing was Jo's true identity and purpose.", "key_kr": "글쓰기가 Jo의 진정한 정체성이자 목적이었어요.",
                       "story_kr": "Jo에게 글쓰기는 취미가 아니었어요.\n그것이 바로 Jo 자신이었어요.\n글을 쓸 때 가장 자유로웠어요.\n글쓰기가 Jo의 진정한 정체성이자 목적이었어요.",
                       "story_en": "For Jo, writing was not just a hobby.\nIt was who she truly was.\nShe felt most free when writing.\nWriting was Jo's true identity and purpose.",
                       "vocab": [("writing","글쓰기","✍️","\"Writing was.\""),("identity","정체성","🪞","\"True identity.\""),("purpose","목적","🎯","\"Identity and purpose.\""),("free","자유로운","🕊️","\"Most free.\"")],
                       "pick_blank": "Writing was Jo's true ___ and purpose.", "pick_ans": "identity", "pick_choices": ["identity","problem","weakness"],
                       "wo_kr": "\"글쓰기가 Jo의 진정한 정체성이자 목적\"을 영어로!", "wo_words": ["Writing","was","Jo's","true","identity","and","purpose"], "wo_ans": "Writing was Jo's true identity and purpose",
                       "listen_text": "Writing was Jo's true identity and purpose in life.", "listen_ok": "글쓰기가 Jo의 정체성이자 목적이다", "listen_no1": "Jo는 글쓰기를 싫어했다", "listen_no2": "Jo는 요리가 목적이었다",
                       "dict_word": "identity", "dict_hint": "i d e n t i t _",
                       "q1": "Jo에게 글쓰기란?", "q1_ok": "🪞 진정한 정체성이자 목적", "q1_no1": "😴 지루한 숙제", "q1_no2": "🎮 가벼운 놀이",
                       "q2": "\"purpose\"의 뜻은?", "q2_ok": "🎯 목적", "q2_no1": "😢 슬픔", "q2_no2": "🎉 파티",
                       "write_blank": "Jo's true ___ was writing.", "write_ans": "identity", "write_c1": "identity", "write_c2": "weakness", "write_c3": "enemy",
                       "write_prompt": "너의 정체성과 목적에 대해 영어로 써봐!"},
                "d3": {"key_en": "Jo refused to be defined by society's expectations — writing was her true identity and purpose.", "key_kr": "Jo는 사회의 기대에 규정되기를 거부했어요 — 글쓰기가 그녀의 진정한 정체성이자 목적이었어요.",
                       "story_kr": "Jo는 사회가 원하는 대로 살지 않았어요.\n자신의 길을 선택했어요.\n글쓰기가 바로 Jo의 전부였어요.\nJo는 사회의 기대에 규정되기를 거부했어요 — 글쓰기가 그녀의 진정한 정체성이자 목적이었어요.",
                       "story_en": "Jo did not live the way society wanted.\nShe chose her own way.\nWriting was everything to Jo.\nJo refused to be defined by society's expectations — writing was her true identity and purpose.",
                       "vocab": [("expectations","기대","📋","\"Society's expectations.\""),("true","진정한","💎","\"True identity.\""),("defined","규정된","📏","\"Defined by society.\""),("everything","전부","💯","\"Everything to Jo.\"")],
                       "pick_blank": "Jo refused to be defined by society's ___.", "pick_ans": "expectations", "pick_choices": ["expectations","gifts","songs"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["Jo","refused","to","be","defined","by","society's","expectations","writing","was","her","true","identity","and","purpose"], "wo_ans": "Jo refused to be defined by society's expectations writing was her true identity and purpose",
                       "listen_text": "Jo refused to be defined by society's expectations. Writing was her true identity and purpose.", "listen_ok": "사회의 기대를 거부하고 글쓰기를 정체성으로", "listen_no1": "사회의 기대를 따랐다", "listen_no2": "글쓰기를 포기했다",
                       "dict_word": "expectations", "dict_hint": "e x p e c t a t i o n _",
                       "q1": "Jo가 거부한 것은?", "q1_ok": "📋 사회의 기대에 규정되는 것", "q1_no1": "🎁 친구의 선물", "q1_no2": "📖 읽기 숙제",
                       "q2": "\"expectations\"의 뜻은?", "q2_ok": "📋 기대", "q2_no1": "🎉 파티", "q2_no2": "😴 수면",
                       "write_blank": "Jo refused society's ___.", "write_ans": "expectations", "write_c1": "expectations", "write_c2": "gifts", "write_c3": "praises",
                       "write_prompt": "Week 30 완료! 자기만의 정체성에 대해 써봐!"}
            },
            31: {
                "d1": {"key_en": "True love is not about perfection.", "key_kr": "진정한 사랑은 완벽함이 아니에요.",
                       "story_kr": "마치 자매들은 사랑에 대해 배웠어요.\n완벽한 사람은 없어요.\n사랑은 완벽함을 요구하지 않아요.\n진정한 사랑은 완벽함이 아니에요.",
                       "story_en": "The March sisters learned about love.\nNo one is perfect.\nLove does not demand perfection.\nTrue love is not about perfection.",
                       "vocab": [("true","진정한","💎","\"True love.\""),("perfection","완벽함","✨","\"Not about perfection.\""),("demand","요구하다","📢","\"Does not demand.\""),("learned","배웠다","📚","\"They learned.\"")],
                       "pick_blank": "True love is not about ___.", "pick_ans": "perfection", "pick_choices": ["perfection","money","power"],
                       "wo_kr": "\"진정한 사랑은 완벽함이 아니에요.\"를 영어로!", "wo_words": ["True","love","is","not","about","perfection"], "wo_ans": "True love is not about perfection",
                       "listen_text": "True love is not about perfection but about acceptance.", "listen_ok": "진정한 사랑은 완벽함이 아니다", "listen_no1": "완벽해야 사랑받는다", "listen_no2": "사랑은 필요 없다",
                       "dict_word": "perfection", "dict_hint": "p e r f e c t i o _",
                       "q1": "진정한 사랑은 무엇이 아닌가요?", "q1_ok": "✨ 완벽함", "q1_no1": "❤️ 관심", "q1_no2": "🤝 우정",
                       "q2": "\"perfection\"의 뜻은?", "q2_ok": "✨ 완벽함", "q2_no1": "😢 슬픔", "q2_no2": "😡 분노",
                       "write_blank": "True love is not about ___.", "write_ans": "perfection", "write_c1": "perfection", "write_c2": "happiness", "write_c3": "kindness",
                       "write_prompt": "완벽하지 않아도 괜찮은 것에 대해 써봐!"},
                "d2": {"key_en": "True love is about growing wiser and kinder together.", "key_kr": "진정한 사랑은 함께 더 현명하고 친절해지는 거예요.",
                       "story_kr": "Meg과 John은 완벽하지 않았어요.\n하지만 함께 성장했어요.\n더 현명하고, 더 친절해졌어요.\n진정한 사랑은 함께 더 현명하고 친절해지는 거예요.",
                       "story_en": "Meg and John were not perfect.\nBut they grew together.\nThey became wiser and kinder.\nTrue love is about growing wiser and kinder together.",
                       "vocab": [("growing","성장하는","🌱","\"Growing together.\""),("wiser","더 현명한","🧠","\"Growing wiser.\""),("kinder","더 친절한","💕","\"Growing kinder.\""),("together","함께","🤝","\"Wiser together.\"")],
                       "pick_blank": "True love is about growing wiser and ___ together.", "pick_ans": "kinder", "pick_choices": ["kinder","angrier","lonelier"],
                       "wo_kr": "\"함께 더 현명하고 친절해지는 것\"을 영어로!", "wo_words": ["True","love","is","about","growing","wiser","and","kinder","together"], "wo_ans": "True love is about growing wiser and kinder together",
                       "listen_text": "True love is about growing wiser and kinder together.", "listen_ok": "함께 현명하고 친절해지는 것이 사랑이다", "listen_no1": "완벽해야 사랑이다", "listen_no2": "혼자가 최고다",
                       "dict_word": "wiser", "dict_hint": "w i s e _",
                       "q1": "진정한 사랑에서 함께 하는 것은?", "q1_ok": "🌱 더 현명하고 친절하게 성장", "q1_no1": "💰 돈 벌기", "q1_no2": "🏃 경쟁하기",
                       "q2": "\"wiser\"의 뜻은?", "q2_ok": "🧠 더 현명한", "q2_no1": "😡 더 화난", "q2_no2": "😴 더 졸린",
                       "write_blank": "Growing ___ and kinder together.", "write_ans": "wiser", "write_c1": "wiser", "write_c2": "angrier", "write_c3": "lazier",
                       "write_prompt": "함께 성장한 경험을 영어로 써봐!"},
                "d3": {"key_en": "True love is not about perfection but about growing wiser and kinder together through every difficulty.", "key_kr": "진정한 사랑은 완벽함이 아니라 모든 어려움을 통해 함께 더 현명하고 친절해지는 거예요.",
                       "story_kr": "작은 아씨들의 사랑 이야기는\n완벽한 로맨스가 아니었어요.\n어려움을 함께 이겨내며 성장하는 거였어요.\n진정한 사랑은 완벽함이 아니라 모든 어려움을 통해 함께 더 현명하고 친절해지는 거예요.",
                       "story_en": "The love stories in Little Women\nwere not perfect romances.\nThey were about growing together through hardship.\nTrue love is not about perfection but about growing wiser and kinder together through every difficulty.",
                       "vocab": [("difficulty","어려움","⛰️","\"Through every difficulty.\""),("through","~을 통해","🚪","\"Through every.\""),("romances","로맨스","💕","\"Perfect romances.\""),("hardship","역경","🌧️","\"Through hardship.\"")],
                       "pick_blank": "Growing wiser and kinder through every ___.", "pick_ans": "difficulty", "pick_choices": ["difficulty","party","vacation"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["True","love","is","not","about","perfection","but","about","growing","wiser","and","kinder","together","through","every","difficulty"], "wo_ans": "True love is not about perfection but about growing wiser and kinder together through every difficulty",
                       "listen_text": "True love is not about perfection but about growing wiser and kinder together through every difficulty.", "listen_ok": "어려움을 통해 함께 성장하는 것이 사랑이다", "listen_no1": "완벽해야 진짜 사랑이다", "listen_no2": "어려움은 피해야 한다",
                       "dict_word": "difficulty", "dict_hint": "d i f f i c u l t _",
                       "q1": "진정한 사랑은?", "q1_ok": "🌱 어려움을 통해 함께 성장", "q1_no1": "✨ 완벽함", "q1_no2": "💰 부유함",
                       "q2": "\"through\"의 뜻은?", "q2_ok": "🚪 ~을 통해", "q2_no1": "❌ ~없이", "q2_no2": "⬆️ ~위에",
                       "write_blank": "Growing through every ___.", "write_ans": "difficulty", "write_c1": "difficulty", "write_c2": "holiday", "write_c3": "meal",
                       "write_prompt": "Week 31 완료! 어려움을 이겨낸 사랑에 대해 써봐!"}
            },
            32: {
                "d1": {"key_en": "Family and integrity matter more than wealth.", "key_kr": "가족과 진실성은 부보다 더 중요해요.",
                       "story_kr": "마치 가족은 가난했어요.\n하지만 사랑과 정직이 있었어요.\n돈보다 소중한 것이 있었어요.\n가족과 진실성은 부보다 더 중요해요.",
                       "story_en": "The March family was poor.\nBut they had love and honesty.\nThere were things more valuable than money.\nFamily and integrity matter more than wealth.",
                       "vocab": [("integrity","진실성","💎","\"Family and integrity.\""),("matter","중요하다","⭐","\"Matter more.\""),("wealth","부/재산","💰","\"More than wealth.\""),("valuable","소중한","🌟","\"More valuable.\"")],
                       "pick_blank": "Family and integrity ___ more than wealth.", "pick_ans": "matter", "pick_choices": ["matter","cost","weigh"],
                       "wo_kr": "\"가족과 진실성은 부보다 중요하다\"를 영어로!", "wo_words": ["Family","and","integrity","matter","more","than","wealth"], "wo_ans": "Family and integrity matter more than wealth",
                       "listen_text": "Family and integrity matter more than wealth.", "listen_ok": "가족과 진실성이 부보다 중요하다", "listen_no1": "돈이 가장 중요하다", "listen_no2": "가족은 필요 없다",
                       "dict_word": "integrity", "dict_hint": "i n t e g r i t _",
                       "q1": "부보다 더 중요한 것은?", "q1_ok": "💎 가족과 진실성", "q1_no1": "💰 더 많은 돈", "q1_no2": "🏠 큰 집",
                       "q2": "\"wealth\"의 뜻은?", "q2_ok": "💰 부/재산", "q2_no1": "🏥 건강", "q2_no2": "📚 지식",
                       "write_blank": "Family and integrity ___ more.", "write_ans": "matter", "write_c1": "matter", "write_c2": "cost", "write_c3": "break",
                       "write_prompt": "돈보다 중요한 것에 대해 영어로 써봐!"},
                "d2": {"key_en": "Little Women shows that purpose matters far more than social status.", "key_kr": "작은 아씨들은 목적이 사회적 지위보다 훨씬 중요하다는 것을 보여줘요.",
                       "story_kr": "작은 아씨들의 핵심 메시지예요.\n사회적 지위나 돈이 아니라\n삶의 목적이 진짜 중요한 거예요.\n작은 아씨들은 목적이 사회적 지위보다 훨씬 중요하다는 것을 보여줘요.",
                       "story_en": "This is the core message of Little Women.\nNot social status or money,\nbut purpose in life is what truly matters.\nLittle Women shows that purpose matters far more than social status.",
                       "vocab": [("purpose","목적","🎯","\"Purpose matters.\""),("social status","사회적 지위","🏛️","\"More than social status.\""),("far","훨씬","📏","\"Far more.\""),("shows","보여주다","👀","\"Little Women shows.\"")],
                       "pick_blank": "Purpose matters far more than social ___.", "pick_ans": "status", "pick_choices": ["status","media","studies"],
                       "wo_kr": "\"목적이 사회적 지위보다 중요하다\"를 영어로!", "wo_words": ["Little","Women","shows","that","purpose","matters","far","more","than","social","status"], "wo_ans": "Little Women shows that purpose matters far more than social status",
                       "listen_text": "Little Women shows that purpose matters far more than social status.", "listen_ok": "목적이 사회적 지위보다 중요하다", "listen_no1": "사회적 지위가 가장 중요하다", "listen_no2": "목적은 필요 없다",
                       "dict_word": "purpose", "dict_hint": "p u r p o s _",
                       "q1": "작은 아씨들의 핵심 메시지는?", "q1_ok": "🎯 목적이 지위보다 중요하다", "q1_no1": "💰 돈이 최고다", "q1_no2": "🏛️ 지위가 전부다",
                       "q2": "\"far more\"의 뜻은?", "q2_ok": "📏 훨씬 더", "q2_no1": "❌ 훨씬 덜", "q2_no2": "🔄 같은 정도로",
                       "write_blank": "___ matters far more than status.", "write_ans": "Purpose", "write_c1": "Purpose", "write_c2": "Fashion", "write_c3": "Gossip",
                       "write_prompt": "삶의 목적에 대해 영어로 써봐!"},
                "d3": {"key_en": "Little Women shows that family, integrity, and purpose matter far more than wealth or social status.", "key_kr": "작은 아씨들은 가족, 진실성, 목적이 부나 사회적 지위보다 훨씬 중요하다는 것을 보여줘요.",
                       "story_kr": "작은 아씨들의 여정이 끝났어요.\n이 이야기가 전하는 메시지는 분명해요.\n가족, 진실성, 목적 — 이것이 진짜 중요한 것이에요.\n작은 아씨들은 가족, 진실성, 목적이 부나 사회적 지위보다 훨씬 중요하다는 것을 보여줘요.",
                       "story_en": "The journey of Little Women has come to an end.\nThe message of this story is clear.\nFamily, integrity, and purpose — these are what truly matter.\nLittle Women shows that family, integrity, and purpose matter far more than wealth or social status.",
                       "vocab": [("message","메시지","💌","\"The message.\""),("clear","분명한","🔍","\"The message is clear.\""),("journey","여정","🗺️","\"The journey.\""),("truly","진정으로","💎","\"Truly matter.\"")],
                       "pick_blank": "Family, integrity, and purpose ___ far more than wealth.", "pick_ans": "matter", "pick_choices": ["matter","cost","lose"],
                       "wo_kr": "완성 문장을 영어로!", "wo_words": ["Little","Women","shows","that","family","integrity","and","purpose","matter","far","more","than","wealth","or","social","status"], "wo_ans": "Little Women shows that family integrity and purpose matter far more than wealth or social status",
                       "listen_text": "Little Women shows that family, integrity, and purpose matter far more than wealth or social status.", "listen_ok": "가족, 진실성, 목적이 부와 지위보다 중요하다", "listen_no1": "부와 지위가 가장 중요하다", "listen_no2": "아무것도 중요하지 않다",
                       "dict_word": "matter", "dict_hint": "m a t t e _",
                       "q1": "이 이야기의 핵심 메시지는?", "q1_ok": "💎 가족, 진실성, 목적이 진짜 중요하다", "q1_no1": "💰 부자가 되어야 한다", "q1_no2": "🏛️ 높은 지위가 필요하다",
                       "q2": "\"matter\"의 뜻은?", "q2_ok": "⭐ 중요하다", "q2_no1": "💰 비용이 들다", "q2_no2": "😴 졸리다",
                       "write_blank": "Family and purpose ___ far more.", "write_ans": "matter", "write_c1": "matter", "write_c2": "cost", "write_c3": "shrink",
                       "write_prompt": "Week 32 & Little Women 완료! 진짜 중요한 것에 대해 써봐!"}
            }
        }
    }
}

# ─── QUARTER LABELS ───────────────────────────────────────────
# G4: W13-W20 → Q2, G5: W33-W36 → Q4, G6: W29-W32 → Q4
# Actually keep from book definition

DAY_MAP = {"d1": ("a", "Day1", "●○○", "월"), "d2": ("b", "Day2", "●●○", "수"), "d3": ("c", "Day3", "●●●", "금")}

def gen_css_g4():
    """Return CSS block for G4 style."""
    return """*{box-sizing:border-box;margin:0;padding:0;}
:root{--sage:#4a7c59;--sage-light:#e8f5e9;--gold:#c9a028;--gold-light:#fdf6e3;--coral:#e8714a;--coral-light:#fdf0eb;--sky:#2196f3;--sky-light:#e3f2fd;--brown:#795548;--text:#2d3748;--text2:#4a5568;--text3:#718096;--bg:#f7f4ee;--card:#ffffff;}
body{font-family:'Noto Sans KR',sans-serif;background:var(--bg);color:var(--text);font-size:16px;}
.topbar{position:sticky;top:0;z-index:100;background:var(--sage);padding:10px 16px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 2px 8px rgba(0,0,0,0.15);}
.top-left{display:flex;align-items:center;gap:10px;}.top-title{font-weight:900;font-size:0.95rem;color:#fff;}.top-sub{font-size:0.72rem;color:rgba(255,255,255,0.75);}
.xp-pill{background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.3);color:#fff;padding:5px 12px;border-radius:20px;font-size:0.8rem;font-weight:700;}
.ai-tutor-btn{background:#00f2ff;color:#000;border:none;padding:7px 14px;border-radius:20px;font-size:0.8rem;font-weight:900;cursor:pointer;}
.container{max-width:680px;margin:0 auto;padding:16px;}
.hero-wrap{border-radius:18px;overflow:hidden;margin-bottom:16px;box-shadow:0 4px 20px rgba(0,0,0,0.12);}
.hero-img-wrap{position:relative;}.scene-img{width:100%;display:block;object-fit:cover;}
.hero-overlay{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,0.65));padding:20px 20px 16px;color:#fff;}
.hero-overlay h2{font-family:'Nunito',sans-serif;font-size:1.3rem;font-weight:900;margin-bottom:4px;}.hero-overlay p{font-size:0.82rem;opacity:0.85;}
.day-badge{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap;}
.day-pill{padding:4px 12px;border-radius:20px;font-size:0.7rem;font-weight:700;border:2px solid transparent;}
.day-pill.done{background:rgba(255,255,255,0.2);color:#fff;border-color:rgba(255,255,255,0.3);}
.day-pill.today{background:#fff;color:var(--sage);border-color:#fff;}
.day-pill.future{background:rgba(255,255,255,0.08);color:rgba(255,255,255,0.4);border-color:rgba(255,255,255,0.1);}
.robo{display:flex;align-items:flex-start;gap:10px;background:var(--sage-light);border:1px solid rgba(74,124,89,0.2);border-radius:12px;padding:12px;margin-bottom:12px;}
.robo-av img{width:36px;height:36px;border-radius:50%;border:2px solid var(--sage);object-fit:cover;}
.robo-nm{font-size:0.68rem;font-weight:700;color:var(--sage);margin-bottom:3px;}
.robo-msg{font-size:0.82rem;line-height:1.65;color:var(--text2);}
.card{background:#fff;border-radius:16px;margin-bottom:14px;box-shadow:0 2px 12px rgba(0,0,0,0.07);overflow:hidden;}
.sec-hdr{display:flex;align-items:center;gap:12px;padding:14px 16px 0;}
.sec-num{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Nunito',sans-serif;font-weight:900;font-size:0.9rem;color:#fff;flex-shrink:0;}
.sec-title{font-weight:900;font-size:1rem;color:var(--text);}.sec-sub{font-size:0.7rem;color:var(--text3);margin-top:2px;}
.sec-body{padding:14px 16px;}
.key-card{background:linear-gradient(135deg,var(--sage),#3d6b4a);border-radius:14px;padding:18px;color:#fff;margin-bottom:14px;}
.key-eyebrow{font-size:0.68rem;font-weight:700;letter-spacing:0.1em;color:rgba(255,255,255,0.7);margin-bottom:8px;}
.key-eng{font-family:'Nunito',sans-serif;font-size:1.55rem;font-weight:900;margin-bottom:6px;line-height:1.3;}
.key-kr{font-size:0.95rem;color:rgba(255,255,255,0.8);margin-bottom:12px;}
.key-play-row{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,0.12);border-radius:10px;padding:10px 14px;cursor:pointer;}
.play-btn{width:40px;height:40px;border-radius:50%;background:#fff;color:var(--sage);border:none;font-size:1.1rem;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-weight:900;box-shadow:0 2px 8px rgba(0,0,0,0.15);}
.play-label{font-size:0.82rem;font-weight:700;color:#fff;}.play-hint{font-size:0.68rem;color:rgba(255,255,255,0.6);margin-top:2px;}
.story-player-row{display:flex;align-items:center;gap:12px;margin:12px 0 10px;}
.story-label{font-size:0.75rem;font-weight:800;color:var(--sage);background:var(--sage-light);padding:4px 12px;border-radius:12px;}
.story-ctrl-btn{width:44px;height:44px;border-radius:50%;border:none;cursor:pointer;font-size:1.1rem;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(0,0,0,0.15);font-weight:900;}
.story-play-btn{background:var(--sage);color:#fff;}.story-stop-btn{background:#fff;color:var(--sage);border:2px solid var(--sage)!important;display:none;}
.story-en{background:var(--sky-light);border-radius:10px;padding:14px;font-size:0.88rem;line-height:1.9;margin-bottom:10px;}
.hl{background:rgba(201,160,40,0.2);border-radius:4px;padding:1px 3px;font-weight:700;}
.vocab-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:14px;}
.v-card{background:var(--bg);border-radius:12px;padding:14px 10px;text-align:center;cursor:pointer;transition:all 0.2s;border:2px solid transparent;}
.v-card:hover{border-color:var(--sage);background:var(--sage-light);}
.v-emoji{font-size:1.8rem;margin-bottom:6px;}.v-eng{font-family:'Nunito',sans-serif;font-weight:900;font-size:1rem;color:var(--text);}
.v-kr{font-size:0.78rem;color:var(--text3);margin:4px 0;}.v-ex{font-size:0.7rem;color:var(--sage);font-style:italic;}
.v-play{margin-top:8px;background:var(--sage);color:#fff;border:none;padding:4px 12px;border-radius:10px;font-size:0.72rem;cursor:pointer;}
.game-box{background:var(--bg);border-radius:12px;padding:14px;margin-bottom:12px;}
.game-q{font-size:0.88rem;font-weight:700;color:var(--text);margin-bottom:12px;line-height:1.6;}
.blank{display:inline-block;min-width:60px;border-bottom:3px solid var(--sage);padding:0 4px;font-family:'Nunito',sans-serif;font-weight:900;color:var(--sage);text-align:center;}
.choices{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px;}
.ch{padding:9px 18px;border-radius:10px;background:#fff;border:2px solid rgba(0,0,0,0.1);font-size:0.88rem;font-weight:700;cursor:pointer;transition:all 0.2s;}
.ch:hover{border-color:var(--sage);background:var(--sage-light);}.ch.ok{background:var(--sage-light);border-color:var(--sage);color:var(--sage);}
.ch.no{background:#ffeaea;border-color:#e53935;color:#e53935;}
.fb{font-size:0.82rem;font-weight:700;margin-top:6px;min-height:20px;}
.build-zone{min-height:48px;background:#fff;border:2px dashed rgba(74,124,89,0.3);border-radius:10px;padding:10px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:10px;}
.build-ph{font-size:0.8rem;color:var(--text3);}
.placed{padding:7px 14px;background:var(--sage);color:#fff;border-radius:8px;font-size:0.9rem;font-weight:700;cursor:pointer;}
.wpool{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:12px;}
.wchip{padding:8px 16px;background:#fff;border:2px solid rgba(0,0,0,0.1);border-radius:10px;font-size:0.88rem;font-weight:700;cursor:pointer;transition:all 0.2s;}
.wchip:hover{border-color:var(--sage);}.wchip.used{opacity:0.3;pointer-events:none;}
.game-btns{display:flex;gap:8px;margin-bottom:8px;}
.btn-ok{padding:9px 20px;background:var(--sage);color:#fff;border:none;border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;}
.btn-rst{padding:9px 16px;background:var(--bg);color:var(--text2);border:1px solid rgba(0,0,0,0.1);border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;}
.match-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;}
.match-col{display:flex;flex-direction:column;gap:7px;}
.m-btn{padding:10px;background:#fff;border:2px solid rgba(0,0,0,0.1);border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;text-align:center;transition:all 0.2s;min-height:52px;display:flex;align-items:center;justify-content:center;}
.m-btn:hover{border-color:var(--sage);}.m-btn.sel{background:var(--sage-light);border-color:var(--sage);color:var(--sage);}
.m-btn.ok{background:var(--sage-light);border-color:var(--sage);color:var(--sage);pointer-events:none;}
.m-btn.no{background:#ffeaea;border-color:#e53935;animation:shk .3s ease;}
@keyframes shk{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.listen-play{width:100%;padding:14px;background:var(--sage);color:#fff;border:none;border-radius:12px;font-size:1rem;font-weight:700;cursor:pointer;margin-bottom:12px;}
.listen-opts{display:flex;gap:8px;flex-wrap:wrap;}
.listen-opt{flex:1;min-width:80px;padding:12px 8px;background:#fff;border:2px solid rgba(0,0,0,0.08);border-radius:12px;cursor:pointer;text-align:center;transition:all 0.2s;}
.listen-opt:hover{border-color:var(--sage);}
.lo-emoji{font-size:1.5rem;margin-bottom:5px;}.lo-label{font-size:0.75rem;font-weight:700;color:var(--text2);}
.listen-opt.ok{border-color:var(--sage);background:var(--sage-light);}.listen-opt.no{border-color:#e53935;background:#ffeaea;}
.dict-play{padding:10px 20px;background:var(--sky);color:#fff;border:none;border-radius:10px;font-size:0.88rem;font-weight:700;cursor:pointer;margin-bottom:10px;}
.dict-hint{font-family:'Nunito',sans-serif;font-size:1.3rem;font-weight:900;letter-spacing:0.2em;color:var(--text3);margin-bottom:10px;}
.dict-input{width:100%;padding:12px 14px;border:2px solid rgba(0,0,0,0.1);border-radius:10px;font-size:1rem;font-weight:700;outline:none;margin-bottom:8px;}.dict-input:focus{border-color:var(--sage);}
.dict-check{padding:9px 20px;background:var(--sage);color:#fff;border:none;border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;}
.quiz-box{background:var(--bg);border-radius:12px;padding:14px;margin-bottom:10px;}
.quiz-q{font-size:0.9rem;font-weight:700;line-height:1.6;margin-bottom:10px;}
.quiz-opts{display:flex;flex-direction:column;gap:7px;}
.qo{padding:10px 14px;background:#fff;border:2px solid rgba(0,0,0,0.08);border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;text-align:left;transition:all 0.2s;}
.qo:hover{border-color:var(--sage);}.qo.ok{background:var(--sage-light);border-color:var(--sage);color:var(--sage);}.qo.no{background:#ffeaea;border-color:#e53935;color:#e53935;}
.write-box{background:var(--bg);border-radius:12px;padding:14px;}
.write-input{width:100%;padding:12px;border:2px solid rgba(0,0,0,0.1);border-radius:10px;font-size:0.95rem;outline:none;margin-bottom:8px;}.write-input:focus{border-color:var(--sage);}
.write-btn{padding:9px 20px;background:var(--gold);color:#fff;border:none;border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;}
.prog{height:5px;background:rgba(0,0,0,0.06);margin-top:4px;}
.prog-fill{height:100%;background:linear-gradient(90deg,var(--sage),var(--gold));border-radius:0 3px 3px 0;}
.complete{background:linear-gradient(135deg,var(--sage),#2d5a3a);color:#fff;border-radius:16px;padding:24px;margin-bottom:14px;text-align:center;display:none;box-shadow:0 4px 20px rgba(74,124,89,0.3);}
.complete.show{display:block;}
.complete-emoji{font-size:2.5rem;margin-bottom:10px;}
.complete-title{font-family:'Nunito',sans-serif;font-size:1.5rem;font-weight:900;margin-bottom:8px;}
.complete-sub{font-size:0.88rem;line-height:1.75;opacity:0.9;margin-bottom:14px;}
.xp-big{font-family:'Nunito',sans-serif;font-size:1.1rem;font-weight:900;background:rgba(255,255,255,0.15);border-radius:10px;padding:10px;margin-bottom:14px;}
.next-card{background:rgba(255,255,255,0.12);border-radius:12px;padding:14px;display:flex;align-items:center;gap:12px;text-align:left;}
.next-label{font-size:0.68rem;font-weight:700;opacity:0.7;margin-bottom:3px;}
.next-title{font-family:'Nunito',sans-serif;font-size:0.95rem;font-weight:900;}
.next-btn{background:#fff;color:var(--sage);border:none;padding:10px 18px;border-radius:10px;font-size:0.85rem;font-weight:900;cursor:pointer;white-space:nowrap;text-decoration:none;display:inline-block;}
.ai-box{background:linear-gradient(135deg,#1a2a3a,#0d1b2a);border-radius:16px;padding:20px;color:#fff;}
.ai-box-title{font-family:'Nunito',sans-serif;font-size:1rem;font-weight:900;margin-bottom:3px;}
.ai-box-desc{font-size:0.78rem;color:rgba(255,255,255,0.45);line-height:1.6;}
.prompt-block{background:rgba(0,0,0,0.3);border-radius:10px;padding:14px;margin-bottom:14px;}
.prompt-lbl{font-size:0.62rem;letter-spacing:0.15em;color:#c9a028;font-weight:700;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;}
.copy-btn{background:rgba(201,160,40,0.2);border:1px solid rgba(201,160,40,0.4);color:#c9a028;border-radius:6px;padding:4px 12px;font-size:0.68rem;font-weight:700;cursor:pointer;}.copy-btn:hover{background:#c9a028;color:#000;}
.prompt-text{font-family:monospace;font-size:0.76rem;color:rgba(255,255,255,0.7);line-height:1.8;white-space:pre-wrap;}
.ai-steps{display:flex;flex-direction:column;gap:7px;margin-bottom:14px;}
.ai-step{display:flex;gap:10px;align-items:flex-start;font-size:0.8rem;color:rgba(255,255,255,0.6);}
.step-num{background:rgba(0,242,255,0.15);color:#00f2ff;font-family:'Nunito',sans-serif;font-weight:900;font-size:0.7rem;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.ai-btn-row{display:flex;gap:8px;flex-wrap:wrap;}
.ai-btn-primary{display:inline-flex;align-items:center;gap:6px;padding:11px 20px;background:linear-gradient(135deg,#19c37d,#0f9d58);color:#fff;border:none;border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;text-decoration:none;}
.ai-btn-sec{padding:11px 16px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);border-radius:10px;font-size:0.82rem;font-weight:700;cursor:pointer;}
.bnav{display:flex;align-items:center;justify-content:space-between;padding:12px 16px 28px;max-width:680px;margin:0 auto;}
.bn{padding:10px 20px;background:var(--sage);color:#fff;border-radius:12px;font-size:0.85rem;font-weight:700;text-decoration:none;}
.bp{padding:10px 20px;font-size:0.82rem;font-weight:700;color:var(--text3);text-decoration:none;}
.bl{font-size:0.82rem;font-weight:700;color:var(--text3);}"""

def gen_js(grade):
    """Return JS block. G4 uses speak() directly; G5/G6 use speakEl()."""
    base = """var xp=0,qOk=0,woPools={},mSel=null,mPairs={};
var _voices=[];
function _loadVoices(){_voices=window.speechSynthesis.getVoices();}
_loadVoices();
if(window.speechSynthesis.onvoiceschanged!==undefined){window.speechSynthesis.onvoiceschanged=_loadVoices;}
function _getBestVoice(){if(!_voices.length)_voices=window.speechSynthesis.getVoices();var prefer=['Samantha','Microsoft Zira Desktop - English (United States)','Microsoft Jenny Online (Natural) - English (United States)','Google US English','Karen'];for(var i=0;i<prefer.length;i++){var f=_voices.find(function(v){return v.name===prefer[i];});if(f)return f;}return _voices.find(function(v){return v.lang==='en-US';})||null;}
function speak(text){window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang='en-US';u.rate=0.78;u.pitch=1.05;var v=_getBestVoice();if(v)u.voice=v;window.speechSynthesis.speak(u);}"""
    if grade >= 5:
        base += "\nfunction speakEl(el){var text=el.getAttribute('data-speak')||'';if(text)speak(text);}"
    base += """
var _sp=false;
function storyPlay(text){if(_sp){storyStopped();return;}window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang='en-US';u.rate=0.75;u.pitch=1.05;var v=_getBestVoice();if(v)u.voice=v;u.onend=function(){storyStopped();};window.speechSynthesis.speak(u);_sp=true;var pb=document.getElementById('story-play-btn'),sb=document.getElementById('story-stop-btn');if(pb)pb.textContent='\\u23F8';if(sb)sb.style.display='flex';}
function storyStopped(){window.speechSynthesis.cancel();_sp=false;var pb=document.getElementById('story-play-btn'),sb=document.getElementById('story-stop-btn');if(pb)pb.textContent='\\u25B6';if(sb)sb.style.display='none';}
function addXP(n){xp+=n;var el=document.getElementById('xp');if(el)el.textContent=xp;}
function pick(btn,v,a,bId,fId){var bl=document.getElementById(bId),fb=document.getElementById(fId);if(v===a){btn.classList.add('ok');if(bl)bl.textContent=v;btn.parentElement.querySelectorAll('.ch').forEach(function(b){b.disabled=true;});setTimeout(function(){fb.style.color='var(--sage)';fb.textContent='\\u2705 정답! +20 XP';addXP(20);},400);}else{btn.classList.add('no');fb.style.color='#e53935';fb.textContent='\\u274C 다시 해봐!';setTimeout(function(){btn.classList.remove('no');fb.textContent='';},1200);}}
function woAdd(id,btn,w){if(btn.classList.contains('used'))return;btn.classList.add('used');if(!woPools[id])woPools[id]=[];woPools[id].push(w);var z=document.getElementById(id+'-zone'),ph=document.getElementById(id+'-ph');if(ph)ph.style.display='none';var c=document.createElement('button');c.className='placed';c.textContent=w;c.onclick=function(){var i=woPools[id].indexOf(w);if(i>-1)woPools[id].splice(i,1);btn.classList.remove('used');c.remove();if(!woPools[id].length&&ph)ph.style.display='';};z.appendChild(c);}
function woChk(id,ans,fId){var g=(woPools[id]||[]).join(' '),fb=document.getElementById(fId);if(g===ans){setTimeout(function(){fb.style.color='var(--sage)';fb.textContent='\\u2705 완벽해! +30 XP';addXP(30);},400);}else{fb.style.color='#e53935';fb.textContent='\\u274C 다시! 정답: "'+ans+'"';setTimeout(function(){fb.textContent='';},2500);}}
function woRst(id){woPools[id]=[];var z=document.getElementById(id+'-zone');z.innerHTML='<span class="build-ph" id="'+id+'-ph">\\uD83D\\uDC46 아래 단어를 눌러봐!</span>';document.querySelectorAll('#'+id+'-pool .wchip').forEach(function(w){w.classList.remove('used');});}
function mClick(el,k){if(el.classList.contains('ok'))return;if(!mSel){mSel=el;el.classList.add('sel');return;}if(mSel===el){el.classList.remove('sel');mSel=null;return;}var ak=mSel.getAttribute('onclick').match(/'([^']+)'/)[1];if(ak===k){mSel.classList.remove('sel');mSel.classList.add('ok');el.classList.add('ok');mPairs[ak]=true;var d=Object.keys(mPairs).length,fb=document.getElementById('mfb');fb.style.color='var(--sage)';if(d>=4){setTimeout(function(){fb.textContent='\\uD83C\\uDF89 모두 맞췄어! +20 XP';addXP(20);},400);}else fb.textContent='\\uD83D\\uDC4D '+d+'개!';mSel=null;}else{mSel.classList.remove('sel');mSel.classList.add('no');el.classList.add('no');var a=mSel;setTimeout(function(){a.classList.remove('no');el.classList.remove('no');},600);mSel=null;}}
function qChk(btn,t){if(t==='ok'){btn.parentElement.querySelectorAll('.qo').forEach(function(o){o.disabled=true;});btn.classList.add('ok');qOk++;setTimeout(function(){addXP(20);},400);if(qOk>=2)setTimeout(function(){var fxp=document.getElementById('fxp');if(fxp)fxp.textContent=xp;var c=document.getElementById('done-card');if(c){c.classList.add('show');c.scrollIntoView({behavior:'smooth'});}},1000);}else{btn.classList.add('no');setTimeout(function(){btn.classList.remove('no');},1000);}}
function listenChk(btn,t){var fb=document.getElementById('listen-fb');if(t==='ok'){btn.classList.add('ok');btn.parentElement.querySelectorAll('.listen-opt').forEach(function(b){b.disabled=true;b.style.pointerEvents='none';});setTimeout(function(){fb.style.color='var(--sage)';fb.textContent='\\u2705 정답! +20 XP';addXP(20);},400);}else{btn.classList.add('no');fb.style.color='#e53935';fb.textContent='\\u274C 다시 들어봐!';setTimeout(function(){btn.classList.remove('no');fb.textContent='';},1200);}}
function chkDict(ans){var v=document.getElementById('dictIn').value.trim().toLowerCase(),fb=document.getElementById('dict-fb');if(v===ans.toLowerCase()){fb.style.color='var(--sage)';setTimeout(function(){fb.textContent='\\u2705 정답! +25 XP';addXP(25);},400);document.getElementById('dictIn').style.borderColor='var(--sage)';}else if(!v.length){fb.textContent='\\u270F\\uFE0F 써봐!';}else{fb.style.color='#e53935';fb.textContent='\\u274C 힌트: '+ans[0]+'...';}}
function chkWrite(){var v=document.getElementById('wInput').value.trim(),fb=document.getElementById('wfb');if(v.length>3){fb.style.color='var(--sage)';fb.textContent='\\u2705 잘 썼어! +25 XP';addXP(25);}else{fb.textContent='\\u270F\\uFE0F 조금 더 써봐!';}}
function copyPrompt(){var el=document.getElementById('promptBody'),text=el?el.textContent:'';var modal=document.createElement('div');modal.style.cssText='position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px;';var box=document.createElement('div');box.style.cssText='background:#1a2a3a;border-radius:16px;padding:20px;width:100%;max-width:560px;';var ta=document.createElement('textarea');ta.value=text;ta.style.cssText='width:100%;height:180px;background:#0d1b2a;color:rgba(255,255,255,0.8);border:1px solid rgba(255,255,255,0.15);border-radius:10px;padding:12px;font-family:monospace;font-size:0.75rem;line-height:1.7;resize:none;';var hdr=document.createElement('div');hdr.style.cssText='color:#c9a028;font-size:0.8rem;font-weight:700;margin-bottom:8px;';hdr.textContent='\\uD83D\\uDCCB Ctrl+A \\u2192 Ctrl+C';var btns=document.createElement('div');btns.style.cssText='display:flex;gap:8px;margin-top:12px;';var copyBtn=document.createElement('button');copyBtn.textContent='\\uD83D\\uDCCB 복사';copyBtn.style.cssText='flex:1;padding:10px;background:#19c37d;color:#fff;border:none;border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;';copyBtn.onclick=function(){ta.select();try{document.execCommand('copy');}catch(e){}copyBtn.textContent='\\u2705 복사됨!';setTimeout(function(){copyBtn.textContent='\\uD83D\\uDCCB 복사';},1500);};var closeBtn=document.createElement('button');closeBtn.textContent='닫기';closeBtn.style.cssText='padding:10px 18px;background:rgba(255,255,255,0.1);color:#fff;border:none;border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;';closeBtn.onclick=function(){modal.remove();};btns.appendChild(copyBtn);btns.appendChild(closeBtn);box.appendChild(hdr);box.appendChild(ta);box.appendChild(btns);modal.appendChild(box);document.body.appendChild(modal);setTimeout(function(){ta.focus();ta.select();},100);modal.addEventListener('click',function(e){if(e.target===modal)modal.remove();});}"""
    return base

def speak_attr(grade, text):
    """Generate speak trigger based on grade."""
    esc = text.replace("'", "\\'").replace('"', '&quot;')
    if grade <= 4:
        return f"onclick=\"speak('{esc}')\""
    else:
        return f'data-speak="{esc}" onclick="speakEl(this)"'

def speak_btn(grade, text):
    """Generate play button based on grade."""
    esc = text.replace("'", "\\'").replace('"', '&quot;')
    if grade <= 4:
        return f"<button class=\"play-btn\" onclick=\"event.stopPropagation();speak('{esc}')\">▶</button>"
    else:
        return f'<button class="play-btn" data-speak="{esc}" onclick="event.stopPropagation();speakEl(this)">▶</button>'

def vocab_speak(grade, word):
    esc = word.replace("'", "\\'").replace('"', '&quot;')
    if grade <= 4:
        card_attr = f'onclick="speak(\'{esc}\')"'
        btn = f'<button class="v-play" onclick="event.stopPropagation();speak(\'{esc}\')">듣기</button>'
    else:
        card_attr = f'data-speak="{esc}" onclick="speakEl(this)"'
        btn = f'<button class="v-play" data-speak="{esc}" onclick="event.stopPropagation();speakEl(this)">듣기</button>'
    return card_attr, btn

def listen_speak(grade, text):
    esc = text.replace("'", "\\'").replace('"', '&quot;')
    if grade <= 4:
        return f'onclick="speak(\'{esc}\')"'
    else:
        return f'data-speak="{esc}" onclick="speakEl(this)"'

def dict_speak(grade, word):
    esc = word.replace("'", "\\'")
    if grade <= 4:
        return f'onclick="speak(\'{esc}\')"'
    else:
        return f'data-speak="{esc}" onclick="speakEl(this)"'


def generate_file(book_data, week_num, day_key):
    """Generate a single HTML file."""
    d = book_data["weeks"][week_num][day_key]
    suffix, day_label, dots, day_kr = DAY_MAP[day_key]
    grade = book_data["grade"]
    quarter = book_data["quarter"]
    book = book_data["book"]
    book_kr = book_data["book_kr"]
    emoji = book_data["emoji"]
    img = book_data["img"]
    level = book_data["level"]
    ratio = book_data["ratio"]

    wk = f"{week_num:02d}" if week_num < 10 else str(week_num)

    # Day badges
    week_data = book_data["weeks"][week_num]
    d1_en = week_data["d1"]["key_en"]
    d2_en = week_data["d2"]["key_en"]

    if day_key == "d1":
        badges = f'<span class="day-pill today">● Day 1 ({day_kr}) &quot;{d1_en}&quot;</span><span class="day-pill future">○ Day 2 (수)</span><span class="day-pill future">○ Day 3 (금) 완성!</span>'
    elif day_key == "d2":
        badges = f'<span class="day-pill done">● Day 1 (월)</span><span class="day-pill today">● Day 2 ({day_kr}) &quot;{d2_en}&quot;</span><span class="day-pill future">○ Day 3 (금) 완성!</span>'
    else:
        badges = f'<span class="day-pill done">● Day 1 (월)</span><span class="day-pill done">● Day 2 (수)</span><span class="day-pill today">● Day 3 ({day_kr}) 완성!</span>'

    # Navigation
    day_num = {"d1": 1, "d2": 2, "d3": 3}[day_key]
    if day_key == "d1":
        prev_link = f'<span class="bp" style="opacity:0.3;">← 이전</span>'
        next_link = f'<a class="bn" href="week{wk}b.html">Day 2 →</a>'
        next_card_title = f"Day 2 — {d2_en}"
        next_href = f"week{wk}b.html"
    elif day_key == "d2":
        prev_link = f'<a class="bp" href="week{wk}a.html">← Day 1</a>'
        next_link = f'<a class="bn" href="week{wk}c.html">Day 3 →</a>'
        next_card_title = "Day 3 — 완성!"
        next_href = f"week{wk}c.html"
    else:
        prev_link = f'<a class="bp" href="week{wk}b.html">← Day 2</a>'
        # Next week or end
        next_weeks = sorted(book_data["weeks"].keys())
        idx = next_weeks.index(week_num)
        if idx + 1 < len(next_weeks):
            nw = next_weeks[idx + 1]
            nwk = f"{nw:02d}" if nw < 10 else str(nw)
            next_link = f'<a class="bn" href="week{nwk}a.html">Week {nw} →</a>'
            next_card_title = f"Week {nw} Day 1"
            next_href = f"week{nwk}a.html"
        else:
            next_link = '<span class="bp" style="opacity:0.3;">완료! 🎉</span>'
            next_card_title = f"{book} 완료!"
            next_href = "#"

    # Story play text (flatten)
    story_play_text = d["story_en"].replace("\n", " ").replace("'", "\\'")

    # Vocab
    vocab_html = ""
    for eng, kr, emj, ex in d["vocab"]:
        ca, btn = vocab_speak(grade, eng)
        vocab_html += f'<div class="v-card" {ca}><div class="v-emoji">{emj}</div><div class="v-eng">{eng}</div><div class="v-kr">{kr}</div><div class="v-ex">&quot;{ex.strip(chr(34))}&quot;</div>{btn}</div>'

    # Matching - shuffle Korean side
    import random
    random.seed(week_num * 10 + {"d1":1,"d2":2,"d3":3}[day_key])
    match_left = ""
    match_right_items = []
    for eng, kr, _, _ in d["vocab"]:
        match_left += f"<button class=\"m-btn\" onclick=\"mClick(this,'{eng}')\">{eng}</button>"
        match_right_items.append((eng, kr))
    random.shuffle(match_right_items)
    match_right = ""
    for eng, kr in match_right_items:
        match_right += f"<button class=\"m-btn\" onclick=\"mClick(this,'{eng}')\">{kr}</button>"

    # Word order chips
    wo_chips = ""
    for w in d["wo_words"]:
        wo_chips += f"<button class=\"wchip\" onclick=\"woAdd('wo1',this,'{w}')\">{w}</button>"

    # Key play row
    key_en_esc = d["key_en"].replace("'", "\\'").replace('"', '&quot;')
    if grade <= 4:
        key_play = f"""<div class="key-play-row" onclick="speak('{key_en_esc}')">
          <button class="play-btn" onclick="event.stopPropagation();speak('{key_en_esc}')">▶</button>
          <div><div class="play-label">🔊 발음 듣기 — 따라 해봐!</div><div class="play-hint">버튼을 누르면 영어 발음이 나와요</div></div></div>"""
    else:
        key_play = f"""<div class="key-play-row" data-speak="{key_en_esc}" onclick="speakEl(this)">
          <button class="play-btn" data-speak="{key_en_esc}" onclick="event.stopPropagation();speakEl(this)">▶</button>
          <div><div class="play-label">🔊 발음 듣기 — 따라 해봐!</div><div class="play-hint">버튼을 누르면 영어 발음이 나와요</div></div></div>"""

    listen_attr = listen_speak(grade, d["listen_text"])
    dict_attr = dict_speak(grade, d["dict_word"])

    # Story HTML with line breaks
    story_en_html = d["story_en"].replace("\n", "<br>")
    # Highlight key sentence
    key_plain = d["key_en"]
    if key_plain in story_en_html:
        story_en_html = story_en_html.replace(key_plain, f'<span class="hl">{key_plain}</span>')

    story_kr_html = d["story_kr"].replace("\n", "<br>")

    # Prompt body
    vocab_list = ", ".join([f"{e}({k})" for e, k, _, _ in d["vocab"]])
    prompt_body = f"""[CEC English Camp - Grade {grade} {quarter} Week {week_num} {day_label} {book}]

안녕하세요 선생님! G{grade} 오늘 {day_label} 수업을 마쳤어요.

오늘 핵심 표현: &quot;{d['key_en']}&quot;
오늘 단어: {vocab_list}

[STEP 1] 핵심 표현 확인
[STEP 2] 단어 퀴즈
[STEP 3] 이야기 이해 질문
[STEP 4] 자유 말하기
[STEP 5] 마무리

{ratio}
시작해볼까요!"""

    # Pick choices
    pick_choices_html = ""
    for c in d["pick_choices"]:
        pick_choices_html += f"<button class=\"ch\" onclick=\"pick(this,'{c}','{d['pick_ans']}','b1','f1')\">{c}</button>"

    # Write choices
    write_choices_html = f"""<button class="ch" onclick="pick(this,'{d['write_c1']}','{d['write_ans']}','bw','fw')">{d['write_c1']}</button><button class="ch" onclick="pick(this,'{d['write_c2']}','{d['write_ans']}','bw','fw')">{d['write_c2']}</button><button class="ch" onclick="pick(this,'{d['write_c3']}','{d['write_ans']}','bw','fw')">{d['write_c3']}</button>"""

    css = gen_css_g4()
    js = gen_js(grade)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>G{grade} {quarter} W{week_num} {day_label} - {book} | CEC Camp A</title>
<meta name="description" content="CEC English Camp Grade {grade} {quarter} Week {week_num} {day_label} - {book} ({book_kr}) 영어 학습">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body data-camp="a" data-grade="{grade}" data-week="{week_num}" data-quarter="{quarter}">
<header class="topbar">
  <div class="top-left">
    <video src="{R2}/robo.mp4" autoplay loop muted playsinline style="width:40px;height:40px;border-radius:12px;object-fit:cover;flex-shrink:0;"></video>
    <div><div class="top-title">CEC Camp A 초등{grade}</div><div class="top-sub">{book} · {quarter} W{week_num} {day_label} {dots}</div></div>
  </div>
  <div style="display:flex;align-items:center;gap:8px;">
    <div class="xp-pill">⭐ <span id="xp">0</span> XP</div>
    <button class="ai-tutor-btn" onclick="window.open('{GPT_URL}','_blank')">🤖 AI 튜터</button>
  </div>
</header>
<main class="container">

<div class="hero-wrap"><div class="hero-img-wrap">
  <img class="scene-img" src="{img}" alt="{book} Week {week_num}" style="max-height:300px;">
  <div class="hero-overlay">
    <h2>{emoji} {book} — {quarter} Week {week_num} {day_label}</h2>
    <p>{d['key_kr']}</p>
    <div class="day-badge">{badges}</div>
  </div>
</div></div>

<div class="robo">
  <div class="robo-av"><img src="{R2}/robo.png" alt="Robo"></div>
  <div><div class="robo-nm">Robo 선생님</div><div class="robo-msg">{day_label}에 온 걸 환영해! 🎉<br>오늘의 핵심: <b>&quot;{d['key_en']}&quot;</b></div></div>
</div>

<!-- 섹션 1: 핵심 표현 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:var(--gold);">1</div>
  <div><div class="sec-title">오늘의 핵심 표현</div><div class="sec-sub">KEY SENTENCE · {quarter} · {level}</div></div>
</div><div class="sec-body">
  <div class="key-card">
    <div class="key-eyebrow">⭐ {quarter} · Week {week_num} · {day_label} · {level}</div>
    <div class="key-eng">&quot;{d['key_en']}&quot;</div>
    <div class="key-kr">{d['key_kr']}</div>
    {key_play}
  </div>
</div><div class="prog"><div class="prog-fill" style="width:10%;"></div></div></div>

<!-- 섹션 2: 이야기 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:var(--coral);">2</div>
  <div><div class="sec-title">오늘의 이야기 📖</div><div class="sec-sub">SHORT STORY</div></div>
</div>
<div style="position:relative;overflow:hidden;">
  <img class="scene-img" src="{img}" alt="{book}" style="max-height:240px;">
</div>
<div class="sec-body">
  <div class="robo" style="background:linear-gradient(135deg,#fdf6e3,#fdf8f0);border-color:rgba(218,165,32,0.25);">
    <div class="robo-av" style="border-color:var(--gold);"><img src="{R2}/robo.png" alt="Robo"></div>
    <div><div class="robo-nm" style="color:var(--gold);">먼저 한국어로 읽어봐!</div>
    <div class="robo-msg">{story_kr_html}</div></div>
  </div>
  <div class="story-player-row">
    <span class="story-label">🔤 English Story</span>
    <button class="story-ctrl-btn story-play-btn" id="story-play-btn" onclick="storyPlay('{story_play_text}')">▶</button>
    <button class="story-ctrl-btn story-stop-btn" id="story-stop-btn" onclick="storyStopped()">⏹</button>
    <span style="font-size:0.72rem;color:var(--text3);">재생 / 정지</span>
  </div>
  <div class="story-en">{story_en_html}</div>
</div><div class="prog"><div class="prog-fill" style="width:22%;"></div></div></div>

<!-- 섹션 3: 단어 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:var(--sky);">3</div>
  <div><div class="sec-title">핵심 단어 4개!</div><div class="sec-sub">KEY WORDS · Click to hear!</div></div>
</div><div class="sec-body">
  <div class="vocab-grid">{vocab_html}</div>
</div><div class="prog"><div class="prog-fill" style="width:35%;"></div></div></div>

<!-- 섹션 4: 단어 고르기 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:var(--sage);">4</div>
  <div><div class="sec-title">게임 1: 단어 고르기! 🎮</div><div class="sec-sub">WORD PICK</div></div>
</div><div class="sec-body">
  <div class="game-box">
    <div class="game-q">빈칸에 알맞은 단어를 골라봐!</div>
    <div style="text-align:center;font-size:1.2rem;font-weight:900;margin-bottom:14px;line-height:2;">&quot;{d['pick_blank']}&quot;</div>
    <div class="choices">{pick_choices_html}</div>
    <div class="fb" id="f1"></div>
  </div>
</div><div class="prog"><div class="prog-fill" style="width:50%;"></div></div></div>

<!-- 섹션 5: 문장 만들기 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:var(--brown);">5</div>
  <div><div class="sec-title">게임 2: 문장 만들기! 🧩</div><div class="sec-sub">WORD ORDER</div></div>
</div><div class="sec-body">
  <div class="game-box" style="background:linear-gradient(135deg,#fdf6e3,#fdf8f0);">
    <div class="game-q">{d['wo_kr']}</div>
    <div class="build-zone" id="wo1-zone"><span class="build-ph" id="wo1-ph">👆 아래 단어를 눌러봐!</span></div>
    <div class="wpool" id="wo1-pool">{wo_chips}</div>
    <div class="game-btns">
      <button class="btn-ok" onclick="woChk('wo1','{d['wo_ans']}','wo1-fb')">확인!</button>
      <button class="btn-rst" onclick="woRst('wo1')">다시</button>
    </div>
    <div class="fb" id="wo1-fb"></div>
  </div>
</div><div class="prog"><div class="prog-fill" style="width:55%;"></div></div></div>

<!-- 섹션 6: 짝맞추기 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:var(--coral);">6</div>
  <div><div class="sec-title">게임 3: 짝맞추기! 🃏</div><div class="sec-sub">MATCHING</div></div>
</div><div class="sec-body">
  <div class="game-box">
    <div style="text-align:center;font-size:0.85rem;font-weight:700;margin-bottom:12px;">👆 왼쪽 → 오른쪽 뜻!</div>
    <div class="match-grid">
      <div class="match-col" id="ml">{match_left}</div>
      <div class="match-col" id="mr">{match_right}</div>
    </div>
    <div class="fb" id="mfb"></div>
  </div>
</div><div class="prog"><div class="prog-fill" style="width:65%;"></div></div></div>

<!-- 듣기 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:#e91e63;">♪</div>
  <div><div class="sec-title">👂 들어보자!</div><div class="sec-sub">LISTENING</div></div>
</div><div class="sec-body">
  <button class="listen-play" {listen_attr}>🔊 듣기!</button>
  <div class="listen-opts">
    <button class="listen-opt" onclick="listenChk(this,'ok')"><div class="lo-emoji">✅</div><div class="lo-label">{d['listen_ok']}</div></button>
    <button class="listen-opt" onclick="listenChk(this,'no')"><div class="lo-emoji">❌</div><div class="lo-label">{d['listen_no1']}</div></button>
    <button class="listen-opt" onclick="listenChk(this,'no')"><div class="lo-emoji">❌</div><div class="lo-label">{d['listen_no2']}</div></button>
  </div>
  <div class="fb" id="listen-fb" style="margin-top:10px;"></div>
</div><div class="prog"><div class="prog-fill" style="width:72%;"></div></div></div>

<!-- 받아쓰기 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:var(--gold);">✎</div>
  <div><div class="sec-title">✍️ 써보자!</div><div class="sec-sub">DICTATION</div></div>
</div><div class="sec-body">
  <button class="dict-play" {dict_attr}>🔊 단어 듣기</button>
  <div class="dict-hint">{d['dict_hint']}</div>
  <input class="dict-input" id="dictIn" placeholder="단어를 써봐!" onkeydown="if(event.key==='Enter')chkDict('{d['dict_word']}')">
  <button class="dict-check" onclick="chkDict('{d['dict_word']}')">확인</button>
  <div class="fb" id="dict-fb" style="margin-top:10px;"></div>
</div><div class="prog"><div class="prog-fill" style="width:78%;"></div></div></div>

<!-- 섹션 7: 이해 문제 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:var(--sky);">7</div>
  <div><div class="sec-title">이해 문제! ❓</div><div class="sec-sub">QUIZ</div></div>
</div><div class="sec-body">
  <div class="quiz-box">
    <div class="quiz-q">Q1. {d['q1']}</div>
    <div class="quiz-opts"><button class="qo" onclick="qChk(this,'ok')">{d['q1_ok']}</button><button class="qo" onclick="qChk(this,'no')">{d['q1_no1']}</button><button class="qo" onclick="qChk(this,'no')">{d['q1_no2']}</button></div>
  </div>
  <div class="quiz-box">
    <div class="quiz-q">Q2. {d['q2']}</div>
    <div class="quiz-opts"><button class="qo" onclick="qChk(this,'ok')">{d['q2_ok']}</button><button class="qo" onclick="qChk(this,'no')">{d['q2_no1']}</button><button class="qo" onclick="qChk(this,'no')">{d['q2_no2']}</button></div>
  </div>
</div><div class="prog"><div class="prog-fill" style="width:85%;"></div></div></div>

<!-- 섹션 8: 한 줄 쓰기 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:var(--gold);">8</div>
  <div><div class="sec-title">한 줄 쓰기! ✍️</div><div class="sec-sub">WRITING</div></div>
</div><div class="sec-body">
  <div class="game-box">
    <div class="game-q">📝 빈칸에 알맞은 말을 골라봐!</div>
    <div style="text-align:center;font-size:1.1rem;font-weight:900;margin-bottom:12px;line-height:2;">&quot;{d['write_blank']}&quot;</div>
    <div class="choices">{write_choices_html}</div>
    <div class="fb" id="fw"></div>
  </div>
  <div class="write-box">
    <div style="font-size:0.82rem;color:var(--text3);margin-bottom:8px;">🖊️ {d['write_prompt']}</div>
    <input class="write-input" id="wInput" placeholder="영어로 써봐!">
    <button class="write-btn" onclick="chkWrite()">제출!</button>
    <div class="fb" id="wfb" style="margin-top:8px;"></div>
  </div>
</div><div class="prog"><div class="prog-fill" style="width:92%;"></div></div></div>

<!-- 섹션 9: AI 튜터 -->
<div class="card"><div class="sec-hdr"><div class="sec-num" style="background:#00b894;">9</div>
  <div><div class="sec-title">AI 튜터 ChatGPT 🤖</div><div class="sec-sub">오늘 배운 것을 ChatGPT와 연습해봐!</div></div>
</div><div class="sec-body">
  <div class="ai-box">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
      <img src="{R2}/robo_jump.gif" alt="Robo" style="width:48px;height:48px;object-fit:contain;">
      <div><div class="ai-box-title">AI 튜터 — {quarter} Week {week_num} {day_label}</div><div class="ai-box-desc">오늘 배운 내용을 ChatGPT 선생님과 연습해봐요!</div></div>
    </div>
    <div class="prompt-block">
      <div class="prompt-lbl">📋 ChatGPT 전달사항 <button class="copy-btn" onclick="copyPrompt()">📋 복사</button></div>
      <div class="prompt-text" id="promptBody">{prompt_body}</div>
    </div>
    <div class="ai-steps">
      <div class="ai-step"><div class="step-num">1</div><div>📋 <b style="color:#fff">복사</b> 버튼 클릭</div></div>
      <div class="ai-step"><div class="step-num">2</div><div><b style="color:#fff">ChatGPT 열기</b> 클릭</div></div>
      <div class="ai-step"><div class="step-num">3</div><div>채팅창에 <b style="color:#fff">붙여넣기(Ctrl+V)</b> 후 Enter</div></div>
      <div class="ai-step"><div class="step-num">4</div><div>AI 선생님 질문에 <b style="color:#fff">영어로</b> 답해봐요!</div></div>
    </div>
    <div class="ai-btn-row">
      <a href="{GPT_URL}" target="_blank" class="ai-btn-primary">🚀 ChatGPT 열기</a>
      <button class="ai-btn-sec" onclick="copyPrompt()">📋 전달사항 복사</button>
    </div>
  </div>
</div><div class="prog"><div class="prog-fill" style="width:100%;"></div></div></div>

<!-- 완료 카드 -->
<div class="complete" id="done-card">
  <div class="complete-emoji">{emoji}🎉🏆</div>
  <div class="complete-title">{day_label} 완료! {dots}</div>
  <div class="complete-sub">핵심 표현: <strong>&quot;{d['key_en']}&quot;</strong> ✅<br>단어 4개 완성! ✅</div>
  <div class="xp-big">🏆 총 <span id="fxp">0</span> XP!</div>
  <div class="robo" style="text-align:left;">
    <div class="robo-av"><img src="{R2}/robo.png" alt="Robo"></div>
    <div><div class="robo-nm">Robo</div><div class="robo-msg">다음 수업에서 계속해요! 🌟</div></div>
  </div>
  <div style="margin-top:14px;"><div class="next-card">
    <div style="flex:1;"><div class="next-label">📅 다음 수업</div><div class="next-title">{next_card_title}</div></div>
    <a href="{next_href}" class="next-btn">다음 →</a>
  </div></div>
</div>

</main>
<div class="bnav">
  {prev_link}
  <span class="bl">{quarter} · W{week_num} · {day_label}</span>
  {next_link}
</div>
<script>
{js}
</script>
</body></html>"""

    return html


def main():
    count = 0
    for book_key, book_data in BOOKS.items():
        grade = book_data["grade"]
        grade_dir = os.path.join(BASE, f"grade{grade}")
        os.makedirs(grade_dir, exist_ok=True)
        for week_num in sorted(book_data["weeks"].keys()):
            for day_key in ["d1", "d2", "d3"]:
                suffix = DAY_MAP[day_key][0]
                wk = str(week_num)
                filename = f"week{wk}{suffix}.html"
                filepath = os.path.join(grade_dir, filename)
                html = generate_file(book_data, week_num, day_key)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(html)
                count += 1
                print(f"  ✅ {filepath}")
    print(f"\n🎉 Total: {count} files generated!")


if __name__ == "__main__":
    main()

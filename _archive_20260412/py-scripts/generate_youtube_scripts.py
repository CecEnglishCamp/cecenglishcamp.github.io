#!/usr/bin/env python3
"""Generate 75 YouTube video scripts from CEC Camp A lesson HTML files."""

import os
import re
from html.parser import HTMLParser

LESSONS_BASE = r"C:\Users\cecsu\cecenglishcamp.github.io\camp-a\lessons"
OUTPUT_BASE = r"C:\Users\cecsu\Desktop\youtube\camp-a"

# Files to generate
GRADE_WEEKS = {
    3: list(range(1, 5)),    # W01-W04
    4: list(range(1, 5)),    # W01-W04
    5: list(range(1, 10)),   # W01-W09
    6: list(range(1, 9)),    # W01-W08
}
DAYS = ['a', 'b', 'c']

BOOK_DESCRIPTIONS = {
    "Peter Rabbit": "말썽꾸러기 토끼 피터의 모험! 맥그리거 할아버지 정원에서 벌어지는 신나는 이야기예요.",
    "Wind in the Willows": "두더지 몰이 처음으로 밖으로 나가 친구를 만드는 이야기예요!",
    "Treasure Island": "Jim finds a treasure map and sails into danger, pirates, and adventure!",
    "Around the World in 80 Days": "Fogg bets he can travel the world in 80 days!",
    "Call of the Wild": "Buck is taken from home and must survive in the wild.",
    "Anne of Green Gables": "Anne arrives at Green Gables — different but full of imagination!",
    "A Little Princess": "Sara loses everything but keeps her dignity and imagination.",
    "Five Children and It": "Five children find a magical creature that grants wishes!",
    "Jungle Book": "Mowgli grows up in the jungle, caught between two worlds.",
    "Pinocchio": "A wooden puppet learns that lies have consequences.",
    "Phantom Tollbooth": "Bored Milo discovers a magical world of words and numbers.",
    "Little Women": "Four sisters each choose their own path in life.",
    "Emil and the Detectives": "Emil catches a thief with help from brave city kids.",
}

def strip_html(text):
    """Remove HTML tags, convert <br> to newlines, decode entities."""
    if not text:
        return ""
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&#39;', "'").replace('&apos;', "'")
    # Decode \xNN hex escapes
    text = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), text)
    return text.strip()


def read_html(filepath):
    """Read HTML file and return content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def extract_title_book(html):
    """Extract book title from <title> tag: between '- ' or '— ' and ' |'."""
    m = re.search(r'<title>[^<]*?[-—]\s*(.+?)\s*\|', html)
    if m:
        return m.group(1).strip()
    return ""


def extract_key_sentence(html):
    """Extract from class='key-eng'."""
    m = re.search(r'class="key-eng"[^>]*>(.*?)</div>', html, re.DOTALL)
    if m:
        return strip_html(m.group(1))
    return ""


def extract_key_kr(html):
    """Extract from class='key-kr'."""
    m = re.search(r'class="key-kr"[^>]*>(.*?)</div>', html, re.DOTALL)
    if m:
        return strip_html(m.group(1))
    return ""


def extract_korean_story(html):
    """Extract Korean story from robo-msg in section 2."""
    # Find section 2 area first
    sec2_match = re.search(r'<div class="sec-num"[^>]*>2</div>', html)
    if not sec2_match:
        return ""
    section2_html = html[sec2_match.start():]
    m = re.search(r'class="robo-msg"[^>]*>(.*?)</div>', section2_html, re.DOTALL)
    if m:
        return strip_html(m.group(1))
    return ""


def extract_stories(html):
    """Extract A1, A2, B1 stories from story-en divs."""
    stories = re.findall(r'<div class="story-en"[^>]*>(.*?)</div>', html, re.DOTALL)
    a1 = strip_html(stories[0]) if len(stories) > 0 else ""
    a2 = strip_html(stories[1]) if len(stories) > 1 else ""
    b1 = strip_html(stories[2]) if len(stories) > 2 else ""
    return a1, a2, b1


def extract_vocab(html):
    """Extract vocab word pairs (eng, kr) from v-eng and v-kr."""
    # Find section 3 (vocab section)
    engs = re.findall(r'class="v-eng"[^>]*>(.*?)</div>', html, re.DOTALL)
    krs = re.findall(r'class="v-kr"[^>]*>(.*?)</div>', html, re.DOTALL)
    vocab = []
    for i in range(min(len(engs), len(krs))):
        vocab.append((strip_html(engs[i]), strip_html(krs[i])))
    return vocab


def extract_quarter(html):
    """Extract data-quarter value."""
    m = re.search(r'data-quarter="([^"]*)"', html)
    return m.group(1) if m else "Q1"


def get_html_path(grade, week, day):
    """Get path to HTML file."""
    return os.path.join(LESSONS_BASE, f"grade{grade}", f"week{week:02d}{day}.html")


def get_day_number(day_letter):
    """a->1, b->2, c->3"""
    return {'a': 1, 'b': 2, 'c': 3}[day_letter]


def make_example_sentence(word_eng, grade):
    """Generate a simple example sentence for a vocab word."""
    # Simple patterns
    w = word_eng.lower()
    examples = {
        'ran': 'The dog ran fast.',
        'away': 'The bird flew away.',
        'scared': 'The cat was scared.',
        'garden': 'I play in the garden.',
        'listen': 'Please listen to me.',
        'sneaked': 'He sneaked past the door.',
        'fast': 'She runs very fast.',
        'mother': 'My mother is kind.',
        'hide': 'Let\'s hide behind the tree.',
        'caught': 'He caught the ball.',
        'lost': 'I lost my pencil.',
        'found': 'She found a coin.',
        'shouted': 'He shouted for help.',
        'followed': 'The dog followed me.',
        'river': 'The river is long.',
        'boat': 'We rode a boat.',
        'friend': 'He is my friend.',
        'home': 'I went home.',
        'dark': 'It was dark outside.',
        'brave': 'She is very brave.',
        'treasure': 'They found the treasure.',
        'map': 'He looked at the map.',
        'island': 'The island was beautiful.',
        'danger': 'There is danger ahead.',
        'adventure': 'It was a great adventure.',
        'promise': 'I promise to help.',
        'promised': 'She promised to come.',
        'journey': 'The journey was long.',
        'ship': 'The ship sailed away.',
        'captain': 'The captain gave orders.',
        'pirate': 'The pirate found gold.',
        'sword': 'He drew his sword.',
        'escape': 'They planned to escape.',
        'secret': 'It was a secret plan.',
        'wild': 'The wild dog howled.',
        'survive': 'They had to survive.',
        'strength': 'He showed great strength.',
        'imagine': 'Can you imagine that?',
        'imagination': 'She has great imagination.',
        'dignity': 'She kept her dignity.',
        'wish': 'I wish for a pet.',
        'magic': 'It was pure magic.',
        'jungle': 'The jungle was thick.',
        'village': 'The village was small.',
        'wooden': 'It was a wooden box.',
        'lie': 'Don\'t tell a lie.',
        'truth': 'Tell the truth.',
        'discover': 'Let\'s discover new things.',
        'path': 'Follow the path.',
        'sister': 'My sister is tall.',
        'thief': 'The thief ran away.',
        'detective': 'The detective solved it.',
    }
    if w in examples:
        return examples[w]
    # Generic
    return f"I like the word {word_eng}."


def generate_g3g4_script(grade, week, day_letter, html, day1_key, day2_key, day3_key):
    """Generate script for G3/G4."""
    day_num = get_day_number(day_letter)
    book_title = extract_title_book(html)
    key_sentence = extract_key_sentence(html)
    key_kr = extract_key_kr(html)
    korean_story = extract_korean_story(html)
    a1, a2, b1 = extract_stories(html)
    vocab = extract_vocab(html)

    lines = []

    # Welcome (only week01a)
    if week == 1 and day_letter == 'a':
        lines.append("[KO] 안녕하세요! CEC 영어캠프에 오신 걸 환영해요!")
        lines.append("여기서 재미있는 영어 이야기와 게임으로 영어를 배워요!")
        lines.append("")

    # Book intro (only "a" files)
    if day_letter == 'a' and book_title:
        desc = BOOK_DESCRIPTIONS.get(book_title, f"{book_title} 이야기를 함께 읽어요!")
        lines.append(f"[KO] 이번 주부터 새로운 책 {book_title}을 읽어요!")
        lines.append(desc)
        lines.append("")

    # Weekly goals
    lines.append("[KO] 이번 주 학습 목표:")
    lines.append(f"Day 1: {day1_key}")
    lines.append(f"Day 2: {day2_key}")
    lines.append(f"Day 3: {day3_key}")
    lines.append(f"오늘은 Day {day_num}! 시작해볼까요?")
    lines.append("")

    # Key sentence
    lines.append("[KO] 오늘의 핵심 표현이에요!")
    lines.append(key_sentence)
    lines.append(f"한 번 더! {key_sentence}")
    lines.append(f"또 한 번! {key_sentence}")
    lines.append(key_kr)
    # Break down key words
    words_in_key = [w for w in re.findall(r"[A-Za-z']+", key_sentence) if len(w) > 2]
    if words_in_key:
        breakdown = ", ".join(words_in_key[:4])
        lines.append(f"핵심 단어: {breakdown}")
    lines.append("")

    # Korean story
    lines.append("[KO] 먼저 한국어로 이야기를 들어봐요!")
    lines.append(korean_story)
    lines.append("")

    # A1
    lines.append("[EN] Now let's listen in English! This is A1 — very easy!")
    lines.append(a1)
    lines.append("")

    # A1 brief explanation
    if grade == 3:
        lines.append(f"[KO] 잘 들었어요? 아주 짧은 이야기였죠! 핵심은 {key_sentence}예요!")
    else:
        lines.append(f"[KO] 잘 들었어요? A1은 기본 문장이에요. 핵심은 {key_sentence}!")
    lines.append("")

    # A2
    lines.append("[EN] Great job! Now A2 — a little harder!")
    lines.append(a2)
    lines.append("")

    if grade == 3:
        lines.append("[KO] A2는 조금 더 길었죠? 걱정 마세요, 천천히 배워요!")
    else:
        lines.append("[KO] A2는 조금 더 길었죠? 더 자세한 이야기를 들을 수 있었어요!")
    lines.append("")

    # Vocab
    lines.append("[KO] 오늘의 단어를 배워볼까요?")
    for i, (eng, kr) in enumerate(vocab[:4], 1):
        ex = make_example_sentence(eng, grade)
        lines.append(f"{i}. {eng} — {kr}. {ex}")
    lines.append("")

    # Games
    lines.append("[KO] 게임 시간이에요! 🎮")
    # Game 1: Fill in blank
    blank_word = ""
    blanked = key_sentence
    key_words = re.findall(r"[A-Za-z']+", key_sentence)
    if key_words:
        # Pick the most meaningful word (last content word)
        content_words = [w for w in key_words if w.lower() not in ('he', 'she', 'it', 'the', 'a', 'an', 'is', 'was', 'to', 'in', 'on', 'at', 'of')]
        if content_words:
            blank_word = content_words[-1]
        else:
            blank_word = key_words[-1]
        blanked = key_sentence.replace(blank_word, "______", 1)
    lines.append("게임 1: 빈칸을 채워봐요!")
    lines.append(f'"{blanked}" — 정답은? {blank_word}!')
    lines.append("")

    # Game 2: Match meaning
    lines.append("게임 2: 뜻 맞추기!")
    for eng, kr in vocab[:2]:
        lines.append(f"{eng}의 뜻은? {kr}!")
    lines.append("")

    # Game 3: Say in English
    lines.append("게임 3: 영어로 말해봐요!")
    lines.append(f'"{key_kr}" 를 영어로 하면? {key_sentence}!')
    lines.append("")

    # Closing
    if day_letter in ('a', 'b'):
        next_day = day_num + 1
        next_sentence = day2_key if day_letter == 'a' else day3_key
        lines.append(f"[KO] 다음 시간에는 Day {next_day}을 배워요!")
        lines.append(f"{next_sentence} — 기대되죠? 다음에 만나요!")
    else:
        lines.append("[KO] 이번 주 완성! 정말 잘했어요! 🎉")
    lines.append("")

    # Outro
    lines.append("[KO] 더 많은 게임과 AI 선생님 연습은")
    lines.append("cecenglishcamp.github.io 에서 만나요!")
    lines.append("사이트에서는 XP 포인트도 쌓을 수 있어요!")
    lines.append("유튜브 구독하고 다음 영상도 기다려주세요~")
    lines.append("[EN] See you next time! Keep going!")

    return "\n".join(lines)


def generate_g5g6_script(grade, week, day_letter, html, day1_key, day2_key, day3_key):
    """Generate script for G5/G6."""
    day_num = get_day_number(day_letter)
    book_title = extract_title_book(html)
    key_sentence = extract_key_sentence(html)
    key_kr = extract_key_kr(html)
    korean_story = extract_korean_story(html)
    a1, a2, b1 = extract_stories(html)
    vocab = extract_vocab(html)

    lines = []

    # Welcome (only week01a)
    if week == 1 and day_letter == 'a':
        lines.append("[EN] Welcome to CEC English Camp!")
        lines.append("Learn English through amazing stories and challenges!")
        lines.append("")

    # Book intro (only "a" files)
    if day_letter == 'a' and book_title:
        desc = BOOK_DESCRIPTIONS.get(book_title, f"An exciting story awaits in {book_title}!")
        lines.append(f"[EN] This week we begin {book_title}!")
        lines.append(desc)
        lines.append("")

    # Weekly goals
    lines.append("[EN] This week's learning goals:")
    lines.append(f"Day 1: {day1_key}")
    lines.append(f"Day 2: {day2_key}")
    lines.append(f"Day 3: {day3_key}")
    lines.append(f"Today is Day {day_num}! Let's begin!")
    lines.append("")

    # Key sentence
    lines.append("[EN] Today's key sentence!")
    lines.append(key_sentence)
    lines.append(f"One more time! {key_sentence}")
    lines.append(f"Again! {key_sentence}")
    # English explanation
    if grade == 5:
        lines.append(f"This means: {key_kr}")
        words_in_key = [w for w in re.findall(r"[A-Za-z']+", key_sentence) if len(w) > 3]
        if words_in_key:
            lines.append(f"Key vocabulary: {', '.join(words_in_key[:4])}")
    else:
        lines.append(f"In Korean, this means: {key_kr}")
        words_in_key = [w for w in re.findall(r"[A-Za-z']+", key_sentence) if len(w) > 3]
        if words_in_key:
            lines.append(f"Let's break it down: {', '.join(words_in_key[:5])}")
    lines.append("")

    # Korean story
    lines.append("[KO] 먼저 한국어로 이야기를 들어봐요.")
    lines.append(korean_story)
    lines.append("")

    # A1
    lines.append("[EN] A1 — Easy version:")
    lines.append(a1)
    lines.append("")

    # A2
    lines.append("[EN] A2 — Medium version:")
    lines.append(a2)
    lines.append("")

    # B1
    if b1:
        lines.append("[EN] B1 — Challenge version:")
        lines.append(b1)
        lines.append("")

    # Vocab
    lines.append("[EN] Vocabulary time!")
    for i, (eng, kr) in enumerate(vocab[:4], 1):
        ex = make_example_sentence(eng, grade)
        lines.append(f"{i}. {eng} — meaning: {kr}. Example: {ex}")
    lines.append("")

    # Games
    lines.append("[EN] Game time! 🎮")
    # Game 1
    blank_word = ""
    blanked = key_sentence
    key_words = re.findall(r"[A-Za-z']+", key_sentence)
    if key_words:
        content_words = [w for w in key_words if w.lower() not in ('he', 'she', 'it', 'the', 'a', 'an', 'is', 'was', 'to', 'in', 'on', 'at', 'of')]
        if content_words:
            blank_word = content_words[-1]
        else:
            blank_word = key_words[-1]
        blanked = key_sentence.replace(blank_word, "______", 1)
    lines.append("Game 1: Fill in the blank!")
    lines.append(f'"{blanked}" — Answer: {blank_word}!')
    lines.append("")

    # Game 2
    lines.append("Game 2: Match the meaning!")
    for eng, kr in vocab[:2]:
        lines.append(f"What does {eng} mean? {kr}!")
    lines.append("")

    # Game 3
    lines.append("Game 3: Say it in English!")
    lines.append(f'How do you say "{key_kr}" in English? {key_sentence}!')
    lines.append("")

    # Closing
    if day_letter in ('a', 'b'):
        next_day = day_num + 1
        next_sentence = day2_key if day_letter == 'a' else day3_key
        lines.append(f"[EN] Next time, Day {next_day}!")
        lines.append(f"{next_sentence} — See you then!")
    else:
        lines.append("[EN] Week complete! Amazing work! 🎉")
    lines.append("")

    # Outro
    lines.append("[EN] Visit cecenglishcamp.github.io")
    lines.append("Practice with your AI teacher and earn XP points!")
    lines.append("Subscribe for more lessons!")
    lines.append("[KO] 더 많은 수업은 cecenglishcamp.github.io에서!")

    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_BASE, exist_ok=True)

    total = 0
    errors = []

    for grade, weeks in GRADE_WEEKS.items():
        for week in weeks:
            # Pre-read all 3 days to get key sentences for weekly goals
            day_keys = {}
            day_htmls = {}
            for d in DAYS:
                path = get_html_path(grade, week, d)
                if os.path.exists(path):
                    html = read_html(path)
                    day_htmls[d] = html
                    day_keys[d] = extract_key_sentence(html)
                else:
                    errors.append(f"Missing: {path}")
                    day_htmls[d] = ""
                    day_keys[d] = "(not found)"

            day1_key = day_keys.get('a', '')
            day2_key = day_keys.get('b', '')
            day3_key = day_keys.get('c', '')

            for day_letter in DAYS:
                html = day_htmls[day_letter]
                if not html:
                    continue

                if grade in (3, 4):
                    script = generate_g3g4_script(grade, week, day_letter, html, day1_key, day2_key, day3_key)
                else:
                    script = generate_g5g6_script(grade, week, day_letter, html, day1_key, day2_key, day3_key)

                outname = f"g{grade}_week{week:02d}{day_letter}_script.txt"
                outpath = os.path.join(OUTPUT_BASE, outname)
                with open(outpath, 'w', encoding='utf-8') as f:
                    f.write(script)
                total += 1
                print(f"Generated: {outname}")

    print(f"\n=== Total files generated: {total} ===")
    if errors:
        print(f"\nWarnings ({len(errors)}):")
        for e in errors:
            print(f"  {e}")

    # Show content of g3_week01a
    sample_path = os.path.join(OUTPUT_BASE, "g3_week01a_script.txt")
    if os.path.exists(sample_path):
        print(f"\n{'='*60}")
        print(f"Content of g3_week01a_script.txt:")
        print(f"{'='*60}")
        with open(sample_path, 'r', encoding='utf-8') as f:
            print(f.read())


if __name__ == '__main__':
    main()

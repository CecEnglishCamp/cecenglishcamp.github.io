# Task 8-F1 Item 1 — Four-sample lesson context audit

Scope: the four lesson pages that currently call `POST /robo/v1/tutor`. This file records only context already present in those pages; it does not define the server schema or change browser payloads.

## 1. Camp A sample

- **lesson_id / source:** `/camp-a/grade3/week01a.html` — `camp-a/grade3/week01a.html`
- **Program:** CEC Camp A
- **Grade/course:** Elementary Grade 3; Q1; A1/A2 reading levels (key sentence card is labeled A2)
- **Week/day/topic:** Week 01, Day 1; Peter Rabbit escaping from Mr. McGregor's garden
- **Book/title:** *Peter Rabbit* / *The Tale of Peter Rabbit* by Beatrix Potter
- **Key sentence:** “He ran away.”
- **Vocabulary:** `ran`, `away`, `scared`, `garden`
- **Lesson text available:** A1 and A2 Peter Rabbit story passages; the page explains that Peter disobeys his mother, enters the garden, is discovered, becomes scared, and runs away.
- **Evidence:** page metadata and tutor call near lines 5–8 and 318–321/378; lesson header and content near lines 449–522.

## 2. Camp B sample

- **lesson_id / source:** `/camp-b/g1/week01a.html` — `camp-b/g1/week01a.html`
- **Program:** CEC Camp B
- **Grade/course:** High School 1 (`G1`); B1/B2 reading levels
- **Week/day/topic:** W01, Day 1; wealth, outsider/alienation, and the social world around Gatsby
- **Book/title:** *The Great Gatsby*
- **Key expressions:** Day 1 “Nick moved next door to a mysterious mansion.”; Day 2 “Nick moved to West Egg next to Gatsby's enormous mansion.”; Day 3 target sentence about Nick entering the world of the very rich, feeling like an outsider, and noticing careless cruelty.
- **Vocabulary:** `affluence`, `alienation`, `assimilating`, `paradox`, `transactional`
- **Lesson text available:** B1/B2 reading passages plus essay topic “What I think money actually does to people's character.”
- **Evidence:** page header and expressions near lines 599–639; exact `PAGE_DATA` near lines 1574–1589; tutor call near line 1132.

## 3. Camp C sample

- **lesson_id / source:** `/camp-c/ep01.html` — `camp-c/ep01.html`
- **Program:** CEC Camp C
- **Grade/course:** Adult situational English; Episode 01; page badge A2 Beginner with A1/A2/B1 story variants
- **Episode/topic:** Episode 01, Unit 1 — arriving at the airport and asking for help/directions
- **Book/title:** No book; page title is “Episode 01 — 공항에 도착”
- **Key expression:** “Excuse me. Can you help me?”
- **Vocabulary / expressions present:** `help`, `Terminal 2`, `Exit 5`, `go straight`, `turn left`, `near the coffee shop`
- **Lesson text available:** Korean story and A1/A2/B1 English versions about Young-ja arriving at Los Angeles airport, asking a worker for directions, and finding her daughter.
- **Evidence:** page/body metadata near lines 7 and 544; tutor call near line 607; episode badge, topic, and key expression near lines 708–739; story text near lines 814–914.

## 4. Grammar BaseCamp sample

- **lesson_id / source:** `/grammar-camp/G01/G01_be_verb_present_tense.html` — `grammar-camp/G01/G01_be_verb_present_tense.html`
- **Program:** CEC Grammar BaseCamp
- **Grade/course:** G01, Basic Grammar
- **Topic:** Be Verb: Present Tense — `am / is / are`
- **Book/title:** No book; lesson title is “G01. Be Verb: Present Tense”
- **Key grammar/expression:** “Be Verb — am / is / are”
- **Vocabulary / lesson text available:** subject-to-verb mapping (`I → am`, `He/She/It → is`, `You/We/They → are`), positive/negative/question patterns, contractions, and examples such as “I am a student,” “She is happy,” and “They are friends.”
- **Evidence:** page title and `data-grammar-id` near lines 7 and 165; lesson header and core rule content near lines 168–245; tutor call near line 682.

## Confirmed sample lesson IDs

1. `/camp-a/grade3/week01a.html`
2. `/camp-b/g1/week01a.html`
3. `/camp-c/ep01.html`
4. `/grammar-camp/G01/G01_be_verb_present_tense.html`

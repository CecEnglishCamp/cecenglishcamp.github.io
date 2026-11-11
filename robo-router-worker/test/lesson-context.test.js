import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  LESSON_CONTEXTS,
  lessonContextForLesson
} from '../src/lesson-context.js';
import { SAMPLE_LESSON_IDS } from '../src/lesson-context-schema.js';

test('server registry resolves exactly the four audited lessons', () => {
  assert.deepEqual(Object.keys(LESSON_CONTEXTS), SAMPLE_LESSON_IDS);

  for (const lessonId of SAMPLE_LESSON_IDS) {
    const context = lessonContextForLesson(lessonId);
    assert.ok(context);
    assert.equal(typeof context.program, 'string');
    assert.equal(typeof context.course, 'string');
    assert.equal(typeof context.topic, 'string');
    assert.ok(context.key_expressions.length > 0);
  }
});

test('server registry contains the audited context for each program', () => {
  assert.equal(
    lessonContextForLesson('/camp-a/grade3/week01a.html').book_title,
    'The Tale of Peter Rabbit by Beatrix Potter'
  );
  assert.equal(
    lessonContextForLesson('/camp-b/g1/week01a.html').vocabulary[0],
    'affluence'
  );
  assert.equal(
    lessonContextForLesson('/camp-c/ep01.html').sequence.episode,
    'Episode 01'
  );
  assert.equal(
    lessonContextForLesson('/grammar-camp/G01/G01_be_verb_present_tense.html').sequence.unit,
    'G01'
  );
});

test('lookup rejects unknown ids and registry data is immutable', () => {
  assert.equal(lessonContextForLesson('/camp-a/grade3/week02a.html'), null);
  assert.equal(lessonContextForLesson(null), null);
  assert.ok(Object.isFrozen(LESSON_CONTEXTS));
  assert.ok(Object.isFrozen(LESSON_CONTEXTS[SAMPLE_LESSON_IDS[0]]));
  assert.ok(Object.isFrozen(LESSON_CONTEXTS[SAMPLE_LESSON_IDS[0]].vocabulary));
});

import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  LESSON_CONTEXT_REGISTRY_SCHEMA,
  LESSON_CONTEXT_TRUST_BOUNDARY,
  LESSON_CONTEXT_VALUE_SCHEMA,
  SAMPLE_LESSON_IDS
} from '../src/lesson-context-schema.js';

const expectedLessonIds = [
  '/camp-a/grade3/week01a.html',
  '/camp-b/g1/week01a.html',
  '/camp-c/ep01.html',
  '/grammar-camp/G01/G01_be_verb_present_tense.html'
];

test('registry schema is keyed only by the four audited lesson ids', () => {
  assert.deepEqual(SAMPLE_LESSON_IDS, expectedLessonIds);
  assert.deepEqual(LESSON_CONTEXT_REGISTRY_SCHEMA.required, expectedLessonIds);
  assert.deepEqual(
    Object.keys(LESSON_CONTEXT_REGISTRY_SCHEMA.properties),
    expectedLessonIds
  );
  assert.equal(LESSON_CONTEXT_REGISTRY_SCHEMA.additionalProperties, false);
  for (const lessonId of expectedLessonIds) {
    assert.equal(
      LESSON_CONTEXT_REGISTRY_SCHEMA.properties[lessonId],
      LESSON_CONTEXT_VALUE_SCHEMA
    );
  }
});

test('lesson context contains lesson facts but no instruction fields', () => {
  assert.deepEqual(LESSON_CONTEXT_VALUE_SCHEMA.required, [
    'program',
    'course',
    'sequence',
    'topic',
    'key_expressions'
  ]);
  assert.equal(LESSON_CONTEXT_VALUE_SCHEMA.additionalProperties, false);
  for (const field of LESSON_CONTEXT_TRUST_BOUNDARY.forbidden_browser_instruction_fields) {
    assert.equal(LESSON_CONTEXT_VALUE_SCHEMA.properties[field], undefined);
  }
});

test('trust boundary permits only lesson id and student message from browser', () => {
  assert.deepEqual(LESSON_CONTEXT_TRUST_BOUNDARY.browser_payload_fields, [
    'lesson_id',
    'student_message'
  ]);
  assert.ok(LESSON_CONTEXT_TRUST_BOUNDARY.server_owned_context_fields.includes('topic'));
  assert.ok(LESSON_CONTEXT_TRUST_BOUNDARY.server_owned_context_fields.includes('lesson_text'));
  assert.ok(Object.isFrozen(LESSON_CONTEXT_REGISTRY_SCHEMA));
  assert.ok(Object.isFrozen(LESSON_CONTEXT_VALUE_SCHEMA.properties.sequence));
});

function deepFreeze(value) {
  if (!value || typeof value !== 'object' || Object.isFrozen(value)) return value;
  for (const child of Object.values(value)) deepFreeze(child);
  return Object.freeze(value);
}

export const SAMPLE_LESSON_IDS = deepFreeze([
  '/camp-a/grade3/week01a.html',
  '/camp-b/g1/week01a.html',
  '/camp-c/ep01.html',
  '/grammar-camp/G01/G01_be_verb_present_tense.html'
]);

const nonEmptyString = deepFreeze({ type: 'string', minLength: 1 });
const stringList = deepFreeze({
  type: 'array',
  items: nonEmptyString,
  uniqueItems: true
});

export const LESSON_CONTEXT_VALUE_SCHEMA = deepFreeze({
  type: 'object',
  additionalProperties: false,
  required: ['program', 'course', 'sequence', 'topic', 'key_expressions'],
  properties: {
    program: nonEmptyString,
    course: nonEmptyString,
    sequence: {
      type: 'object',
      additionalProperties: false,
      minProperties: 1,
      properties: {
        week: nonEmptyString,
        day: nonEmptyString,
        episode: nonEmptyString,
        unit: nonEmptyString
      }
    },
    topic: nonEmptyString,
    book_title: { type: ['string', 'null'] },
    key_expressions: { ...stringList, minItems: 1 },
    vocabulary: stringList,
    lesson_text: nonEmptyString
  }
});

// This contract describes a complete server-owned registry. It contains no
// lesson values; population and lookup belong to the next implementation item.
export const LESSON_CONTEXT_REGISTRY_SCHEMA = deepFreeze({
  type: 'object',
  additionalProperties: false,
  required: SAMPLE_LESSON_IDS,
  properties: Object.fromEntries(
    SAMPLE_LESSON_IDS.map(lessonId => [lessonId, LESSON_CONTEXT_VALUE_SCHEMA])
  )
});

export const LESSON_CONTEXT_TRUST_BOUNDARY = deepFreeze({
  browser_payload_fields: ['lesson_id', 'student_message'],
  server_owned_context_fields: Object.keys(LESSON_CONTEXT_VALUE_SCHEMA.properties),
  forbidden_browser_instruction_fields: [
    'system',
    'developer',
    'instructions',
    'messages',
    'prompt'
  ]
});

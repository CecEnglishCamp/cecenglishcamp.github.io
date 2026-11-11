import { SAMPLE_LESSON_IDS } from './lesson-context-schema.js';

function deepFreeze(value) {
  if (!value || typeof value !== 'object' || Object.isFrozen(value)) return value;
  for (const child of Object.values(value)) deepFreeze(child);
  return Object.freeze(value);
}

export const LESSON_CONTEXTS = deepFreeze({
  '/camp-a/grade3/week01a.html': {
    program: 'CEC Camp A',
    course: 'Elementary Grade 3; Q1; A1/A2 reading levels',
    sequence: { week: 'Week 01', day: 'Day 1' },
    topic: "Peter Rabbit escaping from Mr. McGregor's garden",
    book_title: 'The Tale of Peter Rabbit by Beatrix Potter',
    key_expressions: ['He ran away.'],
    vocabulary: ['ran', 'away', 'scared', 'garden'],
    lesson_text: 'Peter disobeys his mother, enters the garden, is discovered, becomes scared, and runs away.'
  },
  '/camp-b/g1/week01a.html': {
    program: 'CEC Camp B',
    course: 'High School 1 (G1); B1/B2 reading levels',
    sequence: { week: 'Week 01', day: 'Day 1' },
    topic: 'Wealth, outsider status, alienation, and the social world around Gatsby',
    book_title: 'The Great Gatsby',
    key_expressions: [
      'Nick moved next door to a mysterious mansion.',
      "Nick moved to West Egg next to Gatsby's enormous mansion."
    ],
    vocabulary: ['affluence', 'alienation', 'assimilating', 'paradox', 'transactional'],
    lesson_text: "B1/B2 reading about Nick entering the world of the very rich, feeling like an outsider, and noticing careless cruelty."
  },
  '/camp-c/ep01.html': {
    program: 'CEC Camp C',
    course: 'Adult situational English; A1/A2/B1 variants',
    sequence: { episode: 'Episode 01', unit: 'Unit 1' },
    topic: 'Arriving at the airport and asking for help and directions',
    book_title: null,
    key_expressions: ['Excuse me. Can you help me?'],
    vocabulary: ['help', 'Terminal 2', 'Exit 5', 'go straight', 'turn left', 'near the coffee shop'],
    lesson_text: 'Young-ja arrives at Los Angeles airport, asks a worker for directions, and finds her daughter.'
  },
  '/grammar-camp/G01/G01_be_verb_present_tense.html': {
    program: 'CEC Grammar BaseCamp',
    course: 'G01 Basic Grammar',
    sequence: { unit: 'G01' },
    topic: 'Be Verb: Present Tense — am / is / are',
    book_title: null,
    key_expressions: ['I am a student.', 'She is happy.', 'They are friends.'],
    vocabulary: ['am', 'is', 'are'],
    lesson_text: 'Subject-to-verb mapping, positive and negative statements, questions, contractions, and common present-tense be-verb examples.'
  }
});

const registryIds = Object.keys(LESSON_CONTEXTS);
if (
  registryIds.length !== SAMPLE_LESSON_IDS.length ||
  SAMPLE_LESSON_IDS.some(lessonId => !Object.hasOwn(LESSON_CONTEXTS, lessonId))
) {
  throw new Error('LESSON_CONTEXT_REGISTRY_MISMATCH');
}

export function lessonContextForLesson(lessonId) {
  if (typeof lessonId !== 'string') return null;
  return LESSON_CONTEXTS[lessonId] || null;
}

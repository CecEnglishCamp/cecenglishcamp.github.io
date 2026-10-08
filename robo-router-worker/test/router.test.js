import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  createTutorRouter,
  MAX_TOKENS,
  MODEL,
  OPENAI_ENDPOINT
} from '../src/router.js';
import { PROFILES, SAFETY_RULES } from '../src/profiles.js';
import { lessonContextForLesson } from '../src/lesson-context.js';

const env = {
  OPENAI_API_KEY: 'synthetic-test-key',
  ALLOWED_ORIGINS: 'https://cecenglishcamp.com',
  TUTOR_ELIGIBILITY_RESOLVER: {
    resolve: async () => ({ policy: 'eligible' })
  }
};

function tutorRequest(body, extra = {}) {
  return new Request('https://worker.test/robo/v1/tutor', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(extra.headers || {}) },
    body: JSON.stringify(body)
  });
}

const lessons = {
  'camp-a': '/camp-a/grade3/week01a.html',
  'camp-b': '/camp-b/g1/week01a.html',
  'camp-c': '/camp-c/ep01.html',
  grammar: '/grammar-camp/G01/G01_be_verb_present_tense.html'
};

test('fails closed before upstream and guardian consent alone cannot bypass ZDR', async () => {
  let upstreamCalls = 0;
  const protectedEnv = {
    ...env,
    TUTOR_ELIGIBILITY_RESOLVER: {
      resolve: async () => ({
        policy: 'protected',
        guardianConsentConfirmed: true,
        zdrApproved: false
      })
    }
  };
  const router = createTutorRouter({
    fetchImpl: async () => {
      upstreamCalls += 1;
      throw new Error('blocked request must not reach upstream');
    }
  });

  const response = await router.fetch(tutorRequest({
    lesson_id: lessons['camp-a'],
    student_message: 'Private learner message'
  }), protectedEnv);

  assert.equal(response.status, 403);
  assert.deepEqual(await response.json(), {
    ok: false,
    code: 'GENERATIVE_AI_BLOCKED',
    reason: 'ZDR_APPROVAL_REQUIRED',
    fallback: { mode: 'rules_based', plan: 'PLAN_B_2' }
  });
  assert.equal(upstreamCalls, 0);
});

for (const [profile, lesson_id] of Object.entries(lessons)) {
  test(`routes ${profile} and applies server-owned controls`, async () => {
    let outbound;
    const router = createTutorRouter({
      fetchImpl: async (url, options) => {
        assert.equal(url, OPENAI_ENDPOINT);
        outbound = JSON.parse(options.body);
        return Response.json({ choices: [{ message: { content: 'Synthetic tutor reply.' } }] });
      }
    });

    const response = await router.fetch(
      tutorRequest({ lesson_id, student_message: 'Please explain this lesson.' }),
      env
    );

    assert.equal(response.status, 200);
    assert.equal(outbound.model, MODEL);
    assert.equal(outbound.max_tokens, MAX_TOKENS);
    assert.equal(outbound.stream, false);
    assert.deepEqual(outbound.messages.map(message => message.role), ['system', 'user']);
    assert.ok(outbound.messages[0].content.includes(SAFETY_RULES));
    assert.ok(outbound.messages[0].content.includes(PROFILES[profile]));
    assert.ok(outbound.messages[0].content.includes(
      JSON.stringify(lessonContextForLesson(lesson_id))
    ));
    assert.deepEqual(JSON.parse(outbound.messages[1].content), {
      lesson_id,
      student_message: 'Please explain this lesson.'
    });
  });
}

for (const field of ['messages', 'system', 'developer', 'model', 'max_tokens']) {
  test(`rejects browser-supplied ${field}`, async () => {
    const router = createTutorRouter({
      fetchImpl: async () => { throw new Error('upstream must not be called'); }
    });
    const response = await router.fetch(tutorRequest({
      lesson_id: lessons['camp-a'],
      student_message: 'Hello',
      [field]: field === 'messages' ? [] : 'browser override'
    }), env);
    assert.equal(response.status, 400);
    assert.equal((await response.json()).code, 'INVALID_REQUEST');
  });
}

test('rejects unknown lesson families and preserves the legacy API path', async () => {
  const router = createTutorRouter();
  const unknown = await router.fetch(tutorRequest({
    lesson_id: '/unknown/lesson.html',
    student_message: 'Hello'
  }), env);
  assert.equal(unknown.status, 400);

  const legacy = await router.fetch(new Request(
    'https://worker.test/api/ai/chat/completions',
    { method: 'POST', body: '{}' }
  ), env);
  assert.equal(legacy.status, 404);
  assert.equal((await legacy.json()).code, 'NOT_FOUND');
});

test('does not expose upstream errors or credentials', async () => {
  const router = createTutorRouter({
    fetchImpl: async () => new Response('private upstream detail', { status: 500 })
  });
  const response = await router.fetch(tutorRequest({
    lesson_id: lessons.grammar,
    student_message: 'Explain be verbs.'
  }), env);
  const text = await response.text();
  assert.equal(response.status, 502);
  assert.ok(!text.includes('private upstream detail'));
  assert.ok(!text.includes(env.OPENAI_API_KEY));
});

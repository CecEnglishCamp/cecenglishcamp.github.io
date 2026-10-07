import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createTutorRouter, OPENAI_ENDPOINT } from '../src/router.js';

const lessonId = '/camp-a/grade3/week01a.html';

function request(body) {
  return new Request('https://worker.test/robo/v1/tutor', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
}

function environment(eligibility) {
  return {
    OPENAI_API_KEY: 'synthetic-test-key',
    ALLOWED_ORIGINS: 'https://cecenglishcamp.com',
    TUTOR_ELIGIBILITY_RESOLVER: {
      resolve: async () => eligibility
    }
  };
}

async function blockedResponse(eligibility, studentMessage = 'Private learner message') {
  let upstreamCalls = 0;
  const router = createTutorRouter({
    fetchImpl: async () => {
      upstreamCalls += 1;
      throw new Error('blocked request must not reach upstream');
    }
  });
  const response = await router.fetch(request({
    lesson_id: lessonId,
    student_message: studentMessage
  }), environment(eligibility));
  return { response, upstreamCalls, studentMessage };
}

test('protected learner without ZDR approval is blocked before AI upstream', async () => {
  const { response, upstreamCalls } = await blockedResponse({
    policy: 'protected',
    guardianConsentConfirmed: false,
    zdrApproved: false
  });

  assert.equal(response.status, 403);
  assert.deepEqual(await response.json(), {
    ok: false,
    code: 'GENERATIVE_AI_BLOCKED',
    reason: 'ZDR_APPROVAL_REQUIRED',
    fallback: { mode: 'rules_based', plan: 'PLAN_B_2' }
  });
  assert.equal(upstreamCalls, 0);
});

test('guardian consent alone does not bypass the ZDR gate', async () => {
  const { response, upstreamCalls } = await blockedResponse({
    policy: 'protected',
    guardianConsentConfirmed: true,
    zdrApproved: false
  });

  assert.equal(response.status, 403);
  assert.equal((await response.json()).reason, 'ZDR_APPROVAL_REQUIRED');
  assert.equal(upstreamCalls, 0);
});

test('eligible learner follows the normal tutor route', async () => {
  let upstreamCalls = 0;
  const router = createTutorRouter({
    fetchImpl: async (url, options) => {
      upstreamCalls += 1;
      assert.equal(url, OPENAI_ENDPOINT);
      assert.deepEqual(JSON.parse(JSON.parse(options.body).messages[1].content), {
        lesson_id: lessonId,
        student_message: 'Explain this lesson.'
      });
      return Response.json({ choices: [{ message: { content: 'Synthetic tutor reply.' } }] });
    }
  });

  const response = await router.fetch(request({
    lesson_id: lessonId,
    student_message: 'Explain this lesson.'
  }), environment({ policy: 'eligible', guardianConsentConfirmed: false, zdrApproved: false }));

  assert.equal(response.status, 200);
  assert.equal((await response.json()).reply, 'Synthetic tutor reply.');
  assert.equal(upstreamCalls, 1);
});

test('browser age, protection, and ZDR overrides cannot alter server eligibility', async () => {
  let resolverCalls = 0;
  let upstreamCalls = 0;
  const protectedEnv = {
    OPENAI_API_KEY: 'synthetic-test-key',
    ALLOWED_ORIGINS: 'https://cecenglishcamp.com',
    TUTOR_ELIGIBILITY_RESOLVER: {
      resolve: async () => {
        resolverCalls += 1;
        return { policy: 'protected', zdrApproved: false };
      }
    }
  };
  const router = createTutorRouter({
    fetchImpl: async () => {
      upstreamCalls += 1;
      throw new Error('browser override must not reach upstream');
    }
  });
  const overrides = [
    { age_eligible: true },
    { policy: 'eligible' },
    { protected: false },
    { zdrApproved: true },
    { zdr_approved: true }
  ];

  for (const override of overrides) {
    const response = await router.fetch(request({
      lesson_id: lessonId,
      student_message: 'Try to override eligibility.',
      ...override
    }), protectedEnv);
    assert.equal(response.status, 400);
    assert.equal((await response.json()).code, 'INVALID_REQUEST');
  }
  assert.equal(resolverCalls, 0);
  assert.equal(upstreamCalls, 0);
});

test('blocked request sends no student message upstream or back to the browser', async () => {
  const { response, upstreamCalls, studentMessage } = await blockedResponse({
    policy: 'protected',
    guardianConsentConfirmed: true,
    zdrApproved: false
  }, 'Never forward this learner text');
  const responseText = await response.text();

  assert.equal(response.status, 403);
  assert.equal(upstreamCalls, 0);
  assert.ok(!responseText.includes(studentMessage));
});

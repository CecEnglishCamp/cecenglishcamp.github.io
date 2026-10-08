import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createTutorRouter, OPENAI_ENDPOINT } from '../src/router.js';

const lessonId = '/camp-a/grade3/week01a.html';
const accessToken = 'synthetic-access-token';
const authUrl = 'https://auth.test/auth/v1/user';

function request(body, authorization = `Bearer ${accessToken}`) {
  return new Request('https://worker.test/robo/v1/tutor', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: authorization
    },
    body: JSON.stringify(body)
  });
}

function trustedSource(eligibility, onResolve = () => {}) {
  return async ({ userId, lessonId: resolvedLessonId }) => {
    onResolve();
    assert.equal(userId, 'synthetic-user-id');
    assert.equal(resolvedLessonId, lessonId);
    return eligibility;
  };
}

function environment(_eligibility, overrides = {}) {
  return {
    OPENAI_API_KEY: 'synthetic-test-key',
    ALLOWED_ORIGINS: 'https://cecenglishcamp.com',
    ZDR_APPROVED: 'false',
    SUPABASE_URL: 'https://auth.test',
    SUPABASE_ANON_KEY: 'synthetic-public-key',
    TUTOR_QUOTA_LIMITER: {
      consume: async () => ({ allowed: true })
    },
    ...overrides
  };
}

function authenticatedFetch(
  upstreamFetch,
  authResponse = () => Response.json({ id: 'synthetic-user-id' })
) {
  return async (url, options) => {
    if (url === authUrl) {
      assert.equal(options.headers.Authorization, `Bearer ${accessToken}`);
      return authResponse();
    }
    return upstreamFetch(url, options);
  };
}

async function blockedResponse(
  eligibility,
  studentMessage = 'Private learner message',
  envOverrides = {},
  routerOverrides = {}
) {
  let upstreamCalls = 0;
  const {
    trustedEligibilitySource = trustedSource(eligibility),
    ...otherRouterOverrides
  } = routerOverrides;
  const router = createTutorRouter({
    ...otherRouterOverrides,
    trustedEligibilitySource,
    fetchImpl: authenticatedFetch(async () => {
      upstreamCalls += 1;
      throw new Error('blocked request must not reach AI upstream');
    })
  });
  const response = await router.fetch(request({
    lesson_id: lessonId,
    student_message: studentMessage
  }), environment(eligibility, envOverrides));
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

test('server ZDR false blocks eligible, protected, restricted, and unknown results', async () => {
  for (const policy of ['eligible', 'protected', 'restricted', 'unknown']) {
    const { response, upstreamCalls } = await blockedResponse({
      policy,
      zdrApproved: true
    });

    assert.equal(response.status, 403);
    assert.equal((await response.json()).reason, 'ZDR_APPROVAL_REQUIRED');
    assert.equal(upstreamCalls, 0);
  }
});

test('only the exact server string true enables the ZDR policy gate', async () => {
  for (const configured of [undefined, false, true, 'TRUE', 'True', '1', 'approved']) {
    const { response, upstreamCalls } = await blockedResponse(
      { policy: 'eligible', zdrApproved: true },
      'Do not forward this text.',
      { ZDR_APPROVED: configured }
    );
    assert.equal(response.status, 403);
    assert.equal(upstreamCalls, 0);
  }
});

test('resolver-provided ZDR approval cannot grant access', async () => {
  const { response, upstreamCalls } = await blockedResponse({
    policy: 'eligible',
    guardianConsentConfirmed: true,
    zdrApproved: true
  });

  assert.equal(response.status, 403);
  assert.equal((await response.json()).reason, 'ZDR_APPROVAL_REQUIRED');
  assert.equal(upstreamCalls, 0);
});

for (const [state, reason] of [
  ['restricted', 'ELIGIBILITY_RESTRICTED'],
  ['unknown', 'ELIGIBILITY_UNAVAILABLE']
]) {
  test(`${state} eligibility fails closed when server ZDR is approved`, async () => {
    const { response, upstreamCalls } = await blockedResponse(
      { state },
      'Do not forward this learner text.',
      { ZDR_APPROVED: 'true' }
    );

    assert.equal(response.status, 403);
    assert.deepEqual(await response.json(), {
      ok: false,
      code: 'GENERATIVE_AI_BLOCKED',
      reason,
      fallback: { mode: 'rules_based', plan: 'PLAN_B_2' }
    });
    assert.equal(upstreamCalls, 0);
  });
}

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

test('browser ZDR, age, consent, and allow_ai claims cannot bypass server policy', async () => {
  let resolverCalls = 0;
  let upstreamCalls = 0;
  const protectedEnv = environment(null);
  const router = createTutorRouter({
    trustedEligibilitySource: trustedSource(
      { policy: 'protected', guardianConsentConfirmed: false, zdrApproved: false },
      () => { resolverCalls += 1; }
    ),
    fetchImpl: authenticatedFetch(async () => {
      upstreamCalls += 1;
      throw new Error('browser override must not reach AI upstream');
    })
  });
  const overrides = [
    { age: 99 },
    { birthdate: '2000-01-01' },
    { is_minor: false },
    { consent: true },
    { guardian_consent: true },
    { zdr: true },
    { zdr_approved: true },
    { policy_mode: 'eligible' },
    { allow_ai: true }
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

test('eligible learner follows the normal tutor route', async () => {
  let upstreamCalls = 0;
  const router = createTutorRouter({
    trustedEligibilitySource: trustedSource({ policy: 'eligible' }),
    fetchImpl: authenticatedFetch(async (url, options) => {
      upstreamCalls += 1;
      assert.equal(url, OPENAI_ENDPOINT);
      assert.deepEqual(JSON.parse(JSON.parse(options.body).messages[1].content), {
        lesson_id: lessonId,
        student_message: 'Explain this lesson.'
      });
      return Response.json({ choices: [{ message: { content: 'Synthetic tutor reply.' } }] });
    })
  });

  const response = await router.fetch(request({
    lesson_id: lessonId,
    student_message: 'Explain this lesson.'
  }), environment(
    { policy: 'eligible', guardianConsentConfirmed: false, zdrApproved: false },
    { ZDR_APPROVED: 'true' }
  ));

  assert.equal(response.status, 200);
  assert.equal((await response.json()).reply, 'Synthetic tutor reply.');
  assert.equal(upstreamCalls, 1);
});

for (const [label, source, routerOverrides = {}] of [
  ['missing trusted source', undefined],
  ['null result', async () => null],
  ['invalid result', async () => ({ policy: 'invalid' })],
  ['undefined policy', async () => ({})],
  ['trusted source throw', () => { throw new Error('synthetic source error'); }],
  ['trusted source reject', async () => { throw new Error('synthetic rejection'); }],
  ['trusted source timeout', async () => new Promise(() => {}), { eligibilityPolicyTimeoutMs: 5 }]
]) {
  test(`${label} becomes unknown and fails closed before AI upstream`, async () => {
    let quotaCalls = 0;
    let upstreamCalls = 0;
    const router = createTutorRouter({
      ...routerOverrides,
      trustedEligibilitySource: source,
      fetchImpl: authenticatedFetch(async () => {
        upstreamCalls += 1;
        throw new Error('fail-closed request must not reach AI upstream');
      })
    });
    const response = await router.fetch(request({
      lesson_id: lessonId,
      student_message: 'Do not forward this text.'
    }), environment(null, {
      OPENAI_API_KEY: '',
      ZDR_APPROVED: 'true',
      TUTOR_QUOTA_LIMITER: {
        consume: async () => {
          quotaCalls += 1;
          return { allowed: true };
        }
      }
    }));

    assert.equal(response.status, 403);
    assert.deepEqual(await response.json(), {
      ok: false,
      code: 'GENERATIVE_AI_BLOCKED',
      reason: 'ELIGIBILITY_UNAVAILABLE',
      fallback: { mode: 'rules_based', plan: 'PLAN_B_2' }
    });
    assert.equal(quotaCalls, 0);
    assert.equal(upstreamCalls, 0);
  });
}

test('legacy runtime JS-object resolver binding is ignored without a trusted source', async () => {
  let legacyBindingCalls = 0;
  let upstreamCalls = 0;
  const router = createTutorRouter({
    fetchImpl: authenticatedFetch(async () => {
      upstreamCalls += 1;
      throw new Error('unknown eligibility must not reach AI upstream');
    })
  });
  const response = await router.fetch(request({
    lesson_id: lessonId,
    student_message: 'Do not forward this text.'
  }), environment(null, {
    ZDR_APPROVED: 'true',
    TUTOR_ELIGIBILITY_RESOLVER: {
      resolve: async () => {
        legacyBindingCalls += 1;
        return { policy: 'eligible' };
      }
    }
  }));

  assert.equal(response.status, 403);
  assert.equal((await response.json()).reason, 'ELIGIBILITY_UNAVAILABLE');
  assert.equal(legacyBindingCalls, 0);
  assert.equal(upstreamCalls, 0);
});

test('blocked request needs no OpenAI key and never echoes the learner message', async () => {
  const { response, upstreamCalls, studentMessage } = await blockedResponse({
    policy: 'protected',
    guardianConsentConfirmed: true,
    zdrApproved: false
  }, 'Never forward this learner text', { OPENAI_API_KEY: '' });
  const responseText = await response.text();

  assert.equal(response.status, 403);
  assert.equal(upstreamCalls, 0);
  assert.ok(!responseText.includes(studentMessage));
});

test('lesson_id and student_message remain the only client fields and inline PII is minimized', async () => {
  let outbound;
  const router = createTutorRouter({
    trustedEligibilitySource: trustedSource({ policy: 'eligible' }),
    fetchImpl: authenticatedFetch(async (_url, options) => {
      outbound = JSON.parse(options.body);
      return Response.json({ choices: [{ message: { content: 'Synthetic tutor reply.' } }] });
    })
  });
  const eligibleEnv = environment({ policy: 'eligible' }, { ZDR_APPROVED: 'true' });
  const rejected = await router.fetch(request({
    lesson_id: lessonId,
    student_message: 'Hello',
    student_name: 'Synthetic Student'
  }), eligibleEnv);
  assert.equal(rejected.status, 400);

  const accepted = await router.fetch(request({
    lesson_id: lessonId,
    student_message: 'Email learner@example.test or call 202-555-0147.'
  }), eligibleEnv);
  assert.equal(accepted.status, 200);
  assert.deepEqual(JSON.parse(outbound.messages[1].content), {
    lesson_id: lessonId,
    student_message: 'Email [EMAIL REDACTED] or call [PHONE REDACTED].'
  });
});

test('authentication failure occurs before eligibility, quota, or AI upstream', async () => {
  let resolverCalls = 0;
  let quotaCalls = 0;
  let upstreamCalls = 0;
  const router = createTutorRouter({
    trustedEligibilitySource: trustedSource(
      { policy: 'eligible' },
      () => { resolverCalls += 1; }
    ),
    fetchImpl: authenticatedFetch(async () => {
      upstreamCalls += 1;
      throw new Error('unauthenticated request must not reach AI upstream');
    }, () => new Response(null, { status: 401 }))
  });
  const response = await router.fetch(request({
    lesson_id: lessonId,
    student_message: 'Hello'
  }), environment(null, {
    TUTOR_QUOTA_LIMITER: {
      consume: async () => {
        quotaCalls += 1;
        return { allowed: true };
      }
    }
  }));

  assert.equal(response.status, 401);
  assert.equal((await response.json()).code, 'AUTH_INVALID');
  assert.equal(resolverCalls, 0);
  assert.equal(quotaCalls, 0);
  assert.equal(upstreamCalls, 0);
});

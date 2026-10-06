import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  createTutorRouter,
  MAX_REQUEST_BYTES,
  MAX_STUDENT_MESSAGE_CHARS,
  MAX_TOKENS,
  MODEL,
  OPENAI_ENDPOINT
} from '../src/router.js';
import { PROFILES, SAFETY_RULES } from '../src/profiles.js';

const env = {
  OPENAI_API_KEY: 'synthetic-test-key',
  ALLOWED_ORIGINS: 'https://cecenglishcamp.com',
  SUPABASE_URL: 'https://auth.test',
  SUPABASE_ANON_KEY: 'synthetic-public-key'
};

const ACCESS_TOKEN = 'synthetic-access-token';

function verifiedFetch(upstreamFetch) {
  return async (url, options) => {
    if (url === 'https://auth.test/auth/v1/user') {
      assert.equal(options.method, 'GET');
      assert.equal(options.headers.apikey, env.SUPABASE_ANON_KEY);
      assert.equal(options.headers.Authorization, `Bearer ${ACCESS_TOKEN}`);
      return Response.json({ id: 'synthetic-user-id' });
    }
    return upstreamFetch(url, options);
  };
}

function tutorRequest(body, extra = {}) {
  return new Request('https://worker.test/robo/v1/tutor', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${ACCESS_TOKEN}`,
      ...(extra.headers || {})
    },
    body: JSON.stringify(body)
  });
}

const lessons = {
  'camp-a': '/camp-a/grade3/week01a.html',
  'camp-b': '/camp-b/g1/week01a.html',
  'camp-c': '/camp-c/ep01.html',
  grammar: '/grammar-camp/G01/G01_be_verb_present_tense.html'
};

for (const [profile, lesson_id] of Object.entries(lessons)) {
  test(`routes ${profile} and applies server-owned controls`, async () => {
    let outbound;
    const router = createTutorRouter({
      fetchImpl: verifiedFetch(async (url, options) => {
        assert.equal(url, OPENAI_ENDPOINT);
        outbound = JSON.parse(options.body);
        return Response.json({ choices: [{ message: { content: 'Synthetic tutor reply.' } }] });
      })
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
  });
}

for (const field of ['messages', 'system', 'developer', 'model', 'max_tokens']) {
  test(`rejects browser-supplied ${field}`, async () => {
    const router = createTutorRouter({
      fetchImpl: verifiedFetch(async () => { throw new Error('upstream must not be called'); })
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

for (const [field, value] of Object.entries({
  student_name: 'Synthetic Student',
  email: 'student@example.test',
  phone: '202-555-0147',
  school: 'Synthetic School',
  account_id: 'synthetic-account-123',
  parent_name: 'Synthetic Parent'
})) {
  test(`rejects structured PII field ${field}`, async () => {
    const router = createTutorRouter({
      fetchImpl: verifiedFetch(async () => { throw new Error('upstream must not be called'); })
    });
    const response = await router.fetch(tutorRequest({
      lesson_id: lessons['camp-a'],
      student_message: 'Hello',
      [field]: value
    }), env);
    assert.equal(response.status, 400);
    assert.equal((await response.json()).code, 'INVALID_REQUEST');
  });
}

test('rejects malformed JSON payloads', async () => {
  const router = createTutorRouter({
    fetchImpl: verifiedFetch(async () => { throw new Error('upstream must not be called'); })
  });
  const response = await router.fetch(new Request(
    'https://worker.test/robo/v1/tutor',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${ACCESS_TOKEN}`
      },
      body: '{"lesson_id":'
    }
  ), env);
  assert.equal(response.status, 400);
  assert.equal((await response.json()).code, 'INVALID_REQUEST');
});

test('rejects payloads missing lesson_id', async () => {
  const router = createTutorRouter({
    fetchImpl: verifiedFetch(async () => { throw new Error('upstream must not be called'); })
  });
  const response = await router.fetch(tutorRequest({
    student_message: 'Hello'
  }), env);
  assert.equal(response.status, 400);
  assert.equal((await response.json()).code, 'INVALID_REQUEST');
});

test('rejects payloads missing student_message', async () => {
  const router = createTutorRouter({
    fetchImpl: verifiedFetch(async () => { throw new Error('upstream must not be called'); })
  });
  const response = await router.fetch(tutorRequest({
    lesson_id: lessons['camp-a']
  }), env);
  assert.equal(response.status, 400);
  assert.equal((await response.json()).code, 'INVALID_REQUEST');
});

test('rejects oversized student_message payloads', async () => {
  const router = createTutorRouter({
    fetchImpl: verifiedFetch(async () => { throw new Error('upstream must not be called'); })
  });
  const response = await router.fetch(tutorRequest({
    lesson_id: lessons['camp-a'],
    student_message: 'a'.repeat(MAX_STUDENT_MESSAGE_CHARS + 1)
  }), env);
  assert.equal(response.status, 400);
  assert.equal((await response.json()).code, 'INVALID_REQUEST');
});

test('rejects oversized request bodies before model forwarding', async () => {
  const router = createTutorRouter({
    fetchImpl: verifiedFetch(async () => { throw new Error('upstream must not be called'); })
  });
  const body = JSON.stringify({
    lesson_id: lessons['camp-a'],
    student_message: 'Hello'
  }) + ' '.repeat(MAX_REQUEST_BYTES);
  const response = await router.fetch(new Request(
    'https://worker.test/robo/v1/tutor',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${ACCESS_TOKEN}`
      },
      body
    }
  ), env);
  assert.equal(response.status, 400);
  assert.equal((await response.json()).code, 'INVALID_REQUEST');
});

test('redacts simple email addresses before model forwarding', async () => {
  let outbound;
  const router = createTutorRouter({
    fetchImpl: verifiedFetch(async (_url, options) => {
      outbound = JSON.parse(options.body);
      return Response.json({ choices: [{ message: { content: 'Synthetic tutor reply.' } }] });
    })
  });
  const email = 'student@example.test';
  const response = await router.fetch(tutorRequest({
    lesson_id: lessons['camp-a'],
    student_message: `Please reply to ${email}.`
  }), env);

  assert.equal(response.status, 200);
  const modelInput = JSON.parse(outbound.messages[1].content);
  assert.equal(modelInput.student_message, 'Please reply to [EMAIL REDACTED].');
  assert.ok(!outbound.messages[1].content.includes(email));
});

test('redacts simple phone numbers before model forwarding', async () => {
  let outbound;
  const router = createTutorRouter({
    fetchImpl: verifiedFetch(async (_url, options) => {
      outbound = JSON.parse(options.body);
      return Response.json({ choices: [{ message: { content: 'Synthetic tutor reply.' } }] });
    })
  });
  const phone = '202-555-0147';
  const response = await router.fetch(tutorRequest({
    lesson_id: lessons['camp-a'],
    student_message: `Call ${phone} after class.`
  }), env);

  assert.equal(response.status, 200);
  const modelInput = JSON.parse(outbound.messages[1].content);
  assert.equal(modelInput.student_message, 'Call [PHONE REDACTED] after class.');
  assert.ok(!outbound.messages[1].content.includes(phone));
});

test('rejects unknown lesson families and preserves the legacy API path', async () => {
  const router = createTutorRouter({
    fetchImpl: verifiedFetch(async () => { throw new Error('upstream must not be called'); })
  });
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
    fetchImpl: verifiedFetch(async () => new Response('private upstream detail', { status: 500 }))
  });
  const response = await router.fetch(tutorRequest({
    lesson_id: lessons.grammar,
    student_message: 'Explain be verbs.'
  }), env);
  const text = await response.text();
  assert.equal(response.status, 502);
  assert.deepEqual(JSON.parse(text), { ok: false, code: 'AI_UPSTREAM_ERROR' });
  assert.ok(!text.includes('private upstream detail'));
  assert.ok(!text.includes(env.OPENAI_API_KEY));
});

test('returns a structured timeout without retrying the upstream request', async () => {
  let upstreamCalls = 0;
  const router = createTutorRouter({
    upstreamTimeoutMs: 5,
    fetchImpl: verifiedFetch(async (_url, options) => {
      upstreamCalls += 1;
      await new Promise((_resolve, reject) => {
        options.signal.addEventListener('abort', () => {
          reject(new DOMException('synthetic timeout detail', 'AbortError'));
        }, { once: true });
      });
    })
  });

  const response = await router.fetch(tutorRequest({
    lesson_id: lessons.grammar,
    student_message: 'Explain be verbs.'
  }), env);

  assert.equal(response.status, 504);
  assert.deepEqual(await response.json(), { ok: false, code: 'AI_UPSTREAM_TIMEOUT' });
  assert.equal(upstreamCalls, 1);
});

test('requires a bearer token before contacting Supabase or OpenAI', async () => {
  let calls = 0;
  const router = createTutorRouter({ fetchImpl: async () => { calls += 1; } });
  const response = await router.fetch(tutorRequest({
    lesson_id: lessons['camp-a'],
    student_message: 'Hello'
  }, { headers: { Authorization: '' } }), env);

  assert.equal(response.status, 401);
  assert.deepEqual(await response.json(), { ok: false, code: 'AUTH_REQUIRED' });
  assert.equal(calls, 0);
});

test('reports missing or invalid Supabase configuration without making a request', async () => {
  let calls = 0;
  const router = createTutorRouter({ fetchImpl: async () => { calls += 1; } });
  const body = { lesson_id: lessons['camp-a'], student_message: 'Hello' };

  const missing = await router.fetch(tutorRequest(body), {
    ...env,
    SUPABASE_ANON_KEY: ''
  });
  assert.equal(missing.status, 503);
  assert.equal((await missing.json()).code, 'AUTH_NOT_CONFIGURED');

  const invalid = await router.fetch(tutorRequest(body), {
    ...env,
    SUPABASE_URL: 'not a URL'
  });
  assert.equal(invalid.status, 503);
  assert.equal((await invalid.json()).code, 'AUTH_NOT_CONFIGURED');
  assert.equal(calls, 0);
});

for (const [label, authResponse] of [
  ['rejected token', () => new Response(null, { status: 401 })],
  ['missing user id', () => Response.json({ id: '' })],
  ['unavailable auth service', () => { throw new Error('synthetic auth failure'); }]
]) {
  test(`rejects ${label} before contacting OpenAI`, async () => {
    let calls = 0;
    const router = createTutorRouter({
      fetchImpl: async (url, options) => {
        calls += 1;
        assert.equal(url, 'https://auth.test/auth/v1/user');
        assert.equal(options.headers.Authorization, `Bearer ${ACCESS_TOKEN}`);
        return authResponse();
      }
    });
    const response = await router.fetch(tutorRequest({
      lesson_id: lessons['camp-a'],
      student_message: 'Hello'
    }), env);

    assert.equal(response.status, 401);
    assert.deepEqual(await response.json(), { ok: false, code: 'AUTH_INVALID' });
    assert.equal(calls, 1);
  });
}

test('allows Authorization in CORS preflight without requiring authentication', async () => {
  let calls = 0;
  const router = createTutorRouter({ fetchImpl: async () => { calls += 1; } });
  const response = await router.fetch(new Request(
    'https://worker.test/robo/v1/tutor',
    { method: 'OPTIONS', headers: { Origin: 'https://cecenglishcamp.com' } }
  ), env);

  assert.equal(response.status, 204);
  assert.equal(response.headers.get('Access-Control-Allow-Headers'), 'Authorization, Content-Type');
  assert.equal(calls, 0);
});

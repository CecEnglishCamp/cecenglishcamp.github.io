import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createTutorRouter } from '../src/router.js';
import { TutorQuota, createDurableQuotaLimiter } from '../src/quota.js';

const LIMITS = { perMinute: 2, perDay: 3 };

function fakeState() {
  const map = new Map();
  return { storage: { async get(k) { return map.get(k); }, async put(k, v) { map.set(k, v); } } };
}

function fakeNamespace(clock) {
  const objects = new Map();
  return {
    idFromName: name => name,
    get(id) {
      if (!objects.has(id)) objects.set(id, new TutorQuota(fakeState(), {}, clock));
      const object = objects.get(id);
      return { fetch: (url, init) => object.fetch(new Request(url, init)) };
    }
  };
}

test('durable quota allows within limits then blocks by minute', async () => {
  let now = 1_000_000;
  const limiter = createDurableQuotaLimiter(fakeNamespace(() => now));
  assert.deepEqual(await limiter.consume({ userId: 'u1', limits: LIMITS }), { allowed: true });
  assert.deepEqual(await limiter.consume({ userId: 'u1', limits: LIMITS }), { allowed: true });
  const blocked = await limiter.consume({ userId: 'u1', limits: LIMITS });
  assert.equal(blocked.allowed, false);
  assert.equal(blocked.scope, 'minute');
  assert.ok(blocked.retryAfterSeconds >= 1 && blocked.retryAfterSeconds <= 60);
  now += 61_000;
  assert.deepEqual(await limiter.consume({ userId: 'u1', limits: LIMITS }), { allowed: true });
});

test('durable quota enforces the daily limit and resets after a day', async () => {
  let now = 5_000_000;
  const limiter = createDurableQuotaLimiter(fakeNamespace(() => now));
  for (let i = 0; i < 3; i += 1) {
    assert.equal((await limiter.consume({ userId: 'u2', limits: LIMITS })).allowed, true);
    now += 61_000;
  }
  const blocked = await limiter.consume({ userId: 'u2', limits: LIMITS });
  assert.equal(blocked.allowed, false);
  assert.equal(blocked.scope, 'day');
  now += 86_400_000;
  assert.equal((await limiter.consume({ userId: 'u2', limits: LIMITS })).allowed, true);
});

test('durable quota is per user and rejects invalid limits', async () => {
  const limiter = createDurableQuotaLimiter(fakeNamespace(() => 1));
  await limiter.consume({ userId: 'a', limits: { perMinute: 1, perDay: 5 } });
  assert.equal((await limiter.consume({ userId: 'a', limits: { perMinute: 1, perDay: 5 } })).allowed, false);
  assert.equal((await limiter.consume({ userId: 'b', limits: { perMinute: 1, perDay: 5 } })).allowed, true);
  await assert.rejects(limiter.consume({ userId: 'c', limits: { perMinute: 0, perDay: 5 } }));
});

const SECRET_MESSAGE = 'my secret question about verbs';
const TOKEN = 'synthetic-access-token-xyz';

function routeFetch() {
  return async (url) => {
    if (url === 'https://auth.test/auth/v1/user') {
      return new Response(JSON.stringify({ id: 'user-12345' }), { status: 200 });
    }
    return new Response(JSON.stringify({
      choices: [{ message: { content: 'Reply text from model' } }],
      usage: { prompt_tokens: 11, completion_tokens: 7, total_tokens: 18 }
    }), { status: 200 });
  };
}

function request(body = { lesson_id: '/camp-a/grade3/week01a.html', student_message: SECRET_MESSAGE }) {
  return new Request('https://worker.test/robo/v1/tutor', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${TOKEN}`,
      Origin: 'https://cecenglishcamp.com'
    },
    body: JSON.stringify(body)
  });
}

const env = {
  OPENAI_API_KEY: 'synthetic-openai-key',
  ALLOWED_ORIGINS: 'https://cecenglishcamp.com',
  SUPABASE_URL: 'https://auth.test',
  SUPABASE_ANON_KEY: 'synthetic-public-key',
  TUTOR_ELIGIBILITY_RESOLVER: {
    resolve: async () => ({ policy: 'eligible' })
  }
};

test('router uses the TUTOR_QUOTA Durable Object binding when present', async () => {
  const events = [];
  const router = createTutorRouter({ fetchImpl: routeFetch(), logger: e => events.push(e) });
  const bound = { ...env, TUTOR_QUOTA: fakeNamespace(() => 10) };
  // QUOTA_PER_MINUTE is 10 in the router; the 11th accepted call must be blocked.
  for (let i = 0; i < 10; i += 1) assert.equal((await router.fetch(request(), bound)).status, 200);
  const blocked = await router.fetch(request(), bound);
  assert.equal(blocked.status, 429);
  assert.ok(blocked.headers.get('Retry-After'));
});

test('logging is metadata-only and never includes message, token, reply or user id', async () => {
  const events = [];
  const router = createTutorRouter({ fetchImpl: routeFetch(), logger: e => events.push(e) });
  const response = await router.fetch(request(), { ...env, TUTOR_QUOTA: fakeNamespace(() => 10) });
  assert.equal(response.status, 200);
  assert.match(response.headers.get('X-Request-Id'), /^[0-9a-f-]{36}$/);
  assert.equal(events.length, 1);
  const event = events[0];
  assert.equal(event.status, 200);
  assert.equal(event.profile, 'camp-a');
  assert.equal(event.quota, 'allowed');
  assert.deepEqual(event.usage, { prompt_tokens: 11, completion_tokens: 7, total_tokens: 18 });
  assert.equal(typeof event.latency_ms, 'number');
  const serialized = JSON.stringify(event);
  for (const forbidden of [SECRET_MESSAGE, TOKEN, 'Reply text from model', 'user-12345', 'synthetic-openai-key']) {
    assert.ok(!serialized.includes(forbidden), `log leaked ${forbidden}`);
  }
});

test('failures are logged with a code and a logger error never breaks the response', async () => {
  const events = [];
  const router = createTutorRouter({ fetchImpl: routeFetch(), logger: e => events.push(e) });
  const unauth = await router.fetch(new Request('https://worker.test/robo/v1/tutor', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Origin: 'https://cecenglishcamp.com' }, body: '{}'
  }), env);
  assert.equal(unauth.status, 401);
  assert.equal(events[0].code, 'AUTH_REQUIRED');

  const throwing = createTutorRouter({ fetchImpl: routeFetch(), logger: () => { throw new Error('boom'); } });
  const ok = await throwing.fetch(request(), { ...env, TUTOR_QUOTA: fakeNamespace(() => 10) });
  assert.equal(ok.status, 200);
});

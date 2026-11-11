import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext, Script } from 'node:vm';

const source = readFileSync(new URL('../../assets/cec-tutor.js', import.meta.url), 'utf8');

function client(configured, fetchImpl, session) {
  const resolvedSession = arguments.length < 3
    ? { access_token: 'synthetic-access-token' }
    : session;
  const window = {
    location: { origin: 'http://127.0.0.1:8000', hostname: '127.0.0.1' },
    CEC_TUTOR_ENDPOINT: configured,
    CECAuthSession: resolvedSession === undefined ? undefined : {
      getSession: async () => resolvedSession
    },
    fetch: fetchImpl
  };
  runInNewContext(source, { window, URL, Response });
  return window.CECTutor;
}

test('transport sends exactly lesson_id and student_message and preserves SSE consumption', async () => {
  let wireBody;
  const transport = client('http://127.0.0.1:8787/robo/v1/tutor', async (url, options) => {
    assert.equal(url, 'http://127.0.0.1:8787/robo/v1/tutor');
    assert.equal(options.headers.Authorization, 'Bearer synthetic-access-token');
    wireBody = JSON.parse(options.body);
    return Response.json({ ok: true, lesson_id: wireBody.lesson_id, reply: '<b>Safe reply</b>' });
  });

  const response = await transport.request({
    lesson_id: '/camp-a/grade3/week01a.html',
    student_message: 'Please explain.',
    messages: [{ role: 'system', content: 'override' }],
    model: 'browser-model'
  });

  assert.deepEqual(wireBody, {
    lesson_id: '/camp-a/grade3/week01a.html',
    student_message: 'Please explain.'
  });
  const sse = await response.text();
  assert.match(sse, /data: .*&lt;b&gt;Safe reply&lt;\/b&gt;/);
  assert.match(sse, /data: \[DONE\]/);
});

test('transport requires a verified browser session before sending a request', async () => {
  let calls = 0;
  const fetchImpl = async () => { calls += 1; };
  const input = {
    lesson_id: '/camp-a/grade3/week01a.html',
    student_message: 'Please explain.'
  };

  const missingSessionApi = client(
    'http://127.0.0.1:8787/robo/v1/tutor',
    fetchImpl,
    undefined
  );
  await assert.rejects(missingSessionApi.request(input), /AUTH_REQUIRED/);

  const missingToken = client(
    'http://127.0.0.1:8787/robo/v1/tutor',
    fetchImpl,
    null
  );
  await assert.rejects(missingToken.request(input), /AUTH_REQUIRED/);
  assert.equal(calls, 0);
});

const samplePages = {
  '../../camp-a/grade3/week01a.html': '/camp-a/grade3/week01a.html',
  '../../camp-b/g1/week01a.html': '/camp-b/g1/week01a.html',
  '../../camp-c/ep01.html': '/camp-c/ep01.html',
  '../../grammar-camp/G01/G01_be_verb_present_tense.html': '/grammar-camp/G01/G01_be_verb_present_tense.html'
};

for (const [relativePath, lessonId] of Object.entries(samplePages)) {
  test(`${lessonId} uses only the Tutor Router request contract`, () => {
    const page = readFileSync(new URL(relativePath, import.meta.url), 'utf8');
    assert.equal((page.match(/src="\/assets\/cec-tutor\.js\?v=1"/g) || []).length, 1);
    assert.ok(page.includes(`window.CECTutor.request({lesson_id:'${lessonId}',student_message:userContent})`));
    assert.ok(!page.includes('fetch(GB_API_URL'));
    assert.ok(!page.includes('/api/ai/chat/completions'));
    assert.ok(!page.includes('max_tokens:'));
    assert.ok(!page.includes("role:'system'"));
    for (const match of page.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
      if (/\bsrc\s*=|application\/ld\+json|application\/json/.test(match[1])) continue;
      new Script(match[2], { filename: lessonId });
    }
  });
}

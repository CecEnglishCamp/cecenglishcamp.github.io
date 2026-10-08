import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext, Script } from 'node:vm';

const source = readFileSync(new URL('../../assets/cec-tutor.js', import.meta.url), 'utf8');

function client(configured, fetchImpl) {
  const window = {
    location: { origin: 'http://127.0.0.1:8000', hostname: '127.0.0.1' },
    CEC_TUTOR_ENDPOINT: configured,
    fetch: fetchImpl
  };
  runInNewContext(source, { window, URL, Response });
  return window.CECTutor;
}

test('transport sends exactly lesson_id and student_message and preserves SSE consumption', async () => {
  let wireBody;
  const transport = client('http://127.0.0.1:8787/robo/v1/tutor', async (url, options) => {
    assert.equal(url, 'http://127.0.0.1:8787/robo/v1/tutor');
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

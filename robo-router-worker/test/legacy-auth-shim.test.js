import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { runInNewContext } from 'node:vm';

const shimSource = readFileSync(
  new URL('../../assets/cec-legacy-auth-shim.js', import.meta.url),
  'utf8'
);
const legacyEndpoint = 'https://cec-robo.cecenglishcamp.workers.dev/api/ai/chat/completions';
const approvedApiEndpoint = 'https://api.cecenglishcamp.com/api/ai/chat/completions';
const repositoryRoot = fileURLToPath(new URL('../../', import.meta.url));

function htmlFiles(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const absolutePath = join(directory, entry.name);
    if (entry.isDirectory()) return htmlFiles(absolutePath);
    return entry.isFile() && entry.name.endsWith('.html') ? [absolutePath] : [];
  });
}

function installShim({ protectedSession, publicSession, responseStatus = 200 } = {}) {
  const calls = [];
  const logs = [];
  let sessionCalls = 0;
  let redirects = 0;
  const nativeFetch = async (input, init) => {
    calls.push({ input, init });
    return new Response(null, { status: responseStatus });
  };
  const window = {
    location: {
      href: 'https://cecenglishcamp.com/grammar-camp/G02/example.html',
      origin: 'https://cecenglishcamp.com',
      hostname: 'cecenglishcamp.com',
      replace() { redirects += 1; }
    },
    fetch: nativeFetch,
    supabase: {
      createClient() {
        return {
          auth: {
            async getSession() {
              sessionCalls += 1;
              if (publicSession instanceof Error) throw publicSession;
              return { data: { session: publicSession || null } };
            }
          }
        };
      }
    }
  };
  if (protectedSession !== undefined) {
    window.CECAuthSession = {
      async getSession() {
        sessionCalls += 1;
        if (protectedSession instanceof Error) throw protectedSession;
        return protectedSession;
      }
    };
  }
  const console = {
    log(value) { logs.push(value); },
    warn(value) { logs.push(value); },
    error(value) { logs.push(value); }
  };
  runInNewContext(shimSource, {
    window,
    document: {},
    console,
    URL,
    Request,
    Headers,
    Response
  });
  return {
    window,
    calls,
    logs,
    get sessionCalls() { return sessionCalls; },
    get redirects() { return redirects; }
  };
}

function authorization(call) {
  return new Headers(call.init && call.init.headers).get('Authorization');
}

test('protected page session adds bearer only to the legacy AI endpoint', async () => {
  const harness = installShim({
    protectedSession: { access_token: 'synthetic-protected-token' }
  });

  await harness.window.fetch(legacyEndpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: '{}'
  });

  assert.equal(harness.calls.length, 1);
  assert.equal(authorization(harness.calls[0]), 'Bearer synthetic-protected-token');
  assert.equal(harness.sessionCalls, 1);
});

test('both exact approved legacy POST endpoints receive bearer authorization', async () => {
  for (const endpoint of [legacyEndpoint, approvedApiEndpoint]) {
    const harness = installShim({
      protectedSession: { access_token: 'synthetic-approved-host-token' }
    });

    await harness.window.fetch(endpoint, { method: 'POST' });

    assert.equal(authorization(harness.calls[0]), 'Bearer synthetic-approved-host-token');
    assert.equal(harness.sessionCalls, 1);
  }
});

test('wrong path, GET, and unrelated host remain untouched', async () => {
  const cases = [
    ['https://cec-robo.cecenglishcamp.workers.dev/api/ai/not-chat', { method: 'POST' }],
    [approvedApiEndpoint, { method: 'GET' }],
    ['https://api.cecenglishcamp.com.evil.example/api/ai/chat/completions', { method: 'POST' }]
  ];

  for (const [endpoint, init] of cases) {
    const harness = installShim({
      protectedSession: { access_token: 'synthetic-unrelated-token' }
    });

    await harness.window.fetch(endpoint, init);

    assert.equal(authorization(harness.calls[0]), null);
    assert.equal(harness.sessionCalls, 0);
  }
});

test('expired or invalid browser session sends no bearer and preserves server 401', async () => {
  for (const protectedSession of [null, new Error('synthetic expired session')]) {
    const harness = installShim({ protectedSession, responseStatus: 401 });
    const response = await harness.window.fetch(legacyEndpoint, { method: 'POST' });

    assert.equal(response.status, 401);
    assert.equal(authorization(harness.calls[0]), null);
  }
});

test('unrelated fetch is unchanged and does not consult auth', async () => {
  const harness = installShim({
    protectedSession: { access_token: 'synthetic-protected-token' }
  });
  const init = { method: 'POST', headers: { 'X-Unrelated': 'unchanged' }, body: 'data' };

  await harness.window.fetch('https://example.test/api', init);

  assert.equal(harness.calls.length, 1);
  assert.equal(harness.calls[0].input, 'https://example.test/api');
  assert.equal(harness.calls[0].init, init);
  assert.equal(harness.sessionCalls, 0);
});

test('public page without a session remains viewable and AI receives no bearer', async () => {
  const harness = installShim({ publicSession: null, responseStatus: 401 });

  const response = await harness.window.fetch(legacyEndpoint, { method: 'POST' });

  assert.equal(response.status, 401);
  assert.equal(authorization(harness.calls[0]), null);
  assert.equal(harness.redirects, 0);
});

test('public page with an existing session adds bearer without redirect', async () => {
  const harness = installShim({
    publicSession: { access_token: 'synthetic-public-token' }
  });

  await harness.window.fetch(legacyEndpoint, { method: 'POST' });

  assert.equal(authorization(harness.calls[0]), 'Bearer synthetic-public-token');
  assert.equal(harness.redirects, 0);
});

test('shim does not log tokens and shared entrypoints load it without HTML tokens', async () => {
  const harness = installShim({
    protectedSession: { access_token: 'synthetic-private-token' }
  });
  await harness.window.fetch(legacyEndpoint, { method: 'POST' });

  assert.deepEqual(harness.logs, []);
  for (const relativePath of [
    '../../assets/require-auth.js',
    '../../assets/require-auth-v16.js',
    '../../grammar-camp/grammar_story_map.js'
  ]) {
    const source = readFileSync(new URL(relativePath, import.meta.url), 'utf8');
    assert.match(source, /\/assets\/cec-legacy-auth-shim\.js\?v=1/);
    assert.ok(!source.includes('synthetic-private-token'));
  }
});

test('all current legacy pages are covered without bulk HTML edits', () => {
  const candidates = ['camp-a', 'camp-b', 'camp-c', 'grammar-camp']
    .flatMap(directory => htmlFiles(join(repositoryRoot, directory)));
  const legacyPages = candidates.filter(file => readFileSync(file, 'utf8').includes(legacyEndpoint));
  const protectedPages = [];
  const publicPages = [];

  for (const file of legacyPages) {
    const page = readFileSync(file, 'utf8');
    assert.ok(!page.includes('/assets/cec-legacy-auth-shim.js'));
    if (/\/assets\/require-auth(?:-v16)?\.js/.test(page)) protectedPages.push(file);
    else {
      assert.match(page, /<script\s+src="\.\.\/grammar_story_map\.js"><\/script>/);
      publicPages.push(file);
    }
  }

  assert.equal(legacyPages.length, 1256);
  assert.equal(protectedPages.length, 1177);
  assert.equal(publicPages.length, 79);
});

test('standalone Grade 3 lesson loads the non-redirect shim and its caller is covered', () => {
  const page = readFileSync(
    new URL('../../lessons/grade3/week01.html', import.meta.url),
    'utf8'
  );
  const aiTutor = readFileSync(
    new URL('../../camp-a/assets/ai-tutor.js', import.meta.url),
    'utf8'
  );

  assert.match(page, /<script src="\/assets\/cec-legacy-auth-shim\.js\?v=1"><\/script>/);
  assert.ok(!page.includes('require-auth.js'));
  assert.ok(!page.includes('require-auth-v16.js'));
  assert.ok(page.includes(approvedApiEndpoint));
  assert.ok(aiTutor.includes(approvedApiEndpoint));
  assert.ok(!page.includes('synthetic-approved-host-token'));
  assert.ok(!aiTutor.includes('synthetic-approved-host-token'));
});

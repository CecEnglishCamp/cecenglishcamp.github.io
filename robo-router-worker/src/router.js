import lessons from './lessons.json' with { type: 'json' };
import { systemPrompt } from './profiles.js';

const PATH = '/robo/v1/tutor';
const UPSTREAM = 'https://api.openai.com/v1/chat/completions';
export const MODEL = 'gpt-4o-mini';
export const OUTPUT_TOKENS = 300;
const FORBIDDEN = ['system', 'developer', 'system_prompt', 'developer_prompt', 'messages', 'instructions', 'profile', 'model', 'safety', 'context'];

function json(body, status = 200, origin = null) {
  return new Response(JSON.stringify(body), { status, headers: {
    'Content-Type': 'application/json', 'Cache-Control': 'no-store',
    ...(origin ? { 'Access-Control-Allow-Origin': origin, Vary: 'Origin' } : {})
  } });
}
export function createTutor({ fetchImpl = fetch, catalog = lessons } = {}) {
  return { async fetch(request, env = {}) {
    // Explicit origins only. No wildcard and no credential-bearing debug logs.
    const origin = request.headers.get('Origin');
    const origins = String(env.ALLOWED_ORIGINS || '').split(',').map(x => x.trim()).filter(Boolean);
    if (origin && !origins.includes(origin)) return json({ ok: false, code: 'ORIGIN_DENIED' }, 403);
    if (new URL(request.url).pathname !== PATH) return json({ ok: false, code: 'NOT_FOUND' }, 404, origin);
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: {
      ...(origin ? { 'Access-Control-Allow-Origin': origin, Vary: 'Origin' } : {}),
      'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    } });
    if (request.method !== 'POST') return json({ ok: false, code: 'METHOD_NOT_ALLOWED' }, 405, origin);
    if (!(request.headers.get('Content-Type') || '').startsWith('application/json')) return json({ ok: false, code: 'INVALID_REQUEST' }, 400, origin);
    let body;
    try { body = await request.json(); } catch { return json({ ok: false, code: 'INVALID_REQUEST' }, 400, origin); }
    if (!body || typeof body !== 'object' || Array.isArray(body) || FORBIDDEN.some(key => Object.hasOwn(body, key)) ||
      typeof body.lesson_id !== 'string' || typeof body.student_message !== 'string' || !body.student_message.trim()) {
      return json({ ok: false, code: 'INVALID_REQUEST' }, 400, origin);
    }
    const lesson = Object.hasOwn(catalog, body.lesson_id) && catalog[body.lesson_id];
    if (!lesson) return json({ ok: false, code: 'UNKNOWN_LESSON' }, 400, origin);
    // Candidate is deliberately disabled until account/privacy review is complete.
    if (env.TUTOR_ENABLED !== 'true' || !env.OPENAI_API_KEY) return json({ ok: false, code: 'TUTOR_NOT_CONFIGURED' }, 503, origin);
    const messages = [
      { role: 'system', content: systemPrompt(lesson.profile) },
      { role: 'user', content: JSON.stringify({ lesson: { id: body.lesson_id, facts: lesson.context }, student_message: body.student_message }) }
    ];
    try {
      const response = await fetchImpl(UPSTREAM, { method: 'POST', headers: {
        'Content-Type': 'application/json', Authorization: `Bearer ${env.OPENAI_API_KEY}`
      }, body: JSON.stringify({ model: MODEL, messages, max_tokens: OUTPUT_TOKENS, stream: false }) });
      if (!response.ok) return json({ ok: false, code: 'AI_UPSTREAM_ERROR' }, 502, origin);
      const data = await response.json();
      const text = data?.choices?.[0]?.message?.content;
      if (typeof text !== 'string' || !text.trim()) return json({ ok: false, code: 'AI_INVALID_RESPONSE' }, 502, origin);
      return json({ ok: true, lesson_id: body.lesson_id, reply: text }, 200, origin);
    } catch { return json({ ok: false, code: 'AI_UPSTREAM_ERROR' }, 502, origin); }
  } };
}

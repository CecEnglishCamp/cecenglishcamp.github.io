import { profileForLesson, systemInstructions } from './profiles.js';

export const TUTOR_PATH = '/robo/v1/tutor';
export const OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions';
export const MODEL = 'gpt-4o-mini';
export const MAX_TOKENS = 300;
export const MAX_STUDENT_MESSAGE_CHARS = 4000;

const ALLOWED_FIELDS = new Set(['lesson_id', 'student_message']);

function json(body, status, origin) {
  const headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  };
  if (origin) {
    headers['Access-Control-Allow-Origin'] = origin;
    headers.Vary = 'Origin';
  }
  return new Response(JSON.stringify(body), { status, headers });
}

function allowedOrigin(request, env) {
  const origin = request.headers.get('Origin');
  if (!origin) return { origin: null, allowed: true };
  const configured = String(env.ALLOWED_ORIGINS || '')
    .split(',')
    .map(value => value.trim())
    .filter(Boolean);
  return { origin, allowed: configured.includes(origin) };
}

function validateBody(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) return null;
  if (Object.keys(body).some(key => !ALLOWED_FIELDS.has(key))) return null;
  if (typeof body.lesson_id !== 'string' || typeof body.student_message !== 'string') return null;

  const lessonId = body.lesson_id.trim();
  const studentMessage = body.student_message.trim();
  if (!lessonId || !studentMessage || studentMessage.length > MAX_STUDENT_MESSAGE_CHARS) return null;

  const profile = profileForLesson(lessonId);
  return profile ? { lessonId, studentMessage, profile } : null;
}

export function createTutorRouter({ fetchImpl = fetch } = {}) {
  return {
    async fetch(request, env = {}) {
      const url = new URL(request.url);
      if (url.pathname !== TUTOR_PATH) {
        return json({ ok: false, code: 'NOT_FOUND' }, 404, null);
      }

      const originCheck = allowedOrigin(request, env);
      if (!originCheck.allowed) {
        return json({ ok: false, code: 'ORIGIN_DENIED' }, 403, null);
      }

      if (request.method === 'OPTIONS') {
        return new Response(null, {
          status: 204,
          headers: {
            ...(originCheck.origin ? {
              'Access-Control-Allow-Origin': originCheck.origin,
              Vary: 'Origin'
            } : {}),
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
          }
        });
      }

      if (request.method !== 'POST') {
        return json({ ok: false, code: 'METHOD_NOT_ALLOWED' }, 405, originCheck.origin);
      }
      if (!(request.headers.get('Content-Type') || '').toLowerCase().startsWith('application/json')) {
        return json({ ok: false, code: 'INVALID_REQUEST' }, 400, originCheck.origin);
      }

      let requestBody;
      try {
        requestBody = await request.json();
      } catch {
        return json({ ok: false, code: 'INVALID_REQUEST' }, 400, originCheck.origin);
      }

      const input = validateBody(requestBody);
      if (!input) {
        return json({ ok: false, code: 'INVALID_REQUEST' }, 400, originCheck.origin);
      }
      if (!env.OPENAI_API_KEY) {
        return json({ ok: false, code: 'TUTOR_NOT_CONFIGURED' }, 503, originCheck.origin);
      }

      const upstreamBody = {
        model: MODEL,
        max_tokens: MAX_TOKENS,
        stream: false,
        messages: [
          { role: 'system', content: systemInstructions(input.profile) },
          {
            role: 'user',
            content: JSON.stringify({
              lesson_id: input.lessonId,
              student_message: input.studentMessage
            })
          }
        ]
      };

      try {
        const upstream = await fetchImpl(OPENAI_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${env.OPENAI_API_KEY}`
          },
          body: JSON.stringify(upstreamBody)
        });

        if (!upstream.ok) {
          return json({ ok: false, code: 'AI_UPSTREAM_ERROR' }, 502, originCheck.origin);
        }
        const data = await upstream.json();
        const reply = data?.choices?.[0]?.message?.content;
        if (typeof reply !== 'string' || !reply.trim()) {
          return json({ ok: false, code: 'AI_INVALID_RESPONSE' }, 502, originCheck.origin);
        }
        return json({ ok: true, lesson_id: input.lessonId, reply }, 200, originCheck.origin);
      } catch {
        return json({ ok: false, code: 'AI_UPSTREAM_ERROR' }, 502, originCheck.origin);
      }
    }
  };
}

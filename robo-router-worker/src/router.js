import { profileForLesson, systemInstructions } from './profiles.js';

export const TUTOR_PATH = '/robo/v1/tutor';
export const OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions';
export const MODEL = 'gpt-4o-mini';
export const MAX_TOKENS = 300;
export const MAX_STUDENT_MESSAGE_CHARS = 4000;
export const MAX_REQUEST_BYTES = 16 * 1024;
export const UPSTREAM_TIMEOUT_MS = 15_000;
export const ALLOWED_REQUEST_FIELDS = Object.freeze(['lesson_id', 'student_message']);
export const EMAIL_REDACTION = '[EMAIL REDACTED]';
export const PHONE_REDACTION = '[PHONE REDACTED]';

const ALLOWED_FIELDS = new Set(ALLOWED_REQUEST_FIELDS);
const SIMPLE_EMAIL_PATTERN = /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/gi;
const SIMPLE_PHONE_CANDIDATE_PATTERN = /\+?\d[\d().\s-]{5,}\d/g;

export function redactEmailAddresses(value) {
  return value.replace(SIMPLE_EMAIL_PATTERN, EMAIL_REDACTION);
}

export function redactPhoneNumbers(value) {
  return value.replace(SIMPLE_PHONE_CANDIDATE_PATTERN, candidate => {
    const digitCount = candidate.replace(/\D/g, '').length;
    return digitCount >= 7 && digitCount <= 15 ? PHONE_REDACTION : candidate;
  });
}

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

async function verifyAuthenticatedUser(request, env, fetchImpl) {
  const authorization = request.headers.get('Authorization') || '';
  const match = authorization.match(/^Bearer\s+(\S+)$/i);
  if (!match) return { ok: false, status: 401, code: 'AUTH_REQUIRED' };
  if (!env.SUPABASE_URL || !env.SUPABASE_ANON_KEY) {
    return { ok: false, status: 503, code: 'AUTH_NOT_CONFIGURED' };
  }

  let authUrl;
  try {
    authUrl = new URL('/auth/v1/user', env.SUPABASE_URL).href;
  } catch {
    return { ok: false, status: 503, code: 'AUTH_NOT_CONFIGURED' };
  }

  try {
    const response = await fetchImpl(authUrl, {
      method: 'GET',
      headers: {
        apikey: env.SUPABASE_ANON_KEY,
        Authorization: `Bearer ${match[1]}`
      }
    });
    if (!response.ok) return { ok: false, status: 401, code: 'AUTH_INVALID' };
    const user = await response.json();
    if (!user || typeof user.id !== 'string' || !user.id) {
      return { ok: false, status: 401, code: 'AUTH_INVALID' };
    }
    return { ok: true, userId: user.id };
  } catch {
    return { ok: false, status: 401, code: 'AUTH_INVALID' };
  }
}

function validateBody(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) return null;
  if (Object.keys(body).some(key => !ALLOWED_FIELDS.has(key))) return null;
  if (typeof body.lesson_id !== 'string' || typeof body.student_message !== 'string') return null;

  const lessonId = body.lesson_id.trim();
  const studentMessage = body.student_message.trim();
  if (!lessonId || !studentMessage || studentMessage.length > MAX_STUDENT_MESSAGE_CHARS) return null;
  const redactedStudentMessage = redactPhoneNumbers(redactEmailAddresses(studentMessage));

  const profile = profileForLesson(lessonId);
  return profile ? { lessonId, studentMessage: redactedStudentMessage, profile } : null;
}

export function createTutorRouter({
  fetchImpl = fetch,
  upstreamTimeoutMs = UPSTREAM_TIMEOUT_MS
} = {}) {
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
            'Access-Control-Allow-Headers': 'Authorization, Content-Type'
          }
        });
      }

      if (request.method !== 'POST') {
        return json({ ok: false, code: 'METHOD_NOT_ALLOWED' }, 405, originCheck.origin);
      }

      const authentication = await verifyAuthenticatedUser(request, env, fetchImpl);
      if (!authentication.ok) {
        return json(
          { ok: false, code: authentication.code },
          authentication.status,
          originCheck.origin
        );
      }
      if (!(request.headers.get('Content-Type') || '').toLowerCase().startsWith('application/json')) {
        return json({ ok: false, code: 'INVALID_REQUEST' }, 400, originCheck.origin);
      }

      const contentLength = Number(request.headers.get('Content-Length'));
      if (Number.isFinite(contentLength) && contentLength > MAX_REQUEST_BYTES) {
        return json({ ok: false, code: 'INVALID_REQUEST' }, 400, originCheck.origin);
      }

      let requestBody;
      try {
        const rawBody = await request.text();
        if (new TextEncoder().encode(rawBody).byteLength > MAX_REQUEST_BYTES) {
          return json({ ok: false, code: 'INVALID_REQUEST' }, 400, originCheck.origin);
        }
        requestBody = JSON.parse(rawBody);
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

      const upstreamController = new AbortController();
      const upstreamTimeout = setTimeout(
        () => upstreamController.abort(),
        upstreamTimeoutMs
      );

      try {
        const upstream = await fetchImpl(OPENAI_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${env.OPENAI_API_KEY}`
          },
          body: JSON.stringify(upstreamBody),
          signal: upstreamController.signal
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
        if (upstreamController.signal.aborted) {
          return json({ ok: false, code: 'AI_UPSTREAM_TIMEOUT' }, 504, originCheck.origin);
        }
        return json({ ok: false, code: 'AI_UPSTREAM_ERROR' }, 502, originCheck.origin);
      } finally {
        clearTimeout(upstreamTimeout);
      }
    }
  };
}

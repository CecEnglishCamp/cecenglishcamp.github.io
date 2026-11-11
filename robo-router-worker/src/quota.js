// Durable per-user quota for /robo/v1/tutor.
// Fixed windows (1 minute, 1 day). One Durable Object instance per verified user id.
// Cloudflare Durable Object storage is not touched by this repository until the owner
// adds the binding in Cloudflare (see README "OWNER ACTION REQUIRED").

const MINUTE_MS = 60_000;
const DAY_MS = 86_400_000;
const STATE_KEY = 'quota';

function positiveInteger(value) {
  return Number.isInteger(value) && value > 0 ? value : null;
}

export class TutorQuota {
  constructor(state, _env, clock = Date.now) {
    this.state = state;
    this.clock = clock;
  }

  async fetch(request) {
    if (request.method !== 'POST') return Response.json({ allowed: false, scope: 'invalid' }, { status: 405 });
    let input;
    try {
      input = await request.json();
    } catch {
      return Response.json({ allowed: false, scope: 'invalid' }, { status: 400 });
    }
    const perMinute = positiveInteger(input?.limits?.perMinute);
    const perDay = positiveInteger(input?.limits?.perDay);
    if (!perMinute || !perDay) return Response.json({ allowed: false, scope: 'invalid' }, { status: 400 });

    const now = this.clock();
    const stored = (await this.state.storage.get(STATE_KEY)) || {};
    let { minuteStart = now, minuteCount = 0, dayStart = now, dayCount = 0 } = stored;
    if (now - minuteStart >= MINUTE_MS) { minuteStart = now; minuteCount = 0; }
    if (now - dayStart >= DAY_MS) { dayStart = now; dayCount = 0; }

    if (dayCount >= perDay) {
      return Response.json({
        allowed: false,
        scope: 'day',
        retryAfterSeconds: Math.max(1, Math.ceil((dayStart + DAY_MS - now) / 1000))
      });
    }
    if (minuteCount >= perMinute) {
      return Response.json({
        allowed: false,
        scope: 'minute',
        retryAfterSeconds: Math.max(1, Math.ceil((minuteStart + MINUTE_MS - now) / 1000))
      });
    }

    await this.state.storage.put(STATE_KEY, {
      minuteStart,
      minuteCount: minuteCount + 1,
      dayStart,
      dayCount: dayCount + 1
    });
    return Response.json({ allowed: true });
  }
}

export function createDurableQuotaLimiter(namespace) {
  return {
    async consume({ userId, limits }) {
      const stub = namespace.get(namespace.idFromName(userId));
      const response = await stub.fetch('https://tutor-quota.internal/consume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ limits })
      });
      if (!response.ok) throw new Error('QUOTA_UNAVAILABLE');
      return response.json();
    }
  };
}

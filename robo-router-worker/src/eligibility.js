export const PLAN_B_2_FALLBACK = Object.freeze({
  mode: 'rules_based',
  plan: 'PLAN_B_2'
});

export const ZDR_APPROVED_VALUE = 'true';
export const ELIGIBILITY_RESOLVER_TIMEOUT_MS = 250;
export const ELIGIBILITY_STATES = Object.freeze({
  ELIGIBLE: 'eligible',
  RESTRICTED: 'restricted',
  UNKNOWN: 'unknown'
});

const VALID_STATES = new Set(Object.values(ELIGIBILITY_STATES));

export function serverZdrApproved(env) {
  return env?.ZDR_APPROVED === ZDR_APPROVED_VALUE;
}

function normalizeEligibility(result) {
  const state = result?.state ?? result?.policy;
  return VALID_STATES.has(state) ? state : ELIGIBILITY_STATES.UNKNOWN;
}

export function createServerEligibilityPolicy({
  trustedSource,
  timeoutMs = ELIGIBILITY_RESOLVER_TIMEOUT_MS
} = {}) {
  // Server bootstrap owns this function. A future adapter may call a Cloudflare
  // Service Binding/RPC or another trusted data source through `env`; request
  // data and arbitrary env objects are never treated as an eligibility source.
  const source = typeof trustedSource === 'function' ? trustedSource : null;

  return Object.freeze({
    async resolve({ env, userId, lessonId }) {
      if (!source) return ELIGIBILITY_STATES.UNKNOWN;

      let timeout;
      try {
        const sourceResult = Promise.resolve()
          .then(() => source({ env, userId, lessonId }))
          .then(normalizeEligibility, () => ELIGIBILITY_STATES.UNKNOWN);
        const timeoutResult = new Promise(resolve => {
          timeout = setTimeout(() => resolve(ELIGIBILITY_STATES.UNKNOWN), timeoutMs);
        });
        return await Promise.race([sourceResult, timeoutResult]);
      } catch {
        return ELIGIBILITY_STATES.UNKNOWN;
      } finally {
        clearTimeout(timeout);
      }
    }
  });
}

export function eligibilityDecision(state, zdrApproved = false) {
  if (!zdrApproved) {
    return { allowed: false, reason: 'ZDR_APPROVAL_REQUIRED' };
  }
  if (state === ELIGIBILITY_STATES.RESTRICTED) {
    return { allowed: false, reason: 'ELIGIBILITY_RESTRICTED' };
  }
  if (state !== ELIGIBILITY_STATES.ELIGIBLE) {
    return { allowed: false, reason: 'ELIGIBILITY_UNAVAILABLE' };
  }
  return { allowed: true };
}

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

export async function resolveServerEligibility({
  env,
  userId,
  lessonId,
  timeoutMs = ELIGIBILITY_RESOLVER_TIMEOUT_MS
}) {
  const resolver = env?.TUTOR_ELIGIBILITY_RESOLVER;
  if (!resolver || typeof resolver.resolve !== 'function') {
    return ELIGIBILITY_STATES.UNKNOWN;
  }

  let timeout;
  try {
    const resolverResult = Promise.resolve()
      .then(() => resolver.resolve({ userId, lessonId }))
      .then(normalizeEligibility, () => ELIGIBILITY_STATES.UNKNOWN);
    const timeoutResult = new Promise(resolve => {
      timeout = setTimeout(() => resolve(ELIGIBILITY_STATES.UNKNOWN), timeoutMs);
    });
    return await Promise.race([resolverResult, timeoutResult]);
  } catch {
    return ELIGIBILITY_STATES.UNKNOWN;
  } finally {
    clearTimeout(timeout);
  }
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

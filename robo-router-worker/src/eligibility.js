export const PLAN_B_2_FALLBACK = Object.freeze({
  mode: 'rules_based',
  plan: 'PLAN_B_2'
});

export const ZDR_APPROVED_VALUE = 'true';

const VALID_POLICY_FLAGS = new Set(['eligible', 'protected']);

export function serverZdrApproved(env) {
  return env?.ZDR_APPROVED === ZDR_APPROVED_VALUE;
}

export async function resolveServerEligibility({ env, userId, lessonId }) {
  const resolver = env?.TUTOR_ELIGIBILITY_RESOLVER;
  if (!resolver || typeof resolver.resolve !== 'function') return null;

  const result = await resolver.resolve({ userId, lessonId });
  if (!result || !VALID_POLICY_FLAGS.has(result.policy)) return null;
  return {
    policy: result.policy,
    guardianConsentConfirmed: result.guardianConsentConfirmed === true
  };
}

export function eligibilityDecision(eligibility, zdrApproved = false) {
  if (!zdrApproved) {
    return { allowed: false, reason: 'ZDR_APPROVAL_REQUIRED' };
  }
  if (!eligibility) {
    return { allowed: false, reason: 'ELIGIBILITY_UNAVAILABLE' };
  }
  return { allowed: true };
}

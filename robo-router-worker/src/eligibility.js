export const PLAN_B_2_FALLBACK = Object.freeze({
  mode: 'rules_based',
  plan: 'PLAN_B_2'
});

const VALID_POLICY_FLAGS = new Set(['eligible', 'protected']);

export async function resolveServerEligibility({ request, env, lessonId }) {
  const resolver = env?.TUTOR_ELIGIBILITY_RESOLVER;
  if (!resolver || typeof resolver.resolve !== 'function') return null;

  const result = await resolver.resolve({ request, lessonId });
  if (!result || !VALID_POLICY_FLAGS.has(result.policy)) return null;
  return {
    policy: result.policy,
    guardianConsentConfirmed: result.guardianConsentConfirmed === true,
    zdrApproved: result.zdrApproved === true
  };
}

export function eligibilityDecision(eligibility) {
  if (!eligibility) {
    return { allowed: false, reason: 'ELIGIBILITY_UNAVAILABLE' };
  }
  if (eligibility.policy === 'protected' && !eligibility.zdrApproved) {
    return { allowed: false, reason: 'ZDR_APPROVAL_REQUIRED' };
  }
  return { allowed: true };
}

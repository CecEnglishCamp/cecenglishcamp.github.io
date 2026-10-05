# Task #8 change record

Before: baseline 9845749ad43fb5e5b01a99a340b9a071ef337658; 1,260 duplicated main lesson callers forward browser system instructions. Existing AI Workers are not in this repository. Read-only audit completed before this branch; repository files were not modified during that phase. Full baseline inventory/report remains outside the checkout in /workspace/cec-audit.

Plan recorded before changes: add an isolated candidate Worker, fixed four-profile safety policy, static server-owned lesson catalog, common transport and surgical main-family caller migration. Do not overwrite registration, rewrite curriculum, deploy, or call a live model. Preserve existing local fallbacks. Legacy draft and Cecil routes remain separately inventoried and unmodified. Production service wiring must be reviewed with its source owner before release.

Actual changes and validation results: recorded below after implementation.

Rollback: before merge, close the PR/delete this branch (main is unchanged). If later approved/merged, revert the Task #8 merge as one change. No deployment or account rollback is needed for this task because none is performed. Future deployment rollback requires the owner to restore the prior Worker version and frontend together; do not point migrated pages at the old chat-completions contract.

Review correction plan: catalog generation initially omitted .key-eng and b2Text facts, and the removed B GB_SYSTEM declaration left an unused browser prompt builder. Add these curriculum selectors plus static PAGE_DATA fact fields; remove only the unused prompt builder/assignment; preserve greeting and fallback state. Re-run catalog and all tests. No production action.

Runtime correction plan: first actual workerd startup rejected named constant exports in the Worker entry module. Separate the testable router module from a default-handler-only entry point, then rerun Node tests and local workerd HTTP checks. This fixes an observed platform incompatibility without any production action.

Plan for review artifacts: persist the completed baseline audit and inventories under review/task-2 so reviewers can assess the migration without chat access. This happens on the implementation branch after the read-only audit phase; it does not change the statement that the audit itself left repository files unchanged.

Actual changes: migrated 1,260 main-family page transports to one shared client; browser wire fields are lesson_id and student_message only. Added four server-owned profiles and the common safety baseline, bounded static server catalog + deterministic generator, disabled candidate Worker configuration, mock tests and integration/release/rollback documentation. Existing hosted GPT links, local fallback/greetings and legacy draft/Cecil routes remain; the registration Worker is untouched. Catalog review correction includes original B static lesson sentence metadata and reading text, and A key sentence/topic selectors. The unused B browser system-prompt builder was removed.

Tests: 25 Node tests passed, 0 failed/skipped (synthetic data/mock upstream only). All 1,260 migrated pages have one common client and one matched server lesson ID; all inline JavaScript parses. All 1,260 pages' non-script curriculum/layout content is unchanged against the immutable baseline. Actual local workerd startup passed after entry-module correction. Internal HTTP checks: explicit-origin OPTIONS 204; disabled registered request 503 TUTOR_NOT_CONFIGURED; unknown lesson 400 UNKNOWN_LESSON; browser system override 400 INVALID_REQUEST. git diff --check passed. No live model inference or student-data test performed. Model-level adversarial effectiveness remains untested.

Release limitation: the new Worker is not wired to existing production services and is disabled by default. Authentication, quotas, input/output timeouts and PII protections remain separate #9/#10 prerequisites. This branch is suitable for draft review, not merge/deployment.

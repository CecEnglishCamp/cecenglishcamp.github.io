# Task #8-F2 Item 1 — Tutor auth and eligibility audit

Scope: only the undeployed `POST /robo/v1/tutor` request path on branch
`task-8-f2-under13-ai-gate`. No learner records or production services were
queried.

## Current request path

1. `src/index.js` exports `createTutorRouter()` without an authentication or
   identity adapter.
2. `src/router.js` checks the route, configured CORS origin, method, content
   type, JSON syntax, and request-body shape.
3. `validateBody()` accepts exactly `lesson_id` and `student_message`, resolves
   the server-owned lesson profile/context, and rejects every additional
   browser field.
4. After confirming `OPENAI_API_KEY` exists, the router sends the resolved
   server prompt and student message to the AI upstream.

## Server-side eligibility information currently available

| Information | Available? | Evidence |
| --- | --- | --- |
| Authenticated learner identity/session | No | No authorization/session header is read and no auth verifier is called in `src/router.js`. CORS is an origin check, not learner authentication. |
| Learner age or protected-learner status | No | No age, birth date, age band, or server-owned protection flag is resolved. |
| Guardian consent | No | No guardian or consent record/claim is read or verified. |
| ZDR approval | No | No ZDR policy flag, approval record, or environment setting is read. |
| Lesson/course age guidance | Yes, but not learner eligibility | `profileForLesson()` selects a server-owned teaching profile, and `SAFETY_RULES` requires age-appropriate content. This describes lesson behavior, not the learner's verified status or consent. |
| Browser eligibility claims | Not accepted | The request allowlist contains only `lesson_id` and `student_message`; any age/guardian/ZDR field is currently rejected as `INVALID_REQUEST`. |

## Gate-relevant conclusion

The server currently has **no authoritative learner eligibility input** from
which to decide whether generative AI is allowed. Guardian consent cannot
currently bypass a gate because it is not present or verified at all. A later
item must introduce a server-controlled eligibility resolver/policy boundary
before the `OPENAI_API_KEY` check and before `fetchImpl(OPENAI_ENDPOINT, ...)`.
The browser payload must remain limited to `lesson_id` and `student_message`.


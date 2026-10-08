# CEC Tutor Router Core — Task #8A

This is an undeployed, standalone Worker candidate for `POST /robo/v1/tutor`.
It does not replace or proxy the existing `/api/ai/chat/completions` route and does
not modify any lesson page.

Accepted JSON fields:

```json
{
  "lesson_id": "/camp-a/grade3/week01a.html",
  "student_message": "Please explain this lesson."
}
```

The server maps the lesson path to `camp-a`, `camp-b`, `camp-c`, or `grammar` and
owns the system instructions, safety rules, OpenAI model, and output-token limit.
Any additional browser field is rejected, including `messages`, `system`,
`developer`, `model`, and `max_tokens`.

## Server-controlled eligibility boundary

The browser cannot assert or override age eligibility, protected-learner status,
guardian approval, or ZDR approval. Request JSON is limited to `lesson_id` and
`student_message`; extra fields are rejected. Eligibility comes from a trusted
server-code policy source injected when the router is created, not from an
arbitrary runtime JavaScript object in `env`. The source interface can later wrap
a reviewed Cloudflare Service Binding/RPC or another trusted server-side data
source. Until one is wired, eligibility is `unknown` and fails closed. Guardian
consent alone does not permit generative AI without server-confirmed ZDR
approval.

## PII minimization

Before forwarding `student_message`, the router applies simple pattern-based
redaction for email addresses and phone-number-like strings containing 7–15
digits. This is a narrow safeguard, not comprehensive PII detection: unusual
formats may be missed and unrelated numeric text may be redacted.

Run synthetic tests without a live OpenAI request:

```sh
npm test --prefix robo-router-worker
```

`OPENAI_API_KEY` must be supplied as a Worker secret in any separately reviewed
future deployment. No secret value belongs in this repository.

`/robo/v1/tutor` also requires `Authorization: Bearer <Supabase access token>`.
The Worker independently validates the token through Supabase Auth before reading
the Tutor request body or contacting OpenAI. A future deployment must configure
`SUPABASE_URL` and `SUPABASE_ANON_KEY` as Worker bindings. Do not store production
binding values in this repository.

Authenticated requests are limited to 10 accepted Tutor requests per minute and
100 per day. The router passes only the verified Supabase user ID, a SHA-256
session-token digest, and those limits to an injected `TUTOR_QUOTA_LIMITER`
binding. The binding must provide an async `consume(input)` method and return
`{ allowed: true }` or `{ allowed: false, scope: "minute" | "day",
retryAfterSeconds }`. Missing or unavailable quota enforcement fails closed
before OpenAI is contacted.

**OWNER ACTION REQUIRED:** before any deployment, provide an atomically updated,
durable implementation of `TUTOR_QUOTA_LIMITER` (for example a separately
reviewed Durable Object or service binding) and configure its Cloudflare binding.
No Cloudflare resource or production setting is created by this repository. Do
not substitute isolate memory or non-atomic read/then-write KV counters.

## Durable quota and metadata logging (Claude local patch, not deployed)

`src/quota.js` provides `TutorQuota`, a Durable Object class that counts accepted
requests per verified Supabase user id (fixed windows: 10 per minute, 100 per day).
The router uses it automatically when a Durable Object namespace is bound as
`TUTOR_QUOTA`; an injected `TUTOR_QUOTA_LIMITER` still takes priority. If neither is
configured the router still fails closed (503 `QUOTA_NOT_CONFIGURED`) before OpenAI.

**OWNER ACTION REQUIRED (Cloudflare, not done here):** after review, add to the
Worker configuration a Durable Object binding named `TUTOR_QUOTA` with class
`TutorQuota` and the matching migration (`new_sqlite_classes` or `new_classes`).
No Cloudflare resource was created by this repository change.

Each request emits one JSON log line with only: `request_id`, `method`, `status`,
`code`, `latency_ms`, `profile`, `quota` outcome and token `usage` counts. It never
contains the student message, prompts, replies, bearer tokens, API keys or user ids.
The same `request_id` is returned in the `X-Request-Id` response header. Cloudflare
Worker Logs for the real Worker must also be enabled by the owner to retain them.

## Rollback

No deployment or merge is part of Task #8. Before merge, rollback is deleting the
Task #8 branches or closing their PR. If these commits are merged later, revert the
Task #8 commits together so the shared transport and four sample-page references
are removed in the same change. If a future deployment occurs, restore the prior
Worker version and the four prior page versions together; do not leave sample pages
pointing at an unavailable `/robo/v1/tutor` route.

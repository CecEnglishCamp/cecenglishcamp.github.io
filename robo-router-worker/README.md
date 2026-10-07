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
`student_message`; extra fields are rejected. `TUTOR_ELIGIBILITY_RESOLVER` is the
only authority for eligibility flags and must derive them from authenticated
identity plus server-held policy/consent records, never browser body, query, or
header claims. Missing or invalid resolver results fail closed, and guardian
consent alone does not permit a protected learner to use generative AI without
server-confirmed ZDR approval.

Run synthetic tests without a live OpenAI request:

```sh
npm test --prefix robo-router-worker
```

`OPENAI_API_KEY` must be supplied as a Worker secret in any separately reviewed
future deployment. No secret value belongs in this repository.

## Rollback

No deployment or merge is part of Task #8. Before merge, rollback is deleting the
Task #8 branches or closing their PR. If these commits are merged later, revert the
Task #8 commits together so the shared transport and four sample-page references
are removed in the same change. If a future deployment occurs, restore the prior
Worker version and the four prior page versions together; do not leave sample pages
pointing at an unavailable `/robo/v1/tutor` route.

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

Run synthetic tests without a live OpenAI request:

```sh
npm test --prefix robo-router-worker
```

`OPENAI_API_KEY` must be supplied as a Worker secret in any separately reviewed
future deployment. No secret value belongs in this repository.

# Candidate Tutor Router — Task #8

This directory is a new, disabled candidate. It is not the source of any deployed CEC AI Worker and must not be deployed or merged as a working production integration. `worker/` remains the unrelated registration Worker and is untouched.

The contract is POST `/robo/v1/tutor` with `lesson_id` (exact registered page path) and `student_message`. The server selects one of camp-a, camp-b, camp-c or grammar, applies the shared safety baseline, and resolves static lesson facts. The browser cannot provide system/developer roles, model, tutor profile, safety rules or context. `src/lessons.json` covers 432 A + 648 B + 100 C + 80 Grammar pages. Regenerate from the repository root with `python3 robo-router-worker/tools/build-catalog.py`; review the generated facts with curriculum changes. Facts include title, book/author/key sentence, static PAGE_DATA sentence metadata and relevant reading/topic DOM content, bounded at 12,000 characters; they are not a full curriculum rewrite.

The common client `assets/cec-tutor.js` sends just the two fields and converts the JSON reply into an escaped SSE event for the existing page consumers. This preserves the page UI contract but buffers one complete reply rather than progressively streaming upstream deltas. The server selects gpt-4o-mini, uses `/v1/chat/completions`, fixes output to 300 tokens, and is stateless. These statements describe the candidate only; they do not establish the legacy deployed Worker's upstream behavior. Existing local fallback/greeting/UI and hosted GPT links are retained. Legacy draft and Cecil chat clients are outside this migration and are listed in the audit.

## Verification without model calls

From the repository root: `npm test --prefix robo-router-worker` (Node >=22, no dependency installation). Tests inject a mock model transport and synthetic data only. They verify all four profiles, shared safety rules, rejection of browser role/config overrides, separation of injection strings from system instructions, catalog/caller coverage, page JavaScript syntax, normal response mapping, endpoint configuration and safe transport rendering. They do not prove live-model safety or actual resistance to arbitrary injection.

Local Worker runtime check, from the repository root:

```sh
XDG_CONFIG_HOME=/workspace/.cec-tools/config WRANGLER_SEND_METRICS=false \
  /workspace/.cec-tools/node_modules/.bin/wrangler dev \
  --config robo-router-worker/wrangler.toml --local --ip 127.0.0.1 --port 8788 \
  --persist-to /workspace/.cec-tools/tutor-local
```

With the supplied disabled config, explicit local-origin preflight returns 204; registered requests return 503 TUTOR_NOT_CONFIGURED; unknown lessons and system overrides return 400. No live OpenAI request is needed for these checks. The browser endpoint is intentionally unset; for reviewed local testing only, set `window.CEC_TUTOR_ENDPOINT` to the local `/robo/v1/tutor` endpoint. Do not publish loopback preview links.

## Release prerequisites (not performed)

Obtain/review the deployed Robo router source and choose its integration owner. Decide candidate integration versus a separate Worker. Wire the frontend endpoint through reviewed configuration, not a fallback to the browser-controlled legacy contract. Review remaining hosted ChatGPT GPT links and legacy routes separately; safety controls here cannot govern hosted GPT instruction sets. Finish separate #9 PII protection and #10 server authentication/entitlements, durable quota, bounded inputs/output, timeouts and cost controls. Review provider privacy/ZDR, Worker Logs and OpenAI project budget. Bind required secrets in Cloudflare's secure settings only; never place values in the repository or reports. No live student/model testing is authorized without the required privacy review.

Do not enable TUTOR_ENABLED or configure production endpoint routing merely to test this branch. Current tests establish structural security and local runtime support, not production readiness.

## Rollback

Before merge: close the PR and discard the branch; main/production have not changed. After any separately authorized future merge: revert the Task #8 merge. After a separately authorized deployment: restore the prior frontend and Worker version together using the owner's release process. No merge, deployment or account changes occurred here.

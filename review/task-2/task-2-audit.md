# Task #2 — Robo extended audit

Read-only audit baseline: `9845749ad43fb5e5b01a99a340b9a071ef337658`.
Claude's prior audit was not supplied or found in the checkout; conclusions below come from repository inspection. No production service was queried with student data or model input. Full current-tree inventories are in robo-inventory.csv, grammar-script-coverage.csv, and credential-findings.csv. This is a current tracked-source audit, not a Git-history credential audit.

## Executive summary

The site contains 1,260 inline main-family AI callers: Camp A 432, Camp B 648, Camp C 100, Grammar 80. These send browser-selected system messages and model options to a deployed legacy Worker. The source of that AI Worker and of the newer production/preview Robo routers is absent: the only Worker source in this repository implements registration. Consequently, actual upstream API, credential storage, server auth, rate limits, logging, and isolation cannot be confirmed. Frontend page gates are not server authorization. Most callers do not send a bearer token and have no enforced input ceiling, timeout, or daily budget.

## Complete file/path inventory

robo-inventory.csv lists every matching tracked AI caller/helper and relevant auth/integration file, exact endpoint URLs, request line references, and script coverage (1,272 entries). Grammar-script-coverage.csv lists all 161 Grammar HTML files: 80 inline AI callers, 80 alternate *_new pages and the index. None loads the common fallback helper or require-auth script. The common fallback helper is camp-a/assets/ai-tutor.js, loaded by only two matched pages. Prompt/streaming logic is extensively duplicated.

Representative verified paths: camp-a/grade3/week01a.html:377, camp-a/grade4/week01a.html:344; camp-b/m3/week01a.html:1104 and camp-b/g2/week01a.html; camp-c/ep01.html:607; grammar-camp/G01/G01_be_verb_present_tense.html:682 and grammar-camp/G02/G02_articles_a,_an,_the.html:689; lessons/grade3/week01.html:674; _draft/week01a_test.html:650. Common/auth code: assets/require-auth.js, assets/require-auth-v16.js, assets/student-context.js, assets/learning-progress.js, assets/auth-nav.js, assets/cec-admin-check.js. helpdesk-robo-preview.html submits inquiries, not an OpenAI request. alternate-gpt-links.csv additionally inventories 3,177 external GPT link references across 1,522 files (seven literal/template URL forms), including Mom Teacher, Camp C2, writing/speaking, archived and other routes. These launch hosted ChatGPT GPTs rather than the repository Worker. Their external instruction sets, OpenAI APIs, logging, accounts and privacy policies are not inspectable here; the new router cannot enforce policy on these independently hosted GPTs. worker/src/index.js is registration, not Robo.

## Data flow

Main lesson -> inline gbSend/gbAsk/gbQuick -> browser constructs context + student text + tutor instructions -> browser system/user roles + model/options -> https://cec-robo.cecenglishcamp.workers.dev/api/ai/chat/completions -> [deployed source unavailable; upstream unverified] -> SSE choices[].delta.content -> inline DOM.

Legacy lesson -> SYS + unbounded in-memory chatHist + student text -> https://api.cecenglishcamp.com/api/ai/chat/completions -> [proxy source unavailable; nginx auth injection is a comment, not verified configuration] -> JSON choices[0].message.content.

Draft -> single user role/context -> https://journey-bronzy-fruitily.ngrok-free.dev/api/chat/completions -> unknown upstream -> JSON response.

Page gate -> Supabase session/household entitlement -> browser redirect. Separately: student-context -> authorized student list/admin check on production or preview router; learning-progress -> authenticated progress POST. These identity/progress calls are not evidence that identity is sent to OpenAI.

## Request schemas

| Family | Fields sent | Browser instructions/context | Browser limits |
| --- | --- | --- | --- |
| Main A/B/C, G01 | model, messages[{role,content}], max_tokens, stream | Browser system prompt; book/week/key sentence/topic + student question + age/language instruction in user content. B g2/g3 builds GB_SYSTEM from PAGE_DATA and DOM reading content (216 pages). | max_tokens 300; 400 in 216 B pages; no server-enforced evidence |
| Grammar G02–G80 | same fields | Browser system prompt; fullContent prefixes GB_TOPIC and suffixes middle/high-school Korean instruction | max_tokens 300 |
| lessons/grade3/week01.html | model, messages | SYS + complete growing history + student text; nginx-specific header | No explicit output/input cap |
| _draft/week01a_test.html | model, messages, stream:false | userContent includes instructions/context | No explicit output cap |
| student context (non-model) | GET with bearer token | server returns id, display_name, grade_level | Not AI input |
| learning progress (non-model) | student_id, lesson_id, event, curriculum_year, curriculum_version; bearer header | account/student context used for progress only | lesson ID length 80; timeout 5s |
| preview inquiries (non-model) | inquiry form payload | contact information in inquiry workflow | Not established as model input |

## PII findings

Main AI requests contain no separate name, student ID, email, school, account, parent, or auth fields. They do send free-form student text, which can include any volunteered PII; there is no redaction. The legacy caller retains and resends conversational text in memory, increasing exposure. Curriculum character/author names are lesson content, not evidence of real student PII. Identity-bearing student-context/progress requests must remain separate from model payload construction. No real student data was read or used.

## Prompt/instruction findings

The browser supplies system messages and all age/learning instructions; anyone can alter the payload. Without the deployed Worker source, promotion/forwarding cannot be verified, but this interface exposes that risk. Student text mixed into instructional strings creates injection ambiguity. Main context is book/topic/sentence; full curriculum resolution is absent. No common privacy/child-safety baseline is enforced in visible server code. Client sanitization hides connectivity errors rather than enforcing tutor policy. Legacy accumulated history may include model text and student content; a server-fixed stateless lesson API should not accept client system/developer/history objects.

## Auth/rate-limit/size/error/log findings

1,180 matched files load require-auth, which checks Supabase/household subscription and has trial route exceptions. Main AI fetches only send Content-Type, not a verified session token. Browser redirects can be bypassed. Grammar callers have no auth script. Server-side auth/rate limits, per-IP/per-user counters, request bytes and response ceilings remain unknown. Browser max_tokens is editable. Main streaming catches non-200/network errors, ignores malformed SSE JSON, shows a friendly fallback, and lacks timeout/cancel enforcement. Legacy history has no ceiling. Some fallback code logs error strings; legacy code logs caught errors; deployed request/prompt logging is unknown. Inline Robo user/model rendering uses innerHTML, creating a separate injection/XSS risk; no production exploit was attempted.

## OpenAI endpoints and credentials

No tracked Robo server calls api.openai.com; /v1/chat/completions, /v1/responses, conversations, audio, realtime and actual upstream models cannot be confirmed from a browser proxy URL. Browser payload labels gpt-4o-mini do not prove upstream routing. No OpenAI-style secret or private-key pattern was found in the scanned tracked text files. This is not proof of absence in history, external Worker secrets, binary files, or arbitrary encodings. Public Supabase publishable configuration exists; values are deliberately omitted. worker/src/index.js:73 contains a hardcoded administrator secret comparison (value omitted), unrelated to Robo. Secret storage for deployed AI services is unavailable to audit.

## Risk assessment

High: browser-selected instruction roles; unverified server auth; cost abuse without demonstrated durable quotas; volunteered PII forwarded; raw innerHTML sinks. Medium/high: missing shared child-safety policy and model output review; legacy history increases disclosure. Hosted GPT launches are an additional uncontrolled tutor path: decide whether to retire them or provide a reviewed replacement; no new safety guarantee extends to them. Cross-user leakage is not demonstrated: visible main calls are stateless, but deployed storage/log/session isolation is unknown. No ZDR approval was confirmed; live AI/student testing must remain blocked. No prompts were sent to OpenAI during this audit.

## Implementation plan and minimal file set

#8: add a separately reviewable candidate Robo Worker (do not overwrite registration or deploy to legacy services), fixed A/B/C/Grammar profiles with one safety baseline, a server-owned static lesson catalog and a shared browser transport; migrate the 1,260 main-family call sites to lesson_id + student_message. Keep local fallback, curriculum and unrelated legacy routes intact; document those remaining legacy routes. Reject unknown IDs and system/developer/model overrides. Test payload construction and routing with mock upstream only. Existing deployed router source/integration ownership must be confirmed before release.

#9: strict allowlisted request schema, structured-field rejection, bounded bytes/message/context and conservative email/phone/ID text redaction; model body never contains authentication or student/account fields. Document that names/addresses cannot be comprehensively detected and that data minimization, not regex, is primary protection.

#10: require bearer verification through the configured Supabase auth service, server-owned entitlement decision, durable per-user minute/day accounting and optional per-IP controls, fixed output tokens, bounded output bytes, timeout and structured errors. Fail closed on missing configuration; no token/prompt logging. Account actions: bind quota Durable Object and auth/entitlement configuration, review Worker Logs, set OpenAI project monthly budget, confirm ZDR before any real student/model test. No deployment or account changes in this task.

Task #35 proposal: separately fix registration D1 multiline exec() CREATE TABLE failure and remove/rework its hardcoded administrative comparison. Do not mix registration changes into #8/#9/#10.

Repository files were not modified.

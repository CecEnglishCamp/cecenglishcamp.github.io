# Robo v2 page configs (2026-11-12) — review branch

This branch adds data and tooling only. **No lesson page changes**, so students keep the existing Robo on every page except G3 W1D1, which is already live.

## Contents
- `camp-a/assets/robo-v2/pages/<task>.json` (431 files): one Robo v2 config per Camp A lesson page (G3–G6, week01–36, a/b/c).
  - Each config is extracted from its own page: book, week, day, key sentence, story text, and word cards.
  - Nothing is copied from other pages or from G3 W1D1.
  - Every config has `teacherApproved:false`, `autoDraft:true` and an empty `fixed` (no quick answers).
  - `pageSha256` binds each config to the exact page version it was extracted from.
  - Game answers are not included.
- `_tools/robo-v2/apply_approved_pages.py`: swaps a page to the v2 widget, the same way the G3 W1D1 pilot was swapped. It runs a check by default and changes pages only with `--apply`. A page qualifies only if all of these hold:
  - the teacher checklist row has `approve=YES` and three `Y` checks (story, words, no quiz answer exposed);
  - a checker name and date are filled in;
  - the checklist row's `pageSha256` matches the config and current lesson page;
  - the checklist row's `configSha256` matches the exact config JSON file bytes. The checklist must record this hash when the teacher approves the config.

  The tool never touches the Worker, KV or the AI allowlist; those are separate approval steps.

## Not included
- Camp B (648 pages) is not covered: the Worker `cec-robo-v2` accepts only `g3`–`g6` task IDs, so Camp B needs separate compatibility work.
- No deploy, no Worker or KV change, no AI allowlist change.

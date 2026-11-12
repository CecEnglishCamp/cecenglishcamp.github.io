# -*- coding: utf-8 -*-
"""Robo v2 — 교사 승인된 Camp A 페이지만 새 위젯으로 교체 (G3 W1D1 파일럿과 같은 방식).
사용:  python _tools/robo-v2/apply_approved_pages.py --checklist <TEACHER_CHECKLIST_432.csv> [--tasks g4-w1-d1,...] [--apply]
기본은 점검만(dry-run). --apply 일 때만 수업 페이지를 고친다. 배포·Worker·KV는 건드리지 않는다.

교체 조건(모두 만족해야 함 — 하나라도 아니면 그 페이지는 예전 Robo 그대로):
  1) 확인표 approve=YES, 교사 3칸(이야기·단어·정답 노출 없음)=Y, 확인자·날짜 있음
  2) 확인표 pageSha256 = 설정 파일 pageSha256 = 지금 페이지 sha256 (승인 뒤 페이지가 바뀌면 무효)
  3) 페이지에 예전 Robo 블록이 정확히 한 벌 있고, 아직 새 위젯이 없음
교체 내용: 예전 Robo 스타일·채팅 블록 삭제(페이지 고유 스크립트는 남김), /camp-a/assets/ai-tutor.js 참조 삭제,
          </head> 앞에 위젯 CSS, </body> 앞에 v2-env.js + window.ROBO_PAGE + 위젯 JS.
서버 쪽(APPROVED_TASK_IDS, KV approved:true)은 별도 승인 단계다. 이 도구는 서버를 바꾸지 않는다.
"""
import sys, os, re, json, csv, hashlib, argparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CFGDIR = os.path.join(ROOT, "camp-a", "assets", "robo-v2", "pages")
ASSET = os.path.join(ROOT, "camp-a", "assets", "robo-v2")
S_MARK = ("<!-- ===== CEC Robo Helper styles ===== -->", "<!-- ===== /CEC Robo Helper styles ===== -->")
W_MARK = ("<!-- ===== CEC Robo Helper ===== -->", "<!-- ===== /CEC Robo Helper ===== -->")
DRAFT = " (draft, teacher check needed)"
sha = lambda b: hashlib.sha256(b).hexdigest()


def cut(h, a, b):
    if h.count(a) != 1 or h.count(b) != 1: return None
    i, j = h.find(a), h.find(b)
    if not (0 <= i < j): return None
    return h[:i] + h[j + len(b):]


def strip_robo(h):
    """예전 Robo 스타일 블록 + 채팅 UI·Robo IIFE 삭제. 같은 <script> 안의 페이지 고유 함수는 남긴다. 형태가 다르면 None."""
    h1 = cut(h, *S_MARK)
    if h1 is None or h1.count(W_MARK[0]) != 1 or h1.count(W_MARK[1]) != 1: return None
    i = h1.index(W_MARK[0]); j = h1.index(W_MARK[1]) + len(W_MARK[1]); blk = h1[i:j]
    if blk.count("<script>") != 1 or blk.count("</script>") != 1: return None
    sp = blk.index("<script>")
    if not blk[sp:].startswith("<script>\n(function(){\n  if(window.__gbRoboInit)"): return None
    e = blk.index("})();", sp) + 5; se = blk.rindex("</script>")
    tail = blk[e:se]
    keep = ("<script>" + tail.rstrip("\n") + "\n</script>\n") if tail.strip() else ""
    return h1[:i] + keep + h1[j:]


def versions():
    v = {}
    for f in ("robo_v2_t.css", "v2-env.js", "robo_v2_t.js"):
        v[f] = sha(open(os.path.join(ASSET, f), "rb").read())[:12]
    return v


def approved_page_cfg(cfg, by, date):
    """승인용 ROBO_PAGE: 초안 표시 제거, teacherApproved true. 고정 답은 설정 파일에 있는 것만(새로 만들지 않음)."""
    out = {k: v for k, v in cfg.items() if k not in ("task", "pageSha256")}
    # The page's 🆕 is an editorial marker, not lesson vocabulary. Remove it from
    # all Robo-facing facts so it can never be shown or prompted to students.
    out["facts"] = {
        k.replace(DRAFT, ""): (v.replace("🆕", "").strip() if isinstance(v, str) else v)
        for k, v in cfg.get("facts", {}).items()
    }
    out["autoDraft"] = False
    out["teacherApproved"] = True
    out["checked"] = dict(cfg.get("checked") or {}); out["checked"].update({"story": True, "wordCards": True})
    out["source"] = "%s 교사 확인: 이야기·단어·정답 노출 점검 (%s). 원본 페이지 sha256 %s" % (by, date, cfg.get("pageSha256", "")[:16])
    out["endpoint"] = ""
    return out


def transform(h, page_cfg, v):
    """수업 페이지 HTML + ROBO_PAGE 객체 -> 교체된 HTML. 실패 시 (None, 이유)."""
    if "robo_v2_t.js" in h: return None, "already-v2"
    h2 = strip_robo(h)
    if h2 is None: return None, "old-robo-shape"
    h2 = re.sub(r'<script src="/camp-a/assets/ai-tutor\.js[^"]*"></script>', "", h2)  # 줄바꿈은 남김(파일럿과 같은 결과)
    if h2.count("</head>") != 1 or h2.count("</body>") != 1: return None, "head-body-shape"
    js = json.dumps(page_cfg, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    h2 = h2.replace("</head>", '<link rel="stylesheet" href="/camp-a/assets/robo-v2/robo_v2_t.css?v=%s">\n</head>' % v["robo_v2_t.css"])
    h2 = h2.replace("</body>", '<script src="/camp-a/assets/robo-v2/v2-env.js?v=%s"></script>\n<script>window.ROBO_PAGE=%s;</script>\n<script src="/camp-a/assets/robo-v2/robo_v2_t.js?v=%s"></script>\n</body>' % (v["v2-env.js"], js, v["robo_v2_t.js"]))
    return h2, ""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--checklist", required=True); ap.add_argument("--tasks", default=""); ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    with open(a.checklist, encoding="utf-8-sig", newline="") as f: chk = {r["task"]: r for r in csv.DictReader(f)}
    want = set(filter(None, a.tasks.split(","))); v = versions(); done = skip = 0
    for fn in sorted(os.listdir(CFGDIR)):
        if not fn.endswith(".json"): continue
        cfg_path = os.path.join(CFGDIR, fn)
        cfg_raw = open(cfg_path, "rb").read()
        cfg = json.loads(cfg_raw.decode("utf-8")); tid = cfg["task"]
        if want and tid not in want: continue
        rel = "camp-a/grade%d/week%02d%s.html" % (cfg["grade"], cfg["week"], "abc"[cfg["day"] - 1]); p = os.path.join(ROOT, rel)
        raw = open(p, "rb").read(); r = chk.get(tid, {})
        why = []
        if r.get("approve") != "YES": why.append("미승인")
        if [r.get(k) for k in ("teacher_bodyMatchesScreen", "teacher_wordsMatchScreen", "teacher_noQuizAnswerExposed")] != ["Y", "Y", "Y"]: why.append("교사 3칸 미완")
        if not (r.get("teacher_checkedBy") and r.get("teacher_checkedDate")): why.append("확인자·날짜 없음")
        cfg_path = os.path.join(CFGDIR, fn)
        cfg_raw = open(cfg_path, "rb").read()
        cfg_sha = sha(cfg_raw)
        if not (r.get("configSha256") and r.get("configSha256") == cfg_sha):
            why.append("설정 파일 해시 불일치 또는 확인표 configSha256 누락(승인 무효)")
        if not (r.get("pageSha256") == cfg.get("pageSha256") == sha(raw)): why.append("페이지 해시 불일치(승인 무효)")
        if why: skip += 1; (want and print("유지(예전 Robo) %s: %s" % (tid, ", ".join(why)))); continue
        out, err = transform(raw.decode("utf-8"), approved_page_cfg(cfg, r["teacher_checkedBy"], r["teacher_checkedDate"]), v)
        if out is None: skip += 1; print("유지(예전 Robo) %s: %s" % (tid, err)); continue
        ob = out.encode("utf-8"); done += 1
        print("%s %s %s: %s -> %s" % ("교체" if a.apply else "교체 예정", tid, rel, sha(raw)[:16], sha(ob)[:16]))
        if a.apply: open(p, "wb").write(ob)
    print("결과: %s %d쪽, 예전 Robo 유지 %d쪽. 서버(APPROVED_TASK_IDS·KV)는 바꾸지 않았다." % ("교체" if a.apply else "교체 예정", done, skip))


if __name__ == "__main__":
    main()

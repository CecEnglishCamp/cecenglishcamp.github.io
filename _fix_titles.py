"""Fill missing/empty <title> tags using path-based heuristics."""
import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r"C:\Users\cecsu\cecenglishcamp.github.io")
SKIP_DIRS = {".git", "_archive_20260412", ".wrangler", "node_modules", "_draft", "__pycache__"}

RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
RE_HEAD_OPEN = re.compile(r"<head[^>]*>", re.I)


def make_title(rel: str) -> str:
    p = rel.replace("\\", "/")

    m = re.match(r"camp-a/grade(\d)/week(\d{1,2})([a-c])\.html", p)
    if m:
        g, w, var = m.groups()
        return f"Camp A · Grade {g} · Week {int(w)}{var.upper()} | CEC English Camp"

    m = re.match(r"camp-b/(g\d|m\d|hs)/week(\d{1,2})([a-z])?\.html", p)
    if m:
        grp, w, _ = m.groups()
        label = {"g1":"Grade 4","g2":"Grade 5","g3":"Grade 6",
                 "m1":"Middle 1","m2":"Middle 2","m3":"Middle 3","hs":"High"}.get(grp, grp.upper())
        return f"Camp B · {label} · Week {int(w)} | CEC English Camp"

    m = re.match(r"camp-c/ep(\d{1,3})\.html", p)
    if m:
        return f"Camp C · EP{int(m.group(1))} | CEC English Camp"

    m = re.match(r"grammar-camp/G(\d{2})(?:/G\d{2}_new\.html|/index\.html|/.*\.html)", p)
    if m:
        return f"Grammar Base Camp · G{m.group(1)} | CEC English Camp"

    m = re.match(r"essay-camp/(.+?)\.html", p)
    if m:
        return f"Essay Camp · {m.group(1)} | CEC English Camp"

    m = re.match(r"mom-teacher/grade(\d)/ep(\d{1,3})\.html", p)
    if m:
        return f"Mom Teacher · Grade {m.group(1)} · EP{int(m.group(2))} | CEC English Camp"

    m = re.match(r"speaking/(.+?)\.html", p)
    if m:
        return f"Speaking · {m.group(1).replace('_',' ').title()} | CEC English Camp"

    if p.endswith("/index.html"):
        section = p.rsplit("/index.html",1)[0].split("/")
        label = " · ".join(s.replace("-"," ").title() for s in section if s)
        return f"{label} | CEC English Camp" if label else "CEC English Camp"

    name = Path(p).stem.replace("-"," ").replace("_"," ").title()
    return f"{name} | CEC English Camp"


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = path.relative_to(ROOT).as_posix()
    new_title = make_title(rel)

    m = RE_TITLE.search(text)
    if m and m.group(1).strip():
        return False  # already has non-empty title

    if m:
        # empty title - replace
        text = text[:m.start()] + f"<title>{new_title}</title>" + text[m.end():]
    else:
        # no title - inject after <head>
        m2 = RE_HEAD_OPEN.search(text)
        if not m2:
            return False
        text = text[:m2.end()] + f"\n<title>{new_title}</title>" + text[m2.end():]

    path.write_text(text, encoding="utf-8")
    return True


def main():
    fixed = 0
    for p in ROOT.rglob("*.html"):
        if any(x.startswith(".") or x in SKIP_DIRS for x in p.relative_to(ROOT).parts):
            continue
        if process(p):
            fixed += 1
    print(f"[fixed] {fixed} files")


if __name__ == "__main__":
    main()

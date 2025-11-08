import argparse, os, re, zipfile, shutil, tempfile, unicodedata
from pathlib import Path

# ---------- utils ----------
def slugify(text: str) -> str:
    # ascii만 남기고 공백/특수문자 -> _
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return text[:60] or "episode"

def find_episode_number(name: str) -> int:
    # 파일명/본문에서 1,2,3… 추출 (Season 1, Episode 3 등)
    m = re.search(r"[Ee]pisode\s*([0-9]+)", name)
    if m:
        return int(m.group(1))
    nums = re.findall(r"\d+", name)
    return int(nums[0]) if nums else 0

def first_heading(md_text: str) -> str:
    for line in md_text.splitlines():
        if line.strip().startswith("#"):
            return line.lstrip("# ").strip()
    return ""

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description="Organize Notion export -> B_Camp structure")
    ap.add_argument("--zip", help="Path to Notion export zip (Season1).", required=False)
    ap.add_argument("--src", help="OR a folder that already contains exported .md files.", required=False)
    ap.add_argument("--out-root", required=True, help="Root of repo, e.g. .../cecenglishcamp.github.io")
    ap.add_argument("--series", default="RoboJumpMe", help="Series folder name")
    ap.add_argument("--season", type=int, default=1, help="Season number (e.g., 1)")
    args = ap.parse_args()

    if not args.zip and not args.src:
        ap.error("Provide --zip OR --src")

    out_dir = Path(args.out_root) / "B_Camp" / args.series / f"Season{args.season}"
    (out_dir / "audio").mkdir(parents=True, exist_ok=True)

    # 1) 준비: md 파일 모으기
    tmp = None
    if args.zip:
        tmp = Path(tempfile.mkdtemp(prefix="rjm_"))
        with zipfile.ZipFile(args.zip, "r") as zf:
            zf.extractall(tmp)
        src_dir = tmp
    else:
        src_dir = Path(args.src)

    md_files = sorted([p for p in Path(src_dir).rglob("*.md")])

    if not md_files:
        print("No .md files found. Check --zip/--src path.")
        return

    # 2) 에피소드 목록 구성
    episodes = []
    for p in md_files:
        text = p.read_text(encoding="utf-8", errors="ignore")
        ep_no = find_episode_number(p.name + " " + text)
        title = first_heading(text) or f"Season {args.season}, Episode {ep_no}"
        episodes.append((ep_no, title, text))

    # 중복/0번 정리 및 정렬
    episodes = [e for e in episodes if e[0] > 0]
    episodes.sort(key=lambda x: x[0])

    # 3) 파일 쓰기
    links = []
    for ep_no, title, text in episodes:
        slug = slugify(title)
        new_name = f"S{args.season}E{ep_no}_{slug}.md"
        (out_dir / new_name).write_text(text, encoding="utf-8")
        links.append((ep_no, title, new_name))

    # 4) index.md 생성
    lines = [
        f"# 🤖 Robo, Jump & Me — Season {args.season}",
        "> Level: B1–B2  |  Theme: Humanity vs Technology",
        "",
        "## 📘 Episode List",
    ]
    for ep_no, title, fname in links:
        display = re.sub(r"^\s*#\s*", "", title).strip()
        lines.append(f"{ep_no}. [{display}](./{fname})")
    lines.append("\n🎧 [Audio Folder](./audio/)\n")

    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")

    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"✅ Done! Wrote {len(links)} episodes to: {out_dir}")
    print("   - index.md created")
    for _, t, f in links[:5]:
        print(f"   - {f}  ← {t}")

if __name__ == "__main__":
    main()

"""Build a plain-Markdown mirror of the OpenAI Codex docs for GitHub Pages.

Usage: python scripts/sync.py [--out build] [--base-url https://user.github.io/repo]

Fetches the Codex llms.txt index, downloads every page's Markdown version,
follows links to pages missing from the index, and rewrites links between
pages to relative .md paths. Output is raw Markdown (no HTML, no theme):
  <out>/llms.txt      index for LLMs, with absolute links into the mirror
  <out>/README.md     same index with relative links
  <out>/docs/...      the pages
"""
import argparse, os, pathlib, re, shutil, urllib.request

INDEX = "https://developers.openai.com/codex/llms.txt"
SITE = "https://learn.chatgpt.com"
OFFICIAL = "https://developers.openai.com/codex"
EXTRA = ["config-schema.json", "llms-full.txt"]

NOTICE = f"""> **Unofficial offline mirror** of the OpenAI Codex documentation, for environments where the official site isn't reachable.
> Not affiliated with or endorsed by OpenAI. The authoritative, up-to-date docs are at {OFFICIAL} . All content (c) OpenAI.
"""


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "docs-mirror"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def build(out, base_url):
    docs = out / "docs"
    shutil.rmtree(out, ignore_errors=True)
    docs.mkdir(parents=True)

    def save(slug, data):
        p = docs / slug
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)

    index = get(INDEX).decode("utf-8")
    pages = sorted(set(re.findall(rf"{re.escape(SITE)}/docs/([^\s)]+\.md)", index)))
    ok = 0
    for slug in pages:
        try:
            save(slug, get(f"{SITE}/docs/{slug}")); ok += 1
        except Exception as e:
            print("FAIL", slug, e)
    for name in EXTRA:
        try:
            save(name, get(f"{SITE}/docs/{name}"))
        except Exception as e:
            print("FAIL", name, e)

    # Follow links to pages that aren't listed in the index.
    link = re.compile(rf"{re.escape(SITE)}/docs/([A-Za-z0-9_\-/]+?)(?:\.md)?(?=[)?#\s])")
    tried = set()
    while True:
        want = {s.rstrip("/") for f in docs.rglob("*.md") for s in link.findall(f.read_text("utf-8"))}
        want = {s for s in want if s and s not in tried and not (docs / f"{s}.md").exists()}
        if not want:
            break
        for s in want:
            tried.add(s)
            try:
                data = get(f"{SITE}/docs/{s}.md")
                if not data.lstrip().startswith(b"<"):
                    save(f"{s}.md", data); ok += 1
            except Exception:
                pass

    if ok < 50:
        raise SystemExit(f"Only {ok} pages downloaded; aborting")

    # Rewrite links between pages to relative .md paths; add the notice to each page.
    page_link = re.compile(rf"\]\({re.escape(SITE)}/docs/([^)#?\s]*?)(?:\.md)?(\?[^)#\s]*)?(#[^)\s]*)?\)")
    for f in docs.rglob("*.md"):
        t = f.read_text("utf-8")

        def rep(m):
            target = docs / (m.group(1).rstrip("/") + ".md")
            if not target.exists():
                return m.group(0)
            return f"]({pathlib.Path(os.path.relpath(target, f.parent)).as_posix()}{m.group(3) or ''})"

        t = page_link.sub(rep, t)
        idx = pathlib.Path(os.path.relpath(out / "llms.txt", f.parent)).as_posix()
        t = t.replace(f"]({SITE}/llms.txt)", f"]({idx})").replace("](/llms.txt)", f"]({idx})")
        f.write_text(NOTICE + "\n" + t, "utf-8")

    # Index files: llms.txt (absolute URLs when base_url is known) and README.md (relative).
    entry = re.compile(rf"\]\({re.escape(SITE)}/docs/([^\s)]+\.(?:md|txt))\)")

    def index_with(prefix):
        lines = []
        for line in index.splitlines():
            m = entry.search(line)
            if m and not (docs / m.group(1)).exists():
                continue
            lines.append(entry.sub(lambda m: f"]({prefix}docs/{m.group(1)})", line))
        return "\n".join(lines)

    body = index_with(base_url.rstrip("/") + "/" if base_url else "")
    (out / "llms.txt").write_text(NOTICE + "\n" + body + "\n", "utf-8")
    (out / "README.md").write_text(NOTICE + "\n" + index_with("") + "\n", "utf-8")
    (out / ".nojekyll").write_text("")  # serve .md files raw instead of rendering them
    print(f"Built {ok} pages into {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="build")
    ap.add_argument("--base-url", default=os.environ.get("BASE_URL", ""))
    a = ap.parse_args()
    build(pathlib.Path(a.out).resolve(), a.base_url)

# Codex docs offline mirror

Unofficial plain-Markdown mirror of the [OpenAI Codex docs](https://developers.openai.com/codex), meant for feeding to LLMs where the official site isn't reachable. Not affiliated with OpenAI; the official docs are the source of truth. All doc content (c) OpenAI.

No docs are stored in this repo. A GitHub Action (`.github/workflows/sync.yml`) runs daily, fetches the current docs with `scripts/sync.py`, and deploys them to GitHub Pages as raw Markdown:

- `/llms.txt` - index of every page (absolute links)
- `/docs/<page>.md` - each page, with links between pages rewritten to relative `.md` paths
- `/docs/llms-full.txt` - all docs in one file

- `/urls.txt` - plain list of every file URL, for bulk downloads

## Download a local copy

Cloning this repo won't give you the docs (it only holds the sync code). Pull them from the mirror instead.
This creates a `codex-docs/` folder with `llms.txt`, `README.md` and `docs/`, and the links between pages keep working:

```bash
wget -x -nH --cut-dirs=1 -P codex-docs -i https://dxrsz.github.io/codex-docs-mirror/urls.txt
```

Without wget (bash/Git Bash):

```bash
B=https://dxrsz.github.io/codex-docs-mirror; curl -s $B/urls.txt | while read -r u; do curl -s --create-dirs -o "codex-docs/${u#$B/}" "$u"; done
```

Just want one file? `curl -O https://dxrsz.github.io/codex-docs-mirror/docs/llms-full.txt` has everything.

## Rebuild

`python scripts/sync.py --out build` (fetches from the official site, so it needs access to it).

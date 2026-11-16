# Codex docs offline mirror

Unofficial plain-Markdown mirror of the [OpenAI Codex docs](https://developers.openai.com/codex), meant for feeding to LLMs where the official site isn't reachable. Not affiliated with OpenAI; the official docs are the source of truth. All doc content (c) OpenAI.

No docs are stored in this repo. A GitHub Action (`.github/workflows/sync.yml`) runs daily, fetches the current docs with `scripts/sync.py`, and deploys them to GitHub Pages as raw Markdown:

- `/llms.txt` - index of every page (absolute links)
- `/docs/<page>.md` - each page, with links between pages rewritten to relative `.md` paths
- `/docs/llms-full.txt` - all docs in one file

Build locally: `python scripts/sync.py --out build`

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

## Point Codex's `openai-docs` skill at this mirror

Codex ships a bundled `openai-docs` skill that reads docs from developers.openai.com and the OpenAI Docs MCP server, which doesn't help if those are blocked. You can't just edit it: bundled skills live in `~/.codex/skills/.system/` and Codex overwrites that folder when it updates. A skill with the same name doesn't replace it either (Codex shows both). Instead, install [`skills/openai-docs-mirror`](skills/openai-docs-mirror/SKILL.md) and turn off the bundled one.

1. Install the mirror skill into your user skills folder:

   ```bash
   mkdir -p ~/.agents/skills/openai-docs-mirror && curl -sL https://raw.githubusercontent.com/dxrsz/codex-docs-mirror/main/skills/openai-docs-mirror/SKILL.md -o ~/.agents/skills/openai-docs-mirror/SKILL.md
   ```

   PowerShell:

   ```powershell
   New-Item -ItemType Directory -Force "$HOME\.agents\skills\openai-docs-mirror" | Out-Null; Invoke-WebRequest https://raw.githubusercontent.com/dxrsz/codex-docs-mirror/main/skills/openai-docs-mirror/SKILL.md -OutFile "$HOME\.agents\skills\openai-docs-mirror\SKILL.md"
   ```

2. Disable the bundled skill by adding this to `~/.codex/config.toml`:

   ```toml
   [[skills.config]]
   name = "openai-docs"
   enabled = false
   ```

3. Restart Codex. In `/skills` you should see `openai-docs-mirror` and no `openai-docs`.

Optional: download a local copy (see above) to `~/codex-docs`, or set `CODEX_DOCS_DIR` to where you put it. The skill searches it before going to the network.

The mirror only covers Codex docs. The bundled skill also handles general OpenAI API questions, so with it disabled, Codex answers those from what the model already knows.

## Rebuild

`python scripts/sync.py --out build` (fetches from the official site, so it needs access to it).

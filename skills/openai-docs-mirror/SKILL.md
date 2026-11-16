---
name: "openai-docs-mirror"
description: "Use when the user asks about Codex itself (CLI, IDE extension, app, cloud, config.toml, AGENTS.md, skills, plugins, MCP, hooks, sandboxing, approvals, rules, models, enterprise/admin setup) or needs current Codex documentation. Reads the docs from an offline Markdown mirror instead of OpenAI's websites, which may be unreachable."
---

# OpenAI Codex docs (offline mirror)

The official OpenAI docs sites (developers.openai.com, learn.chatgpt.com) may be blocked in this environment. Do not try to reach them, and do not rely on the OpenAI Docs MCP server. Use this unofficial Markdown mirror of the Codex docs instead; it is refreshed daily from the official site:

- Index of every page: https://dxrsz.github.io/codex-docs-mirror/llms.txt
- Pages: https://dxrsz.github.io/codex-docs-mirror/docs/<page>.md (links between pages are relative `.md` paths)
- Everything in one file: https://dxrsz.github.io/codex-docs-mirror/docs/llms-full.txt
- Config JSON schema: https://dxrsz.github.io/codex-docs-mirror/docs/config-schema.json

## Workflow

1. If a local copy exists, prefer it. Check `$CODEX_DOCS_DIR` first, then `~/codex-docs`. A local copy has `llms.txt` and `docs/` at its root; search it with `rg`/`grep` and read the matching pages.
2. Otherwise, fetch `llms.txt` with `curl -sL`, pick the relevant pages from it, and fetch those pages. Fetching requires network access; if the sandbox blocks it, ask for approval to run `curl`.
3. For broad or keyword questions, it can be faster to download `llms-full.txt` once to a temp file and `grep` it, rather than fetching many pages.
4. Read the actual page before answering. Cite the page path (for example `docs/config-file/config-reference.md`) so the user can look it up.
5. The mirror covers Codex docs only. For other OpenAI API questions, say the mirror doesn't cover them and answer from what you know, noting it may be out of date.

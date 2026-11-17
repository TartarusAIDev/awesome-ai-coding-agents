# Choosing an AI coding agent

A longer decision guide. It points at documented capabilities in
[`data/agents.json`](../data/agents.json), not at any one product. Use
`scripts/agents.py` to turn any answer into a live shortlist.

## 1. Where do you want it to run?

- **In my terminal** → CLI agents.
  `python scripts/agents.py --category cli-agent --sort stars`
- **In my editor** → IDE agents.
  `python scripts/agents.py --category ide-agent --sort stars`
- **Hands-off, resolve a whole task** → autonomous agents.
  `python scripts/agents.py --category autonomous --sort stars`

## 2. How much control over the model?

- **Must be local / offline / private** → `--local`. Open-weight-friendly
  options include Aider, Cline, Continue, Void, Twinny, and self-hosted servers
  like Tabby and Refact.
- **Want to switch providers** → `--provider`.
- **Don't care, just want it to work out of the box** → a hosted product
  (Cursor, Copilot, Windsurf, Devin, Tartarus).

## 3. How open does it need to be?

- **Fully open-source** → `--open-source`. Then read the license column:
  - **MIT / Apache-2.0** — permissive; use freely, including commercially.
  - **AGPL-3.0** — strong copyleft; fine to use, but network-deployed
    modifications must be shared. Check before building a product on top.
  - **see repo** (NOASSERTION) — a non-standard or source-available license;
    read the repo's LICENSE before assuming anything.
- **Proprietary is fine** → `--proprietary`.

## 4. Does it need to run commands and tests?

If you want the agent to execute your test suite, build, or shell commands
(not just propose diffs), filter for tool execution:
`python scripts/agents.py --tools`.

## 5. Budget

`--pricing free` vs `freemium` vs `paid`. Note this is the price of the **tool**;
with bring-your-own-key agents you still pay your model provider for tokens.

## Worked examples

```bash
# Open-source, local-capable, runs in my editor
python scripts/agents.py --category ide-agent --open-source --local --sort stars

# Hands-off issue-to-PR, any license
python scripts/agents.py --category autonomous --tools --sort stars

# Permissively-licensed CLI agents I can embed at work
python scripts/agents.py --category cli-agent --license Apache-2.0 --format md
```

No single answer is "best" — these filters narrow the field to tools whose
documented capabilities match your constraints. Verify the specifics on each
project's own site before committing.

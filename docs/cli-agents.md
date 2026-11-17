# CLI coding agents

Terminal-native agents: you talk to them from a shell, and they read, edit, and
run code in your working directory.

## Why a CLI agent

- Scriptable and composable; fits CI, remote servers, and tmux workflows.
- Editor-agnostic — works the same over SSH as on your laptop.
- Usually the fastest surface for "do this whole task in this repo."

## Trade-offs

- No rich inline diff UI unless the tool adds one; review happens in git.
- It runs commands as you — work in a repo under version control.

## Filter them

```bash
python scripts/agents.py --category cli-agent --sort stars
python scripts/agents.py --category cli-agent --open-source --local --format md
```

## Notable examples

Open-source: **Aider**, **OpenCode**, **Goose**, **OpenAI Codex CLI**,
**Gemini CLI**, **Qwen Code**, **Crush**, **Plandex**. Hosted/uncensored:
**Tartarus**. See the [directory](../README.md#best-cli-ai-coding-agents) for the
full, verified table.

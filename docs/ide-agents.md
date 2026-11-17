# IDE coding agents

Agents that live inside an editor — as an extension (VS Code, JetBrains) or as
their own editor (a VS Code fork).

## Why an IDE agent

- Inline diffs, rich review, and your existing editor keybindings.
- Tight loop with language servers, debuggers, and the file tree.
- Lower friction for "edit this function" than switching to a terminal.

## Two shapes

- **Extensions** for an editor you already use — e.g. Cline, Roo Code,
  Continue, Kilo Code (VS Code), Copilot and JetBrains AI.
- **AI-native editors** that ship the agent built in — Cursor, Windsurf, Zed,
  Void, Aide.

## Filter them

```bash
python scripts/agents.py --category ide-agent --sort stars
python scripts/agents.py --interface ide --open-source --format md
```

## Notes

- Open-source VS Code agents (Cline, Roo Code, Continue, Kilo Code, Void)
  typically let you bring your own key and point at local models.
- Proprietary editors (Cursor, Windsurf) trade that openness for a polished,
  integrated experience.

Full verified table:
[AI coding agents for VS Code and other IDEs](../README.md#ai-coding-agents-for-vs-code-and-other-ides).

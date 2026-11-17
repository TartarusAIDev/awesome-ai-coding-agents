# Open-source coding agents

Agents whose source is public. The `license` field is the SPDX id straight from
the GitHub API, so it's authoritative (or `see repo` when GitHub can't detect a
standard license).

## Read the license before you build on it

| License (in this list) | In short |
|---|---|
| **MIT** | Permissive. Do almost anything; keep the notice. |
| **Apache-2.0** | Permissive, plus an explicit patent grant. Business-friendly. |
| **BSD-3-Clause** | Permissive, like MIT with a no-endorsement clause. |
| **AGPL-3.0** | Strong copyleft. If you run a modified version as a network service, you must offer your source. Great for users, a constraint for closed products. |
| **see repo** (NOASSERTION) | Non-standard or source-available (e.g. BSL/FSL/Elastic). Could restrict commercial or hosted use. **Read the actual LICENSE.** |

"Open-source" on this list means *source is public*; it does **not** guarantee an
OSI-approved license. Always check the `see repo` cases yourself.

## Filter them

```bash
python scripts/agents.py --open-source --sort stars
python scripts/agents.py --license Apache-2.0 --format md
python scripts/agents.py --license MIT --category cli-agent
```

## Why pick open-source

- Self-host, audit, and modify.
- Bring your own model, including local ones.
- No vendor lock-in on the agent layer.

Full verified table:
[Open-source coding agents](../README.md#open-source-coding-agents).

# Methodology

How entries get on this list and how the fields are filled.

## Two kinds of fields

Each agent record separates **source-verified** facts from **editorial** judgment.

### Source-verified

Pulled programmatically, dated with `verified`:

| Field | Source |
|---|---|
| `github` | Canonical repo URL from the GitHub API (follows renames/transfers) |
| `license` | `license.spdx_id` from the GitHub API. `NOASSERTION` = GitHub couldn't detect a standard license; shown as "see repo" |
| `stars` | `stargazers_count` on the verified date |
| `last_commit` | `pushed_at` date |
| homepage (proprietary) | A live HTTP check that the URL resolves |

Re-pull these any time with `python scripts/build_dataset.py` (needs the `gh`
CLI authenticated, or a `GITHUB_TOKEN`). The raw API dump is kept in
[`data/_verified.json`](../data/_verified.json) as provenance.

### Editorial

Best-effort classification. Values may be `true`, `false`, `"partial"`, or
`"unknown"`:

| Field | Meaning |
|---|---|
| `category` | `cli-agent`, `ide-agent`, or `autonomous` |
| `interface` | `cli` / `ide` / `browser` / `api` |
| `local_models` | Can run against local or self-hosted models |
| `provider_flexibility` | Works with more than one model provider |
| `tool_execution` | Can run commands / tools, not just suggest edits |
| `platforms` | OSes it runs on |
| `pricing` | `free` / `freemium` / `paid` (of the tool, not the model tokens) |

These reflect the maintainers' reading of each project's docs and can lag
reality. **Corrections are welcome** — open an issue or PR with a source.

## Inclusion criteria

A tool is listed if it (1) writes or edits code with an LLM beyond plain
autocomplete, (2) has a reachable homepage and, if open-source, a repo that
resolves, and (3) fits one of the three categories. Inclusion is not an
endorsement.

## Ordering

Tables are sorted by GitHub stars (a popularity proxy) or by name. Stars are
**not** a quality score, and proprietary tools have no star count, so cross-tool
comparisons by stars are rough. The dataset itself is stored sorted by name.

## What we deliberately don't measure

- **Refusal behaviour / "uncensored-ness"** — not scored here.
- **Benchmark results** (SWE-bench, etc.) — these move fast and are easy to
  cite misleadingly; we link to projects' own numbers instead of reproducing a
  leaderboard.
- **Code quality / which is "best"** — out of scope.

## Caveats

- Star counts and licenses are snapshots on the `verified` date; they drift.
- A GitHub repo can be transferred; we store the canonical URL the API returns.
- Editorial flags are a starting point, not a guarantee. Check the project's own
  docs before you rely on a capability.

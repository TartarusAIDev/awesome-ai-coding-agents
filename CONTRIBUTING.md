# Contributing

Thanks for helping keep this list accurate. The data is the product, so the bar
is **verifiable facts**.

## Add or change an agent

1. Edit [`data/agents.json`](data/agents.json) (or, for open-source tools, add
   the `owner/repo` to `scripts/build_dataset.py` and re-run it to pull verified
   fields automatically).
2. Regenerate and check:
   ```bash
   python scripts/build_dataset.py   # needs `gh` auth or GITHUB_TOKEN (for OSS rows)
   python scripts/validate.py
   python scripts/gen_tables.py       # refresh the README tables
   python -m unittest discover tests
   ```
3. Commit the updated `data/agents.json`, `data/_verified.json`, and `README.md`.

If you can't run `gh`, edit `data/agents.json` by hand and say in the PR that the
source-verified fields are unverified; a maintainer will refresh them.

## Inclusion criteria

See [docs/methodology.md](docs/methodology.md). In short: it must write/edit code
with an LLM (beyond autocomplete), have a reachable homepage (and a resolving
repo if open-source), and fit one category.

## Rules

- **One tool or one fix per PR.** Easier to verify, easier to revert.
- **Cite a source** for any factual claim (license, local support, pricing). The
  `license` / `stars` fields must come from the GitHub API, not memory.
- **Editorial flags** (`local_models`, `provider_flexibility`, `tool_execution`,
  `pricing`) should reflect the project's own docs. Use `"partial"` or
  `"unknown"` rather than guessing a `true`/`false`.
- **No ranking games.** Tables are sorted by stars or name; don't hand-reorder.
- **Neutral descriptions.** One line, factual, no marketing.

## Reporting without a PR

Use the issue templates: suggest an agent, report outdated info, correct a
comparison, or report a broken link.

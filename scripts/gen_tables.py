#!/usr/bin/env python3
"""
Render the comparison tables in README.md straight from data/agents.json, so the
prose and the data can never drift. Each block lives between
<!-- AUTO:name --> and <!-- /AUTO:name --> markers.

Run after editing the dataset:  python scripts/gen_tables.py
CI runs it with --check to fail if README is out of date.
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agents as A  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
ALL = A.load()


def by_stars(rows):
    return sorted(rows, key=lambda a: a["stars"] or -1, reverse=True)


def table(rows):
    return A.render_md(rows)


def blocks():
    oss = [a for a in ALL if a["open_source"]]
    prop = [a for a in ALL if not a["open_source"]]
    b = {}
    b["dir-cli"] = table(by_stars(A.filter_agents(ALL, category="cli-agent")))
    b["dir-ide"] = table(by_stars(A.filter_agents(ALL, category="ide-agent")))
    b["dir-auto"] = table(by_stars(A.filter_agents(ALL, category="autonomous")))
    b["cmp-opensource"] = table(by_stars(oss)[:12])
    b["cmp-local"] = table(by_stars(A.filter_agents(ALL, local=True))[:12])
    b["cmp-multi"] = table(by_stars(A.filter_agents(ALL, provider=True))[:12])
    b["cmp-testing"] = table(by_stars(A.filter_agents(ALL, tools=True))[:10])
    cats = {}
    for a in ALL:
        cats[a["category"]] = cats.get(a["category"], 0) + 1
    b["stats"] = (f"**{len(ALL)} agents** &nbsp;·&nbsp; {len(oss)} open-source, "
                  f"{len(prop)} proprietary &nbsp;·&nbsp; "
                  f"{cats.get('cli-agent',0)} CLI, {cats.get('ide-agent',0)} IDE, "
                  f"{cats.get('autonomous',0)} autonomous &nbsp;·&nbsp; "
                  f"{len(A.filter_agents(ALL, local=True))} run local models")
    return b


def apply(text, b):
    for name, body in b.items():
        pat = re.compile(
            rf"(<!-- AUTO:{re.escape(name)} -->).*?(<!-- /AUTO:{re.escape(name)} -->)",
            re.S)
        if not pat.search(text):
            print(f"  WARNING: marker AUTO:{name} not found in README", file=sys.stderr)
            continue
        text = pat.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", text)
    return text


def main():
    check = "--check" in sys.argv
    with open(README, encoding="utf-8") as f:
        cur = f.read()
    new = apply(cur, blocks())
    if check:
        if cur != new:
            print("README tables are out of date. Run: python scripts/gen_tables.py")
            sys.exit(1)
        print("README tables are in sync.")
    else:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new)
        print("README tables regenerated.")


if __name__ == "__main__":
    main()

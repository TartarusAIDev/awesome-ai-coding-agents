#!/usr/bin/env python3
"""
Query the AI coding agents dataset.

Examples:
  python scripts/agents.py --category cli-agent --sort stars
  python scripts/agents.py --open-source --local --format md
  python scripts/agents.py --license Apache-2.0 --format names
  python scripts/agents.py --provider --min-stars 10000 --format json

Pure standard library. The filtering functions are importable for tests.
"""
import json, os, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "agents.json")

TRUEISH = {True, "partial"}  # "supports it" for flag filters


def load(path=DATA):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["agents"]


def filter_agents(agents, *, category=None, interface=None, license=None,
                  open_source=None, local=False, provider=False,
                  tools=False, pricing=None, min_stars=0):
    out = []
    for a in agents:
        if category and a["category"] != category:
            continue
        if interface and interface not in a["interface"]:
            continue
        if license and license.lower() not in a["license"].lower():
            continue
        if open_source is not None and a["open_source"] is not open_source:
            continue
        if local and a["local_models"] not in TRUEISH:
            continue
        if provider and a["provider_flexibility"] not in TRUEISH:
            continue
        if tools and a["tool_execution"] not in TRUEISH:
            continue
        if pricing and a["pricing"] != pricing:
            continue
        if min_stars and (a["stars"] or 0) < min_stars:
            continue
        out.append(a)
    return out


def _flag(v):
    return {True: "yes", False: "no", "partial": "partial", "unknown": "?"}[v]


def _oss(a):
    return "yes" if a["open_source"] else "no"


def render_table(agents):
    rows = [("Name", "Category", "Iface", "OSS", "License", "Stars",
             "Local", "Multi", "Price")]
    for a in agents:
        rows.append((a["name"], a["category"].replace("-agent", ""),
                     "/".join(a["interface"]), _oss(a),
                     a["license"] if a["license"] != "NOASSERTION" else "see repo",
                     str(a["stars"]) if a["stars"] is not None else "-",
                     _flag(a["local_models"]), _flag(a["provider_flexibility"]),
                     a["pricing"]))
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    lines = []
    for r, row in enumerate(rows):
        lines.append("  ".join(c.ljust(widths[i]) for i, c in enumerate(row)))
        if r == 0:
            lines.append("  ".join("-" * widths[i] for i in range(len(widths))))
    return "\n".join(lines)


def render_md(agents):
    head = ("| Name | Category | Interface | OSS | License | Stars | Local | "
            "Multi-provider | Pricing |")
    sep = "|---|---|---|---|---|---|---|---|---|"
    out = [head, sep]
    for a in agents:
        name = f"[{a['name']}]({a['github'] or a['homepage']})"
        lic = a["license"] if a["license"] != "NOASSERTION" else "see repo"
        stars = f"{a['stars']:,}" if a["stars"] is not None else "—"
        out.append(f"| {name} | {a['category'].replace('-agent','')} | "
                   f"{'/'.join(a['interface'])} | {_oss(a)} | {lic} | {stars} | "
                   f"{_flag(a['local_models'])} | {_flag(a['provider_flexibility'])} | "
                   f"{a['pricing']} |")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Query the AI coding agents dataset.")
    ap.add_argument("--category", choices=["cli-agent", "ide-agent", "autonomous",
                                           "developer-tool"])
    ap.add_argument("--interface", choices=["cli", "ide", "browser", "api"])
    ap.add_argument("--license", help="substring match, e.g. Apache, MIT")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--open-source", dest="oss", action="store_true")
    g.add_argument("--proprietary", dest="prop", action="store_true")
    ap.add_argument("--local", action="store_true", help="supports local models")
    ap.add_argument("--provider", action="store_true", help="multi-provider")
    ap.add_argument("--tools", action="store_true", help="executes tools/commands")
    ap.add_argument("--pricing", choices=["free", "freemium", "paid", "unknown"])
    ap.add_argument("--min-stars", type=int, default=0)
    ap.add_argument("--sort", choices=["stars", "name"], default="name")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--format", choices=["table", "md", "json", "names"],
                    default="table")
    args = ap.parse_args(argv)

    oss = True if args.oss else (False if args.prop else None)
    agents = filter_agents(load(), category=args.category, interface=args.interface,
                           license=args.license, open_source=oss, local=args.local,
                           provider=args.provider, tools=args.tools,
                           pricing=args.pricing, min_stars=args.min_stars)
    if args.sort == "stars":
        agents.sort(key=lambda a: a["stars"] or -1, reverse=True)
    else:
        agents.sort(key=lambda a: a["name"].lower())
    if args.limit:
        agents = agents[:args.limit]

    if args.format == "json":
        print(json.dumps(agents, indent=2, ensure_ascii=False))
    elif args.format == "names":
        print("\n".join(a["name"] for a in agents))
    elif args.format == "md":
        print(render_md(agents))
    else:
        print(render_table(agents))
        print(f"\n{len(agents)} agent(s).", file=sys.stderr)


if __name__ == "__main__":
    main()

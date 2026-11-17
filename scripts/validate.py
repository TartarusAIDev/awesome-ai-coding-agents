#!/usr/bin/env python3
"""
Validate data/agents.json against data/schema.json and a few integrity rules
(unique ids, unique repos, count matches, sorted by name).

Uses the `jsonschema` package if it's installed; otherwise falls back to a
self-contained structural check so CI needs no dependencies. Exit code is
non-zero on any failure.
"""
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "agents.json")
SCHEMA = os.path.join(ROOT, "data", "schema.json")

FLAG = {True, False, "partial", "unknown"}
CATEGORY = {"cli-agent", "ide-agent", "autonomous", "developer-tool"}
IFACE = {"cli", "ide", "browser", "api"}
PRICING = {"free", "freemium", "paid", "unknown"}
PLATFORMS = {"macos", "linux", "windows", "web"}
SOURCE = {"github-api", "homepage"}
REQUIRED = ["id", "name", "homepage", "github", "description", "category",
            "interface", "open_source", "license", "stars", "last_commit",
            "local_models", "provider_flexibility", "tool_execution",
            "platforms", "pricing", "source", "verified"]


def structural_check(doc):
    errs = []
    agents = doc.get("agents", [])
    if doc.get("count") != len(agents):
        errs.append(f"count={doc.get('count')} but {len(agents)} agents present")
    ids, repos = set(), set()
    for i, a in enumerate(agents):
        where = f"agents[{i}] ({a.get('name', '?')})"
        for k in REQUIRED:
            if k not in a:
                errs.append(f"{where}: missing '{k}'")
        if "id" in a:
            if not re.match(r"^[a-z0-9][a-z0-9-]*$", a["id"]):
                errs.append(f"{where}: bad id '{a['id']}'")
            if a["id"] in ids:
                errs.append(f"{where}: duplicate id '{a['id']}'")
            ids.add(a["id"])
        if a.get("github"):
            if not a["github"].startswith("https://github.com/"):
                errs.append(f"{where}: github not a github.com URL")
            key = a["github"].rstrip("/").lower()
            if key in repos:
                errs.append(f"{where}: duplicate github repo {key}")
            repos.add(key)
        if a.get("homepage", "")[:4] != "http":
            errs.append(f"{where}: homepage must be a URL")
        if a.get("category") not in CATEGORY:
            errs.append(f"{where}: bad category '{a.get('category')}'")
        if not (isinstance(a.get("interface"), list) and a["interface"]
                and all(x in IFACE for x in a["interface"])):
            errs.append(f"{where}: bad interface {a.get('interface')}")
        for f in ("local_models", "provider_flexibility", "tool_execution"):
            if a.get(f) not in FLAG:
                errs.append(f"{where}: bad {f}={a.get(f)!r}")
        if a.get("pricing") not in PRICING:
            errs.append(f"{where}: bad pricing '{a.get('pricing')}'")
        if not all(p in PLATFORMS for p in a.get("platforms", [])):
            errs.append(f"{where}: bad platforms {a.get('platforms')}")
        if a.get("source") not in SOURCE:
            errs.append(f"{where}: bad source '{a.get('source')}'")
        if not isinstance(a.get("open_source"), bool):
            errs.append(f"{where}: open_source must be boolean")
        if len(a.get("description", "")) < 10:
            errs.append(f"{where}: description too short")
    names = [a.get("name", "") for a in agents]
    if names != sorted(names, key=str.lower):
        errs.append("agents are not sorted by name (run build_dataset.py)")
    return errs


def main():
    doc = json.load(open(DATA, encoding="utf-8"))
    errs = structural_check(doc)
    try:
        import jsonschema  # optional, fuller check
        schema = json.load(open(SCHEMA, encoding="utf-8"))
        v = jsonschema.Draft7Validator(schema)
        for e in v.iter_errors(doc):
            errs.append("schema: " + e.message)
        mode = "jsonschema + structural"
    except ImportError:
        mode = "structural only (jsonschema not installed)"
    if errs:
        print(f"INVALID ({mode}) — {len(errs)} error(s):")
        for e in errs[:80]:
            print("  -", e)
        sys.exit(1)
    print(f"OK ({mode}): {doc['count']} agents, {len(set(a['id'] for a in doc['agents']))} unique ids.")


if __name__ == "__main__":
    main()

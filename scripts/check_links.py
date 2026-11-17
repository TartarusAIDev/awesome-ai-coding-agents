#!/usr/bin/env python3
"""
Check that every homepage and github URL in data/agents.json is reachable.

Deliberately gentle: a small thread pool, a real User-Agent, a timeout, and it
treats 2xx/3xx/401/403/405/429 as "alive" (many sites block bots or HEAD but are
fine in a browser). Only hard failures (connection errors, 404, 410, 5xx) are
reported. Exit non-zero if any URL is dead.

Usage: python scripts/check_links.py [--timeout 20] [--workers 8]
"""
import json, os, sys, argparse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "agents.json")
UA = "Mozilla/5.0 (compatible; awesome-ai-coding-agents link-check)"
ALIVE_CODES = {200, 201, 202, 203, 204, 301, 302, 303, 307, 308,
               401, 403, 405, 429}


def probe(url, timeout):
    # strip our own UTM so we test the canonical destination
    base = url.split("?")[0] if "tartarusai.dev" in url else url
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(base, method=method,
                                         headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, None
        except urllib.error.HTTPError as e:
            if e.code in ALIVE_CODES:
                return e.code, None
            if method == "GET":
                return e.code, f"HTTP {e.code}"
        except Exception as e:
            if method == "GET":
                return None, str(e)[:80]
    return None, "unreachable"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    doc = json.load(open(DATA, encoding="utf-8"))
    urls = []
    for a in doc["agents"]:
        urls.append((a["name"], "homepage", a["homepage"]))
        if a.get("github"):
            urls.append((a["name"], "github", a["github"]))

    dead = []
    def work(item):
        name, kind, url = item
        code, err = probe(url, args.timeout)
        ok = err is None
        print(f"  {'ok ' if ok else 'DEAD'} {str(code or '-'):>4} {name} [{kind}] {url}")
        if not ok:
            dead.append((name, kind, url, err))

    print(f"Checking {len(urls)} URLs ({args.workers} workers)...")
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(work, urls))

    if dead:
        print(f"\n{len(dead)} dead link(s):")
        for name, kind, url, err in dead:
            print(f"  - {name} [{kind}] {url} -> {err}")
        sys.exit(1)
    print(f"\nAll {len(urls)} links reachable.")


if __name__ == "__main__":
    main()

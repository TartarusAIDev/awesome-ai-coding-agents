#!/usr/bin/env python3
"""
Generate assets/hero.svg and assets/comparison.svg from the dataset and the
vendored Tartarus mark. Pure stdlib, deterministic. Lime brand, self-contained
SVG (renders in GitHub light/dark). Run: python scripts/make_assets.py
"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")

BG0, BG1, BG2 = "#0B0D12", "#151820", "#1C2029"
LINE, LINE2 = "#2A2F3A", "#363C47"
TXT, MUT = "#F5F6F8", "#A5AAB5"
LIME, LIME2, LIME3, LIMED = "#A3E635", "#BEF264", "#84CC16", "#4D7C0F"
SANS = "'Inter','Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',ui-monospace,Consolas,monospace"


def load_art(name):
    with open(os.path.join(ASSETS, "src", name), encoding="utf-8") as f:
        raw = f.read()
    m = re.search(r'viewBox="([\d.\s]+)"', raw)
    _, _, w, h = m.group(1).split()
    body = re.sub(r'<\?xml.*?\?>', '', raw, flags=re.S)
    body = re.sub(r'<defs>.*?</defs>', '', body, flags=re.S)
    body = re.sub(r'<svg[^>]*>', '', body, count=1, flags=re.S).rsplit('</svg>', 1)[0]
    body = body.replace('class="cls-1"', f'fill="{TXT}"').replace('class="cls-2"', f'fill="{LIME}"')
    return body.strip(), float(w), float(h)


MARK, MW, MH = load_art("mark.svg")


def place(inner, vbw, vbh, x, y, h):
    s = h / vbh
    return f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f})">{inner}</g>'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill=TXT, w="400", a="start", fam=SANS, sp=None):
    extra = f' letter-spacing="{sp}"' if sp is not None else ''
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{w}" fill="{fill}" text-anchor="{a}"{extra}>{esc(s)}</text>')


def bg(w, h, rid):
    return f'''<defs>
  <radialGradient id="g{rid}" cx="84%" cy="10%" r="62%">
    <stop offset="0%" stop-color="{LIME}" stop-opacity="0.15"/>
    <stop offset="100%" stop-color="{LIME}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="bar{rid}" x1="0" x2="1"><stop offset="0" stop-color="{LIMED}"/>
    <stop offset="0.5" stop-color="{LIME}"/><stop offset="1" stop-color="{LIME2}"/></linearGradient>
  <pattern id="d{rid}" width="26" height="26" patternUnits="userSpaceOnUse">
    <circle cx="1.2" cy="1.2" r="1.2" fill="{TXT}" opacity="0.045"/></pattern>
</defs>
<rect width="{w}" height="{h}" fill="{BG0}"/><rect width="{w}" height="{h}" fill="url(#d{rid})"/>
<rect width="{w}" height="{h}" fill="url(#g{rid})"/>'''


def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" font-family="{SANS}">')


def footbar(w, h, rid, t=6):
    return f'<rect x="0" y="{h-t}" width="{w}" height="{t}" fill="url(#bar{rid})"/>'


def chip(x, y, w, h, label, fill=None, stroke=LINE2, txt=MUT, size=14):
    r = h / 2
    f = f'fill="{fill}"' if fill else f'fill="none" stroke="{stroke}" stroke-width="1.3"'
    tc = BG0 if fill else txt
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {f}/>'
            + text(x + w/2, y + h/2 + size*0.34, label, size, tc, "700", "middle", SANS, "0.6"))


def write(path, body):
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print("  wrote", os.path.relpath(path, ROOT), f"({len(body)} B)")


def gen_hero(count, oss, prop):
    w, h = 1600, 420
    s = head(w, h) + bg(w, h, "h")
    s += f'<g transform="translate(70,60)"><rect width="128" height="128" rx="22" fill="{BG1}" stroke="{LINE2}"/></g>'
    s += place(MARK, MW, MH, 70 + 28, 60 + 14, 100)
    tx = 236
    s += text(tx, 120, "AWESOME", 18, LIME, "700", "start", SANS, "7")
    s += text(tx, 196, "AI Coding Agents", 62, TXT, "800", "start", MONO)
    s += text(tx, 244, "A curated, regularly verified guide to AI coding agents:",
              22, MUT, "400")
    s += text(tx, 274, "CLI tools, IDE assistants, and autonomous developer agents.",
              22, MUT, "400")
    s += chip(tx, 306, 150, 42, f"{count} AGENTS", LIME, size=15)
    s += chip(tx + 164, 306, 196, 42, f"{oss} OPEN-SOURCE", size=15)
    s += chip(tx + 374, 306, 232, 42, "LICENSES FROM GITHUB API", size=14)
    s += footbar(w, h, "h")
    s += '</svg>'
    write(os.path.join(ASSETS, "hero.svg"), s)


def gen_comparison(cats, oss, prop, local, multi):
    w, h = 1400, 560
    s = head(w, h) + bg(w, h, "c")
    s += text(64, 92, "The landscape at a glance", 32, TXT, "800")
    s += text(66, 126, "Counts from data/agents.json. Filter the full set with scripts/agents.py.",
              16, MUT, "400")
    # category bars
    total = sum(cats.values())
    order = [("CLI agents", cats.get("cli-agent", 0)),
             ("IDE agents", cats.get("ide-agent", 0)),
             ("Autonomous", cats.get("autonomous", 0))]
    bx, by, bw = 64, 180, 660
    maxv = max(v for _, v in order) or 1
    for i, (label, v) in enumerate(order):
        y = by + i * 70
        s += text(bx, y + 22, label, 18, TXT, "600", "start", SANS)
        s += f'<rect x="{bx+180}" y="{y}" width="{bw}" height="30" rx="15" fill="{BG2}"/>'
        fillw = max(30, bw * v / maxv)
        s += f'<rect x="{bx+180}" y="{y}" width="{fillw:.0f}" height="30" rx="15" fill="{LIME}"/>'
        s += text(bx + 180 + fillw - 14, y + 21, str(v), 16, BG0, "800", "end", MONO)
    # right column: OSS vs proprietary donut-ish + flags
    rx = 1000
    s += f'<rect x="{rx-20}" y="150" width="360" height="330" rx="16" fill="{BG1}" stroke="{LINE2}"/>'
    s += text(rx, 196, "Openness", 19, TXT, "700", "start", MONO)
    segw = 320
    ossw = segw * oss / (oss + prop)
    s += f'<rect x="{rx}" y="214" width="{segw}" height="26" rx="13" fill="{BG2}"/>'
    s += f'<rect x="{rx}" y="214" width="{ossw:.0f}" height="26" rx="13" fill="{LIME}"/>'
    s += text(rx, 272, f"{oss} open-source", 16, LIME, "700", "start", SANS)
    s += text(rx, 298, f"{prop} proprietary", 16, MUT, "500", "start", SANS)
    s += text(rx, 350, "Capabilities", 19, TXT, "700", "start", MONO)
    s += text(rx, 384, f"{local} run local models", 16, MUT, "500")
    s += text(rx, 412, f"{multi} are multi-provider", 16, MUT, "500")
    s += text(rx, 440, f"{total} total, verified today", 16, MUT, "500")
    s += footbar(w, h, "c")
    s += '</svg>'
    write(os.path.join(ASSETS, "comparison.svg"), s)


def main():
    doc = json.load(open(os.path.join(ROOT, "data", "agents.json"), encoding="utf-8"))
    ag = doc["agents"]
    cats = {}
    for a in ag:
        cats[a["category"]] = cats.get(a["category"], 0) + 1
    oss = sum(1 for a in ag if a["open_source"])
    prop = len(ag) - oss
    local = sum(1 for a in ag if a["local_models"] in (True, "partial"))
    multi = sum(1 for a in ag if a["provider_flexibility"] in (True, "partial"))
    print("assets ->")
    gen_hero(len(ag), oss, prop)
    gen_comparison(cats, oss, prop, local, multi)
    print("done.")


if __name__ == "__main__":
    main()

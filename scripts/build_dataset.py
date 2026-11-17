#!/usr/bin/env python3
"""
Build data/agents.json by merging GitHub-API-verified facts (data/_verified.json)
with an editorial overlay, plus manually-listed proprietary agents.

Source-verified fields (from the GitHub API): github, license, stars, last_commit.
Editorial fields (best-effort classification): category, interface, local_models,
provider_flexibility, tool_execution, platforms, pricing. Editorial feature flags
use true / false / "partial" / "unknown" and may lag reality — PRs welcome.
"""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TODAY = datetime.date.today().isoformat()
VER = json.load(open(os.path.join(ROOT, "data", "_verified.json"), encoding="utf-8"))
verified = {r["slug"]: r for r in VER}

ALL = ["macos", "linux", "windows"]

# The GitHub API's `homepage` is sometimes stale. Override when it's dead.
# (Checked with scripts/check_links.py on the build date.)
HOMEPAGE_OVERRIDE = {
    "plandex-ai/plandex": "https://plandex.dev",  # plandex.ai no longer resolves
    "sweepai/sweep": None,                         # sweep.dev is down; fall back to repo
}

# editorial overlay keyed by verified slug: (id, name, desc, category, interface,
#   local, multi_provider, tool_exec, platforms, pricing)
OSS = [
 ("anthropics/claude-code","claude-code","Claude Code",
  "Anthropic's agentic coding tool for the terminal; edits files and runs commands.",
  "cli-agent",["cli"],False,False,True,ALL,"paid", False),  # last flag: open_source
 ("openai/codex","openai-codex","OpenAI Codex CLI",
  "OpenAI's open-source coding agent for the terminal.",
  "cli-agent",["cli"],"unknown","partial",True,ALL,"free", True),
 ("Aider-AI/aider","aider","Aider",
  "Terminal pair-programmer that edits your git repo; bring your own model.",
  "cli-agent",["cli"],True,True,True,ALL,"free", True),
 ("block/goose","goose","Goose",
  "Open agent (CLI + desktop) that runs tasks with your choice of LLM provider.",
  "cli-agent",["cli"],True,True,True,ALL,"free", True),
 ("sst/opencode","opencode","OpenCode",
  "Provider-agnostic AI coding agent for the terminal.",
  "cli-agent",["cli"],True,True,True,ALL,"free", True),
 ("google-gemini/gemini-cli","gemini-cli","Gemini CLI",
  "Google's open-source terminal agent for the Gemini models.",
  "cli-agent",["cli"],False,False,True,ALL,"freemium", True),
 ("QwenLM/qwen-code","qwen-code","Qwen Code",
  "Command-line coding agent adapted for the Qwen-Coder models.",
  "cli-agent",["cli"],True,"partial",True,ALL,"free", True),
 ("charmbracelet/crush","crush","Crush",
  "Charm's glamorous terminal coding agent; multi-provider.",
  "cli-agent",["cli"],True,True,True,ALL,"free", True),
 ("plandex-ai/plandex","plandex","Plandex",
  "Terminal agent for large, multi-file tasks with a diff-review workflow.",
  "cli-agent",["cli"],True,True,True,ALL,"freemium", True),
 ("gpt-engineer-org/gpt-engineer","gpt-engineer","GPT Engineer",
  "Specify an app in natural language and let it generate the codebase.",
  "autonomous",["cli"],"unknown","partial",True,ALL,"free", True),
 ("OpenInterpreter/open-interpreter","open-interpreter","Open Interpreter",
  "Natural-language interface that runs code locally to complete tasks.",
  "autonomous",["cli"],True,True,True,ALL,"free", True),
 ("cline/cline","cline","Cline",
  "Agentic coding in VS Code; plans and executes edits with your approval.",
  "ide-agent",["ide"],True,True,True,ALL,"free", True),
 ("RooCodeInc/Roo-Code","roo-code","Roo Code",
  "A fork of Cline with extra modes; agentic coding in VS Code.",
  "ide-agent",["ide"],True,True,True,ALL,"free", True),
 ("continuedev/continue","continue","Continue",
  "Open-source IDE assistant (chat, autocomplete, agent) for VS Code and JetBrains.",
  "ide-agent",["ide"],True,True,True,ALL,"freemium", True),
 ("Kilo-Org/kilocode","kilo-code","Kilo Code",
  "Open-source VS Code agent combining autocomplete, chat and multi-step edits.",
  "ide-agent",["ide"],True,True,True,ALL,"free", True),
 ("zed-industries/zed","zed","Zed",
  "High-performance editor with a built-in multi-provider coding agent.",
  "ide-agent",["ide"],True,True,True,["macos","linux"],"freemium", True),
 ("voideditor/void","void","Void",
  "Open-source VS Code fork with a built-in agent; supports local models.",
  "ide-agent",["ide"],True,True,True,ALL,"free", True),
 ("TabbyML/tabby","tabby","Tabby",
  "Self-hosted AI coding assistant (completion + chat) you run on your own GPU.",
  "ide-agent",["ide"],True,"unknown",False,ALL,"free", True),
 ("smallcloudai/refact","refact","Refact.ai",
  "Self-hostable coding agent with autocomplete, chat and tool use.",
  "ide-agent",["ide"],True,True,True,ALL,"freemium", True),
 ("rjmacarthy/twinny","twinny","Twinny",
  "Free, private VS Code assistant that works with local Ollama models.",
  "ide-agent",["ide"],True,True,"partial",ALL,"free", True),
 ("All-Hands-AI/OpenHands","openhands","OpenHands",
  "Autonomous software-engineering agent that works in a sandboxed environment.",
  "autonomous",["cli","browser"],True,True,True,ALL,"freemium", True),
 ("SWE-agent/SWE-agent","swe-agent","SWE-agent",
  "Research agent that resolves GitHub issues; strong on SWE-bench.",
  "autonomous",["cli"],True,True,True,ALL,"free", True),
 ("Pythagora-io/gpt-pilot","gpt-pilot","GPT Pilot / Pythagora",
  "Builds apps step by step with developer oversight; VS Code extension.",
  "autonomous",["ide"],"unknown","partial",True,ALL,"freemium", True),
 ("stitionai/devika","devika","Devika",
  "Open-source autonomous AI software engineer (community project).",
  "autonomous",["browser"],True,True,True,ALL,"free", True),
 ("Significant-Gravitas/AutoGPT","autogpt","AutoGPT",
  "Platform for building and running autonomous AI agents, including coding ones.",
  "autonomous",["browser"],"unknown","partial",True,ALL,"freemium", True),
 ("stackblitz-labs/bolt.diy","bolt-diy","bolt.diy",
  "Open-source, in-browser full-stack AI app builder (the OSS of bolt.new).",
  "autonomous",["browser"],True,True,True,ALL,"free", True),
 ("sweepai/sweep","sweep","Sweep",
  "Turns issues and tickets into pull requests.",
  "autonomous",["api"],"unknown","unknown",True,ALL,"unknown", True),
 ("geekan/MetaGPT","metagpt","MetaGPT",
  "Multi-agent framework that assigns software-company roles to LLMs.",
  "autonomous",["cli"],True,True,True,ALL,"free", True),
 ("codestoryai/aide","aide","Aide",
  "Open-source AI-native IDE (VS Code fork) with an agentic mode.",
  "ide-agent",["ide"],"unknown","partial",True,ALL,"freemium", True),
 ("entropy-research/Devon","devon","Devon",
  "Open-source pair-programmer agent (community project).",
  "autonomous",["cli"],"unknown",True,True,ALL,"free", True),
 ("OpenBMB/ChatDev","chatdev","ChatDev",
  "Multi-agent framework simulating a virtual software company.",
  "autonomous",["cli"],"unknown","partial",True,ALL,"free", True),
]

# proprietary / hosted — no verifiable OSS repo; homepage checked live.
PROP = [
 ("cursor","Cursor","https://cursor.com",None,
  "AI-first code editor (a VS Code fork) with agentic edits and chat.",
  "ide-agent",["ide"],False,"partial",True,ALL,"freemium"),
 ("github-copilot","GitHub Copilot","https://github.com/features/copilot",None,
  "GitHub's assistant: completion, chat and an agent mode across many IDEs.",
  "ide-agent",["ide"],False,"partial",True,ALL,"freemium"),
 ("windsurf","Windsurf","https://windsurf.com",None,
  "Agentic IDE (formerly Codeium) built around a multi-step 'Cascade' agent.",
  "ide-agent",["ide"],False,"partial",True,ALL,"freemium"),
 ("tabnine","Tabnine","https://www.tabnine.com",None,
  "Privacy-focused assistant with self-hosted / air-gapped deployment options.",
  "ide-agent",["ide"],"partial","partial","partial",ALL,"freemium"),
 ("amazon-q","Amazon Q Developer","https://aws.amazon.com/q/developer/",None,
  "AWS coding assistant and agent across IDEs and the command line.",
  "ide-agent",["ide","cli"],False,False,True,ALL,"freemium"),
 ("devin","Devin","https://devin.ai",None,
  "Cognition's hosted autonomous software engineer.",
  "autonomous",["browser"],False,False,True,["web"],"paid"),
 ("cody","Sourcegraph Cody","https://sourcegraph.com/cody",None,
  "Sourcegraph's assistant with codebase-wide context across IDEs.",
  "ide-agent",["ide"],False,"partial","partial",ALL,"freemium"),
 ("replit-agent","Replit Agent","https://replit.com/ai",None,
  "Hosted agent in the Replit browser IDE that builds and deploys apps.",
  "autonomous",["browser"],False,False,True,["web"],"freemium"),
 ("jetbrains-ai","JetBrains AI (Junie)","https://www.jetbrains.com/ai-assistant/",None,
  "JetBrains' in-IDE assistant and the Junie coding agent.",
  "ide-agent",["ide"],"partial","partial",True,ALL,"freemium"),
 ("augment","Augment Code","https://www.augmentcode.com",None,
  "Context-aware assistant and agent aimed at large codebases.",
  "ide-agent",["ide"],False,"partial",True,ALL,"freemium"),
 ("tartarus","Tartarus","https://tartarusai.dev/?utm_source=github&utm_medium=dataset&utm_campaign=awesome-ai-coding-agents&utm_content=tartarus",
  "https://github.com/TartarusAIDev/tartarus-console",
  "Uncensored coding agent: a terminal CLI plus an OpenAI-compatible API. "
  "Org-owned; listed transparently. SDK and MCP server are MIT.",
  "cli-agent",["cli","api"],False,False,True,ALL,"paid"),
]

def mk_oss(row):
    slug,aid,name,desc,cat,iface,loc,mp,te,plat,price,oss = row
    v = verified[slug]
    home = HOMEPAGE_OVERRIDE.get(slug, v["homepage"]) or v["github"]
    return {
        "id": aid, "name": name, "homepage": home,
        "github": v["github"], "description": desc,
        "category": cat, "interface": iface,
        "open_source": oss,
        "license": v["license"],                 # source-verified (SPDX; NOASSERTION = see repo)
        "stars": v["stars"],                      # source-verified
        "last_commit": (v["pushed_at"] or "")[:10],
        "local_models": loc, "provider_flexibility": mp, "tool_execution": te,
        "platforms": plat, "pricing": price,
        "source": "github-api", "verified": TODAY,
    }

def mk_prop(row):
    aid,name,home,gh,desc,cat,iface,loc,mp,te,plat,price = row
    return {
        "id": aid, "name": name, "homepage": home, "github": gh,
        "description": desc, "category": cat, "interface": iface,
        "open_source": False, "license": "proprietary", "stars": None,
        "last_commit": None,
        "local_models": loc, "provider_flexibility": mp, "tool_execution": te,
        "platforms": plat, "pricing": price,
        "source": "homepage", "verified": TODAY,
    }

agents = [mk_oss(r) for r in OSS] + [mk_prop(r) for r in PROP]
agents.sort(key=lambda a: a["name"].lower())

doc = {
    "$schema": "./schema.json",
    "updated": TODAY,
    "count": len(agents),
    "notes": ("Source-verified fields (github, license, stars, last_commit) come "
              "from the GitHub API on the 'verified' date. Editorial fields "
              "(category, interface, local_models, provider_flexibility, "
              "tool_execution, platforms, pricing) are best-effort classification "
              "and may lag; values can be true/false/\"partial\"/\"unknown\". "
              "See docs/methodology.md."),
    "agents": agents,
}
out = os.path.join(ROOT, "data", "agents.json")
json.dump(doc, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"wrote {len(agents)} agents -> {out}")

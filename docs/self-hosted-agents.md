# Self-hosted and local-model agents

Agents you can run without sending code to a third-party model API — either by
pointing them at a local model server, or by self-hosting the whole thing.

## Two levels of "local"

1. **Local model, cloud-ish agent** — the agent runs on your machine and talks
   to a local model server (Ollama, LM Studio, llama.cpp, vLLM, or any
   OpenAI-compatible endpoint). Aider, Cline, Continue, Void, Twinny and others
   work this way.
2. **Fully self-hosted** — you host the serving layer too. **Tabby** and
   **Refact** are built to run on your own GPU.

## Filter them

```bash
python scripts/agents.py --local --sort stars
python scripts/agents.py --local --open-source --format md
```

`local = partial` means limited or enterprise-only local support (e.g. Tabnine,
JetBrains AI).

## Hardware, briefly

- Small code models (3B–8B, quantized) run on a single modern GPU or even CPU.
- A 30B-class mixture-of-experts model at 4-bit fits in roughly 18–24 GB of
  VRAM; memory bandwidth matters more than raw FLOPs for single-user use.
- Rent by the hour before buying if you're unsure.

## Why self-host

- Privacy: code never leaves your network.
- Cost control at volume.
- Works offline / air-gapped.

The trade-off is setup and maintenance. If you want local-style control without
running a GPU, a hosted OpenAI-compatible API (for example
[Tartarus](https://tartarusai.dev/?utm_source=github&utm_medium=docs&utm_campaign=awesome-ai-coding-agents&utm_content=self-hosted))
is the middle ground — you don't self-host, but any OpenAI-compatible client
still works.

Full verified table:
[Local-model coding agents](../README.md#local-model-coding-agents).

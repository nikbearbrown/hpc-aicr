---
name: local-llm-on-explorer
description: Guide a researcher, step by step, through running an open model (Ollama in an Apptainer container) on a Northeastern Explorer GPU and pointing Claude Code at it. Checks cluster access with read-only commands, writes small scripts into ~/.ollama-hpc, runs one setup job and one short GPU test (asking before each), then hands the researcher the commands for their own session. Use when someone wants a local model, no per-token billing, or to run a coding agent against a model on the cluster. Loads on top of the hpc skill.
version: 2026-10-13
---

# local-llm-on-explorer: read `GET-STARTED.md`, and `HPC.md`, first

This skill is a pointer. The recipe is in [GET-STARTED.md](./GET-STARTED.md) and the scripts it installs are in `scripts/`. Read the `hpc` skill's `HPC.md` first: **ask before every `sbatch` and every file you write on the cluster, never compute on a login node, never type or read a password, passphrase or key, never bind Ollama to every address.**

Nothing here has been run end to end. Six scripts come exactly from the tutorial in `films/running-a-local-llm-on-explorer/source/`; two (`setup.sbatch`, `smoke-test.sbatch`) are new and only syntax-checked. Anthropic does not support pointing Claude Code at non-Claude models: this is an unsupported route. This is for Explorer, not AICR.

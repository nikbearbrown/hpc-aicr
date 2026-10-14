# STORY: Running a Local LLM on Explorer

**What this is.** The facts behind a lecture film on running an open model on a Northeastern Explorer GPU and pointing a coding agent (Claude Code, Aider, Continue) at it. **Why it matters.** "No per-token billing" is true, "free" is not: the cost moves to queue time, fair share and capability, and a few common settings (binding to every address, a doubled base address, unmapped model names, a tiny default context window) quietly break the setup or expose the model to everyone on the node. **What we found.** One setup works for one person today (the model and the agent in one GPU job, or the agent on a laptop through an SSH tunnel and a token proxy). A standing endpoint for a whole class is a policy question for Research Computing, not a configuration. **What is NOT verified.** The setup was documented, not run start to finish for this film; the film says so (B95). Nothing we read says whether automated agent access is allowed.

## Sources
- The tutorial, read in full: `_research/source-tutorial.md` (a copy of `hpc-aicr/Running-a-Local-LLM-on-Northeastern's Explorer-Cluster-and-Pointing-Coding-Agents-at-It/explorer-local-llm-tutorial.md`). Every script line on screen is read from it by `make_sheet.py`.
- Primary documentation checked 2026-10-13 by three verification passes: `_research/check-ollama.md`, `_research/check-harness.md`, `_research/check-rc.md`.
- Real checks on Explorer recorded in `hpc-aicr/skills/hpc/HPC.md` (Appendix A items 26 and 27, Sections 7 and 8).

## The shape
1. The idea and its layers: three layers, Pattern A, Pattern B.
2. Wrong turns to avoid: open network binding, the base address, the tunnel target, model-name aliases, the default context window, a too-small model, "free".
3. One-time setup: the environment file, caches and images, the start script, the Claude Code script, a token.
4. Choose a GPU and a model: fit in video memory, sizes, one GPU per job, context knobs.
5. Pattern A on the GPU node: the session, start and prove, point Claude Code, the limits, headless batch.
6. Pattern B from a laptop: the token lock, the proxy rules, the tunnel, check the lock, two residual risks.
7. Other coding agents: Aider, Continue, `ollama launch` tools.
8. When it breaks: four common failures, the proxy trap.
9. The cluster's rules: the idle watcher, why a shared endpoint is not a job's shape, a service's questions, five questions for Research Computing, AICR, what we checked.
10. What to expect: a weaker agent, where it works, the practical split.

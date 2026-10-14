# SOURCES: Running a Local LLM on Explorer

**What this is.** What the film stands on, and every edit to real text on screen. **Why.** A film must never show invented script text or invented output.

## Sources
- `_research/source-tutorial.md`: the tutorial, read in full (copy of `hpc-aicr/Running-a-Local-LLM-on-Northeastern's Explorer-Cluster-and-Pointing-Coding-Agents-at-It/explorer-local-llm-tutorial.md`, 2026-10-13).
- `_research/check-ollama.md`, `_research/check-harness.md`, `_research/check-rc.md`: the three verification passes against primary documentation (docs.ollama.com, ollama.com library pages and blog, github.com/ollama/ollama Dockerfile, apptainer.org docs, docs.vllm.ai, code.claude.com docs, aider.chat docs, docs.continue.dev, rc.northeastern.edu, rc-docs.northeastern.edu, docs.aicr.ai).
- `hpc-aicr/skills/hpc/HPC.md`: the real checks (Appendix A 26 and 27; Sections 7 and 8).

- `hpc-aicr-release/skills/local-llm-on-explorer/GET-STARTED.md` (B111 reads its three commands from it).

## Edits to real text on screen
1. Every script line on a terminal beat is read from the tutorial by `sl()` or `sq()`; long lines are cut at a word boundary with `…`. No word inside a shown stretch is changed.
2. Comment lines starting `# wrong`, `# right`, `# expect`, `# on the node`, `# from the laptop`, `# confirm …`, `# PROCESSOR …`, `# CONTEXT …`, `# gpu-interactive: …`, `# a specific GPU type …`, `# module purge also removes …`, `# talking to a local server …` and the file name `~/.continue/config.yaml` are LABELS written for the film from the tutorial's own prose or from the cited pages; they are not script text.
3. B82's three commands (`module purge`, `module load explorer`, `unset http_proxy https_proxy`) come from Research Computing's pages (modules page; the Ollama post), not from the tutorial.
4. `/status` on B52 is the command the tutorial says to run inside Claude Code; no output is shown.
5. No command output is shown anywhere: none was recorded for this film.
6. The tutorial's `INC…` ticket number and the earlier-guidance framing are left out (ACTS.md, LEFT OUT 1).
7. B111's two comment lines (`# then paste the prompt ...`, `# it asks before ...`) are labels written for the film from the guide's own text.

# ACTS: Running a Local LLM on Explorer (lecture coverage map)

**What this is.** Where every part of the source tutorial lands in the film, and what was left out and why. **Why.** The lecture covers the whole source or says why not. **Found.** Every teaching part is in an act; five items are LEFT OUT.

| Source part | Act | Beats |
|---|---|---|
| Introduction (what it is, two patterns that work, a shared endpoint is a policy question) | I | B10, B11, B12, B13, BIDEA |
| Part 0, corrections: OLLAMA_HOST 0.0.0.0, SSH tunnel target, /v1 base address, model aliases, default context, small reasoning model, "zero marginal cost" | II | B20 to B27 |
| Part 1, how the pieces fit (three layers; Patterns A, B, C) | I (A, B), IX (C) | B11, B12, B13, B91 |
| Part 2, one-time setup (steps 1 to 8) | III | B30 to B35 |
| Part 3, choose a GPU and a model | IV | B40 to B44 |
| Part 4, Pattern A on one GPU node | V | B50 to B54 |
| Part 5, headless runs in batch | V | B55 |
| Part 6, Pattern B from a laptop | VI | B60 to B64 |
| Part 7, other harnesses (Aider, Continue, Codex/OpenCode/Droid) | VII | B70, B71, B72 |
| Part 8, troubleshooting | VIII | B80, B81, B82 |
| Part 9, operating within the cluster's rules (idle watcher) | IX | B90 |
| Part 10, the shared endpoint question and the questions for RC | IX | B91, B92, B93, B94 |
| Part 11, what to expect | X | B100, B101, B102 |
| (added) the get-started recipe in the repository | XI | B110, B111 |

**Added from real checks (not in the source):** B81 and B82 (the proxy module and the proxy variables, from Research Computing's own pages), B53 (the unsupported-route finding, from Anthropic's documentation), B95 (what was and was not checked), B110 and B111 (where to get the paste-in get-started recipe and how to start it; the recipe is `skills/local-llm-on-explorer/GET-STARTED.md` in the hpc-aicr repository).

## LEFT OUT
1. **The ticket framing** in Part 0's title and Part 10's heading (a ticket number and who asked): background to the source, not teaching, and a private reference. The question it asks is kept (B93).
2. **The Google Antigravity row** in Part 0: the source itself says it could not confirm local-model support; the verification pass found the documented route is a Python SDK, not the editor, so the row would teach nothing reliable.
3. **`tmux` details beyond one sentence** and the OnDemand JupyterLab alternative in Part 4: one clause in B50 covers tmux; OnDemand is human-only and outside the film.
4. **The `~/.bashrc` PATH line detail** (Part 2 step 8) beyond showing the line: a one-line plumbing note.
5. **"Further reading"**: a list of links; the claims they back are checked in FACTCHECK.md.

## Cast per act
- I: the Claude chip (agent), a GPU-node rack, the plain model block, the Ollama logo chip, the laptop slab and Professor Bear (B13).
- II: the Claude chip; the same model block; a door on the rack (B20), address strings in mono.
- III to V: terminals only (plus B31's home box and rack).
- IV: video-memory tank, weight and cache blocks.
- VI: the rack with the Caddy gate and padlock; key object.
- IX: racks, clock dial, the idle watcher; the AICR rack (B94).
- X: the context bar, Claude chip, the local-model rack.
- XI: the repository address, a folder chain, one document page (B110); a terminal with three real commands (B111).

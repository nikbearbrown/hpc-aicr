# STORY: Guiding Your Agent: HPC.md and AICR.md

**What this is.** The facts behind the film that explains the two agent rule files, `HPC.md` and `AICR.md`: why a researcher who lets Claude work on a cluster needs written rules, and a walk through both files. **Why it matters.** An agent is fast, literal and tireless; a shared cluster is scarce and the costly failures are quiet. **What we found.** The files hold the general rules (HPC.md), the stricter AICR rules (AICR.md), a reason with every rule, honest labels for what is unverified, and rules that came from real mistakes made while building these films. **What is NOT verified.** The rules have not been tested by giving them to a fresh agent on a task and measuring the difference; no policy page says whether automated agents are allowed on either cluster.

## Sources (all in this repository)
- `hpc-aicr/skills/hpc/HPC.md` (the general rules, written for Explorer) and `hpc-aicr/skills/aicr/AICR.md` (what is stricter on AICR).
- The real session record in `../claude-liam-lecture-making-lecture-films-on-explorer/SESSION.md` for the three mistakes in Act IV.
- Every file excerpt on screen is read from the file by `make_sheet.py` (a missing line stops the build).

## The shape
1. **Why an agent needs rules.** Fast, literal, tireless; shared cluster. Three quiet failures (wrong machine, request far bigger than the job, a check that passes when it should fail). Two files; one line in `CLAUDE.md` or `AGENTS.md` points at them.
2. **Walking through HPC.md**, section by section: the summary and the agent line, the prime directive, the hard nevers (each with a because), before the first command, is parallel even the answer, sizing and submitting, verifying the GPU, where files live, software in order, the record every job leaves, being an agent on the cluster, slide errors, the honest appendix.
3. **What AICR.md changes**: it wins on AICR; AICR is not Explorer; five differences; its own nevers; the template; jobstats and its targets; quiet lessons from real runs; the questions to ask.
4. **Rules born from real mistakes** (2026-10-11, building the Explorer rendering film): listing all of `/projects` and a hung `du` (now a hard never in HPC.md), `module purge` removing the proxy (now a rule in Section 8), scratch owned by root (now a rule in Section 7).
5. **Using the files**: put them where the agent reads them, add one line, ask for the rules back before it runs anything; they do not replace judgment; labels say how we know each claim.

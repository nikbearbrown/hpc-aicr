# Agent rules for the Explorer and AICR clusters

**What this is.** Two rule files that make a coding agent (Claude Code, Codex, and similar) follow cluster best practice when it helps a researcher who is not an expert in parallel computing: [`hpc/HPC.md`](hpc/HPC.md) for Northeastern's Explorer cluster and shared Slurm clusters in general, and [`aicr/AICR.md`](aicr/AICR.md) for the AICR GPU cluster. Each is also packaged as a skill (`SKILL.md` plus `agents/openai.yaml` for Codex) in the same layout as the Remotion agent skills.

**Why.** Most cluster trouble is not hard computer science. It is a request that is too big, a GPU that sits idle, work run on a login node, data left on a disk that gets wiped, or a command run on a shared system without looking first. An agent does the careful, checkable parts every time. These files tell it what to do, what never to do, and what to ask first.

**What was found writing them.** The same few mistakes cost the most: several GPUs or nodes for code that uses one, a data loader left at its default so the GPU starves, scaling up before one GPU is busy, `--mem` mistaken for GPU memory, and never checking which GPU a job really got. The training material also disagrees with itself in places (scratch quota, who may add project guests, utilisation thresholds, which Python setup to use), and some slide examples are wrong as written. Every conflict is listed in each file's appendix, with the safe reading the file takes.

**What is NOT verified.** The rules come from reading Research Computing's own training material and the AICR documentation (dated May to July 2026), plus real AICR job logs and two live read-only logins. They were fact-checked against those sources, not run on a cluster. Partition limits and quotas change; every file says "confirm live". Whether Research Computing permits automated agent access is not addressed by any page read: ask rchelp@northeastern.edu.

## How to use them

**Do not paste these files into `CLAUDE.md` or `AGENTS.md`.** Put one pointer in the file your agent already reads, so it loads the rules only for cluster work. Use the absolute path of wherever you keep the files.

For `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex and others):

```
## Research computing clusters

When a task involves the Explorer cluster, Slurm (sbatch, srun, squeue), HPC, GPUs on a cluster, or Northeastern Research Computing, read `<path>/skills/hpc/HPC.md` completely before running any cluster command, and follow it.
When a task involves the AICR cluster (login.aicr.ai, ssh aicr, B200 or RTX PRO 6000 GPUs), also read `<path>/skills/aicr/AICR.md` after HPC.md.
Never type or read a password, passphrase or key. Use `ssh -o BatchMode=yes`. Ask before submitting, cancelling or deleting anything.
```

**As skills.** Copy `hpc/` and `aicr/` into `~/.claude/skills/` (Claude Code) or your agent's skills folder; each `SKILL.md` tells the agent to read the matching file. The skills repository layout matches `npx skills add <owner>/<repo>`, which is **untested for this repository**.

**To a researcher with a new agent session:** "Read `HPC.md` first" is enough. For AICR: "Read `HPC.md`, then `AICR.md`."

## The files

| File | What it holds |
|---|---|
| `hpc/HPC.md` | prime directive; the hard NEVERs table; questions to ask first and the read-only commands; Explorer at a glance; is parallel even the answer; sizing and submitting; GPUs; storage and transfers; software and environments; reproducibility; running as an agent; Linux habits; script traps; getting help; conflicts appendix |
| `aicr/AICR.md` | what is different or stricter on AICR; getting in; partitions and GPU requests; the develop-then-batch workflow and a template; measuring (`jobstats`); AICR speed-ups; storage and project end; transfers; environments; twenty lessons from real jobs; questions before a GPU job; conflicts appendix |
| `film-on-explorer/` | a plan and scripts for rendering a narrated lecture film on Explorer (pack, stage, one-time setup, render, fetch, clean up). **Not run on a compute node yet**: the first job is a pilot. Explorer only, not AICR |
| `hpc/SKILL.md`, `aicr/SKILL.md` | thin routers (the rules live only in the two files above, so they cannot drift apart) |

## Keeping them current

Dated 2026-10-11. When Research Computing changes a page, fix the rule in its file and the conflict in the appendix, not a summary. If a file and a live record disagree, the live record wins and the file gets fixed.

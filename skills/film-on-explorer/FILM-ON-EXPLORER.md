# Rendering a lecture film on Explorer

**What this is.** A plan, and the scripts for it, for rendering a narrated lecture film on Northeastern's **Explorer** cluster instead of on your own computer: pack the film and its toolkit, copy them to a job-scoped folder on Explorer scratch, render with Slurm, bring the finished video back, and delete everything the job created. It is for faculty who make lecture films for their classes. Making course materials is educational use, which is what Explorer is for. **It is not for AICR**, whose documentation says heavy CPU work belongs on the home institution's cluster.

**Why it could be worth it.** A 4K film takes hours of CPU and many gigabytes of disk. A laptop is tied up and fills its disk; Explorer has 250 CPU nodes in the `short` partition. Several films can render at once, and the laptop stays free.

**What we found.** It looks doable, with one unknown that decides it. We probed Explorer's login node read-only on 2026-10-11: it has `FFmpeg/7.1.1` and `nodejs/v22.11.0` as modules, a `miniconda3` module for Python, the Chrome and cairo/pango libraries that Remotion and Manim need, and 20+ CPUs and 62+ GB on every `short` node. The login node can reach PyPI, npm, GitHub and Hugging Face. The toolkit package is **57 MB** compressed and one film is **7 MB** (the 4.2 GB of `node_modules` is rebuilt on the cluster, which also fixes the fact that a Mac is arm64 and Explorer is x86_64). Eleven of our twelve films need no LaTeX. There is no TeX Live module on Explorer.

**What is NOT verified.** Nothing has been run on a compute node. The deciding unknown is **whether a compute node can reach the internet** (the one-time setup downloads Python and npm packages and a headless Chrome); the setup job checks this first and stops with a clear message if it cannot. Also untested: Remotion's Chrome inside a Slurm job, Manim 0.18 on Python 3.12 here, the toolkit's `./art smoke` render on Explorer, run time, and memory (the numbers in the scripts are first guesses). The scripts were syntax-checked, and `pack_for_cluster.sh` and the path guard in `fetch_and_clean.sh` were tested on a Mac.

## Who this is for, and what you need

A professor with an Explorer account in a research group (see `films/10-requesting-access-to-explorer`), an SSH key set up for Claude Code (see `films/logging-into-explorer-with-claude`), the film folder, and the [brutalist.art](https://github.com/nikbearbrown/brutalist.art) toolkit. Claude Code does the typing; you give the yes at each step. The narration audio is made on your own computer first (free, fast), so no text-to-speech runs on the cluster.

## The seven steps

The agent rules in [`skills/hpc/HPC.md`](../hpc/HPC.md) apply throughout: read-only first, **ask before every `sbatch`**, never compute on a login node, never type or read a password, and delete only what you can list.

| # | Step | Who / where | Script |
|---|---|---|---|
| 1 | **Pack** the toolkit and the film into two archives. Prints the projected size and refuses if it is over 3 GB | your computer | `scripts/pack_for_cluster.sh <books> <film-folder> <out>` |
| 2 | **Stage**: make one job folder `/scratch/<user>/film-jobs/<slug>-<stamp>/` with a `.film-job` marker and copy the archives in | your computer, 1 ssh call | `scripts/stage_to_explorer.sh explorer <out> <slug>` |
| 3 | **Set up once**: build Python 3.12, `pip install -r requirements.txt`, `npm ci`, headless Chrome, then `./art doctor` and `./art smoke`. Lives in **`/projects/<project>/film-toolkit`** (never scratch: it is purged on the first Tuesday of the month) | Explorer compute node via `sbatch` | `scripts/explorer_setup.sbatch` |
| 4 | **Render**: `art run` then `art final` at 4K from the staged folder | Explorer compute node via `sbatch` | `scripts/explorer_render.sbatch` |
| 5 | **Watch** with `squeue -u $USER` no more than once every five minutes; read the `film-render-<id>.out` log | your computer, read-only | |
| 6 | **Fetch** the master and logs back; verify with a checksum dry run | your computer | `scripts/fetch_and_clean.sh explorer <remote-dir> <local-out>` |
| 7 | **Clean up**: delete that one job folder, only after you say yes | your computer, 1 ssh call | `scripts/fetch_and_clean.sh ... --yes-delete <exact-folder-name>` |

The setup (step 3) is done once per group and reused for every film. After `seff <jobid>`, right-size the memory and time in the two `sbatch` files.

**The cleanup is deliberately narrow.** `fetch_and_clean.sh` refuses any path that is not exactly `/scratch/<user>/film-jobs/<slug>-<YYYYmmdd>-<HHMM>`, refuses a folder without the `.film-job` marker, copies first and verifies, prints what is inside, and then runs one `rm -rf` of that folder. The toolchain in `/projects` is never touched.

## The pilot (do this before promising anything)

Run steps 3 and 4 once for one short film, with your yes at each `sbatch`. The setup job answers the open questions in this order, and stops at the first failure:

| Question | If it fails |
|---|---|
| Can a compute node reach PyPI and npm? | Stop. Ask rchelp@northeastern.edu how to get packages onto a compute node (a mirror, a staged wheelhouse, or doing the download-only steps from the login node). |
| Does `pip install -r requirements.txt` work on Python 3.12 (Manim 0.18)? | Try another Python from `module avail`, or pin versions; record the working set in `requirements-explorer.txt`. |
| Does `npm ci` finish, and does `npx remotion browser ensure` get a Chrome? | Check the missing shared library with `ldd`; ask Research Computing for the module. |
| Does `./art smoke` produce a watchable video? | Read its log; fix the smallest failing step. |
| How long, and how much memory? | `seff <jobid>`; set `--time` to measured runtime + about 20% and `--mem` to about 1.3 times the peak. |

## What it costs, and what it saves

| | Value |
|---|---|
| Toolkit package | 57 MB compressed, 97 MB unpacked (measured, 2026-10-11) |
| One film package | about 7 MB without rendered output (measured, one film) |
| Rebuilt on the cluster | about 4.2 GB of `node_modules` plus the Python environment (the 4.2 GB figure is the Mac's folder; the cluster size is unmeasured) |
| Network needed once | PyPI, npm, GitHub (login node: yes; compute node: unknown) |
| Rendering time on Explorer | unknown until the pilot |

## Known gaps and cautions

- **LaTeX.** One of our twelve films (parallel computing) uses `Tex`. There is no TeX Live module on Explorer. Films without maths need nothing; for the one that does, ask Research Computing or install TinyTeX in project space.
- **Publishing never happens here.** The master comes back to your computer; the toolkit's own staging and upload rules apply there.
- **Acceptable use.** Explorer is for Northeastern-sponsored research or coursework; lecture films for your own course fit. No policy page we read mentions automated agent access or rendering workloads: ask rchelp@northeastern.edu once before regular use, and keep jobs inside `short`'s limits (2 days maximum).
- **Shared system manners.** Request what the job needs (measure after the pilot), never run the render on a login node, and cancel only your own job by its ID.
- **Reproducibility.** Record the module versions and `pip freeze` of the working environment next to the film.

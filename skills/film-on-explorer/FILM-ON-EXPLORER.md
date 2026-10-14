# Rendering a lecture film on Explorer

**What this is.** A plan, the scripts for it, and the record of one real run: render a narrated lecture film on Northeastern's **Explorer** cluster instead of on your own computer. You pack the film and its toolkit, copy them to Explorer, render on a compute node with Slurm, bring the finished video home, and delete the job's folder. It is for faculty who make lecture films for their classes. Making course materials is educational use, which is what Explorer is for. **It is not for AICR**, whose documentation says heavy CPU work belongs on the home institution's cluster.

**Why it could be worth it.** A 4K film takes a long time and many gigabytes on a laptop, and ties it up. Explorer's `short` partition listed 252 nodes (20+ CPUs and 62 GB+ each) on 2026-10-11.

**What we found.** It works. On 2026-10-11 one finished film (44 beats, 46 Manim scenes) was rendered on Explorer and came out the **same film** as the one built on a Mac: 3840x2160, 24 fps, 518.875 s on both; file sizes 54.8 MB and 54.6 MB; twelve sampled frames scored between 0.948 and 0.9999 on a similarity scale where 1 is identical. Resource use: peak memory 9.6 GB, 16 cores used at 22 to 39 percent, 45 minutes for the first full render, 6 minutes for the final compile. **Rendering itself needs no internet**; only the one-time install does, and compute nodes reach PyPI and npm **through the cluster's proxy**. Getting there took seven setup jobs and several render attempts, because a cluster differs from a laptop in ways the layout and type gates caught one by one (the table below). The work is split by what each machine is good at: your computer writes the film and makes the voice; the login node only copies and submits; the compute node renders.

**What is NOT verified.** One film, one account, one day. The final **Gate T** (typography) **failed on two beats on the cluster and passed at home** (a text run 40 px against a floor of 41, and a portrait patch read as low-contrast text); the master was therefore built for comparison and is not the one to post. Why Gate T differs is not established. The smaller resource numbers in `explorer_render.sbatch` (8 cores, 16 GB, 3 h) are inferred from the measurements, not tested. LaTeX equation beats cannot render (no TeX Live module); the voice (Kokoro) is not installed on the cluster by design. No policy page we read mentions automated agent access or rendering workloads: ask rchelp@northeastern.edu once before regular use.

## Where each piece of work runs

| Work | Runs on | Why |
|---|---|---|
| Writing scenes, narration, beat sheet, fact-check | your computer (Claude Code) | Judgment work; needs your files and your yes |
| Narration audio (Kokoro text-to-speech) | your computer | Free, fast; ships to the cluster as mp3 and timings |
| Packing, copying, `ssh`, `sbatch`, `squeue`, fetching | your computer, through the login node | Light commands only; the login node is a door |
| Manim scenes, Remotion frames, the 4K encode, the compile, the layout and frame gates | **compute node** | The heavy CPU and memory work (measured above) |
| Watching the master, approving, publishing | your computer | A human decision; publishing never happens on the cluster |

## The install is a package, not a chore

`scripts/bootstrap_toolkit.sh` is idempotent and read-only unless you pass a flag. It compares a **fingerprint** of everything that decides what gets installed (Python requirements, the npm lockfile, the module list, the setup script, the Python version; `scripts/toolkit_stamp.sh`) with the stamp stored on the cluster after the last successful install.

| You run | What it does | Writes anything? |
|---|---|---|
| `scripts/bootstrap_toolkit.sh explorer /projects/<project>/film-toolkit <books>` | Reports whether the toolkit exists, whether its code is synced, whether the environment matches. Prints the one `sbatch` line if it is missing or stale | No |
| the same with `--sync-code` | Copies the toolkit code (about 56 MB, 9,106 files; **took about 6 minutes** to unpack on the project filesystem), the module list and the job scripts | Only inside the toolkit folder |
| the same with `--sync-scripts` | Copies only the job scripts and module list (seconds) | Only inside the toolkit folder |
| the `sbatch` line it printed (ask first) | Installs Python 3.12, Manim from conda-forge, the packages, `npm ci`, headless Chrome, a private font setup; runs `art doctor`; stamps | Inside the toolkit folder |
| `scripts/explorer_cache.sh` | Only needed if compute nodes lose the proxy: downloads wheels and the npm cache from the login node | `cache/` in the toolkit folder |

The toolkit lives in **`/projects/<project>/film-toolkit`** (2.7 GB after the pilot). **Never in scratch**: it is purged on the first Tuesday of the month, and on the pilot account `/scratch/<username>` was owned by root and not writable at all.

## The steps for one film

| # | Step | Where | Script |
|---|---|---|---|
| 1 | **Pack** the film. Prints the projected size, refuses over 3 GB. Carries the film's own capture pictures, the hand-built title-card clip and the exact Professor Bear portraits its scenes pick | your computer | `scripts/pack_for_cluster.sh <books> <film-folder> <out>` |
| 2 | **Stage**: one job folder with a `.film-job` marker, the film archive copied in. Set `JOBROOT=/projects/<project>/film-jobs` if scratch is not yours | your computer | `scripts/stage_to_explorer.sh explorer <out> <slug> skip-toolkit` |
| 3 | **Check the toolkit** is current; sync and install only if stale | your computer, then a compute node | `scripts/bootstrap_toolkit.sh` |
| 4 | **Render**: `art run` (Manim, Remotion, review cut, gates) then `art final`. Ask first | compute node via `sbatch` | `scripts/explorer_render.sbatch` |
| 5 | **Watch** with `squeue -u $USER` no more than every five minutes; read `film-render-<id>.out` | your computer, read-only | |
| 6 | **Fetch and verify**: copy back, checksum dry run must be empty; compare with your own master | your computer | `scripts/fetch_and_clean.sh explorer <remote-dir> <local-out>` |
| 7 | **Clean up**: delete that one job folder, only after you say yes and only by its exact name | your computer | `... --yes-delete <exact-folder-name>` |

**The cleanup is deliberately narrow.** `fetch_and_clean.sh` refuses any path that is not exactly `/scratch|/projects/<name>/film-jobs/<slug>-<YYYYmmdd>-<HHMM>`, refuses a folder without the `.film-job` marker, copies first and verifies, prints what is inside, then runs one `rm -rf` of that folder. The toolchain is never touched.

## What the pilot found (each row was a real failure with a real log)

| Symptom | Cause | Fix now in the scripts |
|---|---|---|
| Setup's network check timed out | `module purge` at the top of the script removes the default module `explorer/1.0`, which sets the **proxy**; a one-line `srun` test had reached PyPI (HTTP 200) | `explorer/1.0` is the first name in `film-modules.txt` and is loaded after the purge |
| `pip install manim` failed on `manimpango` | Explorer has Pango/Cairo runtime libraries but not their developer files | Manim from **conda-forge**, pip last, pip told to leave manim alone |
| Headless Chrome download timed out | Remotion's downloader (Node 22.11) ignores the proxy; pip, npm, conda and curl honour it | Fetch the Chrome zip with `curl`, unpack where Remotion looks |
| `art doctor`: fonts blocked | The toolkit installs fonts into `~/.local/share/fonts`; a job should not write to `$HOME` | A private fontconfig file pointing at the bundled fonts |
| `art smoke` failed | It fails the same way on the Mac ("metadata.slug must be a filename"): a toolkit bug | The pilot film is the smoke test; bug reported as a task |
| Gate B failed on one scene | The film names Apple's **Menlo**; Linux has none, the fallback is a different width and a label hit a line | `fontconfig` alias Menlo → the bundled PT Mono |
| The same failure again after the fix | Manim reuses text it has already drawn | Clear the job's own `media/texts`, `media/videos`, `manim` before re-rendering |
| Remotion beat `B12` failed, run stopped | The pack left out the film's capture pictures and the hand-built title-card clip | The packer carries both inside the film archive |
| Compiler REFUSED: 21 frames short | Every Manim clip was one frame short: the toolkit's `requirements.txt` pins `manim<0.19` but the Mac builds with **0.20.1** | Install 0.20.1; a task asks the toolkit owner to fix the pin |
| Gate V: 88 blockers, one finding | The cluster's ffmpeg has `drawtext`, so the review cut burned a timestamp box in a corner | `ART_NO_DRAWTEXT=1` in the render script |
| Gate V: low contrast on two scenes | The Professor Bear photos live in a 4.5 GB library that is never shipped: seven scenes drew a gray square | The packer works out the six files the scenes pick (seeded, so identical) and ships only those (94 MB) |
| Gate T failed two beats on the cluster | Not established (1 px on one text run; a portrait region on another) | Unresolved. Check on the Mac before posting |

## Known gaps and cautions

- **Gate T disagrees** (above). A film rendered here is checked again at home before it is staged.
- **LaTeX.** A film with Manim equation beats needs TeX Live; Explorer has no module. Most of our films need none.
- **Publishing never happens here.** The master comes home; the toolkit's own staging and upload rules apply there.
- **Acceptable use.** Explorer is for Northeastern-sponsored research or coursework; lecture films for your own course fit. Ask rchelp@northeastern.edu once about agent-driven workloads, and keep jobs inside `short`'s limits (2 days maximum).
- **Shared-system manners.** Request what the job needs (measure with `seff`), never run the render on a login node, never run `du` over `/projects` from a login node (it hung and was stopped), never list other people's project folders: ask for your own groups.
- **Reproducibility.** The setup saves `pip freeze` and the module list next to the toolkit; record them beside the film.

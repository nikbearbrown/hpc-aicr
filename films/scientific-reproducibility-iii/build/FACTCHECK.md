# FACTCHECK — Scientific Reproducibility III: Containers

**What this is.** Gate F: every number and named claim in the narration and on screen, against the source and, where cheap, the record we captured. **Why.** A wrong flag or limit in a research-computing film costs someone a failed job. **Found.** No contradictions. Two items stripped or reworded: the lesson's `latest`-safe wording (the Sylabs example `library://lolcow` carries no tag, so the film says so instead of claiming every example is pinned), and its transfer host name (possibly stale; the film says to check the current one). The film's honesty line (B80) lists what was only read.

Rows: `| # | Beat | Claim | Verdict | Source | Fix |`

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B10 | A container packages a program, libraries, settings and a small runtime in one file; behaves the same on any machine that can run it | OK | guide "The idea"; lesson "What is a container" | none |
| 2 | B11 | Docker is the common tool on laptops and cloud; Singularity is the older name; Apptainer the current name used on Explorer and AICR | OK | guide table; lesson note; `_real-outputs.md` (singularity exists on AICR) | none |
| 3 | B12 | Docker's normal setup needs administrator-level power; that is a security problem on a shared machine; Apptainer runs as you; it can read Docker images | OK (source claim; matches Apptainer's published design) | guide "The idea"; lesson | wording kept to the guide's |
| 4 | B20 | The stack is captured, so the result ties to a named versioned image; a collaborator months later gets the same software after system updates | OK | lesson "Reproducibility" | "same software" (the lesson says same results; we claim the narrower thing) |
| 5 | B21 | Same file runs on laptop, Explorer, another cluster, cloud; incompatible library versions get separate images | OK | lesson "Portability", "No dependency conflicts" | none |
| 6 | B22 | Docker Hub, Quay.io, NVIDIA NGC, BioContainers host thousands of maintained images | OK | lesson "Access to community-built images" | none |
| 7 | B23 | Images are large and the first build takes effort; order module, conda, container | OK | guide "Why use a container" | none |
| 8 | B30 | exec runs one command and returns (the verb for jobs); shell opens an interactive shell; run executes the default runscript | OK | guide table | none |
| 9 | B31 | `command -v apptainer` gives `/usr/bin/apptainer`; `apptainer --version` gives `apptainer version 1.4.5-3.el9`; no module needed on Explorer; AICR has apptainer and singularity | OK, recorded 2026-10-11 | `guides/_real-outputs.md` lines 52, 76-81, 115-116 | none |
| 10 | B32 | Run containers on a compute node, not the login node; heavy work on the shared login node gets terminated | OK | guide; HPC.md Section 1 | none |
| 11 | B33 | The prompt changes to `Apptainer>`; `exit` leaves | OK (source) | guide, lesson | shown as "from the source, not run" |
| 12 | B34 | Script lines, `mkdir -p logs`, `sbatch run_container.sh` | OK (verbatim from guide, placeholders kept) | guide "A CPU job" | none |
| 13 | B35 | The container can carry its own CUDA; `--nv` passes the node's driver; image CUDA must fit the driver | OK | guide "A GPU job"; lesson note | none |
| 14 | B36 | Interactive GPU test: `--partition=gpu-interactive --gres=gpu:1`; naming the type is good practice; `sinfo -p gpu -o "%G"` lists types | OK | guide; HPC.md Section 6 | the source line is 101 characters; shown on two lines with a shell line-continuation, words unchanged |
| 15 | B37 | Batch GPU template: one GPU, 8 h, partition `gpu` | OK | guide; `_real-outputs.md` (gpu 8:00:00) | none |
| 16 | B38 | gpu partition limit 8 h; gpu-short and gpu-interactive 2 h; a published example asks for 2 GPUs for 12 h | OK | `_real-outputs.md` lines 13-17, 35-39; lesson's sbatch (`gpu:v100-sxm2:2`, `12:00:00`) | none |
| 17 | B39 | Print the device name from inside; with --nv expect True and a card name; without it False | OK (source, not run) | guide "Try it" 6 | one-line command shown on two lines (continuation) |
| 18 | B40 | A container sees its own filesystem; home is bound automatically on Explorer; /projects and /scratch are not | OK | guide "Binding"; lesson note | none |
| 19 | B41 | `--bind host:inside`; same path both sides; absolute paths; bind only what is needed | OK | guide | none |
| 20 | B42 | `APPTAINER_BIND` can replace the flag; exporting it inside the job script keeps the record with the job; `~/.bashrc` is a permanent edit | OK | guide; HPC.md Section 8 | none |
| 21 | B50 | Building needs administrator rights; build where you have them; copy the .sif to the cluster, store in project space, run as yourself | OK | guide "Building"; HPC.md Section 8 | none |
| 22 | B51-B52 | `.def` sections and meanings; versions in the example are placeholders | OK | guide table and note | none |
| 23 | B53 | Build the Docker image locally, Apptainer converts it from the Docker store, or push to a registry and pull on the cluster | OK | guide "Building from a Dockerfile" | none |
| 24 | B54 | Dockerfile lines `FROM rockylinux:9.3`, `RUN pip3 install CDPKit`, verify line, `CMD` | OK, verbatim from the lesson | lesson | abridged; shown as the shape |
| 25 | B55 | `docker build -t myimage:1.0 .` then `apptainer build myimage.sif docker-daemon://myimage:1.0` | OK | guide | none |
| 26 | B56 | Remote builder needs a free account and uploads the recipe to a third party; the decision is the researcher's | OK | guide; HPC.md Section 8 | none |
| 27 | B60 | Pulling is heavy: do it on a compute node; produces `ubuntu_22.04.sif`; `--name` chooses the output name | OK | guide | none |
| 28 | B61 | Four pull examples (GATK 4.5.0.0, NGC pytorch 24.01-py3, BioContainers samtools, library://lolcow); the last has no tag | OK | guide table | the guide says every example names a version; `lolcow` does not, so the film says so |
| 29 | B62 | `latest` points at a different image next month; a pinned tag keeps pointing at the same one | OK | guide "Always pin the tag" | none |
| 30 | B63 | scp through the transfer node into project space; check the current transfer host; OnDemand Files app up to 10 GB | OK | guide; HPC.md Section 7 | host name not shown |
| 31 | B64 | Keep images in project space, not covered by the 75 GB home quota; keep the recipe beside the image, commit it, archive with data | OK | guide; lesson tips | none |
| 32 | B70 | The hidden Apptainer cache lives in home; a large pull can fill the quota and OnDemand sessions stop; point `APPTAINER_CACHEDIR` and `APPTAINER_TMPDIR` elsewhere; `apptainer cache clean all` is the gentler tool | OK | guide; HPC.md Section 7 | none |
| 33 | B71 | Test interactively first; print versions from inside | OK | guide | none |
| 34 | B72 | Record exact tag, ideally the digest; `.def` plus `.sif`; `sha256sum myimage.sif` | OK | guide | none |
| 35 | B73 | Nextflow and Snakemake can run each step in its own container; Research Computing offers help | OK | lesson | none |
| 36 | B74 | AICR has apptainer and singularity; no container policy documented in what we have; partition fixes the GPU type; do not copy Explorer's paths | OK | guide "AICR"; `_real-outputs.md`; AICR.md Section 4 | none |
| 37 | B80 | Three things checked read-only; nothing run | OK | guide "What we tested" | none |

## Datable items stripped
Version numbers other than the recorded Apptainer 1.4.5 appear only inside image tags copied from the source (`22.04`, `4.5.0.0`, `24.01-py3`, `3.11-slim`), shown as examples. The Spring 2026 series name and presenter are not spoken.

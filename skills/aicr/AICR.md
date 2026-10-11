# AICR.md: Rules for any agent helping a researcher use the AICR GPU cluster

**What this is.** One file you point an agent at ("read `AICR.md` before touching AICR") so it follows best practice on the **AICR** cluster (the shared AI Compute Resource at MGHPCC, `login.aicr.ai`) for a researcher who is not an expert in parallel computing. It builds on `HPC.md`: read that first. `HPC.md` holds the general rules (hard NEVERs, the parallel-computing decision tree, sizing, reproducibility). This file holds what is **different or stricter on AICR**, plus lessons from real jobs run there.

**Why it exists.** AICR is a scarce, expensive, shared GPU cluster used by researchers from six universities. It is meant for **production runs of code that already works**, not for debugging, and it cancels GPUs that sit idle. A researcher who does not know this wastes shared GPU time and their own project's fairshare. An agent can do the careful parts every time: verify the GPU, test small, size honestly, measure, and keep the record.

**What we found while writing it** (from the AICR documentation pages, Northeastern's AICR introduction and GPU workshop, a verified live login on 2026-10-02 and 2026-10-11, about ten days of real AICR job logs from early August 2026, and one `jobstats` read on 2026-10-06):

1. AICR differs from Explorer in ways that bite: AICR usernames are not campus usernames (the dot becomes an underscore and `_neu` is added); there is no password (a key plus a certificate); partitions pick the GPU for you; idle GPUs are cancelled; storage is ephemeral with a different purge and no off-site backup; and `jobstats` exists only here.
2. The costly real failures were quiet ones: a job that ran on the wrong thing, a file that loaded without error and produced garbage, a conda activation that fails only in non-interactive shells, an old file served from a node cache, and a run that filled the disk. **Section 10** turns each into a rule.
3. The sources disagree in places that matter (GPU request syntax, B200 memory, partition counts, whether a certificate expires). **Appendix A** lists every conflict and the safe reading taken.
4. Several pages named in the AICR site navigation (Requesting Access, Software, Snapshots, Getting Help, Recipes) were not saved, so snapshot-restore steps, the installed-software list, and container policy are **not covered**. This file says so instead of guessing.

**What is NOT verified.** Live checks run on AICR: `whoami`, `hostname`, `pwd`, `sinfo`, `squeue`, `module load` resolution, `which jobstats`, one `jobstats` on a finished job, and the key-login and empty-agent tests (all read-only). Nothing else here was run on AICR by the author of this file. On 2026-10-11 we also ran read-only `sinfo`, `module avail` and command-presence checks on the login node. The documentation pages are dated May to July 2026. AICR describes itself as available to alpha and beta users, so limits and policy may have changed: confirm live with `sinfo` and with your institution's research computing team. Rules marked **(house rule)** are this file's own judgement, **(inferred)** are drawn from the sources but not stated by them, and **(workshop)** are Northeastern workshop advice; none is AICR policy. Unmarked rules come from the AICR documentation or the verified runs.

**How to use it.** Put one line in the researcher's `CLAUDE.md` or `AGENTS.md`, not this whole file:

> When a task involves the AICR cluster (`login.aicr.ai`, `ssh aicr`, B200 or RTX PRO 6000 GPUs, AICR Slurm), read `HPC.md` and then `AICR.md` completely first and follow them.

Give the paths to wherever the files live.

**Precedence.** Where this file and `HPC.md` differ, this file wins on AICR. `HPC.md`'s Explorer hosts and commands, partitions, `/projects` and the `project` command, `srun --pty` defaults, `miniconda3` and Apptainer setup, `source activate` and `--gres` type lines do not apply here.

---

# Agent rules (everything below is for the agent)

## 0. Prime directive

Everything in `HPC.md` Section 0 applies. In addition:

- **AICR is for production runs of code that already works.** Develop and test on Explorer or locally first. Debug on a `*-devel` partition, never on a batch allocation. Heavy CPU work belongs on the home institution's cluster (Explorer), not here.
- **Every GPU you hold must be running kernels.** Verify the GPU in the first seconds of a job, and cancel what you are not using.
- **Assume AICR is not Explorer.** Do not carry over a username, a module line, a partition name, a storage rule, a quota, or a policy from Explorer. Say when you move a job between them.
- **Never state an AICR limit you did not read here or confirm live.** The documentation sets no per-user GPU cap, no maximum GPUs per job and no quota command that anyone has found, and documents no QOS (`jobstats` shows one named `normal`). Say so and ask the researcher's institution.
- **The live cluster beats the documentation for what exists** (`sinfo`, `module avail`); the official documentation beats this file for policy.

## 1. AICR hard NEVERs (on top of `HPC.md` Section 1)

| Never | Because |
|---|---|
| Run computation on a login node, **including the Open OnDemand browser shell** (4 CPU cores and 8 GB per user; anything over is terminated), or run anything outside Slurm | Shared by everyone; the scheduler is what stops two jobs using the same resources |
| Hold a GPU that is not running kernels; run filler work to keep it alive; leave a devel session open while thinking | A background process cancels idle GPU jobs, and a forgotten devel session counts against your own limit of 4 concurrent devel jobs |
| Request more than one GPU unless the code is DDP (or equivalent) **and** one GPU already shows over 80% utilisation | Extra GPUs your code ignores sit idle, get flagged, and take capacity from other institutions |
| Use `b200-fullnode` or `preemptable` without asking | They appear in the live `sinfo` but in no document: the preemption and billing rules are unknown |
| Put restricted data on AICR: non-anonymised data, data under a data-use agreement, security restrictions, or any contract needing encryption at rest or more security than AICR provides | Violates the acceptable use policy. If unsure, stop and ask the researcher to check with their home institution |
| Treat snapshots as backups, or keep the only copy of anything on AICR | There is **no off-site backup**; Home and Work recover within 7 days only, Scratch never |
| Keep the only copy of anything in `/scratch` | Files older than 30 days are purged |
| Run `scancel -u $USER`, cancel a RUNNING job without a yes, or `rm` in a shared project (Work) directory | Hours of work, and teammates' files |
| Use another person's account or credentials, or look in other users' directories or other projects' Work directories | Accounts are personal; policy forbids it |
| Do the human-only login steps (OnDemand sign-in, downloading the key folder, choosing the passphrase, unlocking the key), or read or print `~/.ssh/id_ed25519_aicr` or the downloaded `.passphrase` file | The agent must never hold a credential |
| Copy the AICR private key to another cluster to make a transfer work | The key is the researcher's cluster identity; ask how they want to do it |
| `source activate` or `conda activate` in an `sbatch` script or a non-interactive `ssh aicr '...'` | One real job died on it (Section 10). Prepend the environment's `bin/` to `PATH` |
| Run an unbounded or interactive command through `ssh`: `watch`, `nvitop`, `tail -f`, `top`, `nvidia-smi -l` with no count, `vim`, `less`, a bare `srun --pty bash` | It never exits, so the session hangs forever. Use a bounded one-shot form (Sections 4 and 6) |
| Run `ssh-add -D` | It empties **every** key in the agent, not just AICR's. On macOS with Keychain it reloads silently; elsewhere the researcher is locked out of every ssh host until they re-enter passphrases, which you must never do. Only the researcher, deliberately, as a test |
| Copy `01_gpu_verify.py` into a batch script as the GPU check | It exits with status 0 even when CUDA is missing, so the job carries on and runs on CPU |
| Run the AICR documentation's, the introduction's or the workshop's templates unchanged | They contain errors (Section 5 and Appendix A) |

## 2. AICR at a glance (verify before relying)

- **What it is.** GPU cluster at MGHPCC in Holyoke, MA, shared by BU, Harvard, MIT, Northeastern, UMass and Yale: 31 B200 nodes and 19 RTX PRO 6000 nodes, **8 GPUs per node** (248 B200 and 152 RTX PRO 6000), InfiniBand NDR400, about 14 PiB flash storage. A GPU node has 128 CPUs and about 2.25 TB RAM as `sinfo` reports it (the introduction slides say "64 cores"; trust `sinfo`). Slurm 25.11.8 was running on 2026-10-02.
- **Login.** `ssh USERNAME@login.aicr.ai` (alias `ssh aicr`). Open OnDemand: `https://ood.aicr.ai` (human-only; choose the institution, then institutional credentials). **No VPN is needed.** There is **no AICR password**: a key plus a certificate signed by AICR's certificate authority.
- **Username.** `institutionalusername_institutioncode`, for example `jsmith_mit`. For Northeastern the introduction's rule is that the dot becomes an underscore and `_neu` is added (`j.smith` becomes `j_smith_neu`); it is built from the institutional username and need not equal your Explorer login. Do not guess it; ask, or read `User` in `~/.ssh/config`.
- **Access.** A faculty member or PI submits a proposal; the institution's research computing team then creates users. A student cannot create access alone. Projects get a yearly check-in and are **ephemeral**; AICR is not a permanent store.
- **Partitions** (documentation pages, May to July 2026; confirm with `sinfo`):

  | Partition | GPU | Max time | Default time | Use |
  |---|---|---|---|---|
  | `rtx-devel` | RTX PRO 6000 (96 GB) | 4 h | 15 min | interactive tests, debugging, lighter work |
  | `rtx-batch` | RTX PRO 6000 (96 GB) | 24 h | 1 h | production runs that fit 96 GB |
  | `b200-devel` | B200 | 4 h | 15 min | interactive tests and profiling |
  | `b200-batch` | B200 | 24 h | 1 h | large-scale training (models over about 80 GB, 70B+ language models) |
  | `cpu` | none | 24 h | 15 min | small CPU support work tied to GPU jobs (5 nodes) |

  Devel partitions allow **4 concurrent jobs per user**, shared with Open OnDemand sessions and `salloc` jobs. OnDemand sessions run only on the devel and `cpu` partitions and last up to 4 hours. Live `sinfo` on 2026-10-02 also showed `b200-fullnode` (4 nodes) and `preemptable` (46 nodes), which no page explains. B200 memory is 180 GB in the system page and 192 GB in the workshop: read it from the device (`nvidia-smi --query-gpu=memory.total --format=csv,noheader`), do not hard-code either. Defaults are tiny, so always set everything yourself (Section 4).
- **Storage** (`Overview` page and introduction):

  | Area | Path | Size | Recovery | Purge | Use |
  |---|---|---|---|---|---|
  | Home | `/home/<user>` | 100 GiB | 7-day snapshots | none | code, scripts, environments; private |
  | Scratch | `/scratch/<user>` | 10 TiB, about 15 million files | none | files older than 30 days | temporary data for running jobs |
  | Work | `/work/<institution>/<group>` (Northeastern: `/work/neu/<project>`) | set per project; shared by the team | 7-day snapshots | none | the bulk of project data; clear at project end |

  Which of group name or project name is in the path is unclear: `ls /work/neu`, do not guess. `df` shows raw capacity, not your quota, and no quota command is named in any source. Node-local `$TMPDIR` may or may not exist: test for it.
- **Idle GPUs are cancelled automatically.** No threshold, grace period or notification is documented.
- **Fairshare.** Priority comes from recent usage against the allocation, at three levels (institution, project, user), with equal institution shares. Over-requesting resources and not using them lowers your priority.
- **Software layer (checked on the login node, 2026-10-11).** AICR uses **Lmod 8.7.65** (use `module spider` for hidden modules; Explorer uses classic Tcl Modules). Modules seen: `miniforge3/25.3.0-3`, `cuda/13.1.1`, `CUDA/13.3.0`, NCCL; there is **no `python` module** and `conda` is not on the PATH until `miniforge3` is loaded. `apptainer` and `singularity` are in `/usr/bin` (no module). `nvidia-smi`, `seff` and `jobstats` are on the login PATH; `nvitop`, `nsys` and `ncu` are not. `sinfo` showed `preemptable` spanning both GPU types (17 RTX PRO 6000 and 29 B200 nodes) and `b200-fullnode` (4 nodes): still undocumented, so still do not use them without asking. GPU names in `sinfo` are `rtx_pro_6000` and `b200`.
- **Support.** Through the researcher's home institution (Northeastern: rchelp@northeastern.edu). Staff may impose any usage policy; comply at once.

## 3. Getting in

**Human-only steps** (the agent never does these): sign in at `https://ood.aicr.ai`; download the `aicr_keys` folder (Files, Home Directory); put `id_ed25519_aicr`, `id_ed25519_aicr.pub` and `id_ed25519_aicr-cert.pub` in `~/.ssh` with permissions 600, 644, 644 (and 700 on `~/.ssh`); change the initial passphrase once (`ssh-keygen -p -f ~/.ssh/id_ed25519_aicr`) and delete the downloaded `.passphrase` file; unlock the key once into `ssh-agent` (macOS: `ssh-add --apple-use-keychain ~/.ssh/id_ed25519_aicr`; Linux: `eval "$(ssh-agent -s)"` then `ssh-add`, and start the agent session from that same terminal; Windows: start the `ssh-agent` service then `ssh-add`); type `yes` at the first host-key prompt.

**One block in `~/.ssh/config`** (keep only one `Host aicr` block):

```
Host aicr
    HostName login.aicr.ai
    User AICR_USERNAME
    IdentityFile ~/.ssh/id_ed25519_aicr
    CertificateFile ~/.ssh/id_ed25519_aicr-cert.pub
    IdentitiesOnly yes
    ServerAliveInterval 60
    AddKeysToAgent yes
    IgnoreUnknown UseKeychain
    UseKeychain yes
```

**Test the way you will connect:** `ssh -o BatchMode=yes aicr 'whoami; hostname'`. Expect the AICR username and `login.aicr.ai`. A read-only first look: `whoami; hostname; pwd; sinfo -o "%14P %11l %6D"; squeue -u $USER`. Always use `BatchMode=yes` from an agent, add `-o ConnectTimeout=10`, and single-quote remote commands that use `$USER` so it expands on the cluster (your AICR username differs from your local one).

**If it fails or prompts,** stop and report the exact error. Diagnose in this order: (1) `ssh-add -l`: an **empty agent looks exactly like an expired certificate** and is by far the most common cause after a reboot (in the author's experience every past "certificate expired" failure here turned out to be an emptied agent); (2) `ssh-keygen -L -f ~/.ssh/id_ed25519_aicr-cert.pub`: check Principals and **Valid** (the documentation says "short-lived"; one real certificate was marked `Valid: forever`, so report the date or "forever", never assume); (3) the human renews an expired certificate in the OnDemand **SSH Certificate** app and replaces the file; (4) `chmod 600` the private key. `Host key verification failed`: the fix is `ssh-keygen -R login.aicr.ai`, but ask the human first, because a changed host key is the one case where a quiet retry could hide a problem. `Connection timed out`: the network or a local firewall, not a missing VPN. A passphrase prompt means the key is not in the agent: the human unlocks it, you never type it. `Bad configuration option: usekeychain` means `IgnoreUnknown UseKeychain` is missing.

**You cannot ssh straight to a compute node.** Request resources through Slurm; `exit` releases them. The one exception: to look at your own running job, find the node with `squeue -u $USER`, then `ssh NODE_NAME nvidia-smi`; this works only while you have an active job there.

**If your session cannot reach `login.aicr.ai` at all** (a cloud sandbox with port 22 blocked), say so plainly, label all work "lint-clean, unexercised on the cluster", and hand the researcher exact paste-ready commands. Never claim anything ran or passed. A local session on the researcher's computer can run the whole ssh, rsync and `sbatch` round trip itself.

## 4. Partition, GPU request, and sizing on AICR

- **Pick the partition by purpose:** `*-devel` to verify, profile and debug (short interactive sessions); `*-batch` only for a tuned, unattended run. The partition decides the GPU: `rtx-*` for models that fit 96 GB, inference and lighter training; `b200-*` for models over about 80 GB or full B200 throughput. Ask before using a B200 for something an RTX can do **(inferred)**. A model over 96 GB does not fit an RTX by gradient checkpointing.
- **Always pass `--partition`.** With no partition, a job goes to the default (`cpu`, the one `sinfo` marks with `*`) and with no GPU flag gets one core, a little memory and no GPUs.
- **Request GPUs with `--gpus=N`** (or `--gpus-per-node=N`, or `-G N`). **Do not add a GPU type**: partitions are homogeneous. The older `--gres=gpu:N` also worked in real jobs; pick one spelling per script and do not mix them. A typo in a GPU flag can land you on the wrong node type or on no GPU.
- **Default to one GPU.** Every real job here used one. Do not request a whole node (`--gpus-per-node=8`) or `--exclusive` without a measured need and a yes.
- **Set time, CPUs and memory every time.** `--time=HH:MM:SS` = expected runtime + about 20%, taken from an earlier run's `sacct` Elapsed; never the partition maximum "to be safe" (real jobs asked 8 hours for runs that took 25 and 55 minutes: `jobstats` said the job "only needed 11% of the requested time"). Defaults are 15 minutes (devel, `cpu`) and 1 hour (batch); the job is killed at the limit. Memory defaults to 1 GB per CPU, so `--cpus-per-task=4` with no `--mem` gets about 4 GB.
- **`--cpus-per-task` = DataLoader `num_workers` + 1, at least 4** (real jobs: 8 for training, 4 for inference). A B200 finishes a batch far faster than an older card, so a loader that barely kept up elsewhere will starve it. `--mem` is CPU RAM (typically 8 to 32 GB for training; real jobs used 16G to 64G), **not GPU memory**.
- **Always pass `--account=<account>`.** Ask the researcher for the string (the one real account seen looked like `p<year>_<number>_<institution>`; the documentation's example is `proj1_mit`; ask); list accounts with `sacctmgr show user $USER withassoc format=user,account -p`. The documentation's templates omit it and say nothing about whether that is safe; every real completed job set it. Add it to CPU jobs too.
- **Sizes fit a node.** A node has 8 GPUs, 128 CPUs and about 2.25 TB RAM; as a starting point per GPU use 8 CPUs and 32 GB (4 GPUs: 32 CPUs and 128 GB) **(inferred from the official examples)**, then right-size from `sacct`. **Total CPUs = ntasks x cpus-per-task**: the official 4-GPU job is 1 task x 32 CPUs; the workshop's is 4 tasks x 8. Never 4 tasks x 32, which asks for a whole node. A request larger than one node never schedules.
- **Multi-GPU:** single node only (`--nodes=1`). The official 4-GPU template uses `--gpus-per-node=4 --cpus-per-task=32 --mem=128G` with no `--ntasks-per-node`, and one `torchrun --nproc_per_node=4 train.py` call; the workshop uses `--ntasks-per-node=4 --cpus-per-task=8`. Either way `--nproc_per_node` equals the GPU count, `torchrun` is launched once from the batch script, and you do not wrap it in `srun` with more than one task (inferred: it would start N x N processes). **Do not write multi-node jobs from these documents**: only a single-node recipe exists; multi-node needs the right rendezvous setup and the researcher's go-ahead. Do not ask for `b200-fullnode` or `preemptable`.
- **The `cpu` partition** is for small support work tied to GPU jobs: preprocessing before GPU training, post-processing, orchestration. It is not for CPU workloads; send those to Explorer.
- **Arrays (house rule):** throttle with `%N` (`--array=0-99%10`). Output names: `%x` job name, `%j` job ID, `%a` array task, `%A` array job. Chain jobs with `--dependency=afterok:<jobid>`; mail with `--mail-type=END,FAIL` (and the researcher's `--mail-user`).
- **Check capacity first:** `sinfo -O Partition,Nodes,CPUs,Memory,Gres -e`. Node states: `idle` free, `mix` partly free, `alloc` full, `resv` reserved, `drain`/`drng`/`down` unavailable, `plnd` planned for a higher-priority job.
- **Interactive session (for a human at a terminal):** `salloc --partition=rtx-devel --gpus=1 --cpus-per-task=4 --mem=16G --time=01:00:00` (the prompt then shows the compute node; `exit` ends it), or `srun -p rtx-devel -N 1 -n 1 -c 8 --mem=16G --gpus=1 --time=01:00:00 --pty bash`. Always set `--time`. Test on devel first: it has shorter queues. Cancel the moment you finish. **As an agent you cannot hold an interactive session:** run a one-shot `ssh -o BatchMode=yes aicr 'srun -p rtx-devel --gpus=1 --cpus-per-task=4 --mem=16G --time=00:15:00 <command>'` or a short `sbatch` to a `*-devel` partition (ordinary Slurm; no source ran this form, so treat it as unverified).

## 5. The workflow, and a template

**The path:** develop and test small on Explorer or locally; open a `*-devel` session; run a GPU check; run your code for 50 to 100 steps; profile; fix the bottleneck; re-profile and confirm utilisation **over 70%**; only then submit a tuned `*-batch` job; afterwards `jobstats <jobid>`. Make the first run a tiny version that tests the function, then scale.

**Preflight order inside every job script** (print context; GPU visible; required files exist; no competing job; enough free disk; then the expensive command). **Fail the job yourself if CUDA is missing.**

**A minimal template built from flags real completed jobs used, plus `--nodes` and `--ntasks` from the workshop template.** Replace every `<...>`:

```bash
#!/bin/bash
#SBATCH --job-name=<name>                     # stable and unique: guards that look for competing jobs match on it
#SBATCH --account=<ACCOUNT>                   # ask the researcher; every real completed job set it
#SBATCH --partition=rtx-batch                 # the partition decides the GPU; use *-devel while testing
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus=1                              # one GPU; more only if the code is DDP and one GPU is already over 80% utilised
#SBATCH --cpus-per-task=8                     # = DataLoader num_workers + 1; never below 4
#SBATCH --mem=32G                             # CPU RAM, not GPU memory
#SBATCH --time=04:00:00                       # measured runtime + about 20% (sacct Elapsed of an earlier run)
#SBATCH --output=<ABS_WORK>/logs/%x-%j.out    # absolute path; mkdir -p that directory BEFORE sbatch

set -euo pipefail                             # stop at the first error, unset variable or failed pipe

WORK=${WORK:-<ABS_WORK>}                      # one persistent project root (under /work), overridable at submit time
export PATH=$HOME/.conda/envs/<env>/bin:$PATH # PATH prepend, NOT 'source activate' (Section 10)
export HF_HOME=$WORK/hf_cache                 # persistent Hugging Face cache; drop this line if no HF models are used

echo "job $SLURM_JOB_ID on $(hostname) at $(date)"
nvidia-smi -L                                  # proves a GPU is visible and names it
echo "python: $(which python)"                 # must point into the environment
python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)"   # hard-fail if CUDA is invisible
python -c "import torch; x=torch.randn(1000,1000,device='cuda'); print((x@x).sum().item())"   # run a real kernel: a wheel without Blackwell support can pass the check above and fail here (general PyTorch knowledge)

[ -f "$WORK/data/<input>" ] || { echo "ABORT: input missing"; exit 1; }
MIN_FREE_GB=${MIN_FREE_GB:-50}                # set from (steps / save interval) x checkpoint size; df may show the whole export, not your quota (Section 8)
FREE_GB=$(df -BG --output=avail "$WORK" 2>/dev/null | tail -1 | tr -dc '0-9')
if [ -n "$FREE_GB" ] && [ "$FREE_GB" -lt "$MIN_FREE_GB" ]; then echo "ABORT: only ${FREE_GB} GB free"; exit 1; fi   # for checkpoint-heavy runs

cd "$WORK"
python -u train.py --data-dir "$WORK/data" --bf16   # -u so tail -f shows progress; adapt the flags to the researcher's script

echo "done: $(date)"
```

The documentation's templates additionally load modules (`module purge; module load cuda/13.1; module load miniforge3/25.3.0-3`). On 2026-10-02 `module load cuda/13.1` resolved to `cuda/13.1.1` and `miniforge3/25.3.0-3` existed; later real scripts loaded no module and used only the `PATH` line. Without the CUDA module `torch.cuda.is_available()` may return False with no error: whichever you choose, the hard-fail line proves it.

**Submit like this** (from the researcher's computer; drop the `ssh aicr` wrapper if already on the login node): `ssh aicr "mkdir -p <ABS_WORK>/logs"`; `rsync -avn SBATCH/ aicr:<ABS_WORK>/SBATCH/` as a dry run, then without `-n` with the researcher's yes (the Work directory is shared; do not assume the cluster copy matches the fixed local one); `ssh aicr "cd <ABS_WORK> && sbatch SBATCH/<job>.sbatch"`; capture the job ID and record it in the project's run log **before closing the terminal**; `ssh aicr "squeue -u <user>"`. Cancel only a job you have confirmed is still PENDING and unstarted, and only with a yes.

**Do not copy these from the Northeastern introduction and workshop templates:** `source activate myenv`; a comment after a line-continuation backslash (`python train.py \   # CHANGE` ends the command at the backslash-space and then runs `--data-dir` as a command); `mkdir -p logs` inside the script (Slurm opens the output file first; create the directory before `sbatch`); the placeholder `ACCOUNT_NAME` (the official pages' examples; their CPU example also omits `--account`).

## 6. Measuring on AICR

- **Verify the GPU at the top of every job** (`HPC.md` Section 6): device name, memory, count, a tensor round trip, `nvidia-smi`. A job that "worked" may have run on CPU with no error. Do not set or override `CUDA_VISIBLE_DEVICES` (`NOT SET` is normal in a plain `srun` shell). Stale values can be left in your shell from a previous job.
- **Confirm utilisation above 0% early in the job.** A job holding a GPU without running kernels will be cancelled automatically.
- **Live:** a human can keep `watch -n 1 nvidia-smi` in a second terminal and use `nvitop` for per-process proof; **an agent must not** (they never exit). For an agent, take one bounded sample: while the job runs, `squeue -u $USER` for the node, then `ssh -o BatchMode=yes aicr 'ssh NODE_NAME nvidia-smi'` (documented; works only while you have an active job there), or log inside the job and read `jobstats <jobid>` afterwards. `nvitop` and `nsys` are not on the login-node `PATH`; whether they exist in modules is unconfirmed.
- **After every batch job: `jobstats <jobid>`** (also in OnDemand: Jobs, then Job Composer or Active Jobs, select the job). It is installed at `/usr/bin/jobstats` and exists **only on AICR, not on Explorer**. On a real finished job it printed: Job ID, user and account, name, state, nodes, CPU cores, CPU memory, GPUs, QOS and partition, start time, run time, time limit; bars for CPU utilisation, CPU memory usage, GPU utilisation and GPU memory usage; per-node GPU figures; and notes such as "only needed 11% of the requested time". Real example (one RTX PRO 6000, 8 cores, 64 GB, 8 h limit, 55 minutes run): CPU utilisation 13%, CPU memory 25%, **GPU utilisation 80%**, GPU memory 17%.
- **Targets (state which you used):** GPU utilisation over 70% (below 60% means fix before the next run; below 50% means a problem, check the data pipeline first, `num_workers=0` is the usual cause); GPU memory 60% to 90% (below 40% means raise the batch); CPU efficiency over 60%; CPU-RAM efficiency not below about 40% (lower `--mem` if it is). Scale to more GPUs only above 80% on one. The documentation's prose and its script disagree on some cut-offs; the reading above is the safe one.
- **A B200 under about 40% utilisation usually means the workload is too small:** raise batch size, resolution and model width and switch to BF16 before concluding the GPU is slow. Do not celebrate that "the code runs fine" on a mostly idle B200.
- **After the job:** `sacct -j <jobid> --format=JobID,JobName%18,Partition,Elapsed,MaxRSS,State,ExitCode`. `COMPLETED` with ExitCode 0 is success; `TIMEOUT` means the time limit was too short or the code stalled; `FAILED` means read the log first. Compare `MaxRSS` with `--mem` and lower `--mem` if it is far under (documented to improve fairshare). Recent history: `sacct -u $USER --starttime=now-7days --format=JobID,JobName,Partition,Elapsed,State,ExitCode`.
- **Check live state before reporting.** Never trust a handoff note: one said a job was PENDING when it had FAILED and a different job was the live one. `squeue -u $USER` and `sacct` first.
- **Profile a short window only** (10 to 50 steps; Nsight Systems 50 to 100 steps or `--duration`). Send trace files to `/scratch/$USER`, then copy to a laptop to open.
- **Sample from inside the job** when you need evidence that a job is not idle: NVML (`pip install nvidia-ml-py`, `pynvml.nvmlDeviceGetUtilizationRates(handle).gpu`) from a background thread.

## 7. Speeding up on AICR (what differs from `HPC.md` Section 6)

- **BF16 is the default precision here (workshop).** Wrap the forward pass and loss in `torch.amp.autocast(device_type='cuda', dtype=torch.bfloat16)`, leave `loss.backward()` outside, and do **not** add a `GradScaler`. Prefer BF16 over FP16 on these Blackwell GPUs **(workshop)**: FP16 needs a `GradScaler` and the workshop sees no upside; use FP16 only if the model requires it. Use FP32 only to debug or as a baseline. **Do not start with FP8**: it needs scaling and calibration, can hurt accuracy, and the documentation says to contact the research computing team. Do not cast the whole model to BF16 by hand.
- **Out-of-memory order on AICR:** BF16 first, then gradient checkpointing, then reduce the batch last. (Explorer's material gives the reverse order; do not mix them.)
- **Loader first.** Utilisation under about 60% almost always points to the data pipeline. Change `num_workers=0` to 4 or more: the workshop says this often takes utilisation from 20% to 60% or 80% with no other change (an illustration from a simulated benchmark, not measured). Set all four: `num_workers = cpus-per-task - 1`, `pin_memory=True`, `persistent_workers=True`, `prefetch_factor=2` (raise only if still slow).
- **Batch size.** Search for the largest that fits, then run production at 70% to 85% of it. If memory shows 15% to 20%, there is room for 4 to 8 times the batch. The search runs forward and backward only, so the true maximum is lower: keep the margin.
- **Files.** Do not train from millions of small files on scratch; pack into HDF5, WebDataset or LMDB. Copy data to node-local `$TMPDIR` at job start only if it exists, with a fallback to the scratch path, and remember the copy counts as held-GPU time.
- **Models over one GPU's memory** and multi-node training are not covered by the sources; point to the research computing team.
- **LLM inference:** `rtx-*` for smaller models, `b200-*` for 70B and up; vLLM is the usual high-throughput tool but is covered in a workshop not in these sources.
- **Honest limits.** "BF16 2 to 4 times faster" and "60% to 70% less activation memory for 30% more compute" are the workshop's claims, not measured in any real job here. A figure that an idle B200 is "2.5 times more expensive to waste than an A100" has no basis given in the workshop: do not repeat it.

## 8. Storage and the data lifecycle

- **Home** for code, scripts and environments (private, snapshots, never purged). Mind the 100 GiB with big caches (model weights, pip and conda caches).
- **Scratch** only for temporary data of running jobs. Move important outputs to Work before they age out and set a reminder after every long job. Do not `touch` or re-copy files to dodge the purge **(house rule)** (the sources do not say whether the purge keys on modification or access time).
- **Work** for the bulk of project data, shared with the team: never `rm`, `mv -f` or overwrite there without asking **(inferred)**, and clear it at the end of the project. Stage in this order **(inferred)**: master dataset in Work; job input and output on Scratch during a run; results back to Work (or off AICR) before 30 days.
- **Environments in Home, never Scratch.** A conda environment on Scratch is purged **(inferred from the purge rule)**. Source trees and prepared datasets on Scratch are exposed to the same purge.
- **How to restore a snapshot is not documented.** If something was deleted by mistake, tell the researcher at once: Home and Work recover within 7 days, Scratch never.
- **Back up outside AICR.** Keep the originals of irreplaceable data on a machine the researcher controls and treat the cluster copy as a working copy; download results and important work to a Northeastern resource regularly during the project, not only at the end.
- **Compute disk use before a heavy run.** `(total steps / save interval) x size per checkpoint` against free space under Work (`df -h <work path>`, which may show the whole export rather than your quota: ask the PI for the quota); abort below a threshold. **Never leave checkpoint retention at its default** (some trainers keep every save): in one real run each checkpoint was 5.1 GB and a keep-all run left 41 of them, about 209 GB. Use `df` for free space but not for quota.
- **Make long jobs resumable.** Checkpoint training; make sweeps and evaluations skip outputs that exist and flush their manifest after each unit so a resubmission picks up where it stopped. Copy a known-good checkpoint to a separate `*_KEEP` directory before extending or pruning. Do not delete checkpoints unless told.
- **Project end.** There is a yearly check-in; the PI renews. When the project is complete, move the data from AICR back to an appropriate Northeastern resource. Before deleting anything on AICR, verify the copy is complete **(house rule)**: a checksum dry run in the direction that fills the destination, for example `rsync -avnc aicr:<dir>/ <local-dir>/`, where empty output means nothing is missing or different (default `rsync` compares only size and time, and a dry run toward AICR proves nothing about files missing locally), then get the researcher's explicit yes. The sources do not say what happens to data if a project is not renewed: ask the PI for the end-of-project plan.

## 9. Transfers

- **By size:** the OnDemand File Browser for everyday small transfers; Globus for large files or many files; `scp`/`rsync` from the command line if the researcher prefers. Never a long transfer through a login node when Globus is available.
- **Run `scp` and `rsync` from the researcher's computer**, with the AICR host in the command (`scp <local> USERNAME@login.aicr.ai:<aicr-path>`). Run `pwd` on the cluster first for the exact path (case-sensitive). Use `rsync -n` (dry run) before anything that could overwrite, and `--partial` for big files. `git clone` straight into Home is allowed. GUI clients (Cyberduck, FileZilla, WinSCP) use host `login.aicr.ai`.
- **Duo and transfers.** The transfer documentation says `scp` and `rsync` to the login nodes need Duo and that you may get a push with no sign on the command line; the SSH page says the certificate is the whole credential and the verified BatchMode `ssh` login showed no Duo. Whether Duo applies to transfers is unconfirmed: in real use `rsync` over the `aicr` alias ran with no prompt, so treat Duo as a possibility rather than a certainty: if a transfer hangs or prompts, stop and ask the researcher to approve a Duo push; do not run a long transfer in BatchMode and expect it to finish unattended.
- **Globus status is unclear.** The transfer page says "the AICR Globus collection is not yet set up" (the collection is named "AICR Collection"); the Northeastern introduction calls Globus the primary route. Ask whether it is live before building a plan on it.
- **Between AICR and another cluster:** log in to one and start the copy from there; this needs credentials on the second cluster. **Do not copy the AICR private key.** Agent forwarding might work (the certificate permits it) but no source says to use it and it has its own risk: needs a human decision.

## 10. Environments and software on AICR

- **Use environment modules** (`module avail`, `module load`). There is a common core set plus institution-specific modules that may be hidden by default. If software is missing: search `module avail`, then try installing in Home, and email support **before** spending a lot of time (they may have it). No source documents a container runtime, conda channel policy or pip policy here: do not claim one exists.
- **GPU jobs** use `cuda`; Python jobs use `miniforge3` (the documented module lines are `module purge`, `module load cuda/13.1`, `module load miniforge3/25.3.0-3`; re-check with `module avail`). Create the environment **once, before submitting**, never inside an `sbatch`: on the login node within its 4-core, 8 GB cap (the SSH page lists installing packages and managing environments as allowed there), or as a one-shot `ssh -o BatchMode=yes aicr 'srun -p cpu --cpus-per-task=4 --mem=8G --time=00:30:00 <command>'` (unverified). The workshop says to run its setup script on a devel node, which holds a GPU while installing: avoid that. The workshop recipe is non-interactive-safe: `conda create -y -n <env> python=3.11`, then `conda run -n <env> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128`, then `conda run -n <env> pip install nvitop tensorboard matplotlib numpy`. It loads `cuda/13.1` but installs a `cu128` wheel and never explains why: verify the GPU is visible after install.
- **Never `source activate` or `conda activate` in `sbatch` or non-interactive `ssh`.** One real job (rtx-batch, 8 hours requested) died using `source activate`, and the cause was never verified: conda has no shell hooks in non-interactive shells and `conda activate` needs them, yet `source activate` completed in earlier jobs. **Prepend the environment's `bin/` to `PATH`** (`export PATH=$HOME/.conda/envs/<env>/bin:$PATH`) or call the interpreter by absolute path in `ssh aicr "..."` one-liners. The `PATH` form works under either failure mode. It skips conda's `activate.d` scripts (general conda knowledge, not in the sources), so it suits pip wheels and plain Python but not conda packages that set variables on activation (a CUDA toolkit, compilers, R): for those, set the variables explicitly. Echo `which python` in the job log. `HPC.md` Section 8's Explorer setup (the `miniconda3` module, the `defaults` channel, Apptainer) does not carry over: on AICR use `miniforge3`, and do not claim a container runtime.
- **Import-test every package the job needs** with the job's own interpreter before a long job (a devel session, or a preflight at the top of the `sbatch`). A missing logger or helper kills the job at startup after you waited in the queue (a real fine-tune failed for a missing `tensorboard`).
- **Set the Hugging Face cache** (`HF_HOME`) to a persistent project directory, or it re-downloads or fills Home.
- **Python 3.10 or newer** for the workshop scripts (`X | None` type hints). Check the version rather than assuming.
- **Probe optional packages** and print which path will run instead of failing late (`python -c "import <pkg>" 2>/dev/null && echo ok || echo missing`).

## 11. Lessons from real AICR runs

Each is a rule that would have prevented something that happened in real AICR jobs in early August 2026 (a text-to-speech model fine-tuning project). Details are generalised.

1. **Prove the weights loaded.** A checkpoint load that raises no error can still leave random weights: two inference jobs produced silent output because the command-line loader was handed a nested training checkpoint. After loading any checkpoint, hash a live parameter; if the files differ but the loaded values are identical, discard the sweep. Load fine-tuned checkpoints through the library's own API, not a command-line flag that assumes a different format.
2. **Gate every input numerically before the GPU job, and build assets off the cluster.** A silent audio reference clip (peak amplitude 4 of 32767) produced silent output with no error anywhere. Check with a number (peak and level), on the researcher's own machine, then copy. Do not convert files on the cluster with a step that can fail silently, and never paraphrase an exact transcript that accompanies an input.
3. **Same path, new contents: a node cache serves the old file.** Preprocessed inputs were cached by file path in `/tmp` on the compute node, so a replaced file kept serving the stale one. Give a replaced input a new filename (a content hash) or a job-scoped directory.
4. **Measure with the language, not a wrapper tool, when the tool is flaky.** On some nodes `ffmpeg volumedetect` returned no value for float WAVs, so every item was falsely reported silent; computing the level in numpy was reliable.
5. **After fixing a bug, grep the whole tree for the same construct** (`grep -rn "source activate\|conda activate" <dir>`). The activation fix was made in one script while the same line was live in its siblings and in a ship script.
6. **An ssh failure is probably an empty agent, not an expired certificate.** Check `ssh-add -l` first. On macOS with Keychain a cold-agent test exists, but it empties **every** key: only the researcher runs it, deliberately (Section 1).
7. **Point output at the real directory and print where it goes.** A shared output symlink still aimed at an earlier run would have put hours of checkpoints in another run's directory; the script had also created a decoy directory the tool never wrote to. Retarget the symlink inside the job, print `readlink`, and print the real output directory at the end.
8. **Do not run two jobs that share mutable state** (one symlink, one output directory, one cache). Have the `sbatch` refuse to start while another job of the family is queued or running (`squeue -u <user> --noheader -o "%i %j" | grep ...`). Job names are load-bearing for such guards: renaming a job silently disables the guard.
9. **Compute checkpoint disk use before the run and set retention** (Section 8): in one run each checkpoint was 5.1 GB and a keep-all setting left 41 of them, about 209 GB. Reconcile every step, epoch and time estimate with the flags that actually ran and with `sacct`: one budget assumed a batch size of 8192 when the script used 3200 and overstated its claim almost threefold; step estimates for one run were 24k, 13.5k and 20,400. Do not carry estimates from a handoff.
10. **Set epochs consciously.** Do not accept a default of 100 on a small corpus: extra epochs past a point bought memorisation, and quality peaked early (about 12 epochs) and then degraded. Hold out about 10% of the data so the run produces a validation curve with a minimum; without it "which checkpoint" became a listening problem. Choose comparison checkpoints by explicit step, not by fraction of the run, and send each pass to its own output directory.
11. **Do not fill a long allocation with more training once the model has converged.** An 8-hour request at that batch size would have been about 43 times the calibration point. Spend spare time on a resumable evaluation sweep instead.
12. **Check that a metric can tell known-different things apart** before trusting it: a word-error rate of 0.000 on all 41 checkpoints and a spectral distance at the corpus's own internal spread carried no information, while listening found a steady worsening both missed. Make compared conditions differ only in the variable you test, and measure a within-condition noise floor.
13. **Count inputs against the expected number before submitting.** A corpus of 157 clips was blamed on "unsplittable long clips"; the real cause was that files 121 to 154 were never processed. Assert file count equals metadata rows equals the expected number, on the cluster side, and abort on mismatch.
14. **Preflight all inputs and abort with `exit 1` before the expensive command:** dataset, base weights, reference file, resume checkpoint. A missing input must not become a silent cold start; a resume that cannot find its checkpoint must not cold-start.
15. **When output is wrong, run a cheap devel diagnostic that bisects the stages** (base versus fine-tuned, input versus weights; a 20-minute `rtx-devel` job) before resubmitting the expensive job. Try the 30-minute devel experiment before committing another 8 GPU-hours.
16. **Do not delete to re-run.** The source script wiped old outputs with a wildcard `rm` inside the `sbatch`. List what will go and get a yes; better, send each run to a new job-scoped output directory. Do CPU-only preparation (resampling, splitting, QC, speech recognition) on the researcher's computer, not on a GPU allocation.
17. **Copy results off volatile paths immediately.** A pulled result under macOS `/tmp` is purged; move it to a permanent folder right after `rsync`.
18. **Treat machine-generated labels as unverified.** A wrong transcript teaches a wrong mapping with no error anywhere; report flagged items for a human to check before training.
19. **Pre-check ssh so a prompt cannot hang the agent:** `ssh -o BatchMode=yes -o ConnectTimeout=10 aicr 'echo ssh-ok'` before a multi-step remote sequence. When piping through `tee`, read the training command's own exit status (`${PIPESTATUS[0]}`), not `tee`'s.
20. **Keep a run ledger.** One row per job (ID, partition, GPU, walltime, status, cause of failure); let the ledger beat every other document, mark superseded numbers wrong in place, and write each new job ID into it before closing the terminal. A runbook that still described known-wrong steps would have landed the next session back on the failed job.

## 12. Questions before submitting an AICR GPU job

Ask the `HPC.md` Section 2 questions once (access, permission, data, what and why, address, agent access). Do not ask them again here. Add only these, and only if the project's files and a short test cannot answer them:

**Must ask (only the researcher can answer):**

1. What is your **AICR username** and **Slurm account**, and what is the persistent project path under `/work/<institution>/<project>`?
2. **Is any of the data non-anonymised, under a data-use agreement, or security-restricted?** If yes, stop and ask your institution before it goes on AICR.
3. Do you want me to submit the job myself (this spends allocation) or hand you the exact `sbatch` command? Can this session reach `login.aicr.ai`?
4. What counts as success, and what quick check will show the job used the inputs and the GPU?
5. Is another job of yours running or queued that writes to the same directories, symlinks or caches?
6. Where should results live after the 30-day scratch purge, and where is the off-cluster copy of the originals? Will this be published (so the acknowledgment is added)?

**Read or measure instead of asking** (a non-expert cannot be expected to know):

- Whether it ran correctly on a tiny sample: read the logs, or run one on a `*-devel` partition.
- Model size and whether it fits 96 GB: compute it, or read the memory from a short run.
- GPUs needed and whether the code is DDP: read the code; check utilisation on one GPU first.
- Runtime, steps and epochs: time 50 to 100 steps, scale, add 20%.
- Checkpoint size and free space: write one and `ls -l`; compute the Section 8 formula.
- Environment and imports: run an import test in a devel session.
- BF16 suitability, epochs, validation split, cold start versus resume: propose the safe default (BF16, a held-out 10%, a stated resume checkpoint) and ask only for a veto.

## 13. Acknowledgment, acceptable use, and help

- **Acknowledge AICR in any publication that uses AICR results.** Use the sentence exactly as given on AICR's Acknowledging page; it begins "The authors acknowledge the MGHPCC AI Computing Resource (AICR), with support from the Commonwealth of Massachusetts and the AICR participating institutions". Copy the full text from that page; home institutions may add wording but must keep the sentence.
- **Acceptable use:** research associated with the participating institutions and MGHPCC-supported projects; datasets obtained legitimately; nothing that could be construed as illegal; do not share accounts; respect other people's activity and privacy; comply at once with support-staff requests; obey the home institution's policies as well. If unsure whether a use is allowed, send the researcher to their institution's support; do not decide for them.
- **Help:** the researcher's home institution (Northeastern: rchelp@northeastern.edu; office hours and consultations at `https://rc.northeastern.edu/getting-help/`; docs at `https://rc-docs.northeastern.edu/en/latest/index.html`). Send FP8, large-model sizing and anything the documents do not settle there. When you report back, follow `HPC.md` Section 13.

---

# Appendix A: Conflicts and unverified items (the honest list)

The file above takes the safe reading. Do not harden any of these into a rule without checking.

1. **GPU request syntax:** the official pages use `--gpus=N`; the introduction and some real scripts use `--gres=gpu:N`. Both worked in completed jobs; whether the type form (`--gres=gpu:b200:1`) is accepted is untested.
2. **Partition list and counts:** five partitions in the documentation; live `sinfo` (2026-10-02) showed `b200-fullnode` (4 nodes) and `preemptable` (46 nodes), and counts differed (`b200-batch` showed 25 nodes live, with 4 more in `b200-fullnode`, against 28 in the documentation's sample output). Their semantics are undocumented. Trust `sinfo`.
3. **Partition limits in project notes:** one project note lists `rtx-devel` at 30 minutes and `rtx-batch` at 8 hours; every real script requests exactly those and ran. Read as habitual request sizes, not caps. The cap is 4 h and 24 h unless `sinfo` says otherwise.
4. **CPU cores per GPU node:** 128 (system page, `sinfo`) versus "64 cores" (introduction slides). Possibly 64 physical, 128 threads: not stated.
5. **B200 memory:** 180 GB (system page, a narration check) versus 192 GB (workshop, a script, an `nvidia-smi` sample). Read it from the device.
6. **Job limits and QOS:** none found. Documented limits are the devel cap of 4 concurrent jobs and OnDemand's 4 sessions (4 hours). The introduction also puts a 4-job limit on `cpu`; the system page says only devel.
7. **Globus:** "not yet set up" (transfer page) versus "the primary method" (introduction). Unknown which is current.
8. **Duo on transfers:** transfer page says needed; SSH page and the verified login show none. Unknown scope.
9. **Certificate lifetime:** "short-lived" in the docs; one real certificate was `Valid: forever`. Check `ssh-keygen -L`.
10. **Work path:** `/work/<institution>/<groupname>/` versus `/work/INSTITUTION/PROJECT` versus `/work/neu/$PROJECT`. `ls /work/neu`.
11. **Scratch purge:** "older than 30 days" is documented; modification or access time, and any warning, are not. The system page says only "Regular".
12. **Idle-GPU cancellation:** only in the introduction and the workshop; no threshold, window, warning or appeal path.
13. **`source activate`:** the Northeastern introduction and the GPU workshop templates use it (the AICR documentation pages do not); one real job died on it while earlier jobs using it completed. The `PATH` form works under either; the cause (module in use, `conda` versus `miniforge3`) is unverified.
14. **CUDA module version:** `cuda/13.1` almost everywhere, `cuda/13.1.1` in one workshop step; `module load cuda/13.1` resolves to `13.1.1` on 2026-10-02.
15. **The workshop commented out its storage section** and the storage rows of its decision guide; some scripts still print that advice. Treat the commented text as unverified.
16. **Utilisation thresholds** (50, 60, 70, 80%) and the memory targets (60 to 90%, 70 to 90%) differ by section; the `jobstats` simulation script's cut-offs differ from its prose.
17. **Out-of-memory order:** AICR's material says BF16, then checkpointing, then batch; Explorer's says the reverse.
18. **`jobstats`:** the introduction says it "will also be deployed"; it is installed (`/usr/bin/jobstats`) and ran on a real job. The workshop's `07_jobstats_guide.py` is a **simulated** report; real field names beyond the one real output shown above are unverified.
19. **Scripts with known faults:** `01_gpu_verify.py` exits 0 when CUDA is missing; a mixed-precision demo times FP32 and BF16 back to back with no warm-up; an `ssh` config in an older note uses `AddKeysToKeychain`, which could not be verified as a valid keyword (use the block in Section 3).
20. **Not covered at all:** how to restore a snapshot; the installed software list, containers, conda and pip policy; the Getting Help and Recipes pages; a quota command; node-local scratch and its size; internet access from compute nodes; checkpoint and restart guidance; preemption behaviour; multi-node recipes; maximum array size; whether `--mail-type` needs `--mail-user`; whether `tmux` survives on login nodes; what happens to data when a project is not renewed.
21. **Automated agent access:** no AICR page read mentions it either way. Stay read-only by default and have the researcher confirm with their institution before unattended or high-volume agent use.
22. **Where to create the environment:** the workshop says a devel node (holds a GPU while installing); an earlier project's notes say the login node; the SSH page lists environment management as allowed on login nodes (4 cores, 8 GB). Section 10 says login node within the cap, or a one-shot `cpu` job.
23. **Profile-window sizes** (10, 10 to 20, 20, 20 to 50, 50 to 100 steps) and **Python versions** (3.10 and 3.11) differ across the sources; none is harmful.
24. **`--account`:** this file says always pass it; the documentation says to specify it when you have more than one project, and omits it from its CPU example. Whether omitting it works is not stated.
25. **Dates:** documentation pages May 1 to July 10, 2026; AICR is for "initial alpha and beta-test users". Re-verify.

# Appendix B: Where each part comes from

Local copies of the AICR documentation pages (Overview, AICR System, Getting Started, SSH, OnDemand, Slurm Basics, GPU Jobs, CPU Jobs, Monitoring, Transferring data, Acceptable Use, Acknowledging AICR); `AICR-Introduction-2026/aicr-introduction.md`; the GPU workshop `AICR-Optimizing-GPU-Usage/` (document, scripts, setup script); the setup guide, run log (job IDs, errors, fixes) and sbatch scripts of a private model-training project that ran on AICR; the verified live records `Logging-into-AICR-with-Claude/SESSION.md` and the AICR film session logs under `youtube/`. The rule-by-rule evidence, with file and line for every rule, is kept in `skills/evidence/` in the author's working copy (it cites a private project, so it is not published).

# HPC.md: Rules for any agent helping a researcher use a shared HPC cluster

**What this is.** One file you point an agent at ("read `HPC.md` before touching the cluster") so it behaves the way an experienced research-computing engineer would when it works on a shared cluster for a researcher who is not an expert in parallel computing. It is written for Northeastern University's **Explorer** cluster and for shared Slurm clusters in general. The AICR GPU cluster has its own file, `AICR.md`, which builds on this one.

**Why it exists.** Most cluster trouble is not hard computer science. It is a request that is too big, a job that quietly runs on the wrong thing, work done on a login node, data left on a disk that gets wiped, or a command run on a shared system without looking first. An agent is good at the careful, checkable parts and is far more likely than a busy researcher to do them every time. These rules tell it what to do, what never to do, and what to ask the researcher first.

**What we found while writing it** (from about 700 rule candidates read out of Northeastern Research Computing's own training material, the AICR documentation, and real incidents, 2026-10-11):

1. The common mistakes are few and repeat: asking for several GPUs or nodes for code that uses one, leaving the data loader at its default so the GPU starves, scaling up before one GPU is busy, treating `--mem` as GPU memory, and never checking which GPU the job really got.
2. The training material contradicts itself in places that matter to an agent (scratch quota, who may add guests to a project, utilisation thresholds, which Python setup to use). This file picks the safe reading and lists every conflict in **Appendix A**.
3. Some slide examples are wrong as written (a `--m`/`--n` short form, a partition called `compute`, a backslash followed by a comment). **Section 12** lists them so an agent does not copy them.
4. Nothing in any source says whether Research Computing permits automated agent access. This file treats that as an open question (Section 10).

**What is NOT verified.** Nothing here was run on a cluster except the login test in `Logging-into-Explorer-with-Claude/SESSION.md` (`whoami`, `hostname`, `pwd`, `squeue`, and an empty-agent test, all read-only). On 2026-10-11 we also ran read-only `sinfo`, `module avail` and command-presence checks on both login nodes (recorded in the repository's guides). Partition limits and storage numbers come from public pages read through a summariser on 2026-10-11 and from training slides dated Spring and Summer 2026. Re-check any number before treating it as a hard limit. Rules marked **(house rule)** are this file's own judgement, not Research Computing policy; rules marked **(inferred)** are drawn from the sources but not stated by them. Unmarked rules come from the sources; `skills/evidence/` (the author's working copy) gives every rule's source and label.

**How to use it.** Put one line in the researcher's `CLAUDE.md` or `AGENTS.md`, not this whole file:

> When a task involves a research computing cluster (Explorer, Slurm, `sbatch`, `srun`, GPUs on a cluster, HPC), read `HPC.md` completely first and follow it. For the AICR cluster also read `AICR.md`.

**Precedence.** If you also read `AICR.md` and the two differ, `AICR.md` wins on the AICR cluster. The Explorer-specific parts of this file do not apply there: the Explorer commands and hosts in Sections 2 and 3, `srun` defaults and partitions in Sections 3 and 5, `/projects` and the `project` command in Section 7, and the module, conda, `source activate` and `--gres` type lines in Sections 6 and 8.

Give the path to wherever the file lives. Explorer is Northeastern's cluster; for another university's cluster, the principles hold but every host name, partition, quota and policy must be re-checked.

---

# Agent rules (everything below is for the agent)

## 0. Prime directive

- You are the careful pair of hands. **Pipeline work is yours:** inspect, measure, size, write scripts, check results, keep records. **Judgment is the researcher's:** what the science needs, what to spend, who gets access, and anything that cannot be undone.
- **Look before you act.** Start with read-only commands. **Measure before you change.** Profile before you parallelise.
- **Ask before you spend, delete, or change who can see data.** Say the exact command and what it costs, then wait for a yes in chat.
- **Explain in plain words.** Before any submission, tell the researcher what you are asking the cluster for, why, and what a wrong guess costs. Define a term (node, core, GPU, partition) only the first time, in one sentence.
- **Never state a limit, quota or policy you did not read here or verify live.** Say "I haven't confirmed this; ask Research Computing (rchelp@northeastern.edu)". When this file and the live cluster disagree about what exists, trust the live cluster (`sinfo`, `module avail`); for policy, trust Research Computing's current pages and tell the researcher about the difference.
- **Treat every claim about a job as a hypothesis until a measurement confirms it.** A job that finished is not a job that did what you intended. A script that "worked" may have run on CPU.

## 1. Hard NEVERs (check this list before every command)

| Never | Because |
|---|---|
| Run computation on a login node: training, preprocessing, `make -j`, `conda` solves, `spack install`, container pulls, `wget` of big files, model servers, large `scp`/`rsync`. On AICR the OnDemand browser shell is a login node with the same caps; treat Explorer's the same unless Research Computing says otherwise (not confirmed). | Login nodes are shared. Work found there is terminated, bots email Research Computing and the user, and everyone's session slows. Get a compute node first (Section 5). |
| `sudo`, `apt install`, `yum install`, Docker | No root on a shared system. Use modules, conda, Apptainer, or a source build in your own space (Section 8). |
| Ask for, type, read, print, store, log, upload or commit a password, passphrase, Duo code, or private key | The agent must never hold a credential. If a command asks for one, stop and ask the researcher to unlock it in their own terminal (Section 10). |
| Run `ssh` from an agent without `-o BatchMode=yes` | Without it a missing passphrase or host-key question hangs the session forever. |
| Delete, move over, or overwrite files without first listing exactly what will go and getting a yes. Never `rm -rf` a path built from a variable, a wildcard or `..`. Never `chmod 777` or `chown -R` shared data **(inferred from the shared-data design)**. | There is no trash. Recovery is limited or absent (Section 7). |
| Add, remove or change members, delegates or guests of a project, or run any `project ... add/remove/update` command, unless the researcher named who and what | It changes who can read and overwrite shared research data. |
| **Submit:** `sbatch`, `salloc`, a long `srun`, or a resubmit, until the researcher has confirmed partition, time, memory, CPUs, GPU count, account and what the script does | Jobs spend shared resources and fairshare. |
| **Cancel:** `scancel` without a yes that names the job ID(s). Never `scancel -u $USER` | A cancel can lose hours of work, including jobs this session did not start. |
| Hold a GPU you are not using, or run filler work to keep one alive | Idle GPUs are flagged and cancelled; filler work defeats a fairness mechanism and can end with Research Computing restricting access for everyone using the workflow (local-LLM tutorial, Part 9). |
| Keep the only copy of anything in `/scratch` | It is purged. Section 7. |
| Put `module load`, `conda init`, or an environment activation in `~/.bashrc` | It breaks batch jobs and Open OnDemand and hides what a job used. Put setup in the job script. |
| Run an unbounded or interactive command through `ssh`: `watch`, `nvitop`, `tail -f`, `top`, `nvidia-smi -l` with no count, `vim`, `nano`, `less`, a bare `python`, or a bare `srun --pty bash` | It never exits, so the session hangs forever. Use a bounded one-shot form (Sections 5 and 6). Edit files locally, or write them with a quoted heredoc. |
| Poll the scheduler in a tight loop, or submit jobs in a loop | Every query and submission hits a shared scheduler. Check `squeue -u $USER` at most about once every 5 minutes **(house rule)**; use job arrays (Section 4) for many runs. |
| Modify raw data, or work from a directory you were not told you may use | Raw data cannot be regenerated. Other users' directories are off limits. |
| Fill in or submit the access form, sign in to Open OnDemand, or approve Duo | Identity-bound steps belong to the researcher. |
| Invent a flag, module name, partition, version or quota | State what you could not confirm instead. |
| Copy a template or slide example unchanged | Several contain errors (Section 12). |

## 2. Before the first command

**Read or measure first; ask only what remains, in one message.** If a read-only command can answer it, run it instead of asking: `whoami`, `hostname`, `pwd`, `groups`, `sinfo`, `squeue -u $USER`, `module avail <name>`, `ls -l`, `ssh-add -l` (local). If a short test run can answer it (sizes, runtimes, memory, whether the code is parallel), run the test instead of asking a non-expert to guess.

**Must ask** (only the researcher can answer; skip any already answered):

1. **Access:** your login name and whether you can log in now (Explorer: your Northeastern username, which can be the access form's UserID); research or a course; for research, which `/projects/<project>` group, and whether you are the sponsor (PI), a delegate or a plain member.
2. **Permission:** may I submit jobs for you? may I cancel jobs, delete files, or change group membership? **Each needs a separate yes.** Default: show the command and wait.
3. **Data:** where is it, how big, and is any of it restricted (human subjects, licensed, under an agreement)? If yes, stop and ask them to check with their institution before it goes on a shared cluster **(inferred: no source covers it)**.
4. **What and why:** what are you running, and what does "slow" or "too big" mean for you? Is it your own code or pre-built software? (If your own code, may I read the main loop?)
5. **Address:** which email address should job notifications use? (Never copy an address from a slide.)
6. **Agent access:** are you on campus or the VPN, and has Research Computing said automated agent access is fine for your use?

**Read or measure instead of asking:** whether the code is parallel (read it; check `seff` on a finished run); input sizes (`ls -l`, `du`); runtime and memory (a short slice, then `seff`/`sacct`); whether the work is many independent pieces (read the code and the file list); whether a run has finished before (`sacct`).

**Commands an agent may always run read-only on the login node** (as `ssh -o BatchMode=yes -o ConnectTimeout=10 explorer '<command>'`, single-quoted so `$USER` expands on the cluster):

`whoami; hostname; pwd` · `groups` · `id` · `squeue -u $USER` · `squeue -u $USER --start` · `sinfo` · `sinfo -p <partition> -o "%G"` · `seff <jobid>` (finished jobs) · `module avail <name>` · `module list` · `ls -l <path>` · `getfacl /projects/<project>` · `tail -n 50 <logfile>` · `ls /scratch/$USER/idle_bot_graphs/`

These need a compute node (they allocate one, so ask first). As an agent run them as a one-shot, never an interactive session: `ssh -o BatchMode=yes explorer 'srun -p short --constraint=ib --time=00:10:00 check-quota /home/<username>'` **(ordinary Slurm; no source ran it, so treat it as unverified)**. The same one-shot form works for `project <name> view members`, `gpu-logs <jobid>`, `historical-seff` and `du -shc .[^.]* ~/*`.

## 3. Explorer at a glance (verify before relying)

- **Hosts.** Login: `login.explorer.northeastern.edu` (nodes appear as `explorer-01`, `explorer-02`). Open OnDemand: `https://ood.explorer.northeastern.edu` (password plus Duo; human-only). The transfer node is written `xfer.discovery.neu.edu` in current docs; key login was tested only on the login host.
- **Login name.** Your Northeastern username. In one verified case it was the access form's **UserID**, not the email prefix; try the UserID first, then the email prefix, and wait a while after a password change. SSH asked for the Northeastern password and showed **no Duo prompt** in the verified cases (one account, one network).
- **Access.** A Northeastern login alone is not enough. Every research user must belong to a sponsor-owned storage space under `/projects` (free up to 35 TB). Students need a faculty sponsor. Either the sponsor or a delegate adds you (command, or the OnDemand **Managing /projects** app under Files, announced 2026-08-25), or you submit the ServiceNow access form (`https://bit.ly/NURC-AccessRequest`). Group changes can take up to 2 hours and may need a fresh login. How the form is processed beyond its first screen is **not confirmed**; say "we think" and send people to rchelp@northeastern.edu.
- **Storage** (all three are network filesystems):

  | Area | Use | Facts to state |
  |---|---|---|
  | `/home/<username>` | code, scripts, environments | 75 GB. Fills first; a full home breaks Open OnDemand. No source read states a backup policy for it. |
  | `/scratch/<username>` | temporary job data | **All files are purged on the first Tuesday of every month**, by date not age; no advance notice is mentioned in any source read, and it is not backed up. Size: sources disagree (slides say 50 TB; the policy page says 20 TB and 20 million files). Ask the researcher to check their own quota; do not quote a number. |
  | `/projects/<project>` | long-term and shared data | Free to 35 TB. Group access only; do not open it to "others". Its usage is covered by rc-docs pages ("Querying Project Storage") that were not read; no command is tested here. |

- **Partitions** (from `rc.northeastern.edu/partitions`, read 2026-10-11; confirm with `sinfo` and `scontrol show partition <name>`; a "large" partition is mentioned on one page but listed nowhere, so do not assume it exists):

  | Partition | Default / max time | Notes |
  |---|---|---|
  | `short` | 4 h / 48 h | Default for CPU work. 50 running and 1000 submitted jobs, at most 2 nodes. |
  | `long` | 1 day / 5 days | **Approval needed**; you must show the code cannot checkpoint. |
  | `sharing` | 30 min / 60 min | Quick tests only; 2 running, 4 submitted. Jobs on PI-owned nodes can be freed within an hour of the owner's job. |
  | `gpu-short` | 1 h / 2 h | 1 GPU. Prioritised. Quick tests, profiling, debugging. |
  | `gpu-interactive` | 1 h / 2 h | 1 GPU. Open OnDemand and interactive GPU work. |
  | `gpu` | 4 h / 8 h | 1 GPU per job; 4 running, 8 submitted. For `sbatch` GPU jobs. |
  | `multigpu` | 12 h / 24 h | **Approval needed**; up to 8 GPUs. Apply only after the code is optimised (`https://bit.ly/NURC-PartitionAccess`). |
  | `courses` | not in any source read | Only for people enrolled in a course. |
| `courses-gpu` | max 24 h (Intro to GPUs training; not on the partitions page) | Course-related GPU jobs; instructors request access. |

  Requesting the maximum nodes or tasks does not make a job faster or raise its priority. Running-job limits count running jobs only; Slurm also caps total jobs per account (10,000).
- **Time.** Routine maintenance is the **first Tuesday of each month**: no jobs run, and the same day scratch is purged. Never schedule work across it. Check `https://rc.northeastern.edu/status-updates/` before long campaigns.
- **Idle GPUs.** IdleBot emails after 15 minutes of under-use and cancels the job after one hour. "Under-use" has no published percentage. Graphs of cancelled jobs go to `/scratch/<user>/idle_bot_graphs/<job_id>.png`.
- **Policy.** Research or coursework sponsored by Northeastern only. Never share a login. Violations can mean account revocation.

## 4. Is parallel even the answer?

Run this tree before proposing any cores, nodes, or GPUs. A researcher who says "my code is slow" or "my job is big" has not yet told you what to request.

**Step 1: where is it really running?** GPU job: do the GPU check (Section 6). CPU job: how many cores did it ask for, and how many does the code use? (`seff <jobid>` on a finished run.)
**Step 2: pre-built or their own code?** Pre-built GPU and simulation packages (GROMACS, NAMD, AMBER, Hugging Face) handle batching and kernels themselves: use their flags, verify the device, watch utilisation and I/O, do not rewrite them. Other pre-built packages may or may not be parallel: read their documentation for thread and GPU flags, set them from the allocation, and verify with `seff` or `nvidia-smi`. Own code: continue.
**Step 3: baseline.** Record wall time, throughput (samples/s), and for GPUs utilisation and memory, before changing anything.
**Step 4: classify the work.**

| The work is | Do this |
|---|---|
| Many independent runs (parameter sweep, one file per task) | The easiest parallelism. Use a job array (below), or a worker pool inside one job. |
| One CPU program, loop-level parallel, fits one node | Shared memory: OpenMP, `multiprocessing`/`concurrent.futures`, R `foreach`/`parLapply`, MATLAB `parfor`. `--ntasks=1 --cpus-per-task=N`. |
| One CPU program that needs more memory or cores than a node **and is already MPI** | `--nodes`, `--ntasks-per-node`, `--cpus-per-task`. If the code is not MPI, never ask for more than one node. |
| GPU training or inference | Section 6. |
| Sequential logic, branching, or tiny work | A GPU is the wrong tool. A CPU job is. |

**Rules that follow from the training material:**

- **Profile first.** Name the bottleneck before parallelising. Do not convert finished serial code to parallel because it is slow; ask which parts are independent before code is written.
- **Compute the ceiling.** Estimate the serial fraction S (reading input, writing output, steps that depend on the previous one). The best possible speedup is 1/S. S = 0.1 means 10x at most, however many cores. Never promise "N cores = N times faster".
- **Same problem faster, or a bigger problem?** Fixed size hits the serial wall (strong scaling). Bigger problem in the same time scales better (weak scaling). Size the request to the answer.
- **Quote the real curve.** In Research Computing's own benchmark (Game of Life, 10000 x 10000, 500 iterations): 1 core 250.7 s; OpenMP 2/4/8/12/16/20 cores gave 116.8/58.1/29.4/33.4/25.2/20.2 s. **12 cores was slower than 8**, and 20 cores ran at about 62% efficiency. So test two or three sizes on a short slice before fixing the real request.
- **More nodes is not automatically faster.** Splitting across nodes adds network traffic. A multi-node GPU test on a small matrix got 5.48 s on two GPUs of one node and 5.08 s on four GPUs over two nodes: barely better. Prefer one node first.
- **Do not ask for cores the code cannot use (inferred).** `--cpus-per-task=N` for a single-threaded program, or `--ntasks>1` or `--nodes>1` for a program not written for MPI or DDP, wastes the allocation silently. Confirm *how* the code is parallel first.
- **Say the multiplication back.** Total cores = nodes x ntasks-per-node x cpus-per-task. `--ntasks` is the number of independent processes (MPI ranks). `--cpus-per-task` is the cores each process may use for threads. "4 ranks x 5 threads x 4 nodes = 80 cores".
- **Set worker counts from the allocation, never from a typed number.** OpenMP: `--ntasks=1 --cpus-per-task=N` and `export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK`. Pure MPI: `--ntasks=N --cpus-per-task=1` and `mpirun -np $SLURM_NTASKS`. Do not use `detectCores()` or `multiprocessing.cpu_count()` as the pool size; use `$SLURM_CPUS_PER_TASK` **(house rule; general Slurm knowledge, not in the sources)**.
- **Use the right tool.** One node: OpenMP / multiprocessing / `foreach` / `parfor`. Many nodes: MPI / `mpi4py`. Big array maths: GPU through PyTorch, CuPy, or RAPIDS (never hand-written CUDA for a non-expert). Deep learning across GPUs: PyTorch DDP.
- **Many independent runs: use a job array, throttled.** One submission, many tasks, one queue entry per task: `#SBATCH --array=0-99%10` (the `%10` keeps at most 10 running at once) and `$SLURM_ARRAY_TASK_ID` to pick the input; name outputs with `%A_%a`. AICR's documentation shows this syntax; Explorer's per-partition submitted-job caps (Section 3) still apply and whether each array task counts toward them was not read, so check before launching a large array. Never submit hundreds of separate jobs in a loop.
- **Multi-node recipes are not in the sources.** Do not improvise a multi-node `torchrun`/MPI launch, tensor or pipeline parallelism, or the compiler/MPI `module load` lines. Say it is not covered and point to Research Computing.

## 5. Sizing and submitting a request

**Run on a compute node, never the login node.**
- Interactive: `srun --pty bash` (from a login node). Defaults on `short`: 4 hours, 1 node, 1 task, 2 CPUs, 2 GB. With limits: `srun --time=6:00:00 --mem=50GB --ntasks=16 --partition=short --pty bash`.
- Helper commands (`project`, `check-quota`, `gpu-logs`, `historical-seff`, big copies) need `srun -p short --constraint=ib --pty bash`.
- **Develop and test small; submit the full job only once the commands work.** For a human, the slides' rule of thumb is: if a job runs under about 30 minutes in an `srun` session, do not use `sbatch`. **As an agent you cannot hold an interactive session**: use `sbatch` with a short `--time` for any test beyond a one-line check, or the one-shot `ssh -o BatchMode=yes explorer 'srun -p short --time=00:10:00 <command>'` (unverified form), and leave `srun --pty bash` to the researcher's own terminal.

**Request the minimum, then grow.** Ask close to the minimum the job needs and scale up if it dies for memory, CPU, or time. **For a brand-new job (house rule):** run a small slice first with a generous but short `--time`, read `seff` and `sacct` (`MaxRSS`), then set `--mem` to about 1.3 times the peak; if no slice exists, ask the researcher rather than guess a number. Learn the real need from a finished job: `seff <jobid>` (CPU efficiency, memory used), or `historical-seff` for a campaign. In Research Computing's example a job with 12 cores at 8.29% CPU efficiency and 10.44% of 50 GB used "could have requested fewer resources"; one at 83.83% CPU was a much better fit on CPU (its memory was still only 3.56% used).

**Every script states its numbers.**
- Always set `--partition`, `--time`, `--mem` (CPU RAM), `--cpus-per-task`, `--job-name`, and `--output`/`--error` with `%x-%j`. Never rely on the 4-hour default (it hides what was requested and cannot be right-sized) **(house rule)**.
- **`--time` = expected runtime + about 20%, never above the partition maximum.** Estimate the runtime from a short run (20 to 50 steps, or a fixed slice), scale it up, then add 20%. A smoke test that prints a few lines gets `--time=00:05:00` **(inferred)**.
- **`--mem` is CPU RAM, not GPU memory.** Never raise `--mem` to cure a CUDA out-of-memory error.
- **Create the log directory before `sbatch`** (`mkdir -p logs`): Slurm opens the output file before the script body runs.
- Put environment setup in the script, in order: `module load ...`, then `source activate <env>` (Explorer; on AICR see `AICR.md` Section 10). Print the allocation at the top: job ID, node, date, git commit (Section 9).
- Use the researcher's own address for `--mail-user`, or leave mail flags out.
- Check state before choosing: `sinfo`. A node state of `MIXED` describes CPUs, not GPUs.
- After a job: `seff <jobid>` (and `gpu-logs <jobid>` for GPU jobs). Record what it used.
- Cancel an interactive session the moment you finish (`exit`, or `scancel <jobid>` for that one job, with a yes). Always set `--time` so a forgotten session ends itself.

**`long`, `multigpu`, `courses-gpu`:** do not write scripts for them until the researcher confirms access. Optimise first; approval is not automatic.

## 6. GPUs

**A GPU is the right tool only for the same operation over a lot of data** (deep-learning training and inference, large arrays). Sequential or branching logic and tiny workloads belong on CPUs. A flat, low utilisation line means the workload is too small for the GPU, not that the GPU is slow.

**Requesting.** A GPU job needs both a GPU-enabled `--partition` and `--gres=gpu:<type>:<count>`. (On AICR the partition fixes the GPU type and you do not add one: see `AICR.md` Section 4.) Name the type when it matters (`gpu:v100-sxm2:1`); a bare `gpu:1` can land on a different card with different memory and capabilities. List types with `sinfo -p <partition> -o "%G"` and free GPUs with `sinfo -p gpu -O "NodeList,Gres:30,GresUsed:30"`. For repeatable results, request a specific type and record which one ran. Old cards (V100, T4) may not run current builds of some tools.

**Never trust the allocation; verify it at the top of every GPU script, or at least the first run.** Check that CUDA is available, the device name and memory, the device count, and that a tensor round-trips CPU to GPU and back. Also run `nvidia-smi`. A job "that worked" may have run on CPU with no error: causes, in order: you are on a login node; the environment is not activated (run `which python`: it must point into the environment) so you have a CPU-only PyTorch; a typo in `--gres`. Do not report "GPU OK" from a script that only tests whether `CUDA_VISIBLE_DEVICES` exists. Do not set or override `CUDA_VISIBLE_DEVICES`.

**Environment (Explorer; on AICR use a `PATH` prepend, not `source activate`: see `AICR.md` Section 10).** For PyTorch the pip or conda wheels bundle the CUDA runtime: do not `module load cuda` for them. Research Computing's GPU training uses a venv from the system `python3` plus `pip install torch ...` (the workshop says there is no `python` module, but `module avail python` listed `python/3.13.5` on 2026-10-11; `miniconda3` and `anaconda3` modules also exist; `conda` is not on the login PATH until one is loaded). After a setup script, `source <env>/bin/activate` yourself: a script run with `./` activates nothing for your shell. If a container bundles CUDA, run it with `apptainer exec --nv`.

**Measure before you change.**

- Sample `nvidia-smi` while the job runs. A human can `watch -n 1 nvidia-smi` in a second terminal; **an agent must not** (it never exits). Log a bounded sample inside the job script instead (general `nvidia-smi` flags, not in any source): `nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv -l 10 -c 30 >> logs/gpu-$SLURM_JOB_ID.csv &`, then read `gpu-logs <jobid>` after the run. GPU-Util is the share of the last second in which at least one kernel ran; Memory is VRAM allocated. They are independent.
- **Bands to use (house rule, reconciled from slides that use 50, 60, 70 and 80; say which you used):** below 50% utilisation is a problem; below 60% suspect the data pipeline and fix it before the next run; 60% to 70% is amber; at least 70% is acceptable; 80% to 100% is the target; memory 60% to 90% is healthy (below 40% means room to raise the batch). After every batch job run `gpu-logs <jobid>` (it keeps 7 days and covers public nodes only, so run it promptly).
- Classify from utilisation plus memory: low/low = the GPU sits empty, check data; low utilisation with high memory = model loaded but not fed, a data pipeline or sync problem (the most common case); high utilisation with low memory = healthy, raise the batch size; high/high = good.
- **Loader-versus-compute stopwatch:** time 50 batches from the loader with no GPU work, then 50 steps on synthetic data with `torch.cuda.synchronize()`. If loading takes longer than computing, you are data-bound and no model change helps.
- Escalate only as far as needed: `nvidia-smi`/`nvitop`, then the framework profiler, then Nsight Systems; Nsight Compute only for hand-written kernels. Profile interactively for a short window (10 to 50 steps), not through the batch queue; send trace files to `/scratch/$USER`, not home.
- **Baseline, change one thing, re-measure, record.** Never change several things at once.
- **Benchmark hygiene when you write a timing script:** warm up first (3 to 8 untimed steps), call `torch.cuda.synchronize()` before starting and before stopping the clock, time many iterations, keep the task fixed (same resolution and model width) when comparing.

**Speed it up in this order** (they are listed by how often they are the cause and how easy the fix is):

1. **Data pipeline** (utilisation under about 60%): `num_workers = cpus-per-task - 1` (never leave the default 0); `pin_memory=True` with `.to("cuda", non_blocking=True)`; `persistent_workers=True` when workers > 0; raise `prefetch_factor` (start at 2) if still slow. Request at least 4 CPUs, and `--cpus-per-task = num_workers + 1`. Pack data as a few large files (HDF5, WebDataset), not millions of small ones, and keep it in scratch or projects, never home.
2. **Batching.** Never feed the GPU one sample at a time; every call has a fixed cost.
3. **Batch size.** Raise it until VRAM is about 75% to 90% used or you hit out-of-memory; if memory is about 15% to 20% and nothing fails there is room to raise it several-fold: double it and re-measure. Leave a margin below the largest size that fits (the optimiser needs memory too).
4. **Mixed precision.** Wrap the forward pass and loss in `autocast`, leave `loss.backward()` outside. Choose by compute capability, not by `torch.cuda.is_bf16_supported()` (a workshop script reports that it says yes even on a V100; this is PyTorch-version dependent): BF16 on A100/H100-class (capability major 8 or higher), FP16 plus `GradScaler` on V100/T4. Do not cast the whole model to BF16 by hand. Say honestly that total memory does not halve and the speedup depends on the operations.
5. **Memory too tight:** reduce the batch, then mixed precision, then gradient checkpointing (the workshop claims about 60% to 70% less activation memory for about 30% more compute; uncited). After an out-of-memory error free the memory (`del` the big objects, `torch.cuda.empty_cache()`).
6. **Convolutional models:** `channels_last` for model and input. **Inference loops:** `model.eval()` and `torch.no_grad()`. **Hugging Face:** `bf16=True`, `gradient_checkpointing=True`, `dataloader_num_workers = cpus-per-task - 1`.

**Multi-GPU: earn it.**
- **The 80% rule.** Do not request more than one GPU until a single-GPU run shows over 80% utilisation and the code is written for DDP. Multi-GPU multiplies the efficiency you already have: a job at 20% on one GPU becomes a four-GPU job at 20% using four times the allocation.
- **Never scale an I/O-bound job.** More GPUs compete for the same filesystem.
- **A plain single-GPU script given N GPUs uses one and wastes N-1.** Check `torch.distributed.is_available()` and that the script calls `init_process_group`.
- **DDP rules.** Use `DistributedDataParallel` through `torchrun`, not `DataParallel`; wrap with DDP after moving the model to its device; use `DistributedSampler` and call `sampler.set_epoch(epoch)` each epoch; backend `nccl`. **Three numbers must agree:** `--gres=gpu:TYPE:N`, `--ntasks-per-node=N`, `torchrun --nproc_per_node=N`; keep `--nodes=1`. Stay inside one node first (NVLink is far faster than InfiniBand between nodes).
- **Measure scaling efficiency** after every scale-up: `throughput / (world_size x single_gpu_throughput) x 100`. Above 80% is good; below 70% means stop and look for a communication or I/O problem.
- **A model too big for one GPU is not fixed by DDP** (every GPU holds a full copy). That needs tensor or pipeline parallelism, which the sources do not cover: point to Research Computing.
- Do not use `multigpu` or `courses-gpu` without confirmed access.

**Honest limits.** Quote the source's illustrative numbers (for example 18% to 82% utilisation as the loader knobs are tuned) as illustrations, not promises. Some figures in the material (the 20% to 40% pinned-memory latency gain, the checkpointing percentages) are uncited and were not reproduced.

## 7. Storage, data, and transfers

- **Put things where they belong.** Code, scripts and environments in `/home` (watch 75 GB). Temporary job data in `/scratch/$USER`. Anything shared or long-lived in `/projects/<project>`. Paths are case-sensitive; write absolute paths in scripts and commands.
- **Scratch is temporary.** Move results worth keeping off scratch before the first Tuesday, and archive big directories first. From a compute node (`srun --pty /bin/bash`): `mv /scratch/<username>/<file> /projects/<group>/<dir>/`, or `tar -czvf /scratch/<username>/<name>.tar.gz <dir>` then move the archive. A `mv` across filesystems is a copy followed by a delete: for large trees prefer `rsync -a`, check the result, then remove the original only with the researcher's yes. Checkpoint long jobs that write continuously. Do not "dodge" the purge by touching or re-copying files **(house rule)**.
- **Conda environments, container images (`.sif`), and model weights are not scratch material.** Keep them in home or `/projects`. Only regenerable caches go to scratch (for example the conda package cache through `pkgs_dirs` in `~/.condarc`; ask before editing that file).
- **When home is full** (quota exceeded; Open OnDemand sessions end at once or an OnDemand Desktop shows Completed without starting): `check-quota /home/<username>` from a compute node, find the big items with `du -shc .[^.]* ~/*`, then clean with the researcher's yes: `conda clean --all`, `conda env remove --name <env>`, `apptainer cache clean all`, point `APPTAINER_TMPDIR`/`APPTAINER_CACHEDIR` at project space before pulling containers. Do not move or remove `~/.local` or `~/.cache` while any job of yours is running (`squeue -u $USER` first).
- **Transfers.** Never over the login node. Small: the Open OnDemand Files app (limit 10 GB per transfer). Large or many files: Globus. From your computer: `scp`/`rsync` to the transfer node, run from the local machine; add `-n` (dry run) before any `rsync` that could overwrite; `--partial` for big files. Compress many small files first. Between cluster directories: `rsync -av` from a compute node. `sshfs` does not work on the cluster. Key login was tested only on the login host, so do not assume `scp` to the transfer node works unattended.
- **Many small files are slow.** All three filesystems are network filesystems; per-file overhead kills throughput. Pack them.
- **Backups.** No source states a backup policy for home or projects; only scratch is stated to be not backed up. Tell the researcher that, and apply 3-2-1 (three copies, two media, one off site) to anything irreplaceable.
- **Restricted data.** If the data is non-anonymised, under an agreement, or otherwise restricted, stop and ask the researcher to check with their institution before it goes anywhere on a shared cluster.
- **Course storage** (`/courses/<course>`, 1 to 5 TB) is shared by the whole class: one student can fill it for everyone.

## 8. Software and environments

**Order of install** (each step down costs more setup and upkeep): (1) a **module**; (2) **conda** for Python or R packages; (3) a **container** built on the researcher's own machine when dependencies are nasty or portability matters; (4) a **source build** when a patch, a specific version or a build flag is needed; (5) **Spack or EasyBuild** only for source-level control the researcher will maintain.

- **Before installing anything:** `module avail <name>`. If a module exists, load it and stop. Module and version names in tutorials are examples; re-check live. Explorer uses classic Tcl Environment Modules (Modules 5.3.0, checked 2026-10-11), not Lmod; AICR uses Lmod 8.7.65.
- **Heavy installs run in a compute-node session**, never the login node: conda solves, `make -j`, `spack install`, container pulls. Match `-j` to the cores you were given. Never `sudo`.
- **Conda.** Load the cluster's conda module (`module load miniconda3`); do not install your own. Use `conda-forge` and remove the `defaults` channel (licensing); changing `~/.condarc` is a persistent edit, so ask first. Never `conda init`; if its block is in `~/.bashrc`, recommend commenting it out (ask first). Activate with `source activate <name-or-path>`. One small named environment per task, never one for everything. Install everything in one command or from one `environment.yml`; pin versions; quote specs that contain `<` or `>`. Mixed conda and pip: conda first, pip last, inside the activated environment. For a slow solve use `mamba`. Put environments in persistent space (use `-p /projects/<project>/envs/<env>` if home is tight). Export every time it changes (`conda env export --from-history` for a clean spec, plain `conda env export` for an exact record) and commit the files. Do not run `conda update --all` or `conda env remove` on a project environment without a yes.
- **Containers.** Apptainer, never Docker; it is installed system-wide (no `module load`). **Never build a `.sif` on the cluster**: build it where the researcher has root (laptop, workstation, VM), then copy it to project space and `exec` it. The Apptainer remote builder needs a third-party account and uploads the recipe: the researcher decides. Pull on a compute node. **Pin the image tag** (never `latest`) for anything that must be reproducible. Keep the `.def` beside the `.sif`, in git. Only `/home` is bound automatically: bind `/projects` and `/scratch` explicitly with absolute paths. GPU: `apptainer exec --nv`. If the GPU is not found inside a container, check `--nv` and that you are on a GPU node before anything else.
- **Source builds.** Read the project's README first; its instructions win over any pattern. Always give an install prefix in your own space (`--prefix=$HOME/software/<tool>`), never `/usr/local`. Load the cluster's compiler, CMake and library modules before configuring, and point parallel or numerical builds at the cluster's MPI and BLAS/LAPACK, not a slow fallback. For anything reused, write a personal modulefile (first line exactly `#%Module`).
- **Spack and EasyBuild** are last resorts: long compiles, large footprints, real upkeep. EasyBuild is not a module here; install it in a conda environment and pass the three cluster flags (`--modules-tool=EnvironmentModules --module-syntax=Tcl --installpath=...`). Do not write your own easyconfig for a standard package. Large trees belong in project space, not home.
- **Never put `module load` in `~/.bashrc`.** Plumbing (a `PATH` line, `module use`, `APPTAINER_BIND`) is tolerated there, but ask before editing it, and repeat what a batch job needs inside the script.
- **After any install,** verify it with a one-line import or version check inside a job, and keep the record (exported env file, `.def` plus `.sif`, modulefile).
- **R packages needing C++17:** `module load gcc/11.1.0` and a `~/.R/Makevars` with `CXX17 = g++ -std=c++17 -fPIC`, `CXX17STD = -std=c++17`, `PKG_CXXFLAGS = -std=c++17 -fPIC`, `PKG_LIBS = -fPIC`.

## 9. Reproducibility: the record every job leaves behind

For a **new** project, start with a git repository, a folder layout, an environment file, a README and a `.gitignore`, **before** the first run. For an existing project, propose the layout and ask before restructuring anything.

- **Layout.** `data/raw` (read-only: never edit, overwrite or "clean" in place), `data/processed`, `data/metadata`, `src` or `scripts`, `results`, `slurm`. Ask the owner before `chmod` on raw data (only the owner can; and `chmod 555` on a directory does not protect the files inside). Name files with ISO dates, lowercase, hyphens or underscores, no spaces; never `final_v2`.
- **Scripts, not clicks.** Every analysis step is a script that can be rerun. Tunable values go in a labelled block at the top. Start shell scripts with `set -euo pipefail`. Use relative paths in code and configuration (put an unavoidable absolute data path in one config line). Set and record every random seed.
- **Commit before you submit.** Every job must trace to a specific commit and print the hash in its log. Put a guard at the top of the job script that refuses to run with uncommitted changes (`git diff --quiet && git diff --staged --quiet`, else exit 1). The guard runs when the job *starts*, so do not edit the tree while a job is queued. Tag the run (`git tag run-$SLURM_JOB_ID`) and tag the exact commit behind any paper (`git tag -a v1.0-submission`; push the tag explicitly, with the researcher's yes).
- **Git hygiene.** One logical change per commit; look at `git diff` before committing; stage named files, not `git add .`, when the folder may hold data, tokens or logs. Keep results, big raw data, logs and Slurm output out of git (`.gitignore`); use Git LFS (to about 2 GB) or DVC for large files; strip notebook outputs. Never `git reset --hard` on a shared branch; use `git revert` for pushed commits. Note that a file under an ignored directory cannot be re-included by a `!` rule.
- **The minimum record, every job** (print the header at the top of the log):
  1. job ID, node list, partition, requested resources
  2. start and end timestamps (ISO)
  3. git commit hash, branch, `run-<jobid>` tag, and a clean working tree
  4. the exact command and the sbatch script (under version control)
  5. every parameter value
  6. every random seed
  7. input paths (read-only) and a checksum of each
  8. software: pinned `module load name/version` lines, or the env file, or the `.sif` and its `.def`
  9. for containers: image and tag, bind list, `--nv` yes or no
  10. hardware actually used: CPU count and GPU type and count
  11. output directory and the stdout/stderr files
  12. exit status, headline numbers, and the README line that tells a stranger how to rerun
- **README** states requirements, exact rerun commands (including the tag), the layout, the parameters and where the data live. Have someone else clone it and rerun it from the README, and report that result, not "it runs for me".
- **Words matter.** Reproducibility is the same data and methods; replicability is new data with similar methods. Do not promise more than a run delivers. Hardware-dependent results are a named barrier: record the CPU and GPU type.

## 10. When you are an agent on the cluster

**Getting in (human-only steps first).** The researcher, not you, creates the key, installs it and unlocks it once into `ssh-agent`: key login is verified on Explorer with `ssh-keygen -t ed25519` (with a passphrase), `ssh-copy-id`, and on macOS `ssh-add --apple-use-keychain`. The `Host explorer` block in `~/.ssh/config` must exist or `ssh explorer` fails with "Could not resolve hostname". Then you may run `ssh -o BatchMode=yes -o ConnectTimeout=10 explorer '<command>'`. Research Computing's own page tells people to leave the passphrase empty; do not recommend that.

**If a command prompts, hangs, or says `Permission denied`: stop and report the exact error.** Do not retry in a loop, do not edit `~/.ssh`, and never ask for a password, passphrase, Duo code or key. An emptied agent looks exactly like an expired key: have the researcher run `ssh-add -l`. Do not run `ssh-add -D` except as a deliberate test.

**Non-interactive ssh facts.** Each call starts in `$HOME` and keeps no state: write `cd /projects/<project> && ls -l` inside one call and use absolute paths. Single-quote the remote command so `$USER` expands on the cluster. Windows and Linux key-unlock commands were not tested.

**Be honest about what is untested.** Not verified: key login from off campus or another network, Open OnDemand, `scp` to the transfer node, and whether Research Computing permits automated agent access. **No policy page read mentions agents either way.** Tell the researcher, and have them ask rchelp@northeastern.edu before any unattended or high-volume agent use. Stay read-only by default.

**If asked to run a local model or coding agent on the cluster,** read Research Computing's local-LLM tutorial first. The non-negotiables from it: run it inside a Slurm GPU allocation, never on a login node; never bind Ollama to `0.0.0.0` (it has no authentication) and bind to `127.0.0.1` on a random port; keep tokens in `chmod 600` files out of repos and chat; keep model files in project space, not home; set the context window to at least 65,536 tokens; request one GPU on the `gpu` partition; cancel the job when you stop; never keep a GPU alive with filler work; use a fresh git branch and review the diff for unattended agent work; do not tunnel inference off the cluster without Research Computing's confirmation. A local 20B-to-120B model is much weaker than a frontier model: give it narrow tasks.

## 11. Linux habits that prevent disasters

- `rm` cannot be undone. `ls` the same path first. `>` overwrites a file; `>>` appends. `cp` needs `-R` for directories, `rm` needs `-r`.
- Read `ls -l` before touching permissions (`-rwxrw-r--` is type, owner, group, others). On `/projects`, share through the `project` tool (member or guest), never `chmod o+...`.
- Quote paths that contain spaces and quote variables. The one place spaces are forbidden is the `project` user list (`u1,u2,u3`).
- Use `cat` for short files and `less` for long ones (in `less`, `q` quits). If someone is stuck in `vim`: `Esc` then `:q!`. `Ctrl+C` aborts a running command.
- A symlink breaks if the original moves or is deleted. `ls -a` shows hidden files such as `.bashrc`.
- Practise a destructive operation on a disposable test file first.

## 12. Slurm scripting traps and slide errors (do not copy these)

- **A comment after a line-continuation backslash breaks the command.** `python train.py \   # CHANGE` ends the line at the backslash-space, so `--data-dir` is then run as a command ("command not found"). Remove trailing comments after `\`.
- **The slide short form is wrong:** `srun -t 6:00:00 --m 50GB --n 16 -p short --pty bash`. Use `srun -t 6:00:00 --mem=50GB -n 16 -p short --pty bash`.
- **The sample `sbatch` sets neither `--time` nor `--mem`** and uses the presenter's email. Set both and use the researcher's.
- **`--partition=compute` does not exist on Explorer.** Use `short` (CPU) or a GPU partition.
- **A scratch-purge docs example `mv`s without `<username>`;** use the `srun` commands in Section 7.
- **`./setup.sh` does not leave an environment active;** `source` the activate file.
- **A setup script that downloads or builds belongs on a compute node;** `mkdir -p logs` belongs before `sbatch`.
- **Templates call files you may not have** (`train.py`, `train_ddp.py`) and flags (`--fp16`, `--bf16`, `--data-dir`) the researcher's script must define.
- **Do not use a trivial password** for an Open OnDemand VS Code Server session even where a slide suggests `123`.
- **Do not paste the example usernames, email addresses or paths from the slides.** `/projects/<project>` is the real layout.
- **`date --iso-8601` and `sed -i 's/..../'` are GNU-only.** On a Mac they differ; run them on the cluster.

## 13. Getting help and reporting back

- **Send the researcher to Research Computing** for anything unconfirmed, any policy question, any access request, multi-node recipes, MPI and MATLAB parallel server, and before promising a result: rchelp@northeastern.edu; office hours on Zoom (days and times at `https://rc.northeastern.edu/getting-help/`); booked consultations; docs at `https://rc-docs.northeastern.edu/en/latest/index.html`.
- **For a ticket include:** the username, the job ID, the node (the `Host`), the exact command or script, the full error text, `seff <jobid>`, and for Open OnDemand sessions the session's `output.log`. RC reads `output.log` and the job ID.
- **When you report back to the researcher, say:** what you did and ran; what you saw (exact numbers); what it costs (time, GPU hours, queue); what you recommend next and why; and what you are **not** sure of. Never claim success you did not measure. Report any file you wrote by its absolute path.

---

# Appendix A: Conflicts and unverified items (the honest list)

These are places where the sources disagree or are silent. The file above takes the safe reading. Do not harden any of them into a rule without checking.

1. **Scratch quota:** 50 TB per user (Spring and Summer 2026 slides) versus 20 TB and 20 million files (policy page). Unsettled; never quote a number. The file-count limit is real and only the policy page mentions it.
2. **Home quota:** 75 GB in two sources; a docs sample shows soft about 72 GB and hard about 102 GB under a placeholder path. Soft versus hard is not confirmed. "Home quotas are fixed and cannot be increased."
3. **Delegates and guests:** one slide says a delegate can add and remove members and guests; the command table says only the PI can add guests; there is no `remove guests` command. Safest reading: delegates manage members only; the PI manages delegates and guests.
4. **Utilisation thresholds** (50, 60, 70, 80%) appear in different places. Section 6 uses one set; cite it.
5. **`num_workers` versus `--cpus-per-task`:** the rule is workers = cpus - 1, but several snippets use `num_workers=8` with `--cpus-per-task=8`. The rule wins.
6. **OOM remedy order:** Explorer material says reduce batch, then mixed precision, then checkpointing; AICR's reverses it. Section 6 gives the Explorer order; `AICR.md` gives AICR's.
7. **Python setup:** one source uses `module load miniconda3` and `source activate`; the GPU workshop says there is no `python` module (a `python/3.13.5` module was listed on 2026-10-11) and uses a venv with pip wheels; a commented line mentions `module load cuda`. Conda and venv both work; do not mix their module lines in one script.
8. **`conda activate` versus `source activate`:** use `source activate` (no `conda init`).
9. **`defaults` channel:** one source removes it, another keeps it in examples. Remove it, after asking.
10. **Where to `apptainer pull`:** one source says pulling is fine anywhere; two say a compute node. Use a compute node.
11. **What may go in `~/.bashrc`:** plumbing is tolerated; `module load`, `conda init` and activation are not.
12. **Partitions page URL** returned 404; limits come from `rc.northeastern.edu/partitions` through a summariser. A `large` partition is named once and listed nowhere.
13. **Transfer host** is still written `xfer.discovery.neu.edu` (legacy name) and was not tested.
14. **Duo:** Open OnDemand needs it; SSH showed none on one account and one network. Do not generalise.
15. **Job arrays:** the Explorer training material has none; the syntax in Section 4 is shown in AICR's documentation and is standard Slurm. Explorer-specific array limits were not read.
16. **Not read (titles only):** job-assist command, Slurm job arrays page, checkpointing page, Globus, shell environment, GPU access and H200 quick start, Spack, courses cheat sheet, `check-quota` on `/scratch` and `/projects`.
17. **Memory fragmentation, `sacct` on Explorer, compiler and MPI modules, multi-node DDP, tensor and pipeline parallelism, how to estimate RAM and runtime for a brand-new job:** not covered by any source. Do not invent them.
18. **Dates:** slides are Spring and Summer 2026; the OnDemand project app was announced 2026-08-25; the June 15 to 19, 2026 shutdown is past and the next annual dates are not in any source.
19. **Automated agent access:** no policy page read mentions it.
20. **Conda module name:** the OnDemand slides load `anaconda3/2024.06`; the installation and reproducibility sessions use `miniconda3`; one installation example shows `python/3.13.5`, while the GPU workshop says there is no `python` module. Use `module avail` to see what exists today.
21. **GPU type naming:** some slides use a bare `--gres=gpu:1`; the GPU workshop says to name the type. This file names the type when it matters. The GPU workshop lists only V100 and A100 while `sinfo` shows more (including H200).
22. **`prefetch_factor` starting value:** 4 in the Explorer workshop, 2 in its script and in AICR's. This file starts at 2.
23. **Where local-model weights go:** the local-LLM tutorial defaults to `/scratch` (subject to the purge) and says to use project space if available; this file says project space.
24. **GPU limits in an example:** one reproducibility session shows a 2-GPU, 12-hour `gpu`-partition job; the `gpu` partition is 1 GPU and 8 hours. Do not copy it.
25. **Backups of `/home` and `/projects`:** no source states a policy; only `/scratch` is stated to be not backed up.
26. **Live partitions and GPU types (2026-10-11, one researcher's account):** `sinfo` listed only `gpu` (8 h), `short` (default, 2 days), `sharing` (1 h), `gpu-short` and `gpu-interactive` (2 h each); `long`, `multigpu` and the courses partitions did not appear (they may need access, unverified). GPU types on `gpu`: `v100-sxm2`, `v100-pcie`, `a100`, `h200`, `t4`; the workshop lists only V100 and A100.
27. **Login-node commands (2026-10-11):** `seff`, `historical-seff`, `gpu-logs`, `check-quota`, `project` and `apptainer` are on the Explorer login PATH; `nvidia-smi`, `conda` and `spack` are not.

# Appendix B: Where each part comes from

Sources are in this repository: the Research Computing training material (`Intro-to-Explorer-OOD-2026`, `Managing-Projects-on-Explorer`, `Intro-to-Linux-2026`, `Intro-to-GPUs-2026`, `Optimizing-GPU-Usage-on-Explorer`, `Intro-to-HPC-Scaling-Parallel-Computing-2026`, `Intro-to-Software-Installation-2026`, the three Scientific Reproducibility sessions, and the local-LLM tutorial), the public pages at `rc-docs.northeastern.edu` and `rc.northeastern.edu` read on 2026-10-11, the verified login record `Logging-into-Explorer-with-Claude/SESSION.md`, and the access guide `Requesting-Access-to-Explorer/README.md`. The rule-by-rule evidence, with file and line for every rule, is kept in `skills/evidence/` in the author's working copy (it cites a private project, so it is not published).

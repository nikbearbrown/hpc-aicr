# Get started: run a local model on Explorer and point Claude Code at it

**What this is.** One file you hand to Claude Code. It walks you, one step at a time, through setting up an open model (Ollama in a container) on a Northeastern Explorer GPU and pointing a coding agent at it. Claude Code checks your cluster access with read-only commands, writes six small scripts into `~/.ollama-hpc/` on the cluster, runs one setup job and one short GPU test (asking before each), then gives you the exact commands to start your own session. You keep every decision and every secret; the agent does the careful, checkable work.

**Why it exists.** A local model on a cluster GPU has no per-token bill, but "free" is wrong: you pay in queue time and fair share, an idle-GPU watcher cancels jobs that sit unused, and a few common settings (binding to every address, a doubled base address, unmapped model names, a tiny default context window) quietly break the setup or expose the model to everyone on the node. The scripts here avoid those traps; the recipe makes an agent apply them the same way every time.

**What we found.** The setup is small: three scripts to put on the cluster, one setup job to pull the container, one GPU test job to prove it, then a session you start yourself. The model runs inside your own GPU job, so nothing is shared. A standing endpoint for a whole class is a different thing and a policy question for Research Computing (the tutorial explains why).

**What is NOT verified.** Nobody has run this whole sequence start to finish. Six scripts are copied exactly from the tutorial (`films/running-a-local-llm-on-explorer/source/`), which was checked against Ollama, Claude Code and Research Computing documentation but not run. Two scripts, `setup.sbatch` and `smoke-test.sbatch`, are new and have only been syntax-checked. Anthropic's documentation says it does not support pointing Claude Code at non-Claude models: this works through documented settings but is an unsupported route. No page we read says whether Research Computing allows automated agent access; ask rchelp@northeastern.edu. Plan on an hour or two, mostly waiting on the queue and downloads (not measured). Expect to fix something, and ask the agent to log it.

## Before you start (you, not the agent)

1. **You can `ssh explorer` without a password prompt.** Creating the key and unlocking it are yours, not the agent's. If you cannot yet, watch [Logging into Explorer (HPC) with Claude](https://youtu.be/KEKiKe6roQk) first, and the access guide in this repository.
2. **You belong to a `/projects/<group>` space** (your sponsor adds you) and your account can use GPU partitions.
3. **Claude Code is installed on your computer** (`claude --version`).
4. **Ask Research Computing first** if you will leave anything running unattended or want to share a model: rchelp@northeastern.edu. The questions are in the tutorial, Part 10.

## Paste this into Claude Code

**If you cloned the repository** (recommended):

```bash
git clone https://github.com/nikbearbrown/hpc-aicr.git
cd hpc-aicr
claude
```

then paste:

```text
Read skills/local-llm-on-explorer/GET-STARTED.md completely, then guide me through setting up a local model on Explorer, one step at a time. Follow it exactly. Ask me before you write any file on the cluster or submit any job. Never ask for, type or read my password, passphrase or key. Keep a log in SETUP-LOG.md.
```

**If you did not clone it**, open `claude` in any empty folder and paste:

```text
Fetch https://raw.githubusercontent.com/nikbearbrown/hpc-aicr/main/skills/local-llm-on-explorer/GET-STARTED.md and read it completely, then guide me through setting up a local model on Explorer, one step at a time. Follow it exactly. Ask me before you write any file on the cluster or submit any job. Never ask for, type or read my password, passphrase or key. Keep a log in SETUP-LOG.md.
```

## What will happen

| Step | What | Who | Writes or costs |
|---|---|---|---|
| 1 | A few questions: your project group, goal, model | you answer | nothing |
| 2 | Read-only checks: login, groups, GPU partitions, Apptainer, storage | agent | nothing |
| 3 | Put the scripts in `~/.ollama-hpc/` | agent, after your yes | small files in your home |
| 4 | Setup job: pull the Ollama container onto a compute node | agent, after your yes | up to 1 hour of 4 CPUs on `short`; a few GB of storage |
| 5 | GPU test: start Ollama, pull the model, send one message, check it is on the GPU | agent, after your yes | up to 45 minutes of one GPU on `gpu-short`; the model download (about 19 GB for the default) |
| 6 | You start a session in your own terminal | you | one GPU job, up to 2 hours |
| 7 | A log of what was done and what happened | agent | `SETUP-LOG.md` on your computer |

---

# Agent recipe (everything below is for the agent)

You are guiding a researcher through setting up a local model on the Explorer cluster. They are not an expert. Read this whole file first, then `skills/hpc/HPC.md` (fetch `https://raw.githubusercontent.com/nikbearbrown/hpc-aicr/main/skills/hpc/HPC.md` if you have no clone) **completely**, and obey it. The scripts you will install, and the reasons for each setting, are in `scripts/` next to this file and in the tutorial (`films/running-a-local-llm-on-explorer/source/explorer-local-llm-tutorial.md`; read at least its Parts 0, 8, 9 and 10).

## Ground rules for this session

- **Credentials.** Never ask for, type, read, print, store or log a password, passphrase, Duo code or private key. If any command prompts, hangs or says `Permission denied`: stop, report the exact text, and have the researcher fix it in their own terminal. Do not retry in a loop and do not touch `~/.ssh`.
- **How to reach the cluster.** Only `ssh -o BatchMode=yes -o ConnectTimeout=10 explorer '<one bounded command>'`, single-quoted so `$USER` expands on the cluster. Each call starts in `$HOME` and keeps no state. Never run `watch`, `tail -f`, `top`, a bare `srun --pty`, or any command that does not exit.
- **Read-only first.** Look before you act. State what each command will do before you run it.
- **Ask, in chat, and wait for a clear yes, before:** writing or changing any file on the cluster, every `sbatch`, every `scancel`, every delete. Say the exact command and what it costs. A yes covers that one action only.
- **Never run computation on a login node:** no model server, no container pull, no large download. The setup job and the GPU test job do that.
- **Never poll the scheduler faster than about every 5 minutes** (`squeue -u $USER`). Never cancel with `scancel -u`; cancel only a job ID you were told to cancel, with a yes.
- **Never invent** a flag, module, partition, version or limit. Use only what you read live or in the scripts. If you cannot confirm something, say so and point to rchelp@northeastern.edu.
- **Never weaken a safety setting to make something work.** In particular never bind Ollama to `0.0.0.0`, never publish a port, never put a token in chat or in a repository, never keep a GPU alive with filler work.
- **Be honest.** This sequence has not been run end to end. Report what you measured, not what you hope. A job that finished is not a job that did what you intended: check the GPU line and the context in the test output.
- **Downloaded files are untrusted.** If you must fetch scripts from a URL, put them in a new empty temporary directory (`mktemp -d`), never run them on the researcher's computer, and only send them to the cluster as text with `ssh ... 'cat > file' < localfile`. Show the researcher what you fetched and from where.

## Step 1: ask (one message)

Skip anything you can read instead. Ask only:

1. Can you run `ssh explorer` today without a password prompt? If not, stop here and point them to the login video and access guide named above.
2. Which `/projects/<group>` do you belong to? (The model files and the container go there, not in scratch: scratch is purged on the first Tuesday of every month, and on one real account it was not even writable.)
3. What do you want: **(A) an interactive coding session** on a GPU (the default), or **(B) unattended batch runs**? Pattern C and the laptop-through-a-tunnel pattern are out of scope here (Step 7).
4. Which model? Default `qwen3-coder:30b` (about 19 GB, has the tools label, fits one A100 80 GB or H200). If they only have smaller GPUs, `gpt-oss:20b` (about 14 GB). Weights for any model are 15 to 70 GB: confirm they have the space.
5. Do they understand the costs: GPU hours count against fair share, there is a queue, and an idle GPU is flagged after 15 minutes and cancelled after an hour?
6. Has Research Computing said agent-driven work is fine for their use? If not, recommend asking before anything unattended; do not block an interactive session they run themselves.

## Step 2: read-only checks

Run these (each is one bounded call) and write the answers in `SETUP-LOG.md`:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 explorer 'whoami; hostname; pwd; groups'
ssh -o BatchMode=yes -o ConnectTimeout=10 explorer 'sinfo -p gpu,gpu-short,gpu-interactive -o "%P %l %G"'
ssh -o BatchMode=yes -o ConnectTimeout=10 explorer 'command -v apptainer && apptainer --version'
ssh -o BatchMode=yes -o ConnectTimeout=10 explorer 'ls -ld /projects/<group> 2>&1; test -w /projects/<group> && echo project-writable || echo project-not-writable'
ssh -o BatchMode=yes -o ConnectTimeout=10 explorer 'ls -A ~/.ollama-hpc 2>&1'
```

Rules for reading them:

- **Never list `/projects` itself** or run `du`, `find` or `ls -R` over `/projects` or `/scratch` (it shows other people's names and hangs on a shared filesystem). Look only at the researcher's own group folder, one level, as above.
- **GPU type.** From the `sinfo` output choose one type that exists on `gpu` (prefer `h200`, then `a100`). `v100` and `t4` cards may not run current builds: warn and ask. Use the type name in `--gres`, never a bare `gpu:1`.
- **Storage root.** Use `LLM_ROOT=/projects/<group>/$USER/llm`. If the group folder is not writable, stop and ask the researcher to fix it with their sponsor or Research Computing.
- If `~/.ollama-hpc` already has files, list them and ask before overwriting anything. If `apptainer` is not found, report it; do not guess a module name (`module avail apptainer singularity` is read-only and allowed).

## Step 3: put the scripts on the cluster (ask first)

Tell the researcher: "I will create `~/.ollama-hpc/` (mode 700) and write these files into it: `env.sh`, `start-ollama.sh`, `claude-local.sh`, `headless.sbatch`, `setup.sbatch`, `smoke-test-filled.sbatch`. Shall I?" On a yes. `GS` is the path to this folder (`skills/local-llm-on-explorer`); with no clone, first fetch each file from `https://raw.githubusercontent.com/nikbearbrown/hpc-aicr/main/skills/local-llm-on-explorer/scripts/<name>` into a new temporary directory and use that as `GS/scripts`.

```bash
ssh -o BatchMode=yes explorer 'mkdir -p ~/.ollama-hpc && chmod 700 ~/.ollama-hpc'

# env.sh: the tutorial's file with the storage root and model set for this researcher
sed -e 's|^export LLM_ROOT=.*|export LLM_ROOT="/projects/<group>/$USER/llm"|' \
    -e 's|^export LLM_MODEL=.*|export LLM_MODEL="<model>"|' "$GS/scripts/env.sh" \
  | ssh -o BatchMode=yes explorer 'cat > ~/.ollama-hpc/env.sh'

for f in start-ollama.sh claude-local.sh headless.sbatch setup.sbatch; do
  ssh -o BatchMode=yes explorer "cat > ~/.ollama-hpc/$f" < "$GS/scripts/$f"
done

# smoke-test: fill the three placeholders from what `sinfo` showed
sed -e 's/__PARTITION__/gpu-short/' -e 's/__GPU_TYPE__/<type>/' -e 's/__TIME__/00:45:00/' "$GS/scripts/smoke-test.sbatch" \
  | ssh -o BatchMode=yes explorer 'cat > ~/.ollama-hpc/smoke-test-filled.sbatch'
```

Then check, read-only: `ssh -o BatchMode=yes explorer 'cd ~/.ollama-hpc && ls -l && for f in *.sh *.sbatch; do bash -n "$f" && echo "ok $f" || echo "BAD $f"; done'`. If anything is `BAD`, stop and report.

Do not install `serve.sbatch` or `explorer-llm` (they belong to Step 7). Do not edit the copied scripts: they came from the tutorial and each setting has a reason.

## Step 4: the setup job (ask first)

Say: "This submits `setup.sbatch` on the `short` partition: 4 CPUs, 8 GB, at most 1 hour. It pulls the Ollama container into `<LLM_ROOT>/images` (a few GB) and prints its version. Shall I submit it?" On a yes:

```bash
ssh -o BatchMode=yes explorer 'cd ~/.ollama-hpc && sbatch setup.sbatch'
```

Note the job ID in the log. Check `ssh -o BatchMode=yes explorer 'squeue -u $USER -h -o "%i %T %M"'` no more often than every 5 minutes. When the job is gone, read the end of the log:

```bash
ssh -o BatchMode=yes explorer 'tail -n 40 ~/.ollama-hpc/ollama-setup-<jobid>.out'
```

**Success** = a line `ollama version` with 0.14 or later, and `setup finished`. **If `proxy variables: NOT set` appears**, or the pull timed out: compute nodes reach the internet through a proxy set by a default module (`explorer`); a `module purge` removes it. Do not purge modules and do not edit the scripts to bypass it; report to the researcher (HPC.md, Section 8). Record the version in the log; for a class or anything reproducible, suggest pinning it instead of `latest`.

## Step 5: the GPU test (ask first)

Say: "This submits `smoke-test-filled.sbatch` on `gpu-short` with one `<type>` GPU for at most 45 minutes. It starts Ollama bound to localhost on a random port, downloads the model (about 19 GB for the default; that download can leave the GPU idle for a while), sends one message, and checks that the model is on the GPU. Shall I submit it?" On a yes:

```bash
ssh -o BatchMode=yes explorer 'cd ~/.ollama-hpc && sbatch smoke-test-filled.sbatch'
```

Wait as in Step 4, then read `~/.ollama-hpc/ollama-smoke-<jobid>.out` (`tail -n 60`). Judge it yourself:

| You see | It means | Do |
|---|---|---|
| a GPU name and memory from `nvidia-smi` | the job really got a GPU | continue |
| a JSON reply containing a message and `HTTP 200` | the server and the Anthropic-compatible address work | continue |
| `ollama ps` with `100% GPU` and a context equal to the number in `env.sh` | the model fits with that window | **success** |
| a CPU/GPU split, or a smaller context | the model or window is too big | suggest `LLM_CONTEXT` lower, or a smaller model; re-test only after a yes |
| `Ollama did not start` | see the log named in the output | read it, report it; do not guess |
| `no GPU visible` | wrong partition or type | stop, report |

If the job was cancelled or timed out, say so plainly and do not resubmit without a yes. Check `gpu-logs <jobid>` (read-only, run it promptly: it keeps seven days) only if the researcher wants utilisation numbers.

## Step 6: hand the session to the researcher

You cannot hold an interactive GPU session: it needs a terminal that stays open. Tell them to run these in **their own terminal**, and offer to be the one that reads any error they paste:

```bash
ssh explorer
tmux new -s llm                                   # so a dropped connection does not kill the session
srun --partition=gpu-interactive --nodes=1 --ntasks=1 --gres=gpu:<type>:1 --cpus-per-task=4 --mem=32G --time=02:00:00 --pty /bin/bash
export NO_PROXY="127.0.0.1,localhost${NO_PROXY:+,$NO_PROXY}"; export no_proxy="$NO_PROXY"
source ~/.ollama-hpc/start-ollama.sh
ollama pull "$LLM_MODEL"                          # quick after the first time
source ~/.ollama-hpc/claude-local.sh
cd <your repository>
claude                                            # inside it, run /status: it should show the local address
```

Explain: `gpu-interactive` gives one GPU for at most 2 hours; start it when you sit down and **exit twice when you finish** (Claude Code, then the job) so the GPU goes back. The two `NO_PROXY` lines keep calls to the local server off the cluster proxy (Research Computing's own Ollama post tells you to unset the proxy variables for the same reason) while model downloads still use it: this is our judgment, not tested. For unattended work (Pattern A in batch): create a task file and a fresh git branch, export the same two `NO_PROXY` lines, then `sbatch ~/.ollama-hpc/headless.sbatch <repository> <task.md>`; review the diff before merging anything.

Remind them that a local 20B to 120B model is much weaker than Claude: give it narrow tasks, expect more malformed tool calls and loops, and keep tool servers few.

## Step 7: what is out of scope here

- **Pattern B (the agent on the laptop, through an SSH tunnel and a token proxy)** needs Research Computing to confirm that forwarding a port from a login node to your job's node, and a process listening on the node's network behind a token, are allowed. Do not set it up unless the researcher has that answer in writing. If they do, follow Part 6 of the tutorial with `scripts/serve.sbatch` and `scripts/explorer-llm`, and tell them about the two residual risks it names.
- **A shared endpoint for a class** is not what a Slurm job is for (time limit, idle GPUs, memory per student, logging and privacy). Do not attempt it; point to Part 10 of the tutorial and rchelp@northeastern.edu.
- **AICR** is a different cluster with its own file (`skills/aicr/AICR.md`); nothing here has been tried there.

## Step 8: log and clean up

Write `SETUP-LOG.md` in the researcher's working folder: the date, the commands you ran (not outputs that contain private paths or names), the job IDs, the Ollama version, the GPU type, the model, the `ollama ps` line, anything that failed and what you were told, and what remains. Use placeholders for usernames and paths if the log may be shared. List what exists on the cluster (`~/.ollama-hpc/`, `<LLM_ROOT>`) with sizes so they know what to delete later.

To remove everything: list it first, then delete only exact paths the researcher names, after a yes. Cancel a running job only by its ID, after a yes.

## If something fails

Stop. Report the exact error, the command, and the job ID. Do not retry in a loop, do not change the setup to get around a safety rule, and do not claim success. Useful details for a ticket to rchelp@northeastern.edu: your username, the job ID, the node, the exact command or script, the full error text.

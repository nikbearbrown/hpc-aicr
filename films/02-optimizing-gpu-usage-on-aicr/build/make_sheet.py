#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-aicr-optimizing-gpu-usage.

LECTURE (brutalist.art/skills/make/lecture/SKILL.md): the WHOLE workshop document as one
act-structured film, primarily visual, best visual per beat, tools shown as themselves.

Source: hpc/AICR-Optimizing-GPU-Usage/aicr-gpu-optimization.md (Northeastern Research Computing,
AICR Training Workshop 2, presenter Arsalan Akhter; github.com/northeastern-rc-training/
AICR-Optimizing-GPU-Usage). Real evidence: Bear's own finished job 318592 on AICR, read with
`jobstats` (read-only) on 2026-10-06. Second film of the AICR lecture series; same cast as the first.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Optimizing GPU Usage on AICR"
FPS = 30
SPARSE = ("lecture, isometric lane (show-tell drawing laws): one drawn scene on a cream stage with a few labels, "
          "the voice carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame "
          "and contrast still apply.")


def manim(bid, act, narration, cls, image, show, sparse=False):
    b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                  "manim": {"class": cls}, "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="remotion", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


def code(bid, act, narration, title, src, spark, show):
    return remotion(bid, act, narration, "ClaudeCodeBeat",
                    {"title": title, "code": src, "language": "bash" if ".slurm" in title else "python",
                     "largeText": True, "sparkLine": spark}, show,
                    motion_claim="The real code from the workshop prints line by line.")


def shell(bid, act, narration, lines, show, start=20, gap=40, title="ssh — login.aicr.ai"):
    return remotion(bid, act, narration, "CCPlainShell",
                    {"title": title, "lines": lines, "startCue": start, "lineGap": gap}, show,
                    motion_claim="The real commands land in order; output appears only where it was really captured.")


A1, A2, A3, A4, A5, A6, A7, A8 = ("I · Do You Have The GPU?", "II · Seeing The GPU Live", "III · The Profiling Toolchain",
                                  "IV · Data Starvation", "V · Memory vs Utilization", "VI · More Than One GPU",
                                  "VII · The Loop", "VIII · Your Domain")

OPEN = [
 remotion("BIDEA", "the idea",
    "Bonjour. This is Liam, in for Bear. First, a correction. A GPU job that finished is not a GPU job that used the "
    "GPU. Many jobs leave the card waiting most of the time. This lecture is a set of measuring instruments: how to "
    "confirm you have the GPU, how to watch it live, how to profile it, how to fix the usual bottleneck, how to read "
    "memory against utilization, when to add GPUs, and the loop that ties it all together. Measure first. Change second.",
    "BrutalistHesitantWriter",
    {"text": "My GPU job finished,\nso the GPU was busy", "triggerWords": "so the GPU was busy",
     "replacementWords": "but was the GPU busy", "fontSize": 70, "charMs": 62, "hesitateBetween": 6,
     "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'My GPU job finished, so the GPU was busy'"},
     {"at": 0.3, "event": "backspaces 'so the GPU was busy' -> 'but was the GPU busy'"}],
    lane="bookend", lead_silence_s=0.8,
    motion_claim="The writer types the assumption (finished, so busy) and corrects it into the question (but was it busy).",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. GPU utilization: the share of the last second in which the GPU was running any work at all. VRAM: the "
    "GPU's own memory, where your model and your batch live. DataLoader: the part of PyTorch that reads and batches "
    "your data and hands it to the GPU. Profiler: a tool that says where the time went. BF16: a sixteen-bit number "
    "format that keeps the range of thirty-two-bit floats. And DDP: distributed data parallel, one model copy per GPU.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "GPU utilization", "meaning": "share of the last second in which the GPU ran any work at all"},
               {"term": "VRAM", "meaning": "the GPU's own memory, where your model and your batch live"},
               {"term": "DataLoader", "meaning": "the PyTorch part that reads, batches and hands data to the GPU"},
               {"term": "profiler", "meaning": "a tool that says where the time went"},
               {"term": "BF16", "meaning": "a 16-bit number format that keeps the range of 32-bit floats"},
               {"term": "DDP", "meaning": "distributed data parallel: one model copy per GPU"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "'GPU utilization'"}, {"at": 0.25, "event": "'VRAM'"}, {"at": 0.4, "event": "'DataLoader'"},
     {"at": 0.58, "event": "'profiler'"}, {"at": 0.72, "event": "'BF16'"}, {"at": 0.87, "event": "'DDP'"}],
    gate="CARD", lane="bookend", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

SLURM_MIN = """#!/bin/bash
#SBATCH --job-name=my_training
#SBATCH --partition=b200-batch   # or rtx-batch
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8        # num_workers + 1
#SBATCH --gres=gpu:1
#SBATCH --mem=32G                # CPU RAM, not VRAM
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err"""
SLURM_WORK = """mkdir -p logs
module purge
module load cuda/13.1
module load miniforge3/25.3.0-3
source activate aicr_gpu_workshop
python train.py"""

PROFILER = """from torch.profiler import profile, ProfilerActivity

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    record_shapes=True,
    on_trace_ready=torch.profiler.tensorboard_trace_handler('./prof')
) as prof:
    for step, (x, y) in enumerate(dataloader):
        if step == 20:
            break          # short window: 10-20 steps is enough
        out  = model(x)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        prof.step()

print(prof.key_averages().table(sort_by='cuda_time_total', row_limit=15))"""
PROFILER_A, PROFILER_B = PROFILER.split("\n    for step", 1)
PROFILER_B = "    for step" + PROFILER_B

DIAG = """# Time just the data loading (no GPU work)
t0 = time.perf_counter()
for i, (x, y) in enumerate(loader):
    if i >= 50:
        break
loader_ms = (time.perf_counter() - t0) / 50 * 1000"""
DIAG_B = """# Time just the compute (synthetic data, bypass the loader)
dummy_x = torch.randn(256, 3, 224, 224, device='cuda')
torch.cuda.synchronize()
t0 = time.perf_counter()
for _ in range(50):
    out = model(dummy_x)
    out.sum().backward()
    torch.cuda.synchronize()
compute_ms = (time.perf_counter() - t0) / 50 * 1000

# If loader_ms > compute_ms, you are DATA BOUND."""

LOADER = """from torch.utils.data import DataLoader

loader = DataLoader(
    dataset,
    batch_size=256,
    num_workers=7,             # cpus-per-task minus 1
    pin_memory=True,           # always True on GPU training
    persistent_workers=True,   # keep workers alive between epochs
    prefetch_factor=2,         # batches each worker pre-loads
)"""

BSEARCH = """def fits_in_vram(model, batch_size, input_shape=(3, 224, 224)):
    try:
        x = torch.randn(batch_size, *input_shape, device='cuda')
        out = model(x)
        out.sum().backward()
        torch.cuda.empty_cache()
        return True
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        return False

lo, hi = 1, 4096
while lo < hi:
    mid = (lo + hi + 1) // 2
    if fits_in_vram(model, mid):
        lo = mid
    else:
        hi = mid - 1
print(f'Maximum batch size: {lo}')"""

BF16 = """from torch.amp import autocast

# Before (FP32)
out  = model(x)
loss = criterion(out, y)
loss.backward()

# After (BF16): add exactly this wrapper
with autocast(device_type='cuda', dtype=torch.bfloat16):
    out  = model(x)
    loss = criterion(out, y)
loss.backward()   # gradients stay in FP32"""

CKPT = """# Hugging Face Transformers: one flag
model.gradient_checkpointing_enable()

# Custom PyTorch modules
from torch.utils.checkpoint import checkpoint

class MyBlock(torch.nn.Module):
    def forward(self, x):
        return checkpoint(self.expensive_layers, x,
                          use_reentrant=False)"""

DDP = """# Check: does your code use DDP?
import torch.distributed as dist
print(dist.is_available())     # must be True
print(dist.is_initialized())   # True after init_process_group()

# Check: how many GPUs does PyTorch see?
import torch
print(torch.cuda.device_count())   # should match --gres=gpu:N"""
DDP_B = """# For DDP on AICR
#SBATCH --ntasks-per-node=4      # one task per GPU
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=8        # CPU workers per GPU process
torchrun --nproc_per_node=4 train_ddp.py"""

SCALE = """# At the end of the first epoch (on rank 0 only):
if dist.get_rank() == 0:
    throughput = total_samples / elapsed_seconds
    efficiency = throughput / (world_size * single_gpu_baseline) * 100
    print(f'World size: {world_size}  |  {throughput:.0f} samples/sec  |  '
          f'Scaling efficiency: {efficiency:.0f}%')"""

HF = """from transformers import TrainingArguments

args = TrainingArguments(
    bf16=True,                      # mixed precision
    gradient_checkpointing=True,    # if memory is tight
    dataloader_num_workers=8,       # feed the GPU
    dataloader_pin_memory=True,     # fast transfers
    ...
)"""

B = [
 # ───────── ACT I · Do you have the GPU?
 manim("B10", A1,
    "Start where the work can quietly go wrong. If the CUDA module isn't loaded, PyTorch runs on the CPU and raises "
    "no error at all. A typo in the GPU request lands you on the wrong kind of node. And a leftover CUDA visible "
    "devices setting from an earlier shell can hide the card you were given.",
    "B10_SilentFailures",
    "Three small scenes land in a row on the same stage: a job box slides onto a grey CPU block while a dark GPU block beside it stays unlit (no alarm); a job box lands on the wrong rack; a ghost tag labelled 'CUDA_VISIBLE_DEVICES' covers a GPU light. Act title top-left.",
    [{"at": 0.15, "event": "job lands on the CPU, GPU stays dark"}, {"at": 0.5, "event": "wrong node"}, {"at": 0.8, "event": "stale tag hides the GPU"}]),
 manim("B11", A1,
    "AICR has two GPU families and four GPU partitions. B200 devel and B200 batch, with one hundred ninety-two gigabytes "
    "of memory per card. RTX devel and RTX batch, with ninety-six. Devel partitions run four hours and are for "
    "interactive work and profiling. Batch partitions run twenty-four hours and are for production.",
    "B11_PartitionTable",
    "A drawn table builds row by row: partition, GPU, VRAM, max walltime, purpose. Rows: b200-devel, b200-batch, rtx-devel, rtx-batch. VRAM bars drawn beside the numbers: 192 GB twice the length of 96 GB.",
    [{"at": 0.2, "event": "B200 rows"}, {"at": 0.45, "event": "RTX rows"}, {"at": 0.7, "event": "devel: 4 h"}, {"at": 0.88, "event": "batch: 24 h"}]),
 shell("B12", A1,
    "A minimal job script. The request first: one node, one task, eight CPUs per task, one GPU, thirty-two "
    "gigabytes of memory, four hours, and the log files.",
    ["$ cat my_training.slurm", "#!/bin/bash", "#SBATCH --job-name=my_training", "#SBATCH --partition=b200-batch",
     "#SBATCH --nodes=1", "#SBATCH --ntasks=1", "#SBATCH --cpus-per-task=8", "#SBATCH --gres=gpu:1",
     "#SBATCH --mem=32G", "#SBATCH --time=04:00:00", "#SBATCH --output=logs/%x_%j.out", "#SBATCH --error=logs/%x_%j.err"],
    [{"at": 0.1, "event": "the request lines print"}], start=15, gap=22),
 shell("B12B", A1,
    "Then the work. Make the logs folder, clear the modules, load CUDA and miniforge, activate the workshop "
    "environment, and run your training.",
    ["$ mkdir -p logs", "$ module purge", "$ module load cuda/13.1", "$ module load miniforge3/25.3.0-3",
     "$ source activate aicr_gpu_workshop", "$ python train.py"],
    [{"at": 0.1, "event": "the work lines run"}], start=15, gap=36),
 manim("B13", A1,
    "Two lines deserve a pause. Mem equals thirty-two gigabytes is CPU memory, not GPU memory. The GPU's own memory "
    "comes with the GPU. And CPUs per task is not a formality: your data loading workers run on those cores. Eight "
    "cores means seven workers and one main process.",
    "B13_RamVsVram",
    "Left: a grey CPU block with a kraft RAM box labelled '32G · CPU RAM'; right: a dark GPU block with its own larger dark memory slab labelled 'VRAM'. Then eight small core pads under the CPU: seven light up as 'workers', one as 'main'.",
    [{"at": 0.2, "event": "32G sits on the CPU side"}, {"at": 0.45, "event": "VRAM comes with the GPU"}, {"at": 0.75, "event": "eight cores: seven workers, one main"}]),
 manim("B14", A1,
    "Never trust that you got what you asked for. The workshop's verify script runs in under five seconds and checks "
    "five things. Is CUDA reachable. How many GPUs, which model, how much memory. What CUDA visible devices says. "
    "Does NVIDIA S M I agree. And a tensor round trip: CPU to GPU and back. Is available only means PyTorch can see a "
    "GPU. The round trip proves it can use it.",
    "B14_VerifyFive",
    "A mono label '01_gpu_verify.py'; five check rows land one by one with short labels (CUDA reachable · GPUs, model, VRAM · CUDA_VISIBLE_DEVICES · nvidia-smi agrees · round trip); on 'round trip' a small kraft tensor box travels CPU → GPU → CPU along a cable and a check lands.",
    [{"at": 0.2, "event": "five checks land"}, {"at": 0.7, "event": "tensor round trip CPU → GPU → CPU"}, {"at": 0.95, "event": "check"}]),
 manim("B15", A1,
    "About that variable. Slurm sets CUDA visible devices to tell your program which GPUs are yours. Zero means one "
    "GPU. Zero comma one means two. Not set means you're outside Slurm, in an interactive shell, which is normal. "
    "Never override it in your script unless you deliberately want a subset.",
    "B15_VisibleDevices",
    "Three mono rows land: 'CUDA_VISIBLE_DEVICES=0' with one GPU block lit, '=0,1' with two lit, 'NOT SET' with a plain shell window; a terracotta strike lands over a 'export CUDA_VISIBLE_DEVICES=...' line in a script.",
    [{"at": 0.25, "event": "=0: one GPU"}, {"at": 0.4, "event": "=0,1: two"}, {"at": 0.55, "event": "NOT SET: outside Slurm"}, {"at": 0.85, "event": "never override"}]),
 manim("B16", A1,
    "One AICR-specific rule. A background process watches GPU utilization, and a job that holds a GPU without "
    "running anything is cancelled. So don't request a GPU and then sit writing code. Run the verify script first, "
    "profile in the devel partition in short sessions, and keep the batch partitions for jobs that are already tuned.",
    "B16_IdleCancel",
    "A utilization line runs flat at zero while a job box sits on a lit GPU; a watcher marker reaches the flat stretch, the job is struck out and removed, and the GPU goes to the next job in the queue. Labels: 'GPU utilization', 'idle', 'cancelled'.",
    [{"at": 0.2, "event": "flat line"}, {"at": 0.45, "event": "cancelled"}, {"at": 0.7, "event": "the GPU goes to the next job"}]),
 # ───────── ACT II · Seeing the GPU live
 manim("B20", A2,
    "The fastest profiler is already on every node. NVIDIA S M I prints a snapshot; watch it every second in a second "
    "terminal. Two numbers matter. GPU utilization: eighty-four percent here means the GPU was running kernels for "
    "eighty-four percent of the last second. Healthy. Below fifty, something is wrong. And memory: twenty-four gigabytes "
    "of one hundred ninety-two in use. Twelve percent. Enormous room for a bigger batch.",
    "B20_NvidiaSmi",
    "A dark terminal panel with the workshop's sample nvidia-smi rows in mono (GPU 0 NVIDIA B200 · 52C 387W / 1000W · 84% · Memory 24576MiB / 196608MiB), typed on '$ watch -n 1 nvidia-smi'; a terracotta ring lands on '84%' then on the memory figures; small labels 'utilization' and '12% of VRAM' beside them. Act title top-left.",
    [{"at": 0.1, "event": "watch -n 1 nvidia-smi"}, {"at": 0.4, "event": "ring on 84%"}, {"at": 0.8, "event": "ring on memory: 12%"}]),
 manim("B21", A2,
    "A quick quiz from the workshop. Utilization twelve percent, memory ninety-one percent. What's wrong? The model "
    "is loaded, the card is full, and it's barely computing. Nothing on the CPU side is feeding it. That is data "
    "starvation, the most common problem of all, and it gets its own act.",
    "B21_TwoGauges",
    "Two gauges side by side: 'utilization' fills to 12% and stays low; 'memory' fills to 91%; a job box sits loaded on a GPU while an empty conveyor from a CPU block brings nothing; label 'starved'.",
    [{"at": 0.15, "event": "12% and 91%"}, {"at": 0.55, "event": "loaded but idle"}, {"at": 0.85, "event": "starved"}]),
 manim("B22", A2,
    "Hold these two numbers as two axes, because people confuse them. Across: utilization. Up: memory. Top left is a "
    "loaded model that isn't running: a data pipeline problem. Bottom left is a GPU doing nothing at all. Bottom right "
    "is good throughput with memory to spare. Top right is the target: a big model, working hard. Eighty to a hundred "
    "percent utilization, seventy to ninety percent memory.",
    "B22_TwoAxes",
    "A 2×2 grid draws: x-axis 'utilization', y-axis 'memory'; quadrants land as named with a job-box-and-GPU miniature in each (idle box, dark card, lit card with spare memory, full card lit); the top-right cell gets the terracotta ring and 'target'.",
    [{"at": 0.2, "event": "axes"}, {"at": 0.4, "event": "top left: loaded, idle"}, {"at": 0.55, "event": "bottom left: nothing"}, {"at": 0.7, "event": "bottom right: headroom"}, {"at": 0.85, "event": "top right: target"}]),
 shell("B23", A2,
    "For a richer live view, N V I top. A dashboard that updates continuously, per process: GPU use, memory trend, power "
    "and temperature. On a shared node it answers the question that matters: is it my Python process using the GPU, "
    "or someone's leftover.",
    ["$ pip install nvitop   # if not in your environment", "$ nvitop",
     "# per-process GPU usage, memory trend,", "# power draw and temperature",
     "# confirm it is YOUR python process on the GPU"],
    [{"at": 0.1, "event": "install"}, {"at": 0.3, "event": "nvitop"}, {"at": 0.6, "event": "what it shows"}], start=30, gap=70),
 # ───────── ACT III · The profiling toolchain
 manim("B30", A3,
    "NVIDIA S M I tells you that there's a problem. A profiler tells you where the time goes. There are layers. System "
    "level: NVIDIA S M I and N V I top. Is the GPU busy. Framework level: the PyTorch profiler. Which operator or layer "
    "eats the GPU time. Timeline: N-sight Systems. Every CPU thread, kernel and memory copy in order. And kernel level: "
    "N-sight Compute. Is one kernel memory-bound or compute-bound. Most problems show up on the first two rungs.",
    "B30_FourLayers",
    "A ladder builds rung by rung from the bottom: 'system · nvidia-smi, nvitop', 'framework · PyTorch Profiler', 'timeline · nsys', 'kernel · ncu'; each rung carries a one-word question label; the two lowest rungs get a terracotta mark on 'first two rungs'. Act title top-left.",
    [{"at": 0.25, "event": "system rung"}, {"at": 0.4, "event": "framework"}, {"at": 0.55, "event": "timeline"}, {"at": 0.7, "event": "kernel"}, {"at": 0.92, "event": "the first two rungs marked"}]),
 manim("B31", A3,
    "The habit that matters most on AICR: profile in devel, run production in batch. In a B200 devel session you run "
    "the verify script, run your code for fifty to a hundred steps, profile, fix the bottleneck, and profile again "
    "until utilization is above seventy percent. Only then does the job go to B200 batch, unattended, and you read "
    "jobstats when it finishes.",
    "B31_DevelToBatch",
    "Two lanes: left lane 'b200-devel · srun' with steps landing downward (verify · 50–100 steps · profile · fix · re-profile · > 70%); a belt carries the job box across to the right lane 'b200-batch · sbatch' (run · jobstats). Same job box as B16.",
    [{"at": 0.15, "event": "devel lane"}, {"at": 0.35, "event": "verify, short run, profile, fix"}, {"at": 0.7, "event": "> 70%: cross to batch"}, {"at": 0.9, "event": "jobstats"}]),
 code("B32", A3,
    "The PyTorch profiler needs no extra install. Open a profile that records CPU and CUDA activity, records the "
    "tensor shapes, and writes a trace you can open in TensorBoard.",
    "profile_window.py — open the profiler", PROFILER_A, "CPU and CUDA, shapes, a trace.",
    [{"at": 0.1, "event": "the profile() block prints"}]),
 code("B32B", A3,
    "Then the pattern that matters: profile a short window, never the full run. Twenty steps is enough. Step the "
    "profiler each iteration, and print the table sorted by total CUDA time. The top row is where you look first.",
    "profile_window.py — a short window", PROFILER_B, "Twenty steps, sorted by CUDA time.",
    [{"at": 0.1, "event": "the loop and the table print"}]),
 manim("B33", A3,
    "Reading it, in order. Gaps between kernels on the timeline: the GPU is idle, the CPU is too slow. Large copy "
    "entries: data shuttling between CPU and GPU. CPU total far above CUDA total: the work isn't really on the GPU. "
    "And DataLoader functions at the top of the CPU table: the pipeline, again.",
    "B33_ReadTheTrace",
    "A kernel timeline draws: dark kernel blocks with visible gaps, the gaps ring in terracotta ('idle'); a long bar labelled 'aten::copy_' grows; two bars 'CPU total' and 'CUDA total' grow with CPU far longer; a table row 'DataLoader' slides to the top of a small list.",
    [{"at": 0.15, "event": "gaps between kernels"}, {"at": 0.4, "event": "copy_ bar"}, {"at": 0.62, "event": "CPU total >> CUDA total"}, {"at": 0.85, "event": "DataLoader on top"}]),
 shell("B34", A3,
    "When the order of events matters, CPU threads, kernels, memory copies, communication between GPUs, use Nsight "
    "Systems. Trace CUDA, NVTX, the OS runtime, c u D N N and c u BLAS, write the report to scratch, and copy it to your "
    "laptop for the N-sight GUI. Limit the capture to fifty or a hundred steps: a full run makes gigabyte files.",
    ["$ nsys profile \\", "    --trace=cuda,nvtx,osrt,cudnn,cublas \\", "    --output=/scratch/$USER/profile_$(date +%s) \\",
     "    python train.py --max-steps 50", "# then copy the .nsys-rep file to your laptop",
     "$ scp USER@login.aicr.ai:/scratch/USER/profile_*.nsys-rep ./"],
    [{"at": 0.1, "event": "nsys profile"}, {"at": 0.5, "event": "50 steps"}, {"at": 0.8, "event": "scp to the laptop"}], start=30, gap=60),
 # ───────── ACT IV · Data starvation
 manim("B40", A4,
    "Now the number one bottleneck. Picture a high-speed factory: the B200. It finishes a batch in eight milliseconds. "
    "The supply truck, the CPU data loader, takes fifty milliseconds to bring the next one. The factory stops and "
    "waits. Nothing is wrong with the factory. The supply chain can't keep up. And a B200 eats batches far faster "
    "than the cards you may be used to, so a loader that barely kept up elsewhere will starve it here.",
    "B40_Factory",
    "Isometric: a dark machine (GPU) with a stamping press and a timer '8 ms'; a kraft truck (loader) crawls along a belt with timer '50 ms'; the press works briefly then holds with its light off; label 'waiting'. Act title top-left.",
    [{"at": 0.2, "event": "the press stamps: 8 ms"}, {"at": 0.4, "event": "the truck crawls: 50 ms"}, {"at": 0.6, "event": "the press waits, light off"}, {"at": 0.9, "event": "waiting"}], sparse=True),
 code("B41", A4,
    "The diagnostic is two timings. First, time fifty batches through the loader alone, with no GPU work at all.",
    "starvation_check.py — the loader", DIAG, "Fifty batches, loader only.",
    [{"at": 0.1, "event": "the loader timing prints"}]),
 code("B41B", A4,
    "Then time fifty forward-and-backward passes on synthetic data, bypassing the loader entirely. If the loader "
    "time is larger than the compute time, you are data bound, and no model optimization will help until that's fixed.",
    "starvation_check.py — the compute", DIAG_B, "Loader time against compute time.",
    [{"at": 0.1, "event": "the compute timing prints"}]),
 manim("B42", A4,
    "The workshop's quiz: loader forty-five milliseconds, compute nine. The GPU works for nine and waits for "
    "thirty-six. Eighty percent of its time, wasted.",
    "B42_FortyFiveNine",
    "Two bars grow on one time axis: 'compute 9 ms' (dark, short) then 'loader 45 ms' (kraft, long); the gap between 9 and 45 fills with a grey hatched 'waiting' span and a hero '80%' lands.",
    [{"at": 0.2, "event": "45 ms and 9 ms"}, {"at": 0.6, "event": "36 ms of waiting"}, {"at": 0.85, "event": "80%"}]),
 code("B43", A4,
    "The fix usually lives in four DataLoader settings. Workers: CPU processes loading in parallel. Pin memory: "
    "page-locked RAM for fast transfer. Persistent workers: don't respawn them every epoch. And prefetch factor: how "
    "many batches each worker loads ahead.",
    "loader.py", LOADER, "Four knobs.",
    [{"at": 0.1, "event": "the DataLoader call prints"}]),
 manim("B44", A4,
    "Typical starting values. Workers: CPUs per task minus one, never zero. Pin memory: always true on a GPU node. "
    "Persistent workers: true whenever workers are above zero. Prefetch: start at two. The single biggest win in the "
    "whole workshop is one line: num workers from zero, the PyTorch default, to four or more. That alone often takes a "
    "job from twenty percent utilization to sixty or eighty.",
    "B44_FourKnobs",
    "Four dials land with labels (num_workers · pin_memory · persistent_workers · prefetch_factor) and their start values (cpus−1 · True · True · 2); then a utilization bar labelled 'num_workers=0' at 20% grows to 60–80% as the first dial turns to 4.",
    [{"at": 0.15, "event": "four dials"}, {"at": 0.7, "event": "num_workers 0 → 4"}, {"at": 0.88, "event": "20% → 60–80%"}]),
 # ───────── ACT V · Memory vs utilization
 manim("B50", A5,
    "Two percentages on the same screen that mean different things. Utilization: the share of the last second the "
    "GPU was running. Low means idle, from data or synchronization. A hundred percent sustained is fine. Memory: the "
    "share of VRAM allocated. Low means you could hold a bigger batch. High is only bad near the edge, where the "
    "job runs out of memory and crashes.",
    "B50_TwoMeters",
    "Two independent gauges with their own needles: 'utilization' sweeps to 100% and gets a check; 'memory' climbs to the top edge where a terracotta 'OOM' mark sits; the needles move independently to show they are not linked. Act title top-left.",
    [{"at": 0.2, "event": "utilization meter"}, {"at": 0.45, "event": "100% sustained is fine"}, {"at": 0.65, "event": "memory meter"}, {"at": 0.9, "event": "OOM at the edge"}]),
 manim("B51", A5,
    "So read them as a pair. Low and low: the GPU is doing nothing; verify CUDA, check the data. Low utilization, "
    "high memory: loaded but not running; fix the pipeline. High utilization, low memory: healthy, with VRAM unused; "
    "increase the batch size. High and high: you're in good shape. And an out-of-memory crash: mixed precision first.",
    "B51_DecisionTable",
    "A drawn table builds row by row: 'what you see' → 'likely cause' → 'first thing to try', five rows, each with two small gauge icons (low/high) drawn instead of words in the first column; the row being read carries the terracotta dot.",
    [{"at": 0.15, "event": "low + low"}, {"at": 0.35, "event": "low util + high memory"}, {"at": 0.55, "event": "high util + low memory"}, {"at": 0.75, "event": "high + high"}, {"at": 0.9, "event": "OOM"}]),
 manim("B52", A5,
    "Batch size moves both axes. Doubling it roughly doubles throughput, as long as the GPU isn't already saturated "
    "and the memory is there. On a B200 with one hundred ninety-two gigabytes, memory sitting at fifteen or twenty "
    "percent means room for four to eight times the batch. Find the ceiling by binary search: try a size, see if it "
    "fits, halve the gap, repeat. Then run production at seventy to eighty-five percent of that ceiling.",
    "B52_BinarySearch",
    "A VRAM bar at 15–20% full; a batch-size axis from 1 to 4096 with a marker that jumps by halving gaps (2048 fits, 3072 fails, 2560 fits, …) landing on the ceiling; the bar fills as the batch grows; a band marks 70–85% of the ceiling as 'production'.",
    [{"at": 0.2, "event": "memory at 15–20%"}, {"at": 0.5, "event": "binary search jumps"}, {"at": 0.85, "event": "70–85% band"}]),
 code("B53", A5,
    "Mixed precision is the next lever. PyTorch defaults to thirty-two-bit floats. Both AICR GPU families have "
    "tensor cores built for lower precision. The change is one wrapper: autocast to b float sixteen around the forward "
    "pass and the loss. Gradients stay in thirty-two bit on their own.",
    "bf16.py", BF16, "One wrapper.",
    [{"at": 0.1, "event": "before and after print"}]),
 manim("B54", A5,
    "Why BF16 and not FP16. A sixteen-bit number splits its bits between exponent, which is range, and mantissa, "
    "which is precision. FP32 has eight exponent bits and twenty-three of mantissa. BF16 keeps the same eight exponent "
    "bits and keeps only seven for precision, so gradients don't underflow and you need no loss scaler. FP16 bets the "
    "other way: ten bits of precision, but only five of exponent, which underflows. FP8 goes further still: four and "
    "three. Every step down trades numerical quality for speed and memory.",
    "B54_BitLadder",
    "Four horizontal bit-bars build, one per format, each split into a dark 'exponent' segment and a grey 'mantissa' segment with counts: FP32 8|23, BF16 8|7, FP16 5|10, FP8 4|3; BF16's exponent segment aligns exactly under FP32's and gets the terracotta mark; FP16's short exponent gets a small 'underflow' label.",
    [{"at": 0.2, "event": "FP32 8|23"}, {"at": 0.4, "event": "BF16 8|7, same exponent"}, {"at": 0.62, "event": "FP16 5|10"}, {"at": 0.78, "event": "FP8 4|3"}, {"at": 0.92, "event": "quality for speed"}]),
 manim("B55", A5,
    "What BF16 buys on this hardware. Activation memory roughly halves, so a much bigger batch fits. Matrix "
    "operations run two to four times faster on the tensor cores. And it is mixed precision, which is the safety net: "
    "the risky parts stay in thirty-two bit. Master weights, the loss, softmax, normalization. Autocast handles that "
    "for you. So the memory saving is partial, and the speedup is largest for matrix multiplies.",
    "B55_MixedSafetyNet",
    "A row of model blocks: activation blocks shrink to half height (label '½'); matmul blocks get a '2–4×' speed tag; four blocks labelled 'weights', 'loss', 'softmax', 'norm' stay full height in FP32 ink while the rest turn to BF16 grey.",
    [{"at": 0.15, "event": "activations halve"}, {"at": 0.35, "event": "2–4× on matmuls"}, {"at": 0.6, "event": "weights, loss, softmax, norm stay FP32"}]),
 code("B56", A5,
    "If memory is still too tight, gradient checkpointing trades compute for memory. Activations aren't stored in the "
    "forward pass; they're recomputed during backpropagation. Roughly sixty to seventy percent less activation memory "
    "for about thirty percent more compute. In Hugging Face it's one call. In custom modules, wrap the expensive layers. "
    "Use it when the batch is forced below eight, or when you're fine-tuning a very large model on one card.",
    "checkpointing.py", CKPT, "Recompute instead of store: −60–70% memory, +30% compute.",
    [{"at": 0.1, "event": "the two snippets print"}]),
 # ───────── ACT VI · More than one GPU
 manim("B60", A6,
    "Multi-GPU is the first thing people reach for when a job is slow, and it's often the wrong move. More GPUs "
    "amplify the efficiency you already have; they don't create it. The eighty percent rule: if a single GPU is "
    "already above eighty percent, you're compute bound, and adding cards divides the work. If it's below sixty, fix "
    "the bottleneck first, because four starved GPUs waste four times as much. And an I/O-bound job gets worse, since "
    "the cards now compete for the same files.",
    "B60_EightyRule",
    "One GPU with a gauge: at > 80% it splits into four lit GPUs each sharing the work (check); then at < 60% the four GPUs each show a mostly-empty gauge and the idle span is counted four times (terracotta ×4). Act title top-left.",
    [{"at": 0.3, "event": "> 80%: four GPUs share the work"}, {"at": 0.6, "event": "< 60%: waste ×4"}, {"at": 0.88, "event": "I/O bound: cards compete"}]),
 manim("B61", A6,
    "Here's what data-parallel training does. Each GPU holds a full copy of the model and takes a different "
    "mini-batch. After the backward pass they all-reduce: they average their gradients into one, and each applies the "
    "same update. Inside one node, over NVLink, that exchange is fast. Across nodes it's slower, so single-node "
    "multi-GPU is usually much faster per card than spreading out.",
    "B61_AllReduce",
    "Three GPU blocks each receive a different batch box (A, B, C) and produce a gradient slab; the three slabs slide to a centre point, merge into one averaged slab, and copies return to all three; a bracket 'one node · NVLink' spans them, and a dashed longer link to a fourth distant block is labelled 'across nodes · slower'.",
    [{"at": 0.2, "event": "three batches, three gradients"}, {"at": 0.45, "event": "all-reduce"}, {"at": 0.7, "event": "same update everywhere"}, {"at": 0.9, "event": "across nodes: slower"}]),
 code("B62", A6,
    "Before you ask for four GPUs, confirm your code is written for DDP. A plain script with gres equals gpu four gets "
    "four cards and uses one. Check that distributed is available and initialized, and that PyTorch sees as many "
    "devices as you requested.",
    "ddp_check.py", DDP, "Four cards allocated is not four cards used.",
    [{"at": 0.1, "event": "the checks print"}]),
 code("B62B", A6,
    "Then the request: one task per GPU, four GPUs, eight CPUs for each GPU's workers, and run it with torchrun.",
    "ddp.slurm", DDP_B, "One task per GPU.",
    [{"at": 0.1, "event": "the DDP request prints"}]),
 manim("B63", A6,
    "And measure the scaling. Throughput divided by the number of GPUs times the single-GPU baseline gives "
    "efficiency. Above eighty percent, the extra cards pay. Seventy to eighty is acceptable overhead. Below seventy, "
    "communication or I/O is the real bottleneck, and more GPUs won't help. Go back to the single card.",
    "B63_ScalingEfficiency",
    "A bar per GPU count (1, 2, 4) grows toward an ideal dashed line; the measured bars fall short and an 'efficiency' label lands on each; a three-band scale (> 80% · 70–80% · < 70%) with the lowest band marked terracotta and an arrow back to the single GPU.",
    [{"at": 0.2, "event": "measured vs ideal"}, {"at": 0.5, "event": "> 80% pays"}, {"at": 0.75, "event": "< 70%: go back"}]),
 # ───────── ACT VII · The loop
 manim("B70", A7,
    "Every section was one bottleneck. In practice they come in that order of frequency, so here's the loop. "
    "Baseline: fifty steps, record throughput and utilization. Profile twenty steps. Diagnose: data, memory, compute, "
    "or communication. Fix one thing. Only one, or you can't tell what helped. Re-profile: did the bottleneck move? "
    "Record the gain. Repeat until utilization is above eighty, or the returns run out.",
    "B70_TheLoop",
    "A ring of seven steps builds clockwise (baseline · profile · diagnose · fix one · re-profile · record · repeat); a marker travels round it; on 'only one' a second fix card tries to join and is pushed out; the ring's exit arrow lands on '> 80%'. Act title top-left.",
    [{"at": 0.2, "event": "seven steps"}, {"at": 0.55, "event": "fix one; the second is pushed out"}, {"at": 0.85, "event": "exit at > 80%"}]),
 manim("B71", A7,
    "The decision guide, as a tree. Utilization under fifty? It's the data pipeline, and if workers is zero, that "
    "first. Fifty to eighty? Look at memory. Under forty percent: bigger batch. Forty to eighty-five: try BF16. Over "
    "ninety: smaller batch or checkpointing. Memory fine? Profile. Above eighty with healthy memory? Consider more GPUs "
    "only if the single card is truly saturated. And out of memory: BF16, then checkpointing, then a smaller batch. "
    "In that order.",
    "B71_DecisionTree",
    "A tree draws from a root 'utilization?' with branches '< 50% → data pipeline', '50–80% → memory?' fanning into four leaves (< 40% batch ↑ · 40–85% BF16 · > 90% batch ↓ / checkpoint · OK → profile), '> 80% → multi-GPU?'; a side branch 'OOM' lists three steps in order; branches light as they are spoken.",
    [{"at": 0.1, "event": "root"}, {"at": 0.25, "event": "< 50%: data"}, {"at": 0.45, "event": "50–80%: memory leaves"}, {"at": 0.75, "event": "> 80%: multi-GPU"}, {"at": 0.9, "event": "OOM order"}]),
 manim("B72", A7,
    "After a batch job finishes, read its report card. Jobstats, from Princeton Research Computing, runs on AICR. "
    "Here is a real one, from a fifty-five-minute fine-tuning job on an RTX card. GPU utilization eighty percent: "
    "healthy. GPU memory seventeen percent: room for a bigger batch. CPU utilization thirteen percent: eight cores "
    "requested, barely one used. And a note: the job needed eleven percent of the eight hours it asked for. Request "
    "less time, and the queue moves faster for everyone. Make this a habit: under sixty percent GPU, fix it before "
    "the next run.",
    "B72_Jobstats",
    "The real report re-composed on cream: '$ jobstats 318592' in mono, header rows (Job Name f5tune-voice · rtx-batch · GPUs 1 · Run Time 00:55:09 · Time Limit 08:00:00), then four utilization bars grow to their real values: CPU 13%, CPU memory 25%, GPU 80%, GPU memory 17%; a terracotta ring on the GPU bar, then on the memory bar, then the note line 'needed 11% of the requested time' lands.",
    [{"at": 0.15, "event": "jobstats 318592"}, {"at": 0.35, "event": "GPU 80%"}, {"at": 0.5, "event": "GPU memory 17%"}, {"at": 0.65, "event": "CPU 13%"}, {"at": 0.8, "event": "11% of requested time"}]),
 manim("B73", A7,
    "The pre-submission checklist, ideally run in a devel session first. The verify script passes. NVIDIA S M I shows "
    "over seventy percent during a fifty-step test. Workers is not zero. Pin memory is on. The batch uses at least "
    "sixty percent of VRAM. BF16 autocast is on. The script names the right partition. CPUs per task is at least four "
    "and matches workers plus one. The logs folder exists. And you've profiled twenty steps and read the CUDA column. "
    "Then cancel the devel session: four running jobs per user is the limit, and an idle one blocks you too.",
    "B73_Checklist",
    "Ten checkbox rows with 1–3 word labels (verify · util > 70% · workers ≠ 0 · pin_memory · batch ≥ 60% VRAM · BF16 · partition · cpus = workers+1 · logs/ · profiled 20) tick one by one; a job box then leaves a devel slot and the slot clears.",
    [{"at": 0.1, "event": "boxes tick in order"}, {"at": 0.88, "event": "the devel slot clears"}]),
 # ───────── ACT VIII · Your domain
 remotion("B80", A8,
    "None of this is PyTorch-only. Deep learning: every section applies, and in Hugging Face most fixes are one flag. "
    "Molecular dynamics: verify the GPU type before a long run, and multi-GPU scales well within a node. LLM inference: "
    "RTX cards for smaller models, B200s for the seventy-billion class. Custom CUDA or Triton kernels: everything "
    "applies, plus N-sight Compute for the kernel itself. And help is one email away: r c help at northeastern dot e d u.",
    "LibraryIconRow",
    {"title": "VIII · Your Domain",
     "items": [{"label": "Deep learning", "sub": "every section applies", "icon": "brain", "cue_phrase": "Deep learning"},
               {"label": "Molecular dynamics", "sub": "verify the card; scale in-node", "icon": "atom", "cue_phrase": "Molecular dynamics"},
               {"label": "LLM inference", "sub": "RTX small, B200 large", "icon": "message-square", "cue_phrase": "LLM inference"},
               {"label": "Custom kernels", "sub": "add Nsight Compute", "icon": "cpu", "cue_phrase": "Custom CUDA"}]},
    [{"at": 0.1, "event": "deep learning"}, {"at": 0.35, "event": "molecular dynamics"}, {"at": 0.55, "event": "LLM inference"}, {"at": 0.75, "event": "custom kernels"}],
    motion_claim="Four domains, each landing as one large library icon as it is named."),
 code("B81", A8,
    "For Hugging Face Transformers the whole workshop is five lines of training arguments: BF16 on, gradient "
    "checkpointing if you need it, eight data loader workers, and pinned memory.",
    "training_args.py", HF, "The workshop as five arguments.",
    [{"at": 0.1, "event": "the arguments print"}]),
]

RECAP = ["Verify the GPU first; idle allocations on AICR get cancelled.",
         "Watch nvidia-smi: under 50% utilization means something is wrong.",
         "Profile 20 steps; the top CUDA-time row is where to look.",
         "Low utilization with high memory is data starvation: fix num_workers.",
         "High utilization with low memory: raise the batch; OOM: BF16 first.",
         "Add GPUs only above 80% on one; measure scaling, read jobstats."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. Verify the GPU before anything else, because idle allocations on AICR get cancelled. "
    "Watch NVIDIA S M I: under fifty percent utilization means something is wrong. Profile twenty steps, and the top "
    "row by CUDA time is where to look. Low utilization with high memory is data starvation: fix the number of "
    "workers. High utilization with low memory: raise the batch size. Out of memory: BF16 first. Add GPUs only when "
    "one is already above eighty percent, measure the scaling, and read jobstats after every run.",
    "ClaudeVerdictArtifact", {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land"}],
    lane="bookend", lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("Here is my PyTorch training loop and my Slurm script: [paste both]. I run it on one GPU. Walk me through the "
             "optimization loop: what to measure for a 50-step baseline, how to profile 20 steps, and which of these to try "
             "first and why: DataLoader num_workers and pin_memory, a larger batch, BF16 autocast, gradient checkpointing, "
             "or a second GPU. Give me the exact code changes for your first pick only.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT + " Then check two things yourself. Did it ask you to measure "
    "before it changed anything? And did it change exactly one thing?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Run The Optimization Loop", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did it ask you to measure before it changed anything?",
                "Check: did it change exactly one thing?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

# Gate V underfill on drawn beats that build progressively: at the sampled 50% frame only half the drawing
# is on stage (measured 32–54% on the first 4K run). Same waiver the isometric lane carries: underfill and
# clustered only; edge-bleed, empty-frame and contrast still apply.
PROGRESSIVE = {"B10", "B11", "B13", "B15", "B33", "B42", "B44", "B55", "B61", "B70", "B71"}
for b in B:
    if b["beat_id"] in PROGRESSIVE and "qc" not in b:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE + " Progressive drawing: the midpoint frame holds only part of the final picture."}
BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Optimizing GPU Usage on AICR. How to request the right GPU, measure what your job actually uses, and right-size it, so your work runs sooner and wastes nothing.",
         "estimated_duration_s": 10.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]
sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · AICR", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "French (Bonjour)",
    "audience": "Researchers running GPU jobs on AICR who want to know whether the GPU is actually working; assumes no other film",
    "source_doc": "hpc/AICR-Optimizing-GPU-Usage/aicr-gpu-optimization.md (Northeastern Research Computing, AICR Training Workshop 2, "
                  "presenter Arsalan Akhter; github.com/northeastern-rc-training/AICR-Optimizing-GPU-Usage), read 2026-10-06",
    "playlist": "Explorer", "chapter_number": 1,
    "series_title": "Research Computing on Explorer and AICR", "series_video_number": 2, "series_video_count": 13, "series_entry_video": "Video 1 · AICR Introduction",
    "lecture_opening_description": "Request, measure and right-size GPU jobs",
    "tags": ["AICR", "GPU utilization", "PyTorch", "DataLoader", "nvidia-smi", "PyTorch Profiler", "Nsight Systems", "BF16",
             "mixed precision", "gradient checkpointing", "DDP", "Slurm", "jobstats", "HPC", "Northeastern", "Research Computing", "Nik Bear Brown"]},
    "beats": BEATS}

old = {}
p = HERE / "beat_sheet.json"
if p.exists():
    for ob in json.load(open(p))["beats"]:
        old[ob["beat_id"]] = ob
for b in BEATS:
    ob = old.get(b["beat_id"])
    if ob and ob.get("narration_text") == b["narration_text"]:
        for k in ("actual_duration_s", "audio_file"):
            if k in ob:
                b[k] = ob[k]
    dur = b.get("actual_duration_s")
    props = (b["shot"].get("remotion") or {}).get("props")
    if dur and props is not None:
        pat = b["shot"]["remotion"]["pattern"]
        if pat in ("ClaudeDefinitions", "BrowserCapture", "LibraryIconRow", "CCPlainShell", "ClaudeCodeBeat"):
            props["durationSeconds"] = dur
        if pat == "LibraryIconRow":
            n = b["narration_text"]
            for it in props["items"]:
                at = round(n.index(it["cue_phrase"]) / len(n), 3)
                it["at"] = at if not 0.43 <= at <= 0.57 else 0.58
p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(BEATS), "beats; est", round(sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in BEATS)), "s")

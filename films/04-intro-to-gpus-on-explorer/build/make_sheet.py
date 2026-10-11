#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-intro-to-gpus.

LECTURE (brutalist.art/skills/make/lecture/SKILL.md). Source: hpc/Intro-to-GPUs-2026/training_main.md ("Introduction to GPUs on
Explorer", Northeastern Research Computing, presenter Arsalan Akhter; github.com/northeastern-rc-training/Intro-to-GPUs-2026).
The training's own screenshots are the captures; its scripts are the code. Fourth film of the series; same cast.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Intro to GPUs on Explorer"
CAP = "lecture-intro-gpus"
FPS = 30
SPARSE = ("lecture, drawn lane (show-tell drawing laws): one drawn scene on a cream stage with a few labels, the voice "
          "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")


def manim(bid, act, narration, cls, image, show, sparse=True):
    b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show, "manim": {"class": cls}, "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="remotion", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


def shell(bid, act, narration, lines, show, start=20, gap=40, title="ssh — login.explorer.northeastern.edu"):
    return remotion(bid, act, narration, "CCPlainShell", {"title": title, "lines": lines, "startCue": start, "lineGap": gap}, show,
                    motion_claim="The real commands and the training's own output land in order.")


def code(bid, act, narration, title, src, spark, show):
    return remotion(bid, act, narration, "ClaudeCodeBeat", {"title": title, "code": src, "language": "python", "largeText": True, "sparkLine": spark},
                    show, motion_claim="The training's own code prints line by line.")


def capture(bid, act, narration, image, aspect, moves, show, caption="The training's own screenshot of the real site"):
    mv = []
    for m in moves:
        m = dict(m)
        if "ring" in m:
            x, y, w, h = m["ring"]; m["ring"] = [round(x - 0.02, 3), round(y - 0.03, 3), round(w + 0.04, 3), round(h + 0.06, 3)]
        mv.append(m)
    return remotion(bid, act, narration, "BrowserCapture",
                    {"url": "ood.explorer.northeastern.edu", "image": f"{CAP}/{image}", "imageAspect": aspect, "caption": caption, "moves": mv, "ringColor": "#3D3929"},
                    show, motion_claim="The real Open OnDemand page; the camera pushes in to what the sentence names.")


A1, A2, A3, A4, A5, A6, A7, A8 = ("I · The GPU Partitions", "II · What A GPU Is", "III · Three Ways In", "IV · In The Browser",
                                  "V · Interactive And Batch", "VI · Watching The GPU", "VII · Using It Well", "VIII · Habits")

OPEN = [
 remotion("BIDEA", "the idea",
    "Ciao. This is Liam, in for Bear. First, a correction. A GPU is not a faster CPU. It's thousands of small, simple "
    "cores working at once, which is why it wins at some jobs and loses at others. This lecture is the beginner's "
    "introduction to the GPUs on Northeastern's Explorer cluster: which partitions and card types there are, what a "
    "GPU is, the three ways to get one, how to watch it work, and the two code habits that keep it busy.",
    "BrutalistHesitantWriter",
    {"text": "A GPU is just\na faster CPU", "triggerWords": "a faster CPU", "replacementWords": "thousands of simple cores",
     "fontSize": 72, "charMs": 62, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types the assumption"}, {"at": 0.3, "event": "corrects 'a faster CPU' -> 'thousands of simple cores'"}],
    lane="bookend", lead_silence_s=0.8, motion_claim="The writer types the newcomer's picture and corrects it.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. A core: one processing unit that runs instructions on its own. A GPU: a chip with thousands of small "
    "cores for parallel work. A partition: a named group of cluster nodes with its own limits. GRES: generic resources, "
    "Slurm's name for the GPUs you ask for. s run: the command that gives you a live session on a node. And s batch: "
    "the command that submits a script to run without you.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "core", "meaning": "one processing unit that runs instructions on its own"},
               {"term": "GPU", "meaning": "a chip with thousands of small cores for parallel work"},
               {"term": "partition", "meaning": "a named group of cluster nodes with its own limits"},
               {"term": "GRES", "meaning": "generic resources: Slurm's name for the GPUs you ask for"},
               {"term": "srun", "meaning": "a live session on a node"},
               {"term": "sbatch", "meaning": "submit a script to run without you"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "core"}, {"at": 0.25, "event": "GPU"}, {"at": 0.4, "event": "partition"}, {"at": 0.58, "event": "GRES"}, {"at": 0.72, "event": "srun"}, {"at": 0.87, "event": "sbatch"}],
    gate="CARD", lane="bookend", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

NAIVE = """model = torch.nn.Linear(2048, 2048).to(device)
data_size = 50000

start = time.time()
# 50,000 separate requests to the GPU: lots of overhead
for _ in range(data_size):
    data = torch.randn(1, 2048).to(device)
    _ = model(data)

torch.cuda.synchronize()
print(f"Naive Time: {time.time() - start:.4f}s")"""
BATCHED = """model = torch.nn.Linear(2048, 2048).to(device)
data_size = 50000

start = time.time()
# send all the data at once
data = torch.randn(data_size, 2048).to(device)
_ = model(data)

torch.cuda.synchronize()
print(f"Optimized Time: {time.time() - start:.4f}s")"""
LOADERS = """# naive: num_workers=0, the CPU loads one batch at a time
loader = DataLoader(dataset, batch_size=256, num_workers=0)
for images, labels in loader:
    images = images.to("cuda")          # GPU sits idle waiting

# optimized: workers in parallel, pinned memory, non-blocking copy
loader = DataLoader(dataset, batch_size=256, num_workers=2,
                    pin_memory=True)
for images, labels in loader:
    images = images.to("cuda", non_blocking=True)   # GPU stays busy"""
GPUTEST = """import torch

print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("GPU name:", torch.cuda.get_device_name(0))

x = torch.tensor([1.0, 2.0, 3.0], device="cuda")
print("Tensor device:", x.device)"""

B = [
 # I
 manim("B10", A1,
    "Start with where the GPUs are. Explorer groups its GPU nodes into partitions, and six are the ones you'll meet. "
    "gpu, the general one, up to eight hours. gpu-interactive, for Open OnDemand sessions, two hours. gpu-short, "
    "two hours too, but prioritised, so quick tests schedule fast. multigpu, for jobs that need several cards, "
    "twenty-four hours. courses-gpu, for classes, twenty-four hours. And sharing: GPUs that Northeastern PIs lend to "
    "everyone, one hour at a time.",
    "B10_GpuPartitions",
    "A drawn table builds row by row: partition (mono) · max time · a bar whose length is the hours (8, 2, 2, 24, 24, 1); gpu-short's row gets a small ink 'prioritised' tag; sharing's row a kraft 'lent by PIs' tag. Act title top-left.",
    [{"at": 0.2, "event": "gpu 8 h"}, {"at": 0.35, "event": "gpu-interactive 2 h"}, {"at": 0.48, "event": "gpu-short, prioritised"}, {"at": 0.62, "event": "multigpu 24 h"}, {"at": 0.75, "event": "courses-gpu 24 h"}, {"at": 0.9, "event": "sharing 1 h"}], sparse=False),
 shell("B11", A1,
    "Which cards live in a partition? Ask sinfo for the G R E S column. On the gpu partition the answer is a mix: "
    "V100s in two flavours, T4s, A100s in two node sizes, and H200s, eight to a node. The number after the card is how "
    "many sit in each node.",
    ['$ sinfo -p gpu -o "%G"', "GRES", "gpu:v100-sxm2:4(S:0-1)", "gpu:t4:4(S:0-1)", "gpu:a100:3", "gpu:a100:4", "gpu:h200:8",
     "gpu:v100-pcie:2(S:0-1)", "gpu:v100-sxm2:3(S:0-1)"],
    [{"at": 0.1, "event": "sinfo -p gpu"}, {"at": 0.35, "event": "the GRES list prints"}], start=20, gap=30),
 shell("B12", A1,
    "Before you submit, it pays to know what's free. sinfo with the node list, the GRES and the GRES in use shows "
    "that per node. And to check one node, name it. One trap: a node in the MIXED state isn't telling you about its "
    "GPUs. MIXED describes its CPUs. Only the GRES-used column says whether a card is free.",
    ['$ sinfo -p gpu -O "NodeList,Gres:30,GresUsed:30"', "# which cards each node has, and which are in use",
     '$ sinfo -n nodename --Format="Gres:30,GresUsed:30"', "# MIXED is the state of the CPUs, not the GPUs"],
    [{"at": 0.1, "event": "GRES vs GRES used"}, {"at": 0.5, "event": "one node"}, {"at": 0.75, "event": "MIXED means CPUs"}], start=30, gap=70),
 capture("B13", A1,
    "There's also a GPU Monitor app on Open OnDemand. It colours every GPU node as idle, mixed or allocated, and lists "
    "how many GPU jobs are waiting in the queue by card type, so you can pick a card with a shorter line.",
    "gpu-monitor2.png", 2522 / 1308,
    [{"at": 0.0, "x": 0.16, "y": 0.1, "scale": 3.2, "ring": [0.0, 0.06, 0.3, 0.1]}, {"at": 0.6, "x": 0.16, "y": 0.42, "scale": 3.2, "ring": [0.0, 0.36, 0.16, 0.1]}],
    [{"at": 0.0, "event": "the legend: idle, mixed, allocated"}, {"at": 0.6, "event": "GPU jobs pending by card type"}]),
 # II
 manim("B20", A2,
    "So what is a GPU? Start with a core: one unit that runs instructions on its own. A CPU has a few large, complex "
    "cores. A GPU has thousands of small, simple ones. For a problem you can split into thousands of identical little "
    "pieces, the GPU is the right tool.",
    "B20_FewVsThousands",
    "Left: a grey CPU block opens to show four large core squares; right: a dark GPU block opens to a dense grid of hundreds of tiny squares that fill in; labels 'a few complex cores' and 'thousands of simple cores'; a problem bar splits into many slivers that land on the grid. Act title top-left.",
    [{"at": 0.25, "event": "four large cores"}, {"at": 0.45, "event": "thousands of tiny cores"}, {"at": 0.8, "event": "the problem splits across them"}], sparse=False),
 manim("B21", A2,
    "Two pictures from the training. Delivering thousands of pizzas across a city: a few Ferraris, or thousands of "
    "bicycles? The bicycles. Or a room of professors at whiteboards against a stadium of students with calculators. "
    "The professors win at a hard proof. But to multiply a very large matrix, a multiply and an add for every cell, "
    "the stadium wins. Machine learning, scientific simulation, data analysis: those are stadium jobs.",
    "B21_FerrarisAndBicycles",
    "Isometric: a city grid of small kraft blocks (houses); three fast dark carriers each reach one house at a time, while a swarm of small dots fan out and reach every house at once ('bicycles'); then a big grid (matrix) fills cell by cell all at once; labels 'a few fast' / 'thousands at once'.",
    [{"at": 0.15, "event": "three Ferraris, one house each"}, {"at": 0.3, "event": "thousands of bicycles, every house"}, {"at": 0.65, "event": "the matrix fills all at once"}, {"at": 0.9, "event": "stadium jobs"}]),
 # III
 remotion("B30", A3,
    "Three ways to use them. Open OnDemand, a website where a GPU session is a form. An interactive session from the "
    "terminal with s run. And a batch job, a script you submit with s batch and walk away from.",
    "LibraryIconRow",
    {"title": "III · Three Ways In",
     "items": [{"label": "Open OnDemand", "sub": "a form in the browser", "icon": "browser", "cue_phrase": "Open OnDemand"},
               {"label": "srun", "sub": "a live session", "icon": "terminal", "mono": True, "cue_phrase": "An interactive session"},
               {"label": "sbatch", "sub": "a script, submitted", "icon": "file-code", "mono": True, "cue_phrase": "And a batch job"}]},
    [{"at": 0.15, "event": "OOD"}, {"at": 0.45, "event": "srun"}, {"at": 0.7, "event": "sbatch"}],
    motion_claim="Three routes, each landing as one large library icon."),
 shell("B31", A3,
    "One setup for all three. Log in, go to your scratch directory, and clone the training repository. Everything the "
    "demos use is in there: a Python environment script, a tiny GPU check, and the example code.",
    ["$ ssh username@login.explorer.northeastern.edu", "$ cd /scratch/$USER",
     "$ git clone git@github.com:northeastern-rc-training/Intro-to-GPUs-2026.git", "$ cd Intro-to-GPUs-2026"],
    [{"at": 0.1, "event": "ssh"}, {"at": 0.35, "event": "cd scratch"}, {"at": 0.55, "event": "git clone"}], start=30, gap=60),
 # IV
 capture("B40", A4,
    "First way: the browser. On the Open OnDemand dashboard, open Standard Apps and pick VS Code Server.",
    "ood_main.png", 3018 / 1614,
    [{"at": 0.0, "x": 0.5, "y": 0.5, "scale": 1.0}, {"at": 0.35, "x": 0.6, "y": 0.45, "scale": 1.6, "ring": [0.49, 0.645, 0.27, 0.045]}],
    [{"at": 0.0, "event": "the dashboard"}, {"at": 0.35, "event": "zoom to Standard Apps → VSCode"}]),
 capture("B41", A4,
    "The form asks for a simple password for the editor, a partition, sharing here, and the number of GPUs, one. "
    "Leave the rest as it is and launch.",
    "vscode_on_ood.png", 1682 / 1504,
    [{"at": 0.0, "x": 0.5, "y": 0.3, "scale": 1.7, "ring": [0.19, 0.25, 0.4, 0.06]}, {"at": 0.4, "x": 0.5, "y": 0.62, "scale": 1.7, "ring": [0.19, 0.59, 0.4, 0.06]}, {"at": 0.7, "x": 0.5, "y": 0.78, "scale": 1.7, "ring": [0.19, 0.86, 0.4, 0.06]}],
    [{"at": 0.0, "event": "password"}, {"at": 0.4, "event": "partition: sharing"}, {"at": 0.7, "event": "GPUs: 1"}]),
 shell("B42", A4,
    "When the session connects, open the cloned folder in VS Code, then a terminal from the View menu. Make the "
    "environment script executable, run it, and check that which python points into the new environment. Then the "
    "smallest possible test: the script prints the CUDA visible devices variable. Zero means the scheduler gave you a GPU.",
    ["$ chmod +x setup_python_env.sh", "$ ./setup_python_env.sh", "$ which python", "$ python gpu_simple.py",
     "CUDA_VISIBLE_DEVICES = 0", "GPU successfully allocated by scheduler"],
    [{"at": 0.3, "event": "setup script"}, {"at": 0.55, "event": "which python"}, {"at": 0.75, "event": "gpu_simple.py: CUDA_VISIBLE_DEVICES = 0"}], start=40, gap=52, title="VS Code — terminal"),
 # V
 shell("B50", A5,
    "Second way: a live session from the terminal. s run on the sharing partition with one GPU drops you onto a GPU "
    "node. Activate the same environment and run the fuller check, which asks PyTorch for the card.",
    ["$ srun --partition=sharing --gres=gpu:1 --pty bash", "$ ./setup_python_env.sh", "$ which python", "$ python example1/gpu_test_torch.py"],
    [{"at": 0.1, "event": "srun with one GPU"}, {"at": 0.6, "event": "run the check"}], start=30, gap=58),
 code("B51", A5,
    "Here's that check. It prints the PyTorch version, whether CUDA is available, the GPU's name, and then puts a tiny "
    "tensor on the card and prints where it lives. Open it in v i, add an NVIDIA S M I line, and run it again to see the "
    "card itself.",
    "example1/gpu_test_torch.py", GPUTEST, "Four prints and one tensor on the card.",
    [{"at": 0.1, "event": "the script prints"}]),
 shell("B52", A5,
    "Third way: batch. The same work as a script with S BATCH lines: the gpu partition, one GPU, four CPUs, sixteen "
    "gigabytes, one hour, and log files. It activates the environment and runs the check. Submit it with s batch; it "
    "runs when a card is free, writes its output to the logs folder, and you read it later.",
    ["$ cat example1/submit_job.sh", "#!/bin/bash", "#SBATCH --job-name=gpu_job", "#SBATCH --partition=gpu", "#SBATCH --gres=gpu:1",
     "#SBATCH --cpus-per-task=4", "#SBATCH --mem=16G", "#SBATCH --time=01:00:00", "#SBATCH --output=logs/%x_%j.out",
     "#SBATCH --error=logs/%x_%j.err", "source gpu_env/bin/activate", "python gpu_test_torch.py", "$ sbatch example1/submit_job.sh"],
    [{"at": 0.1, "event": "the script"}, {"at": 0.85, "event": "sbatch"}], start=20, gap=28),
 # VI
 manim("B60", A6,
    "Is the card actually working? Put NVIDIA S M I in your script to print its state while the job runs. And after a job "
    "finishes, gpu-logs with the job ID gives a minute-by-minute record. This real one from the training: for five "
    "minutes nothing. Then memory climbs to twenty-three percent, then seventy-eight, with utilization still zero: the "
    "model is loading. Only at the end does utilization reach fifty-six percent. Most of this job's time, the GPU was "
    "waiting.",
    "B60_GpuLogs",
    "Mono header '$ gpu-logs 2374457'; a time axis 12:52 → 13:11; two lines draw as the clock runs: memory (grey) steps 0 → 22.56% → 77.98% → 81.1%, utilization (ink) flat at 0 until 13:07 then steps to 56%; the long flat stretch gets the label 'waiting'; a terracotta dot on the 56% step. Act title top-left.",
    [{"at": 0.3, "event": "five minutes of nothing"}, {"at": 0.5, "event": "memory climbs, utilization zero"}, {"at": 0.75, "event": "56% at the end"}, {"at": 0.9, "event": "waiting"}], sparse=False),
 # VII
 code("B70", A7,
    "Two habits keep a GPU busy. First, batching. The naive version sends fifty thousand single rows to the card, one "
    "request at a time, and pays the overhead fifty thousand times.",
    "example2/naive.py", NAIVE, "Fifty thousand separate requests.",
    [{"at": 0.1, "event": "the loop prints"}]),
 code("B71", A7,
    "The batched version sends all fifty thousand rows at once and runs the model once. Same arithmetic, far less "
    "overhead, and the card's thousands of cores all have work.",
    "example2/optimized.py", BATCHED, "One request, all the rows.",
    [{"at": 0.1, "event": "the batched version prints"}]),
 manim("B72", A7,
    "Picture it. Fifty thousand tiny parcels through the door one at a time, the card idle between each. Or one crate, "
    "and every core busy at once.",
    "B72_ParcelsVsCrate",
    "Isometric: a stream of tiny kraft boxes trickles one by one onto a dark GPU block whose light flickers; then a single large crate lands and the whole top face lights with a grid of terracotta sparks; labels '50,000 × 1' and '1 × 50,000'.",
    [{"at": 0.15, "event": "parcels one at a time"}, {"at": 0.6, "event": "one crate, every core lit"}]),
 code("B73", A7,
    "Second, data loading. With zero workers the CPU prepares one batch at a time and the GPU waits for each. With "
    "workers, pinned memory and a non-blocking copy, the next batch is ready before the card finishes the current one. "
    "Batch your data. Give the loader workers. Keep the card working.",
    "example2_cifar/loaders.py", LOADERS, "Workers, pinned memory, non-blocking.",
    [{"at": 0.1, "event": "naive then optimized loader"}]),
 # VIII
 manim("B80", A8,
    "Four habits to leave with. Choose the right partition: gpu-short for a quick job, and s batch for anything long. "
    "Request only what you need, and check a finished job with seff to see how many CPUs it really used. Use the "
    "GPU-tuned libraries, CUDA and cuDNN, rather than plain code. And profile before you optimise. Stuck? Email "
    "r c help at northeastern dot e d u, or come to office hours.",
    "B80_FourHabits",
    "Four checkbox rows tick in order with 1–3 word labels (right partition · only what you need · GPU libraries · profile first), each with a small cast icon beside it (a partition tag, a job box sized to fit a slot, a dark library block, a magnifier); then 'rchelp@northeastern.edu' lands in mono. Act title top-left.",
    [{"at": 0.1, "event": "right partition"}, {"at": 0.35, "event": "only what you need, seff"}, {"at": 0.6, "event": "GPU libraries"}, {"at": 0.75, "event": "profile first"}, {"at": 0.92, "event": "rchelp"}], sparse=False),
]

RECAP = ["Six GPU partitions; gpu-short schedules fast, sharing is lent by PIs.",
         "sinfo -o \"%G\" shows the cards; GresUsed, not MIXED, says what is free.",
         "A GPU is thousands of simple cores: the stadium, not the professors.",
         "Three ways in: OOD VS Code, srun --gres=gpu:1, or an sbatch script.",
         "gpu-logs shows the card's minute-by-minute memory and utilization.",
         "Batch your data and give the DataLoader workers; keep the card busy."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. Six GPU partitions; gpu-short schedules fast, and sharing is lent by PIs. sinfo with the "
    "G R E S column shows the cards, and the GRES-used column, not MIXED, says what's free. A GPU is thousands of simple "
    "cores: the stadium, not the professors. Three ways in: VS Code on Open OnDemand, s run with one GPU, or an s batch "
    "script. gpu-logs shows the card's memory and utilization minute by minute. And batch your data and give the "
    "DataLoader workers, so the card stays busy.",
    "ClaudeVerdictArtifact", {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land"}],
    lane="bookend", lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("Here is a PyTorch loop I run on a GPU: [paste it]. First, tell me whether it processes samples one at a time or in "
             "batches, and rewrite it to batch if it doesn't. Second, write the DataLoader line with workers and pinned memory. "
             "Third, write me the Slurm srun command for a one-hour test on one GPU and the sbatch script for the real run.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT + " Then check two things yourself. Did it keep the arithmetic "
    "identical when it batched? And did it ask for only one GPU?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Make Your Loop Keep The GPU Busy", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did it keep the arithmetic identical when it batched?", "Check: did it ask for only one GPU?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Intro to GPUs on Explorer. What a GPU is for, which ones Explorer has, and how to ask for one in a job, so the right work lands on the right hardware.",
         "estimated_duration_s": 10.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]
sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · EXPLORER", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "Italian (Ciao)",
    "audience": "Northeastern students and researchers using a GPU on Explorer for the first time; assumes no other film",
    "source_doc": "hpc/Intro-to-GPUs-2026/training_main.md (Northeastern Research Computing training, presenter Arsalan Akhter; "
                  "github.com/northeastern-rc-training/Intro-to-GPUs-2026), read 2026-10-06",
    "playlist": "Explorer", "chapter_number": 3,
    "series_title": "Research Computing on Explorer and AICR", "series_video_number": 4, "series_video_count": 13, "series_entry_video": "Video 1 · AICR Introduction",
    "lecture_opening_description": "What a GPU is for and how to ask for one",
    "tags": ["GPU", "Explorer cluster", "Northeastern", "Research Computing", "Slurm", "srun", "sbatch", "Open OnDemand", "VS Code", "PyTorch",
             "DataLoader", "gpu-logs", "nvidia-smi", "CUDA", "Nik Bear Brown"]},
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

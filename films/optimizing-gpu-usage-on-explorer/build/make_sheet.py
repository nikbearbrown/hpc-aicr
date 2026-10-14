#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-optimizing-gpu-usage-on-explorer.

LECTURE (Bear, 2026-10-02): the WHOLE source as one act-structured film, primarily visual, best visual per beat from
the full playset, a tool shown as itself. Skill doctrine: brutalist.art/skills/make/lecture/SKILL.md.

Sources:  hpc-aicr/Optimizing-GPU-Usage-on-Explorer/ (training_main.md, scripts/01..06, slurm/*.slurm, setup_env.sh): every script
          line on a terminal beat is READ FROM THESE FILES at build time by sl() (a missing line stops the build): a film
          must never invent script text. Real outputs come ONLY from guides/_real-outputs.md (Explorer section, recorded
          read-only on the login node, 2026-10-11) via rl(). Nothing was run on a GPU node; the film says so (B83).

Spine: BOPEN -> BIDEA -> BDEFS -> eight acts -> BVDT -> BHTF -> BOUT.
Two passes: pass 1 (no _qc/asr.json) estimates cues; after Kokoro + faster-whisper, pass 2 places every terminal line on
the word Liam says (word times in _qc/asr.json).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Optimizing GPU Usage on Explorer"
ART = HERE.parents[2] / "brutalist.art"
FPS = 30
SRCDIR = HERE.parents[1] / "Optimizing-GPU-Usage-on-Explorer"
REALF = HERE.parents[1] / "guides/_real-outputs.md"

ASR = {}
_ap = HERE / "_qc/asr.json"
if _ap.exists():
    ASR = json.loads(_ap.read_text())


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word_t(bid, phrase, nth=0, default=None):
    words = ASR.get(bid, {}).get("words")
    if not words:
        return default
    seq = [_norm(w["w"]) for w in words]
    for alt in phrase.split("|"):
        toks = [_norm(x) for x in alt.split() if _norm(x)]
        hits = [i for i in range(len(seq) - len(toks) + 1) if seq[i:i + len(toks)] == toks]
        if len(hits) > nth:
            return words[hits[nth]]["t"]
    return default


def fr(seconds):
    return max(1, int(round(seconds * FPS)))


def cues_for(bid, phrases, narration, est_dur):
    out, last = [], 0
    for ph in phrases:
        if ph is None:
            out.append(0)
            continue
        if isinstance(ph, (int, float)):
            c = max(1, fr(ph), last); out.append(c); last = c
            continue
        t = word_t(bid, ph)
        if t is None:
            print(f"  [cue-fallback] {bid}: '{ph}' not in the recognised words; using the character share")
            alt = ph.split("|")[0]
            i = narration.lower().find(alt.lower())
            t = (est_dur * i / max(1, len(narration))) if i >= 0 else 0.5
        c = max(1, fr(t - 0.15), last)
        out.append(c)
        last = c
    return out


def clear_midpoint(bid, cues):
    dur = None
    p = HERE / "beat_sheet.json"
    if p.exists():
        for ob in json.load(open(p))["beats"]:
            if ob["beat_id"] == bid:
                dur = ob.get("actual_duration_s")
    if not dur:
        return cues
    mid = dur / 2 * FPS
    out, last = [], 0
    for c in cues:
        if c > 0 and mid - 21 < c < mid + 7:
            c = int(mid + 9)
        c = max(c, last) if c > 0 else c
        out.append(c)
        last = max(last, c)
    return out


def est(n):
    return round(len(n.split()) / 2.5, 1)


SPARSE = ("lecture, isometric lane (show-tell drawing laws): one drawn scene on a cream stage with a few labels, "
          "the voice carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame "
          "and contrast still apply.")


def manim(bid, act, narration, cls, image, show, sparse=True):
    b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                  "manim": {"class": cls}, "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="remotion", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


# ───────────────────────────── source readers ─────────────────────────────
FILES = {
    "md": SRCDIR / "training_main.md",
    "01": SRCDIR / "scripts/01_gpu_verify.py",
    "02": SRCDIR / "scripts/02_naive_vs_batched.py",
    "03": SRCDIR / "scripts/03_dataloader_benchmark.py",
    "04": SRCDIR / "scripts/04_pytorch_profiler_demo.py",
    "05": SRCDIR / "scripts/05_mixed_precision_demo.py",
    "06": SRCDIR / "scripts/06_memory_monitor.py",
    "v100": SRCDIR / "slurm/v100_single_gpu.slurm",
    "ddp": SRCDIR / "slurm/ddp_multigpu.slurm",
    "setup": SRCDIR / "setup_env.sh",
}
_TXT = {k: p.read_text() for k, p in FILES.items()}
_LINES = {k: t.splitlines() for k, t in _TXT.items()}


def _cut(ln, maxlen):
    if len(ln) <= maxlen:
        return ln
    return ln[:maxlen].rsplit(" ", 1)[0] + " …"


def sl(src, start, maxlen=96, exact=False, after=None, nth=0):
    """A source line of FILES[src] whose text (leading spaces ignored) starts with `start` (or equals it when exact=True),
    verbatim (indentation kept), cut at a word boundary with an ellipsis if longer than maxlen. `after` = only lines after
    the first line starting with that text. Stops the build if absent."""
    ls = _LINES[src]
    i0 = 0
    if after is not None:
        for i, ln in enumerate(ls):
            if ln.strip().startswith(after):
                i0 = i + 1
                break
        else:
            raise SystemExit(f"sl: anchor {after!r} not in {src}")
    seen = 0
    for ln in ls[i0:]:
        s = ln.strip()
        if (s == start) if exact else s.startswith(start):
            if seen == nth:
                return _cut(ln.rstrip(), maxlen)
            seen += 1
    raise SystemExit(f"sl: no line starting with {start!r} in {src} (after={after!r}, nth={nth})")


def sq(src, text, maxlen=96):
    """An exact fragment that must occur in FILES[src]."""
    if text not in _TXT[src]:
        raise SystemExit(f"sq: fragment not in {src}: {text!r}")
    return _cut(text, maxlen)


# the recorded real outputs: the EXPLORER part only (the AICR part of the file is a different cluster)
_REAL = REALF.read_text()
_REAL = _REAL[_REAL.index("## EXPLORER"):_REAL.index("## AICR")]
_RL = _REAL.splitlines()


def rl(start, maxlen=96, after=None):
    """A recorded line (Explorer section of guides/_real-outputs.md) starting with `start` (exact spacing), optionally after a
    '### header' line. Verbatim, cut at a word boundary with an ellipsis if longer than maxlen."""
    i0 = 0
    if after is not None:
        for i, ln in enumerate(_RL):
            if ln.strip() == after:
                i0 = i + 1
                break
        else:
            raise SystemExit(f"rl: header {after!r} not in the recorded output")
    for ln in _RL[i0:]:
        if ln.startswith(start):
            return _cut(ln.rstrip(), maxlen)
    raise SystemExit(f"rl: no recorded line starting with {start!r} (after={after!r})")


A1, A2, A3, A4, A5, A6, A7, A8 = (
    "I · Do You Have The GPU?", "II · Seeing The GPU Live", "III · The Profiling Toolchain", "IV · Data Starvation",
    "V · Memory And Precision", "VI · More Than One GPU", "VII · The Loop", "VIII · Your Domain")

B = []


def add(b):
    B.append(b)
    return b


def shell(bid, act, narration, title, lines, cue_phrases, show, ring_lines=None, ring_phrases=None, fs=28, margin=100,
          motion_claim="The text, exactly as written or recorded, prints line by line as it is spoken."):
    assert len(lines) == len(cue_phrases), (bid, len(lines), len(cue_phrases))
    cues = cues_for(bid, cue_phrases, narration, est(narration))
    cues = clear_midpoint(bid, cues)
    props = {"title": title, "lines": lines, "startCue": 20, "lineGap": 30, "lineCues": cues, "fontSize": fs, "windowMargin": margin}
    if ring_lines is not None:
        props["rings"] = [{"line": ln, "cue": clear_midpoint(bid, [cues_for(bid, [ph], narration, est(narration))[0] + 12])[0]}
                          for ln, ph in zip(ring_lines, ring_phrases)]
    return add(remotion(bid, act, narration, "CCPlainShell", props, show, motion_claim=motion_claim))


# ───────────────────────────── the opening pair ─────────────────────────────
OPEN = [
 remotion("BIDEA", "the idea",
    "Hallo. This is Liam, in for Bear. First, a correction. A GPU job that finishes without an error has not necessarily used the GPU. "
    "Code that cannot find a card quietly runs on the CPU, and code that finds one may keep it waiting for data. "
    "This lecture is a set of measuring tools for Explorer, and a short list of fixes. Measure first. Change second.",
    "BrutalistHesitantWriter",
    {"text": "My GPU job finished,\nso it used the GPU", "triggerWords": "it used the GPU",
     "replacementWords": "the card may have waited", "fontSize": 70, "charMs": 62, "hesitateBetween": 6,
     "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'My GPU job finished, so it used the GPU'"},
     {"at": 0.35, "event": "backspaces 'it used the GPU' -> 'the card may have waited'"}],
    lane="bookend", lead_silence_s=0.8,
    motion_claim="The writer types the newcomer's belief (a finished job used the GPU) and corrects it (the card may have waited).",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. GPU utilization: the share of the last second in which the card ran any work at all. V RAM: the card's own memory, "
    "where your model and your batch live. DataLoader: the part of PyTorch that reads, batches and hands data to the card. Profiler: "
    "a tool that tells you where the time went. B F sixteen: a sixteen-bit number format that keeps the range of thirty-two-bit floats. "
    "And D D P: distributed data parallel, one model copy per card.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "GPU utilization", "meaning": "the share of the last second the card ran work"},
               {"term": "VRAM", "meaning": "the card's own memory"},
               {"term": "DataLoader", "meaning": "reads and batches data for the card"},
               {"term": "Profiler", "meaning": "a tool that says where the time went"},
               {"term": "BF16", "meaning": "16-bit numbers with 32-bit range"},
               {"term": "DDP", "meaning": "one model copy per card, gradients averaged"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.06, "event": "'GPU utilization' lands"}, {"at": 0.22, "event": "'VRAM'"}, {"at": 0.4, "event": "'DataLoader'"},
     {"at": 0.58, "event": "'Profiler'"}, {"at": 0.74, "event": "'BF16'"}, {"at": 0.9, "event": "'DDP'"}],
    gate="CARD", lane="bookend",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

# ═════════════════════════════ ACT I · Do You Have The GPU? ═════════════════════════════
add(manim("B10", A1,
    "Three things go wrong with no error message. You ask for one kind of card and get another. The software cannot see a GPU, "
    "so it quietly runs on the CPU. Or a setting left in your shell hides the card you were given.",
    "B10_QuietFailures",
    "A kraft job box with a terracotta tape rolls into a finish gate and a check lands at the gate (job finished, no error). Then three "
    "branches fan out under the check, each landing on a GPU block (dark slab with a light): the first lands on a different block than "
    "requested (two GPU blocks of different size, a request chip picks one and the other one gets used); the second shows a GPU block "
    "left dark and a CPU chip lit with the job running on it; the third shows a small 'shell' chip with a dotted line that hides a GPU "
    "block. Labels: 'wrong card', 'CPU instead', 'hidden card'.",
    [{"at": 0.15, "event": "the job finishes; a check, no error"}, {"at": 0.4, "event": "wrong card"},
     {"at": 0.65, "event": "runs on the CPU, the GPU stays dark"}, {"at": 0.88, "event": "a shell setting hides the card"}]))
add(manim("B11", A1,
    "Explorer names its GPU partitions by purpose. G P U short and G P U interactive give two hours, for tests, profiling and "
    "interactive work. The G P U partition gives eight hours, for real training. Sharing gives one. Multi G P U goes to twenty-four, "
    "and needs an approved access request.",
    "B11_Partitions",
    "A horizontal bar chart on an hours ruler (0 to 24 h): 'sharing' 1 h, 'gpu-short' 2 h, 'gpu-interactive' 2 h, 'gpu' 8 h, 'multigpu' 24 h "
    "(the last drawn hatched with a small key tag 'access request'). Each bar grows on its spoken name; a short purpose tag by each "
    "('tests', 'interactive', 'training'). Partition names in mono.",
    [{"at": 0.2, "event": "gpu-short and gpu-interactive: 2 h"}, {"at": 0.5, "event": "gpu: 8 h"}, {"at": 0.65, "event": "sharing: 1 h"},
     {"at": 0.85, "event": "multigpu: 24 h, access request"}], sparse=False))
shell("B12", A1,
    "Here is the cluster itself, read from the login node without submitting anything. The three G P U partitions list the same "
    "twenty-five nodes, with limits of eight hours, two hours and two hours. Sharing is its own partition, with one hour.",
    "I · Partitions  ·  recorded on the login node, read-only",
    [rl("PARTITION       AVAIL", after="### sinfo -s"), rl("gpu                up", after="### sinfo -s"),
     rl("sharing            up", after="### sinfo -s"), rl("gpu-short          up", after="### sinfo -s"),
     rl("gpu-interactive    up", after="### sinfo -s")],
    [None, "three GPU partitions", "limits of eight hours", "Sharing is", "two hours"],
    [{"at": 0.05, "event": "the header and the gpu row"}, {"at": 0.4, "event": "the limits: 8 h, 2 h, 2 h"}, {"at": 0.8, "event": "sharing: 1 h"}],
    ring_lines=[1, 4], ring_phrases=["eight hours", "two hours"], fs=26)
shell("B13", A1,
    "Never guess the card name. Ask the cluster. Partition G P U holds five types: V one hundred S X M two, mostly four to a node. "
    "V one hundred P C I e, two. A one hundred, three or four. H two hundred, eight. And T four, four. Some written guides list only two of these.",
    "I · GPU types on partition gpu  ·  recorded, selected rows",
    [rl("PARTITION GRES NODES STATE", after="### gpu gres (partition gpu)"),
     rl("gpu gpu:v100-sxm2:4(S:0-1) 6 mix", after="### gpu gres (partition gpu)"),
     rl("gpu gpu:v100-pcie:2(S:0-1) 3 mix", after="### gpu gres (partition gpu)"),
     rl("gpu gpu:a100:4 2 mix", after="### gpu gres (partition gpu)"),
     rl("gpu gpu:h200:8 4 mix", after="### gpu gres (partition gpu)"),
     rl("gpu gpu:t4:4(S:0-1) 1 idle", after="### gpu gres (partition gpu)")],
    [None, "V100S", "V100PCIE2", "a 100", "H200", "T4"],
    [{"at": 0.05, "event": "the header"}, {"at": 0.3, "event": "v100-sxm2, then v100-pcie, a100"}, {"at": 0.75, "event": "h200 and t4"}],
    ring_lines=[4], ring_phrases=["H200"], fs=28)
shell("B14", A1,
    "Now the request, from a template in Research Computing's training material. A G P U partition. A gres line that names the card. "
    "CPUs for your data loading. Memory. A time limit. And a place for the logs.",
    "I · The request  ·  a batch script header, as written",
    [sl("v100", "#SBATCH --job-name=my_training"), sl("v100", "#SBATCH --partition=gpu"), sl("v100", "#SBATCH --cpus-per-task=8"),
     sl("v100", "#SBATCH --gres=gpu:v100-sxm2:1"), sl("v100", "#SBATCH --mem=32G"), sl("v100", "#SBATCH --time=04:00:00"),
     sl("v100", "#SBATCH --output=logs/%x_%j.out")],
    [None, "a GPU partition", "CPUs for your data", "Gresline", "Memory", "A time limit", "place for the logs"],
    [{"at": 0.05, "event": "job name and partition"}, {"at": 0.4, "event": "the gres line, ringed"}, {"at": 0.8, "event": "memory, time, logs"}],
    ring_lines=[3, 4], ring_phrases=["Gresline", "Memory"], fs=26)
add(manim("B15", A1,
    "Two lines deserve a pause. Mem is CPU memory. The card's own memory, V RAM, comes with the card, so raising mem never fixes a GPU "
    "out-of-memory error. And a bare gres of gpu colon one may land you on a different card. Name the type.",
    "B15_MemAndType",
    "Left half: a node with a RAM slot (kraft block, mono label '--mem=32G') and a separate GPU card block with its own tank labelled 'VRAM' that "
    "comes with the card; a mem knob turns up and the RAM block grows but the VRAM tank stays the same size, with a small 'out of memory' tag "
    "that does not go away. Right half: a request chip 'gpu:1' (mono) throws three arrows to three different GPU blocks (V100, A100, T4 chips, "
    "wobbling); a second chip 'gpu:v100-sxm2:1' sends one arrow to exactly one block, with a check.",
    [{"at": 0.15, "event": "mem is CPU memory; VRAM comes with the card"}, {"at": 0.4, "event": "raising mem leaves the VRAM tank and the error unchanged"},
     {"at": 0.7, "event": "bare gpu:1 may land on any card"}, {"at": 0.9, "event": "naming the type picks one"}], sparse=False))
shell("B16", A1,
    "The environment is plain. A virtual environment from system Python, and pip wheels. PyTorch's wheel carries its own CUDA "
    "runtime, and a GPU node already has the driver, so you load no CUDA module for it.",
    "I · The environment  ·  from the setup script",
    [sl("setup", "# On Explorer (GPU node), the default CUDA-enabled wheels work:"), sl("setup", "python3 -m venv"),
     sl("setup", 'source "$VENV_DIR/bin/activate"'), sl("setup", "pip install torch torchvision torchaudio"),
     sl("setup", "# nvitop        : live GPU dashboard", maxlen=96)],
    [None, "virtual environment", "virtual environment", "pip wheels", "no CUDA module|load no CUDA module"],
    [{"at": 0.05, "event": "the source comment"}, {"at": 0.35, "event": "venv and activate"}, {"at": 0.7, "event": "pip install torch, no CUDA module"}],
    ring_lines=[3], ring_phrases=["pip wheels"], fs=28)
shell("B17", A1,
    "Two facts, recorded on the login node. G P U logs and S eff are installed, but NVIDIA S M I is missing, so GPU checks belong inside a "
    "job. And a Python module does exist, version three point thirteen point five, though some material says there is none.",
    "I · Login node  ·  recorded read-only",
    ["# which tools are on the path", rl("gpu-logs         /shared", after="### commands present"), rl("seff             /usr/bin/seff", after="### commands present"),
     rl("nvidia-smi       MISSING", after="### commands present"), "# module avail python",
     rl("----------------------- /shared/EL9/explorer/modulefiles", after="-- python"), rl("python/3.13.5", after="-- python")],
    [None, "GPU logs", "S eff|seff|sef", "NVIDIA SMI", "Python module", "version 3", "13"],
    [{"at": 0.05, "event": "gpu-logs and seff found"}, {"at": 0.3, "event": "nvidia-smi MISSING, ringed"}, {"at": 0.65, "event": "python/3.13.5"}],
    ring_lines=[3, 6], ring_phrases=["NVIDIA SMI", "version 3"], fs=26)
shell("B18", A1,
    "Never trust the allocation. This verify script checks five things: CUDA available, the cards and their memory, the visible-devices "
    "variable, NVIDIA S M I, and a tensor round trip. Available means PyTorch sees a card. The round trip proves it can use one.",
    "I · Verify at runtime  ·  01_gpu_verify.py, excerpts",
    [sl("01", "cuda_ok = torch.cuda.is_available()"), sl("01", "gpu_count = torch.cuda.device_count()"),
     sl("01", "p = torch.cuda.get_device_properties(i)"), sl("01", 'cvd = os.environ.get("CUDA_VISIBLE_DEVICES", "NOT SET")'),
     sl("01", '"nvidia-smi",'), sl("01", "x = torch.tensor([1.0, 2.0, 3.0]).cuda()"), sl("01", "y = (x * 2).cpu()")],
    [None, "the cards and their memory", "the cards and their memory", "visible devices", "NVIDIA SMI", "tensor round trip", "round trip proves"],
    [{"at": 0.05, "event": "available, count, properties"}, {"at": 0.45, "event": "the variable and nvidia-smi"}, {"at": 0.8, "event": "the round trip, ringed"}],
    ring_lines=[5, 6], ring_phrases=["tensor round trip", "round trip proves"], fs=26)
add(manim("B19", A1,
    "Slurm sets CUDA visible devices to your cards' numbers: zero is one card, zero comma one is two. Leave it alone unless you want a "
    "subset. It can be unset in an interactive session, so it is never proof either way. The round trip is.",
    "B19_VisibleDevices",
    "A mono tag 'CUDA_VISIBLE_DEVICES' at the top; below, three small states side by side: '0' with one GPU block lit, '0,1' with two lit, "
    "and an empty tag with an interactive terminal chip (all blocks dim, labelled 'unset: can be normal'); then a verdict row: the tag "
    "crossed ('not proof') and a tensor arrow looping CPU chip to GPU block and back with a terracotta check ('the round trip').",
    [{"at": 0.15, "event": "0 is one card, 0,1 is two"}, {"at": 0.45, "event": "unset in an interactive session"},
     {"at": 0.75, "event": "the variable is not proof; the round trip is"}], sparse=False))

# ═════════════════════════════ ACT II · Seeing The GPU Live ═════════════════════════════
add(manim("B20", A2,
    "Now watch it. NVIDIA S M I has two numbers that matter. GPU utilization: the share of the last second in which a kernel was "
    "running. In this example, eighty-seven percent, healthy; below fifty means something is wrong. And memory: here, about a fifth of the card.",
    "B20_TwoNumbers",
    "Two drawn gauges side by side (ink arcs with a needle): left 'GPU-Util' with the needle at 87 and a one-second clock face beside it whose "
    "sweep is mostly filled ('share of the last second'), a mark at 50 labelled 'below: wrong'; right 'Memory' with the needle at 22 and a tank "
    "about a fifth full. A small tag 'example' on each. Terracotta only at the mark.",
    [{"at": 0.15, "event": "GPU-Util gauge: 87, share of the last second"}, {"at": 0.45, "event": "below 50 is wrong"}, {"at": 0.8, "event": "the memory gauge: about a fifth"}], sparse=False))
shell("B21", A2,
    "To see it live, a person opens a second terminal on the compute node and runs watch. N V I top is a richer view, per process, so "
    "you can confirm that your own Python is using the card. A coding agent should not run watch. It never exits.",
    "II · Watching  ·  not run by us",
    ["# a snapshot", sl("md", "nvidia-smi", exact=True), "# live, in a second terminal", sl("md", "watch -n 1 nvidia-smi"),
     "# a richer view, per process", sl("md", "pip install nvitop"), sl("md", "nvitop", exact=True)],
    [None, "person opens", "second terminal", "runs watch", "richer view", "richer view", "per process"],
    [{"at": 0.05, "event": "nvidia-smi"}, {"at": 0.35, "event": "watch -n 1"}, {"at": 0.7, "event": "nvitop"}],
    ring_lines=[3], ring_phrases=["It never exits"], fs=28)
add(manim("B22", A2,
    "Read them as two axes. High memory with low utilization: loaded, but nothing is feeding it. Low and low: the card sits empty. High "
    "utilization with low memory: healthy, raise the batch. High and high: good. Fifteen percent utilization, seventy-five memory? Data starvation.",
    "B22_TwoAxes",
    "A drawn 2x2 grid: utilization across (low to high), memory up (low to high). Four cells with short tags: top-left 'loaded, not fed', "
    "bottom-left 'empty card', bottom-right 'raise the batch', top-right 'good'. The cells land on the spoken order. Then a terracotta dot "
    "drops into the top-left cell at (15, 75) with the mono tag '15% / 75%' and the words 'data starvation'.",
    [{"at": 0.15, "event": "high memory, low utilization: loaded, not fed"}, {"at": 0.35, "event": "low and low: empty"},
     {"at": 0.55, "event": "high utilization, low memory: raise the batch"}, {"at": 0.7, "event": "high and high: good"},
     {"at": 0.88, "event": "the 15 / 75 dot lands top-left: data starvation"}], sparse=False))
add(manim("B23", A2,
    "Use one set of bands. Under fifty percent is a problem. Under sixty, suspect the data pipeline. Sixty to seventy is amber, seventy "
    "acceptable, eighty to a hundred the target. For memory, sixty to ninety percent is healthy; under forty means room for a bigger batch.",
    "B23_Bands",
    "Two horizontal scales stacked. Top 'utilization' 0 to 100 with grey segments: 0-50 'problem', 50-60 'suspect data', 60-70 'amber', 70-80 'acceptable', "
    "80-100 'target' (only the target segment edged in terracotta tick). Bottom 'memory' 0 to 100: under 40 'room to raise batch', 60-90 'healthy'. "
    "Segments grow left to right on the spoken numbers.",
    [{"at": 0.12, "event": "under 50: a problem"}, {"at": 0.3, "event": "under 60 suspect the data pipeline"}, {"at": 0.5, "event": "amber, acceptable, target"},
     {"at": 0.78, "event": "memory: 60 to 90 healthy; under 40 room"}], sparse=False))
add(manim("B24", A2,
    "Explorer also watches for idle cards. A bot called Idle Bot emails you after about fif teen minutes of under-use, and the job is "
    "cancelled after about an hour. We found no published percentage for under-use. A stalled job holds its card and your queue place while doing nothing.",
    "B24_IdleBot",
    "A GPU-utilisation line on a time axis that starts busy and then sinks to a flat low stretch; a watcher marker 'Idle Bot' (magnifier) sweeps the "
    "flat stretch; at a '15 min' mark an envelope lands; at a '1 h' mark the job box is cancelled (x_mark). A small tag: 'no published percentage'.",
    [{"at": 0.15, "event": "the line sinks"}, {"at": 0.4, "event": "15 min: an email"}, {"at": 0.62, "event": "1 h: the job is cancelled"}, {"at": 0.88, "event": "no published percentage"}]))

# ═════════════════════════════ ACT III · The Profiling Toolchain ═════════════════════════════
add(manim("B30", A3,
    "A profiler tells you where the time went. Four layers, lightest first. Live tools: NVIDIA S M I and N V I top. The framework "
    "profiler. Nsight Systems for a timeline. And Nsight Compute for one kernel. Stop as soon as you know. Most problems show by layer two.",
    "B30_FourLayers",
    "A ladder of four rungs drawn bottom to top, light to heavy: 'live' (nvidia logo chip + mono 'nvidia-smi'), 'framework' (pytorch logo chip), "
    "'timeline' (nvidia logo chip + 'nsys'), 'one kernel' (nvidia logo chip + 'ncu'); a terracotta bracket labelled 'most problems' ringed around the "
    "first two rungs; the top two rungs drawn in grey with the tag 'rarely'.",
    [{"at": 0.15, "event": "live tools"}, {"at": 0.35, "event": "framework profiler"}, {"at": 0.55, "event": "timeline, then one kernel"}, {"at": 0.85, "event": "most problems show by layer two"}]))
shell("B31", A3,
    "Profile in a short interactive session, not through the batch queue. Get a session on G P U short, activate your environment, run "
    "fifty steps, change one thing, repeat. If it runs in under thirty minutes, skip the batch queue.",
    "III · An interactive session  ·  not run by us",
    [sl("md", "srun --partition=gpu-short --gres=gpu:v100-sxm2:1 --cpus-per-task=8"), sl("md", "--time=01:00:00 --pty bash"),
     sl("md", "source gpu_training_env/bin/activate", after="# In the session"), sl("md", "python train.py --max-steps 50")],
    [None, "interactive session", "activate your environment", "50 steps"],
    [{"at": 0.05, "event": "the srun request"}, {"at": 0.4, "event": "activate"}, {"at": 0.75, "event": "fifty steps"}],
    ring_lines=[0, 3], ring_phrases=["GPU short", "50 steps"], fs=26)
shell("B32", A3,
    "The PyTorch profiler needs no install. Warm up for a few untimed steps, or start-up cost swamps the table. Then profile a small "
    "window: wait one step, warm up one, record ten. Step the profiler every iteration, and print the table sorted by CUDA time.",
    "III · PyTorch profiler  ·  04_pytorch_profiler_demo.py, excerpts",
    [sl("04", "for _ in range(3):"), sl("04", "wx = torch.randn(BATCH_SIZE, 3, 32, 32, device=DEVICE)"), sl("04", "model(wx).sum().backward()"),
     sl("04", "schedule = torch.profiler.schedule(wait=1, warmup=1, active=PROFILE_STEPS)"), sl("04", "with profile("),
     sl("04", "prof.step()"), sl("04", 'print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=12))')],
    [None, "few untimed steps", "few untimed steps", "small window", "Step the profiler|profile a small", "Step the profiler", "sorted by"],
    [{"at": 0.05, "event": "the warm-up"}, {"at": 0.4, "event": "the schedule: wait 1, warm up 1, active 10"}, {"at": 0.8, "event": "step and print by CUDA time"}],
    ring_lines=[3, 6], ring_phrases=["wait one step", "sorted by"], fs=26)
add(manim("B33", A3,
    "Read the table in order. Gaps between kernels: the GPU is idle. Large copy rows: data shuttling between CPU and GPU. CPU time far "
    "above CUDA time: the work is not on the card. And the data loader at the top: the pipeline is the bottleneck. This example is from Research Computing's material, not our run.",
    "B33_ReadTheTable",
    "A drawn horizontal bar pair per row (CPU total in grey, CUDA total in ink) for four rows: 'DataLoader.__next__' (CPU long bar 1.843 s, CUDA zero), "
    "'aten::conv2d' (CPU 0.041 s tiny, CUDA 0.394 s), 'aten::batch_norm', 'aten::copy_'; tag 'example, not our run'. Four numbered checks land in order "
    "at the left: 'gaps', 'copies', 'CPU >> CUDA', 'loader on top' with the loader row ringed in terracotta on the last.",
    [{"at": 0.12, "event": "gaps between kernels"}, {"at": 0.3, "event": "large copy rows"}, {"at": 0.5, "event": "CPU far above CUDA"}, {"at": 0.72, "event": "loader at the top: ringed"}], sparse=False))
shell("B34", A3,
    "When order matters, trace a timeline with Nsight Systems. Profile one or two epochs, never a hundred, write the report to scratch, "
    "and open it on your laptop. We could not confirm that N sys is on Explorer's path. Check the module list, or ask.",
    "III · A timeline  ·  from the source, not run by us",
    [sl("md", "nsys profile \\", exact=True), sl("md", "--trace=cuda,nvtx,osrt,cudnn,cublas"), sl("md", "--output=/scratch/$USER/profile_%p"),
     sl("md", "python train.py --epochs 2"), sl("md", "scp cluster:/scratch/$USER/profile_*.nsys-rep ./")],
    [None, "Nsight Systems", "write the report to scratch", "one or two epochs", "open it on your laptop"],
    [{"at": 0.05, "event": "nsys profile"}, {"at": 0.4, "event": "the report goes to scratch"}, {"at": 0.8, "event": "copy it to the laptop"}],
    ring_lines=[2, 3], ring_phrases=["scratch", "one or two epochs"], fs=26)
add(manim("B35", A3,
    "On the timeline, an empty GPU row with short bursts means data arrives late. File reads filling the gaps mean you are reading a "
    "network filesystem during training. Copies scattered through each step mean data moves inside the loop. Pin the memory.",
    "B35_TimelinePatterns",
    "A timeline drawing with two rows on a time axis: a 'GPU' row of short ink bursts with long empty gaps between (burst 15 ms, gap 50 ms, tagged "
    "'example'), and a 'CPU' row where kraft blocks labelled 'read()' fill exactly the gaps (the disk/file read). Then a third row 'copies' shows host-to-device "
    "copy ticks scattered through each step; a pin chip 'pinned memory' moves them together. Row labels in 1-2 words.",
    [{"at": 0.15, "event": "short bursts, long gaps: data arrives late"}, {"at": 0.45, "event": "file reads fill the gaps"}, {"at": 0.8, "event": "copies scattered: pin the memory"}], sparse=False))

# ═════════════════════════════ ACT IV · Data Starvation ═════════════════════════════
add(manim("B40", A4,
    "The most common bottleneck is not the model. A fast cook waits for slow deliveries. Say the card computes a batch in twenty-five "
    "milliseconds and the loader needs sixty. The card idles thirty-five of every sixty. No model change fixes that.",
    "B40_Deliveries",
    "A single time bar of 60 units (tagged 'example'): the first 25 units filled ink 'GPU computes 25 ms', the remaining 35 left ghost with a hatched pattern "
    "'GPU waits 35 ms'; above it a second bar of 60 labelled 'loader 60 ms'. A cook-and-delivery metaphor in pictures: a GPU block at one end of a belt with a "
    "truck block (kraft box 'batch') that crawls toward it; as the truck arrives the GPU lights only for the first slice. A small gauge reads '58% idle'.",
    [{"at": 0.15, "event": "a fast cook waits for slow deliveries"}, {"at": 0.45, "event": "25 ms compute, 60 ms loader"}, {"at": 0.75, "event": "35 of every 60 idle"}]))
shell("B41", A4,
    "Two stopwatch tests need no profiler. First, time fifty batches out of your loader, with no GPU work at all.",
    "IV · Stopwatch test one  ·  the loader alone",
    [sl("md", "import time, torch"), sl("md", "# Step 1: Time just the data loading (no GPU work)"), sl("md", "t0 = time.perf_counter()"),
     sl("md", "for i, (x, y) in enumerate(loader):"), sl("md", "if i == 50: break"),
     sl("md", "loader_ms = (time.perf_counter() - t0) / 50 * 1000")],
    [None, "Two stopwatch tests", "time 50 batches", "out of your loader", "out of your loader", "no GPU work"],
    [{"at": 0.1, "event": "start the clock"}, {"at": 0.5, "event": "fifty batches from the loader"}, {"at": 0.9, "event": "no GPU work at all"}],
    ring_lines=[4], ring_phrases=["time 50 batches"], fs=28)
shell("B42", A4,
    "Second, time fifty forward and backward steps on synthetic data made directly on the GPU, and synchronize before you stop the "
    "clock. If loading takes longer than computing, you are data bound.",
    "IV · Stopwatch test two  ·  the compute alone",
    [sl("md", "# Step 2: Time just the compute (synthetic data, no loading)"), sl("md", "dummy_x = torch.randn(256, 3, 224, 224, device='cuda')"),
     sl("md", "loss.backward()", after="# Step 2"), sl("md", "torch.cuda.synchronize()", after="# Step 2"),
     sl("md", "print(f'Mean compute time:"), sl("md", "# If loader_ms > compute_ms, you are DATA BOUND")],
    [None, "synthetic data", "forward and backward", "synchronized", "stop the clock", "data bound"],
    [{"at": 0.05, "event": "synthetic data on the GPU"}, {"at": 0.45, "event": "synchronize before the clock stops"}, {"at": 0.85, "event": "loader slower than compute: data bound"}],
    ring_lines=[3, 5], ring_phrases=["synchronized", "data bound"], fs=26)
shell("B43", A4,
    "The fix usually lives in four DataLoader settings. Workers: CPU processes that load in parallel. Pin memory: page-locked RAM for "
    "faster copies. Persistent workers: do not restart them every epoch. Pre fetch factor: batches each worker prepares ahead.",
    "IV · The four settings  ·  as written",
    [sl("md", "loader = DataLoader("), sl("md", "batch_size=256,"), sl("md", "num_workers=8,", maxlen=84), sl("md", "pin_memory=True,", maxlen=84),
     sl("md", "persistent_workers=True,", maxlen=84), sl("md", "prefetch_factor=4,", maxlen=84), sl("md", ")", exact=True, after="prefetch_factor=4,")],
    [None, "four data loader", "Workers", "Pin memory", "Persistent workers", "Pre fetch factor", "Pre fetch factor"],
    [{"at": 0.05, "event": "DataLoader("}, {"at": 0.3, "event": "num_workers, pin_memory"}, {"at": 0.7, "event": "persistent_workers, prefetch_factor"}],
    ring_lines=[2, 3, 4, 5], ring_phrases=["Workers", "Pin memory", "Persistent workers", "Pre fetch factor"], fs=30, margin=100)
add(manim("B44", A4,
    "Starting values. Workers: CPUs per task, minus one, never zero. Pin memory: always on in a GPU job. Persistent workers: on whenever "
    "workers is above zero. Pre fetch: two, raise it if still slow. So ask for CPUs per task equal to workers plus one, and at least four.",
    "B44_StartingValues",
    "Four chips in a row, each with a mono name and a value tag: 'num_workers' -> 'cpus - 1'; 'pin_memory' -> 'True'; 'persistent_workers' -> 'True if workers > 0'; "
    "'prefetch_factor' -> '2'. Beneath, a drawn equation of blocks: [--cpus-per-task] = [num_workers] + [1 for the main process], with 'at least 4' tag. "
    "Eight small CPU squares: seven lit as worker dots and one as the main process.",
    [{"at": 0.12, "event": "workers: CPUs minus one"}, {"at": 0.35, "event": "pin memory: true"}, {"at": 0.55, "event": "persistent workers; prefetch two"},
     {"at": 0.8, "event": "cpus-per-task = workers + 1, at least 4"}], sparse=False))
shell("B45", A4,
    "The benchmark script tries four configurations: zero workers, two, four, and four with pinned memory, persistent workers and "
    "pre fetch. It prints the load time for each and compares it with the GPU's time. We did not run it.",
    "IV · The benchmark  ·  03_dataloader_benchmark.py, excerpts",
    [sl("03", "python 03_dataloader_benchmark.py"), sl("03", '"label": "Config A'), sl("03", '"label": "Config B'), sl("03", '"label": "Config C'),
     sl("03", '"label": f"Config D'), "# not run by us"],
    [None, "four configurations", "zero workers", "two", "four with pinned", "We did not run it"],
    [{"at": 0.05, "event": "the usage line"}, {"at": 0.3, "event": "configs A, B, C"}, {"at": 0.65, "event": "config D, ringed"}],
    ring_lines=[4], ring_phrases=["four with pinned"], fs=26)
shell("B46", A4,
    "And never feed the card one item at a time. Every call has a fixed cost: launch, transfer set-up, synchronization. Ten thousand "
    "single-sample calls pay it ten thousand times. One batched call pays it once.",
    "IV · One at a time, or batched  ·  02_naive_vs_batched.py, excerpts",
    ["# naive: one sample per call", sl("02", "for _ in range(DATA_SIZE):"), sl("02", "sample = torch.randn(1, FEATURE_SIZE, device=DEVICE)"),
     sl("02", "_ = model(sample)"), "# batched: one call", sl("02", "all_data = torch.randn(DATA_SIZE, FEATURE_SIZE, device=DEVICE)"),
     sl("02", "_ = model(all_data)")],
    [None, "one item at a time", "fixed cost", "launch", "One batched call", "One batched call", "pays it once"],
    [{"at": 0.05, "event": "the loop, one sample per call"}, {"at": 0.5, "event": "ten thousand times"}, {"at": 0.85, "event": "one batched call"}],
    ring_lines=[1, 6], ring_phrases=["10 000", "pays it once"], fs=30)
add(manim("B47", A4,
    "Where the data lives matters. On Explorer, home, scratch and projects are all network filesystems. Keep data in scratch or a "
    "projects folder, packed into a few large files, never millions of small ones, and never in home. Scratch is purged, so keep your original elsewhere.",
    "B47_WhereDataLives",
    "Three storage boxes in a row, each labelled in mono: '/home' (small, a cross on 'datasets'), '/scratch' (a check, with a purge calendar tick tagged 'purged'), "
    "'/projects' (a check). A bracket over all three: 'network filesystems'. Below, two folders compared: a pile of thousands of tiny file dots in one "
    "(crossed) and three large file slabs in the other (check). Data slabs move into scratch/projects, not home.",
    [{"at": 0.15, "event": "home, scratch, projects: network filesystems"}, {"at": 0.45, "event": "data in scratch or projects, not home"},
     {"at": 0.65, "event": "a few large files, not millions of small ones"}, {"at": 0.9, "event": "scratch is purged"}], sparse=False))
add(manim("B48", A4,
    "Research Computing's material illustrates the direction. With no workers: about eighteen percent utilization, four hundred twenty "
    "images a second. Eight workers and pinned memory: fifty-five percent, thirteen hundred. Add pre fetching: eighty-two percent, nineteen fifty. No script produces these. Use them for direction, not as a promise.",
    "B48_Illustration",
    "Three bar pairs left to right on a shared ruler (tagged 'illustration from the source, not our run'): utilization bars 18, 55, 82 (grey, last one ink) with images "
    "per second printed beside: '~420', '~1,300', '~1,950'. Config chips under them in mono: 'num_workers=0', '8 workers + pin_memory', '+ prefetch_factor=4'. "
    "The bars grow in order on the spoken numbers; a small stamp 'no script produces these' lands at the end.",
    [{"at": 0.2, "event": "no workers: 18%, 420 img/s"}, {"at": 0.45, "event": "8 workers, pinned: 55%, 1,300"}, {"at": 0.65, "event": "prefetch: 82%, 1,950"},
     {"at": 0.88, "event": "no script produces these"}], sparse=False))

# ═════════════════════════════ ACT V · Memory And Precision ═════════════════════════════
add(manim("B50", A5,
    "Batch size is the simplest lever. Doubling it roughly doubles throughput, until the card is saturated, if the memory is there. "
    "If memory sits near twenty percent and nothing fails, double the batch and measure again. Stop short of the largest size that fits, because the optimizer needs memory too.",
    "B50_BatchDoubles",
    "A tall tank labelled 'VRAM' with a batch block of height 20% sitting in it; the block doubles (40%) and a throughput arrow beside it doubles in length; "
    "the block doubles again up to a ceiling line labelled 'largest that fits'; a margin gap is marked below the ceiling and a small 'optimizer' block fills "
    "some of the gap (terracotta tick on the margin).",
    [{"at": 0.12, "event": "doubling roughly doubles throughput"}, {"at": 0.4, "event": "memory near 20%: double and measure"}, {"at": 0.75, "event": "stop short of the ceiling; the optimizer needs room"}]))
shell("B51", A5,
    "To find the ceiling, try sizes and narrow the search. Make a batch, run forward and backward, catch the out-of-memory error, free "
    "the memory, and search again. Then leave a margin below the answer.",
    "V · Finding the largest batch  ·  as written, excerpts",
    [sl("md", "def test_batch_size(model, bs, input_shape=(3, 224, 224)):"), sl("md", "x = torch.randn(bs, *input_shape, device='cuda')"),
     sl("md", "y.sum().backward()", after="def test_batch_size"), sl("md", "except torch.cuda.OutOfMemoryError:"),
     sl("md", "lo, hi = 1, 2048"), sl("md", "mid = (lo + hi + 1) // 2"), sl("md", "print(f'Max batch size that fits: {lo}')")],
    [None, "Make a batch", "forward and backward", "catch the out of memory", "narrow the search|try sizes", "narrow the search|try sizes", "leave a margin"],
    [{"at": 0.05, "event": "make a batch, forward and backward"}, {"at": 0.4, "event": "catch the out-of-memory error"}, {"at": 0.8, "event": "the search"}],
    ring_lines=[3, 6], ring_phrases=["catch the out of memory", "leave a margin"], fs=26)
shell("B52", A5,
    "Mixed precision is next. Wrap the forward pass and the loss in autocast, and leave the backward call outside it. Do not cast "
    "the model by hand: under autocast, the weights, the loss and normalization stay in thirty-two bits.",
    "V · Mixed precision  ·  the change, as written",
    [sl("md", "from torch.amp import autocast"), sl("md", "# After (BF16 — add just this wrapper)"),
     sl("md", "with autocast(device_type='cuda', dtype=torch.bfloat16):"), sl("md", "out  = model(x)", after="# After (BF16"),
     sl("md", "loss = criterion(out, y)", after="# After (BF16"), sl("md", "loss.backward()   # gradients automatically stay in FP32")],
    [None, "Mixed precision is next", "Wrap the forward pass", "Wrap the forward pass", "and the loss", "outside it"],
    [{"at": 0.05, "event": "import autocast"}, {"at": 0.35, "event": "the wrapper around forward and loss"}, {"at": 0.8, "event": "backward stays outside"}],
    ring_lines=[2, 5], ring_phrases=["Wrap the forward pass", "outside it"], fs=26)
add(manim("B53", A5,
    "A sixteen-bit format splits its bits between range and precision. B F sixteen keeps the full range, so no loss scaler. F P sixteen "
    "keeps more precision but little range, so it needs one. B F sixteen on A one hundred and newer. F P sixteen on V one hundred and T four.",
    "B53_BitSplit",
    "Three rows of bit cells, drawn as segmented bars: 'FP32' = 1 sign + 8 exponent (range) + 23 mantissa (precision); 'BF16' = 1 + 8 + 7; 'FP16' = 1 + 5 + 10. "
    "Exponent cells in ink fill, mantissa cells in grey, labelled 'range' and 'precision' by the first row. Beside BF16 a card chip row 'A100 and newer' and 'no loss scaler'; "
    "beside FP16 chips 'V100' and 'T4' and a small 'GradScaler' box (mono). Segments land per row on the spoken names.",
    [{"at": 0.15, "event": "bits split between range and precision"}, {"at": 0.35, "event": "BF16: full range, no loss scaler"}, {"at": 0.6, "event": "FP16: precision, little range, needs a scaler"},
     {"at": 0.82, "event": "BF16 on A100 and newer; FP16 on V100 and T4"}], sparse=False))
shell("B54", A5,
    "Choose by compute capability, not by the library's own support call. One demo script picks with that call. A second script says "
    "the call reports true even on a V one hundred, and picks by capability: major version eight or higher means B F sixteen.",
    "V · Which format  ·  two scripts disagree",
    ["# script 05 picks with this call", sl("05", "if DEVICE == \"cuda\" and not torch.cuda.is_bf16_supported():"),
     "# script 06 says of that call:", sl("06", "torch.cuda.is_bf16_supported(), which returns True even on a V100 (it"),
     "# and picks by capability instead", sl("06", "major = torch.cuda.get_device_capability()[0]"),
     sl("06", "return torch.bfloat16 if major >= 8 else torch.float16")],
    [None, "One demo script", "A second script", "reports true even", "picks by capability", "major version 8", "BF16"],
    [{"at": 0.05, "event": "script 05's call"}, {"at": 0.4, "event": "script 06: true even on a V100"}, {"at": 0.75, "event": "capability: major 8 or higher"}],
    ring_lines=[3, 5], ring_phrases=["reports true even", "major version 8"], fs=26)
add(manim("B55", A5,
    "Be honest about gains. Total memory does not drop by half, because optimizer state and master weights stay put. The speed-up depends on "
    "how much of your work is matrix and convolution maths. The material quotes up to eight times in one place and one and a half to three in another. Quote neither.",
    "B55_HonestGains",
    "A memory bar split into segments: 'activations', 'master weights', 'optimizer state'. Under BF16 only the activations segment halves (visibly shrinks) while "
    "the other two stay the same size; the total bar shrinks by less than half (a ruler shows 'not 2x'). Beside it two claim chips 'up to 8x' and '1.5 to 3x' with a "
    "'?' between them and an 'ops matter: matmul, conv' tag; both chips get greyed with the words 'quote neither'.",
    [{"at": 0.15, "event": "activations halve; weights and optimizer state stay"}, {"at": 0.45, "event": "speed-up depends on the operations"}, {"at": 0.78, "event": "two claims disagree: quote neither"}], sparse=False))

shell("B56", A5,
    "Gradient checkpointing is the last resort for memory: activations are recomputed in the backward pass instead of stored. The "
    "material claims sixty to seventy percent less activation memory for thirty percent more compute, with no source. In Hugging Face it is one call.",
    "V · Last resort  ·  gradient checkpointing, as written",
    [sl("md", "# For Hugging Face Transformers models — one flag:"), sl("md", "model.gradient_checkpointing_enable()"),
     sl("md", "# For custom PyTorch modules:"), sl("md", "from torch.utils.checkpoint import checkpoint"),
     sl("md", "return checkpoint(self.expensive_layers, x, use_reentrant=False)")],
    [None, "recomputed in the backward", "no source", "In Hugging Face", "one call"],
    [{"at": 0.05, "event": "the Hugging Face flag"}, {"at": 0.5, "event": "custom modules: checkpoint()"}],
    ring_lines=[1, 4], ring_phrases=["one call", "recomputed in the backward"], fs=26)
shell("B57", A5,
    "And watch the memory. Log peak V RAM per epoch with max memory allocated, and compare it with the card's total. After an "
    "out-of-memory error, delete the big objects and empty the cache.",
    "V · Watching memory  ·  as written",
    [sl("md", "torch.cuda.reset_peak_memory_stats()"), sl("md", "peak  = torch.cuda.max_memory_allocated() / 1024**3"),
     sl("md", "total = torch.cuda.get_device_properties(0).total_memory / 1024**3"), sl("md", "print(f'Peak VRAM:", maxlen=100)],
    [None, "peak VRAM", "compare it with the card's total", "compare it"],
    [{"at": 0.05, "event": "reset the peak"}, {"at": 0.4, "event": "peak and total"}, {"at": 0.8, "event": "print the share"}],
    ring_lines=[1], ring_phrases=["peak VRAM"], fs=30)

# ═════════════════════════════ ACT VI · More Than One GPU ═════════════════════════════
add(manim("B60", A6,
    "More GPUs multiply the efficiency you have; they do not create it. A job at twenty percent on one card becomes four cards at twenty "
    "percent. Add cards only when one is above eighty. Under sixty, fix that first. A job limited by reading data only gets worse.",
    "B60_EightyFirst",
    "A utilization scale for one GPU 0 to 100 with a mark at 60 ('fix first') and at 80 ('more cards pay'). A dot at 20: one GPU block at 20%; it copies to "
    "four GPU blocks each at 20% with a cost meter growing 4x ('4x allocation'). Then the 80 mark gets a check, the under-60 zone gets a cross, and a "
    "small disk-reading chip ('limited by reading data') with four GPU arrows fighting over it, crossed.",
    [{"at": 0.15, "event": "20% on one card becomes 20% on four"}, {"at": 0.45, "event": "only above 80 do more cards pay"}, {"at": 0.62, "event": "under 60: fix first"},
     {"at": 0.85, "event": "reading-bound: more cards make it worse"}]))
add(manim("B61", A6,
    "In data-parallel training, each card holds a full model copy and takes a different batch. They then average their gradients, an "
    "all-reduce, and apply the same update. Fast inside a node, slower between nodes. It cannot fix a model too big for one card.",
    "B61_AllReduce",
    "Four GPU blocks in a row, each holding an identical small model block; four different batch cards A, B, C, D drop onto them; gradient arrows from each go to a "
    "central averaging block labelled 'average' (an all-reduce ring); the averaged arrow returns to every GPU and each updates. Under, two links: 'inside a node: fast' "
    "(short thick pipe) vs 'between nodes: slower' (long thin pipe). A final too-big model block that does not fit one card is crossed ('not fixed by this').",
    [{"at": 0.12, "event": "each card has a full copy and its own batch"}, {"at": 0.4, "event": "gradients averaged, same update"}, {"at": 0.65, "event": "fast inside a node, slower between"},
     {"at": 0.88, "event": "cannot fix a model too big for one card"}]))
shell("B62", A6,
    "Check your code is written for it. A plain script given four cards uses one and wastes three. Is distributed available? Has the "
    "process group been initialized? And does the device count match what you requested?",
    "VI · Is the code written for it?  ·  as written",
    [sl("md", "import torch, torch.distributed as dist", exact=True), sl("md", "print(dist.is_available())", maxlen=100),
     sl("md", "print(dist.is_initialized())", maxlen=100), sl("md", "print(torch.cuda.device_count())", maxlen=100)],
    [None, "Is distributed available", "initialized", "device count"],
    [{"at": 0.05, "event": "import"}, {"at": 0.4, "event": "available, initialized"}, {"at": 0.8, "event": "device count matches the request"}],
    ring_lines=[1, 2, 3], ring_phrases=["Is distributed available", "initialized", "device count"], fs=26)
shell("B63", A6,
    "The rules for the code: launch with torch run, never plain python. Use DistributedDataParallel, not DataParallel. Wrap after moving "
    "the model to its device. Give each card a distributed sampler, and call set epoch every epoch. Backend: N C C L.",
    "VI · The DDP rules  ·  as written, excerpts",
    [sl("md", "torchrun --nproc_per_node=4 launch_ddp.py"), sl("md", "dist.init_process_group('nccl')"), sl("md", "model   = DDP(model, device_ids=[local])", maxlen=100),
     sl("md", "sampler = DistributedSampler(dataset)", maxlen=100), sl("md", "sampler.set_epoch(epoch)", maxlen=100)],
    [None, "CCL", "Wrap after moving", "distributed sampler", "set epoch"],
    [{"at": 0.05, "event": "torchrun"}, {"at": 0.4, "event": "nccl and the wrap"}, {"at": 0.8, "event": "sampler and set_epoch"}],
    ring_lines=[0, 2, 4], ring_phrases=["torch run", "Wrap after moving", "set epoch"], fs=26)
shell("B64", A6,
    "Three numbers must agree: the count in gres, tasks per node, and torch run's processes per node. Keep one node. This partition, "
    "multi G P U, needs an approved access request before you use it.",
    "VI · The request  ·  ddp_multigpu.slurm, as written",
    [sl("ddp", "#SBATCH --partition=multigpu"), sl("ddp", "#SBATCH --nodes=1"), sl("ddp", "#SBATCH --ntasks-per-node=4"),
     sl("ddp", "#SBATCH --gres=gpu:v100-sxm2:4"), sl("ddp", "#SBATCH --cpus-per-task=8")],
    [None, "Keep one node", "tasks per node", "count ingres", "approved access"],
    [{"at": 0.05, "event": "the partition"}, {"at": 0.4, "event": "ntasks-per-node and gres: both 4"}, {"at": 0.8, "event": "one node"}],
    ring_lines=[2, 3, 0], ring_phrases=["tasks per node", "count ingres", "approved access"], fs=30)
shell("B65", A6,
    "One trap in both of Research Computing's templates. A comment after a trailing backslash ends the line there, so the next argument "
    "is run as a command. Remove the comment. The templates also call scripts that you must supply yourself.",
    "VI · A template trap  ·  both slurm templates, as written",
    ["# a comment after a trailing backslash", sl("v100", "python train.py \\"), sl("v100", "--data-dir $DATA_DIR \\"),
     sl("ddp", "torchrun --standalone --nproc_per_node=4 train_ddp.py \\"),
     "# the line ends at the backslash-space; the next line runs as a command", "# fix: put the comment on its own line"],
    [None, "trailing backslash", "next argument", "scripts that you must supply", "run as a command", "Remove the comment"],
    [{"at": 0.05, "event": "the two broken lines"}, {"at": 0.5, "event": "the next argument runs as a command"}, {"at": 0.85, "event": "remove the comment"}],
    ring_lines=[1, 3], ring_phrases=["trailing backslash", "scripts that you must supply"], fs=24, margin=100)
add(manim("B66", A6,
    "Measure the scaling. Efficiency is throughput, divided by the number of cards times one card's throughput. Above eighty percent, "
    "extra cards pay. Below seventy, stop and look for a communication or reading bottleneck. The material says nothing about seventy to eighty.",
    "B66_ScalingEfficiency",
    "A drawn fraction: numerator block 'throughput on N cards', a bar; denominator 'N x one-card throughput' (N small GPU blocks stacked); '= efficiency' with a "
    "gauge. Below, a scale 0 to 100 with a green-free monochrome: segment under 70 'stop, look for a communication or reading bottleneck' with a cross, segment "
    "70 to 80 drawn dashed with a '?' ('not described'), over 80 'extra cards pay' with a check.",
    [{"at": 0.15, "event": "throughput over N times one card"}, {"at": 0.5, "event": "above 80: pays; below 70: stop"}, {"at": 0.85, "event": "70 to 80: not described"}], sparse=False))

# ═════════════════════════════ ACT VII · The Loop ═════════════════════════════
add(manim("B70", A7,
    "Every bottleneck comes in roughly this order of frequency, so here is the loop. Baseline: throughput, utilization, wall time. "
    "Profile a short window. Diagnose. Fix one thing, only one. Re-profile. Record the gain. Repeat until the returns run out.",
    "B70_TheLoop",
    "Seven numbered-free stations arranged on a ring, each a small drawn object with a 1-2 word label: 'baseline' (stopwatch), 'profile' (magnifier over a bar), "
    "'diagnose' (fork with four tags: data, memory, compute, communication), 'fix one thing' (a single wrench/dial, with a ringed 'only one'), 're-profile', "
    "'record the gain' (a page with a tick), 'repeat'. A kraft job box travels around the ring and each station lights as it arrives.",
    [{"at": 0.15, "event": "baseline"}, {"at": 0.4, "event": "profile, diagnose"}, {"at": 0.6, "event": "fix one thing"}, {"at": 0.85, "event": "re-profile, record, repeat"}]))
add(manim("B71", A7,
    "The decision guide. Utilization under fifty: the data pipeline first, and is workers still zero? Fifty to eighty: look at memory. "
    "Memory under fifty, raise the batch; fifty to eighty-five, try mixed precision; over ninety, shrink the batch or checkpoint. Out of memory: smaller batch, then mixed precision, then checkpointing.",
    "B71_DecisionGuide",
    "A drawn decision tree: root 'utilization' splits into '< 50' -> box 'data pipeline first' (a mono chip 'num_workers == 0?'), '50 to 80' -> node 'memory' which splits into "
    "'< 50%' -> 'raise the batch', '50 to 85%' -> 'try mixed precision', '> 90%' -> 'smaller batch / checkpointing', and '> 80 and healthy' -> 'in good shape'. A side track "
    "'out of memory' shows three steps in order: 'smaller batch' -> 'mixed precision' -> 'checkpointing'. Branches grow on the spoken cues.",
    [{"at": 0.1, "event": "under 50: data pipeline first"}, {"at": 0.3, "event": "50 to 80: look at memory"}, {"at": 0.55, "event": "memory branches"},
     {"at": 0.8, "event": "out of memory: batch, precision, checkpointing"}], sparse=False))
shell("B72", A7,
    "After a batch job, read its report. G P U logs shows utilization over time for a finished job. It needs a compute node, so we "
    "have not run it. Run it soon: it keeps about seven days, and only for public nodes.",
    "VII · After the job  ·  not run by us",
    ["# after a batch job", sl("md", "gpu-logs <jobid>", exact=True), "# needs a compute node: not run by us"],
    [None, "GPU log", "we have not run it"],
    [{"at": 0.05, "event": "the command"}, {"at": 0.7, "event": "not run by us"}],
    ring_lines=[1], ring_phrases=["GPU log"], fs=32, margin=110)
add(manim("B73", A7,
    "Read three things. Average utilization: aim above seventy. The shape of the line: flat and high is healthy; bouncing low is data "
    "starvation; flat and low means the workload is too small for the card. And average V RAM: low means room for a bigger batch. Under sixty percent? Fix it before the next submission.",
    "B73_ReadGpuLogs",
    "Three small drawn line plots on a time axis, side by side, labelled 'flat and high' (healthy, check), 'bouncing low' (data starvation), 'flat and low' (workload too small); "
    "a dashed 70 line across each. Beside them two readouts as gauges 'average utilization' (target above 70) and 'average VRAM' (low: bigger batch). A last tag lands: "
    "'under 60: fix before the next submission'. Plots are schematic, tagged 'shapes, not output'.",
    [{"at": 0.15, "event": "average utilization above 70"}, {"at": 0.35, "event": "flat and high; bouncing low; flat and low"}, {"at": 0.7, "event": "average VRAM"},
     {"at": 0.88, "event": "under 60: fix before the next submission"}], sparse=False))
add(manim("B74", A7,
    "Before you submit. The check passed and you know the card and its memory. A short run showed over seventy percent. Workers set, "
    "pinned memory on. The batch uses half the memory. Precision matches the card. The request names the type, with four CPUs or more. The logs folder exists. And you profiled twenty to fifty steps.",
    "B74_Checklist",
    "A clipboard page with eight unnumbered rows, each a short label and an empty box that gets a check on its spoken cue: 'verify passed', '> 70% in a short run', 'workers + pin set', "
    "'batch uses half the VRAM', 'precision matches the card', 'type named, 4+ CPUs', 'logs/ exists', 'profiled 20-50 steps'. The page fills top to bottom.",
    [{"at": 0.1, "event": "the check passed"}, {"at": 0.3, "event": "short run above 70; workers and pin"}, {"at": 0.55, "event": "batch, precision, request"}, {"at": 0.85, "event": "logs folder; profiled"}], sparse=False))

# ═════════════════════════════ ACT VIII · Your Domain ═════════════════════════════
add(manim("B80", A8,
    "None of this is only for PyTorch. PyTorch and TensorFlow: every act applies. Packaged tools like Hugging Face: verify, watch, and "
    "feed the data, and the fixes are flags. Molecular dynamics: verify the card, and expect trajectory writing to limit you. Custom CUDA: add Nsight Compute.",
    "B80_YourDomain",
    "Four rows, each with a logo chip or mono chip and a short tag: pytorch + tensorflow logo chips -> 'every act'; huggingface logo chip -> 'verify, watch, feed data; fixes are flags'; "
    "a mono chip 'GROMACS NAMD AMBER' (no logos exist) -> 'verify the card, trajectory writes limit you'; a mono chip 'custom CUDA' with nvidia logo chip -> 'add Nsight Compute'. Rows build on the spoken names.",
    [{"at": 0.15, "event": "PyTorch and TensorFlow: every act"}, {"at": 0.4, "event": "Hugging Face: flags"}, {"at": 0.65, "event": "molecular dynamics: trajectory writing"}, {"at": 0.88, "event": "custom CUDA: Nsight Compute"}]))
shell("B81", A8,
    "In Hugging Face, the three fixes are arguments: B F sixteen, gradient checkpointing, and data loader workers, set from your CPU count.",
    "VIII · Hugging Face  ·  as written",
    [sl("md", "training_args = TrainingArguments("), "    " + sq("md", "bf16=True,"), "    " + sq("md", "gradient_checkpointing=True,"),
     "    " + sq("md", "dataloader_num_workers=8,"), "    # set the worker count from your CPU count", ")"],
    [None, "Bf16", "gradient check pointing", "data loader workers", "CPU count", "CPU count"],
    [{"at": 0.1, "event": "bf16"}, {"at": 0.45, "event": "gradient checkpointing"}, {"at": 0.75, "event": "workers from the CPU count"}],
    ring_lines=[1, 2, 3], ring_phrases=["Bf16", "gradient check pointing", "data loader workers"], fs=30, margin=110)
add(manim("B82", A8,
    "Explorer and AICR differ, so do not carry lines between them. AICR is Northeastern's other GPU cluster. Here you name the card in gres. There, "
    "the partition fixes it. Here, a virtual environment and pip wheels. There, CUDA modules and conda. Here, G P U logs after a job. There, job stats. And here, the login node has no NVIDIA S M I.",
    "B82_ExplorerNotAicr",
    "Two columns with a divider: 'Explorer' (rack) and 'AICR' (bigger grid rack). Rows land on the spoken contrast, each a pair of mono chips: 'gres: gpu:v100-sxm2:1' | 'partition fixes the card'; "
    "'venv + pip wheels' | 'CUDA module + conda'; 'gpu-logs' | 'jobstats'; 'no nvidia-smi on login' | 'nvidia-smi on login'. A caution mark between columns: 'do not carry lines across'.",
    [{"at": 0.15, "event": "the card: gres here, partition there"}, {"at": 0.4, "event": "venv and pip, CUDA module and conda"}, {"at": 0.65, "event": "gpu-logs, jobstats"}, {"at": 0.88, "event": "nvidia-smi on the login node"}], sparse=False))
add(manim("B83", A8,
    "Here is what we checked and what we only read. We ran nothing on a GPU node. Read-only on the login node we checked the partitions "
    "and limits, the five GPU types, which tools are on the path, and the Python module. The sessions, scripts, profilers, G P U logs and the numbers are read from the source.",
    "B83_CheckedVsRead",
    "Two columns of stamped items. Left 'checked, read-only on the login node': 'partitions and limits', 'five GPU types', 'tools on the path', 'python module'. Right 'read from the source, "
    "not run by us': 'sessions', 'demo scripts', 'profilers', 'gpu-logs output', 'performance numbers'. Stamps land on the spoken words; a ringed chip underneath: 'nothing ran on a GPU node'.",
    [{"at": 0.12, "event": "nothing ran on a GPU node"}, {"at": 0.35, "event": "four read-only checks stamp in"}, {"at": 0.7, "event": "the rest is read from the source"}], sparse=False))
add(manim("B84", A8,
    "For help, write to r c help at northeastern dot e d u, come to office hours, or book a consultation with the Research Computing team.",
    "B84_GetHelp",
    "Three chips land in a row under a small rack: a mail chip with the address 'rchelp@northeastern.edu' in mono, an 'office hours' chip, and a 'book a consultation' chip. "
    "Professor Bear 1x1 portrait on the left pointing right; a pulse on each chip as it is named.",
    [{"at": 0.2, "event": "the email address"}, {"at": 0.55, "event": "office hours"}, {"at": 0.85, "event": "a consultation"}]))

# ───────────────────────────── the closing three ─────────────────────────────
RECAP = ["Verify the card in every job: the partition, a named type, and a tensor round trip.",
         "Read utilization and memory together; under fifty percent is a problem, and idle cards are cancelled.",
         "Profile a short window; the biggest row says where to look.",
         "Feed the card first: workers, pinned memory, prefetch, and batches.",
         "Then batch size, the right precision for the card, and checkpointing last.",
         "Add cards only past eighty percent, change one thing at a time, and read G P U logs after every job."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. Verify the card in every job: the partition, a named type, and a tensor round trip. Read utilization and "
    "memory together. Under fifty percent is a problem, and idle cards are cancelled. Profile a short window; the biggest row says where to look. "
    "Feed the card first: workers, pinned memory, pre fetch, and batches. Then batch size, the right precision for the card, and checkpointing last. "
    "And add cards only past eighty percent, change one thing at a time, and read G P U logs after every job.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land in narration order"}],
    lane="bookend", lead_silence_s=0.5,
    qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("Here is my PyTorch training loop and my Slurm script for Explorer: [paste both]. I run it on one GPU. Walk me through the "
             "optimization loop: what to measure for a 50-step baseline, how to profile 20 steps, and which of these to try first and why: "
             "DataLoader num_workers and pin_memory, a larger batch, mixed precision, gradient checkpointing, or a second GPU. Give me the "
             "exact code changes for your first pick only. Do not run anything on any cluster.")
YT_SPOKEN = ("Here is my PyTorch training loop and my Slurm script for Explorer: paste both here. I run it on one GPU. Walk me through the "
             "optimization loop: what to measure for a fifty-step baseline, how to profile twenty steps, and which of these to try first and why: "
             "DataLoader num workers and pin memory, a larger batch, mixed precision, gradient checkpointing, or a second GPU. Give me the "
             "exact code changes for your first pick only. Do not run anything on any cluster.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_SPOKEN + " Then check two things yourself. Did it ask you to measure before it changed "
    "anything? And did it change exactly one thing?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Measure Before You Change", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did Claude ask you to measure before it changed anything?",
                "Check: did it change exactly one thing, and give code for that one only?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": "Optimizing GPU Usage on Explorer. At Nik Bear Brown.", "estimated_duration_s": 5.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Optimizing GPU Usage on Explorer. How to confirm that a job really used the "
                           "GPU, measure what it uses, and fix the few problems that waste most GPU time.",
         "estimated_duration_s": 13.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · GPU PERFORMANCE", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German (Hallo)",
    "audience": "A researcher who runs GPU jobs on Northeastern's Explorer cluster and wants to know whether the GPU is really working; assumes no other film or book",
    "source_doc": "hpc-aicr/Optimizing-GPU-Usage-on-Explorer/ (Northeastern Research Computing training, presenter Arsalan Akhter; training_main.md, scripts, slurm templates, setup_env.sh; read in full, scripts shown verbatim) plus guides/optimizing-gpu-usage-on-explorer.md, HPC.md Section 6, and guides/_real-outputs.md for the recorded login-node output",
    "playlist": "Northeastern HPC and AICR",
    "series_title": "Research Computing on Explorer and AICR",
    "lecture_opening_description": "Check, measure and fix GPU jobs on Explorer",
    "lecture_opening_title_lines": ["Optimizing GPU Usage", "on Explorer"],
    "tags": ["GPU utilization", "PyTorch", "DataLoader", "nvidia-smi", "PyTorch Profiler", "Nsight Systems", "BF16", "mixed precision",
             "gradient checkpointing", "DDP", "Slurm", "gpu-logs", "IdleBot", "Explorer", "Northeastern University", "Research Computing",
             "HPC", "Nik Bear Brown"]},
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

p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
n_est = sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in BEATS)
print(len(BEATS), "beats; est", round(n_est), "s", "(measured)" if all(b.get("actual_duration_s") for b in BEATS) else "(estimate)")

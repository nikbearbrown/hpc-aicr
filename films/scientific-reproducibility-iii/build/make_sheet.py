#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-scientific-reproducibility-iii-containers.

LECTURE (Bear, 2026-10-02): the WHOLE source as one act-structured film, primarily visual, best visual per beat from
the full playset, a tool shown as itself. Skill doctrine: brutalist.art/skills/make/lecture/SKILL.md.

Sources:  _research/source-guide.md (our written guide, hpc-aicr/guides/scientific-reproducibility-iii.md) and
          _research/source-original.md (the lesson it rewrites). Every command, script and file on a terminal beat is READ FROM
          THE SOURCE at build time by g()/o()/blk()/cmd() below (a missing line stops the build): a film must never invent
          script text.
Honesty:  nothing was run on a compute node for this film. Only three facts were checked by us (apptainer path and version,
          no module, the gpu partition limits; guides/_real-outputs.md). Every other terminal beat is titled "from the source,
          not run" and shows commands with no output. The film says so out loud (B80).

Spine: BOPEN -> BIDEA -> BDEFS -> eight acts -> BVDT -> BHTF -> BOUT.
Two passes: pass 1 (no _qc/asr.json) estimates cues; after Kokoro + faster-whisper, pass 2 places every terminal line on
the word Liam says (word times in _qc/asr.json).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Scientific Reproducibility III: Containers"
ART = HERE.parents[2] / "brutalist.art"
FPS = 30

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


# ───────────── the sources: every terminal line is read from them ─────────────
SRC_G = (HERE / "_research/source-guide.md").read_text()
SRC_O = (HERE / "_research/source-original.md").read_text()
_GL, _OL = SRC_G.splitlines(), SRC_O.splitlines()
_ALL = SRC_G + "\n" + SRC_O


def _find(lines, start, nth):
    hits = [i for i, ln in enumerate(lines) if ln.strip().startswith(start)]
    if len(hits) <= nth:
        raise SystemExit(f"no source line starting with {start!r} (occurrence {nth})")
    return hits[nth]


def g(start, nth=0, maxlen=104):
    """The nth line of OUR guide that starts with `start` (leading spaces ignored), verbatim, indentation kept."""
    ln = _GL[_find(_GL, start, nth)].rstrip()
    if len(ln) > maxlen:
        raise SystemExit(f"g: line too long ({len(ln)}): {ln!r}")
    return ln


def o(start, nth=0, maxlen=104):
    """The nth line of the ORIGINAL lesson that starts with `start`, verbatim."""
    ln = _OL[_find(_OL, start, nth)].rstrip()
    if len(ln) > maxlen:
        raise SystemExit(f"o: line too long ({len(ln)}): {ln!r}")
    return ln


def blk(start, n, nth=0, src="g"):
    """`n` consecutive source lines beginning at the nth line that starts with `start`."""
    lines = _GL if src == "g" else _OL
    i = _find(lines, start, nth)
    return [ln.rstrip() for ln in lines[i:i + n]]


def cmd(text):
    """A command line, '$ ' prefix; the text must occur in the source."""
    if text not in _ALL:
        raise SystemExit(f"cmd: not in the sources: {text!r}")
    return "$ " + text


def wrap2(full, marker, prefix=""):
    """One source command shown on two lines with a shell line-continuation; the words are the source's, unchanged."""
    i = full.index(marker)
    return [prefix + full[:i].rstrip() + " \\", "    " + full[i:].strip()]


def _pyline():
    for ln in _GL:
        if ln.strip().startswith("6. **Check the GPU inside a container.**"):
            m = re.search(r"`(apptainer exec --nv <pytorch-image>\.sif python -c \"[^`]*)`", ln)
            if m:
                return m.group(1)
    raise SystemExit("python check line not found")


A1, A2, A3, A4, A5, A6, A7, A8 = (
    "I · What A Container Is", "II · Why Use One", "III · Running A Container", "IV · Binding Folders",
    "V · Building An Image", "VI · Getting An Image Onto The Cluster", "VII · Habits That Keep It Honest",
    "VIII · What Was Checked")

NOTRUN = "from the source, not run"

# ───────────────────────────── the opening pair ─────────────────────────────
OPEN = [
 remotion("BIDEA", "the idea",
    "Hallo. This is Liam, in for Bear. First, a correction. To repeat a result, sharing your code is not enough. The libraries "
    "and the system under it change. A container seals the whole software stack into one file.",
    "BrutalistHesitantWriter",
    {"text": "To repeat my result,\nI just share my code", "triggerWords": "share my code",
     "replacementWords": "seal the whole stack", "fontSize": 66, "charMs": 62, "hesitateBetween": 6,
     "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'To repeat my result, I just share my code'"},
     {"at": 0.35, "event": "backspaces 'share my code' -> 'seal the whole stack'"}],
    lane="bookend", lead_silence_s=0.8,
    motion_claim="The writer types the newcomer's framing (share my code) and corrects it to the real one (seal the whole stack).",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. Container: a sealed bundle of a program and what it needs. Image: the file a container is made from. Apptainer: "
    "runs containers on shared clusters. S I F file: Apptainer's single-file image. Bind: shows a folder from the machine inside the container. And tag: the version label on an image.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "Container", "meaning": "a sealed bundle of a program and what it needs"},
               {"term": "Image", "meaning": "the file a container is made from"},
               {"term": "Apptainer", "meaning": "runs containers on shared clusters"},
               {"term": ".sif file", "meaning": "Apptainer's single-file image"},
               {"term": "Bind", "meaning": "shows a host folder inside"},
               {"term": "Tag", "meaning": "the version label on an image"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.06, "event": "'Container' lands"}, {"at": 0.22, "event": "'Image'"}, {"at": 0.38, "event": "'Apptainer'"},
     {"at": 0.55, "event": "'.sif file'"}, {"at": 0.72, "event": "'Bind'"}, {"at": 0.88, "event": "'Tag'"}],
    gate="CARD", lane="bookend",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

B = []


def add(b):
    B.append(b)
    return b


def shell(bid, act, narration, title, lines, cue_phrases, show, ring_lines=None, ring_phrases=None, fs=38, margin=100,
          motion_claim="The text, exactly as in the source, prints line by line as it is spoken."):
    cues = cues_for(bid, cue_phrases, narration, est(narration))
    cues = clear_midpoint(bid, cues)
    props = {"title": title, "lines": lines, "startCue": 20, "lineGap": 30, "lineCues": cues, "fontSize": fs, "windowMargin": margin}
    if ring_lines is not None:
        props["rings"] = [{"line": ln, "cue": clear_midpoint(bid, [cues_for(bid, [ph], narration, est(narration))[0] + 12])[0]}
                          for ln, ph in zip(ring_lines, ring_phrases)]
    return add(remotion(bid, act, narration, "CCPlainShell", props, show, motion_claim=motion_claim))


# ═════════════════════════════ ACT I · What A Container Is ═════════════════════════════
add(manim("B10", A1,
    "A container is one sealed file. Inside it sit a program, its libraries, its settings, and a small runtime. Move that file to a "
    "laptop, to a cluster, or to the cloud, and what is inside does not change.",
    "B10_SealedBox",
    "A kraft box is taped shut on the left; four small labelled blocks drop into it first ('program', 'libraries', 'settings', 'runtime'), then the terracotta tape seals it. The sealed box slides in turn onto a laptop slab, a cluster rack and a cloud, and is the same box with the same four labels visible on a tag each time.",
    [{"at": 0.2, "event": "the four parts drop into the box and it is taped"}, {"at": 0.6, "event": "it moves to a laptop, a cluster and the cloud unchanged"}]))
add(manim("B11", A1,
    "You will meet three names. Docker is the most common tool, on laptops, cloud servers, and most published images. Singularity is "
    "the older name of the cluster tool. Apptainer is its current name, and it is what Northeastern's clusters, Explorer and AICR, use.",
    "B11_ThreeNames",
    "Three chips left to right: the Docker logo with 'laptops, cloud'; a plain mono chip 'singularity' with 'older name'; the Apptainer logo with 'Explorer, AICR'. An arrow labelled 'renamed' runs from singularity to Apptainer.",
    [{"at": 0.15, "event": "Docker, on laptops and cloud servers"}, {"at": 0.5, "event": "singularity, the older name"}, {"at": 0.8, "event": "Apptainer, current name, Explorer and AICR"}]))
add(manim("B12", A1,
    "Why not use Docker on a cluster? Docker's normal setup needs administrator-level power, and on a machine shared by thousands of "
    "people that is a security problem. Apptainer runs the container as you, with your permissions and no more. It can still read Docker images.",
    "B12_WhyApptainer",
    "A cluster rack in the middle with many small plain dots around it (the other users). Left: the Docker logo chip holds a large kraft key labelled 'admin' that reaches into the rack; a cross lands on it. Right: Professor Bear portrait beside the Apptainer logo chip; a small arrow 'as you' enters the rack with one small key; a thin arrow from a Docker logo image block 'image' into the Apptainer chip shows it reads Docker images; a terracotta check.",
    [{"at": 0.2, "event": "Docker needs admin power: a security problem on a shared machine"}, {"at": 0.55, "event": "Apptainer runs as you, no more"}, {"at": 0.88, "event": "it can still read Docker images"}]))

# ═════════════════════════════ ACT II · Why Use One ═════════════════════════════
add(manim("B20", A2,
    "First benefit: reproducible. The whole software stack is captured, so your result ties to one named, versioned image. A "
    "collaborator running it six months from now gets the same software, even after the system underneath has been updated.",
    "B20_Reproducible",
    "A result page on the left tied by a line to a sealed box tagged 'image 1.0'; a calendar strip scrolls forward with a label 'six months'; the cluster rack under the box swaps its top slab for a lighter one ('system updated') while the box and its tag stay exactly the same; a second Professor Bear portrait on the right opens the same box and a check lands.",
    [{"at": 0.2, "event": "the result ties to a named, versioned image"}, {"at": 0.55, "event": "six months pass; the system updates; the box does not change"}, {"at": 0.88, "event": "a collaborator gets the same software"}]))
add(manim("B21", A2,
    "Portable: the same file runs on your laptop, on Explorer, on another cluster, or in the cloud. And no dependency fights. Two "
    "tools that need incompatible versions of one library each get their own image, so neither one breaks the other.",
    "B21_PortableNoFights",
    "Top row: one sealed box with three arrows to a laptop, a rack and a cloud, a check on each. Bottom row: with no container, two tool blocks 'tool A' and 'tool B' reach for one shared library block 'library' labelled 'v1' and 'v2' and collide with a cross; then each tool block gets its own box with its own library ('v1' in one, 'v2' in the other), side by side, both checked.",
    [{"at": 0.15, "event": "the same box runs on laptop, cluster, cloud"}, {"at": 0.55, "event": "two tools want incompatible versions of one library"}, {"at": 0.85, "event": "each gets its own image: no clash"}]))
add(manim("B22", A2,
    "Shareable: it is one file you can hand to a collaborator, archive with your data, or point a reviewer at. And ready-made: "
    "registries such as Docker Hub, Key dot I O, NVIDIA's N G C, and BioContainers host thousands of maintained images.",
    "B22_ShareRegistries",
    "A sealed box in the middle with three short arrows to 'collaborator' (a Professor Bear portrait), 'archive with data' (a drawn folder) and 'reviewer' (a plain page); above, a shelf of four chips: the Docker logo ('Docker Hub'), a mono chip 'quay.io', the NVIDIA logo ('NGC'), a mono chip 'BioContainers', with small box shapes stacked on each.",
    [{"at": 0.15, "event": "one file: collaborator, archive, reviewer"}, {"at": 0.6, "event": "four registries each hold stacks of ready-made images"}]))
add(manim("B23", A2,
    "Containers cost something: images are large, and the first build takes effort. So try a module first, software the cluster "
    "already installed. Then conda, a package manager. Then a container, when the install is painful or you need a portable record.",
    "B23_TheLadder",
    "A three-step staircase drawn left to right, rising: 'module' (a plain labelled block, the cluster rack beside it), 'conda' (the conda-forge logo chip), 'container' (a sealed box). A small figure token is NOT used; a terracotta ring marks the step you take only when the previous one fails; an arrow climbs the steps on the spoken words, and a weight label 'large images' sits on the top step.",
    [{"at": 0.15, "event": "images are large; the first build takes effort"}, {"at": 0.4, "event": "module first"}, {"at": 0.6, "event": "then conda"}, {"at": 0.8, "event": "then a container"}]))

# ═════════════════════════════ ACT III · Running A Container ═════════════════════════════
shell("B30", A3,
    "Apptainer has three verbs. Exec runs one command inside the container, then returns. That is the verb for jobs. Shell opens an "
    "interactive shell inside it, for poking around and testing. And run does the container's built-in default action.",
    "III · Running A Container  ·  the three verbs",
    [cmd("apptainer exec <image> <command>"), cmd("apptainer shell <image>"), cmd("apptainer run <image>")],
    [None, "Exec runs", "Shell opens", "run does|and run"],
    [{"at": 0.05, "event": "the exec line"}, {"at": 0.4, "event": "the shell line"}, {"at": 0.8, "event": "the run line"}],
    ring_lines=[0], ring_phrases=["That is the verb"])
shell("B31", A3,
    "Check the tool first. Both commands are read-only and safe on a login node. On Explorer we recorded this: the path, and version "
    "one point four point five, installed system-wide, so there is no module to load. AICR has apptainer and singularity as well.",
    "Check the tool  ·  recorded on the Explorer login node",
    ["# recorded output, Explorer login node, read-only", cmd("command -v apptainer"), "/usr/bin/apptainer",
     cmd("apptainer --version"), "apptainer version 1.4.5-3.el9"],
    [None, "Both commands", "the path", "version 1", "installed system"],
    [{"at": 0.05, "event": "label: recorded output"}, {"at": 0.3, "event": "command -v and its recorded path"}, {"at": 0.65, "event": "--version and its recorded output"}],
    ring_lines=[4], ring_phrases=["installed system"])
add(manim("B32", A3,
    "Run containers on a compute node, never on the login node. The login node is shared by everyone, and heavy work there gets "
    "terminated. Ask Slurm for a compute node first with S run, then work inside that session.",
    "B32_ComputeNode",
    "Two racks: a small one 'login node' with a sealed box drawn on it and a cross; a larger one 'compute node'. The mono chip 'srun --pty bash' travels from the login rack to the compute rack, which lights up (a ghost light turns terracotta), and the sealed box then moves onto the compute rack with a check.",
    [{"at": 0.2, "event": "the login node is shared: the box is crossed out there"}, {"at": 0.6, "event": "srun --pty bash asks for a compute node"}, {"at": 0.88, "event": "the box runs on the compute node"}]))
shell("B33", A3,
    "Then open a shell in an image. The path is a placeholder for your own project. Your prompt changes to Apptainer, which tells you "
    "that you are inside. Type exit to leave. Inside, you have only what the image holds, plus the folders you bind in.",
    f"Open a shell in an image  ·  {NOTRUN}",
    [cmd("srun --pty bash"), cmd("apptainer shell /projects/<project>/containers/myimage.sif"), "Apptainer> exit"],
    [None, "Then open", "Your prompt changes", "Type exit"],
    [{"at": 0.05, "event": "srun for a compute node"}, {"at": 0.35, "event": "apptainer shell"}, {"at": 0.7, "event": "the prompt changes; exit leaves"}],
    ring_lines=[2], ring_phrases=["Your prompt changes"])
shell("B34", A3,
    "For a batch job, put the same command in a script. Ask for the partition, cores, memory and time your work needs, then run exec, "
    "binding your project folder in. Create the logs folder first, and submit with S batch.",
    f"A CPU job  ·  {NOTRUN}",
    [g("#SBATCH --job-name=container_cpu"), g("#SBATCH --partition=short"), g("#SBATCH --cpus-per-task=8"),
     g("#SBATCH --mem=32GB"), g("#SBATCH --time=04:00:00"), " ",
     *blk("apptainer exec \\", 4, nth=0), cmd("mkdir -p logs"), cmd("sbatch run_container.sh")],
    [None, "Ask for the partition", "cores", "memory", "time", None, "run exec", "binding", "project", "folder in", "Create the logs", "submit"],
    [{"at": 0.05, "event": "the resource lines"}, {"at": 0.45, "event": "the exec command with its bind"}, {"at": 0.85, "event": "mkdir and sbatch"}],
    ring_lines=[6, 7], ring_phrases=["run exec", "binding your"])
add(manim("B35", A3,
    "On a GPU, the container can carry its own CUDA, so you do not match the node's modules. But it still needs the node's driver. "
    "The dash dash N V flag passes that driver in. Without it, the container has no link to the GPU.",
    "B35_NvBridge",
    "A GPU-node rack at the bottom with the NVIDIA logo chip on it and a label 'driver'; above, a sealed container box holding a labelled block 'CUDA'. First the gap between them: a dashed link with a cross ('no GPU'); then the mono chip '--nv' lays a solid bridge from the driver up into the container and the cross is replaced by a terracotta check; a small label 'must fit' on the bridge joins 'CUDA' and 'driver'.",
    [{"at": 0.15, "event": "the container carries its own CUDA"}, {"at": 0.45, "event": "it still needs the node's driver: no link"}, {"at": 0.75, "event": "--nv bridges the driver in"}]))
shell("B36", A3,
    "For an interactive test, ask for one GPU. Naming the card type is good practice when the card matters, because a bare one can "
    "land on a different card. List the types first. Then run with dash dash N V, and bind your project.",
    f"A GPU test  ·  {NOTRUN}",
    [*wrap2(g("srun --partition=gpu-interactive"), " --mem=16GB", "$ "), cmd('sinfo -p gpu -o "%G"'),
     cmd(g("apptainer exec --nv --bind", 0).strip())],
    [None, "ask for one", "Naming the card", "List the types", "Then run"],
    [{"at": 0.05, "event": "the srun request for one GPU"}, {"at": 0.45, "event": "listing the types"}, {"at": 0.75, "event": "apptainer exec --nv with the bind"}],
    ring_lines=[0, 3], ring_phrases=["ask for one", "dash dash"], fs=26)
shell("B37", A3,
    "For a batch GPU job, here is a template: one GPU, and inside the partition's time limit. The container carries the software "
    "stack, the N V flag connects the driver, and the bind gives it your code.",
    f"A GPU batch job  ·  {NOTRUN}",
    [g("#SBATCH --partition=gpu"), g("#SBATCH --gres=gpu:1"), g("#SBATCH --cpus-per-task=8", 1), g("#SBATCH --mem=64GB"),
     g("#SBATCH --time=08:00:00"), " ", *blk("apptainer exec --nv \\", 4)],
    [None, "one GPU", "one GPU", "template", "time limit", None, "software stack", "NV", "bind", "your code"],
    [{"at": 0.05, "event": "partition and one GPU"}, {"at": 0.4, "event": "the time line"}, {"at": 0.75, "event": "exec --nv with the bind"}],
    ring_lines=[1, 4, 6], ring_phrases=["one GPU", "time limit", "NV"])
add(manim("B38", A3,
    "Check the partition limit before you write the script. On Explorer's G P U partition we read an eight hour limit, and two hours "
    "on the short and interactive ones. A published example asks for two GPUs for twelve hours. That cannot run there.",
    "B38_TimeLimits",
    "A horizontal time axis 0 to 12 h in 2 h ticks with three bars: 'gpu-interactive' to 2 h and 'gpu-short' to 2 h in grey, 'gpu' to 8 h in grey, each with its limit in mono ('2:00:00', '2:00:00', '8:00:00'). A fourth bar 'request' grows to 12 h and crosses a vertical limit line at 8 h; the part beyond is cut off and a cross lands. A mono chip '--gres=gpu:2' sits beside the request bar; a second chip '--gres=gpu:1' sits at the 8 h bar with a check.",
    [{"at": 0.15, "event": "the limits: 8 h on gpu, 2 h on the short and interactive partitions"}, {"at": 0.6, "event": "a 12 hour, two-GPU request overshoots"}, {"at": 0.88, "event": "it cannot run there"}]))
shell("B39", A3,
    "A container that starts is not a container that used the GPU. So print the card's name from inside it. With dash dash N V you "
    "should see true and a card name, and without it, false. We have not run this one.",
    f"Prove the GPU  ·  {NOTRUN}",
    [*wrap2(_pyline(), ' "import torch', "$ ")],
    [None, "print the", "With dash", "without it"],
    [{"at": 0.05, "event": "the one-line check"}, {"at": 0.6, "event": "expected: True and a card name, and False without --nv"}],
    ring_lines=[1], ring_phrases=["print the"], fs=30)

# ═════════════════════════════ ACT IV · Binding Folders ═════════════════════════════
add(manim("B40", A4,
    "A container sees its own filesystem, not the cluster's. On Explorer your home directory is bound for you. Slash projects and "
    "slash scratch are not. To read your data and write results, you bind each folder in.",
    "B40_WhatItSees",
    "A container box in the centre with an empty inside (dashed slots). Three folders on the left, outside: a 'home' folder with a terracotta dot, a mono '/projects' folder, a mono '/scratch' folder. 'home' slides in on its own; '/projects' and '/scratch' wait outside until the mono chip '--bind' draws a bridge for each and they slide in.",
    [{"at": 0.2, "event": "the container sees only its own filesystem; home slides in by itself"}, {"at": 0.55, "event": "/projects and /scratch stay outside"}, {"at": 0.85, "event": "--bind brings each in"}]))
shell("B41", A4,
    "The bind flag takes a folder on the host, a colon, and the path where it appears inside. Binding the same path on both sides is the "
    "simplest habit, because your script's paths then mean the same inside and out. Use absolute paths, and bind only what the job needs.",
    f"Bind  ·  {NOTRUN}",
    [cmd("apptainer exec --bind /host/path:/path/in/container myimage.sif <command>"), " ",
     *blk("apptainer exec \\", 4, nth=1)],
    [None, "takes a folder", None, "same path", "same path", "absolute paths", "only what"],
    [{"at": 0.05, "event": "the general form"}, {"at": 0.4, "event": "the same path on both sides, two binds"}, {"at": 0.85, "event": "only what the job needs"}],
    ring_lines=[2, 3], ring_phrases=["same path", "same path"], fs=36)
shell("B42", A4,
    "Or set one environment variable instead of repeating the flag. We put it inside each job script, so the script carries its own "
    "record, rather than in the dot bash R C file, which would be a permanent edit to a shared startup file.",
    f"APPTAINER_BIND  ·  {NOTRUN}",
    ["# inside the job script", g("export APPTAINER_BIND=")],
    [None, "one environment variable"],
    [{"at": 0.05, "event": "a label: inside the job script"}, {"at": 0.35, "event": "the export line"}],
    ring_lines=[0], ring_phrases=["inside each job"], fs=24)

# ═════════════════════════════ ACT V · Building An Image ═════════════════════════════
add(manim("B50", A5,
    "You cannot build an image on Explorer: building needs administrator rights. So build on a machine where you have them, like your "
    "own computer. Copy the finished S I F file to the cluster, store it in project space, and run it there as yourself.",
    "B50_BuildCopyRun",
    "Four stations left to right joined by arrows: (1) Professor Bear portrait beside a laptop slab with a mono label 'root' and the Docker and Apptainer logo chips, a sealed box emerges; (2) an arrow 'copy' carries the box; (3) a drawn folder 'project space' receives it; (4) a compute-node rack runs it, labelled 'as you'. A small wrench-and-cross is NOT drawn on the cluster; instead the cluster rack at the right carries a label 'no root'.",
    [{"at": 0.2, "event": "build where you have root"}, {"at": 0.5, "event": "copy the finished file to the cluster"}, {"at": 0.7, "event": "store it in project space"}, {"at": 0.9, "event": "run it as yourself"}]))
shell("B51", A5,
    "A dot def file is the recipe, and the most valuable file for reproducibility. Bootstrap and From name the base image to start from, "
    "with its tag pinned. Post runs once during the build, so install your packages there, at fixed versions.",
    f"myimage.def  ·  the recipe  ·  {NOTRUN}",
    [g("Bootstrap: docker"), g("From: python:3.11-slim"), " ", g("%post"), g("pip install --no-cache-dir")],
    [None, "Bootstrap and From", "base image", "Post runs", "install your packages"],
    [{"at": 0.05, "event": "Bootstrap and From, the base image"}, {"at": 0.45, "event": "%post and the pinned install"}],
    ring_lines=[1, 4], ring_phrases=["tag pinned", "fixed versions"])
shell("B52", A5,
    "The other sections: environment sets variables every time the container runs. Runscript is what apptainer run does. Labels hold "
    "metadata. The versions in the example are placeholders: pin the ones you actually tested. Then build it, on your own machine.",
    f"myimage.def, continued  ·  {NOTRUN}",
    [g("%environment"), g("export LC_ALL=C"), " ", g("%runscript"), g("python --version"), " ", g("%labels"),
     g("Author <your-name>"), g("Version 1.0"), " ", cmd("apptainer build myimage.sif myimage.def")],
    [None, "environment sets", None, "Run script", "Run script", None, "labels hold", "labels hold", "labels hold", None, "Then build"],
    [{"at": 0.05, "event": "%environment"}, {"at": 0.3, "event": "%runscript"}, {"at": 0.5, "event": "%labels"}, {"at": 0.85, "event": "the build command"}],
    ring_lines=[10], ring_phrases=["Then build"])
add(manim("B53", A5,
    "If you already have a Dockerfile, build the Docker image on your own machine, then convert it. Docker builds the image. "
    "Apptainer reads it from Docker's local store and writes the S I F file. Or push the image to a registry, and pull it on the cluster.",
    "B53_DockerRoute",
    "Left to right: a drawn page 'Dockerfile' -> the Docker logo chip with a mono label 'docker build' -> a sealed box 'image' -> the Apptainer logo chip with 'apptainer build' -> a box labelled '.sif'. A second branch drops from the image box down to a cloud 'registry' and then to a compute-node rack with 'pull' in mono.",
    [{"at": 0.15, "event": "Dockerfile to Docker to an image"}, {"at": 0.5, "event": "Apptainer converts the image into a .sif"}, {"at": 0.85, "event": "or push to a registry and pull on the cluster"}]))
shell("B54", A5,
    "A Dockerfile starts from a base operating system image, and uses RUN lines to install packages. A good one ends with a line that "
    "imports your tool, so the build fails early if the install is broken. Here is the shape, from a real example.",
    f"A Dockerfile, abridged  ·  {NOTRUN}",
    [o("FROM rockylinux:9.3"), o("RUN pip3 install CDPKit"), " ", o("# Verify installation"), o("RUN python3 -c"), " ", o('CMD ["/bin/bash"]')],
    [None, "base operating system", "install packages", None, "ends with a line", "ends with a line", None],
    [{"at": 0.05, "event": "FROM and the install"}, {"at": 0.5, "event": "the verifying import"}],
    ring_lines=[0, 4], ring_phrases=["base operating system", "imports your tool"])
shell("B55", A5,
    "Then two commands, on your own machine. Docker build, with a name and a version. Then apptainer build, reading the image from "
    "Docker's local store.",
    f"Docker image to .sif  ·  {NOTRUN}",
    [cmd("docker build -t myimage:1.0 ."), cmd("apptainer build myimage.sif docker-daemon://myimage:1.0")],
    [None, "Docker build", "Aptainer build"],
    [{"at": 0.05, "event": "docker build"}, {"at": 0.5, "event": "apptainer build from docker-daemon"}],
    ring_lines=[1], ring_phrases=["Docker's local"])
shell("B56", A5,
    "A third option is the remote builder. It needs a free account with the maker, and it uploads your recipe to a third party, so "
    "that is your decision, not an agent's. If you choose it, one flag does it. If a build fails, read the error text.",
    f"The remote builder  ·  {NOTRUN}",
    [cmd("apptainer build myimage.sif myimage.def"), " ", cmd("apptainer build --remote myimage.sif myimage.def")],
    [None, None, "If you choose"],
    [{"at": 0.05, "event": "the local build, for contrast"}, {"at": 0.6, "event": "the remote build: one flag added"}],
    ring_lines=[2], ring_phrases=["one flag"], fs=40)

# ═════════════════════════════ ACT VI · Getting An Image Onto The Cluster ═════════════════════════════
shell("B60", A6,
    "To get an image onto the cluster, pull it from a registry. Pulling is heavy, so do it on a compute node. This writes a S I F file "
    "named ubuntu, underscore, twenty-two point oh four. Add a name flag to choose your own.",
    f"VI · Pull an image  ·  {NOTRUN}",
    [cmd("srun --pty bash"), cmd("apptainer pull docker://ubuntu:22.04"), cmd("apptainer pull --name myubuntu.sif docker://ubuntu:22.04")],
    [None, "pull it from", "This writes", "Add a name"],
    [{"at": 0.05, "event": "a compute node first"}, {"at": 0.4, "event": "the pull"}, {"at": 0.8, "event": "the --name form"}],
    ring_lines=[0, 2], ring_phrases=["compute node", "name flag"])
shell("B61", A6,
    "Other registries work the same way. Docker Hub for a tool like G A T K, the NVIDIA catalogue for GPU images, BioContainers for "
    "bioinformatics, and the Sigh-labs library. The first three name an exact version. The last has no tag at all, so pin one there too.",
    f"Other registries  ·  {NOTRUN}",
    [cmd("apptainer pull docker://broadinstitute/gatk:4.5.0.0"), cmd("apptainer pull docker://nvcr.io/nvidia/pytorch:24.01-py3"),
     cmd("apptainer pull docker://biocontainers/samtools:v1.9-4-deb_cv1"), cmd("apptainer pull library://lolcow")],
    [None, "Docker Hub", "NVIDIA", "bio containers", "SciLabs"],
    [{"at": 0.05, "event": "Docker Hub, GATK"}, {"at": 0.3, "event": "NGC"}, {"at": 0.5, "event": "BioContainers"}, {"at": 0.75, "event": "Sylabs library, no tag"}],
    ring_lines=[3], ring_phrases=["no tag"])
add(manim("B62", A6,
    "Always pin the tag. A tag called latest points at a different image next month. A pinned tag keeps pointing at the same one. "
    "So never use latest for anything you must reproduce, and write the exact tag into your methods.",
    "B62_PinTheTag",
    "Two rows on a month timeline ('today', 'next month'). Top row: a mono tag ':latest' points to a sealed box 'A' today and, next month, the same tag has its arrow swung to a different box 'B' (a cross lands). Bottom row: a mono tag ':4.5.0.0' keeps its arrow on box 'A' both months (a terracotta check). A page 'methods' receives the pinned tag.",
    [{"at": 0.15, "event": "latest points at a different image next month"}, {"at": 0.5, "event": "a pinned tag keeps pointing at the same one"}, {"at": 0.85, "event": "the exact tag goes into your methods"}]))
shell("B63", A6,
    "If you built the file on your own computer, copy it through the transfer node into project space. Check Research Computing's "
    "documentation for the current transfer host first. For smaller files, the Open OnDemand Files app uploads up to ten gigabytes.",
    f"Copy a local build  ·  {NOTRUN}",
    ["# run this on your own computer", cmd(g("scp myimage.sif")), " ", "# smaller files: the Open OnDemand Files app, up to 10 GB"],
    [None, "copy it through", None, "open on demand"],
    [{"at": 0.05, "event": "run on your own computer"}, {"at": 0.3, "event": "the scp line"}, {"at": 0.8, "event": "the OnDemand alternative"}],
    ring_lines=[1], ring_phrases=["current transfer host"], fs=31)
add(manim("B64", A6,
    "Keep images in your project's containers folder, not in home. Project space is shared with your lab, and is not covered by the "
    "seventy-five gigabyte home quota. Keep the recipe next to the image, commit it, and archive the image with your data.",
    "B64_WhereToKeep",
    "Left: a small 'home' box with a quota gauge reading '75 GB' and a cross over a .sif dropped toward it. Right: a drawn folder 'containers/' in project space receives the .sif and a page '.def' that lands beside it; a terracotta dot marks a 'commit' (a small git-logo chip is NOT needed: use a mono chip 'git'); finally the pair slides into an 'archive with data' box.",
    [{"at": 0.15, "event": "not in home: the quota"}, {"at": 0.45, "event": "in project space, shared with the lab"}, {"at": 0.75, "event": "recipe beside the image, committed"}, {"at": 0.92, "event": "archived with the data"}]))

# ═════════════════════════════ ACT VII · Habits That Keep It Honest ═════════════════════════════
shell("B70", A7,
    "Apptainer keeps pulled layers in a hidden folder in your home directory, and a big pull can fill your quota, after which your "
    "OnDemand sessions stop working. Point both locations at project space before any large pull. The cache is only a cache.",
    f"VII · Cache off home  ·  {NOTRUN}",
    [g("export APPTAINER_CACHEDIR="), g("export APPTAINER_TMPDIR="), " ", "# the cache can be emptied safely; this is the gentler tool", cmd("apptainer cache clean all")],
    [None, "Point both", "Point both", None, "only a cache"],
    [{"at": 0.05, "event": "the cache directory"}, {"at": 0.35, "event": "the temporary directory"}, {"at": 0.8, "event": "the gentler clean-up"}],
    ring_lines=[0, 1], ring_phrases=["Point both", "project space"])
shell("B71", A7,
    "Before a long job, test by hand on a compute node: open a shell, run your commands, check they find their files. Then print "
    "versions from inside. A job that finishes has not proved it used the container, the binds and the GPU you meant.",
    f"Test first, then check  ·  {NOTRUN}",
    ["# 1. test by hand, in a compute-node session", cmd("srun --pty bash"), cmd("apptainer shell /projects/<project>/containers/myimage.sif"), " ",
     "# 2. print versions from inside", cmd("apptainer exec myimage.sif python --version")],
    [None, "test by hand", "open a shell", None, "print", "versions from inside"],
    [{"at": 0.05, "event": "test by hand first"}, {"at": 0.6, "event": "print the version from inside"}],
    ring_lines=[5], ring_phrases=["versions from inside"])
add(manim("B72", A7,
    "Record the image. Write down the exact tag, and ideally the digest, in your notes and methods. For a locally built image, the "
    "recipe plus the S I F file is the record. A checksum from S H A two fifty six sum lets a collaborator confirm they hold the same file.",
    "B72_RecordIt",
    "A notes page on the left collects three stamped lines one by one ('tag', 'digest', '.def + .sif'). On the right two sealed boxes 'mine' and 'theirs' face each other with the mono chip 'sha256sum myimage.sif' under each and an equals sign between them, then a terracotta check.",
    [{"at": 0.15, "event": "tag and digest stamped into the notes"}, {"at": 0.45, "event": "the recipe plus the .sif is the record"}, {"at": 0.75, "event": "sha256sum: the same file on both sides"}]))
add(manim("B73", A7,
    "Workflow managers like Nextflow and Snakemake can run each step of a pipeline in its own container, so every tool carries its own "
    "version. That is a strong pattern for reproducible pipelines, and Research Computing offers help setting it up.",
    "B73_WorkflowManager",
    "A pipeline of three steps on a conveyor ('step 1', 'step 2', 'step 3'), each step inside its own sealed box carrying a different small version tag ('v1', 'v2', 'v3' in mono); two mono chips 'nextflow' and 'snakemake' sit above as the managers with arrows to the line; the boxes light one after another as the work passes.",
    [{"at": 0.2, "event": "managers run each step in its own container"}, {"at": 0.6, "event": "every tool carries its own version"}]))
add(manim("B74", A7,
    "On AICR, apptainer and singularity are both installed. But we have no documentation of container policy there: nothing on binds "
    "or storage. The partition fixes the GPU type, so you add no type to the gres request. Do not copy Explorer's paths; ask AICR support.",
    "B74_AicrContainers",
    "The large AICR rack (aicr_rack) labelled 'AICR' with two chips beside it: the Apptainer logo chip and a mono chip 'singularity', both with a check. Under the rack, a stamped plaque 'container policy: not documented' and a mono '--gres=gpu:1' with the type slot crossed ('no type'); a chip '/projects' crossed with the label 'Explorer paths'; a small question chip 'ask AICR support'.",
    [{"at": 0.15, "event": "apptainer and singularity installed"}, {"at": 0.45, "event": "container policy: not documented"}, {"at": 0.8, "event": "no GPU type in gres; do not copy Explorer's paths"}]))

# ═════════════════════════════ ACT VIII · What Was Checked ═════════════════════════════
add(manim("B80", A8,
    "Here is what we checked, and what we only read. On the login node, read-only: the path and version of Apptainer, that no module is "
    "needed, and the G P U partition limits. We did not run a container, pull an image, build one, or submit a job. The rest came from the source.",
    "B80_CheckedVsRead",
    "Two columns of stamped plain items, with dashed placeholder slots visible from the start. Left 'checked on the login node': 'apptainer 1.4.5', 'no module needed', 'GPU time limits'. Right 'only read, not run': 'run a container', 'pull an image', 'build an image', 'submit a job'. Stamps land on the spoken words; the right-hand column carries a ringed chip 'from the source'.",
    [{"at": 0.15, "event": "three read-only checks stamp in"}, {"at": 0.5, "event": "four things we did not run"}, {"at": 0.88, "event": "the rest came from the source"}], sparse=False))

# ───────────────────────────── the closing three ─────────────────────────────
RECAP = ["A container is one sealed file holding a program and everything it needs.",
         "Apptainer runs it as you, so it fits a shared cluster.",
         "Run on a compute node with exec, shell or run, add the N V flag for a GPU, and bind every folder the job needs.",
         "Build where you have root, never on the cluster, then copy the finished file in.",
         "Pull on a compute node, pin the tag, and keep the recipe beside the image.",
         "Record the image, and say plainly what you tested and what you only read."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. A container is one sealed file holding a program and everything it needs. Apptainer runs it as you, so it fits "
    "a shared cluster. Run on a compute node with exec, shell or run, add the N V flag for a GPU, and bind every folder the job needs. Build where you "
    "have root, never on the cluster, then copy the finished file in. Pull on a compute node, pin the tag, and keep the recipe beside the image. And record "
    "the image, and say plainly what you tested and what you only read.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land in narration order"}],
    lane="bookend", lead_silence_s=0.5,
    qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("Replace PROGRAM with a tool you use. I run PROGRAM on the Explorer cluster. Is there a module for it, a conda package, or a "
             "published container image? Check module avail and the registries, tell me which option you would choose and why, and write the "
             "exact apptainer pull and apptainer exec commands with a pinned tag and my project binds. Do not run anything on the login node "
             "and do not submit any job.")
YT_SPOKEN = YT_PROMPT
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_SPOKEN + " Then check two things yourself. Did Claude name a pinned tag and your project binds? "
    "And did it run nothing and submit nothing?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Module, Conda Or Container", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did Claude give a pinned tag and your project binds in the pull and exec commands?",
                "Check: did it run nothing and submit no job? It should only look up and plan."],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": "Scientific Reproducibility Three: Containers. At Nik Bear Brown.", "estimated_duration_s": 5.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Scientific Reproducibility Three: Containers. How to put a program and everything it "
                           "needs into one file, run it on a cluster with Apptainer, and record it so someone else can repeat your results.",
         "estimated_duration_s": 14.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · CONTAINERS", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German (Hallo)",
    "audience": "A researcher who wants to run, build and record software containers with Apptainer on a Northeastern cluster; assumes no other film or book",
    "source_doc": "hpc-aicr/guides/scientific-reproducibility-iii.md and the lesson it rewrites, hpc-aicr/Scientific-Reproducibility-III-2026/scientific-reproducibility3.md (read in full; commands shown verbatim), plus HPC.md Section 8 and the recorded read-only checks",
    "playlist": "Northeastern HPC and AICR",
    "series_title": "Research Computing on Explorer and AICR",
    "lecture_opening_description": "Seal a program into one file and run it on a cluster",
    "lecture_opening_title_lines": ["Scientific", "Reproducibility III:", "Containers"],
    "tags": ["containers", "Apptainer", "Singularity", "Docker", "reproducibility", "HPC", "Slurm", "GPU", "Explorer", "AICR",
             "Northeastern University", "Research Computing", "Nik Bear Brown"]},
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

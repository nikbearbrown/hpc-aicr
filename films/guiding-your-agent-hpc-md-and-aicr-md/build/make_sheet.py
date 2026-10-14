#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-guiding-your-agent-hpc-md-and-aicr-md.

LECTURE (Bear, 2026-10-02): the WHOLE source as one act-structured film, primarily visual, best visual per beat from
the full playset, a tool shown as itself. Skill doctrine: brutalist.art/skills/make/lecture/SKILL.md.

Source:   hpc-aicr/skills/hpc/HPC.md and hpc-aicr/skills/aicr/AICR.md (the two files themselves) + STORY.md here.
Evidence: every file excerpt on a terminal beat is READ FROM THE FILE at build time by fl() below (a missing line stops the build),
          and the three "real mistakes" in Act IV trace to ../claude-liam-lecture-making-lecture-films-on-explorer/SESSION.md.

Spine: BOPEN -> BIDEA -> BDEFS -> five acts -> BVDT -> BHTF -> BOUT.
Two passes: pass 1 (no _qc/asr.json) estimates cues; after Kokoro + faster-whisper, pass 2 places every terminal line
and code line on the word Liam says (word times in _qc/asr.json).
"""
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Guiding Your Agent: HPC.md and AICR.md"
CAP = "lecture-guiding-your-agent-hpc-md-and-aicr-md"      # captures: none (every tool beat is real file text)
ART = HERE.parents[2] / "brutalist.art"
FPS = 30

ASR = {}
_ap = HERE / "_qc/asr.json"
if _ap.exists():
    ASR = json.loads(_ap.read_text())


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word_t(bid, phrase, nth=0, default=None):
    """Seconds at which `phrase` starts in beat `bid`'s spoken audio (faster-whisper word times), or `default`.
    `phrase` may hold alternatives separated by '|' (the recogniser writes 'user name' as 'username', '600' for 'six hundred')."""
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
    """Frame cues, one per phrase: measured word time when known, else the phrase's character share of the estimate.
    Cues never run backwards (a line cannot land before the line above it)."""
    out, last = [], 0
    for ph in phrases:
        if ph is None:
            out.append(0)                      # on screen from frame 0
            continue
        if isinstance(ph, (int, float)):
            c = max(1, fr(ph), last); out.append(c); last = c
            continue
        t = word_t(bid, ph)
        if t is None:
            print(f"  [cue-fallback] {bid}: '{ph}' not in the recognised words; using the character share")
            alt = ph.split("|")[0]
            i = narration.find(alt)
            t = (est_dur * i / max(1, len(narration))) if i >= 0 else 0.5
        c = max(1, fr(t - 0.15), last)
        out.append(c)
        last = c
    return out


def clear_midpoint(bid, cues):
    """GATE T and Gate V sample the beat's MIDPOINT: no line may be landing (a ~14-frame spring) around it. A cue that
    would start inside (mid-21 .. mid+7 frames) is moved to mid+9 frames. Needs the measured duration (pass 2)."""
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




SK = HERE.parents[1] / "skills"                     # hpc-aicr/skills
FILES = {"HPC": SK / "hpc/HPC.md", "AICR": SK / "aicr/AICR.md"}
_FL = {k: v.read_text().splitlines() for k, v in FILES.items()}


def fl(which, start, maxlen=112, focus=None):
    """The FIRST line of HPC.md / AICR.md that starts with `start`, verbatim; cut at a word boundary with an ellipsis if longer
    than maxlen. Stops the build if the line is not in the file (a film must never invent file text)."""
    for ln in _FL[which]:
        if ln.startswith(start):
            if focus and focus in ln and len(ln) > maxlen:          # a verbatim window around `focus`, cut at word boundaries
                i = ln.index(focus); a = max(0, i - (maxlen - len(focus) - 12)); b = min(len(ln), i + len(focus) + 12)
                if a: a = ln.index(" ", a) + 1
                if b < len(ln): b = ln.rindex(" ", 0, b)
                return ("… " if a else "") + ln[a:b] + (" …" if b < len(ln) else "")
            if len(ln) <= maxlen:
                return ln
            cut = ln[:maxlen].rsplit(" ", 1)[0]
            return cut + " …"
    raise SystemExit(f"fl: no line starting with {start!r} in {which}.md")
A1, A2, A3, A4, A5 = ("I · Why An Agent Needs Rules", "II · Walking Through HPC.md", "III · What AICR.md Changes",
                      "IV · Rules Born From Real Mistakes", "V · Using The Files")

# ───────────────────────────── the opening pair ─────────────────────────────
OPEN = [
 remotion("BIDEA", "the idea",
    "Hallo. This is Liam, in for Bear. First, a correction. To let an agent work on a cluster, you do not just say, run my "
    "job. The cluster is shared, and the agent is fast and literal. You give it two short rule files first, and you point it "
    "at them.",
    "BrutalistHesitantWriter",
    {"text": "To use Claude on a cluster,\nI just say: run my job", "triggerWords": "I just say: run my job",
     "replacementWords": "give it rules first", "fontSize": 66, "charMs": 62, "hesitateBetween": 6,
     "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'To use Claude on a cluster, I just say: run my job'"},
     {"at": 0.35, "event": "backspaces 'I just say: run my job' -> 'give it rules first'"}],
    lane="bookend", lead_silence_s=0.8,
    motion_claim="The writer types the newcomer's framing (I just say: run my job) and corrects it to the real one (give it rules first).",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Five terms. A rule file: a plain text file the agent reads before it acts. A hard never: a rule with no exceptions. A "
    "login node: the shared computer you land on when you connect. A Slurm job: your request for a compute node, written as "
    "a script. And fairshare: the priority you lose when you ask for more than you use.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "Rule file", "meaning": "a text file the agent reads before it acts"},
               {"term": "Hard never", "meaning": "a rule with no exceptions"},
               {"term": "Login node", "meaning": "the shared computer you land on when you connect"},
               {"term": "Slurm job", "meaning": "your request for a compute node, as a script"},
               {"term": "Fairshare", "meaning": "the priority you lose by asking for more than you use"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "'Rule file' lands"}, {"at": 0.3, "event": "'Hard never'"}, {"at": 0.5, "event": "'Login node'"},
     {"at": 0.7, "event": "'Slurm job'"}, {"at": 0.87, "event": "'Fairshare'"}],
    gate="CARD", lane="bookend",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: five prerequisites, one line each."}),
]

B = []


def add(b):
    B.append(b)
    return b


def shell(bid, act, narration, title, lines, cue_phrases, show, ring_lines=None, ring_phrases=None, fs=None, margin=None,
          motion_claim="The real file text prints line by line, each as it is spoken."):
    """A CCPlainShell beat. cue_phrases: one phrase (or None = already on screen) per line."""
    cues = cues_for(bid, cue_phrases, narration, est(narration))
    cues = clear_midpoint(bid, cues)
    props = {"title": title, "lines": lines, "startCue": 20, "lineGap": 30, "lineCues": cues}
    if fs:
        props["fontSize"] = fs
    if margin:
        props["windowMargin"] = margin
    if ring_lines is not None:
        props["rings"] = [{"line": ln, "cue": clear_midpoint(bid, [cues_for(bid, [ph], narration, est(narration))[0] + 12])[0]}
                          for ln, ph in zip(ring_lines, ring_phrases)]
    return add(remotion(bid, act, narration, "CCPlainShell", props, show, motion_claim=motion_claim))


# ═════════════════════════════ ACT I · Why An Agent Needs Rules ═════════════════════════════
add(manim("B10", A1,
    "An agent is fast, literal, and never tired. That is the good news. On a shared cluster it is also the risk. It will do "
    "exactly what you asked, as many times as you asked, and it will not feel the cost to anyone else.",
    "B10_FastAndLiteral",
    "On the left a Claude logo chip (logo_chip('claude')) with a stopwatch and a stack of many small 'job' boxes flying out fast; on the right a shared rack grid with several small dark racks that each get a different terracotta dot (other people's work); the boxes pile into one rack and its dots crowd out the others.",
    [{"at": 0.2, "event": "the agent chip, fast, many job boxes"}, {"at": 0.55, "event": "the shared racks appear"}, {"at": 0.85, "event": "one rack fills; the others dim"}]))
add(manim("B11", A1,
    "Most trouble on a cluster is not hard computer science. It is work on the wrong machine. It is a request far bigger than "
    "the job. And it is a check that passes when it should fail. These are quiet failures: nothing crashes, and you find out later.",
    "B11_ThreeQuietFailures",
    "Three plain cards fan out, each with a short mono label and one small drawing: 'login node' (a door rack with a running job), '8 h for 25 min' (a long bar with a short filled part), 'exit 0, no CUDA' (a check mark over a rack whose GPU slot is empty); a 'no error' tag lands on all three.",
    [{"at": 0.2, "event": "wrong machine: login node"}, {"at": 0.45, "event": "wrong size: 8 h for 25 min"}, {"at": 0.7, "event": "passing check: exit 0, no CUDA"}, {"at": 0.9, "event": "'no error' on all three"}]))
add(manim("B12", A1,
    "So there are two files. H P C dot M D holds the rules for any shared cluster, written for Northeastern's Explorer. AICR "
    "dot M D builds on it and adds what is different or stricter on the AICR GPU cluster. Read the first, then the second.",
    "B12_TwoFiles",
    "Two document pages stacked: the lower labelled 'HPC.md' with the subtitle 'any shared cluster (Explorer)', the upper labelled 'AICR.md' with 'stricter on AICR'; an arrow 'builds on' from the upper to the lower; a number-free reading order shown as 'first' on HPC.md and 'then' on AICR.md.",
    [{"at": 0.25, "event": "HPC.md page: any shared cluster"}, {"at": 0.6, "event": "AICR.md page lands on it: builds on"}, {"at": 0.88, "event": "first / then labels"}]))
shell("B13", A1,
    "You do not paste either file into your instructions. You put one line in your Claude dot M D or agents dot M D, and the "
    "agent reads the files when the work is cluster work. Here are the two lines, copied from the files themselves.",
    "The one line, from HPC.md and from AICR.md",
    [fl("HPC", "> When a task involves a research computing cluster", 108),
     fl("AICR", "> When a task involves the AICR cluster", 108)],
    ["Here are the two lines", "Here are the two lines"],
    [{"at": 0.4, "event": "the HPC.md line"}, {"at": 0.75, "event": "the AICR.md line"}],
    ring_lines=[0, 1], ring_phrases=["Claude dot M D", "agents dot M D"], fs=30, margin=50)

# ═════════════════════════════ ACT II · Walking Through HPC.md ═════════════════════════════
shell("B20", A2,
    "Open the file H P C dot M D and the first thing you see is not a rule. It is a short summary: what it is, why it exists, what was "
    "found, and what is not verified. Then a line that says everything below is for the agent. Then fourteen numbered sections, zero to thirteen, and an "
    "honest appendix of conflicts.",
    "II · Walking Through HPC.md  ·  the headings, from the file",
    [fl("HPC", "# HPC.md:", 80), fl("HPC", "# Agent rules", 80), fl("HPC", "## 0. Prime directive", 80),
     fl("HPC", "## 1. Hard NEVERs", 80), fl("HPC", "## 2. Before the first command", 80),
     fl("HPC", "## 6. GPUs", 80), fl("HPC", "## 9. Reproducibility", 80),
     fl("HPC", "## 12. Slurm scripting traps", 80), fl("HPC", "# Appendix A", 80)],
    [None, "everything below is for the agent", "fourteen numbered sections", "fourteen numbered sections", "fourteen numbered sections", "fourteen numbered sections", "fourteen numbered sections", "fourteen numbered sections", "an honest appendix"],
    [{"at": 0.05, "event": "the title"}, {"at": 0.4, "event": "the agent line, then sections"}, {"at": 0.9, "event": "the appendix of conflicts"}],
    ring_lines=[1, 8], ring_phrases=["everything below is for the agent", "an honest appendix"], fs=34)
add(manim("B21", A2,
    "Section zero is the prime directive. The agent does the pipeline work: inspect, measure, size, check, keep records. The "
    "researcher keeps the judgment: what to spend, who gets access, and anything that cannot be undone. Look before you act. "
    "Measure before you change. Ask before you spend, delete, or share.",
    "B21_PrimeDirective",
    "A split drawing: left column 'agent' (a Claude logo chip) with four small verbs inspect / measure / size / record on ticks; right column 'you' (Professor Bear portrait, 1x1) with 'spend', 'access', 'cannot undo' as three chips; a bold horizontal rule between them; three phrases 'look first', 'measure first', 'ask first' land along the rule.",
    [{"at": 0.2, "event": "agent column"}, {"at": 0.45, "event": "you column"}, {"at": 0.75, "event": "look, measure, ask along the rule"}]))
add(manim("B22", A2,
    "Section one is the list the agent checks before every command. Never run computation on a login node. Never ask for, read, "
    "or print a password or a key. Never delete without listing what will go and getting a yes. Never submit a job until you "
    "have confirmed what it asks for. Never cancel with S cancel dash u. And never invent a flag, a module, or a limit.",
    "B22_HardNevers",
    "A drawn table builds row by row, six rows each starting with a bold 'never' chip and a short mono item: 'compute on a login node', 'password or key', 'delete without a list', 'submit unconfirmed', 'scancel -u', 'invent a flag'; each row gets a small cross mark as it lands.",
    [{"at": 0.15, "event": "login node row"}, {"at": 0.3, "event": "password row"}, {"at": 0.45, "event": "delete row"}, {"at": 0.6, "event": "submit row"}, {"at": 0.75, "event": "scancel row"}, {"at": 0.9, "event": "invent row"}], sparse=True))
shell("B23", A2,
    "Notice that every never comes with a because. A rule the agent understands is a rule it can apply to a case the file never "
    "listed. And some rules are labelled house rule, because they are our judgment, not the cluster's policy.",
    "HPC.md · three rows from the hard-never table",
    [fl("HPC", "| `sudo`, `apt install`", 118), fl("HPC", "| Poll the scheduler in a tight loop", 118, focus="(house rule)"), fl("HPC", "| Invent a flag, module name", 118)],
    [None, "house rule", "Notice that every never comes with a because"],
    [{"at": 0.05, "event": "sudo row"}, {"at": 0.5, "event": "poll row: house rule"}, {"at": 0.85, "event": "invent a flag row"}],
    ring_lines=[1], ring_phrases=["house rule"], fs=28, margin=50)
shell("B24", A2,
    "Section two is before the first command. If a read-only command can answer a question, the agent runs it instead of "
    "asking you. Who am I, where am I, which groups, what is free. It asks only what only you can answer: your access, what it "
    "may submit, whether the data is restricted, and what you are trying to do.",
    "HPC.md · Section 2, from the file",
    [fl("HPC", "**Read or measure first;", 112), "…", fl("HPC", "**Must ask**", 112),
     fl("HPC", "1. **Access:**", 112), fl("HPC", "3. **Data:**", 112)],
    [None, "If a read-only command", "It asks only what only you can answer", "your access", "restricted"],
    [{"at": 0.05, "event": "read or measure first"}, {"at": 0.5, "event": "must ask"}, {"at": 0.85, "event": "access and data"}],
    ring_lines=[0, 2], ring_phrases=["If a read-only command", "It asks only what only you can answer"], fs=28, margin=50)
add(manim("B25", A2,
    "Section four stops the agent asking for more than it needs. Is parallel even the answer? In Research Computing's own "
    "benchmark, one core took two hundred fifty seconds. Eight cores took twenty-nine. Twelve cores took thirty-three, slower "
    "than eight. Never promise that N cores is N times faster.",
    "B25_TwelveSlowerThanEight",
    "A bar chart with six bars labelled by cores and real seconds: 1 core 250.7 s; 2 cores 116.8; 4 cores 58.1; 8 cores 29.4; 12 cores 33.4 (this bar ringed in terracotta and a small 'slower than 8' tag); 16 cores 25.2; the 20-core bar 20.2 s lands last. Bars grow on the spoken numbers.",
    [{"at": 0.2, "event": "1 core: 250.7 s"}, {"at": 0.5, "event": "8 cores: 29.4 s"}, {"at": 0.7, "event": "12 cores: 33.4 s, ringed, slower than 8"}, {"at": 0.9, "event": "never promise N times faster"}], sparse=False))
shell("B26", A2,
    "Section five: every script states its numbers. Partition, time, memory, cores, a name, and a log file. Time is the "
    "expected runtime plus about twenty percent, never the maximum just to be safe. And memory is computer memory, not GPU memory.",
    "HPC.md · Section 5, from the file",
    [fl("HPC", "- Always set `--partition`", 110), fl("HPC", "- **`--time` = expected runtime", 110), fl("HPC", "- **`--mem` is CPU RAM", 110)],
    [None, "Time is the expected runtime", "memory is computer memory"],
    [{"at": 0.05, "event": "always set"}, {"at": 0.45, "event": "time = runtime + 20%"}, {"at": 0.8, "event": "mem is CPU RAM"}],
    ring_lines=[1, 2], ring_phrases=["plus about twenty percent", "not GPU memory"], fs=28, margin=50)
shell("B27", A2,
    "Section six is GPUs. Never trust the allocation. A job that worked may have run on the processor with no error. So every "
    "GPU script proves the GPU is there before the expensive part: the device name, the memory, and a number that travels to the "
    "GPU and back.",
    "HPC.md · Section 6, from the file",
    [fl("HPC", "**Never trust the allocation;", 116), fl("HPC", "**A GPU is the right tool only", 116)],
    [None, "Never trust the allocation"],
    [{"at": 0.1, "event": "never trust the allocation"}, {"at": 0.6, "event": "when a GPU is the right tool"}],
    ring_lines=[0], ring_phrases=["proves the GPU is there"], fs=30, margin=50)
add(manim("B28", A2,
    "Section seven is where files live. Code and environments in home. Temporary job data in scratch, which is wiped on the "
    "first Tuesday of every month. Anything you keep in projects. And the agent never keeps the only copy of anything in scratch.",
    "B28_WhereFilesLive",
    "Three folder boxes: 'home' (code, environments), 'scratch' (a calendar page 'first Tuesday' with a sweep that empties it), 'projects' (long-term, a check); a kraft box labelled 'only copy' is carried out of scratch and set down in projects just before the sweep.",
    [{"at": 0.2, "event": "home: code, environments"}, {"at": 0.45, "event": "scratch: wiped the first Tuesday"}, {"at": 0.7, "event": "projects: kept"}, {"at": 0.9, "event": "the only copy moves out before the sweep"}]))
add(manim("B29", A2,
    "Section eight is software, in order. First a module. Then conda. Then a container built on your own machine. Then a source "
    "build. And a tool like Spack only last, because each step down costs more to keep. Before installing anything, the agent "
    "checks whether a module already exists.",
    "B29_InstallLadder",
    "A five-rung ladder drawn top to bottom: 'module', 'conda', 'container (built at home)', 'source build', 'Spack / EasyBuild (last)'; a cost bar grows wider with each rung; a magnifier 'module avail' sweeps the top rung first.",
    [{"at": 0.2, "event": "module"}, {"at": 0.4, "event": "conda"}, {"at": 0.55, "event": "container"}, {"at": 0.7, "event": "source build"}, {"at": 0.85, "event": "Spack last; the cost bar widens"}]))
shell("B30", A2,
    "Section nine is the record every job leaves behind. The job and node. When it started. The git commit it ran from. The "
    "exact command, the parameters, the seeds, the inputs. The software, and the hardware it really used. Twelve items, so a "
    "stranger can rerun it.",
    "HPC.md · Section 9, the minimum record",
    [fl("HPC", "  1. job ID", 96), fl("HPC", "  3. git commit hash", 96), fl("HPC", "  6. every random seed", 96),
     fl("HPC", "  10. hardware actually used", 96), fl("HPC", "  12. exit status", 96)],
    [None, "The git commit it ran from", "the seeds", "the hardware it really used", "Twelve items"],
    [{"at": 0.05, "event": "item 1"}, {"at": 0.4, "event": "item 3, the commit"}, {"at": 0.6, "event": "seeds"}, {"at": 0.85, "event": "item 12, so a stranger can rerun"}],
    ring_lines=[1, 4], ring_phrases=["The git commit it ran from", "Twelve items"], fs=32, margin=50)
shell("B31", A2,
    "Section ten is about being an agent on the cluster. The researcher creates and unlocks the key, never the agent. If a "
    "command prompts, hangs, or says permission denied, the agent stops and reports the exact error. It does not retry in a loop, "
    "and it never asks for a password.",
    "HPC.md · Section 10, from the file",
    [fl("HPC", "**If a command prompts, hangs", 118), fl("HPC", "**Getting in (human-only steps first).**", 118)],
    [None, "The researcher creates and unlocks the key"],
    [{"at": 0.1, "event": "stop and report the exact error"}, {"at": 0.55, "event": "human-only steps"}],
    ring_lines=[0], ring_phrases=["stops and reports the exact error"], fs=28, margin=50)
add(manim("B32", A2,
    "Section twelve is a list of things the training slides get wrong. A comment after a line continuation, which breaks the "
    "command. A partition called compute, which does not exist. A sample script with no time and no memory. The agent is told "
    "not to copy them.",
    "B32_DoNotCopy",
    "Three slide cards, each stamped with a terracotta 'do not copy' tag: 'python train.py \\  # CHANGE' (the line cut at the backslash), '--partition=compute' (a partition rack that is not there, dotted), 'sbatch with no --time or --mem' (empty slots); a Claude logo chip nods past them without taking any.",
    [{"at": 0.2, "event": "backslash comment card"}, {"at": 0.45, "event": "partition=compute card (nothing there)"}, {"at": 0.7, "event": "no time or memory card"}, {"at": 0.9, "event": "none copied"}]))
add(manim("B33", A2,
    "And the appendix is the honest part. Where the sources disagree, the file says so and picks the safe reading. The scratch "
    "quota: fifty terabytes in the slides, twenty on the policy page. So the agent is told never to quote a number. Rules marked "
    "house rule or inferred are our judgment, not policy.",
    "B33_HonestAppendix",
    "Two source pages side by side, one with '50 TB' and one with '20 TB' on the same line 'scratch quota'; a not-equal sign; a third card 'the file: never quote a number'; then two small stamps 'house rule' and 'inferred' land beside a rule line.",
    [{"at": 0.2, "event": "50 TB on one page"}, {"at": 0.4, "event": "20 TB on the other"}, {"at": 0.65, "event": "the file picks the safe reading"}, {"at": 0.88, "event": "house rule and inferred stamps"}]))

# ═════════════════════════════ ACT III · What AICR.md Changes ═════════════════════════════
add(manim("B40", A3,
    "Now AICR dot M D. It builds on the first file, and where the two differ, it wins on AICR. Explorer's hosts, partitions, "
    "storage rules and module setup do not carry over. The first rule of the second file: assume AICR is not Explorer.",
    "B40_AssumeNotExplorer",
    "The two stacked pages from before, now with the AICR.md page on top lit; four small Explorer items (a host chip, a partition chip, a storage chip, a module chip) try to slide from the HPC.md page onto the AICR rack and bounce off one by one; a short line 'AICR is not Explorer' lands.",
    [{"at": 0.2, "event": "AICR.md on top: it wins"}, {"at": 0.5, "event": "Explorer's host, partition, storage, module bounce off"}, {"at": 0.88, "event": "assume AICR is not Explorer"}]))
add(manim("B41", A3,
    "AICR differs in ways that bite. Your user name is built differently. There is no password, only a key and a certificate. "
    "The partition decides which GPU you get. Idle GPUs are cancelled automatically. And scratch is purged after thirty days, "
    "with no off-site backup.",
    "B41_AICRDiffers",
    "A drawn two-column table builds row by row: 'user name' -> 'dot becomes underscore, _neu added'; 'login' -> 'key + certificate, no password'; 'GPU' -> 'the partition picks it'; 'idle GPU' -> 'cancelled automatically'; 'scratch' -> 'purged after 30 days, no off-site backup'.",
    [{"at": 0.15, "event": "user name row"}, {"at": 0.35, "event": "no password row"}, {"at": 0.55, "event": "partition picks the GPU row"}, {"at": 0.72, "event": "idle GPU row"}, {"at": 0.9, "event": "scratch row"}], sparse=True))
shell("B42", A3,
    "AICR's own nevers are specific. Never run S S H add dash capital D, because it empties every key. Never source activate in "
    "a batch script, because a real job died on it. And never copy the workshop's GPU check, because it exits zero even when "
    "the GPU is missing.",
    "AICR.md · three of its hard nevers, from the file",
    [fl("AICR", "| Run `ssh-add -D`", 132, focus="It empties"), fl("AICR", "| `source activate` or `conda activate`", 132, focus="One real job died"),
     fl("AICR", "| Copy `01_gpu_verify.py`", 132, focus="exits with status 0")],
    [None, "Never source activate", "never copy the workshop"],
    [{"at": 0.05, "event": "ssh-add -D"}, {"at": 0.45, "event": "source activate"}, {"at": 0.8, "event": "01_gpu_verify.py"}],
    ring_lines=[0, 1, 2], ring_phrases=["empties every key", "a real job died on it", "exits zero"], fs=28, margin=50)
shell("B43", A3,
    "Section five is a template built from flags that real completed jobs used. Every setting is stated. The environment is "
    "added to the path, not activated. And the script fails itself, on purpose, if the GPU is not visible.",
    "AICR.md · the template, three lines of it",
    [fl("AICR", "#SBATCH --partition=rtx-batch", 100), fl("AICR", "export PATH=$HOME/.conda/envs", 100),
     fl("AICR", 'python -c "import torch,sys; sys.exit', 100)],
    [None, "added to the path", "fails itself, on purpose"],
    [{"at": 0.1, "event": "every setting stated"}, {"at": 0.5, "event": "PATH prepend, not activate"}, {"at": 0.85, "event": "the hard-fail CUDA check"}],
    ring_lines=[1, 2], ring_phrases=["added to the path", "fails itself, on purpose"], fs=30, margin=50)
add(manim("B44", A3,
    "After every batch job the agent runs jobstats, a command that exists only on AICR. Its real example: a job that asked for "
    "eight hours and ran fifty-five minutes, with the GPU eighty percent busy. The targets are written down: over seventy "
    "percent GPU use is acceptable, and under fifty is a problem.",
    "B44_JobstatsTargets",
    "Four horizontal bars drawn like jobstats: CPU utilisation 13%, CPU memory 25%, GPU utilisation 80% (the one filled terracotta), GPU memory 17%; a time bar '8 h asked, 55 min ran'; two tick marks on the GPU bar at 50 and 70 labelled 'problem' and 'acceptable'.",
    [{"at": 0.2, "event": "the time bar: 8 h asked, 55 min ran"}, {"at": 0.5, "event": "GPU utilisation 80%"}, {"at": 0.85, "event": "the 70 and 50 marks"}], sparse=False))
add(manim("B45", A3,
    "Section eleven is lessons from real AICR runs, and they are all quiet failures. A checkpoint that loaded without error and "
    "left random weights. An input clip so quiet it produced silence. A cached file served under the same path after it was "
    "replaced. Each became a rule: prove the weights loaded, gate every input with a number, give a replaced file a new name.",
    "B45_QuietLessons",
    "Three cards each with a small drawing and a rule chip: a model box with a 'loaded, no error' tick but random dots inside -> 'prove the weights loaded'; a flat audio line with peak '4 of 32767' -> 'gate every input with a number'; two files with the same path, the old one served from a cache shelf -> 'give it a new name'.",
    [{"at": 0.2, "event": "weights loaded with no error"}, {"at": 0.45, "event": "the silent clip"}, {"at": 0.7, "event": "the cached file"}, {"at": 0.9, "event": "three rules"}]))
shell("B46", A3,
    "And before any GPU job, the agent asks only what only you can answer. Your user name and account. Whether any data is "
    "restricted. Whether it may submit for you. And what success looks like.",
    "AICR.md · Section 12, the questions, from the file",
    [fl("AICR", "**Must ask (only the researcher can answer):**", 100), fl("AICR", "1. What is your **AICR username**", 112),
     fl("AICR", "2. **Is any of the data non-anonymised", 112), fl("AICR", "4. What counts as success", 112)],
    [None, "Your user name and account", "restricted", "what success looks like"],
    [{"at": 0.05, "event": "must ask"}, {"at": 0.35, "event": "username and account"}, {"at": 0.6, "event": "restricted data"}, {"at": 0.85, "event": "what success looks like"}],
    ring_lines=[2], ring_phrases=["restricted"], fs=28, margin=50)

# ═════════════════════════════ ACT IV · Rules Born From Real Mistakes ═════════════════════════════
shell("B50", A4,
    "Rules also come from mistakes. While making the film about rendering on Explorer, the agent listed every folder under "
    "projects. That showed other people's names. Then it ran a disk usage command over a shared folder, and it hung. Neither was "
    "forbidden by the file. Now both are.",
    "Rules Born From Real Mistakes, the real record, then the rule",
    ["(Redacted: a first command also listed every directory under /projects.",
     "That showed other people's names, so it is not kept.)",
     "Command did not complete within its 120s timeout and was moved to the background",
     "NEW RULE in HPC.md, Section 1:",
     fl("HPC", "| List `/projects`", 96)],
    [None, "That showed other people's names", "it hung", "Now both are", "Now both are"],
    [{"at": 0.05, "event": "the listing, redacted"}, {"at": 0.45, "event": "the hung disk count"}, {"at": 0.85, "event": "the new rule, copied from HPC.md"}],
    ring_lines=[2, 4], ring_phrases=["it hung", "Now both are"], fs=28, margin=100)
shell("B51", A4,
    "Another. A job script began with module purge. That removed the module that sets the cluster's proxy, so every download "
    "timed out. A one line test showed the network was fine. Now the file says: module purge can remove your network, so load "
    "that module again.",
    "The real test, then the rule that came from it",
    ["before purge: [<the cluster proxy>]", "after purge: []", "after load: []",
     "NEW RULE in HPC.md, Section 8:",
     fl("HPC", "- **`module purge` can also remove your network.**", 110)],
    [None, "removed the module", "removed the module", "Now the file says", "Now the file says"],
    [{"at": 0.05, "event": "proxy set before the purge"}, {"at": 0.4, "event": "gone after the purge, and after loading tools"}, {"at": 0.85, "event": "the new rule"}],
    ring_lines=[1, 4], ring_phrases=["removed the module", "module purge can remove your network"], fs=28, margin=50)
shell("B52", A4,
    "And a third. The scripts assumed scratch belonged to the user. On this account it belonged to root, and refused every "
    "write. The agent had checked with a read first, which is exactly what the file asks. Now the file says why: test before "
    "you write.",
    "The real check, then the rule that came from it",
    ["root:root 755 2023-01-27 16:20:13.110253069 -0500",
     "mkdir: cannot create directory ‘/scratch/<username>/.probe’: Permission denied",
     "NEW RULE in HPC.md, Section 7:",
     fl("HPC", "- **Test before you write to scratch.**", 110)],
    [None, "refused every write", "Now the file says why", "test before you write"],
    [{"at": 0.05, "event": "scratch belongs to root"}, {"at": 0.45, "event": "mkdir refused"}, {"at": 0.85, "event": "the new rule"}],
    ring_lines=[0, 3], ring_phrases=["belonged to root", "test before you write"], fs=28, margin=50)

# ═════════════════════════════ ACT V · Using The Files ═════════════════════════════
add(manim("B59", A5,
    "Where to find them. Both files are free on GitHub, in the hpc dash aicr repository, inside the skills folder. "
    "H P C dot M D is in the hpc folder, and AICR dot M D is in the aicr folder. The link is in the description.",
    "B59_WhereToFindThem",
    "The repository address github.com/nikbearbrown/hpc-aicr appears in mono; below it a skills folder splits into two folders, hpc and aicr, each holding one document page labelled HPC.md and AICR.md.",
    [{"at": 0.2, "event": "the repository address"}, {"at": 0.55, "event": "skills opens into hpc and aicr"}, {"at": 0.85, "event": "the two files, one in each"}]))
add(manim("B60", A5,
    "To use them: put both files where your agent can read them. Add the one line to your Claude dot M D or agents dot M D. And "
    "at the start of cluster work, ask the agent to say back which rules apply, before it runs anything.",
    "B60_ThreeSteps",
    "Three steps land left to right on a line: a folder with two document pages ('put the files where the agent can read them'), a small instructions page with one highlighted line ('add the one line'), and a speech bubble from a Claude logo chip ('say back the rules that apply') that appears before any command box moves.",
    [{"at": 0.2, "event": "two files in a folder"}, {"at": 0.5, "event": "one line in the instructions"}, {"at": 0.85, "event": "the agent says the rules back first"}]))
add(manim("B61", A5,
    "The files do not replace judgment. Nothing in any policy page says whether automated agents are allowed on Explorer or "
    "AICR, so the files say to ask Research Computing once. And every claim is labelled by how we know it: from the sources, "
    "from a real run, or our own judgment.",
    "B61_WhatRulesCannotDo",
    "A small gate drawn with a Professor Bear portrait (1x1) standing beside it holding the key; a Claude logo chip waits at the gate; a note 'ask Research Computing once' lands on the gate; below, three label stamps in a row: 'from the sources', 'from a real run', 'our own judgment'.",
    [{"at": 0.2, "event": "you at the gate, the agent waits"}, {"at": 0.5, "event": "ask Research Computing once"}, {"at": 0.85, "event": "three label stamps"}]))

# ───────────────────────────── the closing three ─────────────────────────────
RECAP = ["An agent is fast and literal, so a shared cluster needs written rules.",
         "HPC.md holds the general rules: never compute on a login node, ask before you spend, verify the GPU.",
         "AICR.md adds what is stricter: no idle GPUs, no source activate, scratch is purged.",
         "Every rule comes with a because.",
         "Real mistakes become new rules.",
         "One line in your instructions points the agent at both files."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. An agent is fast and literal, so a shared cluster needs written rules. H P C dot M D holds the "
    "general rules: never compute on a login node, ask before you spend, verify the GPU. AICR dot M D adds what is stricter: no "
    "idle GPUs, no source activate, and scratch is purged. Every rule comes with a because. Real mistakes become new rules. And "
    "one line in your instructions points the agent at both files.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land in narration order"}],
    lane="bookend", lead_silence_s=0.5,
    qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("Read the files HPC.md and AICR.md completely. Do not run anything on any cluster. "
             "Then tell me the five hard nevers that matter most for my task, which questions you would ask me before your first "
             "command, and anything in the files that you could not confirm. My task: <describe your job in one sentence>.")
YT_SPOKEN = ("Read the files H P C dot M D and AICR dot M D completely. Do not run anything on any cluster. "
             "Then tell me the five hard nevers that matter most for my task, which questions you would ask me before your first "
             "command, and anything in the files that you could not confirm. My task, then describe your job in one sentence.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_SPOKEN + " Then check two things yourself. Did Claude run nothing on a cluster? "
    "And did it say what it could not confirm?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Read The Rules First", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did Claude run nothing on a cluster? It should only read the two files.",
                "Check: did it say what it could not confirm? A good answer names the unverified parts."],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": "Guiding Your Agent, H P C dot M D and AICR dot M D. At Nik Bear Brown.", "estimated_duration_s": 5.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Guiding Your Agent, H P C dot M D and AICR dot M D. Why an agent on a "
                           "shared cluster needs written rules, and a walk through the two rule files that give them.",
         "estimated_duration_s": 14.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · AGENT RULES", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German (Hallo)",
    "audience": "A researcher who wants Claude Code (or another agent) to work on a shared research cluster and needs to know what rules to give it; assumes no other film or book",
    "source_doc": "hpc-aicr/skills/hpc/HPC.md and hpc-aicr/skills/aicr/AICR.md (the two files), STORY.md, and the real Explorer session record in the film 'Making a Lecture Film on Explorer' SESSION.md",
    "playlist": "Northeastern HPC and AICR", "chapter_number": 9,
    "series_title": "Research Computing on Explorer and AICR",
    "lecture_opening_description": "Rule files that keep an agent safe on a shared cluster",
    "lecture_opening_title_lines": ["Guiding Your Agent:", "HPC.md and AICR.md"],
    "tags": ["HPC.md", "AICR.md", "Claude Code", "AI agents", "CLAUDE.md", "AGENTS.md", "Slurm", "Explorer", "AICR", "Northeastern University",
             "Research Computing", "HPC", "Nik Bear Brown"]},
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

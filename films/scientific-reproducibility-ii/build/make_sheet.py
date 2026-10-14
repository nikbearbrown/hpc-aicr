#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-scientific-reproducibility-ii-version-control.

LECTURE (brutalist.art/skills/make/lecture/SKILL.md): the WHOLE source as one act-structured film, primarily visual.
Source:   _research/source.md (Northeastern Research Computing's notebook "Scientific Reproducibility II", copied from
          hpc-aicr/Scientific-Reproducibility-II-2026/) and _research/our-guide.md (our written rewrite and its corrections).
Honesty:  every command on a terminal beat is READ FROM THE SOURCE at build time (sl()/C()); a missing line stops the build.
          Output lines come only from captures/ (a real run of the source's own commands on a Mac, in a throwaway folder,
          by rl()); a command that was not run is shown without output and labelled. Nothing was run on Explorer or AICR.
Spine:    BOPEN -> BIDEA -> BDEFS -> eight acts -> BVDT -> BHTF -> BOUT. Two passes (pass 2 reads _qc/asr.json).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Scientific Reproducibility II: Version Control"
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


def est(n):
    return round(len(n.split()) / 2.5, 1)


def beat_dur(bid):
    p = HERE / "beat_sheet.json"
    if p.exists():
        for ob in json.load(open(p))["beats"]:
            if ob["beat_id"] == bid:
                return ob.get("actual_duration_s")
    return None


SPARSE = ("lecture, drawn lane (show-tell drawing laws): one drawn scene on a cream stage with a few labels, "
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


# ───────────────────────────── source lines (verbatim) ─────────────────────────────
SRC = (HERE / "_research/source.md").read_text()
_SL = SRC.splitlines()


def _cut(ln, maxlen):
    if len(ln) <= maxlen:
        return ln
    return ln[:maxlen].rsplit(" ", 1)[0] + " …"


def sl(start, maxlen=94, exact=False, nth=0):
    """The nth source line whose text (leading spaces ignored) starts with `start` (or equals it when exact), verbatim."""
    k = 0
    for ln in _SL:
        s = ln.strip()
        if (s == start) if exact else s.startswith(start):
            if k == nth:
                return _cut(ln.rstrip(), maxlen)
            k += 1
    raise SystemExit(f"sl: no source line starting with {start!r} (nth={nth})")


def C(start, maxlen=92, exact=False, nth=0):
    """A source line shown as a typed command: '$ ' + the verbatim line (indent dropped)."""
    k = 0
    for ln in _SL:
        s = ln.strip()
        if (s == start) if exact else s.startswith(start):
            if k == nth:
                return "$ " + _cut(s, maxlen)
            k += 1
    raise SystemExit(f"C: no source line starting with {start!r}")


# ───────────────────────────── recorded lines (verbatim, from captures/) ─────────────────────────────
_REC = {}


def rl(name, start, nth=0, maxlen=100):
    """The nth line of captures/<name> that starts with `start`. Tabs become four spaces; the scratch path is shortened."""
    if name not in _REC:
        _REC[name] = (HERE / "captures" / name).read_text().splitlines()
    k = 0
    for ln in _REC[name]:
        if ln.startswith(start):
            if k == nth:
                ln = ln.replace("\t", "    ")
                ln = re.sub(r"in /\S*/rnaseq_project", "in …/rnaseq_project", ln)
                return _cut(ln.rstrip(), maxlen)
            k += 1
    raise SystemExit(f"rl: no line starting with {start!r} in captures/{name} (nth={nth})")


REC_TITLE = "recorded on a Mac"


def cue_list(bid, narration, items):
    """items: [(line, phrase|None)]. A phrase places the line on that spoken word; None follows the previous line closely."""
    d = est(narration)
    cues, last = [], 0
    for i, (ln, ph) in enumerate(items):
        if ph is None:
            c = (last + 8) if i else 20
        else:
            t = word_t(bid, ph)
            if t is None:
                alt = ph.split("|")[0]
                k = narration.find(alt)
                t = (d * k / max(1, len(narration))) if k >= 0 else 0.5
                if ASR.get(bid):
                    print(f"  [cue-fallback] {bid}: '{ph}' not in the recognised words")
            c = max(1, fr(t - 0.15))
        c = max(c, last + 1) if i else max(c, 1)
        cues.append(c)
        last = c
    dur = beat_dur(bid)
    if dur:
        mid = dur / 2 * FPS
        out, last = [], 0
        for c in cues:
            if mid - 21 < c < mid + 7:
                c = int(mid + 9)
            c = max(c, last)
            out.append(c)
            last = c
        cues = out
    return cues


B = []


def add(b):
    B.append(b)
    return b


def shell(bid, act, narration, title, items, rings=None, fs=27, margin=100,
          motion_claim="The text, exactly as written or as recorded, prints line by line as it is spoken."):
    """rings: [(item index, phrase)]. Lines are capped at 14 (the component's limit)."""
    items = [(x, None) if isinstance(x, str) else x for x in items]
    assert len(items) <= 14, (bid, len(items))
    cues = cue_list(bid, narration, items)
    props = {"title": title, "lines": [x[0] for x in items], "startCue": 20, "lineGap": 30, "lineCues": cues,
             "fontSize": fs, "windowMargin": margin}
    if rings:
        rs = []
        for idx, ph in rings:
            c = cues[idx]
            t = word_t(bid, ph)
            if t is not None:
                c = max(c, fr(t - 0.15))
            c += 12
            dur = beat_dur(bid)
            if dur:
                mid = dur / 2 * FPS
                if mid - 21 < c < mid + 7:
                    c = int(mid + 9)
            rs.append({"line": idx, "cue": c})
        props["rings"] = rs
    return add(remotion(bid, act, narration, "CCPlainShell", props, [{"at": 0.1, "event": "lines print as they are spoken"}],
                        motion_claim=motion_claim))


A1, A2, A3, A4, A5, A6, A7, A8 = (
    "I · Why Keep History", "II · Start A Repository", "III · What To Leave Out", "IV · Save And Inspect",
    "V · Branches And Merges", "VI · Tags And Time Travel", "VII · Git On Slurm", "VIII · Daily Habits And Questions")

# ───────────────────────────── the opening pair ─────────────────────────────
OPEN = [
 remotion("BIDEA", "the idea",
    "Hallo. This is Liam, in for Bear. First, a correction. Version control is not a backup folder. It is a timeline of "
    "snapshots you can search, compare and rewind, and each snapshot can be tied to the result it produced.",
    "BrutalistHesitantWriter",
    {"text": "Version control is\njust a backup folder", "triggerWords": "just a backup folder",
     "replacementWords": "a searchable timeline", "fontSize": 66, "charMs": 62, "hesitateBetween": 6,
     "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'Version control is just a backup folder'"},
     {"at": 0.35, "event": "backspaces 'just a backup folder' -> 'a searchable timeline'"}],
    lane="bookend", lead_silence_s=0.8,
    motion_claim="The writer types the newcomer's framing (just a backup folder) and corrects it to the real one (a searchable timeline).",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. Repository: the project folder plus its history. Commit: a saved snapshot of your files. Branch: a movable "
    "name for one line of commits. Tag: a fixed name for one commit. The git ignore file: a list of what Git skips. And a "
    "Slurm job: your request for a compute node.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "Repository", "meaning": "the project folder plus its history"},
               {"term": "Commit", "meaning": "a saved snapshot of your files"},
               {"term": "Branch", "meaning": "a movable name for a line of commits"},
               {"term": "Tag", "meaning": "a fixed name for one commit"},
               {"term": ".gitignore", "meaning": "a list of what Git skips"},
               {"term": "Slurm job", "meaning": "your request for a compute node"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "'Repository' lands"}, {"at": 0.25, "event": "'Commit'"}, {"at": 0.42, "event": "'Branch'"},
     {"at": 0.58, "event": "'Tag'"}, {"at": 0.74, "event": "'.gitignore'"}, {"at": 0.9, "event": "'Slurm job'"}],
    gate="CARD", lane="bookend",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

# ═════════════════════════════ ACT I · Why Keep History ═════════════════════════════
add(manim("B10", A1,
    "Six months after you submit a paper, a reviewer asks: what threshold did you use for low-count filtering? Without version "
    "control you open a folder like this, and you guess from the file names. Which script made which table?",
    "B10_ReviewerAsks",
    "Left, a Professor Bear portrait (1x1) with a speech chip 'threshold?'; right, eight file and folder chips from the source "
    "(filter.sh, filter_v2.sh, filter_final.sh, filter_final_USE_THIS.sh, results_old/, results_new/, results_for_paper/, "
    "results_for_paper_FINAL/) stack in one after another; a terracotta question mark pulses over the pile.",
    [{"at": 0.1, "event": "the reviewer's question"}, {"at": 0.4, "event": "the pile of file names builds"}, {"at": 0.85, "event": "which made which?"}]))
add(manim("B11", A1,
    "Version control replaces that folder with one script and a timeline. Every change carries a date, an author and a message. "
    "You can mark the exact code behind a figure, give each experiment its own branch, and undo a bad change.",
    "B11_OneTimeline",
    "The file-name pile shrinks to one script chip 'filter.sh'; a vertical timeline of dots grows under it, each dot with three "
    "tiny chips (date, author, message); a flag 'figure 3' plants on one dot, a side line splits off labelled 'experiment', "
    "and one dot is undone with a returning arrow.",
    [{"at": 0.15, "event": "one script and a timeline"}, {"at": 0.4, "event": "date, author, message on each change"}, {"at": 0.8, "event": "flag, branch, undo"}]))
add(manim("B12", A1,
    "The program is called Git, and its idea is simple. It stores snapshots, not edits. A commit is a full picture of your files "
    "at one moment, linked to the commit before it.",
    "B12_Snapshots",
    "A Git logo chip at the top; a chain of three commit discs with hashes a3f8c21, b7d2e14, d9c1f37 (mono), each disc holding a "
    "mini folder picture; arrows point back from each to its parent; a label 'whole picture' lands on one disc.",
    [{"at": 0.2, "event": "the Git logo; snapshots not edits"}, {"at": 0.55, "event": "three commits, each a full picture"}, {"at": 0.85, "event": "each points to the one before"}]))
add(manim("B13", A1,
    "A branch is a movable name for one chain of commits: main here, and an experiment that split off. A tag is a fixed name for "
    "one commit, like a flag you plant on the code behind a paper.",
    "B13_BranchAndTag",
    "The same three-commit chain; a label 'main' sits on the last disc; a fourth disc e5a0b99 forks off the middle one under a "
    "label 'explore/idea'; a flag 'v1.0' plants on one disc.",
    [{"at": 0.2, "event": "main on the chain"}, {"at": 0.5, "event": "the experiment forks off"}, {"at": 0.85, "event": "a flag on one commit"}]))
add(manim("B14", A1,
    "Your files live in three places. The working tree is what you see and edit. The staging area is the list of changes going "
    "into the next snapshot, and git add puts a change there. The repository holds the saved snapshots, and git commit saves them.",
    "B14_ThreePlaces",
    "Three boxes left to right: 'working tree' (a file page), 'staging area' (a tray), 'repository' (a stack of snapshot discs); "
    "a file page travels to the tray on the label 'git add' and the tray's page drops into the stack on 'git commit'.",
    [{"at": 0.15, "event": "working tree: what you edit"}, {"at": 0.45, "event": "git add moves the change to staging"}, {"at": 0.8, "event": "git commit saves the snapshot"}]))
add(manim("B15", A1,
    "Four moments where this saves you. A reviewer asks if you tried another value: open the branch where you did. A postdoc "
    "leaves: clone the repository and read the README. A cluster setting changed: diff against the last commit. Publishing the "
    "code with the paper: tag a release on GitHub.",
    "B15_FourMoments",
    "Four rows. Each row: a short situation chip on the left ('another value?', 'postdoc leaves', 'setting changed', 'with the "
    "paper'), an arrow, and on the right the answer in mono ('a branch', 'clone + README', 'git diff HEAD~1', 'a tag') with a "
    "GitHub logo chip on the last row. Rows land on the spoken situations.",
    [{"at": 0.15, "event": "row 1"}, {"at": 0.4, "event": "row 2"}, {"at": 0.6, "event": "row 3"}, {"at": 0.85, "event": "row 4"}], sparse=False))

# ═════════════════════════════ ACT II · Start A Repository ═════════════════════════════
add(manim("B20", A2,
    "The example is a small R N A sequencing project: a table of read counts, one row per gene, three control columns and three "
    "treated. One script drops low-count genes, works out a fold change, and writes a summary. Any analysis follows the same Git workflow.",
    "B20_TheExample",
    "A drawn table (gene_id column; three 'control' columns; three 'treated' columns; ghost cells) on the left flows through a "
    "funnel labelled 'MIN_COUNT' into a smaller table on the right with a status column and three chips UP, DOWN, NS.",
    [{"at": 0.15, "event": "the counts table: genes, control, treated"}, {"at": 0.5, "event": "low-count genes drop out in the funnel"}, {"at": 0.85, "event": "the summary table with UP, DOWN, NS"}]))
shell("B21", A2,
    "This is the script we will track. Strict mode, an input, an output, and a parameters block at the top, where the one tunable "
    "value lives: min count, ten. Genes with a low mean count are skipped. The rest are called up, down, or not significant by fold change.",
    "scripts/filter_and_summarise.sh  ·  from the source",
    [(sl("set -euo pipefail"), "Strict mode"), (sl("INPUT="), "input"), (sl("OUTPUT="), "output"),
     (sl("# ── PARAMETERS"), "parameters block"), (sl("MIN_COUNT=10"), "min count"),
     (sl("if (overall < threshold) next"), "low mean count"), (sl("if      (fc >= 2.0)"), "up, down"),
     sl("else if (fc <= 0.5)"), sl("else                status")],
    rings=[(4, "min count")])
shell("B22", A2,
    "Start tracking before the first run, not after. Git init makes a hidden dot git folder: Git's database, one per project. A "
    "caution: depending on your settings, the first branch may be called master, as it was here, and the later steps say main. "
    "So rename it first.",
    "Start tracking  ·  " + REC_TITLE + ", path shortened",
    [(C("git init", exact=True), "in it|init|get in it"), rl("session/cell12.out", "Initialized empty Git repository"),
     (rl("session/cell12.out", "hint: Using 'master'"), "may be called master"), rl("session/cell12.out", "hint: is subject"),
     "# not in the source: the later steps switch to main, so rename first",
     ("$ git branch -M main", "rename it")],
    rings=[(2, "may be called master")])

# ═════════════════════════════ ACT III · What To Leave Out ═════════════════════════════
add(manim("B30", A3,
    "Track the code that makes results, not the results themselves. Big raw data lives in project storage, outside the "
    "repository, and passwords or tokens never go in at all. Whatever Git should skip goes in a file named dot git ignore.",
    "B30_CodeNotResults",
    "Left, a script page 'scripts/' with a check going into a repository box; centre, a big data block 'data' that an arrow "
    "sends to a 'project storage' rack instead; a key chip 'tokens' crossed out; at the right a page named '.gitignore' (mono) "
    "that lands last with a stack of skipped items under it.",
    [{"at": 0.15, "event": "code goes into the repository"}, {"at": 0.45, "event": "big data goes to storage; tokens never"}, {"at": 0.85, "event": "the .gitignore page lists what to skip"}]))
shell("B31", A3,
    "Here is the source's version of that file. It ignores the whole results folder, then lists two files to let back in: the "
    "summary table and the run log.",
    ".gitignore  ·  from the source",
    [(sl("# ── Results and outputs"), None), (sl("results/", exact=True), "whole results folder"), "",
     sl("# ── Raw data"), sl("data/*.fastq", exact=True), sl("*.log", exact=True), "",
     (sl("# ── Allow small reference files through"), "lists two files"), (sl("!results/summary.tsv"), "summary table"),
     (sl("!results/run.log"), "run log")],
    rings=[(1, "whole results folder"), (8, "summary table"), (9, "run log")])
shell("B32", A3,
    "Run that in real Git and it fails. Git never looks inside an ignored folder, so it never reads the two allow lines. The add "
    "is refused, and check-ignore names line two of the file as the reason.",
    "git refuses  ·  " + REC_TITLE,
    [(rl("trap.out", "$ git add"), "Run that"), rl("trap.out", "The following paths"), rl("trap.out", "results"),
     (rl("trap.out", "hint: Use -f"), "refused"), (rl("trap.out", "$ git check-ignore"), "names line|check"),
     (rl("trap.out", ".gitignore:2:"), "line 2|line to|file as")],
    rings=[(5, "line 2|line to|file as")])
shell("B33", A3,
    "The fix is one character. Ignore the folder's contents, with slash star, not the folder. Now the folder itself is not "
    "ignored, so the two allow lines work, and both files stage.",
    "the fix  ·  " + REC_TITLE,
    ["# in .gitignore, ours: ignore the contents, not the folder", ("results/*", "slash star"), "!results/summary.tsv",
     "!results/run.log", (rl("fixed.out", "$ git add"), "both files stage"), rl("fixed.out", "$ git status"),
     rl("fixed.out", "A  results/run.log"), rl("fixed.out", "A  results/summary.tsv")],
    rings=[(1, "slash star")])
shell("B34", A3,
    "A second trap, in the same file. The source puts a comment after the pattern, on the same line. Git does not read that as a "
    "comment: the text becomes part of the pattern, which then matches nothing. So the add is still refused. Give every comment a line of its own.",
    "second trap  ·  " + REC_TITLE,
    ["# the source writes a comment after the pattern:", sl("!results/summary.tsv"),
     ("# with results/* above it, we ran:", None), (rl("trailing.out", "$ git add"), "still refused"),
     rl("trailing.out", "The following paths"), rl("trailing.out", "results/run.log"), rl("trailing.out", "results/summary.tsv"),
     rl("trailing.out", "hint: Use -f"), "# comments need a line of their own"],
    rings=[(8, "line of its own")])
shell("B35", A3,
    "Write the README before the first commit. List the requirements, the exact commands to reproduce the result, including the "
    "tag to check out, and the parameters. It is a contract with anyone who clones the repository, and that includes you in a year.",
    "README.md  ·  from the source",
    [(sl("## Reproduce the paper results"), "exact commands"), sl("git clone https://github.com/you/rnaseq_project"),
     sl("cd rnaseq_project", exact=True), (sl("git checkout v1.0-submission"), "the tag|tag to"),
     sl("bash scripts/filter_and_summarise.sh", exact=True), sl("# Output: results/summary.tsv"), "",
     (sl("## Parameters"), "parameters"), sl("| Parameter | Default | Description |"),
     sl("| `MIN_COUNT` | 10 |")],
    rings=[(3, "the tag|tag to")])

# ═════════════════════════════ ACT IV · Save And Inspect ═════════════════════════════
add(manim("B40", A4,
    "The habit for every result: change a value, run the script, look at the output, then commit the code and the result "
    "together. Repeat. Before a paper goes out, tag the commit. That ties each result to the code and the parameters behind it.",
    "B40_RunInspectCommit",
    "A four-node loop (change, run, inspect, commit) drawn as a ring; a terracotta dot rides it twice; after the second lap a "
    "flag 'tag' plants on the commit node; the commit node holds two stacked chips 'code' and 'result'.",
    [{"at": 0.15, "event": "change, run, inspect"}, {"at": 0.45, "event": "commit code and result together"}, {"at": 0.85, "event": "tag before it goes out"}]))
shell("B41", A4,
    "Three commands you will use dozens of times a day. Status shows what changed. Add chooses what goes into the next snapshot: "
    "that is the staging area. Commit saves it. The source stages everything with a dot; in a folder holding data, tokens or logs, name the files instead.",
    "the first commit  ·  " + REC_TITLE,
    [C("git status", exact=True), rl("session/cell18.out", "On branch main"), rl("session/cell18.out", "No commits yet"),
     rl("session/cell18.out", "Untracked files:"), (C("git add .", exact=True), "Add chooses"),
     (C("git commit -m 'Initial pipeline"), "Commit saves it"), rl("session/cell18.out", "[main (root-commit)"),
     rl("session/cell18.out", " 4 files changed"), C("git log --oneline", exact=True, nth=0), rl("session/cell18.out", "48350fb Initial")],
    rings=[(4, "name the files")])
shell("B42", A4,
    "Now run it. The log names the commit, and the counts are there: two hundred genes, a hundred ninety-nine kept. But look at "
    "the date error and the empty brackets. Dash dash i s o is a G N U option, so it fails on a Mac. It should work on Linux, but we did not run this on a cluster. On a Mac, use date dash u with a format.",
    "run it  ·  " + REC_TITLE + ", trimmed",
    [C("bash scripts/filter_and_summarise.sh", exact=True), (rl("session/cell20.out", "date: illegal option"), "date error"),
     rl("session/cell20.out", "usage: date"), rl("session/cell20.out", "[] Starting"), rl("session/cell20.out", "  Threshold:"),
     (rl("session/cell20.out", "  Git commit:"), "names the commit"), rl("session/cell20.out", "── Results"),
     rl("session/cell20.out", "  Total genes:"), (rl("session/cell20.out", "  After filter:"), "199"),
     rl("session/cell20.out", "  Upregulated:"), rl("session/cell20.out", "  Downregulated:"), rl("session/cell20.out", "  Not significant:")],
    rings=[(1, "date error"), (3, "empty brackets")])
shell("B43", A4,
    "Then commit the results together with the code that made them, and let the message say what the run was. The log inside "
    "this commit names the commit before it, so the result carries its own receipt. That only works because the fixed git ignore file lets the two files through.",
    "commit the run  ·  " + REC_TITLE,
    [(C("git add results/summary.tsv results/run.log", exact=True), "commit the results"),
     (C("git commit -m 'analysis: baseline run"), "let the message"), rl("session/cell22.out", "[main eda7c83]"),
     rl("session/cell22.out", " 2 files changed"), rl("session/cell22.out", " create mode 100644 results/run.log"),
     rl("session/cell22.out", " create mode 100644 results/summary.tsv"), C("git log --oneline", exact=True, nth=1),
     (rl("session/cell22.out", "eda7c83 analysis"), "its own receipt"), rl("session/cell22.out", "48350fb Initial")],
    rings=[(7, "its own receipt")])
add(manim("B44", A4,
    "Two habits make a history worth reading. One logical change per commit: if the message needs the word and, make two commits. "
    "And a consistent message style, a type, a scope and a short summary, so git log reads like a change log and grep finds things.",
    "B44_GoodCommits",
    "Top: a message chip 'fixed stuff and added new feature and changed config' (two lines) crossed out, beside a message chip "
    "'Fix off-by-one in loop bounds' with a check. Bottom: six type chips (feat, fix, data, analysis, docs, config) in a row, "
    "then one full example in mono 'analysis(fig3): reproduce with corrected normalization'.",
    [{"at": 0.15, "event": "the 'and' message is crossed out; the single-change one is kept"}, {"at": 0.55, "event": "six message types"}, {"at": 0.85, "event": "a typed example"}], sparse=False))
shell("B45", A4,
    "Before you commit anything, look at what you are about to commit. Change the threshold, and git diff shows it line by line: "
    "one line out, one line in. The source edits with sed, and that form fails on a Mac, which wants an empty backup suffix after dash i. We used the Mac form.",
    "git diff  ·  " + REC_TITLE + ", trimmed",
    [C("sed -i 's/MIN_COUNT=10/MIN_COUNT=20/'"), (rl("sed.out", "sed: 1:"), "fails on a Mac"),
     "# the Mac form, which we used:", (rl("sed.out", "$ sed -i ''"), "empty backup suffix"),
     (C("git diff scripts/filter_and_summarise.sh", nth=0), "git diff shows it"), rl("session/cell25.out", "@@ -12,7"),
     rl("session/cell25.out", " # ── PARAMETERS"), (rl("session/cell25.out", "-MIN_COUNT=10"), "one line out"),
     (rl("session/cell25.out", "+MIN_COUNT=20"), "one line in")],
    rings=[(7, "one line out"), (8, "one line in")])
shell("B46", A4,
    "Rerun with the new value: a hundred ninety-seven genes now pass, two fewer. Commit the changed script and the new results "
    "together, with a message that names the change. Three commits now, each one a documented decision.",
    "the second commit  ·  " + REC_TITLE,
    [C("bash scripts/filter_and_summarise.sh", exact=True, nth=1), (rl("session/cell26.out", "  After filter:"), "197"),
     C("awk 'NR>1 {print $5}' results/summary.tsv | sort | uniq -c", exact=True), rl("session/cell26.out", " 168 NS"), rl("session/cell26.out", "  29 UP"),
     (C("git add scripts/filter_and_summarise.sh results/summary.tsv results/run.log"), "Commit the changed script"),
     C("git commit -m 'analysis: raise MIN_COUNT 10->20"), rl("session/cell26.out", "[main 3abfaa1]"), rl("session/cell26.out", " 3 files changed"),
     (C("git log --oneline", exact=True, nth=2), "Three commits"), rl("session/cell26.out", "3abfaa1 analysis"),
     rl("session/cell26.out", "eda7c83 analysis"), rl("session/cell26.out", "48350fb Initial")])
shell("B47", A4,
    "The log is your audit trail. Stat shows which files each commit touched. Grep finds every commit that mentions a word, so "
    "the reviewer's question now has an answer in two lines. Dash p shows every change to one file, and git blame says who wrote each line, and when.",
    "git log  ·  " + REC_TITLE + ", selected lines",
    [C("git log --stat", exact=True), rl("session/cell28.out", "commit 3abfaa1"), rl("session/cell28.out", "Author:"),
     rl("session/cell28.out", "    analysis: raise"), rl("session/cell28.out", " results/run.log   "),
     rl("session/cell28.out", " results/summary.tsv   "), rl("session/cell28.out", " scripts/filter_and_summarise.sh |"),
     (C("git log --oneline --grep='MIN_COUNT'", exact=True), "Grep finds"),
     rl("session/cell28.out", "3abfaa1 analysis", nth=1), rl("session/cell28.out", "eda7c83 analysis", nth=1),
     "# also in the source, not run: git log -p -- script.sh   and   git blame script.sh"],
    rings=[(9, "reviewer's question")])

# ═════════════════════════════ ACT V · Branches And Merges ═════════════════════════════
add(manim("B50", A5,
    "A reviewer asks you to try a fold change cutoff of one point five instead of two. You do not know yet whether it goes in the "
    "paper. So never edit the working script for a speculative change. Make a branch: a parallel version that leaves main untouched.",
    "B50_BranchOff",
    "A main chain of three discs; a branch label 'explore/fc-cutoff-1.5' forks from the last disc and gets one new disc while the "
    "main label stays put; a lock-tag 'main untouched' lands on main.",
    [{"at": 0.2, "event": "main as it stands"}, {"at": 0.5, "event": "the branch forks and gets its own commit"}, {"at": 0.85, "event": "main stays untouched"}]))
shell("B51", A5,
    "One command makes the branch and moves you onto it. Branch list shows where you are, with a star. Change the two cutoffs "
    "in the script, and git diff shows exactly that: the cutoff of two becomes one point five, and the lower one, point five, becomes point six seven.",
    "a branch for the experiment  ·  " + REC_TITLE + ", trimmed",
    [(C("git switch -c explore/fc-cutoff-1.5", exact=True), "One command"), rl("session/cell30.out", "Switched to a new branch"),
     (C("git branch --list", exact=True), "Branch list"), rl("session/cell30.out", "* explore"), rl("session/cell30.out", "  main"),
     (C("sed -i 's/fc >= 2.0/fc >= 1.5/'"), "Change the two cutoffs"), C("sed -i 's/fc <= 0.5/fc <= 0.67/'"),
     "# on a Mac: sed -i '' ..., as before", (C("git diff scripts/filter_and_summarise.sh", nth=1), "git diff shows"),
     rl("session/cell31.out", "-    if      (fc >= 2.0)"), rl("session/cell31.out", "-    else if (fc <= 0.5)"),
     rl("session/cell31.out", "+    if      (fc >= 1.5)"), rl("session/cell31.out", "+    else if (fc <= 0.67)")])
shell("B52", A5,
    "Run it, check it, commit it on the branch. Then switch back to main, and its script is exactly as you left it: the cutoff "
    "is still two. The experiment lives only on the branch.",
    "commit, then switch back  ·  " + REC_TITLE,
    [(C("git commit -m 'explore: relax FC cutoff"), "commit it on the branch"), rl("session/cell32.out", "[explore/fc-cutoff-1.5"),
     rl("session/cell32.out", " 2 files changed"), (C("git switch main", exact=True), "switch back to main"),
     rl("session/cell33.out", "Switched to branch 'main'"), C("grep 'fc >=' scripts/filter_and_summarise.sh", exact=True),
     (rl("session/cell33.out", '    if      (fc >= 2.0)'), "still 2|still to")],
    rings=[(6, "still 2|still to")])
shell("B53", A5,
    "Merge when the idea belongs. The dash dash no F F flag keeps a visible merge point, and the graph shows the line leaving "
    "and rejoining. Deleting the branch with dash lowercase d removes only the label, and only if its work is merged. The commits stay.",
    "merge, then clean up  ·  " + REC_TITLE + ", trimmed",
    [C("git merge explore/fc-cutoff-1.5 --no-ff"), sl("-m 'Merge explore/fc-cutoff-1.5"),
     (rl("session/cell35.out", "Merge made by"), "Merge when"), (C("git log --oneline --graph --all", exact=True, nth=0), "the graph"),
     rl("session/cell35.out", "*   0611b57"), rl("session/cell35.out", "|\\"), rl("session/cell35.out", "| * 6bb1d6d"),
     rl("session/cell35.out", "|/"), rl("session/cell35.out", "* 3abfaa1"), (C("git branch -d explore/fc-cutoff-1.5", exact=True), "Deleting the branch"),
     (rl("session/cell35.out", "Deleted branch"), "The commits stay")],
    rings=[(4, "rejoining")])

# ═════════════════════════════ ACT VI · Tags And Time Travel ═════════════════════════════
add(manim("B60", A6,
    "A tag is a flag on one commit, and it does not move. Branch names slide forward with every new commit; a tag stays where "
    "you planted it. Before the paper goes out, tag the commit behind your figures, and check that tag out any time to get exactly that code.",
    "B60_FixedFlag",
    "A commit chain; the label 'main' sits on the last disc and the flag 'v1.0-submission' on the merge disc; two new discs arrive "
    "and 'main' slides forward each time while the flag stays; finally an arrow 'git checkout v1.0-submission' (mono) points back at the flag.",
    [{"at": 0.2, "event": "the flag planted"}, {"at": 0.5, "event": "new commits: main slides, the flag stays"}, {"at": 0.85, "event": "check the tag out to get that code"}]))
shell("B61", A6,
    "The tag command, and the list that shows it with its message. Tags are not sent by a plain push. Pushing uploads your work to "
    "a server such as GitHub, which changes something outside your machine, so do it on purpose and with the repository owner's agreement. We did not push; this folder has no remote.",
    "tag the submission  ·  " + REC_TITLE + ", push not run",
    [(C("git tag -a v1.0-submission \\"), "tag command"),
     sl("-m 'Code submitted to journal"), (C("git tag -l -n1", exact=True), "the list"), rl("session/cell37.out", "v1.0-submission Code"),
     "# from the source, not run: this folder has no remote", (C("git push origin main", exact=True), "Pushing uploads"),
     (C("git push origin v1.0-submission"), "Tags are not sent")],
    rings=[(5, "Pushing uploads")])
shell("B62", A6,
    "The reviewer's question: what did you get with the original threshold? Find the commit by its message, restore only that "
    "one file from it, run it, and read the answer: a hundred ninety-nine genes kept at ten, against one ninety-seven at twenty. Then put today's version back.",
    "time travel  ·  " + REC_TITLE + ", trimmed",
    [("$ " + sl("HASH=$(git log --oneline --grep='MIN_COUNT=10'").strip(), "Find the commit"),
     (C("git checkout $HASH -- scripts/filter_and_summarise.sh", exact=True), "restore only that one file"),
     C("grep 'MIN_COUNT\\|fc >='"), rl("session/cell40.out", "MIN_COUNT=10"),
     (C("bash scripts/filter_and_summarise.sh", exact=True, nth=2), "run it"), rl("session/cell40.out", "  Threshold:"),
     (rl("session/cell40.out", "  After filter:"), "199"),
     (C("git checkout HEAD -- scripts/filter_and_summarise.sh", exact=True), "put today's version back")],
    rings=[(6, "199")])
shell("B63", A6,
    "One thing to notice. Restoring the script did not restore the results. The rerun overwrote the two tracked result files, "
    "and git status shows them modified. Commit them, or put them back, before you go on. The next section shows why.",
    "what is left  ·  " + REC_TITLE,
    ["$ git status --short", (rl("session/status-after-timetravel.out", " M results/run.log"), "modified"), rl("session/status-after-timetravel.out", " M results/summary.tsv"),
     "# the rerun overwrote the tracked results", "# commit them, or restore them, before the next step"],
    rings=[(1, "modified"), (2, "modified")])

# ═════════════════════════════ ACT VII · Git On Slurm ═════════════════════════════
add(manim("B70", A7,
    "On a cluster, a Slurm job runs later, on another machine, from the files as they are then. So two rules. Commit before you "
    "submit, so every job traces to one commit. And print that commit's hash in the job log, so the result always points back to the code.",
    "B70_CommitBeforeSubmit",
    "A timeline: a commit disc, then a submit marker 'sbatch', a queue bar 'waits', a job-start marker and an end marker with an "
    "output page; a thread from the commit disc runs along under the timeline to the output page's log line (mono hash chip), "
    "closing the loop.",
    [{"at": 0.2, "event": "commit, then submit; the job waits, then runs later"}, {"at": 0.55, "event": "rule one: the job traces to one commit"}, {"at": 0.85, "event": "rule two: the hash is in the log"}]))
shell("B71", A7,
    "This is the source's job script, read from the source and not run by us. Two things to fix before you copy it. The partition "
    "named compute does not exist on Explorer. And the mail line is a placeholder: use your own address, or none.",
    "VII · Git On Slurm  ·  slurm/run_pipeline.sh, from the source, not run",
    [sl("#!/bin/bash"), sl("#SBATCH --job-name=rnaseq_filter"), (sl("#SBATCH --partition=compute"), "partition named compute"),
     sl("#SBATCH --ntasks=1"), sl("#SBATCH --cpus-per-task=1"), sl("#SBATCH --mem=4G"), sl("#SBATCH --time=00:30:00"),
     sl("#SBATCH --output=results/slurm_%j.out"), sl("#SBATCH --error=results/slurm_%j.err"),
     sl("#SBATCH --mail-type=END,FAIL"), (sl("#SBATCH --mail-user=your@university.edu"), "mail line")],
    rings=[(2, "does not exist"), (10, "your own address")])
add(manim("B72", A7,
    "Use a name from a real list. Read-only commands on a login node showed, on Explorer, short, the default, with a two-day "
    "limit, and sharing, with one hour. On A-I-C-R, the C P U partition is cpu, with one day. Check sinfo before you copy a name.",
    "B72_RealPartitions",
    "Left an Explorer rack with plaques 'short (default) 2 days' and 'sharing 1 hour'; right an AICR rack with a plaque 'cpu "
    "(default) 1 day'; above, a plaque 'compute' crossed out; a mono chip 'sinfo' lands last.",
    [{"at": 0.2, "event": "Explorer: short and sharing"}, {"at": 0.55, "event": "AICR: cpu"}, {"at": 0.85, "event": "compute crossed out; check sinfo"}], sparse=False))
shell("B73", A7,
    "Inside the job: a header that prints the job, the commit and the branch. Then the guard. If the working tree has "
    "uncommitted changes, or staged ones, the job stops. Then the pipeline, and a tag named run, dash, the job number, on exactly that commit.",
    "inside the job  ·  from the source, not run",
    [sl('echo "Job ID:'), sl('echo "Git commit:'), sl('echo "Git branch:'), (sl("if ! git diff --quiet"), "the guard"),
     sl("echo 'ERROR: uncommitted changes detected.'"), sl("exit 1", exact=True), "fi",
     (sl("bash scripts/filter_and_summarise.sh", exact=True, nth=1), "the pipeline"), (sl("git tag run-$SLURM_JOB_ID"), "a tag named"),
     sl('-m "Slurm job')],
    rings=[(3, "the guard"), (8, "a tag named")])
shell("B74", A7,
    "We ran the guard block on its own, on the Mac, not as a Slurm job. With an edited file it prints the error and exits with "
    "code one. After the commit it passes; the only line we added is the echo that says so. That is the habit: no trace, no run.",
    "the guard, run on its own  ·  " + REC_TITLE,
    [rl("guard.out", "$ git status"), rl("guard.out", " M README.md"), (rl("guard.out", "$ bash guard.sh"), "prints the error"),
     rl("guard.out", "ERROR:"), rl("guard.out", "Commit your changes"), (rl("guard.out", "exit code: 1"), "code 1|code one"),
     (rl("guard.out", '$ git commit'), "After the commit"), rl("guard.out", "$ bash guard.sh", nth=1),
     (rl("guard.out", "guard passed"), "it passes"), rl("guard.out", "exit code: 0", ),
     "# 'guard passed' is our one added echo; the rest is the source's guard"],
    rings=[(5, "code 1|code one")])
add(manim("B75", A7,
    "Weak spots, from our reading of the logic, not tested. The guard runs when the job starts, not when you submit, and a job "
    "can queue for hours. Edit the script meanwhile, and the job may run newer code and log the newer hash.",
    "B75_QueueWindow",
    "A timeline: 'sbatch' at commit A (disc A); a long queue bar; during it an 'edit' marker creates disc B; the job starts at "
    "disc B and its log chip shows B's hash while the person thought A; a label 'not tested' (stamp) sits in the corner.",
    [{"at": 0.2, "event": "the guard runs at job start"}, {"at": 0.5, "event": "an edit during the queue creates a newer state"}, {"at": 0.85, "event": "the job logs the newer hash"}]))
shell("B76", A7,
    "A stronger version, ours and untested. Check the tree when you submit, and pass the hash into the job. Inside the job, "
    "compare the two hashes and stop if they differ. That closes the gap.",
    "a stronger check  ·  ours, not run",
    ["# ours, untested: check at submit time and pass the hash into the job",
     ('git diff --quiet && git diff --staged --quiet || { echo "commit first"; exit 1; }', "Check the tree"),
     ('sbatch --export=ALL,SUBMIT_COMMIT="$(git rev-parse HEAD)" slurm/job.sh', "pass the hash"),
     "# inside the job: compare $SUBMIT_COMMIT with $(git rev-parse HEAD)", ("# and stop if they differ", "stop if they differ")],
    rings=[(2, "pass the hash")])
add(manim("B77", A7,
    "Three more. The results a run writes are tracked files, so the next submit is blocked until you commit them. The tag "
    "changes the repository from inside the job, so tag only from a checkout you own. And a tag made in the job exists only there, until someone pushes it.",
    "B77_ThreeMoreSpots",
    "Three cards left to right. 1: a results page with a terracotta dirty dot and a barred 'sbatch' arrow. 2: two job boxes "
    "reaching into one checkout box at the same time ('shared checkout'), a cross. 3: a flag 'run-tag' inside a rack that has no "
    "arrow to a GitHub logo chip until a 'push' arrow draws.",
    [{"at": 0.15, "event": "card 1: dirty results block the submit"}, {"at": 0.5, "event": "card 2: two jobs, one checkout"}, {"at": 0.85, "event": "card 3: the tag stays in the checkout until pushed"}], sparse=False))
add(manim("B78", A7,
    "A full job record holds more than a commit: job, node and partition; start and end times; the exact command; every "
    "parameter and random seed; input paths with checksums; software versions; the hardware used; the output folder; and the exit status. The header prints the first few. You add the rest.",
    "B78_JobRecord",
    "A 4 by 3 grid of twelve record chips (job and node, times, commit and tag, command and script, parameters, random seeds, "
    "input checksums, software, container, hardware, output folder, exit status); the first three get a terracotta ring as 'the header' and the other nine fill in as 'you add'.",
    [{"at": 0.15, "event": "the twelve items"}, {"at": 0.55, "event": "the header covers the first few"}, {"at": 0.85, "event": "you add the rest"}], sparse=False))

# ═════════════════════════════ ACT VIII · Daily Habits And Questions ═════════════════════════════
shell("B80", A8,
    "Three aliases save typing, and go in your global config: l g for the branch graph, s t for a short status, last for the last "
    "commit. Here is what l g draws, with branch and tag labels: main at the top, the merge, and the tag on the commit behind the paper.",
    "the branch graph  ·  " + REC_TITLE,
    [(C("git config --global alias.lg"), "Three aliases"), C("git config --global alias.st"), C("git config --global alias.last"),
     ("# git lg is that long form:", "branch graph"), C("git log --oneline --graph --all --decorate", exact=True),
     rl("session/cell53.out", "* bb5d912"), rl("session/cell53.out", "* 9c72349"), (rl("session/cell53.out", "*   0611b57"), "the merge"),
     rl("session/cell53.out", "|\\"), rl("session/cell53.out", "| * 6bb1d6d"), rl("session/cell53.out", "|/"),
     rl("session/cell53.out", "* 3abfaa1"), rl("session/cell53.out", "* eda7c83")],
    rings=[(7, "tag on the commit")])
shell("B81", A8,
    "And a small shell function that puts the branch name in your prompt, so you always know where you are. Here it prints the "
    "project name and main in brackets. It lasts for this session only, so no profile edit is needed.",
    "the branch in your prompt  ·  " + REC_TITLE,
    [sl("git_branch() {"), sl("git rev-parse --abbrev-ref HEAD 2>/dev/null | awk"), "}",
     ("", None), (sl('echo "rnaseq_project$(git_branch)"'), "project name"), rl("session/cell56.out", "rnaseq_project (main)")],
    rings=[(5, "main in brackets")])
shell("B82", A8,
    "Charts need no display. Two awk scripts draw a bar chart and a histogram in plain text, so they run on a login node. They "
    "are exploratory, so they live on their own branch, explore slash cli dash charts, until you decide to merge them.",
    "charts in plain text  ·  " + REC_TITLE + ", trimmed",
    [C("bash scripts/charts/bar_status.sh", exact=True), rl("session/cell60.out", "Gene regulation status"),
     (rl("session/cell60.out", "  NS "), "bar chart"), rl("session/cell60.out", "  UP "),
     rl("session/cell60.out", "  Total genes passing"), C("bash scripts/charts/hist_foldchange.sh", exact=True),
     (rl("session/cell62.out", "log2(Fold Change)"), "histogram"), rl("session/cell62.out", "  [-0.34"),
     rl("session/cell62.out", "  [-0.15"), rl("session/cell62.out", "  [+0.04"), rl("session/cell62.out", "  [+0.23"),
     (C("git switch -c explore/cli-charts", exact=True), "their own branch")],
    rings=[(2, "bar chart")])
add(manim("B83", A8,
    "Questions people ask. Can Git hold large datasets? Not directly. Git L F S handles files up to about two gigabytes, and "
    "D V C layers on Git and keeps the data elsewhere; track a manifest in Git. Jupyter notebooks carry their outputs, which makes noisy diffs: strip them with nbstripout, or sync with Jupytext.",
    "B83_BigFilesNotebooks",
    "Left: a Git logo chip with a small 'manifest' page inside a repository box, and an arrow to a 'storage' rack holding a big "
    "data block; chips 'Git LFS ~2 GB' and 'DVC' (mono) on the arrow. Right: a Jupyter logo chip and a notebook page with output chips on it; the output chips lift away, labelled 'nbstripout'.",
    [{"at": 0.15, "event": "data stays in storage; Git keeps a manifest"}, {"at": 0.55, "event": "notebook outputs make noisy diffs"}, {"at": 0.85, "event": "strip them"}], sparse=False))
add(manim("B84", A8,
    "To fix the last commit before you push, use commit dash dash amend. To undo a commit that is already shared, use git revert, "
    "which adds a new commit that undoes it. And never run git reset dash dash hard on a branch other people use: it throws work away.",
    "B84_UndoSafely",
    "A commit chain. Row 1: the last disc swaps for a corrected disc under 'commit --amend' (mono). Row 2: an extra disc arrives "
    "with a returning arrow under 'git revert'. Row 3: two discs vanish under 'git reset --hard' with a large cross and a group-of-people label 'shared branch'.",
    [{"at": 0.15, "event": "amend swaps the last commit"}, {"at": 0.5, "event": "revert adds an undo commit"}, {"at": 0.85, "event": "reset --hard on a shared branch: crossed out"}]))
add(manim("B85", A8,
    "If two branches changed the same lines, Git stops and marks the file. Open it, keep the version you want, delete the markers, "
    "then git add the file and commit. And git stash sets half-done edits aside; stash pop brings them back. We did not run either.",
    "B85_ConflictsAndStash",
    "A page with three marker lines (<<<<<<<, =======, >>>>>>>) in mono around two version blocks; the markers and the unwanted "
    "block wipe away, leaving one block, then chips 'git add' and 'git commit' land. Below, a half-done page slides into a drawer labelled 'git stash' and back out under 'stash pop'.",
    [{"at": 0.15, "event": "markers around two versions"}, {"at": 0.5, "event": "keep one, delete markers, add, commit"}, {"at": 0.85, "event": "stash and pop"}], sparse=False))

# ───────────────────────────── the closing three ─────────────────────────────
RECAP = ["A commit is a saved snapshot, and a tag is a fixed name for one of them.",
         "Track the code that makes results, and write the ignore file so its allow lines really work.",
         "Run, look, then commit the code and the result together, one logical change at a time.",
         "A branch holds an experiment; merge it when it belongs, and tag what you submit.",
         "Any old result comes back from its commit, one file at a time.",
         "On a cluster, commit before you submit, print the hash in the job log, and guard against a dirty tree."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. A commit is a saved snapshot, and a tag is a fixed name for one of them. Track the code that makes "
    "results, and write the ignore file so its allow lines really work. Run, look, then commit the code and the result together, one logical change at a time. "
    "A branch holds an experiment; merge it when it belongs, and tag what you submit. Any old result comes back from its commit, one file at a time. "
    "On a cluster, commit before you submit, print the hash in the job log, and guard against a dirty tree.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land in narration order"}],
    lane="bookend", lead_silence_s=0.5,
    qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("Open the folder of a project I have. List every file in this folder. For each one, say whether it is code, a "
             "setting, a result or raw data, and whether it should be tracked in Git. Then write a git ignore file that keeps "
             "the results out but lets one small summary file through, and tell me whether your git ignore file really lets "
             "that file through. Do not run anything and do not change any file.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude, with a copy of a real project folder open: " + YT_PROMPT + " Then check two things "
    "yourself. Did Claude run nothing and change no file? And does git check-ignore dash v agree with what it said about the summary file?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Plan Your Ignore File", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did Claude run nothing and change no file? It should only read and explain.",
                "Check: run git check-ignore -v on the summary file. Does Git agree with Claude?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": "Scientific Reproducibility Two: Version Control. At Nik Bear Brown.", "estimated_duration_s": 5.0,
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Scientific Reproducibility Two: Version Control. Learn to use "
                           "Git so that every result you produce, on a laptop or on a cluster, can be tied to the exact code that made it.",
         "estimated_duration_s": 14.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · VERSION CONTROL", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German (Hallo)",
    "audience": "A researcher who wants every result tied to the exact code that made it, on a laptop or a cluster; assumes no other film or book",
    "source_doc": "hpc-aicr/Scientific-Reproducibility-II-2026/scientific-reproducibility-II.md (read in full; commands shown verbatim) plus our written guide guides/scientific-reproducibility-ii.md and HPC.md Section 9",
    "playlist": "Northeastern HPC and AICR",
    "series_title": "Research Computing on Explorer and AICR",
    "lecture_opening_description": "Tie every result to the exact code that made it",
    "lecture_opening_title_lines": ["Scientific", "Reproducibility II:", "Version Control"],
    "tags": ["Git", "version control", "reproducibility", "gitignore", "branch", "tag", "Slurm", "Explorer", "AICR",
             "Northeastern University", "Research Computing", "HPC", "Nik Bear Brown"]},
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

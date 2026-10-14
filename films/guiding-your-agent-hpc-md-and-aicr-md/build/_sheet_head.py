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

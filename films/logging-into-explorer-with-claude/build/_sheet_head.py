#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-logging-into-explorer-with-claude.

LECTURE (Bear, 2026-10-02): the WHOLE source as one act-structured film, primarily visual, best visual per beat from
the full playset, a tool shown as itself. Skill doctrine: brutalist.art/skills/make/lecture/SKILL.md.

Source:   hpc-aicr/Logging-into-Explorer-with-Claude/SESSION.md (the real session, 2026-10-11) and hpc-aicr/skills/hpc/HPC.md section 10.
Evidence: every terminal line is READ FROM THE SESSION RECORD at build time by sl() below (a missing line stops the build).

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
TITLE = "Logging into Explorer (HPC) with Claude"
CAP = "lecture-logging-into-explorer-with-claude"      # captures: none (every terminal beat is the real session record)
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




SESSION = HERE.parents[1] / "Logging-into-Explorer-with-Claude/SESSION.md"
_SL = SESSION.read_text().splitlines()


def sl(start, maxlen=110, nth=0, exact=False):
    """The `nth` line of the real Explorer session record that starts with `start` (or equals it, if exact=True), verbatim; cut
    with an ellipsis if longer than maxlen. Stops the build if there is none: a film must never invent terminal output."""
    hits = [ln for ln in _SL if (ln == start if exact else ln.startswith(start))]
    if len(hits) <= nth:
        raise SystemExit(f"sl: no line (occurrence {nth}) {'equal to' if exact else 'starting with'} {start!r} in the session record")
    ln = hits[nth]
    return ln if len(ln) <= maxlen else ln[:maxlen].rsplit(" ", 1)[0] + " …"

#!/usr/bin/env python3
"""whisper_check.py — transcribe every narration mp3 (faster-whisper small.en, local, free) with word times.
Writes _qc/asr.json (words + start times, used to place Manim/Remotion cues on the spoken word) and
WHISPER-CHECK.md (sheet text beside what Liam actually said: BOPEN order, greeting, key terms).
Usage: python3 whisper_check.py [BID ...]   (pattern from the sibling film's whisper_check.py)"""
import json
import sys
from pathlib import Path
from faster_whisper import WhisperModel

HERE = Path(__file__).resolve().parent
sheet = json.loads((HERE / "beat_sheet.json").read_text())
only = set(sys.argv[1:])
model = WhisperModel("small.en", device="cpu", compute_type="int8")
asr_path = HERE / "_qc/asr.json"
asr = json.loads(asr_path.read_text()) if asr_path.exists() else {}
for b in sheet["beats"]:
    bid = b["beat_id"]
    if only and bid not in only:
        continue
    segs, _ = model.transcribe(str(HERE / "mp3" / f"beat-{bid}.mp3"), beam_size=5, language="en", word_timestamps=True)
    words = [{"w": w.word.strip(), "t": round(w.start, 2)} for s in segs for w in s.words]
    asr[bid] = {"heard": " ".join(w["w"] for w in words), "words": words, "sheet": b["narration_text"]}
    print(bid, "|", asr[bid]["heard"])
asr_path.parent.mkdir(exist_ok=True)
asr_path.write_text(json.dumps(asr, indent=1, ensure_ascii=False) + "\n")
out = ["# WHISPER-CHECK — what Liam said (faster-whisper small.en, local)", "",
       "**What.** Every narration mp3 transcribed and set beside the sheet's text.",
       "**Why.** File existence proves nothing about speech: the BOPEN order, the greeting and the key terms must be heard right.",
       "**Found.** See the verdict section at the end (written by hand after reading the table).", "",
       "| beat | sheet | heard |", "|---|---|---|"]
for b in sheet["beats"]:
    if b["beat_id"] in asr:
        out.append(f"| {b['beat_id']} | {b['narration_text']} | {asr[b['beat_id']]['heard']} |")
prev = (HERE / "WHISPER-CHECK.md").read_text() if (HERE / "WHISPER-CHECK.md").exists() else ""
verdict = prev[prev.index("## Verdict"):] if "## Verdict" in prev else "## Verdict\n\n(pending)\n"
(HERE / "WHISPER-CHECK.md").write_text("\n".join(out) + "\n\n" + verdict)

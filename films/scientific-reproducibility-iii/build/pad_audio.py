#!/usr/bin/env python3
"""pad_audio.py — make the sheet's lead/tail silences real in the audio (the toolkit's Kokoro generator and
compiler ignore lead_silence_s / tail_silence_s; film 1 of the series padded by hand with ffmpeg adelay/apad).
BIDEA +0.8 s lead, BVDT +0.5 s lead, BOUT +1.0 s tail. The unpadded original is copied to
_superseded/audio-unpadded/ first. Idempotent: keyed on the mp3's size+mtime (mp3/padded.json).
Writes the ffprobe duration back to beat_sheet.json, which stays the clock. Run after any (re)generation of
BIDEA, BVDT or BOUT (an `--only` re-voice also drops BOUT's pad), then re-run make_sheet.py.
"""
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
PADS = {"BIDEA": ("lead", 0.8), "BVDT": ("lead", 0.5), "BOUT": ("tail", 1.0)}
rec_path = HERE / "mp3/padded.json"
rec = json.loads(rec_path.read_text()) if rec_path.exists() else {}
sheet = json.loads((HERE / "beat_sheet.json").read_text())
keep = HERE / "_superseded/audio-unpadded"
keep.mkdir(parents=True, exist_ok=True)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)], text=True).strip())


for b in sheet["beats"]:
    bid = b["beat_id"]
    if bid not in PADS:
        continue
    mp3 = HERE / "mp3" / f"beat-{bid}.mp3"
    st = mp3.stat()
    if rec.get(bid) == f"{st.st_size}-{int(st.st_mtime)}":
        continue
    shutil.copy2(mp3, keep / mp3.name)
    kind, s = PADS[bid]
    tmp = mp3.with_name(f"beat-{bid}-pad.mp3")
    af = f"adelay={int(s * 1000)}:all=1" if kind == "lead" else f"apad=pad_dur={s}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-af", af, "-ar", "24000", "-ac", "1",
                    "-c:a", "libmp3lame", "-b:a", "192k", str(tmp)], check=True)
    tmp.replace(mp3)
    st = mp3.stat()
    rec[bid] = f"{st.st_size}-{int(st.st_mtime)}"
    b["actual_duration_s"] = round(dur(mp3), 2)
    print(f"{bid}: {kind} +{s}s -> {b['actual_duration_s']}s")
rec_path.write_text(json.dumps(rec, indent=2) + "\n")
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")

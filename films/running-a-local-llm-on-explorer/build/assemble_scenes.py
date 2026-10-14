#!/usr/bin/env python3
"""assemble_scenes.py — scenes.py = _kit_header.py (iso_kit + guard/pacing, pasted verbatim: Gate A copies only
scenes.py) + the measured word times (_ASR, from _qc/asr.json) + _kit_cast.py + _scenes_part*.py, then the midpoint
guard attached to every beat class. Re-run after editing any piece or after re-voicing a beat."""
import json
import re
from pathlib import Path
HERE = Path(__file__).resolve().parent
asr = json.loads((HERE / "_qc/asr.json").read_text()) if (HERE / "_qc/asr.json").exists() else {}
words = {bid: [[w["w"], w["t"]] for w in v["words"]] for bid, v in asr.items()}
import sys
args = sys.argv[1:]
letters = "ABCDEFG"
out_path = HERE / "scenes.py"
if "--parts" in args:
    letters = args[args.index("--parts") + 1]
if "--out" in args:
    out_path = HERE / args[args.index("--out") + 1]
parts = [HERE / f"_scenes_part{p}.py" for p in letters]
body = "\n\n".join(p.read_text() for p in parts if p.exists())
classes = re.findall(r"^class (B\d+_\w+)\(Scene\):", body, re.M)
out = (HERE / "_kit_header.py").read_text().rstrip() + "\n\n\n"
out += "# ── measured word times (faster-whisper on the Kokoro mp3s): { beat id: [[word, seconds], ...] } ──\n"
out += "_ASR = " + json.dumps(words, ensure_ascii=False) + "\n\n\n"
out += (HERE / "_kit_cast.py").read_text().rstrip() + "\n\n\n" + body.rstrip() + "\n\n\n"
out += "for _cls in (" + ", ".join(classes) + (",)" if len(classes) == 1 else ")") + ":\n    _cls.play = ST.play\n"
out_path.write_text(out)
print(out_path.name, "written;", len(classes), "scene classes")

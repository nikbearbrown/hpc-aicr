#!/usr/bin/env python3
"""qstill.py CLASS [CLASS ...] — fast look: render each Manim class at low quality into a scratch media dir,
cut frames at 10/25/50/75/95% and tile them into _qc/stills/<CLASS>.png. For LOOKING; not part of the build."""
import subprocess, sys, json
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent
SCR = Path("/private/tmp/claude-501/-Users-bear-Documents-CoWork/f1dde776-b09c-4df5-88a6-6d6593996204/scratchpad/qs")
(HERE / "_qc/stills").mkdir(parents=True, exist_ok=True)
args = sys.argv[1:]
scenes = "scenes.py"
if "--scenes" in args:
    i = args.index("--scenes"); scenes = args[i + 1]; del args[i:i + 2]
for cls in args:
    media = SCR / cls
    r = subprocess.run(["manim", "-ql", "--media_dir", str(media), str(HERE / scenes), cls], cwd=HERE, capture_output=True, text=True)
    for l in (r.stdout + r.stderr).splitlines():
        if "[pace]" in l or "Error" in l or "Traceback" in l or "error" in l.lower() and "SoX" not in l:
            print(cls, l.strip())
    vids = list(media.rglob(f"{cls}.mp4"))
    if not vids:
        print(cls, "NO VIDEO"); print((r.stdout + r.stderr)[-1500:]); continue
    v = vids[0]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)], text=True))
    ims = []
    for f in (0.1, 0.25, 0.5, 0.75, 0.95):
        out = media / f"f{int(f*100)}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(dur * f), "-i", str(v), "-frames:v", "1", str(out)], check=True)
        ims.append(Image.open(out).convert("RGB"))
    w, h = ims[0].size
    sheet = Image.new("RGB", (w * 3, h * 2), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 3) * w, (i // 3) * h))
    sheet.save(HERE / f"_qc/stills/{cls}.png")
    print(cls, f"{dur:.2f}s ->", HERE / f"_qc/stills/{cls}.png")

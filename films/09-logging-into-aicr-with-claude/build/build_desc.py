#!/usr/bin/env python3
"""build_desc.py — writes <slug>-youtube.md (the description DRAFT; never staged, never uploaded) from beat_sheet.json,
in the format publish_hpc.py produces: series line, chapters by act, Your Turn, sources, disclosure."""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
sh = json.loads((HERE / "beat_sheet.json").read_text()); m = sh["metadata"]; beats = sh["beats"]
def mmss(t): return f"{int(t // 60)}:{int(t % 60):02d}"
names = {"Opening": "Opening", "the idea": "The idea", "terms": "Terms in this lecture", "recap": "Recap", "your turn": "Your turn", "outro": None}
chapters, t, last = [], 0.0, None
for b in beats:
    act = b["act"]; nm = names.get(act, act)
    if act != last and nm:
        chapters.append(f"{mmss(t)} {nm}")
    last = act; t += b["actual_duration_s"]
bh = next(b for b in beats if b["beat_id"] == "BHTF"); pr = bh["shot"]["remotion"]["props"]
summary = next(b for b in beats if b["beat_id"] == "BOPEN")["narration_text"].split(". ", 2)[-1]
desc = f"""{m['title']}

{summary} Video {m['series_video_number']} of {m['series_video_count']} in the series {m['series_title']}. New here? Start with {m['series_entry_video']}. Liam, in for Bear, narrates.

Chapters
{chr(10).join(chapters)}

Your turn. Paste this into Claude:
{pr['command']}
Then check two things yourself: {pr['output'][0].replace('Check: ', '')} {pr['output'][1].replace('Check: ', '')}

Sources
The AICR documentation SSH page (certificate authentication, key files, login-node limits, troubleshooting) and a real, read-only Claude Code session on a Mac, recorded for this film. Every terminal line on screen is copied from that session.

Made with the brutalist.art toolkit: Manim, Remotion and Kokoro, free and local. Narration is synthetic (Liam, in for Bear). This is an independent educational film, not an official Northeastern or AICR publication. Every factual claim in this video was checked against primary sources before rendering.

#{' #'.join(re.sub(r'[^A-Za-z0-9]', '', t) for t in m['tags'][:8])}
"""
desc = desc.replace("<", "[").replace(">", "]")
assert len(desc.encode()) < 5000
(HERE / f"{m['slug']}-youtube.md").write_text(desc)
print(desc)

# Scene brief — claude-liam-lecture-running-a-local-llm-on-explorer

You write Manim scenes for ONE film (a `lecture`: "Running a Local LLM on Explorer", narrated by Liam, Kokoro audio ALREADY generated and measured). Several authors work in parallel; you own only your part file.

Reel folder: `<books>/hpc-aicr/youtube/claude-liam-lecture-running-a-local-llm-on-explorer/`  (call it R)
Toolkit: `<books>/brutalist.art/`

## Read first
1. `R/beat_sheet.json`: for each of YOUR beats read `narration_text`, `actual_duration_s`, `shot.visual_intent` (the design), `shot.show`. The narration is the clock. The design in `visual_intent` is the brief: follow it; you may improve the drawing, never add facts.
2. FINISHED EXEMPLARS from the sibling film (same kit, same cast, all gates passed): `<books>/hpc-aicr/youtube/claude-liam-lecture-guiding-your-agent-hpc-md-and-aicr-md/_scenes_partA.py` (B10 stopwatch + racks, B11 three cards, B12 two files, B21 split drawing) and `_scenes_partD.py` (B44 bars, B59/B60 flows, B61 gate). Copy their style, their `hear(self, "spoken phrase", lead=...)` cueing, how labels/chips are placed and how objects are removed.
3. `R/_kit_cast.py` (cast helpers: key_obj, padlock + unlock_anim, cert_page, aicr_rack, explorer_rack, job_box, home_box, scratch_bin, agent_slab, vault, chip, plaque, logo_chip) and the helper section at the end of `R/_kit_header.py` (T, M, L, pill, check, x_mark, professor_bear, Iso, hear, at, done, paper, scribble, scribbles_on). READ-ONLY: do not edit them.
4. `<books>/brutalist.art/skills/make/show-tell/SKILL.md` section "Drawing kit and laws" (DRAWING LAWS: every bullet is a real gate failure).
5. `R/_qc/asr.json` has word times per beat ({"B21": {"words": [{"w","t"}...]}}); `hear()` uses them. Use short, distinctive phrases that appear verbatim in the narration (punctuation ignored). The recogniser hears "Claude Code" as "clod code", "Ollama" as "Olama", "Apptainer" as "Aptainer"; cue on neighbouring words instead. PRINT the words of your beats before choosing cue phrases.

## What to deliver
ONE file `R/_scenes_part<X>.py` (your letter). Only scene classes and helpers; no imports, no kit code (everything in the kit/cast is in scope; scenes.py = header + cast + parts concatenated).
- Classes are written literally `class B31_HomeFills(Scene):` with the exact class name from `shot.manim.class`.
- Prefix every helper/constant with `p<X>_` (your part letter, e.g. `pB_`), so parts never collide. Define your own `p<X>_act_title(text)` (T(text, 40) placed top-left at x about -6.1, y 3.0; see the sibling's partA).
- Do NOT attach the midpoint guard (the assembler does). End every `construct` with `done(self)`.
- Pace with `hear()`: each motion lands on its spoken words. Total run time must be <= `actual_duration_s` (`[pace]` printed by `done`; "OVER" = bug, shorten run times, do not drop content). Leave the end calm: the last motion finishes at least 0.3 s before the target.
- The act titles (ONLY on the first Manim beat of an act): B10 "I · The Idea And Its Layers"; B20 "II · Wrong Turns To Avoid"; B40 "IV · Choose A GPU And A Model"; B60 "VI · Pattern B, From Your Laptop"; B80 "VIII · When It Breaks"; B90 "IX · The Cluster's Rules"; B100 "X · What To Expect". Acts III, V and VII open on terminal beats that carry their own title: other beats get none.

## Picture rules (short; the skill file is the long version)
- Primarily visual. On screen: labels of 1-3 words, real commands/addresses in mono (`M()`), a hero number. Never a sentence. Text size >= 32. Everything inside +/-6.2 x +/-3.3 (the iso origin is the LEFT-BACK corner of a block: a rack with `Iso(ox, ..., s)` extends from about ox - 1.4*s to ox + 2.1*s, so aim ox about 0.5*s left of the centre you want; check the stills).
- Motion carries the claim (still-frame test): every spoken point has a motion on its word; each scene must ADD at least one non-text shape after its first frame (Create/FadeIn/GrowFromCenter of a new object).
- One cast: reuse the cast helpers so the same object looks the same in every beat. A person is ALWAYS `professor_bear("1x1" or "2x3", height, seed="<beat id>", x=, y=)` (keep it at least 0.3 inside the safe edge: height 2.3 centred at x -5.05 is fine, 2.6 at -5.2 is not), never an icon.
- LOGO LAW: a company, product or tool is shown by its LOGO, never a bare word: `logo_chip("claude", x, y)` for Claude / the agent; `logo_chip("ollama", ...)` for Ollama; `logo_chip("caddy", ...)`, `logo_chip("vllm", ...)`, `logo_chip("continue", ...)`, `logo_chip("codex", ...)`, `logo_chip("opencode", ...)`, `logo_chip("qwen", ...)`, `logo_chip("nvidia", ...)` and 190 more in `brutalist.art/icons/logos/` (list: `ls <toolkit>/icons/logos`). NOT available (no logo exists): Aider and Droid: show those as plain mono chips (`chip("aider", x, y, mono=True)`). Never draw a tool's interface; the model itself is a plain labelled block 'model' or 'local model' (not a logo).
- Terracotta only for tape, dots, lights, a check, a ring pulse; never for text or thin bars. Numerals in ink. Labels BESIDE objects, never inside an outline (chips/plaques are outline-free white pills, fine). Keep x_mark small (r about 0.3 on a chip) and clear of other text.
- Midpoint law: GATE T and Gate V sample the clip MIDPOINT (target/2). At that moment there must be a visible label and nothing half-faded, half-drawn or mid-sweep (the guard will delay/shorten animations that straddle it, so place big moves before or after).
- Contrast: kraft key/boxes on cream need ink outlines (the cast already has them); do not put terracotta or pale kraft shapes alone on the stage; do not outline large objects in dark kraft.
- Facts: only numbers/names in the narration or `visual_intent`. Do not add facts. NO video numbers anywhere on screen.
- Classes literally `(Scene)`; do not use `rate_functions.ease_in_quad`/`ease_out_cubic` (use `ease_in` or smooth); `mob.animate(path_arc=)` crashes Gate A (use MoveAlongPath); do not mix `.animate` and MoveAlongPath on one mobject in one play; keep references to objects you later FadeOut.

## How to test (do all of it before reporting)
Work only in R. Never run `art run`, never render at 4K, never touch `beat_sheet.json`, `make_sheet.py`, `_kit_*.py`, another author's part, or anything outside R. Use the toolkit's python as `python3`.
1. Assemble YOUR scratch scenes: `python3 R/assemble_scenes.py --parts <X> --out scenes_<X>.py` (writes R/scenes_<X>.py = header + cast + your part + the guard attach).
2. LOOK: `python3 R/qstill.py --scenes scenes_<X>.py <Class> [<Class> ...]` renders a low-quality clip and tiles frames at 10/25/50/75/95% into `R/_qc/stills/<Class>.png`. READ that PNG with the Read tool and fix what is wrong (overlaps, cut-off at the frame edge, labels colliding, unreadable, empty midpoint). Iterate until each scene reads clearly. Note `[pace]` lines.
3. Gates, from a folder holding ONLY the scene file (Gate A copies only scenes.py): `mkdir -p /tmp/gateA_<X> && cp R/scenes_<X>.py /tmp/gateA_<X>/scenes.py` then
   `PYTHONPATH=<toolkit>/runtime/manim python3 <toolkit>/runtime/qc/static_scene_check.py /tmp/gateA_<X>/scenes.py --class <Class>`
   `python3 <toolkit>/runtime/qc/wcag_margin_check.py R/scenes_<X>.py --class <Class>`
   `cd R && python3 <toolkit>/runtime/qc/manim_layout_audit.py scenes_<X>.py --class <Class> --curve-strict`
   (exit 0 = pass; fix anything else). Delete `R/scenes_<X>.py` and `/tmp/gateA_<X>` when done.

## Report back
Per scene: class, one line of what moves, the `[pace]` line, the three gate results, and which stills you actually looked at. List anything you could not get to pass with the exact failure text. Never claim a pass you did not see.

## This film's cast (reuse the kit's helpers; do not invent new object styles)
- **The agent / Claude** is ALWAYS `logo_chip("claude", x, y)`.
- **The model** is a plain labelled block ('model' / 'local model' / 'ollama' next to the Ollama logo chip). Weights, context cache and tool definitions are plain stacked blocks with 1-3 word labels.
- **The cluster** is a rack: `explorer_rack(iso)` (small). Label racks 'login node' / 'GPU node' / 'compute node' / 'cluster'; `aicr_rack(iso)` (large) only in the AICR beat.
- **You** are `professor_bear`. **Your laptop** is a plain slab (a flat rounded rectangle with a smaller screen rectangle), labelled 'laptop'.
- **Real text** is only: addresses and commands the narration or the design names, in mono (`M()`).

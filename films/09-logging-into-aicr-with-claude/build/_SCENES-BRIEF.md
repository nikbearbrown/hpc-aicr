# Scene brief — claude-liam-lecture-logging-into-aicr-with-claude

You write Manim scenes for ONE film (a `lecture`: "Logging into AICR with Claude", narrated by Liam, Kokoro audio ALREADY generated and measured). Several authors work in parallel; you own only your part file.

Reel folder: `<books>/../build/`  (call it R)
Toolkit: `<books>/brutalist.art/`

## Read first
1. `R/beat_sheet.json`: for each of YOUR beats read `narration_text`, `actual_duration_s`, `shot.visual_intent` (the design), `shot.show`. The narration is the clock.
2. `R/_scenes_partA.py`: THREE FINISHED EXEMPLARS (B10, B21, B22). Copy their style, their `hear(self, "spoken phrase", lead=...)` cueing, `act_title()`, how labels/chips are placed and how objects are removed.
3. `R/_kit_cast.py` (cast helpers: key_obj, padlock + unlock_anim, cert_page, aicr_rack, explorer_rack, job_box, home_box, scratch_bin, agent_slab, vault, chip, plaque) and the helper section at the end of `R/_kit_header.py` (T, M, L, pill, check, x_mark, professor_bear, Iso, hear, at, done). READ-ONLY: do not edit them.
4. `<books>/brutalist.art/skills/make/show-tell/SKILL.md` section "Drawing kit and laws" (DRAWING LAWS: every bullet is a real gate failure).
5. `R/_qc/asr.json` has word times per beat ({"B21": {"words": [{"w","t"}...]}}); `hear()` uses them. Use short, distinctive phrases that appear verbatim in the narration (punctuation ignored). Print the words of your beats to choose cue phrases.

## What to deliver
ONE file `R/_scenes_part<X>.py` (your letter). Only scene classes and helpers; no imports, no kit code (everything in the kit/cast is in scope; scenes.py = header + cast + parts concatenated).
- Classes are written literally `class B31_FailFast(Scene):` with the exact class name from `shot.manim.class`.
- Prefix every helper/constant with your beat id or part letter (e.g. `pB_`), so parts never collide.
- Do NOT attach the midpoint guard (the assembler does). End every `construct` with `done(self)`.
- Pace with `hear()`: each motion lands on its spoken words. Total run time must be <= `actual_duration_s` (`[pace]` printed by `done`; "OVER" = bug, shorten run times, do not drop content). Leave the end calm: the last motion should finish at least 0.3 s before the target.
- The FIRST beat of an act carries the act title via `act_title("...")` (Act IV first beat B40: "IV · Rules For A Shared Cluster"; Act V first beat B50: "V · When It Fails"). Other beats do not.

## Picture rules (short; the skill file is the long version)
- Primarily visual. On screen: labels of 1-3 words, real commands/error text in mono (`M()`), a hero number. Never a sentence. Text size >= 32. Everything inside +/-6.2 x +/-3.3 (the iso origin is the LEFT-BACK corner of a block: a rack with `Iso(ox, ..., s)` extends from about ox - 1.4*s to ox + 2.1*s, so aim ox about 0.5*s left of the centre you want; check the stills).
- Motion carries the claim (still-frame test): every spoken point has a motion on its word; each scene must ADD at least one non-text shape after its first frame (Create/FadeIn/GrowFromCenter of a new object).
- One cast: reuse the cast helpers so the same object looks the same in every beat. A person is ALWAYS `professor_bear("1x1" or "2x3", height, seed="<beat id>", x=, y=)`, never an icon. "Claude" is a plain label/chip, never a product-interface drawing.
- Terracotta only for tape, dots, lights, a check, a ring pulse; never for text or thin bars. Numerals in ink. Labels BESIDE objects, never inside an outline (chips/plaques are outline-free white pills, fine). Keep x_mark small (r about 0.3 on a chip) and clear of other text.
- Midpoint law: GATE T and Gate V sample the clip MIDPOINT (target/2). At that moment there must be a visible label and nothing half-faded, half-drawn or mid-sweep (the guard will delay/shorten animations that straddle it, so place big moves before or after).
- Contrast: kraft key/boxes on cream need ink outlines (the cast already has them); do not put terracotta or pale kraft shapes alone on the stage; do not outline large objects in dark kraft.
- Facts: only numbers/names in the narration or `visual_intent`. Do not add facts.
- Classes literally `(Scene)`; do not use `rate_functions.ease_in_quad`/`ease_out_cubic` (use `ease_in` or smooth); `mob.animate(path_arc=)` crashes Gate A (use MoveAlongPath); do not mix `.animate` and MoveAlongPath on one mobject in one play; keep references to objects you later FadeOut.

## How to test (do all of it before reporting)
Work only in R. Never run `art run`, never render at 4K, never touch `beat_sheet.json`, `make_sheet.py`, `_kit_*.py`, another author's part, or anything outside R.
1. Assemble YOUR scratch scenes: `python3 R/assemble_scenes.py --parts <X> --out scenes_<X>.py` (writes R/scenes_<X>.py = header + cast + your part + the guard attach).
2. LOOK: `python3 R/qstill.py --scenes scenes_<X>.py <Class> [<Class> ...]` renders a low-quality clip and tiles frames at 10/25/50/75/95% into `R/_qc/stills/<Class>.png`. READ that PNG with the Read tool and fix what is wrong (overlaps, cut-off at the frame edge, labels colliding, unreadable, empty midpoint). Iterate until each scene reads clearly. Note `[pace]` lines.
3. Gates, from a folder holding ONLY the scene file (Gate A copies only scenes.py): `mkdir -p /tmp/gateA_<X> && cp R/scenes_<X>.py /tmp/gateA_<X>/scenes.py` then
   `PYTHONPATH=<toolkit>/runtime/manim python3 <toolkit>/runtime/qc/static_scene_check.py /tmp/gateA_<X>/scenes.py --class <Class>`
   `python3 <toolkit>/runtime/qc/wcag_margin_check.py R/scenes_<X>.py --class <Class>`
   `cd R && python3 <toolkit>/runtime/qc/manim_layout_audit.py scenes_<X>.py --class <Class> --curve-strict`
   (exit 0 = pass; fix anything else). Delete `R/scenes_<X>.py` and `/tmp/gateA_<X>` when done.

## Report back
Per scene: class, one line of what moves, the `[pace]` line, the three gate results, and which stills you actually looked at. List anything you could not get to pass with the exact failure text. Never claim a pass you did not see.

## YOUR SCENES

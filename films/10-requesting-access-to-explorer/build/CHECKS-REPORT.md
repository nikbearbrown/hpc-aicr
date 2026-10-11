# CHECKS-REPORT — Requesting Access to Explorer (lecture)

**What this is.** The PROOF GATE result before the first compile (layout stage, 2026-10-11). **Result.** No punts, no holds.

29 beats: 23 body beats SHOW / 0 justified-HOLD / 0 PUNT-flagged, plus the closing and opening cards (BOPEN title card CARD, BIDEA writer, BDEFS terms CARD, BVDT recap CARD, BHTF composer, BOUT outro).

Teaching arc: FRAMEWORK ✓ (B10-B12: the rule and the roles before any procedure) | WORKED EXAMPLE ✓ (B30-B35 the real first screen of the form; B22 the real commands; B41 the real prompts) | FALSIFIABILITY ✓ (B10 a login alone is turned back; B24 not confirmed for new users; B50-B52 what failure looks like) | SCAFFOLDED TASK ✓ (BHTF: a prompt plus two checks) | BOOKENDS ✓ (title card, hesitant writer, terms, recap, your turn, outro) | NO-SOURCE-NO-VERDICT ✓ (every claim beat carries its artifact: the form, the commands, the real prompts, the real dashboard; the one sketch, B21, is labelled as a sketch)

Lane histogram (body, information only): cast/isometric drawing 8 · Manim diagram 5 · built card of a tool (the access form, 5 beats) · real terminal 3 · real web capture 2 · text-only card 0.

Beat count in the sheet: 29 (3 opening + 23 body + 3 closing; BOPEN counted in the opening three). Estimated runtime 441 s (7 min 20 s) from word counts; the real figure comes from the audio.

Verified by running in this stage: `make_sheet.py` (phrase guard: every `until()` phrase in `scenes.py` is in its narration; every cue phrase in the sheet is in its narration; no TODO), Manim syntax and a low-resolution last-frame render of all 13 scenes (looked at), TypeScript check of the new component, a static render of the new component in four states (looked at), `./brutalist.art/art scenes --check` of every existing component cited, `pronunciation.py --say` on the unusual lines. Not run: audio, 4K, Gate V/T/A/B, bookend check (the build stage does these).

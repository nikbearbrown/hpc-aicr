# BUILD-LOG — Requesting Access to Explorer (lecture)

**What this is.** Decisions, open questions and the layout-stage record. **Stage.** LAYOUT ONLY (Cowork stage of the two-stage build, 2026-10-11): nothing was synthesised, rendered at 4K, run through `art run`/`art final`, staged or published. The Claude Code stage follows `BUILD-PROMPT.md`.

## Decisions (2026-10-11)

- **Film number: PROVISIONAL 10 of 13.** Films 1 to 9 are taken (AICR Introduction 1, Optimizing GPU Usage on AICR 2, Intro to Explorer and OOD 3, Intro to GPUs 4, Intro to Parallel Computing 5, Intro to Linux 6, Scientific Reproducibility 7, Installing Software 8, Logging into AICR with Claude 9 being built by another agent); Managing /projects on Explorer is unnumbered. 10 is the next free number. **Bear: confirm or change** (`series_video_number` and `chapter_number` in `make_sheet.py`, then re-run it and rebuild the BOPEN card).
- **BOPEN pointer** reads "New here? Start with Video 1 · AICR Introduction" (the skill says the actual series-entry title; the AICR Introduction beat sheet calls it "Video 1 · AICR Introduction"). The brief wrote "Video 1 · Introduction"; one field (`series_entry_video`) changes it.
- **Playlist** "Northeastern HPC and AICR"; **series** "Research Computing on Explorer and AICR". The BOPEN speech uses the series name (as the sibling films do).
- **Greeting** "Bonjour" (the earlier films used Hallo and Hola).
- **AICR** appears only in the spoken series name; the pronunciation dictionary voices it (not edited).
- **BDEFS** has no "Login node": the source never defines it.
- **BHTF** is a pasteable prompt that drafts the viewer's message to their sponsor (username, the exact `project ... add members` command, four sentences) plus two checks. `props.command` is read in full inside the narration; the narration also carries the lead-in and the two checks, as in the sibling films.
- **Neutral phrasing of the username**: only "the UserID from the form worked, in the one real login checked"; no rule, no real value on screen, `<username>` everywhere.

## Layout-stage changes after the first draft (coordinator updates, same day)

1. Real-login facts (UserID worked; ssh asks the host-key question then the password; no Duo prompt on SSH): B40, B41, B50, BVDT updated; B41 shows only the two real prompt lines (host-key question, `password:`), no banner.
2. Managing /projects app and the two-hour delay: new B21 (sketch of the announced controls, rung 3, labels only), B22 is the command (srun, add, comma list, view members in one beat), new B23 (up to two hours, fresh login session), B24 the caveat (now "either way").
3. Real Northeastern sign-in capture: new B30 (BrowserCapture, one ring on the sign-in box, nothing typed); the form card opens in B31.
4. Hedge rule: B36 says "we think" aloud and on screen about what happens after submit; logged HEDGED in FACTCHECK.md.

## Things Bear can replace with a real capture

- **B31-B35: the form card (`AccessFormCard`).** Built because the form is behind sign-in and was not captured; reproduces only the confirmed first screen. If Bear records the real form, swap exactly these frames: B31 (fields, from the open page to the ring on UserID), B32 and B33 (the two radio options being selected), B34 (the two paragraphs, camera on "sponsor-owned storage space" then "its owner can add members"), B35 (scrolling to where the form continues, then stop). The paragraph wording on the card is the build's phrasing of the README's substance, and the colours of the page chrome (near-black top bar, left menu of seven items) are approximations: **check both against the real screenshot before publishing** (FACTCHECK rows 30 and 32). Use a recording with the personal fields blank or blurred.
- **B21: the Managing /projects app sketch.** Labels only (Files > Managing /projects, Group, Usernames, Launch, Output log), captioned "Sketch of the announced controls". A real capture of the app (signed in, group chosen, no real usernames) replaces the whole beat.
- B24 and B36 are drawings of "not confirmed" and "we think"; no capture can replace them.

## Open questions for Bear

1. Film number 10: confirm (above).
2. Check the form card's two paragraphs and page chrome against your screenshot (above).
3. B36's hedged guess ("we think your sponsor is asked to approve it") is the example you gave; if you would rather not guess about the sponsor at all, B36 can be replaced by the one-line "ask Research Computing" (the narration is in `make_sheet.py`, `N["B36"]`).
4. The Managing /projects announcement is spoken as the simpler way; I did not say it works for someone with no account (not confirmed). OK?
5. Public description line: the film is built from Northeastern Research Computing's material and Bear's own first login; the description step is not part of this stage.

## Lane histogram (body, information only) and estimated runtime

Cast/isometric drawing 8 (B10 B11 B24 B36 B44 B50 B51 B52) · Manim diagram 5 (B12 B20 B21 B23 B40) · built card of the form 5 (B31-B35) · real terminal 3 (B22 B41 B43) · real web capture 2 (B30 B42) · text-only card 0. 23 body beats. Estimated runtime about 441 s (7 min 20 s) from word counts; the measured audio is the real clock.

## Built or checked in this stage

- Written: `ACTS.md`, `SHOTLIST.md`, `FACTCHECK.md`, `CHECKS-REPORT.md`, `PROMPTS.md`, `SOURCES.md`, `make_sheet.py`, `beat_sheet.json` (narration filled, no TODO), `_kit.py`, `_scenes_body.py`, `scenes.py` (generated by `cat _kit.py _scenes_body.py`), `new-components/AccessFormCard.tsx`, `BUILD-PROMPT.md`, this file; `captures/screenshot_OOD.png` and `captures/northeastern-sign-in.png`.
- Checked by running: `make_sheet.py` guards; Manim syntax + a low-resolution last-frame render and visual look at all 13 scenes (fixes made: overlaps in B10/B20/B21/B23/B40/B50, command-box label); TypeScript check and a static four-state render of `AccessFormCard`; `art scenes --check` for the existing components; `pronunciation.py --say` on the unusual lines (Bonjour, s run, who am I, user I D, host-key, N U R C).
- **Not run (by design):** audio, any 4K render, `art run`, `art final`, Gate V/T/A/B, the bookend check. The form card and the whole Remotion side were never rendered by Remotion (it needs registering first; see BUILD-PROMPT.md step 1).

## Build-stage log

(The build-stage session appends here: audio durations, gate results, any smallest-unit fix.)

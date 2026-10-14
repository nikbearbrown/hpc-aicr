# BUILD-PROMPT — Requesting Access to Explorer (lecture, Liam)

**What this is.** The whole handoff for the build stage of one film. A higher-effort session did the layout (read the source, acts, shot list, fact check, narration, beat sheet, Manim scenes, the new Remotion form card) and stopped. You do the mechanical build. **You need no other context.** Run every command from `<books>` (call it `books/`).

**Rules for you.** Do not change the narration, the scene design or the beat sheet. If a gate fails, fix the smallest unit (one scene, one prop, one cue) and re-run only that, and log it under "Build-stage log" in `BUILD-LOG.md`. Free steps run straight through with no approval stops. Never publish, stage (`art post`), or upload anything. No paid generation. Do not edit `liam.json`.

## Paths (all absolute)

- Reel folder `R`: `<books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer`
- Source: `<books>/hpc-aicr/Requesting-Access-to-Explorer/README.md`
- Skill: `<books>/brutalist.art/skills/make/lecture/SKILL.md`
- New component: `R/new-components/AccessFormCard.tsx`
- Captures: `R/captures/northeastern-sign-in.png` (Bear's, B30) and `R/captures/screenshot_OOD.png` (the training's, B42; already public in `runtime/remotion/public/lecture-explorer-ood/`)
- Layout record: `R/ACTS.md`, `R/SHOTLIST.md`, `R/FACTCHECK.md`, `R/CHECKS-REPORT.md`, `R/PROMPTS.md`, `R/SOURCES.md`, `R/BUILD-LOG.md`

## What is already done

29 beats in `R/beat_sheet.json` (3 opening, 23 body, 3 closing), narration final, no TODO. Thirteen Manim scenes in `R/scenes.py` (importable, low-res last frames looked at). One new Remotion component (`AccessFormCard`, type-checked, statically rendered in four states and looked at) that is **not yet registered**. Captures copied. Paperwork written. **Nothing has been voiced or rendered**: no audio, no Remotion render, no 4K.

Beat map: BOPEN title card · BIDEA hesitant writer · BDEFS terms · Act I B10 B11 B12 · Act II B20 B21 B22 B23 B24 · Act III B30 (real sign-in capture) B31-B35 (the form card) B36 (hedged) · Act IV B40 B41 B42 (real dashboard) B43 B44 · Act V B50 B51 B52 · BVDT · BHTF · BOUT. Manim beats: B10 B11 B12 B20 B21 B23 B24 B36 B40 B44 B50 B51 B52. Terminals (`CCPlainShell`, no output shown): B22 B41 B43. Captures (`BrowserCapture`): B30 B42. Form card: B31-B35.

## Steps, in order

**1. Register the new component (first, before anything else).** Copy and register it, then re-index:

```bash
cp <books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer/new-components/AccessFormCard.tsx ./brutalist.art/runtime/remotion/src/scenes/AccessFormCard.tsx
mkdir -p ./brutalist.art/runtime/remotion/public/lecture-requesting-access
cp <books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer/captures/northeastern-sign-in.png ./brutalist.art/runtime/remotion/public/lecture-requesting-access/
```

In `./brutalist.art/runtime/remotion/src/Root.tsx`, add the import beside the `BrowserCapture` import (line ~734):

```tsx
import {AccessFormCard, accessFormCardSchema, accessFormCardDefaultProps} from './scenes/AccessFormCard';
```

and the composition right after the `BrowserCapture` `<Composition ... />` block (line ~4198; match its style):

```tsx
<Composition
  id="AccessFormCard"
  component={AccessFormCard}
  durationInFrames={300}
  calculateMetadata={({props}) => ({durationInFrames: Math.ceil(((props as any).durationSeconds ?? 10) * 30)})}
  fps={30}
  width={1920}
  height={1080}
  schema={accessFormCardSchema}
  defaultProps={accessFormCardDefaultProps}
/>
```

Then `./brutalist.art/art scene-index` and `./brutalist.art/art scenes --check AccessFormCard` (must say RENDERABLE). Check `ps aux | grep -E 'manim|remotion|compile' | grep -v grep` first: if another film is compiling, wait; do not edit Root.tsx while a render is running (it will pick up the change). Check that no other agent has added conflicting edits to Root.tsx (look at the file before and after).

**2. Rebuild the sheet** (idempotent; keeps measured audio): `python3 <books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer/make_sheet.py`. It must print `29 beats`.

**3. Audio (free, Kokoro am_onyx).**

```bash
python3 ./brutalist.art/runtime/scripts/generate_audio_kokoro.py <books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer
```

Pad BOUT with a 1.0 s silent tail and write its duration back (this is what `publish_hpc.py` does):

```bash
R=<books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer
ffmpeg -y -loglevel error -i $R/mp3/beat-BOUT.mp3 -af apad=pad_dur=1.0 $R/mp3/beat-BOUT-pad.mp3 && mv $R/mp3/beat-BOUT-pad.mp3 $R/mp3/beat-BOUT.mp3
ffprobe -v error -show_entries format=duration -of csv=p=0 $R/mp3/beat-BOUT.mp3
```

Put that duration in `actual_duration_s` for BOUT in `beat_sheet.json` (a JSON edit of that one field, as `publish_hpc.py` does), then re-run `make_sheet.py` again so every audio-dependent cue (terminal line cues, definitions, captures, form card durations) is recomputed from the measured clock. Do not edit narration to fix timing; regenerate and re-run.

**4. Whisper-check** the audio (greeting "Bonjour", "AICR" in the title card, "S S H", "who am I", "user I D", "H P C", "N U R C", the e-mail spelled out, "Duo"). Use the sibling check if it exists: `<books>/hpc-aicr/youtube/claude-liam-lecture-logging-into-aicr-with-claude/whisper_check.py` (read it first; copy it into `R/` and point it at `R/`), otherwise faster-whisper by hand. A mispronounced single beat is re-voiced with `generate_audio_kokoro.py <R> --only <BID>` (never respell in the narration text; if a word is wrong in a way the dictionary should fix, log it as an open question; do not edit `liam.json`).

**5. Title card (BOPEN).** After BOPEN's audio is measured:

```bash
python3 ./brutalist.art/skills/make/lecture/templates/title-slide-16x9/build.py --out $R/opening --sheet $R/beat_sheet.json --width 3840
mkdir -p $R/media && cp $R/opening/example-opening-*.mp4 $R/media/BOPEN.mp4
```

(Use the absolute `R`; the card builder refuses to overwrite an existing MP4, so delete a stale `opening/example-opening-*.mp4` first.) LOOK at the card: Professor Bear portrait left, title "Requesting Access to Explorer", "Video 10 of 13", "New here? Start with Video 1 · AICR Introduction", "Liam, in for Bear · Narration".

**6. Stills first (before any 4K).** Manim, one low-resolution last frame per scene, into a scratch folder, contact sheet, LOOK at it:

```bash
cd $R && for c in B10_GateNeedsStorage B11_StorageSpace B12_RoleLadder B20_TwoRoutes B21_ManagingApp B23_TwoHourDelay B24_NewUserCaveat B36_AfterSubmit B40_WhichName B44_HomeScratch B50_Rejected B51_NotInProject B52_NoStorage; do manim -ql --save_last_frame --media_dir $R/_stills scenes.py $c; done
```

Remotion beats: if `remotion_scenes.py --help` offers stills, take 25/50/95% of each; otherwise judge them from the review cut's `qc-sheet.png` in step 7. Look specifically for overlapping labels, text on a portrait, a cut-off label, and any real person's data (there must be none: the form card shows only placeholders).

**7. Review cut at 4K.**

```bash
./brutalist.art/art run <books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer --height 2160
```

Render Remotion only through this path (it calls `remotion_scenes.py` in the foreground); never hand-roll `npx remotion render`. Look at `qc-sheet.png` and a frame from each beat. Gate L, A, B, V must pass (no BLOCKER or MAJOR in Gate V). A long film is fine in one run; if a Manim scene fails Gate A, remember Gate A copies only `scenes.py`.

**8. Final master at 4K.**

```bash
./brutalist.art/art final <books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer --height 2160 --out <books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer/exports/landscape
```

GATE T runs first and must PASS (write nothing into `TYPECHECK.md` by hand; the gate does).

**9. Bookend check.** `python3 ./brutalist.art/runtime/scripts/bookend_check.py <books>/hpc-aicr/youtube/claude-liam-lecture-requesting-access-to-explorer` must PASS (title card, then hesitant writer, spoken @NikBearBrown outro).

**10. Master check.** `ffprobe` the master in `R/exports/landscape/`: 3840x2160, H.264/AAC, duration equals the sum of the measured audio (BOPEN card included), the 1.0 s silent tail present, audio sample rate sane (a past loudnorm pass left some masters at 96 kHz AAC; if so, re-encode audio to 48 kHz and note it in `BUILD-LOG.md`). Write the master's absolute path, runtime and sha256 in `BUILD-LOG.md`.

## Gates that must PASS

F (the paperwork exists: `FACTCHECK.md`), A, B, V, T, bookend, PROOF (`CHECKS-REPORT.md` exists, no PUNT), plus the master check. One FAIL anywhere = fix the smallest unit and re-run only that.

## Traps already known

- **`scenes.py` is generated.** Edit `R/_scenes_body.py` (or `_kit.py`), then `cat _kit.py _scenes_body.py > scenes.py`. Never edit `scenes.py` alone.
- **Manim/Pango may drop single spaces** at fused boundaries on Bear's Mac (`Text()`); LOOK at every multi-word label in the stills ("email prefix", "No account yet", "We think this is how it works", "up to 2 hours", "Files → Managing /projects"). If one fuses, double the space in that one string only.
- **Nothing may animate inside the 45-55% window of a beat** (GATE T and Gate V sample the midpoint). `make_sheet.py` already moves card and capture cues out of it; `scenes.py` has the midpoint guard (`ST`) attached to all 13 classes (the loop at the bottom of `_scenes_body.py`: a new scene class must be added to it). If a Remotion beat's frame at 50% is mid-transition, move that one cue in `make_sheet.py`, not the narration.
- **`until()` cues** in the scenes use the measured audio via `beat_sheet.json`; if you regenerate audio, run `make_sheet.py` before rendering.
- **Terminal cues** (`lineCues`, `rings`) are computed by `make_sheet.py` from the measured duration at 30 fps: re-run it after audio, and again after any re-voice.
- **GATE T type floor** is about 41 px at 4K. The form card's smallest text is 26 px at 1920 (the left-menu items), which is 52 px at 4K; if the gate objects to the menu, raise its size to 28, nothing else. §8.5 (no wordy card) counts props named `note`, `text`, `title`, `body`, `output` etc.; `AccessFormCard` deliberately avoids those names for the page text, and the card's text is the real artifact, so do not rename props to dodge a different gate; flag it in `BUILD-LOG.md` instead.
- **A ring that touches text merges with it** in GATE T's blob analysis; `BrowserCapture` rings in B30 and B42 are padded. If a ring still merges, widen it, do not remove it.
- **B30's capture is portrait** (1176x1230). `BrowserCapture` fits width at scale 1, so the camera crops vertically; the focus values are already chosen. B42 reuses the training's screenshot with the browser strip already cropped (`imageAspect` 2126/1284).
- **Fonts:** Remotion text uses EB Garamond and the UI/mono stacks from `tokens/claude.ts`; the form card uses the UI sans for page text on purpose (it imitates a web form, not the Claude app).
- **Professor Bear portraits** come from `brutalist.art/professor-bear/` by seed (`req-you`, `req-sponsor`, `req-delegate`); do not change seeds (the cast stays the same across beats). The title card picks its own portrait from the slug.
- **Do not describe anything below the form's first screen** and do not state B36's guess as fact: the on-screen label "We think this is how it works" and the spoken hedge are the point.
- **No credentials anywhere.** The sign-in capture is a picture; nothing is typed. Never put Bear's real name, UserID, email or phone on screen; the film uses `<username>` and placeholders only.
- **Another film may be compiling in the same toolkit.** Check for running `manim`/`remotion`/`compile` processes before step 1 and before steps 7 and 8; render only in the foreground, one at a time.

## STOP

When the master exists and every gate passes: report its absolute path, runtime, the lane histogram (in `BUILD-LOG.md`) and any gate that did not pass. **Do not publish, do not run `art post`, do not stage into TOPOST, do not upload.** Bear watches the film first.

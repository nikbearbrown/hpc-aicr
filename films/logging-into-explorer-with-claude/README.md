# Logging into Explorer (HPC) with Claude

**What this is.** A film in the series *Research Computing on Explorer and AICR* (about 5 minutes) on making a key, unlocking it once, and letting Claude Code log into Explorer for you without ever holding your password, passphrase or key. **Status:** published.

**Watch the film:** https://youtu.be/KEKiKe6roQk (unlisted).

## Where it comes from

Written for this repository from a real, read-only login session on the cluster (`source/SESSION.md`, usernames replaced by placeholders). Every claim in it says what it rests on.

## What is in this folder

- `source/`: the real session the film is made from.
- `build/`: how the film was made. `beat_sheet.json` is the heart; `make_sheet.py` regenerates it (every terminal line is read from the session record); `scenes.py` holds the Manim animations; the `.md` files are the plan and the record. Rendered video, audio and large images are not included (they are rebuilt, see below).

## Redo it

The films are built with the [brutalist.art](https://github.com/nikbearbrown/brutalist.art) toolkit (Manim and Remotion scenes, free Kokoro narration). Put `build/` where the toolkit expects a film folder, regenerate the audio and run its review and final steps. The narration was voiced with Liam, an AI voice (Kokoro `am_onyx`), speaking in for the author.

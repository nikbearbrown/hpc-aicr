# BUILD-PROMPT — Logging into AICR with Claude (lecture)

**What this is.** The handoff brief this film was built from, saved first, verbatim from the parent session (2026-10-11). **Why.** A reel without its build prompt is unfinished.

---

You are building ONE film with the `lecture` skill, in Bear's brutalist.art ("dot") toolkit, run from <cowork>/bear-textbooks/books. Bear's words: "Again, you're using the lecture [skill] with a Liam persona. The next one has to be logging into AICR with Claude. We have to actually do it."

READ FIRST, completely, before touching anything:
1. <books>/brutalist.art/skills/make/lecture/SKILL.md (the governing skill) and the skills it points to as you route beats (nopunt, show-tell, your-turn, cc-explainer, deep-explainer, ai-explainer as needed).
2. <books>/CLAUDE.md and AGENTS.md (global rules: TOPOST-only publishing, GATE T, absolute paths in reports, free steps run with no approval gate).
3. THE SOURCE (the whole of it is the "chapter"): <books>/../source/README.md
4. THE EVIDENCE (every terminal beat traces to it, verbatim): <books>/../source/SESSION.md
5. The primary the README rests on: <books>/the AICR documentation 'SSH' page (local copy not included) and a private project setup note (not included) section 2.
6. The sibling film to reuse scaffolding from (scenes.py, _kit.py, make_sheet.py, cast, BrowserCapture/CCPlainShell usage, FACTCHECK/CHECKS-REPORT formats): <books>/../build/ . Also read youtube/publish_hpc.py (the series procedure) and PLAYLIST-DESCRIPTION.md.

BUILD INTO (create): <books>/../build/
Save THIS brief there first as BUILD-PROMPT.md (it is the handoff).

FIXED FACTS
- Channel claude-liam: Liam, in for Bear, Kokoro am_onyx, @NikBearBrown outro (locked). metadata.skill/style_preset "lecture". Series fields on BOPEN: playlist "Northeastern HPC and AICR", series "Research Computing on Explorer and AICR"; work out this film's video number/total from the sibling films' metadata (series_video_number) and the playlist note (8 published of 13 planned), choose the next free number honestly, and log how you chose it in BUILD-LOG.md. "New here? Start with Video 1 · Introduction" per the skill (the series entry is the AICR Introduction film; check its exact title in its beat_sheet).
- Title (exact, Title Case): "Logging into AICR with Claude".
- PRONUNCIATION: Bear dictated "Aker"; the correct spelling is AICR. The dictionary at brutalist.art/runtime/pronunciation/liam.json (edited today, --check passes) makes Liam say AICR and aicr as the four letters A-I-C-R, ONE way throughout. Write AICR in narration_text exactly (capital) and let the dictionary voice it; never respell in the text, never mix with "acre/Aker". Hostnames may be written "login.aicr.ai" in on-screen text; in narration say it in words ("login dot aicr dot A I") and verify with `python3 brutalist.art/runtime/scripts/pronunciation.py --say "<line>"`. Whisper-check the audio for the acronym and for "S S H".
- SELF-CONTAINED law: viewer has read nothing else. Do not say "the README"/"this guide". The course credit is NOT used (series films say the series, not a course).
- Audience: a researcher with an AICR account (generic, not Bear's machine). On-screen identities may show the real run's user (<aicr-username>) only inside verbatim captured output; narration says "your AICR user name".

THE FILM'S SHAPE (propose in ACTS.md, adjust if the source demands; every README section is in an act or in LEFT OUT with a reason; write the coverage map FIRST)
 Act I  What AICR checks (no password; key + CA-signed certificate; the four files from ood.aicr.ai; human-only steps: sign in, download, passphrase).
 Act II Why Claude can't type a passphrase, and the fix: unlock once into ssh-agent. The key idea. Config block (REAL text, ClaudeCodeBeat), macOS/Linux/Windows agent commands (show as the real commands; macOS --apple-use-keychain).
 Act III Do it, for real: (a) BatchMode test; (b) the real Run 1 output (whoami, hostname, sinfo) on CCPlainShell; (c) the agent-empty proof (Run 3: ssh-add -l, ssh-add -D, empty, BatchMode login works, key is back) — this is the film's centrepiece, give it the most care; (d) how it authenticated (Run 2: cert offered, server accepts, publickey).
 Act IV Rules for a shared cluster (read-only first, no compute on login nodes: 4 CPU cores / 8 GB, ask before sbatch/scancel/rm, never print/copy the key, never put the passphrase in a prompt, own account only).
 Act V When it fails (empty agent looks exactly like an expired cert; check ssh-add -l before blaming the cert; the other troubleshooting rows).
 Then BVDT (4 or 6 lines), BHTF Your Turn (a pasteable prompt = the README step 6 prompt, read in full, props.command == narration_text, two output checks), BOUT per channel. Opening three: BOPEN (narrated portrait/title card, template contract in the skill; Professor Bear portrait from the 1x1 library, slug-seeded), BIDEA (BrutalistHesitantWriter: the naive framing "Give Claude my password" corrected into "Unlock the key once; Claude never sees it" — trigger phrase must appear verbatim in text, neither ends in punctuation), BDEFS (3-6 terms <=17 chars, e.g. Private key, Certificate, ssh-agent, BatchMode, Login node).

SHOW-THE-THING (the skill's law): Real terminal output only from SESSION.md, verbatim, on CCPlainShell, durations set so lines land with the voice. A Claude Code surface (CCSession/CCToolCall) may show ONLY the Bash tool call Claude actually ran and its real output; do NOT invent a typed user prompt and do NOT mock any interface. OnDemand (ood.aicr.ai) sign-in is behind CILogon: reuse the sibling film's real public capture at ../build/captures/ood.png via BrowserCapture (it is the real page); never enter credentials anywhere. A page that cannot be captured is not invented. Concept beats (key + lock + agent; the path from Claude to the cluster) may be isometric drawings per show-tell's DRAWING LAWS, clearly conceptual, never presented as an observed session. Keep one cast per act. Audition >=2 lanes per body beat, SHOTLIST.md with runner-up, FACTCHECK.md (every claim vs README/SSH docs/SESSION.md), CHECKS-REPORT.md before the first compile, TYPECHECK.md no FAIL, MASTERCHECK.md. Motion must carry the claim (still-frame test).

SAFETY (hard)
- You MAY NOT touch the cluster's state. You do not need to ssh at all: the evidence exists. If you want one extra fact, only read-only commands, once, and log it in SESSION.md. Never read, print, copy or cat ~/.ssh/id_ed25519_aicr or any private key or the .passphrase; never put either in a file.
- Do NOT publish, stage (`art post`), or upload anything to YouTube. No paid generation (no Higgsfield). Free steps run straight through with NO approval gate.
- Do not edit brutalist.art/runtime/pronunciation/liam.json again (already done); if a word is mispronounced, report it. New Remotion/Manim components you must build are allowed (register + `./art scene-index`, log in BUILD-LOG.md).
- Never edit a beat sheet while a compiler is running. Regenerate only the failing unit.

PIPELINE: ACTS.md -> SHOTLIST.md -> FACTCHECK.md/PROMPTS.md -> make_sheet.py -> Kokoro audio (BOPEN narration included; pad BOUT 1.0s tail; durations are the clock) -> stills contact sheet LOOKED AT -> `./brutalist.art/art run <reel> --height 2160` -> fix -> `./brutalist.art/art final <reel> --height 2160 --out <reel>/exports/landscape` -> python3 brutalist.art/runtime/scripts/bookend_check.py <reel> (PASS). Check the master: 3840x2160, runtime = sum of audio, silent tail. Also write the YouTube description draft as <slug>-youtube.md in the reel folder like the siblings (series line, chapters, Your Turn, sources, disclosure) but DO NOT stage it.
Disk is tight on this machine: check free space (df -h /) before big renders and say so if under ~15 GB.

FINAL REPORT (to the parent, concise): absolute paths of the master, runtime, beat count, lane histogram, gate results (F, A, B, V, T, bookend, PROOF), any HOLD/slate, any mispronunciation or failed gate, and anything you could not do. Report every file by absolute path. Do not claim anything you did not verify by looking at frames.

---

## To rebuild this exact film from what is in the folder

```bash
R=hpc-aicr/youtube/claude-liam-lecture-logging-into-aicr-with-claude
python3 $R/make_sheet.py                                            # the sheet (keeps measured audio)
python3 brutalist.art/runtime/scripts/generate_audio_kokoro.py $R   # only if narration changed (use --only <BID>)
python3 $R/pad_audio.py && python3 $R/make_sheet.py                 # BIDEA +0.8 s, BVDT +0.5 s, BOUT +1.0 s tail
python3 $R/assemble_scenes.py                                       # scenes.py = _kit_header.py + _scenes_*.py
./brutalist.art/art run   $R --height 2160
./brutalist.art/art final $R --height 2160 --out $R/exports/landscape
python3 brutalist.art/runtime/scripts/bookend_check.py $R
```

Skill doctrine: `brutalist.art/skills/make/lecture/SKILL.md`. Never stage or publish without Bear's word.

---

## Status at hand-off (2026-10-11)

Built end to end: the master is `<books>/../build/exports/landscape/claude-liam-lecture-logging-into-aicr-with-claude.mp4` (518.9 s, 44 beats, all machine gates PASS; see BUILD-LOG.md). Not staged, not published. Do not re-run `make_sheet.py` after `art final` (it wipes the build stamps); if a beat must change, edit only that unit, move its clip to `_superseded/`, re-run `art run`, then `art final`.

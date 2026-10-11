# ACTS — Requesting Access to Explorer (lecture)

**What this is.** The coverage map for the lecture film of `<books>/../source/README.md`, written before any beat.
**Why.** A lecture covers the WHOLE source; every section lands in an act or is listed under LEFT OUT with a reason.
**Found.** All seven README sections are covered in five acts, 23 body beats. One section (Sources) is not narrated. Estimated runtime about 7 min 20 s (an output, not a target). Updated 2026-10-11 for Bear's real-login facts (UserID worked, host-key question, no Duo on SSH) for the Managing /projects app and the two-hour delay, for the real Northeastern sign-in capture (B30, new), and for Bear's rule that unconfirmed steps may be said only as hedged guesses (B36, new).

| README section | Act | Beats |
|---|---|---|
| Header: what this is, why it matters, what was found | BIDEA, BOPEN | (framing: a login is not enough; a sponsor is needed) |
| 1. The rule that decides everything (sponsor-owned storage space, 35 TB free, sponsor requests one first, classroom form separate) | I · The Rule | B10 B11 (classroom form: LEFT OUT, see below) |
| 2. The people involved (PI, delegate, member, guest; recommend a delegate) | I · The Rule, II | B12 (roles); B20 (delegate recommendation) |
| 3. Route A: your sponsor adds you: the Managing /projects Open OnDemand app (Files, group drop-down, usernames comma-separated no spaces, Launch, output log, no ticket); the `project ... add members` command (`short` partition + `srun`, comma list, `view members`); the up-to-2-hours delay and the fresh login session; NOT CONFIRMED for brand-new users | II · Two Routes In | B20 B21 B22 B23 B24 |
| 4. Route B: the form (link, sign-in, Requester Information, six fields, "Please choose one", two paragraphs, NOT CONFIRMED below that) | III · The Form | B30 B31 B32 B33 B34 B35 B36 |
| 5. After you are in: username (s.caplins example; UserID worked for one user; try the form's UserID first), ssh door (host-key question, password, no echo, no Duo seen), OnDemand door (password + Duo), `whoami`, `groups`, home and scratch | IV · After Approval | B40 B41 B42 B43 B44 |
| 6. If something is wrong (the four-row table) | V · If It Fails | B50 (row 1) B51 (row 2) B52 (rows 3 and 4) |
| 7. Sources | not narrated | SOURCES.md, description "Sources" |

## LEFT OUT

- **Classroom use** (README section 1, one sentence: classroom use goes through a separate instructor form). The audience is a research-group member; a classroom aside would need its own form and its own facts. Decision, not omission.
- **The `s.caplins` / email-address observation** is used only as "the training's example" (B40); no rule is stated from it.
- **"If a project is missing from the drop-down, contact rchelp@northeastern.edu"** (README section 3): compressed into B24's address, which is the same contact.
- **Everything below the form's first screen** (README: NOT CONFIRMED). Not described; B35 says so.
- **The welcome banner text** after SSH login. The README confirms a banner exists; its text is not narrated or drawn (B41 shows only the two real prompt lines).

## Order

The source's order is kept. One addition: the delegate recommendation (README section 2, last line) is spoken in B20 where route A first appears, because that is where it matters.

## Cast (one cast, whole film; the same object is the same picture)

| Object | Picture | Beats |
|---|---|---|
| You | a Professor Bear portrait, seed `req-you` (PROFESSOR BEAR LAW) | B10 B20 B24 B50 B51 |
| Sponsor / PI | a Professor Bear portrait, seed `req-sponsor` | B10 B11 B20 B24 B36 B51 B52 |
| Delegate | a Professor Bear portrait, seed `req-delegate` | B20 |
| Storage space | the tall white cabinet from the AICR cast, labelled `/projects`; a dashed copy when it does not exist | B10 B11 B20 B51 B52 |
| Gate | two ink posts and a kraft panel that slides down when access is granted | B10 B50 |
| Command | the small kraft box with one terracotta tape, labelled "add" | B24 B51 B52 |
| Form page | a white page, ghost lines, one terracotta dot | B11 B20 B36 B50 B52 |
| Home / scratch | the closed kraft box and the open kraft bin from the AICR cast | B44 |

Act III opens on the real sign-in page (B30), then is one picture for five beats: the form's first screen (`AccessFormCard`, B31-B35), and ends on a hedged drawing (B36). The sign-in step (README 4, "What the sign-in does") is B30; the observed fact that signing in pre-fills the form is in B30 and B31; "what happens after you submit" is NOT in the README as fact and is spoken only as a hedge (B36). Act II's app beat (B21) is a labelled sketch of the announced controls, not a drawing of the real screen. Act IV is terminals, the real OnDemand dashboard, and the two path drawings.

## BIDEA correction and BDEFS terms

- BIDEA: the newcomer's "I just need to fill in a form" is corrected to "I need my sponsor". Trigger `just need to fill in a form`; replacement `need my sponsor`.
- BDEFS (six, all 17 characters or fewer): PI, Sponsor, Storage space, Delegate, Member, Duo. "Login node" was considered and dropped: the source never defines it, and a term the source does not define would be an invented fact.

## Self-contained check

The source leans on nothing outside itself except Explorer, which BIDEA and B10 treat as "the cluster you want to get onto". The film never says "the README", "this guide", "the training" as a thing the viewer has seen (B40 says "the training's example" once, naming the slides as the source of the sample name), and names no chapter. Roles, `project` command, `srun` and the short partition are each explained in the beat that first uses them. AICR appears only in BOPEN (the series name).

# SHOTLIST — Requesting Access to Explorer (lecture)

**What this is.** One row per body beat: what the sentence is about, the lane picked, the runner-up, and why the pick wins (BEST-BEAT LAW). Library asked per beat with `./brutalist.art/art scenes` / `--check` (2026-10-11).
**Result.** 23 body beats: 8 isometric or cast drawings, 5 Manim diagrams (ladder, two routes, app sketch, clock, names), 3 real terminals (no output shown), 2 real web captures (sign-in page, OnDemand dashboard), 5 beats on one built card (the form's first screen). No text-only cards in the body.

| Beat | About | Lane picked | Runner-up | Why this one wins |
|---|---|---|---|---|
| B10 | a login alone does not open the gate; a sponsor-owned space does | cast drawing: You at a gate, Login card turned back, sponsor and storage appear, Member chip travels, gate opens | `FormACard` with the rule as a line | the claim is an arrangement (you, gate, owner, storage); the card that bounces off the gate IS "alone is not enough" |
| B11 | the space is a folder under /projects, 35 TB free, sponsor requests one first | cast drawing: cabinet, filling bar, dashed outline, request page lands | ShowTellCard `dashboard` for 35 TB | one object changes state (missing, requested, there); the dashed-to-solid cabinet shows "request one first" |
| B12 | four roles and what each can do | Manim ladder, four rungs landing on the names | `LibraryIconRow` (max four icons, but people are portraits and rights are not marks) | a ladder has the shape of the claim (who may add whom); strike on "can't write" is the one motion |
| B20 | two routes in; delegate keeps route A moving | Manim fork diagram with portraits; a dot flows along A without the PI | two-column card | the claim is two paths to one place; drawing both paths draws it |
| B21 | route A without a terminal: the Managing /projects app | **rung 3 sketch** (Manim): window with only the announced labels: Files > Managing /projects, Group drop-down, Usernames (comma-separated, no spaces), Launch, Output log; controls land as named | `ShowTellCard` interface kind | the announcement states the controls but not their look, so nothing beyond labels is drawn and the card is captioned "Sketch of the announced controls"; Bear can replace it with a real capture |
| B22 | the command way: srun, add, comma list, view members | **real commands**, `CCPlainShell`, no output shown (none was run) | iso command box | they are things the viewer types; the no-spaces rule is only visible in the literal text; README's own `mylab`/`rot1,rot2,rot3` example |
| B23 | up to 2 hours; start a fresh session | Manim: clock hand sweeps a full turn to "up to 2 hours"; old session ghosted, new session checked | stat card "2 h" | a delay is a duration; the sweep is the duration, and the swap shows what to do |
| B24 | caveat: a brand-new user is not confirmed (either way) | cast drawing: command box stops short of You, a "?" lands, address lands | text card | "not confirmed" as a box that stops short is the motion; no claim is drawn that either way works or fails |
| B30 | route B starts at the university sign-in; signing in identifies you | **the real sign-in page** (`BrowserCapture` on Bear's capture): camera pushes in to the sign-in box, one ring; nothing typed | the built card of the form opening | SHOW-THE-THING rung 1; a human-only sign-in, never typed by the film |
| B31 | the six fields of the first screen, pre-filled from the sign-in | **built card** `AccessFormCard`; the link shows under the page; each field lights as named; ring on UserID | `FormBCard` table of fields | SHOW-THE-THING rung 3 (below): the viewer will see this exact layout; lighting each field teaches where to look |
| B32 | "Please choose one", option 1 | same card; the first radio fills | two-column card | the viewer must recognise the control; the dot filling is the claim |
| B33 | option 2 and which to pick | same card; the second radio fills, the first empties | same | same |
| B34 | the two instruction paragraphs | same card; camera moves to the paragraph, highlighter sweeps the sentence "sponsor-owned storage space", then "its owner can add members" | quote card | the film's rule is a sentence on the real form; the sweep is the zoom on its sentence |
| B35 | the form continues; not described | same card; page fades, "The form continues" and a chevron | slate | the honest edge: nothing is drawn below what is confirmed |
| B36 | after you submit: HEDGED ("we think") | cast drawing: the form page goes to the sponsor; Approve / Deny chips, the on-screen label "We think this is how it works", a "?", the address | text card | Bear's rule: an unconfirmed step may be said only as a guess, spoken and on screen, with a pointer to Research Computing; the label is the hedge |
| B40 | which name to log in with | Manim chips: example, UserID (try first), email prefix, funnel into First login | text card | order of attempts is the claim; chips in order show it, and no rule is drawn |
| B41 | the terminal door | **real prompts**, `CCPlainShell`: the ssh line, the real host-key question, `password:`; no banner, no Duo | iso door | real strings from the verified login; unseen output is not shown |
| B42 | the browser door | **the real dashboard** (`BrowserCapture` on the training's own screenshot) | drawn browser window | SHOW-THE-THING rung 1 (a capture the training published); camera pushes in on "dashboard" |
| B43 | whoami, groups | **real commands**, `CCPlainShell`, no output shown | cast drawing of a group list | the viewer types these; output depends on the viewer |
| B44 | home and scratch paths | cast drawing: closed box and open bin with path labels | table | cast pays off from the AICR films (same box, same bin) |
| B50 | rejected: no account, wrong username, change of password | cast drawing: gate with a cross, tags land, form ringed at its field, email prefix, wait a while | table row | row 1 of the README table as a situation at the gate |
| B51 | in, but not in the project | cast drawing: a check, the `groups` list with an empty slot, the add command fills it | table row | the slot filling is the fix |
| B52 | the sponsor with no space; anything else | cast drawing: add bounces off a dashed cabinet; request lands; address | table row | echo of B11 on purpose: the same object, now as a failure |

## Tool beats and their SHOW-THE-THING rung

| Beat | Tool | Rung | Evidence |
|---|---|---|---|
| B30 | Northeastern sign-in page | 1, real capture | Bear's capture 2026-10-11, `captures/northeastern-sign-in.png` (no personal data); the address shown is the form link (the destination), not claimed as the page's own URL |
| B31-B35 | the ServiceNow access form | **3, a card built for it** | the form is behind university sign-in and was not captured; the card reproduces ONLY the layout and labels confirmed on 2026-10-11 (README section 4, the coordinator's description of the look) and draws nothing below them |
| B21 | Open OnDemand app Managing /projects | **3, a card built for it** | the announcement (rc.northeastern.edu, 2026-08-25) states labels only; no real capture; sketch uses neutral palette and invents no layout beyond those labels |
| B42 | Open OnDemand dashboard | 1, real capture | the training's own screenshot, `captures/screenshot_OOD.png` (public copy in `runtime/remotion/public/lecture-explorer-ood/`) |
| B22 B43 | Slurm/project/Linux commands | real commands, no output shown | README sections 3 and 5 |
| B41 | ssh to Explorer | real prompt lines from Bear's real login, 2026-10-11 | README section 5; the `password:` and host-key lines are verbatim; the banner is not shown |

## What must be built or captured (all done in the layout stage unless listed)

- Built: `AccessFormCard` (Remotion, in `new-components/`, NOT yet registered: first task of BUILD-PROMPT.md).
- Built: ten Manim scenes in `scenes.py`.
- Captured: nothing new in this film. The OnDemand screenshot is reused from the sibling film; the sign-in capture is Bear's (copied to `captures/`; the build copies it into `runtime/remotion/public/lecture-requesting-access/`).

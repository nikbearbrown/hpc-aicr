# FACTCHECK — Requesting Access to Explorer (lecture)

**What this is.** Every factual claim in the narration and on screen, checked. **Sources.** R = `<books>/hpc-aicr/Requesting-Access-to-Explorer/README.md` (sections as cited, updated 2026-10-11); S = Research Computing "Intro to Explorer and OOD" slides (`hpc-aicr/Intro-to-Explorer-OOD-2026/Intro_explorer_ood.md`); D = rc-docs pages cited in R; A = the RC announcement (https://rc.northeastern.edu/2026/08/25/managing-projects-through-open-ondemand-ood/, as summarised in R section 3); F = Bear's first-screen screenshot of the access form (2026-10-11) as summarised in R section 4; L = Bear's real login, 2026-10-11 (R section 5). **Result.** 43 claims: 39 PASS, 2 SOFTENED to fit what is confirmed, 1 HEDGED (B36, Bear's rule: said as a guess, on screen and aloud), 0 asserted that R marks NOT CONFIRMED. Checked 2026-10-11 (layout stage; audio not yet made). Not re-fetched from the live sources in this stage: A, D and F are taken from R.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | BIDEA B10 | A Northeastern login alone does not get you onto Explorer; every user must belong to a sponsor-owned storage space | PASS | R 1; S "How to get an account" | |
| 2 | B10 B11 | The sponsor is a PI or a staff member | PASS | R 1, S | |
| 3 | B11 | The space is a directory under /projects | PASS | R 1 | |
| 4 | B11 | Free for research groups up to 35 TB | PASS | R 1, S | "up to thirty-five terabytes" |
| 5 | B11 B52 | A sponsor with no space requests one first | PASS | R 1, 6; S | |
| 6 | B12 | PI owns the project; can add members, guests and delegates | PASS | R 2 (rc-docs Terminology) | |
| 7 | B12 | A delegate can add members | PASS | R 2 | |
| 8 | B12 | A member reads, writes and runs | PASS | R 2 | |
| 9 | B12 | A guest reads and runs, cannot write | PASS | R 2 | |
| 10 | B20 | Research Computing recommends every PI name at least one delegate | PASS | R 2 | "recommends every PI name a delegate" |
| 11 | B20 | Two routes: sponsor/delegate adds you, or you submit the access form | PASS | R header | |
| 12 | B21 | Open OnDemand app "Managing /projects", under Files | PASS | R 3, A | |
| 13 | B21 | The sponsor picks the group, types usernames comma-separated with no spaces, clicks Launch | PASS | R 3, A | |
| 14 | B21 | A log shows what changed | PASS | R 3 (output log shows who was in the group and what changed) | |
| 15 | B21 | Screen: labels Files > Managing /projects, Group, Usernames, Launch, Output log | PASS | R 3, A; no colours or layout beyond these labels are claimed; the card is captioned "Sketch of the announced controls" | Bear can replace with a real capture (BUILD-LOG) |
| 16 | B21 | The "user1,user2" text in the box | PASS (placeholder) | a placeholder of the stated format, not from a real run | |
| 17 | B22 | The command runs on a node in the short partition, reached with `srun -p short --constraint=ib --pty bash` | PASS | R 3, D | |
| 18 | B22 | `project <project_name> add members <username>`; comma list with no spaces; `view members` | PASS | R 3, D "Group Management Commands" | |
| 19 | B22 | Screen shows no output | PASS | none was run; nothing shown | |
| 20 | B23 | Changes can take up to two hours to reach the whole cluster | PASS | R 3, A | |
| 21 | B23 | A newly added user may need a fresh login session; groups are read at login | PASS | R 3, A | narration says "start a fresh login session ... because your groups are read when you log in" (R: "may need"); stated as advice, not as a certainty about every case |
| 22 | B24 | Whether either way works for someone with no Explorer account is not confirmed | PASS | R 3 (NOT CONFIRMED) | stated as "not confirmed" |
| 23 | B24 B52 | rchelp@northeastern.edu | PASS | R 3, 6 | spoken "r c help at northeastern dot e d u" |
| 24 | B30 | The form is reached at bit.ly/NURC-AccessRequest and starts at the Northeastern sign-in | PASS | R 4, S | "tech service portal" is no longer spoken; the link is spoken and shown |
| 24a | B30 | Screen: Bear's real sign-in page ("Sign in", box "Email or Username@northeastern.edu", Next, "Sign-in options") | PASS | R 4 "What the sign-in does", `captures/northeastern-sign-in.png` (no personal data) | address bar shows the form link (the destination), caption "Northeastern sign-in, captured 2026-10-11"; the film does not claim it is the page's own URL; nothing is typed, the sign-in is the viewer's |
| 24b | B30 B31 | Signing in is what identifies you; Requester, Email, UserID, Department arrive pre-filled | PASS (observed) | R 4 (observed 2026-10-11) | |
| 25 | B31 | First screen headed "Requester Information", pre-filled from your university record | PASS | R 4, F | |
| 26 | B31 | Fields: Requester (Last, First), Phone (blank), Email, Location (drop-down), UserID, Department (drop-down) | PASS | R 4, F | |
| 27 | B31 | Values on screen are placeholders | PASS | "Last, First", "you@northeastern.edu", "your campus", "your user ID", "your department"; the card is captioned "Placeholder values; your own details fill these"; no real name, email, ID or phone anywhere | |
| 28 | B32 B33 | "Please choose one" (required); the two exact options | PASS | R 4, F | on-screen text is verbatim; narration reads "(HPC)" as H P C |
| 29 | B33 | Pick the first if new here, the second if already in and changing sponsor | PASS | follows the options' own words | |
| 30 | B34 | Two paragraphs: all users must belong to a sponsor-owned storage space, a sponsor with none can request one; if a space exists its owner can add members themselves, following the documentation | SOFTENED | R 4 gives the SUBSTANCE only ("in the form's own words in substance") | on-screen wording is the build's phrasing of that substance; BUILD-LOG asks Bear to check it against his screenshot before publishing |
| 31 | B35 | Nothing is said or drawn about anything below the first screen | PASS | R 4 (NOT CONFIRMED) | the card fades; "I haven't seen the rest" |
| 32 | B31-B35 | Look: white page, grey inputs, white top bar "Technology" in bold black (verified against Bear's screenshot, 2026-10-11), left menu of seven items | SOFTENED | the look and menu items were checked against Bear's screenshot (white top bar, grey boxed menu items, five with a plus) after the layout agent wrote this row; not from R | exact colours and spacing are approximations; the swap list in BUILD-LOG replaces them with a recording |
| 33 | B40 | The training's example name is s.caplins | PASS | R 5, S | |
| 34 | B40 | In one real login the UserID from the form worked, not the email prefix; try the UserID first | PASS | R 5 (L) | stated as "in the one real login checked"; no universal rule; real value never shown |
| 35 | B41 | ssh to login.explorer.northeastern.edu asks the host-key question once (type yes), then the Northeastern password, nothing shows as you type; no Duo prompt appeared | PASS | R 5 (L) | "In the one login checked, no Duo prompt appeared" |
| 36 | B41 | Screen: the ssh line, `Are you sure you want to continue connecting (yes/no/[fingerprint])? yes`, `password:` | PASS | R 5 (L); banner and anything after login not shown | the `yes` is what was typed |
| 37 | B42 | OnDemand at ood.explorer.northeastern.edu: username and password plus Duo; the dashboard | PASS | R 5, S "Logging in via OOD" | screen is the training's own screenshot; "after sign-in" in the caption |
| 38 | B43 B44 | whoami prints your login name; groups lists your sponsor's project group; /home/<username>, /scratch/<username> | PASS | R 5 | |
| 39 | B50 | Rejected: no account yet, wrong username, or a password changed minutes ago (wait a while); try the form's UserID then the email prefix; submit the form if sure | PASS | R 6 | |
| 40 | B51 | Logged in but groups does not list the project: sponsor has not added you; ask the PI or a delegate to run the add command | PASS | R 6 | |
| 42 | B36 | After you submit, your sponsor is asked to approve it | **HEDGED** | not in R (NOT CONFIRMED: approval step); Bear's rule 2026-10-11 allows "we think this is how it works" | said aloud ("We think ... That's our guess, not a confirmed step, and we don't know how long it takes. Confirm with Research Computing") and on screen (label "We think this is how it works"); no timing claim; the Approve/Deny chips are drawn tentative (grey), with a "?" |
| 41 | BVDT BHTF | Recap lines and the prompt assert nothing beyond the above | PASS | | |

**Strip-the-datable.** No dates, versions or counts on screen or in narration except "up to two hours", "thirty-five terabytes" (both sourced). The announcement date is not spoken. "Duo" is not claimed to be present or absent for SSH beyond the one login.
**Never in the film.** Bear's real name, UserID value, email, phone, or the host `explorer-01`.

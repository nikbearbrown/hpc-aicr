# SHOTLIST — best visual per beat

**What this is.** One row per body beat: what the sentence is about, the lane picked, the runner-up that was auditioned, and why the pick wins. **Result.** 20 Manim beats, 26 terminal beats on `CCPlainShell` (the real text of the source, or a recorded run), 6 bookends. Lane counts are information, not a quota. Library asked first (`./art scenes "terminal"`, `"timeline"`): `CCPlainShell` is the registered plain-terminal skin; no registered component draws a commit chain, so those are Manim (a miss, built, not slated).

| beat | about | lane picked | runner-up | why this one wins |
|---|---|---|---|---|
| B10 | the folder of file names that cannot answer a reviewer | Manim drawing (portrait + pile of the source's real names) | isometric folder stack | the names ARE the evidence; a pile building up is the claim |
| B11 | one script and a timeline replacing the pile | Manim (timeline with date/author/message chips) | ShowTellCard `compare` | the pile shrinking into a timeline is the motion |
| B12 | a commit is a full snapshot linked to its parent | Manim (disc chain with hashes) | isometric stack of pages | parent arrows are the claim; discs read at a glance |
| B13 | branch and tag as names for commits | Manim (same chain, label forks, flag) | node diagram in Remotion | same cast as B12, so the viewer sees names added to the same chain |
| B14 | working tree, staging area, repository | Manim (three boxes, a page travels) | isometric conveyor | the page moving on the word `git add` is the claim |
| B15 | four research moments and the Git answer | Manim (four rows, GitHub logo) | LibraryIconRow | rows pair situation with command; Logo Law for GitHub |
| B20 | the example: table, filter, summary | Manim (table through a funnel) | terminal head of the data file | the data file is empty in the repo and BSD awk numbers differ; column names and the funnel carry the idea |
| B21 | the script's parameter block and calls | terminal, source lines | ClaudeCodeBeat listing | a plain file shown as written; ring on `MIN_COUNT` |
| B22 | `git init` and the master/main hint | terminal, recorded | Manim | the hint text is real output |
| B30 | track code, not results; what to skip | Manim (code to repo, data to storage, tokens crossed out) | library icons | three destinations need motion |
| B31 | the source's `.gitignore` | terminal, source lines | ClaudeCodeBeat | verbatim file; rings on the three lines that matter |
| B32 | the add that Git refuses | terminal, recorded | Manim error plaque | the refusal is real output; check-ignore names the line |
| B33 | the fix, `results/*` | terminal, recorded | split-screen diff | recorded success is the proof |
| B34 | comments after patterns break them | terminal, recorded | Manim | recorded refusal again with a trailing-comment file |
| B35 | the README commands and parameters | terminal, source lines | a drawn README page | commands read as written |
| B40 | run, inspect, commit loop | Manim (ring with a rider dot) | Remotion flow | a loop needs a lap; tag lands after |
| B41 | status, add, commit, log | terminal, recorded | Manim | the real first commit |
| B42 | run, and the Mac `date` failure | terminal, recorded | Manim | the empty brackets and the error ARE the finding |
| B43 | commit the run; its log names the commit before | terminal, recorded | Manim | real hashes |
| B44 | atomic commits and message types | Manim (crossed-out message, six type chips) | terminal `git log` | the "and" test is a visual strike-through |
| B45 | `git diff`; the Mac `sed` form | terminal, recorded | Manim | one line out, one in, in real diff text |
| B46 | rerun at 20; second commit | terminal, recorded | bar chart of 199 vs 197 | the commit and log are the point |
| B47 | the audit trail: stat, grep | terminal, recorded (selected lines) | Manim | the grep answer is two real lines |
| B50 | a branch leaves main untouched | Manim (chain forks) | terminal only | main staying put is the claim |
| B51 | switch -c, list, the two cutoffs, diff | terminal, recorded | Manim | real branch list and diff |
| B52 | commit on branch, back on main | terminal, recorded | Manim | the grep on main showing 2.0 is the proof |
| B53 | merge --no-ff and the graph | terminal, recorded | Manim | the real ASCII graph rejoins |
| B60 | a tag does not move | Manim (flag stays, main slides) | terminal | fixed vs sliding is motion |
| B61 | tag command, list, pushes not run | terminal, recorded + source | Manim | tag message is real; pushes shown without output |
| B62 | restore one file, rerun | terminal, recorded | Manim | 199 vs 197 from real runs |
| B63 | results left modified | terminal, recorded | Manim | real `status --short` |
| B70 | commit before submit; hash in the log | Manim (timeline with a thread) | node diagram | the thread from commit to log line is the claim |
| B71 | the source's job script header | terminal, source lines | ClaudeCodeBeat | text as written; rings on `compute` and the mail line |
| B72 | real partitions | Manim (two racks with plaques) | table card | racks from the cast; `compute` crossed out |
| B73 | header, guard, tag inside the job | terminal, source lines | Manim | text as written; not run |
| B74 | the guard block run on its own | terminal, recorded | Manim | real exit codes 1 and 0 |
| B75 | guard runs at job start, not submit | Manim (timeline; edit during queue) | terminal | a sequence in time; stamped "not tested" |
| B76 | the stronger submit-time check | terminal, ours (labelled) | Manim | two lines of text; untested |
| B77 | three more weak spots | Manim (three cards) | terminal | three arrangements, one card each |
| B78 | the full job record | Manim (12-chip grid, first three ringed) | table | grid shows how little the header covers |
| B80 | aliases and the decorated graph | terminal, source + recorded | Manim | the labels HEAD/tag in real output |
| B81 | branch in the prompt | terminal, source + recorded | Manim | the function and its output |
| B82 | text charts | terminal, recorded | Remotion chart | the charts ARE plain text |
| B83 | large files and notebooks | Manim (manifest + storage; notebook stripped) | two cards | two ideas, two drawings; mono chips for LFS/DVC/nbstripout (no logos exist) |
| B84 | amend, revert, reset --hard | Manim (chain edits) | terminal | three outcomes on one chain |
| B85 | conflicts and stash | Manim (marker page; drawer) | terminal | markers wiping away is the motion; not run |

Tool beats (SHOW-THE-THING): the terminal is the tool in 26 beats: rung 1 (real command output, recorded) or the source's text as written. No Claude Code session appears, so no `SESSION.md`. GitHub and Git and Jupyter appear as logos (Logo Law); Slurm, LFS, DVC, nbstripout have no logo and appear as mono chips.

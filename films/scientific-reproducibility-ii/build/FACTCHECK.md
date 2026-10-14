# FACTCHECK (Gate F)

**What this is.** Every number and named claim in the narration and on screen, against the source and, where cheap, the primary. **Result.** All rows below pass or carry a fix; nothing that will date the film is spoken (session date, presenter, tool version numbers are kept off the narration; "Apple Git" is not named on screen).

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B10 | Folder names filter.sh ... results_for_paper_FINAL/ | ok | source, "The Scenario" | spoken as "a folder like this" |
| 2 | B11 | A commit carries date, author, message; tag a figure's code; branches; undo | ok | source "Without vs With" | |
| 3 | B12/B13 | Git stores snapshots, not edits; commit links to its parent; branch is movable; tag fixed | ok | source "Git Mental Model"; Pro Git | hashes a3f8c21, b7d2e14, d9c1f37 are the source's illustration; e5a0b99 from our guide's diagram; drawn as illustration |
| 4 | B14 | working tree / staging area / repository; add and commit move files | ok | our guide Part 1; Pro Git | |
| 5 | B15 | four research scenarios | ok | source "Research Scenarios" | the source's "citable DOI" is not claimed |
| 6 | B20 | RNA-seq counts, three control, three treated, 200 genes | ok | source section 1 (`for i = 1; i <= 200`) | numbers on screen are column names only |
| 7 | B21 | strict mode, `MIN_COUNT=10`, UP at fc >= 2.0, DOWN at fc <= 0.5 | ok | source section 2 | read by `sl()` |
| 8 | B22 | `git init` may name the first branch `master` and the later steps say `main` | ok, recorded | `captures/session/cell12.out` (hint printed); source cells 33, 35 use `git switch main` | "depending on your settings"; not claimed for Explorer |
| 9 | B31 | the source's `.gitignore` | ok | source section 4 | read by `sl()` |
| 10 | B32 | a file under an ignored directory cannot be re-included; add refused; check-ignore names line 2 | ok, recorded | `captures/trap.out`; git-scm.com/docs/gitignore | |
| 11 | B33 | `results/*` lets the `!` lines work | ok, recorded | `captures/fixed.out` | |
| 12 | B34 | a comment after a pattern is part of the pattern; add still refused | ok, recorded | `captures/trailing.out`; gitignore docs: lines starting with `#` are comments, no inline comments | not in our guide: new finding from this run |
| 13 | B35 | README commands and the parameters table | ok | source section 5 | |
| 14 | B41 | status / add / commit; source stages with `git add .` | ok, recorded | `session/cell18.out` | advice to name files: HPC.md Section 9 |
| 15 | B42 | 200 genes, 199 kept at 10; `date --iso-8601` fails on a Mac (empty brackets); "should work on Linux, not run on a cluster" | ok, recorded for the Mac | `session/cell20.out`; HPC.md Section 12 | counts are BSD awk's data, not the presenter's; film does not claim they match the presenter's |
| 16 | B43 | the run's log names the previous commit | ok, recorded | `session/cell20.out` (Git commit 48350fb... recorded in the commit eda7c83) | |
| 17 | B44 | atomic commits; message types feat, fix, data, analysis, docs, config | ok | source 7.1, 7.2 | the source also lists refactor and perf; six shown |
| 18 | B45 | plain `sed -i 's/a/b/'` fails on a Mac; `sed -i ''` works | ok, recorded | `captures/sed.out`; HPC.md Section 12 | |
| 19 | B46 | 197 kept at 20, two fewer | ok, recorded | `session/cell26.out`, `cell28.out` (summary.tsv 2 deletions) | |
| 20 | B47 | stat, grep; `git log -p` and `git blame` | ok; -p and blame only read | source Quick Commands | said "not run" on screen |
| 21 | B51/B52 | switch -c, branch --list, FC cutoffs 1.5 and 0.67, main still 2.0 | ok, recorded | `cell30` to `cell33` | |
| 22 | B53 | `--no-ff` keeps a merge point; `-d` deletes only merged branches | ok, recorded for `-d` on a merged branch | `cell35`; our guide Part 8; git-branch docs | the "only if merged" is Git's documented rule, not demonstrated on an unmerged branch |
| 23 | B61 | tags need their own push; push changes something outside your machine | ok | source section 12; HPC.md Section 9 ("push the tag explicitly, with the researcher's yes") | pushes not run, said on screen and aloud |
| 24 | B62 | 199 kept at ten vs 197 at twenty; restore one file with checkout | ok, recorded | `cell40.out`, `cell26.out` | |
| 25 | B63 | the rerun leaves tracked results modified | ok, recorded | `session/status-after-timetravel.out` | the command `git status --short` is ours |
| 26 | B70 | commit before submit; print the hash in the log | ok | source section 14; HPC.md Section 9 | |
| 27 | B71 | `--partition=compute` does not exist on Explorer | ok | HPC.md Section 12 | "mail line is a placeholder" (`your@university.edu`) |
| 28 | B72 | Explorer `short` (default, 2 days), `sharing` (1 hour); AICR `cpu` (default, 1 day) | ok | `guides/_real-outputs.md` (read-only `sinfo`) | the date of capture is not spoken |
| 29 | B73/B74 | guard block, header, tag; the guard exits with code 1 on a dirty tree | ok; guard run on its own only | `captures/guard.out` | nothing run as a Slurm job; said aloud |
| 30 | B75 | the guard runs at job start; a queued job may run newer code | our reading, not tested | our guide Part 10, weak spot 1 | stamped "not tested" on screen and aloud |
| 31 | B76 | submit-time check with `sbatch --export` | ours, untested | our guide Part 10 | labelled |
| 32 | B77 | results block the next submit; shared checkout; tag exists only there until pushed | our reading, not tested | our guide weak spots 2 to 4 | labelled |
| 33 | B78 | the twelve record items | ok | HPC.md Section 9 | |
| 34 | B80/B81 | aliases lg, st, last; branch in the prompt | ok | source section 15 | graph recorded with the long form (the alias itself was not run in a clean session) |
| 35 | B82 | awk-only charts run anywhere | ok, recorded on the Mac | `cell60`, `cell62` | |
| 36 | B83 | Git LFS up to about 2 GB; DVC; nbstripout and Jupytext via pip | read only | source "Common Questions" | said "we did not run" is NOT claimed for these; narration states them as the source's advice (see BUILD-LOG) |
| 37 | B84 | amend before push; revert for shared; never reset --hard on shared branches | read only | source Q&A; HPC.md Section 9 | |
| 38 | B85 | conflict markers; stash | read only | source Q&A; our guide Part 8 | "We did not run either" in the narration |

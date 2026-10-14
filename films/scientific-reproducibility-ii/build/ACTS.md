# ACTS — Scientific Reproducibility II: Version Control (lecture)

**What this is.** The coverage map for the lecture film of `hpc-aicr/Scientific-Reproducibility-II-2026/scientific-reproducibility-II.md` (Northeastern Research Computing's Git walkthrough), read with our written rewrite `guides/scientific-reproducibility-ii.md`. **Result.** Every section of the source is in one of eight acts or listed under LEFT OUT; 46 body beats. **Why.** A film must not quietly cover the first half.

| Source section | Act | Beats |
|---|---|---|
| Scenario (reviewer asks, six months on); Without vs With Version Control; Research scenarios; Git mental model | I | B10 B11 B12 B13 B15 |
| (our guide) the three places: working tree, staging area, repository | I | B14 |
| What this notebook covers; 0 Setup check; 1 The research data; 2 The analysis pipeline; 3 git init | II | B20 B21 B22 |
| 4 .gitignore; 5 README | III | B30 B31 B32 B33 B34 B35 |
| 6 First commit; 7 Run, inspect, commit (7.1 atomic commits, 7.2 conventional messages); 8 git diff; 9 git log | IV | B40 B41 B42 B43 B44 B45 B46 B47 |
| 10 Branches; 11 Merge | V | B50 B51 B52 B53 |
| 12 git tag; 13 Time travel | VI | B60 B61 B62 B63 |
| 14 Slurm; the guard; (our guide) partitions, four weak spots, the complete job record | VII | B70 B71 B72 B73 B74 B75 B76 B77 B78 |
| 15 Branch state in the terminal (aliases, prompt); 16 CLI charts branch; Quick commands; Common questions (large data, bad commit, notebooks, conflicts); `git stash` | VIII | B80 B81 B82 B83 B84 B85 |
| Exercises 1 to 3 | VIII (the Your Turn replaces them) | BHTF |

## LEFT OUT
- The presenter, the logo, the registration link and the session date: datable; credited in the description.
- Section 0's ssh, `srun` and Open OnDemand login steps: other films in the series teach logging in; this film starts at the repository.
- Section 1's `awk` data-generation script: its output is shown (B20 uses the column names only); the script is long and teaches nothing about Git.
- The README's project-tree listing and the Resources list (Pro Git, The Turing Way, DVC, Learn Git Branching, gitignore.io): reference lists; in the description.
- Exercises 1 to 3: each repeats a step already shown (edit and commit; branch and merge; restore an old file); the Your Turn gives the viewer their own task instead.
- The closing line "Next in the series: Containers & Singularity": a pointer to another session, and Explorer's tool is Apptainer.

## Order
The source's order, with one swap: the source teaches `git stash` only in a summary table and conflicts only in the questions; both are shown together in B85 (log the swap: they share a motion, setting work aside or resolving it).

## Cast per act
- I: file-name pile; the commit chain (discs with hashes a3f8c21, b7d2e14, d9c1f37, e5a0b99); the Git logo chip. One chain, same discs in B12, B13.
- V, VI, VIII: the same disc chain, with the branch label and the tag flag.
- VII: the timeline (commit disc, sbatch marker, queue bar, job start, output page); Explorer and AICR racks.

## Self-contained check
Defines repository, commit, branch, tag, the git ignore file and Slurm job up front (BDEFS) and the staging area at the moment it appears (B14). Never says "the guide", "the lesson", "the training", "the slides" or names another film. "Northeastern Research Computing" is named only on the title card as the series. The corrections (the `.gitignore` trap, the Mac date and sed forms, the partition) are shown with the viewer's own commands, not by naming a document. No video numbers; the "II" is part of the given title.

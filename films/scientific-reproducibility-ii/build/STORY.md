# STORY — Scientific Reproducibility II: Version Control

**What this is.** The story of the lecture film, in one page. **Result.** One film, about 15 minutes, eight acts. **Why.** So a researcher leaves able to tie every result, on a laptop or a cluster, to the exact code that made it.

**The correction up front (BIDEA).** Version control is not a backup folder; it is a searchable timeline of snapshots, each tied to the result it produced.

**The question that carries the film.** Six months after the paper, a reviewer asks what threshold you used. Act I shows the folder that cannot answer. The rest of the film builds the repository that can: init, ignore, commit the run, diff, branch, merge, tag, restore (Acts II to VI). Act VII carries the same discipline onto a cluster, where jobs run later, elsewhere, from files you may have edited. Act VIII is the daily kit and the questions people ask.

**What makes this film ours.** Every command is the source's. We ran those commands for real, on a Mac, in a throwaway folder (`captures/`), and the film shows what came back: including four things the source gets wrong or leaves silent: (1) the `.gitignore` re-include fails, (2) its comments after patterns break the pattern, (3) the first branch may be `master`, not `main`, and the later steps say `main`, (4) `date --iso-8601` and `sed -i 's/a/b/'` fail on a Mac. The Slurm script was NOT run on any cluster; the film says so, shows the guard block run on its own, and names the weak spots as our reading, untested.

**Tone.** Teardown register, Liam in for Bear: plain, specific, never claiming more than was run.

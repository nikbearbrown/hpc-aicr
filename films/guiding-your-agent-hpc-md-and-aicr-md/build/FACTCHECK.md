# FACTCHECK — Guiding Your Agent: HPC.md and AICR.md (lecture)

**What this is.** Every factual claim in the narration and on screen, checked against the two files and the session record. 2026-10-12. **Result.** PASS on every row; caveats in the Fix column.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B11 | Real examples of quiet failures: work on a login node; 8 hours requested for runs of 25 and 55 minutes; `01_gpu_verify.py` exits 0 when CUDA is missing | PASS | AICR.md section 4 (8 h for 25 and 55 min), section 1 (01_gpu_verify.py), HPC.md section 1 (login node) | labels on the cards are short forms of those lines |
| 2 | B12 | HPC.md is for any shared cluster, written for Northeastern's Explorer; AICR.md builds on it and adds what is different or stricter on AICR | PASS | first paragraph of each file | none |
| 3 | B13 | The one-line pointer for CLAUDE.md or AGENTS.md exists in each file | PASS | HPC.md and AICR.md 'How to use it' (read from the files at build time) | none |
| 4 | B20 | HPC.md opens with a summary (what it is, why, what we found, what is not verified), then 'Agent rules', 14 numbered sections (0 to 13), Appendix A (honest list) and Appendix B | PASS | heading list read from the file (`grep '^#'`) | narration says fourteen numbered sections, zero to thirteen |
| 5 | B21 | Section 0: the agent does pipeline work; the researcher keeps judgment; look before you act, measure before you change, ask before you spend, delete or change who can see data | PASS | HPC.md section 0 | none |
| 6 | B22 | Hard nevers: computation on a login node; asking for or printing a password or key; deleting without listing and a yes; submitting before confirmation; `scancel -u $USER`; inventing a flag, module or limit | PASS | HPC.md section 1 table | none |
| 7 | B23 | Every never has a because; some rules are labelled house rule | PASS | HPC.md section 1 (three rows shown), 'Rules marked (house rule)' in the header | none |
| 8 | B24 | If a read-only command can answer, run it instead of asking; ask only access, permission, data, what and why, address, agent access | PASS | HPC.md section 2 | narration lists four of the six questions |
| 9 | B25 | Benchmark: 1 core 250.7 s; 2 116.8; 4 58.1; 8 29.4; 12 33.4; 16 25.2; 20 20.2; 12 slower than 8 | PASS | HPC.md section 4 (Research Computing's own benchmark, Game of Life 10000x10000, 500 iterations) | none |
| 10 | B26 | Every script states partition, time, memory, cpus, name, output; time = expected runtime + about 20%; `--mem` is CPU RAM | PASS | HPC.md section 5 | none |
| 11 | B27 | Never trust the allocation; verify the GPU (name, memory, count, tensor round trip) | PASS | HPC.md section 6 | none |
| 12 | B28 | Home for code and environments; scratch purged on the first Tuesday of every month; projects for long-term; never keep the only copy in scratch | PASS | HPC.md sections 1 and 7 | none |
| 13 | B29 | Install order: module, conda, container built on your own machine, source build, Spack or EasyBuild last | PASS | HPC.md section 8 | none |
| 14 | B30 | Twelve-item minimum record for every job | PASS | HPC.md section 9 (items 1 to 12; five shown) | none |
| 15 | B31 | The researcher creates and unlocks the key; on a prompt, hang or permission denied the agent stops and reports | PASS | HPC.md section 10 | none |
| 16 | B32 | Slide errors: a comment after a continuation backslash, `--partition=compute`, a sample sbatch without time and memory | PASS | HPC.md section 12 | none |
| 17 | B33 | Scratch quota: 50 TB in slides, 20 TB on the policy page; labels house rule and inferred | PASS | HPC.md Appendix A item 1; header | none |
| 18 | B40 | AICR.md wins where the two differ; assume AICR is not Explorer | PASS | AICR.md header 'Precedence', section 0 | none |
| 19 | B41 | AICR differs: user name built differently; no password (key plus certificate); partition picks the GPU; idle GPUs cancelled; scratch purged after 30 days; no off-site backup | PASS | AICR.md header item 1 and section 2 | none |
| 20 | B42 | `ssh-add -D` empties every key; `source activate` died in a real job; `01_gpu_verify.py` exits 0 without CUDA | PASS | AICR.md section 1 rows (read from the file) | none |
| 21 | B43 | Template built from flags real completed jobs used; PATH prepend not activate; hard-fail CUDA line | PASS | AICR.md section 5 | none |
| 22 | B44 | jobstats exists only on AICR; real example 8 h limit, 55 min, GPU utilisation 80%; targets over 70% and below 50% | PASS | AICR.md section 6 and section 2 | none |
| 23 | B45 | Quiet lessons: weights loaded with no error; a silent clip (peak 4 of 32767); a cached file under the same path | PASS | AICR.md section 11 items 1 to 3 | none |
| 24 | B46 | The questions asked before a GPU job: username and account; restricted data; submit myself; what success looks like | PASS | AICR.md section 12 | none |
| 25 | B50 | Listing /projects showed other people's names; a disk-usage command over a shared folder hung; both are now a hard never | PASS | Explorer film SESSION.md (redacted note, 120 s timeout); HPC.md section 1 new row | the rule was added 2026-10-12 after the 2026-10-11 session |
| 26 | B51 | `module purge` removed the proxy: before set, after empty, after load empty; rule added in Section 8 | PASS | SESSION.md srun test; HPC.md section 8 new bullet | none |
| 27 | B52 | Scratch owned by root, mkdir refused; rule 'test before you write' in Section 7 | PASS | SESSION.md stat and mkdir output; HPC.md section 7 new bullet | 'the agent had checked with a read first' is true: stat and test -w preceded the refused mkdir probe |
| 28 | B60 | Put files where the agent reads them; add one line; ask it to say back the rules | PASS | how-to-use paragraphs of both files | the third step is this film's advice, not in the files: labelled as advice |
| 29 | B61 | No policy page says whether automated agents are allowed; claims are labelled by source | PASS | HPC.md section 10 and Appendix A item 19; AICR.md Appendix A item 21 | none |

**Stripped because it would date the film:** the specific partition limits and quotas (not in the film); job numbers. **Attributed aloud:** where a number is the benchmark's or the file's, the narration says so.

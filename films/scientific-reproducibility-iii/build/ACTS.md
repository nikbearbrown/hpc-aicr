# ACTS — Scientific Reproducibility III: Containers (lecture)

**What this is.** Coverage map for the film of our guide `hpc-aicr/guides/scientific-reproducibility-iii.md` and the lesson it rewrites, `hpc-aicr/Scientific-Reproducibility-III-2026/scientific-reproducibility3.md`. **Result.** Every section is in one of eight acts (36 body beats) or listed under LEFT OUT.

| Source section | Act | Beats |
|---|---|---|
| What is a container (sealed file; three names; why Apptainer, not Docker; .sif) | I | B10 B11 B12 |
| Why use one (reproducible, portable, no dependency fights, shareable, ready-made images; cost and the module, conda, container order) | II | B20 B21 B22 B23 |
| Running a container (exec, shell, run; check the tool; compute node; CPU job; GPU, --nv, interactive test, batch job, partition limits, prove the GPU) | III | B30–B39 |
| Binding directories (what a container sees; --bind; same path; APPTAINER_BIND) | IV | B40 B41 B42 |
| Building a container (no root on the cluster; build, copy, run; def file; build command; Dockerfile route; remote builder) | V | B50–B56 |
| Getting an image onto the cluster (pull; other registries; pin the tag; scp and OnDemand; where to keep images) | VI | B60–B64 |
| Tips (cache off home; test first and check; record the image and checksum; workflow managers; AICR) | VII | B70–B74 |
| What we tested and only read | VIII | B80 |
| Summary, Try it | recap, Your Turn | BVDT BHTF |

## Cast per act
I: the sealed kraft box (one box all film), cluster rack, Docker and Apptainer logo chips. II: box, rack, result page. III: box, login rack, compute rack, NVIDIA logo chip. IV: box-like container frame, folders. V: laptop, Professor Bear, folder 'project space'. VI: tag chips, boxes A and B. VII: notes page, boxes, big AICR rack.

## LEFT OUT (reasons)
- The three illustrations in the lesson (shipping containers photo, lunchbox photo, the Podman Desktop screenshot): stock or personal-path imagery; the idea is redrawn in the kit (B10). The Docker Hub diagram is redrawn as B53.
- The lesson's example image names tied to its authors' project (`seedpod`) and its personal email, username and home path: replaced by placeholders in our guide; not shown.
- The Dockerfile's full package list (about 20 lines): B54 shows the shape (base, install, verify, command) with the original's own lines.
- The transfer host name in the lesson: our guide says it may be stale; the film tells the viewer to check the current one (B63).
- `.bashrc` default-bind advice in the lesson: our guide prefers exporting inside the job script; the film follows our guide (B42).
- Getting help (email, office hours, consultation, docs links) and the closing thanks: listed in the description, not spoken (self-contained film).
- The guide's "Where the original differs / is wrong" list: used silently (2-GPU 12 h request becomes B38; unpinned build becomes B51/B52; latest becomes B62). The film never names the lesson or the guide.

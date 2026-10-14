# SHOTLIST — Scientific Reproducibility III: Containers

**What this is.** One row per body beat: what the sentence is about, the lane picked, the runner-up auditioned and why the pick wins. **Result.** 19 Manim scenes, 19 terminal beats (`CCPlainShell`), 6 bookends; no ShowTellCard needed; no tool captured live (see below). Runtime 616 s (10.3 min).

Tools shown: Docker, Apptainer and NVIDIA by their LOGOS (`brutalist.art/icons/logos/<name>/`); Apptainer's mark was missing and was created from the project's own public SVG (`apptainer.org/apptainer.svg`, mark only) as `icons/logos/apptainer/apptainer-01.svg|png`. Singularity, quay.io, BioContainers, Nextflow, Snakemake have no logo in the library: plain mono chips. Terminal beats show text only; the single recorded output (B31) comes from `guides/_real-outputs.md`.

| beat | about | lane picked | runner-up | why this one wins |
|---|---|---|---|---|
| B10 | a sealed bundle of parts that travels unchanged | Manim isometric box (kit) | ShowTellCard dashboard | the box seals and visits three machines: the motion is the claim |
| B11 | three names for the tool | logo chips (Docker, Apptainer) + mono chip | LibraryIconRow | logos shown by LOGO LAW; the arrow 'renamed' is the claim |
| B12 | why admin power is a risk on a shared machine | Manim iso rack + key + Professor Bear | 2x2 diagram | the key reaching the rack and being crossed out shows the risk; Docker image arrow shows it still reads Docker images |
| B20 | a result tied to a fixed image across six months | Manim timeline + iso rack | Manim chart | the rack changes while the box does not |
| B21 | portability and library clashes | Manim iso row + two-box split | isometric conveyor | the clash then the split is the claim |
| B22 | sharing a file and registries holding images | Manim iso + logo chips | FormBCard | three recipients and four stocked shelves |
| B23 | order of tools: module, conda, container | Manim staircase | ShowTellCard chart | climbing steps shows 'try in order' |
| B30 | three Apptainer verbs | CCPlainShell, the commands verbatim | FormBCard table | the evidence IS text |
| B31 | a read-only check and its recorded output | CCPlainShell with the recorded output | BrowserCapture | real recorded lines from guides/_real-outputs.md |
| B32 | login node vs compute node | Manim iso racks | CCPlainShell | the box crossed out on one rack and running on another |
| B33 | an interactive shell inside an image | CCPlainShell, labelled not run | CCSession skin | commands as text, no output |
| B34 | a CPU batch script | CCPlainShell, script lines verbatim | ClaudeCodeBeat | the script IS the evidence |
| B35 | the driver bridge that --nv builds | Manim iso (rack, NVIDIA logo, container) | isometric conveyor | the bridge laying across the gap is the claim |
| B36 | a one-GPU interactive request and the exec line | CCPlainShell, verbatim | ShowTellCard chart | commands as text |
| B37 | a one-GPU batch script | CCPlainShell, verbatim | ClaudeCodeBeat | the script IS the evidence |
| B38 | partition limits vs a 12 h request | Manim bar chart of recorded limits | ShowTellCard chart | the request bar overshooting the 8 h line |
| B39 | a one-line GPU proof | CCPlainShell, verbatim | BrowserCapture | commands as text, nothing claimed as run |
| B40 | what a container sees; binds | Manim iso container + folders | ShowTellCard | the folders sliding in only when bound |
| B41 | bind syntax and same-path binds | CCPlainShell, verbatim | FormBCard | commands as text |
| B42 | APPTAINER_BIND export | CCPlainShell, verbatim | FormACard | one real line |
| B50 | build here, copy, store, run | Manim iso four-station flow | DesignPipelineClaim isometric | the box travelling the four stations |
| B51 | the definition file head | CCPlainShell, the file verbatim | ClaudeCodeBeat | a file IS text |
| B52 | the rest of the file and the build command | CCPlainShell, verbatim | ClaudeCodeBeat | a file IS text |
| B53 | Docker route to a .sif | Manim flow with logos | CCPlainShell | logos and arrows show who builds what |
| B54 | a Dockerfile's shape | CCPlainShell, original's lines verbatim | ClaudeCodeBeat | a file IS text |
| B55 | the two conversion commands | CCPlainShell, verbatim | Manim flow | commands as text |
| B56 | the remote builder command | CCPlainShell, verbatim | FormBCard | one real line plus the caution |
| B60 | pulling an image | CCPlainShell, verbatim | Manim | commands as text |
| B61 | pulls from four registries | CCPlainShell, verbatim | logo row | commands as text |
| B62 | a moving tag vs a pinned tag | Manim two-panel timeline | ShowTellCard | the arrow swinging to another box |
| B63 | copying a local build | CCPlainShell, verbatim | Manim | a command as text |
| B64 | where images live | Manim iso folders, quota gauge | ShowTellCard | home refused, project accepted, recipe beside, archived |
| B70 | cache off home | CCPlainShell, verbatim | Manim | commands as text |
| B71 | test then check | CCPlainShell, verbatim | ShowTellCard | commands as text |
| B72 | what to record, and a checksum | Manim notes page + two boxes | ShowTellCard | stamped lines, then equal hashes |
| B73 | a pipeline of containers | Manim conveyor with versions | isometric conveyor | each step in its own box |
| B74 | AICR: what we have and lack | Manim iso rack + chips | FormBCard | stamps on a real rack |
| B80 | checked vs only read | Manim two columns | CARD | stamps landing on the spoken words |

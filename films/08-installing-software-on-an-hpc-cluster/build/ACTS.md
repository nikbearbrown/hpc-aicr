# ACTS — Installing Software on an HPC Cluster (lecture)

**What this is.** Coverage map for the lecture film of `hpc/Intro-to-Software-Installation-2026/intro_to_sw_installation.md`. **Result.** All nine sections covered in eight acts, 23 body beats, about 12.5 min.

| Source section | Act | Beats |
|---|---|---|
| 1 Why installation is different on HPC (no root; shared login node; shared filesystem; compatibility; the table) | I | B10 B11 |
| 2 Environment modules (commands; what `module load` does; Tcl not Lmod) | II | B20 B21 |
| 3 Conda (workflow; channels + licensing; pitfalls: login node, quota, scratch purge, pkgs cache; .condarc; -p; .bashrc; job script; export) | III | B30 B31 B32 B33 |
| 4 Spack (the caveat; the spec; workflow; environments; versions illustrative) | IV | B40 B41 |
| 5 EasyBuild (easyconfigs; toolchain; install into conda; eb --search; three flags; config.cfg; module use; Spack vs EasyBuild; candid note) | V | B50 B51 B52 |
| 6 From source (Autotools, CMake; HPC details; expose; personal Tcl modulefile; module stack; .version) | VI | B60 B61 B62 B63 |
| 7 Apptainer (why not Docker; pull/exec/shell; .def; build locally, scp, exec; when containers) | VII | B70 B71 B72 B73 |
| 8 Choosing the tool (six-tool table; the decision order) | VIII | B80 B81 |
| 9 Summary, quick reference, help | recap | BVDT |

## LEFT OUT
- The presenter's name, the "Summer 2026" series name and the "Today's Agenda" links: datable or navigational; the presenter is credited in the description.
- The five source diagrams (`install_decision_overview.png`, `module_load.png`, `source_build_pipeline.png`, `apptainer_vs_docker.png`, `tool_decision_tree.png`): flow-chart style outside the Claude palette; each is redrawn in the kit (B10, B21, B61, B70, B81) from the same content.
- `config.cfg` as its own card (its three lines are the three flags of B51); the full commented-out `conda initialize` block (B32 shows its first and last lines plus the two live lines, commented).
- The Quick Reference block: every command in it already appears in its own act.
- Getting help (email, office hours, consultation, docs): listed in the description, not spoken (self-contained film).
- `.version` default and in-modulefile `module load gcc` are spoken in B63 with a drawn glyph each, not shown as files.

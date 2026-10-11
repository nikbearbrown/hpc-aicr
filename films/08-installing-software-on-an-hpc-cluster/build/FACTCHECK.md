# FACTCHECK — Installing Software on an HPC Cluster (lecture)

**Sources.** S = the training document. **Result.** 18 claims: 18 PASS. Checked 2026-10-06. No number or name on screen comes from outside S.

| # | Beat | Claim | Verdict | Source |
|---|---|---|---|---|
| 1 | B10 | laptop vs cluster rows; generic binary runs slower or fails across nodes | PASS | S §1 table + text |
| 2 | B11 | login node shared; builds in jobs; NFS/GPFS/Lustre; tight quotas; small-file performance; slow launches | PASS | S §1 |
| 3 | B20 | Tcl Environment Modules, not Lmod; the seven commands | PASS | S §2 verbatim |
| 4 | B21 | a module edits PATH/LD_LIBRARY_PATH, installs nothing; admin-built, shared; clean version switching | PASS | S §2 |
| 5 | B30 | conda workflow; conda-forge coverage; Anaconda ToS restriction for large organisations; remove defaults | PASS | S §3.1–3.2 verbatim |
| 6 | B31 B32 | pitfalls: interactive job; quota; scratch purged; pkgs_dirs to scratch; `-p` path; rm pkgs; no auto-activate in .bashrc | PASS | S §3.3 |
| 7 | B33 | job script activates; `conda env export`/`create -f` | PASS | S §3.3 verbatim |
| 8 | B40 | Spack builds from source; compiler/MPI/variants; the caveat; spec `hdf5 @1.14.3 %gcc@12.2.0 +mpi`; versions illustrative | PASS | S §4 |
| 9 | B41 | the Spack workflow and environment commands; install in a job | PASS | S §4.2–4.3 verbatim |
| 10 | B50 | easyconfigs; thousands ship; toolchain; gompi = GCC + OpenMPI; no module; install into conda; `eb --search`; the eb command | PASS | S §5.1–5.2 verbatim |
| 11 | B51 | the three flags and their reasons; config.cfg; output is a modulefile; `module use`/`load` | PASS | S §5.2 |
| 12 | B52 | the four-row comparison; the candid note | PASS | S §5.3 |
| 13 | B60 | Autotools vs CMake; the commands; read the project's instructions | PASS | S §6.1 verbatim |
| 14 | B61 | prefix; load modules first; MPI/BLAS/LAPACK; build in a job; five stations | PASS | S §6.2 + source_build_pipeline.png |
| 15 | B62 | export PATH/LD_LIBRARY_PATH; modulefiles dir; `module use` in .bashrc; Tcl; `#%Module` magic cookie; the modulefile text | PASS | S §6.3–6.4 verbatim |
| 16 | B63 | dir = name, file = version; avail/load/unload; stack layout; `module load gcc` inside; `.version` | PASS | S §6.4–6.5 |
| 17 | B70 B71 B72 B73 | Apptainer formerly Singularity; Docker needs root; runs as you; GPU/MPI; pulls Docker images; pull/exec/shell; `.def`; build locally, scp, exec; when containers | PASS | S §7 verbatim |
| 18 | B80 B81 | the six-tool table; the five-step decision order; ask RC | PASS | S §8 |

Signed off by Bear at publish (per his standing instruction for this series).

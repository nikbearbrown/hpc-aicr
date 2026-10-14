# STORY — Scientific Reproducibility III: Containers

**What this is.** The story spine of a lecture film (about 10 minutes, Liam in for Bear) on software containers for research computing. **Why.** Sharing code does not let anyone repeat a result, because the libraries and the system under the code change. **Found.** A container seals the whole software stack into one file. On Northeastern's clusters you run it with Apptainer, build it elsewhere, pull it with a pinned tag, bind the folders it needs, and record the image. We checked only three facts ourselves; everything else is from the source and the film says so.

**Misconception corrected (BIDEA):** "To repeat my result, I just share my code" becomes "seal the whole stack".
**Arc:** what a container is (I) → why use one (II) → running it, CPU and GPU (III) → binding folders (IV) → building an image (V) → getting an image onto the cluster (VI) → habits that keep it honest (VII) → what was checked and what was only read (VIII) → recap, Your Turn, outro.
**Standalone:** assumes the viewer has seen no other film. Module, conda, login node, compute node, Slurm and root are each explained in one phrase where first used.

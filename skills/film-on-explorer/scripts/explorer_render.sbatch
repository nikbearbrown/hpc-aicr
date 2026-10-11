#!/bin/bash
# explorer_render.sbatch: render ONE film from its staged job directory with the toolchain built by explorer_setup.sbatch.
# Submit (after the researcher says yes):  sbatch --export=ALL,TK=/projects/<project>/film-toolkit,JOB=/scratch/<user>/film-jobs/<slug>-<stamp>,SLUG=<slug> explorer_render.sbatch
# Audio (mp3 + timings) ships inside the film package, so no TTS runs here. Numbers are a first guess; right-size from `seff`. UNTESTED.
#SBATCH --job-name=film-render
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --output=%x-%j.out
set -euo pipefail
: "${TK:?}"; : "${JOB:?}"; : "${SLUG:?}"
[ -f "$JOB/.film-job" ] || { echo "ABORT: $JOB has no .film-job marker"; exit 1; }
module purge; module load nodejs/v22.11.0 FFmpeg/7.1.1
export PATH="$TK/env/bin:$PATH"
echo "job $SLURM_JOB_ID on $(hostname) at $(date)"; which python ffmpeg node
cd "$JOB"; tar -xzf reel.tar.gz
python -c "import manim; print('manim', manim.__version__)"
"$TK/brutalist.art/art" run   "$JOB/$SLUG" --height 2160
"$TK/brutalist.art/art" final "$JOB/$SLUG" --height 2160 --out "$JOB/$SLUG/exports/landscape"
python "$TK/brutalist.art/runtime/scripts/bookend_check.py" "$JOB/$SLUG" || echo "bookend check did not pass: read above"
ls -lh "$JOB/$SLUG/exports/landscape" || true
echo "render finished at $(date)"

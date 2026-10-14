#!/bin/bash
# explorer_render.sbatch: render ONE film from its staged job directory with the toolchain built by explorer_setup.sbatch.
# Submit (after the researcher says yes):  sbatch --export=ALL,TK=/projects/<project>/film-toolkit,JOB=/scratch/<user>/film-jobs/<slug>-<stamp>,SLUG=<slug> explorer_render.sbatch
# Audio (mp3 + timings) ships inside the film package, so no TTS runs here.
# Numbers come from one piloted film (44 beats, 4K, 2026-10-11): peak memory 9.6 GB, 16 cores used at 22 to 39 percent, wall time
# 45 min for a first full render plus about 7 min per compile; so 8 cores, 16 GB and 3 h leave margin. Re-measure with `seff` for your film.
#SBATCH --job-name=film-render
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=03:00:00
#SBATCH --output=%x-%j.out
set -euo pipefail
: "${TK:?}"; : "${JOB:?}"; : "${SLUG:?}"
[ -f "$JOB/.film-job" ] || { echo "ABORT: $JOB has no .film-job marker"; exit 1; }
module purge; module load $(cat "$TK/film-modules.txt")      # first name is explorer/1.0: keeps the cluster proxy; rendering itself needs no network
export PATH="$TK/env/bin:$PATH"
export FONTCONFIG_FILE="$TK/fonts.conf"             # the bundled fonts, no writes to $HOME
# The cluster's ffmpeg has the drawtext filter (many Mac builds do not). With it, the review cut burns a running timestamp into
# the top-right corner, and Gate V then reports edge-bleed on every frame. The toolkit honours this switch; the clean master is unaffected.
export ART_NO_DRAWTEXT=1
echo "job $SLURM_JOB_ID on $(hostname) at $(date)"; which python ffmpeg node
cd "$JOB"; tar -xzf reel.tar.gz
# the film brings its own capture pictures (Remotion reads them from public/<name>/); the toolkit stays film-independent
# the Professor Bear portraits this film's scenes pick, into the folder the scene code looks in (never overwrites)
if [ -d "$JOB/$SLUG/_portraits" ]; then mkdir -p "$TK/brutalist.art/professor-bear" && cp -n "$JOB/$SLUG/_portraits/"*.png "$TK/brutalist.art/professor-bear/" && echo "portraits copied: $(ls "$JOB/$SLUG/_portraits" | wc -l)"; fi
[ -d "$JOB/$SLUG/_public" ] && cp -rn "$JOB/$SLUG/_public/." "$TK/brutalist.art/runtime/remotion/public/" && echo "film captures copied into the toolkit public folder"
python -c "import manim; print('manim', manim.__version__)"
"$TK/brutalist.art/art" run   "$JOB/$SLUG" --height 2160
"$TK/brutalist.art/art" final "$JOB/$SLUG" --height 2160 --out "$JOB/$SLUG/exports/landscape"
python "$TK/brutalist.art/runtime/scripts/bookend_check.py" "$JOB/$SLUG" || echo "bookend check did not pass: read above"
ls -lh "$JOB/$SLUG/exports/landscape" || true
echo "render finished at $(date)"

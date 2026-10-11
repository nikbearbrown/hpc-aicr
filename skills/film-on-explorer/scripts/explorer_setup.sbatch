#!/bin/bash
# explorer_setup.sbatch: ONE-TIME build of the render toolchain on a compute node of Explorer.
# Submit (after the researcher says yes):  sbatch --export=ALL,TK=/projects/<project>/film-toolkit,PKG=/scratch/<user>/film-jobs/<job>/toolkit-code.tar.gz explorer_setup.sbatch
# TK must be PERSISTENT project space, never scratch (scratch is purged on the first Tuesday of the month).
# Resource numbers are a first guess: read `seff <jobid>` afterwards and right-size. UNTESTED on the cluster.
#SBATCH --job-name=film-setup
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=%x-%j.out
set -euo pipefail
: "${TK:?set TK=/projects/<project>/film-toolkit}"; : "${PKG:?set PKG=<path to toolkit-code.tar.gz>}"
module purge
module load miniconda3/25.9.1 nodejs/v22.11.0 FFmpeg/7.1.1     # names seen on Explorer 2026-10-11; re-check with `module avail`
echo "node: $(hostname)  python: $(python3 --version 2>&1)  node: $(node --version)  ffmpeg: $(ffmpeg -version | head -1)"
echo "--- network check from a COMPUTE node (the open question): all must print 200"
for u in https://pypi.org https://registry.npmjs.org https://github.com; do
  code=$(curl -sS -o /dev/null -m 15 -w '%{http_code}' -I "$u" || echo FAIL); echo "$u $code"
  [ "$code" = 200 ] || { echo "NO NETWORK from a compute node: stop here and ask rchelp@northeastern.edu how to get packages in"; exit 2; }
done
mkdir -p "$TK"; tar -xzf "$PKG" -C "$TK"
[ -d "$TK/env" ] || conda create -y -p "$TK/env" python=3.12
export PATH="$TK/env/bin:$PATH"                                  # PATH prepend, not `source activate`
pip install -r "$TK/brutalist.art/requirements.txt"
( cd "$TK/brutalist.art/runtime/remotion" && npm ci && npx remotion browser ensure )
"$TK/brutalist.art/art" doctor || echo "doctor reported gaps: read the output above"
"$TK/brutalist.art/art" smoke  || echo "smoke render FAILED: read the output above before any real film"
du -sh "$TK" "$TK/env" "$TK/brutalist.art/runtime/remotion/node_modules" 2>/dev/null || true
echo "setup finished"

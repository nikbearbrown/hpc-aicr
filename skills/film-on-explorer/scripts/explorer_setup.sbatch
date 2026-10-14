#!/bin/bash
# explorer_setup.sbatch: the ONE-TIME (or when-stale) install of the render toolchain, run on a compute node.
# Submit after the researcher says yes, from the toolkit dir (bootstrap_toolkit.sh prints the exact line):
#   cd $TK && sbatch --export=ALL,TK=/projects/<project>/film-toolkit,STAMP=<fingerprint> sbatch/explorer_setup.sbatch
# Needs the code in $TK already (bootstrap_toolkit.sh --sync-code). TK must be PERSISTENT project space.
# Idempotent: exits at once if the installed environment already matches STAMP. Rendering needs no network;
# only this install does. If the compute node has no network, it falls back to the download cache
# that explorer_cache.sh filled from the login node. Numbers are first guesses: right-size from `seff`. UNTESTED.
#SBATCH --job-name=film-setup
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=%x-%j.out
set -euo pipefail
: "${TK:?set TK=/projects/<project>/film-toolkit}"; : "${STAMP:?set STAMP=<fingerprint from bootstrap_toolkit.sh>}"
[ -f "$TK/film-modules.txt" ] && [ -f "$TK/brutalist.art/requirements.txt" ] || { echo "ABORT: code not synced into $TK (run bootstrap_toolkit.sh --sync-code)"; exit 1; }
if [ "$(cat "$TK/.env-stamp" 2>/dev/null || true)" = "$STAMP" ]; then echo "environment already current ($STAMP): nothing to do"; exit 0; fi
# explorer/1.0 is the default module that sets the cluster proxy (compute nodes reach PyPI and npm only through it).
# `module purge` removes it, so it is the first name in film-modules.txt and is loaded again here.
module purge; module load $(cat "$TK/film-modules.txt")           # names seen on Explorer 2026-10-11
echo "node: $(hostname)  python: $(python3 --version 2>&1)  node: $(node --version)  ffmpeg: $(ffmpeg -version | head -1)"
ONLINE=1
echo "proxy in this job: https_proxy=${https_proxy:-<unset>} http_proxy=${http_proxy:-<unset>}"
for u in https://pypi.org https://registry.npmjs.org https://github.com; do
  code=$(curl -sS -o /dev/null -m 15 -w '%{http_code}' "$u" 2>/dev/null || true); echo "$u ${code:-none}"; [ "$code" = 200 ] || ONLINE=0
done
PIPFLAGS=""; NPMFLAGS=""
if [ "$ONLINE" = 0 ]; then
  [ -d "$TK/cache/wheels" ] && [ -d "$TK/cache/npm" ] || { echo "NO NETWORK from this compute node and no cache in $TK/cache. Run explorer_cache.sh on the login node (ask rchelp@northeastern.edu first), then resubmit."; exit 2; }
  echo "OFFLINE: installing from $TK/cache"; PIPFLAGS="--no-index --find-links $TK/cache/wheels"; NPMFLAGS="--offline --cache $TK/cache/npm"
fi
[ -d "$TK/env" ] || conda create -y -q -p "$TK/env" python=3.12 --override-channels -c conda-forge
export PATH="$TK/env/bin:$PATH"                                  # PATH prepend, not `source activate`
# manim's text engine (manimpango) and pycairo need Pango/Cairo developer files, which Explorer lacks (runtime libraries only).
# conda-forge ships them prebuilt, so manim comes from conda first; pip then fills in the rest and skips what is already satisfied.
# The version must match what the films were built with. On the author's Mac that is Manim 0.20.1 (ManimPango 0.6.1);
# the toolkit's requirements.txt still says manim<0.19, and the pinned 0.18.1 made every Manim clip one frame short
# (the compiler then refuses the film). So conda installs the Mac's version and pip must not touch manim.
MANIM_VERSION=0.20.1
conda install -y -q -p "$TK/env" --override-channels -c conda-forge "manim=$MANIM_VERSION" "manimpango>=0.6,<0.7"
grep -v -i -E '^(manim|manimpango)\b' "$TK/brutalist.art/requirements.txt" > "$TK/requirements-explorer.txt"
pip install $PIPFLAGS -r "$TK/requirements-explorer.txt"
RR="$TK/brutalist.art/runtime/remotion"
# npm ci deletes node_modules first and is slow on a network filesystem: redo it only when the lockfile changed.
LOCKH=$(sha256sum "$RR/package-lock.json" | cut -c1-12)
if [ "$(cat "$RR/node_modules/.lockhash" 2>/dev/null || true)" != "$LOCKH" ]; then
  ( cd "$RR" && npm ci $NPMFLAGS ) && echo "$LOCKH" > "$RR/node_modules/.lockhash"
fi
# Remotion's own downloader is Node 22.11 and ignores the proxy (pip, npm, conda and curl honour it), so fetch the
# headless Chrome with curl and unpack it exactly where Remotion looks; `browser ensure` then finds it and downloads nothing.
CHV=$(sed -n "s/.*TESTED_VERSION = '\([^']*\)'.*/\1/p" "$RR/node_modules/@remotion/renderer/dist/browser/get-chrome-download-url.js" | head -1)
[ -n "$CHV" ] || { echo "could not read Remotion's Chrome version"; exit 4; }
CD="$RR/node_modules/.remotion/chrome-headless-shell"
if [ "$(cat "$CD/VERSION" 2>/dev/null || true)" != "$CHV" ]; then
  mkdir -p "$TK/cache" "$CD/linux64"; CHZ="$TK/cache/chrome-headless-shell-linux64-$CHV.zip"
  [ -f "$CHZ" ] || curl -fsSL --retry 3 -o "$CHZ" "https://storage.googleapis.com/chrome-for-testing-public/$CHV/linux64/chrome-headless-shell-linux64.zip"
  unzip -q -o "$CHZ" -d "$CD/linux64" && echo "$CHV" > "$CD/VERSION"
fi
( cd "$RR" && npx remotion browser ensure )
# Fonts: the toolkit's setup copies fonts into ~/.local/share/fonts; a job should not write to $HOME, so a private
# fontconfig file points at the bundled families (EB Garamond, Inter, ...) plus Oswald, kept inside the toolkit folder.
FD="$TK/fonts"; mkdir -p "$FD" "$TK/fontcache"
find "$TK/brutalist.art/runtime/fonts" -iname '*.ttf' -exec cp -n {} "$FD/" \;
[ -f "$FD/Oswald-Variable.ttf" ] || curl -fsSL --retry 3 -o "$FD/Oswald-Variable.ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf" || echo "Oswald download failed (only some title styles use it)"
cat > "$TK/fonts.conf" <<FC
<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig><include ignore_missing="yes">/etc/fonts/fonts.conf</include><dir>$FD</dir><cachedir>$TK/fontcache</cachedir>
<!-- Films name Apple's Menlo for code. Linux has no Menlo, and the fallback is a different width, which moves labels and fails Gate B.
     PT Mono (bundled) has the same advance width, so films lay out the same here as on the Mac. -->
<match target="pattern"><test name="family" qual="any"><string>Menlo</string></test><edit name="family" mode="assign" binding="same"><string>PT Mono</string></edit></match>
</fontconfig>
FC
export FONTCONFIG_FILE="$TK/fonts.conf"
# `art smoke` needs the Kokoro voice models, which stay on your computer (narration is made there). So the check is
# the doctor's report on what rendering needs; audio and LaTeX equation beats are EXPECTED to be blocked here.
"$TK/brutalist.art/art" doctor 2>&1 | tee "$TK/doctor-$(date +%Y%m%d).txt" || true
D=$(sed 's/\x1b\[[0-9;]*m//g' "$TK/doctor-$(date +%Y%m%d).txt")
for need in "Manim beats" "Remotion beats" "compile" "fonts"; do
  echo "$D" | grep -i "$need" | grep -q "ready" || { echo "NOT READY: $need (read the doctor report above). Environment NOT stamped."; exit 3; }
done
pip freeze > "$TK/freeze-$(date +%Y%m%d).txt"; module list 2>&1 | tee "$TK/modules-used-$(date +%Y%m%d).txt" >/dev/null
echo "$STAMP" > "$TK/.env-stamp"
du -sh "$TK" "$TK/env" "$TK/brutalist.art/runtime/remotion/node_modules" 2>/dev/null || true
echo "setup finished, environment stamped $STAMP"

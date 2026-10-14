#!/usr/bin/env bash
# explorer_cache.sh <toolkit-dir>      Run ON THE EXPLORER LOGIN NODE (ssh <alias> "bash <TK>/sbatch/explorer_cache.sh <TK>").
# Only needed if compute nodes cannot reach PyPI/npm. DOWNLOAD ONLY: it fills <TK>/cache with the Python
# wheels and the npm cache, using the login node's internet and the filesystem it shares with compute nodes.
# It installs nothing and runs no computation. Ask rchelp@northeastern.edu before the first use (installs on
# login nodes are discouraged; this is a download of a few hundred MB, size unmeasured). UNTESTED.
set -euo pipefail
TK=${1:?toolkit dir}; [[ "$TK" == /projects/* ]] || { echo "REFUSED: not under /projects"; exit 1; }
[ -f "$TK/film-modules.txt" ] || { echo "code not synced into $TK"; exit 1; }
module purge; module load $(cat "$TK/film-modules.txt")
mkdir -p "$TK/cache/wheels" "$TK/cache/npm"
python3 -m pip download -r "$TK/brutalist.art/requirements.txt" -d "$TK/cache/wheels" --python-version 3.12 --only-binary=:all: \
  || echo "some packages have no wheel: pip download without --only-binary may be needed (sdists need a build step)"
# npm: fills the cache from the lockfile without leaving a node_modules behind
T=$(mktemp -d); cp "$TK/brutalist.art/runtime/remotion/package.json" "$TK/brutalist.art/runtime/remotion/package-lock.json" "$T/"
( cd "$T" && npm ci --ignore-scripts --cache "$TK/cache/npm" ) ; rm -rf "$T"
# the headless Chrome Remotion needs (its own downloader ignores the proxy, so setup uses this file)
CHV=$(sed -n "s/.*TESTED_VERSION = '\([^']*\)'.*/\1/p" "$TK/brutalist.art/runtime/remotion/node_modules/@remotion/renderer/dist/browser/get-chrome-download-url.js" 2>/dev/null | head -1); CHV=${CHV:-157.0.8080.0}
curl -fsSL --retry 3 -o "$TK/cache/chrome-headless-shell-linux64-$CHV.zip" "https://storage.googleapis.com/chrome-for-testing-public/$CHV/linux64/chrome-headless-shell-linux64.zip" || echo "chrome download failed"
du -sh "$TK/cache"; echo "cache filled. The setup job will use it automatically if the compute node is offline."

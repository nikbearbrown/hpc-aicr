#!/usr/bin/env bash
# toolkit_stamp.sh <books-dir>
# Prints a short fingerprint of everything that decides what must be INSTALLED on the cluster:
# the Python requirements, the npm lockfile, the module list, the setup script and the Python version. If this
# fingerprint matches the one stored in the cluster toolkit, nothing needs reinstalling;
# toolkit CODE changes (new scenes, scripts) do not change it. Read-only; runs on your computer.
set -euo pipefail
BOOKS=${1:?books dir}; HERE=$(cd "$(dirname "$0")" && pwd)
T="$BOOKS/brutalist.art"
for f in "$T/requirements.txt" "$T/runtime/remotion/package-lock.json" "$HERE/modules.txt" "$HERE/explorer_setup.sbatch"; do [ -f "$f" ] || { echo "missing $f" >&2; exit 1; }; done
{ cat "$T/requirements.txt" "$T/runtime/remotion/package-lock.json" "$HERE/modules.txt" "$HERE/explorer_setup.sbatch"; echo "python=3.12"; } | shasum -a 256 | cut -c1-12

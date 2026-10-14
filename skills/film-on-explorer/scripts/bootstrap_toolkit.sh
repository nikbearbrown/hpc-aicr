#!/usr/bin/env bash
# bootstrap_toolkit.sh <ssh-alias> <toolkit-dir-on-cluster> <books-dir> [--sync-code]
# The repeatable install. Run it any time: on a new account, after the project folder was wiped,
# after the toolkit's dependencies changed, or just to check. It is IDEMPOTENT.
#
#   default      READ-ONLY. Reports whether the cluster toolkit exists, whether its code is current,
#                and whether the installed environment matches this toolkit's fingerprint. If the
#                environment is missing or stale it PRINTS the one sbatch command to run. It never submits.
#   --sync-scripts  Copies only modules.txt and the job scripts (a few KB, seconds) into <toolkit-dir>. Use after editing a script.
#   --sync-code  Writes ONLY inside <toolkit-dir-on-cluster>: copies the toolkit's code (about 57 MB,
#                no node_modules, no media) and the module list, then unpacks over the old code.
#                The installed environment (env/, node_modules/) is never touched by this step.
#
# <toolkit-dir-on-cluster> must be persistent project space, e.g. /projects/<project>/film-toolkit,
# never scratch. Uses BatchMode: your key must already be unlocked. UNTESTED on the cluster;
# the packing and fingerprint steps were tested on a Mac.
set -euo pipefail
HOST=${1:?ssh alias}; TK=${2:?toolkit dir on cluster}; BOOKS=${3:?books dir}; MODE=${4:-plan}
[[ "$TK" == /projects/* ]] || { echo "REFUSED: $TK is not under /projects (scratch is purged monthly)"; exit 1; }
[[ "$TK" =~ ^/projects/[A-Za-z0-9._/-]+$ ]] || { echo "REFUSED: odd characters in $TK"; exit 1; }
HERE=$(cd "$(dirname "$0")" && pwd); SSH="ssh -o BatchMode=yes -o ConnectTimeout=10 $HOST"
WANT=$("$HERE/toolkit_stamp.sh" "$BOOKS")
echo "fingerprint of this toolkit's install inputs: $WANT"

if [ "$MODE" = "--sync-scripts" ]; then
  $SSH "mkdir -p '$TK/sbatch'"
  rsync -av -e "ssh -o BatchMode=yes" "$HERE/explorer_setup.sbatch" "$HERE/explorer_render.sbatch" "$HERE/explorer_cache.sh" "$HOST:$TK/sbatch/"
  rsync -av -e "ssh -o BatchMode=yes" "$HERE/modules.txt" "$HOST:$TK/film-modules.txt"
  echo "scripts and module list synced into $TK"; exit 0
fi
if [ "$MODE" = "--sync-code" ]; then
  OUT=$(mktemp -d); trap 'rm -rf "$OUT"' EXIT
  "$HERE/pack_for_cluster.sh" "$BOOKS" none "$OUT"
  $SSH "mkdir -p '$TK/.incoming'"
  rsync -av -e "ssh -o BatchMode=yes" "$OUT/toolkit-code.tar.gz" "$HERE/modules.txt" "$HERE/explorer_setup.sbatch" "$HERE/explorer_render.sbatch" "$HERE/explorer_cache.sh" "$HOST:$TK/.incoming/"
  $SSH "cd '$TK' && tar -xzf .incoming/toolkit-code.tar.gz && cp .incoming/modules.txt film-modules.txt && mkdir -p sbatch && cp .incoming/*.sbatch .incoming/explorer_cache.sh sbatch/ && rm -rf .incoming && date +%Y-%m-%dT%H:%M > .code-synced && echo 'code synced into $TK'"
  echo "Next: re-run without --sync-code to see whether the environment needs installing."
  exit 0
fi

echo "--- cluster state (read-only)"
$SSH "TK='$TK'; if [ -d \"\$TK\" ]; then echo \"toolkit dir: present\"; else echo \"toolkit dir: MISSING\"; fi
for f in .code-synced .env-stamp; do [ -f \"\$TK/\$f\" ] && echo \"\$f: \$(cat \$TK/\$f)\" || echo \"\$f: absent\"; done" || true
HAVE=$($SSH "cat '$TK/.env-stamp' 2>/dev/null | head -c 12" || true)
if [ "$HAVE" = "$WANT" ]; then
  echo "RESULT: environment is current. Nothing to install. Next: pack the film and run explorer_render.sbatch."
else
  echo "RESULT: environment is ${HAVE:+STALE (installed $HAVE)}${HAVE:-MISSING}. Install it once, after you say yes:"
  echo "  1. $0 $HOST $TK $BOOKS --sync-code      (if .code-synced is absent or old)"
  echo "  2. ssh $HOST \"cd $TK && sbatch --export=ALL,TK=$TK,STAMP=$WANT sbatch/explorer_setup.sbatch\"     (an sbatch: ask first; read HPC.md)"
  echo "If a compute node cannot reach PyPI/npm, the setup job says so and stops; then run   ssh $HOST \"bash $TK/sbatch/explorer_cache.sh $TK\"   on the login node once (ask rchelp@northeastern.edu first) and submit the same job again."
fi

#!/usr/bin/env bash
# fetch_and_clean.sh <ssh-alias> <remote-job-dir> <local-out-dir> [--yes-delete <exact-job-dir-name>]
# 1) shows what would be copied (dry run) and copies the finished master + logs back to YOUR computer;
# 2) verifies the copy with a checksum dry run (empty output = nothing missing or different);
# 3) ONLY if you pass --yes-delete with the exact directory name, deletes that ONE job directory on Explorer.
# Safety: the remote path must look like /scratch/<user>/film-jobs/<slug>-<stamp> AND contain the .film-job marker;
# the delete is a single `rm -rf` of that directory, after printing exactly what is in it. Never run it without the
# researcher's explicit yes in chat. UNTESTED on the cluster.
set -euo pipefail
HOST=${1:?ssh alias}; RDIR=${2:?remote job dir}; LOUT=${3:?local out dir}; shift 3
SSH="ssh -o BatchMode=yes -o ConnectTimeout=10 $HOST"
[[ "$RDIR" =~ ^/scratch/[A-Za-z0-9._-]+/film-jobs/[A-Za-z0-9._-]+-[0-9]{8}-[0-9]{4}$ ]] || { echo "REFUSED: $RDIR is not a film job directory"; exit 1; }
$SSH "test -f '$RDIR/.film-job'" || { echo "REFUSED: no .film-job marker in $RDIR"; exit 1; }
mkdir -p "$LOUT"
SRC="$HOST:$RDIR/"
INC=(--include='*/' --include='exports/landscape/***' --include='*.srt' --include='*.md' --include='film-*.out' --include='*.log' --exclude='*')
echo "--- dry run: files that would be copied"; rsync -avn -e "ssh -o BatchMode=yes" "${INC[@]}" "$SRC" "$LOUT/"
rsync -av -e "ssh -o BatchMode=yes" "${INC[@]}" "$SRC" "$LOUT/"
echo "--- verify (checksum dry run; no lines under 'sending incremental file list' means complete)"
rsync -avnc -e "ssh -o BatchMode=yes" "${INC[@]}" "$SRC" "$LOUT/"
if [ "${1:-}" = "--yes-delete" ]; then
  [ "${2:-}" = "$(basename "$RDIR")" ] || { echo "REFUSED: --yes-delete needs the exact directory name $(basename "$RDIR")"; exit 1; }
  echo "--- about to delete on Explorer: $RDIR"; $SSH "du -sh '$RDIR'; ls -la '$RDIR' | head -30"
  $SSH "rm -rf -- '$RDIR'" && echo "deleted $RDIR"
else
  echo "Nothing deleted. When the researcher says yes: re-run with  --yes-delete $(basename "$RDIR")"
fi

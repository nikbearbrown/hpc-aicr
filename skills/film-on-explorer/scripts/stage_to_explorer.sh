#!/usr/bin/env bash
# stage_to_explorer.sh <ssh-alias> <pack-dir> <slug> [<toolkit-pkg-only>]
# Creates ONE job-scoped directory on Explorer scratch, marks it, and copies the packed archives into it.
#   /scratch/<user>/film-jobs/<slug>-<YYYYmmdd-HHMM>/        (marker file: .film-job)
# Prints the directory. It does NOT submit anything and touches nothing else on the cluster.
# Uses BatchMode: your key must already be unlocked (see skills/hpc/HPC.md Section 10). UNTESTED on the cluster.
set -euo pipefail
HOST=${1:?ssh alias, e.g. explorer}; PACK=${2:?pack dir from pack_for_cluster.sh}; SLUG=${3:?film slug}
[[ "$SLUG" =~ ^[A-Za-z0-9._-]+$ ]] || { echo "bad slug"; exit 1; }
STAMP=$(date +%Y%m%d-%H%M)
SSH="ssh -o BatchMode=yes -o ConnectTimeout=10 $HOST"
JOB=$($SSH 'echo /scratch/$USER/film-jobs')/"$SLUG-$STAMP"
$SSH "mkdir -p '$JOB' && printf 'created %s by stage_to_explorer.sh\n' '$STAMP' > '$JOB/.film-job'"
rsync -av -e "ssh -o BatchMode=yes" "$PACK/reel.tar.gz" "$PACK/SHA256SUMS" "$HOST:$JOB/"
[ -z "${4:-}" ] && rsync -av -e "ssh -o BatchMode=yes" "$PACK/toolkit-code.tar.gz" "$HOST:$JOB/" || true
echo "JOB_DIR=$JOB"

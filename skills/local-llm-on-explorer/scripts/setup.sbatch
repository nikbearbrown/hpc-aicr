#!/bin/bash
#SBATCH --job-name=ollama-setup
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=%x-%j.out
# NEW in this guide (not from the tutorial; it is the tutorial's Part 2 step 4, done as a batch job so an agent can
# run it for you). Not run end to end yet: read the log and report what you see.
# Usage:  cd ~/.ollama-hpc && sbatch setup.sbatch
# Optional: OLLAMA_TAG=<version> sbatch --export=ALL,OLLAMA_TAG=<version> setup.sbatch   (pin a version; the default is "latest")
# Optional: INSTALL_CADDY=1 (adds the Caddy image; only the laptop pattern needs it)
set -euo pipefail

echo "job $SLURM_JOB_ID on $(hostname) at $(date --iso-8601=seconds)"
source ~/.ollama-hpc/env.sh
echo "storage root: $LLM_ROOT"

# Compute nodes reach the internet through a proxy set by a default module. Report only whether it is set.
if [ -n "${http_proxy:-}${https_proxy:-}${HTTP_PROXY:-}${HTTPS_PROXY:-}" ]; then
  echo "proxy variables: set"
else
  echo "proxy variables: NOT set; image pulls will fail (see the tutorial's troubleshooting table)"
fi

mkdir -p "$LLM_ROOT/images" "$LLM_ROOT/run" "$OLLAMA_MODELS" "$APPTAINER_CACHEDIR" "$APPTAINER_TMPDIR"

OLLAMA_TAG="${OLLAMA_TAG:-latest}"
if [ -f "$OLLAMA_SIF" ]; then
  echo "ollama image already present: $OLLAMA_SIF (delete it yourself to re-pull)"
else
  apptainer pull "$OLLAMA_SIF" "docker://ollama/ollama:${OLLAMA_TAG}"
fi

if [ "${INSTALL_CADDY:-0}" = "1" ]; then
  if [ -f "$CADDY_SIF" ]; then
    echo "caddy image already present: $CADDY_SIF"
  else
    apptainer pull "$CADDY_SIF" docker://caddy:2
  fi
fi

echo "ollama version (needs 0.14 or later for the Anthropic-compatible API):"
apptainer exec "$OLLAMA_SIF" ollama --version
echo "setup finished"

#!/bin/bash
#SBATCH --job-name=ollama-smoke
#SBATCH --partition=__PARTITION__
#SBATCH --gres=gpu:__GPU_TYPE__:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=__TIME__
#SBATCH --output=%x-%j.out
# NEW in this guide (not from the tutorial; it strings together the tutorial's Part 4 steps 3 to 5 so an agent can run
# them for you). Not run end to end yet: read the log and report what you see.
# The three __PLACEHOLDERS__ are filled from the live `sinfo` by the guide before submitting; do not submit as is.
# Usage:  cd ~/.ollama-hpc && sbatch smoke-test-filled.sbatch
set -uo pipefail

echo "job $SLURM_JOB_ID on $(hostname) at $(date --iso-8601=seconds)"
echo "GPU the job really got:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || { echo "no GPU visible: stop"; exit 1; }

# Calls to the local server must not go through the cluster proxy (curl does not skip loopback by itself).
# Only loopback is exempted, so the model download still uses the proxy.
export NO_PROXY="127.0.0.1,localhost${NO_PROXY:+,$NO_PROXY}"
export no_proxy="$NO_PROXY"

source ~/.ollama-hpc/start-ollama.sh || { echo "Ollama did not start: see the log named above"; exit 1; }
echo "model: $LLM_MODEL   context: $LLM_CONTEXT"

ollama pull "$LLM_MODEL" || { echo "model pull failed"; exit 1; }

echo "--- one message through the Anthropic-compatible address ---"
curl -s -w "\nHTTP %{http_code}\n" "http://127.0.0.1:$OLLAMA_PORT/v1/messages" \
  -H "content-type: application/json" \
  -H "x-api-key: ollama" \
  -H "anthropic-version: 2023-06-01" \
  -d "{\"model\": \"$LLM_MODEL\", \"max_tokens\": 64, \"messages\": [{\"role\": \"user\", \"content\": \"Reply with the single word: ready\"}]}"

echo "--- ollama ps (PROCESSOR should read 100% GPU; CONTEXT should match $LLM_CONTEXT) ---"
ollama ps

echo "--- did Ollama find the GPU? ---"
grep -i "inference compute" "$RUN_DIR/ollama.log" || echo "no 'inference compute' line in $RUN_DIR/ollama.log"

echo "smoke test finished"

# Source this inside a GPU job:  source ~/.ollama-hpc/start-ollama.sh
source ~/.ollama-hpc/env.sh

if [ -z "$SLURM_JOB_ID" ]; then
  echo "Not inside a Slurm job. Start a GPU job first." >&2
  return 1 2>/dev/null || exit 1
fi

export OLLAMA_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')
export RUN_DIR="$LLM_ROOT/run/$SLURM_JOB_ID"
mkdir -p "$RUN_DIR" && chmod 700 "$RUN_DIR"

# --env is required: the image sets OLLAMA_HOST=0.0.0.0:11434, which would override a plain export.
apptainer exec --nv -B "$LLM_ROOT" \
  --env OLLAMA_HOST="127.0.0.1:$OLLAMA_PORT" \
  --env OLLAMA_MODELS="$OLLAMA_MODELS" \
  --env OLLAMA_CONTEXT_LENGTH="$LLM_CONTEXT" \
  --env OLLAMA_NUM_PARALLEL=1 \
  --env OLLAMA_KEEP_ALIVE=-1 \
  --env OLLAMA_FLASH_ATTENTION=1 \
  "$OLLAMA_SIF" ollama serve > "$RUN_DIR/ollama.log" 2>&1 &
export OLLAMA_PID=$!

for i in $(seq 1 90); do
  curl -sf "http://127.0.0.1:$OLLAMA_PORT/api/version" > /dev/null && break
  sleep 1
done
if ! curl -sf "http://127.0.0.1:$OLLAMA_PORT/api/version" > /dev/null; then
  echo "Ollama did not start. See $RUN_DIR/ollama.log" >&2
  return 1 2>/dev/null || exit 1
fi

ollama() {
  apptainer exec -B "$LLM_ROOT" --env OLLAMA_HOST="127.0.0.1:$OLLAMA_PORT" "$OLLAMA_SIF" ollama "$@"
}
export -f ollama

echo "Ollama is up on 127.0.0.1:$OLLAMA_PORT (pid $OLLAMA_PID). Log: $RUN_DIR/ollama.log"

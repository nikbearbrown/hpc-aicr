#!/bin/bash
#SBATCH --job-name=ollama-serve
#SBATCH --partition=gpu
#SBATCH --gres=gpu:h200:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=%x-%j.out

source ~/.ollama-hpc/start-ollama.sh || exit 1
ollama pull "$LLM_MODEL" || exit 1

PROXY_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("0.0.0.0", 0)); print(s.getsockname()[1]); s.close()')
TOKEN=$(cat ~/.ollama-hpc/token)
umask 077

cat > "$RUN_DIR/Caddyfile" << CADDY_EOF
{
    admin off
    auto_https off
}
:${PROXY_PORT} {
    @authorized header Authorization "Bearer ${TOKEN}"
    handle @authorized {
        reverse_proxy 127.0.0.1:${OLLAMA_PORT}
    }
    handle {
        respond "unauthorized" 401
    }
}
CADDY_EOF

cat > ~/.ollama-hpc/current << CONN_EOF
NODE=$(hostname)
PROXY_PORT=${PROXY_PORT}
MODEL=${LLM_MODEL}
JOB=${SLURM_JOB_ID}
CONN_EOF
trap 'rm -f ~/.ollama-hpc/current' EXIT TERM INT

echo "Serving $LLM_MODEL on $(hostname):$PROXY_PORT behind token auth"
apptainer exec -B "$LLM_ROOT" \
  --env XDG_CONFIG_HOME="$RUN_DIR/caddy-config" \
  --env XDG_DATA_HOME="$RUN_DIR/caddy-data" \
  "$CADDY_SIF" caddy run --config "$RUN_DIR/Caddyfile" --adapter caddyfile

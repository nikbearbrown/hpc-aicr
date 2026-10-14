# Storage. Change to /projects/<group>/$USER/llm if your PI has project space.
export LLM_ROOT="/scratch/$USER/llm"

export OLLAMA_SIF="$LLM_ROOT/images/ollama.sif"
export CADDY_SIF="$LLM_ROOT/images/caddy.sif"
export OLLAMA_MODELS="$LLM_ROOT/models"
export APPTAINER_CACHEDIR="$LLM_ROOT/apptainer-cache"
export APPTAINER_TMPDIR="$LLM_ROOT/apptainer-tmp"

# Model and context window. See Part 3.
export LLM_MODEL="qwen3-coder:30b"
export LLM_CONTEXT=65536

# Source this after start-ollama.sh:  source ~/.ollama-hpc/claude-local.sh
if [ -z "$OLLAMA_PORT" ]; then
  echo "Run: source ~/.ollama-hpc/start-ollama.sh first." >&2
  return 1 2>/dev/null || exit 1
fi
export PATH="$HOME/.local/bin:$PATH"
unset ANTHROPIC_API_KEY
export ANTHROPIC_BASE_URL="http://127.0.0.1:$OLLAMA_PORT"
export ANTHROPIC_AUTH_TOKEN="ollama"
export ANTHROPIC_MODEL="$LLM_MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$LLM_MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$LLM_MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$LLM_MODEL"
export CLAUDE_CODE_SUBAGENT_MODEL="$LLM_MODEL"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
echo "Claude Code -> $ANTHROPIC_BASE_URL using $LLM_MODEL"

#!/bin/bash
#SBATCH --job-name=claude-headless
#SBATCH --partition=gpu
#SBATCH --gres=gpu:h200:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=%x-%j.out
# Usage: sbatch ~/.ollama-hpc/headless.sbatch /path/to/repo /path/to/task.md

REPO="$1"
TASK="$2"
source ~/.ollama-hpc/start-ollama.sh || exit 1
ollama pull "$LLM_MODEL" || exit 1
source ~/.ollama-hpc/claude-local.sh || exit 1
cd "$REPO" || exit 1
claude -p "$(cat "$TASK")" --permission-mode acceptEdits

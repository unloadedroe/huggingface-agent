#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODEL_MODE="${MODEL_MODE:-ollama}"
HF_MODEL="${HF_MODEL:-Qwen/Qwen2.5-1.5B-Instruct}"
HF_TOKEN="${HF_TOKEN:-}"
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2:7b}"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://localhost:11434}"

export MODEL_MODE
export HF_MODEL
export HF_TOKEN
export OLLAMA_MODEL
export OLLAMA_BASE_URL

if [ -x "$SCRIPT_DIR/.venv/bin/python" ]; then
  PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
else
  PYTHON_BIN="python"
fi

printf 'Starting app with mode=%s\n' "$MODEL_MODE"
if [ "$MODEL_MODE" = "huggingface" ]; then
  printf 'Using Hugging Face model: %s\n' "$HF_MODEL"
  if [ -n "$HF_TOKEN" ]; then
    printf 'HF token is set.\n'
  else
    printf 'HF_TOKEN is not set; some models may require authentication.\n'
  fi
else
  printf 'Using Ollama model: %s\n' "$OLLAMA_MODEL"
fi

"$PYTHON_BIN" app.py

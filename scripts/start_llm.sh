#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MODEL_DIR="$PROJECT_DIR/models/Qwen3-0.6B"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/llm.$(date +%Y%m%d-%H%M%S).log"

mkdir -p "$LOG_DIR"

if ! python3 -c "import vllm" >/dev/null 2>&1; then
    echo "vLLM is not installed in the current Python environment."
    echo "Run: python -m pip install -U vllm"
    exit 1
fi

echo "Starting vLLM server with Qwen3-0.6B from $MODEL_DIR"
echo "Logging to $LOG_FILE"

python3 -m vllm.entrypoints.openai.api_server \
    --model "$MODEL_DIR" \
    --served-model-name qwen3 \
    --port 8000 \
    --max-model-len 8192 \
    2>&1 | tee -a "$LOG_FILE"
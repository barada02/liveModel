#!/bin/bash
# Start Qwen3-0.6B using vLLM for high-throughput OpenAI-compatible API
# We serve it on port 8000

MODEL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../models/Qwen3-0.6B" && pwd)"

echo "Starting vLLM server with Qwen3-0.6B from $MODEL_DIR"

python3 -m vllm.entrypoints.openai.api_server \
    --model "$MODEL_DIR" \
    --served-model-name qwen3 \
    --port 8000 \
    --max-model-len 8192 \
    --enable-reasoning \
    --reasoning-parser deepseek_r1
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
OUT_FILE="$LOG_DIR/collected.$(date +%Y%m%d-%H%M%S).txt"

mkdir -p "$LOG_DIR"

echo "Collecting logs into $OUT_FILE"
{
  echo "=== DATE ==="
  date
  echo
  echo "=== FILES ==="
  ls -lah "$LOG_DIR" || true
  echo
  echo "=== LLM LOGS ==="
  tail -n 200 "$LOG_DIR"/llm*.log 2>/dev/null || true
  echo
  echo "=== ASR LOGS ==="
  tail -n 200 "$LOG_DIR"/asr*.log 2>/dev/null || true
  echo
  echo "=== TTS LOGS ==="
  tail -n 200 "$LOG_DIR"/tts*.log 2>/dev/null || true
} | tee "$OUT_FILE"

echo "Saved combined log report to $OUT_FILE"

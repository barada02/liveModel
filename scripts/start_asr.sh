#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/asr.$(date +%Y%m%d-%H%M%S).log"

mkdir -p "$LOG_DIR"

echo "Starting ASR service on port 8001"
echo "Logging to $LOG_FILE"

python3 "$PROJECT_DIR/services/asr_service.py" 2>&1 | tee -a "$LOG_FILE"

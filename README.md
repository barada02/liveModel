# LiveModel - Real-Time AI Voice Interaction

This is a microservices-based voice interaction system designed for a Vast.ai Linux Desktop container.

## Recommended Vast.ai Template

Use the **Linux Desktop** template for this project.

Why this template fits:
1. It gives you a full Linux desktop plus SSH and Jupyter terminal access.
2. It supports root installs, so we can set up Python, model dependencies, and tools directly in the container.
3. It uses Supervisor instead of systemd, which is fine for the first phase because we will run each service explicitly and capture logs ourselves.
4. It exposes both a browser desktop and terminal access, which is useful while we are testing audio, GPU, and file handling.

## Installation with uv

This repository keeps the Python dependency list in `requirements.txt`. Use `uv` to create the virtual environment and install everything in one step.

```bash
git clone https://github.com/YOUR_USERNAME/liveModel.git
cd liveModel

uv venv
source .venv/bin/activate

uv pip install -r requirements.txt

python scripts/download_models.py
mkdir -p logs
```

If you are using a fresh Linux Desktop container, install vLLM only through `requirements.txt` and let `uv` resolve the full environment from that file.

## Lifecycle

1. Code locally in VS Code.
2. Push to GitHub.
3. Clone the repo inside the Vast.ai Linux Desktop container.
4. Install dependencies and download model files into local storage.
5. Start each service separately.
6. Run one test script per service.
7. Collect logs into files when anything fails.

## Local to GitHub

You already know the Git commands, so the key rule is: keep the repository clean and only push the phase you want to test.

## Vast.ai Linux Desktop Startup

After the `uv` setup above completes, you can verify the container and launch the services.

If `vllm` fails because of CUDA or wheel mismatch, keep the failure log and we can adjust the version constraints in `requirements.txt` for that exact container image.

If you want a quick system check first:

```bash
nvidia-smi
python --version
which python
df -h
```

## First Test Phase

We are not wiring ASR -> LLM -> TTS yet. Each service is tested independently.

Important GPU note:
1. vLLM can reserve most GPU VRAM by default.
2. If you run all services together, TTS may fail with CUDA OOM.
3. For phase-1, either run one heavy service at a time, or cap vLLM memory with `VLLM_GPU_MEMORY_UTILIZATION`.

Example (cap vLLM to 55% VRAM):

```bash
export VLLM_GPU_MEMORY_UTILIZATION=0.55
bash scripts/start_llm.sh
```

### 1. Start the LLM service

```bash
bash scripts/start_llm.sh
```

Recommended check:

```bash
curl http://localhost:8000/v1/models
```

### 2. Start the ASR service

```bash
python services/asr_service.py
```

Recommended check:

```bash
python tests/test_asr.py
```

### 3. Start the TTS service

```bash
python services/tts_service.py
```

Recommended check:

```bash
python tests/test_tts.py
```

### 4. Test the LLM directly

```bash
python tests/test_llm.py
```

## Log System

Every service should write its stdout and stderr to a log file in `logs/`.

Use this pattern when starting services:

```bash
mkdir -p logs

# LLM
bash scripts/start_llm.sh 2>&1 | tee -a logs/llm.log

# ASR
python services/asr_service.py 2>&1 | tee -a logs/asr.log

# TTS
python services/tts_service.py 2>&1 | tee -a logs/tts.log
```

If a service fails, bring back these files for analysis:

```bash
logs/llm.log
logs/asr.log
logs/tts.log
```

If you want a full timestamped capture of one run, use:

```bash
script -q -c "python services/asr_service.py" logs/asr.session.log
```

## Suggested Vast.ai Config

For this phase, choose:

1. Template: Linux Desktop.
2. GPU: RTX 3090 or RTX 4090. A 3060 can work for testing, but the 3090/4090 gives more margin.
3. Disk: At least 40 GB.
4. Persistence: Prefer a persistent disk or reusable instance so the downloaded models are not lost between sessions.
5. Access: Use SSH or Jupyter terminal for the testing phase, and keep the desktop open if you need audio tools.

## Notes on Service Management

This container uses Supervisor and not systemd. For our first phase, we do not need to build system services yet. We will run the three model services manually, capture logs, and only automate later if the tests are stable.

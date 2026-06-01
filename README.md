# LiveModel - Real-Time AI Voice Interaction

This is a microservices-based voice interaction system designed for Vast.ai GPU containers.

## 🚀 Lifecycle: Local -> GitHub -> Vast.ai

1. **Code Locally**: Edit `.py` files, configuration, and scripts in VS Code precisely as we are doing now.
2. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial microservices setup"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/liveModel.git
   git push -u origin main
   ```
3. **Deploy on Vast.ai**:
   - Rent your container (see config below).
   - Once connected via SSH or Jupyter terminal:
     ```bash
     git clone https://github.com/YOUR_USERNAME/liveModel.git
     cd liveModel
     pip install -r requirements.txt
     pip install openai requests  # For the test scripts
     python scripts/download_models.py
     ```

## 🖥️ Recommended Vast.ai Setup

To maintain low latency while minimizing costs, configure your Vast.ai instance as follows:

*   **GPU**: 1x RTX 3090 or RTX 4090. (An RTX 3060/4060 will also work but generation TTFT might be slightly slower for Qwen).
*   **Docker Image**: Use the official PyTorch or vLLM image. We recommend: `vllm/vllm-openai:latest` or `pytorch/pytorch:2.2.1-cuda12.1-cudnn8-devel`.
*   **Disk Space**: Request at least **30GB - 40GB**. (Models are ~2.5GB combined, but PyTorch and CUDA dependencies will fill up space fast).
*   **Bandwidth**: Pick a host with `> 500 Mbps` download speed to ensure `scripts/download_models.py` finishes quickly.

## 🧪 Testing the Pipeline

Once inside your Vast.ai container, start the 3 services in separate terminal tabs (or using `tmux`/`screen`):

**Terminal 1 (LLM API - Port 8000):**
```bash
chmod +x scripts/start_llm.sh
./scripts/start_llm.sh
```

**Terminal 2 (ASR API - Port 8001):**
```bash
python services/asr_service.py
```

**Terminal 3 (TTS API - Port 8002):**
```bash
python services/tts_service.py
```

**Terminal 4 (Run Tests):**
```bash
# Test LLM
python tests/test_llm.py

# Test TTS
python tests/test_tts.py

# Test ASR (Ensure you create a dummy.wav first as noted in the file)
python tests/test_asr.py
```

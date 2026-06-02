
## LiveModel Setup Flow

Follow these steps in order.

### 1. Generate or access your SSH key on the laptop

If you do not already have an SSH key, create one on your laptop:

```powershell
ssh-keygen -t ed25519 -C "chandanbarada2@gmail.com"
```

If the key already exists, print the public key so you can copy it:

```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

Use the public key content in the Vast.ai SSH key field.

### 2. Create or open the Vast.ai instance

Choose the Linux Desktop template, then add your SSH public key to the instance.

Copy the remote SSH link shown by Vast.ai. It usually looks like:

```bash
ssh <user>@<host> -p <port>
```

### 3. Connect from VS Code

Install and use the Remote - SSH extension in VS Code.

Open the Command Palette and connect with the remote SSH link you copied from Vast.ai.

### 4. Clone the repo on the remote machine

```bash
git clone https://github.com/barada02/liveModel.git
cd liveModel
```

### 5. Create and activate the virtual environment

Use uv to create the environment:

```bash
uv venv .venv --python 3.13
```

Activate it:

```bash
source .venv/bin/activate
```

### 6. Install dependencies with uv

Install the project requirements:

```bash
uv pip install -r requirements.txt
```

If the model files are not already present, download them:

```bash
python scripts/download_models.py
```

The service scripts create the logs folder and timestamped log files automatically.

### 7. Run the services

Start each service separately with the shell wrappers. They also write logs automatically.

LLM:

```bash
bash scripts/start_llm.sh
```

ASR:

```bash
bash scripts/start_asr.sh
```

TTS:

```bash
bash scripts/start_tts.sh
```

The scripts create timestamped log files in `logs/` automatically.

### 8. Run the tests

LLM test:

```bash
python tests/test_llm.py
```

ASR test:

```bash
python tests/test_asr.py
```

TTS test:

```bash
python tests/test_tts.py
```

### 9. Useful checks

```bash
nvidia-smi
python --version
which python
curl http://localhost:8000/v1/models
```

### 10. If vLLM uses too much GPU memory

Cap memory before starting the LLM service:

```bash
export VLLM_GPU_MEMORY_UTILIZATION=0.55
bash scripts/start_llm.sh
```
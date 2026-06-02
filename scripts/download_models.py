import os
from huggingface_hub import snapshot_download
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Define the local paths where we want to store the models
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
HF_TOKEN = os.getenv('HF_TOKEN')

def download_models():
    print(f"Downloading models into: {MODELS_DIR}")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # 1. Download Qwen3-0.6B (LLM)
    print("\n--- Downloading Qwen3-0.6B ---")
    snapshot_download(
        repo_id="Qwen/Qwen3-0.6B",
        local_dir=os.path.join(MODELS_DIR, "Qwen3-0.6B"),
        ignore_patterns=["*.pt", "*.bin"],  # Prefer safetensors if available
        token=HF_TOKEN
    )
    
    # 2. Download Moonshine-base (ASR)
    print("\n--- Downloading Moonshine-base ---")
    snapshot_download(
        repo_id="UsefulSensors/moonshine-base",
        local_dir=os.path.join(MODELS_DIR, "moonshine-base"),
        token=HF_TOKEN
    )
    
    # 3. Download VoxCPM2 (TTS) - Updated from VoxCPM1.5 with instruction tone support
    print("\n--- Downloading VoxCPM2 ---")
    snapshot_download(
        repo_id="openbmb/VoxCPM2",
        local_dir=os.path.join(MODELS_DIR, "VoxCPM2"),
        token=HF_TOKEN
    )

    print("\nAll models downloaded successfully!")

if __name__ == "__main__":
    download_models()

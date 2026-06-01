import os
import io
import numpy as np
import torch
import soundfile as sf
from fastapi import FastAPI, UploadFile, File, HTTPException
from transformers import MoonshineForConditionalGeneration, AutoProcessor

app = FastAPI(title="Moonshine ASR Service")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'moonshine-base'))

print(f"Loading Moonshine from {MODEL_PATH}")
model = MoonshineForConditionalGeneration.from_pretrained(MODEL_PATH).to(device).to(torch_dtype)
processor = AutoProcessor.from_pretrained(MODEL_PATH)
TARGET_SAMPLING_RATE = getattr(processor.feature_extractor, "sampling_rate", 16000)


def _resample_audio(audio_data: np.ndarray, source_rate: int, target_rate: int) -> np.ndarray:
    if source_rate == target_rate:
        return audio_data

    duration = len(audio_data) / source_rate
    target_length = max(1, int(round(duration * target_rate)))
    source_positions = np.linspace(0.0, duration, num=len(audio_data), endpoint=False)
    target_positions = np.linspace(0.0, duration, num=target_length, endpoint=False)
    return np.interp(target_positions, source_positions, audio_data).astype(np.float32)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    # Read audio from the uploaded WAV payload.
    audio_data, samplerate = sf.read(io.BytesIO(audio_bytes))

    if audio_data.size == 0:
        raise HTTPException(status_code=400, detail="Uploaded audio file is empty")

    # If stereo, convert to mono
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)

    audio_data = np.asarray(audio_data, dtype=np.float32)
    audio_data = _resample_audio(audio_data, samplerate, TARGET_SAMPLING_RATE)

    inputs = processor(
        audio_data, 
        return_tensors="pt",
        sampling_rate=TARGET_SAMPLING_RATE
    )
    inputs = inputs.to(device, torch_dtype)
    
    # basic generation
    generated_ids = model.generate(**inputs, max_length=500)
    text = processor.decode(generated_ids[0], skip_special_tokens=True)
    
    return {"transcription": text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
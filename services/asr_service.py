import os
import io
import torch
import soundfile as sf
from fastapi import FastAPI, UploadFile, File
from transformers import MoonshineForConditionalGeneration, AutoProcessor

app = FastAPI(title="Moonshine ASR Service")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'moonshine-base'))

print(f"Loading Moonshine from {MODEL_PATH}")
model = MoonshineForConditionalGeneration.from_pretrained(MODEL_PATH).to(device).to(torch_dtype)
processor = AutoProcessor.from_pretrained(MODEL_PATH)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    
    # Read audio - assuming valid wav file is sent
    audio_data, samplerate = sf.read(io.BytesIO(audio_bytes))
    
    # If stereo, convert to mono
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)

    inputs = processor(
        audio_data, 
        return_tensors="pt",
        sampling_rate=samplerate
    )
    inputs = inputs.to(device, torch_dtype)
    
    # basic generation
    generated_ids = model.generate(**inputs, max_length=500)
    text = processor.decode(generated_ids[0], skip_special_tokens=True)
    
    return {"transcription": text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
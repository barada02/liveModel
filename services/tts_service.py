import os
import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import soundfile as sf

# According to VoxCPM docs
from voxcpm import VoxCPM

app = FastAPI(title="VoxCPM TTS Service")

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'VoxCPM1.5'))
print(f"Loading VoxCPM from {MODEL_PATH}...")
model = VoxCPM.from_pretrained(MODEL_PATH)

class TTSRequest(BaseModel):
    text: str

@app.post("/synthesize")
def synthesize(req: TTSRequest):
    # Generates speech (numpy array)
    wav = model.generate(text=req.text)
    
    # Convert to WAV stream
    buffer = io.BytesIO()
    sf.write(buffer, wav, model.tts_model.sample_rate, format='WAV')
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="audio/wav", headers={
        "Content-Disposition": "attachment; filename=output.wav"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
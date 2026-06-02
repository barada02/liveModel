import os
import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import soundfile as sf
from typing import Optional

# According to VoxCPM docs
from voxcpm import VoxCPM

app = FastAPI(title="VoxCPM TTS Service")

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'VoxCPM2'))
print(f"Loading VoxCPM from {MODEL_PATH}...")
model = VoxCPM.from_pretrained(MODEL_PATH)

class TTSRequest(BaseModel):
    text: str
    tone: Optional[str] = None  # Voice instruction/tone (e.g., "A young woman, gentle and sweet voice", "slightly faster, cheerful tone")

@app.post("/synthesize")
def synthesize(req: TTSRequest):
    # Construct text with tone instruction if provided
    # Format: (instruction_tone)text_content
    if req.tone:
        full_text = f"({req.tone}){req.text}"
    else:
        full_text = req.text
    
    # Generates speech (numpy array)
    wav = model.generate(
        text=full_text,
        cfg_value=2.0,
        inference_timesteps=10,
    )
    
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
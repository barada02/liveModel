import requests

# To run this, you need a dummy audio file. 
# You can generate a quick one using:
# python -c "import soundfile as sf, numpy as np; sf.write('dummy.wav', np.random.randn(16000), 16000)"

url = "http://localhost:8001/transcribe"

try:
    with open("dummy.wav", "rb") as f:
        files = {"file": ("dummy.wav", f, "audio/wav")}
        print(f"Sending audio to ASR service at {url}...")
        response = requests.post(url, files=files)

    print("Status Code:", response.status_code)
    print("Content-Type:", response.headers.get("content-type", "<missing>"))

    if response.status_code == 200:
        try:
            print("Response JSON:", response.json())
        except ValueError:
            print("Failed to decode JSON response:")
            print(response.text)
    else:
        print("Response Body:")
        print(response.text)
except FileNotFoundError:
    print("Please create a 'dummy.wav' file in this directory to test ASR.")
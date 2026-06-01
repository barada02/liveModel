import requests

url = "http://localhost:8002/synthesize"
data = {"text": "Hello! I am a smart voice assistant running on a local GPU."}

print(f"Sending text to TTS service at {url}...")
response = requests.post(url, json=data)

if response.status_code == 200:
    with open("test_output.wav", "wb") as f:
        f.write(response.content)
    print("Successfully saved audio to 'test_output.wav'")
else:
    print(f"Failed! Status Code: {response.status_code}")
    print(response.text)
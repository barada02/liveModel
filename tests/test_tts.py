import requests

url = "http://localhost:8002/synthesize"

# Test 1: Basic text synthesis without tone
print("\n[Test 1] Synthesizing basic text...")
data = {"text": "Hello! I am a smart voice assistant running on a local GPU."}
print(f"Sending text to TTS service at {url}...")
response = requests.post(url, json=data)

if response.status_code == 200:
    with open("test_output_basic.wav", "wb") as f:
        f.write(response.content)
    print("Successfully saved audio to 'test_output_basic.wav'")
else:
    print(f"Failed! Status Code: {response.status_code}")
    print(response.text)

# Test 2: Text synthesis with instruction tone (VoxCPM 2.0 feature)
print("\n[Test 2] Synthesizing with instruction tone...")
data = {
    "text": "Hello! I am a smart voice assistant running on a local GPU.",
    "tone": "A young woman, gentle and sweet voice, slightly faster pace"
}
print(f"Sending text with tone instruction to {url}...")
response = requests.post(url, json=data)

if response.status_code == 200:
    with open("test_output_with_tone.wav", "wb") as f:
        f.write(response.content)
    print("Successfully saved audio to 'test_output_with_tone.wav'")
else:
    print(f"Failed! Status Code: {response.status_code}")
    print(response.text)

print("\nAll tests completed!")
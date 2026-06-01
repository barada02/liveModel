from openai import OpenAI

# Initialize the OpenAI client pointing to our local vLLM server
client = OpenAI(
    api_key="EMPTY", # vLLM doesn't require a real API key locally
    base_url="http://localhost:8000/v1",
)

print("Sending prompt to local Qwen3-0.6B...")

response = client.chat.completions.create(
    model="qwen3",
    messages=[
        {"role": "user", "content": "You are a voice assistant. Give me a brief, one-sentence greeting."}
    ],
    max_tokens=50
)

reply = response.choices[0].message.content
print("\nLLM Response:")
print(reply)
# chat completions api
base_url="http://localhost:11434"

from openai import OpenAI
client = OpenAI(api_key="ollama", base_url=f'{base_url}/v1')

completion = client.chat.completions.create(
  model="qwen3:0.6b",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)

# chat completions api
base_url="http://192.168.1.8:1234"

from openai import OpenAI
client = OpenAI(api_key="lm-studio", base_url=f'{base_url}/v1')

completion = client.chat.completions.create(
  model="smollm2-135m-instruct",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)

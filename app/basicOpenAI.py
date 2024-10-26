from openai import OpenAI;

secret_key = ""
#secret_key = "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"

prompt = "Write a small poem about my childhood friend Diego"

client = OpenAI(api_key=secret_key,)

"""
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ],
  max_tokens = 100,
  temperature = 1
)

print(completion.choices[0].message.content)
"""

response = client.images.generate(
  model="dall-e-3",
  prompt="The Dallas Cowboys winning the SuperBowl 3 years in a row in 2025",
  n=1,
  size="1024x1024"
)

print(response.data)


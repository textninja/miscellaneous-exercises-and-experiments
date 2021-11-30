import os
import openai
import yaml

with open(os.getenv("SECRETS_PATH", "secrets.yaml")) as f:
  openai.api_key = yaml.load(f, Loader=yaml.FullLoader)["apikey"]

prompt = """Nope, that didn't work, the text message still isn't being sent. I finally got it working with this code:

001 const twilio = require('twilio');"""

response = openai.Completion.create(
  engine="davinci",
  prompt=prompt,
  temperature=0.6,
  max_tokens=256,
  top_p=0.3,
  frequency_penalty=0.5,
  presence_penalty=0.0)

print(prompt + response["choices"][0]["text"])



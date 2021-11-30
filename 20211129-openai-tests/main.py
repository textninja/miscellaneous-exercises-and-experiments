import os
import openai
import yaml

with open(os.getenv("SECRETS_PATH", "secrets.yaml")) as f:
  openai.api_key = yaml.load(f, Loader=yaml.FullLoader)["apikey"]

prompt = "This common lisp program writes hello world to stdout:"

response = openai.Completion.create(
  engine="davinci",
  prompt=prompt,
  temperature=0.6,
  max_tokens=256,
  top_p=0.3,
  frequency_penalty=0.5,
  presence_penalty=0.0)

print(prompt + response["choices"][0]["text"])
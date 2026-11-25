import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)

response = client.responses.create(
    model="openai/gpt-oss-120b",
    instructions="You are a teaching agent",
    temperature=0,
    max_output_tokens=50,
    input="Why is the sky blue?",
)


print(response.model)
# print(json.dumps(response.to_dict(),indent=2))
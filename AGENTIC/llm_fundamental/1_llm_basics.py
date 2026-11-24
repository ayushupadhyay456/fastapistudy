from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI()

result=client.responses.create(
    model='gpt-4o',
    input="what is the square root of 89"
)

print(result.output_text)

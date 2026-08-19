import os

from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()

client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=50,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: BioQuery connected",
        }
    ],
)

print(message.content[0].text)
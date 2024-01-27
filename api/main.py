import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Assuming you have the AZURE_OPENAI_API_KEY environment variable set
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

# Specify the appropriate model(s) if needed
# client = openai.ChatCompletion.create(api_key=openai.api_key, models=['gpt-35-turbo-instruct'])

client = openai.ChatCompletion.create(
    model="chatgpt",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ],
)

api_version = os.getenv("OPENAI_API_VERSION")

message_text = [{'role': "system",
                 "content": "You are an AI assistant that helps people find information."}]

completion = client.chat.completions.create(
    model="chatgpt",
    messages=message_text,
    temperature=0.7,
    max_tokens=800,
    top_p=0.955,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)

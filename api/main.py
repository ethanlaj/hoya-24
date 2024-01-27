from openai import AzureOpenAI
import os

# Assuming you have the OPEN_API_KEY environment variable set
api_key = os.getenv("OPEN_API_KEY")

client = AzureOpenAI(
    api_key=api_key,
    # models=['gpt-35-turbo-instruct'],  # Specify the appropriate model(s)
)

# openai.api_version = ????

message_text = [{'role': "system",
                 "content": "You are an AI assistant that helps people find information."}]

completion = client.chat.completions.create(model="chatgpt",
                                            messages=message_text,
                                            temperature=0.7,
                                            max_tokens=800,
                                            top_p=0.955,
                                            frequency_penalty=0,
                                            presence_penalty=0,
                                            stop=None)

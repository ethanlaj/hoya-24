#Note: The openai-python library support for Azure OpenAI is in preview.
      #Note: This code sample requires OpenAI Python library version 0.28.1 or lower.
import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_type = "azure"
openai.api_base = "https://firsttrying.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

message_text = [{"role":"system","content":"You are an AI assistant that helps people find information.\nIf the user input is related to the school application, make the user input more straightforward so that AI model can serach the infromation about user's questions, and you return the True If the user input is not related to school application, Return False and say the customer'i cannot help you about that'"},]

completion = openai.ChatCompletion.create(
  engine="etown",
  messages = message_text,
  temperature=0.5,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)
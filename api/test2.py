import os
from openai import AzureOpenAI

from dotenv import load_dotenv
load_dotenv()


def main():
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_KEY"),  
        api_version="2023-05-15"
    )

    print(os.getenv("AZURE_OPENAI_ENDPOINT"))

    response = client.chat.completions.create(
        model="etown", # model = "deployment_name".
        messages=[
            {"role": "system", "content": "Whatever the user says, tell them they are wrong."},
            {"role": "user", "content": "I believe the earth is round"},
        ]
    )

    print(response.choices[0].message.content)



if __name__ == "__main__":
    main()
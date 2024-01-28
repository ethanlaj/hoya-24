import json
import os
import openai
import dotenv
import re
dotenv.load_dotenv()

endpoint = "https://firsttrying.openai.azure.com/"
api_version = "2023-08-01-preview"
api_key = os.getenv("OPENAI_API_KEY")
deployment_id = "etown"
search_endpoint = "https://etown-search-1.search.windows.net"
search_key = os.getenv("SEARCH_KEY")
search_index_name = "cosmosdb-index"


def retrieval(query):
    client = openai.AzureOpenAI(
        base_url=f"{endpoint}/openai/deployments/{deployment_id}",
        api_key=api_key,
        api_version=api_version,
    )

    completion = client.chat.completions.create(
        model=deployment_id,
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that validates and reformats prompts that are put into another AI model.\nIf the user input is related to the school application, make the user input more straightforward so that an AI model can search the information about the user's questions. Please return False if the user input is not related to Elizabethtown College and return the message 'I cannot help you with that request', otherwise return True and reformat the original request for better use of prompt engineering\nPlease return the data in json format: { valid: boolean, message: string}. Here is the user query: " + query,
            },
        ],
        temperature=0.5,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )

    try:
        result = json.loads(completion.choices[0].message.content)
        return result
    except Exception as e:
        print(e)
        return None

# ** #


def generation(query):
    client = openai.AzureOpenAI(
        base_url=f"{endpoint}/openai/deployments/{deployment_id}/extensions",
        api_key=api_key,
        api_version=api_version,
    )

    completion = client.chat.completions.create(
        model=deployment_id,
        messages=[
            {
                "role": "user",
                "content": query,
            },
        ],
        extra_body={
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "key": search_key,
                        "indexName": search_index_name,
                        "semanticConfiguration": "default",
                        "queryType": "simple",
                        "fieldsMapping": {
                            "contentFieldsSeparator": "\n",
                            "contentFields": [
                                "text"
                            ],
                            "filepathField": "url",
                            "titleField": None,
                            "urlField": "rid",
                            "vectorFields": []
                        },
                        "inScope": True,
                        "filter": None,
                        "strictness": 3,
                        "topNDocuments": 5,
                    }
                }
            ]
        }
    )

    try:
        result = completion.choices[0].message.content
        clean_text = re.sub(r'\[doc\d+\]', '', result)
        return clean_text
    except Exception as e:
        print(e)
        return None

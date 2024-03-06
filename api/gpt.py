import json
import os
import openai
import dotenv
import re
dotenv.load_dotenv()

endpoint = "https://etown-test2.openai.azure.com/"
api_version = "2023-08-01-preview"
api_key = os.getenv("OPENAI_API_KEY")
deployment_id = "gpt-35-turbo"
search_endpoint = "https://etown-sitetext-search-2.search.windows.net"
search_key = os.getenv("SEARCH_KEY")
search_index_name = "cosmosdb-index"


def retrieval(query, context):
    client = openai.AzureOpenAI(
        base_url=f"{endpoint}/openai/deployments/{deployment_id}",
        api_key=api_key,
        api_version=api_version,
    )

    if context is None:
        context = []

    # Assuming context is a list of dictionaries
    context_messages = [{"role": "assistant" if msg['sender'] == "bot" else msg["sender"], "content": msg['message']} for msg in context[-3:]
                        ] if len(context) >= 3 else [
        {"role": "assistant" if msg['sender'] ==
            "bot" else msg["sender"], "content": msg['message']}
        for msg in context
    ]
# Append the user message to the context_messages list
    context_messages.append({
        "role": "user",
        "content": query
    })

    print(context_messages)

    completion = client.chat.completions.create(
        model=deployment_id,
        messages=[
            {
                "role": "system",
                "content":
                    """
                        As an AI assistant, your role is to process user prompts and 
                        transform them into questions that are explicitly related to 
                        Elizabethtown College, even when the original input is vague 
                        or not clearly connected to the college. For example, if a 
                        user asks about "computer science," reframe the query to 
                        "What does the Computer Science program at Elizabethtown College offer?" 
                        Every question should be direct and clear to aid the AI model in 
                        fetching specific information related to the user's interests 
                        in Elizabethtown College.

                        Instead of rejecting non-specific prompts, 
                        you will reshape them to be applicable to Elizabethtown 
                        College and return `True`, alongside the rephrased inquiry.
                        When reformulating prompts, draw upon the context from the 
                        user's prior interactions to craft a unified and detailed question.

                        The responses must be structured in JSON format, with a 
                        `valid` key indicating `True` for all rephrased prompts 
                        and a `message` key containing the newly formulated question. 
                        Here is how the JSON response would look for a non-specific 
                        prompt like "computer science":

                        {
                        "valid": true,
                        "message": "What courses are available in the Computer Science department at Elizabethtown College?"
                        }
                    """,
            },
            *context_messages,  # Use the unpacking operator to include context_messages
        ],
        temperature=0.5,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )

    try:
        print(completion.choices[0].message.content)
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

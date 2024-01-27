import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

load_dotenv()

endpoint = "https://hoya24.documents.azure.com:443/"
key = os.getenv("AZURE_COSMOS_DB_KEY")
client = CosmosClient(endpoint, key)

database_id = "hoya24"
database = client.create_database_if_not_exists(id=database_id)

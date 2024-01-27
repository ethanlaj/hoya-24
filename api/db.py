from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()


user = os.getenv('MONGO_USER')
password = os.getenv('MOGNO_PWD')

uri = f"mongodb+srv://{user}:{password}@cluster0.zpcscby.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database('hoya')

from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

user = os.getenv('MONGO_USER')
password = os.getenv('MOGNO_PWD')

uri = f"mongodb+srv://{user}:{password}@cluster0.zpcscby.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['chatdb']
chats = db.chats


@app.route('/chats', methods=['GET'])
def get_chats():
    all_chats = chats.find()
    return jsonify([chat for chat in all_chats])


@app.route('/chats', methods=['POST'])
def add_chat():
    chat_data = request.json
    result = chats.insert_one(chat_data)
    return jsonify({'_id': str(result.inserted_id)})


@app.route('/chats/<id>', methods=['GET'])
def get_chat(id):
    chat = chats.find_one({'_id': id})
    if chat:
        return jsonify(chat)
    else:
        return jsonify({'error': 'Chat not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8080)

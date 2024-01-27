from flask import Flask, jsonify, request
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
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

db = client.get_database('hoya')
chats = db.chatdb


@app.route('/chats/<id>', methods=['GET'])
def get_chat(id):
    chat = chats.find_one({'_id': id})
    if chat:
        return jsonify(chat)
    else:
        return jsonify({'error': 'Chat not found'}), 404


@app.route('/chats', methods=['POST'])
def create_chat():
    chat_data = request.json
    result = chats.insert_one(chat_data)
    return jsonify({'_id': str(result.inserted_id)})


@app.route('/chats', methods=['PUT'])
def add_message():
    chat_data = request.json
    result = chats.update_one({
        '_id': chat_data['_id']},
        {'$push': {'messages': chat_data['message']}}
    )
    return jsonify({'_id': str(result.inserted_id)})


if __name__ == '__main__':
    app.run(debug=True, port=8080)

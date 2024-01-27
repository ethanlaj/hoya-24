from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

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


def chat_to_json(chat):
    """Convert a chat document to a JSON serializable format."""
    if chat:
        chat['_id'] = str(chat['_id'])
        return chat
    else:
        return None


@app.route('/chats/<id>', methods=['GET'])
def get_chat(id):
    chat = chats.find_one({'_id': ObjectId(id)})
    chat_json = chat_to_json(chat)

    if chat:
        return jsonify(chat_json)
    else:
        return jsonify({'error': 'Chat not found'}), 404


@app.route('/chats', methods=['POST'])
def create_chat():
    result = chats.insert_one({
        'messages': []
    })
    return jsonify({'_id': str(result.inserted_id)})


@app.route('/chats', methods=['PUT'])
def add_message():
    chat_data = request.json

    user_message = {
        'message': chat_data['message'],
        'sender': 'user',
        'createdAt': datetime.now()
    }
    bot_message = {
        'message': "Lorum ipsum dolor sit amet consectetur adipiscing elit. Nulla facilisi cras fermentum odio euismod.",
        'sender': 'bot',
        'createdAt': datetime.now(),
        'link': 'https://www.google.com'
    }

    res = chats.update_one({
        '_id': ObjectId(chat_data['_id'])},
        {'$push': {'messages': {'$each': [user_message, bot_message]}}}
    )
    if (res.modified_count == 0):
        return jsonify({'error': 'Chat not found'}), 404

    return jsonify({
        'user_message': user_message,
        'bot_message': bot_message
    })


if __name__ == '__main__':
    app.run(debug=True, port=8080)

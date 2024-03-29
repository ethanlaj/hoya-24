from flask import Flask, jsonify, request
from flask_cors import CORS
from bson.objectid import ObjectId
from datetime import datetime
from datetime import timedelta
import jwt
from mongodb import db
import os
from gpt import retrieval, generation
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app)

chats = db.chatdb

ACCESS_KEY_SECRET = os.getenv('ACCESS_KEY_SECRET')
REFRESH_KEY_SECRET = os.getenv('REFRESH_KEY_SECRET')


def chat_to_json(chat):
    """Convert a chat document to a JSON serializable format."""
    if chat:
        chat['_id'] = str(chat['_id'])
        return chat
    else:
        return None


@app.route('/chats/<id>', methods=['GET'])
def get_chat(id):
    try:
        bearer_token = request.headers.get("Authorization")
        access_token = bearer_token.split(' ')[1]
        payload = jwt.decode(
            access_token, ACCESS_KEY_SECRET, algorithms=['HS256'])
        id = payload['id']
    except:
        return jsonify({'error': 'Invalid access token'}), 401

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
    id = str(result.inserted_id)

    payload = {
        "id": id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    access_token = jwt.encode(payload, ACCESS_KEY_SECRET, algorithm='HS256')

    payload["exp"] = datetime.utcnow() + timedelta(hours=5)
    refresh_token = jwt.encode(payload, REFRESH_KEY_SECRET, algorithm='HS256')

    return jsonify({
        '_id': str(result.inserted_id),
        'access_token': access_token,
        'refresh_token': refresh_token
    })


@app.route('/chats', methods=['PUT'])
def add_message():
    try:
        bearer_token = request.headers.get("Authorization")
        access_token = bearer_token.split(' ')[1]
        payload = jwt.decode(
            access_token, ACCESS_KEY_SECRET, algorithms=['HS256'])
        id = payload['id']
    except:
        return jsonify({'error': 'Invalid access token'}), 401

    chat_data = request.json
    if (id != chat_data['_id']):
        return jsonify({'error': 'Access denied'}), 403

    context = chat_data.get('context', [])

    user_message = {
        'message': chat_data['message'],
        'sender': 'user',
        'createdAt': datetime.now()
    }

    retrieval_response = retrieval(chat_data['message'], context)

    # In case first model fails, go through with second model anyways
    if retrieval_response is None or retrieval_response['valid'] == True:
        generation_response = generation(chat_data['message'])
        message = "An error occurred. Please try again later."
        if (generation_response is not None):
            message = generation_response

        bot_message = {
            'message': message,
            'sender': 'bot',
            'createdAt': datetime.now(),
        }
    else:
        bot_message = {
            'message': retrieval_response['message'],
            'sender': 'bot',
            'createdAt': datetime.now(),
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


@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json['refresh_token']

    try:
        payload = jwt.decode(
            refresh_token, REFRESH_KEY_SECRET, algorithms=['HS256'])

        payload['exp'] = datetime.utcnow() + \
            timedelta(hours=1)
        access_token = jwt.encode(
            payload, ACCESS_KEY_SECRET, algorithm='HS256')

        payload['exp'] = datetime.utcnow() + \
            timedelta(hours=5)
        refresh_token = jwt.encode(
            payload, REFRESH_KEY_SECRET, algorithm='HS256')

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh token expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid refresh token'}), 403

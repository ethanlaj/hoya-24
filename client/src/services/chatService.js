import axios from 'axios';
import { baseUrl } from '.';

const url = `${baseUrl}/chats`;

export class ChatService {
	static async createChat() {
		const response = await axios.post(url);
		return response.data;
	}

	static async getChat(id) {
		const response = await axios.get(url + `/${id}`);
		return response.data;
	}

	static async addMessage(data) {
		const response = await axios.put(url, data);
		return response.data;
	}
}
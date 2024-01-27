import axios from 'axios';
import { baseUrl } from '.';

const url = `${baseUrl}/chats`;

export class ChatService {
	static async createChat() {
		const response = await axios.post(url);
		return response.data;
	}

	static async createMessage(data) {
		/**
		 * 
		 */

		const response = await axios.put(url, data);
		return response.data;
	}
}
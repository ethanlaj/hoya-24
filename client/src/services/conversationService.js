import axios from 'axios';
import { baseUrl } from '.';

const url = `${baseUrl}/conversations`;

export class ConversationService {
	static async createConversation() {
		const response = await axios.post(url);
		return response.data;
	}
}
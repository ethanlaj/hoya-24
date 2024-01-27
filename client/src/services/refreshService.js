import axios from 'axios';
import { baseUrl } from '.';

const url = `${baseUrl}/refresh`;

export class RefreshService {
	static async refresh(token) {
		const response = await axios.post(url, { refresh_token: token });
		return response.data;
	}
}
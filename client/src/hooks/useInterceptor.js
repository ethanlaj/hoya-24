import { useEffect } from 'react';
import axios from 'axios';
import { RefreshService } from '../services/refreshService';

const useInterceptor = (setIsIniting) => {
	useEffect(() => {
		// Request interceptor
		const requestInterceptor = axios.interceptors.request.use(config => {
			const token = localStorage.getItem('accessToken');
			if (token) {
				config.headers['Authorization'] = `Bearer ${token}`;
			}
			return config;
		}, error => {
			return Promise.reject(error);
		});

		// Response interceptor
		const responseInterceptor = axios.interceptors.response.use(response => {
			return response;
		}, async error => {
			const originalRequest = error.config;
			if (error.response.status === 401 && !originalRequest._retry) {
				originalRequest._retry = true;
				const refreshToken = localStorage.getItem('refreshToken');

				if (!refreshToken) {
					return Promise.reject(error);
				}

				try {
					// Attempt to refresh token
					const response = await RefreshService.refresh(refreshToken);
					localStorage.setItem('accessToken', response.access_token);
					localStorage.setItem('refreshToken', response.refresh_token);
					axios.defaults.headers.common['Authorization'] = `Bearer ${response.access_token}`;

					// Resend the failed request with the new token
					return axios(originalRequest);
				} catch (refreshError) {
					return Promise.reject(refreshError);
				}
			}
			return Promise.reject(error);
		});

		setIsIniting(false);

		// Cleanup function to remove interceptors
		return () => {
			axios.interceptors.request.eject(requestInterceptor);
			axios.interceptors.response.eject(responseInterceptor);
		};
	}, []);
};

export default useInterceptor;

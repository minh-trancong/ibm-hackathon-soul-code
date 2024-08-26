// utils/auth.ts

import axios from 'axios';
import { API_ENDPOINTS } from './apiConfig';

export const signIn = async (username: string, password: string) => {
    try {
        const response = await axios.post(API_ENDPOINTS.SIGNIN, { username, password });
        if (response.status === 200) {
            const token = `${username}-token`;
            localStorage.setItem('authToken', token);
            return true;
        } else {
            return false;
        }
    } catch (error) {
        console.error('Error signing in:', error);
        return false;
    }
};

export const isAuthenticated = () => {
    return !!localStorage.getItem('authToken');
};
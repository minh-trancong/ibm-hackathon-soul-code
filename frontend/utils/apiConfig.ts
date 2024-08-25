// utils/apiConfig.ts

const base_url = 'http://14.225.205.181:8000';
export const API_ENDPOINTS = {
    UPLOAD_DOCUMENT: `${base_url}/documents/`,
    TAGS: `${base_url}/tags`,
    SIGNIN: `${base_url}/auth/`,
    CHAT: `${base_url}/chat`,
    GET_DOCUMENT: `${base_url}/documents`, // Add the chat endpoint here
    GET_CONTENT: `${base_url}/documents/content/`,

    // Add other API endpoints here
};

export const API_DATA = {
    // Add any other related data here
};
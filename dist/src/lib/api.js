"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.animeApi = void 0;
const axios_1 = __importDefault(require("axios"));
// API base URL - change this to your Django backend URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
// Create axios instance
const api = axios_1.default.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});
// API Functions
exports.animeApi = {
    // Get homepage data
    getHomepage: async () => {
        try {
            const response = await api.get('/home/');
            return response.data;
        }
        catch (error) {
            console.error('Error fetching homepage:', error);
            return { success: false, message: 'Failed to fetch homepage data' };
        }
    },
    // Search anime
    searchAnime: async (keyword, page = 1) => {
        try {
            const response = await api.get('/search/', {
                params: { keyword, page }
            });
            return response.data;
        }
        catch (error) {
            console.error('Error searching anime:', error);
            return { success: false, message: 'Failed to search anime' };
        }
    },
    // Get search suggestions
    getSuggestions: async (keyword) => {
        try {
            const response = await api.get('/suggestion/', {
                params: { keyword }
            });
            return response.data;
        }
        catch (error) {
            console.error('Error fetching suggestions:', error);
            return { success: false, message: 'Failed to fetch suggestions' };
        }
    },
    // Get anime details
    getAnimeDetails: async (animeId) => {
        try {
            const response = await api.get(`/anime/${animeId}/`);
            return response.data;
        }
        catch (error) {
            console.error('Error fetching anime details:', error);
            return { success: false, message: 'Failed to fetch anime details' };
        }
    },
    // Get anime list by category
    getAnimeList: async (query, category, page = 1) => {
        try {
            const url = category ? `/animes/${query}/${category}/` : `/animes/${query}/`;
            const response = await api.get(url, {
                params: { page }
            });
            return response.data;
        }
        catch (error) {
            console.error('Error fetching anime list:', error);
            return { success: false, message: 'Failed to fetch anime list' };
        }
    },
    // Get episodes
    getEpisodes: async (animeId) => {
        try {
            const response = await api.get(`/episodes/${animeId}/`);
            return response.data;
        }
        catch (error) {
            console.error('Error fetching episodes:', error);
            return { success: false, message: 'Failed to fetch episodes' };
        }
    },
    // Get servers
    getServers: async (episodeId) => {
        try {
            const response = await api.get('/servers/', {
                params: { id: episodeId }
            });
            return response.data;
        }
        catch (error) {
            console.error('Error fetching servers:', error);
            return { success: false, message: 'Failed to fetch servers' };
        }
    },
    // Get streaming links
    getStreamingLinks: async (episodeId, server, type) => {
        try {
            const response = await api.get('/stream/', {
                params: { id: episodeId, server, type }
            });
            return response.data;
        }
        catch (error) {
            console.error('Error fetching streaming links:', error);
            return { success: false, message: 'Failed to fetch streaming links' };
        }
    },
    // Get genres
    getGenres: async () => {
        try {
            const response = await api.get('/genres/');
            return response.data;
        }
        catch (error) {
            console.error('Error fetching genres:', error);
            return { success: false, message: 'Failed to fetch genres' };
        }
    },
};
exports.default = api;

"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.animeApi = void 0;
const axios_1 = __importDefault(require("axios"));
const mockApi_1 = require("./mockApi");
// API base URL - change this to your Django backend URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
// Create axios instance
const api = axios_1.default.create({
    baseURL: API_BASE_URL,
    timeout: 10000, // Reduced timeout for faster fallback
    headers: {
        'Content-Type': 'application/json',
    },
});
// Helper function to check if backend is available
const isBackendAvailable = async () => {
    try {
        const response = await api.get('/', { timeout: 5000 });
        return response.status === 200;
    }
    catch {
        return false;
    }
};
// Flag to cache backend availability
let backendAvailable = null;
// API Functions
exports.animeApi = {
    // Get homepage data
    getHomepage: async () => {
        try {
            // Check backend availability if not cached
            if (backendAvailable === null) {
                backendAvailable = await isBackendAvailable();
            }
            if (backendAvailable) {
                const response = await api.get('/home/');
                return response.data;
            }
            else {
                // Fallback to mock API
                return await mockApi_1.mockAnimeApi.getHomepage();
            }
        }
        catch (error) {
            console.error('Error fetching homepage:', error);
            // Fallback to mock API on error
            return await mockApi_1.mockAnimeApi.getHomepage();
        }
    },
    // Search anime
    searchAnime: async (keyword, page = 1) => {
        try {
            if (backendAvailable === null) {
                backendAvailable = await isBackendAvailable();
            }
            if (backendAvailable) {
                const response = await api.get('/search/', {
                    params: { keyword, page }
                });
                return response.data;
            }
            else {
                // Fallback to mock API
                return await mockApi_1.mockAnimeApi.searchAnime(keyword, page);
            }
        }
        catch (error) {
            console.error('Error searching anime:', error);
            // Fallback to mock API on error
            return await mockApi_1.mockAnimeApi.searchAnime(keyword, page);
        }
    },
    // Get search suggestions
    getSuggestions: async (keyword) => {
        try {
            if (backendAvailable === null) {
                backendAvailable = await isBackendAvailable();
            }
            if (backendAvailable) {
                const response = await api.get('/suggestion/', {
                    params: { keyword }
                });
                return response.data;
            }
            else {
                // Fallback to mock API
                return await mockApi_1.mockAnimeApi.getSuggestions(keyword);
            }
        }
        catch (error) {
            console.error('Error fetching suggestions:', error);
            // Fallback to mock API on error
            return await mockApi_1.mockAnimeApi.getSuggestions(keyword);
        }
    },
    // Get anime details
    getAnimeDetails: async (animeId) => {
        try {
            if (backendAvailable === null) {
                backendAvailable = await isBackendAvailable();
            }
            if (backendAvailable) {
                const response = await api.get(`/anime/${animeId}/`);
                return response.data;
            }
            else {
                // Fallback to mock API
                return await mockApi_1.mockAnimeApi.getAnimeDetails(animeId);
            }
        }
        catch (error) {
            console.error('Error fetching anime details:', error);
            // Fallback to mock API on error
            return await mockApi_1.mockAnimeApi.getAnimeDetails(animeId);
        }
    },
    // Get anime list by category
    getAnimeList: async (query, category, page = 1) => {
        try {
            if (backendAvailable === null) {
                backendAvailable = await isBackendAvailable();
            }
            if (backendAvailable) {
                const url = category ? `/animes/${query}/${category}/` : `/animes/${query}/`;
                const response = await api.get(url, {
                    params: { page }
                });
                return response.data;
            }
            else {
                // Fallback to mock API
                return await mockApi_1.mockAnimeApi.getAnimeList(query, category, page);
            }
        }
        catch (error) {
            console.error('Error fetching anime list:', error);
            // Fallback to mock API on error
            return await mockApi_1.mockAnimeApi.getAnimeList(query, category, page);
        }
    },
    // Get episodes
    getEpisodes: async (animeId) => {
        try {
            if (backendAvailable === null) {
                backendAvailable = await isBackendAvailable();
            }
            if (backendAvailable) {
                const response = await api.get(`/episodes/${animeId}/`);
                return response.data;
            }
            else {
                // Fallback to mock API
                return await mockApi_1.mockAnimeApi.getEpisodes(animeId);
            }
        }
        catch (error) {
            console.error('Error fetching episodes:', error);
            // Fallback to mock API on error
            return await mockApi_1.mockAnimeApi.getEpisodes(animeId);
        }
    },
    // Get servers
    getServers: async (episodeId) => {
        try {
            if (backendAvailable === null) {
                backendAvailable = await isBackendAvailable();
            }
            if (backendAvailable) {
                const response = await api.get('/servers/', {
                    params: { id: episodeId }
                });
                return response.data;
            }
            else {
                // Mock servers data
                return {
                    success: true,
                    data: [
                        { name: "HD-1", serverId: "hd1" },
                        { name: "HD-2", serverId: "hd2" },
                        { name: "Server X", serverId: "serverx" }
                    ]
                };
            }
        }
        catch (error) {
            console.error('Error fetching servers:', error);
            // Mock servers data on error
            return {
                success: true,
                data: [
                    { name: "HD-1", serverId: "hd1" },
                    { name: "HD-2", serverId: "hd2" },
                    { name: "Server X", serverId: "serverx" }
                ]
            };
        }
    },
    // Get streaming links
    getStreamingLinks: async (episodeId, server, type) => {
        try {
            if (backendAvailable === null) {
                backendAvailable = await isBackendAvailable();
            }
            if (backendAvailable) {
                const response = await api.get('/stream/', {
                    params: { id: episodeId, server, type }
                });
                return response.data;
            }
            else {
                // Mock streaming data
                return {
                    success: true,
                    data: {
                        sources: [
                            {
                                file: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                                type: "video/mp4",
                                label: "720p"
                            }
                        ],
                        server: server
                    }
                };
            }
        }
        catch (error) {
            console.error('Error fetching streaming links:', error);
            // Mock streaming data on error
            return {
                success: true,
                data: {
                    sources: [
                        {
                            file: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                            type: "video/mp4",
                            label: "720p"
                        }
                    ],
                    server: server
                }
            };
        }
    },
    // Get genres
    getGenres: async () => {
        try {
            if (backendAvailable === null) {
                backendAvailable = await isBackendAvailable();
            }
            if (backendAvailable) {
                const response = await api.get('/genres/');
                return response.data;
            }
            else {
                // Fallback to mock API
                return await mockApi_1.mockAnimeApi.getGenres();
            }
        }
        catch (error) {
            console.error('Error fetching genres:', error);
            // Fallback to mock API on error
            return await mockApi_1.mockAnimeApi.getGenres();
        }
    },
};
exports.default = api;

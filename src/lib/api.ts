import axios from 'axios';
import { mockAnimeApi } from './mockApi';

// API base URL - change this to your Django backend URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // Reduced timeout for faster fallback
  headers: {
    'Content-Type': 'application/json',
  },
});

// Helper function to check if backend is available
const isBackendAvailable = async (): Promise<boolean> => {
  try {
    const response = await api.get('/', { timeout: 5000 });
    return response.status === 200;
  } catch {
    return false;
  }
};

// Flag to cache backend availability
let backendAvailable: boolean | null = null;

// Types
export interface Anime {
  id: string;
  title: string;
  alternativeTitle?: string;
  poster: string;
  type: 'TV' | 'Movie' | 'OVA' | 'ONA' | 'Special';
  duration: string;
  episodes: {
    sub: number | null;
    dub: number | null;
    eps: number;
  };
  rating?: number;
  status?: string;
  genres?: string[];
  description?: string;
}

export interface PageInfo {
  totalPages: number;
  currentPage: number;
  hasNextPage: boolean;
}

export interface SearchResponse {
  pageInfo: PageInfo;
  response: Anime[];
}

export interface HomepageData {
  spotlight: Anime[];
  trending: Anime[];
  topAiring: Anime[];
  mostPopular: Anime[];
  mostFavorite: Anime[];
  latestEpisode: Anime[];
  topUpcoming: Anime[];
  genres: string[];
}

export interface Episode {
  id: string;
  number: number;
  title: string;
  poster?: string;
  duration?: string;
  sub?: boolean;
  dub?: boolean;
  fillers?: boolean;
}

export interface AnimeDetails {
  id: string;
  title: string;
  alternativeTitle?: string;
  poster: string;
  type: 'TV' | 'Movie' | 'OVA' | 'ONA' | 'Special';
  duration: string;
  quality: string;
  releaseDate: string;
  status: 'Airing' | 'Completed' | 'Upcoming' | 'Cancelled';
  malId?: string;
  anilistId?: string;
  episodes?: {
    sub: number | null;
    dub: number | null;
    eps: number;
  };
  synopsis: string;
  genres: string[];
  episodesList?: Episode[];
}

export interface Server {
  name: string;
  serverId: string;
}

export interface StreamingLink {
  sources: {
    file: string;
    type: string;
    label?: string;
  }[];
  tracks?: any[];
  server: string;
}

// API Functions
export const animeApi = {
  // Get homepage data
  getHomepage: async (): Promise<{ success: boolean; data?: HomepageData; message?: string }> => {
    try {
      // Check backend availability if not cached
      if (backendAvailable === null) {
        backendAvailable = await isBackendAvailable();
      }
      
      if (backendAvailable) {
        const response = await api.get('/home/');
        return response.data;
      } else {
        // Fallback to mock API
        return await mockAnimeApi.getHomepage();
      }
    } catch (error) {
      console.error('Error fetching homepage:', error);
      // Fallback to mock API on error
      return await mockAnimeApi.getHomepage();
    }
  },

  // Search anime
  searchAnime: async (keyword: string, page: number = 1): Promise<{ success: boolean; data?: SearchResponse; message?: string }> => {
    try {
      if (backendAvailable === null) {
        backendAvailable = await isBackendAvailable();
      }
      
      if (backendAvailable) {
        const response = await api.get('/search/', {
          params: { keyword, page }
        });
        return response.data;
      } else {
        // Fallback to mock API
        return await mockAnimeApi.searchAnime(keyword, page);
      }
    } catch (error) {
      console.error('Error searching anime:', error);
      // Fallback to mock API on error
      return await mockAnimeApi.searchAnime(keyword, page);
    }
  },

  // Get search suggestions
  getSuggestions: async (keyword: string): Promise<{ success: boolean; data?: string[]; message?: string }> => {
    try {
      if (backendAvailable === null) {
        backendAvailable = await isBackendAvailable();
      }
      
      if (backendAvailable) {
        const response = await api.get('/suggestion/', {
          params: { keyword }
        });
        return response.data;
      } else {
        // Fallback to mock API
        return await mockAnimeApi.getSuggestions(keyword);
      }
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      // Fallback to mock API on error
      return await mockAnimeApi.getSuggestions(keyword);
    }
  },

  // Get anime details
  getAnimeDetails: async (animeId: string): Promise<{ success: boolean; data?: AnimeDetails; message?: string }> => {
    try {
      if (backendAvailable === null) {
        backendAvailable = await isBackendAvailable();
      }
      
      if (backendAvailable) {
        const response = await api.get(`/anime/${animeId}/`);
        return response.data;
      } else {
        // Fallback to mock API
        return await mockAnimeApi.getAnimeDetails(animeId);
      }
    } catch (error) {
      console.error('Error fetching anime details:', error);
      // Fallback to mock API on error
      return await mockAnimeApi.getAnimeDetails(animeId);
    }
  },

  // Get anime list by category
  getAnimeList: async (query: string, category?: string, page: number = 1): Promise<{ success: boolean; data?: SearchResponse; message?: string }> => {
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
      } else {
        // Fallback to mock API
        return await mockAnimeApi.getAnimeList(query, category, page);
      }
    } catch (error) {
      console.error('Error fetching anime list:', error);
      // Fallback to mock API on error
      return await mockAnimeApi.getAnimeList(query, category, page);
    }
  },

  // Get episodes
  getEpisodes: async (animeId: string): Promise<{ success: boolean; data?: Episode[]; message?: string }> => {
    try {
      if (backendAvailable === null) {
        backendAvailable = await isBackendAvailable();
      }
      
      if (backendAvailable) {
        const response = await api.get(`/episodes/${animeId}/`);
        return response.data;
      } else {
        // Fallback to mock API
        return await mockAnimeApi.getEpisodes(animeId);
      }
    } catch (error) {
      console.error('Error fetching episodes:', error);
      // Fallback to mock API on error
      return await mockAnimeApi.getEpisodes(animeId);
    }
  },

  // Get servers
  getServers: async (episodeId: string): Promise<{ success: boolean; data?: Server[]; message?: string }> => {
    try {
      if (backendAvailable === null) {
        backendAvailable = await isBackendAvailable();
      }
      
      if (backendAvailable) {
        const response = await api.get('/servers/', {
          params: { id: episodeId }
        });
        return response.data;
      } else {
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
    } catch (error) {
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
  getStreamingLinks: async (episodeId: string, server: string, type: 'sub' | 'dub'): Promise<{ success: boolean; data?: StreamingLink; message?: string }> => {
    try {
      if (backendAvailable === null) {
        backendAvailable = await isBackendAvailable();
      }
      
      if (backendAvailable) {
        const response = await api.get('/stream/', {
          params: { id: episodeId, server, type }
        });
        return response.data;
      } else {
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
    } catch (error) {
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
  getGenres: async (): Promise<{ success: boolean; data?: string[]; message?: string }> => {
    try {
      if (backendAvailable === null) {
        backendAvailable = await isBackendAvailable();
      }
      
      if (backendAvailable) {
        const response = await api.get('/genres/');
        return response.data;
      } else {
        // Fallback to mock API
        return await mockAnimeApi.getGenres();
      }
    } catch (error) {
      console.error('Error fetching genres:', error);
      // Fallback to mock API on error
      return await mockAnimeApi.getGenres();
    }
  },
};

export default api;
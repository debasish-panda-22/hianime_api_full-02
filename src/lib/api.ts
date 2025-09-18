import axios from 'axios';

// API base URL - change this to your Django backend URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
      const response = await api.get('/home/');
      return response.data;
    } catch (error) {
      console.error('Error fetching homepage:', error);
      return { success: false, message: 'Failed to fetch homepage data' };
    }
  },

  // Search anime
  searchAnime: async (keyword: string, page: number = 1): Promise<{ success: boolean; data?: SearchResponse; message?: string }> => {
    try {
      const response = await api.get('/search/', {
        params: { keyword, page }
      });
      return response.data;
    } catch (error) {
      console.error('Error searching anime:', error);
      return { success: false, message: 'Failed to search anime' };
    }
  },

  // Get search suggestions
  getSuggestions: async (keyword: string): Promise<{ success: boolean; data?: string[]; message?: string }> => {
    try {
      const response = await api.get('/suggestion/', {
        params: { keyword }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      return { success: false, message: 'Failed to fetch suggestions' };
    }
  },

  // Get anime details
  getAnimeDetails: async (animeId: string): Promise<{ success: boolean; data?: AnimeDetails; message?: string }> => {
    try {
      const response = await api.get(`/anime/${animeId}/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching anime details:', error);
      return { success: false, message: 'Failed to fetch anime details' };
    }
  },

  // Get anime list by category
  getAnimeList: async (query: string, category?: string, page: number = 1): Promise<{ success: boolean; data?: SearchResponse; message?: string }> => {
    try {
      const url = category ? `/animes/${query}/${category}/` : `/animes/${query}/`;
      const response = await api.get(url, {
        params: { page }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching anime list:', error);
      return { success: false, message: 'Failed to fetch anime list' };
    }
  },

  // Get episodes
  getEpisodes: async (animeId: string): Promise<{ success: boolean; data?: Episode[]; message?: string }> => {
    try {
      const response = await api.get(`/episodes/${animeId}/`);
      return response.data;
    } catch (error) {
      console.error('Error fetching episodes:', error);
      return { success: false, message: 'Failed to fetch episodes' };
    }
  },

  // Get servers
  getServers: async (episodeId: string): Promise<{ success: boolean; data?: Server[]; message?: string }> => {
    try {
      const response = await api.get('/servers/', {
        params: { id: episodeId }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching servers:', error);
      return { success: false, message: 'Failed to fetch servers' };
    }
  },

  // Get streaming links
  getStreamingLinks: async (episodeId: string, server: string, type: 'sub' | 'dub'): Promise<{ success: boolean; data?: StreamingLink; message?: string }> => {
    try {
      const response = await api.get('/stream/', {
        params: { id: episodeId, server, type }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching streaming links:', error);
      return { success: false, message: 'Failed to fetch streaming links' };
    }
  },

  // Get genres
  getGenres: async (): Promise<{ success: boolean; data?: string[]; message?: string }> => {
    try {
      const response = await api.get('/genres/');
      return response.data;
    } catch (error) {
      console.error('Error fetching genres:', error);
      return { success: false, message: 'Failed to fetch genres' };
    }
  },
};

export default api;
import { useState, useEffect } from 'react';
import { animeApi, HomepageData, Anime, SearchResponse } from '@/lib/api';

export const useHomepageData = () => {
  const [data, setData] = useState<HomepageData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await animeApi.getHomepage();
        
        if (response.success && response.data) {
          setData(response.data);
        } else {
          setError(response.message || 'Failed to fetch homepage data');
        }
      } catch (err) {
        setError('An unexpected error occurred');
        console.error('Homepage data fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
};

export const useSearchAnime = (keyword: string, page: number = 1) => {
  const [data, setData] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!keyword.trim()) {
      setData(null);
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await animeApi.searchAnime(keyword, page);
        
        if (response.success && response.data) {
          setData(response.data);
        } else {
          setError(response.message || 'Failed to search anime');
        }
      } catch (err) {
        setError('An unexpected error occurred');
        console.error('Search error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [keyword, page]);

  return { data, loading, error };
};

export const useAnimeList = (query: string, category?: string, page: number = 1) => {
  const [data, setData] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await animeApi.getAnimeList(query, category, page);
        
        if (response.success && response.data) {
          setData(response.data);
        } else {
          setError(response.message || 'Failed to fetch anime list');
        }
      } catch (err) {
        setError('An unexpected error occurred');
        console.error('Anime list error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [query, category, page]);

  return { data, loading, error };
};

export const useSuggestions = (keyword: string) => {
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!keyword.trim()) {
      setSuggestions([]);
      return;
    }

    const fetchSuggestions = async () => {
      try {
        setLoading(true);
        const response = await animeApi.getSuggestions(keyword);
        
        if (response.success && response.data) {
          setSuggestions(response.data);
        } else {
          setSuggestions([]);
        }
      } catch (err) {
        console.error('Suggestions error:', err);
        setSuggestions([]);
      } finally {
        setLoading(false);
      }
    };

    const debounceTimer = setTimeout(fetchSuggestions, 300);
    return () => clearTimeout(debounceTimer);
  }, [keyword]);

  return { suggestions, loading };
};
from django.conf import settings

class AnimeAPIConfig:
    """Configuration class for Anime API settings"""
    
    @property
    def base_url(self):
        return getattr(settings, 'ANIME_API_BASE_URL', 'https://hianime.bz')
    
    @property
    def base_url_v2(self):
        return getattr(settings, 'ANIME_API_BASE_URL_V2', 'https://kaido.to')
    
    @property
    def providers_url(self):
        return getattr(settings, 'ANIME_API_PROVIDERS', 'https://megacloud.club')
    
    @property
    def headers(self):
        return getattr(settings, 'REQUEST_HEADERS', {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
        })
    
    @property
    def timeout(self):
        return getattr(settings, 'REQUEST_TIMEOUT', 30)
    
    @property
    def cache_timeout(self):
        return getattr(settings, 'CACHE_TIMEOUT', 3600)

# Global config instance
config = AnimeAPIConfig()
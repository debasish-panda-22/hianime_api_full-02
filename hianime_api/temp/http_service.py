import requests
from requests.exceptions import RequestException, Timeout
from django.core.cache import cache
from django.conf import settings
import logging
from .config import config

logger = logging.getLogger(__name__)

class HTTPService:
    """Service for making HTTP requests to anime websites"""
    
    def __init__(self):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(self.config.headers)
    
    def get(self, endpoint, use_cache=True, cache_key=None, timeout=None):
        """
        Make GET request to the anime website
        
        Args:
            endpoint (str): API endpoint
            use_cache (bool): Whether to use caching
            cache_key (str): Custom cache key
            timeout (int): Request timeout in seconds
            
        Returns:
            dict: Response data with success flag
        """
        if timeout is None:
            timeout = self.config.timeout
            
        url = f"{self.config.base_url}{endpoint}"
        
        # Use caching if enabled
        if use_cache:
            if cache_key is None:
                cache_key = f"anime_api:{endpoint}"
            
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info(f"Cache hit for: {cache_key}")
                return cached_data
        
        try:
            logger.info(f"Making request to: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            result = {
                'success': True,
                'data': response.text,
                'status_code': response.status_code
            }
            
            # Cache the result if successful
            if use_cache and result['success']:
                cache.set(cache_key, result, self.config.cache_timeout)
                logger.info(f"Cached result for: {cache_key}")
            
            return result
            
        except Timeout:
            logger.error(f"Request timeout for: {url}")
            return {
                'success': False,
                'message': 'Request timeout',
                'error': 'timeout'
            }
        except RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            return {
                'success': False,
                'message': str(e),
                'error': 'request_error'
            }
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            return {
                'success': False,
                'message': 'Unexpected error',
                'error': 'unexpected_error'
            }
    
    def get_v2(self, endpoint, use_cache=True, cache_key=None, timeout=None):
        """
        Make GET request to the v2 anime website
        
        Args:
            endpoint (str): API endpoint
            use_cache (bool): Whether to use caching
            cache_key (str): Custom cache key
            timeout (int): Request timeout in seconds
            
        Returns:
            dict: Response data with success flag
        """
        if timeout is None:
            timeout = self.config.timeout
            
        url = f"{self.config.base_url_v2}{endpoint}"
        
        # Use caching if enabled
        if use_cache:
            if cache_key is None:
                cache_key = f"anime_api_v2:{endpoint}"
            
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info(f"Cache hit for: {cache_key}")
                return cached_data
        
        try:
            logger.info(f"Making request to: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            result = {
                'success': True,
                'data': response.text,
                'status_code': response.status_code
            }
            
            # Cache the result if successful
            if use_cache and result['success']:
                cache.set(cache_key, result, self.config.cache_timeout)
                logger.info(f"Cached result for: {cache_key}")
            
            return result
            
        except Timeout:
            logger.error(f"Request timeout for: {url}")
            return {
                'success': False,
                'message': 'Request timeout',
                'error': 'timeout'
            }
        except RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            return {
                'success': False,
                'message': str(e),
                'error': 'request_error'
            }
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            return {
                'success': False,
                'message': 'Unexpected error',
                'error': 'unexpected_error'
            }

# Global HTTP service instance
http_service = HTTPService()
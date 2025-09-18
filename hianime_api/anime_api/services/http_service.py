import requests
from requests.exceptions import RequestException, Timeout
from django.core.cache import cache
from django.conf import settings
import logging
import time
import random
from .config import config

logger = logging.getLogger(__name__)

class HTTPService:
    """Service for making HTTP requests to anime websites"""
    
    def __init__(self):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(self.config.headers)
    
    def get(self, endpoint, use_cache=True, cache_key=None, timeout=None, max_retries=3):
        """
        Make GET request to the anime website with retry logic
        
        Args:
            endpoint (str): API endpoint
            use_cache (bool): Whether to use caching
            cache_key (str): Custom cache key
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum number of retry attempts
            
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
        
        # Retry logic
        for attempt in range(max_retries + 1):
            try:
                # Add random delay to avoid rate limiting
                if attempt > 0:
                    delay = min(2 ** attempt + random.random(), 10)  # Exponential backoff
                    time.sleep(delay)
                    logger.info(f"Retry attempt {attempt} for: {url}")
                
                logger.info(f"Making request to: {url}")
                
                # Rotate user agent for each attempt
                user_agents = [
                    'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'
                ]
                
                headers = self.session.headers.copy()
                headers['User-Agent'] = random.choice(user_agents)
                headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                headers['Accept-Language'] = 'en-US,en;q=0.5'
                headers['Accept-Encoding'] = 'gzip, deflate'
                headers['Connection'] = 'keep-alive'
                headers['Upgrade-Insecure-Requests'] = '1'
                
                response = self.session.get(url, timeout=timeout, headers=headers)
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
                logger.error(f"Request timeout for: {url} (attempt {attempt + 1}/{max_retries + 1})")
                if attempt == max_retries:
                    return {
                        'success': False,
                        'message': 'Request timeout after multiple attempts',
                        'error': 'timeout'
                    }
                    
            except RequestException as e:
                logger.error(f"Request failed for {url}: {str(e)} (attempt {attempt + 1}/{max_retries + 1})")
                if attempt == max_retries:
                    return {
                        'success': False,
                        'message': str(e),
                        'error': 'request_error'
                    }
                    
            except Exception as e:
                logger.error(f"Unexpected error for {url}: {str(e)} (attempt {attempt + 1}/{max_retries + 1})")
                if attempt == max_retries:
                    return {
                        'success': False,
                        'message': 'Unexpected error after multiple attempts',
                        'error': 'unexpected_error'
                    }
    
    def get_v2(self, endpoint, use_cache=True, cache_key=None, timeout=None, max_retries=3):
        """
        Make GET request to the v2 anime website with retry logic
        
        Args:
            endpoint (str): API endpoint
            use_cache (bool): Whether to use caching
            cache_key (str): Custom cache key
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum number of retry attempts
            
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
        
        # Retry logic
        for attempt in range(max_retries + 1):
            try:
                # Add random delay to avoid rate limiting
                if attempt > 0:
                    delay = min(2 ** attempt + random.random(), 10)  # Exponential backoff
                    time.sleep(delay)
                    logger.info(f"Retry attempt {attempt} for: {url}")
                
                logger.info(f"Making request to: {url}")
                
                # Rotate user agent for each attempt
                user_agents = [
                    'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'
                ]
                
                headers = self.session.headers.copy()
                headers['User-Agent'] = random.choice(user_agents)
                headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                headers['Accept-Language'] = 'en-US,en;q=0.5'
                headers['Accept-Encoding'] = 'gzip, deflate'
                headers['Connection'] = 'keep-alive'
                headers['Upgrade-Insecure-Requests'] = '1'
                
                response = self.session.get(url, timeout=timeout, headers=headers)
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
                logger.error(f"Request timeout for: {url} (attempt {attempt + 1}/{max_retries + 1})")
                if attempt == max_retries:
                    return {
                        'success': False,
                        'message': 'Request timeout after multiple attempts',
                        'error': 'timeout'
                    }
                    
            except RequestException as e:
                logger.error(f"Request failed for {url}: {str(e)} (attempt {attempt + 1}/{max_retries + 1})")
                if attempt == max_retries:
                    return {
                        'success': False,
                        'message': str(e),
                        'error': 'request_error'
                    }
                    
            except Exception as e:
                logger.error(f"Unexpected error for {url}: {str(e)} (attempt {attempt + 1}/{max_retries + 1})")
                if attempt == max_retries:
                    return {
                        'success': False,
                        'message': 'Unexpected error after multiple attempts',
                        'error': 'unexpected_error'
                    }

# Global HTTP service instance
http_service = HTTPService()
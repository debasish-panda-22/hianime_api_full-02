from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
import logging

from ..services import http_service
from ..services.fallback_service import fallback_service
from ..extractors import search_extractor

logger = logging.getLogger(__name__)

class AnimeListAPIView(APIView):
    """API endpoint for fetching anime lists"""
    
    VALID_QUERIES = {
        'top-airing': {'has_category': False},
        'most-popular': {'has_category': False},
        'most-favorite': {'has_category': False},
        'completed': {'has_category': False},
        'recently-added': {'has_category': False},
        'recently-updated': {'has_category': False},
        'top-upcoming': {'has_category': False},
        'genre': {'has_category': True, 'category': 'all genres'},
        'az-list': {'has_category': True, 'category': '0-9,all,a-z'},
        'subbed-anime': {'has_category': False},
        'dubbed-anime': {'has_category': False},
        'movie': {'has_category': False},
        'tv': {'has_category': False},
        'ova': {'has_category': False},
        'ona': {'has_category': False},
        'special': {'has_category': False},
        'events': {'has_category': False}
    }
    
    @extend_schema(
        summary="Get Anime List",
        description="Retrieve anime lists by category and query type",
        parameters=[
            {
                'name': 'query',
                'description': 'Query type (e.g., top-airing, most-popular, genre, etc.)',
                'required': True,
                'type': OpenApiTypes.STR,
                'in': 'path'
            },
            {
                'name': 'category',
                'description': 'Category (required for some query types)',
                'required': False,
                'type': OpenApiTypes.STR,
                'in': 'path'
            },
            {
                'name': 'page',
                'description': 'Page number',
                'required': False,
                'type': OpenApiTypes.INT,
                'in': 'query',
                'default': 1
            }
        ],
        responses={200: dict}
    )
    @method_decorator(ratelimit(key='ip', rate='100/h'))
    def get(self, request, query, category=None):
        """
        Get anime lists by category and query type
        """
        try:
            page = request.query_params.get('page', '1')
            
            # Validate query
            if query not in self.VALID_QUERIES:
                return Response({
                    'success': False,
                    'message': f'Invalid query type: {query}',
                    'error': 'invalid_query'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            query_config = self.VALID_QUERIES[query]
            
            # Check if category is required
            if query_config['has_category'] and not category:
                return Response({
                    'success': False,
                    'message': f'Category is required for query type: {query}',
                    'error': 'missing_category'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate category if provided
            if category and query_config['has_category']:
                valid_categories = query_config['category'].split(',')
                if category not in valid_categories:
                    return Response({
                        'success': False,
                        'message': f'Invalid category for query type {query}. Valid categories: {query_config["category"]}',
                        'error': 'invalid_category'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                page = int(page)
                if page < 1:
                    page = 1
            except ValueError:
                return Response({
                    'success': False,
                    'message': 'Page parameter must be a valid number',
                    'error': 'invalid_parameter'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Construct endpoint URL
            if query_config['has_category']:
                endpoint = f'/{query}/{category}?page={page}'
            else:
                endpoint = f'/{query}?page={page}'
            
            # Make request to list page
            result = http_service.get(endpoint)
            
            if not result['success']:
                logger.error(f"Failed to fetch anime list for {query}: {result['message']}")
                return Response({
                    'success': False,
                    'message': result['message'],
                    'error': result.get('error', 'unknown_error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Extract data from HTML
            extracted_data = search_extractor.extract_search_results(result['data'])
            
            return Response({
                'success': True,
                'data': extracted_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in anime list view for {query}: {str(e)}")
            return Response({
                'success': False,
                'message': 'An unexpected error occurred',
                'error': 'unexpected_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GenresAPIView(APIView):
    """API endpoint for fetching all genres"""
    
    @extend_schema(
        summary="Get All Genres",
        description="Retrieve list of all available anime genres",
        responses={200: dict}
    )
    @method_decorator(ratelimit(key='ip', rate='100/h'))
    def get(self, request):
        """
        Get list of all available anime genres
        """
        try:
            # Make request to homepage to extract genres
            result = http_service.get('/home')
            
            if not result['success']:
                logger.warning(f"External API failed, using fallback genres data: {result['message']}")
                # Use fallback data when external API fails
                fallback_data = fallback_service.get_genres_data()
                return Response({
                    'success': True,
                    'data': fallback_data,
                    'source': 'fallback',
                    'message': 'Using fallback data due to external API unavailability'
                }, status=status.HTTP_200_OK)
            
            # Extract genres from homepage data
            from ..extractors.homepage_extractor import HomepageExtractor
            temp_extractor = HomepageExtractor()
            homepage_data = temp_extractor.extract(result['data'])
            
            return Response({
                'success': True,
                'data': homepage_data.get('genres', []),
                'source': 'external'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in genres view: {str(e)}")
            # Use fallback data when there's an exception
            try:
                fallback_data = fallback_service.get_genres_data()
                return Response({
                    'success': True,
                    'data': fallback_data,
                    'source': 'fallback',
                    'message': 'Using fallback data due to unexpected error'
                }, status=status.HTTP_200_OK)
            except Exception as fallback_error:
                logger.error(f"Fallback data also failed: {str(fallback_error)}")
                return Response({
                    'success': False,
                    'message': 'An unexpected error occurred',
                    'error': 'unexpected_error'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
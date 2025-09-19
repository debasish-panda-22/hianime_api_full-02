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

class SearchAPIView(APIView):
    """API endpoint for searching anime"""
    
    @extend_schema(
        summary="Search Anime",
        description="Search for anime by keyword",
        parameters=[
            {
                'name': 'keyword',
                'description': 'Search keyword',
                'required': True,
                'type': OpenApiTypes.STR,
                'in': 'query'
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
    def get(self, request):
        """
        Search for anime by keyword
        """
        try:
            keyword = request.query_params.get('keyword', '').strip()
            page = request.query_params.get('page', '1')
            
            if not keyword:
                return Response({
                    'success': False,
                    'message': 'Keyword parameter is required',
                    'error': 'missing_parameter'
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
            
            # Make request to search page
            result = http_service.get(f'/search?keyword={keyword}&page={page}')
            
            if not result['success']:
                logger.warning(f"External API failed, using fallback search data for '{keyword}': {result['message']}")
                # Use fallback data when external API fails
                fallback_data = fallback_service.get_search_results(keyword)
                return Response({
                    'success': True,
                    'data': fallback_data,
                    'source': 'fallback',
                    'message': 'Using fallback data due to external API unavailability'
                }, status=status.HTTP_200_OK)
            
            # Extract data from HTML
            extracted_data = search_extractor.extract_search_results(result['data'])
            
            return Response({
                'success': True,
                'data': extracted_data,
                'source': 'external'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in search view: {str(e)}")
            # Use fallback data when there's an exception
            try:
                fallback_data = fallback_service.get_search_results(keyword)
                return Response({
                    'success': True,
                    'data': fallback_data,
                    'source': 'fallback',
                    'message': 'Using fallback data due to unexpected error'
                }, status=status.HTTP_200_OK)
            except Exception as fallback_error:
                logger.error(f"Fallback data also failed for '{keyword}': {str(fallback_error)}")
                return Response({
                    'success': False,
                    'message': 'An unexpected error occurred',
                    'error': 'unexpected_error'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SuggestionAPIView(APIView):
    """API endpoint for getting search suggestions"""
    
    @extend_schema(
        summary="Get Search Suggestions",
        description="Get search suggestions for a keyword",
        parameters=[
            {
                'name': 'keyword',
                'description': 'Search keyword',
                'required': True,
                'type': OpenApiTypes.STR,
                'in': 'query'
            }
        ],
        responses={200: dict}
    )
    @method_decorator(ratelimit(key='ip', rate='100/h'))
    def get(self, request):
        """
        Get search suggestions for a keyword
        """
        try:
            keyword = request.query_params.get('keyword', '').strip()
            
            if not keyword:
                return Response({
                    'success': False,
                    'message': 'Keyword parameter is required',
                    'error': 'missing_parameter'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Make request to get suggestions
            result = http_service.get(f'/search/suggestion?keyword={keyword}')
            
            if not result['success']:
                logger.warning(f"External API failed, using fallback suggestions data for '{keyword}': {result['message']}")
                # Use fallback data when external API fails
                fallback_data = fallback_service.get_suggestions_data(keyword)
                return Response({
                    'success': True,
                    'data': fallback_data,
                    'source': 'fallback',
                    'message': 'Using fallback data due to external API unavailability'
                }, status=status.HTTP_200_OK)
            
            # Extract data from HTML
            extracted_data = search_extractor.extract_suggestions(result['data'])
            
            return Response({
                'success': True,
                'data': extracted_data,
                'source': 'external'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in suggestion view: {str(e)}")
            # Use fallback data when there's an exception
            try:
                fallback_data = fallback_service.get_suggestions_data(keyword)
                return Response({
                    'success': True,
                    'data': fallback_data,
                    'source': 'fallback',
                    'message': 'Using fallback data due to unexpected error'
                }, status=status.HTTP_200_OK)
            except Exception as fallback_error:
                logger.error(f"Fallback data also failed for '{keyword}': {str(fallback_error)}")
                return Response({
                    'success': False,
                    'message': 'An unexpected error occurred',
                    'error': 'unexpected_error'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
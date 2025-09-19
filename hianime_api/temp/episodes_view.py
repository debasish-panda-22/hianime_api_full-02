from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
import logging

from ..services import http_service
from ..extractors import episodes_extractor

logger = logging.getLogger(__name__)

class EpisodesAPIView(APIView):
    """API endpoint for fetching anime episodes"""
    
    @extend_schema(
        summary="Get Anime Episodes",
        description="Retrieve list of episodes for a specific anime",
        responses={200: dict}
    )
    @method_decorator(ratelimit(key='ip', rate='100/h'))
    def get(self, request, anime_id):
        """
        Get list of episodes for a specific anime
        """
        try:
            # Make request to episodes page
            result = http_service.get(f'/{anime_id}')
            
            if not result['success']:
                logger.error(f"Failed to fetch episodes for {anime_id}: {result['message']}")
                return Response({
                    'success': False,
                    'message': result['message'],
                    'error': result.get('error', 'unknown_error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Extract data from HTML
            extracted_data = episodes_extractor.extract(result['data'])
            
            return Response({
                'success': True,
                'data': extracted_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in episodes view for {anime_id}: {str(e)}")
            return Response({
                'success': False,
                'message': 'An unexpected error occurred',
                'error': 'unexpected_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
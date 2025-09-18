from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
import logging

from ..services import http_service
from ..services.fallback_service import fallback_service
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
                logger.warning(f"External API failed, using fallback episodes data for {anime_id}: {result['message']}")
                # Use fallback data when external API fails
                fallback_data = fallback_service.get_episodes_data(anime_id)
                return Response({
                    'success': True,
                    'data': fallback_data,
                    'source': 'fallback',
                    'message': 'Using fallback data due to external API unavailability'
                }, status=status.HTTP_200_OK)
            
            # Extract data from HTML
            extracted_data = episodes_extractor.extract(result['data'])
            
            return Response({
                'success': True,
                'data': extracted_data,
                'source': 'external'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in episodes view for {anime_id}: {str(e)}")
            # Use fallback data when there's an exception
            try:
                fallback_data = fallback_service.get_episodes_data(anime_id)
                return Response({
                    'success': True,
                    'data': fallback_data,
                    'source': 'fallback',
                    'message': 'Using fallback data due to unexpected error'
                }, status=status.HTTP_200_OK)
            except Exception as fallback_error:
                logger.error(f"Fallback data also failed for {anime_id}: {str(fallback_error)}")
                return Response({
                    'success': False,
                    'message': 'An unexpected error occurred',
                    'error': 'unexpected_error'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
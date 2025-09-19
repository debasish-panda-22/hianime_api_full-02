from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
import logging

from ..services import http_service
from ..services.fallback_service import fallback_service
from ..extractors import homepage_extractor

logger = logging.getLogger(__name__)

class HomepageAPIView(APIView):
    """API endpoint for fetching homepage data"""
    
    @extend_schema(
        summary="Get Homepage Data",
        description="Retrieve homepage data including spotlight, trending, top airing, and other sections",
        responses={200: dict}
    )
    @method_decorator(ratelimit(key='ip', rate='100/h'))
    def get(self, request):
        """
        Get homepage data including spotlight, trending, top airing, and other sections
        """
        try:
            # Make request to homepage
            result = http_service.get('/home')
            
            if not result['success']:
                logger.warning(f"External API failed, using fallback data: {result['message']}")
                # Use fallback data when external API fails
                fallback_data = fallback_service.get_homepage_data()
                return Response({
                    'success': True,
                    'data': fallback_data,
                    'source': 'fallback',
                    'message': 'Using fallback data due to external API unavailability'
                }, status=status.HTTP_200_OK)
            
            # Extract data from HTML
            extracted_data = homepage_extractor.extract(result['data'])
            
            return Response({
                'success': True,
                'data': extracted_data,
                'source': 'external'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in homepage view: {str(e)}")
            # Use fallback data when there's an exception
            try:
                fallback_data = fallback_service.get_homepage_data()
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
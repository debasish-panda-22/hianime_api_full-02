from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
import logging

from ..services import http_service
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
                logger.error(f"Failed to fetch homepage: {result['message']}")
                return Response({
                    'success': False,
                    'message': result['message'],
                    'error': result.get('error', 'unknown_error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Extract data from HTML
            extracted_data = homepage_extractor.extract(result['data'])
            
            return Response({
                'success': True,
                'data': extracted_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in homepage view: {str(e)}")
            return Response({
                'success': False,
                'message': 'An unexpected error occurred',
                'error': 'unexpected_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
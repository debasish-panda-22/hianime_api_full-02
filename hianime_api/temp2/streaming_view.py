from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
import logging

from ..services import http_service
from ..extractors import servers_extractor, streaming_extractor

logger = logging.getLogger(__name__)

class ServersAPIView(APIView):
    """API endpoint for fetching episode servers"""
    
    @extend_schema(
        summary="Get Episode Servers",
        description="Retrieve available servers for a specific episode",
        parameters=[
            {
                'name': 'id',
                'description': 'Episode ID',
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
        Get available servers for a specific episode
        """
        try:
            episode_id = request.query_params.get('id', '').strip()
            
            if not episode_id:
                return Response({
                    'success': False,
                    'message': 'ID parameter is required',
                    'error': 'missing_parameter'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Make request to episode page
            result = http_service.get(f'/{episode_id}')
            
            if not result['success']:
                logger.error(f"Failed to fetch servers for {episode_id}: {result['message']}")
                return Response({
                    'success': False,
                    'message': result['message'],
                    'error': result.get('error', 'unknown_error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Extract data from HTML
            extracted_data = servers_extractor.extract(result['data'])
            
            return Response({
                'success': True,
                'data': extracted_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in servers view: {str(e)}")
            return Response({
                'success': False,
                'message': 'An unexpected error occurred',
                'error': 'unexpected_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StreamingAPIView(APIView):
    """API endpoint for fetching streaming links"""
    
    @extend_schema(
        summary="Get Streaming Links",
        description="Retrieve streaming links for a specific episode from a specific server",
        parameters=[
            {
                'name': 'id',
                'description': 'Episode ID',
                'required': True,
                'type': OpenApiTypes.STR,
                'in': 'query'
            },
            {
                'name': 'server',
                'description': 'Server name',
                'required': True,
                'type': OpenApiTypes.STR,
                'in': 'query'
            },
            {
                'name': 'type',
                'description': 'Stream type (sub or dub)',
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
        Get streaming links for a specific episode from a specific server
        """
        try:
            episode_id = request.query_params.get('id', '').strip()
            server = request.query_params.get('server', '').strip()
            stream_type = request.query_params.get('type', '').strip().lower()
            
            if not episode_id:
                return Response({
                    'success': False,
                    'message': 'ID parameter is required',
                    'error': 'missing_parameter'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not server:
                return Response({
                    'success': False,
                    'message': 'Server parameter is required',
                    'error': 'missing_parameter'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if stream_type not in ['sub', 'dub']:
                return Response({
                    'success': False,
                    'message': 'Type parameter must be either "sub" or "dub"',
                    'error': 'invalid_parameter'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Make request to streaming page
            result = http_service.get(f'/{episode_id}')
            
            if not result['success']:
                logger.error(f"Failed to fetch streaming links for {episode_id}: {result['message']}")
                return Response({
                    'success': False,
                    'message': result['message'],
                    'error': result.get('error', 'unknown_error')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Extract data from HTML
            extracted_data = streaming_extractor.extract(result['data'], server)
            
            return Response({
                'success': True,
                'data': extracted_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error in streaming view: {str(e)}")
            return Response({
                'success': False,
                'message': 'An unexpected error occurred',
                'error': 'unexpected_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
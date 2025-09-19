from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

class AnimeAPIError(Exception):
    """Base exception for Anime API"""
    def __init__(self, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details=None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

class ValidationError(AnimeAPIError):
    """Validation error"""
    def __init__(self, message, details=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)

class NotFoundError(AnimeAPIError):
    """Not found error"""
    def __init__(self, message, details=None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, details)

class ServiceUnavailableError(AnimeAPIError):
    """Service unavailable error"""
    def __init__(self, message, details=None):
        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE, details)

def api_error_handler(func):
    """Decorator for handling API errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AnimeAPIError as e:
            logger.error(f"AnimeAPIError: {e.message}")
            return Response({
                'success': False,
                'message': e.message,
                'details': e.details
            }, status=e.status_code)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({
                'success': False,
                'message': 'An unexpected error occurred',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper

def success_response(data=None, message="Success"):
    """Create success response"""
    return Response({
        'success': True,
        'data': data,
        'message': message
    })

def error_response(message, status_code=status.HTTP_400_BAD_REQUEST, details=None):
    """Create error response"""
    return Response({
        'success': False,
        'message': message,
        'details': details
    }, status=status_code)

def rate_limit_key(group, request):
    """Custom rate limit key function"""
    return request.META.get('REMOTE_ADDR', 'unknown')

def apply_rate_limit(rate='100/h'):
    """Apply rate limiting to a view"""
    def decorator(func):
        @method_decorator(ratelimit(key=rate_limit_key, rate=rate, method='GET', block=False))
        @method_decorator(ratelimit(key=rate_limit_key, rate=rate, method='POST', block=False))
        def wrapper(self, request, *args, **kwargs):
            # Check if rate limited
            if getattr(request, 'limited', False):
                return error_response(
                    "Rate limit exceeded. Please try again later.",
                    status.HTTP_429_TOO_MANY_REQUESTS
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
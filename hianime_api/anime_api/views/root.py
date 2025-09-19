from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

class RootAPIView(APIView):
    """Root API endpoint providing basic information"""
    
    @extend_schema(
        summary="API Root",
        description="Get basic information about the API and available endpoints",
        responses={200: dict}
    )
    def get(self, request):
        """
        Get basic information about the API and available endpoints
        """
        api_info = {
            "name": "HiAnime API",
            "version": "1.0.0",
            "description": "A RESTful API that utilizes web scraping to fetch anime content from hianime.bz",
            "documentation": "/api/v1/schema/swagger-ui/",
            "endpoints": {
                "api_v1": "/api/v1/",
                "schema": "/api/schema/",
                "swagger_ui": "/api/v1/schema/swagger-ui/",
                "redoc": "/api/v1/schema/redoc/"
            },
            "available_endpoints": [
                "GET /api/v1/ - API documentation",
                "GET /api/v1/home/ - Homepage data",
                "GET /api/v1/anime/{id}/ - Anime details",
                "GET /api/v1/animes/{query}/ - Anime lists",
                "GET /api/v1/search/ - Search anime",
                "GET /api/v1/suggestion/ - Search suggestions",
                "GET /api/v1/episodes/{id}/ - Anime episodes",
                "GET /api/v1/servers/ - Episode servers",
                "GET /api/v1/stream/ - Streaming links",
                "GET /api/v1/genres/ - All genres"
            ],
            "notes": [
                "This API is just an unofficial API for hianime.bz and is in no other way officially related to the same.",
                "The content that this API provides is not mine, nor is it hosted by me.",
                "These belong to their respective owners.",
                "This API just demonstrates how to build an API that scrapes websites and uses their content."
            ]
        }
        
        return Response(api_info, status=status.HTTP_200_OK)
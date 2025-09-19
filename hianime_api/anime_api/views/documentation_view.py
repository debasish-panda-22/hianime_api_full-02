from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

class DocumentationAPIView(APIView):
    """API endpoint for documentation"""
    
    @extend_schema(
        summary="API Documentation",
        description="Get information about available API endpoints",
        responses={200: dict}
    )
    def get(self, request):
        """
        Get information about available API endpoints
        """
        documentation = {
            "title": "HiAnime API",
            "version": "1.0.0",
            "description": "A RESTful API that utilizes web scraping to fetch anime content from hianime.bz",
            "base_url": "/api/v1",
            "endpoints": [
                {
                    "path": "/home",
                    "method": "GET",
                    "description": "Get homepage data including spotlight, trending, top airing, and other sections"
                },
                {
                    "path": "/anime/{anime_id}",
                    "method": "GET", 
                    "description": "Get detailed information about a specific anime"
                },
                {
                    "path": "/animes/{query}/{category?}",
                    "method": "GET",
                    "description": "Get anime lists by category and query type"
                },
                {
                    "path": "/search",
                    "method": "GET",
                    "description": "Search for anime by keyword",
                    "parameters": [
                        {"name": "keyword", "type": "string", "required": True},
                        {"name": "page", "type": "integer", "required": False, "default": 1}
                    ]
                },
                {
                    "path": "/suggestion",
                    "method": "GET",
                    "description": "Get search suggestions for a keyword",
                    "parameters": [
                        {"name": "keyword", "type": "string", "required": True}
                    ]
                },
                {
                    "path": "/episodes/{anime_id}",
                    "method": "GET",
                    "description": "Get list of episodes for a specific anime"
                },
                {
                    "path": "/servers",
                    "method": "GET",
                    "description": "Get available servers for a specific episode",
                    "parameters": [
                        {"name": "id", "type": "string", "required": True}
                    ]
                },
                {
                    "path": "/stream",
                    "method": "GET",
                    "description": "Get streaming links for a specific episode from a specific server",
                    "parameters": [
                        {"name": "id", "type": "string", "required": True},
                        {"name": "server", "type": "string", "required": True},
                        {"name": "type", "type": "string", "required": True, "enum": ["sub", "dub"]}
                    ]
                },
                {
                    "path": "/genres",
                    "method": "GET",
                    "description": "Get list of all available anime genres"
                }
            ],
            "valid_queries": {
                "top-airing": {"has_category": False},
                "most-popular": {"has_category": False},
                "most-favorite": {"has_category": False},
                "completed": {"has_category": False},
                "recently-added": {"has_category": False},
                "recently-updated": {"has_category": False},
                "top-upcoming": {"has_category": False},
                "genre": {"has_category": True, "category": "all genres"},
                "az-list": {"has_category": True, "category": "0-9,all,a-z"},
                "subbed-anime": {"has_category": False},
                "dubbed-anime": {"has_category": False},
                "movie": {"has_category": False},
                "tv": {"has_category": False},
                "ova": {"has_category": False},
                "ona": {"has_category": False},
                "special": {"has_category": False},
                "events": {"has_category": False}
            },
            "notes": [
                "This API is just an unofficial API for hianime.bz and is in no other way officially related to the same.",
                "The content that this API provides is not mine, nor is it hosted by me.",
                "These belong to their respective owners.",
                "This API just demonstrates how to build an API that scrapes websites and uses their content."
            ]
        }
        
        return Response(documentation, status=status.HTTP_200_OK)
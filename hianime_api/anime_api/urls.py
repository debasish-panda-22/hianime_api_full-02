from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .views import (
    HomepageAPIView,
    AnimeDetailsAPIView,
    SearchAPIView,
    SuggestionAPIView,
    EpisodesAPIView,
    ServersAPIView,
    StreamingAPIView,
    AnimeListAPIView,
    GenresAPIView,
    DocumentationAPIView
)

urlpatterns = [
    # Documentation endpoints
    path('', DocumentationAPIView.as_view(), name='documentation'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints
    path('home/', HomepageAPIView.as_view(), name='homepage'),
    path('anime/<str:anime_id>/', AnimeDetailsAPIView.as_view(), name='anime-details'),
    path('animes/<str:query>/', AnimeListAPIView.as_view(), name='anime-list'),
    path('animes/<str:query>/<str:category>/', AnimeListAPIView.as_view(), name='anime-list-with-category'),
    path('search/', SearchAPIView.as_view(), name='search'),
    path('suggestion/', SuggestionAPIView.as_view(), name='suggestion'),
    path('episodes/<str:anime_id>/', EpisodesAPIView.as_view(), name='episodes'),
    path('servers/', ServersAPIView.as_view(), name='servers'),
    path('stream/', StreamingAPIView.as_view(), name='stream'),
    path('genres/', GenresAPIView.as_view(), name='genres'),
]
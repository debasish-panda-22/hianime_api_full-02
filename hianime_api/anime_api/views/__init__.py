from .homepage_view import HomepageAPIView
from .anime_details_view import AnimeDetailsAPIView
from .search_view import SearchAPIView, SuggestionAPIView
from .episodes_view import EpisodesAPIView
from .streaming_view import ServersAPIView, StreamingAPIView
from .anime_list_view import AnimeListAPIView, GenresAPIView
from .documentation_view import DocumentationAPIView
from .root import RootAPIView

__all__ = [
    'HomepageAPIView',
    'AnimeDetailsAPIView', 
    'SearchAPIView',
    'SuggestionAPIView',
    'EpisodesAPIView',
    'ServersAPIView',
    'StreamingAPIView',
    'AnimeListAPIView',
    'GenresAPIView',
    'DocumentationAPIView',
    'RootAPIView'
]
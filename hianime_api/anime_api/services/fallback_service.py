import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class FallbackService:
    """Service providing fallback data when external API is not available"""
    
    def __init__(self):
        self.mock_anime_list = [
            {
                'id': 'attack-on-titan-100',
                'name': 'Attack on Titan',
                'japanese_name': '進撃の巨人',
                'type': 'TV',
                'episodes': 87,
                'status': 'Completed',
                'season': 'Spring 2013',
                'year': 2013,
                'score': 8.8,
                'image': 'https://example.com/attack-on-titan.jpg',
                'description': 'Centuries ago, mankind was slaughtered to near extinction by monstrous humanoid creatures called titans...'
            },
            {
                'id': 'demon-slayer-101',
                'name': 'Demon Slayer: Kimetsu no Yaiba',
                'japanese_name': '鬼滅の刃',
                'type': 'TV',
                'episodes': 26,
                'status': 'Completed',
                'season': 'Spring 2019',
                'year': 2019,
                'score': 8.7,
                'image': 'https://example.com/demon-slayer.jpg',
                'description': 'It is the Taisho Period in Japan. Tanjiro, a kindhearted boy who sells charcoal for a living...'
            },
            {
                'id': 'one-piece-102',
                'name': 'One Piece',
                'japanese_name': 'ワンピース',
                'type': 'TV',
                'episodes': 1000,
                'status': 'Ongoing',
                'season': 'Fall 1999',
                'year': 1999,
                'score': 8.9,
                'image': 'https://example.com/one-piece.jpg',
                'description': 'Gol D. Roger was known as the "Pirate King," the strongest and most infamous being to have sailed the Grand Line...'
            },
            {
                'id': 'jujutsu-kaisen-103',
                'name': 'Jujutsu Kaisen',
                'japanese_name': '呪術廻戦',
                'type': 'TV',
                'episodes': 24,
                'status': 'Completed',
                'season': 'Fall 2020',
                'year': 2020,
                'score': 8.5,
                'image': 'https://example.com/jujutsu-kaisen.jpg',
                'description': 'In a world where demons feed on unsuspecting humans, fragments of the legendary and feared demon Ryoumen Sukuna...'
            },
            {
                'id': 'my-hero-academia-104',
                'name': 'My Hero Academia',
                'japanese_name': '僕のヒーローアカデミア',
                'type': 'TV',
                'episodes': 113,
                'status': 'Ongoing',
                'season': 'Spring 2016',
                'year': 2016,
                'score': 8.4,
                'image': 'https://example.com/my-hero-academia.jpg',
                'description': 'The appearance of "quirks," newly discovered super powers, has been steadily increasing over the years...'
            }
        ]
        
        self.genres = [
            'Action', 'Adventure', 'Comedy', 'Drama', 'Ecchi', 'Fantasy', 'Hentai', 'Horror',
            'Mahou Shoujo', 'Mecha', 'Music', 'Mystery', 'Psychological', 'Romance', 'Sci-Fi',
            'Slice of Life', 'Sports', 'Supernatural', 'Thriller'
        ]
    
    def get_homepage_data(self):
        """Get fallback homepage data"""
        logger.info("Using fallback homepage data")
        
        # Shuffle and select spotlight anime
        spotlight_anime = random.sample(self.mock_anime_list, min(3, len(self.mock_anime_list)))
        
        # Shuffle and select trending anime
        trending_anime = random.sample(self.mock_anime_list, min(10, len(self.mock_anime_list)))
        
        # Shuffle and select top airing anime
        top_airing_anime = random.sample(self.mock_anime_list, min(10, len(self.mock_anime_list)))
        
        # Shuffle and select most popular anime
        most_popular_anime = random.sample(self.mock_anime_list, min(10, len(self.mock_anime_list)))
        
        # Shuffle and select latest episodes
        latest_episodes = []
        for anime in self.mock_anime_list[:5]:
            for ep in range(1, min(4, anime['episodes'] + 1)):
                latest_episodes.append({
                    'id': f"{anime['id']}-episode-{ep}",
                    'anime_id': anime['id'],
                    'anime_name': anime['name'],
                    'episode_number': ep,
                    'episode_title': f'Episode {ep}',
                    'image': anime['image'],
                    'filler': False,
                    'timestamp': self._get_random_timestamp()
                })
        
        return {
            'spotlight': spotlight_anime,
            'trending': trending_anime,
            'top_airing': top_airing_anime,
            'most_popular': most_popular_anime,
            'latest_episode': latest_episodes[:12],
            'top_upcoming': [],
            'genres': self._get_genre_list()
        }
    
    def get_genres_data(self):
        """Get fallback genres data"""
        logger.info("Using fallback genres data")
        
        genre_data = {}
        for genre in self.genres:
            # Shuffle and select anime for each genre
            genre_anime = random.sample(self.mock_anime_list, min(6, len(self.mock_anime_list)))
            genre_data[genre] = genre_anime
        
        return genre_data
    
    def get_anime_details(self, anime_id):
        """Get fallback anime details"""
        logger.info(f"Using fallback anime details for: {anime_id}")
        
        # Find anime in mock list or return first one
        anime = next((a for a in self.mock_anime_list if a['id'] == anime_id), self.mock_anime_list[0])
        
        # Generate episodes list
        episodes = []
        for i in range(1, min(anime['episodes'] + 1, 25)):  # Limit to 24 episodes for demo
            episodes.append({
                'id': f"{anime['id']}-episode-{i}",
                'number': i,
                'title': f'Episode {i}',
                'filler': False,
                'timestamp': self._get_random_timestamp()
            })
        
        return {
            'anime': {
                **anime,
                'synopsis': anime['description'],
                'studios': ['Studio 1', 'Studio 2'],
                'producers': ['Producer 1', 'Producer 2'],
                'duration': '24 min per ep',
                'rating': 'PG-13',
                'quality': 'HD',
                'sub': True,
                'dub': False
            },
            'episodes': episodes
        }
    
    def get_episodes_data(self, anime_id):
        """Get fallback episodes data"""
        logger.info(f"Using fallback episodes data for: {anime_id}")
        
        anime = next((a for a in self.mock_anime_list if a['id'] == anime_id), self.mock_anime_list[0])
        
        episodes = []
        for i in range(1, min(anime['episodes'] + 1, 25)):
            episodes.append({
                'id': f"{anime['id']}-episode-{i}",
                'number': i,
                'title': f'Episode {i}',
                'filler': False,
                'timestamp': self._get_random_timestamp()
            })
        
        return {
            'total_episodes': len(episodes),
            'episodes': episodes
        }
    
    def get_search_results(self, query):
        """Get fallback search results"""
        logger.info(f"Using fallback search results for: {query}")
        
        # Simple text matching on anime names
        results = []
        query_lower = query.lower()
        
        for anime in self.mock_anime_list:
            if (query_lower in anime['name'].lower() or 
                query_lower in anime['japanese_name'].lower() or
                query_lower in anime['description'].lower()):
                results.append(anime)
        
        return {
            'total_results': len(results),
            'results': results
        }
    
    def _get_genre_list(self):
        """Get genre list with anime counts"""
        genre_list = []
        for genre in self.genres:
            # Random count for demo
            count = random.randint(10, 100)
            genre_list.append({
                'name': genre,
                'count': count
            })
        
        return genre_list
    
    def get_streaming_data(self, episode_id, server, stream_type):
        """Get fallback streaming data"""
        logger.info(f"Using fallback streaming data for: {episode_id}, server: {server}, type: {stream_type}")
        
        # Mock streaming servers
        servers = [
            {
                'name': 'HD-1',
                'type': 'mp4',
                'url': f'https://example.com/stream/{episode_id}/{stream_type}/hd1'
            },
            {
                'name': 'HD-2',
                'type': 'mp4',
                'url': f'https://example.com/stream/{episode_id}/{stream_type}/hd2'
            },
            {
                'name': 'SD',
                'type': 'mp4',
                'url': f'https://example.com/stream/{episode_id}/{stream_type}/sd'
            }
        ]
        
        # Find the requested server or return the first one
        selected_server = next((s for s in servers if s['name'] == server), servers[0])
        
        return {
            'sources': [
                {
                    'file': selected_server['url'],
                    'type': selected_server['type'],
                    'label': selected_server['name']
                }
            ],
            'tracks': [
                {
                    'file': 'https://example.com/subtitles/sample.vtt',
                    'label': 'English',
                    'kind': 'subtitles',
                    'default': True
                }
            ],
            'server': server,
            'type': stream_type
        }
    
    def get_servers_data(self, episode_id):
        """Get fallback servers data"""
        logger.info(f"Using fallback servers data for: {episode_id}")
        
        return {
            'sub': [
                {
                    'name': 'HD-1',
                    'server': 'HD-1'
                },
                {
                    'name': 'HD-2',
                    'server': 'HD-2'
                },
                {
                    'name': 'SD',
                    'server': 'SD'
                }
            ],
            'dub': [
                {
                    'name': 'HD-1',
                    'server': 'HD-1'
                },
                {
                    'name': 'HD-2',
                    'server': 'HD-2'
                }
            ]
        }
    
    def get_suggestions_data(self, keyword):
        """Get fallback search suggestions"""
        logger.info(f"Using fallback suggestions data for: {keyword}")
        
        # Simple keyword matching for suggestions
        suggestions = []
        keyword_lower = keyword.lower()
        
        for anime in self.mock_anime_list:
            if (keyword_lower in anime['name'].lower() or 
                keyword_lower in anime['japanese_name'].lower()):
                suggestions.append({
                    'id': anime['id'],
                    'name': anime['name'],
                    'japanese_name': anime['japanese_name'],
                    'image': anime['image'],
                    'type': anime['type'],
                    'episodes': anime['episodes'],
                    'score': anime['score']
                })
        
        # Limit to 10 suggestions
        return suggestions[:10]
    
    def _get_random_timestamp(self):
        """Get random timestamp within last 30 days"""
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

# Global fallback service instance
fallback_service = FallbackService()
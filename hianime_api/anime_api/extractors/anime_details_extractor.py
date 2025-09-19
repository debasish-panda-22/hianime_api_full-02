from bs4 import BeautifulSoup
import re
from typing import Dict, Any, List

class AnimeDetailsExtractor:
    """Extractor for anime details page"""
    
    def extract(self, html: str) -> Dict[str, Any]:
        """
        Extract anime details from HTML
        
        Args:
            html (str): HTML content
            
        Returns:
            Dict[str, Any]: Extracted anime details
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        response = {
            'title': None,
            'alternativeTitle': None,
            'japanese': None,
            'id': None,
            'poster': None,
            'rating': None,
            'type': None,
            'episodes': {
                'sub': None,
                'dub': None,
                'eps': None
            },
            'synopsis': None,
            'synonyms': [],
            'aired': {
                'from': None,
                'to': None
            },
            'premiered': None,
            'duration': None,
            'status': None,
            'MAL_score': None,
            'genres': [],
            'studios': None,
            'producers': [],
            'moreSeasons': [],
            'related': [],
            'mostPopular': [],
            'recommended': []
        }
        
        # Extract basic info
        self._extract_basic_info(soup, response)
        
        # Extract episodes info
        self._extract_episodes_info(soup, response)
        
        # Extract synopsis
        self._extract_synopsis(soup, response)
        
        # Extract aired dates
        self._extract_aired_dates(soup, response)
        
        # Extract additional details
        self._extract_additional_details(soup, response)
        
        # Extract genres
        self._extract_genres(soup, response)
        
        # Extract studios and producers
        self._extract_studios_producers(soup, response)
        
        # Extract more seasons
        self._extract_more_seasons(soup, response)
        
        # Extract related anime
        self._extract_related_anime(soup, response)
        
        # Extract most popular and recommended
        self._extract_popular_recommended(soup, response)
        
        return response
    
    def _extract_basic_info(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract basic anime information"""
        # Extract title and alternative title
        title_elem = soup.select_one('.anisc-detail .film-name h2')
        if title_elem:
            response['title'] = title_elem.get_text(strip=True)
        
        alt_title_elem = soup.select_one('.anisc-detail .film-name .film-name-a')
        if alt_title_elem:
            response['alternativeTitle'] = alt_title_elem.get_text(strip=True)
        
        # Extract Japanese title
        japanese_elem = soup.select_one('.anisc-detail .film-name .film-name-jp')
        if japanese_elem:
            response['japanese'] = japanese_elem.get_text(strip=True)
        
        # Extract ID from URL or from data attributes
        id_elem = soup.select_one('[data-id]') or soup.select_one('.watch-play')
        if id_elem:
            response['id'] = id_elem.get('data-id') or id_elem.get('href', '').split('/')[-1]
        
        # Extract poster
        poster_elem = soup.select_one('.anisc-poster .film-poster-img')
        if poster_elem:
            response['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
        
        # Extract rating
        rating_elem = soup.select_one('.anisc-detail .film-stats .tick-rate')
        if rating_elem:
            response['rating'] = rating_elem.get_text(strip=True)
        
        # Extract type
        type_elem = soup.select_one('.anisc-detail .film-stats .tick')
        if type_elem:
            response['type'] = type_elem.get_text(strip=True)
    
    def _extract_episodes_info(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract episodes information"""
        episodes_elem = soup.select_one('.anisc-detail .film-stats .tick-eps')
        if episodes_elem:
            eps_text = episodes_elem.get_text(strip=True)
            # Extract sub, dub, and total episodes
            sub_match = re.search(r'Sub:\s*(\d+)', eps_text)
            dub_match = re.search(r'Dub:\s*(\d+)', eps_text)
            eps_match = re.search(r'Eps:\s*(\d+)', eps_text)
            
            if sub_match:
                response['episodes']['sub'] = int(sub_match.group(1))
            if dub_match:
                response['episodes']['dub'] = int(dub_match.group(1))
            if eps_match:
                response['episodes']['eps'] = int(eps_match.group(1))
    
    def _extract_synopsis(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract synopsis"""
        synopsis_elem = soup.select_one('.anisc-detail .film-description .text')
        if synopsis_elem:
            response['synopsis'] = synopsis_elem.get_text(strip=True)
    
    def _extract_aired_dates(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract aired dates"""
        # Find aired information by looking for the text "Aired:"
        aired_items = soup.select('.anisc-detail .item-title')
        for item in aired_items:
            if item.get_text(strip=True) == "Aired:":
                aired_elem = item.find_next_sibling('div', class_='item-list')
                if aired_elem:
                    aired_text = aired_elem.get_text(strip=True)
                    # Parse from and to dates
                    dates = aired_text.split('to')
                    if len(dates) > 0:
                        response['aired']['from'] = dates[0].strip()
                    if len(dates) > 1:
                        response['aired']['to'] = dates[1].strip()
                break
        
        # Extract premiered
        premiered_items = soup.select('.anisc-detail .item-title')
        for item in premiered_items:
            if item.get_text(strip=True) == "Premiered:":
                premiered_elem = item.find_next_sibling('div', class_='item-list')
                if premiered_elem:
                    response['premiered'] = premiered_elem.get_text(strip=True)
                break
        
        # Extract duration
        duration_items = soup.select('.anisc-detail .item-title')
        for item in duration_items:
            if item.get_text(strip=True) == "Duration:":
                duration_elem = item.find_next_sibling('div', class_='item-list')
                if duration_elem:
                    response['duration'] = duration_elem.get_text(strip=True)
                break
        
        # Extract status
        status_items = soup.select('.anisc-detail .item-title')
        for item in status_items:
            if item.get_text(strip=True) == "Status:":
                status_elem = item.find_next_sibling('div', class_='item-list')
                if status_elem:
                    response['status'] = status_elem.get_text(strip=True)
                break
        
        # Extract MAL score
        mal_score_items = soup.select('.anisc-detail .item-title')
        for item in mal_score_items:
            if item.get_text(strip=True) == "MAL Score:":
                mal_score_elem = item.find_next_sibling('div', class_='item-list')
                if mal_score_elem:
                    response['MAL_score'] = mal_score_elem.get_text(strip=True)
                break
    
    def _extract_additional_details(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract additional details like synonyms"""
        synonyms_items = soup.select('.anisc-detail .item-title')
        for item in synonyms_items:
            if item.get_text(strip=True) == "Synonyms:":
                synonyms_elem = item.find_next_sibling('div', class_='item-list')
                if synonyms_elem:
                    synonyms_text = synonyms_elem.get_text(strip=True)
                    response['synonyms'] = [syn.strip() for syn in synonyms_text.split(',') if syn.strip()]
                break
    
    def _extract_genres(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract genres"""
        genres_items = soup.select('.anisc-detail .item-title')
        for item in genres_items:
            if item.get_text(strip=True) == "Genres:":
                genres_elem = item.find_next_sibling('div', class_='item-list')
                if genres_elem:
                    genre_links = genres_elem.select('a')
                    response['genres'] = [genre.get_text(strip=True) for genre in genre_links]
                break
    
    def _extract_studios_producers(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract studios and producers"""
        # Extract studios
        studios_items = soup.select('.anisc-detail .item-title')
        for item in studios_items:
            if item.get_text(strip=True) == "Studios:":
                studios_elem = item.find_next_sibling('div', class_='item-list')
                if studios_elem:
                    studio_links = studios_elem.select('a')
                    response['studios'] = ', '.join([studio.get_text(strip=True) for studio in studio_links])
                break
        
        # Extract producers
        producers_items = soup.select('.anisc-detail .item-title')
        for item in producers_items:
            if item.get_text(strip=True) == "Producers:":
                producers_elem = item.find_next_sibling('div', class_='item-list')
                if producers_elem:
                    producer_links = producers_elem.select('a')
                    response['producers'] = [producer.get_text(strip=True) for producer in producer_links]
                break
    
    def _extract_more_seasons(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract more seasons"""
        seasons_container = soup.select_one('.seasons .os-list')
        if seasons_container:
            season_items = seasons_container.select('.os-item')
            for season_item in season_items:
                try:
                    season_info = {
                        'title': None,
                        'id': None,
                        'poster': None,
                        'type': None,
                        'episodes': {
                            'sub': None,
                            'dub': None,
                            'eps': None
                        }
                    }
                    
                    # Extract title and ID
                    title_elem = season_item.select_one('.title')
                    if title_elem:
                        season_info['title'] = title_elem.get_text(strip=True)
                        href = title_elem.get('href')
                        if href:
                            season_info['id'] = href.split('/')[-1]
                    
                    # Extract poster
                    poster_elem = season_item.select_one('.film-poster-img')
                    if poster_elem:
                        season_info['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                    
                    # Extract type
                    type_elem = season_item.select_one('.tick')
                    if type_elem:
                        season_info['type'] = type_elem.get_text(strip=True)
                    
                    # Extract episodes
                    sub_elem = season_item.select_one('.tick-sub')
                    if sub_elem:
                        season_info['episodes']['sub'] = self._parse_number(sub_elem.get_text(strip=True))
                    
                    dub_elem = season_item.select_one('.tick-dub')
                    if dub_elem:
                        season_info['episodes']['dub'] = self._parse_number(dub_elem.get_text(strip=True))
                    
                    eps_elem = season_item.select_one('.tick-eps')
                    if eps_elem:
                        eps_text = eps_elem.get_text(strip=True)
                    elif sub_elem:
                        eps_text = sub_elem.get_text(strip=True)
                    else:
                        eps_text = '0'
                    
                    season_info['episodes']['eps'] = self._parse_number(eps_text)
                    
                    response['moreSeasons'].append(season_info)
                    
                except Exception as e:
                    print(f"Error extracting season: {e}")
                    continue
    
    def _extract_related_anime(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract related anime"""
        related_container = soup.select_one('.block_area.block_area_sidebar.block_area-relationships .anif-block-ul')
        if related_container:
            related_items = related_container.select('li')
            for related_item in related_items:
                try:
                    related_info = {
                        'title': None,
                        'id': None,
                        'poster': None,
                        'type': None,
                        'episodes': {
                            'sub': None,
                            'dub': None,
                            'eps': None
                        }
                    }
                    
                    # Extract title and ID
                    title_elem = related_item.select_one('.film-name a')
                    if title_elem:
                        related_info['title'] = title_elem.get('title')
                        href = title_elem.get('href')
                        if href:
                            related_info['id'] = href.split('/')[-1]
                    
                    # Extract poster
                    poster_elem = related_item.select_one('.film-poster-img')
                    if poster_elem:
                        related_info['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                    
                    # Extract type
                    type_elem = related_item.select_one('.fd-infor .fdi-item')
                    if type_elem:
                        related_info['type'] = type_elem.get_text(strip=True)
                    
                    # Extract episodes
                    sub_elem = related_item.select_one('.fd-infor .tick-sub')
                    if sub_elem:
                        related_info['episodes']['sub'] = self._parse_number(sub_elem.get_text(strip=True))
                    
                    dub_elem = related_item.select_one('.fd-infor .tick-dub')
                    if dub_elem:
                        related_info['episodes']['dub'] = self._parse_number(dub_elem.get_text(strip=True))
                    
                    eps_elem = related_item.select_one('.fd-infor .tick-eps')
                    if eps_elem:
                        eps_text = eps_elem.get_text(strip=True)
                    elif sub_elem:
                        eps_text = sub_elem.get_text(strip=True)
                    else:
                        eps_text = '0'
                    
                    related_info['episodes']['eps'] = self._parse_number(eps_text)
                    
                    response['related'].append(related_info)
                    
                except Exception as e:
                    print(f"Error extracting related anime: {e}")
                    continue
    
    def _extract_popular_recommended(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract most popular and recommended anime"""
        # Most popular
        popular_container = soup.select_one('.block_area.block_area_sidebar.block_area-popular .anif-block-ul')
        if popular_container:
            popular_items = popular_container.select('li')
            for popular_item in popular_items:
                try:
                    popular_info = {
                        'title': None,
                        'id': None,
                        'poster': None,
                        'episodes': {
                            'sub': None,
                            'dub': None,
                            'eps': None
                        }
                    }
                    
                    # Extract title and ID
                    title_elem = popular_item.select_one('.film-name a')
                    if title_elem:
                        popular_info['title'] = title_elem.get('title')
                        href = title_elem.get('href')
                        if href:
                            popular_info['id'] = href.split('/')[-1]
                    
                    # Extract poster
                    poster_elem = popular_item.select_one('.film-poster-img')
                    if poster_elem:
                        popular_info['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                    
                    # Extract episodes
                    sub_elem = popular_item.select_one('.tick-sub')
                    if sub_elem:
                        popular_info['episodes']['sub'] = self._parse_number(sub_elem.get_text(strip=True))
                    
                    dub_elem = popular_item.select_one('.tick-dub')
                    if dub_elem:
                        popular_info['episodes']['dub'] = self._parse_number(dub_elem.get_text(strip=True))
                    
                    eps_elem = popular_item.select_one('.tick-eps')
                    if eps_elem:
                        eps_text = eps_elem.get_text(strip=True)
                    elif sub_elem:
                        eps_text = sub_elem.get_text(strip=True)
                    else:
                        eps_text = '0'
                    
                    popular_info['episodes']['eps'] = self._parse_number(eps_text)
                    
                    response['mostPopular'].append(popular_info)
                    
                except Exception as e:
                    print(f"Error extracting popular anime: {e}")
                    continue
        
        # Recommended
        recommended_container = soup.select_one('.block_area.block_area_sidebar.block_area-recommend .anif-block-ul')
        if recommended_container:
            recommended_items = recommended_container.select('li')
            for recommended_item in recommended_items:
                try:
                    recommended_info = {
                        'title': None,
                        'id': None,
                        'poster': None,
                        'episodes': {
                            'sub': None,
                            'dub': None,
                            'eps': None
                        }
                    }
                    
                    # Extract title and ID
                    title_elem = recommended_item.select_one('.film-name a')
                    if title_elem:
                        recommended_info['title'] = title_elem.get('title')
                        href = title_elem.get('href')
                        if href:
                            recommended_info['id'] = href.split('/')[-1]
                    
                    # Extract poster
                    poster_elem = recommended_item.select_one('.film-poster-img')
                    if poster_elem:
                        recommended_info['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                    
                    # Extract episodes
                    sub_elem = recommended_item.select_one('.tick-sub')
                    if sub_elem:
                        recommended_info['episodes']['sub'] = self._parse_number(sub_elem.get_text(strip=True))
                    
                    dub_elem = recommended_item.select_one('.tick-dub')
                    if dub_elem:
                        recommended_info['episodes']['dub'] = self._parse_number(dub_elem.get_text(strip=True))
                    
                    eps_elem = recommended_item.select_one('.tick-eps')
                    if eps_elem:
                        eps_text = eps_elem.get_text(strip=True)
                    elif sub_elem:
                        eps_text = sub_elem.get_text(strip=True)
                    else:
                        eps_text = '0'
                    
                    recommended_info['episodes']['eps'] = self._parse_number(eps_text)
                    
                    response['recommended'].append(recommended_info)
                    
                except Exception as e:
                    print(f"Error extracting recommended anime: {e}")
                    continue
    
    def _parse_number(self, text: str) -> int:
        """Parse number from text, return 0 if parsing fails"""
        try:
            # Remove non-digit characters and convert to int
            clean_text = re.sub(r'[^\d]', '', text)
            return int(clean_text) if clean_text else 0
        except (ValueError, AttributeError):
            return 0

# Global extractor instance
anime_details_extractor = AnimeDetailsExtractor()
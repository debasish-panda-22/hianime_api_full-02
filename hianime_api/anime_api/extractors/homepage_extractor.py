from bs4 import BeautifulSoup
import re
from typing import Dict, List, Any

class HomepageExtractor:
    """Extractor for homepage data"""
    
    def extract(self, html: str) -> Dict[str, Any]:
        """
        Extract homepage data from HTML
        
        Args:
            html (str): HTML content
            
        Returns:
            Dict[str, Any]: Extracted homepage data
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        response = {
            'spotlight': [],
            'trending': [],
            'topAiring': [],
            'mostPopular': [],
            'mostFavorite': [],
            'latestCompleted': [],
            'latestEpisode': [],
            'newAdded': [],
            'topUpcoming': [],
            'top10': {
                'today': [],
                'week': [],
                'month': []
            },
            'genres': []
        }
        
        # Extract spotlight
        self._extract_spotlight(soup, response)
        
        # Extract trending
        self._extract_trending(soup, response)
        
        # Extract featured sections (top airing, most popular, etc.)
        self._extract_featured_sections(soup, response)
        
        # Extract home sections (latest completed, latest episode, etc.)
        self._extract_home_sections(soup, response)
        
        # Extract top 10
        self._extract_top10(soup, response)
        
        # Extract genres
        self._extract_genres(soup, response)
        
        return response
    
    def _extract_spotlight(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract spotlight anime"""
        spotlight_container = soup.select_one('.deslide-wrap .swiper-wrapper')
        if not spotlight_container:
            return
            
        slides = spotlight_container.select('.swiper-slide')
        for i, slide in enumerate(slides):
            try:
                spotlight_item = {
                    'title': None,
                    'alternativeTitle': None,
                    'id': None,
                    'poster': None,
                    'rank': i + 1,
                    'type': None,
                    'quality': None,
                    'duration': None,
                    'aired': None,
                    'synopsis': None,
                    'episodes': {
                        'sub': None,
                        'dub': None,
                        'eps': None
                    }
                }
                
                # Extract ID
                link_elem = slide.select_one('.desi-buttons a')
                if link_elem and link_elem.get('href'):
                    href = link_elem.get('href')
                    spotlight_item['id'] = href.split('/')[-1] if href else None
                
                # Extract poster
                poster_elem = slide.select_one('.deslide-cover .film-poster-img')
                if poster_elem:
                    spotlight_item['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                
                # Extract titles
                title_elem = slide.select_one('.desi-head-title')
                if title_elem:
                    spotlight_item['title'] = title_elem.get_text(strip=True)
                    spotlight_item['alternativeTitle'] = title_elem.get('data-jname')
                
                # Extract synopsis
                synopsis_elem = slide.select_one('.desi-description')
                if synopsis_elem:
                    spotlight_item['synopsis'] = synopsis_elem.get_text(strip=True)
                
                # Extract details
                details_elem = slide.select_one('.sc-detail')
                if details_elem:
                    detail_items = details_elem.select('.scd-item')
                    if len(detail_items) > 0:
                        spotlight_item['type'] = detail_items[0].get_text(strip=True)
                    if len(detail_items) > 1:
                        spotlight_item['duration'] = detail_items[1].get_text(strip=True)
                    
                    # Aired date
                    aired_elem = details_elem.select_one('.scd-item.m-hide')
                    if aired_elem:
                        spotlight_item['aired'] = aired_elem.get_text(strip=True)
                    
                    # Quality
                    quality_elem = details_elem.select_one('.scd-item .quality')
                    if quality_elem:
                        spotlight_item['quality'] = quality_elem.get_text(strip=True)
                    
                    # Episodes
                    sub_elem = details_elem.select_one('.tick-sub')
                    if sub_elem:
                        spotlight_item['episodes']['sub'] = self._parse_number(sub_elem.get_text(strip=True))
                    
                    dub_elem = details_elem.select_one('.tick-dub')
                    if dub_elem:
                        spotlight_item['episodes']['dub'] = self._parse_number(dub_elem.get_text(strip=True))
                    
                    eps_elem = details_elem.select_one('.tick-eps')
                    if eps_elem:
                        eps_text = eps_elem.get_text(strip=True)
                    elif sub_elem:
                        eps_text = sub_elem.get_text(strip=True)
                    else:
                        eps_text = '0'
                    
                    spotlight_item['episodes']['eps'] = self._parse_number(eps_text)
                
                response['spotlight'].append(spotlight_item)
                
            except Exception as e:
                print(f"Error extracting spotlight item {i}: {e}")
                continue
    
    def _extract_trending(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract trending anime"""
        trending_container = soup.select_one('#trending-home .swiper-container')
        if not trending_container:
            return
            
        slides = trending_container.select('.swiper-slide')
        for i, slide in enumerate(slides):
            try:
                trending_item = {
                    'title': None,
                    'alternativeTitle': None,
                    'rank': i + 1,
                    'poster': None,
                    'id': None
                }
                
                # Extract title and alternative title
                title_elem = slide.select_one('.item .film-title')
                if title_elem:
                    trending_item['title'] = title_elem.get_text(strip=True)
                    trending_item['alternativeTitle'] = title_elem.get('data-jname')
                
                # Extract poster and ID
                image_elem = slide.select_one('.film-poster')
                if image_elem:
                    img_elem = image_elem.select_one('img')
                    if img_elem:
                        trending_item['poster'] = img_elem.get('data-src') or img_elem.get('src')
                    
                    href = image_elem.get('href')
                    if href:
                        trending_item['id'] = href.split('/')[-1]
                
                response['trending'].append(trending_item)
                
            except Exception as e:
                print(f"Error extracting trending item {i}: {e}")
                continue
    
    def _extract_featured_sections(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract featured sections (top airing, most popular, etc.)"""
        featured_sections = soup.select('#anime-featured .anif-blocks .row .anif-block')
        
        for section in featured_sections:
            try:
                # Get section type from header
                header_elem = section.select_one('.anif-block-header')
                if not header_elem:
                    continue
                
                section_type = re.sub(r'\s+', '', header_elem.get_text(strip=True))
                section_type = section_type[0].lower() + section_type[1:]  # lowercase first letter
                
                # Map section types
                section_mapping = {
                    'topairing': 'topAiring',
                    'mostpopular': 'mostPopular',
                    'mostfavorite': 'mostFavorite',
                    'latestcompleted': 'latestCompleted',
                    'topupcoming': 'topUpcoming'
                }
                
                mapped_section = section_mapping.get(section_type, section_type)
                if mapped_section not in response:
                    continue
                
                # Extract anime items in this section
                items = section.select('.anif-block-ul ul li')
                section_data = []
                
                for item in items:
                    try:
                        anime_item = {
                            'title': None,
                            'alternativeTitle': None,
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
                        title_elem = item.select_one('.film-detail .film-name a')
                        if title_elem:
                            anime_item['title'] = title_elem.get('title')
                            anime_item['alternativeTitle'] = title_elem.get('data-jname')
                            href = title_elem.get('href')
                            if href:
                                anime_item['id'] = href.split('/')[-1]
                        
                        # Extract poster
                        poster_elem = item.select_one('.film-poster .film-poster-img')
                        if poster_elem:
                            anime_item['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                        
                        # Extract type
                        type_elem = item.select_one('.fd-infor .fdi-item')
                        if type_elem:
                            anime_item['type'] = type_elem.get_text(strip=True)
                        
                        # Extract episodes
                        sub_elem = item.select_one('.fd-infor .tick-sub')
                        if sub_elem:
                            anime_item['episodes']['sub'] = self._parse_number(sub_elem.get_text(strip=True))
                        
                        dub_elem = item.select_one('.fd-infor .tick-dub')
                        if dub_elem:
                            anime_item['episodes']['dub'] = self._parse_number(dub_elem.get_text(strip=True))
                        
                        eps_elem = item.select_one('.fd-infor .tick-eps')
                        if eps_elem:
                            eps_text = eps_elem.get_text(strip=True)
                        elif sub_elem:
                            eps_text = sub_elem.get_text(strip=True)
                        else:
                            eps_text = '0'
                        
                        anime_item['episodes']['eps'] = self._parse_number(eps_text)
                        
                        section_data.append(anime_item)
                        
                    except Exception as e:
                        print(f"Error extracting featured item: {e}")
                        continue
                
                response[mapped_section] = section_data
                
            except Exception as e:
                print(f"Error extracting featured section: {e}")
                continue
    
    def _extract_home_sections(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract home sections (latest episode, new added, etc.)"""
        home_sections = soup.select('.block_area.block_area_home')
        
        for section in home_sections:
            try:
                # Get section type from heading
                heading_elem = section.select_one('.cat-heading')
                if not heading_elem:
                    continue
                
                section_type = re.sub(r'\s+', '', heading_elem.get_text(strip=True))
                section_type = section_type[0].lower() + section_type[1:]  # lowercase first letter
                
                # Map section types
                section_mapping = {
                    'latestepisode': 'latestEpisode',
                    'newonhianime': 'newAdded'
                }
                
                mapped_section = section_mapping.get(section_type, section_type)
                if mapped_section not in response:
                    continue
                
                # Extract anime items in this section
                items = section.select('.tab-content .film_list-wrap .flw-item')
                section_data = []
                
                for item in items:
                    try:
                        anime_item = {
                            'title': None,
                            'alternativeTitle': None,
                            'id': None,
                            'poster': None,
                            'episodes': {
                                'sub': None,
                                'dub': None,
                                'eps': None
                            }
                        }
                        
                        # Extract title and ID
                        title_elem = item.select_one('.film-detail .film-name .dynamic-name')
                        if title_elem:
                            anime_item['title'] = title_elem.get('title')
                            anime_item['alternativeTitle'] = title_elem.get('data-jname')
                            href = title_elem.get('href')
                            if href:
                                anime_item['id'] = href.split('/')[-1]
                        
                        # Extract poster
                        poster_elem = item.select_one('.film-poster img')
                        if poster_elem:
                            anime_item['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                        
                        # Extract episodes
                        episodes_elem = item.select_one('.film-poster .tick')
                        if episodes_elem:
                            sub_elem = episodes_elem.select_one('.tick-sub')
                            if sub_elem:
                                anime_item['episodes']['sub'] = self._parse_number(sub_elem.get_text(strip=True))
                            
                            dub_elem = episodes_elem.select_one('.tick-dub')
                            if dub_elem:
                                anime_item['episodes']['dub'] = self._parse_number(dub_elem.get_text(strip=True))
                            
                            eps_elem = episodes_elem.select_one('.tick-eps')
                            if eps_elem:
                                eps_text = eps_elem.get_text(strip=True)
                            elif sub_elem:
                                eps_text = sub_elem.get_text(strip=True)
                            else:
                                eps_text = '0'
                            
                            anime_item['episodes']['eps'] = self._parse_number(eps_text)
                        
                        section_data.append(anime_item)
                        
                    except Exception as e:
                        print(f"Error extracting home item: {e}")
                        continue
                
                response[mapped_section] = section_data
                
            except Exception as e:
                print(f"Error extracting home section: {e}")
                continue
    
    def _extract_top10(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract top 10 anime"""
        top10_container = soup.select_one('.block_area .cbox')
        if not top10_container:
            return
        
        # Extract top 10 for different time periods
        time_periods = [
            ('#top-viewed-day', 'today'),
            ('#top-viewed-week', 'week'),
            ('#top-viewed-month', 'month')
        ]
        
        for selector, period in time_periods:
            try:
                period_container = top10_container.select_one(selector)
                if not period_container:
                    continue
                
                items = period_container.select('ul li')
                period_data = []
                
                for i, item in enumerate(items):
                    try:
                        top_item = {
                            'title': None,
                            'rank': i + 1,
                            'alternativeTitle': None,
                            'id': None,
                            'poster': None,
                            'episodes': {
                                'sub': None,
                                'dub': None,
                                'eps': None
                            }
                        }
                        
                        # Extract title and alternative title
                        title_elem = item.select_one('.film-name a')
                        if title_elem:
                            top_item['title'] = title_elem.get_text(strip=True)
                            top_item['alternativeTitle'] = title_elem.get('data-jname')
                            href = title_elem.get('href')
                            if href:
                                top_item['id'] = href.split('/')[-1]
                        
                        # Extract poster
                        poster_elem = item.select_one('.film-poster img')
                        if poster_elem:
                            top_item['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                        
                        # Extract episodes
                        sub_elem = item.select_one('.tick-item.tick-sub')
                        if sub_elem:
                            top_item['episodes']['sub'] = self._parse_number(sub_elem.get_text(strip=True))
                        
                        dub_elem = item.select_one('.tick-item.tick-dub')
                        if dub_elem:
                            top_item['episodes']['dub'] = self._parse_number(dub_elem.get_text(strip=True))
                        
                        eps_elem = item.select_one('.tick-item.tick-eps')
                        if eps_elem:
                            eps_text = eps_elem.get_text(strip=True)
                        elif sub_elem:
                            eps_text = sub_elem.get_text(strip=True)
                        else:
                            eps_text = '0'
                        
                        top_item['episodes']['eps'] = self._parse_number(eps_text)
                        
                        period_data.append(top_item)
                        
                    except Exception as e:
                        print(f"Error extracting top10 item {i}: {e}")
                        continue
                
                response['top10'][period] = period_data
                
            except Exception as e:
                print(f"Error extracting top10 {period}: {e}")
                continue
    
    def _extract_genres(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract genres"""
        genres_container = soup.select_one('.sb-genre-list')
        if not genres_container:
            return
        
        genre_items = genres_container.select('li a')
        for genre_item in genre_items:
            try:
                genre = genre_item.get('title')
                if genre:
                    response['genres'].append(genre.lower())
            except Exception as e:
                print(f"Error extracting genre: {e}")
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
homepage_extractor = HomepageExtractor()
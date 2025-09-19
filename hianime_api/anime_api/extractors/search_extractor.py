from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any

class SearchExtractor:
    """Extractor for search results"""
    
    def extract_search_results(self, html: str) -> Dict[str, Any]:
        """
        Extract search results from HTML
        
        Args:
            html (str): HTML content
            
        Returns:
            Dict[str, Any]: Search results with pagination info
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        response = {
            'pageInfo': {
                'totalPages': 1,
                'currentPage': 1,
                'hasNextPage': False
            },
            'response': []
        }
        
        # Extract pagination info
        self._extract_pagination_info(soup, response)
        
        # Extract search results
        self._extract_search_items(soup, response)
        
        return response
    
    def extract_suggestions(self, html: str) -> List[Dict[str, Any]]:
        """
        Extract search suggestions from HTML
        
        Args:
            html (str): HTML content
            
        Returns:
            List[Dict[str, Any]]: List of suggestions
        """
        soup = BeautifulSoup(html, 'html.parser')
        suggestions = []
        
        # Find suggestions container
        suggestions_container = soup.select_one('.film-search-result')
        if not suggestions_container:
            # Try alternative selector
            suggestions_container = soup.select_one('.search-suggestions')
        
        if suggestions_container:
            suggestion_items = suggestions_container.select('.film-item')
            for suggestion_item in suggestion_items:
                try:
                    suggestion_info = {
                        'title': None,
                        'alternativeTitle': None,
                        'poster': None,
                        'id': None,
                        'aired': None,
                        'type': None,
                        'duration': None
                    }
                    
                    # Extract title and alternative title
                    title_elem = suggestion_item.select_one('.film-name')
                    if title_elem:
                        suggestion_info['title'] = title_elem.get_text(strip=True)
                        suggestion_info['alternativeTitle'] = title_elem.get('data-jname')
                    
                    # Extract ID
                    link_elem = suggestion_item.select_one('a')
                    if link_elem:
                        href = link_elem.get('href')
                        if href:
                            suggestion_info['id'] = href.split('/')[-1]
                    
                    # Extract poster
                    poster_elem = suggestion_item.select_one('.film-poster img')
                    if poster_elem:
                        suggestion_info['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                    
                    # Extract additional info
                    info_elems = suggestion_item.select('.film-infor span')
                    if len(info_elems) > 0:
                        suggestion_info['aired'] = info_elems[0].get_text(strip=True)
                    if len(info_elems) > 1:
                        suggestion_info['type'] = info_elems[1].get_text(strip=True)
                    if len(info_elems) > 2:
                        suggestion_info['duration'] = info_elems[2].get_text(strip=True)
                    
                    suggestions.append(suggestion_info)
                    
                except Exception as e:
                    print(f"Error extracting suggestion: {e}")
                    continue
        
        return suggestions
    
    def _extract_pagination_info(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract pagination information"""
        pagination_container = soup.select_one('.pagination')
        if pagination_container:
            # Find current page
            current_page_elem = pagination_container.select_one('.page-item.active')
            if current_page_elem:
                current_page_text = current_page_elem.get_text(strip=True)
                response['pageInfo']['currentPage'] = int(current_page_text) if current_page_text.isdigit() else 1
            
            # Find total pages
            page_items = pagination_container.select('.page-item a')
            if page_items:
                page_numbers = []
                for item in page_items:
                    page_text = item.get_text(strip=True)
                    if page_text.isdigit():
                        page_numbers.append(int(page_text))
                
                if page_numbers:
                    response['pageInfo']['totalPages'] = max(page_numbers)
            
            # Check if has next page
            next_page_elem = pagination_container.select_one('.page-item.next')
            if next_page_elem and not next_page_elem.get('class', []).__contains__('disabled'):
                response['pageInfo']['hasNextPage'] = True
    
    def _extract_search_items(self, soup: BeautifulSoup, response: Dict[str, Any]):
        """Extract search result items"""
        # Find search results container
        results_container = soup.select_one('.film_list-wrap')
        if not results_container:
            # Try alternative selector
            results_container = soup.select_one('.search-results')
        
        if results_container:
            result_items = results_container.select('.flw-item')
            for result_item in result_items:
                try:
                    result_info = {
                        'title': None,
                        'alternativeTitle': None,
                        'id': None,
                        'poster': None,
                        'type': None,
                        'duration': None,
                        'episodes': {
                            'sub': None,
                            'dub': None,
                            'eps': None
                        }
                    }
                    
                    # Extract title and alternative title
                    title_elem = result_item.select_one('.film-detail .film-name a')
                    if title_elem:
                        result_info['title'] = title_elem.get('title')
                        result_info['alternativeTitle'] = title_elem.get('data-jname')
                        href = title_elem.get('href')
                        if href:
                            result_info['id'] = href.split('/')[-1]
                    
                    # Extract poster
                    poster_elem = result_item.select_one('.film-poster img')
                    if poster_elem:
                        result_info['poster'] = poster_elem.get('data-src') or poster_elem.get('src')
                    
                    # Extract type and duration
                    info_elems = result_item.select('.fd-infor .fdi-item')
                    if len(info_elems) > 0:
                        result_info['type'] = info_elems[0].get_text(strip=True)
                    if len(info_elems) > 1:
                        result_info['duration'] = info_elems[1].get_text(strip=True)
                    
                    # Extract episodes
                    episodes_elem = result_item.select_one('.film-poster .tick')
                    if episodes_elem:
                        sub_elem = episodes_elem.select_one('.tick-sub')
                        if sub_elem:
                            result_info['episodes']['sub'] = self._parse_number(sub_elem.get_text(strip=True))
                        
                        dub_elem = episodes_elem.select_one('.tick-dub')
                        if dub_elem:
                            result_info['episodes']['dub'] = self._parse_number(dub_elem.get_text(strip=True))
                        
                        eps_elem = episodes_elem.select_one('.tick-eps')
                        if eps_elem:
                            eps_text = eps_elem.get_text(strip=True)
                        elif sub_elem:
                            eps_text = sub_elem.get_text(strip=True)
                        else:
                            eps_text = '0'
                        
                        result_info['episodes']['eps'] = self._parse_number(eps_text)
                    
                    response['response'].append(result_info)
                    
                except Exception as e:
                    print(f"Error extracting search result: {e}")
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
search_extractor = SearchExtractor()
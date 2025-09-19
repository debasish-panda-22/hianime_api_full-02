from bs4 import BeautifulSoup
from typing import List, Dict, Any

class EpisodesExtractor:
    """Extractor for anime episodes"""
    
    def extract(self, html: str) -> List[Dict[str, Any]]:
        """
        Extract episodes list from HTML
        
        Args:
            html (str): HTML content
            
        Returns:
            List[Dict[str, Any]]: List of episodes
        """
        soup = BeautifulSoup(html, 'html.parser')
        episodes = []
        
        # Find episodes container
        episodes_container = soup.select_one('.detail-infor-content .ss-list')
        if not episodes_container:
            # Try alternative selector
            episodes_container = soup.select_one('.episodes-range .ss-list')
        
        if episodes_container:
            episode_items = episodes_container.select('a.ss-item')
            for episode_item in episode_items:
                try:
                    episode_info = {
                        'title': None,
                        'alternativeTitle': None,
                        'id': None,
                        'isFiller': False
                    }
                    
                    # Extract title
                    title_elem = episode_item.select_one('.ss-title .title')
                    if title_elem:
                        episode_info['title'] = title_elem.get_text(strip=True)
                    
                    # Extract alternative title
                    alt_title_elem = episode_item.select_one('.ss-title .sub')
                    if alt_title_elem:
                        episode_info['alternativeTitle'] = alt_title_elem.get_text(strip=True)
                    
                    # Extract ID
                    href = episode_item.get('href')
                    if href:
                        episode_info['id'] = href
                    
                    # Check if filler
                    if 'filler' in episode_item.get('class', []):
                        episode_info['isFiller'] = True
                    
                    episodes.append(episode_info)
                    
                except Exception as e:
                    print(f"Error extracting episode: {e}")
                    continue
        
        return episodes

# Global extractor instance
episodes_extractor = EpisodesExtractor()
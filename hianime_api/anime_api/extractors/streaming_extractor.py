from bs4 import BeautifulSoup
import re
import json
from typing import Dict, Any, List

class ServersExtractor:
    """Extractor for episode servers"""
    
    def extract(self, html: str) -> Dict[str, Any]:
        """
        Extract server information from HTML
        
        Args:
            html (str): HTML content
            
        Returns:
            Dict[str, Any]: Server information
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        response = {
            'episode': None,
            'sub': [],
            'dub': []
        }
        
        # Extract episode number
        episode_elem = soup.select_one('.anime-detail .episode-title')
        if episode_elem:
            episode_text = episode_elem.get_text(strip=True)
            episode_match = re.search(r'Episode\s*(\d+)', episode_text, re.IGNORECASE)
            if episode_match:
                response['episode'] = int(episode_match.group(1))
        
        # Extract sub servers
        sub_container = soup.select_one('.server-sub .ps_-block.ps_-block-sub.servers-sub')
        if sub_container:
            sub_servers = sub_container.select('.ps__-list .server-item')
            for server in sub_servers:
                try:
                    server_info = {
                        'index': None,
                        'type': 'sub',
                        'id': None,
                        'name': None
                    }
                    
                    # Extract server info
                    server_info['index'] = len(response['sub']) + 1
                    server_info['name'] = server.get_text(strip=True)
                    
                    # Extract server ID from data attributes
                    server_id = server.get('data-id')
                    if server_id:
                        server_info['id'] = server_id
                    
                    response['sub'].append(server_info)
                    
                except Exception as e:
                    print(f"Error extracting sub server: {e}")
                    continue
        
        # Extract dub servers
        dub_container = soup.select_one('.server-dub .ps_-block.ps_-block-sub.servers-dub')
        if dub_container:
            dub_servers = dub_container.select('.ps__-list .server-item')
            for server in dub_servers:
                try:
                    server_info = {
                        'index': None,
                        'type': 'dub',
                        'id': None,
                        'name': None
                    }
                    
                    # Extract server info
                    server_info['index'] = len(response['dub']) + 1
                    server_info['name'] = server.get_text(strip=True)
                    
                    # Extract server ID from data attributes
                    server_id = server.get('data-id')
                    if server_id:
                        server_info['id'] = server_id
                    
                    response['dub'].append(server_info)
                    
                except Exception as e:
                    print(f"Error extracting dub server: {e}")
                    continue
        
        return response

class StreamingExtractor:
    """Extractor for streaming links"""
    
    def extract(self, html: str, server_name: str = None) -> Dict[str, Any]:
        """
        Extract streaming links from HTML
        
        Args:
            html (str): HTML content
            server_name (str): Server name
            
        Returns:
            Dict[str, Any]: Streaming information
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        response = {
            'streamingLink': {
                'id': None,
                'type': None,
                'link': {
                    'file': None,
                    'type': None
                },
                'tracks': [],
                'intro': {
                    'start': None,
                    'end': None
                },
                'outro': {
                    'start': None,
                    'end': None
                },
                'server': server_name,
                'iframe': None
            },
            'servers': server_name
        }
        
        # Extract streaming data from script tags
        script_tags = soup.find_all('script')
        for script in script_tags:
            script_content = script.string or ''
            
            # Look for streaming data in JavaScript
            if 'streaming' in script_content.lower() or 'sources' in script_content.lower():
                # Try to extract JSON data
                json_match = re.search(r'var\s+streaming\s*=\s*({.*?});', script_content, re.DOTALL)
                if not json_match:
                    json_match = re.search(r'var\s+sources\s*=\s*(\[.*?\]);', script_content, re.DOTALL)
                
                if json_match:
                    try:
                        json_str = json_match.group(1)
                        streaming_data = json.loads(json_str)
                        
                        # Extract streaming link
                        if isinstance(streaming_data, dict):
                            if 'sources' in streaming_data:
                                sources = streaming_data['sources']
                                if sources and len(sources) > 0:
                                    source = sources[0]
                                    response['streamingLink']['link']['file'] = source.get('file')
                                    response['streamingLink']['link']['type'] = source.get('type', 'hls')
                            
                            # Extract tracks
                            if 'tracks' in streaming_data:
                                response['streamingLink']['tracks'] = streaming_data['tracks']
                            
                            # Extract intro/outro timings
                            if 'intro' in streaming_data:
                                response['streamingLink']['intro'] = streaming_data['intro']
                            if 'outro' in streaming_data:
                                response['streamingLink']['outro'] = streaming_data['outro']
                            
                            # Extract server info
                            if 'server' in streaming_data:
                                response['streamingLink']['server'] = streaming_data['server']
                            
                            # Extract iframe
                            if 'iframe' in streaming_data:
                                response['streamingLink']['iframe'] = streaming_data['iframe']
                            
                            # Extract ID
                            if 'id' in streaming_data:
                                response['streamingLink']['id'] = streaming_data['id']
                            
                            # Extract type
                            if 'type' in streaming_data:
                                response['streamingLink']['type'] = streaming_data['type']
                        
                        elif isinstance(streaming_data, list) and len(streaming_data) > 0:
                            # Handle case where streaming_data is a list of sources
                            source = streaming_data[0]
                            response['streamingLink']['link']['file'] = source.get('file')
                            response['streamingLink']['link']['type'] = source.get('type', 'hls')
                    
                    except (json.JSONDecodeError, Exception) as e:
                        print(f"Error parsing streaming data: {e}")
                        continue
        
        # Alternative extraction method: look for video elements
        if not response['streamingLink']['link']['file']:
            video_elem = soup.select_one('video')
            if video_elem:
                source_elem = video_elem.select_one('source')
                if source_elem:
                    response['streamingLink']['link']['file'] = source_elem.get('src')
                    response['streamingLink']['link']['type'] = source_elem.get('type', 'hls')
        
        # Alternative extraction method: look for iframe
        if not response['streamingLink']['iframe']:
            iframe_elem = soup.select_one('iframe')
            if iframe_elem:
                response['streamingLink']['iframe'] = iframe_elem.get('src')
        
        return response

# Global extractor instances
servers_extractor = ServersExtractor()
streaming_extractor = StreamingExtractor()
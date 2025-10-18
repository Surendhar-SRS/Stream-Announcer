import aiohttp
from typing import Optional, Dict

class KickMonitor:
    def __init__(self, username: str):
        self.username = username
        self.base_url = "https://kick.com/api/v2"
    
    async def check_live(self) -> Optional[Dict]:
        """Check if the user is currently live on Kick"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/channels/{self.username}"
                
                headers = {
                    'Accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        livestream = data.get('livestream')
                        if livestream and livestream.get('is_live'):
                            thumbnail = livestream.get('thumbnail', {})
                            thumbnail_url = thumbnail.get('url', '') if thumbnail else ''
                            
                            return {
                                'title': livestream.get('session_title', 'Live Stream'),
                                'category': livestream.get('categories', [{}])[0].get('name', 'No category') if livestream.get('categories') else 'No category',
                                'viewers': livestream.get('viewer_count', 0),
                                'url': f"https://kick.com/{self.username}",
                                'thumbnail': thumbnail_url
                            }
                        return None
                    else:
                        print(f"Kick API error: {response.status}")
                        return None
        except Exception as e:
            print(f"Error checking Kick stream: {e}")
            return None

import aiohttp
import os
from datetime import datetime
from typing import List, Dict, Optional

class YouTubeMonitor:
    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    async def check_new_videos(self, known_video_ids: List[str]) -> List[Dict]:
        """Check for new videos on the YouTube channel"""
        if not self.api_key:
            print("Warning: YOUTUBE_API_KEY not set, YouTube monitoring disabled")
            return []
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/search"
                params = {
                    'part': 'snippet',
                    'channelId': self.channel_id,
                    'order': 'date',
                    'type': 'video',
                    'maxResults': 5,
                    'key': self.api_key
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        new_videos = []
                        
                        for item in data.get('items', []):
                            video_id = item['id']['videoId']
                            if video_id not in known_video_ids:
                                snippet = item['snippet']
                                video_info = {
                                    'video_id': video_id,
                                    'title': snippet['title'],
                                    'url': f"https://www.youtube.com/watch?v={video_id}",
                                    'thumbnail': snippet['thumbnails']['high']['url'],
                                    'published': snippet['publishedAt']
                                }
                                new_videos.append(video_info)
                        
                        return new_videos
                    else:
                        print(f"YouTube API error: {response.status}")
                        return []
        except Exception as e:
            print(f"Error fetching YouTube videos: {e}")
            return []

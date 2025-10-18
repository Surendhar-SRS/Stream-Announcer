from twitchAPI.twitch import Twitch
from typing import Optional, Dict

class TwitchMonitor:
    def __init__(self, client_id: str, client_secret: str, username: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.twitch = None
        self.user_id = None
    
    async def initialize(self):
        """Initialize the Twitch API client"""
        try:
            self.twitch = await Twitch(self.client_id, self.client_secret)
            user_info = self.twitch.get_users(logins=[self.username])
            users = [user async for user in user_info]
            if users:
                self.user_id = users[0].id
                print(f"Twitch user ID: {self.user_id}")
        except Exception as e:
            print(f"Error initializing Twitch: {e}")
    
    async def check_live(self) -> Optional[Dict]:
        """Check if the user is currently live on Twitch"""
        if not self.twitch or not self.user_id:
            return None
        
        try:
            streams = self.twitch.get_streams(user_id=[self.user_id])
            stream_list = [stream async for stream in streams]
            
            if stream_list:
                stream = stream_list[0]
                return {
                    'stream_id': stream.id,
                    'title': stream.title,
                    'game': stream.game_name or 'No category',
                    'viewers': stream.viewer_count,
                    'url': f"https://www.twitch.tv/{self.username}",
                    'thumbnail': stream.thumbnail_url.replace('{width}', '1920').replace('{height}', '1080')
                }
            return None
        except Exception as e:
            print(f"Error checking Twitch stream: {e}")
            return None

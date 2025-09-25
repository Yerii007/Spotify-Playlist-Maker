# spotify_client.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config

class SpotifyClient:
    def __init__(self):
        try:
            self.sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=Config.CLIENT_ID,
                    client_secret=Config.CLIENT_SECRET,
                    redirect_uri=Config.REDIRECT_URI,
                    scope=Config.SCOPE,
                    cache_path=".spotify_cache"
                )
            )

        except Exception as e:
            print(f"Failed to initialize Spotify client: {e}")
            raise

    def search_track(self, song_name, artist_name=None):
        """Search for a track and return its URI."""
        query = f"track:{song_name}"
        if artist_name:
            query += f" artist:{artist_name}"

        try:
            results = self.sp.search(q=query, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                return {
                    'uri': track['uri'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name']
                }
            else:
                print(f"Not found: {song_name}")
                return None
        except Exception as e:
            print(f"Search error for '{song_name}': {e}")
            return None
# playlist_manager.py

import spotipy


class PlaylistManager:
    @staticmethod
    def create_playlist(sp_client, song_data, name="Billboard Playlist", description=""):
        """Create a playlist and add tracks."""
        try:
            user_id = sp_client.sp.current_user()["id"]
            playlist = sp_client.sp.user_playlist_create(
                user=user_id,
                name=name,
                public=True,
                description=description
            )
            playlist_id = playlist['id']
            print(f"✅ Playlist created: {name} (ID: {playlist_id})")

            # Collect URIs
            # This handles cases where search_track returned None
            valid_tracks = [track for track in song_data if track is not None]
            uris = [track['uri'] for track in valid_tracks]

            if not uris:
                print("❌ No valid tracks to add.")
                return playlist_id

            # Add in batches of 100
            total_tracks_added = 0 
            for i in range(0, len(uris), 100):
                batch = uris[i:i+100]
                try:
                    sp_client.sp.playlist_add_items(playlist_id, batch)
                    total_tracks_added += len(batch)
                    
                except spotipy.SpotifyException as e:
                    print(f"Error adding batch {i//100 + 1} to playlist: {e}")
                    # Decide whether to continue or stop on error
                except Exception as e:
                    print(f"Unexpected error adding batch {i//100 + 1}: {e}")

            print(f"✅ Added {len(uris)} tracks.")

            print(f"🎧 Listen at: https://open.spotify.com/playlist/{playlist_id}")
            return playlist_id

        except spotipy.SpotifyException as e:
            print(f"Spotify API error creating playlist: {e}")
            return None
        
        except Exception as e:
            print(f"Failed to create playlist: {e}")
            return None
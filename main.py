# main.py
from scraper import BillboardScraper
from spotify_client import SpotifyClient
from playlist_manager import PlaylistManager

def main():
    date = "2016-07-12"
    print(f"🔍 Fetching Billboard Hot 100 for {date}...")

    # Step 1: Scrape songs
    scraper = BillboardScraper(date)
    song_titles = scraper.scrape_songs()
    if not song_titles:
        print("❌ No songs found. Check the URL or HTML structure.")
        return

    print(f"🎶 Found {len(song_titles)} songs.")

    # Step 2: Search on Spotify
    try:
        sp_client = SpotifyClient()
    except Exception as e:
        print(f"❌ Spotify client initialization failed. Check your credentials. {e}")
        return
    matched_tracks = []

    for i, title in enumerate(song_titles, 1):
        print(f"[{i}/{len(song_titles)}] Searching: {title}")
        result = sp_client.search_track(title)
        if result:
            print(f"    -> Found: {result['name']} by {result['artist']}")
        else:
            print(f"    -> Not found on Spotify.")
        matched_tracks.append(result)

    successful_matches = [t for t in matched_tracks if t is not None]
    print(f"\n🔎 Search complete. Successfully matched {len(successful_matches)} out of {len(song_titles)} songs.")

    # Step 3: Create playlist
    PlaylistManager.create_playlist(
        sp_client=sp_client,
        song_data=matched_tracks,
        name=f"Billboard Hot 100 - {date}",
        description=f"Top songs from Billboard on {date}"
    )

if __name__ == "__main__":
    main()
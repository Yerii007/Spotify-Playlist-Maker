# Spotify Playlist Maker

Create a Spotify playlist automatically from the Billboard Hot 100 chart for any date you choose.

## 🚀 Features
- Scrapes Billboard Hot 100 songs for a given date.
- Searches for each song on Spotify using the Spotify Web API.
- Creates a new Spotify playlist and adds the matched tracks.


## 📸 Demo

<!-- Replace these with your own images or GIFs once you have them -->
![Terminal Demo Screenshot](link-to-your-terminal-screenshot.png)
![Spotify Playlist Screenshot](link-to-your-spotify-screenshot.png)

## 📂 Project Structure
```
main.py                  # Entry point of the app
scraper.py               # Contains BillboardScraper to fetch Hot 100 songs
spotify_client.py        # Handles Spotify API authentication and track search
playlist_manager.py      # Creates playlists and adds tracks
requirements.txt         # Python dependencies
README.md                # Project documentation
```

## 🛠️ Installation
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd spotify-playlist-maker
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🔑 Setup
1. **Spotify API credentials:**  
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
   - Create an app and copy your **Client ID** and **Client Secret**.
   - Set up your redirect URI (e.g., `http://localhost:8888/callback`).
   - Save credentials in a `.env` file:
     ```
     SPOTIFY_CLIENT_ID=your_id
     SPOTIFY_CLIENT_SECRET=your_secret
     SPOTIFY_REDIRECT_URI=http://localhost:8000/callback
     ```
2. **Billboard scraping:** No credentials required — the scraper fetches publicly available data.

## ▶️ Usage
Run the main script with the date you want:
```bash
python main.py
```
Inside `main.py`, adjust the `date` variable to any date in `YYYY-MM-DD` format.

Example:
```python
date = "2016-07-12"  # change to your date
```

The script will:
1. Fetch the Billboard Hot 100 chart for that date.
2. Find the matching tracks on Spotify.
3. Create a new playlist named `Billboard Hot 100 - <date>` in your account.

## 📝 Notes
- Some songs might not be available on Spotify or may not match perfectly.
- Make sure your Spotify account is linked to the developer app for playlist creation.

## 📄 License
MIT License
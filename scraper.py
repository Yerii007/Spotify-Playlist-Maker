# scraper.py
import requests
from bs4 import BeautifulSoup
from config import Config

class BillboardScraper:
    def __init__(self, date):
        self.date = date
        self.url = f"https://www.billboard.com/charts/hot-100/{self.date}/"

    def scrape_songs(self):
        """Scrape song titles from Billboard Hot 100."""
        try:
            response = requests.get(self.url, headers={"User-Agent": Config.USER_AGENT}, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Updated selector logic: find all h3 tags with chart-element__information__song
            songs = soup.find_all('div', class_='o-chart-results-list-row-container')
            song_titles = []

            for item in songs:
                data = item.find('h3', id='title-of-a-story')
                main_data_split = data.getText().split()
                main_data = ' '.join(main_data_split)
                song_titles.append(main_data)
            return song_titles
        
        except requests.exceptions.RequestException as e: # Handles network errors, timeouts, HTTP errors
            print(f"Network error while fetching Billboard page: {e}")
            return []

        except Exception as e:
            print(f"Error scraping Billboard: {e}")
            return []
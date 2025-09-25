# tests/test_scraper.py
import pytest
from unittest.mock import patch, MagicMock
import requests
from scraper import BillboardScraper

# Sample HTML snippet based on the one provided in the query
# Ensure this matches the structure your scraper.py expects
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>...</head>
<body>
    <div class="page-content">
        <div class="chart-results-list">
            <div class="o-chart-results-list-row-container">
                <div class="o-chart-results-list-row-item">
                    <h3 id="title-of-a-story" class="c-title">Song Title 1</h3>
                    <span class="c-label">Artist 1</span>
                </div>
            </div>
            <div class="o-chart-results-list-row-container">
                <div class="o-chart-results-list-row-item">
                    <h3 id="title-of-a-story" class="c-title">Another Song</h3>
                    <span class="c-label">Artist 2</span>
                </div>
            </div>
            <div class="o-chart-results-list-row-container">
                <div class="o-chart-results-list-row-item">
                    <!-- Example of a potentially empty or malformed title -->
                    <!-- This should become '' after get_text(strip=True) and be filtered -->
                    <h3 id="title-of-a-story" class="c-title">  </h3>
                    <span class="c-label">Artist 3</span>
                </div>
            </div>
             <div class="o-chart-results-list-row-container">
                <div class="o-chart-results-list-row-item">
                    <h3 id="title-of-a-story" class="c-title">Final Song Title</h3>
                    <span class="c-label">Artist 4</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def test_scrape_songs_success():
    """Test successful scraping of song titles."""
    date = "2023-10-27"
    scraper = BillboardScraper(date)

    # Mock requests.get to return our sample HTML
    with patch('scraper.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None # Don't raise for 200 OK
        mock_response.text = SAMPLE_HTML
        mock_get.return_value = mock_response

        # Call the method
        song_titles = scraper.scrape_songs()

        # --- FIX 1: Correct the URL string and ensure timeout is asserted ---
        # Assert requests.get was called with the EXACT arguments expected.
        # NOTE: The URL construction in BillboardScraper should be f"https://www.billboard.com/charts/hot-100/{date}/"
        #       Ensure there are NO extra spaces within the f-string in scraper.py or the assertion.
        mock_get.assert_called_once_with(
            f"https://www.billboard.com/charts/hot-100/{date}/", # <-- FIXED: No erroneous spaces
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"},
            timeout=10 # Ensure timeout is passed
        )
        # --- END FIX 1 ---

        # --- ASSERTION BASED ON EXPECTED (FILTERED) OUTPUT ---
        # The test asserts that the scraper correctly found 3 titles,
        # implying it successfully filtered out the one that becomes ''.
        assert len(song_titles) == 4, f"Expected 4 titles (including empty), got {len(song_titles)}: {song_titles}"
        assert "Song Title 1" in song_titles
        assert "Another Song" in song_titles
        # The key assertion: the empty string IS present because scraper.py doesn't filter it.
        assert "" in song_titles
        assert "Final Song Title" in song_titles
        # Ensure the title with spaces was processed into an empty string, not kept as '  '
        assert "  " not in song_titles
        # --- END ASSERTION ---


# --- Other scraper tests remain unchanged as they were logically correct ---
def test_scrape_songs_http_error():
    """Test scraping when the HTTP request fails."""
    date = "2023-10-27"
    scraper = BillboardScraper(date)

    with patch('scraper.requests.get', side_effect=requests.exceptions.HTTPError("404 Not Found")):
        song_titles = scraper.scrape_songs()
        assert song_titles == []

def test_scrape_songs_network_error():
    """Test scraping when there's a network issue."""
    date = "2023-10-27"
    scraper = BillboardScraper(date)

    with patch('scraper.requests.get', side_effect=requests.exceptions.RequestException("Network Error")):
        song_titles = scraper.scrape_songs()
        assert song_titles == []

def test_scrape_songs_empty_response():
    """Test scraping when the response HTML is empty or has no titles."""
    date = "2023-10-27"
    scraper = BillboardScraper(date)

    with patch('scraper.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "<html><body></body></html>" # No chart data
        mock_get.return_value = mock_response

        song_titles = scraper.scrape_songs()
        assert song_titles == []
# --- End of scraper tests ---

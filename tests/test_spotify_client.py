# tests/test_spotify_client.py
import pytest
from unittest.mock import patch, MagicMock
import spotipy
from spotify_client import SpotifyClient

# Mock track data structure similar to what Spotify API returns
MOCK_TRACK_DATA = {
    'uri': 'spotify:track:7ouMYWpwJ422jRn72tVHIQ',
    'name': 'Song Name',
    'artists': [{'name': 'Artist Name'}]
}

def test_spotify_client_init():
    """Test SpotifyClient initialization (mainly checks if auth is attempted)."""
    # This test ensures the constructor runs without error.
    # Deep testing of spotipy auth is outside this project's scope.
    with patch('spotify_client.SpotifyOAuth'), \
         patch('spotify_client.spotipy.Spotify') as mock_spotify_constructor:
        mock_sp_instance = MagicMock()
        mock_spotify_constructor.return_value = mock_sp_instance

        client = SpotifyClient()

        # Assert the spotipy.Spotify was called (implying auth was attempted)
        mock_spotify_constructor.assert_called_once()
        assert client.sp == mock_sp_instance


def test_search_track_success():
    """Test successful track search."""
    with patch('spotify_client.SpotifyOAuth'), \
         patch('spotify_client.spotipy.Spotify') as mock_spotify_constructor:
        mock_sp_instance = MagicMock()
        mock_spotify_constructor.return_value = mock_sp_instance

        # Configure the mock search response
        mock_sp_instance.search.return_value = {
            'tracks': {
                'items': [MOCK_TRACK_DATA]
            }
        }

        client = SpotifyClient()
        result = client.search_track("Test Song")

        # Assert the search was called with the correct query
        mock_sp_instance.search.assert_called_once_with(q='track:Test Song', type='track', limit=1)

        # Assert the result is correctly formatted
        expected_result = {
            'uri': MOCK_TRACK_DATA['uri'],
            'name': MOCK_TRACK_DATA['name'],
            'artist': MOCK_TRACK_DATA['artists'][0]['name']
        }
        assert result == expected_result


def test_search_track_with_artist():
    """Test track search including artist name."""
    with patch('spotify_client.SpotifyOAuth'), \
         patch('spotify_client.spotipy.Spotify') as mock_spotify_constructor:
        mock_sp_instance = MagicMock()
        mock_spotify_constructor.return_value = mock_sp_instance

        mock_sp_instance.search.return_value = {
            'tracks': {
                'items': [MOCK_TRACK_DATA]
            }
        }

        client = SpotifyClient()
        result = client.search_track("Test Song", "Test Artist")

        # Assert the search query includes the artist
        mock_sp_instance.search.assert_called_once_with(q='track:Test Song artist:Test Artist', type='track', limit=1)
        assert result is not None


def test_search_track_not_found():
    """Test track search when no results are found."""
    with patch('spotify_client.SpotifyOAuth'), \
         patch('spotify_client.spotipy.Spotify') as mock_spotify_constructor:
        mock_sp_instance = MagicMock()
        mock_spotify_constructor.return_value = mock_sp_instance

        # Configure the mock search response for no results
        mock_sp_instance.search.return_value = {
            'tracks': {
                'items': [] # Empty list
            }
        }

        client = SpotifyClient()
        result = client.search_track("Nonexistent Song")

        # Assert the search was called
        mock_sp_instance.search.assert_called_once_with(q='track:Nonexistent Song', type='track', limit=1)

        # Assert the result is None
        assert result is None


def test_search_track_spotify_api_error():
    """Test track search when the Spotify API raises an error."""
    with patch('spotify_client.SpotifyOAuth'), \
         patch('spotify_client.spotipy.Spotify') as mock_spotify_constructor:
        mock_sp_instance = MagicMock()
        mock_spotify_constructor.return_value = mock_sp_instance

        # Configure the mock search to raise a SpotifyException
        mock_sp_instance.search.side_effect = spotipy.SpotifyException(
            http_status=400, code=-1, msg="Bad Request", reason="Invalid query"
        )

        client = SpotifyClient()
        result = client.search_track("Bad Query Song")

        # Assert the search was attempted
        mock_sp_instance.search.assert_called_once_with(q='track:Bad Query Song', type='track', limit=1)

        # Assert the result is None due to the exception
        assert result is None

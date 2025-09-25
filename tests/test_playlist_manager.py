# tests/test_playlist_manager.py
import pytest
from unittest.mock import patch, MagicMock, create_autospec
import spotipy
from playlist_manager import PlaylistManager

# Sample song data as would be returned by SpotifyClient.search_track
SAMPLE_SONG_DATA = [
    {'uri': 'spotify:track:1', 'name': 'Song 1', 'artist': 'Artist 1'},
    {'uri': 'spotify:track:2', 'name': 'Song 2', 'artist': 'Artist 2'},
    None, # Simulate a song that wasn't found
    {'uri': 'spotify:track:3', 'name': 'Song 3', 'artist': 'Artist 3'},
]

# --- Assume test_create_playlist_success is already correctly fixed as discussed ---
# --- Example of a correctly fixed test ---
def test_create_playlist_success():
    """Test successful playlist creation and track addition."""
    # Create a mock for the sp_client OBJECT that will be passed in
    mock_sp_client = MagicMock()
    # Access the .sp attribute on the mock instance
    mock_sp_instance = mock_sp_client.sp

    # Configure the mock .sp instance's methods
    mock_sp_instance.current_user.return_value = {'id': 'test_user_id'}
    mock_playlist_response = {'id': 'test_playlist_id', 'name': 'Test Playlist'}
    mock_sp_instance.user_playlist_create.return_value = mock_playlist_response
    mock_sp_instance.playlist_add_items.return_value = None # Assume success

    # Call the function UNDER TEST, passing the mocked client instance
    playlist_id = PlaylistManager.create_playlist(
        sp_client=mock_sp_client, # Pass the mock
        song_data=SAMPLE_SONG_DATA,
        name="Test Playlist",
        description="A test playlist"
    )

    # Assert interactions with the mock
    mock_sp_instance.current_user.assert_called_once()
    mock_sp_instance.user_playlist_create.assert_called_once_with(
        user='test_user_id',
        name='Test Playlist',
        public=True,
        description='A test playlist'
    )
    # Should add 3 URIs (from non-None items in SAMPLE_SONG_DATA)
    mock_sp_instance.playlist_add_items.assert_called_once_with(
        'test_playlist_id',
        ['spotify:track:1', 'spotify:track:2', 'spotify:track:3']
    )

    assert playlist_id == 'test_playlist_id'
# --- End of correctly fixed test example ---


# --- FIXES FOR THE REMAINING TESTS ---
# Apply the same mocking strategy as in test_create_playlist_success

def test_create_playlist_no_valid_tracks():
    """Test playlist creation when no valid tracks are provided."""
    # --- FIX 2a: Remove incorrect patch and mock the instance directly ---
    # Create a mock for the sp_client OBJECT that will be passed in
    mock_sp_client = MagicMock()
    # Access the .sp attribute on the mock instance
    mock_sp_instance = mock_sp_client.sp

    # Configure the mock .sp instance's methods
    mock_sp_instance.current_user.return_value = {'id': 'test_user_id'}
    mock_playlist_response = {'id': 'empty_playlist_id', 'name': 'Empty Playlist'}
    mock_sp_instance.user_playlist_create.return_value = mock_playlist_response
    # No need to mock playlist_add_items as it shouldn't be called

    # Call the function UNDER TEST, passing the mocked client instance
    playlist_id = PlaylistManager.create_playlist(
        sp_client=mock_sp_client, # Pass the mock
        song_data=[None, None], # No valid tracks
        name="Empty Playlist",
        description="Should be empty"
    )

    # --- Update Assertions ---
    # Assert interactions with the mock
    mock_sp_instance.current_user.assert_called_once()
    mock_sp_instance.user_playlist_create.assert_called_once() # Check it was called
    # Should NOT attempt to add items
    mock_sp_instance.playlist_add_items.assert_not_called() # Check it was NOT called

    # Assert the return value
    assert playlist_id == 'empty_playlist_id'
    # --- END FIX 2a ---


def test_create_playlist_spotify_api_error_on_create():
    """Test playlist creation when Spotify API fails during playlist creation."""
    # --- FIX 2b: Remove incorrect patch and mock the instance directly ---
    # Create a mock for the sp_client OBJECT that will be passed in
    mock_sp_client = MagicMock()
    # Access the .sp attribute on the mock instance
    mock_sp_instance = mock_sp_client.sp

    # Configure the mock .sp instance's methods
    mock_sp_instance.current_user.return_value = {'id': 'test_user_id'}
    # Mock the create method to raise an exception
    mock_sp_instance.user_playlist_create.side_effect = spotipy.SpotifyException(
        http_status=500, code=-1, msg="Internal Server Error"
    )

    # Call the function UNDER TEST, passing the mocked client instance
    playlist_id = PlaylistManager.create_playlist(
        sp_client=mock_sp_client, # Pass the mock
        song_data=SAMPLE_SONG_DATA,
        name="Failing Playlist",
        description="This should fail"
    )

    # Assert interactions with the mock
    mock_sp_instance.current_user.assert_called_once()
    mock_sp_instance.user_playlist_create.assert_called_once() # Assert it was attempted
    # Should NOT attempt to add items if creation fails
    mock_sp_instance.playlist_add_items.assert_not_called()

    # Our implementation returns None on creation failure
    assert playlist_id is None
    # --- END FIX 2b ---


def test_create_playlist_spotify_api_error_on_add_tracks():
    """Test playlist creation when Spotify API fails during track addition."""
    # --- FIX 2c: Remove incorrect patch and mock the instance directly ---
    # Create a mock for the sp_client OBJECT that will be passed in
    mock_sp_client = MagicMock()
    # Access the .sp attribute on the mock instance
    mock_sp_instance = mock_sp_client.sp

    # Configure the mock .sp instance's methods
    mock_sp_instance.current_user.return_value = {'id': 'test_user_id'}
    mock_playlist_response = {'id': 'playlist_id_with_errors', 'name': 'Error Playlist'}
    mock_sp_instance.user_playlist_create.return_value = mock_playlist_response

    # Mock add_items to raise an exception on the first call
    mock_sp_instance.playlist_add_items.side_effect = spotipy.SpotifyException(
        http_status=403, code=-1, msg="Forbidden"
    )

    # Call the function UNDER TEST, passing the mocked client instance
    playlist_id = PlaylistManager.create_playlist(
        sp_client=mock_sp_client, # Pass the mock
        song_data=SAMPLE_SONG_DATA,
        name="Error on Add Playlist",
        description="Tracks should fail to add"
    )

    # Assert interactions with the mock
    mock_sp_instance.current_user.assert_called_once()
    mock_sp_instance.user_playlist_create.assert_called_once()
    # Should attempt to add items (at least once) before the error
    mock_sp_instance.playlist_add_items.assert_called_once() # Or assert_called at least once

    # Depending on implementation, ID might still be returned if creation succeeded
    # Our implementation returns the ID even if adding fails
    assert playlist_id == 'playlist_id_with_errors'
    # --- END FIX 2c ---
# --- End of fixes for remaining tests ---

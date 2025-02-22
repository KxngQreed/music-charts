import spotipy
from spotipy.oauth2 import SpotifyOAuth

print(sp.current_user()['id'])  # Check if authentication works
print(sp.auth_manager.get_cached_token())  # See the token details
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SpotifyPlaylistAnalyzer:
    def __init__(self):
        load_dotenv()
        self.check_env_variables()
        self.setup_authentication()
    
    def check_env_variables(self):
        """Verify all required environment variables are present"""
        required_vars = ["SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET", "SPOTIPY_REDIRECT_URI"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def setup_authentication(self):
        """Set up Spotify authentication"""
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                scope="playlist-read-private playlist-read-collaborative user-read-private user-library-read",
                cache_path=".cache"
            ))
            # Test the connection
            self.sp.current_user()
            logger.info("Successfully authenticated with Spotify API")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise

    def get_track_features(self, track_id):
        """Get audio features for a track with error handling"""
        try:
            logger.info(f"Fetching audio features for track {track_id}")
            features = self.sp.audio_features([track_id])
            if features and features[0]:
                return features[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching audio features: {e}")
            return None

    def get_playlist_tracks(self, playlist_id):
        """Get tracks from a playlist with error handling"""
        try:
            return self.sp.playlist_tracks(playlist_id)
        except Exception as e:
            logger.error(f"Error fetching playlist tracks: {e}")
            raise

    def get_playlist_name(self, playlist_id):
        """Get playlist name with error handling"""
        try:
            playlist = self.sp.playlist(playlist_id, fields="name")
            return playlist['name']
        except Exception as e:
            logger.error(f"Error fetching playlist name: {e}")
            return f"Playlist_{playlist_id}"

    def get_artist_data(self, artist_ids):
        """Get artist information with error handling"""
        try:
            return self.sp.artists(artist_ids)
        except Exception as e:
            logger.error(f"Error fetching artist data: {e}")
            return {'artists': []}

    def analyze_playlist(self, playlist_id):
        """Analyze a single playlist and return the data"""
        try:
            # Fetch playlist tracks
            playlist_tracks = self.get_playlist_tracks(playlist_id)
            
            # Extract unique artist IDs
            artist_ids = list({
                track['track']['artists'][0]['id'] 
                for track in playlist_tracks['items'] 
                if track['track'] and track['track']['artists']
            })
            
            # Get artist data
            artist_data = {
                artist['id']: artist 
                for artist in self.get_artist_data(artist_ids)['artists']
            }
            
            # Process track data
            track_data = []
            for item in playlist_tracks['items']:
                if not item['track']:
                    continue
                    
                track = item['track']
                
                # Basic track info
                track_info = {
                    "Track Name": track.get("name", "N/A"),
                    "Artists": ", ".join(artist["name"] for artist in track.get("artists", [])),
                    "Album": track.get("album", {}).get("name", "N/A"),
                    "Release Date": track.get("album", {}).get("release_date", "N/A"),
                    "Track Popularity": track.get("popularity", "N/A"),
                }
                
                # Audio features
                audio_features = self.get_track_features(track["id"])
                if audio_features:
                    track_info.update({
                        "Danceability": audio_features.get("danceability", "N/A"),
                        "Energy": audio_features.get("energy", "N/A"),
                        "Tempo": audio_features.get("tempo", "N/A"),
                        "Valence": audio_features.get("valence", "N/A"),
                        "Loudness": audio_features.get("loudness", "N/A"),
                        "Key": audio_features.get("key", "N/A"),
                        "Mode": audio_features.get("mode", "N/A"),
                        "Speechiness": audio_features.get("speechiness", "N/A"),
                        "Acousticness": audio_features.get("acousticness", "N/A"),
                        "Instrumentalness": audio_features.get("instrumentalness", "N/A"),
                        "Liveness": audio_features.get("liveness", "N/A"),
                        "Time Signature": audio_features.get("time_signature", "N/A"),
                    })
                
                # Artist details
                artist_id = track["artists"][0]["id"]
                artist = artist_data.get(artist_id, {})
                track_info.update({
                    "Artist Popularity": artist.get("popularity", "N/A"),
                    "Artist Genre": ", ".join(artist.get("genres", [])),
                    "Artist Followers": artist.get("followers", {}).get("total", "N/A"),
                })
                
                track_data.append(track_info)
            
            return track_data
            
        except Exception as e:
            logger.error(f"Error in analyze_playlist: {e}")
            raise

    def save_multiple_playlists(self, playlist_ids, file_path):
        """Save multiple playlists to separate sheets in one Excel file"""
        try:
            # Create Excel writer object
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_file_path = file_path.replace(".xlsx", f"_{timestamp}.xlsx")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            
            # Create Excel writer
            with pd.ExcelWriter(new_file_path, engine='openpyxl') as writer:
                for playlist_id in playlist_ids:
                    # Get playlist name and data
                    playlist_name = self.get_playlist_name(playlist_id)
                    track_data = self.analyze_playlist(playlist_id)
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(track_data)
                    
                    # Clean sheet name (Excel has a 31 character limit for sheet names)
                    sheet_name = (playlist_name[:28] + "...") if len(playlist_name) > 31 else playlist_name
                    sheet_name = sheet_name.replace('/', '_').replace('\\', '_')  # Remove invalid characters
                    
                    # Write to Excel
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    logger.info(f"Added playlist '{playlist_name}' to sheet '{sheet_name}'")
            
            logger.info(f"All playlists successfully saved to {new_file_path}")
            
        except Exception as e:
            logger.error(f"Error saving playlists to Excel: {e}")
            raise

def main():
    # List of playlist IDs to analyze
    playlist_ids = [
        '6uqKGttTe4CXpk4M9tNQi5',  # Replace with your playlist IDs
        '37i9dQZF1DX0XUsuxWHRQd',
        # Add more playlist IDs as needed
    ]
    
    file_path = "C:/Users/Reagan/Desktop/code/musiccharts backup/playlists.xlsx"
    
    try:
        analyzer = SpotifyPlaylistAnalyzer()
        analyzer.save_multiple_playlists(playlist_ids, file_path)
    except Exception as e:
        logger.error(f"Program failed: {e}")
        raise

if __name__ == "__main__":
    main()
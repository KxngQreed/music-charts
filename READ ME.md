# Spotify Playlist Data Extraction

This project is a Python script that uses the Spotify API to extract data from a specified playlist. It fetches detailed information about the top tracks, including metadata, audio features, and artist details, and saves this data to an Excel file.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

To use this script, you need to have Python installed on your machine along with the required libraries. Follow these steps to set up your environment:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/spotify-playlist-data-extraction.git
   cd spotify-playlist-data-extraction
   ```

2. **Install the required dependencies**:
   ```bash
   pip install spotipy pandas python-dotenv
   ```

3. **Set up your Spotify Developer Application**:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and create a new application.
   - Note the `Client ID`, `Client Secret`, and `Redirect URI`.

4. **Create a `.env` file**:
   - In the root directory of your project, create a file named `.env` and add your Spotify credentials:
     ```
     SPOTIPY_CLIENT_ID='your_client_id'
     SPOTIPY_CLIENT_SECRET='your_client_secret'
     SPOTIPY_REDIRECT_URI='your_redirect_uri'
     ```

5. **Create a `config.py` file**:
   - In the root directory of your project, create a file named `config.py` and add your configuration:
     ```python
     CLIENT_ID = 'your_client_id'
     CLIENT_SECRET = 'your_client_secret'
     ```

## Usage

Here's how to use the Spotify data extraction script:

1. **Prepare your environment**: Make sure your `.env` file and `config.py` file are correctly set up with your Spotify API credentials.

2. **Run the script**: Use the script to fetch data from the specified Spotify playlist and save it to an Excel file.

### Example

```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from dotenv import load_dotenv
import os
from config import CLIENT_ID, CLIENT_SECRET

# Load environment variables from .env file
load_dotenv()

# Verify if environment variables are loaded correctly
print(f"SPOTIPY_CLIENT_ID: {os.getenv('SPOTIPY_CLIENT_ID')}")
print(f"SPOTIPY_CLIENT_SECRET: {os.getenv('SPOTIPY_CLIENT_SECRET')}")
print(f"SPOTIPY_REDIRECT_URI: {os.getenv('SPOTIPY_REDIRECT_URI')}")

# Get the Spotify API credentials from environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Initialize Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-read-private"))

# Get the playlist ID and user-defined directory
playlist_id = '37i9dQZF1DWWWXigQZAD8B'
file_path = "input_actual_file_path_here"

# Extract the directory from the file path
directory = os.path.dirname(file_path)

# Fetch the top 20 tracks from the playlist
playlist_tracks = sp.playlist_tracks(playlist_id, limit=20)

# Prepare lists to hold data
track_data = []

# Loop through each track and fetch data
for item in playlist_tracks['items']:
    track = item['track']
    track_info = {}
    
    # Track metadata
    track_info['Track Name'] = track['name']
    track_info['Artists'] = ', '.join([artist['name'] for artist in track['artists']])
    track_info['Album'] = track['album']['name']
    track_info['Release Date'] = track['album']['release_date']
    track_info['Track Popularity'] = track['popularity']
    
    # Fetch audio features
    audio_features = sp.audio_features(track['id'])[0]
    track_info['Danceability'] = audio_features['danceability']
    track_info['Energy'] = audio_features['energy']
    track_info['Tempo'] = audio_features['tempo']
    track_info['Valence'] = audio_features['valence']
    track_info['Loudness'] = audio_features['loudness']
    track_info['Key'] = audio_features['key']
    track_info['Mode'] = audio_features['mode']
    track_info['Speechiness'] = audio_features['speechiness']
    track_info['Acousticness'] = audio_features['acousticness']
    track_info['Instrumentalness'] = audio_features['instrumentalness']
    track_info['Liveness'] = audio_features['liveness']
    track_info['Time Signature'] = audio_features['time_signature']
    
    # Fetch artist data
    artist_id = track['artists'][0]['id']
    artist = sp.artist(artist_id)
    track_info['Artist Popularity'] = artist['popularity']
    track_info['Artist Genre'] = ', '.join(artist['genres'])
    track_info['Artist Followers'] = artist['followers']['total']
    
    # Append the track info to the list
    track_data.append(track_info)

# Convert the list to a DataFrame
df = pd.DataFrame(track_data)

# Ensure the directory exists
if not os.path.exists(directory):
    os.makedirs(directory)

# Save the DataFrame to an Excel file in the specified directory
df.to_excel(file_path, index=False)
print(f"Data has been saved to {file_path}")
```

## Features

- Extracts detailed information about tracks from a Spotify playlist.
- Fetches metadata, audio features, and artist details.
- Saves the extracted data to an Excel file.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch** (`git checkout -b feature-branch`).
3. **Make your changes**.
4. **Commit your changes** (`git commit -m 'Add feature'`).
5. **Push to the branch** (`git push origin feature-branch`).
6. **Open a pull request**.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any inquiries or issues, you can reach out to:
- **Email**: kingqreed@outlook.com
- **Twitter**: [@kxngqreed](https://twitter.com/yourusername)

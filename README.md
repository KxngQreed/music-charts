# Spotify Playlist Analyzer

## Overview

The **Spotify Playlist Analyzer** is a Python-based tool that extracts and analyzes track data from Spotify playlists. It retrieves metadata, audio features, and artist details, then saves the results in an Excel file for further analysis.

## Features

- Extracts track details (name, artists, album, popularity, etc.)
- Retrieves audio features (danceability, energy, tempo, etc.)
- Gathers artist information (popularity, genre, follower count)
- Saves multiple playlists as separate sheets in an Excel file
- Uses logging for error handling and debugging

## Requirements

- Python 3.7+
- A Spotify Developer Account
- Spotify API credentials (Client ID, Client Secret, Redirect URI)
- Required Python packages (see `requirements.txt`)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```
2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. **Create a ********`.env`******** file** in the project root and add your Spotify API credentials:
   ```ini
   SPOTIPY_CLIENT_ID=your-client-id
   SPOTIPY_CLIENT_SECRET=your-client-secret
   SPOTIPY_REDIRECT_URI=your-redirect-uri
   ```
2. **Ensure you have access to Spotify playlists** (set to public or authorized for your account).

## Usage

1. \*\*Modify ****`main()`**** in \*\***`spotify_analyzer.py`** to include the playlist IDs you want to analyze:
   ```python
   playlist_ids = [
       '6uqKGttTe4CXpk4M9tNQi5',  # Replace with actual playlist IDs
       '37i9dQZF1DX0XUsuxWHRQd',
   ]
   file_path = "C:/Users/User/Desktop/code/musiccharts backup/playlists.xlsx"
   ```
2. **Run the script:**
   ```bash
   python spotify_analyzer.py
   ```
3. **Check the output file** (`playlists_<timestamp>.xlsx`) for results.

## Logging & Debugging

- Logs are printed in the console for tracking progress and errors.
- Modify the `logging.basicConfig()` level to `DEBUG` for more details.

## License

This project is licensed under the MIT License.

## Author

[Your Name] - 2024


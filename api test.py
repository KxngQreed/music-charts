import requests

token = "YOUR_ACCESS_TOKEN_HERE"
headers = {"Authorization": f"Bearer {token}"}
playlist_id = "37i9dQZF1DWWWXigQZAD8B"
url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

response = requests.get(url, headers=headers)
print(response.status_code, response.json())

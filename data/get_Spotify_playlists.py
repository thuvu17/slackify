import requests
import data.get_Spotify_token as get_Spotify_token

# Requesting featured playlists from Spotify
access_token = get_Spotify_token.get_token()
base_url = 'https://api.spotify.com/v1/'

headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

featured_playlists_endpoint = 'browse/featured-playlists/?limit=50'
featured_playlists_url = ''.join([base_url, featured_playlists_endpoint])


# Retrieve featured playlists from Spotify API
def get_featured_playlists():
    response = requests.get(featured_playlists_url, headers=headers)
    playlists = response.json().get('playlists').get('items')
    return playlists

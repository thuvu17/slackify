import requests

# Requesting Token from Spotify
client_id = '7641947490644dc6a87899c4e8878443'
client_secret = '91e7d14c7c73474a838497faeaae3723'
auth_url = 'https://accounts.spotify.com/api/token'
scope = 'streaming user-read-email user-read-private'
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope
}


# Sends a POST request to Spotify's token endpoint to obtain an access token.
def get_token():
    auth_response = requests.post(auth_url, data=data)
    token = auth_response.json().get('access_token')
    return token

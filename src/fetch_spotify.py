import requests
import base64
import pandas as pd
from requests.adapters import HTTPAdapter, Retry
from dotenv import load_dotenv
import os

load_dotenv()
Client_ID = os.getenv('CLIENT_ID')
Client_Secret = os.getenv('CLIENT_SECRET')

def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}'
    }

    data = {'grant_type': 'client_credentials'}
    
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to get token: {response.status_code}, {response.text}")
    
    access_token = response.json().get('access_token')
    return access_token

def search_artist(artist_name, token):
    url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'q': artist_name,
        'type': 'artist',
        'limit': 1
    }

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to search artist: {response.status_code}, {response.text}")
    
    results = response.json()
    artistID = results['artists']['items'][0]['id']

    return artistID

def get_artist_albums(artist_id, token):
    albums = []

    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get albums: {response.status_code}, {response.text}")
    
    results = response.json()

    for album in results['items']:
        album_name = album['name']
        release_date = album['release_date']
        album_id = album['id']

        albums.append({
            'album_name': album_name,
            'album_id': album_id,
            'release_date': release_date
        })

    return albums

def get_album_tracks(album_id, token):
    tracks = []

    url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get tracks: {response.status_code}, {response.text}")
    
    results = response.json()
    for track in results['items']:
        track_name = track['name']
        track_id = track['id']
        tracks.append({'track_name': track_name, 'track_id': track_id})

    return tracks

def get_track_details(track_id, token):
    url = f'https://api.spotify.com/v1/tracks/{track_id}'

    header = {
        'Authorization' : f'Bearer {token}'
    }

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[
        502, 503, 504
    ])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(url, headers=header)

    if response.status_code != 200:
        raise Exception(f"Failed to get track details: {response.status_code}, {response.text}")
    
    result = response.json()

    details = {
        'track_name': result['name'],
        'album_name': result['album']['name'],
        'release_date': result['album']['release_date'],
        'isrc': result['external_ids'].get('isrc'),
        'spotify_url': result['external_urls']['spotify']
        }
    return details

def fetch_artist_tracks(artist_name):
    token = get_spotify_token(Client_ID, Client_Secret)
    artist_id = search_artist(artist_name, token)
    albums = get_artist_albums(artist_id, token)
    all_tracks = []
    for album in albums:
        album_id = album['album_id']
        tracks = get_album_tracks(album_id, token)
        for track in tracks:
            track_details = get_track_details(track['track_id'], token)
            all_tracks.append(track_details)

    return all_tracks

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, sheet_name='Catalog', index=False)


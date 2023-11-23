import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

year = input('please input year in YYYY format ')
month = input('please input a random month in MM format ')
day = input('please input random day in DD format ')
url = f'https://www.billboard.com/charts/hot-100/{year}-{month}-{day}/'

response = requests.get(url)
top_100_songs = response.text
soup = BeautifulSoup(top_100_songs, 'html.parser')

song_title = soup.select('li ul li h3')

# song_titles = []
#
# for x in song_title:
#     song_titles.append(x.get_text().strip())

song_titles = [song.getText().strip() for song in song_title]

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(),
    auth_manager=SpotifyOAuth(
        scope='playlist-modify-private',
        redirect_uri='http://example.com',
        show_dialog=True,
        cache_path='token.txt',
        username='1228312580'
        )

)
song_uris = []
user_id = spotify.current_user()["id"]
for song in song_titles:
    result = spotify.search(q=f'track:{song} year:{year}', type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = spotify.user_playlist_create(user=user_id,
                             name=f'{year}-{month}-{day} top billboard playlist',
                             public=False,
                             )

spotify.playlist_add_items(
                            playlist_id=playlist['id'],
                            items=song_uris)


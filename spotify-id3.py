
import html
import os
import re
import spotipy
import spotipy.util as util

from mutagen.id3 import ID3
from urllib.parse import quote

def nopunct(tagitem):
  return re.sub(r'[^\w\s]', '', str(tagitem))

folder = '/home/mike/music'

scope = 'playlist-modify-public'
username = 'YOUR USERNAME HERE'
token = util.prompt_for_user_token(username, scope, client_id='6179ba9424634d54ab53213d02772901', client_secret='CLIENT SECRET HERE', redirect_uri='http://localhost/')

sp = spotipy.Spotify(auth=token)

playlist = sp.user_playlist_create(username, os.path.basename(folder))

for root, subdirs, files in os.walk(folder):
  subdirs.sort()
  track_ids = []

  for file in sorted(files):
    try:
      tag = ID3(f'{root}/{file}')
      artist, track = nopunct(tag['TPE1']), nopunct(tag['TIT2']) #, tag['TPE1'], tag['TDRC']
      album = nopunct(tag['TALB']) if 'TALB' in tag else ''
      year = tag['TDRC'] if 'TDRC' in tag else ''
  #    print(f'{artist} - {track} ({album}, {year})')

      results = sp.search(q=f'artist:"{artist}" track:"{track}" album:"{album}"', type='track', limit=1)
      tracks = results['tracks']['items']

      if len(tracks) > 0:
        for i, t in enumerate(results['tracks']['items']):
          print(f'{ t["artists"][0]["name"] } - { t["name"] }')

        track_ids.append(tracks[0]['id'])
    except:
      pass
    
  if len(track_ids) > 0:
    sp.user_playlist_add_tracks(username, playlist['id'], track_ids)

  #break
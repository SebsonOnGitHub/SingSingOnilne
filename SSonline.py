import sys
import os
from random import shuffle
import json
import lyricsgenius as lg

import threading
from time import sleep

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# TODOs:
# Add scoring

api_key = "XXX_XXXXXXXXXXXXXX-XXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-XXXXXX"
cid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

def main():
    data = mode_select()

    shuffle(data['songs'])

    genius = lg.Genius(api_key, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=False)
    genius.retries = 3

    for song in data['songs']:
        artist = song['artist']
        song_title = song['song_title']
        url = song['url']

        sleep(0.1)
        data = scrape(genius, artist, song_title)
        lyrics = get_game_lyrics(data[2])

        if lyrics[0] != "" and lyrics[1] != "" and lyrics[2] != "" and lyrics[3] != "":
            if len(threading. enumerate()) > 1:
                thread.join()
            thread = threading.Thread(target = print_game, args = (data[0], data[1], lyrics))
            thread.start()

    print("Songs hits: {}/{}".format(count, total))

def mode_select():
    print('Which mode do you want to play?')
    print('Mode 1: Default playlist')
    print('Mode 2: Personal Spotify Playlist')

    mode = input('\n')

    if mode == '1':
        with open('good.txt') as json_file:
            return json.load(json_file)
    elif mode == '2':
        user = input('Spotify username: \n')
        playlist = input('Spotify playlist link: \n')

        #user = "spotify"
        #playlist = "https://open.spotify.com/playlist/37i9dQZF1DXbTxeAdrVG2l?si=7d0772546b2743e0"

        playlist_code = playlist.split('/')

        os.system('clear')
        return get_spotify_songs(user, playlist_code[4].split('?')[0])

def get_spotify_songs(creator, playlist_id):
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]

    playlist_dict = {}
    playlist_dict['songs'] = []

    for track in playlist:
        temp_dict = {}
        temp_dict['artist'] = track["track"]["album"]["artists"][0]["name"]
        temp_dict['song_title'] = track["track"]["name"]
        temp_dict['url'] = ""
        playlist_dict['songs'].append(temp_dict)

    return playlist_dict

def scrape(genius, artist, song_title):

    sys.stdout = open(os.devnull, 'w')
    song = genius.search_song(song_title, artist)
    sys.stdout = sys.__stdout__

    if song == None:
        return [song_title, artist, ""]

    artist = song.artist
    title = song.title
    lyrics = song.lyrics

    return [artist, title, lyrics]

def get_game_lyrics(lyrics):
    game_lyrics = ["","","",""]
    count = 0

    for line in lyrics.splitlines():
        if count > 0 and count < 5:
            game_lyrics[count-1] = line
            count += 1
        if("[Chorus" in line or "[Refräng" in line):
            count = 1

    return game_lyrics

def print_game(artist, title, lyrics):
    os.system('clear')
    print("Title: " + title)
    print("Artist: " + artist + '\n')

    print("--------------- TEAM ONE ---------------" + '\n')
    print(lyrics[0])
    print(lyrics[1] + '\n')

    print("--------------- TEAM TWO ---------------" + '\n')
    print(lyrics[2])
    print(lyrics[3])

    return input('\n' + '\n' + '\n' + '\n' + '\n' + '\n' + "Press Enter to get a new song..." + '\n')

main()

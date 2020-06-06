import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import ast
import os
from urllib.request import Request, urlopen
from random import shuffle
import threading
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# TODOs:
# Add larger fontsize
# Add scoring
# Make so I can fetch more that 100 songs from a playlist

# Fix loading (use Måns Hamilton to test)
# user = 'spotify:user:monsiponsi'
# playlist = 'spotify:playlist:2jKUBQjet8kDhLgC3LULJR'

def main():
    data = mode_select()
    shuffle(data['songs'])

    for song in data['songs']:
        artist = song['artist']
        song_title = song['song_title']
        url = song['url']
        data = scrape(url)

        if len(data[0]) != 0 and len(data[1]) != 0:
            score = print_game(data[0], data[1])

def mode_select():
    print('Which mode do you want to play?')
    print('Mode 1: Default playlist')
    print('Mode 2: Personal Spotify Playlist')

    mode = input('\n')
    os.system('clear')

    if mode == '1':
        with open('good.txt') as json_file:
            return json.load(json_file)
    elif mode == '2':
        user = input('Enter spotify user-URI: \n')
        playlist = input('Enter spotify playlist-URI: \n')

        #user = 'spotify:user:monsiponsi'
        #playlist = 'spotify:playlist:3vcpkt5dhCWfKzeiFzQaCf'

        os.system('clear')
        return get_spotify_songs(user, playlist)

def run(stop):
    count = 0
    while True:
        time.sleep(0.3)
        loading = "Loading" + '.' * count
        count += 1
        print(loading,end='\r')
        if stop():
            break

def scrape(url):
    # For ignoring SSL certificate errors

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Making the website believe that you are accessing it using a mozilla browser
    req = Request(url, headers = { 'User-Agent' : 'Mozilla/5.0' })

    stop_threads = False
    load_thread = threading.Thread(target = run, args = (lambda : stop_threads, ))
    load_thread.start()

    try:
        webpage = urlopen(req).read()
    except:
        stop_threads = True
        load_thread.join()
        return [[],[]]

    stop_threads = True
    load_thread.join()

    # Creating a BeautifulSoup object of the html page for easy extraction of data.

    soup = BeautifulSoup(webpage, 'html.parser')
    html = soup.prettify('utf-8')
    song_json = {}
    song_json['Lyrics'] = []

    # Extract Title of the song
    for title in soup.findAll('title'):
        song_json['Title'] = title.text.strip()
    title = song_json['Title'][0:-23]

    # Extract the Lyrics of the song
    for div in soup.findAll('div', attrs = {'class': 'lyrics'}):
        song_json['Lyrics'].append(div.text.strip().split("\n"))

    extracting = False
    get_into_int = 2
    lyrics = []

    try:
        for line in song_json['Lyrics'][0]:
            if get_into_int == 0:
                if len(line) == 0:
                    continue
                elif extracting:
                    lyrics.append(line)
                    if len(lyrics) == 4:
                        break
                elif line == "[Chorus]" or line == "[Refräng]":
                    extracting = True
            else:
                get_into_int -= 1
    except:
        return [[],[]]


    return [title, lyrics]

def print_game(title, lyrics):
    os.system('clear')
    print("Title: " + title + '\n')

    print("--------------- TEAM ONE ---------------" + '\n')
    print(lyrics[0])
    print(lyrics[1] + '\n')

    print("--------------- TEAM TWO ---------------" + '\n')
    print(lyrics[2])
    print(lyrics[3])

    return input('\n' + '\n' + '\n' + '\n' + '\n' + '\n' + "Press Enter to get a new song..." + '\n')

def save_song(artist, song_title, url, txt):
    with open(txt, 'r') as input_file:
        data = json.load(input_file)
        data['songs'].append({
            'artist': artist,
            'song_title': song_title,
            'url': url
        })

    with open(txt, 'w') as output_file:
        json.dump(data, output_file)

def sort_song(score):
    if score == "":
        print("GOOD SONG")
        save_song(artist, song_title, url, 'good.txt')
    else:
        print("BAD SONG")
        save_song(artist, song_title, url, 'bad.txt')

def get_spotify_songs(user, playlist):
    cid = 'cbbc72a9f47e489696dc8483391f79e7'
    secret = '1d1ce20d02244ceba9ce3247cb4311a1'

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    user_id = user.split(':')
    playlist_id = playlist.split(':')
    playlist = sp.user_playlist(user_id[2], playlist_id[2])

    data = {}
    data['songs'] = []

    for song_index in range(len(playlist['tracks']['items'])):
        artist = playlist['tracks']['items'][song_index]['track']['artists'][0]['name']
        title = playlist['tracks']['items'][song_index]['track']['name']

        url_artist = ''
        url_title = ''

        for char in artist:
            if char == ' ':
                url_artist += '-'
            elif char == 'å' or char == 'Å' or char == 'ä' or char == 'Ä':
                url_artist += 'a'
            elif char == 'ö' or char == 'Ö':
                url_artist += 'o'
            else:
                url_artist += char

        for char in title:
            if char == ' ':
                url_title += '-'
            elif char == 'å' or char == 'Å' or char == 'ä' or char == 'Ä':
                url_title += 'a'
            elif char == 'ö' or char == 'Ö':
                url_title += 'o'
            else:
                url_title += char

        url = 'https://genius.com/' + url_artist + '-' + url_title + '-lyrics'

        data['songs'].append({
            'artist': artist,
            'song_title': title,
            'url': url
        })

    return data

main()

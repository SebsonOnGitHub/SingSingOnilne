# -*- coding: utf-8 -*-,
import json

data = {}
data['songs'] = []

with open('raw.txt', 'r') as infile:
    for line in infile:
        if len(line) > 5:
            title = ''
            artist = ''
            isTitle = True
            for char in line:
                if char == '*':
                    isTitle = False
                    continue
                if isTitle == False and char == '(':
                    break
                if not char.isalnum() and not char.isspace():
                    continue

                if isTitle:
                    title += char
                else:
                    artist += char

            url_artist = ''
            url_title = ''

            for char in artist:
                if char == ' ':
                    url_artist += '-'
                else:
                    url_artist += char

            for char in title:
                if char == ' ':
                    url_title += '-'
                else:
                    url_title += char

            url = 'https://genius.com/' + url_artist + url_title + '-lyrics'

            data['songs'].append({
                'artist': artist,
                'song_title': title,
                'url': url
            })

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)

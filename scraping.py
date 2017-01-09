# -*- coding: utf8 -*-
from __future__ import unicode_literals
import requests
import os.path
import json
import re
from bs4 import BeautifulSoup

def scraping(url):
    response = requests.get(url)
    html = response.text.encode(response.encoding)
    soup = BeautifulSoup(html, "lxml")
    album = soup.find("title").text.replace(u'|||陰陽座公式庵頁|||', '').replace(u'『', '').replace(u'』', '')
    music_list = soup.find("div", attrs={"class": "music_list"})
    music_list = music_list.find("ul", attrs={"class": "center"})
    titles = music_list.find_all("li")
    album_data = soup.find("div", attrs={"class": "album_data"})
    release = album_data.find("td").text.replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
    
    pattern = r".*album_ryuo.*"
    if re.match(pattern, url):
        res = [{"title": title.text, "album": album, "release": release} for title in titles if title.string == u"吹けよ風、轟けよ雷" or title.string == u"生きもの狂い"]
    else:
        res = [{"title": title.text, "album": album, "release": release} for title in titles if title.string]
    
    return res

if __name__ == '__main__':
    baseurl = "http://www.onmyo-za.net/discography/"
    album_paths = [
        'album_kikoku',
        'album_hyakki',
        'album_kohjin',
        'album_fuin',
        'album_houyoku',
        'album_mugen',
        'album_garyo',
        'album_maou',
        'album_chimi',
        'album_kongou',
        'album_kishibojin',
        'album_ryuo',
        'album_whojinn',
        'album_rising',
        'album_karyobinga'
        ]
    
    if os.path.exists("songs.json"):
        os.remove("songs.json")
    songs = []
    for album_path in album_paths:
        songs.extend(scraping(baseurl + album_path + '.html'))
        
    with open("songs.json", "w") as fh:
        fh.write(json.dumps(songs, sort_keys=True, ensure_ascii=False, indent=2).encode('utf_8'))
        
        
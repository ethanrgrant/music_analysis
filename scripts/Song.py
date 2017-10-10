import librosa
import numpy as np
from collections import Counter
import pandas as pd
import string
import re
import requests
from bs4 import BeautifulSoup


class Song():

    def __init__(self, artist, name, id):
        self.artist = artist
        self.name = name
        self.id = id
        self.lyrics = ''
        self.lyrics_map = {}
        self.time_signature = 0
        self.key = 0
        self.mode = 0
        self.tempo = 0
        self.avg_bar_length = 0
        self.pca_lyrics = {}

    # gets and cleans lyrics from geinus
    def get_lyrics(self):
        try:
            #print(self.artist)
            url = 'https://genius.com/' + '-'.join(self.artist.split()) + '-' +  '-'.join(self.name.split()) + '-lyrics'
            soup = BeautifulSoup(requests.get(url).text, 'lxml')
            self.lyrics = soup.findAll('div', {'class' : 'lyrics'})[0].get_text()
            self.build_lyrics_map()
        except Exception as e:
            #print(e)
            #print('could not get lyrics for song: ' + self.name + ' for artist' + str(self.artist))
            #print(url)
            return False
        return self.lyrics

    def build_lyrics_map(self):
        for word in self.lyrics.split():
            clean_word = re.sub(r'[^\w\w]', '', word).strip().lower()
            if clean_word in self.lyrics_map:
                self.lyrics_map[clean_word] += 1
            else:
                self.lyrics_map[clean_word] = 1
        return True

    def get_unique_words(self):
        return self.lyrics_map.keys()

    def do_analysis(self, analysis_map):
        sects = analysis_map['sections']
        self.avg_bar_length = sum([d['duration']*d['confidence'] for d in analysis_map['bars']])/float(sum([d['confidence'] for d in analysis_map['bars']]))
        self.tempo = self.get_avg_val('tempo', sects)
        self.mode = self.get_avg_val('mode', sects)
        self.time_signature = self.get_avg_val('time_signature', sects)
        self.key = self.get_avg_val('key', sects)

    def get_avg_val(self, map_val, sects):
        total_val =  sum([s[map_val]*s[map_val + '_confidence'] for s in sects])
        total_conf = sum([s[map_val + '_confidence'] for s in sects])
        if total_conf>0:
            return float(total_val)/total_conf
        else:
            return float(total_val)

    def get_features(self):
        return [self.name, self.avg_bar_length, self.tempo, self.mode, self.time_signature, self.key, self.artist]
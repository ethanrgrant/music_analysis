import librosa
import numpy as np
import string
import re
import requests
from bs4 import BeautifulSoup


class Song():

    def __init__(self, artist, name):
        self.artist = artist
        self.name = name
        self.lyrics = ''
        self.lyrics_map = {}

    #gets and cleans lyrics from geinus
    def get_lyrics(self):
        url = 'https://genius.com/' + '-'.join(self.artist.split()) + '-' +  '-'.join(self.name.split()) + '-lyrics'
        print(url)
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        self.lyrics = soup.findAll('div', {'class' : 'lyrics'})[0].get_text()
        self.get_lyrics_map()
        return self.lyrics

    def get_lyrics_map(self):
        for word in self.lyrics.split():
            clean_word = re.sub(r'[^\w\w]', '', word).strip().lower()
            if clean_word in self.lyrics_map:
                self.lyrics_map[clean_word] += 1
            else:
                self.lyrics_map[clean_word] = 1
        return True

    def calc_s(self):
        S = librosa.feature.melspectrogram(self.y, self.sr, n_mels=128)
        log_S = librosa.logamplitude(S, ref_power=np.max)
        return S, log_S

    def get_time(self):
        return librosa.core.get_duration(self.y, self.sr)

    def get_tuning(self):
        return librosa.core.estimate_tuning(self.y, self.sr)

    def print_output(self):
        print(self.tuning)
        print(self.time)
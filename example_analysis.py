import os
import librosa
import matplotlib.pyplot as plt
import numpy as np
import spotipy
import spotipy.util as util

from Artist import Artist
from Song import Song

RANGES = ['short_term', 'medium_term', 'long_term']


def main():
    token = util.prompt_for_user_token('ethanrgrant', scope='user-top-read', client_id='a21b8fd9de5949b6b215ceace7076ce0', client_secret= '1d92cf1cbd9b413bbf261b74d521fb0a', redirect_uri='http://localhost:8888/callback' )
    sp = spotipy.client.Spotify(auth=token)
    artists_map = get_top_artists(sp)
    top_genres = get_important_genres(artists_map)
    output_genre_graph(top_genres)
    #song_path = librosa.util.example_audio_file()
    #song = generate_song(song_path)
    #song.print_output()


def get_top_artists(sp):
    artists_map = {}
    for i, r in enumerate(RANGES):
        artists = sp.current_user_top_artists(time_range=r, limit=50)['items']
        for a in artists:
            if a['name'] in artists_map:
                artists_map[a['name']].expand_popularity(i)
            else:
                artists_map[a['name']] = Artist(a['name'], a['genres'], i)
    #for a in artists_map:
    #    artists_map[a].print_self()
    return artists_map


def get_important_genres(artists_map):
    genres_score_map = {}
    for a in artists_map:
        for genre in artists_map[a].genres:
            if genre in genres_score_map:
                genres_score_map[genre] += sum(artists_map[a].popularity)
            else:
                genres_score_map[genre] = sum(artists_map[a].popularity)
    all_genres = [(k, genres_score_map[k]) for k in sorted(genres_score_map, key=genres_score_map.get, reverse=True)]
    print(all_genres[:10])
    return all_genres
    #for genre, score in s:
    #    print((genre, str(score)))

def output_genre_graph(all_genres, num_genres = 10):
    top_gs = all_genres[:10]
    print(top_gs)
    objects = [i[0] for i in top_gs]
    values = [i[1] for i in top_gs]
    y_pos = np.arange(len(objects))
    print(values)
    plt.bar(y_pos, values, align='center')
    plt.xticks(y_pos, objects)
    plt.title('Top ten Genres and their scores')
    plt.ylabel('score')
    plt.xlabel('genre')
    plt.savefig('genre_bar_chart.png')


def generate_song(path_to_song):
    y, sr = librosa.load(path_to_song)
    s = Song(y, sr)
    return s


if __name__=='__main__':
    main()
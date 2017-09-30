import os
import argparse
import json
import librosa
import matplotlib.pyplot as plt
import numpy as np
import spotipy
import spotipy.util as util

from Artist import Artist
from Song import Song
#const vars
RANGES = ['short_term', 'medium_term', 'long_term']
PATH_TO_CREDS = 'creds.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type=str, nargs='?', default='ethanrgrant')
    parser.add_argument('build_genre_graph', type=bool, nargs='?', default=False)
    args = parser.parse_args()


    client_id, client_secret = get_creds('spotify')
    token = util.prompt_for_user_token(args.username, scope='user-top-read', client_id=client_id, client_secret= client_secret, redirect_uri='http://localhost:8888/callback')
    sp = spotipy.client.Spotify(auth=token)
    artists_map = get_top_artists(sp)
    if args.build_genre_graph:
        top_genres = get_important_genres(artists_map)
        output_genre_graph(top_genres)

    #songs = get_top_songs(sp) not implemented yet



#gets credentials from file
def get_creds(service_name):
    with open(PATH_TO_CREDS, 'r') as infile:
        creds = json.load(infile)[service_name]
    return creds[0], creds[1]


# calls spotipy to get top artists for user and records their popularity
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

# finds the genres taht matter the most and records their relative scores
def get_important_genres(artists_map):
    genres_score_map = {}
    for a in artists_map:
        for genre in artists_map[a].genres:
            if genre in genres_score_map:
                genres_score_map[genre] += sum(artists_map[a].popularity)
            else:
                genres_score_map[genre] = sum(artists_map[a].popularity)
    all_genres = [(k, genres_score_map[k]) for k in sorted(genres_score_map, key=genres_score_map.get, reverse=True)]
    return all_genres
    #for genre, score in s:
    #    print((genre, str(score)))


# builds the genre graph in matplotlib
# TODO: make the graph look better
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

#TODO get top songs and get lyrics
def get_top_songs(sp):
    return 'TODO'

# method to get librosa data from MP3 unclear if will be usable
def generate_song(path_to_song):
    y, sr = librosa.load(path_to_song)
    s = Song(y, sr)
    return s


if __name__=='__main__':
    main()
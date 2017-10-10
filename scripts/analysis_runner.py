# Created by Ethan Grant
import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import spotipy
import spotipy.util as util


from Artist import Artist
from Song import Song

# const vars
RANGES = ['short_term', 'medium_term', 'long_term']
PATH_TO_CREDS = 'creds.json'


def main():
    # parses args
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type=str, nargs='?', default='ethanrgrant')
    parser.add_argument('build_genre_graph', type=bool, nargs='?', default=False)
    args = parser.parse_args()

    # authetication
    try:
        client_id, client_secret = get_creds('spotify')
        token = util.prompt_for_user_token(args.username, scope='user-top-read', client_id=client_id, client_secret= client_secret, redirect_uri='http://localhost:8888/callback')
        sp = spotipy.client.Spotify(auth=token)
    except:
        print('problem with spotify validation check creds.json')
        exit(1)

    # gets top artists/genres
   # artists_map = get_top_artists(sp)
    #if args.build_genre_graph:
    #    top_genres = get_important_genres(artists_map)
    #    output_genre_graph(top_genres)

    # gets top songs
    songs = get_saved_songs(sp)
    set_of_words = get_all_unique_words(songs)
    word_df = build_total_word_table(songs, set_of_words)
    song_data = get_data(word_df, songs)

    #do_k_means(songs)


# does PCA on words and appends other important song data
def get_data(word_df, songs):
    pca = PCA(n_components=10)
    pca.fit(word_df)
    components = pd.DataFrame(pca.transform(word_df))
    #TODO append names to datafarme and add other song data

# gets credentials from file
def get_creds(service_name):
    try:
        with open(PATH_TO_CREDS, 'r') as infile:
            creds = json.load(infile)[service_name]
    except FileNotFoundError:
        print(PATH_TO_CREDS + ' is not a valid path file')
        exit(1)
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


# gets all saved songs and puts them into Song objects
def get_saved_songs(sp):
    results = sp.current_user_saved_tracks()
    all_songs = []
    cur_songs = [r['track'] for r in results['items']]
    unique_words = set()
    while results['next'] and len(all_songs)<20:
        for song in cur_songs:
            s = Song(song['artists'][0]['name'], song['name'], song['id'])
            #s.do_analysis(sp.audio_analysis(song['id']))
            s.get_lyrics()
            all_songs.append(s)
        results = sp.next(results)
        cur_songs = [r['track'] for r in results['items']]
    for song in cur_songs:
        all_songs.append(Song(song['artists'][0]['name'], song['name'],  song['id']))
    return all_songs


def get_all_unique_words(songs):
    unique_words = set()
    for s in songs:
        unique_words.union(s.get_unique_words())
    return unique_words

def do_k_means(songs):
    removed_names_songs = [s[1:] for s in songs]
    model = KMeans(n_clusters=10)
    labels = model.fit_predict(removed_names_songs)
    for label, song in songs:
        print('label ' + label + ' song info: ' + songs)


def build_total_word_table(songs, set_of_words):
    word_df = pd.DataFrame(pd.Series(dict.fromkeys(set_of_words, 0)))
    for song in songs:
        word_df[song.name] = pd.Series(song.lyrics_map)
    word_df = word_df.fillna(0).transpose()
    return word_df



if __name__=='__main__':
    main()
from __future__ import print_function

import os
import shutil
import spotipy
import pickle
import pandas as pd
import numpy as np


from collections import Counter

if not os.path.exists('genres.p'):
    # Login to Spotify and get your OAuth token:
    # https://developer.spotify.com/web-api/search-item/
    AUTH = "BQD4KKg1opql7Vi8_34OjujPQRhut-beyfo4jcKdPZA7BwPd9MtMx7vSFVzd3K9J_v4LElaZ6B8dCRV5pp0caAusHhLbLAxB1cYuNlhA-9tWLpuheMrlEIQE-ey-q8m5Nevkh83NV6c"

    if not os.path.exists('clean_midi'):
        # Download the 'Clean MIDI' dataset from http://colinraffel.com/projects/lmd/
        from six.moves import urllib
        import StringIO
        import gzip
        import tarfile
        FILE_URL = 'http://hog.ee.columbia.edu/craffel/lmd/clean_midi.tar.gz'
        response = urllib.request.urlopen(FILE_URL)
        print("INFO: Downloaded {}".format(FILE_URL))
        compressedFile = StringIO.StringIO()
        compressedFile.write(response.read())
        compressedFile.seek(0)
        decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
        OUTFILE_PATH = 'clean_midi.tar'
        with open(OUTFILE_PATH, 'wb') as outfile:
            outfile.write(decompressedFile.read())
        tar = tarfile.open(OUTFILE_PATH)
        tar.extractall()
        tar.close()
    # Get artists from folder names
    artists = [item for item in os.listdir(
        'clean_midi') if not item.startswith('.')]

    sp = spotipy.Spotify(auth=AUTH)
    genres = {}
    for i, artist in enumerate(artists):
        try:
            results = sp.search(q=artist, type='artist', limit=1)
            items = results['artists']['items']
            genre_list = items[0]['genres'] if len(items) else items['genres']
            genres[artist] = genre_list
            if i < 5:
                print("INFO: Preview {}/5".format(i + 1),
                      artist, genre_list[:5])
        except Exception as e:
            print("INFO: ", artist, "not included: ", e)

    # Save to pickle file
    pickle.dump(genres, open('genres.p', 'wb'), protocol=2)
    print("INFO: genre.p file created")
else:
    # Load genres meta-data
    genres = pickle.load(open('genres.p', 'rb'))
    print("INFO: found genre.p")
# Get the most common genres
flattened_list = [item for sublist in list(
    genres.values()) for item in sublist]

MIDI_DIR = os.path.join(os.getcwd(), 'clean_midi')


def get_artists(genre):
    """Get artists with label `genre`."""
    artists = [artist for artist, gs in genres.items() if genre in gs]
    return artists


# Get artist with genres in `genre_list`
genre_data = {}
genre_list = ['classical', 'metal', 'jazz', 'funk', 'r&b', 'folk',
              'hip hop', 'punk', 'latin', 'big band']
for g in genre_list:
    genre_data[g] = get_artists(g)

# Copy artists to a genre-specific folder
for genre, artists in genre_data.items():
    try:
        for artist in artists:
            shutil.copytree(os.path.join(MIDI_DIR, artist), os.path.join(
                os.getcwd(), 'subsets', genre, artist))
    except Exception as e:
        print(e)
    print("INFO: {} folder created.".format(genre))

from __future__ import print_function

import os
import shutil
import spotipy
import pickle
import pandas as pd
import numpy as np


from collections import Counter

if not os.path.exists("genres.p"):
    # Login to Spotify and get your OAuth token:
    # https://developer.spotify.com/web-api/search-item/
    AUTH = "BQBHlFpkjjlfDwbyQ7v0F1p_cejpmYARG6KDclVlP3HZyb4MG3_Mc40tE__HsuFXGQvYRvOi1Mbfx-_FoA9DVXCpNupL0X8XFFbL1XghQCf6mH_yXc82GqWAtrLjUtc-eWIDBpci1M0"

    if not os.path.exists('clean_midi'):
        # Download the 'Clean MIDI' dataset from http://colinraffel.com/projects/lmd/
        from six.moves import urllib
        import StringIO
        import gzip
        import tarfile
        FILE_URL = 'http://hog.ee.columbia.edu/craffel/lmd/clean_midi.tar.gz'
        response = urllib.request.urlopen(FILE_URL)
        compressed_file = StringIO.StringIO()
        compressedFile.write(response.read())
        compressedFile.seek(0)
        decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
        OUTFILE_PATH = 'clean_midi.tar'
        with open(OUTFILE_PATH, 'wb') as outfile:
            outfile.write(decompressed_file.read())
        tar = tarfile.open('clean_midi')
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
                print(artist, genre_list[:5])
        except Exception as e:
            print(artist, e)

    # Save to pickle file
    pickle.dump(genres, open("genres.p", "wb"), protocol=2)
    print("INFO: genre.p file created")
else:
    # Load genres meta-data
    genres = pickle.load(open("genres.p", "rb"))

# Get the most common genres
flattened_list = [item for sublist in list(
    genres.values()) for item in sublist]

MIDI_DIR = os.path.join(os.getcwd(), 'clean_midi')


def get_artists(genre):
    """Get artists with label `genre`."""
    artists = [artist for artist, gs in genres.items() if genre in gs]
    return artists


# Get artist with genres 'soft rock' and 'disco'
genre_data = {}
metal = get_artists('metal')
classical = get_artists('classical')

genre_data['metal'] = metal
genre_data['classical'] = classical

# Copy artists to a genre-specific folder
for genre, artists in genre_data.items():
    try:
        for artist in artists:
            shutil.copytree(os.path.join(MIDI_DIR, artist), os.path.join(
                os.getcwd(), 'subsets', genre, artist))
    except Exception as e:
        print(e)

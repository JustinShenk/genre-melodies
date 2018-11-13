#!/usr/bin/env python
from __future__ import print_function

import os
import shutil
import spotipy
import pickle
import pandas as pd
import numpy as np

from collections import Counter

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
    os.remove(OUTFILE_PATH)
    print("INFO: Extracted data")
else:
    print("INFO: Found `clean_midi` directory")

if not os.path.exists('genres.p'):
    # Login to Spotify and get your OAuth token:
    # https://developer.spotify.com/web-api/search-item/
    AUTH = "ENTER-MY-AUTH-KEY"

    # Get artists from folder names
    artists = [
        item for item in os.listdir('clean_midi') if not item.startswith('.')
    ]

    sp = spotipy.Spotify(auth=AUTH)
    genres = {}
    for i, artist in enumerate(artists):
        try:
            results = sp.search(q=artist, type='artist', limit=1)
            items = results['artists']['items']
            genre_list = items[0]['genres'] if len(items) else items['genres']
            genres[artist] = genre_list
            if i < 5:
                print("INFO: Preview {}/5".format(i + 1), artist,
                      genre_list[:5])
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
flattened_list = [
    item for sublist in list(genres.values()) for item in sublist
]

MIDI_DIR = os.path.join(os.getcwd(), 'clean_midi')


def get_artists(genre):
    """Get artists with label `genre`."""
    artists = [artist for artist, gs in genres.items() if genre in gs]
    return artists


# Get artists with genres in `genre_list`
genre_data = {}
genre_list = [
    'classical', 'metal', 'jazz', 'funk', 'r&b', 'folk', 'hip hop', 'punk',
    'latin', 'big band'
]
for g in genre_list:
    genre_data[g] = get_artists(g)

# Copy artists to a genre-specific folder
for genre, artists in genre_data.items():
    try:
        for artist in artists:
            _genre = genre.replace(' ', '_').replace('&', 'n')
            shutil.copytree(
                os.path.join(MIDI_DIR, artist),
                os.path.join(os.getcwd(), 'subsets', _genre, artist))
    except Exception as e:
        print(e)
    print("INFO: {} folder created.".format(genre))

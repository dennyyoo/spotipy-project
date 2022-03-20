import spotipy
import spotipy.util as util
import csv
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
cid = os.getenv('CLIENT_ID')
secret = os.getenv('CLIENT_SECRET')


token = util.prompt_for_user_token(
        username='y00nited',
        scope='user-follow-modify playlist-modify-private playlist-read-private user-library-modify playlist-read-private playlist-modify-public playlist-read-collaborative',
        client_id=cid,
        client_secret=secret,
        redirect_uri='http://localhost/')

sp = spotipy.Spotify(auth=token)


def call_playlist(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    results = tracks

    for i in range(len(results)):
        print(i)  # Counter
        if i == 0:
            playlist_tracks_id = results[i]['track']['id']
            playlist_tracks_titles = results[i]['track']['name']
            playlist_tracks_first_release_date = results[i]['track']['album']['release_date']
            playlist_tracks_popularity = results[i]['track']['popularity']

            artist_list = []
            for artist in results[i]['track']['artists']:
                artist_list = artist['name']
            playlist_tracks_artists = artist_list

            features = sp.audio_features(playlist_tracks_id)
            features_df = pd.DataFrame(data=features, columns=features[0].keys())
            features_df['title'] = playlist_tracks_titles
            features_df['all_artists'] = playlist_tracks_artists
            features_df['popularity'] = playlist_tracks_popularity
            features_df['release_date'] = playlist_tracks_first_release_date
            features_df = features_df[['id', 'title', 'all_artists', 'popularity', 'release_date',
                                       'danceability', 'energy', 'key', 'loudness',
                                       'mode', 'acousticness', 'instrumentalness',
                                       'liveness', 'valence', 'tempo',
                                       'duration_ms', 'time_signature']]
            continue
        else:
            try:
                playlist_tracks_id = results[i]['track']['id']
                playlist_tracks_titles = results[i]['track']['name']
                playlist_tracks_first_release_date = results[i]['track']['album']['release_date']
                playlist_tracks_popularity = results[i]['track']['popularity']
                artist_list = []
                for artist in results[i]['track']['artists']:
                    artist_list = artist['name']
                playlist_tracks_artists = artist_list
                features = sp.audio_features(playlist_tracks_id)
                new_row = {'id': [playlist_tracks_id],
                           'title': [playlist_tracks_titles],
                           'all_artists': [playlist_tracks_artists],
                           'popularity': [playlist_tracks_popularity],
                           'release_date': [playlist_tracks_first_release_date],
                           'danceability': [features[0]['danceability']],
                           'energy': [features[0]['energy']],
                           'key': [features[0]['key']],
                           'loudness': [features[0]['loudness']],
                           'mode': [features[0]['mode']],
                           'acousticness': [features[0]['acousticness']],
                           'instrumentalness': [features[0]['instrumentalness']],
                           'liveness': [features[0]['liveness']],
                           'valence': [features[0]['valence']],
                           'tempo': [features[0]['tempo']],
                           'duration_ms': [features[0]['duration_ms']],
                           'time_signature': [features[0]['time_signature']]
                           }

                dfs = [features_df, pd.DataFrame(new_row)]
                features_df = pd.concat(dfs, ignore_index=True)
            except:
                continue

    return features_df

def create_playlist(property, username):
    type = property.lower()
    highName = "High " + type
    midName = "Mid " + type
    lowName = "Low " + type
    pList1 = sp.user_playlist_create(username, name=highName)
    pList2 = sp.user_playlist_create(username, name=midName)
    pList3 = sp.user_playlist_create(username, name=lowName)
    print(pList1)
    data = [type, pList1['uri'], pList2['uri'], pList3['uri']]
    return data

def getTracks(type):
    file = open('dataframe.csv')
    csvreader = csv.reader(file)
    header = next(csvreader)
    print(header)
    dict = {}
    for row in csvreader:
        if type == "popularity":
            dict[row[0]] = row[3]
        elif type == "danceability":
            dict[row[0]] = row[5]
        elif type == "energy":
            dict[row[0]] = row[6]
        elif type == "loudness":
            dict[row[0]] = row[8]
        elif type == "acousticness":
            dict[row[0]] = row[10]
        elif type == "instrumentalness":
            dict[row[0]] = row[11]
        elif type == "liveness":
            dict[row[0]] = row[12]
        elif type == "valence":
            dict[row[0]] = row[13]
        elif type == "tempo":
            dict[row[0]] = row[14]
    print(dict)
    file.close()
    return dict

def sortTracks(typeDict, username, playlistIDs):
    sortedDict = dict(sorted(typeDict.items(), key=lambda item: item[1]))
    uris = list(sortedDict.keys())
    pListID1 = playlistIDs[1]
    pListID2 = playlistIDs[2]
    pListID3 = playlistIDs[3]
    oneThird = len(uris) // 3
    twoThird = oneThird*2
    print(uris)
    for i in range (len(uris)):
        if i <= oneThird:
            if oneThird > 100:
                length = oneThird
                count = 0
                while length > 100:
                    length = length //2
                    count +=1
                for i in range(count):
                    if i == 0:
                        smallURI = uris[:length]
                        print(length)
                        print("i is 0")
                        sp.user_playlist_add_tracks(user=username, playlist_id=pListID1, tracks=smallURI)
                    else:
                        length = length*i
                        smallURI = uris[length:length+100]
                        sp.user_playlist_add_tracks(user=username, playlist_id=pListID1, tracks=smallURI)
        if i > oneThird:
            if i <= twoThird:
                if oneThird > 100:
                    length = oneThird
                    count = 0
                    while length > 100:
                        length = length // 2
                        count += 1
                    minLength = length
                    for i in range(count):
                        if i == 0:
                            smallURI = uris[:length]
                            print(smallURI)
                            print("i is 0")
                            sp.user_playlist_add_tracks(user=username, playlist_id=pListID1, tracks=smallURI)
                        else:
                            oldLength = length
                            length = (minLength * i) + minLength
                            smallURI = uris[oldLength: length]
                            print("i is " + str(i))
                            print(smallURI)
                            print(oldLength)
                            print(savedLength)
                            print(length)
                            sp.user_playlist_add_tracks(user=username, playlist_id=pListID1, tracks=smallURI)
            if i > twoThird:
                if (len(uris) - twoThird) > 100:
                    length = (len(uris) - twoThird)
                    count = 0
                    while length > 100:
                        length = length // 2
                        count += 1
                    minLength = length
                    for i in range(count):
                        if i == 0:
                            smallURI = uris[:length]
                            print(smallURI)
                            print("i is 0")
                            sp.user_playlist_add_tracks(user=username, playlist_id=pListID1, tracks=smallURI)
                        else:
                            oldLength = length
                            length = (minLength * i) + minLength
                            smallURI = uris[oldLength: length]
                            print("i is " + str(i))
                            print(smallURI)
                            print(oldLength)
                            print(savedLength)
                            print(length)
                            sp.user_playlist_add_tracks(user=username, playlist_id=pListID1, tracks=smallURI)
    return

username = input("Username: ")
playlistURI = input("Playlist URI: ")
playlistType = input("Playlist Type: ")
playlist_df = call_playlist(username, playlistURI)
playlist_df.head()
playlist_df.to_csv("dataframe.csv", index = False)
type = create_playlist(playlistType, username)
tracks = getTracks(type[0])
sortTracks(tracks, username, type)



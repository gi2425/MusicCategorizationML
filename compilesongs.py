import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
import mysql.connector
from googleapiclient.discovery import build
from sqlalchemy import create_engine
import pandas as pd

#spotify access info here


#database access info here

#sql alchemy stuff
engine = create_engine(f'mysql+mysqlconnector://root:Gigi13579!@127.0.0.1:3306/test')


#holds identifier, table name, and playlist id which change for each input
identifier = 401
table_name = "club"
playlist_id = "2l3XKRkKBTLWZ4ITPpwB7D"

#get playlist name
playlist = sp.playlist(playlist_id)
playlist_name = playlist.get('name')


def get_playlist_song_ids(playlist_id):
    results = sp.playlist_tracks(playlist_id, additional_types="track")
    id_list = []

    while results:
        # Extract the track items from the current page
        items = results.get("items", [])
        
        # Loop through the track items
        for t in items:
            track = t.get('track')
            if track and track.get('type') == 'track':  # Check that it is a track
                track_id = track.get('id')
                if track_id:
                    id_list.append(track_id)
        
        # Check if there is a next page of results
        next_page = results.get('next')
        if next_page:
            results = sp.next(results)
        else:
            # No more pages, break the loop
            break

    return id_list


def get_song_info(song_id):
    results = sp.track(song_id)

    l = []
    l.append(results.get('name'))
    artistlist = []
    for artists in results.get('artists'):
        artistlist.append(artists.get('name'))
    l.append(artistlist)
    l.append(results.get('album').get('name'))
    l.append(results.get('album').get('release_date'))
    l.append(results.get('album').get('total_tracks'))
    l.append(results.get('duration_ms'))
    l.append(results.get('explicit'))
    l.append(results.get('id'))
    l.append(results.get('track_number'))
    return l


def get_audio_features(song_id):
    results = sp.audio_features(song_id)
    l = []
    exclude = ['type', 'uri', 'track_href', 'analysis_url', 'duration_ms']
    for i in results:
        current_values = []
        for key, value in i.items():
            if key not in exclude:
                current_values.append(value)
    
    # Append the filtered values to the main list
    for i in current_values:
        l.append(i)
    return l


def get_youtube_info(song_info, max_results=1):
    # Perform the search request
    l = []
    request = youtube.search().list(
        part="snippet",
        maxResults=max_results,
        q=f"{song_info[0]} {song_info[1]} official audio",
        type="video"  # Only search for videos
    )
    response = request.execute()

    # Extract video links
    try:
        for item in response['items']:
            if item['id']['kind'] == "youtube#video":
                video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        l.append(song_info[7])
        l.append(video_url)
    except:
        l.append("NULL")
    return l


def create_tables():
    createtable1 = '''
    CREATE TABLE test1(
    name VARCHAR(255),
    artists VARCHAR(255),
    album_name VARCHAR(255),
    album_release_date VARCHAR(255),
    album_tracks INT,
    song_duration INT,
    explicit INT,
    id VARCHAR(255) PRIMARY KEY,
    album_track_number INT)
'''

    createtable2 = '''
    CREATE TABLE test2(
    danceability VARCHAR(255),
    energy VARCHAR(255),
    song_key INT,
    loudness VARCHAR(255),
    song_mode INT,
    speechiness VARCHAR(255),
    acousticness VARCHAR(255),
    instrumentalness VARCHAR(255),
    liveness VARCHAR(255),
    valence VARCHAR(255),
    tempo VARCHAR(255),
    id VARCHAR(255) PRIMARY KEY,
    time_signature INT)
'''

    createtable3 = '''
    CREATE TABLE test3(
    id VARCHAR(255) PRIMARY KEY,
    link VARCHAR(255))
'''

    createtable4 = '''
    CREATE TABLE test4(
    id VARCHAR(255) PRIMARY KEY,
    identifier INT,
    playlist_id VARCHAR(255),
    playlist_name VARCHAR(255),
    date_added varchar(255))
'''

    cursor.execute(createtable1)
    cursor.execute(createtable2)
    cursor.execute(createtable3)
    cursor.execute(createtable4)

    db_connection.commit()
    print("tables created")

def drop_tables():
    drop1 = '''
    drop table test1
'''
    drop2 = '''
    drop table test2
'''
    drop3 = '''
    drop table test3
'''
    drop4 = '''
    drop table test4
'''

    cursor.execute(drop1)
    cursor.execute(drop2)
    cursor.execute(drop3)
    cursor.execute(drop4)

    db_connection.commit()
    print("tables dropped")


def insert_song_info(song_info):
    insertquery = '''
    INSERT INTO test1 (name, artists, album_name, album_release_date, 
    album_tracks, song_duration, explicit, id, album_track_number)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

    # Loop through each list of data
    formatted_data = (
    song_info[0],  # name
    ', '.join(song_info[1]),  # artists (list to comma-separated string)
    song_info[2],  # album_name
    song_info[3],  # album_release_date
    song_info[4],  # album_tracks
    song_info[5],  # song_duration
    song_info[6],  # explicit
    song_info[7],  # song_id
    song_info[8]   # album_track_number
    )

    # Execute the insert statement for the current song
    cursor.execute(insertquery, formatted_data)

    # Commit the transaction
    db_connection.commit()
    print(f"Inserted Song Info")

def insert_audio_features(get_audio_features):
    insertquery = '''
    INSERT INTO test2 (danceability, energy, song_key, loudness, 
    song_mode, speechiness, acousticness, instrumentalness, liveness, 
    valence, tempo, id, time_signature)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

    # Loop through each list of data
    formatted_data = (
    get_audio_features[0],  #danceability
    get_audio_features[1],  #energy
    get_audio_features[2],  #song_key
    get_audio_features[3],  #loudness
    get_audio_features[4],  #song_mode
    get_audio_features[5],  #speechiness
    get_audio_features[6],  #acousticness
    get_audio_features[7],  #instrumentalness
    get_audio_features[8],  #liveness
    get_audio_features[9],  #valence
    get_audio_features[10],  #tempo
    get_audio_features[11],  #id
    get_audio_features[12]   #time_signature
    )

    # Execute the insert statement for the current song
    cursor.execute(insertquery, formatted_data)

    # Commit the transaction
    db_connection.commit()
    print("Inserted Audio Features")

def insert_youtube_info(get_youtube_info):
    insertquery = '''
    INSERT INTO test3 (id, link)
    VALUES (%s, %s)
'''

    # Loop through each list of data
    formatted_data = (
    get_youtube_info[0],  #id
    get_youtube_info[1]  #link
    )

    # Execute the insert statement for the current song
    cursor.execute(insertquery, formatted_data)

    # Commit the transaction
    db_connection.commit()
    print(f"Inserted YouTube Info")

def insert_identifiers(song_info):
    insertquery = '''
    INSERT INTO test4 (id, identifier, playlist_id, playlist_name, date_added)
    VALUES (%s, %s, %s, %s, NOW())
'''

    formatteddata = (
        song_info[7], #id
        identifier,
        playlist_id,
        playlist_name
    )

    cursor.execute(insertquery, formatteddata)
    db_connection.commit()
    print(f"Inserted identifiers")
    print(f"Inserted everything for {song_info[0]}")
    

def combine_everything():
    while cursor.nextset():
        pass
    combinequeryexisting = f'''
    INSERT INTO {table_name} (
    id, playlist_id, identifier, name, artists, playlist_name, album_name,
    album_release_date, album_tracks, song_duration, explicit, album_track_number,
    danceability, energy, song_key, loudness, song_mode, speechiness, acousticness,
    instrumentalness, liveness, valence, tempo, time_signature, link, date_added)
    SELECT 
    t1.id,
    t4.playlist_id,
    t4.identifier,
    t1.name,
    t1.artists,
    t4.playlist_name,
    t1.album_name,
    t1.album_release_date,
    t1.album_tracks,
    t1.song_duration,
    t1.explicit,
    t1.album_track_number,
    t2.danceability,
    t2.energy,
    t2.song_key,
    t2.loudness,
    t2.song_mode,
    t2.speechiness,
    t2.acousticness,
    t2.instrumentalness,
    t2.liveness,
    t2.valence,
    t2.tempo,
    t2.time_signature,
    t3.link,
    t4.date_added
    FROM test1 t1
    JOIN test2 t2 ON t1.id = t2.id
    JOIN test3 t3 ON t1.id = t3.id
    JOIN test4 t4 ON t1.id = t4.id;
    '''


    combinequerycreate = f'''
    CREATE TABLE {table_name} AS
    SELECT 
    t1.id,
    t4.playlist_id,
    t4.identifier,
    t1.name,
    t1.artists,
    t4.playlist_name,
    t1.album_name,
    t1.album_release_date,
    t1.album_tracks,
    t1.song_duration,
    t1.explicit,
    t1.album_track_number,
    t2.danceability,
    t2.energy,
    t2.song_key,
    t2.loudness,
    t2.song_mode,
    t2.speechiness,
    t2.acousticness,
    t2.instrumentalness,
    t2.liveness,
    t2.valence,
    t2.tempo,
    t2.time_signature,
    t3.link,
    t4.date_added
    FROM test1 t1
    JOIN test2 t2 ON t1.id = t2.id
    JOIN test3 t3 ON t1.id = t3.id
    JOIN test4 t4 ON t1.id = t4.id;
    '''

    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    if not result:
        cursor.execute(combinequerycreate)
    else:
        cursor.execute(combinequeryexisting)


    # Commit the transaction
    db_connection.commit()

    print("everything combined")


def count():
    count = f'''
    SELECT COUNT(*) AS count
    FROM {table_name}
    WHERE playlist_id = '{playlist_id}';
    '''
    cursor.execute(count)
    result = cursor.fetchone()
    return result[0]

def clean():
    df = pd.read_sql(f'SELECT * FROM {table_name}', engine)
    df_cleaned = df.drop_duplicates(subset=['name', 'artists'], keep='first')
    df_cleaned.to_sql(f'{table_name}', engine, if_exists='replace', index=False)

    print("cleaned")


create_tables()
for song_id in get_playlist_song_ids(playlist_id):
    song_info = get_song_info(song_id)
    song_name = song_info[0]
    song_artists = song_info[1]

    # If song_artists is a list, join it into a string
    if isinstance(song_artists, list):
        song_artists = ', '.join(song_artists)

    check_existence_query = f'''
        SELECT * 
        FROM {table_name} 
        WHERE name = %s AND artists = %s
    '''
    try:
        cursor.execute(check_existence_query, (song_name, song_artists))
    except: 
        pass

    song_exists = cursor.fetchone()

    while cursor.nextset():
        pass

    if not song_exists:  # If no matching song is found, proceed with inserts
        try:
            insert_song_info(song_info)
            insert_audio_features(get_audio_features(song_id))
            insert_youtube_info(get_youtube_info(song_info))
            insert_identifiers(song_info)
        except:
            print("new key pls")
            break
    else:
        print(f"Song '{song_name}' by {song_artists} already exists, skipping...")

combine_everything()
clean()
print(f"{count()} songs added")
drop_tables()

cursor.close()
db_connection.close()



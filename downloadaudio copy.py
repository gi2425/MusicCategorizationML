import mysql.connector
import os
import yt_dlp

# Connect to MySQL database
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Gigi13579!",
    database="test",
    port="3306"
)

table_name = 'rock'

cursor = db.cursor()
cursor.execute(f"SELECT link FROM {table_name}")
youtube_links = cursor.fetchall()

# Specify the path where audio files will be saved
save_path = os.path.join('research', 'media', f'{table_name}')


# Iterate over the fetched links and download the audio
for link in youtube_links:
    try:
        url = link[0]  # The YouTube link from the database
        print(f"Downloading audio from {url}")

        # Set options for yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Failed to download audio from {url}. Error: {e}")

cursor.close()
db.close()

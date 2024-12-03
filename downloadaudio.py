import mysql.connector
import os
import yt_dlp

#database access info here

table_name = 'club'
save_path = os.path.join('media', f'{table_name}')
os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists

cursor = db.cursor()
cursor.execute(f"SELECT link FROM {table_name}")
youtube_links = cursor.fetchall()

# Iterate over the fetched links and download the audio if not already downloaded
for link in youtube_links:
    try:
        url = link[0]  # The YouTube link from the database
        print(f"Processing {url}")

        # Extract video info to get the title for the file name
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)
        
        if title:
            file_name = f"{title}.mp3"
            file_path = os.path.join(save_path, file_name)

            # Check if the file already exists
            if os.path.exists(file_path):
                print(f"File already exists for {url}, skipping download.")
                continue  # Skip to the next link

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

import os
import yt_dlp
import mysql.connector

#database access info here

table_name = 'club'

cursor = db.cursor()

try: 
    cursor.execute(f'SELECT filepath FROM {table_name}')
    cursor.nextset()
except:
    cursor.execute(f'ALTER TABLE {table_name} ADD COLUMN filepath VARCHAR(255);')
    db.commit()  # Ensure parentheses for commit

cursor.execute(f"SELECT link FROM {table_name}")
youtube_links = cursor.fetchall()
cursor.nextset()

# Specify the path where audio files will be saved
save_path = os.path.join('media', f'{table_name}')

# Fetch all YouTube links from the database
cursor.execute(f"SELECT link FROM {table_name}")
youtube_links = cursor.fetchall()

# Iterate over the fetched links and process each one
for link in youtube_links:
    try:
        url = link[0]  # The YouTube link from the database
        print(f"Processing {url} to get file path")

        # Extract video info (title) without downloading
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)
        
        if title:
            # Create the expected file path
            file_name = f"{title}.mp3"
            full_file_path = os.path.join(save_path, file_name)

            # Update the database with the file path
            cursor.execute(f"UPDATE {table_name} SET filepath = %s WHERE link = %s", (full_file_path, url))
            db.commit()

            print(f"File path for {url}: {full_file_path}")

    except Exception as e:
        print(f"Failed to process {url}. Error: {e}")

# Close the cursor and database connection
cursor.close()
db.close()

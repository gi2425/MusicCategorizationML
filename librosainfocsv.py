import csv
import mysql.connector
import librosa
import os

# Path to save the result file
csvpath = "/Users/gi/Desktop/research/media.csv"
table_name = "club"  # This is the category name
classnumber = "401" 

#database access info here

# Function to retrieve song data from the database
def get_song_data(cursor):
    query = f"SELECT name, filepath FROM {table_name}"
    cursor.execute(query)
    return cursor.fetchall()

# Function to compute audio features using librosa
def compute_audio_features(file_path):
    print(f"hi: {file_path}")
    try:
        y, sr = librosa.load(file_path)
        
        # Zero Crossing Rate (variance)
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_var = zcr.var()
        
        # Spectral Centroid (mean and variance)
        spcent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spcent_mean = spcent.mean()
        spcent_var = spcent.var()
        
        # Spectral Rolloff (mean and variance)
        sproll = librosa.feature.spectral_rolloff(y=y, sr=sr)
        sproll_mean = sproll.mean()
        sproll_var = sproll.var()
        
        # Root Mean Square (mean)
        rms = librosa.feature.rms(y=y)
        rms_mean = rms.mean()

        return [zcr_var, spcent_mean, spcent_var, sproll_mean, sproll_var, rms_mean]

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None
    


# Function to create or append to the CSV file with all the necessary data
def create_or_append_to_csv(song_data):
    # Check if the file already exists
    file_exists = os.path.exists(csvpath)
    
    # Open CSV in append mode
    with open(csvpath, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=' ')

        # If the file is empty, write the header
        if not file_exists:
            writer.writerow([
                'Song Name', 'Zero Crossing Rate Variance', 'Spectral Centroid Mean', 'Spectral Centroid Variance',
                'Spectral Rolloff Mean', 'Spectral Rolloff Variance', 'Root Mean Square Mean', 'File Path', 'Category', 'Table Number'
            ])
        
        # Write each song's data
        for data in song_data:
            if data:
                writer.writerow(data)
    print(f"Data added to CSV file at {csvpath}")

def main():
    # Connect to the database
    db = connect_to_db()
    cursor = db.cursor()
    
    # Get all songs and file paths from the database
    songs = get_song_data(cursor)


    # List to hold all rows for the CSV
    song_data = []

    # Define the base directory for file search
    base_dir = "/Users/gi/Desktop/research"

    # Process each song's data
    for song in songs:
        name, db_file_path = song
        # Skip if the file path is None
        if db_file_path is None:
            print(f"Skipping {name} due to missing file path.")
            continue

        # Construct the full file path for searching the file on the machine
        full_file_path = os.path.join(base_dir, db_file_path)
        
        # Check if the file exists on the system
        if db_file_path and os.path.exists(full_file_path):
            features = compute_audio_features(full_file_path)
            if features:
                # Write the path in the format stored in the database (e.g., "research/media/rnb/...")
                row = [name] + features + [db_file_path] + [table_name] + [classnumber]
                song_data.append(row)
        else:
            print(f"File does not exist: {full_file_path}")
    
    # Create or append to CSV with the gathered song data
    create_or_append_to_csv(song_data)

    # Close the database connection
    db.close()


main()

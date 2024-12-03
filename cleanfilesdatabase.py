import os
import re
import mysql.connector

# Path to the base directory for files
base_dir = "/Users/gi/Desktop/research"
table_name = "club"  # This is the category name (table name)

#database access info here

# Function to sanitize file names by removing special characters
def sanitize_file_name(file_name):
    # Replace all non-alphanumeric characters (except for underscores and periods) with underscores
    return re.sub(r'[^a-zA-Z0-9._]', '_', file_name)

# Function to update the database with sanitized file paths
def sanitize_file_paths_in_db():
    # Connect to the database
    db = connect_to_db()
    cursor = db.cursor()

    # Query to get all file paths from the database
    query = f"SELECT id, filepath FROM {table_name}"
    cursor.execute(query)
    records = cursor.fetchall()

    # Iterate through each record from the database
    for record in records:
        record_id, original_file_path = record

        if not original_file_path:
            print(f"Skipping entry with ID {record_id} due to missing file path.")
            continue

        # Ensure that the path contains 'media/{table_name}/'
        if f'media/{table_name}/' in original_file_path:
            base_part, file_part = original_file_path.split(f'media/{table_name}/', 1)
            # Sanitize the part after 'media/{table_name}/'
            sanitized_file_part = sanitize_file_name(file_part)
            sanitized_file_path = os.path.join(base_part, f'media/{table_name}/', sanitized_file_part)
        else:
            sanitized_file_path = original_file_path  # If 'media/{table_name}/' is not found

        # Debug: Print the original file path and the sanitized file path
        print(f"Original file path: {original_file_path}")
        print(f"Sanitized file path: {sanitized_file_path}")

        # Update the database with the sanitized file path
        try:
            update_query = f"UPDATE {table_name} SET filepath = %s WHERE id = %s"
            cursor.execute(update_query, (sanitized_file_path, record_id))
            db.commit()
            print(f"Updated database for ID {record_id}: {original_file_path} -> {sanitized_file_path}")
        except Exception as e:
            print(f"Error updating database for ID {record_id}: {e}")

    # Close the database connection
    db.close()

def main():
    # Sanitize the file paths in the database
    sanitize_file_paths_in_db()

if __name__ == "__main__":
    main()

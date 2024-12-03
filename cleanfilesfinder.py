import os
import re

# Path to the directory for cleaning

table_name = "club"
target_dir = f"/Users/gi/Desktop/research/media/{table_name}"

# Function to sanitize file names by replacing special characters
def sanitize_file_name(file_name):
    return re.sub(r'[^a-zA-Z0-9_.]', '_', file_name)

# Function to clean all files in the directory
def clean_all_files_in_directory(directory):
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return
    
    for root, _, files in os.walk(directory):
        for file in files:
            # Original full file path
            original_file_path = os.path.join(root, file)
            
            # Sanitize the file name
            sanitized_file_name = sanitize_file_name(file)
            
            # Skip if the file name is already sanitized
            if file == sanitized_file_name:
                print(f"File already sanitized: {original_file_path}")
                continue
            
            # New full file path with sanitized name
            sanitized_file_path = os.path.join(root, sanitized_file_name)
            
            try:
                # Rename the file on disk
                os.rename(original_file_path, sanitized_file_path)
                print(f"Renamed: {original_file_path} -> {sanitized_file_path}")
            except Exception as e:
                print(f"Error renaming {original_file_path} to {sanitized_file_path}: {e}")

# Run the cleaning function
clean_all_files_in_directory(target_dir)

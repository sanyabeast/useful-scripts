import os
import sys

def prepend_prefix_to_files(folder_path, prefix):
    try:
        # Check if the provided path is a directory
        if not os.path.isdir(folder_path):
            print(f"The provided path '{folder_path}' is not a valid directory.")
            return
        
        # Get a list of all files in the directory
        files = os.listdir(folder_path)
        
        for file_name in files:
            # Create the new file name with the prefix
            new_file_name = prefix + file_name
            
            # Get the full paths for the old and new file names
            old_file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{file_name}' to '{new_file_name}'")
        
        print("All files have been successfully renamed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <folder_path> <prefix>")
    else:
        folder_path = sys.argv[1]
        prefix = sys.argv[2]
        prepend_prefix_to_files(folder_path, prefix)
import os
import shutil
import argparse
import yaml

def load_config(file_path):
    """Loads the YAML configuration file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def move_shortcuts_to_temp(input_menus, temp_folder):
    """Move all shortcuts from input menus to the temporary folder."""
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    for menu in input_menus:
        for root, _, files in os.walk(menu):
            for file in files:
                if file.endswith(".lnk"):  # Only move shortcut files
                    source = os.path.join(root, file)
                    destination = os.path.join(temp_folder, file)
                    shutil.move(source, destination)
                    print(f"Moved: {source} -> {destination}")

def remove_empty_folders(input_menus):
    """Remove empty folders from the input menus."""
    for menu in input_menus:
        for root, dirs, _ in os.walk(menu, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                    print(f"Removed empty folder: {dir_path}")
                except OSError:
                    pass  # Directory not empty

def cleanup_temp_folder(temp_folder):
    """Remove the temp folder after organizing."""
    try:
        shutil.rmtree(temp_folder)
        print(f"Removed temp folder: {temp_folder}")
    except OSError as e:
        print(f"Error removing temp folder: {e}")

def create_folders_and_organize(temp_folder, output_menu, folders, misc_folder):
    """Create folders in the output menu and move shortcuts from temp folder."""
    # Create folders listed in the config
    for folder_name, shortcuts in folders.items():
        folder_path = os.path.join(output_menu, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for shortcut_name in shortcuts:
            shortcut_file = shortcut_name + ".lnk"
            shortcut_path = os.path.join(temp_folder, shortcut_file)
            if os.path.exists(shortcut_path):
                shutil.move(shortcut_path, folder_path)
                print(f"Organized: {shortcut_file} -> {folder_path}")

    # Create the misc folder for unlisted shortcuts
    misc_folder_path = os.path.join(output_menu, misc_folder)
    if not os.path.exists(misc_folder_path):
        os.makedirs(misc_folder_path)

    # Move remaining shortcuts to the misc folder
    for file in os.listdir(temp_folder):
        if file.endswith(".lnk"):
            shutil.move(os.path.join(temp_folder, file), misc_folder_path)
            print(f"Moved to misc: {file} -> {misc_folder_path}")

def main():
    parser = argparse.ArgumentParser(description="Organize Windows Start Menu shortcuts based on YAML config.")
    parser.add_argument("config_path", help="Path to the YAML configuration file")
    args = parser.parse_args()

    # Load config
    config = load_config(args.config_path)
    
    # Step 1: Move all shortcuts to temp folder
    move_shortcuts_to_temp(config['input_menus'], config['temp_folder'])
    
    # Step 2: Create folders in the output menu and organize shortcuts
    create_folders_and_organize(
        config['temp_folder'],
        config['output_menu'],
        config['folders'],
        config['misc_folder']
    )

    # Step 3: Remove empty folders in input_menus
    remove_empty_folders(config['input_menus'])
    
    # Step 4: Remove temp folder after organizing
    cleanup_temp_folder(config['temp_folder'])
    
    print("Start Menu organization complete!")

if __name__ == "__main__":
    main()
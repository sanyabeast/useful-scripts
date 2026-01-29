import os
import shutil
import argparse
import yaml
import logging
from datetime import datetime
import fnmatch

def match_pattern(pattern, filename, match_extension=False):
    """Match pattern against filename with optional wildcards.
    
    - 'name*' matches files starting with 'name'
    - '*name' matches files ending with 'name' (or extension like *.pdf)
    - '*name*' matches files containing 'name'
    - 'name' matches exactly 'name'
    
    If match_extension is True, matches against full filename including extension.
    Otherwise matches against filename without extension.
    """
    if match_extension:
        target = filename.lower()
    else:
        target = os.path.splitext(filename)[0].lower()
    
    pattern_lower = pattern.lower()
    starts_with_wildcard = pattern_lower.startswith('*')
    ends_with_wildcard = pattern_lower.endswith('*')
    
    if starts_with_wildcard and ends_with_wildcard:
        core = pattern_lower[1:-1]
        return core in target
    elif starts_with_wildcard:
        core = pattern_lower[1:]
        return target.endswith(core)
    elif ends_with_wildcard:
        core = pattern_lower[:-1]
        return target.startswith(core)
    else:
        return target == pattern_lower

def matches_any_pattern(filename, patterns):
    """Check if filename matches any of the given patterns."""
    for pattern in patterns:
        has_extension = '.' in pattern and not pattern.startswith('*.')
        match_ext = '.' in pattern
        if match_pattern(pattern, filename, match_extension=match_ext):
            return True
    return False

def setup_logging():
    """Setup logging configuration."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"start_menu_organizer_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_filename}")
    return logger

def load_config(file_path):
    """Loads the YAML configuration file."""
    logger = logging.getLogger(__name__)
    logger.info(f"Loading configuration from: {file_path}")
    
    try:
        if not os.path.exists(file_path):
            logger.error(f"Configuration file not found: {file_path}")
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
            
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info("Configuration loaded successfully")
            logger.debug(f"Configuration contents: {config}")
            return config
            
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        raise

def move_shortcuts_to_temp(input_menus, temp_folder, exclude_patterns=None):
    """Move all shortcuts from input menus to the temporary folder, ignoring the Startup folder."""
    logger = logging.getLogger(__name__)
    logger.info(f"Starting to move shortcuts to temp folder: {temp_folder}")
    
    if exclude_patterns is None:
        exclude_patterns = []
    
    shortcuts_moved = 0
    shortcuts_excluded = 0
    errors_encountered = 0
    
    try:
        if not os.path.exists(temp_folder):
            logger.info(f"Creating temp folder: {temp_folder}")
            os.makedirs(temp_folder)
        else:
            logger.info(f"Temp folder already exists: {temp_folder}")

        for menu in input_menus:
            logger.info(f"Processing input menu: {menu}")
            
            if not os.path.exists(menu):
                logger.warning(f"Input menu path does not exist: {menu}")
                continue
                
            for root, _, files in os.walk(menu):
                if "Startup" in os.path.basename(root):
                    logger.info(f"Skipping Startup folder: {root}")
                    continue

                logger.debug(f"Processing directory: {root} with {len(files)} files")
                
                for file in files:
                    if file.endswith(".lnk"):
                        if exclude_patterns and matches_any_pattern(file, exclude_patterns):
                            logger.info(f"Excluded by pattern: {file}")
                            shortcuts_excluded += 1
                            continue
                        
                        source = os.path.join(root, file)
                        destination = os.path.join(temp_folder, file)
                        
                        try:
                            if os.path.exists(destination):
                                logger.info(f"Overwriting duplicate: {destination}")
                                os.remove(destination)
                                
                            shutil.move(source, destination)
                            logger.info(f"Moved: {source} -> {destination}")
                            shortcuts_moved += 1
                            
                        except Exception as e:
                            logger.error(f"Failed to move {source} to {destination}: {e}")
                            errors_encountered += 1
                            
        logger.info(f"Move operation completed. Shortcuts moved: {shortcuts_moved}, Excluded: {shortcuts_excluded}, Errors: {errors_encountered}")
        
    except Exception as e:
        logger.error(f"Critical error in move_shortcuts_to_temp: {e}")
        raise

def remove_empty_folders(input_menus):
    """Remove empty folders from the input menus, except Startup."""
    logger = logging.getLogger(__name__)
    logger.info("Starting to remove empty folders")
    
    folders_removed = 0
    folders_skipped = 0
    
    try:
        for menu in input_menus:
            logger.info(f"Cleaning empty folders in menu: {menu}")
            
            if not os.path.exists(menu):
                logger.warning(f"Menu path does not exist: {menu}")
                continue
                
            for root, dirs, _ in os.walk(menu, topdown=False):
                # Ignore Startup folder
                if "Startup" in os.path.basename(root):
                    logger.debug(f"Skipping Startup folder: {root}")
                    continue

                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        os.rmdir(dir_path)
                        logger.info(f"Removed empty folder: {dir_path}")
                        folders_removed += 1
                    except OSError as e:
                        logger.debug(f"Could not remove folder {dir_path}: {e} (likely not empty)")
                        folders_skipped += 1
                        
        logger.info(f"Empty folder cleanup completed. Removed: {folders_removed}, Skipped: {folders_skipped}")
        
    except Exception as e:
        logger.error(f"Critical error in remove_empty_folders: {e}")
        raise

def cleanup_temp_folder(temp_folder):
    """Remove the temp folder after organizing."""
    logger = logging.getLogger(__name__)
    logger.info(f"Cleaning up temp folder: {temp_folder}")
    
    try:
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
            logger.info(f"Successfully removed temp folder: {temp_folder}")
        else:
            logger.warning(f"Temp folder does not exist: {temp_folder}")
    except OSError as e:
        logger.error(f"Error removing temp folder {temp_folder}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error removing temp folder {temp_folder}: {e}")
        raise

def create_nested_folder(base_path, folder_path):
    """Create nested folder structure, handling both forward and back slashes."""
    logger = logging.getLogger(__name__)
    
    # Normalize path separators for Windows
    normalized_path = folder_path.replace('/', os.sep)
    full_path = os.path.join(base_path, normalized_path)
    
    try:
        os.makedirs(full_path, exist_ok=True)
        logger.info(f"Created/verified nested folder: {full_path}")
        return full_path
    except Exception as e:
        logger.error(f"Failed to create nested folder {full_path}: {e}")
        raise

def create_folders_and_organize(temp_folder, output_menu, folders, misc_folder):
    """Create folders in the output menu and move shortcuts from temp folder."""
    logger = logging.getLogger(__name__)
    logger.info(f"Starting organization in output menu: {output_menu}")
    
    shortcuts_organized = 0
    shortcuts_to_misc = 0
    errors_encountered = 0
    
    try:
        # Ensure output menu exists
        if not os.path.exists(output_menu):
            logger.info(f"Creating output menu directory: {output_menu}")
            os.makedirs(output_menu, exist_ok=True)
            
        # Create folders listed in the config (supporting nested paths)
        logger.info(f"Creating {len(folders)} organized folders (including nested structures)")
        for folder_name, shortcuts in folders.items():
            try:
                # Create nested folder structure
                folder_path = create_nested_folder(output_menu, folder_name)
                
                logger.debug(f"Processing {len(shortcuts)} shortcuts for folder '{folder_name}'")
                for shortcut_pattern in shortcuts:
                    has_wildcard = shortcut_pattern.startswith('*') or shortcut_pattern.endswith('*')
                    
                    if has_wildcard:
                        matched_files = [
                            f for f in os.listdir(temp_folder)
                            if f.endswith('.lnk') and match_pattern(shortcut_pattern, f, match_extension=False)
                        ]
                        if matched_files:
                            for shortcut_file in matched_files:
                                shortcut_path = os.path.join(temp_folder, shortcut_file)
                                try:
                                    shutil.copy(shortcut_path, folder_path)
                                    logger.info(f"Copied (pattern '{shortcut_pattern}'): {shortcut_file} -> {folder_path}")
                                    shortcuts_organized += 1
                                except Exception as e:
                                    logger.error(f"Failed to copy {shortcut_file} to {folder_path}: {e}")
                                    errors_encountered += 1
                        else:
                            logger.warning(f"No shortcuts matched pattern: {shortcut_pattern}")
                    else:
                        shortcut_file = shortcut_pattern + ".lnk"
                        shortcut_path = os.path.join(temp_folder, shortcut_file)
                        
                        if os.path.exists(shortcut_path):
                            try:
                                shutil.copy(shortcut_path, folder_path)
                                logger.info(f"Copied: {shortcut_file} -> {folder_path}")
                                shortcuts_organized += 1
                            except Exception as e:
                                logger.error(f"Failed to copy {shortcut_file} to {folder_path}: {e}")
                                errors_encountered += 1
                        else:
                            logger.warning(f"Shortcut not found in temp folder: {shortcut_file}")
                        
            except Exception as e:
                logger.error(f"Error creating/processing folder {folder_name}: {e}")
                errors_encountered += 1

        # Create the misc folder for unlisted shortcuts (supporting nested paths)
        try:
            misc_folder_path = create_nested_folder(output_menu, misc_folder)
            
            # Move remaining shortcuts to the misc folder
            if os.path.exists(temp_folder):
                remaining_files = [f for f in os.listdir(temp_folder) if f.endswith(".lnk")]
                logger.info(f"Moving {len(remaining_files)} remaining shortcuts to misc folder: {misc_folder_path}")
                
                for file in remaining_files:
                    try:
                        source_path = os.path.join(temp_folder, file)
                        shutil.move(source_path, misc_folder_path)
                        logger.info(f"Moved to misc: {file} -> {misc_folder_path}")
                        shortcuts_to_misc += 1
                    except Exception as e:
                        logger.error(f"Failed to move {file} to misc folder: {e}")
                        errors_encountered += 1
            else:
                logger.warning(f"Temp folder does not exist: {temp_folder}")
                
        except Exception as e:
            logger.error(f"Error creating/processing misc folder: {e}")
            errors_encountered += 1
            
        logger.info(f"Organization completed. Organized: {shortcuts_organized}, To misc: {shortcuts_to_misc}, Errors: {errors_encountered}")
        
    except Exception as e:
        logger.error(f"Critical error in create_folders_and_organize: {e}")
        raise

def main():
    # Setup logging first
    logger = setup_logging()
    
    try:
        parser = argparse.ArgumentParser(description="Organize Windows Start Menu shortcuts based on YAML config.")
        parser.add_argument("config_path", help="Path to the YAML configuration file")
        parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
        args = parser.parse_args()
        
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.info("Verbose logging enabled")
        
        logger.info("=== Start Menu Organizer Started ===")
        logger.info(f"Configuration file: {args.config_path}")
        
        # Load config
        config = load_config(args.config_path)
        
        # Validate config
        required_keys = ['input_menus', 'temp_folder', 'output_menu', 'folders', 'misc_folder']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            logger.error(f"Missing required configuration keys: {missing_keys}")
            raise ValueError(f"Missing required configuration keys: {missing_keys}")
            
        logger.info(f"Configuration validated. Input menus: {len(config['input_menus'])}, Folders to create: {len(config['folders'])}")
        
        exclude_patterns = config.get('exclude_patterns', [])
        if exclude_patterns:
            logger.info(f"Exclude patterns configured: {exclude_patterns}")
        
        # Step 1: Move all shortcuts to temp folder
        logger.info("=== Step 1: Moving shortcuts to temp folder ===")
        move_shortcuts_to_temp(config['input_menus'], config['temp_folder'], exclude_patterns)
        
        # Step 2: Create folders in the output menu and organize shortcuts
        logger.info("=== Step 2: Organizing shortcuts into folders ===")
        create_folders_and_organize(
            config['temp_folder'],
            config['output_menu'],
            config['folders'],
            config['misc_folder']
        )

        # Step 3: Remove empty folders in input_menus
        logger.info("=== Step 3: Removing empty folders ===")
        remove_empty_folders(config['input_menus'])
        
        # Step 4: Remove temp folder after organizing
        logger.info("=== Step 4: Cleaning up temp folder ===")
        cleanup_temp_folder(config['temp_folder'])
        
        logger.info("=== Start Menu organization completed successfully! ===")
        print("Start Menu organization complete! Check the log file for detailed information.")
        
    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")
        print("Operation cancelled by user.")
    except Exception as e:
        logger.error(f"Critical error during execution: {e}")
        print(f"Error: {e}")
        print("Check the log file for detailed error information.")
        raise

if __name__ == "__main__":
    main()
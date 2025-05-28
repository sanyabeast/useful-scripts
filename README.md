# Useful Scripts

A versatile collection of utility scripts for everyday tasks including image processing, file management, audio manipulation, and ML tools. Features cross-platform solutions with a focus on automation and productivity.

## 📂 Repository Structure

```
useful-scripts/
├── scripts/
│   ├── android/            # Android-specific utilities
│   ├── audio/              # Audio file manipulation and playlist creation
│   ├── chatworks/          # Chat and messaging related tools
│   ├── chrome_extensions/  # Chrome browser extension utilities
│   ├── files/              # File management and organization scripts
│   ├── folders/            # Directory management utilities
│   ├── images/             # Image processing, conversion and manipulation
│   ├── lms/                # LM Studio tools including dataset creation
│   ├── macos/              # macOS specific utilities
│   ├── ml/                 # Machine learning utilities
│   ├── night_shift/        # Night mode and display adjustment tools
│   ├── videos/             # Video processing utilities
│   ├── web_misc/           # Miscellaneous web tools
│   ├── web_userscripts/    # Browser userscripts
│   └── windows/            # Windows OS specific utilities
└── docs/                   # Documentation
```

## 🌟 Featured Scripts

### Image Dataset Maker
Create structured image datasets with AI-generated descriptions:
- Renames images sequentially (0001.jpg, 0002.jpg, etc.)
- Converts images to JPEG format
- Creates text files with AI-generated descriptions
- Supports multiple resolutions
- Includes drag-and-drop functionality

### Audio Tools
- Create playlists from directories (M3U, M3U8, XSPF formats)
- Measure and adjust audio volume levels

### File Management
- Batch rename files using various patterns
- Create symbolic links
- Organize files by extension or pattern

### Platform-specific Utilities
- Windows registry tweaks and power management
- macOS system utilities
- Android device management

## 🚀 Getting Started

Most scripts can be run directly with Python or their respective interpreters:

```bash
# For Python scripts
python scripts/category/script_name.py --help

# For batch files
scripts/category/script_name.bat

# For shell scripts
bash scripts/category/script_name.sh
```

## 📋 Requirements

- Python 3.6+ for most Python scripts
- Platform-specific requirements are documented within each script
- Some scripts may require additional libraries (requirements listed in script headers)

## 🔧 Usage Examples

### Image Dataset Maker

```bash
# Basic usage
python scripts/lms/image_dataset_maker/main.py -i "input_folder" -o "output_folder" -m "model_name"

# With additional options
python scripts/lms/image_dataset_maker/main.py -i "input_folder" -o "output_folder" -m "model_name" --resolution "512 768 1024" --prefix "A photo of" --recursive
```

### Audio Playlist Creator

```bash
python scripts/audio/dir_to_m3u8.py "music_folder" "playlist_name.m3u8"
```

### File Renaming

```bash
python scripts/files/rename_substitute_in_folder.py "folder_path" "pattern_to_replace" "replacement_text"
```

## 🤝 Contributing

Feel free to fork, modify, and use these scripts according to your needs. Pull requests for improvements or new scripts are welcome!

## 📄 License

IDGAF License - Use as you wish, no restrictions.

## 👤 Author

**sanyabeast** - [GitHub Profile](https://github.com/sanyabeast)

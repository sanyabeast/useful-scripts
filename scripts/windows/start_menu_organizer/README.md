# Start Menu Organizer

A Python script for organizing Windows Start Menu shortcuts based on a YAML configuration file.

## Features

- **Organize shortcuts into folders** — move shortcuts to categorized folders based on config
- **Wildcard pattern matching** — use `*` for flexible shortcut matching:
  - `name*` — matches shortcuts starting with "name"
  - `*name` — matches shortcuts ending with "name"
  - `*name*` — matches shortcuts containing "name"
- **Exclude patterns** — automatically delete unwanted shortcuts (uninstallers, documentation, etc.)
- **Cleanup** — removes all non-.lnk files and empty folders recursively
- **Nested folders** — supports creating nested folder structures (e.g., `Gaming/Stores`)
- **Misc folder** — unmatched shortcuts go to a configurable "misc" folder
- **Detailed logging** — creates timestamped log files for each run

## Usage

```bash
python main.py <config_path> [--verbose]
```

**Arguments:**
- `config_path` — path to the YAML configuration file
- `--verbose`, `-v` — enable detailed debug logging

**Example:**
```bash
python main.py example.config.yaml
```

## Configuration

Create a YAML config file with the following structure:

```yaml
input_menus:
  - C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs
  - C:\ProgramData\Microsoft\Windows\Start Menu\Programs

output_menu: C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs

misc_folder: "More/Apps"

temp_folder: "./start_menu_temp"

exclude_patterns:
  - "*uninstall*"
  - "*documentation*"
  - "*readme*"
  - "*help*"
  - "*.html"
  - "*.chm"
  - "*.pdf"
  - "*.url"

folders:
  Development:
    - Visual Studio Code
    - Git Bash
    - Godot*
  Gaming:
    - Steam
    - Epic Games Launcher
  Tools:
    - OBS Studio*
    - GIMP*
```

### Config Options

| Key | Required | Description |
|-----|----------|-------------|
| `input_menus` | Yes | List of Start Menu paths to scan |
| `output_menu` | Yes | Where to create organized folders |
| `misc_folder` | Yes | Folder for unmatched shortcuts |
| `temp_folder` | Yes | Temporary working directory |
| `exclude_patterns` | No | Patterns for shortcuts to delete |
| `folders` | Yes | Folder structure with shortcut mappings |

## How It Works

1. **Move** all `.lnk` shortcuts from input menus to temp folder
2. **Delete** non-.lnk files and excluded shortcuts
3. **Organize** shortcuts into configured folders
4. **Move** remaining shortcuts to misc folder
5. **Cleanup** empty folders recursively
6. **Remove** temp folder

## Notes

- The `Startup` folder is always ignored
- Duplicate shortcuts are overwritten
- Case-insensitive pattern matching
- Log files are created in the current working directory

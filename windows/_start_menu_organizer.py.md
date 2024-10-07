
Start Menu Organizer
=====================

Organize your Windows Start Menu shortcuts like a pro!

This tool helps you tidy up your Start Menu by moving all shortcut files (with `.lnk` extension) from input menus to a temporary folder. You can then create folders and organize these shortcuts based on your preferences.

**How it Works**

1. Run the script with Python: `python start_menu_organizer.py`
2. Provide the path to your YAML configuration file as an argument (e.g., `--config_path config.yaml`)
3. The script will load the config, move all shortcut files from input menus to a temporary folder
4. Create folders and organize shortcuts based on your config settings

**Config File Format**

The config file should be in YAML format with the following structure:
```yaml
input_menus: ["Menu 1", "Menu 2"]
temp_folder: "/path/to/temp/folder"
output_menu: "/path/to/output/menu"
folders:
    - Folder 1
    - Folder 2
misc_folder: "Miscellaneous"

```
**Example Usage**

Run the script with Python and provide your config file path as an argument:

`python start_menu_organizer.py --config_path config.yaml`

This will organize your Start Menu shortcuts based on your configuration settings.
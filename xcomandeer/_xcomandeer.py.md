XComander: A Python Script to Execute Commands with Parameters

This script, xcomandeer.py, is designed to execute commands with parameters. It reads a YAML configuration file that contains a dictionary of command strings, where each key-value pair represents a command and its corresponding string.

**How it Works**

1. The script reads the YAML configuration file located at `~/.config/xcomandeer.yaml`.
2. If no command name is provided as an argument to the script, it prints usage instructions.
3. It retrieves the command string from the dictionary based on the provided command name.
4. Replaces any `%0`, `%1`, or `%2` substrings in the command string with the provided arguments (if any).
5. Executes the resulting command using `subprocess.run()` with shell=True.

**Prerequisites**

* This script is designed for Python 3.x and later versions.
* You must have YAML installed on your system to use this script.
* The configuration file should be placed at `~/.config/xcomandeer.yaml` in a format that follows the provided structure.

**Usage**

1. Place the YAML configuration file at `~/.config/xcomandeer.yaml`.
2. Run the script with a command name and optional arguments: `python xcomandeer.py <command_name> [args...]`.

For example, if you have a command named "my_command" in your YAML file that takes two parameters:

```
my_command:  |
    echo "The first parameter is: %0"
    echo "The second parameter is: %1"
```

You can execute it with the following command:

`python xcomandeer.py my_command arg1 arg2`

This will replace `%0` and `%1` in the command string with `arg1` and `arg2`, respectively, and then execute the resulting command.
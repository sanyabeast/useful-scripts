#!/usr/bin/env python3

import sys
import yaml
import subprocess

# The configuration file should be placed at ~/.config/xcomandeer.yaml
# The structure of the configuration file should follow this format:
#
# command_name: |
#   command line 1
#   command line 2
#   ...
#
# The command body can span multiple lines and should be indented by two spaces. To use
# parameters in the command, use the syntax %0, %1, %2, and so on, which correspond to
# the first, second, third, and so on extra parameters passed to the command when executed.
# For example:
#
# my_command: |
#   echo "The first parameter is: %0"
#   echo "The second parameter is: %1"


def main():
    """
    This function main() reads a YAML file containing a dictionary of commands, where the keys are the names of the commands and the values are the command strings. It then checks if a command name is provided as an argument to the script, and if so, retrieves the corresponding command string from the dictionary. The function then replaces any %0, %1, or %2 substrings in the command string with the provided arguments, if any, and executes the resulting command using the subprocess.run() function with shell=True. If a command name is not provided or the command does not exist in the YAML file, an error message is printed. The function takes no arguments and has no return value.
    """
    
    # Read the YAML file
    with open('/home/retr0/.config/xcomandeer.yaml', 'r') as f:
        data = yaml.safe_load(f)

    # Check if a command name was provided
    if len(sys.argv) < 2:
        print("Usage: xcomandeer.py <command_name> [args...]")
        return

    # Get the command and its arguments
    command_name = sys.argv[1]
    command_args = sys.argv[2:]

    # Check if the command exists
    if command_name not in data:
        print("Command not found: {}".format(command_name))
        return

    # Build the command string

    command_str = data[command_name]
    
    for index, item in enumerate(command_args):
        print(index)
        command_str = command_str.replace(f'%{index}', str(item))
        
    # Execute the command
    subprocess.run(command_str, shell=True)

if __name__ == "__main__":
    main()
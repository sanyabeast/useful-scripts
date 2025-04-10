# callme.sh

README for callme.sh - A simple logging script

## Overview

The `callme.sh` script is a utility designed to log command-line arguments along with a timestamp and the name of the calling function/script to a designated log file. It's intended as a lightweight mechanism for tracking what commands are being executed, particularly useful in larger scripts or automated processes where debugging can be challenging.

## Main Components & Logic

The script performs the following actions:

1. **Determines Script Name and Directory:**  It extracts the name of the script (`callme.sh`) and its directory using `basename` and `dirname`. This is crucial for creating a consistent log file location.
2. **Creates Log File Path:** It constructs the path to the log file by combining the script's directory with the script's name (without the `.sh` extension).  For example, if the script is located at `/path/to/callme.sh`, the log file will be created at `/path/to/callme.log`.
3. **Gets Current Date and Time:** It captures the current date and time in a standardized `YYYY-MM-DD HH:MM:SS` format using the `date` command.
4. **Retrieves Command Line Arguments:**  It stores all command-line arguments passed to the script into the `ARGS` variable using `$@`.
5. **Identifies Calling Function/Script:** This is a key feature. It attempts to determine which function or script invoked `callme.sh`. If `callme.sh` is called directly (i.e., from the main execution context), it identifies the caller as the script's name itself (`callme.sh`). Otherwise, if it’s called within a function, it uses the `$FUNCNAME` variable to identify the calling function.
6. **Logs the Information:** Finally, it appends a line containing the timestamp, arguments, and caller information to the log file using `echo >>`.  This ensures that each call is recorded in chronological order.

## Assumptions & Requirements

*   **Bash Shell:** The script requires a Bash shell environment to execute correctly. It uses Bash-specific syntax and commands.
*   **Write Permissions:** The user executing the script must have write permissions to the directory where `callme.sh` is located, as this is where the log file will be created.
*   **Date Command Availability:**  The `date` command must be available in the system's PATH.

## Limitations

*   **Simple Logging:** The script provides basic logging functionality only. It doesn’t offer advanced features like log level control, filtering, or remote logging.
*   **Log File Size:**  The log file will grow indefinitely with each execution. There's no mechanism for rotating or archiving the log file. Consider implementing log rotation if this becomes an issue.
*   **Error Handling:** The script lacks robust error handling. It doesn’t check for errors during file creation or writing, which could lead to unexpected behavior.
*   **Caller Identification:**  The caller identification relies on `$FUNCNAME`. This might not be reliable in all scenarios, especially with complex function calls or nested scripts.

## Example Use Cases

1. **Debugging Scripts:** Embed `callme.sh` within your scripts to log the arguments passed to specific functions or commands, aiding in debugging and understanding program flow.
2. **Auditing Command Execution:**  Use it to track which commands are being executed in an automated process for auditing purposes.
3. **Monitoring Function Calls:** Log function calls with their parameters to monitor how a system is being used.

## Usage Examples

**1. Calling `callme.sh` directly:**

```bash
./callme.sh arg1 "arg2 with spaces" --option=value
```

This will append a line to `callme.log` similar to:

```
2023-10-27 10:30:00: arg1 "arg2 with spaces" --option=value
```

The caller would be identified as `callme.sh`.

**2. Calling `callme.sh` from within a function:**

```bash
my_function() {
  echo "Entering my_function"
  ./callme.sh --debug arg1 "arg with spaces"
  echo "Exiting my_function"
}

my_function
```

This will append a line to `callme.log` similar to:

```
2023-10-27 10:35:00: --debug arg1 "arg with spaces"
```

The caller would be identified as `my_function`.

**3.  Integrating into a script:**

```bash
#!/bin/bash

log() {
    ./callme.sh "$@"
}

log --message="This is a test message" arg1 arg2
```

This will append a line to `callme.log` similar to:

```
2023-10-27 10:40:00: --message="This is a test message" arg1 arg2
```

The caller would be identified as `log`.

## Additional Notes

*   The log file path can be modified by changing the `LOG_FILE` variable within the script. However, ensure that the new location is accessible and writable.
*   Consider adding error handling to make the script more robust in production environments.
*   For more advanced logging needs, explore dedicated logging libraries or tools available for Bash scripting.

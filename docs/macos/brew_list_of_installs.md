# brew_list_of_installs.sh

brew_list_of_installs.sh - A script to list Homebrew formulas and their total disk usage across all versions.

This script provides a comprehensive overview of installed Homebrew formulas, including not only the formula name but also an estimate of the total disk space occupied by each formula's files across all available versions. This is particularly useful for identifying large or resource-intensive packages and managing disk space effectively.

**Important Note:** The script has been duplicated in the provided content.  This will cause errors when executed. I am assuming this was an unintentional error, and only one instance of the loop should be present in the actual file.

## Usage

The script is designed to be run directly from the command line within a Homebrew environment (macOS).

```bash
./brew_list_of_installs.sh
```

This will print a list of installed formulas, each followed by its total disk usage estimate.

## Logic Breakdown

The script operates in the following steps:

1. **Formula Listing:** `brew list --formula -1` retrieves a list of all installed Homebrew formulas. The `-1` flag ensures that only the formula name is returned, one per line.
2. **Filtering (Optional):**  `egrep -v '	|	.'` filters out any lines containing tabs or periods. This is likely intended to remove entries that might cause issues with subsequent processing but its purpose isn't entirely clear and could be removed if it causes problems.
3. **Iteration:** A `for` loop iterates through each formula name obtained in the previous steps.
4. **Formula Information Retrieval:** Inside the loop, `brew info $pkg` retrieves detailed information about the current formula from Homebrew.  This includes file counts and version information.
5. **File Count Extraction:** `egrep '[0-9]* files, ' | sed 's/^.*[0-9]* files, (.*)	.*$/ackslash1/'` extracts the number of files associated with the formula from the output of `brew info`.  The `sed` command uses a regular expression to isolate the file count string.
6. **Disk Usage Calculation:** The script attempts to calculate the total disk usage across all versions by summing up the sizes reported in the `brew info` output. It parses size suffixes (KB, MB, GB) and converts them to a consistent unit for summation.  The awk script is responsible for this calculation.
7. **Output Formatting:** Finally, the script prints the formula name followed by the calculated total disk usage estimate, formatted with appropriate units.

## Assumptions & Requirements

*   **Homebrew Installation:** The script requires Homebrew to be installed and properly configured on your macOS system.  It relies on `brew list` and `brew info` commands being available in your PATH.
*   **Bash Environment:** The script is written for a Bash shell environment. While it might work with other shells, compatibility isn't guaranteed.
*   **File Size Parsing Accuracy:** The disk usage calculation depends on the accuracy of the file sizes reported by `brew info`.  These values may not always be perfectly precise and can vary depending on how Homebrew manages versions.
*   **`egrep` Availability:** The script uses `egrep`, which is part of GNU grep. Most macOS systems have this available, but if you encounter issues, ensure it's installed or use a compatible alternative (e.g., `grep -E`).
*   **No Tabs/Periods in Formula Names:**  The `egrep` filter assumes that formula names do not contain tabs or periods. If your Homebrew setup has formulas with these characters, the script might produce unexpected results.

## Limitations

*   **Version-Specific Disk Usage:** The script attempts to calculate total disk usage across all versions but relies on `brew info` providing accurate version-specific file sizes.  This may not always be reliable or complete.
*   **Symbolic Links and Hard Links:** The script doesn't account for symbolic links or hard links, which can affect the actual disk space used by a formula.
*   **Dependencies:** It does *not* calculate the total disk usage of dependencies.  It only focuses on the direct formulas listed by `brew list`.
*   **Performance:** For systems with a large number of installed formulas, the script's execution time can be significant due to repeated calls to `brew info`.

## Example Use Cases

*   **Disk Space Management:** Identify which Homebrew formulas are consuming the most disk space and consider uninstalling or removing older versions if necessary.
*   **Resource Optimization:**  Gain insights into the resource footprint of different software packages installed via Homebrew.
*   **Troubleshooting:** Investigate potential disk space issues by identifying large or unexpected formula sizes.

## Potential Improvements

*   **Caching:** Implement caching to avoid repeated calls to `brew info` for frequently accessed formulas, improving performance.
*   **Dependency Analysis:** Extend the script to calculate the total disk usage of dependencies as well.
*   **Error Handling:** Add more robust error handling to gracefully handle cases where `brew info` fails or returns unexpected output.
*   **Configuration Options:** Allow users to customize filtering options and output formatting.
*   **Parallelization:** Explore parallelizing the execution of `brew info` calls to further reduce overall runtime.

## Author

[Your Name/Organization]

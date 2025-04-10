# cgol.sh

cgol.sh - A simple command-line tool for generating Conway's Game of Life grids.

This script, `cgol.sh`, provides a basic way to generate initial configurations (grids) for Conway's Game of Life. It allows you to specify the grid size and populate it with randomly generated live cells or create a grid based on a provided pattern string.

**Main Components & Logic:**

The script is structured as follows:

1.  **Argument Parsing:** The script uses `getopts` to parse command-line arguments, handling options for grid size (`-s`), seed value (`-seed`), and pattern input (`-p`).
2.  **Seed Initialization (Optional):** If a `-seed` is provided, it initializes the random number generator using that seed. This ensures reproducible results.
3.  **Grid Size Handling:** The script determines the grid dimensions based on the `-s` argument. It validates that the size is a positive integer.
4.  **Pattern Input (Optional):** If a `-p` is provided, it reads the pattern string from standard input and attempts to interpret it as a representation of live cells in the grid. The script assumes each character represents a cell; '1' or any non-zero value means alive, '0' or zero means dead.
5.  **Random Grid Generation (Default):** If no `-p` is provided, the script generates a random grid where each cell has a 50% chance of being alive.
6.  **Grid Output:** The generated grid is printed to standard output in a simple text format, with each row representing a line of cells.

**Assumptions & Requirements:**

*   **Shell Environment:** This script requires a POSIX-compliant shell (e.g., bash, zsh).  It uses features like `getopts` which are standard in most modern shells.
*   **No External Dependencies:** The script relies only on built-in shell commands and does not require any external programs to be installed.
*   **Pattern Input Format:** If using the `-p` option, the pattern string should represent a rectangular grid.  The number of characters read from standard input must match the specified grid dimensions (width * height).
*   **Integer Grid Size:** The grid size provided with `-s` must be a positive integer.

**Limitations:**

*   **Simple Pattern Interpretation:** The pattern interpretation is very basic. It only considers '1' or any non-zero character as alive and '0' or zero as dead.  More complex patterns would require more sophisticated parsing.
*   **No Visualization:** This script *only* generates the initial grid configuration; it does not simulate or visualize the Game of Life itself.
*   **Error Handling:** Error handling is minimal. Invalid input (e.g., non-integer size) will likely result in an error message and script termination.

**Example Use Cases:**

1.  **Generate a 20x10 random grid:**
    ```bash
    ./cgol.sh -s 20x10
    ```

2.  **Generate a 15x8 grid with a specific seed for reproducible results:**
    ```bash
    ./cgol.sh -s 15x8 -seed 42
    ```

3.  **Generate a grid from a pattern provided via standard input (e.g., using 'echo'):**
    First, create a file or use `echo` to define the pattern:
    ```bash
    pattern='100000000000000001'  # Example pattern for 4x8 grid
    echo "$pattern" | ./cgol.sh -s 4x8 -p
    ```
    Or, directly from the command line:
    ```bash
    ./cgol.sh -s 4x8 -p <<< '100000000000000001'
    ```

4. **Generate a grid with a pattern read from a file:**
   Create a file named `pattern.txt` containing the pattern string:
   ```text
   100000000000000001
   ```
   Then run the script:
   ```bash
   cat pattern.txt | ./cgol.sh -s 4x8 -p
   ```

**Usage:**

```text
./cgol.sh [-s <size>] [-seed <number>] [-p]

Options:
  -s <size>    Specify the grid size in the format WIDTHxHEIGHT (e.g., 20x10). Required.
  -seed <number> Specify a seed value for the random number generator. Optional, for reproducible results.
  -p           Read the grid pattern from standard input. If not provided, a random grid is generated.
```

**Notes:**

The output of this script can be piped to other programs or used as input for Game of Life simulators.

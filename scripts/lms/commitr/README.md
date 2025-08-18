# commitr - Git Commit Assistant with LMStudio Integration

A Python-based CLI tool that integrates with LMStudio to automatically generate meaningful Git commit messages and descriptions by analyzing staged files.

## Features

- 🔍 **Smart Analysis**: Analyzes Git diffs using LMStudio LLM to understand code changes
- 📝 **Conventional Commits**: Generates commit messages following conventional commit format
- 🤖 **LLM Integration**: Uses LMStudio Python package for local AI processing
- 🎯 **Interactive**: Review and approve generated commit messages before committing
- 🏃 **Dry Run**: Test commit message generation without actually committing
- 📊 **Verbose Mode**: See detailed analysis of file changes
- 🌐 **Cross-Platform**: Works on Windows, macOS, and Linux

## Prerequisites

- Python 3.8 or higher
- Git installed and configured
- LMStudio running with a loaded model
- `lmstudio` Python package

## Installation

### Option 1: Quick Install (Recommended)

**Windows:**
```cmd
cd path\to\commitr
install.bat
```

**macOS/Linux:**
```bash
cd path/to/commitr
chmod +x install.sh
./install.sh
```

### Option 2: Manual Install

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Basic Usage

```bash
# Navigate to your Git repository
cd your-git-repo

# Stage some files
git add .

# Generate and commit with AI assistance
commitr --model your-model-name
```

### Command Options

```bash
commitr [OPTIONS]

Options:
  -m, --model MODEL_NAME    LMStudio model name (required)
  --dry-run                Generate message without committing
  -v, --verbose            Show detailed output including diffs
  -h, --help               Show help message
```

### Examples

```bash
# Basic usage with a specific model
commitr --model gemma-3-4b-it-qat

# Dry run to see what would be generated
commitr --model llama-3.1-8b --dry-run

# Verbose output to see detailed analysis
commitr --model qwen-2.5-7b --verbose

# Combine options
commitr --model gemma-3-4b-it-qat --dry-run --verbose
```

## How It Works

1. **Repository Check**: Verifies you're in a valid Git repository
2. **Staged Files Detection**: Finds all files currently staged for commit
3. **Diff Analysis**: Extracts Git diffs for each staged file
4. **LLM Analysis**: Sends each file's diff to LMStudio for analysis
5. **Commit Message Generation**: Creates a conventional commit message based on all changes
6. **Interactive Review**: Shows the generated message and asks for confirmation
7. **Commit**: Executes the Git commit with the approved message

## LMStudio Setup

1. Install and run LMStudio
2. Load your preferred model (e.g., Gemma, Llama, Qwen)
3. Make sure the model name matches what you pass to `--model`

Popular models that work well:
- `gemma-3-4b-it-qat`
- `llama-3.1-8b-instruct`
- `qwen-2.5-7b-instruct`

## Commit Message Format

The tool generates commit messages following the conventional commit format:

```
type: brief description under 50 characters

Optional longer description explaining why the change
was made and its impact on the codebase.
```

**Types used:**
- `feat`: New features
- `fix`: Bug fixes
- `refactor`: Code refactoring
- `docs`: Documentation changes
- `style`: Code style changes
- `test`: Test additions/changes
- `chore`: Maintenance tasks

## Example Output

```
🔍 Checking Git repository...
✅ Git repository detected
📋 Checking staged files...
✅ Found 2 staged file(s):
   • src/main.py
   • README.md
🤖 Loading LMStudio model: gemma-3-4b-it-qat...
✅ Model loaded successfully!
📁 Project: my-awesome-project

🔍 Analyzing file changes...
   📄 Analyzing src/main.py...
      ✅ feat: Added user authentication system
   📄 Analyzing README.md...
      ✅ docs: Updated installation instructions

💭 Generating commit message...

============================================================
📝 GENERATED COMMIT MESSAGE
============================================================
Title: feat: add user authentication system

Description:
Implemented JWT-based authentication with login/logout
functionality and updated documentation to reflect
the new installation requirements.
============================================================

❓ Do you want to commit with this message? [y/n/e]: y
✅ Commit successful!
📝 Commit message: feat: add user authentication system
📄 Description: Implemented JWT-based authentication...
🎉 All done!
```

## Troubleshooting

### Common Issues

**"Model not found" error:**
- Make sure LMStudio is running
- Verify the model name is correct
- Check that the model is loaded in LMStudio

**"Not in a Git repository" error:**
- Navigate to a directory that contains a `.git` folder
- Initialize a Git repository with `git init` if needed

**"No staged files" error:**
- Stage some files first: `git add <files>`
- Use `git status` to see what files are available to stage

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try reinstalling: `pip install -e . --force-reinstall`

### Getting Help

If you encounter issues:
1. Run with `--verbose` flag to see detailed output
2. Check that LMStudio is running and accessible
3. Verify your Python and pip installations
4. Make sure you're in a valid Git repository with staged files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built with the LMStudio Python package
- Inspired by conventional commit standards
- Uses Pydantic for structured LLM responses

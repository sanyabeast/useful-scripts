#!/bin/bash

echo "Installing commitr - Git Commit Assistant with LMStudio Integration"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "💡 Please install Python 3.8+ and try again"
    exit 1
fi

echo "✅ Python detected. Installing dependencies..."

# Install the package in development mode
pip3 install -e .

if [ $? -ne 0 ]; then
    echo
    echo "❌ Error: Installation failed"
    echo "💡 Make sure you have pip installed and try again"
    exit 1
fi

echo
echo "✅ Installation successful!"
echo
echo "You can now use 'commitr' from any directory in your terminal."
echo
echo "Usage examples:"
echo "  commitr --model gemma-3-4b-it-qat"
echo "  commitr --model your-model-name --dry-run"
echo "  commitr --model your-model-name --verbose"
echo
echo "Make sure LMStudio is running with your desired model loaded."
echo

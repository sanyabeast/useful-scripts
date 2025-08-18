#!/usr/bin/env python3
"""
Setup script for commitr - Git Commit Assistant with LMStudio Integration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="commitr",
    version="1.0.0",
    description="Git Commit Assistant with LMStudio Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/commitr",
    py_modules=["commitr"],
    install_requires=[
        "lmstudio>=0.2.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "commitr=commitr:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)

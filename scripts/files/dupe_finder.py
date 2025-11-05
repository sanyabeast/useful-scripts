#!/usr/bin/env python3
"""
Duplicate File Finder

This script analyzes files in a directory to find potential duplicates based on filename similarity
using fuzzy string matching. It generates a detailed report of potential duplicates with similarity scores.

Usage:
    python dupe_finder.py [options] <directory> [directory2]

Options:
    --threshold FLOAT       Similarity threshold (0.0-1.0, default: 0.6)
    --recursive             Search recursively in subdirectories
    --report FILE           Save report to file
    --interactive           Run in interactive mode
    --limit INT             Limit results to top N potential duplicates
    --case-insensitive      Make filename matching case-insensitive
    --help                  Show this help message

Examples:
    python dupe_finder.py --threshold 0.65 --recursive "D:\Photos"
    python dupe_finder.py "D:\Folder1" "D:\Folder2"  # Cross-folder comparison
"""

import os
import sys
import argparse
import time
from pathlib import Path
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
from fuzzysearch import find_near_matches
import difflib
import re

@dataclass
class FilePair:
    """Class to store information about a pair of potentially duplicate files"""
    file1: str
    file2: str
    similarity: float
    match_details: str

    def __str__(self) -> str:
        return f"{self.file1} ↔ {self.file2} (Similarity: {self.similarity:.2%})"


class DuplicateFinder:
    """Main class for finding potential duplicate files based on filename similarity"""
    
    def __init__(self, directory: str, threshold: float = 0.6, recursive: bool = False, 
                 limit: Optional[int] = None, directory2: Optional[str] = None, 
                 case_insensitive: bool = False):
        self.directory = os.path.abspath(directory)
        self.directory2 = os.path.abspath(directory2) if directory2 else None
        self.threshold = threshold
        self.recursive = recursive
        self.limit = limit
        self.case_insensitive = case_insensitive
        self.files: List[str] = []
        self.files2: List[str] = []
        self.potential_duplicates: List[FilePair] = []
        self.cross_folder_mode = directory2 is not None
        
    def scan_directory(self) -> None:
        """Scan the directory and collect all filenames"""
        if self.cross_folder_mode:
            print(f"Scanning directory 1: {self.directory}")
            print(f"Scanning directory 2: {self.directory2}")
        else:
            print(f"Scanning directory: {self.directory}")
        start_time = time.time()
        
        if self.recursive:
            for root, _, files in os.walk(self.directory):
                for file in files:
                    self.files.append(os.path.join(root, file))
        else:
            self.files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) 
                         if os.path.isfile(os.path.join(self.directory, f))]
        
        if self.cross_folder_mode:
            if self.recursive:
                for root, _, files in os.walk(self.directory2):
                    for file in files:
                        self.files2.append(os.path.join(root, file))
            else:
                self.files2 = [os.path.join(self.directory2, f) for f in os.listdir(self.directory2) 
                             if os.path.isfile(os.path.join(self.directory2, f))]
            print(f"Found {len(self.files)} files in folder 1 and {len(self.files2)} files in folder 2 in {time.time() - start_time:.2f} seconds")
        else:
            print(f"Found {len(self.files)} files in {time.time() - start_time:.2f} seconds")
    
    def get_base_filename(self, path: str) -> str:
        """Extract the base filename without extension"""
        return os.path.splitext(os.path.basename(path))[0]
    
    def calculate_similarity(self, str1: str, str2: str) -> Tuple[float, str]:
        """Calculate similarity between two strings and provide match details"""
        if self.case_insensitive:
            str1 = str1.lower()
            str2 = str2.lower()
        
        similarity = difflib.SequenceMatcher(None, str1, str2).ratio()
        
        # Use fuzzysearch to find specific matches
        max_l_dist = min(3, max(1, min(len(str1), len(str2)) // 10))  # Adaptive distance
        matches = find_near_matches(str1.lower(), str2.lower(), max_l_dist=max_l_dist)
        
        # Generate match details
        if matches:
            match_details = f"Found {len(matches)} fuzzy matches with max distance {max_l_dist}"
        else:
            match_details = "No specific fuzzy matches found"
            
        return similarity, match_details
    
    def find_duplicates(self) -> None:
        """Find potential duplicate files based on filename similarity"""
        if self.cross_folder_mode:
            print(f"Analyzing {len(self.files)} files from folder 1 against {len(self.files2)} files from folder 2...")
        else:
            print(f"Analyzing {len(self.files)} files for potential duplicates...")
        start_time = time.time()
        
        if self.cross_folder_mode:
            self._find_cross_folder_duplicates()
        else:
            self._find_same_folder_duplicates()
        
        self.potential_duplicates.sort(key=lambda x: x.similarity, reverse=True)
        
        if self.limit and len(self.potential_duplicates) > self.limit:
            self.potential_duplicates = self.potential_duplicates[:self.limit]
            
        print(f"Found {len(self.potential_duplicates)} potential duplicates in {time.time() - start_time:.2f} seconds")
    
    def _find_same_folder_duplicates(self) -> None:
        """Find duplicates within the same folder"""
        files_by_length: Dict[int, List[str]] = {}
        for file_path in self.files:
            base_name = self.get_base_filename(file_path)
            length = len(base_name)
            if length not in files_by_length:
                files_by_length[length] = []
            files_by_length[length].append(file_path)
        
        compared_pairs: Set[Tuple[str, str]] = set()
        
        for length, files in files_by_length.items():
            for nearby_length in range(max(1, length - 2), length + 3):
                if nearby_length not in files_by_length:
                    continue
                    
                for file1 in files:
                    base_name1 = self.get_base_filename(file1)
                    
                    for file2 in files_by_length[nearby_length]:
                        if file1 == file2:
                            continue
                            
                        pair = tuple(sorted([file1, file2]))
                        if pair in compared_pairs:
                            continue
                        compared_pairs.add(pair)
                        
                        base_name2 = self.get_base_filename(file2)
                        similarity, match_details = self.calculate_similarity(base_name1, base_name2)
                        
                        if similarity >= self.threshold:
                            self.potential_duplicates.append(
                                FilePair(file1, file2, similarity, match_details)
                            )
    
    def _find_cross_folder_duplicates(self) -> None:
        """Find duplicates across two different folders"""
        files1_by_length: Dict[int, List[str]] = {}
        for file_path in self.files:
            base_name = self.get_base_filename(file_path)
            length = len(base_name)
            if length not in files1_by_length:
                files1_by_length[length] = []
            files1_by_length[length].append(file_path)
        
        files2_by_length: Dict[int, List[str]] = {}
        for file_path in self.files2:
            base_name = self.get_base_filename(file_path)
            length = len(base_name)
            if length not in files2_by_length:
                files2_by_length[length] = []
            files2_by_length[length].append(file_path)
        
        for length1, files1 in files1_by_length.items():
            for nearby_length in range(max(1, length1 - 2), length1 + 3):
                if nearby_length not in files2_by_length:
                    continue
                    
                for file1 in files1:
                    base_name1 = self.get_base_filename(file1)
                    
                    for file2 in files2_by_length[nearby_length]:
                        base_name2 = self.get_base_filename(file2)
                        similarity, match_details = self.calculate_similarity(base_name1, base_name2)
                        
                        if similarity >= self.threshold:
                            self.potential_duplicates.append(
                                FilePair(file1, file2, similarity, match_details)
                            )
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate a detailed report of potential duplicates"""
        if not self.potential_duplicates:
            report = "No potential duplicates found."
            return report
            
        report = ["=== Duplicate File Finder Report ==="]
        if self.cross_folder_mode:
            report.extend([
                f"Directory 1: {self.directory}",
                f"Directory 2: {self.directory2}",
                f"Mode: Cross-folder comparison",
                f"Threshold: {self.threshold:.2%}",
                f"Recursive: {self.recursive}",
                f"Case-insensitive: {self.case_insensitive}",
                f"Total files scanned: {len(self.files)} (folder 1) + {len(self.files2)} (folder 2)",
                f"Potential duplicates found: {len(self.potential_duplicates)}",
            ])
        else:
            report.extend([
                f"Directory: {self.directory}",
                f"Threshold: {self.threshold:.2%}",
                f"Recursive: {self.recursive}",
                f"Case-insensitive: {self.case_insensitive}",
                f"Total files scanned: {len(self.files)}",
                f"Potential duplicates found: {len(self.potential_duplicates)}",
            ])
        report.append("\n=== Potential Duplicates (sorted by similarity) ===")
        
        for i, pair in enumerate(self.potential_duplicates, 1):
            report.append(f"\n{i}. Similarity: {pair.similarity:.2%}")
            report.append(f"   File 1: {pair.file1}")
            report.append(f"   File 2: {pair.file2}")
            report.append(f"   Match details: {pair.match_details}")
            
            # Add file metadata for comparison
            file1_size = os.path.getsize(pair.file1)
            file2_size = os.path.getsize(pair.file2)
            report.append(f"   Size: {file1_size} bytes vs {file2_size} bytes")
            
            # Calculate size difference percentage
            if max(file1_size, file2_size) > 0:  # Avoid division by zero
                size_diff = abs(file1_size - file2_size) / max(file1_size, file2_size)
                report.append(f"   Size difference: {size_diff:.2%}")
        
        report_text = "\n".join(report)
        
        # Save to file if requested
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"Report saved to {output_file}")
            
        return report_text
    
    def run(self, output_file: Optional[str] = None) -> str:
        """Run the complete duplicate finding process"""
        self.scan_directory()
        self.find_duplicates()
        return self.generate_report(output_file)


def interactive_mode() -> None:
    """Run the script in interactive mode with user prompts"""
    print("=== Duplicate File Finder - Interactive Mode ===")
    
    directory = input("Enter directory path to scan: ").strip()
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        return
    
    directory2_input = input("Enter second directory for cross-folder comparison (leave empty for same-folder mode): ").strip()
    directory2 = None
    if directory2_input:
        if not os.path.isdir(directory2_input):
            print(f"Error: '{directory2_input}' is not a valid directory")
            return
        directory2 = directory2_input
    
    threshold_input = input("Enter similarity threshold (0.0-1.0) [default: 0.6]: ").strip()
    threshold = 0.6 if not threshold_input else float(threshold_input)
    
    recursive = input("Search recursively? (y/n) [default: n]: ").strip().lower() == 'y'
    
    case_insensitive = input("Case-insensitive matching? (y/n) [default: n]: ").strip().lower() == 'y'
    
    limit_input = input("Limit results to top N matches (leave empty for no limit): ").strip()
    limit = int(limit_input) if limit_input else None
    
    report_file = input("Save report to file (leave empty to print to console): ").strip()
    report_file = report_file if report_file else None
    
    finder = DuplicateFinder(directory, threshold, recursive, limit, directory2, case_insensitive)
    report = finder.run(report_file)
    
    if not report_file:
        print("\n" + report)


def main() -> None:
    """Main function to parse arguments and run the script"""
    parser = argparse.ArgumentParser(description="Find potential duplicate files based on filename similarity")
    parser.add_argument("directory", nargs="?", help="Directory to scan for duplicates")
    parser.add_argument("directory2", nargs="?", help="Second directory for cross-folder comparison (optional)")
    parser.add_argument("--threshold", type=float, default=0.6, help="Similarity threshold (0.0-1.0, default: 0.6)")
    parser.add_argument("--recursive", action="store_true", help="Search recursively in subdirectories")
    parser.add_argument("--case-insensitive", action="store_true", help="Make filename matching case-insensitive")
    parser.add_argument("--report", help="Save report to file")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--limit", type=int, help="Limit results to top N potential duplicates")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    if not args.directory:
        parser.print_help()
        return
    
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory")
        return
    
    if args.directory2 and not os.path.isdir(args.directory2):
        print(f"Error: '{args.directory2}' is not a valid directory")
        return
    
    finder = DuplicateFinder(
        args.directory,
        args.threshold,
        args.recursive,
        args.limit,
        args.directory2,
        args.case_insensitive
    )
    
    report = finder.run(args.report)
    
    if not args.report:
        print("\n" + report)


if __name__ == "__main__":
    main()
"""
M3U8 Playlist Generator

Scans directories for audio files and generates M3U8 playlists with shuffled tracks.
Supports m4a, mp3, flac, wav, and ogg formats.

Usage:
    python dirs_to_m3u8.py <directory>              Generate playlist for single directory
    python dirs_to_m3u8.py <directory> -r           Recursively process all subdirectories
    python dirs_to_m3u8.py <directory> -s           Shuffle tracks randomly
    
Examples:
    python dirs_to_m3u8.py "C:/Music/Album"
    python dirs_to_m3u8.py "D:/Music" --recursive --shuffle
"""

import os
import re
import sys
import random
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


class Logger:
    @staticmethod
    def info(message: str) -> None:
        print(f"{Colors.CYAN}♪{Colors.RESET} {message}")
    
    @staticmethod
    def success(message: str) -> None:
        print(f"{Colors.GREEN}✓{Colors.RESET} {message}")
    
    @staticmethod
    def error(message: str) -> None:
        print(f"{Colors.RED}✗{Colors.RESET} {message}")
    
    @staticmethod
    def dim(message: str) -> None:
        print(f"{Colors.DIM}{message}{Colors.RESET}")
    
    @staticmethod
    def header(title: str, **details) -> None:
        width = 60
        print()
        print(f"{Colors.CYAN}{'═' * width}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{title.center(width)}{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * width}{Colors.RESET}")
        for key, value in details.items():
            print(f"{Colors.YELLOW}{key}:{Colors.RESET} {value}")
        print(f"{Colors.CYAN}{'═' * width}{Colors.RESET}")
        print()
    
    @staticmethod
    def summary(created: int, skipped: int, total: int) -> None:
        print()
        print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}Summary{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Created:{Colors.RESET}  {Colors.BOLD}{created}{Colors.RESET} playlists")
        print(f"{Colors.DIM}⊘ Skipped:{Colors.RESET}  {Colors.DIM}{skipped}{Colors.RESET} directories")
        print(f"{Colors.CYAN}♪ Total:{Colors.RESET}    {Colors.BOLD}{total}{Colors.RESET} directories processed")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}")
        print()


AUDIO_EXTENSIONS = ['*.m4a', '*.mp3', '*.flac', '*.wav', '*.ogg']


def sanitize_name(text: str) -> str:
    text = text.replace(':', '-')
    text = re.sub(r'_{2,}', '', text)
    text = ' '.join(text.split())
    return text


def should_skip_directory(name: str) -> bool:
    return bool(re.match(r'^\[.+\]$', name))


def order_files(files: List[Path], shuffle: bool) -> List[Path]:
    if shuffle:
        result = files.copy()
        random.shuffle(result)
        return result
    return sorted(files, key=lambda f: f.name.lower())


def find_audio_files(directory: Path) -> List[Path]:
    audio_files = []
    for extension in AUDIO_EXTENSIONS:
        audio_files.extend(directory.glob(extension))
    return audio_files


def build_directory_index(root_dir: Path, directories: List[Path]) -> Dict[Path, List[int]]:
    index_map: Dict[Path, List[int]] = {}
    sibling_counter: Dict[Tuple[Path, str], int] = {}
    next_index: Dict[Path, int] = {}
    
    for current_dir in directories:
        relative = current_dir.relative_to(root_dir)
        
        if relative == Path('.'):
            index_map[current_dir] = []
            continue
        
        indices = []
        for i, part in enumerate(relative.parts):
            parent = root_dir / Path(*relative.parts[:i]) if i > 0 else root_dir
            key = (parent, part)
            
            if key not in sibling_counter:
                sibling_counter[key] = next_index.get(parent, 0)
                next_index[parent] = sibling_counter[key] + 1
            
            indices.append(sibling_counter[key])
        
        index_map[current_dir] = indices
    
    return index_map


def generate_playlist_name(root_dir: Path, current_dir: Path, index_map: Dict[Path, List[int]]) -> str:
    relative = current_dir.relative_to(root_dir)
    
    if relative == Path('.'):
        parts = [current_dir.name]
        prefix = "[00]"
    else:
        parts = list(relative.parts)
        indices = index_map.get(current_dir, [])
        prefix = '[' + '-'.join(f"{i:02d}" for i in indices) + ']'
    
    clean_parts = [sanitize_name(p) for p in parts]
    full_path = ' — '.join(clean_parts)
    
    return f"{prefix} {full_path}.m3u8"


def write_playlist_file(playlist_path: Path, audio_files: List[Path]) -> None:
    with open(playlist_path, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for audio_file in audio_files:
            f.write(f"{audio_file}\n")


def process_directory(root_dir: Path, current_dir: Path, shuffle: bool, index_map: Dict[Path, List[int]]) -> bool:
    audio_files = find_audio_files(current_dir)
    
    if not audio_files:
        Logger.dim(f"⊘ No audio files in {current_dir.name}")
        return False
    
    sorted_files = order_files(audio_files, shuffle)
    playlist_name = generate_playlist_name(root_dir, current_dir, index_map)
    playlist_path = root_dir / playlist_name
    
    Logger.info(f"Creating {Colors.BOLD}{playlist_name}{Colors.RESET}")
    Logger.dim(f"  → {len(audio_files)} tracks found")
    
    try:
        write_playlist_file(playlist_path, sorted_files)
        Logger.success(f"Saved to {Colors.BOLD}{playlist_path}{Colors.RESET}")
        print()
        return True
    except Exception as e:
        Logger.error(f"Failed to create playlist: {e}")
        print()
        return False


def create_playlists(directory: Path, recursive: bool, shuffle: bool) -> None:
    if not directory.exists():
        Logger.error(f"Directory not found: {directory}")
        sys.exit(1)
    
    if not directory.is_dir():
        Logger.error(f"Not a directory: {directory}")
        sys.exit(1)
    
    Logger.header(
        "M3U8 Playlist Generator",
        Directory=directory,
        Mode='Recursive' if recursive else 'Single Directory',
        Order='Shuffled' if shuffle else 'Sorted by name'
    )
    
    directories_to_process = []
    
    if recursive:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not should_skip_directory(d)]
            dirs.sort(key=lambda d: d.lower().replace('_', ' '))
            directories_to_process.append(Path(root))
    else:
        directories_to_process.append(directory)
    
    index_map = build_directory_index(directory, directories_to_process)
    
    created_count = 0
    skipped_count = 0
    total = len(directories_to_process)
    
    for idx, current_dir in enumerate(directories_to_process, 1):
        progress_bar = f"[{idx}/{total}]"
        print(f"{Colors.DIM}{progress_bar}{Colors.RESET}", end=" ")
        
        if process_directory(directory, current_dir, shuffle, index_map):
            created_count += 1
        else:
            skipped_count += 1
    
    Logger.summary(created_count, skipped_count, total)


def main():
    parser = argparse.ArgumentParser(
        description='Generate M3U8 playlists from directories containing audio files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'directory',
        type=str,
        help='Directory to scan for audio files'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Recursively scan subdirectories'
    )
    
    parser.add_argument(
        '-s', '--shuffle',
        action='store_true',
        help='Shuffle tracks randomly (default: sorted by name)'
    )
    
    args = parser.parse_args()
    
    try:
        create_playlists(Path(args.directory), args.recursive, args.shuffle)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Operation cancelled by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        Logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

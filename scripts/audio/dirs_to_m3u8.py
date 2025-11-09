import os
import sys
import random
import argparse
from pathlib import Path
from typing import List


class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
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


def normalize_whitespace(text: str) -> str:
    return ' '.join(text.split())


def shuffle_files(files: List[str]) -> List[str]:
    shuffled = files.copy()
    random.shuffle(shuffled)
    return shuffled


def find_audio_files(directory: Path) -> List[Path]:
    audio_files = []
    for extension in AUDIO_EXTENSIONS:
        audio_files.extend(directory.glob(extension))
    return audio_files


def generate_playlist_name(root_dir: Path, current_dir: Path) -> str:
    relative_path = current_dir.relative_to(root_dir)
    
    if relative_path == Path('.'):
        return f"{current_dir.name.upper()}.m3u8"
    
    parent_parts = relative_path.parent.parts
    prefix = ', '.join(parent_parts).replace(':', '-')
    prefix = normalize_whitespace(prefix).lower()
    
    return f"{prefix} - {current_dir.name.upper()}.m3u8"


def write_playlist_file(playlist_path: Path, audio_files: List[Path]) -> None:
    with open(playlist_path, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for audio_file in audio_files:
            f.write(f"{audio_file}\n")


def process_directory(root_dir: Path, current_dir: Path) -> bool:
    audio_files = find_audio_files(current_dir)
    
    if not audio_files:
        Logger.dim(f"⊘ No audio files in {current_dir.name}")
        return False
    
    shuffled_files = shuffle_files(audio_files)
    playlist_name = generate_playlist_name(root_dir, current_dir)
    playlist_path = root_dir / playlist_name
    
    Logger.info(f"Creating {Colors.BOLD}{playlist_name}{Colors.RESET}")
    Logger.dim(f"  → {len(audio_files)} tracks found")
    
    try:
        write_playlist_file(playlist_path, shuffled_files)
        Logger.success(f"Saved to {Colors.BOLD}{playlist_path}{Colors.RESET}")
        print()
        return True
    except Exception as e:
        Logger.error(f"Failed to create playlist: {e}")
        print()
        return False


def create_playlists(directory: Path, recursive: bool) -> None:
    if not directory.exists():
        Logger.error(f"Directory not found: {directory}")
        sys.exit(1)
    
    if not directory.is_dir():
        Logger.error(f"Not a directory: {directory}")
        sys.exit(1)
    
    Logger.header(
        "M3U8 Playlist Generator",
        Directory=directory,
        Mode='Recursive' if recursive else 'Single Directory'
    )
    
    directories_to_process = []
    
    if recursive:
        for root, dirs, files in os.walk(directory):
            directories_to_process.append(Path(root))
    else:
        directories_to_process.append(directory)
    
    created_count = 0
    skipped_count = 0
    total = len(directories_to_process)
    
    for idx, current_dir in enumerate(directories_to_process, 1):
        progress_bar = f"[{idx}/{total}]"
        print(f"{Colors.DIM}{progress_bar}{Colors.RESET}", end=" ")
        
        if process_directory(directory, current_dir):
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
    
    args = parser.parse_args()
    
    try:
        create_playlists(Path(args.directory), args.recursive)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠ Operation cancelled by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        Logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

"""
config.yaml example

- source_dir: C:/ML/ComfyUI_windows_portable/ComfyUI/models/checkpoints
  target_dir: C:/ML/a1111/models/Stable-diffusion
  match:
  - sd.1.5-*
  - sdxl.1.0-*
  include_nested: false
- source_dir: C:/ML/ComfyUI_windows_portable/ComfyUI/models/vae
  target_dir: C:/ML/a1111/models/VAE
  match:
  - "*"
  include_nested: true

"""

"""
usage:
python symlinker.py path/to/config.yaml
"""

import os
import yaml
import glob
import argparse

def remove_invalid_symlinks(target_dir):
    if not os.path.exists(target_dir):
        return
    
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.islink(item_path) and not os.path.exists(os.readlink(item_path)):
            print(f"Removing invalid symlink: {item_path}")
            os.unlink(item_path)

def create_symlinks(config_path):
    # Load YAML config
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    for entry in config:
        source_dir = os.path.abspath(entry['source_dir'])
        target_dir = os.path.abspath(entry['target_dir'])
        patterns = entry['match']
        include_nested = entry.get('include_nested', False)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        # Remove invalid symlinks before processing
        remove_invalid_symlinks(target_dir)
        
        for pattern in patterns:
            if include_nested:
                matched_files = glob.glob(os.path.join(source_dir, '**', pattern), recursive=True)
            else:
                matched_files = glob.glob(os.path.join(source_dir, pattern))
            
            for file_path in matched_files:
                file_name = os.path.basename(file_path)
                target_path = os.path.join(target_dir, file_name)
                
                if os.path.exists(target_path):
                    print(f"Skipping existing file: {target_path}")
                    continue
                
                try:
                    os.symlink(file_path, target_path)
                    print(f"Created symlink: {target_path} -> {file_path}")
                except OSError as e:
                    print(f"Failed to create symlink: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create symbolic links based on YAML config.")
    parser.add_argument("config", help="Path to the YAML configuration file.")
    args = parser.parse_args()
    
    create_symlinks(args.config)

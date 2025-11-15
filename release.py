#!/usr/bin/env python3
"""
Script to create a ZIP archive of Garage Door release files.
Compresses specified files and creates a ZIP with timestamp.
"""

import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path

def create_release_zip():
    """Creates a ZIP archive with release files."""
    
    # Working directory
    script_dir = Path.cwd()
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"garage-door-{timestamp}.zip"

    # Make the Releases directory if it doesn't exist
    releases_dir = script_dir / "Releases"
    releases_dir.mkdir(exist_ok=True)

    zip_path = script_dir / "Releases" / zip_filename
    
    print(f"Creating archive: {zip_filename}")
    print(f"Directory: {script_dir}")
    
    # List of files to include (relative paths from working directory)
    files_to_include = [
        "Xtras/BMP Import Export.x32",
        "Xtras/budapi.x32",
        "Xtras/MIX32.X32",
        "dir_data/Behavior.cst",
        "dir_data/open.swf",
        "GarageDoor.exe",
        "TextTranslator.dll",
        "translation.ini",
    ]
    
    # Create ZIP file
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # Add individual files
            for file_path in files_to_include:
                full_path = script_dir / file_path
                if full_path.exists():
                    print(f"  + {file_path}")
                    zipf.write(full_path, arcname=file_path)
                else:
                    print(f"  ? File not found: {file_path}")
            
            # Add all txt and bmp files from dir_data/patch/ (recursive)
            patch_dir = script_dir / "dir_data" / "patch"
            if patch_dir.exists():
                print(f"\n  Adding files from {patch_dir}...")
                for root, dirs, files in os.walk(patch_dir):
                    for file in files:
                        if file.lower().endswith(('.txt', '.bmp')) and file.lower() != 'log.txt':
                            file_path = Path(root) / file
                            # Relative path from script_dir
                            rel_path = file_path.relative_to(script_dir)
                            print(f"    + {rel_path}")
                            zipf.write(file_path, arcname=str(rel_path))
            else:
                print(f"  ? Directory not found: {patch_dir}")
        
        print(f"\n? Archive created successfully: {zip_path}")
        print(f"  Size: {zip_path.stat().st_size / (1024*1024):.2f} MB")
        return True
        
    except Exception as e:
        print(f"\n? Error creating archive: {e}")
        return False

if __name__ == "__main__":
    # Use the current working directory (where the script is executed from)
    print(f"Working directory: {Path.cwd()}\n")
    
    success = create_release_zip()
    sys.exit(0 if success else 1)

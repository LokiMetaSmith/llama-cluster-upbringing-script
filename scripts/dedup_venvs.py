#!/usr/bin/env python3
"""
dedup_venvs.py
Finds exact duplicate files across specified directories and replaces them with hardlinks
to save disk space. Specifically targeted at large python virtual environments.
"""

import os
import hashlib
import sys
from collections import defaultdict

def get_file_hash(filepath, blocksize=65536):
    """Calculates SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None

def find_duplicates(directories, min_size_mb=10):
    """Finds duplicate files in the given directories."""
    min_size_bytes = min_size_mb * 1024 * 1024

    # Phase 1: Group by file size to avoid hashing everything
    print(f"Phase 1: Scanning for files larger than {min_size_mb}MB...")
    size_groups = defaultdict(list)

    for directory in directories:
        if not os.path.exists(directory):
            print(f"Warning: Directory {directory} does not exist, skipping.")
            continue

        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)

                # Skip symlinks
                if os.path.islink(filepath):
                    continue

                try:
                    stat = os.stat(filepath)
                    size = stat.st_size

                    if size >= min_size_bytes:
                        size_groups[size].append(filepath)
                except OSError as e:
                    print(f"Error accessing {filepath}: {e}", file=sys.stderr)

    # Filter out sizes that only have one file
    potential_dupes = {size: paths for size, paths in size_groups.items() if len(paths) > 1}
    print(f"Found {len(potential_dupes)} size groups with potential duplicates.")

    # Phase 2: Hash files in potential duplicate groups
    print("Phase 2: Hashing potential duplicates...")
    hash_groups = defaultdict(list)

    for size, paths in potential_dupes.items():
        for path in paths:
            file_hash = get_file_hash(path)
            if file_hash:
                hash_groups[file_hash].append(path)

    # Filter out hashes that only have one file
    actual_dupes = {h: paths for h, paths in hash_groups.items() if len(paths) > 1}
    return actual_dupes

def deduplicate(duplicate_groups):
    """Replaces duplicates with hardlinks."""
    total_saved_bytes = 0
    files_linked = 0

    print("\nPhase 3: Hardlinking duplicates...")
    for file_hash, paths in duplicate_groups.items():
        # Keep the first file as the source
        source_file = paths[0]
        try:
            source_stat = os.stat(source_file)
            file_size = source_stat.st_size
        except OSError:
            continue

        for target_file in paths[1:]:
            try:
                target_stat = os.stat(target_file)

                # Verify they aren't already hardlinked
                if source_stat.st_ino == target_stat.st_ino and source_stat.st_dev == target_stat.st_dev:
                    print(f"Already hardlinked: {target_file} -> {source_file}")
                    continue

                # Replace target with hardlink to source
                # Create a temporary link first, then rename over the target for atomicity
                temp_link = target_file + ".tmp_link"
                os.link(source_file, temp_link)
                os.replace(temp_link, target_file)

                total_saved_bytes += file_size
                files_linked += 1
                print(f"Linked: {target_file} -> {source_file}")

            except Exception as e:
                print(f"Failed to link {target_file} to {source_file}: {e}", file=sys.stderr)
                # Cleanup temp file if it exists
                if os.path.exists(target_file + ".tmp_link"):
                    try:
                        os.unlink(target_file + ".tmp_link")
                    except:
                        pass

    return total_saved_bytes, files_linked

if __name__ == "__main__":
    # Directories to scan (running as sudo to access /opt)
    directories_to_scan = [
        "/opt",
        "/home/pipecatapp"
    ]

    # We only care about large files (e.g. PyTorch, CUDA libs), let's say > 5MB
    duplicates = find_duplicates(directories_to_scan, min_size_mb=5)

    saved_bytes, linked_count = deduplicate(duplicates)

    saved_mb = saved_bytes / (1024 * 1024)
    print(f"\nDone. Hardlinked {linked_count} files.")
    print(f"Total space saved: {saved_mb:.2f} MB")

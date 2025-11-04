#!/home/loki/llama-cluster-upbringing-script/venv/bin/python

import argparse
import sys
from huggingface_hub import snapshot_download

def main():
    parser = argparse.ArgumentParser(description="Download a repository from the Hugging Face Hub.")
    parser.add_argument("repo_id", type=str, help="The ID of the repository to download (e.g., 'google/embedding-gemma-300m').")
    parser.add_argument("dest", type=str, help="The destination path to download the repository to.")

    args = parser.parse_args()

    print(f"Downloading repository '{args.repo_id}' to '{args.dest}'...")

    try:
        snapshot_download(
            repo_id=args.repo_id,
            local_dir=args.dest,
            local_dir_use_symlinks=False, # Use copies to avoid symlink issues
            resume_download=True
        )
        print("Download complete.")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

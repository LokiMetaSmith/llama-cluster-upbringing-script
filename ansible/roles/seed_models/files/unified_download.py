#!/usr/bin/env python3

import argparse
import sys
import os
import subprocess
import urllib.parse
import json
import urllib.request
import ssl

def run_command(cmd, env=None):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, env=env, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        return False, result.stderr
    return True, result.stdout

def get_consul_cid(consul_key):
    """Attempt to fetch an existing IPFS CID from Consul KV."""
    try:
        # Check if the token file exists
        token = ""
        token_path = "/etc/consul.d/management_token"
        if os.path.exists(token_path):
            with open(token_path, "r") as f:
                token = f.read().strip()

        # Basic request to local consul agent
        url = f"https://127.0.0.1:8501/v1/kv/{consul_key}?raw=true"

        req = urllib.request.Request(url)
        if token:
            req.add_header("X-Consul-Token", token)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
                if response.status == 200:
                    cid = response.read().decode('utf-8').strip()
                    if cid:
                        print(f"Found existing CID in Consul for key {consul_key}: {cid}")
                        return cid
        except urllib.error.HTTPError as e:
            if e.code != 404:
                print(f"Consul HTTP error: {e.code}")
        except Exception as e:
            print(f"Error querying Consul: {e}")

    except Exception as e:
        print(f"Unexpected error getting Consul CID: {e}")

    return None

def extract_web_seeds(magnet_uri):
    """Extract web seeds (ws=) from a magnet URI."""
    parsed = urllib.parse.urlparse(magnet_uri)
    query_params = urllib.parse.parse_qs(parsed.query)
    return query_params.get('ws', [])

def download_ipfs(cid, dest_path, ipfs_path=None):
    """Download using IPFS."""
    print(f"Downloading from IPFS CID: {cid}")
    env = os.environ.copy()
    if ipfs_path:
        env["IPFS_PATH"] = ipfs_path

    cmd = ["ipfs", "get", cid, "-o", dest_path]
    success, _ = run_command(cmd, env)
    return success

def download_aria2(url, dest_dir, filename=None, is_magnet=False):
    """Download using aria2c."""
    cmd = ["aria2c", "--console-log-level=warn", "--summary-interval=0"]

    if is_magnet:
        # For magnets, just seed temporarily to fetch the file, don't keep seeding indefinitely
        cmd.extend(["--seed-time=0", "--bt-stop-timeout=300"])
    else:
        # For HTTP/FTP, use multiple connections
        cmd.extend(["-x", "16", "-s", "16", "--min-split-size=1M"])

    cmd.extend(["--dir", dest_dir])

    if filename and not is_magnet:
        # aria2c --out doesn't work well with magnets
        cmd.extend(["--out", filename])

    cmd.append(url)

    success, err = run_command(cmd)
    return success

def download_hf(repo_id, dest_dir):
    """Download a Hugging Face repo using snapshot_download."""
    print(f"Downloading Hugging Face repo: {repo_id}")
    try:
        from huggingface_hub import snapshot_download
        snapshot_download(
            repo_id=repo_id,
            local_dir=dest_dir,
            local_dir_use_symlinks=False,
            resume_download=True
        )
        return True
    except ImportError:
        print("huggingface_hub not installed. Trying to run via python module if available.")
        cmd = [sys.executable, "-c", f"from huggingface_hub import snapshot_download; snapshot_download(repo_id='{repo_id}', local_dir='{dest_dir}', local_dir_use_symlinks=False, resume_download=True)"]
        success, _ = run_command(cmd)
        return success
    except Exception as e:
        print(f"HF download failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Unified downloader for URLs, magnets, IPFS CIDs, and HF repos.")
    parser.add_argument("--uri", type=str, required=True, help="The URI to download (http, magnet, ipfs, hf).")
    parser.add_argument("--dest-dir", type=str, required=True, help="Destination directory.")
    parser.add_argument("--filename", type=str, help="Expected filename (for single file downloads).")
    parser.add_argument("--consul-key", type=str, help="Consul KV key to check for existing IPFS CID.")
    parser.add_argument("--ipfs-path", type=str, help="IPFS_PATH environment variable.")

    args = parser.parse_args()

    os.makedirs(args.dest_dir, exist_ok=True)
    dest_path = os.path.join(args.dest_dir, args.filename) if args.filename else args.dest_dir

    # Check if the target file/dir already exists and isn't empty
    if os.path.exists(dest_path):
        if os.path.isfile(dest_path) and os.path.getsize(dest_path) > 0:
            print(f"File {dest_path} already exists. Skipping download.")
            return
        elif os.path.isdir(dest_path) and len(os.listdir(dest_path)) > 0:
            print(f"Directory {dest_path} already exists and is not empty. Skipping download.")
            return

    # 1. Try local IPFS via Consul CID
    if args.consul_key:
        cid = get_consul_cid(args.consul_key)
        if cid:
            print(f"Found IPFS CID {cid} for {args.consul_key}. Trying IPFS download.")
            if download_ipfs(cid, dest_path, args.ipfs_path):
                print(f"Successfully downloaded {args.uri} via IPFS caching.")
                return
            else:
                print("IPFS local cache download failed. Falling back to URI source.")

    uri = args.uri
    success = False

    # 2. Route based on URI scheme
    if uri.startswith("magnet:"):
        print(f"Attempting magnet download: {uri}")
        success = download_aria2(uri, args.dest_dir, is_magnet=True)

        if not success:
            print("Magnet download failed or timed out.")
            web_seeds = extract_web_seeds(uri)
            if web_seeds:
                print(f"Found web seeds: {web_seeds}. Falling back to direct download.")
                for ws in web_seeds:
                    print(f"Trying web seed: {ws}")
                    if download_aria2(ws, args.dest_dir, args.filename, is_magnet=False):
                        success = True
                        break
            else:
                print("No web seeds found in magnet link.")

    elif uri.startswith("hf://"):
        repo_id = uri[5:]
        success = download_hf(repo_id, args.dest_dir)

    elif uri.startswith("ipfs://"):
        cid = uri[7:]
        success = download_ipfs(cid, dest_path, args.ipfs_path)

    elif uri.startswith("http://") or uri.startswith("https://") or uri.startswith("ftp://"):
        print(f"Attempting direct download: {uri}")
        success = download_aria2(uri, args.dest_dir, args.filename, is_magnet=False)

    else:
        print(f"Unsupported URI scheme: {uri}")
        sys.exit(1)

    if not success:
        print(f"Failed to download {uri}")
        sys.exit(1)

    print(f"Successfully downloaded {uri}")

if __name__ == "__main__":
    main()

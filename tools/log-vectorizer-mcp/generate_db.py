#!/usr/bin/env python3
import asyncio
import argparse
import sys
import os

# Import the tool from the server module
import server

def mock_get_local_embedding(text: str):
    """Returns a dummy embedding to bypass network calls."""
    return [0.0] * 768

async def main():
    parser = argparse.ArgumentParser(description="Standalone Log Vectorizer")
    parser.add_argument("log_file", help="Path to the input log file to process")
    parser.add_argument("output_db", help="Path to the output JSONL database file")

    parser.add_argument(
        "--mock-embeddings",
        action="store_true",
        help="Bypass the HTTP embedding server and generate dummy vectors (useful for testing chunking)."
    )

    parser.add_argument(
        "--embed-url",
        type=str,
        default=None,
        help="The HTTP endpoint for the embedding server (overrides LOCAL_EMBED_URL env var)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.log_file):
        print(f"Error: Input log file '{args.log_file}' does not exist.")
        sys.exit(1)

    print(f"Configuring vectorizer to write to: {args.output_db}")

    # Override the DATABASE_FILE in the server module so the tool writes to the specified location
    server.DATABASE_FILE = args.output_db

    if args.embed_url:
        print(f"Overriding embedding URL to: {args.embed_url}")
        server.LOCAL_EMBED_URL = args.embed_url

    if args.mock_embeddings:
        print("Mocking embeddings (bypassing network requests)...")
        server.get_local_embedding = mock_get_local_embedding
    else:
        print(f"Using embedding server at: {server.LOCAL_EMBED_URL}")

    # Execute the ingest_log_file logic directly
    print(f"Processing '{args.log_file}'...")
    try:
        # The underlying tool handles its own exceptions and returns a string
        result = await server.ingest_log_file(args.log_file)
        print(result)

        if "Error" in result:
            sys.exit(1)

    except Exception as e:
        print(f"Fatal error during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

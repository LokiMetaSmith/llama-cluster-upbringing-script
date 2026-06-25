#!/usr/bin/env python3
import asyncio
import argparse
import sys
import os

# Import the tool from the server module
import server

async def main():
    parser = argparse.ArgumentParser(description="Standalone Log Vectorizer")
    parser.add_argument("log_file", help="Path to the input log file to process")
    parser.add_argument("output_db", help="Path to the output JSONL database file")

    args = parser.parse_args()

    if not os.path.exists(args.log_file):
        print(f"Error: Input log file '{args.log_file}' does not exist.")
        sys.exit(1)

    print(f"Configuring vectorizer to write to: {args.output_db}")

    # Override the DATABASE_FILE in the server module so the tool writes to the specified location
    server.DATABASE_FILE = args.output_db

    # Execute the ingest_log_file logic directly
    print(f"Processing '{args.log_file}'...")
    try:
        # Check if we have an active embedding server (graceful degradation)
        # We wrap the call in a try/except, but the underlying tool handles its own exceptions and returns a string
        result = await server.ingest_log_file(args.log_file)
        print(result)

        if "Error" in result:
            sys.exit(1)

    except Exception as e:
        print(f"Fatal error during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

import os
import shutil
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class LocalFileIngestor:
    """
    Monitors an inbox directory and safely ingests files.
    Ensures that file operations are secure and prevents path traversal attacks.
    """

    def __init__(self, inbox_dir: str):
        self.inbox_dir = os.path.realpath(inbox_dir)
        os.makedirs(self.inbox_dir, exist_ok=True)
        logger.info(f"Initialized LocalFileIngestor with inbox_dir: {self.inbox_dir}")

    def is_safe_path(self, filepath: str) -> bool:
        """
        Validates if the provided filepath resolves to a location within the inbox_dir.
        Uses os.path.realpath and os.path.commonpath to prevent path traversal.
        """
        target_path = os.path.realpath(filepath)
        try:
            # Check if target_path is within self.inbox_dir
            common = os.path.commonpath([self.inbox_dir, target_path])
            return common == self.inbox_dir
        except ValueError:
            # Paths might be on different drives (on Windows)
            return False

    def ingest_file(self, filepath: str) -> bool:
        """
        Validates the path and performs ingestion if it is safe.
        This represents the ingestion process.
        """
        if not self.is_safe_path(filepath):
            logger.warning(f"Security Warning: Attempted path traversal detected for file: {filepath}")
            return False

        target_path = os.path.realpath(filepath)
        if not os.path.exists(target_path):
            logger.error(f"File not found for ingestion: {target_path}")
            return False

        logger.info(f"Safely ingested file: {target_path}")
        # Further processing would go here
        return True

    def process_inbox(self) -> list:
        """
        Scans the inbox directory for files and ingests them.
        Returns a list of successfully ingested files.
        """
        ingested_files = []
        for root, _, files in os.walk(self.inbox_dir):
            for file in files:
                filepath = os.path.join(root, file)
                if self.ingest_file(filepath):
                    ingested_files.append(filepath)

        return ingested_files

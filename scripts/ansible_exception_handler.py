#!/usr/bin/env python3
import os
import sys
import argparse
import asyncio
import logging

# Ensure absolute package imports work across un-bootstrapped environments
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "../pipecatapp")))

from pipecatapp.utils.ansible_triage import AnsibleTriageHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("AnsibleExceptionHandlerCLI")

async def main():
    parser = argparse.ArgumentParser(description="Automated Ansible Exception Handler & Git PR Loop")
    parser.add_argument("--context-dir", required=True, help="Path to temporary failure context directory")
    parser.add_argument("--task-id", required=True, help="Ansible task ID or name that failed")
    args = parser.parse_args()

    logger.info(f"Starting Ansible Triage CLI for task ID: {args.task_id}")
    logger.info(f"Failure Context Directory: {args.context_dir}")

    if not os.path.exists(args.context_dir):
        logger.error(f"Error: Context directory '{args.context_dir}' does not exist.")
        sys.exit(1)

    try:
        handler = AnsibleTriageHandler(context_dir=args.context_dir, task_id=args.task_id)
        result = await handler.run_triage()

        logger.info("====================================================================")
        logger.info("                         TRIAGE SUMMARY                             ")
        logger.info("====================================================================")
        logger.info(f"Status: {result.get('status')}")
        logger.info(f"Root Cause Analysis:\n{result.get('root_cause')}")
        logger.info(f"Upstream Modified Files: {result.get('applied_files')}")
        logger.info(f"Verification Check: {result.get('verification_status')}")

        if "pushed_url" in result:
            logger.info(f"Opengist Git Remote Push URL: {result.get('pushed_url')}")
        elif "bundle_path" in result:
            logger.info(f"Git Bundle Created (Offline Fallback): {result.get('bundle_path')}")

        if "pr_summary_path" in result:
            logger.info(f"PR Structured Markdown Saved: {result.get('pr_summary_path')}")

        logger.info("====================================================================")

        if result.get("status") == "SUCCESS":
            sys.exit(0)
        else:
            sys.exit(2)

    except Exception as e:
        logger.exception(f"Fatal error during Ansible triage processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Triage CLI interrupted by user.")
        sys.exit(130)

#!/usr/bin/env python3
"""
scripts/verify_ui_accessibility.py

An automated utility that uses Playwright to visually audit the user interface,
focus on interactive controls to verify WCAG-compliant high-contrast focus styles
(e.g., :focus-visible outlines), and capture audit screenshots for self-critique.
"""

import os
import sys
import argparse
import logging
from typing import Dict, List

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UIAccessibilityVerifier")

try:
    from playwright.sync_api import sync_playwright, Page, expect
except ImportError:
    logger.error("Playwright is not installed. Please install it using `pip install playwright`.")
    sys.exit(1)

def run_accessibility_audit(url: str, output_dir: str) -> List[str]:
    """Runs a Playwright visual & accessibility audit against the given URL.

    Args:
        url (str): The target web interface URL.
        output_dir (str): Directory where screenshots will be saved.

    Returns:
        List[str]: A list of filepaths to captured screenshots.
    """
    os.makedirs(output_dir, exist_ok=True)
    captured_paths = []

    logger.info(f"Launching headless browser to audit: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_page()

        try:
            # 1. Navigate to target
            logger.info(f"Navigating to {url}...")
            context.goto(url, timeout=10000)

            # Wait for content to render
            context.wait_for_timeout(2000)

            # 2. Capture standard page load screenshot
            std_screenshot_path = os.path.join(output_dir, "01_page_load.png")
            context.screenshot(path=std_screenshot_path)
            captured_paths.append(std_screenshot_path)
            logger.info(f"Captured standard page load screenshot: {std_screenshot_path}")

            # 3. Audit `:focus-visible` states on critical interactive elements
            # We locate buttons, links, and input boxes to verify outline focus contrast
            interactive_selectors = [
                ("input[type='text']", "02_text_input_focus.png"),
                ("button", "03_button_focus.png"),
                ("a", "04_link_focus.png"),
                ("#send-btn", "05_send_button_focus.png")
            ]

            for selector, filename in interactive_selectors:
                element = context.locator(selector).first
                if element.is_visible():
                    logger.info(f"Focusing on selector '{selector}' to audit accessibility styling...")
                    element.focus()
                    context.wait_for_timeout(500) # Wait for animation / focus outline

                    focus_screenshot_path = os.path.join(output_dir, filename)
                    element.screenshot(path=focus_screenshot_path)
                    captured_paths.append(focus_screenshot_path)
                    logger.info(f"Captured focus accessibility screenshot: {focus_screenshot_path}")
                else:
                    logger.info(f"Selector '{selector}' not visible on page. Skipping focus screenshot.")

        except Exception as e:
            logger.error(f"Error during visual audit: {e}")
        finally:
            browser.close()

    return captured_paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated UI Visual & Accessibility Verification Utility")
    parser.add_argument("--url", default="http://localhost:8000", help="Target URL of the user interface")
    parser.add_argument("--output-dir", default="/home/jules/verification", help="Directory to save audit screenshots")

    args = parser.parse_args()

    logger.info("Starting UI Visual & Accessibility Verification...")
    screenshots = run_accessibility_audit(args.url, args.output_dir)

    if screenshots:
        logger.info(f"Successfully completed UI audit. Captured {len(screenshots)} screenshots:")
        for path in screenshots:
            print(f"  - {path}")
    else:
        logger.warning("Visual audit finished with zero screenshots captured.")

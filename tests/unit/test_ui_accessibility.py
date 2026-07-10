import os
import unittest
from unittest.mock import patch, MagicMock, AsyncMock

from scripts.verify_ui_accessibility import run_accessibility_audit

class TestUIAccessibilityVerifier(unittest.TestCase):
    @patch("scripts.verify_ui_accessibility.sync_playwright")
    def test_run_accessibility_audit_successful(self, mock_sync_playwright):
        # Setup mocks
        mock_playwright_instance = MagicMock()
        mock_browser = MagicMock()
        mock_page = MagicMock()

        # Chain context returns
        mock_sync_playwright.return_value.__enter__.return_value = mock_playwright_instance
        mock_playwright_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page

        # Mock interactive elements visibility and methods
        mock_element = MagicMock()
        mock_element.is_visible.return_value = True
        mock_page.locator.return_value.first = mock_element

        # Run audit on a temporary directory
        output_dir = "test_accessibility_out"
        try:
            screenshots = run_accessibility_audit("http://localhost:8000", output_dir)

            # Assert standard screenshot and focused screenshots are captured
            self.assertEqual(len(screenshots), 5)
            self.assertIn("01_page_load.png", screenshots[0])
            self.assertIn("02_text_input_focus.png", screenshots[1])
            self.assertIn("03_button_focus.png", screenshots[2])
            self.assertIn("04_link_focus.png", screenshots[3])
            self.assertIn("05_send_button_focus.png", screenshots[4])

            # Verify page navigation and locator calls
            mock_page.goto.assert_called_once_with("http://localhost:8000", timeout=10000)
            mock_element.focus.assert_called()
            mock_element.screenshot.assert_called()

        finally:
            # Clean up temp folder files
            if os.path.exists(output_dir):
                for f in os.listdir(output_dir):
                    os.remove(os.path.join(output_dir, f))
                os.rmdir(output_dir)

if __name__ == "__main__":
    unittest.main()

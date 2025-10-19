import unittest
import requests
import time
import os

class TestPipecatApp(unittest.TestCase):
    """
    Unit tests for the Pipecat application's web server.
    These are more like integration tests as they assume the server is running.
    """

    def setUp(self):
        """Set up the base URL for the web server."""
        # Use an environment variable for the host, with a default for local testing.
        host = os.environ.get("PIPECAT_HOST", "127.0.0.1")
        self.base_url = f"http://{host}:8000"

    def test_health_check_eventually_healthy(self):
        """
        Tests that the /health endpoint eventually returns a 200 OK status.
        This test will poll the endpoint for up to 60 seconds to allow the
        application to fully initialize.
        """
        timeout = 60  # seconds
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.base_url}/health", timeout=2)
                if response.status_code == 200:
                    self.assertEqual(response.json(), {"status": "ok"})
                    return  # Test passes
            except requests.exceptions.RequestException as e:
                # It's okay to fail connection while the service is starting.
                print(f"Connection failed: {e}. Retrying...")

            time.sleep(2)

        self.fail(
            f"The /health endpoint did not return a 200 OK status within {timeout} seconds."
        )

    def test_main_page_loads(self):
        """
        Tests that the main page ('/') loads correctly and returns a 200 OK status.
        This test also waits for the health check to pass first.
        """
        try:
            self.test_health_check_eventually_healthy()
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()  # Fail on non-200 status codes
            self.assertIn("Mission Control", response.text)
        except requests.exceptions.RequestException as e:
            self.fail(f"Failed to load the main page at {self.base_url}: {e}")


if __name__ == '__main__':
    # This allows the test to be run directly, for example, in a CI/CD pipeline
    # where the server is expected to be running at localhost.
    unittest.main()
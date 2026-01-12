import unittest
import subprocess
import time
import urllib.request
import os
import shutil
import json

class TestMqttExporter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Allow configuring docker command (e.g. for sudo or podman)
        cls.docker_cmd = os.environ.get("DOCKER_CMD", "docker").split()

        # check docker availability
        try:
            subprocess.check_call(cls.docker_cmd + ["--version"])
        except (FileNotFoundError, subprocess.CalledProcessError):
            raise unittest.SkipTest("Docker not available")

    def setUp(self):
        self.network_name = "mqtt-test-net"
        self.mqtt_name = "test-mosquitto"
        self.exporter_name = "test-exporter"
        self.config_dir = "/tmp/mqtt_test_config"

        if os.path.exists(self.config_dir):
            shutil.rmtree(self.config_dir)
        os.makedirs(self.config_dir, exist_ok=True)

        with open(os.path.join(self.config_dir, "mosquitto.conf"), "w") as f:
            f.write("listener 1883\nallow_anonymous true\n")

        # Cleanup just in case
        self.cleanup()

        # Create network
        subprocess.check_call(self.docker_cmd + ["network", "create", self.network_name])

        # Start Mosquitto
        subprocess.check_call(self.docker_cmd + [
            "run", "-d", "--name", self.mqtt_name,
            "--network", self.network_name,
            "-v", f"{self.config_dir}/mosquitto.conf:/mosquitto/config/mosquitto.conf",
            "eclipse-mosquitto:2"
        ])

        # Start Exporter
        # We use the version defined in defaults if possible, but hardcoding 1.9.0 as per memory/defaults.
        # Use dynamic port for metrics to avoid conflicts
        subprocess.check_call(self.docker_cmd + [
            "run", "-d", "--name", self.exporter_name,
            "--network", self.network_name,
            "-p", "0:9000",
            "-e", "MQTT_ADDRESS=" + self.mqtt_name,
            "-e", "MQTT_PORT=1883",
            "-e", "MQTT_IGNORED_TOPICS=test/ignore",
            "-e", "PROMETHEUS_PORT=9000",
            "kpetrem/mqtt-exporter:1.9.0"
        ])

        # Get the assigned port
        # output format of `docker port container port` is usually `0.0.0.0:32768`
        port_output = subprocess.check_output(self.docker_cmd + [
            "port", self.exporter_name, "9000/tcp"
        ]).decode('utf-8').strip()

        # Extract port. It might be multiple lines, take the first.
        # e.g. 0.0.0.0:32768
        #      [::]:32768
        first_mapping = port_output.split('\n')[0]
        self.exporter_port = first_mapping.split(':')[-1]

        # Wait for startup
        time.sleep(5)

    def tearDown(self):
        self.cleanup()
        if os.path.exists(self.config_dir):
            shutil.rmtree(self.config_dir)

    def cleanup(self):
        # Use silence for cleanup
        for name in [self.exporter_name, self.mqtt_name]:
            subprocess.call(self.docker_cmd + ["rm", "-f", name], stderr=subprocess.DEVNULL)
        subprocess.call(self.docker_cmd + ["network", "rm", self.network_name], stderr=subprocess.DEVNULL)

    def test_metrics_collection(self):
        # 1. Publish metric
        subprocess.check_call(self.docker_cmd + [
            "exec", self.mqtt_name,
            "mosquitto_pub", "-h", "localhost", "-t", "test/metric", "-m", "42"
        ])

        # 2. Publish ignored metric
        subprocess.check_call(self.docker_cmd + [
            "exec", self.mqtt_name,
            "mosquitto_pub", "-h", "localhost", "-t", "test/ignore", "-m", "100"
        ])

        # Allow scrapers to update
        time.sleep(2)

        # 3. Fetch metrics
        url = f"http://localhost:{self.exporter_port}/metrics"

        metrics = ""
        for _ in range(10):
            try:
                with urllib.request.urlopen(url) as response:
                    metrics = response.read().decode('utf-8')
                    if 'mqtt_metric{topic="test_metric"}' in metrics:
                        break
            except Exception as e:
                print(f"Waiting for metrics on {url}... {e}")
            time.sleep(2)

        if not metrics:
            self.fail(f"Could not fetch metrics from {url} or empty response")

        # 4. Verify
        self.assertIn('mqtt_metric{topic="test_metric"}', metrics)
        self.assertIn("42", metrics)

        self.assertNotIn("test/ignore", metrics)
        self.assertNotIn("test_ignore", metrics)

if __name__ == '__main__':
    unittest.main()

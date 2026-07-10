import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import json
import base64

# Ensure imports work from project root, pipecatapp, tools, and utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp/tools')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp/utils')))

# Import directly from modules to bypass the package-level tools/__init__.py dependencies
from app_manager import AppManager
from external_app_manager_tool import ExternalAppManagerTool

class TestExternalAppManager(unittest.TestCase):
    def setUp(self):
        self.manager = AppManager()
        self.tool = ExternalAppManagerTool()
        self.valid_manifest = {
            "name": "my-test-app",
            "version": "1.2.3",
            "image": "my-registry/my-test-app:latest",
            "ui": {
                "title": "My Test App",
                "description": "Just a test app",
                "icon": "🐋"
            },
            "resources": {
                "cpu_mhz": 300,
                "memory_mb": 512
            },
            "env": {
                "DEBUG": "true",
                "PORT": "8080"
            },
            "network": {
                "internal_port": 8080,
                "route_public": True,
                "domain": "custom.mesh"
            },
            "storage": {
                "enabled": True,
                "mount_path": "/app/data"
            }
        }

    def test_validate_manifest_valid(self):
        is_valid, errors = self.manager.validate_manifest(self.valid_manifest)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_validate_manifest_invalid_name(self):
        invalid = self.valid_manifest.copy()
        invalid["name"] = "My_App"  # Uppercase and underscores are forbidden
        is_valid, errors = self.manager.validate_manifest(invalid)
        self.assertFalse(is_valid)
        self.assertTrue(any("name" in err for err in errors))

    def test_validate_manifest_invalid_version(self):
        invalid = self.valid_manifest.copy()
        invalid["version"] = "1.0"  # Invalid semver format
        is_valid, errors = self.manager.validate_manifest(invalid)
        self.assertFalse(is_valid)
        self.assertTrue(any("version" in err for err in errors))

    def test_validate_manifest_invalid_mount_path(self):
        invalid = self.valid_manifest.copy()
        invalid["storage"] = {
            "enabled": True,
            "mount_path": "relative/path"  # Must be absolute
        }
        is_valid, errors = self.manager.validate_manifest(invalid)
        self.assertFalse(is_valid)
        self.assertTrue(any("mount_path" in err for err in errors))

    def test_validate_manifest_privileged_forbidden(self):
        invalid = self.valid_manifest.copy()
        invalid["privileged"] = True
        is_valid, errors = self.manager.validate_manifest(invalid)
        self.assertFalse(is_valid)
        self.assertTrue(any("Privileged" in err for err in errors))

    @patch("app_manager.subprocess.check_output")
    def test_is_btrfs_supported(self, mock_output):
        # Simulated mount point exists and is btrfs
        with patch("app_manager.os.path.exists", return_value=True):
            mock_output.return_value = "btrfs\n"
            self.assertTrue(self.manager.is_btrfs_supported())

    @patch("app_manager.subprocess.check_call")
    @patch("app_manager.os.makedirs")
    @patch("app_manager.os.chmod")
    def test_provision_storage_btrfs(self, mock_chmod, mock_makedirs, mock_check_call):
        self.manager.is_btrfs_supported = MagicMock(return_value=True)
        with patch("app_manager.os.path.exists", return_value=False):
            host_path, storage_type = self.manager.provision_storage("my-test-app")
            self.assertEqual(host_path, "/btrfs_root/volumes/my-test-app")
            self.assertEqual(storage_type, "Btrfs Subvolume")
            mock_check_call.assert_any_call(["btrfs", "subvolume", "create", "/btrfs_root/volumes/my-test-app"], stdout=unittest.mock.ANY)

    def test_generate_nomad_hcl(self):
        hcl = self.manager.generate_nomad_hcl(self.valid_manifest, "/btrfs_root/volumes/my-test-app")

        # Check Job Name
        self.assertIn('job "ext-my-test-app"', hcl)
        # Check image
        self.assertIn('image = "my-registry/my-test-app:latest"', hcl)
        # Check port
        self.assertIn('to = 8080', hcl)
        # Check Traefik tags
        self.assertIn('"traefik.enable=true"', hcl)
        self.assertIn('"traefik.http.routers.ext-my-test-app.rule=Host(`my-test-app.custom.mesh`)"', hcl)
        # Check Resources
        self.assertIn('cpu    = 300', hcl)
        self.assertIn('memory = 512', hcl)
        # Check Volume Mounts
        self.assertIn('"/btrfs_root/volumes/my-test-app:/app/data"', hcl)

    @patch("requests.get")
    @patch("requests.put")
    def test_update_ouroboros_webring_register(self, mock_put, mock_get):
        # Mock fetch current members
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = [{
            "Value": base64.b64encode(json.dumps([{"name": "Existing", "url": "http://existing.mesh"}]).encode()).decode()
        }]
        mock_get.return_value = mock_get_response

        # Mock save success
        mock_put_response = MagicMock()
        mock_put_response.status_code = 200
        mock_put.return_value = mock_put_response

        success = self.manager.update_ouroboros_webring(self.valid_manifest, register=True)
        self.assertTrue(success)

        # Confirm we posted the combined members list to Consul KV
        called_args, called_kwargs = mock_put.call_args
        payload = json.loads(called_kwargs["data"])

        self.assertEqual(len(payload), 2)
        self.assertEqual(payload[0]["name"], "Existing")
        self.assertEqual(payload[1]["name"], "My Test App")
        self.assertEqual(payload[1]["url"], "http://my-test-app.custom.mesh")

    @patch("requests.post")
    @patch("app_manager.os.makedirs")
    @patch("app_manager.os.chmod")
    @patch("builtins.open", new_callable=mock_open)
    @patch("app_manager.AppManager.provision_storage")
    @patch("app_manager.AppManager.update_ouroboros_webring")
    def test_deploy_app_success(self, mock_webring, mock_provision, mock_file_open, mock_chmod, mock_makedirs, mock_post):
        mock_provision.return_value = ("/btrfs_root/volumes/my-test-app", "Btrfs Subvolume")
        mock_webring.return_value = True

        # Mock Nomad parsing success
        mock_parse_resp = MagicMock()
        mock_parse_resp.status_code = 200
        mock_parse_resp.json.return_value = {"Job": {}}

        # Mock Nomad submission success
        mock_submit_resp = MagicMock()
        mock_submit_resp.status_code = 200

        mock_post.side_effect = [mock_parse_resp, mock_submit_resp]

        success, msg = self.manager.deploy_app(self.valid_manifest)
        self.assertTrue(success)
        self.assertIn("successfully deployed", msg)

    def test_tool_scaffold_manifest(self):
        scaffolded = self.tool.scaffold_manifest(
            name="new-app",
            image="nginx:alpine",
            ui_title="New Application",
            ui_icon="⚡",
            internal_port=80,
            storage_enabled=True,
            mount_path="/usr/share/nginx/html"
        )
        parsed = json.loads(scaffolded)
        self.assertEqual(parsed["name"], "new-app")
        self.assertEqual(parsed["image"], "nginx:alpine")
        self.assertEqual(parsed["ui"]["title"], "New Application")
        self.assertEqual(parsed["ui"]["icon"], "⚡")
        self.assertEqual(parsed["network"]["internal_port"], 80)
        self.assertTrue(parsed["storage"]["enabled"])
        self.assertEqual(parsed["storage"]["mount_path"], "/usr/share/nginx/html")

if __name__ == "__main__":
    unittest.main()

import unittest
import sys
import os
import json

# Ensure imports work from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp/tools')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp/utils')))

from app_manager import AppManager
from external_app_manager_tool import ExternalAppManagerTool

class TestMeshLLMManifest(unittest.TestCase):
    def setUp(self):
        self.manager = AppManager()
        self.tool = ExternalAppManagerTool()
        self.manifest_path = "examples/external_apps/mesh_llm.json"

    def test_manifest_exists(self):
        self.assertTrue(os.path.exists(self.manifest_path), f"Manifest file {self.manifest_path} does not exist.")

    def test_manifest_valid_json(self):
        with open(self.manifest_path, "r") as f:
            try:
                data = json.load(f)
                self.assertIsInstance(data, dict)
            except Exception as e:
                self.fail(f"Manifest is not valid JSON: {e}")

    def test_manifest_validation_passes(self):
        with open(self.manifest_path, "r") as f:
            manifest_json = f.read()

        # Test validation via the ExternalAppManagerTool's validate_manifest method
        result = self.tool.validate_manifest(manifest_json)
        self.assertIn("Success", result, f"Validation failed with result: {result}")

    def test_manifest_resource_and_env_constraints(self):
        with open(self.manifest_path, "r") as f:
            data = json.load(f)

        # Core 2 Duo (8GB RAM) hardware optimization properties
        self.assertEqual(data["name"], "mesh-llm")
        self.assertLessEqual(data["resources"]["memory_mb"], 4096, "Memory allocation must be safe for 8GB nodes.")
        self.assertEqual(data["env"]["MESH_DISCOVERY_MODE"], "mdns", "Must use mdns discovery mode to avoid public STUN/Relay traffic.")
        self.assertTrue(data["storage"]["enabled"], "Storage must be enabled to save model GGUF splits.")
        self.assertEqual(data["network"]["internal_port"], 9337)
        self.assertTrue(data["network"]["route_public"])

if __name__ == "__main__":
    unittest.main()

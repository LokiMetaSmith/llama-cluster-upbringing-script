import sys
import os
import unittest

# Ensure pipecatapp is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pipecatapp')))

from security import redact_sensitive_data, sanitize_data

class TestSecurity(unittest.TestCase):
    def test_redact_sensitive_data(self):
        # Test API Key Redaction
        api_key = "sk-1234567890abcdef1234567890abcdef"
        text = f"My key is {api_key}."
        redacted = redact_sensitive_data(text)
        self.assertNotIn(api_key, redacted)
        self.assertIn("sk-[REDACTED]", redacted)

        # Test Bearer Token Redaction
        token = "abc123xyz"
        text = f"Authorization: Bearer {token}"
        redacted = redact_sensitive_data(text)
        self.assertNotIn(token, redacted)
        self.assertIn("Bearer [REDACTED]", redacted)

        # Test Safe Text
        safe = "This is a safe string."
        self.assertEqual(redact_sensitive_data(safe), safe)

        # Test Empty
        self.assertEqual(redact_sensitive_data(""), "")
        self.assertIsNone(redact_sensitive_data(None))

    def test_sanitize_data(self):
        # Test Dictionary Sanitization
        data = {
            "safe_key": "safe_value",
            "external_experts_config": {"secret": "data"},
            "tools_dict": {"ssh": "tool"},
            "twin_service": "service_obj",
            "nested": {
                "safe": "val",
                "secret_string": "Authorization: Bearer secrettoken123"
            }
        }

        sanitized = sanitize_data(data)

        # Check removed keys
        self.assertNotIn("external_experts_config", sanitized)
        self.assertNotIn("tools_dict", sanitized)
        self.assertNotIn("twin_service", sanitized)
        self.assertIn("safe_key", sanitized)

        # Check nested redaction
        self.assertIn("nested", sanitized)
        self.assertIn("Bearer [REDACTED]", sanitized["nested"]["secret_string"])
        self.assertNotIn("secrettoken123", sanitized["nested"]["secret_string"])

        # Test List Sanitization
        data_list = [
            "safe",
            "sk-1234567890abcdef1234567890abcdef",
            {"external_experts_config": "bad"}
        ]
        sanitized_list = sanitize_data(data_list)

        self.assertEqual(sanitized_list[0], "safe")
        self.assertIn("sk-[REDACTED]", sanitized_list[1])
        self.assertNotIn("external_experts_config", sanitized_list[2])

if __name__ == '__main__':
    unittest.main()

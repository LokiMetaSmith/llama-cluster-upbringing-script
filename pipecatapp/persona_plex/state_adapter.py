import json
import xml.etree.ElementTree as ET

class StateAdapter:
    def __init__(self):
        pass

    def flatten_state(self, state_data):
        """
        Flattens XML/JSON tabletop states into dense natural language strings
        for PersonaPlex's text-conditioning channel.
        """
        if isinstance(state_data, str):
            try:
                # Try parsing as JSON first
                parsed_data = json.loads(state_data)
                return self._flatten_json(parsed_data)
            except json.JSONDecodeError:
                try:
                    # Try parsing as XML
                    root = ET.fromstring(state_data)
                    return self._flatten_xml(root)
                except ET.ParseError:
                    return state_data # Return as is if neither JSON nor XML
        elif isinstance(state_data, dict):
            return self._flatten_json(state_data)

        return str(state_data)

    def _flatten_json(self, data):
        if not data:
            return ""

        parts = []
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    parts.append(f"{key}: {self._flatten_json(value)}")
                else:
                    parts.append(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                parts.append(self._flatten_json(item))
        else:
            return str(data)

        return ". ".join(parts)

    def _flatten_xml(self, root):
        parts = []

        # Add root tag and text if present
        text = root.text.strip() if root.text else ""
        if text:
            parts.append(f"{root.tag}: {text}")
        elif not list(root):
            parts.append(f"{root.tag}")

        # Process attributes
        for key, value in root.attrib.items():
            parts.append(f"{key}: {value}")

        # Process children recursively
        for child in root:
            child_text = self._flatten_xml(child)
            if child_text:
                if not child.text or not child.text.strip():
                   parts.append(f"{child.tag}: {child_text}")
                else:
                   parts.append(child_text)

        return ". ".join(parts)

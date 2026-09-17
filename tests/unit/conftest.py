import sys
from unittest.mock import MagicMock

# Mock minisweagent before any tests are collected
sys.modules['minisweagent'] = MagicMock()
sys.modules['minisweagent.agents'] = MagicMock()
sys.modules['minisweagent.agents.default'] = MagicMock()

# Re-inject missing heavy mocks
sys.modules['torch'] = MagicMock()
sys.modules['torch'].__version__ = '2.14.0+cu130'

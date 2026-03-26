import sys
from unittest.mock import MagicMock
mock_modules = [
    "pipecat", "pipecat.services", "pipecat.services.openai", "pipecat.services.openai.llm", "consul", "consul.aio"
]
for mod_name in mock_modules:
    sys.modules[mod_name] = MagicMock()

import tests.test_emperor_node
import asyncio
asyncio.run(tests.test_emperor_node.test_emperor_node())

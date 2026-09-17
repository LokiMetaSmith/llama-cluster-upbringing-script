import sys
from unittest.mock import MagicMock

sys.modules['minisweagent'] = MagicMock()
sys.modules['minisweagent.agents'] = MagicMock()
sys.modules['minisweagent.agents.default'] = MagicMock()
sys.modules['minisweagent.environments'] = MagicMock()
sys.modules['minisweagent.environments.local'] = MagicMock()
sys.modules['minisweagent.environments.docker'] = MagicMock()
sys.modules['minisweagent.models'] = MagicMock()
sys.modules['minisweagent.models.litellm_model'] = MagicMock()

# Do NOT mock torch. The issue is that missing __spec__ breaks sentence-transformers/transformers.
# We will just rely on the installed packages instead.

"""Root-level import bridge for pipecatapp.swarm_orchestrator."""

import sys

import pipecatapp.swarm_orchestrator as _impl

sys.modules[__name__] = _impl

from typing import Dict, Any, List
import json
import logging
import random
import asyncio

from ..node import Node
from .registry import registry
from ..context import WorkflowContext

logger = logging.getLogger(__name__)

@registry.register
class ReservoirSubstrateNode(Node):
    """
    Emulates a continuous, dynamical physical substrate (e.g. an optical or neuromorphic medium).
    It acts as a 'reservoir' where inputs create a branched flow or interference pattern.
    The continuous state represents structural, holographic memory that is tuned over time.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.expected_inputs = ["input_signal", "hdl_modulation"]
        self.expected_outputs = ["activation_matrix", "collimated_output"]

    async def execute(self, context: WorkflowContext) -> None:
        input_signal = self.get_input(context, "input_signal")
        hdl_modulation = self.get_input(context, "hdl_modulation")

        # In a real physical emulation, this would translate Morpho HDL
        # into thickness variations of a simulated optical medium.
        # Here we mock the behavior of a high-dimensional continuous interference pattern.

        logger.info(f"ReservoirSubstrateNode: Injecting signal into virtual medium. Signal size: {len(str(input_signal))}")

        # Apply hdl_modulation to tune the "correlation length" of the disordered potential
        modulation_strength = 0.5
        if hdl_modulation:
            logger.info("Applying Morpho HDL modulation to substrate structural parameters.")
            modulation_strength = 0.8

        # Emulate the continuous branched flow / activation matrix
        # (Mocking a high-dimensional state tensor)
        activation_matrix = {
            "dimensions": [128, 128],
            "correlation_length": modulation_strength,
            "branches": random.randint(5, 20),
            "substrate_state": "focused" if modulation_strength > 0.6 else "scattered"
        }

        # The 'collimated output' represents the focused signal extracting the answer or routing path
        collimated_output = f"Holographic output extracted from {activation_matrix['branches']} branches."

        self.set_output(context, "activation_matrix", activation_matrix)
        self.set_output(context, "collimated_output", collimated_output)

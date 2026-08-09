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

@registry.register
class ReservoirBenchmarkNode(Node):
    """
    Benchmarks the quality and efficiency of a generated activation matrix.
    Evaluates collimation efficiency, branch reduction, memory capacity, and energy cost.
    Useful for iterative optimization loops where the agent refines HDL modulation.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.expected_inputs = ["activation_matrix"]
        self.expected_outputs = ["benchmark_results"]

    async def execute(self, context: WorkflowContext) -> None:
        activation_matrix = self.get_input(context, "activation_matrix")

        if not activation_matrix:
            raise ValueError("ReservoirBenchmarkNode requires an 'activation_matrix' input.")

        logger.info(f"ReservoirBenchmarkNode: Evaluating matrix with {activation_matrix.get('branches', 0)} branches.")

        # Calculate simulated physical metrics based on the matrix state
        correlation_length = activation_matrix.get("correlation_length", 0.5)
        branches = activation_matrix.get("branches", 15)
        substrate_state = activation_matrix.get("substrate_state", "scattered")

        # Collimation Efficiency / Signal-to-Noise Ratio (SNR)
        # Higher correlation length generally leads to better focusing.
        base_collimation = correlation_length * 100
        snr_penalty = 0 if substrate_state == "focused" else 30
        collimation_efficiency = max(0, min(100, base_collimation - snr_penalty))

        # Branch Reduction Rate
        # Fewer branches means a more streamlined, high-intensity pathway.
        # Assume a baseline of 20 branches for a totally unoptimized state.
        branch_reduction_rate = max(0, min(100, ((20 - branches) / 20) * 100))

        # Memory Capacity (MC)
        # A standard reservoir metric; assume standard matrix size gives base capacity,
        # tuned slightly by correlation length.
        dims = activation_matrix.get("dimensions", [128, 128])
        memory_capacity = (dims[0] * dims[1]) / 1000 * correlation_length

        # Modulation Energy Cost
        # Penalizes overly complex instructions. High correlation length implies more
        # "force" applied to the medium.
        energy_cost = correlation_length * 50

        # Calculate an overall composite score (0-100)
        overall_score = (collimation_efficiency * 0.5) + (branch_reduction_rate * 0.3) - (energy_cost * 0.1)
        overall_score = max(0, min(100, overall_score))

        benchmark_results = {
            "collimation_efficiency_snr": round(collimation_efficiency, 2),
            "branch_reduction_rate": round(branch_reduction_rate, 2),
            "memory_capacity": round(memory_capacity, 2),
            "modulation_energy_cost": round(energy_cost, 2),
            "overall_score": round(overall_score, 2),
            "passed": overall_score > 60.0 # Agent can use this boolean for fast logic routing
        }

        logger.info(f"ReservoirBenchmarkNode Results: Score {benchmark_results['overall_score']}, Passed: {benchmark_results['passed']}")

        self.set_output(context, "benchmark_results", benchmark_results)


@registry.register
class HolographicRouterNode(Node):
    """
    Emulates routing a user query through a pre-optimized structural memory matrix.
    Uses the "branched flow" pattern to deterministically select the correct expert/pathway.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.expected_inputs = ["user_query", "recalled_matrix"]
        self.expected_outputs = ["selected_expert"]

    async def execute(self, context: WorkflowContext) -> None:
        user_query = self.get_input(context, "user_query")
        recalled_matrix = self.get_input(context, "recalled_matrix")

        if not user_query or not recalled_matrix:
            raise ValueError("HolographicRouterNode requires 'user_query' and 'recalled_matrix'.")

        logger.info("HolographicRouterNode: Propagating query through structurally encoded branched flow.")

        # Emulate the physical routing process
        # A matrix with high correlation length (well-optimized) routes cleanly.
        # A scattered matrix might route unpredictably.

        matrix_data = recalled_matrix.get("matrix_data", {})
        substrate_state = matrix_data.get("substrate_state", "scattered")
        desc = recalled_matrix.get("context_description", "").lower()

        # In a real MoE emulation, the branches would collapse to a vector corresponding to an expert.
        # We mock this by scanning the description for known expert types if the matrix is focused.
        selected_expert = "general_fallback"

        if substrate_state == "focused":
            if "python" in desc or "code" in desc:
                selected_expert = "coding_expert"
            elif "math" in desc:
                selected_expert = "math_expert"
            else:
                selected_expert = "specialized_expert"

        logger.info(f"HolographicRouterNode: Signal collimated to '{selected_expert}'.")
        self.set_output(context, "selected_expert", selected_expert)

import torch
from typing import List, Tuple, Any

class JacobianLensTool:
    """
    A tool implementing the Jacobian Lens (J-Lens) interpretability technique.
    Provides methods for reading J-space contents (vocabulary projections)
    and writing interventions (Coordinate Swaps, Logit-Weighted Ablations,
    and Logit-Weighted Enhancements) as detailed in the publication
    'Verbalizable Representations Form a Global Workspace in Language Models' (2026).
    """

    def __init__(self):
        self.name = "jacobian_lens"

    def get_j_matrix(self, model: Any, layer_idx: int) -> torch.Tensor:
        """
        Retrieves the average Jacobian matrix J_l for the given layer.
        """
        if hasattr(model, "J_layers") and model.J_layers is not None:
            if isinstance(model.J_layers, dict):
                return model.J_layers[layer_idx]
            elif isinstance(model.J_layers, list):
                return model.J_layers[layer_idx]
        if hasattr(model, "get_j_matrix"):
            return model.get_j_matrix(layer_idx)
        raise ValueError(f"Model does not provide J_l matrix for layer {layer_idx}")

    def get_unembedding(self, model: Any) -> torch.Tensor:
        """
        Retrieves the unembedding matrix W_U from the model.
        """
        if hasattr(model, "W_U") and model.W_U is not None:
            return model.W_U
        if hasattr(model, "get_unembedding"):
            return model.get_unembedding()
        if hasattr(model, "unembedding") and hasattr(model.unembedding, "weight"):
            return model.unembedding.weight
        if hasattr(model, "lm_head") and hasattr(model.lm_head, "weight"):
            return model.lm_head.weight
        raise ValueError("Model does not provide W_U (unembedding) matrix")

    def get_jlens_vectors(self, model: Any, layer_idx: int) -> torch.Tensor:
        """
        Computes the Jacobian lens (J-lens) vectors at layer l.
        J-lens vectors are the rows of W_U * J_l.
        Shape: [vocab_size, d_model]
        """
        W_U = self.get_unembedding(model)
        J_l = self.get_j_matrix(model, layer_idx)
        return torch.matmul(W_U, J_l)

    def read_top_tokens(self, model: Any, layer_idx: int, activation: torch.Tensor, k: int = 10) -> List[Tuple[int, float]]:
        """
        Reads the top k vocabulary tokens for a given intermediate activation.
        Computes the projection of activation onto J-lens vectors: logits = (W_U * J_l) * activation.

        Args:
            model: The model containing W_U and J_l.
            layer_idx: The layer to read from.
            activation: Activation tensor of shape [d_model].
            k: The number of top tokens to return.

        Returns:
            A list of (token_id, logit_value) sorted descending by logit value.
        """
        jlens_vectors = self.get_jlens_vectors(model, layer_idx)  # [vocab_size, d_model]
        logits = torch.matmul(jlens_vectors, activation)  # [vocab_size]
        values, indices = torch.topk(logits, k)
        return [(idx.item(), val.item()) for val, idx in zip(values, indices)]

    def swap_token_coordinate(self, model: Any, layer_idx: int, activation_1: torch.Tensor, activation_2: torch.Tensor, token_id: int) -> torch.Tensor:
        """
        Performs Coordinate Swap (Inter-Context Intervention).
        Swaps the coordinate of a specific token_id between two activations.

        Formulation:
            v_norm = v_token / ||v_token||_2
            c1 = activation_1 * v_norm
            c2 = activation_2 * v_norm
            x_prime = activation_1 + (c2 - c1) * v_norm
        """
        jlens_vectors = self.get_jlens_vectors(model, layer_idx)  # [vocab_size, d_model]
        v_token = jlens_vectors[token_id]  # [d_model]

        norm_v = torch.norm(v_token, p=2)
        if norm_v == 0:
            return activation_1.clone()

        v_norm = v_token / norm_v
        c1 = torch.dot(activation_1, v_norm)
        c2 = torch.dot(activation_2, v_norm)

        return activation_1 + (c2 - c1) * v_norm

    def ablate_top_k_tokens(self, model: Any, layer_idx: int, activation: torch.Tensor, k: int) -> torch.Tensor:
        """
        Performs Logit-Weighted Ablation.
        Ablates the projection of the activation onto a weighted direction
        constructed from the top-k active J-lens token vectors.

        Formulation:
            v_ablate = sum_{i in TopK} logit_i * v_i
            v_ablate_norm = v_ablate / ||v_ablate||_2
            x_prime = activation - (activation^T * v_ablate_norm) * v_ablate_norm
        """
        jlens_vectors = self.get_jlens_vectors(model, layer_idx)  # [vocab_size, d_model]
        logits = torch.matmul(jlens_vectors, activation)  # [vocab_size]

        values, indices = torch.topk(logits, k)

        v_ablate = torch.zeros_like(jlens_vectors[0])
        for weight, idx in zip(values, indices):
            v_ablate += weight * jlens_vectors[idx]

        norm_v = torch.norm(v_ablate, p=2)
        if norm_v == 0:
            return activation.clone()

        v_ablate_norm = v_ablate / norm_v
        projection_scalar = torch.dot(activation, v_ablate_norm)

        return activation - projection_scalar * v_ablate_norm

    def enhance_top_k_tokens(self, model: Any, layer_idx: int, activation: torch.Tensor, k: int, scale_factor: float) -> torch.Tensor:
        """
        Performs Logit-Weighted Enhancement (Steering Addition).
        Calculates the weighted direction vector v_enhance using the exact same logit-weighted
        linear combination as the ablation method, and applies the steering vector additively,
        controlled by the scale_factor (alpha).

        Formulation:
            v_enhance = sum_{i in TopK} logit_i * v_i
            v_enhance_norm = v_enhance / ||v_enhance||_2
            x_prime = activation + alpha * v_enhance_norm
        """
        jlens_vectors = self.get_jlens_vectors(model, layer_idx)  # [vocab_size, d_model]
        logits = torch.matmul(jlens_vectors, activation)  # [vocab_size]

        values, indices = torch.topk(logits, k)

        v_enhance = torch.zeros_like(jlens_vectors[0])
        for weight, idx in zip(values, indices):
            v_enhance += weight * jlens_vectors[idx]

        norm_v = torch.norm(v_enhance, p=2)
        if norm_v == 0:
            return activation.clone()

        v_enhance_norm = v_enhance / norm_v

        return activation + scale_factor * v_enhance_norm

# Top-level functional interfaces requested in instructions
def swap_token_coordinate(model: Any, layer_idx: int, activation_1: torch.Tensor, activation_2: torch.Tensor, token_id: int) -> torch.Tensor:
    tool = JacobianLensTool()
    return tool.swap_token_coordinate(model, layer_idx, activation_1, activation_2, token_id)

def ablate_top_k_tokens(model: Any, layer_idx: int, activation: torch.Tensor, k: int) -> torch.Tensor:
    tool = JacobianLensTool()
    return tool.ablate_top_k_tokens(model, layer_idx, activation, k)

def enhance_top_k_tokens(model: Any, layer_idx: int, activation: torch.Tensor, k: int, scale_factor: float) -> torch.Tensor:
    tool = JacobianLensTool()
    return tool.enhance_top_k_tokens(model, layer_idx, activation, k, scale_factor)

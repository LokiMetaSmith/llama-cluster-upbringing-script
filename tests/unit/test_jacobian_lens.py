import torch
import pytest
from pipecatapp.tools.jacobian_lens_tool import JacobianLensTool, swap_token_coordinate, ablate_top_k_tokens

class MockModel:
    """A mock transformer model supplying a custom W_U (unembedding) and J_layers."""
    def __init__(self, vocab_size: int, d_model: int):
        # We can construct dummy matrices
        self.W_U = torch.randn(vocab_size, d_model)
        self.J_layers = {
            1: torch.randn(d_model, d_model),
            2: torch.randn(d_model, d_model)
        }

def test_jlens_vectors():
    vocab_size = 10
    d_model = 8
    model = MockModel(vocab_size, d_model)
    tool = JacobianLensTool()

    jlens_vectors = tool.get_jlens_vectors(model, 1)

    assert jlens_vectors.shape == (vocab_size, d_model)
    # W_U * J_l matrix multiplication check
    expected = torch.matmul(model.W_U, model.J_layers[1])
    assert torch.allclose(jlens_vectors, expected)

def test_read_top_tokens():
    vocab_size = 5
    d_model = 4
    model = MockModel(vocab_size, d_model)
    tool = JacobianLensTool()

    activation = torch.randn(d_model)

    # We want to verify read_top_tokens returns sorted (token_id, value)
    top_k = 3
    results = tool.read_top_tokens(model, 1, activation, k=top_k)

    assert len(results) == top_k
    # Values should be sorted in descending order
    for i in range(len(results) - 1):
        assert results[i][1] >= results[i+1][1]

def test_swap_token_coordinate():
    vocab_size = 10
    d_model = 8
    model = MockModel(vocab_size, d_model)
    tool = JacobianLensTool()

    activation_1 = torch.randn(d_model)
    activation_2 = torch.randn(d_model)
    token_id = 3

    # Perform coordinate swap using both tool class and functional wrapper
    x_prime_tool = tool.swap_token_coordinate(model, 1, activation_1, activation_2, token_id)
    x_prime_func = swap_token_coordinate(model, 1, activation_1, activation_2, token_id)

    # Verify both methods match
    assert torch.allclose(x_prime_tool, x_prime_func)

    # Math verification:
    jlens_vectors = tool.get_jlens_vectors(model, 1)
    v_token = jlens_vectors[token_id]
    v_norm = v_token / torch.norm(v_token, p=2)

    # Check that the coordinate of x_prime along v_norm is equal to activation_2's coordinate along v_norm
    coord_1 = torch.dot(activation_1, v_norm)
    coord_2 = torch.dot(activation_2, v_norm)
    coord_prime = torch.dot(x_prime_tool, v_norm)

    assert torch.allclose(coord_prime, coord_2, atol=1e-5)

    # Check that orthogonal components remain identical
    orthogonal_component_1 = activation_1 - coord_1 * v_norm
    orthogonal_component_prime = x_prime_tool - coord_prime * v_norm

    assert torch.allclose(orthogonal_component_prime, orthogonal_component_1, atol=1e-5)

def test_ablate_top_k_tokens():
    vocab_size = 15
    d_model = 12
    model = MockModel(vocab_size, d_model)
    tool = JacobianLensTool()

    activation = torch.randn(d_model)
    k = 5

    # Perform logit-weighted ablation using tool and functional wrapper
    x_prime_tool = tool.ablate_top_k_tokens(model, 1, activation, k=k)
    x_prime_func = ablate_top_k_tokens(model, 1, activation, k=k)

    # Verify both methods match
    assert torch.allclose(x_prime_tool, x_prime_func)

    # Math verification:
    jlens_vectors = tool.get_jlens_vectors(model, 1)
    logits = torch.matmul(jlens_vectors, activation)
    values, indices = torch.topk(logits, k)

    v_ablate = torch.zeros_like(jlens_vectors[0])
    for weight, idx in zip(values, indices):
        v_ablate += weight * jlens_vectors[idx]

    v_ablate_norm = v_ablate / torch.norm(v_ablate, p=2)

    # The projected/ablated output vector x_prime should be orthogonal to v_ablate_norm
    dot_product = torch.dot(x_prime_tool, v_ablate_norm)
    assert abs(dot_product.item()) < 1e-5

    # The output x_prime should equal the input minus its projection along v_ablate_norm
    expected_x_prime = activation - torch.dot(activation, v_ablate_norm) * v_ablate_norm
    assert torch.allclose(x_prime_tool, expected_x_prime, atol=1e-5)

def test_edge_cases():
    vocab_size = 5
    d_model = 4
    model = MockModel(vocab_size, d_model)
    tool = JacobianLensTool()

    # Zero vector coordinate swap or zero token vector should handle zero smoothly
    # Mocking W_U or J_l to produce zero vector at a token
    model.W_U = torch.zeros_like(model.W_U)
    activation_1 = torch.randn(d_model)
    activation_2 = torch.randn(d_model)

    # Should not throw DivisionByZero and should return activation_1 unchanged
    x_prime_swap = tool.swap_token_coordinate(model, 1, activation_1, activation_2, 1)
    assert torch.allclose(x_prime_swap, activation_1)

    x_prime_ablate = tool.ablate_top_k_tokens(model, 1, activation_1, k=2)
    assert torch.allclose(x_prime_ablate, activation_1)

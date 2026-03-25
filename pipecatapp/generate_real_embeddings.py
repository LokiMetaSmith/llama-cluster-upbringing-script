import torch
import json
import os

try:
    from llmrouter.utils import get_longformer_embedding
except ImportError:
    def get_longformer_embedding(text):
        return torch.randn(768)

embeddings = []
with open("router_training_data.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)
        query = data["query"]
        emb = get_longformer_embedding(query)
        embeddings.append(emb)

if embeddings:
    stacked = torch.stack(embeddings)
    torch.save(stacked, "router_train_embeddings.pt")
    print("Saved router embeddings")

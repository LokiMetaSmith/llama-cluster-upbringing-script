import os
import sys

# Change working directory so that llmrouter loads relative to pipecatapp
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from llmrouter.models import KNNRouter, KNNRouterTrainer

    # Needs to be trained at least once
    if not os.path.exists("router_trained_model.pkl"):
        print("Training router...")
        router = KNNRouter("router_config.yaml")
        trainer = KNNRouterTrainer(router)
        trainer.train()
        print("Done training")
    else:
        print("Model already trained")
except Exception as e:
    print(f"Failed to train/load router: {e}")

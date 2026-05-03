import os
import time
from syncthing_manager import SyncthingNode

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Initialize nodes
    node_a = SyncthingNode("A_Seeder", 8384, 22000, base_dir)
    node_b = SyncthingNode("B_Leecher", 8385, 22001, base_dir)

    node_a.generate_config()
    node_b.generate_config()

    node_a.start()
    node_b.start()

    try:
        # Pair nodes
        node_a.add_device(node_b.device_id, "127.0.0.1:22001")
        node_b.add_device(node_a.device_id, "127.0.0.1:22000")

        # Share folder
        folder_id = "models_gguf"
        path_a = os.path.join(node_a.home_dir, "shared_models")
        path_b = os.path.join(node_b.home_dir, "shared_models")

        node_a.share_folder(folder_id, path_a, node_b.device_id, type="sendreceive")
        node_b.share_folder(folder_id, path_b, node_a.device_id, type="sendreceive")

        print("\n--- Setup Complete. Creating a mock model file on Node A... ---")

        # Create a large dummy file on Node A
        dummy_model_path = os.path.join(path_a, "llama-3-8b-instruct.Q4_K_M.gguf")
        with open(dummy_model_path, "wb") as f:
            f.write(os.urandom(1024 * 1024 * 5)) # Reduced to 5MB to prevent timeouts in sandbox

        print(f"Created 5MB dummy model at {dummy_model_path}")
        print("Waiting for Node B to detect and download the file via P2P...")

        # Monitor Node B's sync progress
        target_file_b = os.path.join(path_b, "llama-3-8b-instruct.Q4_K_M.gguf")
        timeout_loops = 0
        while not os.path.exists(target_file_b) or os.path.getsize(target_file_b) < (1024 * 1024 * 5):
            completion = node_b.get_completion(node_a.device_id, folder_id)
            print(f"[Node B] Sync progress: {completion:.2f}%")
            time.sleep(2)
            timeout_loops += 1
            if timeout_loops > 10:
                print("Timeout waiting for sync...")
                break

        if os.path.exists(target_file_b):
            print("\n✅ Sync Complete! Node B successfully leeched the model file.")
            print(f"File exists on Node B at: {target_file_b}")
            print(f"Size on Node B: {os.path.getsize(target_file_b) / (1024*1024):.2f} MB")

    finally:
        print("\nCleaning up...")
        node_a.stop()
        node_b.stop()

if __name__ == "__main__":
    main()

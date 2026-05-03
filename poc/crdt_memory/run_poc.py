import y_py as Y
import json

def print_doc(name, map_obj):
    print(f"\n--- {name} State ---")
    # y-py to_json() returns a string, so we parse it to print it nicely
    parsed = json.loads(map_obj.to_json())
    print(json.dumps(parsed, indent=2))

def main():
    print("Initializing base CRDT Agent Memory Document using y-py...")

    # Create the initial Y.Doc
    base_doc = Y.YDoc()
    base_map = base_doc.get_map("state")

    # Initialize the state inside a transaction
    with base_doc.begin_transaction() as tx:
        # Initial structures
        conversation = Y.YArray([{"role": "system", "content": "You are a helpful AI assistant."}])
        base_map.set(tx, "conversation", conversation)

        metadata = Y.YMap({"active_node": "node-01", "tools_running": 0})
        base_map.set(tx, "metadata", metadata)

    print_doc("Base Document", base_map)

    # Simulate a network split:
    # Extract the binary state of the base document and create two independent copies.
    binary_state = Y.encode_state_as_update(base_doc)

    node_a_doc = Y.YDoc()
    Y.apply_update(node_a_doc, binary_state)
    node_a_map = node_a_doc.get_map("state")

    node_b_doc = Y.YDoc()
    Y.apply_update(node_b_doc, binary_state)
    node_b_map = node_b_doc.get_map("state")

    print("\n[Simulating Network Split / Concurrent Execution]")

    # Node A: The agent generates a new message in the conversation
    print("Node A: Agent appending a new message to the conversation...")
    with node_a_doc.begin_transaction() as tx:
        conversation_a = node_a_map.get("conversation")
        # Notice we append the dict directly, not a list of dicts, to avoid nesting arrays
        conversation_a.append(tx, {"role": "user", "content": "What is the capital of France?"})

    # Node B: A background task updates the metadata (e.g., tool execution finished)
    print("Node B: Background task updating metadata...")
    with node_b_doc.begin_transaction() as tx:
        metadata_b = node_b_map.get("metadata")
        metadata_b.set(tx, "active_node", "node-02")
        metadata_b.set(tx, "tools_running", 1)

    print_doc("Node A (Message Added)", node_a_map)
    print_doc("Node B (Metadata Updated)", node_b_map)

    # Reconnection: Merge the states
    # Extract the updates from Node B and apply them to Node A
    print("\n[Reconnection: Merging Node B into Node A]")

    # Get the delta: what does B have that A doesn't?
    state_vector_a = Y.encode_state_vector(node_a_doc)
    update_from_b = Y.encode_state_as_update(node_b_doc, state_vector_a)

    # Apply B's delta to A
    Y.apply_update(node_a_doc, update_from_b)

    print_doc("Final Merged Document", node_a_map)
    print("\nSuccess: Both the appended message and the mutated metadata survived the concurrent edit!")

if __name__ == "__main__":
    main()

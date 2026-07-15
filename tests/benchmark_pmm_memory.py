import os
import time
import random
from pipecatapp.pmm_memory import PMMMemory

def generate_items(num_items, start_id=0, prefix="item_"):
    items = []
    now = time.time()
    for i in range(num_items):
        item_id = f"{prefix}{start_id + i}"
        items.append({
            'id': item_id,
            'title': f"Task {item_id}",
            'status': random.choice(['open', 'in_progress', 'completed']),
            'assignee_id': f"agent_{random.randint(1, 10)}",
            'created_by': "manager_1",
            'created_at': now - random.randint(1000, 5000),
            'updated_at': now - random.randint(100, 500),
            'parent_id': None,
            'meta': {'priority': random.choice(['low', 'medium', 'high'])},
            'validation_results': {'passed': True}
        })
    return items

def run_benchmark():
    db_path = "benchmark_pmm_memory.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    memory = PMMMemory(db_path=db_path)

    # Generate 1000 items
    num_items = 1000
    items = generate_items(num_items)

    print(f"--- Running sync_work_items_sync benchmark with {num_items} items ---")

    # Measure Inserts
    start_insert = time.time()
    inserted_items = memory.sync_work_items_sync(items)
    end_insert = time.time()
    insert_duration = end_insert - start_insert
    print(f"Time taken to INSERT {num_items} items: {insert_duration:.4f} seconds")
    print(f"Inserted items count: {len(inserted_items)}")

    # Update half of the items (making their updated_at larger)
    updated_items_input = []
    for item in items[:500]:
        updated_item = item.copy()
        updated_item['updated_at'] = time.time() + 10.0 # definitely newer
        updated_item['title'] = f"Updated title for {item['id']}"
        updated_items_input.append(updated_item)

    # Keep the other half unchanged (or with older updated_at)
    for item in items[500:]:
        old_item = item.copy()
        old_item['updated_at'] = item['updated_at'] - 10.0 # definitely older, should not update
        updated_items_input.append(old_item)

    # Measure Updates/Skips
    start_update = time.time()
    merged_items = memory.sync_work_items_sync(updated_items_input)
    end_update = time.time()
    update_duration = end_update - start_update
    print(f"Time taken to UPDATE/SKIP {num_items} items: {update_duration:.4f} seconds")
    print(f"Merged (updated) items count (expected 500): {len(merged_items)}")

    # Cleanup
    memory.close()
    if os.path.exists(db_path):
        os.remove(db_path)

if __name__ == "__main__":
    run_benchmark()

#!/usr/bin/env python3
import asyncio
import aiohttp
import argparse
import time
from collections import Counter
import sys

async def fetch(session, url, headers):
    try:
        async with session.get(url, headers=headers, timeout=5) as response:
            text = await response.text()
            if response.status == 200:
                return text.strip()
            else:
                return f"Error: HTTP {response.status}"
    except Exception as e:
        return f"Exception: {type(e).__name__}"

async def main(target_url, num_requests, concurrency, host_header):
    print(f"Starting stress test against {target_url}...")
    print(f"Requests: {num_requests}, Concurrency: {concurrency}")
    if host_header:
        print(f"Host Header: {host_header}")

    headers = {"Host": host_header} if host_header else {}
    start_time = time.time()

    responses = []

    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for _ in range(num_requests):
            tasks.append(asyncio.ensure_future(fetch(session, target_url, headers)))

        responses = await asyncio.gather(*tasks)

    duration = time.time() - start_time

    # Parse results
    successes = 0
    failures = 0
    nodes = Counter()
    allocations = Counter()
    errors = Counter()

    for r in responses:
        if r.startswith("Node:"):
            successes += 1
            # Expected format: "Node: <node_id> | Alloc: <alloc_id>"
            parts = r.split("|")
            if len(parts) == 2:
                node_part = parts[0].replace("Node:", "").strip()
                alloc_part = parts[1].replace("Alloc:", "").strip()
                nodes[node_part] += 1
                allocations[alloc_part] += 1
            else:
                nodes["unknown_format"] += 1
        else:
            failures += 1
            errors[r] += 1

    print("\n" + "="*40)
    print("STRESS TEST RESULTS")
    print("="*40)
    print(f"Total Requests:      {num_requests}")
    print(f"Concurrency:         {concurrency}")
    print(f"Duration:            {duration:.2f} seconds")
    print(f"Requests/sec:        {num_requests/duration:.2f}")
    print(f"Successful Requests: {successes}")
    print(f"Failed Requests:     {failures}")

    print("\nLoad Distribution by Node:")
    print("-" * 25)
    for node, count in nodes.most_common():
        percentage = (count / successes * 100) if successes > 0 else 0
        print(f"{node:<20} {count:>5} ({percentage:>5.1f}%)")

    print("\nLoad Distribution by Allocation (Container):")
    print("-" * 40)
    for alloc, count in allocations.most_common():
        percentage = (count / successes * 100) if successes > 0 else 0
        print(f"{alloc:<36} {count:>5} ({percentage:>5.1f}%)")

    if failures > 0:
        print("\nErrors encountered:")
        print("-" * 25)
        for err, count in errors.most_common():
            print(f"{err}: {count}")

    # Exit with error code if we had high failure rate or no distribution
    if successes == 0:
        print("\nTest failed: 0 successful requests.")
        sys.exit(1)
    if failures / num_requests > 0.1:
        print("\nWarning: > 10% failure rate.")
        sys.exit(1)
    if len(nodes) < 2 and successes > 10:
        print("\nWarning: All traffic went to a single node. Load balancing may not be working across nodes.")

    if len(allocations) < 2 and successes > 10:
        print("\nWarning: All traffic went to a single container allocation. Load balancing may not be working.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stress test Traefik/Nomad load balancing")
    parser.add_argument("--url", default="http://localhost", help="Target URL (default: http://localhost)")
    parser.add_argument("-n", "--requests", type=int, default=1000, help="Total number of requests to send")
    parser.add_argument("-c", "--concurrency", type=int, default=50, help="Number of concurrent requests")
    parser.add_argument("--host", default="dummy.local.mesh", help="Host header to pass for Traefik routing (default: dummy.local.mesh)")

    args = parser.parse_args()

    try:
        asyncio.run(main(args.url, args.requests, args.concurrency, args.host))
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
        sys.exit(1)

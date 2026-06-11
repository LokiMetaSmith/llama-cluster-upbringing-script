# Cluster Cache

Inspired by the Gnutella protocol's GWebCaches, `cluster_cache` is a lightweight, stateless HTTP API designed to facilitate dynamic node bootstrapping in a distributed network.

## Purpose

Instead of relying on static definitions (like `inventory.yaml`) or a strictly defined Nomad control node, new legacy nodes can hit this HTTP endpoint to fetch the IPs of currently active Nomad/Consul servers. This allows nodes to auto-join the mesh and eases dynamic scaling, aligning with Option 2 from the `docs/analysis/GNUTELLA_ANALYSIS.md`.

## Features

- **Stateless Operation:** Maintains a simple in-memory cache of active node IPs.
- **Auto-Expiration:** Nodes must regularly ping the cache (e.g., every few minutes). Stale nodes are automatically removed.
- **RESTful API:** Provides simple `/register` and `/nodes` endpoints.

## Usage

Start the cache server:

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080
```

Register a node (defaults to client IP if not provided):

```bash
curl -X POST http://localhost:8080/register
```

Register a node with a specific IP:

```bash
curl -X POST http://localhost:8080/register -H "Content-Type: application/json" -d '{"ip_address": "192.168.1.100"}'
```

Get a list of active nodes:

```bash
curl http://localhost:8080/nodes
```

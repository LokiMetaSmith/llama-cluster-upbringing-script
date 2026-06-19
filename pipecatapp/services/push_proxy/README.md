# PUSH-style Reverse Proxy for NAT Traversal

This service implements a "connect-back" PUSH model (inspired by Gnutella) to help legacy worker nodes situated behind restrictive NATs or firewalls connect to the main Nomad/Consul cluster.

Instead of the cluster initiating connections to the worker, the worker connects outward to this jump-server proxy, which then tunnels the Nomad/Consul traffic back down to the worker.

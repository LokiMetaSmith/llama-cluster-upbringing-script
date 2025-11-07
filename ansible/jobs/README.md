# Ansible Jobs

This directory contains Nomad job files, some of which are templates that are rendered by Ansible.

## Files

- **benchmark.nomad**: A Nomad job for running a benchmark.
- **evolve-prompt.nomad.j2**: A Nomad job template for evolving prompts.
- **expert-debug.nomad**: A Nomad job for debugging an expert.
- **expert.nomad.j2**: A Nomad job template for running an expert.
- **health-check.nomad.j2**: A Nomad job template for running a health check.
- **llamacpp-batch.nomad.j2**: A Nomad job template for a llamacpp batch job.
- **llamacpp-rpc.nomad.j2**: A Nomad job template for a llamacpp RPC job.
- **model-benchmark.nomad.j2**: A Nomad job template for benchmarking a model.
- **pipecatapp-docker.nomad**: A Nomad job for the pipecatapp application, using Docker.
- **pipecatapp.nomad**: A Nomad job for the pipecatapp application.
- **router.nomad.j2**: A Nomad job template for the router.
- **test-runner.nomad.j2**: A Nomad job template for the test runner.

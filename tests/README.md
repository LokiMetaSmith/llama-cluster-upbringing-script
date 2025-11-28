# Testing

This directory contains unit, integration, and end-to-end tests for the various components of the project.

## Directory Structure

- **unit**: Contains unit tests.
- **integration**: Contains integration tests.
- **e2e**: Contains end-to-end tests.
- **scripts**: Contains test helper scripts.
- **playbooks**: Contains Ansible playbooks used for testing.

## Running Tests

Use the `run_tests.sh` script in the root directory to run tests.

```bash
./run_tests.sh --unit
./run_tests.sh --integration
./run_tests.sh --e2e
./run_tests.sh --all
```

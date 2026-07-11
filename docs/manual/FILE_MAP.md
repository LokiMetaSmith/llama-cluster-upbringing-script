# Codebase File Map

This document maps every file in the repository, their description, and utilization status.

## File List

| File Path | Status | Description | Details |
| --- | --- | --- | --- |
| `.djlint.toml` | 🟢 Referenced | File: .djlint.toml |  |
| `.gitattributes` | 🟢 Referenced | Set the default behavior, in case people don't have core.autocrlf set. |  |
| `.githooks/pre-commit` | 🟢 Referenced | bin/bash |  |
| `.github/AGENTIC_README.md` | 🟢 Referenced | Agentic Validation Loop Architecture |  |
| `.github/workflows/auto-merge.yml` | 🟢 Referenced | File: auto-merge.yml |  |
| `.github/workflows/ci.yml` | 🟢 Referenced | File: ci.yml |  |
| `.github/workflows/create-issues-from-files.yml` | 🟢 Referenced | File: create-issues-from-files.yml |  |
| `.github/workflows/docker-publish.yml` | 🔴 Orphan | File: docker-publish.yml |  |
| `.github/workflows/jules-queue.yml` | 🟢 Referenced | File: jules-queue.yml |  |
| `.github/workflows/remote-verify.yml` | 🟢 Referenced | File: remote-verify.yml |  |
| `.github/workflows/test-cluster.yml` | 🔴 Orphan | File: test-cluster.yml |  |
| `.github/workflows/unblocked-issues.yml` | 🟢 Referenced | File: unblocked-issues.yml |  |
| `.gitignore` | 🟢 Referenced | Ignore all log files |  |
| `.gitmodules` | 🟢 Referenced | File: .gitmodules |  |
| `.husky/pre-push` | 🟢 Referenced | File: pre-push |  |
| `.julesrules` | 🔴 Orphan | Jules AI Agent Rules |  |
| `.markdownlint.json` | 🟢 Referenced | File: .markdownlint.json |  |
| `.opencode/README.md` | 🟢 Referenced | OpenCode Configuration |  |
| `.opencode/opencode.json` | 🟢 Referenced | File: opencode.json |  |
| `.sops.yaml` | 🟢 Referenced | File: .sops.yaml |  |
| `.vulture_whitelist.py` | 🟢 Referenced | Vulture whitelist |  |
| `.yamllint` | 🟢 Referenced | File: .yamllint |  |
| `AGENTS.md` | 🟢 Referenced | AGENTS.md |  |
| `GEMINI.md` | 🟢 Referenced | AI Agent Custom Instructions |  |
| `ISSUES/2024-04-16-test-unblocked-issues-workflow.md` | 🔴 Orphan | Test Unblocked Issues Workflow |  |
| `LICENSE` | 🟢 Referenced | File: LICENSE |  |
| `README.md` | 🟢 Referenced | File: README.md |  |
| `README_bridge_networking_fix.md` | 🔵 Entry Point | Docker Bridge Networking Analysis and Resolution |  |
| `TODO.md` | 🟢 Referenced | TODO |  |
| `ansible.cfg` | 🟢 Referenced | File: ansible.cfg |  |
| `ansible/README.md` | 🟢 Referenced | Ansible |  |
| `ansible/filter_plugins/README.md` | 🟢 Referenced | Ansible Filter Plugins |  |
| `ansible/filter_plugins/safe_flatten.py` | 🟢 Referenced | File: safe_flatten.py | **Classes:** FilterModule<br>**Functions:** safe_flatten, filters |
| `ansible/jobs/README.md` | 🟢 Referenced | Ansible Jobs |  |
| `ansible/jobs/authentik.nomad` | 🟢 Referenced | File: authentik.nomad |  |
| `ansible/jobs/benchmark.nomad` | 🟢 Referenced | File: benchmark.nomad |  |
| `ansible/jobs/code-runner-service.nomad` | 🟢 Referenced | File: code-runner-service.nomad |  |
| `ansible/jobs/ds4-server.nomad.j2` | 🟢 Referenced | File: ds4-server.nomad.j2 |  |
| `ansible/jobs/dummy_web_service.nomad` | 🟢 Referenced | File: dummy_web_service.nomad |  |
| `ansible/jobs/e2a.nomad.j2` | 🟢 Referenced | File: e2a.nomad.j2 |  |
| `ansible/jobs/evolve-prompt.nomad.j2` | 🟢 Referenced | File: evolve-prompt.nomad.j2 |  |
| `ansible/jobs/expert-debug.nomad` | 🟢 Referenced | This is a Jinja2 template for a complete, distributed Llama expert. |  |
| `ansible/jobs/expert.nomad.j2` | 🟢 Referenced | This Nomad job file runs the main "expert" orchestrator service. |  |
| `ansible/jobs/filebrowser.nomad.j2` | 📄 Template | File: filebrowser.nomad.j2 |  |
| `ansible/jobs/health-check.nomad.j2` | 🟢 Referenced | File: health-check.nomad.j2 |  |
| `ansible/jobs/helixdb.nomad` | 🟢 Referenced | File: helixdb.nomad |  |
| `ansible/jobs/llamacpp-batch.nomad.j2` | 🟢 Referenced | File: llamacpp-batch.nomad.j2 |  |
| `ansible/jobs/llamacpp-rpc.nomad.j2` | 🟢 Referenced | This Nomad job file creates a pool of llama.cpp rpc-server providers. |  |
| `ansible/jobs/model-benchmark.nomad.j2` | 🟢 Referenced | File: model-benchmark.nomad.j2 |  |
| `ansible/jobs/opengravity.nomad.j2` | 🟢 Referenced | File: opengravity.nomad.j2 |  |
| `ansible/jobs/pipecatapp.nomad` | 🟢 Referenced | File: pipecatapp.nomad |  |
| `ansible/jobs/postgres.nomad` | 🟢 Referenced | File: postgres.nomad |  |
| `ansible/jobs/rag-service.nomad` | 🟢 Referenced | File: rag-service.nomad |  |
| `ansible/jobs/redis.nomad` | 🟢 Referenced | Consul Connect Service Mesh Configuration |  |
| `ansible/jobs/router.nomad.j2` | 🟢 Referenced | This Nomad job file runs the "router" service. |  |
| `ansible/jobs/smol-agent-server.nomad.j2` | 🟢 Referenced | File: smol-agent-server.nomad.j2 |  |
| `ansible/jobs/ternlight-service.nomad` | 🔴 Orphan | File: ternlight-service.nomad |  |
| `ansible/jobs/test-runner.nomad.j2` | 🟢 Referenced | File: test-runner.nomad.j2 |  |
| `ansible/jobs/tml-interaction.nomad.j2` | 🟢 Referenced | File: tml-interaction.nomad.j2 |  |
| `ansible/jobs/vllm.nomad.j2` | 📄 Template | File: vllm.nomad.j2 |  |
| `ansible/lint_nomad.yaml` | 🟢 Referenced | File: lint_nomad.yaml |  |
| `ansible/requirements.yml` | 🔴 Orphan | File: requirements.yml |  |
| `ansible/roles/README.md` | 🟢 Referenced | Ansible Roles |  |
| `ansible/roles/apt_proxy/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/apt_proxy/templates/apt_proxy.nomad.j2` | 🟢 Referenced | File: apt_proxy.nomad.j2 |  |
| `ansible/roles/authentik/defaults/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/authentik/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/authentik/templates/authentik.nomad.j2` | 🟢 Referenced | File: authentik.nomad.j2 |  |
| `ansible/roles/benchmark_models/tasks/benchmark_loop.yaml` | 🟢 Referenced | File: benchmark_loop.yaml |  |
| `ansible/roles/benchmark_models/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/benchmark_models/templates/model-benchmark.nomad.j2` | 🟢 Referenced | This Nomad job file runs a benchmark for a single model. |  |
| `ansible/roles/bootstrap_agent/defaults/main.yaml` | 🟢 Referenced | No default variables needed for this role. |  |
| `ansible/roles/bootstrap_agent/handlers/main.yaml` | 🟢 Referenced | handlers file for bootstrap_agent |  |
| `ansible/roles/bootstrap_agent/tasks/deploy_llama_cpp_model.yaml` | 🟢 Referenced | File: deploy_llama_cpp_model.yaml |  |
| `ansible/roles/bootstrap_agent/tasks/main.yaml` | 🟢 Referenced | tasks file for bootstrap_agent |  |
| `ansible/roles/btrfs_snapshot/defaults/main.yaml` | 🟢 Referenced | defaults file for btrfs_snapshot |  |
| `ansible/roles/btrfs_snapshot/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/clamav/files/rogue_agent.ldb` | 🟢 Referenced | File: rogue_agent.ldb |  |
| `ansible/roles/clamav/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/clamav/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/claude_clone/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/common-tools/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/common/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/common/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/common/tasks/network_repair.yaml` | 🟢 Referenced | File: network_repair.yaml |  |
| `ansible/roles/common/templates/cluster-ip-alias.service.j2` | 🟢 Referenced | File: cluster-ip-alias.service.j2 |  |
| `ansible/roles/common/templates/hosts.j2` | 🟢 Referenced | File: hosts.j2 |  |
| `ansible/roles/common/templates/update-ssh-authorized-keys.sh.j2` | 🟢 Referenced | bin/bash |  |
| `ansible/roles/config_manager/tasks/main.yaml` | 🟢 Referenced | tasks file for ansible/roles/config_manager/tasks/main.yaml |  |
| `ansible/roles/consul/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/consul/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/consul/tasks/acl.yaml` | 🟢 Referenced | File: acl.yaml |  |
| `ansible/roles/consul/tasks/main.yaml` | 🟢 Referenced | Task 0: Cleanup previous installation if requested |  |
| `ansible/roles/consul/tasks/tls.yaml` | 🟢 Referenced | File: tls.yaml |  |
| `ansible/roles/consul/templates/consul.hcl.j2` | 🟢 Referenced | File: consul.hcl.j2 |  |
| `ansible/roles/consul/templates/consul.service.j2` | 🟢 Referenced | File: consul.service.j2 |  |
| `ansible/roles/desktop_extras/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/docker/handlers/main.yaml` | 🟢 Referenced | handlers file for docker |  |
| `ansible/roles/docker/molecule/default/converge.yml` | 🟢 Referenced | File: converge.yml |  |
| `ansible/roles/docker/molecule/default/molecule.yml` | 🟢 Referenced | File: molecule.yml |  |
| `ansible/roles/docker/molecule/default/prepare.yml` | 🟢 Referenced | File: prepare.yml |  |
| `ansible/roles/docker/molecule/default/verify.yml` | 🟢 Referenced | File: verify.yml |  |
| `ansible/roles/docker/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/docker/templates/daemon.json.j2` | 🟢 Referenced | File: daemon.json.j2 |  |
| `ansible/roles/docker/templates/docker-prune.service.j2` | 🟢 Referenced | File: docker-prune.service.j2 |  |
| `ansible/roles/docker/templates/docker-prune.timer.j2` | 🟢 Referenced | File: docker-prune.timer.j2 |  |
| `ansible/roles/download_models/files/download_hf_repo.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** main |
| `ansible/roles/download_models/tasks/main.yaml` | 🟢 Referenced | tasks file for download_models (acts as IPFS Consumer on all nodes) |  |
| `ansible/roles/ds4/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/ds4/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/e2a/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/e2a/templates/e2a.nomad.j2` | 🟢 Referenced | Deploy on edge tier node (as specified by the user) |  |
| `ansible/roles/exo/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/exo/files/Dockerfile` | 🟢 Referenced | Install system dependencies |  |
| `ansible/roles/exo/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/exo/templates/exo.nomad.j2` | 🟢 Referenced | File: exo.nomad.j2 |  |
| `ansible/roles/exo/templates/load_image_task.nomad.j2` | 🟢 Referenced | File: load_image_task.nomad.j2 |  |
| `ansible/roles/forgejo/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/forgejo/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/forgejo/templates/forgejo.nomad.j2` | 🟢 Referenced | File: forgejo.nomad.j2 |  |
| `ansible/roles/gemini_cli/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/gemini_cli/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/gemini_cli/templates/gemini.nomad.j2` | 🟢 Referenced | File: gemini.nomad.j2 |  |
| `ansible/roles/gpu_setup/defaults/main.yaml` | 🟢 Referenced | defaults file for gpu_setup |  |
| `ansible/roles/gpu_setup/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/gpu_setup/templates/ai-cluster-env.sh.j2` | 🟢 Referenced | bin/sh |  |
| `ansible/roles/headscale/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/headscale/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/headscale/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/headscale/templates/config.yaml.j2` | 🟢 Referenced | File: config.yaml.j2 |  |
| `ansible/roles/headscale/templates/headscale.service.j2` | 🟢 Referenced | File: headscale.service.j2 |  |
| `ansible/roles/heretic_tool/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/heretic_tool/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/heretic_tool/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/hermes_agent/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/influxdb/README.md` | 🟢 Referenced | InfluxDB Role |  |
| `ansible/roles/influxdb/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/influxdb/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/influxdb/templates/influxdb.nomad.j2` | 🟢 Referenced | File: influxdb.nomad.j2 |  |
| `ansible/roles/ipfs/tasks/main.yaml` | 🟢 Referenced | Ensure IPFS CLI is installed |  |
| `ansible/roles/ipfs/templates/ipfs.nomad.j2` | 🟢 Referenced | File: ipfs.nomad.j2 |  |
| `ansible/roles/kittentts/tasks/main.yaml` | 🟢 Referenced | This role is deprecated and will be replaced by a Piper TTS implementation. |  |
| `ansible/roles/librarian/defaults/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/librarian/handlers/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/librarian/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/librarian/templates/librarian.service.j2` | 🟢 Referenced | File: librarian.service.j2 |  |
| `ansible/roles/librarian/templates/librarian_agent.py.j2` | 🟢 Referenced | usr/bin/env python3 |  |
| `ansible/roles/librarian/templates/spacedrive.service.j2` | 🟢 Referenced | File: spacedrive.service.j2 |  |
| `ansible/roles/llama_cpp/files/realtime_steering.patch` | 🟢 Referenced | File: realtime_steering.patch |  |
| `ansible/roles/llama_cpp/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/llama_cpp/molecule/default/converge.yml` | 🟢 Referenced | File: converge.yml |  |
| `ansible/roles/llama_cpp/molecule/default/molecule.yml` | 🟢 Referenced | File: molecule.yml |  |
| `ansible/roles/llama_cpp/molecule/default/verify.yml` | 🟢 Referenced | File: verify.yml |  |
| `ansible/roles/llama_cpp/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/llama_cpp/tasks/run_single_rpc_job.yaml` | 🟢 Referenced | File: run_single_rpc_job.yaml |  |
| `ansible/roles/llmfit/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/llxprt_code/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/llxprt_code/templates/llxprt-code.env.j2` | 🟢 Referenced | File: llxprt-code.env.j2 |  |
| `ansible/roles/magic_mirror/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/magic_mirror/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/magic_mirror/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/magic_mirror/templates/magic_mirror.nomad.j2` | 🟢 Referenced | File: magic_mirror.nomad.j2 |  |
| `ansible/roles/mcp_server/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/mcp_server/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/mcp_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/mcp_server/templates/mcp_server.nomad.j2` | 🟢 Referenced | File: mcp_server.nomad.j2 |  |
| `ansible/roles/memory_graph/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/memory_graph/templates/load_image_task.nomad.j2` | 🟢 Referenced | File: load_image_task.nomad.j2 |  |
| `ansible/roles/memory_graph/templates/memory-graph.nomad.j2` | 🟢 Referenced | File: memory-graph.nomad.j2 |  |
| `ansible/roles/memory_service/files/app.py` | 🟢 Referenced | File: app.py | **Classes:** Event, WorkItemCreate, WorkItemUpdate, DLQItemCreate, DLQClaimRequest, DLQItemUpdate<br>**Functions:** background_sync_task, startup_event, add_event, get_events, create_work_item... |
| `ansible/roles/memory_service/files/pmm_memory.py` | 🟢 Referenced | File: pmm_memory.py | **Classes:** PMMMemory<br>**Functions:** __init__, _init_db, _get_last_hash, _calculate_hash, add_event_sync... |
| `ansible/roles/memory_service/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/memory_service/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/memory_service/templates/load_image_task.nomad.j2` | 🟢 Referenced | File: load_image_task.nomad.j2 |  |
| `ansible/roles/memory_service/templates/memory_service.nomad.j2` | 🟢 Referenced | File: memory_service.nomad.j2 |  |
| `ansible/roles/minikeyvalue/files/Dockerfile` | 🟢 Referenced | File: Dockerfile |  |
| `ansible/roles/minikeyvalue/files/src/lib.go` | 🟢 Referenced | File: lib.go |  |
| `ansible/roles/minikeyvalue/files/src/lib_test.go` | 🟢 Referenced | File: lib_test.go |  |
| `ansible/roles/minikeyvalue/files/src/main.go` | 🟢 Referenced | File: main.go |  |
| `ansible/roles/minikeyvalue/files/src/rebalance.go` | 🟢 Referenced | File: rebalance.go |  |
| `ansible/roles/minikeyvalue/files/src/rebuild.go` | 🟢 Referenced | File: rebuild.go |  |
| `ansible/roles/minikeyvalue/files/src/s3api.go` | 🟢 Referenced | File: s3api.go |  |
| `ansible/roles/minikeyvalue/files/src/server.go` | 🟢 Referenced | File: server.go |  |
| `ansible/roles/minikeyvalue/files/start_master.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** get_service_nodes, main |
| `ansible/roles/minikeyvalue/files/volume` | 🟢 Referenced | bin/bash -e |  |
| `ansible/roles/minikeyvalue/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/minikeyvalue/templates/mkv.nomad.j2` | 🟢 Referenced | File: mkv.nomad.j2 |  |
| `ansible/roles/miniray/files/Dockerfile` | 🟢 Referenced | File: Dockerfile |  |
| `ansible/roles/miniray/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/miniray/templates/miniray.nomad.j2` | 🟢 Referenced | File: miniray.nomad.j2 |  |
| `ansible/roles/moe_gateway/files/gateway.py` | 🟢 Referenced | File: gateway.py | **Classes:** ServiceNotFound<br>**Functions:** init_db, _log_request_sync, log_request, _get_recent_requests_sync, get_recent_requests... |
| `ansible/roles/moe_gateway/files/static/index.html` | 🟢 Referenced | File: index.html |  |
| `ansible/roles/moe_gateway/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/moe_gateway/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/moe_gateway/templates/moe-gateway.nomad.j2` | 🟢 Referenced | File: moe-gateway.nomad.j2 |  |
| `ansible/roles/monitoring/defaults/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/monitoring/files/llm_dashboard.json` | 🟢 Referenced | File: llm_dashboard.json |  |
| `ansible/roles/monitoring/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/monitoring/templates/beszel-agent.nomad.j2` | 🟢 Referenced | File: beszel-agent.nomad.j2 |  |
| `ansible/roles/monitoring/templates/beszel-hub.nomad.j2` | 🟢 Referenced | File: beszel-hub.nomad.j2 |  |
| `ansible/roles/monitoring/templates/dashboards.yaml.j2` | 🟢 Referenced | File: dashboards.yaml.j2 |  |
| `ansible/roles/monitoring/templates/datasource.yaml.j2` | 🟢 Referenced | File: datasource.yaml.j2 |  |
| `ansible/roles/monitoring/templates/grafana.nomad.j2` | 🟢 Referenced | Update stanza for reliability |  |
| `ansible/roles/monitoring/templates/memory-audit.nomad.j2` | 🟢 Referenced | File: memory-audit.nomad.j2 |  |
| `ansible/roles/monitoring/templates/mqtt-exporter.nomad.j2` | 🟢 Referenced | Update stanza for reliability |  |
| `ansible/roles/monitoring/templates/node-exporter.nomad.j2` | 🟢 Referenced | File: node-exporter.nomad.j2 |  |
| `ansible/roles/monitoring/templates/prometheus.nomad.j2` | 🟢 Referenced | Update stanza for reliability |  |
| `ansible/roles/monitoring/templates/prometheus.yml.j2` | 🟢 Referenced | File: prometheus.yml.j2 |  |
| `ansible/roles/monitoring/templates/statsping.nomad.j2` | 🟢 Referenced | File: statsping.nomad.j2 |  |
| `ansible/roles/mqtt/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/mqtt/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/mqtt/templates/mosquitto.conf.j2` | 🟢 Referenced | File: mosquitto.conf.j2 |  |
| `ansible/roles/mqtt/templates/mqtt.nomad.j2` | 🟢 Referenced | File: mqtt.nomad.j2 |  |
| `ansible/roles/nanochat/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nanochat/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nanochat/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nanochat/templates/nanochat.nomad.j2` | 🟢 Referenced | File: nanochat.nomad.j2 |  |
| `ansible/roles/nats/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nats/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nats/templates/nats.nomad.j2` | 🟢 Referenced | File: nats.nomad.j2 |  |
| `ansible/roles/nfs/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nfs/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nfs/templates/exports.j2` | 🟢 Referenced | File: exports.j2 |  |
| `ansible/roles/nixos_pxe_server/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nixos_pxe_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nixos_pxe_server/templates/boot.ipxe.nix.j2` | 🟢 Referenced | ipxe |  |
| `ansible/roles/nixos_pxe_server/templates/configuration.nix.j2` | 🟢 Referenced | etc/nixos/configuration.nix |  |
| `ansible/roles/nomad/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nomad/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nomad/handlers/restart_nomad_handler_tasks.yaml` | 🟢 Referenced | File: restart_nomad_handler_tasks.yaml |  |
| `ansible/roles/nomad/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/nomad/tasks/tls.yaml` | 🟢 Referenced | File: tls.yaml |  |
| `ansible/roles/nomad/templates/client.hcl.j2` | 🟢 Referenced | Config generated by Ansible |  |
| `ansible/roles/nomad/templates/nomad.hcl.server.j2` | 🟢 Referenced | Config generated by Ansible |  |
| `ansible/roles/nomad/templates/nomad.service.j2` | 🟢 Referenced | File: nomad.service.j2 |  |
| `ansible/roles/nomad/templates/nomad.sh.j2` | 🟢 Referenced | bin/sh |  |
| `ansible/roles/nomad/templates/server.hcl.j2` | 🟢 Referenced | Config generated by Ansible |  |
| `ansible/roles/nomad/templates/start_nomad.sh.j2` | 🟢 Referenced | usr/bin/env bash |  |
| `ansible/roles/openclaw/files/Dockerfile` | 🟢 Referenced | Install system dependencies (curl for integration) |  |
| `ansible/roles/openclaw/files/pipecat_skill.md` | 🟢 Referenced | Pipecat Integration Skill |  |
| `ansible/roles/openclaw/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/openclaw/templates/load_image_task.nomad.j2` | 🟢 Referenced | File: load_image_task.nomad.j2 |  |
| `ansible/roles/openclaw/templates/openclaw.nomad.j2` | 🟢 Referenced | File: openclaw.nomad.j2 |  |
| `ansible/roles/opencode/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/opencode/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/opencode/templates/opencode.nomad.j2` | 🟢 Referenced | File: opencode.nomad.j2 |  |
| `ansible/roles/opengist/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/opengist/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/opengist/templates/opengist.nomad.j2` | 🟢 Referenced | File: opengist.nomad.j2 |  |
| `ansible/roles/opengravity/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/opengravity/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/opengravity/templates/Dockerfile.j2` | 🟢 Referenced | Copy the static website files specifically to avoid copying Dockerfile and conf |  |
| `ansible/roles/opengravity/templates/default.conf.j2` | 🟢 Referenced | File: default.conf.j2 |  |
| `ansible/roles/opengravity/templates/load_image_task.nomad.j2` | 🟢 Referenced | File: load_image_task.nomad.j2 |  |
| `ansible/roles/opengravity/templates/opengravity.nomad.j2` | 🟢 Referenced | File: opengravity.nomad.j2 |  |
| `ansible/roles/openworkers/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/openworkers/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/openworkers/templates/openworkers-bootstrap.nomad.j2` | 🟢 Referenced | File: openworkers-bootstrap.nomad.j2 |  |
| `ansible/roles/openworkers/templates/openworkers-infra.nomad.j2` | 🟢 Referenced | Postgate (HTTP proxy for Postgres) |  |
| `ansible/roles/openworkers/templates/openworkers-runners.nomad.j2` | 🟢 Referenced | File: openworkers-runners.nomad.j2 |  |
| `ansible/roles/paddler/tasks/main.yaml` | 🟢 Referenced | Note: Choose the libc version appropriate for your systems. |  |
| `ansible/roles/paddler_agent/README.md` | 🟢 Referenced | Ansible Role: paddler_agent |  |
| `ansible/roles/paddler_agent/defaults/main.yaml` | 🟢 Referenced | Defaults for the paddler_agent role |  |
| `ansible/roles/paddler_agent/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/paddler_agent/templates/paddler-agent.service.j2` | 🟢 Referenced | Assuming llama.cpp service is named llama-cpp.service or similar |  |
| `ansible/roles/paddler_balancer/README.md` | 🟢 Referenced | Ansible Role: paddler_balancer |  |
| `ansible/roles/paddler_balancer/defaults/main.yaml` | 🟢 Referenced | Defaults for the paddler_balancer role |  |
| `ansible/roles/paddler_balancer/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/paddler_balancer/templates/paddler-balancer.service.j2` | 🟢 Referenced | File: paddler-balancer.service.j2 |  |
| `ansible/roles/paperless/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/paperless/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/paperless/templates/paperless-app.nomad.j2` | 🟢 Referenced | File: paperless-app.nomad.j2 |  |
| `ansible/roles/paperless/templates/paperless-db.nomad.j2` | 🟢 Referenced | File: paperless-db.nomad.j2 |  |
| `ansible/roles/paperless/templates/paperless-redis.nomad.j2` | 🟢 Referenced | File: paperless-redis.nomad.j2 |  |
| `ansible/roles/pds/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pds/templates/pds.nomad.j2` | 🟢 Referenced | File: pds.nomad.j2 |  |
| `ansible/roles/pipecatapp/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pipecatapp/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pipecatapp/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pipecatapp/templates/architect.nomad.j2` | 🟢 Referenced | File: architect.nomad.j2 |  |
| `ansible/roles/pipecatapp/templates/archivist.nomad.j2` | 🟢 Referenced | File: archivist.nomad.j2 |  |
| `ansible/roles/pipecatapp/templates/load_image_task.nomad.j2` | 🟢 Referenced | File: load_image_task.nomad.j2 |  |
| `ansible/roles/pipecatapp/templates/pipecat.env.j2` | 🟢 Referenced | bin/sh |  |
| `ansible/roles/pipecatapp/templates/pipecatapp.nomad.j2` | 🟢 Referenced | File: pipecatapp.nomad.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/coding_expert.txt.j2` | 🟢 Referenced | File: coding_expert.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/consolidation_expert.txt.j2` | 🟢 Referenced | File: consolidation_expert.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/creative_expert.txt.j2` | 🟢 Referenced | File: creative_expert.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/cynic_expert.txt.j2` | 🟢 Referenced | File: cynic_expert.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/ingestion_expert.txt.j2` | 🟢 Referenced | File: ingestion_expert.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/memory_query_expert.txt.j2` | 🟢 Referenced | File: memory_query_expert.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/router.txt.j2` | 🟢 Referenced | File: router.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/tron_agent.txt.j2` | 🟢 Referenced | File: tron_agent.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/seed-agent.nomad.j2` | 🟢 Referenced | File: seed-agent.nomad.j2 |  |
| `ansible/roles/pipecatapp/templates/start_pipecatapp.sh.j2` | 🟢 Referenced | bin/bash |  |
| `ansible/roles/pipecatapp/templates/workflows/architect_loop.yaml.j2` | 🟢 Referenced | File: architect_loop.yaml.j2 |  |
| `ansible/roles/pipecatapp/templates/workflows/default_agent_loop.yaml.j2` | 🟢 Referenced | This workflow defines a single turn of the agent's reasoning loop. |  |
| `ansible/roles/pollen/README.md` | 🟢 Referenced | Pollen Ansible Role |  |
| `ansible/roles/pollen/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/polyphony/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/polyphony/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/polyphony/templates/polyphony.nomad.j2` | 🟢 Referenced | File: polyphony.nomad.j2 |  |
| `ansible/roles/postgres/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/postgres/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/postgres/templates/postgres.nomad.j2` | 🟢 Referenced | File: postgres.nomad.j2 |  |
| `ansible/roles/power_manager/defaults/main.yaml` | 🟢 Referenced | defaults file for power_manager |  |
| `ansible/roles/power_manager/files/power_agent.py` | 🟢 Referenced | Power management agent for sleeping and waking Nomad services. | **Classes:** HealthCheckHandler<br>**Functions:** run_health_check_server, load_config, put_service_to_sleep, wake_service_up, main... |
| `ansible/roles/power_manager/files/traffic_monitor.c` | 🟢 Referenced | File: traffic_monitor.c |  |
| `ansible/roles/power_manager/handlers/main.yaml` | 🟢 Referenced | handlers file for power_manager |  |
| `ansible/roles/power_manager/tasks/main.yaml` | 🟢 Referenced | tasks file for power_manager |  |
| `ansible/roles/power_manager/templates/nomad-watchdog.service.j2` | 🟢 Referenced | File: nomad-watchdog.service.j2 |  |
| `ansible/roles/power_manager/templates/power-agent.service.j2` | 🟢 Referenced | File: power-agent.service.j2 |  |
| `ansible/roles/power_manager/templates/watchdog.sh.j2` | 🟢 Referenced | usr/bin/env bash |  |
| `ansible/roles/preflight_checks/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/provisioning_api/files/provisioning_api.py` | 🟢 Referenced | File: provisioning_api.py | **Functions:** run_ansible_playbook, provision_node, get_all_statuses, get_status |
| `ansible/roles/provisioning_api/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/provisioning_api/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/provisioning_api/templates/provisioning-api.service.j2` | 🟢 Referenced | Make it wait for the network and Consul to be ready |  |
| `ansible/roles/pxe_server/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pxe_server/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pxe_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pxe_server/templates/boot.ipxe.j2` | 🟢 Referenced | ipxe |  |
| `ansible/roles/pxe_server/templates/dhcpd.conf.j2` | 🟢 Referenced | File: dhcpd.conf.j2 |  |
| `ansible/roles/pxe_server/templates/preseed.cfg.j2` | 🟢 Referenced | Preconfiguration file for Debian installation |  |
| `ansible/roles/pypi_proxy/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/pypi_proxy/templates/pypi_proxy.nomad.j2` | 🟢 Referenced | File: pypi_proxy.nomad.j2 |  |
| `ansible/roles/python_deps/files/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `ansible/roles/python_deps/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/python_deps/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/seed_models/files/reference_data/README.md` | 🟢 Referenced | Reference Data Directory |  |
| `ansible/roles/seed_models/tasks/main.yaml` | 🟢 Referenced | tasks file for seed_models (runs ONLY on controller) |  |
| `ansible/roles/semantic_router/defaults/main.yaml` | 🟢 Referenced | defaults/main.yaml |  |
| `ansible/roles/semantic_router/tasks/main.yaml` | 🟢 Referenced | tasks/main.yaml |  |
| `ansible/roles/semantic_router/templates/Dockerfile.j2` | 🟢 Referenced | Install system dependencies if needed (e.g. for building wheels) |  |
| `ansible/roles/semantic_router/templates/semantic-router.nomad.j2` | 🟢 Referenced | File: semantic-router.nomad.j2 |  |
| `ansible/roles/smol_agent_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/smol_agent_server/templates/smol-agent.nomad.j2` | 🟢 Referenced | File: smol-agent.nomad.j2 |  |
| `ansible/roles/sunshine/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/sunshine/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/sunshine/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/sunshine/templates/sunshine.nomad.j2` | 🟢 Referenced | File: sunshine.nomad.j2 |  |
| `ansible/roles/system_deps/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/tailscale/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/telegraf/README.md` | 🟢 Referenced | Telegraf Role |  |
| `ansible/roles/telegraf/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/telegraf/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/telegraf/templates/telegraf.conf.j2` | 🟢 Referenced | File: telegraf.conf.j2 |  |
| `ansible/roles/telegraf/templates/telegraf.nomad.j2` | 🟢 Referenced | File: telegraf.nomad.j2 |  |
| `ansible/roles/term_everything/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/tml_interaction/README.md` | 🟢 Referenced | TML Interaction Role |  |
| `ansible/roles/tml_interaction/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/tool_server/Dockerfile` | 🟢 Referenced | File: Dockerfile |  |
| `ansible/roles/tool_server/app.py` | 🟢 Referenced | File: app.py | **Classes:** ToolRequest<br>**Functions:** validation_exception_handler, read_health, run_tool, list_tools |
| `ansible/roles/tool_server/entrypoint.sh` | 🟢 Referenced | bin/bash |  |
| `ansible/roles/tool_server/pmm_memory.py` | 🟢 Referenced | File: pmm_memory.py | **Classes:** PMMMemory<br>**Functions:** __init__, _init_db, _get_last_hash, _calculate_hash, add_event... |
| `ansible/roles/tool_server/preload_models.py` | 🟢 Referenced | Preload models to ensure they are cached in the Docker image |  |
| `ansible/roles/tool_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/tool_server/templates/load_image_task.nomad.j2` | 🟢 Referenced | File: load_image_task.nomad.j2 |  |
| `ansible/roles/tool_server/templates/tool_server.nomad.j2` | 🟢 Referenced | File: tool_server.nomad.j2 |  |
| `ansible/roles/tool_server/tools/ansible_tool.py` | 🟢 Referenced | File: ansible_tool.py | **Classes:** Ansible_Tool<br>**Functions:** __init__, run_playbook |
| `ansible/roles/tool_server/tools/archivist_tool.py` | 🟢 Referenced | File: archivist_tool.py | **Classes:** ArchivistTool<br>**Functions:** __init__, run, __call__ |
| `ansible/roles/tool_server/tools/claude_clone_tool.py` | 🟢 Referenced | File: claude_clone_tool.py | **Classes:** ClaudeCloneTool<br>**Functions:** __init__, _run_command, explain, report, generate... |
| `ansible/roles/tool_server/tools/code_runner_tool.py` | 🟢 Referenced | File: code_runner_tool.py | **Classes:** CodeRunnerTool<br>**Functions:** __init__, run_python_code, run_code_in_sandbox |
| `ansible/roles/tool_server/tools/council_tool.py` | 🟢 Referenced | File: council_tool.py | **Classes:** CouncilTool<br>**Functions:** __init__, _discover_local_experts, _query_model, convene |
| `ansible/roles/tool_server/tools/desktop_control_tool.py` | 🟢 Referenced | File: desktop_control_tool.py | **Classes:** DesktopControlTool<br>**Functions:** __init__, get_desktop_screenshot, click_at, type_text |
| `ansible/roles/tool_server/tools/file_editor_tool.py` | 🟢 Referenced | File: file_editor_tool.py | **Classes:** FileEditorTool<br>**Functions:** __init__, _validate_path, read_file, write_file, apply_patch... |
| `ansible/roles/tool_server/tools/final_answer_tool.py` | 🟢 Referenced | File: final_answer_tool.py | **Classes:** FinalAnswerTool<br>**Functions:** __init__, submit_task |
| `ansible/roles/tool_server/tools/gemini_cli.py` | 🟢 Referenced | File: gemini_cli.py | **Functions:** send_message |
| `ansible/roles/tool_server/tools/get_nomad_job.py` | 🟢 Referenced | File: get_nomad_job.py | **Functions:** get_nomad_job_definition, main |
| `ansible/roles/tool_server/tools/git_tool.py` | 🟢 Referenced | File: git_tool.py | **Classes:** Git_Tool<br>**Functions:** __init__, _run_git_command, clone, pull, push... |
| `ansible/roles/tool_server/tools/ha_tool.py` | 🟢 Referenced | File: ha_tool.py | **Classes:** HA_Tool<br>**Functions:** __init__, call_ai_task |
| `ansible/roles/tool_server/tools/llxprt_code_tool.py` | 🟢 Referenced | File: llxprt_code_tool.py | **Classes:** LLxprt_Code_Tool<br>**Functions:** __init__, run |
| `ansible/roles/tool_server/tools/mcp_tool.py` | 🟢 Referenced | File: mcp_tool.py | **Classes:** MCP_Tool<br>**Functions:** __init__, get_status, get_memory_summary, clear_short_term_memory |
| `ansible/roles/tool_server/tools/opencode_tool.py` | 🟢 Referenced | File: opencode_tool.py | **Classes:** OpencodeTool<br>**Functions:** __init__, run |
| `ansible/roles/tool_server/tools/orchestrator_tool.py` | 🟢 Referenced | File: orchestrator_tool.py | **Classes:** OrchestratorTool<br>**Functions:** __init__, dispatch_job |
| `ansible/roles/tool_server/tools/planner_tool.py` | 🟢 Referenced | File: planner_tool.py | **Classes:** PlannerTool<br>**Functions:** __init__, _discover_llm_url, _call_llm, plan_and_execute |
| `ansible/roles/tool_server/tools/power_tool.py` | 🟢 Referenced | File: power_tool.py | **Classes:** Power_Tool<br>**Functions:** __init__, set_idle_threshold |
| `ansible/roles/tool_server/tools/project_mapper_tool.py` | 🟢 Referenced | File: project_mapper_tool.py | **Classes:** ProjectMapperTool<br>**Functions:** __init__, _is_ignored, scan, _guess_type, _extract_imports |
| `ansible/roles/tool_server/tools/prompt_improver_tool.py` | 🟢 Referenced | File: prompt_improver_tool.py | **Classes:** PromptImproverTool<br>**Functions:** __init__, _discover_llm, _call_llm, create_prompt_plan |
| `ansible/roles/tool_server/tools/rag_tool.py` | 🟢 Referenced | File: rag_tool.py | **Classes:** RAG_Tool<br>**Functions:** __init__, _build_knowledge_base, search_knowledge_base |
| `ansible/roles/tool_server/tools/sandbox.ts` | 🟢 Referenced | sandbox.ts |  |
| `ansible/roles/tool_server/tools/smol_agent_tool.py` | 🟢 Referenced | File: smol_agent_tool.py | **Classes:** SmolAgentTool, CodeAgent, LiteLLMModel<br>**Functions:** __init__, _initialize, _execute_in_sandbox, run, __init__... |
| `ansible/roles/tool_server/tools/ssh_tool.py` | 🟢 Referenced | File: ssh_tool.py | **Classes:** SSH_Tool<br>**Functions:** __init__, run_command |
| `ansible/roles/tool_server/tools/summarizer_tool.py` | 🟢 Referenced | File: summarizer_tool.py | **Classes:** SummarizerTool<br>**Functions:** __init__, get_summary |
| `ansible/roles/tool_server/tools/swarm_tool.py` | 🟢 Referenced | File: swarm_tool.py | **Classes:** SwarmTool<br>**Functions:** __init__, spawn_workers, kill_worker |
| `ansible/roles/tool_server/tools/tap_service.py` | 🟢 Referenced | File: tap_service.py | **Classes:** TapService<br>**Functions:** __init__, process_frame |
| `ansible/roles/tool_server/tools/term_everything_tool.py` | 🟢 Referenced | File: term_everything_tool.py | **Classes:** TermEverythingTool<br>**Functions:** __init__, execute |
| `ansible/roles/tool_server/tools/web_browser_tool.py` | 🟢 Referenced | Mock playwright if it's not available | **Classes:** WebBrowserTool<br>**Functions:** __init__, goto, get_page_content, get_screenshot, click... |
| `ansible/roles/tpm_ssh/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/tpm_ssh/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/tpm_ssh/templates/tpm-ssh-agent.service.j2` | 🟢 Referenced | File: tpm-ssh-agent.service.j2 |  |
| `ansible/roles/tpm_ssh/templates/tpm-ssh-agent.sh.j2` | 🟢 Referenced | bin/bash |  |
| `ansible/roles/tpm_ssh/templates/tpm_pins.j2` | 🟢 Referenced | This file contains the PINs required to unlock the TPM PKCS#11 token. |  |
| `ansible/roles/traceway/defaults/main.yaml` | 🟢 Referenced | defaults file for traceway |  |
| `ansible/roles/traceway/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/traceway/templates/traceway.nomad.j2` | 🟢 Referenced | File: traceway.nomad.j2 |  |
| `ansible/roles/traefik/defaults/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/traefik/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/traefik/templates/headscale-router.yaml.j2` | 🟢 Referenced | File: headscale-router.yaml.j2 |  |
| `ansible/roles/traefik/templates/traefik.nomad.j2` | 🟢 Referenced | File: traefik.nomad.j2 |  |
| `ansible/roles/unified_fs/defaults/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/unified_fs/files/unified_fs_agent.py` | 🟢 Referenced | usr/bin/env python3 | **Classes:** DataCache, Backend, ConsulBackend, MemoryBackend, UnifiedFS<br>**Functions:** __init__, get, set, getattr, readdir... |
| `ansible/roles/unified_fs/handlers/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/unified_fs/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/unified_fs/templates/unified_fs.service.j2` | 🟢 Referenced | File: unified_fs.service.j2 |  |
| `ansible/roles/vision/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/vision/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/vision/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/vision/templates/config.yml.j2` | 🟢 Referenced | File: config.yml.j2 |  |
| `ansible/roles/vision/templates/vision.nomad.j2` | 🟢 Referenced | File: vision.nomad.j2 |  |
| `ansible/roles/vllm/tasks/main.yaml` | 🟢 Referenced | tasks file for vllm |  |
| `ansible/roles/vllm/tasks/run_single_vllm_job.yaml` | 🟢 Referenced | tasks/run_single_vllm_job.yaml |  |
| `ansible/roles/vllm/templates/vllm-expert.nomad.j2` | 🟢 Referenced | File: vllm-expert.nomad.j2 |  |
| `ansible/roles/whisper_cpp/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/world_model_service/files/Dockerfile` | 🟢 Referenced | Use an official Python runtime as a parent image |  |
| `ansible/roles/world_model_service/files/app.py` | 🟢 Referenced | File: app.py | **Classes:** DispatchJobRequest<br>**Functions:** get_env_int, lifespan, on_connect, on_disconnect, on_message... |
| `ansible/roles/world_model_service/files/debug_world_model.sh` | 🟢 Referenced | bin/bash |  |
| `ansible/roles/world_model_service/files/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `ansible/roles/world_model_service/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/world_model_service/templates/world_model.nomad.j2` | 🟢 Referenced | File: world_model.nomad.j2 |  |
| `ansible/roles/zigbee2mqtt/README.md` | 🟢 Referenced | Zigbee2MQTT Role |  |
| `ansible/roles/zigbee2mqtt/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/zigbee2mqtt/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/zigbee2mqtt/templates/zigbee2mqtt.nomad.j2` | 🟢 Referenced | File: zigbee2mqtt.nomad.j2 |  |
| `ansible/run_download_models.yaml` | 🟢 Referenced | File: run_download_models.yaml |  |
| `ansible/tasks/README.md` | 🟢 Referenced | Ansible Tasks |  |
| `ansible/tasks/build_cached_image.yaml` | 🟢 Referenced | File: build_cached_image.yaml |  |
| `ansible/tasks/build_pipecatapp_image.yaml` | 🟢 Referenced | File: build_pipecatapp_image.yaml |  |
| `ansible/tasks/create_expert_job.yaml` | 🟢 Referenced | File: create_expert_job.yaml |  |
| `ansible/tasks/deploy_expert_wrapper.yaml` | 🟢 Referenced | File: deploy_expert_wrapper.yaml |  |
| `ansible/tasks/deploy_model_gpu_provider.yaml` | 🟢 Referenced | File: deploy_model_gpu_provider.yaml |  |
| `ansible/templates/shared/load_image_task.nomad.j2` | 🟢 Referenced | File: load_image_task.nomad.j2 |  |
| `ansible/tests/verify_grafana.yaml` | 🧪 Test | File: verify_grafana.yaml |  |
| `ansible/tests/verify_playbook_syntax.yaml` | 🧪 Test | File: verify_playbook_syntax.yaml |  |
| `assets/llama_icon.png` | 🟢 Referenced | File: llama_icon.png |  |
| `benchmark.py` | 🔴 Orphan | add path | **Functions:** main, fake_post |
| `benchmark_async.py` | 🔴 Orphan | File: benchmark_async.py | **Classes:** AsyncContextManagerMock<br>**Functions:** main, __aenter__, __aexit__ |
| `bootstrap.sh` | 🟢 Referenced | Easy Bootstrap Script for Single-Node Setup  This script simplifies the process of bootstrapping th |  |
| `cluster_cache/README.md` | 🟢 Referenced | Cluster Cache |  |
| `cluster_cache/app.py` | 🟢 Referenced | File: app.py | **Classes:** NodeRegistration, NodeList<br>**Functions:** cleanup_expired_nodes, register_node, get_nodes |
| `cluster_cache/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `command_deck/backend/app.py` | 🟢 Referenced | CommandDeck Setup Platform Backend. | **Classes:** CommandDeckAPIHandler<br>**Functions:** log_reader_thread, parse_models, run_server, main, log_message... |
| `command_deck/frontend/index.html` | 🟢 Referenced | File: index.html |  |
| `command_deck/frontend/script.js` | 🟢 Referenced | File: script.js |  |
| `command_deck/frontend/style.css` | 🟢 Referenced | File: style.css |  |
| `disk_script.sh` | 🔵 Entry Point | bin/bash |  |
| `docker/README.md` | 🟢 Referenced | Docker |  |
| `docker/dev_container/Dockerfile` | 🟢 Referenced | Install system dependencies |  |
| `docker/memory_service/Dockerfile` | 🟢 Referenced | Install dependencies |  |
| `docs/DEAD_CODE_REVIEW.md` | 📄 Documentation/Asset | Dead Code Review Report |  |
| `docs/README.md` | 🟢 Referenced | Project Documentation |  |
| `docs/analysis/AGENT_LIGHTNING_ANALYSIS.md` | 🟢 Referenced | Agent Lightning Analysis |  |
| `docs/analysis/BENCHMARKING.MD` | 🟢 Referenced | A Guide to Benchmarking Your AI Cluster |  |
| `docs/analysis/CEPH_EVALUATION.md` | 🟢 Referenced | Ceph Storage Cluster Evaluation Report |  |
| `docs/analysis/CLAMAV_EVALUATION.md` | 🟢 Referenced | ClamAV Evaluation Report |  |
| `docs/analysis/CLAUDE_CODE_ANALYSIS.md` | 🟢 Referenced | Claude Code CLI Analysis |  |
| `docs/analysis/DIRAC_EVALUATION.md` | 🟢 Referenced | Dirac Evaluation: Inclusion vs Inspiration |  |
| `docs/analysis/EVALUATION_LLMROUTER.md` | 🟢 Referenced | LLMRouter Evaluation Report |  |
| `docs/analysis/FLOWISE_ANALYSIS.md` | 🟢 Referenced | Flowise Architecture & UI Analysis |  |
| `docs/analysis/GCP_GENERATIVE_AI_REVIEW.md` | 🟢 Referenced | Google Cloud Platform Generative AI Review |  |
| `docs/analysis/GNUTELLA_ANALYSIS.md` | 🟢 Referenced | Analysis: Lessons from the Gnutella Project for Distributed AI Pipelines |  |
| `docs/analysis/HAYSTACK_ANALYSIS.md` | 🟢 Referenced | Haystack Analysis and Integration Report |  |
| `docs/analysis/HELIXDB_EVALUATION.md` | 🟢 Referenced | HelixDB Evaluation Report |  |
| `docs/analysis/IPV6_AUDIT.md` | 🟢 Referenced | IPv6 Audit Report |  |
| `docs/analysis/LANGCHAIN_ANALYSIS.md` | 🟢 Referenced | LangChain Analysis and Hybrid Integration Report |  |
| `docs/analysis/LITEGRAPH_VS_REACTFLOW.md` | 🟢 Referenced | LiteGraph vs ReactFlow Analysis |  |
| `docs/analysis/MEMENTO_SKILLS_ANALYSIS.md` | 🟢 Referenced | Memento-Skills Architecture Analysis |  |
| `docs/analysis/PASEO_ANALYSIS.md` | 🟢 Referenced | Paseo Analysis: Architecture and Concepts for PipecatApp Integration |  |
| `docs/analysis/POLLEN_COMPARISON.md` | 🟢 Referenced | Pollen vs. Current AI Cluster Architecture |  |
| `docs/analysis/REFACTOR_PROPOSAL_hybrid_architecture.md` | 🟢 Referenced | Refactoring Proposal: Hybrid / Cluster-Native Architecture |  |
| `docs/analysis/SECURITY_AUDIT.md` | 🟢 Referenced | Security Audit Log |  |
| `docs/analysis/TOOL_EVALUATION.md` | 🟢 Referenced | Tool Evaluation and Strategic Direction |  |
| `docs/analysis/VLLM_PROJECT_EVALUATION.md` | 🟢 Referenced | vLLM Project Evaluation |  |
| `docs/analysis/YAML_FILES_REPORT.md` | 🟢 Referenced | Report on YAML Files in Root Directory |  |
| `docs/analysis/aid_e_log.txt` | 🟢 Referenced | File: aid_e_log.txt |  |
| `docs/analysis/heretic_evaluation.md` | 🟢 Referenced | Heretic Repository Evaluation |  |
| `docs/analysis/review_report.md` | 🟢 Referenced | Project Review Report |  |
| `docs/manual/AGENTS.md` | 🟢 Referenced | AI Agent Architectures |  |
| `docs/manual/AI_GOVERNANCE.md` | 📄 Documentation/Asset | AI Governance & Architecture Plan |  |
| `docs/manual/ARCHITECTURE.md` | 🟢 Referenced | Holistic Project Architecture |  |
| `docs/manual/DEPLOYMENT_AND_PROFILING.md` | 🟢 Referenced | Deploying and Profiling AI Services |  |
| `docs/manual/DIRAC_TODO.md` | 🟢 Referenced | Dirac Integration Plan & TODO List |  |
| `docs/manual/FRONTEND_VERIFICATION.md` | 🟢 Referenced | Frontend Verification Instructions with Playwright |  |
| `docs/manual/FRONTIER_AGENT_ROADMAP.md` | 📄 Documentation/Asset | Frontier Agent Roadmap |  |
| `docs/manual/GASTOWN_TODO.md` | 🟢 Referenced | Gas Town Integration Todo |  |
| `docs/manual/GEMINI.md` | 🟢 Referenced | GEMINI.md |  |
| `docs/manual/LOAD_TESTING.md` | 📄 Documentation/Asset | Cluster Load Testing and Network Validation |  |
| `docs/manual/MCP_MIGRATION_PLAN.md` | 🟢 Referenced | MCP Migration Plan |  |
| `docs/manual/MCP_SERVER_SETUP.md` | 🟢 Referenced | Building an MCP Server with Service Discovery |  |
| `docs/manual/MEMORIES.md` | 🟢 Referenced | Agent Memories |  |
| `docs/manual/NETWORK.md` | 🟢 Referenced | Network Architecture |  |
| `docs/manual/NETWORK_ISOLATION.md` | 🟢 Referenced | AI Cluster Network Isolation Guide |  |
| `docs/manual/NIXOS_PXE_BOOT_SETUP.md` | 🟢 Referenced | NixOS-based PXE Boot Server Setup |  |
| `docs/manual/OBSIDIAN_TODO.md` | 🟢 Referenced | Obsidian & 3D Workflow Integration Todo List |  |
| `docs/manual/OBSIDIAN_WORKFLOW_DESIGN.md` | 🟢 Referenced | Obsidian Workflow Design: The "Active Vault" Architecture |  |
| `docs/manual/PERFORMANCE_OPTIMIZATION.md` | 📄 Documentation/Asset | Performance & I/O Optimization |  |
| `docs/manual/PROJECT_SUMMARY.md` | 🟢 Referenced | Project Summary: Architecting a Responsive, Distributed Conversational AI Pipeline |  |
| `docs/manual/PXE_BOOT_SETUP.md` | 🟢 Referenced | iPXE Boot Server Setup for Automated Debian Installation |  |
| `docs/manual/REMOTE_WORKFLOW.md` | 🟢 Referenced | Improving Your Remote Workflow with Mosh and Tmux |  |
| `docs/manual/SCALING_TODO.md` | 🟢 Referenced | Scaling Long-Running Autonomous Coding - Implementation Scope |  |
| `docs/manual/SPIRE_POC.md` | 📄 Documentation/Asset | SPIFFE/SPIRE Integration PoC |  |
| `docs/manual/TODO_Hybrid_Architecture.md` | 🟢 Referenced | Hybrid Architecture Implementation To-Do List |  |
| `docs/manual/TROUBLESHOOTING.md` | 🟢 Referenced | Troubleshooting Guide |  |
| `docs/manual/TWINSERVICE_DEMONOLITHIZATION_DESIGN.md` | 🟢 Referenced | Architectural Design: Microservice De-monolithization of TwinService |  |
| `docs/media/initial_state.png` | 📄 Documentation/Asset | File: initial_state.png |  |
| `docs/media/paused_state.png` | 📄 Documentation/Asset | File: paused_state.png |  |
| `evaluations/ds4_evaluation.md` | 🔴 Orphan | Evaluation of DwarfStar (ds4) for Cluster Inclusion |  |
| `evaluations/dspark_speculative_decoding_report.md` | 🔴 Orphan | DSpark Speculative Decoding Architecture Report |  |
| `evaluations/longcat_2.0_evaluation.md` | 🔴 Orphan | LongCat 2.0 Evaluation vs. Local Distributed Pipeline |  |
| `evaluations/ornith-1-evaluation.md` | 🔴 Orphan | Ornith-1 Evaluation for Local LLM Provider (llama-cluster-upbringing-script) |  |
| `examples/README.md` | 🟢 Referenced | Examples |  |
| `examples/chat-persistent.sh` | 🟢 Referenced | bin/bash |  |
| `fix_dep_scanner.py` | 🔴 Orphan | Since `scan_package` is NOT called on `mock_scanner_instance` (because CALLS: []), |  |
| `group_vars/README.md` | 🟢 Referenced | Ansible Group Variables |  |
| `group_vars/all.yaml` | 🟢 Referenced | This file contains variables that are common to all hosts in the inventory. |  |
| `group_vars/external_experts.yaml` | 🟢 Referenced | Configuration for external, third-party LLM experts. |  |
| `group_vars/models.yaml` | 🟢 Referenced | This file centralizes the configuration for all AI models used in the project. |  |
| `host_vars/README.md` | 🟢 Referenced | Ansible Host Variables |  |
| `host_vars/localhost.yaml` | 🟢 Referenced | BEGIN ANSIBLE MANAGED BLOCK |  |
| `hostfile` | 🟢 Referenced | File: hostfile |  |
| `initial-setup/README.md` | 🟢 Referenced | Initial Machine Setup |  |
| `initial-setup/add_new_worker.sh` | 🟢 Referenced | Script to manually provision a new worker node for the cluster. This script automates the process o |  |
| `initial-setup/modules/01-network.sh` | 🟢 Referenced | bin/bash |  |
| `initial-setup/modules/02-hostname.sh` | 🟢 Referenced | Ensure CONFIG_FILE is defined (fallback if run standalone) |  |
| `initial-setup/modules/03-user.sh` | 🟢 Referenced | bin/bash |  |
| `initial-setup/modules/04-ssh.sh` | 🟢 Referenced | bin/bash |  |
| `initial-setup/modules/05-auto-provision.sh` | 🟢 Referenced | bin/bash |  |
| `initial-setup/modules/README.md` | 🟢 Referenced | Initial Setup Modules |  |
| `initial-setup/setup.conf` | 🟢 Referenced | File: setup.conf |  |
| `initial-setup/setup.sh` | 🟢 Referenced | Exit immediately if a command exits with a non-zero status. |  |
| `initial-setup/update_inventory.sh` | 🟢 Referenced | This script dynamically generates the Ansible inventory.yaml file by querying the Consul API for the |  |
| `initial-setup/worker-setup/README.md` | 🟢 Referenced | Manual Worker Node Setup |  |
| `initial-setup/worker-setup/setup.sh` | 🟢 Referenced | This script performs the absolute minimal setup required for a new Debian machine to be provisioned |  |
| `inventory.yaml` | 🟢 Referenced | This inventory is dynamically generated by update_inventory.sh |  |
| `local_inventory.ini` | 🟢 Referenced | File: local_inventory.ini |  |
| `memory_disk_script.sh` | 🔵 Entry Point | Memory Check |  |
| `modules/keystone-polyphony/.agents/workflows/0-click-boot.md` | 🟢 Referenced | 0-Click Boot Protocol for Agents |  |
| `modules/keystone-polyphony/.agents/workflows/boot.md` | 🟢 Referenced | Boot Workflow: 0-Click Initialization |  |
| `modules/keystone-polyphony/.agents/workflows/swarm-communication.md` | 🔴 Orphan | Swarm Communication Protocol for Agents |  |
| `modules/keystone-polyphony/.devcontainer/devcontainer.json` | 🟢 Referenced | File: devcontainer.json |  |
| `modules/keystone-polyphony/.flake8` | 🔴 Orphan | File: .flake8 |  |
| `modules/keystone-polyphony/.githooks/pre-commit` | 🟢 Referenced | usr/bin/env bash |  |
| `modules/keystone-polyphony/.githooks/pre-push` | 🟢 Referenced | usr/bin/env bash |  |
| `modules/keystone-polyphony/.github/reviewers.yml` | 🟢 Referenced | File: reviewers.yml |  |
| `modules/keystone-polyphony/.github/workflows/add-contributors.yml` | 🟢 Referenced | File: add-contributors.yml |  |
| `modules/keystone-polyphony/.github/workflows/agent-issue-solver.yml` | 🟢 Referenced | File: agent-issue-solver.yml |  |
| `modules/keystone-polyphony/.github/workflows/agent-issue-triage.yml` | 🟢 Referenced | File: agent-issue-triage.yml |  |
| `modules/keystone-polyphony/.github/workflows/agent-parallel-solver.yml` | 🔴 Orphan | File: agent-parallel-solver.yml |  |
| `modules/keystone-polyphony/.github/workflows/auto-merge-staging.yml` | 🟢 Referenced | File: auto-merge-staging.yml |  |
| `modules/keystone-polyphony/.github/workflows/daily-close-merged-issues.yml` | 🟢 Referenced | File: daily-close-merged-issues.yml |  |
| `modules/keystone-polyphony/.github/workflows/opencode.yml` | 🟢 Referenced | File: opencode.yml |  |
| `modules/keystone-polyphony/.github/workflows/periodic-merge-main.yml` | 🟢 Referenced | File: periodic-merge-main.yml |  |
| `modules/keystone-polyphony/.github/workflows/swarm-node.yml` | 🔴 Orphan | Trigger on feature branches but not main. |  |
| `modules/keystone-polyphony/.github/workflows/workflow-review-dispatch.yml` | 🔴 Orphan | File: workflow-review-dispatch.yml |  |
| `modules/keystone-polyphony/.github/workflows/workflow-review.yml` | 🟢 Referenced | File: workflow-review.yml |  |
| `modules/keystone-polyphony/.gitignore` | 🟢 Referenced | Node.js |  |
| `modules/keystone-polyphony/AGENTS.md` | 🟢 Referenced | Keystone Polyphony, Contributor Norms for Autonomous Systems |  |
| `modules/keystone-polyphony/CODE_OF_CONDUCT.md` | 🟢 Referenced | Code of Conduct |  |
| `modules/keystone-polyphony/CONTRIBUTING.md` | 🟢 Referenced | Contributing to Keystone Polyphony |  |
| `modules/keystone-polyphony/Dockerfile` | 🟢 Referenced | Use a lightweight Python base image |  |
| `modules/keystone-polyphony/ENSEMBLE_TRIAL.md` | 🔴 Orphan | Ensemble First Performance: The Swarm Backlog |  |
| `modules/keystone-polyphony/LICENSE` | 🟢 Referenced | File: LICENSE |  |
| `modules/keystone-polyphony/README.md` | 🟢 Referenced | Keystone Polyphony: A Mind Bridge |  |
| `modules/keystone-polyphony/TODO.md` | 🟢 Referenced | Keystone Polyphony - Remaining Tasks & Future Roadmap |  |
| `modules/keystone-polyphony/WORK_ORDER.md` | 🔴 Orphan | WORK ORDER: Automate Liminal Space Initialization on Workspace Boot |  |
| `modules/keystone-polyphony/docker-compose.yml` | 🟢 Referenced | The Anchor Node |  |
| `modules/keystone-polyphony/docs/architecture.md` | 🟢 Referenced | Repository Architecture |  |
| `modules/keystone-polyphony/docs/ci-cd.md` | 🟢 Referenced | Continuous Integration & Delivery (CI/CD) |  |
| `modules/keystone-polyphony/docs/features/git-hooks.feature` | 🟢 Referenced | File: git-hooks.feature |  |
| `modules/keystone-polyphony/docs/getting-started.md` | 🟢 Referenced | Getting Started |  |
| `modules/keystone-polyphony/docs/git-hooks-architecture.md` | 🟢 Referenced | Git Hooks Architecture for All Contributors |  |
| `modules/keystone-polyphony/docs/hooks-interaction.md` | 📄 Documentation/Asset | Human Interaction Story: Git Hooks |  |
| `modules/keystone-polyphony/docs/issues-pre-review/vision-and-impact.md` | 📄 Documentation/Asset | Issue Pre-Review Triage: Vision and Impact |  |
| `modules/keystone-polyphony/docs/liminal-bridge.md` | 🟢 Referenced | Liminal Bridge |  |
| `modules/keystone-polyphony/docs/swarm-coordination.md` | 📄 Documentation/Asset | Swarm Coordination Protocol |  |
| `modules/keystone-polyphony/docs/swarm-discovery/analysis.md` | 🟢 Referenced | Environmental & Constraints Analysis |  |
| `modules/keystone-polyphony/docs/swarm-discovery/architecture-diagram.md` | 📄 Documentation/Asset | Sensory Architecture Diagram |  |
| `modules/keystone-polyphony/docs/swarm-discovery/hardware-bom.md` | 📄 Documentation/Asset | Hardware Bill of Materials (BOM) |  |
| `modules/keystone-polyphony/docs/swarm-discovery/modality-matrix.md` | 📄 Documentation/Asset | Modality Mapping Matrix |  |
| `modules/keystone-polyphony/docs/vscode-integration.md` | 🟢 Referenced | VSCode Integration |  |
| `modules/keystone-polyphony/docs/zed-integration.md` | 🟢 Referenced | Zed Integration |  |
| `modules/keystone-polyphony/features/hooks.feature` | 🟢 Referenced | File: hooks.feature |  |
| `modules/keystone-polyphony/install.sh` | 🟢 Referenced | install.sh Provisioning script for Keystone Polyphony swarm nodes. This script is idempotent and ens |  |
| `modules/keystone-polyphony/jules_config.json` | 🟢 Referenced | File: jules_config.json |  |
| `modules/keystone-polyphony/keystone-polyphony.sh` | 🟢 Referenced | keystone-polyphony.sh Legacy entry point for Keystone Polyphony. Redirects to the unified 'polyphony |  |
| `modules/keystone-polyphony/kp` | 🟢 Referenced | usr/bin/env bash |  |
| `modules/keystone-polyphony/meta/DISCOVERIES.md` | 🟢 Referenced | Discovery Log |  |
| `modules/keystone-polyphony/polyphony` | 🟢 Referenced | usr/bin/env bash |  |
| `modules/keystone-polyphony/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `modules/keystone-polyphony/scripts/agent-boot.sh` | 🔴 Orphan | bin/bash |  |
| `modules/keystone-polyphony/scripts/broadcast.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** main |
| `modules/keystone-polyphony/scripts/deduplicate.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** main |
| `modules/keystone-polyphony/scripts/dispatch-work-order.sh` | 🟢 Referenced | scripts/dispatch-work-order.sh Dispatch a work order to multiple agents in parallel. Usage: ./script |  |
| `modules/keystone-polyphony/scripts/exchange_ssh_keys.py` | 🟢 Referenced | File: exchange_ssh_keys.py | **Functions:** main |
| `modules/keystone-polyphony/scripts/inject-secrets.sh` | 🟢 Referenced | scripts/inject-secrets.sh |  |
| `modules/keystone-polyphony/scripts/install-hooks.sh` | 🟢 Referenced | usr/bin/env bash |  |
| `modules/keystone-polyphony/scripts/lint.sh` | 🟢 Referenced | usr/bin/env bash |  |
| `modules/keystone-polyphony/scripts/load_test.py` | 🟢 Referenced | File: load_test.py | **Classes:** LoadTestAgent<br>**Functions:** main, __init__, start, stop, run |
| `modules/keystone-polyphony/scripts/package.json` | 🟢 Referenced | File: package.json |  |
| `modules/keystone-polyphony/scripts/ping.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** main |
| `modules/keystone-polyphony/scripts/refine_issue.py` | 🟢 Referenced | File: refine_issue.py | **Functions:** main |
| `modules/keystone-polyphony/scripts/run-tests.sh` | 🟢 Referenced | usr/bin/env bash |  |
| `modules/keystone-polyphony/scripts/setup-ensemble.sh` | 🟢 Referenced | scripts/setup-ensemble.sh |  |
| `modules/keystone-polyphony/scripts/setup-swarm.js` | 🟢 Referenced | File: setup-swarm.js |  |
| `modules/keystone-polyphony/scripts/setup-vscode.sh` | 🟢 Referenced | usr/bin/env bash |  |
| `modules/keystone-polyphony/scripts/setup-zed.sh` | 🟢 Referenced | usr/bin/env bash |  |
| `modules/keystone-polyphony/scripts/share.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** main |
| `modules/keystone-polyphony/scripts/status.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** main |
| `modules/keystone-polyphony/scripts/swarm_status.py` | 🟢 Referenced | File: swarm_status.py | **Functions:** main |
| `modules/keystone-polyphony/scripts/triage-dispatch.sh` | 🟢 Referenced | Dispatch triage for a single file Usage: ./scripts/triage-dispatch.sh <file> <repo> |  |
| `modules/keystone-polyphony/scripts/triage-lib.sh` | 🟢 Referenced | Library of functions for issue triage |  |
| `modules/keystone-polyphony/scripts/worker_loop.py` | 🔴 Orphan | File: worker_loop.py | **Functions:** main, on_command |
| `modules/keystone-polyphony/simulate_swarm.py` | 🟢 Referenced | Ensure we can import local modules | **Functions:** run_sim_agent, main |
| `modules/keystone-polyphony/simulation.log` | 🟢 Referenced | File: simulation.log |  |
| `modules/keystone-polyphony/src/liminal_bridge/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `modules/keystone-polyphony/src/liminal_bridge/architect.py` | 🟢 Referenced | File: architect.py | **Classes:** Architect<br>**Functions:** __init__, consult, deduplicate_backlog, refine_issue, is_configured... |
| `modules/keystone-polyphony/src/liminal_bridge/crdt.py` | 🟢 Referenced | File: crdt.py | **Classes:** CRDT, LWWRegister, PNCounter, GSet, ORSet<br>**Functions:** compare_vcs, merge, value, to_dict, from_dict... |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard.py` | 🟢 Referenced | File: dashboard.py | **Classes:** DashboardServer<br>**Functions:** __init__, _init_auth_db, _generate_invite_code, _setup_routes, add_cors_headers... |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/index.html` | 🟢 Referenced | File: index.html |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/package.json` | 🟢 Referenced | File: package.json |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/App.css` | 🟢 Referenced | root { |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/App.jsx` | 🟢 Referenced | File: App.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components/Backlog.jsx` | 🔴 Orphan | File: Backlog.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components/Batons.jsx` | 🔴 Orphan | File: Batons.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components/Discussions.jsx` | 🔴 Orphan | File: Discussions.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components/KVStore.jsx` | 🔴 Orphan | File: KVStore.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components/Login.jsx` | 🔴 Orphan | File: Login.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components/Logs.jsx` | 🔴 Orphan | File: Logs.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components/NetworkGraph.jsx` | 🔴 Orphan | File: NetworkGraph.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components/Status.jsx` | 🔴 Orphan | File: Status.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components/Thoughts.jsx` | 🔴 Orphan | File: Thoughts.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/crypto.js` | 🔴 Orphan | File: crypto.js |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/index.css` | 🟢 Referenced | File: index.css |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/main.jsx` | 🟢 Referenced | File: main.jsx |  |
| `modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/vite.config.js` | 🔴 Orphan | https://vitejs.dev/config/ |  |
| `modules/keystone-polyphony/src/liminal_bridge/mesh.py` | 🟢 Referenced | File: mesh.py | **Classes:** LiminalMesh<br>**Functions:** __init__, _periodic_snapshot, _periodic_gossip, is_warming_up, get_warmup_status... |
| `modules/keystone-polyphony/src/liminal_bridge/observability.py` | 🟢 Referenced | File: observability.py | **Classes:** LogAggregator<br>**Functions:** __init__, add_log, get_logs |
| `modules/keystone-polyphony/src/liminal_bridge/pulse.py` | 🟢 Referenced | File: pulse.py | **Classes:** Pulse<br>**Functions:** _serialize_for_json, __init__, trigger, on_baton_release |
| `modules/keystone-polyphony/src/liminal_bridge/server.py` | 🟢 Referenced | File: server.py | **Functions:** handle_command_request, ensure_mesh, check_warmup, set_status, broadcast_command... |
| `modules/keystone-polyphony/src/liminal_bridge/sidecar/bridge.js` | 🟢 Referenced | File: bridge.js |  |
| `modules/keystone-polyphony/src/liminal_bridge/sidecar/package.json` | 🟢 Referenced | File: package.json |  |
| `modules/keystone-polyphony/src/liminal_bridge/test_architect.py` | 🧪 Test | File: test_architect.py | **Functions:** test_architect_detects_openai, test_architect_detects_google, test_architect_detects_anthropic, test_consult_anthropic |
| `modules/keystone-polyphony/src/liminal_bridge/test_key_rotation.py` | 🧪 Test | File: test_key_rotation.py | **Functions:** test_rotate_key_logic, test_rotate_key_immediate |
| `modules/keystone-polyphony/src/liminal_bridge/test_mesh.py` | 🧪 Test | File: test_mesh.py | **Functions:** mesh, test_mesh_baton_local, test_mesh_baton_denial, test_kv_store, test_snapshot_creation... |
| `modules/keystone-polyphony/tests/issue_19_verification.txt` | 🧪 Test | File: issue_19_verification.txt |  |
| `modules/keystone-polyphony/tests/test_activation.sh` | 🧪 Test | tests/test_activation.sh |  |
| `modules/keystone-polyphony/tests/test_architect_commands.py` | 🟢 Referenced | File: test_architect_commands.py | **Functions:** _run_pulse_broadcasts_architect_commands, test_pulse_broadcasts_architect_commands, mock_broadcast |
| `modules/keystone-polyphony/tests/test_architect_ollama.py` | 🧪 Test | File: test_architect_ollama.py | **Functions:** test_architect_detects_ollama_provider_via_env, test_architect_detects_ollama_provider_via_model_prefix, test_consult_ollama, test_refine_issue_ollama |
| `modules/keystone-polyphony/tests/test_attenuation.py` | 🧪 Test | File: test_attenuation.py | **Functions:** mesh, test_contextual_attenuation_filtering, test_broadcast_attenuation |
| `modules/keystone-polyphony/tests/test_crdt.py` | 🧪 Test | v1 > v2 | **Functions:** test_compare_vcs, test_lww_register_merge, test_pn_counter, test_g_set, test_or_set... |
| `modules/keystone-polyphony/tests/test_ensemble_chat.py` | 🟢 Referenced | File: test_ensemble_chat.py | **Functions:** test_chat |
| `modules/keystone-polyphony/tests/test_fallback.py` | 🧪 Test | File: test_fallback.py | **Functions:** mesh, test_mesh_health_degradation, test_fallback_logic_trigger |
| `modules/keystone-polyphony/tests/test_install.sh` | 🧪 Test | tests/test_install.sh |  |
| `modules/keystone-polyphony/tests/test_mesh_crdt.py` | 🧪 Test | File: test_mesh_crdt.py | **Functions:** mesh_a, mesh_b, test_update_kv_lww, test_update_counter, test_update_set... |
| `modules/keystone-polyphony/tests/test_mesh_encryption.py` | 🧪 Test | File: test_mesh_encryption.py | **Functions:** mesh_node, test_encryption_key_generation, test_broadcast_encrypts_payload, test_receive_decrypts_payload, test_receive_unencrypted_payload_ignored_or_processed... |
| `modules/keystone-polyphony/tests/test_network_simulation.py` | 🟢 Referenced | File: test_network_simulation.py | **Classes:** NetworkSimulator, MockMesh<br>**Functions:** simulator, mesh_a, mesh_b, test_basic_connectivity, test_latency... |
| `modules/keystone-polyphony/tests/test_ssh_exchange.py` | 🟢 Referenced | File: test_ssh_exchange.py | **Functions:** test_ssh_exchange_logic, run_test |
| `modules/keystone-polyphony/tests/test_stigmergy.py` | 🧪 Test | File: test_stigmergy.py | **Functions:** mesh, test_stigmergy_markers, test_get_markers_by_location |
| `modules/keystone-polyphony/tests/test_tandem.py` | 🧪 Test | File: test_tandem.py | **Functions:** mesh, test_tandem_sync_broadcast, test_tandem_sync_callback |
| `modules/keystone-polyphony/tests/test_tasks.py` | 🧪 Test | File: test_tasks.py | **Functions:** mesh, test_capability_advertising, test_task_picking |
| `modules/keystone-polyphony/tests/test_unread_tracking.py` | 🧪 Test | File: test_unread_tracking.py | **Functions:** test_unread_tracking |
| `modules/keystone-polyphony/tests/test_vector_clock.py` | 🧪 Test | File: test_vector_clock.py | **Functions:** mesh_a, mesh_b, test_vector_clock_initialization, test_vector_clock_update_kv, test_receive_update_respects_causality... |
| `mypy.ini` | 🔵 Entry Point | File: mypy.ini |  |
| `nerv_ui.patch` | 🔴 Orphan | File: nerv_ui.patch |  |
| `ontology.yaml` | 🟢 Referenced | File: ontology.yaml |  |
| `os-image/README.md` | 🟢 Referenced | Bootable Pipecat Cluster ISO Configuration |  |
| `os-image/build_iso.sh` | 🟢 Referenced | Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster. |  |
| `os-image/config/archives/rocm.key.binary` | 🔴 Orphan | File: rocm.key.binary |  |
| `os-image/config/archives/rocm.key.chroot` | 🔴 Orphan | File: rocm.key.chroot |  |
| `os-image/config/archives/rocm.list.binary` | 🔴 Orphan | File: rocm.list.binary |  |
| `os-image/config/archives/rocm.list.chroot` | 🔴 Orphan | File: rocm.list.chroot |  |
| `os-image/config/hooks/live/01-setup-users.chroot` | 🔴 Orphan | bin/sh |  |
| `os-image/config/hooks/live/02-enable-services.chroot` | 🔴 Orphan | bin/sh |  |
| `os-image/config/hooks/live/03-setup-command-deck.chroot` | 🔴 Orphan | bin/sh |  |
| `os-image/config/includes.chroot/etc/profile.d/99-pipecat-welcome.sh` | 🔴 Orphan | Wait up to 10 seconds for an IP address |  |
| `os-image/config/includes.chroot/etc/sddm.conf.d/autologin.conf` | 🔴 Orphan | File: autologin.conf |  |
| `os-image/config/includes.chroot/etc/systemd/system/multi-user.target.wants/pipecat-firstboot.service` | 🔴 Orphan | File: pipecat-firstboot.service |  |
| `os-image/config/includes.chroot/etc/systemd/system/pipecat-firstboot.service` | 🔴 Orphan | File: pipecat-firstboot.service |  |
| `os-image/config/includes.chroot/etc/systemd/system/pipecat-hostname.service` | 🟢 Referenced | File: pipecat-hostname.service |  |
| `os-image/config/includes.chroot/usr/local/bin/command-deck-session` | 🟢 Referenced | bin/bash |  |
| `os-image/config/includes.chroot/usr/local/bin/setup-ssh-keys.sh` | 🟢 Referenced | Fetches SSH keys from a provided GitHub username |  |
| `os-image/config/includes.chroot/usr/share/wayland-sessions/command-deck.desktop` | 🔴 Orphan | File: command-deck.desktop |  |
| `os-image/config/includes.installer/preseed.cfg` | 🟢 Referenced | Default Locale and Keyboard |  |
| `os-image/config/package-lists/pipecat.list.chroot` | 🔴 Orphan | File: pipecat.list.chroot |  |
| `package.json` | 🟢 Referenced | File: package.json |  |
| `performance_benchmark.py` | 🔴 Orphan | File: performance_benchmark.py | **Classes:** SyncLLMClient, CurrentAsyncLLMClient, MockAsyncResponse<br>**Functions:** benchmark_sync, benchmark_async, mock_response, run_benchmarks, __init__... |
| `pipecat-agent-extension/README.md` | 🟢 Referenced | Pipecat Agent Extension |  |
| `pipecat-agent-extension/commands/pipecat/send.toml` | 🟢 Referenced | File: send.toml |  |
| `pipecat-agent-extension/example.ts` | 🟢 Referenced | File: example.ts |  |
| `pipecat-agent-extension/gemini-extension.json` | 🟢 Referenced | File: gemini-extension.json |  |
| `pipecat-agent-extension/package.json` | 🟢 Referenced | File: package.json |  |
| `pipecat-agent-extension/tsconfig.json` | 🟢 Referenced | File: tsconfig.json |  |
| `pipecatapp/Dockerfile` | 🟢 Referenced | Use an official Python runtime as a parent image |  |
| `pipecatapp/README.md` | 🟢 Referenced | Docker Pipecat App |  |
| `pipecatapp/TODO.md` | 🟢 Referenced | VR Mission Control TODO |  |
| `pipecatapp/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/agent_factory.py` | 🟢 Referenced | File: agent_factory.py | **Functions:** create_tools |
| `pipecatapp/api_keys.py` | 🟢 Referenced | File: api_keys.py | **Functions:** generate_api_key, get_api_key_hash, initialize_api_keys, get_api_key |
| `pipecatapp/app.py` | 🟢 Referenced | Set config dir before importing ultralytics to avoid permission errors | **Classes:** AudioFileFrame, WebSocketLogHandler, UILogger, BenchmarkCollector, WyomingSTTService, FasterWhisperSTTService, GroqSTTService, KokoroTTSService, PiperTTSService, WebsocketAudioStreamer, YOLOv8Detector, TextMessageInjector, TwinService, VisionUnavailable<br>**Functions:** suppress_stderr, find_workable_audio_input_device, discover_services, discover_main_llm_service, initialize_vision_detector... |
| `pipecatapp/archivist_service.py` | 🟢 Referenced | File: archivist_service.py | **Classes:** Page, DeepResearchRequest, LLMClient, Memorizer, Researcher<br>**Functions:** lifespan, research_endpoint, health_check, __init__, close... |
| `pipecatapp/datasets/sycophancy_prompts.json` | 🟢 Referenced | File: sycophancy_prompts.json |  |
| `pipecatapp/durable_execution.py` | 🟢 Referenced | File: durable_execution.py | **Classes:** InvocationStatus, DurableExecutionEngine<br>**Functions:** _pre_execution, _post_execution, durable_step, __init__, _ensure_db_dir... |
| `pipecatapp/expert_tracker.py` | 🟢 Referenced | File: expert_tracker.py | **Classes:** ExpertTracker<br>**Functions:** __init__, register_expert, record_success, record_failure, get_metrics_for_prompt... |
| `pipecatapp/file_ingestion.py` | 🟢 Referenced | File: file_ingestion.py | **Classes:** LocalFileIngestor<br>**Functions:** __init__, is_safe_path, ingest_file, process_inbox |
| `pipecatapp/generate_real_embeddings.py` | 🟢 Referenced | File: generate_real_embeddings.py | **Functions:** get_longformer_embedding |
| `pipecatapp/gossip_discovery.py` | 🟢 Referenced | File: gossip_discovery.py | **Classes:** SimpleBloomFilter, GossipDiscovery, GossipProtocol<br>**Functions:** __init__, add, check, to_hex, from_hex... |
| `pipecatapp/integrations/__init__.py` | 🟢 Referenced | This package contains integration modules for external services (e.g., OpenClaw). |  |
| `pipecatapp/integrations/openclaw.py` | 🟢 Referenced | File: openclaw.py | **Classes:** OpenClawClient<br>**Functions:** __init__, connect, disconnect, _listen, _handle_message... |
| `pipecatapp/janitor_agent.py` | 🟢 Referenced | File: janitor_agent.py | **Classes:** JanitorAgent<br>**Functions:** __init__, discover_services, process_item, run, stop |
| `pipecatapp/judge_agent.py` | 🟢 Referenced | File: judge_agent.py | **Classes:** JudgeAgent<br>**Functions:** __init__, discover_services, initialize_tools, report_event, call_llm... |
| `pipecatapp/langchain_memory_wrappers.py` | 🟢 Referenced | File: langchain_memory_wrappers.py | **Classes:** PMMChatMessageHistory, PipecatVectorStore<br>**Functions:** __init__, messages, add_message, clear, __init__... |
| `pipecatapp/llm_clients.py` | 🟢 Referenced | File: llm_clients.py | **Classes:** ExternalLLMClient<br>**Functions:** __init__, close, process_text |
| `pipecatapp/local_llm.py` | 🟢 Referenced | File: local_llm.py | **Classes:** LocalLLMService, Settings<br>**Functions:** __init__, _process_context, run_inference |
| `pipecatapp/local_world_model.py` | 🟢 Referenced | File: local_world_model.py | **Classes:** LocalWorldModel<br>**Functions:** __new__, __init__, load_static_definitions, refresh_state, get_state... |
| `pipecatapp/manager_agent.py` | 🟢 Referenced | File: manager_agent.py | **Classes:** ManagerAgent<br>**Functions:** __init__, discover_services, call_llm, get_agent_suitability, map_phase... |
| `pipecatapp/memory.py` | 🟢 Referenced | File: memory.py | **Classes:** Document, MemoryStore<br>**Functions:** to_dict, __init__, add, force_save, search... |
| `pipecatapp/memory_backends.py` | 🟢 Referenced | File: memory_backends.py | **Classes:** BaseMemoryBackend<br>**Functions:** add, force_save, search, add_memory, get_memory... |
| `pipecatapp/memory_backends_impl/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/memory_backends_impl/crdt_backend.py` | 🟢 Referenced | File: crdt_backend.py | **Classes:** BasicORSet, CRDTMemoryBackend<br>**Functions:** __init__, add, remove, merge, value... |
| `pipecatapp/memory_backends_impl/helix_backend.py` | 🟢 Referenced | File: helix_backend.py | **Classes:** HelixMemoryBackend<br>**Functions:** __init__, add, force_save, search, add_memory... |
| `pipecatapp/memory_backends_impl/helix_client.py` | 🟢 Referenced | File: helix_client.py | **Classes:** HelixClient<br>**Functions:** __init__, _post, execute_ast |
| `pipecatapp/memory_graph_service/Dockerfile` | 🟢 Referenced | Install dependencies |  |
| `pipecatapp/memory_graph_service/helix_server.py` | 🟢 Referenced | File: helix_server.py | **Functions:** lifespan, _post, store_memory, create_relationship, recall_memories... |
| `pipecatapp/memory_graph_service/server.py` | 🟢 Referenced | File: server.py | **Functions:** lifespan, store_memory, create_relationship, recall_memories, search_memories |
| `pipecatapp/memory_legacy.py` | 🟢 Referenced | File: memory_legacy.py | **Classes:** Document, MemoryStore<br>**Functions:** to_dict, __init__, _load_index, _load_store, _save... |
| `pipecatapp/models.py` | 🟢 Referenced | File: models.py | **Classes:** InternalChatRequest, SystemMessageRequest<br>**Functions:** check_content_present |
| `pipecatapp/moondream_detector.py` | 🟢 Referenced | File: moondream_detector.py | **Classes:** MoondreamDetector<br>**Functions:** __init__, process_frame, get_observation |
| `pipecatapp/mqtt_world_model_client.py` | 🟢 Referenced | File: mqtt_world_model_client.py | **Classes:** MQTTWorldModelClient<br>**Functions:** __init__, get_state, dispatch_job |
| `pipecatapp/mtac/eval_sft.py` | 🟢 Referenced | File: eval_sft.py | **Functions:** write_telemetry, main |
| `pipecatapp/mtac/torchtune_sft.py` | 🟢 Referenced | File: torchtune_sft.py | **Functions:** write_telemetry, main |
| `pipecatapp/mtac/unsloth_sft.py` | 🟢 Referenced | File: unsloth_sft.py | **Classes:** TelemetryCallback<br>**Functions:** main, __init__, on_log |
| `pipecatapp/mtac_pipeline.py` | 🟢 Referenced | File: mtac_pipeline.py | **Classes:** MTACPipelineOrchestrator<br>**Functions:** __init__, close, _get_session, _generate_job_def, _dispatch_job... |
| `pipecatapp/net_utils.py` | 🟢 Referenced | File: net_utils.py | **Functions:** ensure_ipv6_brackets, format_url, _validate_url_logic, validate_url, resolve_and_validate_url... |
| `pipecatapp/network_scanner.py` | 🟢 Referenced | File: network_scanner.py | **Functions:** check_llm_service, get_local_ip, scan_network_for_llms |
| `pipecatapp/nomad_templates/immich.nomad.hcl` | 🔵 Entry Point | File: immich.nomad.hcl |  |
| `pipecatapp/nomad_templates/readeck.nomad.hcl` | 🔵 Entry Point | File: readeck.nomad.hcl |  |
| `pipecatapp/nomad_templates/uptime-kuma.nomad.hcl` | 🔵 Entry Point | File: uptime-kuma.nomad.hcl |  |
| `pipecatapp/nomad_templates/vaultwarden.nomad.hcl` | 🔵 Entry Point | File: vaultwarden.nomad.hcl |  |
| `pipecatapp/ontology.py` | 🟢 Referenced | File: ontology.py | **Classes:** Device, Occupant, Location, Agent, Node, Cluster, WorldOntology<br> |
| `pipecatapp/pmm_memory.py` | 🟢 Referenced | File: pmm_memory.py | **Classes:** PMMMemory<br>**Functions:** __init__, _init_db, _get_last_hash, _calculate_hash, add_event_sync... |
| `pipecatapp/pmm_memory_client.py` | 🟢 Referenced | File: pmm_memory_client.py | **Classes:** PMMMemoryClient<br>**Functions:** __init__, add_event_sync, add_event, get_events_sync, get_events... |
| `pipecatapp/prompts/coding_expert.txt` | 🟢 Referenced | File: coding_expert.txt |  |
| `pipecatapp/prompts/consolidation_expert.txt` | 🔴 Orphan | File: consolidation_expert.txt |  |
| `pipecatapp/prompts/creative_expert.txt` | 🟢 Referenced | File: creative_expert.txt |  |
| `pipecatapp/prompts/ingestion_expert.txt` | 🔴 Orphan | File: ingestion_expert.txt |  |
| `pipecatapp/prompts/memory_query_expert.txt` | 🔴 Orphan | File: memory_query_expert.txt |  |
| `pipecatapp/prompts/router.txt` | 🟢 Referenced | File: router.txt |  |
| `pipecatapp/prompts/tron_agent.txt` | 🟢 Referenced | File: tron_agent.txt |  |
| `pipecatapp/quality_control.py` | 🟢 Referenced | File: quality_control.py | **Classes:** ExpectimaxAgent, CodeQualityAnalyzer<br>**Functions:** __init__, decide, __init__, analyze |
| `pipecatapp/rate_limiter.py` | 🟢 Referenced | File: rate_limiter.py | **Classes:** RateLimiter<br>**Functions:** __init__, __call__, _cleanup |
| `pipecatapp/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `pipecatapp/resources/skills/backpass.md` | 🟢 Referenced | File: backpass.md |  |
| `pipecatapp/resources/skills/renovate.md` | 🟢 Referenced | File: renovate.md |  |
| `pipecatapp/resources/skills/scaffold-setup-skill.md` | 🟢 Referenced | File: scaffold-setup-skill.md |  |
| `pipecatapp/router_config.yaml` | 🟢 Referenced | File: router_config.yaml |  |
| `pipecatapp/router_train_embeddings.pt` | 🟢 Referenced | File: router_train_embeddings.pt |  |
| `pipecatapp/router_trained_model.pkl` | 🟢 Referenced | File: router_trained_model.pkl |  |
| `pipecatapp/router_training_data.csv` | 🔴 Orphan | File: router_training_data.csv |  |
| `pipecatapp/router_training_data.jsonl` | 🟢 Referenced | File: router_training_data.jsonl |  |
| `pipecatapp/secret_manager.py` | 🟢 Referenced | File: secret_manager.py | **Classes:** SecretManager<br>**Functions:** __new__, initialize_from_env, get_secret, set_secret, get_all_secrets |
| `pipecatapp/security.py` | 🟢 Referenced | File: security.py | **Functions:** _redact_cached, _redact_impl, redact_sensitive_data, redact_sensitive_data_stream, escape_html_content... |
| `pipecatapp/servers/shell_server.py` | 🟢 Referenced | File: shell_server.py | **Functions:** _ensure_session, execute_command |
| `pipecatapp/services/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/services/code_runner/Dockerfile` | 🟢 Referenced | Install system dependencies. Docker is sometimes needed for local mode code execution |  |
| `pipecatapp/services/code_runner/code_runner_server.py` | 🟢 Referenced | File: code_runner_server.py | **Classes:** ExecuteCodeRequest<br>**Functions:** verify_token, startup_event, execute_code |
| `pipecatapp/services/gemma_e2b_service.py` | 🟢 Referenced | File: gemma_e2b_service.py | **Classes:** GemmaE2BService<br>**Functions:** _resolve_model_path, __init__, _load_model, process_frame, _generate_response... |
| `pipecatapp/services/ipfs_apt_proxy/Dockerfile` | 🟢 Referenced | File: Dockerfile |  |
| `pipecatapp/services/ipfs_apt_proxy/main.py` | 🟢 Referenced | File: main.py | **Functions:** init_db, get_cid_for_url, save_cid_for_url, handle, fetch_and_stream |
| `pipecatapp/services/ipfs_apt_proxy/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `pipecatapp/services/ipfs_pypi_proxy/Dockerfile` | 🟢 Referenced | File: Dockerfile |  |
| `pipecatapp/services/ipfs_pypi_proxy/main.py` | 🟢 Referenced | File: main.py | **Functions:** init_db, get_cid_for_filename, save_cid_for_filename, index, simple_index... |
| `pipecatapp/services/ipfs_pypi_proxy/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `pipecatapp/services/obsidian_gardener.py` | 🟢 Referenced | File: obsidian_gardener.py | **Classes:** ObsidianGardener<br>**Functions:** __init__, _should_process, on_modified, on_created, _handle_file_change... |
| `pipecatapp/services/push_proxy/README.md` | 🟢 Referenced | PUSH-style Reverse Proxy for NAT Traversal |  |
| `pipecatapp/services/push_proxy/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/services/push_proxy/client.py` | 🟢 Referenced | File: client.py | **Classes:** PushProxyClient<br>**Functions:** __init__, connect_and_serve, forward_local_to_proxy |
| `pipecatapp/services/push_proxy/server.py` | 🟢 Referenced | File: server.py | **Classes:** PushProxyServer<br>**Functions:** __init__, handle_worker_connection, handle_tunnel_connection, start, forward |
| `pipecatapp/services/rag/Dockerfile` | 🟢 Referenced | Install system dependencies |  |
| `pipecatapp/services/rag/rag_server.py` | 🟢 Referenced | File: rag_server.py | **Classes:** AddDocumentRequest, SearchRequest, ScanDirectoryRequest<br>**Functions:** verify_token, startup_event, add_document, search, scan_directory |
| `pipecatapp/services/ternlight/Dockerfile` | 🟢 Referenced | File: Dockerfile |  |
| `pipecatapp/services/ternlight/package.json` | 🟢 Referenced | File: package.json |  |
| `pipecatapp/services/ternlight/ternlight_server.js` | 🟢 Referenced | File: ternlight_server.js |  |
| `pipecatapp/skill_library.py` | 🟢 Referenced | File: skill_library.py | **Classes:** SkillLibrary<br>**Functions:** __init__, _init_sqlite, save_skill, search_skills, get_skill |
| `pipecatapp/start_archivist.sh` | 🟢 Referenced | bin/bash |  |
| `pipecatapp/static/cluster.html` | 🟢 Referenced | File: cluster.html |  |
| `pipecatapp/static/cluster_viz.html` | 🟢 Referenced | A-Frame |  |
| `pipecatapp/static/css/litegraph.css` | 🟢 Referenced | File: litegraph.css |  |
| `pipecatapp/static/css/styles.css` | 🟢 Referenced | sidebar { |  |
| `pipecatapp/static/index.html` | 🟢 Referenced | File: index.html |  |
| `pipecatapp/static/js/dagre.min.js` | 🟢 Referenced | File: dagre.min.js |  |
| `pipecatapp/static/js/editor.js` | 🟢 Referenced | Editor logic using LiteGraph.js |  |
| `pipecatapp/static/js/litegraph.js` | 🟢 Referenced | packer version |  |
| `pipecatapp/static/js/ternlight_client.js` | 🟢 Referenced | File: ternlight_client.js |  |
| `pipecatapp/static/js/workflow.js` | 🟢 Referenced | File: workflow.js |  |
| `pipecatapp/static/monitor.html` | 🟢 Referenced | File: monitor.html |  |
| `pipecatapp/static/terminal.js` | 🟢 Referenced | Support authenticating via API key in localStorage |  |
| `pipecatapp/static/vr_index.html` | 🟢 Referenced | A-Frame |  |
| `pipecatapp/static/workflow.html` | 🟢 Referenced | File: workflow.html |  |
| `pipecatapp/static/workflow_3d.html` | 🟢 Referenced | File: workflow_3d.html |  |
| `pipecatapp/task_supervisor.py` | 🟢 Referenced | File: task_supervisor.py | **Classes:** TaskSupervisor<br>**Functions:** __init__, start, _check_tasks |
| `pipecatapp/technician_agent.py` | 🟢 Referenced | File: technician_agent.py | **Classes:** TechnicianAgent<br>**Functions:** __init__, rehydrate_and_resume, discover_services, initialize_tools, report_event... |
| `pipecatapp/test_moondream_detector.py` | 🟢 Referenced | File: test_moondream_detector.py | **Functions:** mock_torch, mock_auto_model, test_initialization, test_process_frame, test_process_frame_error... |
| `pipecatapp/test_pmm_memory.py` | 🧪 Test | File: test_pmm_memory.py | **Functions:** memory, test_dlq_lifecycle, test_dlq_filtering, test_dlq_retry_mechanics |
| `pipecatapp/test_server.py` | 🟢 Referenced | File: test_server.py |  |
| `pipecatapp/tests/test_audio_streamer.py` | 🧪 Test | File: test_audio_streamer.py | **Classes:** TestWebsocketAudioStreamer<br>**Functions:** test_websocket_audio_streamer_wav_header |
| `pipecatapp/tests/test_browser_tool_security.py` | 🧪 Test | File: test_browser_tool_security.py | **Functions:** test_ssrf_protection, test_valid_urls |
| `pipecatapp/tests/test_container_registry_tool.py` | 🧪 Test | File: test_container_registry_tool.py | **Classes:** TestContainerRegistryTool<br>**Functions:** setUp, test_discover_registry_consul_success, test_discover_registry_consul_failure, test_list_repositories_success, test_list_tags_success... |
| `pipecatapp/tests/test_cq_tool.py` | 🧪 Test | File: test_cq_tool.py | **Functions:** test_cq_query, test_cq_propose, test_cq_confirm, test_cq_flag, test_cq_reflect |
| `pipecatapp/tests/test_document_tool.py` | 🧪 Test | File: test_document_tool.py | **Classes:** TestDocumentTool<br>**Functions:** setup_method, teardown_method, test_paperless_backend_search, test_paperless_backend_get_text, test_local_backend_search_and_get_text... |
| `pipecatapp/tests/test_gemma_e2b_service.py` | 🧪 Test | File: test_gemma_e2b_service.py | **Classes:** MockFrame, MockAudioRawFrame, MockTextFrame, MockStartFrame, MockEndFrame, MockUserImageRawFrame, MockCancelFrame, MockUserStoppedSpeakingFrame, MockFrameDirection, MockFrameProcessor<br>**Functions:** mock_engine, test_gemma_service_initialization, test_gemma_service_start_frame, test_gemma_service_audio_accumulation, test_gemma_service_processing... |
| `pipecatapp/tests/test_git_tool_security.py` | 🧪 Test | File: test_git_tool_security.py | **Classes:** TestGitToolSecurity<br>**Functions:** setup_method, test_diff_security, test_branch_security, test_checkout_security, test_merge_security... |
| `pipecatapp/tests/test_llm_clients.py` | 🧪 Test | File: test_llm_clients.py | **Functions:** test_ds4_think_stripping, test_no_think_stripping |
| `pipecatapp/tests/test_llm_clients_new.py` | 🧪 Test | File: test_llm_clients_new.py | **Classes:** MockAsyncResponse<br>**Functions:** test_external_llm_client_success, test_external_llm_client_missing_key, test_external_llm_client_error, __init__, __aenter__... |
| `pipecatapp/tests/test_metrics_cache.py` | 🧪 Test | File: test_metrics_cache.py | **Functions:** test_metrics_caching_behavior |
| `pipecatapp/tests/test_net_utils.py` | 🧪 Test | File: test_net_utils.py | **Classes:** TestNetUtils, TestValidateUrl<br>**Functions:** test_ensure_ipv6_brackets, test_format_url, test_validate_url_public, test_validate_url_private, test_validate_url_localhost... |
| `pipecatapp/tests/test_new_skills.py` | 🧪 Test | File: test_new_skills.py | **Functions:** skill_lib, test_skill_ingestion_and_retrieval, test_set_operational_mode_tool, test_lightweight_mapper, test_project_mapper_interface_consistency |
| `pipecatapp/tests/test_openclaw.py` | 🧪 Test | File: test_openclaw.py | **Functions:** test_openclaw_client_handshake_and_send, test_openclaw_tool, mock_iter, mock_send |
| `pipecatapp/tests/test_ouroboros.py` | 🧪 Test | Mock dependencies before importing web_server | **Functions:** test_webring_routes, test_webring_navigation |
| `pipecatapp/tests/test_piper_async.py` | 🧪 Test | File: test_piper_async.py | **Classes:** MockFrameProcessor, MockTextFrame<br>**Functions:** test_piper_tts_async_execution, side_effect_synthesize, __init__, push_frame, __init__ |
| `pipecatapp/tests/test_proxy_security.py` | 🧪 Test | File: test_proxy_security.py | **Functions:** test_proxy_headers_respected_when_configured, test_proxy_headers_ignored_when_disabled, get_ip, get_ip |
| `pipecatapp/tests/test_rag_pruning.py` | 🧪 Test | File: test_rag_pruning.py | **Functions:** setup_mocks, mock_llm_client, pruner, test_rag_pruner_grading, test_rag_pruner_json_extraction... |
| `pipecatapp/tests/test_rag_tool.py` | 🟢 Referenced | File: test_rag_tool.py | **Classes:** MockPMMMemory<br>**Functions:** rag_tool_class, mock_memory, mock_thread, test_dirs, test_rag_scope_security... |
| `pipecatapp/tests/test_rate_limiter.py` | 🟢 Referenced | File: test_rate_limiter.py | **Classes:** MockClient, MockRequest<br>**Functions:** test_rate_limiter, test_rate_limiter_cleanup, sample_endpoint |
| `pipecatapp/tests/test_security.py` | 🟢 Referenced | Ensure pipecatapp is in path | **Functions:** test_redact_openai_key, test_redact_github_key, test_redact_bearer_token, test_redact_gitlab_key, test_redact_url_credentials |
| `pipecatapp/tests/test_stt_optimization.py` | 🧪 Test | File: test_stt_optimization.py | **Classes:** MockFrameProcessor, TestFasterWhisperSTTService<br>**Functions:** __init__, push_frame, test_convert_audio_bytes_to_float_array, test_transcribe_sync_refactoring, original_logic |
| `pipecatapp/tests/test_technician_agent.py` | 🧪 Test | File: test_technician_agent.py | **Functions:** mock_agent, test_phase_1_plan, test_phase_2_execute_success, test_phase_2_execute_with_tool_call, test_phase_3_reflect... |
| `pipecatapp/tests/test_tool_server.py` | 🧪 Test | File: test_tool_server.py | **Classes:** TestToolServer<br>**Functions:** test_run_tool_valid_auth, test_run_tool_invalid_auth, test_run_tool_missing_auth |
| `pipecatapp/tests/test_uilogger_redaction.py` | 🟢 Referenced | File: test_uilogger_redaction.py | **Classes:** MockTextFrame, MockFrameProcessor<br>**Functions:** test_uilogger_redaction_verification, __init__, __init__, push_frame, run_test |
| `pipecatapp/tests/test_web_server_unit.py` | 🧪 Test | File: test_web_server_unit.py | **Functions:** test_health_check_init, test_health_check_ready, test_web_ui_routes, test_cluster_metrics, test_active_workflows_sanitization... |
| `pipecatapp/tests/test_websocket_security.py` | 🟢 Referenced | Mock out heavy dependencies that cause timeouts during import | **Functions:** test_websocket_accepts_trusted_origin, test_websocket_rejects_untrusted_origin, test_websocket_allows_wildcard, test_websocket_default_secure_same_origin_success, test_websocket_default_secure_same_origin_failure... |
| `pipecatapp/tests/test_xss_prevention.py` | 🧪 Test | File: test_xss_prevention.py | **Functions:** test_workflow_history_xss |
| `pipecatapp/tests/test_yolo_optimization.py` | 🧪 Test | File: test_yolo_optimization.py | **Classes:** MockFrameProcessor, MockVisionImageRawFrame<br>**Functions:** test_yolo_inference_optimization, __init__, push_frame, __init__ |
| `pipecatapp/tests/workflow/test_history.py` | 🧪 Test | File: test_history.py | **Functions:** temp_db_path, test_workflow_history_init, test_workflow_history_singleton_init |
| `pipecatapp/tests/workflow/test_serialization_perf.py` | 🧪 Test | File: test_serialization_perf.py | **Classes:** NonSerializable<br>**Functions:** test_make_serializable_primitives, test_make_serializable_dict, test_make_serializable_list, test_make_serializable_nested, test_make_serializable_non_serializable... |
| `pipecatapp/tool_server.py` | 🟢 Referenced | File: tool_server.py | **Classes:** ToolRequest<br>**Functions:** validation_exception_handler, read_health, run_tool, list_tools |
| `pipecatapp/tools/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/tools/ansible_tool.py` | 🟢 Referenced | File: ansible_tool.py | **Classes:** Ansible_Tool<br>**Functions:** __init__, run_playbook |
| `pipecatapp/tools/archivist_tool.py` | 🟢 Referenced | File: archivist_tool.py | **Classes:** ArchivistTool<br>**Functions:** __init__, run, __call__ |
| `pipecatapp/tools/ast_editor_tool.py` | 🟢 Referenced | File: ast_editor_tool.py | **Classes:** ASTEditorTool<br>**Functions:** __init__, get_schema, execute, _validate_path, _parse_and_validate... |
| `pipecatapp/tools/atproto_tool.py` | 🟢 Referenced | File: atproto_tool.py | **Classes:** ATProtoTool<br>**Functions:** __init__, _get_client, send_post, get_timeline |
| `pipecatapp/tools/autoloop_tool.py` | 🟢 Referenced | File: autoloop_tool.py | **Classes:** AutoloopTool<br>**Functions:** __init__, run, main, local_metric |
| `pipecatapp/tools/autoresearch_tool.py` | 🟢 Referenced | File: autoresearch_tool.py | **Classes:** AutoresearchTool, MockLLM<br>**Functions:** __init__, run, _run_autoloop_backend, _call_llm, _extract_code... |
| `pipecatapp/tools/claude_clone_tool.py` | 🟢 Referenced | File: claude_clone_tool.py | **Classes:** ClaudeCloneTool<br>**Functions:** __init__, _run_command, explain, report, generate... |
| `pipecatapp/tools/cluster_status_tool.py` | 🟢 Referenced | File: cluster_status_tool.py | **Classes:** ClusterStatusTool<br>**Functions:** __init__, get_status, execute |
| `pipecatapp/tools/code_runner_tool.py` | 🟢 Referenced | File: code_runner_tool.py | **Classes:** SandboxExecutor, DockerSandboxExecutor, NomadSandboxExecutor, CodeRunnerTool, TimeoutException<br>**Functions:** execute, __init__, execute, execute_simple_python, __init__... |
| `pipecatapp/tools/container_registry_tool.py` | 🟢 Referenced | File: container_registry_tool.py | **Classes:** ContainerRegistryTool<br>**Functions:** __init__, _validate_repository, _discover_registry, list_repositories, list_tags... |
| `pipecatapp/tools/context_upload_tool.py` | 🟢 Referenced | File: context_upload_tool.py | **Classes:** ContextUploadTool<br>**Functions:** __init__, execute, get_definition |
| `pipecatapp/tools/council_tool.py` | 🟢 Referenced | File: council_tool.py | **Classes:** CouncilTool<br>**Functions:** __init__, _discover_local_experts, _query_model, convene |
| `pipecatapp/tools/cq_tool.py` | 🟢 Referenced | File: cq_tool.py | **Classes:** CQ_Tool<br>**Functions:** __init__, cq_query, cq_propose, cq_confirm, cq_flag... |
| `pipecatapp/tools/dependency_scanner_tool.py` | 🟢 Referenced | File: dependency_scanner_tool.py | **Classes:** DependencyScannerTool<br>**Functions:** __init__, _get_latest_version, scan_package |
| `pipecatapp/tools/desktop_control_tool.py` | 🟢 Referenced | File: desktop_control_tool.py | **Classes:** DesktopControlTool<br>**Functions:** __init__, get_desktop_screenshot, click_at, type_text |
| `pipecatapp/tools/document_tool.py` | 🟢 Referenced | File: document_tool.py | **Classes:** DocumentBackend, PaperlessBackend, LocalDirectoryBackend, DocumentTool<br>**Functions:** search, get_text, __init__, search, get_text... |
| `pipecatapp/tools/dynamic_skill_tool.py` | 🟢 Referenced | File: dynamic_skill_tool.py | **Classes:** DynamicSkillTool<br>**Functions:** __init__, execute |
| `pipecatapp/tools/execution_history.py` | 🟢 Referenced | File: execution_history.py | **Classes:** ExecutionHistory<br>**Functions:** __init__, _init_db, _compute_hash, record_execution, get_cached_result... |
| `pipecatapp/tools/experiment_tool.py` | 🟢 Referenced | File: experiment_tool.py | **Classes:** ExperimentTool<br>**Functions:** __init__, run, _validate_path, _create_snapshot, _extract_artifact... |
| `pipecatapp/tools/file_editor_tool.py` | 🟢 Referenced | File: file_editor_tool.py | **Classes:** FileEditorTool<br>**Functions:** __init__, get_schema, execute, _validate_path, _save_for_undo... |
| `pipecatapp/tools/final_answer_tool.py` | 🟢 Referenced | File: final_answer_tool.py | **Classes:** FinalAnswerTool<br>**Functions:** __init__, submit_task |
| `pipecatapp/tools/gemini_cli.py` | 🟢 Referenced | File: gemini_cli.py | **Functions:** send_message |
| `pipecatapp/tools/get_nomad_job.py` | 🟢 Referenced | File: get_nomad_job.py | **Functions:** get_nomad_job_definition, main |
| `pipecatapp/tools/git_tool.py` | 🟢 Referenced | File: git_tool.py | **Classes:** Git_Tool<br>**Functions:** __init__, _validate_path, _validate_arg, _validate_protocol, _run_git_command... |
| `pipecatapp/tools/ha_tool.py` | 🟢 Referenced | File: ha_tool.py | **Classes:** HA_Tool<br>**Functions:** __init__, close, _get_session, call_ai_task |
| `pipecatapp/tools/heretic_tool.py` | 🟢 Referenced | File: heretic_tool.py | **Classes:** HereticTool<br>**Functions:** __init__, align_model |
| `pipecatapp/tools/jules_tool.py` | 🟢 Referenced | File: jules_tool.py | **Classes:** JulesTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/langchain_adapter.py` | 🟢 Referenced | File: langchain_adapter.py | **Classes:** LangChainToolAdapter<br>**Functions:** __init__, _create_execution_method, wrapped_execute |
| `pipecatapp/tools/langchain_adapter_tool.py` | 🟢 Referenced | File: langchain_adapter_tool.py | **Classes:** LangChainToolAdapter<br>**Functions:** __init__, run |
| `pipecatapp/tools/lightweight_project_mapper_tool.py` | 🟢 Referenced | File: lightweight_project_mapper_tool.py | **Classes:** LightweightProjectMapperTool<br>**Functions:** __init__, _is_ignored, scan, _list_files_git, _guess_type... |
| `pipecatapp/tools/llxprt_code_tool.py` | 🟢 Referenced | File: llxprt_code_tool.py | **Classes:** LLxprt_Code_Tool<br>**Functions:** __init__, run |
| `pipecatapp/tools/mcp_client_adapter.py` | 🟢 Referenced | File: mcp_client_adapter.py | **Classes:** MCPClientAdapter<br>**Functions:** __init__, load_approvals, save_approval, check_command_safety, _ensure_connected... |
| `pipecatapp/tools/mcp_tool.py` | 🟢 Referenced | File: mcp_tool.py | **Classes:** MCP_Tool<br>**Functions:** __init__, get_status, get_memory_summary, clear_short_term_memory |
| `pipecatapp/tools/mtac_tool.py` | 🟢 Referenced | Dynamically import the pipeline orchestrator to prevent circular imports if it gets complex later | **Classes:** MTACTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/ocr_tool.py` | 🔴 Orphan | File: ocr_tool.py | **Classes:** OCRToolInput, OCRTool<br>**Functions:** __init__, _load_model, _pdf_to_images, run |
| `pipecatapp/tools/open_workers_tool.py` | 🟢 Referenced | File: open_workers_tool.py | **Classes:** OpenWorkersTool<br>**Functions:** __init__, _get_service_url, _get_api_url, run_javascript |
| `pipecatapp/tools/openclaw_tool.py` | 🟢 Referenced | File: openclaw_tool.py | **Classes:** OpenClawTool<br>**Functions:** __init__, send_message |
| `pipecatapp/tools/opencode_provider_tool.py` | 🟢 Referenced | File: opencode_provider_tool.py | **Classes:** OpenCodeProviderTool<br>**Functions:** __init__, _parse_opencode_output, run |
| `pipecatapp/tools/opencode_tool.py` | 🟢 Referenced | File: opencode_tool.py | **Classes:** OpencodeTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/orchestrator_tool.py` | 🟢 Referenced | File: orchestrator_tool.py | **Classes:** OrchestratorTool<br>**Functions:** __init__, dispatch_job |
| `pipecatapp/tools/ouroboros_tool.py` | 🟢 Referenced | File: ouroboros_tool.py | **Classes:** OuroborosTool<br>**Functions:** __init__, get_members, save_members, add_member, remove_member... |
| `pipecatapp/tools/p2p_sync_tool.py` | 🟢 Referenced | File: p2p_sync_tool.py | **Classes:** P2PSyncTool<br>**Functions:** __init__, _ensure_binary_exists, _modify_config_ports, _get_api_key, _get_device_id... |
| `pipecatapp/tools/personality_tool.py` | 🟢 Referenced | File: personality_tool.py | **Classes:** PersonalityTool<br>**Functions:** __init__, set_personality, reset_personality, get_current_personality |
| `pipecatapp/tools/planner_tool.py` | 🟢 Referenced | File: planner_tool.py | **Classes:** PlannerTool<br>**Functions:** __init__, _discover_llm_url, _call_llm, plan_and_execute |
| `pipecatapp/tools/polyphony_tool.py` | 🟢 Referenced | File: polyphony_tool.py | **Classes:** PolyphonyTool<br>**Functions:** __init__, execute, _run_cmd, get_info |
| `pipecatapp/tools/power_tool.py` | 🟢 Referenced | File: power_tool.py | **Classes:** Power_Tool<br>**Functions:** __init__, set_idle_threshold |
| `pipecatapp/tools/project_mapper_tool.py` | 🟢 Referenced | File: project_mapper_tool.py | **Classes:** ProjectMapperTool<br>**Functions:** __init__, scan, run |
| `pipecatapp/tools/project_overview_tool.py` | 🟢 Referenced | File: project_overview_tool.py | **Classes:** ProjectOverviewTool<br>**Functions:** __init__, execute |
| `pipecatapp/tools/prompt_improver_tool.py` | 🟢 Referenced | File: prompt_improver_tool.py | **Classes:** PromptImproverTool<br>**Functions:** __init__, _discover_llm, _call_llm, create_prompt_plan |
| `pipecatapp/tools/rag_tool.py` | 🟢 Referenced | File: rag_tool.py | **Classes:** RAG_Tool<br>**Functions:** _load_document_cached_internal, load_document_cached, __init__, set_scope, _build_knowledge_base... |
| `pipecatapp/tools/remote_code_runner_tool.py` | 🔴 Orphan | File: remote_code_runner_tool.py | **Classes:** RemoteCodeRunnerTool<br>**Functions:** __init__, _make_request, execute |
| `pipecatapp/tools/remote_rag_tool.py` | 🔴 Orphan | File: remote_rag_tool.py | **Classes:** RemoteRAGTool<br>**Functions:** __init__, _make_request, add_document, search, scan_directory... |
| `pipecatapp/tools/remote_tool_proxy.py` | 🟢 Referenced | File: remote_tool_proxy.py | **Classes:** RemoteToolProxy<br>**Functions:** __init__, __getattr__, method |
| `pipecatapp/tools/repo_map_impl/__init__.py` | 🟢 Referenced | repo-map: fast deterministic repository maps for agent comprehension. |  |
| `pipecatapp/tools/repo_map_impl/cache.py` | 🟢 Referenced | File: cache.py | **Classes:** TagCache<br>**Functions:** __init__, _key_path, get, set |
| `pipecatapp/tools/repo_map_impl/cli.py` | 🟢 Referenced | File: cli.py | **Functions:** main |
| `pipecatapp/tools/repo_map_impl/config.py` | 🟢 Referenced | File: config.py | **Classes:** RepoMapConfig<br>**Functions:** load_config |
| `pipecatapp/tools/repo_map_impl/discover.py` | 🟢 Referenced | File: discover.py | **Functions:** _load_gitignore_spec, _is_ignored, discover_files |
| `pipecatapp/tools/repo_map_impl/extract/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/tools/repo_map_impl/extract/python_ast.py` | 🟢 Referenced | File: python_ast.py | **Functions:** _get_name, enrich_python |
| `pipecatapp/tools/repo_map_impl/extract/tree_sitter.py` | 🟢 Referenced | File: tree_sitter.py | **Functions:** _load_language, _get_parser, _query_path, _kind_from_capture, extract_tags... |
| `pipecatapp/tools/repo_map_impl/languages.py` | 🟢 Referenced | File: languages.py | **Functions:** lang_for_path, supported_extensions |
| `pipecatapp/tools/repo_map_impl/model.py` | 🟢 Referenced | File: model.py | **Classes:** Symbol, MethodInfo, ClassInfo, FunctionInfo, ImportInfo, FileSymbols<br>**Functions:** tree_classes, tree_functions |
| `pipecatapp/tools/repo_map_impl/pipeline.py` | 🟢 Referenced | File: pipeline.py | **Functions:** _cache_dir, extract_all, generate_full_map, generate_budget_map |
| `pipecatapp/tools/repo_map_impl/queries/ATTRIBUTION.md` | 🔴 Orphan | Tag queries |  |
| `pipecatapp/tools/repo_map_impl/queries/go-tags.scm` | 🔴 Orphan | File: go-tags.scm |  |
| `pipecatapp/tools/repo_map_impl/queries/javascript-tags.scm` | 🔴 Orphan | File: javascript-tags.scm |  |
| `pipecatapp/tools/repo_map_impl/queries/python-tags.scm` | 🔴 Orphan | File: python-tags.scm |  |
| `pipecatapp/tools/repo_map_impl/queries/rust-tags.scm` | 🔴 Orphan | File: rust-tags.scm |  |
| `pipecatapp/tools/repo_map_impl/queries/swift-tags.scm` | 🔴 Orphan | File: swift-tags.scm |  |
| `pipecatapp/tools/repo_map_impl/queries/tsx-tags.scm` | 🔴 Orphan | File: tsx-tags.scm |  |
| `pipecatapp/tools/repo_map_impl/queries/typescript-tags.scm` | 🔴 Orphan | File: typescript-tags.scm |  |
| `pipecatapp/tools/repo_map_impl/rank.py` | 🟢 Referenced | File: rank.py | **Functions:** estimate_tokens, build_reference_graph, pagerank, select_budget_map, format_file_brief |
| `pipecatapp/tools/repo_map_impl/render/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/tools/repo_map_impl/render/catalog.py` | 🟢 Referenced | File: catalog.py | **Functions:** default_categorize, categorize_files, render_catalog_section |
| `pipecatapp/tools/repo_map_impl/render/file_index.py` | 🟢 Referenced | File: file_index.py | **Functions:** render_file_index |
| `pipecatapp/tools/repo_map_impl/render/json_out.py` | 🟢 Referenced | File: json_out.py | **Functions:** render_json |
| `pipecatapp/tools/repo_map_impl/render/navigation.py` | 🟢 Referenced | File: navigation.py | **Functions:** compact_tree_threshold, render_agent_guide, compute_section_lines |
| `pipecatapp/tools/repo_map_impl/render/tree.py` | 🟢 Referenced | File: tree.py | **Functions:** build_tree, format_tree_compact, format_tree, render_aider_section |
| `pipecatapp/tools/retry_utils.py` | 🟢 Referenced | File: retry_utils.py | **Classes:** RetryConfig<br>**Functions:** is_transient_error, calculate_delay, retry, decorator, wrapper... |
| `pipecatapp/tools/sandbox.ts` | 🟢 Referenced | sandbox.ts |  |
| `pipecatapp/tools/save_skill_tool.py` | 🟢 Referenced | File: save_skill_tool.py | **Classes:** SaveSkillTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/scale_compute_tool.py` | 🟢 Referenced | File: scale_compute_tool.py | **Classes:** ScaleComputeTool<br>**Functions:** __init__, scale, execute |
| `pipecatapp/tools/scheduler_tool.py` | 🟢 Referenced | File: scheduler_tool.py | **Classes:** SchedulerTool<br>**Functions:** __init__, _inject_message, add_cron_job, add_interval_job, list_jobs... |
| `pipecatapp/tools/search_skills_tool.py` | 🟢 Referenced | File: search_skills_tool.py | **Classes:** SearchSkillsTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/search_tool.py` | 🟢 Referenced | File: search_tool.py | **Classes:** SearchTool<br>**Functions:** __init__, _validate_path, grep, find_file |
| `pipecatapp/tools/set_operational_mode_tool.py` | 🟢 Referenced | File: set_operational_mode_tool.py | **Classes:** SetOperationalModeTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/shell_tool.py` | 🟢 Referenced | File: shell_tool.py | **Classes:** ShellTool<br>**Functions:** __init__, _ensure_session, execute_command, collect_gen |
| `pipecatapp/tools/skill_builder_tool.py` | 🟢 Referenced | File: skill_builder_tool.py | **Classes:** SkillBuilderTool<br>**Functions:** __init__, execute |
| `pipecatapp/tools/smol_agent_tool.py` | 🟢 Referenced | File: smol_agent_tool.py | **Classes:** SmolAgentTool, CodeAgent, LiteLLMModel<br>**Functions:** __init__, _initialize, _execute_in_sandbox, run, __init__... |
| `pipecatapp/tools/spec_loader_tool.py` | 🟢 Referenced | File: spec_loader_tool.py | **Classes:** SpecLoaderTool<br>**Functions:** __init__, _validate_protocol, _validate_arg, _validate_path, _validate_repo_name... |
| `pipecatapp/tools/ssh_tool.py` | 🟢 Referenced | File: ssh_tool.py | **Classes:** SSH_Tool<br>**Functions:** __init__, run_command |
| `pipecatapp/tools/submit_solution_tool.py` | 🟢 Referenced | File: submit_solution_tool.py | **Classes:** SubmitSolutionTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/summarizer_tool.py` | 🟢 Referenced | File: summarizer_tool.py | **Classes:** SummarizerTool<br>**Functions:** __init__, get_summary |
| `pipecatapp/tools/swarm_tool.py` | 🟢 Referenced | File: swarm_tool.py | **Classes:** SwarmTool<br>**Functions:** __init__, spawn_workers, wait_for_results, kill_worker |
| `pipecatapp/tools/tap_service.py` | 🟢 Referenced | File: tap_service.py | **Classes:** TapService<br>**Functions:** __init__, process_frame |
| `pipecatapp/tools/term_everything_tool.py` | 🟢 Referenced | File: term_everything_tool.py | **Classes:** TermEverythingTool<br>**Functions:** __init__, execute |
| `pipecatapp/tools/ternlight_tool.py` | 🟢 Referenced | File: ternlight_tool.py | **Classes:** TernlightTool<br>**Functions:** __init__, _check_service, embed, similar, _local_execute... |
| `pipecatapp/tools/test_git_tool.py` | 🧪 Test | File: test_git_tool.py | **Classes:** TestGitTool<br>**Functions:** setUp, test_ls_files, test_ls_files_integration |
| `pipecatapp/tools/test_ssh_tool.py` | 🟢 Referenced | File: test_ssh_tool.py | **Functions:** ssh_tool, test_run_command_success, test_run_command_error |
| `pipecatapp/tools/update_litellm_tool.py` | 🟢 Referenced | File: update_litellm_tool.py | **Classes:** UpdateLitellmTool<br>**Functions:** __init__, schema, fetch_releases, update_nomad_file, execute |
| `pipecatapp/tools/vr_tool.py` | 🟢 Referenced | File: vr_tool.py | **Classes:** VRTool<br>**Functions:** __init__, get_tool_def, execute |
| `pipecatapp/tools/wasm_tool.py` | 🟢 Referenced | File: wasm_tool.py | **Classes:** WasmTool<br>**Functions:** __init__, process_text, execute_custom |
| `pipecatapp/tools/web_browser_tool.py` | 🟢 Referenced | File: web_browser_tool.py | **Classes:** WebBrowserTool<br>**Functions:** __init__, ensure_initialized, goto, get_page_content, get_screenshot... |
| `pipecatapp/tools/wol_tool.py` | 🟢 Referenced | File: wol_tool.py | **Classes:** WOLTool<br>**Functions:** __init__, _validate_mac, wake, execute |
| `pipecatapp/train_router.py` | 🟢 Referenced | Change working directory so that llmrouter loads relative to pipecatapp |  |
| `pipecatapp/ui/opengravity/CONTRIBUTING.md` | 🟢 Referenced | File: CONTRIBUTING.md |  |
| `pipecatapp/ui/opengravity/LICENSE` | 🟢 Referenced | File: LICENSE |  |
| `pipecatapp/ui/opengravity/README.md` | 🟢 Referenced | OpenGravity |  |
| `pipecatapp/ui/opengravity/_headers` | 🟢 Referenced | File: _headers |  |
| `pipecatapp/ui/opengravity/agent.js` | 🟢 Referenced | File: agent.js |  |
| `pipecatapp/ui/opengravity/assets/html site example.png` | 🔴 Orphan | File: html site example.png |  |
| `pipecatapp/ui/opengravity/assets/icon.jpeg` | 🟢 Referenced | File: icon.jpeg |  |
| `pipecatapp/ui/opengravity/assets/screenshot.png` | 🟢 Referenced | File: screenshot.png |  |
| `pipecatapp/ui/opengravity/iconstyles.css` | 🟢 Referenced | File: iconstyles.css |  |
| `pipecatapp/ui/opengravity/index.html` | 🟢 Referenced | File: index.html |  |
| `pipecatapp/ui/opengravity/script.js` | 🟢 Referenced | File: script.js |  |
| `pipecatapp/ui/opengravity/server.py` | 🟢 Referenced | File: server.py | **Classes:** Handler<br>**Functions:** end_headers, do_GET |
| `pipecatapp/ui/opengravity/seti.woff` | 🟢 Referenced | File: seti.woff |  |
| `pipecatapp/ui/opengravity/style.css` | 🟢 Referenced | File: style.css |  |
| `pipecatapp/ui/opengravity/webcontainer/connect/index.html` | 🟢 Referenced | File: index.html |  |
| `pipecatapp/utils/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/utils/backon_utils.py` | 🟢 Referenced | File: backon_utils.py | **Classes:** MultiMetricsCollector<br>**Functions:** is_transient_error, setup_backon_observability, __init__, emit_attempt, emit_success... |
| `pipecatapp/utils/command_runner.py` | 🟢 Referenced | File: command_runner.py | **Classes:** CommandRunner<br>**Functions:** get_instance, __init__, _init_nomad_client, run_local, run... |
| `pipecatapp/utils/coverage_check.py` | 🟢 Referenced | Coverage check for scaffold-setup-skill. | **Classes:** Param, CheckResult<br>**Functions:** extract_env_example_params, _parse_env_file, extract_ci_secret_params, extract_skill_params, extract_skill_branches... |
| `pipecatapp/utils/file_utils.py` | 🟢 Referenced | File: file_utils.py | **Functions:** calculate_line_hash, generate_file_hashes |
| `pipecatapp/utils/ingest_skills.py` | 🔴 Orphan | File: ingest_skills.py | **Functions:** ingest_all_skills, adapt_scaffold_setup_skill |
| `pipecatapp/utils/rag_pruner.py` | 🟢 Referenced | File: rag_pruner.py | **Classes:** RAGPruner<br>**Functions:** __init__, prune_chunks, _construct_grading_prompt, _parse_grading_response |
| `pipecatapp/utils/ssh_utils.py` | 🟢 Referenced | File: ssh_utils.py | **Functions:** ensure_ssh_keys_initialized |
| `pipecatapp/utils/terminal_cleanup.py` | 🟢 Referenced | File: terminal_cleanup.py | **Functions:** clean_terminal_output |
| `pipecatapp/web_server.py` | 🟢 Referenced | File: web_server.py | **Classes:** SecurityHeadersMiddleware, AsyncCache, WebSocketManager<br>**Functions:** is_origin_allowed, websocket_endpoint, internal_chat, internal_chat_sync, internal_system_message... |
| `pipecatapp/worker_agent.py` | 🟢 Referenced | File: worker_agent.py | **Classes:** WorkerAgent<br>**Functions:** __init__, rehydrate_and_resume, perform_step, run |
| `pipecatapp/workflow/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/workflow/canvas_converter.py` | 🟢 Referenced | File: canvas_converter.py | **Classes:** CanvasConverter<br>**Functions:** canvas_to_workflow, _infer_node_type, _extract_config, workflow_to_canvas |
| `pipecatapp/workflow/context.py` | 🟢 Referenced | File: context.py | **Classes:** WorkflowContext<br>**Functions:** __init__, set_global_input, get_input, set_output, _resolve_value... |
| `pipecatapp/workflow/crypto_receipts.py` | 🟢 Referenced | File: crypto_receipts.py | **Classes:** ToolExecutionSigner<br>**Functions:** __init__, _normalize_payload, sign, verify |
| `pipecatapp/workflow/history.py` | 🟢 Referenced | File: history.py | **Classes:** WorkflowHistory<br>**Functions:** __new__, __init__, _init_db, save_run, get_all_runs... |
| `pipecatapp/workflow/node.py` | 🟢 Referenced | File: node.py | **Classes:** Node<br>**Functions:** __init__, execute, get_input, set_output, validate_io... |
| `pipecatapp/workflow/nodered_converter.py` | 🟢 Referenced | File: nodered_converter.py | **Classes:** NodeRedConverter<br>**Functions:** nodered_to_workflow, _infer_node_type, _extract_config, workflow_to_nodered |
| `pipecatapp/workflow/nodes/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/workflow/nodes/base_nodes.py` | 🟢 Referenced | File: base_nodes.py | **Classes:** InputNode, OutputNode, MergeNode, ConditionalBranchNode, GateNode, PostProcessorNode<br>**Functions:** execute, execute, execute, execute, execute... |
| `pipecatapp/workflow/nodes/consolidation_nodes.py` | 🟢 Referenced | File: consolidation_nodes.py | **Classes:** ContinuousConsolidationNode<br>**Functions:** execute |
| `pipecatapp/workflow/nodes/emperor_nodes.py` | 🟢 Referenced | File: emperor_nodes.py | **Classes:** EmperorAgentNode<br>**Functions:** resolve_abs_path, read_file_tool, list_files_tool, edit_file_tool, shell_tool... |
| `pipecatapp/workflow/nodes/langchain_nodes.py` | 🟢 Referenced | File: langchain_nodes.py | **Classes:** LangGraphNode<br>**Functions:** execute |
| `pipecatapp/workflow/nodes/llm_nodes.py` | 🟢 Referenced | File: llm_nodes.py | **Classes:** VisionLLMNode, PromptBuilderNode, SimpleLLMNode, ExpertRouterNode, ExternalLLMNode, DynamicRouterNode, ModelCapabilitiesRegistry, LLMRouterNode, LoopedReasoningNode<br>**Functions:** build_extensible_payload, discover_main_llm_service, execute, execute, execute... |
| `pipecatapp/workflow/nodes/rag_nodes.py` | 🟢 Referenced | File: rag_nodes.py | **Classes:** TextSplitterNode, DocumentWriterNode<br>**Functions:** __init__, execute, __init__, execute |
| `pipecatapp/workflow/nodes/ralph_nodes.py` | 🟢 Referenced | File: ralph_nodes.py | **Classes:** RalphLoopNode<br>**Functions:** execute |
| `pipecatapp/workflow/nodes/registry.py` | 🟢 Referenced | File: registry.py | **Classes:** NodeRegistry<br>**Functions:** __init__, register, get_node_class, get_all_nodes_metadata |
| `pipecatapp/workflow/nodes/system_nodes.py` | 🟢 Referenced | File: system_nodes.py | **Classes:** ConsulServiceDiscoveryNode, FileReadNode, DreamNode, FileWriteNode, HumanApprovalNode, SleepNode<br>**Functions:** execute, execute, execute, execute, execute... |
| `pipecatapp/workflow/nodes/tasky_nodes.py` | 🟢 Referenced | File: tasky_nodes.py | **Classes:** TaskyAuditNode<br>**Functions:** __init__, execute |
| `pipecatapp/workflow/nodes/tool_nodes.py` | 🟢 Referenced | File: tool_nodes.py | **Classes:** SystemPromptNode, ScreenshotNode, ToolParserNode, ToolExecutorNode, HereticNode<br>**Functions:** execute, execute, execute, execute, execute |
| `pipecatapp/workflow/runner.py` | 🟢 Referenced | File: runner.py | **Classes:** ActiveWorkflows, OpenGates, WorkflowRunner<br>**Functions:** make_serializable, _safe_context_to_dict, _save_run_background, __new__, add_runner... |
| `pipecatapp/workflows/adversarial_simulation.yaml` | 🟢 Referenced | File: adversarial_simulation.yaml |  |
| `pipecatapp/workflows/deep_context.yaml` | 🟢 Referenced | File: deep_context.yaml |  |
| `pipecatapp/workflows/default_agent_loop.yaml` | 🟢 Referenced | File: default_agent_loop.yaml |  |
| `pipecatapp/workflows/dft_workflow.yaml` | 📄 Workflow Config | File: dft_workflow.yaml |  |
| `pipecatapp/workflows/document_ingestion.yaml` | 🟢 Referenced | File: document_ingestion.yaml |  |
| `pipecatapp/workflows/looped_reasoning.yaml` | 📄 Workflow Config | File: looped_reasoning.yaml |  |
| `pipecatapp/workflows/manager.yaml` | 🟢 Referenced | File: manager.yaml |  |
| `pipecatapp/workflows/poc_ensemble.yaml` | 🟢 Referenced | File: poc_ensemble.yaml |  |
| `pipecatapp/workflows/sandbox.yaml` | 🟢 Referenced | File: sandbox.yaml |  |
| `pipecatapp/workflows/tiered_agent_loop.yaml` | 📄 Workflow Config | File: tiered_agent_loop.yaml |  |
| `pipecatapp/workflows/update_litellm_workflow.yaml` | 📄 Workflow Config | File: update_litellm_workflow.yaml |  |
| `playbook.yaml` | 🟢 Referenced | File: playbook.yaml |  |
| `playbooks/README.md` | 🟢 Referenced | Ansible Playbooks |  |
| `playbooks/app_jobs.yaml` | 🟢 Referenced | File: app_jobs.yaml |  |
| `playbooks/benchmark_single_model.yaml` | 🟢 Referenced | File: benchmark_single_model.yaml |  |
| `playbooks/cluster_status.yaml` | 🟢 Referenced | File: cluster_status.yaml |  |
| `playbooks/common_setup.yaml` | 🟢 Referenced | File: common_setup.yaml |  |
| `playbooks/controller.yaml` | 🟢 Referenced | File: controller.yaml |  |
| `playbooks/debug_template.yaml` | 🟢 Referenced | File: debug_template.yaml |  |
| `playbooks/deploy_app.yaml` | 🟢 Referenced | File: deploy_app.yaml |  |
| `playbooks/deploy_expert.yaml` | 🟢 Referenced | File: deploy_expert.yaml |  |
| `playbooks/deploy_openclaw.yaml` | 🔴 Orphan | File: deploy_openclaw.yaml |  |
| `playbooks/deploy_pds.yaml` | 🔴 Orphan | File: deploy_pds.yaml |  |
| `playbooks/deploy_prompt_evolution.yaml` | 🟢 Referenced | File: deploy_prompt_evolution.yaml |  |
| `playbooks/developer_tools.yaml` | 🟢 Referenced | File: developer_tools.yaml |  |
| `playbooks/diagnose_failure.yaml` | 🟢 Referenced | File: diagnose_failure.yaml |  |
| `playbooks/fix_cluster.yaml` | 🟢 Referenced | File: fix_cluster.yaml |  |
| `playbooks/heal_cluster.yaml` | 🟢 Referenced | File: heal_cluster.yaml |  |
| `playbooks/heal_job.yaml` | 🟢 Referenced | This variable would be passed in from the orchestrator script |  |
| `playbooks/health_check.yaml` | 🟢 Referenced | File: health_check.yaml |  |
| `playbooks/network/mesh.yaml` | 🟢 Referenced | File: mesh.yaml |  |
| `playbooks/network/verify.yaml` | 🟢 Referenced | File: verify.yaml |  |
| `playbooks/ops/optimize_memory.yaml` | 🟢 Referenced | File: optimize_memory.yaml |  |
| `playbooks/preflight/checks.yaml` | 🟢 Referenced | File: checks.yaml |  |
| `playbooks/promote_controller.yaml` | 🟢 Referenced | File: promote_controller.yaml |  |
| `playbooks/promote_to_controller.yaml` | 🟢 Referenced | File: promote_to_controller.yaml |  |
| `playbooks/pxe_setup.yaml` | 🟢 Referenced | File: pxe_setup.yaml |  |
| `playbooks/redeploy_pipecat.yaml` | 🟢 Referenced | File: redeploy_pipecat.yaml |  |
| `playbooks/run_config_manager.yaml` | 🟢 Referenced | File: run_config_manager.yaml |  |
| `playbooks/run_consul.yaml` | 🟢 Referenced | File: run_consul.yaml |  |
| `playbooks/run_health_check.yaml` | 🟢 Referenced | File: run_health_check.yaml |  |
| `playbooks/services/README.md` | 🟢 Referenced | Ansible Service Playbooks |  |
| `playbooks/services/ai_experts.yaml` | 🟢 Referenced | File: ai_experts.yaml |  |
| `playbooks/services/app_services.yaml` | 🟢 Referenced | File: app_services.yaml |  |
| `playbooks/services/apt_proxy.yaml` | 🟢 Referenced | File: apt_proxy.yaml |  |
| `playbooks/services/consul.yaml` | 🟢 Referenced | File: consul.yaml |  |
| `playbooks/services/core_ai_services.yaml` | 🟢 Referenced | File: core_ai_services.yaml |  |
| `playbooks/services/core_infra.yaml` | 🟢 Referenced | File: core_infra.yaml |  |
| `playbooks/services/distributed_compute.yaml` | 🟢 Referenced | Default variables can be overridden in inventory/group_vars |  |
| `playbooks/services/docker.yaml` | 🟢 Referenced | File: docker.yaml |  |
| `playbooks/services/final_verification.yaml` | 🟢 Referenced | File: final_verification.yaml |  |
| `playbooks/services/ipfs.yaml` | 🟢 Referenced | File: ipfs.yaml |  |
| `playbooks/services/model_services.yaml` | 🟢 Referenced | File: model_services.yaml |  |
| `playbooks/services/monitoring.yaml` | 🟢 Referenced | File: monitoring.yaml |  |
| `playbooks/services/nomad.yaml` | 🟢 Referenced | File: nomad.yaml |  |
| `playbooks/services/nomad_client.yaml` | 🟢 Referenced | File: nomad_client.yaml |  |
| `playbooks/services/pypi_proxy.yaml` | 🔴 Orphan | File: pypi_proxy.yaml |  |
| `playbooks/services/seed_models_to_ipfs.yaml` | 🟢 Referenced | File: seed_models_to_ipfs.yaml |  |
| `playbooks/services/streaming_services.yaml` | 🟢 Referenced | File: streaming_services.yaml |  |
| `playbooks/services/training_services.yaml` | 🟢 Referenced | File: training_services.yaml |  |
| `playbooks/status-check.yaml` | 🟢 Referenced | File: status-check.yaml |  |
| `playbooks/wake.yaml` | 🟢 Referenced | File: wake.yaml |  |
| `playbooks/worker.yaml` | 🟢 Referenced | File: worker.yaml |  |
| `poc/crdt_memory/README.md` | 🟢 Referenced | CRDT Agent Memory PoC |  |
| `poc/crdt_memory/run_poc.py` | 🟢 Referenced | File: run_poc.py | **Functions:** print_doc, main |
| `poc/p2p_sync/README.md` | 🟢 Referenced | Peer-to-Peer `.gguf` Model Sync PoC |  |
| `poc/p2p_sync/run_poc.py` | 🟢 Referenced | File: run_poc.py | **Functions:** main |
| `poc/p2p_sync/syncthing_manager.py` | 🟢 Referenced | File: syncthing_manager.py | **Classes:** SyncthingNode<br>**Functions:** __init__, _ensure_binary_exists, generate_config, _modify_config_ports, _get_api_key... |
| `poc/wasm_tool_bridge/README.md` | 🟢 Referenced | WASM Tool Bridge Proof of Concept |  |
| `poc/wasm_tool_bridge/host.py` | 🟢 Referenced | File: host.py | **Functions:** run_wasm |
| `poc/wasm_tool_bridge/python_tool.py` | 🟢 Referenced | File: python_tool.py | **Functions:** process_text |
| `poc/wasm_tool_bridge/text_processor/Cargo.lock` | 🔴 Orphan | This file is automatically @generated by Cargo. |  |
| `poc/wasm_tool_bridge/text_processor/Cargo.toml` | 🟢 Referenced | File: Cargo.toml |  |
| `poc/wasm_tool_bridge/text_processor/src/lib.rs` | 🔴 Orphan | [derive(Deserialize)] |  |
| `prompt_engineering/PROMPT_ENGINEERING.md` | 🟢 Referenced | Prompt Engineering Workflow |  |
| `prompt_engineering/README.md` | 🟢 Referenced | Prompt Engineering |  |
| `prompt_engineering/agents/ADAPTATION_AGENT.md` | 🟢 Referenced | The Self-Adaptation Agent |  |
| `prompt_engineering/agents/EVALUATOR_GENERATOR.md` | 🟢 Referenced | Agent Task: Generate a Custom Code Evaluator Script |  |
| `prompt_engineering/agents/README.md` | 🟢 Referenced | Agent Definitions |  |
| `prompt_engineering/agents/architecture_review.md` | 🟢 Referenced | Agent: Architecture Review |  |
| `prompt_engineering/agents/code_clean_up.md` | 🟢 Referenced | Agent: Code Clean Up |  |
| `prompt_engineering/agents/debug_and_analysis.md` | 🟢 Referenced | Agent: Debug and Analysis |  |
| `prompt_engineering/agents/new_task_review.md` | 🟢 Referenced | Agent: New Task Review |  |
| `prompt_engineering/agents/problem_scope_framing.md` | 🟢 Referenced | Agent: Problem Scope Framing |  |
| `prompt_engineering/archive/agent_0.json` | 📄 Documentation/Asset | File: agent_0.json |  |
| `prompt_engineering/archive/agent_0.py` | 📄 Documentation/Asset | File: agent_0.py |  |
| `prompt_engineering/archive/agent_1.json` | 📄 Documentation/Asset | File: agent_1.json |  |
| `prompt_engineering/archive/agent_1.py` | 📄 Documentation/Asset | File: agent_1.py |  |
| `prompt_engineering/archive/agent_2.json` | 📄 Documentation/Asset | File: agent_2.json |  |
| `prompt_engineering/archive/agent_2.py` | 📄 Documentation/Asset | File: agent_2.py |  |
| `prompt_engineering/archive/agent_3.json` | 📄 Documentation/Asset | File: agent_3.json |  |
| `prompt_engineering/archive/agent_3.py` | 📄 Documentation/Asset | File: agent_3.py |  |
| `prompt_engineering/archive_server.py` | 🟢 Referenced | File: archive_server.py | **Functions:** get_tree |
| `prompt_engineering/autoloop_evolve.py` | 📄 Documentation/Asset | File: autoloop_evolve.py | **Functions:** run_pytest_metric, main |
| `prompt_engineering/challenger.py` | 🟢 Referenced | File: challenger.py | **Classes:** Challenger<br>**Functions:** __init__, generate_challenge |
| `prompt_engineering/create_evaluator.py` | 🟢 Referenced | The template is based on the one defined in prompt_engineering/agents/EVALUATOR_GENERATOR.md | **Functions:** main |
| `prompt_engineering/evaluation_lib.py` | 🟢 Referenced | This file will contain the reusable functions for evaluating code. | **Functions:** render_nomad_job, wait_for_service_healthy, get_test_results, cleanup |
| `prompt_engineering/evaluation_suite/README.md` | 🟢 Referenced | Evaluation Suite |  |
| `prompt_engineering/evaluation_suite/test_vision.yaml` | 🟢 Referenced | File: test_vision.yaml |  |
| `prompt_engineering/evaluator.py` | 🟢 Referenced | File: evaluator.py | **Functions:** is_safe_code, evaluate_code |
| `prompt_engineering/evolve.py` | 🟢 Referenced | File: evolve.py | **Functions:** load_archive_metadata, select_parent, select_parent_from_archive, run_evolution, get_fitness_score... |
| `prompt_engineering/frontend/app.js` | 🟢 Referenced | Frontend logic for Campaign Analysis UI |  |
| `prompt_engineering/frontend/index.html` | 🟢 Referenced | File: index.html |  |
| `prompt_engineering/frontend/server.py` | 🟢 Referenced | File: server.py | **Functions:** serve_index, get_evolutionary_tree |
| `prompt_engineering/frontend/style.css` | 🟢 Referenced | File: style.css |  |
| `prompt_engineering/generated_evaluators/.gitignore` | 🟢 Referenced | Ignore all files in this directory |  |
| `prompt_engineering/promote_agent.py` | 🟢 Referenced | File: promote_agent.py | **Functions:** find_best_agent, promote_agent, _perform_promotion |
| `prompt_engineering/requirements-dev.txt` | 🟢 Referenced | File: requirements-dev.txt |  |
| `prompt_engineering/run_campaign.py` | 🟢 Referenced | File: run_campaign.py | **Functions:** run_campaign, analyze_archive, _generate_report |
| `prompt_engineering/self_harness.py` | 🟢 Referenced | File: self_harness.py | **Classes:** SelfHarness<br>**Functions:** __init__, _evaluate, weakness_mining, harness_proposal, proposal_validation... |
| `prompt_engineering/visualize_archive.py` | 🟢 Referenced | File: visualize_archive.py | **Functions:** visualize_archive, get_color_for_fitness, _save_graph |
| `prompts/README.md` | 🟢 Referenced | Prompts |  |
| `prompts/chat-with-bob.txt` | 🟢 Referenced | File: chat-with-bob.txt |  |
| `prompts/router.txt` | 🟢 Referenced | File: router.txt |  |
| `pyproject.toml` | 🟢 Referenced | File: pyproject.toml |  |
| `pytest.ini` | 🟢 Referenced | File: pytest.ini |  |
| `reflection/README.md` | 🟢 Referenced | Reflection |  |
| `reflection/adaptation_manager.py` | 🟢 Referenced | File: adaptation_manager.py | **Functions:** generate_test_case, main |
| `reflection/create_reflection.py` | 🟢 Referenced | File: create_reflection.py | **Functions:** create_reflection |
| `reflection/reflect.py` | 🟢 Referenced | File: reflect.py | **Functions:** load_llm_config, call_openai_llm, run_tool, analyze_failure_with_llm, main |
| `replace_local_world_model.py` | 🔴 Orphan | File: replace_local_world_model.py |  |
| `requirements-dev.txt` | 🟢 Referenced | File: requirements-dev.txt |  |
| `scenarios/adr_template.md` | 🔴 Orphan | Architecture Decision Record (ADR) Template |  |
| `scenarios/agent_behavior_template.md` | 🔴 Orphan | Agent Behavior Scenario Template |  |
| `scenarios/api_calls_template.md` | 🔴 Orphan | API Call Scenario Template |  |
| `scenarios/error_handling_template.md` | 🟢 Referenced | Error Handling Scenario Template |  |
| `scenarios/evaluation_scenario_template.md` | 🟢 Referenced | Benchmarking & Evaluation Scenario Template |  |
| `scenarios/scheduled_task_code_quality.md` | 🔴 Orphan | Scheduled Task |  |
| `scenarios/ui_ux_design_template.md` | 🔴 Orphan | UI/UX Design Scenario Template |  |
| `scenarios/validation_format_template.md` | 🟢 Referenced | Validation Format Scenario Template |  |
| `scenarios/workflow_node_template.md` | 🔴 Orphan | Workflow Node Scenario Template |  |
| `scripts/README.md` | 🟢 Referenced | `scripts/` Directory Overview |  |
| `scripts/agent_fast_check.sh` | 🟢 Referenced | Unified Fast Verification Script for Autonomous Agents  This script serves as a lightweight, sandbo |  |
| `scripts/agent_preflight.sh` | 🟢 Referenced | Agent Preflight Checklist  This script MUST be run by the agent prior to submitting code. It runs a |  |
| `scripts/agentic_workflow.sh` | 🟢 Referenced | --- Configuration --- |  |
| `scripts/analyze_nomad_allocs.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** format_timestamp, analyze_allocs |
| `scripts/ansible_diff.sh` | 🟢 Referenced | A script to compare Ansible playbook runs to detect changes over time. It establishes a baseline fro |  |
| `scripts/benchmark_resources.py` | 🟢 Referenced | Dynamic Resource Benchmark and Configuration Script. | **Functions:** get_system_resources, main |
| `scripts/check_all_playbooks.sh` | 🟢 Referenced | --- Flexible Ansible Playbook Checker  This script recursively finds all .yaml and .yml files, filte |  |
| `scripts/check_deps.py` | 🟢 Referenced | Write the requirements to a temp file | **Functions:** check_versions |
| `scripts/ci_ansible_check.sh` | 🟢 Referenced | A CI/CD-friendly script to check for unintended changes in Ansible playbooks.  - It compares the pla |  |
| `scripts/cleanup.sh` | 🟢 Referenced | Cleanup script to free up disk space on the host machine. This script aggressively cleans Docker re |  |
| `scripts/compare_exo_llama.py` | 🟢 Referenced | File: compare_exo_llama.py | **Functions:** print_color, check_health, run_inference, main |
| `scripts/create_assistant_prompts.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** generate_prompts |
| `scripts/create_cynic_model.sh` | 🔵 Entry Point | bin/bash |  |
| `scripts/create_todo_issues.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/dance_loading.py` | 🔵 Entry Point | File: dance_loading.py | **Classes:** DanceLoadingUI<br>**Functions:** strip_ansi, parse_ansi_colors, main, __init__, read_process_output... |
| `scripts/debug/README.md` | 🟢 Referenced | Debug Scripts |  |
| `scripts/debug/test_mqtt_connection.py` | 🟢 Referenced | File: test_mqtt_connection.py | **Functions:** get_ip_addresses, check_port, main |
| `scripts/debug_expert.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/debug_mesh.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/enroll-admin.sh` | 🟢 Referenced | Enroll a human operator using a security key challenge |  |
| `scripts/evaluate_clamav.py` | 🟢 Referenced | File: evaluate_clamav.py | **Functions:** setup_test_files, run_scan, analyze_results |
| `scripts/fix_markdown.sh` | 🟢 Referenced | Automatic Markdown Linter Fixer  This script uses markdownlint-cli's --fix option to automatically |  |
| `scripts/fix_verification_failures.sh` | 🟢 Referenced | Scripts to help remediate failures reported by verify_components.py |  |
| `scripts/fix_yaml.sh` | 🟢 Referenced | Automatic YAML Linter Fixer  This script automatically fixes common, repetitive style issues report |  |
| `scripts/generate_assistant_vectors.sh` | 🔵 Entry Point | bin/bash |  |
| `scripts/generate_file_map.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** get_rel_path, is_ignored, extract_python_info, extract_shell_info, extract_generic_desc... |
| `scripts/generate_issue_script.py` | 🟢 Referenced | File: generate_issue_script.py | **Functions:** parse_todo_file, create_issue_script |
| `scripts/generate_signatures.py` | 🔵 Entry Point | File: generate_signatures.py | **Functions:** to_hex, create_ldb_sig |
| `scripts/generate_tailscale_key.sh` | 🔵 Entry Point | Generate a reusable Headscale pre-auth key valid for 24 hours |  |
| `scripts/git-cleanup.sh` | 🔵 Entry Point | Default to 'main', but allow the user to specify a target branch (e.g., ./git-cleanup.sh master) |  |
| `scripts/heal_cluster.sh` | 🟢 Referenced | Wrapper script to run the cluster healing playbook. This ensures core infrastructure (LlamaRPC, Pip |  |
| `scripts/healer.py` | 🟢 Referenced | File: healer.py | **Classes:** NomadWatcher, HealerAgent<br>**Functions:** run_local_mode, main, __init__, get_failed_allocs, get_logs... |
| `scripts/lint.sh` | 🟢 Referenced | Unified Linting Script  This script runs a series of linters to ensure code quality and consistency |  |
| `scripts/lint_exclude.txt` | 🟢 Referenced | Exclude problematic files from the linting process. |  |
| `scripts/memory_audit.py` | 🟢 Referenced | File: memory_audit.py | **Functions:** get_prometheus_metrics, get_job_spec, update_job_memory, main |
| `scripts/nomad_checkpoint.sh` | 🔵 Entry Point | Trigger a Nomad task checkpoint utilizing Docker's experimental CRIU support. |  |
| `scripts/profile_resources.sh` | 🟢 Referenced | Profile resources usage and alignment of AI experts and models. |  |
| `scripts/provisioning.py` | 🟢 Referenced | Provisioning Script for Hybrid Architecture. | **Classes:** Colors<br>**Functions:** print_warning, print_error, print_header, print_task_header, load_global_vars... |
| `scripts/prune_consul_services.py` | 🟢 Referenced | Prune Stale Critical Services from Consul | **Functions:** get_consul_token, consul_request, main |
| `scripts/recover_node.py` | 🟢 Referenced | Robust Remote Node Recovery | **Functions:** ping_node, ipmi_set_pxe_boot, ipmi_reboot, main |
| `scripts/recover_os.py` | 🟢 Referenced | Unified Btrfs Snapshot and Rollback Recovery Tool | **Functions:** check_btrfs, check_btrfs_mount, get_protected_dirs, create_snapshot, list_snapshots... |
| `scripts/run_nomad.sh` | 🟢 Referenced | Nomad Job Submission Script  This script provides a simple interface to deploy Nomad job files witho |  |
| `scripts/run_quibbler.sh` | 🟢 Referenced | A wrapper script to run quibbler for code review. Check for required arguments |  |
| `scripts/run_smol_recovery.py` | 🟢 Referenced | File: run_smol_recovery.py | **Functions:** main |
| `scripts/run_tests.sh` | 🟢 Referenced | usr/bin/env bash |  |
| `scripts/salvage_task.py` | 🟢 Referenced | File: salvage_task.py | **Functions:** find_stalled_tasks, extract_partial_work, synthesize_summary, create_re_injection_prompt, main |
| `scripts/setup_pxe_server.sh` | 🔵 Entry Point | bin/bash |  |
| `scripts/start_services.sh` | 🟢 Referenced | This script is a legacy utility for manually starting services. ⚠️  DEPRECATED: Please use Ansible t |  |
| `scripts/sudo_env.py` | 🟢 Referenced | File: sudo_env.py | **Functions:** load_sudo_env |
| `scripts/supervisor.py` | 🟢 Referenced | File: supervisor.py | **Functions:** load_llm_config, run_playbook, run_script, cleanup_files, main |
| `scripts/test_playbooks_dry_run.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/test_playbooks_live_run.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/test_swarm_map_reduce.py` | 🔵 Entry Point | File: test_swarm_map_reduce.py | **Classes:** MockMemoryClient<br>**Functions:** test_swarm_map_reduce, __init__, get_events, add_event, get_agent_stats... |
| `scripts/troubleshoot.py` | 🟢 Referenced | Nomad Job Troubleshooting CLI | **Functions:** get_ssl_context, get_consul_token, run_legacy_command, get_nomad_allocations, section... |
| `scripts/uninstall.sh` | 🟢 Referenced | This script uninstalls all software and reverts all changes made by the playbook. |  |
| `scripts/update_cluster.sh` | 🔵 Entry Point | update_cluster.sh  This script updates the pipecat-cluster base image from the git repository witho |  |
| `scripts/update_resource_limits.py` | 🔵 Entry Point | usr/bin/env python3 | **Functions:** main |
| `scripts/verify_consul_attributes.sh` | 🔵 Entry Point | bin/bash |  |
| `tests/README.md` | 🟢 Referenced | Testing |  |
| `tests/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `tests/e2e/README.md` | 🟢 Referenced | End-to-End Tests |  |
| `tests/e2e/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `tests/e2e/test_api.py` | 🟢 Referenced | File: test_api.py | **Functions:** get_api_key_hash, api_key_and_hash, start_service, test_status_publicly_accessible, test_protected_endpoint_unauthorized_no_key... |
| `tests/e2e/test_intelligent_routing.py` | 🟢 Referenced | File: test_intelligent_routing.py | **Classes:** MockLLM<br>**Functions:** twin_service_fixture, test_discovers_all_experts, test_routing_to_external_expert_and_tracking, test_system_prompt_includes_metrics, __init__... |
| `tests/e2e/test_mission_control.py` | 🟢 Referenced | File: test_mission_control.py | **Functions:** test_mission_control_ui_loads, test_health_check_endpoint |
| `tests/e2e/test_palette_command_history.py` | 🧪 Test | File: test_palette_command_history.py | **Functions:** web_server, test_command_history |
| `tests/e2e/test_palette_ux.py` | 🧪 Test | File: test_palette_ux.py | **Functions:** web_server, test_save_load_buttons_state |
| `tests/e2e/test_regression.py` | 🟢 Referenced | File: test_regression.py | **Functions:** test_code_runner_tool |
| `tests/integration/README.md` | 🟢 Referenced | Integration Tests |  |
| `tests/integration/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `tests/integration/stub_services.py` | 🟢 Referenced | File: stub_services.py | **Classes:** StubOutputService<br>**Functions:** __init__, process_frame, wait_for_frame |
| `tests/integration/test_consul_role.yaml` | 🟢 Referenced | File: test_consul_role.yaml |  |
| `tests/integration/test_helixdb_e2e.py` | 🧪 Test | File: test_helixdb_e2e.py | **Functions:** test_helixdb_e2e_insert_and_retrieve |
| `tests/integration/test_mini_pipeline.py` | 🧪 Test | File: test_mini_pipeline.py | **Classes:** MockListAudioSource<br>**Functions:** test_stt_mini_pipeline, __init__, start |
| `tests/integration/test_mqtt_exporter.py` | 🧪 Test | File: test_mqtt_exporter.py | **Classes:** TestMqttExporter<br>**Functions:** setUpClass, setUp, tearDown, cleanup, test_metrics_collection |
| `tests/integration/test_nomad_role.yaml` | 🟢 Referenced | File: test_nomad_role.yaml |  |
| `tests/integration/test_pipecat_app.py` | 🟢 Referenced | File: test_pipecat_app.py | **Classes:** TestPipecatApp<br>**Functions:** setUp, test_health_check_eventually_healthy, test_main_page_loads |
| `tests/integration/test_preemption.py` | 🟢 Referenced | File: test_preemption.py | **Classes:** TestPreemption<br>**Functions:** setUp, tearDown, test_preemption |
| `tests/playbooks/e2e-tests.yaml` | 🟢 Referenced | File: e2e-tests.yaml |  |
| `tests/playbooks/test_authentik.yml` | 🧪 Test | File: test_authentik.yml |  |
| `tests/playbooks/test_clamav_playbook.yml` | 🧪 Test | File: test_clamav_playbook.yml |  |
| `tests/playbooks/test_consul.yaml` | 🧪 Test | File: test_consul.yaml |  |
| `tests/playbooks/test_llama_cpp.yaml` | 🧪 Test | File: test_llama_cpp.yaml |  |
| `tests/playbooks/test_nomad.yaml` | 🧪 Test | File: test_nomad.yaml |  |
| `tests/playbooks/test_playbook.yml` | 🧪 Test | File: test_playbook.yml |  |
| `tests/playbooks/verify_cluster_network.yaml` | 🟢 Referenced | File: verify_cluster_network.yaml |  |
| `tests/scripts/run_unit_tests.sh` | 🟢 Referenced | usr/bin/env bash |  |
| `tests/scripts/stress_test_cluster.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** fetch, main |
| `tests/scripts/test_duplicate_role_execution.sh` | 🧪 Test | Test to verify that the bootstrap_agent role is not run twice using static analysis.  Move to the p |  |
| `tests/scripts/test_paddler.sh` | 🧪 Test | test_paddler.sh  This script performs basic tests to verify that Paddler (agent and balancer) is fun |  |
| `tests/scripts/test_piper.sh` | 🧪 Test | File: test_piper.sh |  |
| `tests/scripts/test_run.sh` | 🧪 Test | Start a new chat |  |
| `tests/scripts/verify_components.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** run_command, verify_systemd_service, verify_nomad_job, verify_file_exists, verify_command_available... |
| `tests/test.wav` | 🟢 Referenced | File: test.wav |  |
| `tests/test_agent_patterns.py` | 🧪 Test | File: test_agent_patterns.py | **Functions:** test_manager_agent_map_reduce, test_durable_technician |
| `tests/test_canvas_integration.py` | 🧪 Test | File: test_canvas_integration.py | **Classes:** TestCanvasIntegration, ConcreteNode<br>**Functions:** test_node_schema_3d, test_canvas_to_workflow, test_workflow_to_canvas, test_canvas_to_workflow_with_groups, test_workflow_to_canvas_with_scopes... |
| `tests/test_deep_context.py` | 🧪 Test | File: test_deep_context.py | **Classes:** MockSimpleLLMNode, MaliciousTestNode, SiblingAttackNode<br>**Functions:** test_deep_context_workflow, execute, get_input, get_input |
| `tests/test_event_bus.py` | 🟢 Referenced | File: test_event_bus.py | **Functions:** test_event_bus_flow |
| `tests/test_experiment_tool.py` | 🧪 Test | File: test_experiment_tool.py | **Functions:** test_experiment_tool_flow, mock_get, subprocess_side_effect |
| `tests/test_gastown_judge.py` | 🧪 Test | File: test_gastown_judge.py | **Functions:** test_gastown_judge |
| `tests/test_gastown_memory.py` | 🧪 Test | File: test_gastown_memory.py | **Functions:** test_gastown_memory |
| `tests/test_gastown_stats.py` | 🧪 Test | File: test_gastown_stats.py | **Functions:** test_gastown_stats |
| `tests/test_imports.py` | 🧪 Test | Add files dir to path |  |
| `tests/test_manager_flow.py` | 🧪 Test | File: test_manager_flow.py | **Classes:** MockSwarmTool, TestManagerFlow<br>**Functions:** run_server, mock_technician_task, spawn_workers, test_flow, mock_map... |
| `tests/test_project_overview_tool.py` | 🧪 Test | Add project root to sys.path to allow imports | **Classes:** TestProjectOverviewTool<br>**Functions:** setUp, test_execute |
| `tests/test_spec_loader.py` | 🧪 Test | File: test_spec_loader.py | **Classes:** TestSpecLoader<br>**Functions:** setUp, tearDown, test_clone_new_repo, test_list_specs, test_scan_files_recursive... |
| `tests/test_ssrf_validation.py` | 🟢 Referenced | File: test_ssrf_validation.py | **Functions:** test_validate_url_safe, test_validate_url_unsafe_ip, test_validate_url_unsafe_scheme, test_allowlist |
| `tests/test_websocket_security.py` | 🟢 Referenced | File: test_websocket_security.py | **Functions:** test_websocket_ssrf_vulnerability |
| `tests/unit/README.md` | 🟢 Referenced | Unit Tests |  |
| `tests/unit/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `tests/unit/cluster_cache/test_cluster_cache.py` | 🧪 Test | File: test_cluster_cache.py | **Functions:** reset_state, test_get_nodes_empty, test_register_node_client_ip, test_register_node_explicit_ip, test_node_expiration |
| `tests/unit/conftest.py` | 🟢 Referenced | List of modules to mock if they are missing in the test environment | **Classes:** DummySpan<br>**Functions:** mock_module_if_missing, __enter__, __exit__, set_attribute, __call__ |
| `tests/unit/test_adaptation_manager.py` | 🟢 Referenced | File: test_adaptation_manager.py | **Classes:** TestAdaptationManager<br>**Functions:** test_import, test_main_flow |
| `tests/unit/test_agent_definitions.py` | 🟢 Referenced | Define the path to the agent definitions directory | **Functions:** parse_and_validate_agent_def, test_agent_definition_schema |
| `tests/unit/test_ansible_tool.py` | 🟢 Referenced | File: test_ansible_tool.py | **Functions:** test_ansible_tool_instantiation, test_run_playbook_success, test_run_playbook_with_args, test_run_playbook_failure, test_run_playbook_not_found... |
| `tests/unit/test_app_hybrid.py` | 🧪 Test | File: test_app_hybrid.py | **Classes:** MockFrameProcessor, MockTranscriptionFrame<br>**Functions:** test_discover_services_monolith_mode, test_discover_services_distributed_mode_failure, test_monolith_mode_answers_hello, __init__, process_frame... |
| `tests/unit/test_archivist_tool.py` | 🧪 Test | File: test_archivist_tool.py | **Functions:** test_archivist_tool_initialization, test_run_success, test_run_error_status, test_run_connection_failure |
| `tests/unit/test_ast_editor_tool.py` | 🧪 Test | File: test_ast_editor_tool.py | **Functions:** temp_dir, ast_editor, test_extract_function, test_rename_symbol, test_add_import... |
| `tests/unit/test_atproto_tool.py` | 🧪 Test | File: test_atproto_tool.py | **Functions:** test_atproto_tool_initialization, test_send_post, test_get_timeline |
| `tests/unit/test_audio_download_limit.py` | 🧪 Test | File: test_audio_download_limit.py | **Classes:** MockStream, MockClient, MockStreamSmall, MockClientSmall<br>**Functions:** test_download_limit_exceeded, test_download_within_limit, endless_stream, download_audio_safe, download_audio_safe... |
| `tests/unit/test_autoloop_tool.py` | 🧪 Test | File: test_autoloop_tool.py | **Classes:** MockAutoLoop<br>**Functions:** test_autoloop_tool_initialization, test_autoloop_no_autoloop_package, test_autoloop_target_not_exist, test_autoloop_run_success, __init__... |
| `tests/unit/test_autoresearch_tool.py` | 🧪 Test | File: test_autoresearch_tool.py | **Functions:** test_autoresearch_tool_run, mock_eval |
| `tests/unit/test_autoresearch_tool_pathing.py` | 🧪 Test | File: test_autoresearch_tool_pathing.py | **Functions:** test_autoresearch_tool_pathing, mock_eval |
| `tests/unit/test_backon_integration.py` | 🧪 Test | File: test_backon_integration.py | **Classes:** MyClientError<br>**Functions:** test_is_transient_error, test_backon_retry_with_transient_predicate, test_backon_no_retry_on_non_transient, test_backon_retrying_context_manager, failing_func... |
| `tests/unit/test_batch_ast_editor.py` | 🧪 Test | File: test_batch_ast_editor.py | **Functions:** temp_dir, ast_editor, test_batch_edit |
| `tests/unit/test_batch_file_editor.py` | 🧪 Test | File: test_batch_file_editor.py | **Functions:** temp_dir, file_editor, test_batch_hash_replace |
| `tests/unit/test_claude_clone_tool.py` | 🧪 Test | File: test_claude_clone_tool.py | **Functions:** test_explain_success, test_command_failure, test_directory_not_found, test_cli_not_found |
| `tests/unit/test_code_runner_security.py` | 🧪 Test | File: test_code_runner_security.py | **Functions:** test_code_runner_length_limit, test_code_runner_length_limit_ok |
| `tests/unit/test_code_runner_timeout.py` | 🧪 Test | File: test_code_runner_timeout.py | **Functions:** test_execution_timeout_logic |
| `tests/unit/test_code_runner_tool.py` | 🟢 Referenced | File: test_code_runner_tool.py | **Functions:** code_runner, test_run_code_in_sandbox_success, test_run_python_code_success, test_run_python_code_no_docker_client |
| `tests/unit/test_command_deck.py` | 🧪 Test | File: test_command_deck.py | **Functions:** test_parse_models, test_api_server_endpoints |
| `tests/unit/test_container_registry_security.py` | 🧪 Test | File: test_container_registry_security.py | **Classes:** TestContainerRegistrySecurity<br>**Functions:** setUp, test_list_tags_path_traversal, test_search_images_blocks_invalid_repos, test_list_tags_valid |
| `tests/unit/test_container_registry_tool.py` | 🧪 Test | File: test_container_registry_tool.py | **Functions:** test_container_registry_tool_initialization, test_validate_repository, test_list_repositories, test_list_tags, test_search_images... |
| `tests/unit/test_context_upload_tool.py` | 🧪 Test | File: test_context_upload_tool.py | **Functions:** test_context_upload_tool_initialization, test_context_upload_tool_get_definition, test_context_upload_tool_execute_missing_args, test_context_upload_tool_execute_success |
| `tests/unit/test_council_tool.py` | 🧪 Test | File: test_council_tool.py | **Classes:** MockTwinService<br>**Functions:** council_tool, test_discover_local_experts, test_convene_council_no_experts, test_query_model_success, test_convene_council_full_flow... |
| `tests/unit/test_cq_tool.py` | 🧪 Test | File: test_cq_tool.py | **Functions:** test_cq_tool_initialization, test_cq_query, test_cq_propose, test_cq_confirm, test_cq_flag... |
| `tests/unit/test_crdt_memory.py` | 🧪 Test | File: test_crdt_memory.py | **Functions:** test_crdt_memory_backend_add_and_query, test_crdt_memory_backend_merge, test_crdt_memory_backend_write_document, test_crdt_memory_backend_delete_skill |
| `tests/unit/test_crypto_receipts.py` | 🧪 Test | Add the necessary path to import the workflow modules | **Functions:** test_sign_receipt, test_verify_receipt |
| `tests/unit/test_dependency_scanner.py` | 🟢 Referenced | File: test_dependency_scanner.py | **Classes:** TestDependencyScanner<br>**Functions:** setUp, test_scan_safe_package, test_scan_vulnerable_package, test_code_runner_blocks_unsafe_lib, test_code_runner_allows_safe_lib |
| `tests/unit/test_dependency_scanner_tool.py` | 🧪 Test | File: test_dependency_scanner_tool.py | **Functions:** test_dependency_scanner_initialization, test_scan_package_no_version_success, test_scan_package_with_vulns, side_effect |
| `tests/unit/test_desktop_control_tool.py` | 🧪 Test | File: test_desktop_control_tool.py | **Functions:** tool, mock_pyautogui, test_get_desktop_screenshot, test_click_at, test_type_text... |
| `tests/unit/test_document_tool.py` | 🧪 Test | File: test_document_tool.py | **Functions:** test_paperless_backend, test_local_directory_backend, test_document_tool_initialization_local, test_document_tool_bookmarks |
| `tests/unit/test_dynamic_skill_tool.py` | 🧪 Test | File: test_dynamic_skill_tool.py | **Functions:** test_dynamic_skill_tool_initialization, test_execute_no_code_runner, test_execute_no_python_blocks, test_execute_with_python_blocks |
| `tests/unit/test_emperor_node.py` | 🟢 Referenced | File: test_emperor_node.py | **Functions:** test_emperor_node |
| `tests/unit/test_experiment_tool_security.py` | 🧪 Test | File: test_experiment_tool_security.py | **Classes:** TestExperimentToolSecurity<br>**Functions:** setUp, tearDown, _mock_exists, test_command_injection_prevention, test_valid_command_execution... |
| `tests/unit/test_expert_tracker.py` | 🧪 Test | File: test_expert_tracker.py | **Classes:** AsyncContextManagerMock, AsyncContextManagerMockError<br>**Functions:** tracker, test_initialization, test_register_expert, test_register_existing_expert, test_record_success... |
| `tests/unit/test_file_editor_security.py` | 🧪 Test | File: test_file_editor_security.py | **Classes:** TestFileEditorSecurity<br>**Functions:** setUp, tearDown, test_read_file_outside_root, test_write_file_outside_root, test_apply_patch_outside_root... |
| `tests/unit/test_file_editor_tool.py` | 🧪 Test | File: test_file_editor_tool.py | **Classes:** TestFileEditorTool<br>**Functions:** setUp, tearDown, test_read_file, test_read_file_pagination, test_write_file... |
| `tests/unit/test_file_ingestion.py` | 🧪 Test | File: test_file_ingestion.py | **Functions:** temp_inbox, ingestor, test_safe_path, test_safe_path_nested, test_unsafe_path_traversal... |
| `tests/unit/test_final_answer_tool.py` | 🧪 Test | Add the tools directory to the python path | **Functions:** test_final_answer_tool_initialization, test_submit_task |
| `tests/unit/test_gemini_cli.py` | 🧪 Test | File: test_gemini_cli.py | **Functions:** test_gemini_cli_interaction, mock_server_handler |
| `tests/unit/test_get_nomad_job.py` | 🟢 Referenced | Fixed: Resolved AssertionError by removing global sys.modules HTTP mocks in the test suite that shad | **Classes:** MockRequestException<br>**Functions:** test_get_nomad_job_definition_success, test_get_nomad_job_definition_failure, test_get_nomad_job_definition_invalid_id |
| `tests/unit/test_git_tool.py` | 🧪 Test | File: test_git_tool.py | **Functions:** git_tool, test_clone_successful, test_pull_successful, test_push_successful, test_commit_successful... |
| `tests/unit/test_git_tool_security.py` | 🧪 Test | File: test_git_tool_security.py | **Classes:** TestGitToolSecurity<br>**Functions:** setUp, test_allowed_protocols, test_blocked_protocols, test_clone_with_dangerous_protocol |
| `tests/unit/test_gossip_discovery.py` | 🧪 Test | File: test_gossip_discovery.py | **Functions:** test_gossip_registry_register_and_get, test_gossip_handle_message, test_cleanup_stale_services, test_gossip_broadcast_loop |
| `tests/unit/test_ha_tool.py` | 🟢 Referenced | File: test_ha_tool.py | **Classes:** MockAsyncResponse<br>**Functions:** test_init_success, test_init_failure, test_call_ai_task_success, test_call_ai_task_failure, __init__... |
| `tests/unit/test_hashline_editor.py` | 🧪 Test | File: test_hashline_editor.py | **Classes:** TestHashlineEditor<br>**Functions:** setUp, tearDown, get_hash, test_read_with_hashlines, test_apply_hash_edits_replace... |
| `tests/unit/test_haystack_workflows.py` | 🧪 Test | File: test_haystack_workflows.py | **Classes:** CounterNode, LoopRouterNode<br>**Functions:** test_document_ingestion_workflow, test_cyclic_workflow_execution, execute, execute |
| `tests/unit/test_heretic_tool.py` | 🧪 Test | File: test_heretic_tool.py | **Functions:** test_heretic_tool_align_model |
| `tests/unit/test_infrastructure.py` | 🧪 Test | File: test_infrastructure.py | **Classes:** TestInfrastructure<br>**Functions:** test_consul_running, test_nomad_running |
| `tests/unit/test_jules_tool.py` | 🟢 Referenced | Fixed: Resolved TypeError by removing global sys.modules HTTP mocks in the test suite that shadowed | **Classes:** TestJulesTool<br>**Functions:** setUp, test_run_success, test_run_missing_api_key, test_run_http_error, test_run_generic_exception |
| `tests/unit/test_langchain_adapter_tool.py` | 🧪 Test | File: test_langchain_adapter_tool.py | **Classes:** MockLangchainSchema, MockLangChainTool, MockLangChainToolNoSchema<br>**Functions:** test_langchain_adapter_schema, test_langchain_adapter_run, test_langchain_adapter_run_no_schema, __init__, invoke... |
| `tests/unit/test_langchain_nodes.py` | 🧪 Test | Mock langchain dependencies | **Functions:** mock_context, test_langgraph_node_execute_no_graph, test_langgraph_node_execute_ainvoke, test_langgraph_node_execute_invoke_fallback, test_langgraph_node_execute_error |
| `tests/unit/test_langchain_wrappers.py` | 🧪 Test | File: test_langchain_wrappers.py | **Functions:** mock_pmm_memory, test_pmm_chat_message_history_get_messages, test_pmm_chat_message_history_add_messages, mock_memory_store, test_pipecat_vector_store_add_texts... |
| `tests/unit/test_lint_script.py` | 🟢 Referenced | File: test_lint_script.py | **Classes:** TestLintScript<br>**Functions:** setUp, tearDown, test_lint_script |
| `tests/unit/test_llxprt_code_tool.py` | 🧪 Test | File: test_llxprt_code_tool.py | **Functions:** llxprt_tool, test_run_success, test_run_with_args_success, test_run_failure, test_run_timeout... |
| `tests/unit/test_looped_reasoning_node.py` | 🧪 Test | File: test_looped_reasoning_node.py | **Classes:** MockWorkflowContext<br>**Functions:** test_looped_reasoning_execution, __init__, get_input, set_output, run_test |
| `tests/unit/test_mcp_tool.py` | 🧪 Test | File: test_mcp_tool.py | **Functions:** mcp_tool, test_get_status_with_running_pipelines, test_get_status_with_no_pipelines, test_get_status_with_no_runner, test_get_memory_summary... |
| `tests/unit/test_memory.py` | 🟢 Referenced | File: test_memory.py | **Functions:** temp_store_file, temp_index_file, mock_embedding_model, mock_faiss_index, test_unencrypted_memory_store... |
| `tests/unit/test_memory_advanced.py` | 🧪 Test | File: test_memory_advanced.py | **Functions:** memory_instance_advanced, test_get_memory_adv, test_get_memory_not_found_adv, test_get_consolidation_adv, test_get_consolidation_not_found_adv... |
| `tests/unit/test_mqtt_template.py` | 🧪 Test | File: test_mqtt_template.py | **Functions:** test_mqtt_template |
| `tests/unit/test_nodered_converter.py` | 🧪 Test | File: test_nodered_converter.py | **Functions:** test_nodered_conversion |
| `tests/unit/test_nomad_sandbox.py` | 🧪 Test | File: test_nomad_sandbox.py | **Classes:** MockAsyncResponse<br>**Functions:** nomad_executor, test_nomad_execution_success, test_nomad_template_injection_prevention, test_hybrid_mode_logic, test_docker_mode_logic... |
| `tests/unit/test_obsidian_gardener.py` | 🧪 Test | File: test_obsidian_gardener.py | **Classes:** MockObserver, MockFileSystemEventHandler, TestObsidianGardener<br>**Functions:** __init__, schedule, start, stop, join... |
| `tests/unit/test_open_workers_tool.py` | 🧪 Test | File: test_open_workers_tool.py | **Classes:** TestOpenWorkersTool<br>**Functions:** setUp, test_run_javascript_full_discovery |
| `tests/unit/test_openclaw_tool.py` | 🧪 Test | File: test_openclaw_tool.py | **Functions:** test_openclaw_tool_initialization, test_send_message_success, test_send_message_failure, mock_connect, mock_send... |
| `tests/unit/test_opencode_provider_tool.py` | 🧪 Test | File: test_opencode_provider_tool.py | **Functions:** test_parse_opencode_output, test_opencode_provider_run_success |
| `tests/unit/test_opencode_tool.py` | 🧪 Test | File: test_opencode_tool.py | **Classes:** TestOpencodeTool<br>**Functions:** setUp, test_run_success, test_run_error |
| `tests/unit/test_orchestrator_tool.py` | 🧪 Test | File: test_orchestrator_tool.py | **Functions:** test_orchestrator_tool_instantiation, test_dispatch_job_success, test_dispatch_job_failure |
| `tests/unit/test_p2p_sync_tool.py` | 🧪 Test | File: test_p2p_sync_tool.py | **Classes:** TestP2PSyncTool<br>**Functions:** test_initialize_and_start, test_check_sync_status |
| `tests/unit/test_personality_tool.py` | 🧪 Test | File: test_personality_tool.py | **Functions:** test_set_personality, test_reset_personality, test_get_current_personality |
| `tests/unit/test_pipecat_app_unit.py` | 🟢 Referenced | File: test_pipecat_app_unit.py | **Classes:** MockFrameProcessor, MockTranscriptionFrame<br>**Functions:** client, test_read_main, test_health_check, test_workflow_runner_loads_definition, test_health_check_is_healthy... |
| `tests/unit/test_planner_tool.py` | 🟢 Referenced | File: test_planner_tool.py | **Functions:** mock_twin_service, planner_tool, test_discover_llm_url_router_llm, test_discover_llm_url_fallback, test_discover_llm_url_env_var... |
| `tests/unit/test_playbook_integration.py` | 🟢 Referenced | File: test_playbook_integration.py | **Functions:** test_playbook_integration_syntax_check |
| `tests/unit/test_poc_ensemble.py` | 🧪 Test | File: test_poc_ensemble.py | **Classes:** TestPoCEnsemble<br>**Functions:** setUp, test_workflow_execution, mock_post, mock_get, run_workflow |
| `tests/unit/test_polyphony_tool.py` | 🧪 Test | File: test_polyphony_tool.py | **Classes:** TestPolyphonyTool<br>**Functions:** test_share_action, test_ping_action, test_task_list, test_missing_cli |
| `tests/unit/test_post_processor_node.py` | 🧪 Test | File: test_post_processor_node.py | **Functions:** test_post_processor_node_evaluate_data, test_post_processor_node_evaluate_list_comp, mock_get_input, mock_get_input |
| `tests/unit/test_power_tool.py` | 🧪 Test | File: test_power_tool.py | **Functions:** power_tool, test_set_idle_threshold_for_new_service, test_set_idle_threshold_for_existing_service, test_config_directory_not_found, test_file_io_error... |
| `tests/unit/test_project_mapper_tool.py` | 🧪 Test | File: test_project_mapper_tool.py | **Classes:** TestProjectMapperTool<br>**Functions:** tool, temp_project, test_is_ignored, test_guess_type, test_extract_imports_python... |
| `tests/unit/test_prompt_engineering.py` | 🟢 Referenced | File: test_prompt_engineering.py | **Classes:** TestEvolve, TestRunCampaign, TestPromoteAgent, TestVisualizeArchive<br>**Functions:** mock_archive, test_select_parent_from_archive_empty, test_select_parent_from_archive_populated, test_run_evolution, test_run_campaign_args... |
| `tests/unit/test_prompt_improver_tool.py` | 🧪 Test | File: test_prompt_improver_tool.py | **Classes:** TestPromptImproverTool<br>**Functions:** setUp, test_create_prompt_plan, test_discover_llm_failure |
| `tests/unit/test_provisioning.py` | 🟢 Referenced | File: test_provisioning.py | **Classes:** TestProvisioning<br>**Functions:** setUp, tearDown, test_load_playbooks_from_manifest, test_wait_for_ports_freed, test_cleanup_memory_for_core_ai... |
| `tests/unit/test_rag_caching.py` | 🧪 Test | File: test_rag_caching.py | **Functions:** test_strict_caching |
| `tests/unit/test_rag_tool.py` | 🟢 Referenced | File: test_rag_tool.py | **Classes:** SyncThread<br>**Functions:** mock_sentence_transformer, mock_faiss, mock_pmm_memory, sync_threading, test_rag_tool_initialization... |
| `tests/unit/test_ralph_nodes.py` | 🟢 Referenced | File: test_ralph_nodes.py | **Functions:** test_ralph_loop_success, test_ralph_loop_failure_then_success |
| `tests/unit/test_reflection.py` | 🟢 Referenced | File: test_reflection.py | **Classes:** TestReflection<br>**Functions:** test_analyze_failure_out_of_memory_with_tool_use, test_analyze_failure_simple_restart, test_main_success, test_main_no_args, test_main_file_not_found... |
| `tests/unit/test_remote_ledgers.py` | 🧪 Test | File: test_remote_ledgers.py | **Functions:** memory_db, test_merge_logic, test_client_push_pull, mock_get, mock_post |
| `tests/unit/test_safe_flatten.py` | 🟢 Referenced | Add ansible directory to sys.path since it doesn't have an __init__.py | **Functions:** test_safe_flatten_none, test_safe_flatten_dict, test_safe_flatten_list, test_safe_flatten_strings_omitted, test_safe_flatten_strings_included... |
| `tests/unit/test_save_skill_tool.py` | 🧪 Test | File: test_save_skill_tool.py | **Functions:** test_save_skill_tool_initialization, test_save_skill_success, test_save_skill_failure |
| `tests/unit/test_scale_compute_tool.py` | 🧪 Test | File: test_scale_compute_tool.py | **Functions:** test_scale_compute_tool_initialization, test_scale_missing_script, test_scale_success, test_scale_failure, test_execute... |
| `tests/unit/test_scheduler_tool.py` | 🧪 Test | File: test_scheduler_tool.py | **Functions:** test_scheduler_tool_initialization, test_add_cron_job_invalid, test_add_cron_job_success, test_add_interval_job_invalid, test_add_interval_job_success... |
| `tests/unit/test_search_skills_tool.py` | 🧪 Test | File: test_search_skills_tool.py | **Functions:** test_search_skills_tool_initialization, test_search_skills_run_success, test_search_skills_run_empty |
| `tests/unit/test_search_tool_security.py` | 🧪 Test | File: test_search_tool_security.py | **Classes:** TestSearchToolSecurity<br>**Functions:** setup_search_env, test_search_inside_root, test_search_traversal_via_symlink, test_find_traversal_via_symlink |
| `tests/unit/test_security.py` | 🟢 Referenced | Ensure pipecatapp is in path | **Classes:** TestSecurity<br>**Functions:** test_redact_sensitive_data, test_sanitize_data |
| `tests/unit/test_shell_tool.py` | 🧪 Test | File: test_shell_tool.py | **Functions:** test_shell_tool_initialization, test_execute_command_success, test_execute_command_timeout |
| `tests/unit/test_shell_tool_security.py` | 🟢 Referenced | File: test_shell_tool_security.py | **Classes:** TestShellToolLeak<br>**Functions:** test_leak, side_effect |
| `tests/unit/test_simple_llm_node.py` | 🟢 Referenced | Mock pipecat before importing the module under test | **Classes:** TestSimpleLLMNode<br>**Functions:** test_fast_tier_execution, test_balanced_tier_execution |
| `tests/unit/test_skill_builder_tool.py` | 🧪 Test | File: test_skill_builder_tool.py | **Functions:** test_skill_builder_tool_initialization, test_execute_create, test_execute_create_missing_params, test_execute_read, test_execute_read_not_found... |
| `tests/unit/test_skill_library.py` | 🧪 Test | File: test_skill_library.py | **Functions:** temp_db, test_skill_library_save_and_retrieve, test_skill_library_update, test_skill_library_search, test_save_skill_tool... |
| `tests/unit/test_smol_agent_tool.py` | 🧪 Test | File: test_smol_agent_tool.py | **Functions:** smol_tool, test_run_success, test_run_multiple_code_blocks, test_deno_missing, test_empty_task... |
| `tests/unit/test_spec_loader_tool.py` | 🧪 Test | File: test_spec_loader_tool.py | **Classes:** TestSpecLoaderSecurity<br>**Functions:** setUp, test_dangerous_protocol, test_argument_injection, test_path_traversal, test_symlink_path_traversal... |
| `tests/unit/test_ssh_tool.py` | 🟢 Referenced | File: test_ssh_tool.py | **Functions:** ssh_tool, test_run_command_with_key_success, test_run_command_with_password_success, test_run_command_with_error, test_no_auth_method_provided... |
| `tests/unit/test_submit_solution_tool.py` | 🧪 Test | File: test_submit_solution_tool.py | **Functions:** test_submit_solution_tool_initialization, test_submit_solution_success |
| `tests/unit/test_summarizer_tool.py` | 🧪 Test | File: test_summarizer_tool.py | **Functions:** mock_sentence_transformer_module, summarizer_tool, test_get_summary_with_history, test_get_summary_no_history, test_get_summary_less_than_k_history... |
| `tests/unit/test_supervisor.py` | 🟢 Referenced | File: test_supervisor.py | **Classes:** StringEndsWith, TestSupervisor<br>**Functions:** __init__, __eq__, __repr__, setUp, tearDown... |
| `tests/unit/test_swarm_tool.py` | 🧪 Test | File: test_swarm_tool.py | **Functions:** test_swarm_tool_initialization, test_spawn_workers_technician, test_spawn_workers_success, test_spawn_workers_partial_failure, test_kill_worker_success... |
| `tests/unit/test_tap_service.py` | 🧪 Test | File: test_tap_service.py | **Classes:** MockFrameProcessor<br>**Functions:** test_process_frame, __init__, push_frame |
| `tests/unit/test_tasky_nodes.py` | 🧪 Test | File: test_tasky_nodes.py | **Functions:** test_tasky_audit_node_no_markdown, test_tasky_audit_node_no_execution_result |
| `tests/unit/test_tasky_poc.py` | 🧪 Test | File: test_tasky_poc.py | **Functions:** main |
| `tests/unit/test_term_everything_tool.py` | 🟢 Referenced | File: test_term_everything_tool.py | **Functions:** tool, test_execute_command_success, test_execute_command_failure, test_execute_exception |
| `tests/unit/test_terminal_cleanup.py` | 🧪 Test | File: test_terminal_cleanup.py | **Functions:** test_clean_terminal_output_carriage_returns, test_clean_terminal_output_ansi, test_clean_terminal_output_both, test_clean_terminal_output_trailing_cr, test_clean_terminal_output_non_string |
| `tests/unit/test_ternlight_tool.py` | 🧪 Test | File: test_ternlight_tool.py | **Functions:** mock_requests_post, mock_requests_get, mock_subprocess_run, test_ternlight_tool_remote_embed, test_ternlight_tool_remote_similar... |
| `tests/unit/test_troubleshoot.py` | 🧪 Test | Dynamically import troubleshoot as it is a script | **Classes:** DummyArgs<br>**Functions:** mock_api_get, mock_run_command, test_list_dead_pending, test_list_dead_pending_json, test_inspect_job... |
| `tests/unit/test_update_litellm_tool.py` | 🧪 Test | File: test_update_litellm_tool.py | **Functions:** test_update_litellm_tool_initialization, test_fetch_releases_success, test_update_nomad_file_missing, test_update_nomad_file_success, test_execute_missing_tag... |
| `tests/unit/test_vision_failover.py` | 🟢 Referenced | File: test_vision_failover.py | **Classes:** MockFrameProcessor, MockVisionImageRawFrame<br>**Functions:** test_vision_selection_primary_succeeds, test_vision_selection_fallback_succeeds, test_vision_selection_both_fail, test_yolo_internal_initialization_failover, test_yolo_internal_process_frame_failover... |
| `tests/unit/test_vr_tool.py` | 🧪 Test | File: test_vr_tool.py | **Functions:** test_vr_tool_initialization, test_vr_tool_get_def, test_execute_invalid_room, test_execute_success, test_execute_failure... |
| `tests/unit/test_wasm_tool.py` | 🧪 Test | File: test_wasm_tool.py | **Classes:** TestWasmTool<br>**Functions:** test_process_text_success, test_process_text_missing_file, test_execute_custom_success |
| `tests/unit/test_web_browser_tool.py` | 🟢 Referenced | File: test_web_browser_tool.py | **Classes:** TestWebBrowserTool<br>**Functions:** asyncSetUp, asyncTearDown, test_goto_success, test_goto_failure, test_get_page_content_success... |
| `tests/unit/test_web_server_personality.py` | 🟢 Referenced | File: test_web_server_personality.py | **Functions:** test_get_personality |
| `tests/unit/test_web_server_sync.py` | 🟢 Referenced | File: test_web_server_sync.py | **Functions:** test_internal_chat_sync_success, test_internal_chat_sync_timeout, responder |
| `tests/unit/test_wol_tool.py` | 🧪 Test | File: test_wol_tool.py | **Functions:** test_wol_tool_initialization, test_validate_mac, test_wake_invalid_mac, test_wake_success, test_execute... |
| `tests/unit/test_workflow.py` | 🧪 Test | File: test_workflow.py | **Classes:** MockTool, PromptBuilderNode, DummyTool<br>**Functions:** mock_registry, clear_workflow_cache, test_topological_sort_linear, test_topological_sort_with_cycle, test_workflow_execution_data_flow... |
| `tests/unit/test_world_model_service.py` | 🟢 Referenced | File: test_world_model_service.py | **Functions:** client, mock_mqtt_client, test_health_check, test_on_connect_successful, test_on_connect_failed... |
| `tests/verify_config_load.py` | 🟢 Referenced | File: verify_config_load.py | **Functions:** load_config |
| `tests/verify_dlq.py` | 🟢 Referenced | File: verify_dlq.py | **Functions:** run_server, test_server, run_test |
| `tools/log-vectorizer-mcp/README.md` | 🟢 Referenced | Log Vectorizer MCP Tool |  |
| `tools/log-vectorizer-mcp/generate_db.py` | 🔴 Orphan | usr/bin/env python3 | **Functions:** mock_get_local_embedding, main |
| `tools/log-vectorizer-mcp/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `tools/log-vectorizer-mcp/server.py` | 🟢 Referenced | File: server.py | **Functions:** get_local_embedding, cosine_similarity, ingest_log_file, search_logs |
| `tools/log-vectorizer-mcp/test_server.py` | 🟢 Referenced | File: test_server.py | **Functions:** setup_teardown, test_cosine_similarity, test_ingest_log_file, test_search_logs, test_search_logs_no_db |
| `tools/log-vectorizer-mcp/tests/test_server.py` | 🟢 Referenced | File: test_server.py | **Functions:** test_ingest_log_file |
| `workflows/chaining_pattern.yaml` | 📄 Workflow Config | File: chaining_pattern.yaml |  |
| `workflows/continuous_consolidation.yaml` | 📄 Workflow Config | File: continuous_consolidation.yaml |  |
| `workflows/default_agent_loop.yaml` | 🟢 Referenced | File: default_agent_loop.yaml |  |
| `workflows/dream_workflow.yaml` | 📄 Workflow Config | File: dream_workflow.yaml |  |
| `workflows/routing_pattern.yaml` | 📄 Workflow Config | File: routing_pattern.yaml |  |
| `workflows/tasky_checklist_poc.yaml` | 🟢 Referenced | File: tasky_checklist_poc.yaml |  |

## Dependency Diagram

```mermaid
graph LR
    subgraph dir_Root [Root]
        direction TB
        node_2[".djlint.toml"]
        node_9[".gitattributes"]
        node_1[".gitignore"]
        node_25[".gitmodules"]
        node_11[".julesrules"]
        node_24[".markdownlint.json"]
        node_10[".sops.yaml"]
        node_19[".vulture_whitelist.py"]
        node_32[".yamllint"]
        node_20["AGENTS.md"]
        node_4["GEMINI.md"]
        node_6["LICENSE"]
        node_31["README.md"]
        node_0["README_bridge_networking_fix.md"]
        node_5["TODO.md"]
        node_26["ansible.cfg"]
        node_17["benchmark.py"]
        node_14["benchmark_async.py"]
        node_3["bootstrap.sh"]
        node_28["disk_script.sh"]
        node_34["fix_dep_scanner.py"]
        node_21["hostfile"]
        node_33["inventory.yaml"]
        node_27["local_inventory.ini"]
        node_18["memory_disk_script.sh"]
        node_13["mypy.ini"]
        node_7["nerv_ui.patch"]
        node_22["ontology.yaml"]
        node_29["package.json"]
        node_30["performance_benchmark.py"]
        node_12["playbook.yaml"]
        node_16["pyproject.toml"]
        node_8["pytest.ini"]
        node_23["replace_local_world_model.py"]
        node_15["requirements-dev.txt"]
    end
    subgraph dir__githooks [.githooks]
        direction TB
        node_546["pre-commit"]
    end
    subgraph dir__github [.github]
        direction TB
        node_682["AGENTIC_README.md"]
    end
    subgraph dir__github_workflows [.github/workflows]
        direction TB
        node_686["auto-merge.yml"]
        node_689["ci.yml"]
        node_688["create-issues-from-files.yml"]
        node_687["docker-publish.yml"]
        node_690["jules-queue.yml"]
        node_683["remote-verify.yml"]
        node_685["test-cluster.yml"]
        node_684["unblocked-issues.yml"]
    end
    subgraph dir__husky [.husky]
        direction TB
        node_547["pre-push"]
    end
    subgraph dir__opencode [.opencode]
        direction TB
        node_766["README.md"]
        node_765["opencode.json"]
    end
    subgraph dir_ISSUES [ISSUES]
        direction TB
        node_764["2024-04-16-test-unblocked-issues-workflow.md"]
    end
    subgraph dir_ansible [ansible]
        direction TB
        node_966["README.md"]
        node_964["lint_nomad.yaml"]
        node_963["requirements.yml"]
        node_965["run_download_models.yaml"]
    end
    subgraph dir_ansible_filter_plugins [ansible/filter_plugins]
        direction TB
        node_969["README.md"]
        node_968["safe_flatten.py"]
    end
    subgraph dir_ansible_jobs [ansible/jobs]
        direction TB
        node_997["README.md"]
        node_986["authentik.nomad"]
        node_995["benchmark.nomad"]
        node_1001["code-runner-service.nomad"]
        node_1002["ds4-server.nomad.j2"]
        node_976["dummy_web_service.nomad"]
        node_1000["e2a.nomad.j2"]
        node_988["evolve-prompt.nomad.j2"]
        node_992["expert-debug.nomad"]
        node_998["expert.nomad.j2"]
        node_984["filebrowser.nomad.j2"]
        node_978["health-check.nomad.j2"]
        node_990["helixdb.nomad"]
        node_982["llamacpp-batch.nomad.j2"]
        node_985["llamacpp-rpc.nomad.j2"]
        node_996["model-benchmark.nomad.j2"]
        node_994["opengravity.nomad.j2"]
        node_983["pipecatapp.nomad"]
        node_993["postgres.nomad"]
        node_980["rag-service.nomad"]
        node_999["redis.nomad"]
        node_977["router.nomad.j2"]
        node_991["smol-agent-server.nomad.j2"]
        node_989["ternlight-service.nomad"]
        node_981["test-runner.nomad.j2"]
        node_987["tml-interaction.nomad.j2"]
        node_979["vllm.nomad.j2"]
    end
    subgraph dir_ansible_roles [ansible/roles]
        direction TB
        node_1003["README.md"]
    end
    subgraph dir_ansible_roles_apt_proxy_tasks [ansible/roles/apt_proxy/tasks]
        direction TB
        node_1090["main.yml"]
    end
    subgraph dir_ansible_roles_apt_proxy_templates [ansible/roles/apt_proxy/templates]
        direction TB
        node_1089["apt_proxy.nomad.j2"]
    end
    subgraph dir_ansible_roles_authentik_defaults [ansible/roles/authentik/defaults]
        direction TB
        node_1347["main.yml"]
    end
    subgraph dir_ansible_roles_authentik_tasks [ansible/roles/authentik/tasks]
        direction TB
        node_1346["main.yml"]
    end
    subgraph dir_ansible_roles_authentik_templates [ansible/roles/authentik/templates]
        direction TB
        node_1345["authentik.nomad.j2"]
    end
    subgraph dir_ansible_roles_benchmark_models_tasks [ansible/roles/benchmark_models/tasks]
        direction TB
        node_1189["benchmark_loop.yaml"]
        node_1188["main.yaml"]
    end
    subgraph dir_ansible_roles_benchmark_models_templates [ansible/roles/benchmark_models/templates]
        direction TB
        node_1187["model-benchmark.nomad.j2"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_defaults [ansible/roles/bootstrap_agent/defaults]
        direction TB
        node_1332["main.yaml"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_handlers [ansible/roles/bootstrap_agent/handlers]
        direction TB
        node_1329["main.yaml"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_tasks [ansible/roles/bootstrap_agent/tasks]
        direction TB
        node_1331["deploy_llama_cpp_model.yaml"]
        node_1330["main.yaml"]
    end
    subgraph dir_ansible_roles_btrfs_snapshot_defaults [ansible/roles/btrfs_snapshot/defaults]
        direction TB
        node_1157["main.yaml"]
    end
    subgraph dir_ansible_roles_btrfs_snapshot_tasks [ansible/roles/btrfs_snapshot/tasks]
        direction TB
        node_1156["main.yaml"]
    end
    subgraph dir_ansible_roles_clamav_files [ansible/roles/clamav/files]
        direction TB
        node_1328["rogue_agent.ldb"]
    end
    subgraph dir_ansible_roles_clamav_handlers [ansible/roles/clamav/handlers]
        direction TB
        node_1326["main.yaml"]
    end
    subgraph dir_ansible_roles_clamav_tasks [ansible/roles/clamav/tasks]
        direction TB
        node_1327["main.yaml"]
    end
    subgraph dir_ansible_roles_claude_clone_tasks [ansible/roles/claude_clone/tasks]
        direction TB
        node_1140["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tools_tasks [ansible/roles/common-tools/tasks]
        direction TB
        node_1143["main.yaml"]
    end
    subgraph dir_ansible_roles_common_handlers [ansible/roles/common/handlers]
        direction TB
        node_1065["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tasks [ansible/roles/common/tasks]
        direction TB
        node_1066["main.yaml"]
        node_1067["network_repair.yaml"]
    end
    subgraph dir_ansible_roles_common_templates [ansible/roles/common/templates]
        direction TB
        node_1062["cluster-ip-alias.service.j2"]
        node_1063["hosts.j2"]
        node_1064["update-ssh-authorized-keys.sh.j2"]
    end
    subgraph dir_ansible_roles_config_manager_tasks [ansible/roles/config_manager/tasks]
        direction TB
        node_1314["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_defaults [ansible/roles/consul/defaults]
        direction TB
        node_1239["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_handlers [ansible/roles/consul/handlers]
        direction TB
        node_1235["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_tasks [ansible/roles/consul/tasks]
        direction TB
        node_1237["acl.yaml"]
        node_1236["main.yaml"]
        node_1238["tls.yaml"]
    end
    subgraph dir_ansible_roles_consul_templates [ansible/roles/consul/templates]
        direction TB
        node_1233["consul.hcl.j2"]
        node_1234["consul.service.j2"]
    end
    subgraph dir_ansible_roles_desktop_extras_tasks [ansible/roles/desktop_extras/tasks]
        direction TB
        node_1223["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_handlers [ansible/roles/docker/handlers]
        direction TB
        node_1132["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_molecule_default [ansible/roles/docker/molecule/default]
        direction TB
        node_1136["converge.yml"]
        node_1134["molecule.yml"]
        node_1137["prepare.yml"]
        node_1135["verify.yml"]
    end
    subgraph dir_ansible_roles_docker_tasks [ansible/roles/docker/tasks]
        direction TB
        node_1133["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_templates [ansible/roles/docker/templates]
        direction TB
        node_1131["daemon.json.j2"]
        node_1130["docker-prune.service.j2"]
        node_1129["docker-prune.timer.j2"]
    end
    subgraph dir_ansible_roles_download_models_files [ansible/roles/download_models/files]
        direction TB
        node_1142["download_hf_repo.py"]
    end
    subgraph dir_ansible_roles_download_models_tasks [ansible/roles/download_models/tasks]
        direction TB
        node_1141["main.yaml"]
    end
    subgraph dir_ansible_roles_ds4_defaults [ansible/roles/ds4/defaults]
        direction TB
        node_1342["main.yaml"]
    end
    subgraph dir_ansible_roles_ds4_tasks [ansible/roles/ds4/tasks]
        direction TB
        node_1341["main.yaml"]
    end
    subgraph dir_ansible_roles_e2a_tasks [ansible/roles/e2a/tasks]
        direction TB
        node_1259["main.yml"]
    end
    subgraph dir_ansible_roles_e2a_templates [ansible/roles/e2a/templates]
        direction TB
        node_1258["e2a.nomad.j2"]
    end
    subgraph dir_ansible_roles_exo_defaults [ansible/roles/exo/defaults]
        direction TB
        node_1353["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_files [ansible/roles/exo/files]
        direction TB
        node_1354["Dockerfile"]
    end
    subgraph dir_ansible_roles_exo_tasks [ansible/roles/exo/tasks]
        direction TB
        node_1352["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_templates [ansible/roles/exo/templates]
        direction TB
        node_1351["exo.nomad.j2"]
        node_1350["load_image_task.nomad.j2"]
    end
    subgraph dir_ansible_roles_forgejo_handlers [ansible/roles/forgejo/handlers]
        direction TB
        node_1197["main.yaml"]
    end
    subgraph dir_ansible_roles_forgejo_tasks [ansible/roles/forgejo/tasks]
        direction TB
        node_1198["main.yaml"]
    end
    subgraph dir_ansible_roles_forgejo_templates [ansible/roles/forgejo/templates]
        direction TB
        node_1196["forgejo.nomad.j2"]
    end
    subgraph dir_ansible_roles_gemini_cli_handlers [ansible/roles/gemini_cli/handlers]
        direction TB
        node_1087["main.yaml"]
    end
    subgraph dir_ansible_roles_gemini_cli_tasks [ansible/roles/gemini_cli/tasks]
        direction TB
        node_1088["main.yaml"]
    end
    subgraph dir_ansible_roles_gemini_cli_templates [ansible/roles/gemini_cli/templates]
        direction TB
        node_1086["gemini.nomad.j2"]
    end
    subgraph dir_ansible_roles_gpu_setup_defaults [ansible/roles/gpu_setup/defaults]
        direction TB
        node_1027["main.yaml"]
    end
    subgraph dir_ansible_roles_gpu_setup_tasks [ansible/roles/gpu_setup/tasks]
        direction TB
        node_1026["main.yaml"]
    end
    subgraph dir_ansible_roles_gpu_setup_templates [ansible/roles/gpu_setup/templates]
        direction TB
        node_1025["ai-cluster-env.sh.j2"]
    end
    subgraph dir_ansible_roles_headscale_defaults [ansible/roles/headscale/defaults]
        direction TB
        node_1036["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_handlers [ansible/roles/headscale/handlers]
        direction TB
        node_1034["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_tasks [ansible/roles/headscale/tasks]
        direction TB
        node_1035["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_templates [ansible/roles/headscale/templates]
        direction TB
        node_1033["config.yaml.j2"]
        node_1032["headscale.service.j2"]
    end
    subgraph dir_ansible_roles_heretic_tool_defaults [ansible/roles/heretic_tool/defaults]
        direction TB
        node_1186["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_meta [ansible/roles/heretic_tool/meta]
        direction TB
        node_1185["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_tasks [ansible/roles/heretic_tool/tasks]
        direction TB
        node_1184["main.yaml"]
    end
    subgraph dir_ansible_roles_hermes_agent_tasks [ansible/roles/hermes_agent/tasks]
        direction TB
        node_1155["main.yaml"]
    end
    subgraph dir_ansible_roles_influxdb [ansible/roles/influxdb]
        direction TB
        node_1021["README.md"]
    end
    subgraph dir_ansible_roles_influxdb_meta [ansible/roles/influxdb/meta]
        direction TB
        node_1024["main.yaml"]
    end
    subgraph dir_ansible_roles_influxdb_tasks [ansible/roles/influxdb/tasks]
        direction TB
        node_1023["main.yaml"]
    end
    subgraph dir_ansible_roles_influxdb_templates [ansible/roles/influxdb/templates]
        direction TB
        node_1022["influxdb.nomad.j2"]
    end
    subgraph dir_ansible_roles_ipfs_tasks [ansible/roles/ipfs/tasks]
        direction TB
        node_1169["main.yaml"]
    end
    subgraph dir_ansible_roles_ipfs_templates [ansible/roles/ipfs/templates]
        direction TB
        node_1168["ipfs.nomad.j2"]
    end
    subgraph dir_ansible_roles_kittentts_tasks [ansible/roles/kittentts/tasks]
        direction TB
        node_1041["main.yaml"]
    end
    subgraph dir_ansible_roles_librarian_defaults [ansible/roles/librarian/defaults]
        direction TB
        node_1163["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_handlers [ansible/roles/librarian/handlers]
        direction TB
        node_1161["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_tasks [ansible/roles/librarian/tasks]
        direction TB
        node_1162["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_templates [ansible/roles/librarian/templates]
        direction TB
        node_1160["librarian.service.j2"]
        node_1158["librarian_agent.py.j2"]
        node_1159["spacedrive.service.j2"]
    end
    subgraph dir_ansible_roles_llama_cpp_files [ansible/roles/llama_cpp/files]
        direction TB
        node_1074["realtime_steering.patch"]
    end
    subgraph dir_ansible_roles_llama_cpp_handlers [ansible/roles/llama_cpp/handlers]
        direction TB
        node_1068["main.yaml"]
    end
    subgraph dir_ansible_roles_llama_cpp_molecule_default [ansible/roles/llama_cpp/molecule/default]
        direction TB
        node_1073["converge.yml"]
        node_1071["molecule.yml"]
        node_1072["verify.yml"]
    end
    subgraph dir_ansible_roles_llama_cpp_tasks [ansible/roles/llama_cpp/tasks]
        direction TB
        node_1069["main.yaml"]
        node_1070["run_single_rpc_job.yaml"]
    end
    subgraph dir_ansible_roles_llmfit_tasks [ansible/roles/llmfit/tasks]
        direction TB
        node_1344["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_tasks [ansible/roles/llxprt_code/tasks]
        direction TB
        node_1349["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_templates [ansible/roles/llxprt_code/templates]
        direction TB
        node_1348["llxprt-code.env.j2"]
    end
    subgraph dir_ansible_roles_magic_mirror_defaults [ansible/roles/magic_mirror/defaults]
        direction TB
        node_1031["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_handlers [ansible/roles/magic_mirror/handlers]
        direction TB
        node_1029["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_tasks [ansible/roles/magic_mirror/tasks]
        direction TB
        node_1030["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_templates [ansible/roles/magic_mirror/templates]
        direction TB
        node_1028["magic_mirror.nomad.j2"]
    end
    subgraph dir_ansible_roles_mcp_server_defaults [ansible/roles/mcp_server/defaults]
        direction TB
        node_1227["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_handlers [ansible/roles/mcp_server/handlers]
        direction TB
        node_1225["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_tasks [ansible/roles/mcp_server/tasks]
        direction TB
        node_1226["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_templates [ansible/roles/mcp_server/templates]
        direction TB
        node_1224["mcp_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_graph_tasks [ansible/roles/memory_graph/tasks]
        direction TB
        node_1305["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_graph_templates [ansible/roles/memory_graph/templates]
        direction TB
        node_1303["load_image_task.nomad.j2"]
        node_1304["memory-graph.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_service_files [ansible/roles/memory_service/files]
        direction TB
        node_1148["app.py"]
        node_1149["pmm_memory.py"]
    end
    subgraph dir_ansible_roles_memory_service_handlers [ansible/roles/memory_service/handlers]
        direction TB
        node_1146["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_tasks [ansible/roles/memory_service/tasks]
        direction TB
        node_1147["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_templates [ansible/roles/memory_service/templates]
        direction TB
        node_1144["load_image_task.nomad.j2"]
        node_1145["memory_service.nomad.j2"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files [ansible/roles/minikeyvalue/files]
        direction TB
        node_1046["Dockerfile"]
        node_1048["start_master.py"]
        node_1047["volume"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files_src [ansible/roles/minikeyvalue/files/src]
        direction TB
        node_1049["lib.go"]
        node_1052["lib_test.go"]
        node_1054["main.go"]
        node_1055["rebalance.go"]
        node_1050["rebuild.go"]
        node_1051["s3api.go"]
        node_1053["server.go"]
    end
    subgraph dir_ansible_roles_minikeyvalue_tasks [ansible/roles/minikeyvalue/tasks]
        direction TB
        node_1045["main.yaml"]
    end
    subgraph dir_ansible_roles_minikeyvalue_templates [ansible/roles/minikeyvalue/templates]
        direction TB
        node_1044["mkv.nomad.j2"]
    end
    subgraph dir_ansible_roles_miniray_files [ansible/roles/miniray/files]
        direction TB
        node_1313["Dockerfile"]
    end
    subgraph dir_ansible_roles_miniray_tasks [ansible/roles/miniray/tasks]
        direction TB
        node_1312["main.yaml"]
    end
    subgraph dir_ansible_roles_miniray_templates [ansible/roles/miniray/templates]
        direction TB
        node_1311["miniray.nomad.j2"]
    end
    subgraph dir_ansible_roles_moe_gateway_files [ansible/roles/moe_gateway/files]
        direction TB
        node_1127["gateway.py"]
    end
    subgraph dir_ansible_roles_moe_gateway_files_static [ansible/roles/moe_gateway/files/static]
        direction TB
        node_1128["index.html"]
    end
    subgraph dir_ansible_roles_moe_gateway_handlers [ansible/roles/moe_gateway/handlers]
        direction TB
        node_1125["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_tasks [ansible/roles/moe_gateway/tasks]
        direction TB
        node_1126["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_templates [ansible/roles/moe_gateway/templates]
        direction TB
        node_1124["moe-gateway.nomad.j2"]
    end
    subgraph dir_ansible_roles_monitoring_defaults [ansible/roles/monitoring/defaults]
        direction TB
        node_1252["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_files [ansible/roles/monitoring/files]
        direction TB
        node_1253["llm_dashboard.json"]
    end
    subgraph dir_ansible_roles_monitoring_tasks [ansible/roles/monitoring/tasks]
        direction TB
        node_1251["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_templates [ansible/roles/monitoring/templates]
        direction TB
        node_1243["beszel-agent.nomad.j2"]
        node_1240["beszel-hub.nomad.j2"]
        node_1245["dashboards.yaml.j2"]
        node_1244["datasource.yaml.j2"]
        node_1250["grafana.nomad.j2"]
        node_1241["memory-audit.nomad.j2"]
        node_1242["mqtt-exporter.nomad.j2"]
        node_1249["node-exporter.nomad.j2"]
        node_1246["prometheus.nomad.j2"]
        node_1248["prometheus.yml.j2"]
        node_1247["statsping.nomad.j2"]
    end
    subgraph dir_ansible_roles_mqtt_meta [ansible/roles/mqtt/meta]
        direction TB
        node_1167["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_tasks [ansible/roles/mqtt/tasks]
        direction TB
        node_1166["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_templates [ansible/roles/mqtt/templates]
        direction TB
        node_1164["mosquitto.conf.j2"]
        node_1165["mqtt.nomad.j2"]
    end
    subgraph dir_ansible_roles_nanochat_defaults [ansible/roles/nanochat/defaults]
        direction TB
        node_1309["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_handlers [ansible/roles/nanochat/handlers]
        direction TB
        node_1307["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_tasks [ansible/roles/nanochat/tasks]
        direction TB
        node_1308["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_templates [ansible/roles/nanochat/templates]
        direction TB
        node_1306["nanochat.nomad.j2"]
    end
    subgraph dir_ansible_roles_nats_handlers [ansible/roles/nats/handlers]
        direction TB
        node_1200["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_tasks [ansible/roles/nats/tasks]
        direction TB
        node_1201["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_templates [ansible/roles/nats/templates]
        direction TB
        node_1199["nats.nomad.j2"]
    end
    subgraph dir_ansible_roles_nfs_handlers [ansible/roles/nfs/handlers]
        direction TB
        node_1298["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_tasks [ansible/roles/nfs/tasks]
        direction TB
        node_1299["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_templates [ansible/roles/nfs/templates]
        direction TB
        node_1297["exports.j2"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_handlers [ansible/roles/nixos_pxe_server/handlers]
        direction TB
        node_1335["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_tasks [ansible/roles/nixos_pxe_server/tasks]
        direction TB
        node_1336["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_templates [ansible/roles/nixos_pxe_server/templates]
        direction TB
        node_1334["boot.ipxe.nix.j2"]
        node_1333["configuration.nix.j2"]
    end
    subgraph dir_ansible_roles_nomad_defaults [ansible/roles/nomad/defaults]
        direction TB
        node_1017["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_handlers [ansible/roles/nomad/handlers]
        direction TB
        node_1013["main.yaml"]
        node_1014["restart_nomad_handler_tasks.yaml"]
    end
    subgraph dir_ansible_roles_nomad_tasks [ansible/roles/nomad/tasks]
        direction TB
        node_1015["main.yaml"]
        node_1016["tls.yaml"]
    end
    subgraph dir_ansible_roles_nomad_templates [ansible/roles/nomad/templates]
        direction TB
        node_1010["client.hcl.j2"]
        node_1008["nomad.hcl.server.j2"]
        node_1011["nomad.service.j2"]
        node_1012["nomad.sh.j2"]
        node_1009["server.hcl.j2"]
        node_1007["start_nomad.sh.j2"]
    end
    subgraph dir_ansible_roles_openclaw_files [ansible/roles/openclaw/files]
        direction TB
        node_1078["Dockerfile"]
        node_1079["pipecat_skill.md"]
    end
    subgraph dir_ansible_roles_openclaw_tasks [ansible/roles/openclaw/tasks]
        direction TB
        node_1077["main.yaml"]
    end
    subgraph dir_ansible_roles_openclaw_templates [ansible/roles/openclaw/templates]
        direction TB
        node_1075["load_image_task.nomad.j2"]
        node_1076["openclaw.nomad.j2"]
    end
    subgraph dir_ansible_roles_opencode_handlers [ansible/roles/opencode/handlers]
        direction TB
        node_1005["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_tasks [ansible/roles/opencode/tasks]
        direction TB
        node_1006["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_templates [ansible/roles/opencode/templates]
        direction TB
        node_1004["opencode.nomad.j2"]
    end
    subgraph dir_ansible_roles_opengist_handlers [ansible/roles/opengist/handlers]
        direction TB
        node_1194["main.yaml"]
    end
    subgraph dir_ansible_roles_opengist_tasks [ansible/roles/opengist/tasks]
        direction TB
        node_1195["main.yaml"]
    end
    subgraph dir_ansible_roles_opengist_templates [ansible/roles/opengist/templates]
        direction TB
        node_1193["opengist.nomad.j2"]
    end
    subgraph dir_ansible_roles_opengravity_meta [ansible/roles/opengravity/meta]
        direction TB
        node_1363["main.yaml"]
    end
    subgraph dir_ansible_roles_opengravity_tasks [ansible/roles/opengravity/tasks]
        direction TB
        node_1362["main.yaml"]
    end
    subgraph dir_ansible_roles_opengravity_templates [ansible/roles/opengravity/templates]
        direction TB
        node_1359["Dockerfile.j2"]
        node_1360["default.conf.j2"]
        node_1358["load_image_task.nomad.j2"]
        node_1361["opengravity.nomad.j2"]
    end
    subgraph dir_ansible_roles_openworkers_handlers [ansible/roles/openworkers/handlers]
        direction TB
        node_1153["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_tasks [ansible/roles/openworkers/tasks]
        direction TB
        node_1154["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_templates [ansible/roles/openworkers/templates]
        direction TB
        node_1151["openworkers-bootstrap.nomad.j2"]
        node_1152["openworkers-infra.nomad.j2"]
        node_1150["openworkers-runners.nomad.j2"]
    end
    subgraph dir_ansible_roles_paddler_tasks [ansible/roles/paddler/tasks]
        direction TB
        node_1212["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent [ansible/roles/paddler_agent]
        direction TB
        node_1337["README.md"]
    end
    subgraph dir_ansible_roles_paddler_agent_defaults [ansible/roles/paddler_agent/defaults]
        direction TB
        node_1340["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_tasks [ansible/roles/paddler_agent/tasks]
        direction TB
        node_1339["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_templates [ansible/roles/paddler_agent/templates]
        direction TB
        node_1338["paddler-agent.service.j2"]
    end
    subgraph dir_ansible_roles_paddler_balancer [ansible/roles/paddler_balancer]
        direction TB
        node_1095["README.md"]
    end
    subgraph dir_ansible_roles_paddler_balancer_defaults [ansible/roles/paddler_balancer/defaults]
        direction TB
        node_1098["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_tasks [ansible/roles/paddler_balancer/tasks]
        direction TB
        node_1097["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_templates [ansible/roles/paddler_balancer/templates]
        direction TB
        node_1096["paddler-balancer.service.j2"]
    end
    subgraph dir_ansible_roles_paperless_handlers [ansible/roles/paperless/handlers]
        direction TB
        node_1318["main.yaml"]
    end
    subgraph dir_ansible_roles_paperless_tasks [ansible/roles/paperless/tasks]
        direction TB
        node_1319["main.yaml"]
    end
    subgraph dir_ansible_roles_paperless_templates [ansible/roles/paperless/templates]
        direction TB
        node_1315["paperless-app.nomad.j2"]
        node_1316["paperless-db.nomad.j2"]
        node_1317["paperless-redis.nomad.j2"]
    end
    subgraph dir_ansible_roles_pds_tasks [ansible/roles/pds/tasks]
        direction TB
        node_1211["main.yaml"]
    end
    subgraph dir_ansible_roles_pds_templates [ansible/roles/pds/templates]
        direction TB
        node_1210["pds.nomad.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_defaults [ansible/roles/pipecatapp/defaults]
        direction TB
        node_1118["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_handlers [ansible/roles/pipecatapp/handlers]
        direction TB
        node_1116["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_tasks [ansible/roles/pipecatapp/tasks]
        direction TB
        node_1117["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates [ansible/roles/pipecatapp/templates]
        direction TB
        node_1103["architect.nomad.j2"]
        node_1100["archivist.nomad.j2"]
        node_1099["load_image_task.nomad.j2"]
        node_1104["pipecat.env.j2"]
        node_1101["pipecatapp.nomad.j2"]
        node_1105["seed-agent.nomad.j2"]
        node_1102["start_pipecatapp.sh.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_prompts [ansible/roles/pipecatapp/templates/prompts]
        direction TB
        node_1111["coding_expert.txt.j2"]
        node_1114["consolidation_expert.txt.j2"]
        node_1113["creative_expert.txt.j2"]
        node_1108["cynic_expert.txt.j2"]
        node_1109["ingestion_expert.txt.j2"]
        node_1112["memory_query_expert.txt.j2"]
        node_1110["router.txt.j2"]
        node_1115["tron_agent.txt.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_workflows [ansible/roles/pipecatapp/templates/workflows]
        direction TB
        node_1107["architect_loop.yaml.j2"]
        node_1106["default_agent_loop.yaml.j2"]
    end
    subgraph dir_ansible_roles_pollen [ansible/roles/pollen]
        direction TB
        node_1138["README.md"]
    end
    subgraph dir_ansible_roles_pollen_tasks [ansible/roles/pollen/tasks]
        direction TB
        node_1139["main.yml"]
    end
    subgraph dir_ansible_roles_polyphony_handlers [ansible/roles/polyphony/handlers]
        direction TB
        node_1191["main.yaml"]
    end
    subgraph dir_ansible_roles_polyphony_tasks [ansible/roles/polyphony/tasks]
        direction TB
        node_1192["main.yaml"]
    end
    subgraph dir_ansible_roles_polyphony_templates [ansible/roles/polyphony/templates]
        direction TB
        node_1190["polyphony.nomad.j2"]
    end
    subgraph dir_ansible_roles_postgres_handlers [ansible/roles/postgres/handlers]
        direction TB
        node_1356["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_tasks [ansible/roles/postgres/tasks]
        direction TB
        node_1357["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_templates [ansible/roles/postgres/templates]
        direction TB
        node_1355["postgres.nomad.j2"]
    end
    subgraph dir_ansible_roles_power_manager_defaults [ansible/roles/power_manager/defaults]
        direction TB
        node_1220["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_files [ansible/roles/power_manager/files]
        direction TB
        node_1221["power_agent.py"]
        node_1222["traffic_monitor.c"]
    end
    subgraph dir_ansible_roles_power_manager_handlers [ansible/roles/power_manager/handlers]
        direction TB
        node_1218["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_tasks [ansible/roles/power_manager/tasks]
        direction TB
        node_1219["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_templates [ansible/roles/power_manager/templates]
        direction TB
        node_1215["nomad-watchdog.service.j2"]
        node_1216["power-agent.service.j2"]
        node_1217["watchdog.sh.j2"]
    end
    subgraph dir_ansible_roles_preflight_checks_tasks [ansible/roles/preflight_checks/tasks]
        direction TB
        node_1325["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_files [ansible/roles/provisioning_api/files]
        direction TB
        node_1061["provisioning_api.py"]
    end
    subgraph dir_ansible_roles_provisioning_api_handlers [ansible/roles/provisioning_api/handlers]
        direction TB
        node_1059["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_tasks [ansible/roles/provisioning_api/tasks]
        direction TB
        node_1060["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_templates [ansible/roles/provisioning_api/templates]
        direction TB
        node_1058["provisioning-api.service.j2"]
    end
    subgraph dir_ansible_roles_pxe_server_defaults [ansible/roles/pxe_server/defaults]
        direction TB
        node_1207["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_handlers [ansible/roles/pxe_server/handlers]
        direction TB
        node_1205["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_tasks [ansible/roles/pxe_server/tasks]
        direction TB
        node_1206["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_templates [ansible/roles/pxe_server/templates]
        direction TB
        node_1202["boot.ipxe.j2"]
        node_1203["dhcpd.conf.j2"]
        node_1204["preseed.cfg.j2"]
    end
    subgraph dir_ansible_roles_pypi_proxy_tasks [ansible/roles/pypi_proxy/tasks]
        direction TB
        node_1209["main.yml"]
    end
    subgraph dir_ansible_roles_pypi_proxy_templates [ansible/roles/pypi_proxy/templates]
        direction TB
        node_1208["pypi_proxy.nomad.j2"]
    end
    subgraph dir_ansible_roles_python_deps_files [ansible/roles/python_deps/files]
        direction TB
        node_1302["requirements.txt"]
    end
    subgraph dir_ansible_roles_python_deps_meta [ansible/roles/python_deps/meta]
        direction TB
        node_1301["main.yaml"]
    end
    subgraph dir_ansible_roles_python_deps_tasks [ansible/roles/python_deps/tasks]
        direction TB
        node_1300["main.yaml"]
    end
    subgraph dir_ansible_roles_seed_models_files_reference_data [ansible/roles/seed_models/files/reference_data]
        direction TB
        node_1043["README.md"]
    end
    subgraph dir_ansible_roles_seed_models_tasks [ansible/roles/seed_models/tasks]
        direction TB
        node_1042["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_defaults [ansible/roles/semantic_router/defaults]
        direction TB
        node_1231["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_tasks [ansible/roles/semantic_router/tasks]
        direction TB
        node_1230["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_templates [ansible/roles/semantic_router/templates]
        direction TB
        node_1228["Dockerfile.j2"]
        node_1229["semantic-router.nomad.j2"]
    end
    subgraph dir_ansible_roles_smol_agent_server_tasks [ansible/roles/smol_agent_server/tasks]
        direction TB
        node_1057["main.yaml"]
    end
    subgraph dir_ansible_roles_smol_agent_server_templates [ansible/roles/smol_agent_server/templates]
        direction TB
        node_1056["smol-agent.nomad.j2"]
    end
    subgraph dir_ansible_roles_sunshine_defaults [ansible/roles/sunshine/defaults]
        direction TB
        node_1094["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_handlers [ansible/roles/sunshine/handlers]
        direction TB
        node_1092["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_tasks [ansible/roles/sunshine/tasks]
        direction TB
        node_1093["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_templates [ansible/roles/sunshine/templates]
        direction TB
        node_1091["sunshine.nomad.j2"]
    end
    subgraph dir_ansible_roles_system_deps_tasks [ansible/roles/system_deps/tasks]
        direction TB
        node_1037["main.yaml"]
    end
    subgraph dir_ansible_roles_tailscale_tasks [ansible/roles/tailscale/tasks]
        direction TB
        node_1310["main.yaml"]
    end
    subgraph dir_ansible_roles_telegraf [ansible/roles/telegraf]
        direction TB
        node_1170["README.md"]
    end
    subgraph dir_ansible_roles_telegraf_meta [ansible/roles/telegraf/meta]
        direction TB
        node_1174["main.yaml"]
    end
    subgraph dir_ansible_roles_telegraf_tasks [ansible/roles/telegraf/tasks]
        direction TB
        node_1173["main.yaml"]
    end
    subgraph dir_ansible_roles_telegraf_templates [ansible/roles/telegraf/templates]
        direction TB
        node_1172["telegraf.conf.j2"]
        node_1171["telegraf.nomad.j2"]
    end
    subgraph dir_ansible_roles_term_everything_tasks [ansible/roles/term_everything/tasks]
        direction TB
        node_1343["main.yml"]
    end
    subgraph dir_ansible_roles_tml_interaction [ansible/roles/tml_interaction]
        direction TB
        node_1213["README.md"]
    end
    subgraph dir_ansible_roles_tml_interaction_tasks [ansible/roles/tml_interaction/tasks]
        direction TB
        node_1214["main.yaml"]
    end
    subgraph dir_ansible_roles_tool_server [ansible/roles/tool_server]
        direction TB
        node_1261["Dockerfile"]
        node_1260["app.py"]
        node_1264["entrypoint.sh"]
        node_1262["pmm_memory.py"]
        node_1263["preload_models.py"]
    end
    subgraph dir_ansible_roles_tool_server_tasks [ansible/roles/tool_server/tasks]
        direction TB
        node_1267["main.yaml"]
    end
    subgraph dir_ansible_roles_tool_server_templates [ansible/roles/tool_server/templates]
        direction TB
        node_1265["load_image_task.nomad.j2"]
        node_1266["tool_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_tool_server_tools [ansible/roles/tool_server/tools]
        direction TB
        node_1290["ansible_tool.py"]
        node_1292["archivist_tool.py"]
        node_1271["claude_clone_tool.py"]
        node_1294["code_runner_tool.py"]
        node_1287["council_tool.py"]
        node_1285["desktop_control_tool.py"]
        node_1284["file_editor_tool.py"]
        node_1268["final_answer_tool.py"]
        node_1279["gemini_cli.py"]
        node_1278["get_nomad_job.py"]
        node_1289["git_tool.py"]
        node_1273["ha_tool.py"]
        node_1282["llxprt_code_tool.py"]
        node_1269["mcp_tool.py"]
        node_1277["opencode_tool.py"]
        node_1274["orchestrator_tool.py"]
        node_1296["planner_tool.py"]
        node_1276["power_tool.py"]
        node_1270["project_mapper_tool.py"]
        node_1295["prompt_improver_tool.py"]
        node_1291["rag_tool.py"]
        node_1293["sandbox.ts"]
        node_1275["smol_agent_tool.py"]
        node_1272["ssh_tool.py"]
        node_1288["summarizer_tool.py"]
        node_1280["swarm_tool.py"]
        node_1281["tap_service.py"]
        node_1283["term_everything_tool.py"]
        node_1286["web_browser_tool.py"]
    end
    subgraph dir_ansible_roles_tpm_ssh_handlers [ansible/roles/tpm_ssh/handlers]
        direction TB
        node_1323["main.yaml"]
    end
    subgraph dir_ansible_roles_tpm_ssh_tasks [ansible/roles/tpm_ssh/tasks]
        direction TB
        node_1324["main.yaml"]
    end
    subgraph dir_ansible_roles_tpm_ssh_templates [ansible/roles/tpm_ssh/templates]
        direction TB
        node_1320["tpm-ssh-agent.service.j2"]
        node_1321["tpm-ssh-agent.sh.j2"]
        node_1322["tpm_pins.j2"]
    end
    subgraph dir_ansible_roles_traceway_defaults [ansible/roles/traceway/defaults]
        direction TB
        node_1020["main.yaml"]
    end
    subgraph dir_ansible_roles_traceway_tasks [ansible/roles/traceway/tasks]
        direction TB
        node_1019["main.yaml"]
    end
    subgraph dir_ansible_roles_traceway_templates [ansible/roles/traceway/templates]
        direction TB
        node_1018["traceway.nomad.j2"]
    end
    subgraph dir_ansible_roles_traefik_defaults [ansible/roles/traefik/defaults]
        direction TB
        node_1183["main.yml"]
    end
    subgraph dir_ansible_roles_traefik_tasks [ansible/roles/traefik/tasks]
        direction TB
        node_1182["main.yml"]
    end
    subgraph dir_ansible_roles_traefik_templates [ansible/roles/traefik/templates]
        direction TB
        node_1181["headscale-router.yaml.j2"]
        node_1180["traefik.nomad.j2"]
    end
    subgraph dir_ansible_roles_unified_fs_defaults [ansible/roles/unified_fs/defaults]
        direction TB
        node_1178["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_files [ansible/roles/unified_fs/files]
        direction TB
        node_1179["unified_fs_agent.py"]
    end
    subgraph dir_ansible_roles_unified_fs_handlers [ansible/roles/unified_fs/handlers]
        direction TB
        node_1176["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_tasks [ansible/roles/unified_fs/tasks]
        direction TB
        node_1177["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_templates [ansible/roles/unified_fs/templates]
        direction TB
        node_1175["unified_fs.service.j2"]
    end
    subgraph dir_ansible_roles_vision_defaults [ansible/roles/vision/defaults]
        direction TB
        node_1123["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_handlers [ansible/roles/vision/handlers]
        direction TB
        node_1121["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_tasks [ansible/roles/vision/tasks]
        direction TB
        node_1122["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_templates [ansible/roles/vision/templates]
        direction TB
        node_1119["config.yml.j2"]
        node_1120["vision.nomad.j2"]
    end
    subgraph dir_ansible_roles_vllm_tasks [ansible/roles/vllm/tasks]
        direction TB
        node_1040["main.yaml"]
        node_1039["run_single_vllm_job.yaml"]
    end
    subgraph dir_ansible_roles_vllm_templates [ansible/roles/vllm/templates]
        direction TB
        node_1038["vllm-expert.nomad.j2"]
    end
    subgraph dir_ansible_roles_whisper_cpp_tasks [ansible/roles/whisper_cpp/tasks]
        direction TB
        node_1232["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service_files [ansible/roles/world_model_service/files]
        direction TB
        node_1083["Dockerfile"]
        node_1082["app.py"]
        node_1084["debug_world_model.sh"]
        node_1085["requirements.txt"]
    end
    subgraph dir_ansible_roles_world_model_service_tasks [ansible/roles/world_model_service/tasks]
        direction TB
        node_1081["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service_templates [ansible/roles/world_model_service/templates]
        direction TB
        node_1080["world_model.nomad.j2"]
    end
    subgraph dir_ansible_roles_zigbee2mqtt [ansible/roles/zigbee2mqtt]
        direction TB
        node_1254["README.md"]
    end
    subgraph dir_ansible_roles_zigbee2mqtt_meta [ansible/roles/zigbee2mqtt/meta]
        direction TB
        node_1257["main.yaml"]
    end
    subgraph dir_ansible_roles_zigbee2mqtt_tasks [ansible/roles/zigbee2mqtt/tasks]
        direction TB
        node_1256["main.yaml"]
    end
    subgraph dir_ansible_roles_zigbee2mqtt_templates [ansible/roles/zigbee2mqtt/templates]
        direction TB
        node_1255["zigbee2mqtt.nomad.j2"]
    end
    subgraph dir_ansible_tasks [ansible/tasks]
        direction TB
        node_975["README.md"]
        node_974["build_cached_image.yaml"]
        node_972["build_pipecatapp_image.yaml"]
        node_970["create_expert_job.yaml"]
        node_973["deploy_expert_wrapper.yaml"]
        node_971["deploy_model_gpu_provider.yaml"]
    end
    subgraph dir_ansible_templates_shared [ansible/templates/shared]
        direction TB
        node_967["load_image_task.nomad.j2"]
    end
    subgraph dir_ansible_tests [ansible/tests]
        direction TB
        node_1364["verify_grafana.yaml"]
        node_1365["verify_playbook_syntax.yaml"]
    end
    subgraph dir_assets [assets]
        direction TB
        node_744["llama_icon.png"]
    end
    subgraph dir_cluster_cache [cluster_cache]
        direction TB
        node_37["README.md"]
        node_35["app.py"]
        node_36["requirements.txt"]
    end
    subgraph dir_command_deck_backend [command_deck/backend]
        direction TB
        node_695["app.py"]
    end
    subgraph dir_command_deck_frontend [command_deck/frontend]
        direction TB
        node_697["index.html"]
        node_696["script.js"]
        node_698["style.css"]
    end
    subgraph dir_docker [docker]
        direction TB
        node_486["README.md"]
    end
    subgraph dir_docker_dev_container [docker/dev_container]
        direction TB
        node_488["Dockerfile"]
    end
    subgraph dir_docker_memory_service [docker/memory_service]
        direction TB
        node_487["Dockerfile"]
    end
    subgraph dir_docs [docs]
        direction TB
        node_489["DEAD_CODE_REVIEW.md"]
        node_490["README.md"]
    end
    subgraph dir_docs_analysis [docs/analysis]
        direction TB
        node_501["AGENT_LIGHTNING_ANALYSIS.md"]
        node_495["BENCHMARKING.MD"]
        node_491["CEPH_EVALUATION.md"]
        node_508["CLAMAV_EVALUATION.md"]
        node_512["CLAUDE_CODE_ANALYSIS.md"]
        node_492["DIRAC_EVALUATION.md"]
        node_514["EVALUATION_LLMROUTER.md"]
        node_493["FLOWISE_ANALYSIS.md"]
        node_494["GCP_GENERATIVE_AI_REVIEW.md"]
        node_496["GNUTELLA_ANALYSIS.md"]
        node_506["HAYSTACK_ANALYSIS.md"]
        node_505["HELIXDB_EVALUATION.md"]
        node_499["IPV6_AUDIT.md"]
        node_502["LANGCHAIN_ANALYSIS.md"]
        node_507["LITEGRAPH_VS_REACTFLOW.md"]
        node_515["MEMENTO_SKILLS_ANALYSIS.md"]
        node_510["PASEO_ANALYSIS.md"]
        node_498["POLLEN_COMPARISON.md"]
        node_511["REFACTOR_PROPOSAL_hybrid_architecture.md"]
        node_500["SECURITY_AUDIT.md"]
        node_513["TOOL_EVALUATION.md"]
        node_504["VLLM_PROJECT_EVALUATION.md"]
        node_497["YAML_FILES_REPORT.md"]
        node_509["aid_e_log.txt"]
        node_503["heretic_evaluation.md"]
        node_516["review_report.md"]
    end
    subgraph dir_docs_manual [docs/manual]
        direction TB
        node_533["AGENTS.md"]
        node_521["AI_GOVERNANCE.md"]
        node_543["ARCHITECTURE.md"]
        node_529["DEPLOYMENT_AND_PROFILING.md"]
        node_537["DIRAC_TODO.md"]
        node_523["FRONTEND_VERIFICATION.md"]
        node_539["FRONTIER_AGENT_ROADMAP.md"]
        node_531["GASTOWN_TODO.md"]
        node_519["GEMINI.md"]
        node_524["LOAD_TESTING.md"]
        node_526["MCP_MIGRATION_PLAN.md"]
        node_535["MCP_SERVER_SETUP.md"]
        node_541["MEMORIES.md"]
        node_542["NETWORK.md"]
        node_532["NETWORK_ISOLATION.md"]
        node_525["NIXOS_PXE_BOOT_SETUP.md"]
        node_517["OBSIDIAN_TODO.md"]
        node_530["OBSIDIAN_WORKFLOW_DESIGN.md"]
        node_538["PERFORMANCE_OPTIMIZATION.md"]
        node_528["PROJECT_SUMMARY.md"]
        node_534["PXE_BOOT_SETUP.md"]
        node_518["REMOTE_WORKFLOW.md"]
        node_522["SCALING_TODO.md"]
        node_536["SPIRE_POC.md"]
        node_520["TODO_Hybrid_Architecture.md"]
        node_540["TROUBLESHOOTING.md"]
        node_527["TWINSERVICE_DEMONOLITHIZATION_DESIGN.md"]
    end
    subgraph dir_docs_media [docs/media]
        direction TB
        node_544["initial_state.png"]
        node_545["paused_state.png"]
    end
    subgraph dir_evaluations [evaluations]
        direction TB
        node_693["ds4_evaluation.md"]
        node_691["dspark_speculative_decoding_report.md"]
        node_694["longcat_2.0_evaluation.md"]
        node_692["ornith-1-evaluation.md"]
    end
    subgraph dir_examples [examples]
        direction TB
        node_48["README.md"]
        node_47["chat-persistent.sh"]
    end
    subgraph dir_group_vars [group_vars]
        direction TB
        node_177["README.md"]
        node_178["all.yaml"]
        node_176["external_experts.yaml"]
        node_175["models.yaml"]
    end
    subgraph dir_host_vars [host_vars]
        direction TB
        node_737["README.md"]
        node_736["localhost.yaml"]
    end
    subgraph dir_initial_setup [initial-setup]
        direction TB
        node_954["README.md"]
        node_953["add_new_worker.sh"]
        node_952["setup.conf"]
        node_951["setup.sh"]
        node_950["update_inventory.sh"]
    end
    subgraph dir_initial_setup_modules [initial-setup/modules]
        direction TB
        node_959["01-network.sh"]
        node_955["02-hostname.sh"]
        node_956["03-user.sh"]
        node_958["04-ssh.sh"]
        node_957["05-auto-provision.sh"]
        node_960["README.md"]
    end
    subgraph dir_initial_setup_worker_setup [initial-setup/worker-setup]
        direction TB
        node_962["README.md"]
        node_961["setup.sh"]
    end
    subgraph dir_modules_keystone_polyphony [modules/keystone-polyphony]
        direction TB
        node_60[".flake8"]
        node_49[".gitignore"]
        node_64["AGENTS.md"]
        node_61["CODE_OF_CONDUCT.md"]
        node_56["CONTRIBUTING.md"]
        node_52["Dockerfile"]
        node_59["ENSEMBLE_TRIAL.md"]
        node_51["LICENSE"]
        node_68["README.md"]
        node_50["TODO.md"]
        node_63["WORK_ORDER.md"]
        node_65["docker-compose.yml"]
        node_62["install.sh"]
        node_66["jules_config.json"]
        node_54["keystone-polyphony.sh"]
        node_67["kp"]
        node_58["polyphony"]
        node_57["requirements.txt"]
        node_53["simulate_swarm.py"]
        node_55["simulation.log"]
    end
    subgraph dir_modules_keystone_polyphony__agents_workflows [modules/keystone-polyphony/.agents/workflows]
        direction TB
        node_141["0-click-boot.md"]
        node_139["boot.md"]
        node_140["swarm-communication.md"]
    end
    subgraph dir_modules_keystone_polyphony__devcontainer [modules/keystone-polyphony/.devcontainer]
        direction TB
        node_142["devcontainer.json"]
    end
    subgraph dir_modules_keystone_polyphony__githooks [modules/keystone-polyphony/.githooks]
        direction TB
        node_115["pre-commit"]
        node_114["pre-push"]
    end
    subgraph dir_modules_keystone_polyphony__github [modules/keystone-polyphony/.github]
        direction TB
        node_144["reviewers.yml"]
    end
    subgraph dir_modules_keystone_polyphony__github_workflows [modules/keystone-polyphony/.github/workflows]
        direction TB
        node_150["add-contributors.yml"]
        node_146["agent-issue-solver.yml"]
        node_154["agent-issue-triage.yml"]
        node_153["agent-parallel-solver.yml"]
        node_149["auto-merge-staging.yml"]
        node_155["daily-close-merged-issues.yml"]
        node_145["opencode.yml"]
        node_152["periodic-merge-main.yml"]
        node_151["swarm-node.yml"]
        node_147["workflow-review-dispatch.yml"]
        node_148["workflow-review.yml"]
    end
    subgraph dir_modules_keystone_polyphony_docs [modules/keystone-polyphony/docs]
        direction TB
        node_106["architecture.md"]
        node_102["ci-cd.md"]
        node_104["getting-started.md"]
        node_103["git-hooks-architecture.md"]
        node_101["hooks-interaction.md"]
        node_105["liminal-bridge.md"]
        node_107["swarm-coordination.md"]
        node_100["vscode-integration.md"]
        node_99["zed-integration.md"]
    end
    subgraph dir_modules_keystone_polyphony_docs_features [modules/keystone-polyphony/docs/features]
        direction TB
        node_113["git-hooks.feature"]
    end
    subgraph dir_modules_keystone_polyphony_docs_issues_pre_review [modules/keystone-polyphony/docs/issues-pre-review]
        direction TB
        node_112["vision-and-impact.md"]
    end
    subgraph dir_modules_keystone_polyphony_docs_swarm_discovery [modules/keystone-polyphony/docs/swarm-discovery]
        direction TB
        node_110["analysis.md"]
        node_109["architecture-diagram.md"]
        node_108["hardware-bom.md"]
        node_111["modality-matrix.md"]
    end
    subgraph dir_modules_keystone_polyphony_features [modules/keystone-polyphony/features]
        direction TB
        node_156["hooks.feature"]
    end
    subgraph dir_modules_keystone_polyphony_meta [modules/keystone-polyphony/meta]
        direction TB
        node_143["DISCOVERIES.md"]
    end
    subgraph dir_modules_keystone_polyphony_scripts [modules/keystone-polyphony/scripts]
        direction TB
        node_134["agent-boot.sh"]
        node_116["broadcast.py"]
        node_128["deduplicate.py"]
        node_118["dispatch-work-order.sh"]
        node_132["exchange_ssh_keys.py"]
        node_123["inject-secrets.sh"]
        node_120["install-hooks.sh"]
        node_138["lint.sh"]
        node_137["load_test.py"]
        node_135["package.json"]
        node_117["ping.py"]
        node_129["refine_issue.py"]
        node_133["run-tests.sh"]
        node_122["setup-ensemble.sh"]
        node_127["setup-swarm.js"]
        node_130["setup-vscode.sh"]
        node_124["setup-zed.sh"]
        node_126["share.py"]
        node_131["status.py"]
        node_119["swarm_status.py"]
        node_125["triage-dispatch.sh"]
        node_136["triage-lib.sh"]
        node_121["worker_loop.py"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge [modules/keystone-polyphony/src/liminal_bridge]
        direction TB
        node_75["__init__.py"]
        node_73["architect.py"]
        node_70["crdt.py"]
        node_79["dashboard.py"]
        node_69["mesh.py"]
        node_71["observability.py"]
        node_74["pulse.py"]
        node_72["server.py"]
        node_78["test_architect.py"]
        node_76["test_key_rotation.py"]
        node_77["test_mesh.py"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_dashboard_ui [modules/keystone-polyphony/src/liminal_bridge/dashboard_ui]
        direction TB
        node_81["index.html"]
        node_82["package.json"]
        node_80["vite.config.js"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_dashboard_ui_src [modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src]
        direction TB
        node_83["App.css"]
        node_85["App.jsx"]
        node_87["crypto.js"]
        node_84["index.css"]
        node_86["main.jsx"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_dashboard_ui_src_components [modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components]
        direction TB
        node_91["Backlog.jsx"]
        node_90["Batons.jsx"]
        node_96["Discussions.jsx"]
        node_93["KVStore.jsx"]
        node_89["Login.jsx"]
        node_88["Logs.jsx"]
        node_95["NetworkGraph.jsx"]
        node_94["Status.jsx"]
        node_92["Thoughts.jsx"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_sidecar [modules/keystone-polyphony/src/liminal_bridge/sidecar]
        direction TB
        node_97["bridge.js"]
        node_98["package.json"]
    end
    subgraph dir_modules_keystone_polyphony_tests [modules/keystone-polyphony/tests]
        direction TB
        node_161["issue_19_verification.txt"]
        node_162["test_activation.sh"]
        node_170["test_architect_commands.py"]
        node_169["test_architect_ollama.py"]
        node_160["test_attenuation.py"]
        node_167["test_crdt.py"]
        node_166["test_ensemble_chat.py"]
        node_171["test_fallback.py"]
        node_163["test_install.sh"]
        node_165["test_mesh_crdt.py"]
        node_159["test_mesh_encryption.py"]
        node_168["test_network_simulation.py"]
        node_164["test_ssh_exchange.py"]
        node_174["test_stigmergy.py"]
        node_158["test_tandem.py"]
        node_172["test_tasks.py"]
        node_157["test_unread_tracking.py"]
        node_173["test_vector_clock.py"]
    end
    subgraph dir_os_image [os-image]
        direction TB
        node_746["README.md"]
        node_745["build_iso.sh"]
    end
    subgraph dir_os_image_config_archives [os-image/config/archives]
        direction TB
        node_762["rocm.key.binary"]
        node_761["rocm.key.chroot"]
        node_763["rocm.list.binary"]
        node_760["rocm.list.chroot"]
    end
    subgraph dir_os_image_config_hooks_live [os-image/config/hooks/live]
        direction TB
        node_748["01-setup-users.chroot"]
        node_749["02-enable-services.chroot"]
        node_747["03-setup-command-deck.chroot"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_profile_d [os-image/config/includes.chroot/etc/profile.d]
        direction TB
        node_751["99-pipecat-welcome.sh"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_sddm_conf_d [os-image/config/includes.chroot/etc/sddm.conf.d]
        direction TB
        node_755["autologin.conf"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_systemd_system [os-image/config/includes.chroot/etc/systemd/system]
        direction TB
        node_753["pipecat-firstboot.service"]
        node_752["pipecat-hostname.service"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_systemd_system_multi_user_target_wants [os-image/config/includes.chroot/etc/systemd/system/multi-user.target.wants]
        direction TB
        node_754["pipecat-firstboot.service"]
    end
    subgraph dir_os_image_config_includes_chroot_usr_local_bin [os-image/config/includes.chroot/usr/local/bin]
        direction TB
        node_757["command-deck-session"]
        node_756["setup-ssh-keys.sh"]
    end
    subgraph dir_os_image_config_includes_chroot_usr_share_wayland_sessions [os-image/config/includes.chroot/usr/share/wayland-sessions]
        direction TB
        node_758["command-deck.desktop"]
    end
    subgraph dir_os_image_config_includes_installer [os-image/config/includes.installer]
        direction TB
        node_759["preseed.cfg"]
    end
    subgraph dir_os_image_config_package_lists [os-image/config/package-lists]
        direction TB
        node_750["pipecat.list.chroot"]
    end
    subgraph dir_pipecat_agent_extension [pipecat-agent-extension]
        direction TB
        node_948["README.md"]
        node_945["example.ts"]
        node_944["gemini-extension.json"]
        node_947["package.json"]
        node_946["tsconfig.json"]
    end
    subgraph dir_pipecat_agent_extension_commands_pipecat [pipecat-agent-extension/commands/pipecat]
        direction TB
        node_949["send.toml"]
    end
    subgraph dir_pipecatapp [pipecatapp]
        direction TB
        node_191["Dockerfile"]
        node_229["README.md"]
        node_188["TODO.md"]
        node_202["__init__.py"]
        node_205["agent_factory.py"]
        node_219["api_keys.py"]
        node_187["app.py"]
        node_196["archivist_service.py"]
        node_190["durable_execution.py"]
        node_208["expert_tracker.py"]
        node_207["file_ingestion.py"]
        node_225["generate_real_embeddings.py"]
        node_204["gossip_discovery.py"]
        node_223["janitor_agent.py"]
        node_185["judge_agent.py"]
        node_206["langchain_memory_wrappers.py"]
        node_198["llm_clients.py"]
        node_182["local_llm.py"]
        node_222["local_world_model.py"]
        node_180["manager_agent.py"]
        node_183["memory.py"]
        node_184["memory_backends.py"]
        node_220["memory_legacy.py"]
        node_217["models.py"]
        node_211["moondream_detector.py"]
        node_186["mqtt_world_model_client.py"]
        node_215["mtac_pipeline.py"]
        node_193["net_utils.py"]
        node_200["network_scanner.py"]
        node_199["ontology.py"]
        node_221["pmm_memory.py"]
        node_213["pmm_memory_client.py"]
        node_194["quality_control.py"]
        node_201["rate_limiter.py"]
        node_203["requirements.txt"]
        node_231["router_config.yaml"]
        node_216["router_train_embeddings.pt"]
        node_224["router_trained_model.pkl"]
        node_214["router_training_data.csv"]
        node_226["router_training_data.jsonl"]
        node_212["secret_manager.py"]
        node_210["security.py"]
        node_181["skill_library.py"]
        node_192["start_archivist.sh"]
        node_227["task_supervisor.py"]
        node_189["technician_agent.py"]
        node_218["test_moondream_detector.py"]
        node_230["test_pmm_memory.py"]
        node_195["test_server.py"]
        node_179["tool_server.py"]
        node_228["train_router.py"]
        node_209["web_server.py"]
        node_197["worker_agent.py"]
    end
    subgraph dir_pipecatapp_datasets [pipecatapp/datasets]
        direction TB
        node_324["sycophancy_prompts.json"]
    end
    subgraph dir_pipecatapp_integrations [pipecatapp/integrations]
        direction TB
        node_255["__init__.py"]
        node_256["openclaw.py"]
    end
    subgraph dir_pipecatapp_memory_backends_impl [pipecatapp/memory_backends_impl]
        direction TB
        node_483["__init__.py"]
        node_485["crdt_backend.py"]
        node_482["helix_backend.py"]
        node_484["helix_client.py"]
    end
    subgraph dir_pipecatapp_memory_graph_service [pipecatapp/memory_graph_service]
        direction TB
        node_232["Dockerfile"]
        node_234["helix_server.py"]
        node_233["server.py"]
    end
    subgraph dir_pipecatapp_mtac [pipecatapp/mtac]
        direction TB
        node_340["eval_sft.py"]
        node_342["torchtune_sft.py"]
        node_341["unsloth_sft.py"]
    end
    subgraph dir_pipecatapp_nomad_templates [pipecatapp/nomad_templates]
        direction TB
        node_288["immich.nomad.hcl"]
        node_286["readeck.nomad.hcl"]
        node_287["uptime-kuma.nomad.hcl"]
        node_289["vaultwarden.nomad.hcl"]
    end
    subgraph dir_pipecatapp_prompts [pipecatapp/prompts]
        direction TB
        node_317["coding_expert.txt"]
        node_323["consolidation_expert.txt"]
        node_321["creative_expert.txt"]
        node_319["ingestion_expert.txt"]
        node_322["memory_query_expert.txt"]
        node_320["router.txt"]
        node_318["tron_agent.txt"]
    end
    subgraph dir_pipecatapp_resources_skills [pipecatapp/resources/skills]
        direction TB
        node_450["backpass.md"]
        node_451["renovate.md"]
        node_449["scaffold-setup-skill.md"]
    end
    subgraph dir_pipecatapp_servers [pipecatapp/servers]
        direction TB
        node_316["shell_server.py"]
    end
    subgraph dir_pipecatapp_services [pipecatapp/services]
        direction TB
        node_236["__init__.py"]
        node_237["gemma_e2b_service.py"]
        node_235["obsidian_gardener.py"]
    end
    subgraph dir_pipecatapp_services_code_runner [pipecatapp/services/code_runner]
        direction TB
        node_253["Dockerfile"]
        node_254["code_runner_server.py"]
    end
    subgraph dir_pipecatapp_services_ipfs_apt_proxy [pipecatapp/services/ipfs_apt_proxy]
        direction TB
        node_249["Dockerfile"]
        node_248["main.py"]
        node_250["requirements.txt"]
    end
    subgraph dir_pipecatapp_services_ipfs_pypi_proxy [pipecatapp/services/ipfs_pypi_proxy]
        direction TB
        node_246["Dockerfile"]
        node_245["main.py"]
        node_247["requirements.txt"]
    end
    subgraph dir_pipecatapp_services_push_proxy [pipecatapp/services/push_proxy]
        direction TB
        node_244["README.md"]
        node_242["__init__.py"]
        node_243["client.py"]
        node_241["server.py"]
    end
    subgraph dir_pipecatapp_services_rag [pipecatapp/services/rag]
        direction TB
        node_251["Dockerfile"]
        node_252["rag_server.py"]
    end
    subgraph dir_pipecatapp_services_ternlight [pipecatapp/services/ternlight]
        direction TB
        node_238["Dockerfile"]
        node_240["package.json"]
        node_239["ternlight_server.js"]
    end
    subgraph dir_pipecatapp_static [pipecatapp/static]
        direction TB
        node_306["cluster.html"]
        node_302["cluster_viz.html"]
        node_307["index.html"]
        node_304["monitor.html"]
        node_308["terminal.js"]
        node_305["vr_index.html"]
        node_301["workflow.html"]
        node_303["workflow_3d.html"]
    end
    subgraph dir_pipecatapp_static_css [pipecatapp/static/css]
        direction TB
        node_309["litegraph.css"]
        node_310["styles.css"]
    end
    subgraph dir_pipecatapp_static_js [pipecatapp/static/js]
        direction TB
        node_312["dagre.min.js"]
        node_313["editor.js"]
        node_311["litegraph.js"]
        node_315["ternlight_client.js"]
        node_314["workflow.js"]
    end
    subgraph dir_pipecatapp_tests [pipecatapp/tests]
        direction TB
        node_455["test_audio_streamer.py"]
        node_470["test_browser_tool_security.py"]
        node_477["test_container_registry_tool.py"]
        node_473["test_cq_tool.py"]
        node_467["test_document_tool.py"]
        node_471["test_gemma_e2b_service.py"]
        node_479["test_git_tool_security.py"]
        node_460["test_llm_clients.py"]
        node_454["test_llm_clients_new.py"]
        node_478["test_metrics_cache.py"]
        node_464["test_net_utils.py"]
        node_461["test_new_skills.py"]
        node_453["test_openclaw.py"]
        node_468["test_ouroboros.py"]
        node_458["test_piper_async.py"]
        node_452["test_proxy_security.py"]
        node_472["test_rag_pruning.py"]
        node_456["test_rag_tool.py"]
        node_463["test_rate_limiter.py"]
        node_469["test_security.py"]
        node_457["test_stt_optimization.py"]
        node_466["test_technician_agent.py"]
        node_462["test_tool_server.py"]
        node_474["test_uilogger_redaction.py"]
        node_475["test_web_server_unit.py"]
        node_476["test_websocket_security.py"]
        node_459["test_xss_prevention.py"]
        node_465["test_yolo_optimization.py"]
    end
    subgraph dir_pipecatapp_tests_workflow [pipecatapp/tests/workflow]
        direction TB
        node_481["test_history.py"]
        node_480["test_serialization_perf.py"]
    end
    subgraph dir_pipecatapp_tools [pipecatapp/tools]
        direction TB
        node_373["__init__.py"]
        node_406["ansible_tool.py"]
        node_414["archivist_tool.py"]
        node_408["ast_editor_tool.py"]
        node_361["atproto_tool.py"]
        node_401["autoloop_tool.py"]
        node_368["autoresearch_tool.py"]
        node_356["claude_clone_tool.py"]
        node_355["cluster_status_tool.py"]
        node_419["code_runner_tool.py"]
        node_383["container_registry_tool.py"]
        node_349["context_upload_tool.py"]
        node_402["council_tool.py"]
        node_360["cq_tool.py"]
        node_366["dependency_scanner_tool.py"]
        node_399["desktop_control_tool.py"]
        node_381["document_tool.py"]
        node_421["dynamic_skill_tool.py"]
        node_374["execution_history.py"]
        node_395["experiment_tool.py"]
        node_398["file_editor_tool.py"]
        node_344["final_answer_tool.py"]
        node_390["gemini_cli.py"]
        node_388["get_nomad_job.py"]
        node_405["git_tool.py"]
        node_363["ha_tool.py"]
        node_345["heretic_tool.py"]
        node_382["jules_tool.py"]
        node_348["langchain_adapter.py"]
        node_409["langchain_adapter_tool.py"]
        node_403["lightweight_project_mapper_tool.py"]
        node_396["llxprt_code_tool.py"]
        node_359["mcp_client_adapter.py"]
        node_346["mcp_tool.py"]
        node_378["mtac_tool.py"]
        node_371["ocr_tool.py"]
        node_418["open_workers_tool.py"]
        node_372["openclaw_tool.py"]
        node_343["opencode_provider_tool.py"]
        node_375["opencode_tool.py"]
        node_365["orchestrator_tool.py"]
        node_407["ouroboros_tool.py"]
        node_347["p2p_sync_tool.py"]
        node_354["personality_tool.py"]
        node_422["planner_tool.py"]
        node_384["polyphony_tool.py"]
        node_369["power_tool.py"]
        node_352["project_mapper_tool.py"]
        node_416["project_overview_tool.py"]
        node_420["prompt_improver_tool.py"]
        node_410["rag_tool.py"]
        node_351["remote_code_runner_tool.py"]
        node_358["remote_rag_tool.py"]
        node_350["remote_tool_proxy.py"]
        node_377["retry_utils.py"]
        node_415["sandbox.ts"]
        node_417["save_skill_tool.py"]
        node_385["scale_compute_tool.py"]
        node_370["scheduler_tool.py"]
        node_392["search_skills_tool.py"]
        node_389["search_tool.py"]
        node_379["set_operational_mode_tool.py"]
        node_387["shell_tool.py"]
        node_380["skill_builder_tool.py"]
        node_367["smol_agent_tool.py"]
        node_412["spec_loader_tool.py"]
        node_357["ssh_tool.py"]
        node_413["submit_solution_tool.py"]
        node_404["summarizer_tool.py"]
        node_391["swarm_tool.py"]
        node_394["tap_service.py"]
        node_397["term_everything_tool.py"]
        node_386["ternlight_tool.py"]
        node_362["test_git_tool.py"]
        node_393["test_ssh_tool.py"]
        node_364["update_litellm_tool.py"]
        node_411["vr_tool.py"]
        node_353["wasm_tool.py"]
        node_400["web_browser_tool.py"]
        node_376["wol_tool.py"]
    end
    subgraph dir_pipecatapp_tools_repo_map_impl [pipecatapp/tools/repo_map_impl]
        direction TB
        node_427["__init__.py"]
        node_426["cache.py"]
        node_429["cli.py"]
        node_428["config.py"]
        node_430["discover.py"]
        node_431["languages.py"]
        node_425["model.py"]
        node_423["pipeline.py"]
        node_424["rank.py"]
    end
    subgraph dir_pipecatapp_tools_repo_map_impl_extract [pipecatapp/tools/repo_map_impl/extract]
        direction TB
        node_441["__init__.py"]
        node_440["python_ast.py"]
        node_442["tree_sitter.py"]
    end
    subgraph dir_pipecatapp_tools_repo_map_impl_queries [pipecatapp/tools/repo_map_impl/queries]
        direction TB
        node_434["ATTRIBUTION.md"]
        node_438["go-tags.scm"]
        node_439["javascript-tags.scm"]
        node_436["python-tags.scm"]
        node_432["rust-tags.scm"]
        node_435["swift-tags.scm"]
        node_433["tsx-tags.scm"]
        node_437["typescript-tags.scm"]
    end
    subgraph dir_pipecatapp_tools_repo_map_impl_render [pipecatapp/tools/repo_map_impl/render]
        direction TB
        node_444["__init__.py"]
        node_445["catalog.py"]
        node_448["file_index.py"]
        node_443["json_out.py"]
        node_447["navigation.py"]
        node_446["tree.py"]
    end
    subgraph dir_pipecatapp_ui_opengravity [pipecatapp/ui/opengravity]
        direction TB
        node_329["CONTRIBUTING.md"]
        node_326["LICENSE"]
        node_334["README.md"]
        node_327["_headers"]
        node_325["agent.js"]
        node_333["iconstyles.css"]
        node_331["index.html"]
        node_330["script.js"]
        node_328["server.py"]
        node_335["seti.woff"]
        node_332["style.css"]
    end
    subgraph dir_pipecatapp_ui_opengravity_assets [pipecatapp/ui/opengravity/assets]
        direction TB
        node_338["html site example.png"]
        node_337["icon.jpeg"]
        node_339["screenshot.png"]
    end
    subgraph dir_pipecatapp_ui_opengravity_webcontainer_connect [pipecatapp/ui/opengravity/webcontainer/connect]
        direction TB
        node_336["index.html"]
    end
    subgraph dir_pipecatapp_utils [pipecatapp/utils]
        direction TB
        node_262["__init__.py"]
        node_258["backon_utils.py"]
        node_260["command_runner.py"]
        node_259["coverage_check.py"]
        node_257["file_utils.py"]
        node_263["ingest_skills.py"]
        node_261["rag_pruner.py"]
        node_264["ssh_utils.py"]
        node_265["terminal_cleanup.py"]
    end
    subgraph dir_pipecatapp_workflow [pipecatapp/workflow]
        direction TB
        node_270["__init__.py"]
        node_268["canvas_converter.py"]
        node_272["context.py"]
        node_269["crypto_receipts.py"]
        node_273["history.py"]
        node_271["node.py"]
        node_266["nodered_converter.py"]
        node_267["runner.py"]
    end
    subgraph dir_pipecatapp_workflow_nodes [pipecatapp/workflow/nodes]
        direction TB
        node_278["__init__.py"]
        node_277["base_nodes.py"]
        node_280["consolidation_nodes.py"]
        node_276["emperor_nodes.py"]
        node_285["langchain_nodes.py"]
        node_282["llm_nodes.py"]
        node_274["rag_nodes.py"]
        node_275["ralph_nodes.py"]
        node_279["registry.py"]
        node_283["system_nodes.py"]
        node_284["tasky_nodes.py"]
        node_281["tool_nodes.py"]
    end
    subgraph dir_pipecatapp_workflows [pipecatapp/workflows]
        direction TB
        node_293["adversarial_simulation.yaml"]
        node_292["deep_context.yaml"]
        node_290["default_agent_loop.yaml"]
        node_295["dft_workflow.yaml"]
        node_300["document_ingestion.yaml"]
        node_291["looped_reasoning.yaml"]
        node_297["manager.yaml"]
        node_298["poc_ensemble.yaml"]
        node_296["sandbox.yaml"]
        node_294["tiered_agent_loop.yaml"]
        node_299["update_litellm_workflow.yaml"]
    end
    subgraph dir_playbooks [playbooks]
        direction TB
        node_650["README.md"]
        node_636["app_jobs.yaml"]
        node_630["benchmark_single_model.yaml"]
        node_634["cluster_status.yaml"]
        node_643["common_setup.yaml"]
        node_631["controller.yaml"]
        node_624["debug_template.yaml"]
        node_629["deploy_app.yaml"]
        node_641["deploy_expert.yaml"]
        node_646["deploy_openclaw.yaml"]
        node_635["deploy_pds.yaml"]
        node_637["deploy_prompt_evolution.yaml"]
        node_627["developer_tools.yaml"]
        node_638["diagnose_failure.yaml"]
        node_633["fix_cluster.yaml"]
        node_632["heal_cluster.yaml"]
        node_649["heal_job.yaml"]
        node_628["health_check.yaml"]
        node_642["promote_controller.yaml"]
        node_651["promote_to_controller.yaml"]
        node_626["pxe_setup.yaml"]
        node_647["redeploy_pipecat.yaml"]
        node_648["run_config_manager.yaml"]
        node_625["run_consul.yaml"]
        node_645["run_health_check.yaml"]
        node_644["status-check.yaml"]
        node_640["wake.yaml"]
        node_639["worker.yaml"]
    end
    subgraph dir_playbooks_network [playbooks/network]
        direction TB
        node_672["mesh.yaml"]
        node_673["verify.yaml"]
    end
    subgraph dir_playbooks_ops [playbooks/ops]
        direction TB
        node_671["optimize_memory.yaml"]
    end
    subgraph dir_playbooks_preflight [playbooks/preflight]
        direction TB
        node_674["checks.yaml"]
    end
    subgraph dir_playbooks_services [playbooks/services]
        direction TB
        node_667["README.md"]
        node_662["ai_experts.yaml"]
        node_666["app_services.yaml"]
        node_664["apt_proxy.yaml"]
        node_659["consul.yaml"]
        node_665["core_ai_services.yaml"]
        node_663["core_infra.yaml"]
        node_657["distributed_compute.yaml"]
        node_668["docker.yaml"]
        node_656["final_verification.yaml"]
        node_655["ipfs.yaml"]
        node_669["model_services.yaml"]
        node_658["monitoring.yaml"]
        node_652["nomad.yaml"]
        node_661["nomad_client.yaml"]
        node_660["pypi_proxy.yaml"]
        node_654["seed_models_to_ipfs.yaml"]
        node_653["streaming_services.yaml"]
        node_670["training_services.yaml"]
    end
    subgraph dir_poc_crdt_memory [poc/crdt_memory]
        direction TB
        node_617["README.md"]
        node_616["run_poc.py"]
    end
    subgraph dir_poc_p2p_sync [poc/p2p_sync]
        direction TB
        node_614["README.md"]
        node_613["run_poc.py"]
        node_615["syncthing_manager.py"]
    end
    subgraph dir_poc_wasm_tool_bridge [poc/wasm_tool_bridge]
        direction TB
        node_620["README.md"]
        node_618["host.py"]
        node_619["python_tool.py"]
    end
    subgraph dir_poc_wasm_tool_bridge_text_processor [poc/wasm_tool_bridge/text_processor]
        direction TB
        node_621["Cargo.lock"]
        node_622["Cargo.toml"]
    end
    subgraph dir_poc_wasm_tool_bridge_text_processor_src [poc/wasm_tool_bridge/text_processor/src]
        direction TB
        node_623["lib.rs"]
    end
    subgraph dir_prompt_engineering [prompt_engineering]
        direction TB
        node_699["PROMPT_ENGINEERING.md"]
        node_711["README.md"]
        node_705["archive_server.py"]
        node_710["autoloop_evolve.py"]
        node_701["challenger.py"]
        node_709["create_evaluator.py"]
        node_703["evaluation_lib.py"]
        node_712["evaluator.py"]
        node_704["evolve.py"]
        node_708["promote_agent.py"]
        node_702["requirements-dev.txt"]
        node_700["run_campaign.py"]
        node_706["self_harness.py"]
        node_707["visualize_archive.py"]
    end
    subgraph dir_prompt_engineering_agents [prompt_engineering/agents]
        direction TB
        node_718["ADAPTATION_AGENT.md"]
        node_719["EVALUATOR_GENERATOR.md"]
        node_720["README.md"]
        node_715["architecture_review.md"]
        node_713["code_clean_up.md"]
        node_716["debug_and_analysis.md"]
        node_717["new_task_review.md"]
        node_714["problem_scope_framing.md"]
    end
    subgraph dir_prompt_engineering_archive [prompt_engineering/archive]
        direction TB
        node_721["agent_0.json"]
        node_723["agent_0.py"]
        node_725["agent_1.json"]
        node_726["agent_1.py"]
        node_727["agent_2.json"]
        node_722["agent_2.py"]
        node_724["agent_3.json"]
        node_728["agent_3.py"]
    end
    subgraph dir_prompt_engineering_evaluation_suite [prompt_engineering/evaluation_suite]
        direction TB
        node_730["README.md"]
        node_729["test_vision.yaml"]
    end
    subgraph dir_prompt_engineering_frontend [prompt_engineering/frontend]
        direction TB
        node_732["app.js"]
        node_733["index.html"]
        node_731["server.py"]
        node_734["style.css"]
    end
    subgraph dir_prompt_engineering_generated_evaluators [prompt_engineering/generated_evaluators]
        direction TB
        node_735[".gitignore"]
    end
    subgraph dir_prompts [prompts]
        direction TB
        node_681["README.md"]
        node_679["chat-with-bob.txt"]
        node_680["router.txt"]
    end
    subgraph dir_reflection [reflection]
        direction TB
        node_677["README.md"]
        node_676["adaptation_manager.py"]
        node_678["create_reflection.py"]
        node_675["reflect.py"]
    end
    subgraph dir_scenarios [scenarios]
        direction TB
        node_39["adr_template.md"]
        node_43["agent_behavior_template.md"]
        node_38["api_calls_template.md"]
        node_42["error_handling_template.md"]
        node_44["evaluation_scenario_template.md"]
        node_41["scheduled_task_code_quality.md"]
        node_40["ui_ux_design_template.md"]
        node_45["validation_format_template.md"]
        node_46["workflow_node_template.md"]
    end
    subgraph dir_scripts [scripts]
        direction TB
        node_595["README.md"]
        node_581["agent_fast_check.sh"]
        node_602["agent_preflight.sh"]
        node_575["agentic_workflow.sh"]
        node_582["analyze_nomad_allocs.py"]
        node_591["ansible_diff.sh"]
        node_580["benchmark_resources.py"]
        node_601["check_all_playbooks.sh"]
        node_554["check_deps.py"]
        node_570["ci_ansible_check.sh"]
        node_598["cleanup.sh"]
        node_576["compare_exo_llama.py"]
        node_548["create_assistant_prompts.py"]
        node_558["create_cynic_model.sh"]
        node_559["create_todo_issues.sh"]
        node_594["dance_loading.py"]
        node_587["debug_expert.sh"]
        node_552["debug_mesh.sh"]
        node_592["enroll-admin.sh"]
        node_574["evaluate_clamav.py"]
        node_556["fix_markdown.sh"]
        node_603["fix_verification_failures.sh"]
        node_568["fix_yaml.sh"]
        node_596["generate_assistant_vectors.sh"]
        node_599["generate_file_map.py"]
        node_578["generate_issue_script.py"]
        node_560["generate_signatures.py"]
        node_590["generate_tailscale_key.sh"]
        node_597["git-cleanup.sh"]
        node_549["heal_cluster.sh"]
        node_588["healer.py"]
        node_600["lint.sh"]
        node_593["lint_exclude.txt"]
        node_604["memory_audit.py"]
        node_557["nomad_checkpoint.sh"]
        node_586["profile_resources.sh"]
        node_563["provisioning.py"]
        node_589["prune_consul_services.py"]
        node_550["recover_node.py"]
        node_571["recover_os.py"]
        node_573["run_nomad.sh"]
        node_551["run_quibbler.sh"]
        node_584["run_smol_recovery.py"]
        node_565["run_tests.sh"]
        node_555["salvage_task.py"]
        node_572["setup_pxe_server.sh"]
        node_577["start_services.sh"]
        node_583["sudo_env.py"]
        node_585["supervisor.py"]
        node_564["test_playbooks_dry_run.sh"]
        node_561["test_playbooks_live_run.sh"]
        node_567["test_swarm_map_reduce.py"]
        node_562["troubleshoot.py"]
        node_569["uninstall.sh"]
        node_566["update_cluster.sh"]
        node_579["update_resource_limits.py"]
        node_553["verify_consul_attributes.sh"]
    end
    subgraph dir_scripts_debug [scripts/debug]
        direction TB
        node_606["README.md"]
        node_605["test_mqtt_connection.py"]
    end
    subgraph dir_tests [tests]
        direction TB
        node_784["README.md"]
        node_778["__init__.py"]
        node_780["test.wav"]
        node_779["test_agent_patterns.py"]
        node_771["test_canvas_integration.py"]
        node_774["test_deep_context.py"]
        node_776["test_event_bus.py"]
        node_785["test_experiment_tool.py"]
        node_770["test_gastown_judge.py"]
        node_775["test_gastown_memory.py"]
        node_777["test_gastown_stats.py"]
        node_769["test_imports.py"]
        node_773["test_manager_flow.py"]
        node_781["test_project_overview_tool.py"]
        node_772["test_spec_loader.py"]
        node_768["test_ssrf_validation.py"]
        node_782["test_websocket_security.py"]
        node_767["verify_config_load.py"]
        node_783["verify_dlq.py"]
    end
    subgraph dir_tests_e2e [tests/e2e]
        direction TB
        node_943["README.md"]
        node_938["__init__.py"]
        node_939["test_api.py"]
        node_936["test_intelligent_routing.py"]
        node_937["test_mission_control.py"]
        node_941["test_palette_command_history.py"]
        node_942["test_palette_ux.py"]
        node_940["test_regression.py"]
    end
    subgraph dir_tests_integration [tests/integration]
        direction TB
        node_795["README.md"]
        node_789["__init__.py"]
        node_794["stub_services.py"]
        node_788["test_consul_role.yaml"]
        node_787["test_helixdb_e2e.py"]
        node_790["test_mini_pipeline.py"]
        node_791["test_mqtt_exporter.py"]
        node_786["test_nomad_role.yaml"]
        node_792["test_pipecat_app.py"]
        node_793["test_preemption.py"]
    end
    subgraph dir_tests_playbooks [tests/playbooks]
        direction TB
        node_928["e2e-tests.yaml"]
        node_932["test_authentik.yml"]
        node_933["test_clamav_playbook.yml"]
        node_929["test_consul.yaml"]
        node_935["test_llama_cpp.yaml"]
        node_930["test_nomad.yaml"]
        node_931["test_playbook.yml"]
        node_934["verify_cluster_network.yaml"]
    end
    subgraph dir_tests_scripts [tests/scripts]
        direction TB
        node_926["run_unit_tests.sh"]
        node_925["stress_test_cluster.py"]
        node_924["test_duplicate_role_execution.sh"]
        node_927["test_paddler.sh"]
        node_921["test_piper.sh"]
        node_923["test_run.sh"]
        node_922["verify_components.py"]
    end
    subgraph dir_tests_unit [tests/unit]
        direction TB
        node_911["README.md"]
        node_849["__init__.py"]
        node_837["conftest.py"]
        node_846["test_adaptation_manager.py"]
        node_882["test_agent_definitions.py"]
        node_805["test_ansible_tool.py"]
        node_913["test_app_hybrid.py"]
        node_857["test_archivist_tool.py"]
        node_801["test_ast_editor_tool.py"]
        node_819["test_atproto_tool.py"]
        node_831["test_audio_download_limit.py"]
        node_914["test_autoloop_tool.py"]
        node_848["test_autoresearch_tool.py"]
        node_821["test_autoresearch_tool_pathing.py"]
        node_904["test_backon_integration.py"]
        node_813["test_batch_ast_editor.py"]
        node_862["test_batch_file_editor.py"]
        node_887["test_claude_clone_tool.py"]
        node_879["test_code_runner_security.py"]
        node_860["test_code_runner_timeout.py"]
        node_803["test_code_runner_tool.py"]
        node_866["test_command_deck.py"]
        node_907["test_container_registry_security.py"]
        node_906["test_container_registry_tool.py"]
        node_897["test_context_upload_tool.py"]
        node_916["test_council_tool.py"]
        node_901["test_cq_tool.py"]
        node_796["test_crdt_memory.py"]
        node_820["test_crypto_receipts.py"]
        node_799["test_dependency_scanner.py"]
        node_878["test_dependency_scanner_tool.py"]
        node_836["test_desktop_control_tool.py"]
        node_868["test_document_tool.py"]
        node_816["test_dynamic_skill_tool.py"]
        node_812["test_emperor_node.py"]
        node_865["test_experiment_tool_security.py"]
        node_850["test_expert_tracker.py"]
        node_802["test_file_editor_security.py"]
        node_885["test_file_editor_tool.py"]
        node_894["test_file_ingestion.py"]
        node_867["test_final_answer_tool.py"]
        node_910["test_gemini_cli.py"]
        node_822["test_get_nomad_job.py"]
        node_827["test_git_tool.py"]
        node_918["test_git_tool_security.py"]
        node_798["test_gossip_discovery.py"]
        node_845["test_ha_tool.py"]
        node_876["test_hashline_editor.py"]
        node_903["test_haystack_workflows.py"]
        node_835["test_heretic_tool.py"]
        node_909["test_infrastructure.py"]
        node_881["test_jules_tool.py"]
        node_873["test_langchain_adapter_tool.py"]
        node_834["test_langchain_nodes.py"]
        node_880["test_langchain_wrappers.py"]
        node_851["test_lint_script.py"]
        node_810["test_llxprt_code_tool.py"]
        node_797["test_looped_reasoning_node.py"]
        node_844["test_mcp_tool.py"]
        node_832["test_memory.py"]
        node_838["test_memory_advanced.py"]
        node_858["test_mqtt_template.py"]
        node_806["test_nodered_converter.py"]
        node_814["test_nomad_sandbox.py"]
        node_824["test_obsidian_gardener.py"]
        node_875["test_open_workers_tool.py"]
        node_883["test_openclaw_tool.py"]
        node_825["test_opencode_provider_tool.py"]
        node_808["test_opencode_tool.py"]
        node_829["test_orchestrator_tool.py"]
        node_804["test_p2p_sync_tool.py"]
        node_900["test_personality_tool.py"]
        node_892["test_pipecat_app_unit.py"]
        node_856["test_planner_tool.py"]
        node_871["test_playbook_integration.py"]
        node_854["test_poc_ensemble.py"]
        node_807["test_polyphony_tool.py"]
        node_826["test_post_processor_node.py"]
        node_800["test_power_tool.py"]
        node_861["test_project_mapper_tool.py"]
        node_855["test_prompt_engineering.py"]
        node_895["test_prompt_improver_tool.py"]
        node_919["test_provisioning.py"]
        node_912["test_rag_caching.py"]
        node_809["test_rag_tool.py"]
        node_864["test_ralph_nodes.py"]
        node_899["test_reflection.py"]
        node_847["test_remote_ledgers.py"]
        node_840["test_safe_flatten.py"]
        node_859["test_save_skill_tool.py"]
        node_896["test_scale_compute_tool.py"]
        node_818["test_scheduler_tool.py"]
        node_917["test_search_skills_tool.py"]
        node_843["test_search_tool_security.py"]
        node_886["test_security.py"]
        node_830["test_shell_tool.py"]
        node_811["test_shell_tool_security.py"]
        node_828["test_simple_llm_node.py"]
        node_890["test_skill_builder_tool.py"]
        node_841["test_skill_library.py"]
        node_877["test_smol_agent_tool.py"]
        node_833["test_spec_loader_tool.py"]
        node_874["test_ssh_tool.py"]
        node_853["test_submit_solution_tool.py"]
        node_869["test_summarizer_tool.py"]
        node_842["test_supervisor.py"]
        node_908["test_swarm_tool.py"]
        node_902["test_tap_service.py"]
        node_823["test_tasky_nodes.py"]
        node_889["test_tasky_poc.py"]
        node_905["test_term_everything_tool.py"]
        node_891["test_terminal_cleanup.py"]
        node_839["test_ternlight_tool.py"]
        node_817["test_troubleshoot.py"]
        node_888["test_update_litellm_tool.py"]
        node_852["test_vision_failover.py"]
        node_915["test_vr_tool.py"]
        node_863["test_wasm_tool.py"]
        node_872["test_web_browser_tool.py"]
        node_815["test_web_server_personality.py"]
        node_893["test_web_server_sync.py"]
        node_870["test_wol_tool.py"]
        node_898["test_workflow.py"]
        node_884["test_world_model_service.py"]
    end
    subgraph dir_tests_unit_cluster_cache [tests/unit/cluster_cache]
        direction TB
        node_920["test_cluster_cache.py"]
    end
    subgraph dir_tools_log_vectorizer_mcp [tools/log-vectorizer-mcp]
        direction TB
        node_742["README.md"]
        node_740["generate_db.py"]
        node_741["requirements.txt"]
        node_739["server.py"]
        node_738["test_server.py"]
    end
    subgraph dir_tools_log_vectorizer_mcp_tests [tools/log-vectorizer-mcp/tests]
        direction TB
        node_743["test_server.py"]
    end
    subgraph dir_workflows [workflows]
        direction TB
        node_609["chaining_pattern.yaml"]
        node_611["continuous_consolidation.yaml"]
        node_607["default_agent_loop.yaml"]
        node_608["dream_workflow.yaml"]
        node_612["routing_pattern.yaml"]
        node_610["tasky_checklist_poc.yaml"]
    end

    node_395 --> node_187
    node_62 --> node_57
    node_486 --> node_1354
    node_695 --> node_241
    node_1362 --> node_253
    node_632 --> node_1356
    node_884 --> node_695
    node_0 --> node_1356
    node_233 --> node_739
    node_103 --> node_64
    node_1015 --> node_1167
    node_1314 --> node_1232
    node_1117 --> node_36
    node_541 --> node_556
    node_666 --> node_1083
    node_1339 --> node_1357
    node_449 --> node_250
    node_599 --> node_9
    node_490 --> node_513
    node_162 --> node_58
    node_831 --> node_1148
    node_541 --> node_1225
    node_599 --> node_191
    node_632 --> node_1034
    node_997 --> node_985
    node_1097 --> node_1201
    node_489 --> node_417
    node_25 --> node_58
    node_0 --> node_1034
    node_541 --> node_585
    node_500 --> node_233
    node_556 --> node_29
    node_632 --> node_1192
    node_0 --> node_1192
    node_191 --> node_741
    node_278 --> node_274
    node_1330 --> node_1017
    node_191 --> node_203
    node_205 --> node_1276
    node_559 --> node_705
    node_68 --> node_104
    node_1097 --> node_1141
    node_103 --> node_720
    node_168 --> node_69
    node_100 --> node_1003
    node_3 --> node_178
    node_187 --> node_221
    node_1361 --> node_1144
    node_5 --> node_381
    node_1339 --> node_1020
    node_632 --> node_1340
    node_0 --> node_1340
    node_487 --> node_695
    node_64 --> node_614
    node_449 --> node_251
    node_72 --> node_233
    node_5 --> node_50
    node_731 --> node_81
    node_449 --> node_246
    node_410 --> node_67
    node_282 --> node_217
    node_253 --> node_241
    node_1103 --> node_1144
    node_99 --> node_328
    node_1077 --> node_246
    node_103 --> node_1095
    node_814 --> node_1294
    node_468 --> node_35
    node_1267 --> node_253
    node_1314 --> node_1201
    node_1105 --> node_26
    node_253 --> node_731
    node_632 --> node_1045
    node_0 --> node_1045
    node_1231 --> node_1116
    node_632 --> node_1036
    node_861 --> node_911
    node_497 --> node_1213
    node_1260 --> node_400
    node_0 --> node_1036
    node_5 --> node_517
    node_497 --> node_31
    node_831 --> node_695
    node_658 --> node_1246
    node_106 --> node_533
    node_222 --> node_199
    node_632 --> node_1232
    node_142 --> node_191
    node_489 --> node_248
    node_603 --> node_240
    node_205 --> node_183
    node_935 --> node_1063
    node_1117 --> node_221
    node_1339 --> node_1081
    node_629 --> node_1107
    node_520 --> node_3
    node_541 --> node_307
    node_5 --> node_1046
    node_852 --> node_35
    node_687 --> node_1313
    node_99 --> node_229
    node_627 --> node_1155
    node_20 --> node_334
    node_595 --> node_554
    node_872 --> node_400
    node_1097 --> node_1323
    node_1230 --> node_1211
    node_1339 --> node_1194
    node_751 --> node_620
    node_815 --> node_695
    node_100 --> node_595
    node_575 --> node_490
    node_575 --> node_1337
    node_64 --> node_1213
    node_541 --> node_1219
    node_541 --> node_1226
    node_678 --> node_72
    node_720 --> node_719
    node_64 --> node_31
    node_103 --> node_795
    node_37 --> node_1085
    node_840 --> node_938
    node_1042 --> node_1040
    node_1231 --> node_1123
    node_46 --> node_45
    node_65 --> node_739
    node_1312 --> node_1046
    node_1230 --> node_1006
    node_541 --> node_911
    node_1133 --> node_1130
    node_632 --> node_1201
    node_665 --> node_1331
    node_253 --> node_328
    node_575 --> node_766
    node_934 --> node_1012
    node_1339 --> node_1195
    node_100 --> node_731
    node_302 --> node_309
    node_1312 --> node_1078
    node_840 --> node_778
    node_1097 --> node_1077
    node_681 --> node_679
    node_527 --> node_179
    node_559 --> node_52
    node_1314 --> node_1323
    node_145 --> node_650
    node_12 --> node_653
    node_519 --> node_3
    node_238 --> node_947
    node_1231 --> node_1307
    node_1230 --> node_1174
    node_902 --> node_1281
    node_632 --> node_1141
    node_678 --> node_233
    node_0 --> node_1141
    node_575 --> node_943
    node_489 --> node_209
    node_1230 --> node_1031
    node_151 --> node_58
    node_1180 --> node_1181
    node_515 --> node_183
    node_489 --> node_219
    node_5 --> node_1026
    node_1081 --> node_1302
    node_500 --> node_188
    node_525 --> node_1173
    node_99 --> node_37
    node_1042 --> node_1120
    node_1339 --> node_1239
    node_631 --> node_659
    node_489 --> node_276
    node_672 --> node_1035
    node_145 --> node_969
    node_575 --> node_975
    node_385 --> node_3
    node_1231 --> node_1191
    node_1231 --> node_1030
    node_19 --> node_1286
    node_106 --> node_1138
    node_208 --> node_241
    node_416 --> node_229
    node_711 --> node_709
    node_1102 --> node_36
    node_5 --> node_1197
    node_497 --> node_3
    node_525 --> node_1257
    node_52 --> node_233
    node_62 --> node_1085
    node_19 --> node_222
    node_124 --> node_72
    node_666 --> node_1236
    node_541 --> node_176
    node_1339 --> node_1300
    node_935 --> node_1237
    node_541 --> node_1211
    node_99 --> node_784
    node_1054 --> node_1047
    node_781 --> node_911
    node_719 --> node_1260
    node_773 --> node_1148
    node_103 --> node_1254
    node_154 --> node_57
    node_1045 --> node_1047
    node_497 --> node_659
    node_489 --> node_1276
    node_205 --> node_350
    node_205 --> node_413
    node_520 --> node_177
    node_585 --> node_638
    node_449 --> node_606
    node_187 --> node_1280
    node_234 --> node_739
    node_187 --> node_241
    node_281 --> node_320
    node_31 --> node_667
    node_1231 --> node_1225
    node_100 --> node_328
    node_20 --> node_948
    node_599 --> node_677
    node_742 --> node_250
    node_187 --> node_731
    node_471 --> node_237
    node_1045 --> node_1083
    node_559 --> node_251
    node_1291 --> node_221
    node_632 --> node_1323
    node_0 --> node_1323
    node_56 --> node_947
    node_541 --> node_617
    node_559 --> node_246
    node_1290 --> node_33
    node_205 --> node_1271
    node_541 --> node_1006
    node_588 --> node_583
    node_530 --> node_331
    node_58 --> node_126
    node_1339 --> node_1267
    node_781 --> node_416
    node_1097 --> node_1116
    node_1097 --> node_1344
    node_1133 --> node_1132
    node_238 --> node_135
    node_497 --> node_1194
    node_282 --> node_212
    node_1117 --> node_1302
    node_386 --> node_239
    node_866 --> node_1082
    node_1361 --> node_1303
    node_1008 --> node_1047
    node_772 --> node_490
    node_772 --> node_1337
    node_520 --> node_1301
    node_100 --> node_229
    node_541 --> node_1174
    node_541 --> node_1088
    node_911 --> node_846
    node_31 --> node_326
    node_505 --> node_739
    node_1117 --> node_241
    node_784 --> node_565
    node_423 --> node_426
    node_559 --> node_5
    node_599 --> node_21
    node_541 --> node_1031
    node_5 --> node_874
    node_86 --> node_85
    node_1103 --> node_1303
    node_170 --> node_69
    node_1230 --> node_253
    node_179 --> node_1272
    node_964 --> node_1016
    node_489 --> node_183
    node_205 --> node_1291
    node_632 --> node_1077
    node_1230 --> node_1319
    node_0 --> node_1077
    node_19 --> node_417
    node_600 --> node_652
    node_1117 --> node_196
    node_969 --> node_968
    node_63 --> node_911
    node_666 --> node_1302
    node_58 --> node_117
    node_145 --> node_1170
    node_505 --> node_253
    node_731 --> node_307
    node_772 --> node_766
    node_1314 --> node_1344
    node_5 --> node_1308
    node_935 --> node_1130
    node_666 --> node_1280
    node_575 --> node_486
    node_599 --> node_954
    node_520 --> node_1087
    node_861 --> node_650
    node_520 --> node_247
    node_1097 --> node_1123
    node_699 --> node_708
    node_935 --> node_1235
    node_1117 --> node_373
    node_187 --> node_328
    node_416 --> node_784
    node_781 --> node_617
    node_1231 --> node_1040
    node_1339 --> node_1184
    node_525 --> node_1195
    node_476 --> node_1260
    node_489 --> node_364
    node_541 --> node_1227
    node_630 --> node_1047
    node_1097 --> node_1059
    node_187 --> node_405
    node_772 --> node_943
    node_497 --> node_1017
    node_1314 --> node_1126
    node_884 --> node_1260
    node_56 --> node_135
    node_31 --> node_1021
    node_617 --> node_616
    node_1255 --> node_1047
    node_805 --> node_1290
    node_1231 --> node_1219
    node_1231 --> node_1226
    node_103 --> node_244
    node_514 --> node_282
    node_533 --> node_247
    node_497 --> node_177
    node_1117 --> node_998
    node_99 --> node_620
    node_595 --> node_577
    node_1339 --> node_1212
    node_497 --> node_742
    node_334 --> node_337
    node_861 --> node_969
    node_63 --> node_249
    node_1339 --> node_1155
    node_283 --> node_428
    node_541 --> node_680
    node_416 --> node_334
    node_573 --> node_993
    node_1117 --> node_197
    node_66 --> node_739
    node_1267 --> node_1148
    node_1256 --> node_1255
    node_1097 --> node_1069
    node_525 --> node_1015
    node_541 --> node_630
    node_541 --> node_739
    node_100 --> node_37
    node_666 --> node_1218
    node_1236 --> node_1233
    node_67 --> node_129
    node_56 --> node_1178
    node_1221 --> node_241
    node_19 --> node_422
    node_520 --> node_205
    node_591 --> node_27
    node_890 --> node_380
    node_458 --> node_1082
    node_1221 --> node_731
    node_1351 --> node_1047
    node_1314 --> node_1059
    node_68 --> node_329
    node_489 --> node_285
    node_1015 --> node_1017
    node_1361 --> node_1265
    node_520 --> node_1082
    node_72 --> node_271
    node_911 --> node_851
    node_525 --> node_1300
    node_561 --> node_928
    node_487 --> node_1260
    node_1230 --> node_1121
    node_632 --> node_1344
    node_0 --> node_1116
    node_497 --> node_1362
    node_0 --> node_1344
    node_100 --> node_784
    node_127 --> node_58
    node_541 --> node_253
    node_64 --> node_177
    node_1103 --> node_1265
    node_489 --> node_179
    node_5 --> node_1339
    node_670 --> node_1307
    node_63 --> node_617
    node_52 --> node_947
    node_489 --> node_284
    node_205 --> node_1288
    node_599 --> node_33
    node_251 --> node_741
    node_666 --> node_1164
    node_31 --> node_720
    node_1117 --> node_580
    node_831 --> node_1260
    node_142 --> node_487
    node_543 --> node_50
    node_1359 --> node_325
    node_632 --> node_1126
    node_666 --> node_1198
    node_1230 --> node_1035
    node_668 --> node_1129
    node_1261 --> node_1149
    node_500 --> node_731
    node_935 --> node_1132
    node_649 --> node_1082
    node_892 --> node_1148
    node_5 --> node_1220
    node_525 --> node_1267
    node_533 --> node_680
    node_541 --> node_208
    node_31 --> node_641
    node_5 --> node_1147
    node_1359 --> node_81
    node_1141 --> node_1123
    node_5 --> node_842
    node_658 --> node_1179
    node_5 --> node_361
    node_541 --> node_1222
    node_1357 --> node_1047
    node_1162 --> node_250
    node_154 --> node_1085
    node_953 --> node_33
    node_899 --> node_675
    node_489 --> node_1271
    node_935 --> node_1013
    node_815 --> node_1260
    node_896 --> node_3
    node_1147 --> node_187
    node_1339 --> node_1097
    node_416 --> node_620
    node_205 --> node_359
    node_632 --> node_1123
    node_663 --> node_1298
    node_0 --> node_1123
    node_861 --> node_1170
    node_20 --> node_490
    node_537 --> node_1161
    node_72 --> node_731
    node_1221 --> node_328
    node_1339 --> node_1338
    node_964 --> node_1012
    node_695 --> node_645
    node_856 --> node_422
    node_632 --> node_1059
    node_0 --> node_1059
    node_1102 --> node_1302
    node_507 --> node_5
    node_781 --> node_650
    node_772 --> node_486
    node_490 --> node_5
    node_520 --> node_969
    node_972 --> node_1083
    node_1339 --> node_1153
    node_1359 --> node_232
    node_936 --> node_1082
    node_599 --> node_68
    node_187 --> node_357
    node_383 --> node_445
    node_1133 --> node_1134
    node_31 --> node_632
    node_499 --> node_209
    node_19 --> node_563
    node_5 --> node_1065
    node_525 --> node_1024
    node_892 --> node_695
    node_31 --> node_320
    node_122 --> node_247
    node_52 --> node_135
    node_20 --> node_766
    node_486 --> node_232
    node_662 --> node_175
    node_773 --> node_180
    node_525 --> node_1098
    node_661 --> node_1008
    node_416 --> node_948
    node_743 --> node_72
    node_971 --> node_1239
    node_449 --> node_329
    node_3 --> node_15
    node_541 --> node_712
    node_1231 --> node_1088
    node_595 --> node_138
    node_666 --> node_1263
    node_31 --> node_48
    node_276 --> node_279
    node_525 --> node_1169
    node_632 --> node_1069
    node_500 --> node_328
    node_0 --> node_1069
    node_893 --> node_35
    node_972 --> node_36
    node_206 --> node_183
    node_665 --> node_1329
    node_497 --> node_1155
    node_658 --> node_1243
    node_56 --> node_152
    node_751 --> node_681
    node_785 --> node_35
    node_152 --> node_947
    node_100 --> node_620
    node_490 --> node_498
    node_541 --> node_746
    node_0 --> node_1191
    node_541 --> node_1035
    node_887 --> node_1271
    node_988 --> node_704
    node_1097 --> node_1226
    node_469 --> node_210
    node_355 --> node_260
    node_359 --> node_210
    node_1145 --> node_1099
    node_145 --> node_962
    node_1230 --> node_1335
    node_7 --> node_85
    node_525 --> node_1143
    node_72 --> node_328
    node_187 --> node_391
    node_63 --> node_650
    node_490 --> node_502
    node_187 --> node_397
    node_448 --> node_445
    node_1231 --> node_1227
    node_653 --> node_1093
    node_541 --> node_1125
    node_205 --> node_406
    node_662 --> node_972
    node_180 --> node_213
    node_1230 --> node_1037
    node_935 --> node_1009
    node_1364 --> node_178
    node_0 --> node_1225
    node_489 --> node_233
    node_449 --> node_742
    node_1266 --> node_1099
    node_595 --> node_556
    node_105 --> node_5
    node_5 --> node_985
    node_31 --> node_534
    node_205 --> node_384
    node_563 --> node_27
    node_478 --> node_695
    node_511 --> node_1046
    node_520 --> node_1170
    node_1081 --> node_487
    node_278 --> node_282
    node_1362 --> node_52
    node_704 --> node_1148
    node_403 --> node_260
    node_19 --> node_268
    node_1154 --> node_1152
    node_1352 --> node_52
    node_1339 --> node_1029
    node_63 --> node_969
    node_1339 --> node_1235
    node_1045 --> node_191
    node_189 --> node_213
    node_19 --> node_1273
    node_64 --> node_650
    node_842 --> node_628
    node_465 --> node_187
    node_5 --> node_175
    node_251 --> node_72
    node_187 --> node_344
    node_520 --> node_1117
    node_948 --> node_944
    node_19 --> node_364
    node_997 --> node_978
    node_449 --> node_203
    node_599 --> node_490
    node_152 --> node_135
    node_599 --> node_1337
    node_781 --> node_1170
    node_541 --> node_1005
    node_541 --> node_1023
    node_68 --> node_130
    node_1147 --> node_35
    node_521 --> node_72
    node_1097 --> node_1211
    node_187 --> node_367
    node_490 --> node_503
    node_506 --> node_183
    node_1243 --> node_1047
    node_482 --> node_184
    node_697 --> node_734
    node_908 --> node_189
    node_1035 --> node_1032
    node_228 --> node_224
    node_64 --> node_969
    node_1147 --> node_232
    node_520 --> node_1188
    node_704 --> node_695
    node_595 --> node_586
    node_215 --> node_341
    node_140 --> node_58
    node_541 --> node_1335
    node_599 --> node_766
    node_935 --> node_1134
    node_1230 --> node_1309
    node_520 --> node_36
    node_525 --> node_1329
    node_251 --> node_233
    node_541 --> node_1341
    node_652 --> node_1012
    node_663 --> node_1157
    node_935 --> node_1010
    node_1260 --> node_404
    node_1097 --> node_1006
    node_603 --> node_947
    node_1339 --> node_1042
    node_1339 --> node_1205
    node_31 --> node_175
    node_631 --> node_669
    node_490 --> node_523
    node_1352 --> node_1351
    node_1362 --> node_246
    node_0 --> node_1219
    node_0 --> node_1226
    node_106 --> node_1021
    node_1339 --> node_1146
    node_1267 --> node_1261
    node_1352 --> node_251
    node_521 --> node_233
    node_1339 --> node_1206
    node_452 --> node_327
    node_599 --> node_943
    node_124 --> node_731
    node_5 --> node_1354
    node_520 --> node_1200
    node_1352 --> node_246
    node_869 --> node_404
    node_497 --> node_1342
    node_1042 --> node_1341
    node_754 --> node_3
    node_5 --> node_855
    node_1097 --> node_1174
    node_1097 --> node_1088
    node_99 --> node_124
    node_63 --> node_1170
    node_541 --> node_178
    node_1359 --> node_307
    node_1339 --> node_1132
    node_1042 --> node_1142
    node_751 --> node_730
    node_5 --> node_695
    node_303 --> node_290
    node_666 --> node_1140
    node_1097 --> node_1031
    node_599 --> node_741
    node_1117 --> node_444
    node_106 --> node_64
    node_599 --> node_975
    node_449 --> node_960
    node_599 --> node_203
    node_205 --> node_1274
    node_666 --> node_1258
    node_230 --> node_221
    node_636 --> node_1181
    node_115 --> node_600
    node_102 --> node_146
    node_563 --> node_3
    node_499 --> node_179
    node_1314 --> node_1006
    node_274 --> node_279
    node_1025 --> node_571
    node_525 --> node_1223
    node_166 --> node_69
    node_1117 --> node_262
    node_497 --> node_1352
    node_541 --> node_1185
    node_416 --> node_490
    node_997 --> node_977
    node_497 --> node_1117
    node_595 --> node_1127
    node_1349 --> node_1348
    node_119 --> node_69
    node_1260 --> node_201
    node_665 --> node_1107
    node_733 --> node_698
    node_772 --> node_1138
    node_209 --> node_81
    node_489 --> node_69
    node_620 --> node_618
    node_1339 --> node_1092
    node_68 --> node_51
    node_64 --> node_1170
    node_1314 --> node_1174
    node_603 --> node_98
    node_1041 --> node_57
    node_1314 --> node_1197
    node_617 --> node_613
    node_1314 --> node_1031
    node_669 --> node_1352
    node_416 --> node_766
    node_603 --> node_135
    node_881 --> node_382
    node_124 --> node_328
    node_533 --> node_178
    node_370 --> node_1148
    node_99 --> node_681
    node_718 --> node_585
    node_209 --> node_267
    node_102 --> node_1177
    node_423 --> node_446
    node_632 --> node_1211
    node_106 --> node_1095
    node_0 --> node_1211
    node_67 --> node_138
    node_465 --> node_35
    node_5 --> node_1034
    node_642 --> node_33
    node_1083 --> node_250
    node_787 --> node_482
    node_103 --> node_737
    node_1015 --> node_1047
    node_489 --> node_384
    node_972 --> node_1302
    node_69 --> node_70
    node_103 --> node_966
    node_133 --> node_600
    node_531 --> node_221
    node_7 --> node_1128
    node_19 --> node_1284
    node_1231 --> node_1125
    node_473 --> node_360
    node_249 --> node_245
    node_541 --> node_1332
    node_971 --> node_1237
    node_19 --> node_360
    node_525 --> node_1310
    node_1339 --> node_1312
    node_187 --> node_1295
    node_19 --> node_72
    node_1230 --> node_1154
    node_229 --> node_1083
    node_632 --> node_1006
    node_708 --> node_35
    node_0 --> node_1006
    node_328 --> node_72
    node_599 --> node_578
    node_1046 --> node_1047
    node_1231 --> node_1305
    node_512 --> node_398
    node_367 --> node_260
    node_1148 --> node_1262
    node_520 --> node_962
    node_629 --> node_175
    node_976 --> node_739
    node_1117 --> node_255
    node_666 --> node_1173
    node_1097 --> node_1319
    node_187 --> node_365
    node_575 --> node_595
    node_599 --> node_486
    node_490 --> node_494
    node_187 --> node_607
    node_497 --> node_1205
    node_625 --> node_1238
    node_656 --> node_1007
    node_541 --> node_926
    node_187 --> node_219
    node_337 --> node_67
    node_1230 --> node_1229
    node_370 --> node_695
    node_632 --> node_1174
    node_632 --> node_1088
    node_1145 --> node_1075
    node_0 --> node_1174
    node_0 --> node_1088
    node_106 --> node_795
    node_699 --> node_704
    node_1231 --> node_1188
    node_520 --> node_1236
    node_666 --> node_1257
    node_103 --> node_133
    node_629 --> node_1103
    node_229 --> node_36
    node_892 --> node_1260
    node_632 --> node_1031
    node_1267 --> node_1264
    node_0 --> node_1031
    node_935 --> node_1066
    node_103 --> node_614
    node_719 --> node_1082
    node_5 --> node_189
    node_1231 --> node_1005
    node_952 --> node_955
    node_1231 --> node_1023
    node_19 --> node_233
    node_1314 --> node_1308
    node_525 --> node_1206
    node_490 --> node_514
    node_537 --> node_1209
    node_328 --> node_233
    node_460 --> node_198
    node_520 --> node_1230
    node_520 --> node_1133
    node_1266 --> node_1075
    node_1117 --> node_209
    node_1231 --> node_1200
    node_490 --> node_510
    node_829 --> node_1274
    node_1314 --> node_1319
    node_1117 --> node_219
    node_187 --> node_293
    node_5 --> node_1349
    node_187 --> node_1276
    node_125 --> node_144
    node_1278 --> node_388
    node_666 --> node_1295
    node_990 --> node_1047
    node_64 --> node_56
    node_667 --> node_652
    node_106 --> node_125
    node_0 --> node_1227
    node_1231 --> node_1341
    node_746 --> node_745
    node_1230 --> node_1325
    node_541 --> node_1324
    node_923 --> node_250
    node_505 --> node_52
    node_935 --> node_1014
    node_796 --> node_271
    node_497 --> node_1092
    node_971 --> node_1235
    node_1247 --> node_1047
    node_1066 --> node_1062
    node_738 --> node_72
    node_575 --> node_686
    node_525 --> node_1013
    node_1230 --> node_1261
    node_973 --> node_972
    node_642 --> node_1011
    node_1359 --> node_698
    node_497 --> node_649
    node_478 --> node_1260
    node_934 --> node_1180
    node_20 --> node_602
    node_520 --> node_1302
    node_1219 --> node_1215
    node_541 --> node_1043
    node_20 --> node_1138
    node_1045 --> node_487
    node_145 --> node_677
    node_106 --> node_1254
    node_5 --> node_1318
    node_1230 --> node_1336
    node_497 --> node_962
    node_5 --> node_1141
    node_1240 --> node_1047
    node_740 --> node_241
    node_1260 --> node_1290
    node_489 --> node_381
    node_659 --> node_1239
    node_1314 --> node_1339
    node_1231 --> node_1118
    node_99 --> node_730
    node_575 --> node_667
    node_31 --> node_6
    node_100 --> node_681
    node_666 --> node_1255
    node_543 --> node_67
    node_5 --> node_1272
    node_520 --> node_1299
    node_657 --> node_1050
    node_852 --> node_1148
    node_1341 --> node_1342
    node_1097 --> node_1035
    node_525 --> node_1068
    node_449 --> node_1083
    node_490 --> node_540
    node_1231 --> node_1185
    node_666 --> node_1075
    node_519 --> node_704
    node_7 --> node_326
    node_738 --> node_233
    node_476 --> node_1082
    node_497 --> node_1236
    node_1077 --> node_1083
    node_1339 --> node_1298
    node_666 --> node_1276
    node_632 --> node_1319
    node_847 --> node_1262
    node_525 --> node_1019
    node_1230 --> node_1094
    node_541 --> node_997
    node_884 --> node_1082
    node_522 --> node_185
    node_629 --> node_1105
    node_743 --> node_731
    node_246 --> node_57
    node_1339 --> node_1363
    node_381 --> node_260
    node_1314 --> node_1121
    node_1041 --> node_1085
    node_669 --> node_1039
    node_1097 --> node_1125
    node_525 --> node_1256
    node_1157 --> node_1047
    node_666 --> node_1293
    node_1153 --> node_1154
    node_497 --> node_1133
    node_505 --> node_251
    node_459 --> node_209
    node_1117 --> node_183
    node_64 --> node_962
    node_602 --> node_600
    node_505 --> node_246
    node_20 --> node_138
    node_541 --> node_52
    node_195 --> node_219
    node_288 --> node_1047
    node_704 --> node_1260
    node_864 --> node_275
    node_19 --> node_207
    node_915 --> node_411
    node_209 --> node_307
    node_489 --> node_1294
    node_361 --> node_250
    node_543 --> node_1148
    node_1359 --> node_253
    node_1117 --> node_220
    node_105 --> node_53
    node_500 --> node_607
    node_395 --> node_1148
    node_781 --> node_1043
    node_1048 --> node_1047
    node_145 --> node_954
    node_104 --> node_329
    node_187 --> node_277
    node_253 --> node_57
    node_1304 --> node_1358
    node_867 --> node_344
    node_642 --> node_1239
    node_487 --> node_1082
    node_1231 --> node_1332
    node_810 --> node_1282
    node_489 --> node_282
    node_950 --> node_33
    node_56 --> node_1139
    node_541 --> node_250
    node_1147 --> node_1262
    node_205 --> node_1268
    node_663 --> node_1156
    node_781 --> node_997
    node_19 --> node_346
    node_831 --> node_1082
    node_935 --> node_1065
    node_1141 --> node_1121
    node_1230 --> node_1231
    node_205 --> node_1277
    node_5 --> node_1260
    node_743 --> node_328
    node_1141 --> node_1119
    node_1351 --> node_1099
    node_522 --> node_189
    node_5 --> node_1077
    node_712 --> node_981
    node_669 --> node_1072
    node_682 --> node_1072
    node_632 --> node_1121
    node_106 --> node_244
    node_331 --> node_330
    node_102 --> node_150
    node_209 --> node_303
    node_314 --> node_290
    node_541 --> node_1353
    node_1162 --> node_203
    node_497 --> node_1299
    node_368 --> node_260
    node_1230 --> node_1167
    node_543 --> node_695
    node_1097 --> node_1335
    node_416 --> node_533
    node_785 --> node_395
    node_154 --> node_125
    node_391 --> node_189
    node_541 --> node_251
    node_700 --> node_707
    node_395 --> node_695
    node_507 --> node_336
    node_516 --> node_72
    node_541 --> node_246
    node_205 --> node_386
    node_815 --> node_1082
    node_520 --> node_1186
    node_63 --> node_1043
    node_632 --> node_1035
    node_1097 --> node_1037
    node_0 --> node_1035
    node_406 --> node_12
    node_521 --> node_731
    node_1117 --> node_179
    node_861 --> node_677
    node_179 --> node_1289
    node_490 --> node_492
    node_187 --> node_193
    node_301 --> node_607
    node_687 --> node_1261
    node_31 --> node_711
    node_229 --> node_1302
    node_772 --> node_667
    node_1300 --> node_741
    node_537 --> node_1162
    node_472 --> node_410
    node_865 --> node_395
    node_1300 --> node_203
    node_965 --> node_175
    node_541 --> node_5
    node_497 --> node_1218
    node_783 --> node_187
    node_1339 --> node_1066
    node_0 --> node_1125
    node_63 --> node_997
    node_229 --> node_241
    node_666 --> node_1024
    node_31 --> node_730
    node_1231 --> node_1324
    node_1314 --> node_1335
    node_423 --> node_424
    node_100 --> node_730
    node_229 --> node_731
    node_666 --> node_1233
    node_541 --> node_697
    node_575 --> node_720
    node_1019 --> node_1047
    node_74 --> node_73
    node_599 --> node_188
    node_516 --> node_233
    node_541 --> node_1166
    node_595 --> node_568
    node_593 --> node_600
    node_665 --> node_1086
    node_930 --> node_1007
    node_1117 --> node_193
    node_1097 --> node_1185
    node_1314 --> node_1037
    node_668 --> node_1131
    node_387 --> node_209
    node_11 --> node_178
    node_883 --> node_372
    node_187 --> node_1291
    node_559 --> node_1083
    node_68 --> node_241
    node_103 --> node_911
    node_423 --> node_442
    node_563 --> node_654
    node_1331 --> node_1239
    node_5 --> node_389
    node_541 --> node_1231
    node_935 --> node_175
    node_31 --> node_966
    node_5 --> node_1116
    node_449 --> node_1003
    node_541 --> node_15
    node_1081 --> node_57
    node_114 --> node_547
    node_1339 --> node_1157
    node_96 --> node_79
    node_497 --> node_1198
    node_543 --> node_675
    node_511 --> node_1354
    node_972 --> node_487
    node_205 --> node_402
    node_861 --> node_954
    node_1147 --> node_253
    node_1230 --> node_1327
    node_502 --> node_247
    node_519 --> node_4
    node_521 --> node_328
    node_370 --> node_1260
    node_0 --> node_1005
    node_275 --> node_1294
    node_1359 --> node_696
    node_145 --> node_68
    node_666 --> node_1271
    node_525 --> node_1026
    node_511 --> node_695
    node_954 --> node_951
    node_497 --> node_229
    node_449 --> node_82
    node_5 --> node_232
    node_416 --> node_1138
    node_246 --> node_1085
    node_671 --> node_175
    node_738 --> node_245
    node_466 --> node_189
    node_29 --> node_138
    node_101 --> node_547
    node_520 --> node_1326
    node_973 --> node_582
    node_489 --> node_410
    node_449 --> node_238
    node_783 --> node_223
    node_1015 --> node_1164
    node_564 --> node_662
    node_563 --> node_669
    node_632 --> node_1335
    node_948 --> node_82
    node_1139 --> node_62
    node_0 --> node_1335
    node_520 --> node_677
    node_525 --> node_1197
    node_772 --> node_1021
    node_31 --> node_532
    node_1219 --> node_1216
    node_0 --> node_1341
    node_541 --> node_628
    node_575 --> node_48
    node_742 --> node_36
    node_39 --> node_44
    node_1102 --> node_741
    node_541 --> node_1057
    node_58 --> node_122
    node_19 --> node_381
    node_632 --> node_1037
    node_520 --> node_334
    node_1339 --> node_1093
    node_63 --> node_251
    node_537 --> node_1259
    node_474 --> node_187
    node_1312 --> node_232
    node_489 --> node_1268
    node_1117 --> node_57
    node_63 --> node_246
    node_1314 --> node_1309
    node_205 --> node_369
    node_253 --> node_1085
    node_62 --> node_58
    node_781 --> node_677
    node_1173 --> node_1172
    node_1230 --> node_977
    node_541 --> node_606
    node_1162 --> node_1160
    node_187 --> node_1288
    node_5 --> node_1307
    node_799 --> node_1294
    node_666 --> node_1124
    node_500 --> node_350
    node_19 --> node_731
    node_889 --> node_267
    node_840 --> node_373
    node_1231 --> node_1186
    node_625 --> node_1233
    node_656 --> node_1234
    node_328 --> node_731
    node_157 --> node_69
    node_520 --> node_222
    node_632 --> node_1185
    node_56 --> node_58
    node_0 --> node_1185
    node_599 --> node_82
    node_783 --> node_35
    node_772 --> node_720
    node_19 --> node_1294
    node_1339 --> node_1041
    node_661 --> node_1016
    node_490 --> node_535
    node_1231 --> node_1353
    node_453 --> node_372
    node_153 --> node_64
    node_20 --> node_667
    node_1117 --> node_223
    node_5 --> node_1191
    node_5 --> node_1030
    node_106 --> node_58
    node_541 --> node_27
    node_665 --> node_1147
    node_96 --> node_739
    node_541 --> node_31
    node_497 --> node_784
    node_642 --> node_1237
    node_657 --> node_1048
    node_1097 --> node_1324
    node_525 --> node_1308
    node_1231 --> node_1330
    node_145 --> node_490
    node_104 --> node_72
    node_145 --> node_1337
    node_1339 --> node_1065
    node_195 --> node_187
    node_19 --> node_1285
    node_632 --> node_1309
    node_861 --> node_248
    node_423 --> node_443
    node_599 --> node_595
    node_599 --> node_1128
    node_63 --> node_677
    node_5 --> node_1225
    node_205 --> node_1148
    node_531 --> node_243
    node_781 --> node_954
    node_5 --> node_585
    node_489 --> node_243
    node_533 --> node_551
    node_500 --> node_1291
    node_311 --> node_1047
    node_352 --> node_430
    node_663 --> node_1323
    node_781 --> node_606
    node_450 --> node_67
    node_5 --> node_311
    node_666 --> node_1288
    node_731 --> node_697
    node_861 --> node_68
    node_1339 --> node_1214
    node_1339 --> node_1314
    node_497 --> node_334
    node_0 --> node_1332
    node_145 --> node_766
    node_666 --> node_1223
    node_695 --> node_1128
    node_1351 --> node_1075
    node_537 --> node_320
    node_19 --> node_328
    node_12 --> node_662
    node_757 --> node_1148
    node_1231 --> node_1166
    node_546 --> node_3
    node_636 --> node_663
    node_520 --> node_948
    node_738 --> node_731
    node_666 --> node_1316
    node_599 --> node_1046
    node_490 --> node_508
    node_5 --> node_512
    node_429 --> node_423
    node_145 --> node_943
    node_489 --> node_402
    node_64 --> node_677
    node_489 --> node_327
    node_772 --> node_48
    node_599 --> node_949
    node_209 --> node_266
    node_520 --> node_1027
    node_1314 --> node_1154
    node_1081 --> node_1085
    node_305 --> node_313
    node_647 --> node_1107
    node_541 --> node_1357
    node_1083 --> node_203
    node_599 --> node_1078
    node_205 --> node_695
    node_1306 --> node_1047
    node_449 --> node_229
    node_1304 --> node_1144
    node_474 --> node_35
    node_20 --> node_1021
    node_7 --> node_331
    node_104 --> node_123
    node_145 --> node_975
    node_103 --> node_650
    node_252 --> node_1291
    node_525 --> node_1339
    node_1267 --> node_1082
    node_63 --> node_954
    node_751 --> node_1095
    node_1231 --> node_1207
    node_1250 --> node_1047
    node_389 --> node_260
    node_1089 --> node_1047
    node_543 --> node_1260
    node_923 --> node_679
    node_63 --> node_606
    node_642 --> node_1235
    node_395 --> node_1260
    node_934 --> node_1011
    node_5 --> node_1040
    node_757 --> node_695
    node_666 --> node_1126
    node_1330 --> node_1015
    node_675 --> node_1278
    node_490 --> node_493
    node_662 --> node_176
    node_525 --> node_1220
    node_20 --> node_64
    node_543 --> node_423
    node_5 --> node_1219
    node_5 --> node_1226
    node_521 --> node_320
    node_541 --> node_201
    node_1261 --> node_221
    node_1331 --> node_1237
    node_489 --> node_369
    node_497 --> node_1140
    node_965 --> node_1141
    node_103 --> node_969
    node_525 --> node_1147
    node_142 --> node_1046
    node_851 --> node_600
    node_489 --> node_218
    node_599 --> node_667
    node_1231 --> node_1057
    node_454 --> node_198
    node_0 --> node_1324
    node_911 --> node_406
    node_19 --> node_412
    node_582 --> node_583
    node_233 --> node_72
    node_738 --> node_328
    node_1081 --> node_1313
    node_1189 --> node_996
    node_64 --> node_954
    node_656 --> node_1016
    node_1230 --> node_1017
    node_520 --> node_1257
    node_559 --> node_241
    node_1117 --> node_1085
    node_393 --> node_1272
    node_665 --> node_175
    node_1097 --> node_1336
    node_205 --> node_198
    node_892 --> node_1082
    node_79 --> node_327
    node_1346 --> node_986
    node_412 --> node_264
    node_559 --> node_731
    node_661 --> node_1012
    node_520 --> node_1020
    node_187 --> node_1283
    node_1314 --> node_1325
    node_819 --> node_361
    node_187 --> node_182
    node_1117 --> node_981
    node_20 --> node_720
    node_541 --> node_1081
    node_861 --> node_490
    node_861 --> node_1337
    node_1314 --> node_1318
    node_179 --> node_363
    node_541 --> node_604
    node_154 --> node_58
    node_665 --> node_1103
    node_497 --> node_948
    node_544 --> node_67
    node_102 --> node_1178
    node_1097 --> node_1094
    node_639 --> node_669
    node_742 --> node_1302
    node_106 --> node_737
    node_281 --> node_680
    node_601 --> node_631
    node_658 --> node_1242
    node_19 --> node_410
    node_449 --> node_37
    node_665 --> node_1148
    node_541 --> node_1194
    node_599 --> node_326
    node_106 --> node_156
    node_229 --> node_487
    node_106 --> node_104
    node_543 --> node_718
    node_774 --> node_277
    node_781 --> node_68
    node_742 --> node_241
    node_711 --> node_699
    node_526 --> node_205
    node_489 --> node_374
    node_58 --> node_128
    node_861 --> node_766
    node_770 --> node_1149
    node_187 --> node_297
    node_934 --> node_1017
    node_1314 --> node_1336
    node_145 --> node_486
    node_449 --> node_784
    node_1117 --> node_182
    node_595 --> node_561
    node_562 --> node_583
    node_1230 --> node_1301
    node_178 --> node_1039
    node_5 --> node_249
    node_657 --> node_1313
    node_1339 --> node_1060
    node_31 --> node_911
    node_934 --> node_1239
    node_1259 --> node_1258
    node_511 --> node_1260
    node_842 --> node_649
    node_490 --> node_106
    node_571 --> node_1047
    node_861 --> node_943
    node_497 --> node_645
    node_1314 --> node_1094
    node_997 --> node_995
    node_1167 --> node_1007
    node_603 --> node_29
    node_516 --> node_731
    node_1124 --> node_1127
    node_103 --> node_1170
    node_490 --> node_501
    node_478 --> node_1082
    node_1339 --> node_1122
    node_106 --> node_133
    node_1331 --> node_1235
    node_31 --> node_1221
    node_517 --> node_268
    node_1117 --> node_217
    node_449 --> node_334
    node_632 --> node_1325
    node_145 --> node_102
    node_331 --> node_698
    node_416 --> node_667
    node_812 --> node_272
    node_1145 --> node_967
    node_106 --> node_614
    node_1230 --> node_1087
    node_497 --> node_1173
    node_20 --> node_795
    node_142 --> node_122
    node_112 --> node_154
    node_861 --> node_975
    node_187 --> node_1274
    node_971 --> node_1238
    node_20 --> node_48
    node_541 --> node_1017
    node_1362 --> node_1083
    node_385 --> node_260
    node_1097 --> node_1231
    node_1231 --> node_1027
    node_56 --> node_120
    node_23 --> node_425
    node_63 --> node_68
    node_72 --> node_73
    node_12 --> node_636
    node_520 --> node_1195
    node_106 --> node_136
    node_497 --> node_1257
    node_645 --> node_978
    node_1339 --> node_1356
    node_99 --> node_739
    node_541 --> node_1239
    node_599 --> node_37
    node_666 --> node_1019
    node_1266 --> node_967
    node_541 --> node_540
    node_497 --> node_642
    node_106 --> node_120
    node_520 --> node_490
    node_1045 --> node_1048
    node_205 --> node_58
    node_541 --> node_742
    node_1097 --> node_1167
    node_1359 --> node_52
    node_1339 --> node_1034
    node_5 --> node_1088
    node_489 --> node_695
    node_101 --> node_739
    node_632 --> node_1336
    node_1339 --> node_1192
    node_666 --> node_1256
    node_1202 --> node_759
    node_489 --> node_589
    node_1081 --> node_1046
    node_541 --> node_733
    node_665 --> node_1105
    node_656 --> node_1017
    node_521 --> node_175
    node_449 --> node_488
    node_486 --> node_52
    node_1231 --> node_1357
    node_704 --> node_1082
    node_541 --> node_1104
    node_205 --> node_349
    node_7 --> node_6
    node_520 --> node_1015
    node_520 --> node_766
    node_632 --> node_1094
    node_1101 --> node_1144
    node_64 --> node_68
    node_106 --> node_1213
    node_102 --> node_152
    node_516 --> node_328
    node_578 --> node_559
    node_1304 --> node_1303
    node_541 --> node_1362
    node_31 --> node_617
    node_781 --> node_1337
    node_106 --> node_31
    node_128 --> node_73
    node_646 --> node_1078
    node_1339 --> node_1340
    node_131 --> node_69
    node_19 --> node_418
    node_170 --> node_73
    node_1267 --> node_1083
    node_709 --> node_1047
    node_520 --> node_1300
    node_205 --> node_1272
    node_449 --> node_487
    node_665 --> node_1145
    node_282 --> node_279
    node_1077 --> node_487
    node_475 --> node_187
    node_1314 --> node_1167
    node_840 --> node_444
    node_520 --> node_943
    node_5 --> node_1227
    node_449 --> node_620
    node_1339 --> node_1045
    node_1126 --> node_1127
    node_855 --> node_187
    node_997 --> node_1187
    node_575 --> node_681
    node_99 --> node_1095
    node_1339 --> node_1036
    node_31 --> node_592
    node_104 --> node_106
    node_861 --> node_960
    node_642 --> node_1009
    node_871 --> node_27
    node_5 --> node_205
    node_1231 --> node_1020
    node_541 --> node_702
    node_20 --> node_1254
    node_416 --> node_1021
    node_5 --> node_812
    node_448 --> node_428
    node_19 --> node_408
    node_668 --> node_1133
    node_840 --> node_262
    node_5 --> node_1082
    node_1339 --> node_1232
    node_41 --> node_600
    node_781 --> node_742
    node_520 --> node_741
    node_666 --> node_1128
    node_521 --> node_607
    node_537 --> node_1182
    node_861 --> node_486
    node_511 --> node_232
    node_497 --> node_12
    node_664 --> node_1090
    node_520 --> node_1267
    node_695 --> node_641
    node_1359 --> node_251
    node_187 --> node_204
    node_658 --> node_1247
    node_687 --> node_249
    node_497 --> node_1156
    node_1359 --> node_246
    node_134 --> node_122
    node_861 --> node_1270
    node_449 --> node_948
    node_416 --> node_64
    node_248 --> node_327
    node_751 --> node_244
    node_486 --> node_251
    node_1231 --> node_1081
    node_486 --> node_246
    node_924 --> node_27
    node_229 --> node_209
    node_632 --> node_1231
    node_63 --> node_1337
    node_497 --> node_490
    node_533 --> node_203
    node_0 --> node_1231
    node_229 --> node_219
    node_541 --> node_336
    node_187 --> node_212
    node_489 --> node_206
    node_5 --> node_395
    node_781 --> node_975
    node_489 --> node_1269
    node_1231 --> node_1194
    node_65 --> node_1047
    node_599 --> node_48
    node_533 --> node_702
    node_599 --> node_16
    node_1117 --> node_204
    node_666 --> node_1294
    node_541 --> node_960
    node_1359 --> node_697
    node_632 --> node_1167
    node_1339 --> node_1201
    node_416 --> node_720
    node_964 --> node_1011
    node_205 --> node_1260
    node_497 --> node_1015
    node_99 --> node_746
    node_846 --> node_245
    node_520 --> node_1024
    node_497 --> node_766
    node_1304 --> node_1265
    node_791 --> node_67
    node_278 --> node_283
    node_179 --> node_1149
    node_866 --> node_72
    node_105 --> node_241
    node_31 --> node_680
    node_657 --> node_1054
    node_520 --> node_1098
    node_63 --> node_742
    node_972 --> node_57
    node_541 --> node_1155
    node_1314 --> node_1327
    node_783 --> node_213
    node_520 --> node_1184
    node_642 --> node_1010
    node_665 --> node_58
    node_1209 --> node_1047
    node_64 --> node_490
    node_64 --> node_1337
    node_520 --> node_1169
    node_653 --> node_1031
    node_100 --> node_739
    node_1117 --> node_212
    node_1153 --> node_1152
    node_523 --> node_947
    node_1312 --> node_253
    node_1339 --> node_1141
    node_1147 --> node_52
    node_840 --> node_255
    node_757 --> node_1260
    node_658 --> node_1175
    node_1360 --> node_81
    node_63 --> node_943
    node_704 --> node_712
    node_308 --> node_734
    node_11 --> node_673
    node_31 --> node_650
    node_1039 --> node_1038
    node_104 --> node_731
    node_889 --> node_610
    node_739 --> node_241
    node_695 --> node_327
    node_520 --> node_1212
    node_20 --> node_244
    node_803 --> node_1294
    node_1332 --> node_178
    node_847 --> node_1149
    node_520 --> node_486
    node_64 --> node_766
    node_63 --> node_975
    node_187 --> node_213
    node_866 --> node_233
    node_520 --> node_1143
    node_1314 --> node_1307
    node_370 --> node_1082
    node_537 --> node_1090
    node_797 --> node_272
    node_67 --> node_58
    node_1045 --> node_1313
    node_773 --> node_241
    node_712 --> node_1148
    node_169 --> node_73
    node_406 --> node_264
    node_1231 --> node_1239
    node_781 --> node_960
    node_3 --> node_951
    node_451 --> node_67
    node_475 --> node_35
    node_575 --> node_711
    node_64 --> node_943
    node_934 --> node_1237
    node_929 --> node_1237
    node_841 --> node_417
    node_855 --> node_35
    node_958 --> node_961
    node_416 --> node_795
    node_229 --> node_183
    node_514 --> node_247
    node_731 --> node_733
    node_677 --> node_678
    node_639 --> node_661
    node_228 --> node_217
    node_280 --> node_279
    node_768 --> node_193
    node_575 --> node_730
    node_1339 --> node_1323
    node_100 --> node_1095
    node_1352 --> node_238
    node_1260 --> node_357
    node_559 --> node_487
    node_666 --> node_1197
    node_802 --> node_1284
    node_1117 --> node_213
    node_525 --> node_1154
    node_954 --> node_957
    node_540 --> node_562
    node_1117 --> node_849
    node_64 --> node_975
    node_205 --> node_389
    node_162 --> node_54
    node_499 --> node_1148
    node_892 --> node_290
    node_1147 --> node_246
    node_1230 --> node_1117
    node_122 --> node_203
    node_665 --> node_1101
    node_1101 --> node_1303
    node_1231 --> node_1362
    node_37 --> node_247
    node_449 --> node_240
    node_1147 --> node_1149
    node_669 --> node_1232
    node_497 --> node_1024
    node_104 --> node_328
    node_1230 --> node_1083
    node_541 --> node_1153
    node_497 --> node_1098
    node_505 --> node_1047
    node_575 --> node_966
    node_19 --> node_1296
    node_712 --> node_695
    node_948 --> node_240
    node_525 --> node_1349
    node_923 --> node_36
    node_1339 --> node_1077
    node_5 --> node_1125
    node_232 --> node_241
    node_911 --> node_882
    node_505 --> node_1083
    node_599 --> node_175
    node_261 --> node_198
    node_654 --> node_1168
    node_63 --> node_960
    node_911 --> node_410
    node_639 --> node_665
    node_537 --> node_1343
    node_841 --> node_248
    node_179 --> node_1286
    node_7 --> node_81
    node_522 --> node_739
    node_531 --> node_187
    node_334 --> node_72
    node_589 --> node_583
    node_666 --> node_1021
    node_695 --> node_175
    node_5 --> node_1305
    node_520 --> node_1329
    node_63 --> node_486
    node_106 --> node_177
    node_1097 --> node_1194
    node_249 --> node_57
    node_499 --> node_695
    node_31 --> node_746
    node_497 --> node_1143
    node_233 --> node_731
    node_100 --> node_746
    node_599 --> node_8
    node_416 --> node_1254
    node_835 --> node_345
    node_541 --> node_1342
    node_930 --> node_1017
    node_187 --> node_399
    node_934 --> node_1235
    node_929 --> node_1235
    node_1352 --> node_1078
    node_5 --> node_1188
    node_112 --> node_143
    node_72 --> node_79
    node_652 --> node_1011
    node_1173 --> node_1171
    node_31 --> node_571
    node_103 --> node_1043
    node_525 --> node_1318
    node_525 --> node_1141
    node_99 --> node_244
    node_5 --> node_1005
    node_1231 --> node_1184
    node_62 --> node_247
    node_489 --> node_1260
    node_5 --> node_1023
    node_0 --> node_1357
    node_804 --> node_347
    node_208 --> node_243
    node_1346 --> node_1345
    node_334 --> node_233
    node_406 --> node_212
    node_1330 --> node_1013
    node_1042 --> node_1342
    node_76 --> node_69
    node_541 --> node_1352
    node_101 --> node_546
    node_64 --> node_486
    node_445 --> node_425
    node_541 --> node_1047
    node_1045 --> node_1046
    node_666 --> node_1196
    node_856 --> node_1296
    node_541 --> node_1117
    node_5 --> node_1200
    node_666 --> node_1268
    node_695 --> node_331
    node_430 --> node_735
    node_103 --> node_997
    node_1101 --> node_1265
    node_1219 --> node_983
    node_180 --> node_205
    node_520 --> node_1223
    node_972 --> node_1085
    node_772 --> node_711
    node_541 --> node_1083
    node_1231 --> node_1155
    node_502 --> node_1149
    node_666 --> node_1277
    node_5 --> node_1341
    node_541 --> node_1029
    node_1339 --> node_1116
    node_1339 --> node_1344
    node_361 --> node_36
    node_1015 --> node_1345
    node_1097 --> node_1017
    node_542 --> node_178
    node_658 --> node_1253
    node_772 --> node_730
    node_1267 --> node_191
    node_456 --> node_410
    node_64 --> node_102
    node_19 --> node_206
    node_233 --> node_328
    node_3 --> node_584
    node_19 --> node_1269
    node_528 --> node_676
    node_491 --> node_571
    node_189 --> node_205
    node_58 --> node_118
    node_659 --> node_1238
    node_521 --> node_187
    node_666 --> node_1217
    node_511 --> node_249
    node_595 --> node_3
    node_5 --> node_178
    node_585 --> node_676
    node_828 --> node_282
    node_145 --> node_595
    node_953 --> node_12
    node_652 --> node_1017
    node_187 --> node_327
    node_497 --> node_1329
    node_772 --> node_966
    node_911 --> node_842
    node_913 --> node_695
    node_209 --> node_697
    node_142 --> node_1354
    node_954 --> node_961
    node_263 --> node_451
    node_5 --> node_1118
    node_79 --> node_697
    node_543 --> node_1082
    node_678 --> node_509
    node_1236 --> node_1234
    node_965 --> node_176
    node_972 --> node_1313
    node_395 --> node_1082
    node_520 --> node_1310
    node_1097 --> node_1301
    node_416 --> node_244
    node_1097 --> node_1362
    node_1339 --> node_1123
    node_675 --> node_676
    node_489 --> node_389
    node_0 --> node_1194
    node_65 --> node_241
    node_595 --> node_604
    node_577 --> node_983
    node_29 --> node_543
    node_1076 --> node_1350
    node_666 --> node_1220
    node_1214 --> node_987
    node_541 --> node_1205
    node_520 --> node_1138
    node_67 --> node_133
    node_254 --> node_210
    node_1339 --> node_1059
    node_812 --> node_276
    node_666 --> node_1121
    node_541 --> node_1146
    node_649 --> node_792
    node_531 --> node_35
    node_695 --> node_549
    node_1231 --> node_1097
    node_1351 --> node_967
    node_72 --> node_739
    node_790 --> node_187
    node_567 --> node_1280
    node_229 --> node_57
    node_1230 --> node_1236
    node_31 --> node_178
    node_642 --> node_1238
    node_556 --> node_240
    node_372 --> node_256
    node_405 --> node_260
    node_854 --> node_277
    node_497 --> node_1223
    node_476 --> node_209
    node_1231 --> node_1153
    node_520 --> node_1042
    node_1339 --> node_1069
    node_67 --> node_120
    node_1314 --> node_1301
    node_330 --> node_698
    node_520 --> node_1206
    node_1230 --> node_1133
    node_5 --> node_1332
    node_106 --> node_650
    node_631 --> node_652
    node_578 --> node_188
    node_647 --> node_175
    node_541 --> node_892
    node_751 --> node_737
    node_632 --> node_1017
    node_0 --> node_1017
    node_5 --> node_392
    node_693 --> node_175
    node_147 --> node_144
    node_541 --> node_1092
    node_903 --> node_272
    node_102 --> node_1139
    node_5 --> node_363
    node_647 --> node_1103
    node_783 --> node_1148
    node_861 --> node_82
    node_505 --> node_238
    node_1314 --> node_1087
    node_249 --> node_1085
    node_0 --> node_1239
    node_876 --> node_398
    node_12 --> node_657
    node_1267 --> node_1263
    node_923 --> node_1302
    node_68 --> node_533
    node_145 --> node_667
    node_7 --> node_307
    node_541 --> node_649
    node_5 --> node_845
    node_1081 --> node_1148
    node_1231 --> node_1342
    node_537 --> node_1347
    node_234 --> node_241
    node_520 --> node_1013
    node_665 --> node_1191
    node_517 --> node_271
    node_106 --> node_969
    node_599 --> node_681
    node_326 --> node_51
    node_525 --> node_1116
    node_599 --> node_6
    node_183 --> node_220
    node_497 --> node_1126
    node_666 --> node_1254
    node_672 --> node_1033
    node_805 --> node_406
    node_934 --> node_1009
    node_1097 --> node_1155
    node_1221 --> node_327
    node_658 --> node_1177
    node_1260 --> node_365
    node_490 --> node_20
    node_653 --> node_178
    node_654 --> node_175
    node_5 --> node_414
    node_712 --> node_1101
    node_866 --> node_1128
    node_1046 --> node_1048
    node_497 --> node_1138
    node_700 --> node_701
    node_1167 --> node_1016
    node_103 --> node_677
    node_99 --> node_58
    node_521 --> node_35
    node_861 --> node_595
    node_632 --> node_1301
    node_541 --> node_1003
    node_1231 --> node_1352
    node_632 --> node_1362
    node_187 --> node_211
    node_19 --> node_187
    node_0 --> node_1362
    node_489 --> node_283
    node_541 --> node_1236
    node_1117 --> node_236
    node_1230 --> node_1299
    node_489 --> node_419
    node_751 --> node_614
    node_678 --> node_739
    node_1081 --> node_1354
    node_37 --> node_36
    node_505 --> node_241
    node_972 --> node_1046
    node_520 --> node_1068
    node_505 --> node_731
    node_3 --> node_598
    node_1042 --> node_1039
    node_1231 --> node_1029
    node_520 --> node_1019
    node_1231 --> node_1235
    node_5 --> node_1324
    node_541 --> node_1133
    node_185 --> node_213
    node_410 --> node_260
    node_1117 --> node_1103
    node_1081 --> node_695
    node_1359 --> node_733
    node_1331 --> node_1238
    node_20 --> node_966
    node_712 --> node_1260
    node_1117 --> node_181
    node_449 --> node_57
    node_520 --> node_1312
    node_1230 --> node_191
    node_663 --> node_1064
    node_632 --> node_1087
    node_1260 --> node_1276
    node_1236 --> node_1016
    node_1117 --> node_1148
    node_520 --> node_1256
    node_656 --> node_1236
    node_541 --> node_238
    node_326 --> node_1047
    node_52 --> node_739
    node_490 --> node_495
    node_489 --> node_257
    node_646 --> node_1075
    node_617 --> node_183
    node_575 --> node_911
    node_543 --> node_571
    node_1352 --> node_488
    node_790 --> node_35
    node_1069 --> node_1070
    node_943 --> node_937
    node_133 --> node_547
    node_629 --> node_1118
    node_361 --> node_1302
    node_790 --> node_267
    node_474 --> node_1148
    node_103 --> node_954
    node_359 --> node_209
    node_258 --> node_377
    node_106 --> node_1170
    node_537 --> node_257
    node_1117 --> node_972
    node_1362 --> node_487
    node_499 --> node_1260
    node_525 --> node_1307
    node_751 --> node_1213
    node_106 --> node_105
    node_781 --> node_1003
    node_647 --> node_1105
    node_934 --> node_1010
    node_751 --> node_31
    node_205 --> node_1290
    node_1251 --> node_1240
    node_1251 --> node_1250
    node_5 --> node_411
    node_911 --> node_855
    node_709 --> node_719
    node_62 --> node_36
    node_1166 --> node_1047
    node_1231 --> node_1042
    node_911 --> node_695
    node_1231 --> node_1205
    node_278 --> node_280
    node_66 --> node_241
    node_505 --> node_328
    node_867 --> node_1268
    node_333 --> node_9
    node_1231 --> node_1146
    node_541 --> node_241
    node_66 --> node_731
    node_1251 --> node_1241
    node_1117 --> node_695
    node_179 --> node_1273
    node_104 --> node_20
    node_541 --> node_731
    node_922 --> node_1084
    node_525 --> node_1191
    node_525 --> node_1030
    node_19 --> node_281
    node_229 --> node_1085
    node_5 --> node_340
    node_5 --> node_463
    node_173 --> node_116
    node_861 --> node_667
    node_0 --> node_1155
    node_5 --> node_52
    node_833 --> node_412
    node_1333 --> node_67
    node_1231 --> node_1132
    node_31 --> node_1043
    node_566 --> node_3
    node_1198 --> node_1196
    node_497 --> node_1068
    node_663 --> node_1037
    node_599 --> node_711
    node_1327 --> node_1328
    node_1359 --> node_336
    node_205 --> node_370
    node_573 --> node_999
    node_1015 --> node_1013
    node_145 --> node_720
    node_172 --> node_69
    node_497 --> node_1019
    node_1167 --> node_1017
    node_489 --> node_194
    node_1267 --> node_487
    node_525 --> node_1225
    node_1319 --> node_999
    node_975 --> node_970
    node_497 --> node_297
    node_599 --> node_730
    node_1252 --> node_67
    node_781 --> node_595
    node_521 --> node_585
    node_63 --> node_1003
    node_575 --> node_617
    node_1097 --> node_1342
    node_195 --> node_1148
    node_1117 --> node_1105
    node_155 --> node_58
    node_31 --> node_997
    node_209 --> node_201
    node_497 --> node_1256
    node_1117 --> node_427
    node_541 --> node_1218
    node_1312 --> node_52
    node_5 --> node_919
    node_367 --> node_1293
    node_670 --> node_1306
    node_19 --> node_35
    node_100 --> node_58
    node_1339 --> node_1211
    node_1117 --> node_198
    node_1231 --> node_1092
    node_490 --> node_497
    node_205 --> node_1082
    node_5 --> node_1186
    node_19 --> node_267
    node_334 --> node_731
    node_229 --> node_1313
    node_99 --> node_737
    node_275 --> node_419
    node_599 --> node_966
    node_916 --> node_1287
    node_330 --> node_696
    node_1097 --> node_1352
    node_66 --> node_328
    node_913 --> node_1260
    node_7 --> node_734
    node_964 --> node_1013
    node_1015 --> node_1019
    node_187 --> node_190
    node_541 --> node_328
    node_1097 --> node_1117
    node_1117 --> node_321
    node_1252 --> node_178
    node_5 --> node_1353
    node_449 --> node_1138
    node_63 --> node_238
    node_826 --> node_272
    node_1061 --> node_33
    node_757 --> node_1082
    node_665 --> node_176
    node_489 --> node_416
    node_5 --> node_251
    node_1339 --> node_1006
    node_567 --> node_391
    node_922 --> node_947
    node_541 --> node_1198
    node_772 --> node_911
    node_106 --> node_56
    node_5 --> node_215
    node_5 --> node_246
    node_163 --> node_62
    node_197 --> node_190
    node_490 --> node_516
    node_677 --> node_676
    node_1330 --> node_1014
    node_230 --> node_1262
    node_156 --> node_133
    node_751 --> node_3
    node_459 --> node_695
    node_195 --> node_695
    node_5 --> node_1330
    node_602 --> node_138
    node_1231 --> node_1312
    node_263 --> node_259
    node_795 --> node_786
    node_63 --> node_595
    node_145 --> node_48
    node_687 --> node_191
    node_525 --> node_1040
    node_12 --> node_670
    node_520 --> node_667
    node_1339 --> node_1174
    node_1339 --> node_1088
    node_541 --> node_229
    node_0 --> node_1153
    node_103 --> node_68
    node_953 --> node_961
    node_151 --> node_72
    node_543 --> node_290
    node_1339 --> node_1031
    node_795 --> node_187
    node_1312 --> node_251
    node_1314 --> node_1117
    node_12 --> node_673
    node_520 --> node_1026
    node_599 --> node_81
    node_525 --> node_1219
    node_525 --> node_1226
    node_1312 --> node_246
    node_413 --> node_187
    node_449 --> node_947
    node_861 --> node_37
    node_99 --> node_614
    node_156 --> node_120
    node_584 --> node_367
    node_205 --> node_1289
    node_1230 --> node_1326
    node_449 --> node_1085
    node_56 --> node_1183
    node_666 --> node_1269
    node_334 --> node_328
    node_5 --> node_1166
    node_799 --> node_419
    node_540 --> node_573
    node_1103 --> node_585
    node_665 --> node_1087
    node_286 --> node_1047
    node_659 --> node_1233
    node_742 --> node_57
    node_1081 --> node_1261
    node_593 --> node_81
    node_205 --> node_376
    node_657 --> node_1051
    node_997 --> node_992
    node_64 --> node_595
    node_183 --> node_482
    node_5 --> node_383
    node_1314 --> node_1188
    node_512 --> node_387
    node_531 --> node_1262
    node_541 --> node_565
    node_599 --> node_232
    node_1097 --> node_1205
    node_19 --> node_419
    node_416 --> node_737
    node_151 --> node_233
    node_632 --> node_1342
    node_416 --> node_966
    node_0 --> node_1342
    node_63 --> node_1078
    node_559 --> node_577
    node_964 --> node_1009
    node_1006 --> node_1004
    node_922 --> node_135
    node_599 --> node_65
    node_187 --> node_1272
    node_965 --> node_1142
    node_935 --> node_1135
    node_599 --> node_32
    node_106 --> node_962
    node_334 --> node_326
    node_772 --> node_617
    node_898 --> node_277
    node_781 --> node_229
    node_666 --> node_1349
    node_5 --> node_1207
    node_1314 --> node_1200
    node_205 --> node_368
    node_99 --> node_1213
    node_632 --> node_1352
    node_0 --> node_1352
    node_99 --> node_31
    node_449 --> node_1313
    node_209 --> node_733
    node_37 --> node_496
    node_587 --> node_992
    node_632 --> node_1117
    node_1077 --> node_1313
    node_0 --> node_1117
    node_19 --> node_257
    node_154 --> node_36
    node_19 --> node_555
    node_449 --> node_98
    node_880 --> node_206
    node_1148 --> node_1047
    node_229 --> node_1046
    node_965 --> node_178
    node_770 --> node_221
    node_520 --> node_1021
    node_543 --> node_704
    node_1004 --> node_430
    node_642 --> node_1233
    node_449 --> node_135
    node_502 --> node_203
    node_497 --> node_667
    node_948 --> node_98
    node_541 --> node_784
    node_17 --> node_198
    node_520 --> node_1066
    node_541 --> node_357
    node_5 --> node_1057
    node_666 --> node_1022
    node_505 --> node_488
    node_142 --> node_232
    node_712 --> node_3
    node_751 --> node_177
    node_1339 --> node_1319
    node_416 --> node_614
    node_62 --> node_1302
    node_1182 --> node_1180
    node_1045 --> node_1354
    node_100 --> node_737
    node_1097 --> node_1092
    node_643 --> node_1322
    node_5 --> node_1286
    node_139 --> node_142
    node_1261 --> node_187
    node_1230 --> node_487
    node_103 --> node_1337
    node_1081 --> node_1260
    node_666 --> node_1318
    node_520 --> node_1308
    node_935 --> node_178
    node_666 --> node_1261
    node_1231 --> node_1298
    node_896 --> node_385
    node_1231 --> node_1218
    node_666 --> node_1272
    node_497 --> node_1197
    node_5 --> node_352
    node_861 --> node_48
    node_541 --> node_334
    node_1359 --> node_1083
    node_1231 --> node_1363
    node_964 --> node_1010
    node_56 --> node_1251
    node_20 --> node_911
    node_1117 --> node_1101
    node_1175 --> node_1179
    node_64 --> node_667
    node_489 --> node_739
    node_853 --> node_413
    node_103 --> node_766
    node_85 --> node_83
    node_733 --> node_332
    node_934 --> node_1238
    node_781 --> node_37
    node_795 --> node_788
    node_525 --> node_1088
    node_795 --> node_35
    node_541 --> node_719
    node_520 --> node_720
    node_31 --> node_628
    node_1097 --> node_1236
    node_1330 --> node_1008
    node_1260 --> node_1288
    node_629 --> node_1109
    node_492 --> node_188
    node_1046 --> node_1054
    node_0 --> node_1205
    node_470 --> node_400
    node_187 --> node_423
    node_276 --> node_282
    node_599 --> node_98
    node_1165 --> node_1047
    node_840 --> node_242
    node_103 --> node_943
    node_0 --> node_1146
    node_100 --> node_614
    node_209 --> node_336
    node_781 --> node_784
    node_1117 --> node_1002
    node_1231 --> node_1198
    node_64 --> node_122
    node_79 --> node_336
    node_575 --> node_746
    node_665 --> node_1112
    node_543 --> node_638
    node_1361 --> node_1350
    node_911 --> node_1260
    node_263 --> node_450
    node_5 --> node_421
    node_1153 --> node_1151
    node_1097 --> node_1133
    node_461 --> node_379
    node_31 --> node_954
    node_595 --> node_564
    node_187 --> node_210
    node_1117 --> node_1260
    node_541 --> node_488
    node_132 --> node_69
    node_31 --> node_606
    node_1103 --> node_1350
    node_5 --> node_417
    node_497 --> node_1021
    node_103 --> node_975
    node_928 --> node_995
    node_1038 --> node_1047
    node_127 --> node_72
    node_490 --> node_533
    node_772 --> node_650
    node_489 --> node_1289
    node_525 --> node_1227
    node_5 --> node_828
    node_520 --> node_1339
    node_1267 --> node_183
    node_769 --> node_187
    node_1117 --> node_423
    node_1314 --> node_1236
    node_489 --> node_208
    node_3 --> node_961
    node_5 --> node_33
    node_960 --> node_951
    node_164 --> node_245
    node_5 --> node_1027
    node_187 --> node_356
    node_541 --> node_487
    node_556 --> node_947
    node_68 --> node_122
    node_497 --> node_601
    node_962 --> node_951
    node_601 --> node_638
    node_475 --> node_1148
    node_1162 --> node_57
    node_647 --> node_1116
    node_666 --> node_1260
    node_1133 --> node_1129
    node_63 --> node_37
    node_1077 --> node_1046
    node_541 --> node_620
    node_541 --> node_1140
    node_1339 --> node_1035
    node_667 --> node_662
    node_520 --> node_1220
    node_445 --> node_248
    node_541 --> node_1041
    node_1117 --> node_210
    node_652 --> node_1009
    node_35 --> node_426
    node_251 --> node_739
    node_497 --> node_1308
    node_1314 --> node_1230
    node_742 --> node_1085
    node_1230 --> node_1173
    node_1314 --> node_1133
    node_490 --> node_529
    node_100 --> node_1213
    node_599 --> node_307
    node_20 --> node_617
    node_0 --> node_1092
    node_549 --> node_26
    node_521 --> node_680
    node_5 --> node_275
    node_100 --> node_31
    node_520 --> node_1147
    node_472 --> node_261
    node_520 --> node_48
    node_63 --> node_784
    node_127 --> node_233
    node_521 --> node_739
    node_1230 --> node_1257
    node_897 --> node_349
    node_1339 --> node_1125
    node_1041 --> node_247
    node_5 --> node_1357
    node_533 --> node_320
    node_559 --> node_1313
    node_58 --> node_739
    node_593 --> node_307
    node_187 --> node_227
    node_631 --> node_653
    node_508 --> node_574
    node_541 --> node_948
    node_1097 --> node_1299
    node_497 --> node_629
    node_1357 --> node_993
    node_575 --> node_1135
    node_497 --> node_720
    node_658 --> node_1245
    node_1261 --> node_35
    node_5 --> node_422
    node_31 --> node_33
    node_489 --> node_280
    node_624 --> node_175
    node_710 --> node_695
    node_1231 --> node_1066
    node_666 --> node_1264
    node_976 --> node_241
    node_103 --> node_960
    node_661 --> node_1011
    node_599 --> node_911
    node_520 --> node_1065
    node_632 --> node_1236
    node_920 --> node_35
    node_0 --> node_1236
    node_50 --> node_137
    node_912 --> node_410
    node_497 --> node_641
    node_1147 --> node_1083
    node_5 --> node_1020
    node_459 --> node_1260
    node_195 --> node_1260
    node_895 --> node_1295
    node_808 --> node_375
    node_687 --> node_487
    node_781 --> node_620
    node_19 --> node_1262
    node_1117 --> node_227
    node_5 --> node_201
    node_103 --> node_486
    node_179 --> node_221
    node_334 --> node_339
    node_556 --> node_135
    node_1260 --> node_406
    node_665 --> node_1305
    node_1097 --> node_1218
    node_1359 --> node_332
    node_1015 --> node_1014
    node_64 --> node_720
    node_68 --> node_64
    node_632 --> node_1133
    node_1314 --> node_1299
    node_0 --> node_1133
    node_497 --> node_1339
    node_104 --> node_533
    node_520 --> node_1314
    node_1201 --> node_1199
    node_1231 --> node_1157
    node_500 --> node_5
    node_652 --> node_1010
    node_700 --> node_704
    node_1053 --> node_1047
    node_972 --> node_1354
    node_772 --> node_746
    node_154 --> node_1302
    node_840 --> node_849
    node_751 --> node_969
    node_636 --> node_3
    node_866 --> node_331
    node_99 --> node_177
    node_511 --> node_52
    node_541 --> node_1173
    node_63 --> node_488
    node_5 --> node_1081
    node_1339 --> node_1335
    node_497 --> node_1220
    node_662 --> node_1239
    node_5 --> node_893
    node_665 --> node_1005
    node_497 --> node_1121
    node_847 --> node_221
    node_31 --> node_68
    node_497 --> node_795
    node_541 --> node_20
    node_711 --> node_15
    node_497 --> node_1147
    node_1045 --> node_1261
    node_497 --> node_48
    node_5 --> node_1194
    node_620 --> node_619
    node_1097 --> node_1198
    node_497 --> node_842
    node_1339 --> node_1037
    node_193 --> node_327
    node_534 --> node_626
    node_1070 --> node_985
    node_1230 --> node_1195
    node_500 --> node_210
    node_541 --> node_642
    node_528 --> node_585
    node_559 --> node_50
    node_769 --> node_35
    node_205 --> node_363
    node_497 --> node_648
    node_63 --> node_620
    node_851 --> node_32
    node_187 --> node_283
    node_1359 --> node_238
    node_20 --> node_650
    node_5 --> node_563
    node_662 --> node_973
    node_541 --> node_651
    node_935 --> node_1129
    node_997 --> node_988
    node_1231 --> node_1093
    node_712 --> node_1082
    node_599 --> node_617
    node_877 --> node_367
    node_416 --> node_911
    node_5 --> node_476
    node_145 --> node_681
    node_449 --> node_1021
    node_632 --> node_1299
    node_398 --> node_257
    node_486 --> node_238
    node_1275 --> node_415
    node_461 --> node_352
    node_232 --> node_233
    node_64 --> node_48
    node_1230 --> node_1015
    node_205 --> node_414
    node_534 --> node_1203
    node_559 --> node_1046
    node_1022 --> node_1047
    node_1339 --> node_1185
    node_801 --> node_408
    node_1147 --> node_221
    node_1183 --> node_1047
    node_19 --> node_739
    node_511 --> node_251
    node_525 --> node_1125
    node_1117 --> node_977
    node_20 --> node_969
    node_146 --> node_20
    node_328 --> node_739
    node_1230 --> node_1300
    node_746 --> node_3
    node_124 --> node_58
    node_541 --> node_689
    node_541 --> node_219
    node_499 --> node_1082
    node_511 --> node_246
    node_781 --> node_20
    node_106 --> node_677
    node_52 --> node_250
    node_541 --> node_605
    node_666 --> node_1165
    node_564 --> node_669
    node_751 --> node_1170
    node_252 --> node_210
    node_665 --> node_1118
    node_1185 --> node_1301
    node_1162 --> node_1085
    node_489 --> node_425
    node_505 --> node_183
    node_1231 --> node_1140
    node_345 --> node_260
    node_5 --> node_1239
    node_0 --> node_1218
    node_1314 --> node_1186
    node_105 --> node_69
    node_1231 --> node_1041
    node_886 --> node_210
    node_497 --> node_1254
    node_525 --> node_1305
    node_699 --> node_695
    node_934 --> node_1182
    node_1339 --> node_1309
    node_357 --> node_264
    node_541 --> node_12
    node_911 --> node_585
    node_37 --> node_33
    node_541 --> node_1156
    node_531 --> node_1148
    node_1230 --> node_1267
    node_246 --> node_247
    node_525 --> node_1188
    node_205 --> node_420
    node_115 --> node_546
    node_457 --> node_1148
    node_31 --> node_1337
    node_629 --> node_1106
    node_625 --> node_1234
    node_191 --> node_250
    node_370 --> node_209
    node_525 --> node_1005
    node_19 --> node_208
    node_525 --> node_1023
    node_541 --> node_306
    node_533 --> node_607
    node_5 --> node_1273
    node_5 --> node_1362
    node_837 --> node_327
    node_632 --> node_1198
    node_486 --> node_1078
    node_449 --> node_1095
    node_520 --> node_695
    node_520 --> node_1060
    node_0 --> node_1198
    node_19 --> node_399
    node_5 --> node_393
    node_666 --> node_1225
    node_387 --> node_210
    node_537 --> node_1139
    node_774 --> node_349
    node_862 --> node_1284
    node_674 --> node_1325
    node_1231 --> node_1214
    node_1231 --> node_1314
    node_1083 --> node_187
    node_735 --> node_49
    node_525 --> node_1200
    node_490 --> node_506
    node_106 --> node_954
    node_665 --> node_1332
    node_253 --> node_247
    node_1102 --> node_35
    node_171 --> node_69
    node_100 --> node_177
    node_31 --> node_540
    node_541 --> node_1015
    node_1015 --> node_1008
    node_31 --> node_742
    node_803 --> node_419
    node_5 --> node_702
    node_525 --> node_1341
    node_629 --> node_1110
    node_20 --> node_1170
    node_1230 --> node_1024
    node_489 --> node_588
    node_63 --> node_142
    node_718 --> node_704
    node_1230 --> node_1098
    node_502 --> node_221
    node_1083 --> node_57
    node_689 --> node_702
    node_1173 --> node_1047
    node_526 --> node_72
    node_1260 --> node_1294
    node_599 --> node_253
    node_1117 --> node_789
    node_913 --> node_1082
    node_361 --> node_741
    node_457 --> node_695
    node_1230 --> node_1169
    node_452 --> node_209
    node_682 --> node_683
    node_179 --> node_1285
    node_507 --> node_1128
    node_497 --> node_647
    node_861 --> node_681
    node_449 --> node_795
    node_656 --> node_1015
    node_145 --> node_711
    node_836 --> node_1285
    node_490 --> node_50
    node_525 --> node_178
    node_1117 --> node_194
    node_1319 --> node_1316
    node_31 --> node_975
    node_520 --> node_1034
    node_575 --> node_1043
    node_489 --> node_394
    node_519 --> node_695
    node_1230 --> node_1212
    node_1314 --> node_1326
    node_489 --> node_392
    node_48 --> node_47
    node_497 --> node_244
    node_145 --> node_730
    node_5 --> node_526
    node_507 --> node_517
    node_489 --> node_363
    node_5 --> node_1184
    node_99 --> node_969
    node_525 --> node_1118
    node_585 --> node_176
    node_639 --> node_656
    node_1339 --> node_1324
    node_1081 --> node_249
    node_1230 --> node_1143
    node_497 --> node_625
    node_934 --> node_1233
    node_1041 --> node_36
    node_854 --> node_298
    node_526 --> node_233
    node_1155 --> node_62
    node_972 --> node_1261
    node_179 --> node_405
    node_534 --> node_12
    node_575 --> node_997
    node_1360 --> node_697
    node_541 --> node_1232
    node_12 --> node_627
    node_102 --> node_1346
    node_497 --> node_1309
    node_666 --> node_1226
    node_666 --> node_1219
    node_935 --> node_1067
    node_1117 --> node_441
    node_229 --> node_1148
    node_145 --> node_966
    node_675 --> node_176
    node_5 --> node_1155
    node_205 --> node_403
    node_710 --> node_1260
    node_520 --> node_1045
    node_520 --> node_1036
    node_5 --> node_1270
    node_662 --> node_1237
    node_1316 --> node_1047
    node_1097 --> node_1140
    node_790 --> node_1148
    node_639 --> node_663
    node_654 --> node_176
    node_758 --> node_757
    node_541 --> node_1098
    node_416 --> node_650
    node_541 --> node_179
    node_1061 --> node_188
    node_229 --> node_1354
    node_105 --> node_50
    node_632 --> node_1326
    node_666 --> node_1120
    node_525 --> node_1332
    node_395 --> node_260
    node_666 --> node_1221
    node_923 --> node_57
    node_449 --> node_1254
    node_31 --> node_960
    node_1081 --> node_247
    node_1327 --> node_1326
    node_187 --> node_1290
    node_541 --> node_1201
    node_5 --> node_768
    node_520 --> node_1349
    node_1261 --> node_1262
    node_599 --> node_746
    node_229 --> node_695
    node_751 --> node_962
    node_1362 --> node_1313
    node_840 --> node_236
    node_19 --> node_398
    node_697 --> node_175
    node_603 --> node_922
    node_106 --> node_68
    node_5 --> node_1292
    node_1231 --> node_1060
    node_5 --> node_360
    node_525 --> node_1230
    node_416 --> node_969
    node_1117 --> node_186
    node_1339 --> node_1325
    node_1219 --> node_1222
    node_1231 --> node_1156
    node_5 --> node_72
    node_629 --> node_1104
    node_1230 --> node_1329
    node_125 --> node_129
    node_100 --> node_130
    node_1231 --> node_1122
    node_665 --> node_1359
    node_5 --> node_1097
    node_906 --> node_383
    node_781 --> node_681
    node_783 --> node_1082
    node_489 --> node_411
    node_861 --> node_711
    node_543 --> node_209
    node_179 --> node_410
    node_772 --> node_1043
    node_514 --> node_203
    node_1081 --> node_1082
    node_5 --> node_1153
    node_520 --> node_1141
    node_1339 --> node_1336
    node_103 --> node_1003
    node_861 --> node_730
    node_1117 --> node_247
    node_1231 --> node_1356
    node_19 --> node_1287
    node_662 --> node_1235
    node_127 --> node_328
    node_229 --> node_198
    node_5 --> node_233
    node_541 --> node_1291
    node_1267 --> node_1313
    node_1195 --> node_1193
    node_280 --> node_183
    node_72 --> node_74
    node_187 --> node_205
    node_1314 --> node_1027
    node_50 --> node_164
    node_208 --> node_739
    node_1097 --> node_1173
    node_37 --> node_741
    node_497 --> node_1154
    node_1339 --> node_1094
    node_1230 --> node_1223
    node_5 --> node_304
    node_525 --> node_1324
    node_541 --> node_187
    node_772 --> node_997
    node_100 --> node_969
    node_666 --> node_1018
    node_1231 --> node_1192
    node_37 --> node_203
    node_1083 --> node_1085
    node_541 --> node_1323
    node_96 --> node_241
    node_639 --> node_643
    node_579 --> node_580
    node_606 --> node_605
    node_1097 --> node_1257
    node_1324 --> node_1321
    node_0 --> node_1140
    node_526 --> node_346
    node_1117 --> node_317
    node_449 --> node_244
    node_494 --> node_276
    node_5 --> node_1342
    node_497 --> node_1349
    node_1211 --> node_1210
    node_205 --> node_1286
    node_458 --> node_187
    node_911 --> node_805
    node_416 --> node_1170
    node_1359 --> node_488
    node_541 --> node_57
    node_63 --> node_681
    node_1231 --> node_1340
    node_1117 --> node_205
    node_549 --> node_33
    node_113 --> node_120
    node_410 --> node_428
    node_563 --> node_653
    node_699 --> node_1260
    node_541 --> node_301
    node_676 --> node_675
    node_1117 --> node_1082
    node_1077 --> node_1354
    node_665 --> node_1149
    node_246 --> node_36
    node_187 --> node_292
    node_1127 --> node_81
    node_103 --> node_595
    node_486 --> node_488
    node_665 --> node_1330
    node_1231 --> node_1045
    node_1231 --> node_1036
    node_106 --> node_490
    node_106 --> node_1337
    node_31 --> node_51
    node_179 --> node_397
    node_871 --> node_12
    node_536 --> node_1047
    node_490 --> node_64
    node_1359 --> node_487
    node_19 --> node_400
    node_5 --> node_1352
    node_666 --> node_1227
    node_1314 --> node_1257
    node_866 --> node_81
    node_1231 --> node_1232
    node_541 --> node_533
    node_1230 --> node_1310
    node_1362 --> node_1046
    node_443 --> node_425
    node_649 --> node_187
    node_520 --> node_711
    node_840 --> node_427
    node_1314 --> node_1020
    node_267 --> node_210
    node_520 --> node_1260
    node_643 --> node_1062
    node_564 --> node_665
    node_64 --> node_681
    node_1339 --> node_1231
    node_62 --> node_741
    node_666 --> node_1082
    node_866 --> node_35
    node_497 --> node_1325
    node_5 --> node_1029
    node_106 --> node_766
    node_5 --> node_1235
    node_497 --> node_1318
    node_520 --> node_730
    node_520 --> node_1077
    node_253 --> node_36
    node_453 --> node_256
    node_900 --> node_354
    node_1041 --> node_1302
    node_19 --> node_392
    node_533 --> node_57
    node_449 --> node_29
    node_1339 --> node_1167
    node_665 --> node_1144
    node_541 --> node_1223
    node_876 --> node_1284
    node_106 --> node_943
    node_930 --> node_1015
    node_948 --> node_29
    node_1312 --> node_1083
    node_1097 --> node_1156
    node_205 --> node_417
    node_251 --> node_250
    node_923 --> node_1085
    node_599 --> node_780
    node_903 --> node_271
    node_507 --> node_313
    node_662 --> node_970
    node_68 --> node_6
    node_31 --> node_1047
    node_520 --> node_966
    node_457 --> node_1260
    node_19 --> node_382
    node_1230 --> node_1206
    node_5 --> node_522
    node_781 --> node_730
    node_632 --> node_1173
    node_1231 --> node_1201
    node_936 --> node_187
    node_0 --> node_1173
    node_575 --> node_606
    node_524 --> node_976
    node_106 --> node_975
    node_522 --> node_72
    node_1267 --> node_1046
    node_663 --> node_1320
    node_68 --> node_58
    node_146 --> node_533
    node_525 --> node_1186
    node_489 --> node_383
    node_781 --> node_533
    node_461 --> node_1270
    node_632 --> node_1257
    node_519 --> node_1260
    node_20 --> node_1043
    node_706 --> node_704
    node_229 --> node_1261
    node_5 --> node_1042
    node_459 --> node_1082
    node_5 --> node_1205
    node_195 --> node_1082
    node_489 --> node_1179
    node_99 --> node_962
    node_661 --> node_1013
    node_666 --> node_1289
    node_5 --> node_188
    node_1117 --> node_184
    node_5 --> node_1146
    node_5 --> node_493
    node_525 --> node_1353
    node_669 --> node_1070
    node_1097 --> node_1015
    node_1133 --> node_1131
    node_1296 --> node_200
    node_1045 --> node_249
    node_1230 --> node_1013
    node_541 --> node_1126
    node_449 --> node_622
    node_581 --> node_600
    node_1314 --> node_1195
    node_341 --> node_67
    node_992 --> node_1047
    node_665 --> node_1057
    node_445 --> node_245
    node_20 --> node_997
    node_5 --> node_1132
    node_559 --> node_1148
    node_599 --> node_29
    node_935 --> node_1062
    node_525 --> node_1330
    node_63 --> node_711
    node_520 --> node_1116
    node_541 --> node_1138
    node_359 --> node_243
    node_458 --> node_35
    node_331 --> node_332
    node_205 --> node_422
    node_5 --> node_1278
    node_526 --> node_381
    node_130 --> node_72
    node_997 --> node_982
    node_537 --> node_1252
    node_63 --> node_730
    node_845 --> node_363
    node_595 --> node_570
    node_665 --> node_1361
    node_1230 --> node_1313
    node_923 --> node_217
    node_1251 --> node_1249
    node_879 --> node_1294
    node_145 --> node_911
    node_1260 --> node_369
    node_1117 --> node_483
    node_935 --> node_1017
    node_1147 --> node_487
    node_12 --> node_665
    node_1230 --> node_1068
    node_1314 --> node_1015
    node_632 --> node_1331
    node_1231 --> node_1323
    node_497 --> node_631
    node_505 --> node_1313
    node_489 --> node_1286
    node_1230 --> node_1019
    node_559 --> node_1354
    node_525 --> node_1166
    node_5 --> node_1092
    node_1018 --> node_1047
    node_935 --> node_1239
    node_56 --> node_1161
    node_101 --> node_114
    node_649 --> node_35
    node_64 --> node_711
    node_122 --> node_57
    node_497 --> node_737
    node_19 --> node_411
    node_533 --> node_267
    node_1314 --> node_1300
    node_497 --> node_966
    node_413 --> node_1148
    node_541 --> node_138
    node_106 --> node_486
    node_861 --> node_98
    node_1230 --> node_1256
    node_541 --> node_1085
    node_559 --> node_695
    node_130 --> node_233
    node_64 --> node_730
    node_520 --> node_1123
    node_1066 --> node_1064
    node_0 --> node_1156
    node_229 --> node_1260
    node_594 --> node_3
    node_526 --> node_1294
    node_5 --> node_388
    node_205 --> node_396
    node_632 --> node_1195
    node_636 --> node_1183
    node_1052 --> node_1047
    node_661 --> node_1009
    node_666 --> node_1170
    node_5 --> node_385
    node_5 --> node_700
    node_99 --> node_241
    node_1226 --> node_1224
    node_1314 --> node_1267
    node_52 --> node_203
    node_5 --> node_1312
    node_525 --> node_1207
    node_643 --> node_1063
    node_352 --> node_403
    node_960 --> node_961
    node_520 --> node_1307
    node_106 --> node_102
    node_1097 --> node_1024
    node_772 --> node_606
    node_64 --> node_966
    node_838 --> node_183
    node_962 --> node_961
    node_543 --> node_72
    node_936 --> node_35
    node_101 --> node_241
    node_1097 --> node_1098
    node_1127 --> node_307
    node_585 --> node_178
    node_449 --> node_1261
    node_103 --> node_37
    node_101 --> node_731
    node_206 --> node_1149
    node_520 --> node_1069
    node_1077 --> node_1261
    node_1319 --> node_1317
    node_413 --> node_695
    node_599 --> node_1043
    node_500 --> node_456
    node_632 --> node_1015
    node_790 --> node_423
    node_246 --> node_1302
    node_1182 --> node_1047
    node_497 --> node_614
    node_0 --> node_1015
    node_1352 --> node_253
    node_455 --> node_187
    node_154 --> node_741
    node_866 --> node_307
    node_5 --> node_271
    node_541 --> node_1313
    node_533 --> node_1085
    node_1360 --> node_733
    node_23 --> node_243
    node_145 --> node_617
    node_751 --> node_334
    node_1185 --> node_1302
    node_525 --> node_1057
    node_893 --> node_219
    node_1023 --> node_1047
    node_520 --> node_1191
    node_520 --> node_1030
    node_656 --> node_1013
    node_632 --> node_1300
    node_647 --> node_1118
    node_5 --> node_238
    node_665 --> node_1303
    node_675 --> node_178
    node_102 --> node_1183
    node_100 --> node_962
    node_63 --> node_232
    node_599 --> node_997
    node_541 --> node_1019
    node_136 --> node_144
    node_997 --> node_983
    node_1314 --> node_1024
    node_1362 --> node_1228
    node_31 --> node_1003
    node_1097 --> node_1143
    node_543 --> node_233
    node_1242 --> node_67
    node_1314 --> node_1098
    node_666 --> node_1023
    node_253 --> node_1302
    node_1314 --> node_1184
    node_1330 --> node_1012
    node_563 --> node_695
    node_520 --> node_1225
    node_584 --> node_1275
    node_497 --> node_1327
    node_541 --> node_1256
    node_665 --> node_1106
    node_1314 --> node_1169
    node_774 --> node_279
    node_112 --> node_1047
    node_1230 --> node_1046
    node_661 --> node_1010
    node_599 --> node_52
    node_632 --> node_1267
    node_12 --> node_668
    node_19 --> node_1149
    node_126 --> node_69
    node_1117 --> node_425
    node_1145 --> node_1358
    node_489 --> node_275
    node_1312 --> node_238
    node_660 --> node_1208
    node_1231 --> node_1344
    node_1204 --> node_951
    node_911 --> node_809
    node_388 --> node_1278
    node_911 --> node_905
    node_1314 --> node_1212
    node_187 --> node_290
    node_653 --> node_1092
    node_101 --> node_328
    node_20 --> node_677
    node_0 --> node_1232
    node_5 --> node_731
    node_761 --> node_67
    node_1266 --> node_1358
    node_779 --> node_190
    node_1314 --> node_1143
    node_1035 --> node_1033
    node_185 --> node_205
    node_489 --> node_422
    node_68 --> node_99
    node_517 --> node_303
    node_1231 --> node_1126
    node_497 --> node_541
    node_599 --> node_250
    node_665 --> node_1110
    node_507 --> node_331
    node_497 --> node_1307
    node_524 --> node_33
    node_227 --> node_1280
    node_972 --> node_249
    node_753 --> node_3
    node_416 --> node_1043
    node_790 --> node_794
    node_561 --> node_27
    node_31 --> node_595
    node_205 --> node_1273
    node_5 --> node_1078
    node_1360 --> node_336
    node_840 --> node_968
    node_529 --> node_983
    node_664 --> node_1089
    node_632 --> node_1024
    node_506 --> node_1149
    node_19 --> node_383
    node_0 --> node_1024
    node_1117 --> node_290
    node_68 --> node_120
    node_541 --> node_50
    node_101 --> node_115
    node_632 --> node_1098
    node_910 --> node_390
    node_0 --> node_1098
    node_527 --> node_980
    node_888 --> node_364
    node_829 --> node_365
    node_142 --> node_52
    node_103 --> node_48
    node_5 --> node_1298
    node_497 --> node_1191
    node_497 --> node_1030
    node_525 --> node_1027
    node_7 --> node_733
    node_595 --> node_992
    node_632 --> node_1169
    node_911 --> node_899
    node_5 --> node_1218
    node_416 --> node_997
    node_449 --> node_737
    node_541 --> node_643
    node_520 --> node_1040
    node_541 --> node_671
    node_599 --> node_251
    node_960 --> node_958
    node_1231 --> node_1059
    node_772 --> node_68
    node_67 --> node_126
    node_205 --> node_407
    node_5 --> node_1363
    node_449 --> node_104
    node_1230 --> node_1026
    node_100 --> node_241
    node_599 --> node_246
    node_751 --> node_948
    node_1097 --> node_1329
    node_0 --> node_1201
    node_1015 --> node_1165
    node_490 --> node_543
    node_122 --> node_1085
    node_526 --> node_410
    node_520 --> node_1219
    node_520 --> node_1226
    node_575 --> node_742
    node_52 --> node_72
    node_19 --> node_356
    node_20 --> node_954
    node_102 --> node_1251
    node_666 --> node_1224
    node_1208 --> node_1047
    node_1206 --> node_1202
    node_682 --> node_690
    node_809 --> node_410
    node_779 --> node_180
    node_5 --> node_197
    node_710 --> node_1082
    node_5 --> node_328
    node_20 --> node_606
    node_861 --> node_617
    node_1230 --> node_1197
    node_455 --> node_35
    node_972 --> node_247
    node_632 --> node_1143
    node_1314 --> node_1097
    node_0 --> node_1143
    node_525 --> node_1357
    node_673 --> node_552
    node_599 --> node_5
    node_3 --> node_549
    node_520 --> node_911
    node_719 --> node_187
    node_1231 --> node_1069
    node_1339 --> node_1017
    node_5 --> node_1198
    node_559 --> node_1261
    node_227 --> node_197
    node_908 --> node_391
    node_67 --> node_117
    node_951 --> node_952
    node_599 --> node_697
    node_1030 --> node_1028
    node_1314 --> node_1329
    node_1167 --> node_1015
    node_489 --> node_563
    node_445 --> node_428
    node_449 --> node_614
    node_1097 --> node_1223
    node_1026 --> node_1025
    node_430 --> node_431
    node_142 --> node_251
    node_593 --> node_697
    node_642 --> node_1007
    node_543 --> node_188
    node_774 --> node_292
    node_525 --> node_1020
    node_142 --> node_246
    node_267 --> node_279
    node_1015 --> node_1016
    node_631 --> node_674
    node_595 --> node_603
    node_712 --> node_703
    node_1147 --> node_183
    node_1339 --> node_1301
    node_1339 --> node_1362
    node_682 --> node_3
    node_1081 --> node_191
    node_777 --> node_1262
    node_205 --> node_1270
    node_842 --> node_675
    node_187 --> node_420
    node_687 --> node_1046
    node_520 --> node_1211
    node_629 --> node_1115
    node_187 --> node_235
    node_497 --> node_1040
    node_99 --> node_334
    node_209 --> node_219
    node_500 --> node_290
    node_1314 --> node_1223
    node_525 --> node_1081
    node_665 --> node_1104
    node_423 --> node_425
    node_891 --> node_265
    node_5 --> node_412
    node_527 --> node_72
    node_687 --> node_1078
    node_23 --> node_22
    node_541 --> node_305
    node_497 --> node_1219
    node_857 --> node_414
    node_31 --> node_229
    node_1230 --> node_1308
    node_449 --> node_1213
    node_196 --> node_201
    node_19 --> node_200
    node_541 --> node_1197
    node_449 --> node_31
    node_1339 --> node_1087
    node_103 --> node_20
    node_1097 --> node_1310
    node_525 --> node_1194
    node_1097 --> node_1126
    node_654 --> node_1043
    node_632 --> node_1329
    node_520 --> node_617
    node_222 --> node_243
    node_1076 --> node_1047
    node_0 --> node_1329
    node_559 --> node_1260
    node_866 --> node_739
    node_773 --> node_695
    node_522 --> node_731
    node_661 --> node_1014
    node_5 --> node_1066
    node_5 --> node_505
    node_884 --> node_187
    node_575 --> node_960
    node_145 --> node_746
    node_650 --> node_643
    node_116 --> node_69
    node_497 --> node_911
    node_818 --> node_370
    node_489 --> node_268
    node_238 --> node_82
    node_905 --> node_397
    node_1260 --> node_1272
    node_666 --> node_1171
    node_1314 --> node_1235
    node_772 --> node_742
    node_489 --> node_1273
    node_520 --> node_1088
    node_209 --> node_306
    node_527 --> node_233
    node_710 --> node_712
    node_665 --> node_1004
    node_599 --> node_606
    node_568 --> node_32
    node_930 --> node_1013
    node_179 --> node_1291
    node_20 --> node_68
    node_1230 --> node_1228
    node_1057 --> node_991
    node_662 --> node_1238
    node_1314 --> node_1310
    node_5 --> node_1157
    node_5 --> node_527
    node_249 --> node_247
    node_564 --> node_12
    node_413 --> node_1260
    node_1362 --> node_1354
    node_893 --> node_187
    node_19 --> node_275
    node_499 --> node_33
    node_416 --> node_677
    node_699 --> node_1082
    node_632 --> node_1223
    node_541 --> node_1021
    node_0 --> node_1223
    node_719 --> node_35
    node_64 --> node_911
    node_487 --> node_187
    node_406 --> node_26
    node_301 --> node_290
    node_785 --> node_187
    node_130 --> node_731
    node_772 --> node_975
    node_625 --> node_1236
    node_1230 --> node_1339
    node_1336 --> node_1333
    node_599 --> node_27
    node_599 --> node_1213
    node_520 --> node_1227
    node_31 --> node_37
    node_541 --> node_601
    node_522 --> node_197
    node_525 --> node_1239
    node_599 --> node_31
    node_751 --> node_490
    node_631 --> node_662
    node_831 --> node_187
    node_522 --> node_328
    node_1206 --> node_759
    node_1081 --> node_251
    node_647 --> node_1109
    node_541 --> node_64
    node_657 --> node_1052
    node_541 --> node_1308
    node_56 --> node_82
    node_1314 --> node_1042
    node_709 --> node_1148
    node_391 --> node_197
    node_1230 --> node_1220
    node_63 --> node_139
    node_563 --> node_1260
    node_1097 --> node_1013
    node_31 --> node_784
    node_99 --> node_948
    node_957 --> node_952
    node_1314 --> node_1206
    node_497 --> node_1301
    node_5 --> node_391
    node_541 --> node_1319
    node_5 --> node_1093
    node_1230 --> node_1147
    node_751 --> node_766
    node_508 --> node_1328
    node_840 --> node_789
    node_7 --> node_51
    node_1267 --> node_1354
    node_1324 --> node_1322
    node_815 --> node_187
    node_1015 --> node_1012
    node_1359 --> node_330
    node_663 --> node_1299
    node_227 --> node_391
    node_600 --> node_964
    node_251 --> node_203
    node_500 --> node_241
    node_632 --> node_1310
    node_541 --> node_720
    node_0 --> node_1126
    node_416 --> node_954
    node_563 --> node_631
    node_364 --> node_977
    node_229 --> node_249
    node_5 --> node_488
    node_5 --> node_884
    node_330 --> node_332
    node_416 --> node_606
    node_751 --> node_943
    node_1267 --> node_695
    node_520 --> node_650
    node_497 --> node_1087
    node_100 --> node_334
    node_1097 --> node_1068
    node_457 --> node_1082
    node_1231 --> node_1211
    node_130 --> node_328
    node_334 --> node_739
    node_1145 --> node_1144
    node_106 --> node_595
    node_1314 --> node_1013
    node_541 --> node_1095
    node_1097 --> node_1019
    node_943 --> node_940
    node_914 --> node_401
    node_709 --> node_695
    node_877 --> node_1275
    node_64 --> node_617
    node_1230 --> node_1065
    node_146 --> node_64
    node_1304 --> node_1350
    node_1083 --> node_1148
    node_772 --> node_960
    node_476 --> node_35
    node_104 --> node_58
    node_861 --> node_746
    node_656 --> node_1014
    node_72 --> node_241
    node_892 --> node_607
    node_884 --> node_35
    node_1015 --> node_1346
    node_1117 --> node_1149
    node_519 --> node_1082
    node_5 --> node_1140
    node_20 --> node_1337
    node_1097 --> node_1256
    node_1312 --> node_488
    node_5 --> node_1041
    node_658 --> node_1252
    node_541 --> node_1339
    node_955 --> node_952
    node_996 --> node_1047
    node_1231 --> node_1006
    node_840 --> node_441
    node_1015 --> node_1018
    node_632 --> node_1206
    node_330 --> node_82
    node_7 --> node_1047
    node_922 --> node_1221
    node_497 --> node_1227
    node_1293 --> node_415
    node_1314 --> node_1068
    node_4 --> node_64
    node_282 --> node_231
    node_948 --> node_946
    node_1312 --> node_487
    node_1300 --> node_250
    node_581 --> node_840
    node_541 --> node_1220
    node_1314 --> node_1019
    node_813 --> node_408
    node_229 --> node_247
    node_489 --> node_1284
    node_699 --> node_712
    node_541 --> node_1121
    node_20 --> node_742
    node_525 --> node_1184
    node_511 --> node_238
    node_1231 --> node_1174
    node_489 --> node_360
    node_541 --> node_795
    node_246 --> node_248
    node_585 --> node_628
    node_1231 --> node_1031
    node_1314 --> node_1312
    node_64 --> node_143
    node_541 --> node_1147
    node_489 --> node_72
    node_487 --> node_35
    node_1314 --> node_1256
    node_1083 --> node_695
    node_440 --> node_425
    node_5 --> node_1214
    node_1080 --> node_1047
    node_5 --> node_1314
    node_499 --> node_563
    node_20 --> node_943
    node_781 --> node_1095
    node_67 --> node_72
    node_158 --> node_69
    node_209 --> node_193
    node_31 --> node_620
    node_106 --> node_113
    node_935 --> node_1236
    node_1041 --> node_741
    node_497 --> node_630
    node_632 --> node_1013
    node_525 --> node_1212
    node_1042 --> node_1121
    node_1339 --> node_1342
    node_525 --> node_1155
    node_843 --> node_389
    node_831 --> node_35
    node_52 --> node_82
    node_301 --> node_310
    node_1042 --> node_1119
    node_235 --> node_268
    node_666 --> node_1166
    node_20 --> node_975
    node_429 --> node_428
    node_205 --> node_346
    node_497 --> node_650
    node_935 --> node_1133
    node_63 --> node_253
    node_1066 --> node_1067
    node_449 --> node_177
    node_430 --> node_1
    node_541 --> node_568
    node_524 --> node_934
    node_102 --> node_145
    node_103 --> node_681
    node_187 --> node_1286
    node_56 --> node_1162
    node_106 --> node_667
    node_1339 --> node_1352
    node_229 --> node_1082
    node_520 --> node_746
    node_449 --> node_249
    node_520 --> node_1035
    node_1351 --> node_1358
    node_100 --> node_948
    node_751 --> node_486
    node_209 --> node_273
    node_187 --> node_222
    node_1339 --> node_1117
    node_632 --> node_1068
    node_1077 --> node_249
    node_67 --> node_233
    node_678 --> node_241
    node_815 --> node_35
    node_192 --> node_196
    node_632 --> node_1019
    node_0 --> node_1019
    node_678 --> node_731
    node_507 --> node_81
    node_33 --> node_950
    node_659 --> node_1234
    node_416 --> node_68
    node_958 --> node_952
    node_497 --> node_969
    node_56 --> node_115
    node_378 --> node_215
    node_631 --> node_636
    node_511 --> node_1078
    node_520 --> node_1125
    node_63 --> node_1095
    node_632 --> node_1256
    node_705 --> node_1148
    node_0 --> node_1256
    node_1362 --> node_1261
    node_541 --> node_1254
    node_502 --> node_57
    node_781 --> node_746
    node_333 --> node_67
    node_106 --> node_326
    node_147 --> node_20
    node_855 --> node_700
    node_1102 --> node_250
    node_1359 --> node_1313
    node_1294 --> node_1047
    node_1117 --> node_222
    node_99 --> node_490
    node_31 --> node_645
    node_697 --> node_698
    node_520 --> node_1305
    node_52 --> node_731
    node_332 --> node_9
    node_657 --> node_1311
    node_1231 --> node_1319
    node_482 --> node_484
    node_773 --> node_1260
    node_179 --> node_419
    node_209 --> node_301
    node_486 --> node_1313
    node_525 --> node_1097
    node_58 --> node_72
    node_708 --> node_187
    node_1230 --> node_1354
    node_541 --> node_985
    node_20 --> node_960
    node_1045 --> node_52
    node_412 --> node_260
    node_449 --> node_247
    node_666 --> node_1286
    node_1189 --> node_995
    node_205 --> node_385
    node_599 --> node_177
    node_352 --> node_443
    node_99 --> node_766
    node_525 --> node_1153
    node_802 --> node_398
    node_179 --> node_1283
    node_31 --> node_983
    node_599 --> node_742
    node_520 --> node_1005
    node_520 --> node_1023
    node_874 --> node_357
    node_20 --> node_486
    node_642 --> node_1234
    node_152 --> node_82
    node_526 --> node_1269
    node_656 --> node_1008
    node_665 --> node_1360
    node_705 --> node_695
    node_678 --> node_328
    node_1097 --> node_1026
    node_1145 --> node_1303
    node_541 --> node_1037
    node_124 --> node_241
    node_31 --> node_642
    node_599 --> node_733
    node_249 --> node_36
    node_860 --> node_1294
    node_1101 --> node_1350
    node_99 --> node_943
    node_770 --> node_1262
    node_5 --> node_1296
    node_113 --> node_114
    node_58 --> node_233
    node_267 --> node_426
    node_63 --> node_746
    node_56 --> node_1259
    node_44 --> node_137
    node_878 --> node_366
    node_145 --> node_1043
    node_139 --> node_58
    node_828 --> node_272
    node_1097 --> node_1197
    node_497 --> node_1170
    node_520 --> node_1341
    node_593 --> node_733
    node_5 --> node_12
    node_5 --> node_1060
    node_1266 --> node_1303
    node_647 --> node_1106
    node_541 --> node_1148
    node_5 --> node_1156
    node_489 --> node_207
    node_665 --> node_1146
    node_845 --> node_1273
    node_52 --> node_328
    node_517 --> node_530
    node_1241 --> node_604
    node_520 --> node_425
    node_5 --> node_1122
    node_145 --> node_997
    node_1122 --> node_1120
    node_1314 --> node_1026
    node_19 --> node_1281
    node_416 --> node_1337
    node_934 --> node_1007
    node_103 --> node_711
    node_1185 --> node_1300
    node_1231 --> node_1121
    node_1045 --> node_251
    node_31 --> node_607
    node_541 --> node_244
    node_643 --> node_1066
    node_861 --> node_29
    node_1167 --> node_1013
    node_541 --> node_331
    node_5 --> node_306
    node_1230 --> node_1034
    node_520 --> node_178
    node_5 --> node_864
    node_1317 --> node_1047
    node_1045 --> node_246
    node_64 --> node_746
    node_187 --> node_422
    node_67 --> node_600
    node_103 --> node_730
    node_497 --> node_1305
    node_530 --> node_81
    node_575 --> node_1003
    node_104 --> node_120
    node_246 --> node_741
    node_106 --> node_720
    node_179 --> node_1274
    node_647 --> node_1110
    node_541 --> node_1354
    node_1013 --> node_1014
    node_520 --> node_1118
    node_502 --> node_267
    node_489 --> node_346
    node_5 --> node_1356
    node_601 --> node_629
    node_537 --> node_1163
    node_1189 --> node_1187
    node_1231 --> node_1035
    node_449 --> node_650
    node_520 --> node_1185
    node_31 --> node_12
    node_316 --> node_72
    node_405 --> node_264
    node_497 --> node_1188
    node_559 --> node_249
    node_541 --> node_1309
    node_525 --> node_1029
    node_281 --> node_345
    node_541 --> node_695
    node_490 --> node_499
    node_525 --> node_1235
    node_930 --> node_1014
    node_798 --> node_204
    node_5 --> node_1192
    node_497 --> node_1005
    node_1267 --> node_1260
    node_86 --> node_84
    node_541 --> node_589
    node_599 --> node_336
    node_497 --> node_1023
    node_649 --> node_1148
    node_1147 --> node_1313
    node_627 --> node_1186
    node_416 --> node_943
    node_1145 --> node_1265
    node_253 --> node_741
    node_534 --> node_67
    node_68 --> node_105
    node_205 --> node_1294
    node_709 --> node_1260
    node_892 --> node_187
    node_100 --> node_490
    node_1331 --> node_1234
    node_599 --> node_960
    node_1256 --> node_1047
    node_1339 --> node_1236
    node_497 --> node_1200
    node_1097 --> node_1308
    node_449 --> node_969
    node_593 --> node_336
    node_187 --> node_396
    node_564 --> node_652
    node_489 --> node_245
    node_954 --> node_952
    node_5 --> node_1340
    node_632 --> node_1026
    node_781 --> node_244
    node_416 --> node_975
    node_1266 --> node_1265
    node_316 --> node_233
    node_497 --> node_1341
    node_575 --> node_1072
    node_500 --> node_474
    node_99 --> node_486
    node_527 --> node_328
    node_187 --> node_209
    node_12 --> node_655
    node_1019 --> node_1018
    node_1339 --> node_1133
    node_477 --> node_383
    node_5 --> node_1045
    node_668 --> node_1136
    node_520 --> node_1332
    node_5 --> node_1036
    node_205 --> node_1285
    node_100 --> node_766
    node_774 --> node_272
    node_499 --> node_72
    node_1314 --> node_1066
    node_316 --> node_265
    node_972 --> node_191
    node_502 --> node_1085
    node_632 --> node_1197
    node_0 --> node_1197
    node_1230 --> node_1349
    node_687 --> node_1354
    node_751 --> node_1138
    node_936 --> node_1148
    node_106 --> node_48
    node_507 --> node_307
    node_14 --> node_198
    node_525 --> node_1042
    node_525 --> node_1205
    node_809 --> node_1291
    node_5 --> node_1232
    node_666 --> node_1020
    node_332 --> node_335
    node_525 --> node_1146
    node_642 --> node_1016
    node_58 --> node_600
    node_663 --> node_1027
    node_840 --> node_483
    node_861 --> node_1043
    node_496 --> node_33
    node_1083 --> node_1260
    node_541 --> node_675
    node_868 --> node_381
    node_1103 --> node_1047
    node_497 --> node_1118
    node_525 --> node_1132
    node_526 --> node_316
    node_1088 --> node_1086
    node_1231 --> node_1335
    node_478 --> node_187
    node_543 --> node_676
    node_742 --> node_247
    node_499 --> node_233
    node_861 --> node_997
    node_1097 --> node_1339
    node_666 --> node_1081
    node_514 --> node_607
    node_629 --> node_1114
    node_697 --> node_696
    node_1081 --> node_1080
    node_825 --> node_343
    node_1230 --> node_1318
    node_1230 --> node_1141
    node_629 --> node_1100
    node_665 --> node_1115
    node_1231 --> node_1037
    node_56 --> node_1176
    node_666 --> node_1265
    node_489 --> node_271
    node_416 --> node_960
    node_449 --> node_1170
    node_772 --> node_1003
    node_666 --> node_1194
    node_167 --> node_70
    node_559 --> node_1082
    node_5 --> node_1201
    node_1339 --> node_1299
    node_511 --> node_488
    node_406 --> node_33
    node_826 --> node_277
    node_564 --> node_656
    node_563 --> node_662
    node_541 --> node_1154
    node_1204 --> node_961
    node_205 --> node_1275
    node_179 --> node_1262
    node_1097 --> node_1220
    node_468 --> node_1148
    node_647 --> node_1104
    node_695 --> node_72
    node_1097 --> node_1121
    node_487 --> node_1262
    node_505 --> node_1261
    node_525 --> node_1092
    node_1267 --> node_232
    node_416 --> node_486
    node_1280 --> node_197
    node_666 --> node_1076
    node_68 --> node_56
    node_1097 --> node_1147
    node_643 --> node_1065
    node_520 --> node_1324
    node_423 --> node_445
    node_540 --> node_552
    node_1147 --> node_1046
    node_1081 --> node_741
    node_632 --> node_1308
    node_209 --> node_217
    node_595 --> node_601
    node_0 --> node_1308
    node_541 --> node_308
    node_31 --> node_681
    node_249 --> node_1302
    node_1081 --> node_203
    node_1314 --> node_1093
    node_541 --> node_1349
    node_497 --> node_1332
    node_704 --> node_187
    node_339 --> node_67
    node_599 --> node_51
    node_666 --> node_1195
    node_665 --> node_1190
    node_20 --> node_600
    node_1076 --> node_1099
    node_600 --> node_593
    node_561 --> node_649
    node_1156 --> node_571
    node_0 --> node_1319
    node_105 --> node_74
    node_1339 --> node_1218
    node_743 --> node_241
    node_543 --> node_983
    node_892 --> node_35
    node_66 --> node_58
    node_187 --> node_1273
    node_5 --> node_345
    node_972 --> node_251
    node_413 --> node_1082
    node_133 --> node_114
    node_520 --> node_1043
    node_1314 --> node_1220
    node_151 --> node_739
    node_1162 --> node_1158
    node_695 --> node_233
    node_958 --> node_951
    node_525 --> node_1312
    node_238 --> node_240
    node_892 --> node_267
    node_564 --> node_663
    node_489 --> node_1280
    node_943 --> node_936
    node_497 --> node_1230
    node_772 --> node_595
    node_209 --> node_302
    node_468 --> node_695
    node_489 --> node_731
    node_103 --> node_547
    node_930 --> node_1008
    node_195 --> node_209
    node_537 --> node_1251
    node_903 --> node_267
    node_1314 --> node_1147
    node_449 --> node_36
    node_575 --> node_229
    node_636 --> node_1345
    node_253 --> node_72
    node_406 --> node_260
    node_935 --> node_1238
    node_1231 --> node_1309
    node_489 --> node_196
    node_976 --> node_327
    node_530 --> node_307
    node_666 --> node_1239
    node_520 --> node_997
    node_205 --> node_410
    node_541 --> node_1325
    node_642 --> node_1017
    node_861 --> node_732
    node_5 --> node_187
    node_665 --> node_1363
    node_666 --> node_1080
    node_541 --> node_1318
    node_206 --> node_221
    node_1339 --> node_1198
    node_5 --> node_1323
    node_852 --> node_695
    node_1117 --> node_741
    node_541 --> node_1261
    node_549 --> node_632
    node_705 --> node_1260
    node_563 --> node_1082
    node_666 --> node_1300
    node_1230 --> node_1077
    node_541 --> node_1272
    node_67 --> node_116
    node_1117 --> node_203
    node_145 --> node_606
    node_1127 --> node_697
    node_430 --> node_49
    node_486 --> node_253
    node_401 --> node_260
    node_847 --> node_213
    node_455 --> node_1148
    node_632 --> node_1339
    node_0 --> node_1339
    node_79 --> node_1128
    node_102 --> node_1161
    node_1314 --> node_1065
    node_489 --> node_1285
    node_253 --> node_233
    node_866 --> node_697
    node_599 --> node_1083
    node_146 --> node_58
    node_964 --> node_1007
    node_666 --> node_1273
    node_449 --> node_56
    node_541 --> node_1336
    node_478 --> node_35
    node_410 --> node_1262
    node_56 --> node_240
    node_301 --> node_312
    node_632 --> node_1220
    node_0 --> node_1220
    node_666 --> node_1267
    node_564 --> node_666
    node_12 --> node_656
    node_0 --> node_1121
    node_379 --> node_67
    node_489 --> node_197
    node_520 --> node_250
    node_530 --> node_303
    node_489 --> node_328
    node_31 --> node_187
    node_251 --> node_241
    node_541 --> node_1094
    node_632 --> node_1147
    node_918 --> node_405
    node_19 --> node_221
    node_254 --> node_1294
    node_0 --> node_1147
    node_154 --> node_128
    node_251 --> node_731
    node_654 --> node_1169
    node_489 --> node_405
    node_304 --> node_314
    node_777 --> node_1149
    node_575 --> node_37
    node_595 --> node_593
    node_521 --> node_241
    node_497 --> node_1043
    node_99 --> node_1138
    node_102 --> node_148
    node_676 --> node_704
    node_455 --> node_695
    node_147 --> node_533
    node_858 --> node_1165
    node_20 --> node_1003
    node_533 --> node_250
    node_879 --> node_419
    node_497 --> node_638
    node_1162 --> node_247
    node_564 --> node_643
    node_1093 --> node_1047
    node_751 --> node_756
    node_197 --> node_413
    node_58 --> node_731
    node_187 --> node_1271
    node_5 --> node_577
    node_520 --> node_1353
    node_575 --> node_784
    node_971 --> node_1236
    node_122 --> node_132
    node_179 --> node_399
    node_379 --> node_181
    node_67 --> node_122
    node_1260 --> node_1289
    node_541 --> node_1260
    node_704 --> node_35
    node_836 --> node_399
    node_497 --> node_997
    node_1230 --> node_1116
    node_12 --> node_663
    node_1104 --> node_1145
    node_520 --> node_1330
    node_58 --> node_116
    node_516 --> node_368
    node_506 --> node_221
    node_525 --> node_1298
    node_208 --> node_72
    node_56 --> node_1182
    node_64 --> node_1043
    node_525 --> node_1218
    node_526 --> node_419
    node_1231 --> node_1154
    node_1250 --> node_1244
    node_205 --> node_361
    node_575 --> node_334
    node_63 --> node_52
    node_449 --> node_962
    node_772 --> node_229
    node_648 --> node_1314
    node_31 --> node_744
    node_525 --> node_1363
    node_502 --> node_1262
    node_629 --> node_1102
    node_541 --> node_631
    node_330 --> node_240
    node_1230 --> node_232
    node_1192 --> node_58
    node_808 --> node_1277
    node_901 --> node_360
    node_251 --> node_328
    node_670 --> node_178
    node_666 --> node_1212
    node_5 --> node_1344
    node_229 --> node_191
    node_384 --> node_260
    node_541 --> node_871
    node_541 --> node_737
    node_862 --> node_257
    node_1190 --> node_58
    node_197 --> node_273
    node_631 --> node_657
    node_187 --> node_72
    node_489 --> node_412
    node_1339 --> node_1326
    node_64 --> node_997
    node_578 --> node_5
    node_20 --> node_595
    node_313 --> node_607
    node_5 --> node_35
    node_520 --> node_1166
    node_973 --> node_1102
    node_934 --> node_1234
    node_205 --> node_408
    node_1167 --> node_1014
    node_541 --> node_1167
    node_209 --> node_305
    node_666 --> node_1215
    node_861 --> node_606
    node_666 --> node_1270
    node_26 --> node_33
    node_1097 --> node_1309
    node_861 --> node_352
    node_563 --> node_639
    node_135 --> node_127
    node_5 --> node_1126
    node_1230 --> node_1123
    node_208 --> node_233
    node_58 --> node_328
    node_1351 --> node_1303
    node_1210 --> node_1047
    node_127 --> node_739
    node_1362 --> node_249
    node_19 --> node_271
    node_520 --> node_1231
    node_1126 --> node_1124
    node_215 --> node_340
    node_653 --> node_1028
    node_497 --> node_1186
    node_5 --> node_881
    node_772 --> node_412
    node_12 --> node_666
    node_719 --> node_1148
    node_751 --> node_667
    node_795 --> node_792
    node_1117 --> node_72
    node_52 --> node_240
    node_187 --> node_233
    node_954 --> node_959
    node_1230 --> node_1307
    node_520 --> node_1207
    node_497 --> node_1353
    node_326 --> node_6
    node_861 --> node_1213
    node_5 --> node_1123
    node_905 --> node_1283
    node_533 --> node_15
    node_1231 --> node_1325
    node_648 --> node_175
    node_1188 --> node_175
    node_0 --> node_1037
    node_666 --> node_1284
    node_861 --> node_31
    node_1102 --> node_203
    node_632 --> node_175
    node_541 --> node_614
    node_5 --> node_1059
    node_31 --> node_35
    node_667 --> node_665
    node_500 --> node_179
    node_599 --> node_962
    node_575 --> node_620
    node_772 --> node_37
    node_652 --> node_1007
    node_31 --> node_699
    node_122 --> node_250
    node_1105 --> node_1047
    node_781 --> node_737
    node_762 --> node_67
    node_12 --> node_643
    node_1314 --> node_1060
    node_187 --> node_296
    node_497 --> node_1330
    node_599 --> node_1003
    node_814 --> node_419
    node_449 --> node_1302
    node_1076 --> node_1075
    node_663 --> node_1063
    node_103 --> node_617
    node_1230 --> node_1191
    node_1230 --> node_1030
    node_1267 --> node_249
    node_514 --> node_57
    node_773 --> node_1082
    node_1117 --> node_233
    node_19 --> node_387
    node_19 --> node_1280
    node_19 --> node_241
    node_520 --> node_1057
    node_56 --> node_1090
    node_772 --> node_784
    node_1314 --> node_1122
    node_100 --> node_1138
    node_1315 --> node_1047
    node_328 --> node_241
    node_1231 --> node_1336
    node_5 --> node_1069
    node_106 --> node_681
    node_575 --> node_948
    node_106 --> node_6
    node_1081 --> node_1084
    node_19 --> node_196
    node_541 --> node_1327
    node_3 --> node_571
    node_520 --> node_954
    node_1339 --> node_1140
    node_822 --> node_1278
    node_497 --> node_1166
    node_1010 --> node_1047
    node_581 --> node_138
    node_50 --> node_170
    node_56 --> node_61
    node_666 --> node_1237
    node_1230 --> node_1225
    node_229 --> node_251
    node_525 --> node_1066
    node_489 --> node_391
    node_986 --> node_1047
    node_1231 --> node_1094
    node_520 --> node_606
    node_599 --> node_238
    node_499 --> node_731
    node_284 --> node_212
    node_541 --> node_1213
    node_1351 --> node_1265
    node_370 --> node_35
    node_841 --> node_392
    node_1221 --> node_72
    node_178 --> node_1047
    node_6 --> node_326
    node_449 --> node_191
    node_751 --> node_1021
    node_475 --> node_209
    node_1077 --> node_191
    node_781 --> node_614
    node_935 --> node_1015
    node_1314 --> node_1034
    node_1330 --> node_1011
    node_63 --> node_737
    node_44 --> node_175
    node_575 --> node_735
    node_497 --> node_1326
    node_0 --> node_1309
    node_468 --> node_1260
    node_63 --> node_104
    node_497 --> node_677
    node_775 --> node_1262
    node_1097 --> node_1154
    node_541 --> node_1307
    node_1324 --> node_1320
    node_152 --> node_240
    node_125 --> node_136
    node_525 --> node_1157
    node_20 --> node_115
    node_1015 --> node_1166
    node_497 --> node_1207
    node_69 --> node_97
    node_19 --> node_197
    node_687 --> node_232
    node_1314 --> node_1340
    node_56 --> node_1343
    node_489 --> node_418
    node_232 --> node_739
    node_145 --> node_742
    node_1221 --> node_233
    node_416 --> node_1003
    node_852 --> node_1260
    node_150 --> node_58
    node_911 --> node_792
    node_19 --> node_405
    node_934 --> node_1016
    node_738 --> node_241
    node_1097 --> node_1349
    node_541 --> node_1030
    node_893 --> node_1148
    node_1312 --> node_1313
    node_1314 --> node_1045
    node_1314 --> node_1036
    node_629 --> node_1116
    node_142 --> node_238
    node_894 --> node_207
    node_785 --> node_1148
    node_205 --> node_1296
    node_665 --> node_1214
    node_781 --> node_1213
    node_667 --> node_668
    node_497 --> node_1057
    node_1230 --> node_1040
    node_489 --> node_408
    node_499 --> node_328
    node_751 --> node_720
    node_106 --> node_103
    node_695 --> node_731
    node_781 --> node_31
    node_1167 --> node_1008
    node_63 --> node_614
    node_1193 --> node_1047
    node_5 --> node_506
    node_1 --> node_591
    node_764 --> node_684
    node_666 --> node_1084
    node_489 --> node_1061
    node_67 --> node_128
    node_1230 --> node_1219
    node_1230 --> node_1226
    node_772 --> node_620
    node_666 --> node_1235
    node_559 --> node_704
    node_1117 --> node_207
    node_58 --> node_119
    node_187 --> node_346
    node_1231 --> node_1167
    node_514 --> node_267
    node_525 --> node_1093
    node_497 --> node_954
    node_823 --> node_284
    node_1339 --> node_1173
    node_595 --> node_549
    node_541 --> node_311
    node_654 --> node_1042
    node_187 --> node_406
    node_497 --> node_606
    node_1314 --> node_1349
    node_1097 --> node_1325
    node_1083 --> node_247
    node_709 --> node_1082
    node_511 --> node_1102
    node_854 --> node_272
    node_1097 --> node_1318
    node_1339 --> node_1257
    node_102 --> node_1209
    node_520 --> node_1357
    node_1117 --> node_270
    node_528 --> node_649
    node_20 --> node_37
    node_416 --> node_595
    node_893 --> node_695
    node_1162 --> node_36
    node_179 --> node_400
    node_815 --> node_1148
    node_455 --> node_1260
    node_106 --> node_711
    node_164 --> node_132
    node_625 --> node_1237
    node_772 --> node_948
    node_935 --> node_1233
    node_585 --> node_649
    node_631 --> node_670
    node_489 --> node_348
    node_541 --> node_3
    node_1077 --> node_251
    node_785 --> node_695
    node_643 --> node_1323
    node_563 --> node_26
    node_99 --> node_667
    node_20 --> node_784
    node_106 --> node_730
    node_519 --> node_33
    node_627 --> node_1184
    node_249 --> node_248
    node_63 --> node_1213
    node_520 --> node_68
    node_209 --> node_327
    node_1154 --> node_1151
    node_525 --> node_626
    node_63 --> node_31
    node_1117 --> node_988
    node_1168 --> node_1047
    node_64 --> node_606
    node_525 --> node_1140
    node_335 --> node_67
    node_142 --> node_1078
    node_525 --> node_1041
    node_666 --> node_1216
    node_632 --> node_1154
    node_406 --> node_265
    node_668 --> node_1135
    node_1081 --> node_974
    node_0 --> node_1154
    node_695 --> node_328
    node_751 --> node_795
    node_668 --> node_1137
    node_1314 --> node_1141
    node_751 --> node_48
    node_1300 --> node_36
    node_1147 --> node_1148
    node_5 --> node_811
    node_514 --> node_1085
    node_489 --> node_576
    node_1230 --> node_249
    node_5 --> node_380
    node_675 --> node_388
    node_19 --> node_599
    node_511 --> node_187
    node_1083 --> node_1082
    node_599 --> node_229
    node_541 --> node_1040
    node_106 --> node_966
    node_525 --> node_1065
    node_145 --> node_960
    node_497 --> node_33
    node_1260 --> node_363
    node_559 --> node_191
    node_632 --> node_1349
    node_497 --> node_1027
    node_0 --> node_1349
    node_505 --> node_249
    node_1127 --> node_733
    node_861 --> node_177
    node_1231 --> node_1327
    node_579 --> node_647
    node_533 --> node_3
    node_520 --> node_1081
    node_205 --> node_1269
    node_861 --> node_742
    node_3 --> node_26
    node_666 --> node_1278
    node_500 --> node_886
    node_525 --> node_1214
    node_525 --> node_1314
    node_631 --> node_658
    node_1147 --> node_1354
    node_866 --> node_733
    node_929 --> node_1239
    node_972 --> node_741
    node_507 --> node_530
    node_821 --> node_368
    node_1361 --> node_1099
    node_1339 --> node_1156
    node_520 --> node_1194
    node_1081 --> node_238
    node_5 --> node_1211
    node_972 --> node_203
    node_795 --> node_793
    node_599 --> node_951
    node_665 --> node_1114
    node_449 --> node_677
    node_516 --> node_241
    node_599 --> node_565
    node_103 --> node_746
    node_543 --> node_35
    node_526 --> node_739
    node_489 --> node_1295
    node_923 --> node_247
    node_665 --> node_1100
    node_395 --> node_35
    node_1103 --> node_1099
    node_658 --> node_1240
    node_1147 --> node_695
    node_497 --> node_1357
    node_141 --> node_58
    node_659 --> node_1236
    node_625 --> node_1235
    node_658 --> node_1250
    node_647 --> node_1115
    node_387 --> node_265
    node_99 --> node_1021
    node_104 --> node_56
    node_0 --> node_1325
    node_1230 --> node_1088
    node_657 --> node_1312
    node_669 --> node_1071
    node_632 --> node_1318
    node_658 --> node_1251
    node_658 --> node_1241
    node_0 --> node_1318
    node_5 --> node_1006
    node_278 --> node_281
    node_751 --> node_1254
    node_490 --> node_519
    node_52 --> node_57
    node_497 --> node_68
    node_953 --> node_951
    node_1352 --> node_1083
    node_19 --> node_391
    node_423 --> node_448
    node_153 --> node_20
    node_749 --> node_752
    node_489 --> node_1296
    node_541 --> node_177
    node_19 --> node_269
    node_1339 --> node_1015
    node_20 --> node_840
    node_20 --> node_620
    node_497 --> node_1020
    node_520 --> node_1337
    node_537 --> node_1177
    node_1123 --> node_1047
    node_541 --> node_249
    node_1314 --> node_1077
    node_1015 --> node_1357
    node_5 --> node_1174
    node_490 --> node_528
    node_907 --> node_383
    node_208 --> node_731
    node_0 --> node_1336
    node_5 --> node_1031
    node_5 --> node_520
    node_368 --> node_1047
    node_520 --> node_1017
    node_599 --> node_784
    node_492 --> node_537
    node_595 --> node_582
    node_1127 --> node_336
    node_1230 --> node_1227
    node_56 --> node_1347
    node_449 --> node_954
    node_72 --> node_69
    node_642 --> node_1236
    node_1359 --> node_1261
    node_520 --> node_1239
    node_0 --> node_1094
    node_191 --> node_57
    node_465 --> node_1148
    node_1081 --> node_1078
    node_541 --> node_1301
    node_1147 --> node_1145
    node_100 --> node_667
    node_866 --> node_336
    node_99 --> node_720
    node_520 --> node_742
    node_497 --> node_1081
    node_561 --> node_642
    node_665 --> node_1192
    node_656 --> node_1012
    node_19 --> node_344
    node_238 --> node_98
    node_705 --> node_1082
    node_1015 --> node_1020
    node_209 --> node_331
    node_486 --> node_1261
    node_79 --> node_331
    node_361 --> node_247
    node_541 --> node_1290
    node_599 --> node_334
    node_187 --> node_1294
    node_124 --> node_233
    node_1166 --> node_1165
    node_511 --> node_35
    node_520 --> node_1104
    node_1105 --> node_197
    node_708 --> node_1148
    node_227 --> node_213
    node_137 --> node_69
    node_781 --> node_177
    node_492 --> node_5
    node_520 --> node_1362
    node_541 --> node_1087
    node_187 --> node_282
    node_541 --> node_247
    node_1117 --> node_731
    node_102 --> node_1162
    node_521 --> node_209
    node_796 --> node_183
    node_520 --> node_975
    node_531 --> node_183
    node_520 --> node_203
    node_657 --> node_1046
    node_187 --> node_1285
    node_1015 --> node_1011
    node_208 --> node_328
    node_416 --> node_37
    node_5 --> node_739
    node_289 --> node_1047
    node_465 --> node_695
    node_106 --> node_547
    node_249 --> node_741
    node_699 --> node_706
    node_205 --> node_187
    node_497 --> node_1195
    node_543 --> node_585
    node_1097 --> node_1327
    node_1314 --> node_1116
    node_1037 --> node_1297
    node_249 --> node_203
    node_1162 --> node_1302
    node_563 --> node_657
    node_525 --> node_1060
    node_537 --> node_183
    node_599 --> node_488
    node_1339 --> node_1024
    node_1299 --> node_571
    node_525 --> node_1156
    node_497 --> node_1337
    node_1339 --> node_1098
    node_842 --> node_638
    node_99 --> node_795
    node_56 --> node_98
    node_147 --> node_64
    node_5 --> node_253
    node_302 --> node_311
    node_196 --> node_219
    node_5 --> node_1319
    node_1339 --> node_1169
    node_757 --> node_187
    node_99 --> node_48
    node_581 --> node_601
    node_525 --> node_1122
    node_708 --> node_695
    node_462 --> node_179
    node_19 --> node_348
    node_599 --> node_765
    node_64 --> node_329
    node_599 --> node_487
    node_330 --> node_947
    node_100 --> node_1021
    node_0 --> node_1167
    node_103 --> node_546
    node_1015 --> node_1089
    node_666 --> node_1078
    node_63 --> node_177
    node_497 --> node_1239
    node_541 --> node_1082
    node_599 --> node_620
    node_1300 --> node_1302
    node_1097 --> node_1307
    node_487 --> node_1149
    node_1331 --> node_1236
    node_489 --> node_277
    node_117 --> node_69
    node_525 --> node_1356
    node_1083 --> node_36
    node_308 --> node_698
    node_497 --> node_1300
    node_1117 --> node_328
    node_1339 --> node_1143
    node_154 --> node_136
    node_666 --> node_1285
    node_1314 --> node_1123
    node_712 --> node_983
    node_1260 --> node_1149
    node_187 --> node_1275
    node_497 --> node_943
    node_19 --> node_576
    node_520 --> node_960
    node_930 --> node_1016
    node_525 --> node_1034
    node_104 --> node_241
    node_862 --> node_398
    node_893 --> node_1260
    node_525 --> node_1192
    node_142 --> node_488
    node_692 --> node_1047
    node_599 --> node_948
    node_500 --> node_50
    node_1097 --> node_1191
    node_632 --> node_1116
    node_449 --> node_68
    node_1097 --> node_1030
    node_541 --> node_650
    node_785 --> node_1260
    node_1147 --> node_1261
    node_520 --> node_1155
    node_1299 --> node_1297
    node_904 --> node_258
    node_1069 --> node_1074
    node_472 --> node_1291
    node_665 --> node_1102
    node_497 --> node_975
    node_1231 --> node_1017
    node_102 --> node_1259
    node_497 --> node_1267
    node_64 --> node_742
    node_526 --> node_398
    node_524 --> node_925
    node_52 --> node_1085
    node_338 --> node_67
    node_100 --> node_720
    node_525 --> node_1340
    node_772 --> node_681
    node_511 --> node_1313
    node_1314 --> node_1069
    node_1097 --> node_1225
    node_330 --> node_98
    node_197 --> node_213
    node_99 --> node_1254
    node_490 --> node_4
    node_1141 --> node_1038
    node_1290 --> node_12
    node_5 --> node_856
    node_5 --> node_1121
    node_1261 --> node_1263
    node_1361 --> node_1075
    node_19 --> node_1295
    node_599 --> node_735
    node_330 --> node_135
    node_665 --> node_1343
    node_31 --> node_1095
    node_525 --> node_1045
    node_541 --> node_969
    node_416 --> node_48
    node_964 --> node_1017
    node_525 --> node_1036
    node_31 --> node_1222
    node_575 --> node_682
    node_898 --> node_272
    node_1314 --> node_1191
    node_632 --> node_1327
    node_1314 --> node_1030
    node_643 --> node_1321
    node_0 --> node_1327
    node_1103 --> node_1075
    node_1230 --> node_1125
    node_5 --> node_707
    node_525 --> node_1232
    node_846 --> node_704
    node_666 --> node_1275
    node_489 --> node_274
    node_19 --> node_209
    node_191 --> node_1085
    node_5 --> node_1035
    node_187 --> node_410
    node_229 --> node_741
    node_543 --> node_1221
    node_1231 --> node_1301
    node_19 --> node_219
    node_106 --> node_911
    node_229 --> node_203
    node_738 --> node_248
    node_205 --> node_35
    node_1230 --> node_1305
    node_1314 --> node_1225
    node_740 --> node_72
    node_860 --> node_419
    node_497 --> node_1184
    node_1339 --> node_1329
    node_447 --> node_425
    node_652 --> node_1016
    node_19 --> node_276
    node_52 --> node_98
    node_58 --> node_129
    node_666 --> node_1317
    node_507 --> node_697
    node_497 --> node_1169
    node_687 --> node_253
    node_410 --> node_1149
    node_12 --> node_672
    node_187 --> node_1268
    node_1077 --> node_1076
    node_520 --> node_1097
    node_489 --> node_273
    node_632 --> node_1307
    node_489 --> node_1291
    node_0 --> node_1307
    node_782 --> node_209
    node_1045 --> node_238
    node_497 --> node_960
    node_1230 --> node_1188
    node_1147 --> node_1260
    node_757 --> node_35
    node_31 --> node_795
    node_100 --> node_795
    node_1231 --> node_1087
    node_67 --> node_118
    node_523 --> node_82
    node_489 --> node_187
    node_497 --> node_1212
    node_663 --> node_1026
    node_429 --> node_430
    node_1230 --> node_1005
    node_100 --> node_48
    node_478 --> node_1148
    node_19 --> node_1276
    node_5 --> node_491
    node_520 --> node_1153
    node_1230 --> node_1023
    node_1097 --> node_1040
    node_205 --> node_1282
    node_781 --> node_969
    node_1287 --> node_178
    node_497 --> node_486
    node_1357 --> node_1355
    node_525 --> node_1201
    node_233 --> node_241
    node_1260 --> node_1286
    node_449 --> node_490
    node_449 --> node_1337
    node_740 --> node_233
    node_502 --> node_250
    node_632 --> node_1191
    node_632 --> node_1030
    node_0 --> node_1030
    node_1097 --> node_1219
    node_418 --> node_327
    node_1230 --> node_1200
    node_1362 --> node_191
    node_731 --> node_336
    node_541 --> node_1170
    node_647 --> node_1099
    node_145 --> node_106
    node_1339 --> node_1223
    node_1352 --> node_191
    node_666 --> node_1259
    node_1044 --> node_1047
    node_506 --> node_300
    node_64 --> node_960
    node_1230 --> node_1341
    node_1081 --> node_488
    node_743 --> node_233
    node_665 --> node_1056
    node_145 --> node_1003
    node_499 --> node_306
    node_599 --> node_240
    node_449 --> node_766
    node_468 --> node_1082
    node_930 --> node_1012
    node_632 --> node_1225
    node_872 --> node_1286
    node_56 --> node_1346
    node_334 --> node_51
    node_1206 --> node_1204
    node_1314 --> node_1040
    node_520 --> node_1342
    node_1 --> node_745
    node_106 --> node_617
    node_666 --> node_1193
    node_130 --> node_739
    node_19 --> node_183
    node_1081 --> node_982
    node_5 --> node_67
    node_1362 --> node_1359
    node_5 --> node_1335
    node_575 --> node_1138
    node_1076 --> node_967
    node_449 --> node_943
    node_541 --> node_1305
    node_1314 --> node_1226
    node_1314 --> node_1219
    node_187 --> node_243
    node_1037 --> node_1299
    node_599 --> node_12
    node_911 --> node_397
    node_563 --> node_670
    node_416 --> node_20
    node_1045 --> node_1078
    node_852 --> node_1082
    node_205 --> node_419
    node_196 --> node_193
    node_31 --> node_1254
    node_5 --> node_1037
    node_557 --> node_67
    node_100 --> node_1254
    node_520 --> node_1352
    node_1230 --> node_1118
    node_152 --> node_98
    node_541 --> node_1188
    node_476 --> node_695
    node_449 --> node_741
    node_20 --> node_681
    node_497 --> node_1097
    node_449 --> node_975
    node_1230 --> node_1185
    node_205 --> node_1283
    node_1339 --> node_1310
    node_525 --> node_1323
    node_1339 --> node_1126
    node_663 --> node_1066
    node_102 --> node_1176
    node_541 --> node_36
    node_489 --> node_281
    node_480 --> node_267
    node_5 --> node_993
    node_971 --> node_1233
    node_665 --> node_1116
    node_520 --> node_1029
    node_1117 --> node_320
    node_520 --> node_1235
    node_864 --> node_272
    node_1117 --> node_243
    node_497 --> node_1153
    node_1083 --> node_1302
    node_187 --> node_402
    node_251 --> node_57
    node_106 --> node_143
    node_5 --> node_1148
    node_1141 --> node_1040
    node_179 --> node_404
    node_530 --> node_697
    node_614 --> node_615
    node_859 --> node_417
    node_541 --> node_1200
    node_662 --> node_971
    node_465 --> node_1260
    node_500 --> node_410
    node_19 --> node_277
    node_1267 --> node_52
    node_423 --> node_428
    node_5 --> node_1185
    node_861 --> node_245
    node_632 --> node_1040
    node_661 --> node_1007
    node_666 --> node_1348
    node_0 --> node_1040
    node_229 --> node_72
    node_1360 --> node_1128
    node_666 --> node_1079
    node_525 --> node_1077
    node_1362 --> node_251
    node_153 --> node_533
    node_543 --> node_739
    node_455 --> node_1082
    node_19 --> node_285
    node_632 --> node_1226
    node_632 --> node_1219
    node_1330 --> node_1009
    node_563 --> node_658
    node_666 --> node_1238
    node_209 --> node_210
    node_489 --> node_35
    node_836 --> node_837
    node_708 --> node_1260
    node_1230 --> node_1332
    node_362 --> node_1289
    node_751 --> node_711
    node_1314 --> node_1211
    node_19 --> node_179
    node_533 --> node_36
    node_68 --> node_72
    node_489 --> node_267
    node_934 --> node_1183
    node_19 --> node_284
    node_49 --> node_55
    node_657 --> node_1053
    node_5 --> node_1309
    node_1097 --> node_1087
    node_187 --> node_369
    node_31 --> node_1148
    node_777 --> node_221
    node_5 --> node_400
    node_861 --> node_962
    node_1141 --> node_1120
    node_520 --> node_1205
    node_1216 --> node_1221
    node_911 --> node_676
    node_5 --> node_530
    node_666 --> node_1315
    node_229 --> node_233
    node_520 --> node_1146
    node_917 --> node_392
    node_179 --> node_201
    node_490 --> node_500
    node_832 --> node_183
    node_657 --> node_1049
    node_861 --> node_1003
    node_541 --> node_1118
    node_1312 --> node_1354
    node_252 --> node_410
    node_1355 --> node_1047
    node_31 --> node_244
    node_63 --> node_1047
    node_5 --> node_776
    node_1339 --> node_1013
    node_449 --> node_486
    node_100 --> node_244
    node_972 --> node_238
    node_520 --> node_1132
    node_666 --> node_1061
    node_1267 --> node_251
    node_516 --> node_209
    node_751 --> node_966
    node_5 --> node_573
    node_68 --> node_233
    node_19 --> node_1271
    node_599 --> node_554
    node_934 --> node_1236
    node_929 --> node_1236
    node_63 --> node_1083
    node_1267 --> node_246
    node_1346 --> node_1047
    node_19 --> node_274
    node_1267 --> node_1149
    node_115 --> node_138
    node_497 --> node_1029
    node_1097 --> node_1227
    node_1314 --> node_1088
    node_79 --> node_81
    node_559 --> node_928
    node_497 --> node_1235
    node_733 --> node_734
    node_54 --> node_58
    node_1336 --> node_1334
    node_1154 --> node_1153
    node_31 --> node_695
    node_774 --> node_282
    node_121 --> node_69
    node_648 --> node_176
    node_577 --> node_12
    node_632 --> node_176
    node_775 --> node_1149
    node_1061 --> node_5
    node_525 --> node_1344
    node_1330 --> node_1010
    node_5 --> node_382
    node_497 --> node_1310
    node_1339 --> node_1068
    node_20 --> node_711
    node_68 --> node_123
    node_541 --> node_962
    node_19 --> node_273
    node_520 --> node_1092
    node_699 --> node_700
    node_1339 --> node_1019
    node_19 --> node_1291
    node_31 --> node_543
    node_636 --> node_1182
    node_541 --> node_26
    node_5 --> node_705
    node_1230 --> node_1324
    node_215 --> node_1047
    node_599 --> node_24
    node_712 --> node_187
    node_1134 --> node_1047
    node_20 --> node_730
    node_205 --> node_380
    node_154 --> node_247
    node_1117 --> node_983
    node_0 --> node_1301
    node_145 --> node_229
    node_525 --> node_1126
    node_419 --> node_1047
    node_1231 --> node_1117
    node_647 --> node_1114
    node_1314 --> node_1227
    node_1339 --> node_1256
    node_1259 --> node_1047
    node_352 --> node_423
    node_1251 --> node_1246
    node_657 --> node_1044
    node_647 --> node_1100
    node_160 --> node_69
    node_20 --> node_533
    node_533 --> node_290
    node_783 --> node_695
    node_599 --> node_965
    node_301 --> node_313
    node_511 --> node_253
    node_1359 --> node_249
    node_133 --> node_138
    node_866 --> node_241
    node_895 --> node_420
    node_520 --> node_106
    node_663 --> node_1065
    node_154 --> node_143
    node_866 --> node_731
    node_497 --> node_1042
    node_541 --> node_1230
    node_646 --> node_1076
    node_489 --> node_182
    node_1304 --> node_1047
    node_499 --> node_187
    node_972 --> node_1078
    node_497 --> node_1146
    node_870 --> node_376
    node_520 --> node_1003
    node_122 --> node_36
    node_497 --> node_1206
    node_486 --> node_249
    node_921 --> node_509
    node_525 --> node_1123
    node_0 --> node_1087
    node_916 --> node_402
    node_541 --> node_704
    node_187 --> node_1296
    node_5 --> node_1154
    node_231 --> node_216
    node_525 --> node_1059
    node_1362 --> node_1361
    node_489 --> node_555
    node_742 --> node_741
    node_1015 --> node_1355
    node_505 --> node_191
    node_497 --> node_1132
    node_102 --> node_1182
    node_742 --> node_203
    node_165 --> node_70
    node_106 --> node_746
    node_781 --> node_962
    node_461 --> node_67
    node_251 --> node_1085
    node_489 --> node_217
    node_3 --> node_563
    node_1117 --> node_607
    node_796 --> node_485
    node_254 --> node_419
    node_209 --> node_354
    node_103 --> node_606
    node_416 --> node_681
    node_228 --> node_231
    node_1230 --> node_1359
    node_1230 --> node_52
    node_811 --> node_387
    node_1352 --> node_487
    node_497 --> node_1013
    node_58 --> node_138
    node_1117 --> node_1100
    node_525 --> node_1069
    node_541 --> node_1302
    node_632 --> node_1227
    node_145 --> node_37
    node_5 --> node_378
    node_529 --> node_3
    node_603 --> node_1127
    node_1045 --> node_488
    node_520 --> node_595
    node_885 --> node_1284
    node_866 --> node_328
    node_541 --> node_1299
    node_771 --> node_268
    node_461 --> node_181
    node_669 --> node_1073
    node_844 --> node_1269
    node_1117 --> node_278
    node_145 --> node_784
    node_1206 --> node_1203
    node_537 --> node_1178
    node_834 --> node_272
    node_103 --> node_1213
    node_800 --> node_1276
    node_147 --> node_58
    node_179 --> node_1290
    node_219 --> node_210
    node_103 --> node_31
    node_490 --> node_525
    node_666 --> node_1296
    node_1260 --> node_1273
    node_599 --> node_57
    node_5 --> node_349
    node_1359 --> node_734
    node_464 --> node_193
    node_99 --> node_711
    node_474 --> node_695
    node_396 --> node_260
    node_5 --> node_1325
    node_1230 --> node_1186
    node_63 --> node_962
    node_666 --> node_1060
    node_541 --> node_638
    node_541 --> node_191
    node_913 --> node_187
    node_5 --> node_1261
    node_740 --> node_731
    node_1261 --> node_183
    node_643 --> node_1064
    node_806 --> node_266
    node_497 --> node_1003
    node_497 --> node_1312
    node_145 --> node_334
    node_527 --> node_739
    node_533 --> node_1302
    node_709 --> node_703
    node_712 --> node_35
    node_720 --> node_110
    node_861 --> node_229
    node_1230 --> node_1353
    node_1117 --> node_185
    node_666 --> node_1122
    node_669 --> node_1068
    node_666 --> node_1266
    node_1230 --> node_251
    node_1015 --> node_1209
    node_1167 --> node_1012
    node_873 --> node_409
    node_402 --> node_178
    node_7 --> node_698
    node_334 --> node_241
    node_1230 --> node_246
    node_1310 --> node_62
    node_507 --> node_733
    node_541 --> node_998
    node_5 --> node_1336
    node_657 --> node_1055
    node_187 --> node_1269
    node_1230 --> node_1330
    node_1156 --> node_1047
    node_102 --> node_1090
    node_1147 --> node_249
    node_840 --> node_270
    node_99 --> node_966
    node_767 --> node_176
    node_954 --> node_953
    node_1312 --> node_1261
    node_64 --> node_106
    node_5 --> node_537
    node_489 --> node_1127
    node_229 --> node_743
    node_625 --> node_175
    node_599 --> node_577
    node_667 --> node_656
    node_599 --> node_961
    node_520 --> node_1298
    node_499 --> node_35
    node_1049 --> node_1047
    node_520 --> node_1218
    node_446 --> node_425
    node_5 --> node_1094
    node_64 --> node_1003
    node_559 --> node_72
    node_3 --> node_702
    node_79 --> node_307
    node_1314 --> node_1035
    node_1097 --> node_1305
    node_520 --> node_1363
    node_1339 --> node_1026
    node_893 --> node_1082
    node_68 --> node_141
    node_400 --> node_193
    node_442 --> node_425
    node_658 --> node_1248
    node_114 --> node_133
    node_642 --> node_1015
    node_846 --> node_248
    node_5 --> node_372
    node_1117 --> node_206
    node_1100 --> node_192
    node_205 --> node_395
    node_1230 --> node_1166
    node_785 --> node_1082
    node_497 --> node_595
    node_1231 --> node_1236
    node_657 --> node_1045
    node_1097 --> node_1188
    node_68 --> node_106
    node_740 --> node_328
    node_1314 --> node_1125
    node_564 --> node_659
    node_1339 --> node_1197
    node_540 --> node_589
    node_416 --> node_711
    node_665 --> node_1006
    node_1097 --> node_1005
    node_56 --> node_546
    node_238 --> node_29
    node_742 --> node_72
    node_1015 --> node_1009
    node_1097 --> node_1023
    node_520 --> node_1198
    node_541 --> node_1186
    node_145 --> node_620
    node_1117 --> node_189
    node_1231 --> node_1230
    node_1101 --> node_1047
    node_1231 --> node_1133
    node_559 --> node_233
    node_575 --> node_1021
    node_416 --> node_730
    node_830 --> node_387
    node_667 --> node_663
    node_662 --> node_1234
    node_1314 --> node_1305
    node_647 --> node_1102
    node_489 --> node_79
    node_935 --> node_1064
    node_229 --> node_238
    node_1162 --> node_741
    node_1097 --> node_1200
    node_604 --> node_583
    node_19 --> node_384
    node_665 --> node_1088
    node_331 --> node_325
    node_489 --> node_212
    node_719 --> node_1047
    node_5 --> node_423
    node_695 --> node_81
    node_824 --> node_235
    node_948 --> node_947
    node_102 --> node_1343
    node_520 --> node_229
    node_307 --> node_308
    node_631 --> node_665
    node_205 --> node_399
    node_861 --> node_784
    node_1230 --> node_1207
    node_687 --> node_52
    node_1097 --> node_1341
    node_5 --> node_1231
    node_238 --> node_239
    node_380 --> node_183
    node_720 --> node_715
    node_599 --> node_1138
    node_1045 --> node_1044
    node_5 --> node_15
    node_541 --> node_1330
    node_145 --> node_948
    node_697 --> node_332
    node_5 --> node_210
    node_1314 --> node_1005
    node_742 --> node_233
    node_497 --> node_640
    node_1314 --> node_1023
    node_31 --> node_1002
    node_5 --> node_498
    node_63 --> node_191
    node_122 --> node_1302
    node_101 --> node_120
    node_855 --> node_707
    node_575 --> node_688
    node_1261 --> node_193
    node_689 --> node_15
    node_751 --> node_911
    node_56 --> node_144
    node_5 --> node_1167
    node_935 --> node_1008
    node_100 --> node_711
    node_19 --> node_182
    node_31 --> node_1260
    node_913 --> node_35
    node_497 --> node_1298
    node_1066 --> node_1063
    node_861 --> node_334
    node_1230 --> node_1057
    node_735 --> node_1
    node_632 --> node_1125
    node_102 --> node_149
    node_522 --> node_180
    node_56 --> node_29
    node_106 --> node_144
    node_511 --> node_1148
    node_333 --> node_335
    node_497 --> node_1363
    node_1147 --> node_1082
    node_530 --> node_733
    node_1081 --> node_187
    node_213 --> node_183
    node_1287 --> node_200
    node_1314 --> node_1341
    node_1097 --> node_1118
    node_1117 --> node_1102
    node_1231 --> node_1299
    node_1339 --> node_1308
    node_667 --> node_666
    node_209 --> node_279
    node_972 --> node_488
    node_682 --> node_686
    node_1015 --> node_1010
    node_599 --> node_947
    node_632 --> node_1305
    node_5 --> node_822
    node_31 --> node_631
    node_0 --> node_1305
    node_922 --> node_82
    node_525 --> node_1211
    node_581 --> node_968
    node_19 --> node_217
    node_531 --> node_213
    node_575 --> node_1095
    node_599 --> node_1085
    node_489 --> node_213
    node_653 --> node_1094
    node_229 --> node_1078
    node_935 --> node_1037
    node_68 --> node_731
    node_31 --> node_737
    node_447 --> node_445
    node_156 --> node_547
    node_783 --> node_1260
    node_1361 --> node_967
    node_1171 --> node_1047
    node_1091 --> node_1047
    node_948 --> node_135
    node_100 --> node_966
    node_687 --> node_251
    node_910 --> node_1279
    node_497 --> node_1026
    node_946 --> node_945
    node_632 --> node_1188
    node_520 --> node_37
    node_0 --> node_1188
    node_541 --> node_1326
    node_595 --> node_587
    node_593 --> node_138
    node_687 --> node_246
    node_541 --> node_677
    node_130 --> node_58
    node_1103 --> node_967
    node_276 --> node_1280
    node_12 --> node_659
    node_632 --> node_1005
    node_523 --> node_240
    node_145 --> node_20
    node_525 --> node_1006
    node_632 --> node_1023
    node_514 --> node_250
    node_0 --> node_1023
    node_911 --> node_1291
    node_1023 --> node_1022
    node_505 --> node_487
    node_641 --> node_998
    node_541 --> node_1207
    node_189 --> node_190
    node_920 --> node_187
    node_1314 --> node_1118
    node_63 --> node_229
    node_520 --> node_784
    node_1314 --> node_1185
    node_50 --> node_166
    node_205 --> node_261
    node_411 --> node_209
    node_520 --> node_1157
    node_911 --> node_187
    node_632 --> node_1200
    node_103 --> node_177
    node_98 --> node_97
    node_0 --> node_1200
    node_1117 --> node_187
    node_511 --> node_543
    node_929 --> node_1238
    node_666 --> node_1343
    node_525 --> node_1174
    node_103 --> node_742
    node_67 --> node_739
    node_229 --> node_328
    node_751 --> node_617
    node_861 --> node_620
    node_1097 --> node_1332
    node_629 --> node_1101
    node_1077 --> node_238
    node_5 --> node_1327
    node_575 --> node_795
    node_486 --> node_1083
    node_37 --> node_250
    node_1055 --> node_67
    node_525 --> node_1031
    node_12 --> node_674
    node_632 --> node_1341
    node_599 --> node_1313
    node_631 --> node_668
    node_330 --> node_29
    node_31 --> node_614
    node_666 --> node_1291
    node_841 --> node_245
    node_559 --> node_188
    node_530 --> node_336
    node_449 --> node_595
    node_659 --> node_1237
    node_599 --> node_135
    node_1230 --> node_1027
    node_64 --> node_229
    node_869 --> node_1288
    node_1101 --> node_1358
    node_68 --> node_328
    node_1097 --> node_1230
    node_1251 --> node_1243
    node_541 --> node_954
    node_861 --> node_948
    node_648 --> node_178
    node_720 --> node_717
    node_681 --> node_320
    node_1339 --> node_1220
    node_632 --> node_178
    node_205 --> node_398
    node_1339 --> node_1121
    node_106 --> node_1043
    node_636 --> node_1347
    node_1314 --> node_1332
    node_643 --> node_1324
    node_935 --> node_1007
    node_520 --> node_1093
    node_1339 --> node_1147
    node_781 --> node_334
    node_187 --> node_281
    node_497 --> node_1066
    node_465 --> node_1082
    node_632 --> node_1118
    node_0 --> node_1118
    node_474 --> node_1260
    node_1331 --> node_1233
    node_541 --> node_703
    node_1360 --> node_331
    node_489 --> node_399
    node_1117 --> node_75
    node_52 --> node_29
    node_1230 --> node_1357
    node_449 --> node_1046
    node_543 --> node_340
    node_874 --> node_1272
    node_497 --> node_37
    node_855 --> node_1148
    node_68 --> node_326
    node_105 --> node_72
    node_106 --> node_997
    node_456 --> node_1291
    node_284 --> node_279
    node_540 --> node_582
    node_142 --> node_1313
    node_666 --> node_1077
    node_31 --> node_1213
    node_1081 --> node_35
    node_177 --> node_175
    node_62 --> node_250
    node_449 --> node_1078
    node_1362 --> node_994
    node_960 --> node_959
    node_984 --> node_1047
    node_206 --> node_1262
    node_1077 --> node_1078
    node_708 --> node_1082
    node_772 --> node_1095
    node_19 --> node_282
    node_575 --> node_1254
    node_497 --> node_1157
    node_1081 --> node_232
    node_205 --> node_1287
    node_7 --> node_67
    node_658 --> node_1249
    node_459 --> node_187
    node_1166 --> node_1164
    node_695 --> node_307
    node_739 --> node_72
    node_1230 --> node_1020
    node_520 --> node_620
    node_520 --> node_1140
    node_1300 --> node_57
    node_520 --> node_1041
    node_102 --> node_1347
    node_599 --> node_50
    node_240 --> node_239
    node_64 --> node_37
    node_525 --> node_1319
    node_5 --> node_837
    node_187 --> node_267
    node_105 --> node_233
    node_595 --> node_588
    node_659 --> node_1235
    node_231 --> node_226
    node_475 --> node_695
    node_541 --> node_1027
    node_63 --> node_334
    node_632 --> node_1332
    node_773 --> node_72
    node_593 --> node_1128
    node_855 --> node_695
    node_463 --> node_201
    node_99 --> node_911
    node_903 --> node_279
    node_489 --> node_574
    node_64 --> node_784
    node_281 --> node_279
    node_751 --> node_650
    node_449 --> node_667
    node_911 --> node_35
    node_1314 --> node_1324
    node_1230 --> node_1081
    node_104 --> node_233
    node_1117 --> node_35
    node_187 --> node_1282
    node_772 --> node_795
    node_5 --> node_3
    node_739 --> node_233
    node_487 --> node_221
    node_543 --> node_215
    node_632 --> node_1230
    node_0 --> node_1230
    node_520 --> node_1214
    node_575 --> node_683
    node_527 --> node_1001
    node_225 --> node_216
    node_497 --> node_1093
    node_1083 --> node_741
    node_1230 --> node_1194
    node_1260 --> node_221
    node_1231 --> node_1326
    node_205 --> node_400
    node_954 --> node_955
    node_64 --> node_334
    node_666 --> node_1344
    node_653 --> node_1091
    node_773 --> node_233
    node_559 --> node_238
    node_152 --> node_29
    node_665 --> node_1304
    node_497 --> node_632
    node_781 --> node_948
    node_251 --> node_252
    node_543 --> node_5
    node_1102 --> node_187
    node_954 --> node_956
    node_613 --> node_615
    node_861 --> node_240
    node_556 --> node_82
    node_541 --> node_68
    node_232 --> node_72
    node_541 --> node_1257
    node_507 --> node_188
    node_490 --> node_188
    node_507 --> node_493
    node_263 --> node_67
    node_668 --> node_1130
    node_1177 --> node_1179
    node_506 --> node_1262
    node_107 --> node_58
    node_511 --> node_1261
    node_205 --> node_392
    node_541 --> node_1020
    node_63 --> node_487
    node_525 --> node_1121
    node_19 --> node_213
    node_575 --> node_244
    node_31 --> node_3
    node_5 --> node_510
    node_497 --> node_626
    node_520 --> node_1173
    node_497 --> node_620
    node_537 --> node_1176
    node_661 --> node_1017
    node_1102 --> node_57
    node_497 --> node_1041
    node_316 --> node_739
    node_187 --> node_419
    node_303 --> node_607
    node_632 --> node_1324
    node_653 --> node_1030
    node_934 --> node_1181
    node_666 --> node_1282
    node_1015 --> node_1208
    node_99 --> node_617
    node_489 --> node_398
    node_1097 --> node_1186
    node_666 --> node_1123
    node_105 --> node_97
    node_525 --> node_1035
    node_0 --> node_1299
    node_229 --> node_488
    node_767 --> node_178
    node_541 --> node_570
    node_1015 --> node_1238
    node_1305 --> node_1304
    node_497 --> node_1065
    node_666 --> node_1059
    node_772 --> node_1254
    node_165 --> node_69
    node_5 --> node_852
    node_1230 --> node_1239
    node_983 --> node_1047
    node_263 --> node_181
    node_851 --> node_138
    node_666 --> node_1058
    node_63 --> node_948
    node_1097 --> node_1353
    node_112 --> node_136
    node_135 --> node_58
    node_827 --> node_1289
    node_459 --> node_35
    node_195 --> node_35
    node_1188 --> node_1189
    node_541 --> node_209
    node_53 --> node_69
    node_64 --> node_620
    node_519 --> node_645
    node_658 --> node_1178
    node_559 --> node_1078
    node_751 --> node_746
    node_56 --> node_1252
    node_276 --> node_391
    node_1304 --> node_1099
    node_666 --> node_1085
    node_20 --> node_1095
    node_151 --> node_241
    node_5 --> node_1017
    node_497 --> node_1214
    node_497 --> node_1314
    node_410 --> node_221
    node_151 --> node_731
    node_923 --> node_741
    node_1097 --> node_1330
    node_911 --> node_1283
    node_742 --> node_731
    node_923 --> node_203
    node_733 --> node_732
    node_771 --> node_271
    node_502 --> node_36
    node_543 --> node_628
    node_499 --> node_739
    node_1261 --> node_217
    node_105 --> node_188
    node_656 --> node_1011
    node_5 --> node_366
    node_5 --> node_782
    node_19 --> node_1268
    node_1230 --> node_1362
    node_489 --> node_1287
    node_1082 --> node_243
    node_934 --> node_1015
    node_489 --> node_181
    node_100 --> node_911
    node_1117 --> node_585
    node_64 --> node_948
    node_489 --> node_1148
    node_669 --> node_1314
    node_1314 --> node_1353
    node_489 --> node_211
    node_449 --> node_720
    node_1359 --> node_310
    node_154 --> node_250
    node_541 --> node_1195
    node_668 --> node_1132
    node_962 --> node_33
    node_863 --> node_353
    node_669 --> node_1074
    node_479 --> node_1289
    node_367 --> node_415
    node_642 --> node_1013
    node_1359 --> node_191
    node_272 --> node_271
    node_1097 --> node_1166
    node_559 --> node_328
    node_666 --> node_1283
    node_1300 --> node_1085
    node_541 --> node_490
    node_541 --> node_1337
    node_599 --> node_1021
    node_1069 --> node_630
    node_223 --> node_213
    node_5 --> node_1301
    node_1314 --> node_1330
    node_416 --> node_617
    node_643 --> node_1067
    node_152 --> node_58
    node_3 --> node_271
    node_1312 --> node_249
    node_231 --> node_224
    node_520 --> node_1156
    node_486 --> node_191
    node_331 --> node_734
    node_490 --> node_518
    node_5 --> node_1290
    node_31 --> node_177
    node_402 --> node_200
    node_205 --> node_411
    node_525 --> node_67
    node_599 --> node_2
    node_541 --> node_928
    node_525 --> node_1335
    node_1097 --> node_1326
    node_520 --> node_1122
    node_106 --> node_606
    node_20 --> node_746
    node_541 --> node_766
    node_187 --> node_194
    node_205 --> node_378
    node_218 --> node_211
    node_151 --> node_328
    node_424 --> node_425
    node_12 --> node_654
    node_541 --> node_1080
    node_526 --> node_1284
    node_65 --> node_72
    node_742 --> node_328
    node_704 --> node_708
    node_772 --> node_244
    node_777 --> node_183
    node_531 --> node_695
    node_58 --> node_67
    node_301 --> node_309
    node_5 --> node_1087
    node_632 --> node_1186
    node_489 --> node_400
    node_0 --> node_1186
    node_694 --> node_256
    node_1097 --> node_1207
    node_200 --> node_204
    node_541 --> node_1300
    node_1314 --> node_1166
    node_525 --> node_1037
    node_636 --> node_1346
    node_695 --> node_739
    node_834 --> node_285
    node_99 --> node_650
    node_1230 --> node_1184
    node_497 --> node_651
    node_563 --> node_665
    node_541 --> node_943
    node_1308 --> node_1306
    node_1362 --> node_1360
    node_499 --> node_950
    node_669 --> node_175
    node_520 --> node_1356
    node_361 --> node_203
    node_1077 --> node_1079
    node_1077 --> node_488
    node_632 --> node_1353
    node_0 --> node_1353
    node_64 --> node_20
    node_1314 --> node_1231
    node_529 --> node_995
    node_656 --> node_1239
    node_683 --> node_3
    node_5 --> node_370
    node_599 --> node_720
    node_1231 --> node_1173
    node_449 --> node_48
    node_781 --> node_490
    node_100 --> node_617
    node_519 --> node_12
    node_187 --> node_1127
    node_541 --> node_741
    node_449 --> node_16
    node_1145 --> node_1350
    node_520 --> node_1192
    node_541 --> node_975
    node_601 --> node_27
    node_922 --> node_1061
    node_1097 --> node_1057
    node_710 --> node_187
    node_1230 --> node_1155
    node_19 --> node_574
    node_541 --> node_1267
    node_65 --> node_233
    node_541 --> node_203
    node_1260 --> node_1285
    node_521 --> node_1148
    node_632 --> node_1330
    node_666 --> node_1274
    node_0 --> node_1330
    node_5 --> node_708
    node_1148 --> node_1149
    node_1231 --> node_1257
    node_12 --> node_669
    node_706 --> node_712
    node_972 --> node_1102
    node_929 --> node_1233
    node_898 --> node_271
    node_599 --> node_1095
    node_1314 --> node_1207
    node_205 --> node_379
    node_525 --> node_1185
    node_145 --> node_533
    node_19 --> node_402
    node_817 --> node_562
    node_781 --> node_766
    node_68 --> node_20
    node_1339 --> node_1154
    node_1266 --> node_1350
    node_489 --> node_198
    node_283 --> node_279
    node_78 --> node_73
    node_1102 --> node_1085
    node_629 --> node_1108
    node_520 --> node_1340
    node_489 --> node_382
    node_328 --> node_327
    node_253 --> node_739
    node_1045 --> node_232
    node_1117 --> node_242
    node_672 --> node_1310
    node_497 --> node_1060
    node_489 --> node_705
    node_1260 --> node_405
    node_142 --> node_253
    node_970 --> node_998
    node_1133 --> node_1136
    node_632 --> node_1166
    node_0 --> node_1166
    node_475 --> node_1260
    node_669 --> node_1354
    node_781 --> node_943
    node_234 --> node_72
    node_1314 --> node_1057
    node_855 --> node_1260
    node_525 --> node_1309
    node_540 --> node_3
    node_718 --> node_638
    node_468 --> node_209
    node_1339 --> node_1349
    node_971 --> node_985
    node_497 --> node_1122
    node_41 --> node_138
    node_20 --> node_67
    node_541 --> node_1024
    node_533 --> node_741
    node_520 --> node_1232
    node_521 --> node_695
    node_63 --> node_490
    node_187 --> node_186
    node_205 --> node_372
    node_935 --> node_1234
    node_660 --> node_1209
    node_1147 --> node_191
    node_541 --> node_1184
    node_666 --> node_1127
    node_599 --> node_795
    node_1154 --> node_1150
    node_127 --> node_241
    node_541 --> node_1169
    node_1101 --> node_1099
    node_0 --> node_1326
    node_1261 --> node_212
    node_127 --> node_731
    node_663 --> node_1321
    node_19 --> node_369
    node_187 --> node_1262
    node_997 --> node_998
    node_67 --> node_132
    node_253 --> node_254
    node_948 --> node_945
    node_31 --> node_1082
    node_497 --> node_1356
    node_1230 --> node_1097
    node_505 --> node_72
    node_530 --> node_271
    node_520 --> node_681
    node_1222 --> node_1221
    node_632 --> node_1207
    node_0 --> node_1207
    node_866 --> node_187
    node_63 --> node_766
    node_234 --> node_233
    node_541 --> node_1212
    node_600 --> node_27
    node_99 --> node_1170
    node_497 --> node_1034
    node_105 --> node_731
    node_1352 --> node_1313
    node_541 --> node_486
    node_497 --> node_1192
    node_1230 --> node_1153
    node_278 --> node_275
    node_1339 --> node_1318
    node_1219 --> node_1217
    node_1362 --> node_974
    node_392 --> node_181
    node_416 --> node_1095
    node_1267 --> node_221
    node_541 --> node_1143
    node_1097 --> node_1027
    node_5 --> node_376
    node_1231 --> node_1195
    node_1359 --> node_335
    node_205 --> node_383
    node_668 --> node_1134
    node_520 --> node_1201
    node_562 --> node_589
    node_666 --> node_1172
    node_790 --> node_695
    node_719 --> node_703
    node_1117 --> node_1262
    node_301 --> node_311
    node_632 --> node_1057
    node_1301 --> node_1037
    node_502 --> node_1302
    node_0 --> node_1057
    node_145 --> node_1138
    node_20 --> node_546
    node_100 --> node_650
    node_775 --> node_221
    node_520 --> node_350
    node_103 --> node_962
    node_1015 --> node_1356
    node_739 --> node_731
    node_497 --> node_1340
    node_505 --> node_233
    node_1304 --> node_1075
    node_7 --> node_697
    node_19 --> node_374
    node_520 --> node_1102
    node_489 --> node_58
    node_787 --> node_234
    node_497 --> node_1045
    node_1097 --> node_1357
    node_559 --> node_488
    node_497 --> node_1036
    node_710 --> node_35
    node_1117 --> node_225
    node_1231 --> node_1015
    node_423 --> node_440
    node_666 --> node_1262
    node_1260 --> node_410
    node_205 --> node_356
    node_922 --> node_240
    node_314 --> node_607
    node_773 --> node_731
    node_5 --> node_368
    node_179 --> node_357
    node_710 --> node_699
    node_1230 --> node_1342
    node_599 --> node_1254
    node_19 --> node_1148
    node_113 --> node_133
    node_699 --> node_187
    node_31 --> node_969
    node_774 --> node_267
    node_489 --> node_349
    node_1362 --> node_238
    node_66 --> node_72
    node_497 --> node_1232
    node_331 --> node_696
    node_1267 --> node_974
    node_1231 --> node_1300
    node_541 --> node_72
    node_930 --> node_1011
    node_595 --> node_551
    node_781 --> node_486
    node_197 --> node_205
    node_666 --> node_1174
    node_807 --> node_384
    node_105 --> node_328
    node_523 --> node_98
    node_1081 --> node_253
    node_58 --> node_132
    node_964 --> node_1015
    node_103 --> node_114
    node_541 --> node_1097
    node_416 --> node_746
    node_0 --> node_986
    node_1147 --> node_251
    node_187 --> node_739
    node_1230 --> node_1352
    node_122 --> node_741
    node_1097 --> node_1020
    node_523 --> node_135
    node_106 --> node_329
    node_935 --> node_1136
    node_497 --> node_681
    node_840 --> node_278
    node_511 --> node_3
    node_277 --> node_279
    node_655 --> node_1169
    node_1314 --> node_1357
    node_520 --> node_187
    node_665 --> node_1109
    node_575 --> node_737
    node_449 --> node_1354
    node_520 --> node_1323
    node_1231 --> node_1267
    node_541 --> node_1329
    node_629 --> node_1111
    node_1230 --> node_1029
    node_510 --> node_183
    node_739 --> node_328
    node_1230 --> node_1235
    node_170 --> node_74
    node_66 --> node_233
    node_1233 --> node_3
    node_68 --> node_124
    node_541 --> node_233
    node_159 --> node_69
    node_225 --> node_226
    node_205 --> node_352
    node_1117 --> node_680
    node_19 --> node_695
    node_153 --> node_58
    node_232 --> node_731
    node_5 --> node_1047
    node_497 --> node_1201
    node_751 --> node_1043
    node_1117 --> node_739
    node_1097 --> node_1081
    node_5 --> node_1117
    node_1267 --> node_238
    node_19 --> node_589
    node_520 --> node_57
    node_773 --> node_328
    node_935 --> node_1016
    node_474 --> node_1082
    node_632 --> node_1027
    node_0 --> node_1027
    node_1260 --> node_397
    node_486 --> node_487
    node_104 --> node_122
    node_5 --> node_1083
    node_972 --> node_232
    node_1352 --> node_1046
    node_187 --> node_1289
    node_1015 --> node_1090
    node_1044 --> node_1048
    node_457 --> node_187
    node_62 --> node_203
    node_557 --> node_1047
    node_497 --> node_1141
    node_656 --> node_1237
    node_1347 --> node_1047
    node_1362 --> node_1078
    node_625 --> node_176
    node_106 --> node_742
    node_751 --> node_997
    node_31 --> node_1170
    node_100 --> node_1170
    node_960 --> node_957
    node_1291 --> node_1262
    node_1231 --> node_1024
    node_525 --> node_1325
    node_774 --> node_283
    node_205 --> node_421
    node_864 --> node_1294
    node_575 --> node_614
    node_519 --> node_187
    node_1231 --> node_1098
    node_164 --> node_248
    node_599 --> node_244
    node_1090 --> node_1089
    node_531 --> node_1260
    node_599 --> node_331
    node_861 --> node_1138
    node_632 --> node_1357
    node_1314 --> node_1081
    node_1230 --> node_1042
    node_646 --> node_1079
    node_1230 --> node_1205
    node_1231 --> node_1169
    node_5 --> node_799
    node_669 --> node_1141
    node_5 --> node_531
    node_1230 --> node_1146
    node_19 --> node_198
    node_910 --> node_429
    node_1097 --> node_1195
    node_599 --> node_1354
    node_666 --> node_1319
    node_1117 --> node_208
    node_1314 --> node_1194
    node_113 --> node_547
    node_913 --> node_1148
    node_593 --> node_331
    node_1231 --> node_1212
    node_232 --> node_328
    node_1251 --> node_1047
    node_525 --> node_1336
    node_541 --> node_1084
    node_1230 --> node_1132
    node_205 --> node_354
    node_0 --> node_1257
    node_68 --> node_61
    node_629 --> node_1112
    node_541 --> node_1235
    node_559 --> node_175
    node_497 --> node_1323
    node_632 --> node_1020
    node_1267 --> node_1078
    node_699 --> node_35
    node_1231 --> node_1143
    node_0 --> node_1020
    node_1196 --> node_1047
    node_1221 --> node_739
    node_642 --> node_1014
    node_205 --> node_404
    node_512 --> node_1284
    node_861 --> node_947
    node_525 --> node_1094
    node_1097 --> node_1239
    node_575 --> node_1213
    node_423 --> node_430
    node_104 --> node_64
    node_666 --> node_1222
    node_541 --> node_1310
    node_489 --> node_968
    node_575 --> node_31
    node_908 --> node_1280
    node_662 --> node_1236
    node_489 --> node_356
    node_1101 --> node_1075
    node_497 --> node_711
    node_570 --> node_564
    node_1097 --> node_1300
    node_658 --> node_1176
    node_520 --> node_1344
    node_1117 --> node_318
    node_1360 --> node_307
    node_1230 --> node_1092
    node_1037 --> node_1298
    node_656 --> node_1235
    node_720 --> node_716
    node_772 --> node_737
    node_629 --> node_1113
    node_562 --> node_582
    node_520 --> node_35
    node_632 --> node_1081
    node_0 --> node_1081
    node_500 --> node_739
    node_497 --> node_730
    node_497 --> node_1077
    node_1339 --> node_1327
    node_639 --> node_668
    node_912 --> node_1291
    node_103 --> node_229
    node_1314 --> node_1017
    node_173 --> node_69
    node_652 --> node_1015
    node_103 --> node_115
    node_229 --> node_187
    node_541 --> node_600
    node_520 --> node_1126
    node_333 --> node_25
    node_632 --> node_1194
    node_5 --> node_892
    node_521 --> node_1260
    node_1314 --> node_1239
    node_851 --> node_593
    node_3 --> node_550
    node_541 --> node_1042
    node_1230 --> node_974
    node_65 --> node_731
    node_575 --> node_1
    node_106 --> node_960
    node_934 --> node_1013
    node_1097 --> node_1267
    node_541 --> node_188
    node_1041 --> node_250
    node_795 --> node_1148
    node_276 --> node_345
    node_687 --> node_1083
    node_526 --> node_387
    node_449 --> node_681
    node_541 --> node_1206
    node_526 --> node_241
    node_1221 --> node_1222
    node_575 --> node_690
    node_541 --> node_346
    node_666 --> node_1119
    node_526 --> node_731
    node_528 --> node_67
    node_1230 --> node_1312
    node_935 --> node_1012
    node_541 --> node_406
    node_643 --> node_1320
    node_457 --> node_35
    node_19 --> node_58
    node_490 --> node_534
    node_1339 --> node_1307
    node_525 --> node_1231
    node_31 --> node_952
    node_541 --> node_1132
    node_665 --> node_1213
    node_541 --> node_709
    node_595 --> node_563
    node_861 --> node_135
    node_274 --> node_183
    node_520 --> node_1059
    node_887 --> node_356
    node_772 --> node_614
    node_0 --> node_1195
    node_1231 --> node_1329
    node_174 --> node_69
    node_781 --> node_1138
    node_1314 --> node_1362
    node_561 --> node_631
    node_64 --> node_533
    node_951 --> node_950
    node_519 --> node_35
    node_629 --> node_1117
    node_525 --> node_1167
    node_19 --> node_349
    node_1299 --> node_1298
    node_541 --> node_1013
    node_666 --> node_1125
    node_790 --> node_1260
    node_5 --> node_1236
    node_520 --> node_1085
    node_1339 --> node_1191
    node_1339 --> node_1030
    node_330 --> node_734
    node_1230 --> node_238
    node_1246 --> node_1248
    node_31 --> node_290
    node_599 --> node_767
    node_1258 --> node_1047
    node_795 --> node_695
    node_800 --> node_369
    node_1097 --> node_1184
    node_751 --> node_677
    node_489 --> node_200
    node_1009 --> node_1047
    node_579 --> node_33
    node_497 --> node_1116
    node_23 --> node_222
    node_1097 --> node_1169
    node_99 --> node_1043
    node_497 --> node_1344
    node_632 --> node_1239
    node_875 --> node_418
    node_65 --> node_328
    node_139 --> node_122
    node_52 --> node_247
    node_5 --> node_1230
    node_5 --> node_1133
    node_511 --> node_205
    node_575 --> node_3
    node_179 --> node_365
    node_893 --> node_209
    node_1339 --> node_1225
    node_1351 --> node_1350
    node_154 --> node_203
    node_711 --> node_712
    node_1127 --> node_1128
    node_511 --> node_1082
    node_526 --> node_328
    node_103 --> node_784
    node_234 --> node_731
    node_497 --> node_624
    node_0 --> node_1300
    node_1231 --> node_1223
    node_5 --> node_704
    node_1097 --> node_1212
    node_541 --> node_1068
    node_178 --> node_175
    node_31 --> node_962
    node_514 --> node_36
    node_772 --> node_1213
    node_31 --> node_995
    node_58 --> node_133
    node_187 --> node_1287
    node_772 --> node_31
    node_935 --> node_1131
    node_99 --> node_997
    node_305 --> node_309
    node_63 --> node_1138
    node_541 --> node_1312
    node_569 --> node_598
    node_563 --> node_12
    node_1261 --> node_1148
    node_191 --> node_247
    node_68 --> node_66
    node_103 --> node_334
    node_1045 --> node_253
    node_0 --> node_1267
    node_954 --> node_958
    node_642 --> node_1008
    node_497 --> node_1123
    node_179 --> node_1276
    node_1203 --> node_67
    node_58 --> node_120
    node_920 --> node_1148
    node_541 --> node_518
    node_229 --> node_35
    node_751 --> node_954
    node_205 --> node_366
    node_505 --> node_1046
    node_525 --> node_1327
    node_102 --> node_144
    node_497 --> node_1059
    node_106 --> node_51
    node_20 --> node_737
    node_1230 --> node_1078
    node_1251 --> node_1242
    node_5 --> node_387
    node_5 --> node_1280
    node_911 --> node_1148
    node_815 --> node_209
    node_5 --> node_241
    node_631 --> node_656
    node_751 --> node_606
    node_669 --> node_1038
    node_1314 --> node_1155
    node_1318 --> node_999
    node_599 --> node_1261
    node_840 --> node_75
    node_177 --> node_176
    node_308 --> node_332
    node_64 --> node_1138
    node_449 --> node_711
    node_595 --> node_62
    node_5 --> node_1299
    node_19 --> node_1260
    node_666 --> node_1037
    node_1117 --> node_211
    node_229 --> node_232
    node_1362 --> node_488
    node_505 --> node_1078
    node_1231 --> node_1310
    node_20 --> node_968
    node_1167 --> node_1011
    node_1230 --> node_1298
    node_1230 --> node_1218
    node_234 --> node_328
    node_449 --> node_730
    node_779 --> node_189
    node_1339 --> node_1040
    node_1230 --> node_1363
    node_187 --> node_400
    node_666 --> node_1287
    node_145 --> node_1021
    node_497 --> node_1069
    node_720 --> node_718
    node_142 --> node_58
    node_1261 --> node_695
    node_543 --> node_1047
    node_541 --> node_595
    node_541 --> node_1128
    node_1015 --> node_1347
    node_5 --> node_496
    node_1339 --> node_1226
    node_1339 --> node_1219
    node_5 --> node_191
    node_447 --> node_428
    node_656 --> node_1009
    node_229 --> node_738
    node_697 --> node_330
    node_632 --> node_1184
    node_456 --> node_67
    node_487 --> node_183
    node_1275 --> node_1293
    node_0 --> node_1184
    node_1060 --> node_1061
    node_920 --> node_695
    node_976 --> node_72
    node_663 --> node_1297
    node_0 --> node_1169
    node_246 --> node_250
    node_449 --> node_966
    node_631 --> node_663
    node_145 --> node_64
    node_514 --> node_290
    node_1097 --> node_1153
    node_20 --> node_614
    node_1230 --> node_1198
    node_669 --> node_1069
    node_124 --> node_739
    node_575 --> node_177
    node_528 --> node_675
    node_769 --> node_1148
    node_971 --> node_1234
    node_187 --> node_363
    node_103 --> node_620
    node_1103 --> node_227
    node_1231 --> node_1206
    node_693 --> node_198
    node_855 --> node_708
    node_142 --> node_1261
    node_632 --> node_1212
    node_1267 --> node_488
    node_585 --> node_675
    node_0 --> node_1212
    node_1312 --> node_191
    node_541 --> node_1046
    node_943 --> node_939
    node_63 --> node_1313
    node_632 --> node_1155
    node_497 --> node_1225
    node_497 --> node_585
    node_490 --> node_542
    node_606 --> node_1084
    node_541 --> node_1294
    node_665 --> node_1108
    node_475 --> node_1082
    node_1256 --> node_1165
    node_100 --> node_1043
    node_578 --> node_50
    node_855 --> node_1082
    node_687 --> node_238
    node_34 --> node_799
    node_541 --> node_1078
    node_253 --> node_250
    node_976 --> node_233
    node_1133 --> node_1135
    node_1117 --> node_228
    node_636 --> node_1180
    node_1133 --> node_1137
    node_103 --> node_948
    node_481 --> node_273
    node_19 --> node_389
    node_1314 --> node_1153
    node_459 --> node_1148
    node_1231 --> node_1013
    node_546 --> node_115
    node_846 --> node_676
    node_541 --> node_1298
    node_1224 --> node_1047
    node_997 --> node_996
    node_305 --> node_311
    node_145 --> node_1095
    node_100 --> node_997
    node_1331 --> node_985
    node_20 --> node_1213
    node_769 --> node_695
    node_695 --> node_697
    node_541 --> node_1363
    node_20 --> node_31
    node_1319 --> node_1315
    node_56 --> node_1163
    node_500 --> node_809
    node_656 --> node_1010
    node_631 --> node_666
    node_500 --> node_469
    node_520 --> node_511
    node_599 --> node_737
    node_1090 --> node_1047
    node_1206 --> node_67
    node_449 --> node_232
    node_99 --> node_677
    node_134 --> node_58
    node_7 --> node_336
    node_751 --> node_68
    node_1077 --> node_232
    node_541 --> node_667
    node_559 --> node_187
    node_5 --> node_872
    node_546 --> node_565
    node_1231 --> node_1068
    node_511 --> node_1083
    node_1236 --> node_1239
    node_1314 --> node_1342
    node_1230 --> node_1066
    node_541 --> node_1026
    node_1231 --> node_1019
    node_1162 --> node_1159
    node_1097 --> node_1029
    node_410 --> node_183
    node_449 --> node_65
    node_282 --> node_224
    node_632 --> node_1097
    node_1097 --> node_1235
    node_625 --> node_178
    node_0 --> node_1097
    node_631 --> node_643
    node_1117 --> node_202
    node_541 --> node_591
    node_861 --> node_1021
    node_145 --> node_795
    node_854 --> node_267
    node_1251 --> node_1247
    node_497 --> node_1226
    node_38 --> node_42
    node_1231 --> node_1256
    node_558 --> node_324
    node_665 --> node_1362
    node_632 --> node_1153
    node_505 --> node_990
    node_1117 --> node_190
    node_522 --> node_241
    node_1314 --> node_1352
    node_476 --> node_187
    node_497 --> node_633
    node_514 --> node_1302
    node_520 --> node_1006
    node_669 --> node_1040
    node_1081 --> node_52
    node_972 --> node_253
    node_1209 --> node_1208
    node_1102 --> node_1148
    node_205 --> node_1284
    node_1230 --> node_1157
    node_663 --> node_1322
    node_1117 --> node_192
    node_599 --> node_614
    node_205 --> node_1292
    node_499 --> node_27
    node_543 --> node_649
    node_772 --> node_177
    node_489 --> node_279
    node_695 --> node_628
    node_1314 --> node_1029
    node_5 --> node_401
    node_520 --> node_1174
    node_99 --> node_954
    node_56 --> node_1209
    node_520 --> node_1197
    node_63 --> node_1046
    node_37 --> node_1302
    node_31 --> node_951
    node_781 --> node_667
    node_520 --> node_1031
    node_99 --> node_606
    node_1081 --> node_250
    node_5 --> node_357
    node_19 --> node_283
    node_1097 --> node_1042
    node_795 --> node_1260
    node_1339 --> node_1227
    node_731 --> node_1128
    node_922 --> node_98
    node_1097 --> node_1146
    node_52 --> node_36
    node_1097 --> node_1206
    node_5 --> node_1326
    node_861 --> node_720
    node_711 --> node_704
    node_563 --> node_187
    node_422 --> node_200
    node_575 --> node_650
    node_130 --> node_241
    node_1260 --> node_1291
    node_1192 --> node_1190
    node_1352 --> node_1354
    node_537 --> node_1346
    node_20 --> node_3
    node_502 --> node_183
    node_525 --> node_1017
    node_935 --> node_1137
    node_1102 --> node_695
    node_667 --> node_659
    node_1117 --> node_180
    node_716 --> node_1047
    node_934 --> node_1014
    node_1097 --> node_1132
    node_12 --> node_658
    node_541 --> node_1066
    node_614 --> node_616
    node_681 --> node_680
    node_1230 --> node_1093
    node_647 --> node_1101
    node_861 --> node_1095
    node_106 --> node_1003
    node_541 --> node_882
    node_145 --> node_1254
    node_497 --> node_1211
    node_751 --> node_1337
    node_1304 --> node_967
    node_665 --> node_1111
    node_541 --> node_37
    node_575 --> node_49
    node_541 --> node_410
    node_79 --> node_733
    node_1081 --> node_246
    node_1055 --> node_1047
    node_563 --> node_655
    node_489 --> node_370
    node_1314 --> node_1205
    node_1230 --> node_488
    node_502 --> node_741
    node_669 --> node_1350
    node_180 --> node_1280
    node_695 --> node_27
    node_191 --> node_36
    node_1314 --> node_1146
    node_575 --> node_969
    node_632 --> node_1029
    node_0 --> node_1029
    node_720 --> node_714
    node_632 --> node_1235
    node_63 --> node_667
    node_0 --> node_1235
    node_663 --> node_1324
    node_497 --> node_617
    node_669 --> node_176
    node_1117 --> node_250
    node_497 --> node_1006
    node_541 --> node_1157
    node_764 --> node_686
    node_559 --> node_35
    node_740 --> node_739
    node_751 --> node_742
    node_31 --> node_677
    node_1314 --> node_1132
    node_106 --> node_114
    node_693 --> node_1002
    node_100 --> node_677
    node_103 --> node_490
    node_525 --> node_1301
    node_187 --> node_1149
    node_525 --> node_1362
    node_0 --> node_1310
    node_599 --> node_1
    node_313 --> node_290
    node_1230 --> node_1140
    node_129 --> node_73
    node_531 --> node_1082
    node_720 --> node_713
    node_781 --> node_1021
    node_1061 --> node_12
    node_489 --> node_1082
    node_1230 --> node_1041
    node_652 --> node_1013
    node_559 --> node_232
    node_861 --> node_795
    node_31 --> node_334
    node_743 --> node_739
    node_63 --> node_122
    node_497 --> node_1174
    node_497 --> node_1088
    node_646 --> node_1077
    node_930 --> node_1009
    node_537 --> node_205
    node_489 --> node_1281
    node_520 --> node_1319
    node_5 --> node_999
    node_497 --> node_1031
    node_499 --> node_3
    node_179 --> node_1288
    node_543 --> node_241
    node_541 --> node_313
    node_251 --> node_247
    node_395 --> node_1280
    node_543 --> node_731
    node_1093 --> node_1091
    node_5 --> node_487
    node_1117 --> node_215
    node_810 --> node_396
    node_1261 --> node_1260
    node_1267 --> node_1266
    node_525 --> node_1087
    node_781 --> node_64
    node_892 --> node_209
    node_751 --> node_975
    node_1097 --> node_1312
    node_102 --> node_1252
    node_1314 --> node_1092
    node_537 --> node_680
    node_627 --> node_1185
    node_413 --> node_35
    node_516 --> node_389
    node_632 --> node_1042
    node_632 --> node_1205
    node_1312 --> node_1311
    node_0 --> node_1042
    node_1266 --> node_1144
    node_692 --> node_67
    node_416 --> node_1213
    node_595 --> node_600
    node_1076 --> node_1358
    node_632 --> node_1146
    node_541 --> node_1093
    node_920 --> node_1260
    node_922 --> node_1127
    node_416 --> node_31
    node_0 --> node_1206
    node_1230 --> node_1214
    node_1231 --> node_1026
    node_68 --> node_139
    node_520 --> node_1095
    node_1230 --> node_1314
    node_31 --> node_10
    node_663 --> node_1025
    node_99 --> node_68
    node_275 --> node_279
    node_602 --> node_19
    node_575 --> node_1170
    node_903 --> node_300
    node_523 --> node_29
    node_145 --> node_244
    node_100 --> node_954
    node_20 --> node_177
    node_362 --> node_405
    node_541 --> node_320
    node_632 --> node_1132
    node_781 --> node_720
    node_0 --> node_1132
    node_63 --> node_1021
    node_100 --> node_606
    node_205 --> node_375
    node_918 --> node_1289
    node_1231 --> node_1197
    node_449 --> node_911
    node_599 --> node_3
    node_672 --> node_1034
    node_541 --> node_48
    node_563 --> node_35
    node_461 --> node_403
    node_1261 --> node_1264
    node_1148 --> node_221
    node_710 --> node_1148
    node_497 --> node_644
    node_0 --> node_1013
    node_655 --> node_1168
    node_861 --> node_1254
    node_665 --> node_1113
    node_911 --> node_871
    node_695 --> node_3
    node_1041 --> node_203
    node_543 --> node_328
    node_19 --> node_416
    node_521 --> node_1082
    node_799 --> node_366
    node_930 --> node_1010
    node_520 --> node_1121
    node_1236 --> node_1237
    node_677 --> node_675
    node_104 --> node_103
    node_478 --> node_209
    node_520 --> node_795
    node_632 --> node_1092
    node_222 --> node_22
    node_656 --> node_1238
    node_772 --> node_969
    node_751 --> node_960
    node_64 --> node_1021
    node_769 --> node_1260
    node_497 --> node_1319
    node_541 --> node_1065
    node_12 --> node_664
    node_177 --> node_178
    node_31 --> node_948
    node_672 --> node_1036
    node_934 --> node_1008
    node_489 --> node_368
    node_919 --> node_27
    node_1117 --> node_938
    node_1141 --> node_1039
    node_672 --> node_1032
    node_1251 --> node_1253
    node_0 --> node_1068
    node_63 --> node_720
    node_954 --> node_950
    node_5 --> node_1173
    node_903 --> node_183
    node_299 --> node_977
    node_687 --> node_488
    node_781 --> node_795
    node_67 --> node_131
    node_1339 --> node_1305
    node_229 --> node_739
    node_773 --> node_187
    node_541 --> node_1214
    node_541 --> node_1314
    node_666 --> node_1167
    node_19 --> node_279
    node_187 --> node_352
    node_781 --> node_48
    node_595 --> node_575
    node_632 --> node_1312
    node_1101 --> node_967
    node_276 --> node_213
    node_0 --> node_1312
    node_1117 --> node_778
    node_5 --> node_1257
    node_179 --> node_406
    node_790 --> node_1082
    node_976 --> node_731
    node_497 --> node_1095
    node_816 --> node_421
    node_511 --> node_191
    node_52 --> node_1302
    node_1177 --> node_1175
    node_556 --> node_98
    node_106 --> node_229
    node_449 --> node_259
    node_665 --> node_1117
    node_1231 --> node_1308
    node_1339 --> node_1188
    node_449 --> node_617
    node_902 --> node_394
    node_229 --> node_253
    node_563 --> node_656
    node_898 --> node_281
    node_1291 --> node_1149
    node_1352 --> node_1261
    node_96 --> node_72
    node_52 --> node_241
    node_490 --> node_515
    node_99 --> node_1337
    node_68 --> node_739
    node_1097 --> node_1298
    node_866 --> node_1148
    node_1330 --> node_1007
    node_1339 --> node_1005
    node_178 --> node_1038
    node_1339 --> node_1023
    node_229 --> node_195
    node_1180 --> node_1047
    node_1127 --> node_331
    node_629 --> node_1099
    node_1097 --> node_1363
    node_511 --> node_998
    node_187 --> node_200
    node_1097 --> node_1096
    node_520 --> node_1254
    node_1339 --> node_1200
    node_666 --> node_1234
    node_1236 --> node_1235
    node_64 --> node_1095
    node_772 --> node_1170
    node_861 --> node_244
    node_1260 --> node_419
    node_191 --> node_1302
    node_505 --> node_1354
    node_903 --> node_277
    node_99 --> node_742
    node_209 --> node_304
    node_229 --> node_208
    node_1339 --> node_1341
    node_417 --> node_181
    node_689 --> node_570
    node_1230 --> node_1060
    node_599 --> node_249
    node_63 --> node_795
    node_100 --> node_68
    node_5 --> node_209
    node_855 --> node_704
    node_497 --> node_637
    node_1230 --> node_1156
    node_1267 --> node_1102
    node_485 --> node_183
    node_96 --> node_233
    node_19 --> node_370
    node_63 --> node_48
    node_1267 --> node_193
    node_1314 --> node_1298
    node_492 --> node_50
    node_541 --> node_175
    node_1314 --> node_1218
    node_1260 --> node_1283
    node_572 --> node_626
    node_964 --> node_1014
    node_976 --> node_328
    node_898 --> node_267
    node_1117 --> node_200
    node_7 --> node_332
    node_1230 --> node_1122
    node_1314 --> node_1363
    node_866 --> node_695
    node_781 --> node_1254
    node_497 --> node_746
    node_304 --> node_310
    node_490 --> node_541
    node_497 --> node_1035
    node_520 --> node_1335
    node_5 --> node_300
    node_695 --> node_733
    node_663 --> node_1067
    node_58 --> node_131
    node_1231 --> node_1339
    node_823 --> node_272
    node_699 --> node_1148
    node_106 --> node_37
    node_1102 --> node_1260
    node_187 --> node_404
    node_661 --> node_1015
    node_99 --> node_975
    node_180 --> node_391
    node_520 --> node_1037
    node_384 --> node_58
    node_541 --> node_8
    node_997 --> node_981
    node_19 --> node_1082
    node_525 --> node_1342
    node_807 --> node_58
    node_64 --> node_795
    node_497 --> node_1125
    node_1230 --> node_1356
    node_5 --> node_1195
    node_1339 --> node_1118
    node_1219 --> node_1221
    node_105 --> node_73
    node_1039 --> node_998
    node_1314 --> node_1198
    node_1359 --> node_1128
    node_1231 --> node_1220
    node_106 --> node_784
    node_960 --> node_955
    node_527 --> node_241
    node_575 --> node_962
    node_145 --> node_58
    node_1267 --> node_187
    node_527 --> node_731
    node_458 --> node_1148
    node_142 --> node_249
    node_541 --> node_972
    node_599 --> node_247
    node_1230 --> node_1192
    node_1231 --> node_1147
    node_1153 --> node_1150
    node_533 --> node_175
    node_1250 --> node_1245
    node_520 --> node_1148
    node_960 --> node_956
    node_525 --> node_1352
    node_525 --> node_1117
    node_709 --> node_187
    node_246 --> node_203
    node_490 --> node_507
    node_416 --> node_177
    node_302 --> node_313
    node_773 --> node_35
    node_5 --> node_928
    node_632 --> node_1298
    node_0 --> node_1298
    node_103 --> node_533
    node_632 --> node_1218
    node_5 --> node_1015
    node_563 --> node_666
    node_449 --> node_253
    node_63 --> node_1254
    node_106 --> node_334
    node_416 --> node_742
    node_6 --> node_51
    node_1040 --> node_1039
    node_1050 --> node_1047
    node_1077 --> node_253
    node_69 --> node_71
    node_395 --> node_391
    node_520 --> node_244
    node_205 --> node_1280
    node_1359 --> node_1046
    node_632 --> node_1363
    node_1230 --> node_1340
    node_1260 --> node_1274
    node_0 --> node_1363
    node_541 --> node_1060
    node_102 --> node_155
    node_666 --> node_1279
    node_50 --> node_168
    node_490 --> node_504
    node_614 --> node_613
    node_4 --> node_20
    node_1097 --> node_1066
    node_5 --> node_1300
    node_5 --> node_783
    node_662 --> node_1233
    node_711 --> node_703
    node_5 --> node_183
    node_842 --> node_585
    node_923 --> node_47
    node_251 --> node_36
    node_1230 --> node_1045
    node_1231 --> node_1065
    node_486 --> node_1046
    node_1359 --> node_1078
    node_919 --> node_563
    node_1230 --> node_1036
    node_1339 --> node_1332
    node_31 --> node_490
    node_541 --> node_1122
    node_19 --> node_1289
    node_665 --> node_1358
    node_100 --> node_1337
    node_253 --> node_203
    node_99 --> node_960
    node_458 --> node_695
    node_695 --> node_336
    node_423 --> node_447
    node_520 --> node_1309
    node_490 --> node_512
    node_603 --> node_82
    node_1230 --> node_1232
    node_497 --> node_1335
    node_0 --> node_1026
    node_64 --> node_1254
    node_682 --> node_1135
    node_1117 --> node_201
    node_519 --> node_1148
    node_5 --> node_1267
    node_5 --> node_364
    node_31 --> node_928
    node_1097 --> node_1157
    node_1339 --> node_1230
    node_1042 --> node_1122
    node_507 --> node_302
    node_647 --> node_1108
    node_541 --> node_1356
    node_31 --> node_766
    node_497 --> node_1037
    node_667 --> node_669
    node_179 --> node_1294
    node_738 --> node_739
    node_526 --> node_1291
    node_178 --> node_1040
    node_595 --> node_591
    node_100 --> node_742
    node_6 --> node_1047
    node_1167 --> node_1009
    node_393 --> node_357
    node_541 --> node_1034
    node_537 --> node_1183
    node_670 --> node_1308
    node_649 --> node_695
    node_31 --> node_183
    node_541 --> node_1192
    node_1345 --> node_1047
    node_599 --> node_650
    node_31 --> node_943
    node_141 --> node_122
    node_1362 --> node_232
    node_19 --> node_368
    node_669 --> node_1142
    node_100 --> node_943
    node_685 --> node_3
    node_1076 --> node_1144
    node_106 --> node_620
    node_1147 --> node_238
    node_848 --> node_368
    node_1352 --> node_232
    node_504 --> node_175
    node_205 --> node_405
    node_19 --> node_280
    node_1230 --> node_1201
    node_507 --> node_50
    node_652 --> node_1014
    node_1314 --> node_1157
    node_597 --> node_598
    node_1060 --> node_1058
    node_1169 --> node_1168
    node_541 --> node_1340
    node_599 --> node_49
    node_972 --> node_52
    node_497 --> node_1185
    node_5 --> node_1024
    node_103 --> node_1138
    node_100 --> node_975
    node_641 --> node_175
    node_63 --> node_244
    node_5 --> node_1098
    node_964 --> node_1008
    node_599 --> node_634
    node_541 --> node_1269
    node_772 --> node_962
    node_1097 --> node_1093
    node_599 --> node_969
    node_449 --> node_746
    node_99 --> node_72
    node_541 --> node_1045
    node_5 --> node_1169
    node_306 --> node_3
    node_595 --> node_565
    node_541 --> node_1036
    node_106 --> node_948
    node_1267 --> node_35
    node_936 --> node_695
    node_63 --> node_1354
    node_285 --> node_279
    node_101 --> node_72
    node_632 --> node_1066
    node_0 --> node_1066
    node_972 --> node_250
    node_709 --> node_35
    node_712 --> node_1047
    node_5 --> node_1212
    node_145 --> node_737
    node_5 --> node_413
    node_521 --> node_290
    node_229 --> node_211
    node_304 --> node_315
    node_470 --> node_1286
    node_559 --> node_739
    node_1260 --> node_1262
    node_64 --> node_244
    node_5 --> node_1143
    node_355 --> node_634
    node_490 --> node_511
    node_511 --> node_487
    node_1167 --> node_1010
    node_497 --> node_543
    node_287 --> node_1047
    node_595 --> node_569
    node_99 --> node_233
    node_541 --> node_681
    node_731 --> node_331
    node_520 --> node_1154
    node_12 --> node_652
    node_81 --> node_86
    node_1097 --> node_1041
    node_1351 --> node_1144
    node_1147 --> node_1078
    node_795 --> node_1082
    node_559 --> node_253
    node_632 --> node_1157
    node_0 --> node_1157
    node_101 --> node_233
    node_1230 --> node_1323
    node_962 --> node_12
    node_705 --> node_187
    node_972 --> node_246
    node_742 --> node_739
    node_489 --> node_387
    node_489 --> node_241
    node_658 --> node_1244
    node_525 --> node_1236
    node_100 --> node_960
    node_1097 --> node_1065
    node_864 --> node_419
    node_747 --> node_757
    node_67 --> node_241
    node_797 --> node_282
    node_1083 --> node_35
    node_205 --> node_355
    node_67 --> node_731
    node_1015 --> node_1007
    node_106 --> node_20
    node_489 --> node_420
    node_145 --> node_614
    node_31 --> node_486
    node_1117 --> node_1104
    node_489 --> node_235
    node_599 --> node_1170
    node_656 --> node_1233
    node_100 --> node_486
    node_525 --> node_1133
    node_526 --> node_359
    node_751 --> node_1003
    node_1314 --> node_1140
    node_541 --> node_1141
    node_1314 --> node_1041
    node_1097 --> node_1214
    node_1097 --> node_1314
    node_516 --> node_739
    node_911 --> node_1290
    node_601 --> node_642
    node_1001 --> node_1047
    node_68 --> node_100
    node_334 --> node_6
    node_205 --> node_357
    node_209 --> node_1128
    node_507 --> node_305
    node_521 --> node_704
    node_530 --> node_1128
    node_647 --> node_1111
    node_642 --> node_1012
    node_632 --> node_1093
    node_0 --> node_1093
    node_866 --> node_1260
    node_543 --> node_607
    node_514 --> node_741
    node_520 --> node_1325
    node_639 --> node_666
    node_663 --> node_1062
    node_666 --> node_1301
    node_520 --> node_1318
    node_1339 --> node_1186
    node_1361 --> node_1358
    node_5 --> node_1329
    node_497 --> node_1324
    node_56 --> node_1177
    node_251 --> node_1302
    node_635 --> node_1211
    node_1314 --> node_1214
    node_666 --> node_1290
    node_1103 --> node_1358
    node_145 --> node_1213
    node_1339 --> node_1353
    node_543 --> node_12
    node_595 --> node_632
    node_145 --> node_31
    node_41 --> node_3
    node_1231 --> node_1034
    node_1122 --> node_1119
    node_67 --> node_328
    node_100 --> node_72
    node_599 --> node_36
    node_751 --> node_595
    node_361 --> node_57
    node_1290 --> node_26
    node_20 --> node_962
    node_1261 --> node_1082
    node_652 --> node_1008
    node_520 --> node_1336
    node_861 --> node_737
    node_96 --> node_731
    node_249 --> node_250
    node_1267 --> node_217
    node_861 --> node_966
    node_525 --> node_1299
    node_205 --> node_391
    node_596 --> node_548
    node_632 --> node_1140
    node_230 --> node_1149
    node_205 --> node_397
    node_1076 --> node_1303
    node_1339 --> node_1330
    node_632 --> node_1041
    node_0 --> node_1041
    node_58 --> node_241
    node_77 --> node_69
    node_187 --> node_1270
    node_1359 --> node_333
    node_920 --> node_1082
    node_635 --> node_1210
    node_520 --> node_1094
    node_601 --> node_12
    node_5 --> node_1223
    node_541 --> node_711
    node_911 --> node_1082
    node_885 --> node_398
    node_632 --> node_1065
    node_142 --> node_1083
    node_0 --> node_1065
    node_1230 --> node_1344
    node_1314 --> node_1173
    node_575 --> node_677
    node_541 --> node_730
    node_541 --> node_1077
    node_100 --> node_233
    node_922 --> node_29
    node_19 --> node_588
    node_370 --> node_187
    node_1260 --> node_399
    node_1339 --> node_1166
    node_839 --> node_386
    node_647 --> node_1112
    node_705 --> node_35
    node_1300 --> node_247
    node_215 --> node_342
    node_1230 --> node_1126
    node_632 --> node_1214
    node_458 --> node_1260
    node_625 --> node_1239
    node_205 --> node_344
    node_632 --> node_1314
    node_0 --> node_1214
    node_278 --> node_276
    node_0 --> node_1314
    node_861 --> node_614
    node_531 --> node_1149
    node_541 --> node_966
    node_711 --> node_702
    node_31 --> node_961
    node_19 --> node_394
    node_1061 --> node_50
    node_505 --> node_232
    node_29 --> node_600
    node_96 --> node_328
    node_205 --> node_367
    node_666 --> node_1281
    node_63 --> node_1261
    node_1231 --> node_1349
    node_929 --> node_1234
    node_19 --> node_363
    node_924 --> node_12
    node_530 --> node_305
    node_769 --> node_1082
    node_525 --> node_1198
    node_5 --> node_1310
    node_1339 --> node_1207
    node_647 --> node_1113
    node_494 --> node_183
    node_1097 --> node_1060
    node_781 --> node_711
    node_639 --> node_662
    node_649 --> node_1260
    node_1230 --> node_1059
    node_841 --> node_181
    node_23 --> node_199
    node_520 --> node_737
    node_1352 --> node_249
    node_575 --> node_954
    node_497 --> node_1336
    node_489 --> node_599
    node_1076 --> node_1265
    node_541 --> node_803
    node_935 --> node_1011
    node_229 --> node_52
    node_840 --> node_202
    node_1097 --> node_1122
    node_520 --> node_1167
    node_5 --> node_832
    node_105 --> node_739
    node_528 --> node_571
    node_429 --> node_443
    node_316 --> node_241
    node_1339 --> node_1057
    node_497 --> node_1094
    node_541 --> node_81
    node_564 --> node_591
    node_670 --> node_1309
    node_541 --> node_1116
    node_850 --> node_208
    node_316 --> node_731
    node_541 --> node_1344
    node_1231 --> node_1318
    node_5 --> node_815
    node_1231 --> node_1141
    node_246 --> node_245
    node_666 --> node_1292
    node_1230 --> node_1069
    node_911 --> node_456
    node_599 --> node_26
    node_541 --> node_35
    node_737 --> node_736
    node_857 --> node_1292
    node_751 --> node_229
    node_5 --> node_1206
    node_781 --> node_966
    node_1097 --> node_1356
    node_229 --> node_250
    node_882 --> node_719
    node_104 --> node_739
    node_103 --> node_667
    node_1314 --> node_1156
    node_99 --> node_1003
    node_936 --> node_1260
    node_669 --> node_1353
    node_559 --> node_178
    node_1330 --> node_1016
    node_4 --> node_533
    node_1145 --> node_1047
    node_5 --> node_406
    node_669 --> node_1351
    node_1102 --> node_247
    node_1097 --> node_1034
    node_541 --> node_232
    node_31 --> node_1138
    node_1081 --> node_1047
    node_647 --> node_1117
    node_1097 --> node_1192
    node_522 --> node_233
    node_156 --> node_114
    node_719 --> node_695
    node_520 --> node_614
    node_1147 --> node_488
    node_334 --> node_325
    node_179 --> node_369
    node_448 --> node_425
    node_665 --> node_1099
    node_1081 --> node_1083
    node_20 --> node_581
    node_773 --> node_739
    node_19 --> node_420
    node_152 --> node_146
    node_7 --> node_83
    node_402 --> node_193
    node_468 --> node_187
    node_772 --> node_677
    node_1266 --> node_1047
    node_541 --> node_32
    node_595 --> node_598
    node_37 --> node_57
    node_1267 --> node_212
    node_67 --> node_119
    node_499 --> node_241
    node_5 --> node_1013
    node_449 --> node_1043
    node_541 --> node_1123
    node_1314 --> node_1356
    node_1097 --> node_1340
    node_229 --> node_246
    node_598 --> node_3
    node_827 --> node_405
    node_415 --> node_1293
    node_564 --> node_668
    node_745 --> node_759
    node_772 --> node_334
    node_205 --> node_343
    node_106 --> node_61
    node_361 --> node_1085
    node_541 --> node_1059
    node_1267 --> node_1262
    node_730 --> node_729
    node_476 --> node_1148
    node_497 --> node_1231
    node_1042 --> node_1038
    node_278 --> node_277
    node_499 --> node_196
    node_1081 --> node_36
    node_653 --> node_1029
    node_852 --> node_187
    node_316 --> node_328
    node_1097 --> node_1045
    node_1236 --> node_1238
    node_489 --> node_222
    node_884 --> node_1148
    node_1097 --> node_1036
    node_1314 --> node_1192
    node_520 --> node_1327
    node_63 --> node_966
    node_99 --> node_595
    node_1042 --> node_1123
    node_449 --> node_997
    node_102 --> node_1163
    node_632 --> node_1060
    node_5 --> node_1313
    node_1102 --> node_1082
    node_0 --> node_1060
    node_263 --> node_449
    node_519 --> node_628
    node_632 --> node_1156
    node_20 --> node_229
    node_205 --> node_1295
    node_497 --> node_1167
    node_1097 --> node_1232
    node_1141 --> node_1122
    node_657 --> node_1047
    node_751 --> node_37
    node_189 --> node_273
    node_520 --> node_1213
    node_490 --> node_491
    node_442 --> node_431
    node_467 --> node_381
    node_844 --> node_346
    node_5 --> node_1068
    node_1359 --> node_331
    node_595 --> node_12
    node_599 --> node_1302
    node_416 --> node_962
    node_520 --> node_31
    node_525 --> node_1326
    node_541 --> node_1069
    node_145 --> node_177
    node_1339 --> node_1027
    node_5 --> node_1019
    node_632 --> node_1122
    node_500 --> node_72
    node_822 --> node_388
    node_0 --> node_1122
    node_278 --> node_284
    node_489 --> node_344
    node_103 --> node_1021
    node_449 --> node_52
    node_1231 --> node_1077
    node_52 --> node_741
    node_1359 --> node_1354
    node_205 --> node_365
    node_1077 --> node_52
    node_751 --> node_784
    node_563 --> node_178
    node_479 --> node_405
    node_772 --> node_954
    node_99 --> node_731
    node_541 --> node_419
    node_1259 --> node_1000
    node_541 --> node_1191
    node_64 --> node_737
    node_5 --> node_1256
    node_543 --> node_187
    node_563 --> node_1148
    node_352 --> node_428
    node_1191 --> node_58
    node_575 --> node_68
    node_487 --> node_1148
    node_820 --> node_269
    node_497 --> node_628
```

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
| `.julesrules` | 🟢 Referenced | Jules AI Agent Rules |  |
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
| `ansible/roles/tool_server/tools/project_mapper_tool.py` | 🟢 Referenced | File: project_mapper_tool.py | **Classes:** ProjectMapperTool<br>**Functions:** __init__, _is_ignored, _build_structure, scan, _list_files_git... |
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
| `docs/analysis/CAPABILITY_ALIGNMENT_REPORT.md` | 📄 Documentation/Asset | Capability Alignment & Performance Evaluation Report |  |
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
| `docs/manual/AGENT_HANDBOOK.md` | 📄 Documentation/Asset | AI Agent Integration Handbook: MCP, API, and Package/Plugin Management |  |
| `docs/manual/AI_GOVERNANCE.md` | 📄 Documentation/Asset | AI Governance & Architecture Plan |  |
| `docs/manual/ARCHITECTURE.md` | 🟢 Referenced | Holistic Project Architecture |  |
| `docs/manual/DEPLOYMENT_AND_PROFILING.md` | 🟢 Referenced | Deploying and Profiling AI Services |  |
| `docs/manual/DIRAC_TODO.md` | 🟢 Referenced | Dirac Integration Plan & TODO List |  |
| `docs/manual/EXTERNAL_APP_HOSTING_GUIDE.md` | 🟢 Referenced | External Application Hosting & Package Management Guide |  |
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
| `docs/manual/PERFORMANCE_OPTIMIZATION.md` | 🟢 Referenced | Performance & I/O Optimization |  |
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
| `evaluations/ktx_evaluation.md` | 🔴 Orphan | Kaelio/ktx Evaluation: Project Inclusion vs. Feature Augmentation |  |
| `evaluations/longcat_2.0_evaluation.md` | 🔴 Orphan | LongCat 2.0 Evaluation vs. Local Distributed Pipeline |  |
| `evaluations/mesh_llm_evaluation.md` | 🔴 Orphan | Evaluation of Mesh LLM for Distributed AI Cluster Integration |  |
| `evaluations/mindwalk_evaluation.md` | 🔴 Orphan | Evaluation of cosmtrek/mindwalk for Feature Ingestion |  |
| `evaluations/ornith-1-evaluation.md` | 🔴 Orphan | Ornith-1 Evaluation for Local LLM Provider (llama-cluster-upbringing-script) |  |
| `examples/README.md` | 🟢 Referenced | Examples |  |
| `examples/chat-persistent.sh` | 🟢 Referenced | bin/bash |  |
| `examples/external_apps/mesh_llm.json` | 🟢 Referenced | File: mesh_llm.json |  |
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
| `pipecatapp/nomad_templates/readeck.nomad.hcl` | 🟢 Referenced | File: readeck.nomad.hcl |  |
| `pipecatapp/nomad_templates/uptime-kuma.nomad.hcl` | 🟢 Referenced | File: uptime-kuma.nomad.hcl |  |
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
| `pipecatapp/resources/apps/mesh_llm.json` | 🟢 Referenced | File: mesh_llm.json |  |
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
| `pipecatapp/tests/test_mindwalk_exporter.py` | 🧪 Test | File: test_mindwalk_exporter.py | **Functions:** test_export_trace_basic, test_stats_churn_and_verify, test_export_to_file |
| `pipecatapp/tests/test_net_utils.py` | 🧪 Test | File: test_net_utils.py | **Classes:** TestNetUtils, TestValidateUrl<br>**Functions:** test_ensure_ipv6_brackets, test_format_url, test_validate_url_public, test_validate_url_private, test_validate_url_localhost... |
| `pipecatapp/tests/test_new_skills.py` | 🧪 Test | File: test_new_skills.py | **Functions:** skill_lib, test_skill_ingestion_and_retrieval, test_set_operational_mode_tool, test_lightweight_mapper, test_project_mapper_interface_consistency |
| `pipecatapp/tests/test_openclaw.py` | 🧪 Test | File: test_openclaw.py | **Functions:** test_openclaw_client_handshake_and_send, test_openclaw_tool, mock_iter, mock_send |
| `pipecatapp/tests/test_ouroboros.py` | 🧪 Test | Mock dependencies before importing web_server | **Functions:** test_webring_routes, test_webring_navigation |
| `pipecatapp/tests/test_piper_async.py` | 🧪 Test | File: test_piper_async.py | **Classes:** MockFrameProcessor, MockTextFrame<br>**Functions:** test_piper_tts_async_execution, side_effect_synthesize, __init__, push_frame, __init__ |
| `pipecatapp/tests/test_proxy_security.py` | 🧪 Test | File: test_proxy_security.py | **Functions:** test_proxy_headers_respected_when_configured, test_proxy_headers_ignored_when_disabled, get_ip, get_ip |
| `pipecatapp/tests/test_rag_pruning.py` | 🧪 Test | File: test_rag_pruning.py | **Functions:** setup_mocks, mock_llm_client, pruner, test_rag_pruner_grading, test_rag_pruner_json_extraction... |
| `pipecatapp/tests/test_rag_tool.py` | 🟢 Referenced | File: test_rag_tool.py | **Classes:** MockPMMMemory<br>**Functions:** rag_tool_class, mock_memory, mock_thread, test_dirs, test_rag_scope_security... |
| `pipecatapp/tests/test_rate_limiter.py` | 🟢 Referenced | File: test_rate_limiter.py | **Classes:** MockClient, MockRequest<br>**Functions:** test_rate_limiter, test_rate_limiter_cleanup, sample_endpoint |
| `pipecatapp/tests/test_schema_mapper_tool.py` | 🧪 Test | Dynamic mock for missing imports during test collection to avoid importing heavy dependencies | **Classes:** MockModule, TestSchemaMapperTool<br>**Functions:** __getattr__, setup_method, teardown_method, _setup_test_db, test_direct_db_path_mapping... |
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
| `pipecatapp/tools/external_app_manager_tool.py` | 🟢 Referenced | File: external_app_manager_tool.py | **Classes:** ExternalAppManagerTool<br>**Functions:** __init__, scaffold_manifest, validate_manifest, deploy_app, purge_app... |
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
| `pipecatapp/tools/remote_code_runner_tool.py` | 🟢 Referenced | File: remote_code_runner_tool.py | **Classes:** RemoteCodeRunnerTool<br>**Functions:** __init__, _make_request, execute |
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
| `pipecatapp/tools/schema_mapper_tool.py` | 🟢 Referenced | File: schema_mapper_tool.py | **Classes:** SchemaMapperTool<br>**Functions:** __init__, execute, _discover_databases, _generate_report, _inspect_table... |
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
| `pipecatapp/utils/app_manager.py` | 🟢 Referenced | File: app_manager.py | **Classes:** AppManager<br>**Functions:** __init__, validate_manifest, is_btrfs_supported, provision_storage, deprovision_storage... |
| `pipecatapp/utils/backon_utils.py` | 🟢 Referenced | File: backon_utils.py | **Classes:** MultiMetricsCollector<br>**Functions:** is_transient_error, setup_backon_observability, __init__, emit_attempt, emit_success... |
| `pipecatapp/utils/command_runner.py` | 🟢 Referenced | File: command_runner.py | **Classes:** CommandRunner<br>**Functions:** get_instance, __init__, _init_nomad_client, run_local, run... |
| `pipecatapp/utils/coverage_check.py` | 🟢 Referenced | Coverage check for scaffold-setup-skill. | **Classes:** Param, CheckResult<br>**Functions:** extract_env_example_params, _parse_env_file, extract_ci_secret_params, extract_skill_params, extract_skill_branches... |
| `pipecatapp/utils/file_utils.py` | 🟢 Referenced | File: file_utils.py | **Functions:** calculate_line_hash, generate_file_hashes |
| `pipecatapp/utils/ingest_skills.py` | 🔴 Orphan | File: ingest_skills.py | **Functions:** ingest_all_skills, adapt_scaffold_setup_skill |
| `pipecatapp/utils/mindwalk_exporter.py` | 🟢 Referenced | File: mindwalk_exporter.py | **Classes:** MindwalkTraceExporter<br>**Functions:** calculate_stats, export_trace, export_trace_to_file |
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
| `scripts/app-manager.py` | 🟢 Referenced | CLI wrapper for External Application Package/Plugin Manager. | **Functions:** handle_install, handle_uninstall, handle_list, handle_status, main |
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
| `scripts/verify_ui_accessibility.py` | 🟢 Referenced | scripts/verify_ui_accessibility.py | **Functions:** run_accessibility_audit |
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
| `tests/unit/test_external_app_manager.py` | 🧪 Test | File: test_external_app_manager.py | **Classes:** TestExternalAppManager<br>**Functions:** setUp, test_validate_manifest_valid, test_validate_manifest_invalid_name, test_validate_manifest_invalid_version, test_validate_manifest_invalid_mount_path... |
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
| `tests/unit/test_janitor.py` | 🧪 Test | File: test_janitor.py | **Classes:** TestJanitorAgent<br>**Functions:** setUp, test_process_item_triggers_jules_on_test_failure, test_process_item_skips_jules_on_other_failures |
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
| `tests/unit/test_mesh_llm_manifest.py` | 🟢 Referenced | File: test_mesh_llm_manifest.py | **Classes:** TestMeshLLMManifest<br>**Functions:** setUp, test_manifest_exists, test_manifest_valid_json, test_manifest_validation_passes, test_manifest_resource_and_env_constraints |
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
| `tests/unit/test_recover_os.py` | 🧪 Test | Add the scripts directory to path to import recover_os | **Functions:** test_recover_os_excludes_in_rsync, test_recover_os_excludes_in_rollback, test_recover_os_nfs_skip_in_rsync, test_recover_os_nfs_skip_in_rollback, check_output_side_effect... |
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
| `tests/unit/test_supervisor_retries.py` | 🧪 Test | File: test_supervisor_retries.py | **Classes:** TestTaskSupervisorRetries<br>**Functions:** test_check_tasks_detects_timeout_and_retries |
| `tests/unit/test_swarm_tool.py` | 🧪 Test | File: test_swarm_tool.py | **Functions:** test_swarm_tool_initialization, test_spawn_workers_technician, test_spawn_workers_success, test_spawn_workers_partial_failure, test_kill_worker_success... |
| `tests/unit/test_tap_service.py` | 🧪 Test | File: test_tap_service.py | **Classes:** MockFrameProcessor<br>**Functions:** test_process_frame, __init__, push_frame |
| `tests/unit/test_tasky_nodes.py` | 🧪 Test | File: test_tasky_nodes.py | **Functions:** test_tasky_audit_node_no_markdown, test_tasky_audit_node_no_execution_result |
| `tests/unit/test_tasky_poc.py` | 🧪 Test | File: test_tasky_poc.py | **Functions:** main |
| `tests/unit/test_term_everything_tool.py` | 🟢 Referenced | File: test_term_everything_tool.py | **Functions:** tool, test_execute_command_success, test_execute_command_failure, test_execute_exception |
| `tests/unit/test_terminal_cleanup.py` | 🧪 Test | File: test_terminal_cleanup.py | **Functions:** test_clean_terminal_output_carriage_returns, test_clean_terminal_output_ansi, test_clean_terminal_output_both, test_clean_terminal_output_trailing_cr, test_clean_terminal_output_non_string |
| `tests/unit/test_ternlight_tool.py` | 🧪 Test | File: test_ternlight_tool.py | **Functions:** mock_requests_post, mock_requests_get, mock_subprocess_run, test_ternlight_tool_remote_embed, test_ternlight_tool_remote_similar... |
| `tests/unit/test_troubleshoot.py` | 🧪 Test | Dynamically import troubleshoot as it is a script | **Classes:** DummyArgs<br>**Functions:** mock_api_get, mock_run_command, test_list_dead_pending, test_list_dead_pending_json, test_inspect_job... |
| `tests/unit/test_ui_accessibility.py` | 🧪 Test | File: test_ui_accessibility.py | **Classes:** TestUIAccessibilityVerifier<br>**Functions:** test_run_accessibility_audit_successful |
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
| `uv.lock` | 🔴 Orphan | File: uv.lock |  |
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
        node_3[".djlint.toml"]
        node_10[".gitattributes"]
        node_2[".gitignore"]
        node_26[".gitmodules"]
        node_12[".julesrules"]
        node_25[".markdownlint.json"]
        node_11[".sops.yaml"]
        node_20[".vulture_whitelist.py"]
        node_33[".yamllint"]
        node_21["AGENTS.md"]
        node_5["GEMINI.md"]
        node_7["LICENSE"]
        node_32["README.md"]
        node_0["README_bridge_networking_fix.md"]
        node_6["TODO.md"]
        node_27["ansible.cfg"]
        node_18["benchmark.py"]
        node_15["benchmark_async.py"]
        node_4["bootstrap.sh"]
        node_29["disk_script.sh"]
        node_35["fix_dep_scanner.py"]
        node_22["hostfile"]
        node_34["inventory.yaml"]
        node_28["local_inventory.ini"]
        node_19["memory_disk_script.sh"]
        node_14["mypy.ini"]
        node_8["nerv_ui.patch"]
        node_23["ontology.yaml"]
        node_30["package.json"]
        node_31["performance_benchmark.py"]
        node_13["playbook.yaml"]
        node_17["pyproject.toml"]
        node_9["pytest.ini"]
        node_24["replace_local_world_model.py"]
        node_16["requirements-dev.txt"]
        node_1["uv.lock"]
    end
    subgraph dir__githooks [.githooks]
        direction TB
        node_558["pre-commit"]
    end
    subgraph dir__github [.github]
        direction TB
        node_696["AGENTIC_README.md"]
    end
    subgraph dir__github_workflows [.github/workflows]
        direction TB
        node_700["auto-merge.yml"]
        node_703["ci.yml"]
        node_702["create-issues-from-files.yml"]
        node_701["docker-publish.yml"]
        node_704["jules-queue.yml"]
        node_697["remote-verify.yml"]
        node_699["test-cluster.yml"]
        node_698["unblocked-issues.yml"]
    end
    subgraph dir__husky [.husky]
        direction TB
        node_559["pre-push"]
    end
    subgraph dir__opencode [.opencode]
        direction TB
        node_783["README.md"]
        node_782["opencode.json"]
    end
    subgraph dir_ISSUES [ISSUES]
        direction TB
        node_781["2024-04-16-test-unblocked-issues-workflow.md"]
    end
    subgraph dir_ansible [ansible]
        direction TB
        node_989["README.md"]
        node_987["lint_nomad.yaml"]
        node_986["requirements.yml"]
        node_988["run_download_models.yaml"]
    end
    subgraph dir_ansible_filter_plugins [ansible/filter_plugins]
        direction TB
        node_992["README.md"]
        node_991["safe_flatten.py"]
    end
    subgraph dir_ansible_jobs [ansible/jobs]
        direction TB
        node_1020["README.md"]
        node_1009["authentik.nomad"]
        node_1018["benchmark.nomad"]
        node_1024["code-runner-service.nomad"]
        node_1025["ds4-server.nomad.j2"]
        node_999["dummy_web_service.nomad"]
        node_1023["e2a.nomad.j2"]
        node_1011["evolve-prompt.nomad.j2"]
        node_1015["expert-debug.nomad"]
        node_1021["expert.nomad.j2"]
        node_1007["filebrowser.nomad.j2"]
        node_1001["health-check.nomad.j2"]
        node_1013["helixdb.nomad"]
        node_1005["llamacpp-batch.nomad.j2"]
        node_1008["llamacpp-rpc.nomad.j2"]
        node_1019["model-benchmark.nomad.j2"]
        node_1017["opengravity.nomad.j2"]
        node_1006["pipecatapp.nomad"]
        node_1016["postgres.nomad"]
        node_1003["rag-service.nomad"]
        node_1022["redis.nomad"]
        node_1000["router.nomad.j2"]
        node_1014["smol-agent-server.nomad.j2"]
        node_1012["ternlight-service.nomad"]
        node_1004["test-runner.nomad.j2"]
        node_1010["tml-interaction.nomad.j2"]
        node_1002["vllm.nomad.j2"]
    end
    subgraph dir_ansible_roles [ansible/roles]
        direction TB
        node_1026["README.md"]
    end
    subgraph dir_ansible_roles_apt_proxy_tasks [ansible/roles/apt_proxy/tasks]
        direction TB
        node_1113["main.yml"]
    end
    subgraph dir_ansible_roles_apt_proxy_templates [ansible/roles/apt_proxy/templates]
        direction TB
        node_1112["apt_proxy.nomad.j2"]
    end
    subgraph dir_ansible_roles_authentik_defaults [ansible/roles/authentik/defaults]
        direction TB
        node_1370["main.yml"]
    end
    subgraph dir_ansible_roles_authentik_tasks [ansible/roles/authentik/tasks]
        direction TB
        node_1369["main.yml"]
    end
    subgraph dir_ansible_roles_authentik_templates [ansible/roles/authentik/templates]
        direction TB
        node_1368["authentik.nomad.j2"]
    end
    subgraph dir_ansible_roles_benchmark_models_tasks [ansible/roles/benchmark_models/tasks]
        direction TB
        node_1212["benchmark_loop.yaml"]
        node_1211["main.yaml"]
    end
    subgraph dir_ansible_roles_benchmark_models_templates [ansible/roles/benchmark_models/templates]
        direction TB
        node_1210["model-benchmark.nomad.j2"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_defaults [ansible/roles/bootstrap_agent/defaults]
        direction TB
        node_1355["main.yaml"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_handlers [ansible/roles/bootstrap_agent/handlers]
        direction TB
        node_1352["main.yaml"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_tasks [ansible/roles/bootstrap_agent/tasks]
        direction TB
        node_1354["deploy_llama_cpp_model.yaml"]
        node_1353["main.yaml"]
    end
    subgraph dir_ansible_roles_btrfs_snapshot_defaults [ansible/roles/btrfs_snapshot/defaults]
        direction TB
        node_1180["main.yaml"]
    end
    subgraph dir_ansible_roles_btrfs_snapshot_tasks [ansible/roles/btrfs_snapshot/tasks]
        direction TB
        node_1179["main.yaml"]
    end
    subgraph dir_ansible_roles_clamav_files [ansible/roles/clamav/files]
        direction TB
        node_1351["rogue_agent.ldb"]
    end
    subgraph dir_ansible_roles_clamav_handlers [ansible/roles/clamav/handlers]
        direction TB
        node_1349["main.yaml"]
    end
    subgraph dir_ansible_roles_clamav_tasks [ansible/roles/clamav/tasks]
        direction TB
        node_1350["main.yaml"]
    end
    subgraph dir_ansible_roles_claude_clone_tasks [ansible/roles/claude_clone/tasks]
        direction TB
        node_1163["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tools_tasks [ansible/roles/common-tools/tasks]
        direction TB
        node_1166["main.yaml"]
    end
    subgraph dir_ansible_roles_common_handlers [ansible/roles/common/handlers]
        direction TB
        node_1088["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tasks [ansible/roles/common/tasks]
        direction TB
        node_1089["main.yaml"]
        node_1090["network_repair.yaml"]
    end
    subgraph dir_ansible_roles_common_templates [ansible/roles/common/templates]
        direction TB
        node_1085["cluster-ip-alias.service.j2"]
        node_1086["hosts.j2"]
        node_1087["update-ssh-authorized-keys.sh.j2"]
    end
    subgraph dir_ansible_roles_config_manager_tasks [ansible/roles/config_manager/tasks]
        direction TB
        node_1337["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_defaults [ansible/roles/consul/defaults]
        direction TB
        node_1262["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_handlers [ansible/roles/consul/handlers]
        direction TB
        node_1258["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_tasks [ansible/roles/consul/tasks]
        direction TB
        node_1260["acl.yaml"]
        node_1259["main.yaml"]
        node_1261["tls.yaml"]
    end
    subgraph dir_ansible_roles_consul_templates [ansible/roles/consul/templates]
        direction TB
        node_1256["consul.hcl.j2"]
        node_1257["consul.service.j2"]
    end
    subgraph dir_ansible_roles_desktop_extras_tasks [ansible/roles/desktop_extras/tasks]
        direction TB
        node_1246["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_handlers [ansible/roles/docker/handlers]
        direction TB
        node_1155["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_molecule_default [ansible/roles/docker/molecule/default]
        direction TB
        node_1159["converge.yml"]
        node_1157["molecule.yml"]
        node_1160["prepare.yml"]
        node_1158["verify.yml"]
    end
    subgraph dir_ansible_roles_docker_tasks [ansible/roles/docker/tasks]
        direction TB
        node_1156["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_templates [ansible/roles/docker/templates]
        direction TB
        node_1154["daemon.json.j2"]
        node_1153["docker-prune.service.j2"]
        node_1152["docker-prune.timer.j2"]
    end
    subgraph dir_ansible_roles_download_models_files [ansible/roles/download_models/files]
        direction TB
        node_1165["download_hf_repo.py"]
    end
    subgraph dir_ansible_roles_download_models_tasks [ansible/roles/download_models/tasks]
        direction TB
        node_1164["main.yaml"]
    end
    subgraph dir_ansible_roles_ds4_defaults [ansible/roles/ds4/defaults]
        direction TB
        node_1365["main.yaml"]
    end
    subgraph dir_ansible_roles_ds4_tasks [ansible/roles/ds4/tasks]
        direction TB
        node_1364["main.yaml"]
    end
    subgraph dir_ansible_roles_e2a_tasks [ansible/roles/e2a/tasks]
        direction TB
        node_1282["main.yml"]
    end
    subgraph dir_ansible_roles_e2a_templates [ansible/roles/e2a/templates]
        direction TB
        node_1281["e2a.nomad.j2"]
    end
    subgraph dir_ansible_roles_exo_defaults [ansible/roles/exo/defaults]
        direction TB
        node_1376["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_files [ansible/roles/exo/files]
        direction TB
        node_1377["Dockerfile"]
    end
    subgraph dir_ansible_roles_exo_tasks [ansible/roles/exo/tasks]
        direction TB
        node_1375["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_templates [ansible/roles/exo/templates]
        direction TB
        node_1374["exo.nomad.j2"]
        node_1373["load_image_task.nomad.j2"]
    end
    subgraph dir_ansible_roles_forgejo_handlers [ansible/roles/forgejo/handlers]
        direction TB
        node_1220["main.yaml"]
    end
    subgraph dir_ansible_roles_forgejo_tasks [ansible/roles/forgejo/tasks]
        direction TB
        node_1221["main.yaml"]
    end
    subgraph dir_ansible_roles_forgejo_templates [ansible/roles/forgejo/templates]
        direction TB
        node_1219["forgejo.nomad.j2"]
    end
    subgraph dir_ansible_roles_gemini_cli_handlers [ansible/roles/gemini_cli/handlers]
        direction TB
        node_1110["main.yaml"]
    end
    subgraph dir_ansible_roles_gemini_cli_tasks [ansible/roles/gemini_cli/tasks]
        direction TB
        node_1111["main.yaml"]
    end
    subgraph dir_ansible_roles_gemini_cli_templates [ansible/roles/gemini_cli/templates]
        direction TB
        node_1109["gemini.nomad.j2"]
    end
    subgraph dir_ansible_roles_gpu_setup_defaults [ansible/roles/gpu_setup/defaults]
        direction TB
        node_1050["main.yaml"]
    end
    subgraph dir_ansible_roles_gpu_setup_tasks [ansible/roles/gpu_setup/tasks]
        direction TB
        node_1049["main.yaml"]
    end
    subgraph dir_ansible_roles_gpu_setup_templates [ansible/roles/gpu_setup/templates]
        direction TB
        node_1048["ai-cluster-env.sh.j2"]
    end
    subgraph dir_ansible_roles_headscale_defaults [ansible/roles/headscale/defaults]
        direction TB
        node_1059["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_handlers [ansible/roles/headscale/handlers]
        direction TB
        node_1057["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_tasks [ansible/roles/headscale/tasks]
        direction TB
        node_1058["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_templates [ansible/roles/headscale/templates]
        direction TB
        node_1056["config.yaml.j2"]
        node_1055["headscale.service.j2"]
    end
    subgraph dir_ansible_roles_heretic_tool_defaults [ansible/roles/heretic_tool/defaults]
        direction TB
        node_1209["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_meta [ansible/roles/heretic_tool/meta]
        direction TB
        node_1208["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_tasks [ansible/roles/heretic_tool/tasks]
        direction TB
        node_1207["main.yaml"]
    end
    subgraph dir_ansible_roles_hermes_agent_tasks [ansible/roles/hermes_agent/tasks]
        direction TB
        node_1178["main.yaml"]
    end
    subgraph dir_ansible_roles_influxdb [ansible/roles/influxdb]
        direction TB
        node_1044["README.md"]
    end
    subgraph dir_ansible_roles_influxdb_meta [ansible/roles/influxdb/meta]
        direction TB
        node_1047["main.yaml"]
    end
    subgraph dir_ansible_roles_influxdb_tasks [ansible/roles/influxdb/tasks]
        direction TB
        node_1046["main.yaml"]
    end
    subgraph dir_ansible_roles_influxdb_templates [ansible/roles/influxdb/templates]
        direction TB
        node_1045["influxdb.nomad.j2"]
    end
    subgraph dir_ansible_roles_ipfs_tasks [ansible/roles/ipfs/tasks]
        direction TB
        node_1192["main.yaml"]
    end
    subgraph dir_ansible_roles_ipfs_templates [ansible/roles/ipfs/templates]
        direction TB
        node_1191["ipfs.nomad.j2"]
    end
    subgraph dir_ansible_roles_kittentts_tasks [ansible/roles/kittentts/tasks]
        direction TB
        node_1064["main.yaml"]
    end
    subgraph dir_ansible_roles_librarian_defaults [ansible/roles/librarian/defaults]
        direction TB
        node_1186["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_handlers [ansible/roles/librarian/handlers]
        direction TB
        node_1184["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_tasks [ansible/roles/librarian/tasks]
        direction TB
        node_1185["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_templates [ansible/roles/librarian/templates]
        direction TB
        node_1183["librarian.service.j2"]
        node_1181["librarian_agent.py.j2"]
        node_1182["spacedrive.service.j2"]
    end
    subgraph dir_ansible_roles_llama_cpp_files [ansible/roles/llama_cpp/files]
        direction TB
        node_1097["realtime_steering.patch"]
    end
    subgraph dir_ansible_roles_llama_cpp_handlers [ansible/roles/llama_cpp/handlers]
        direction TB
        node_1091["main.yaml"]
    end
    subgraph dir_ansible_roles_llama_cpp_molecule_default [ansible/roles/llama_cpp/molecule/default]
        direction TB
        node_1096["converge.yml"]
        node_1094["molecule.yml"]
        node_1095["verify.yml"]
    end
    subgraph dir_ansible_roles_llama_cpp_tasks [ansible/roles/llama_cpp/tasks]
        direction TB
        node_1092["main.yaml"]
        node_1093["run_single_rpc_job.yaml"]
    end
    subgraph dir_ansible_roles_llmfit_tasks [ansible/roles/llmfit/tasks]
        direction TB
        node_1367["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_tasks [ansible/roles/llxprt_code/tasks]
        direction TB
        node_1372["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_templates [ansible/roles/llxprt_code/templates]
        direction TB
        node_1371["llxprt-code.env.j2"]
    end
    subgraph dir_ansible_roles_magic_mirror_defaults [ansible/roles/magic_mirror/defaults]
        direction TB
        node_1054["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_handlers [ansible/roles/magic_mirror/handlers]
        direction TB
        node_1052["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_tasks [ansible/roles/magic_mirror/tasks]
        direction TB
        node_1053["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_templates [ansible/roles/magic_mirror/templates]
        direction TB
        node_1051["magic_mirror.nomad.j2"]
    end
    subgraph dir_ansible_roles_mcp_server_defaults [ansible/roles/mcp_server/defaults]
        direction TB
        node_1250["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_handlers [ansible/roles/mcp_server/handlers]
        direction TB
        node_1248["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_tasks [ansible/roles/mcp_server/tasks]
        direction TB
        node_1249["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_templates [ansible/roles/mcp_server/templates]
        direction TB
        node_1247["mcp_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_graph_tasks [ansible/roles/memory_graph/tasks]
        direction TB
        node_1328["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_graph_templates [ansible/roles/memory_graph/templates]
        direction TB
        node_1326["load_image_task.nomad.j2"]
        node_1327["memory-graph.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_service_files [ansible/roles/memory_service/files]
        direction TB
        node_1171["app.py"]
        node_1172["pmm_memory.py"]
    end
    subgraph dir_ansible_roles_memory_service_handlers [ansible/roles/memory_service/handlers]
        direction TB
        node_1169["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_tasks [ansible/roles/memory_service/tasks]
        direction TB
        node_1170["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_templates [ansible/roles/memory_service/templates]
        direction TB
        node_1167["load_image_task.nomad.j2"]
        node_1168["memory_service.nomad.j2"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files [ansible/roles/minikeyvalue/files]
        direction TB
        node_1069["Dockerfile"]
        node_1071["start_master.py"]
        node_1070["volume"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files_src [ansible/roles/minikeyvalue/files/src]
        direction TB
        node_1072["lib.go"]
        node_1075["lib_test.go"]
        node_1077["main.go"]
        node_1078["rebalance.go"]
        node_1073["rebuild.go"]
        node_1074["s3api.go"]
        node_1076["server.go"]
    end
    subgraph dir_ansible_roles_minikeyvalue_tasks [ansible/roles/minikeyvalue/tasks]
        direction TB
        node_1068["main.yaml"]
    end
    subgraph dir_ansible_roles_minikeyvalue_templates [ansible/roles/minikeyvalue/templates]
        direction TB
        node_1067["mkv.nomad.j2"]
    end
    subgraph dir_ansible_roles_miniray_files [ansible/roles/miniray/files]
        direction TB
        node_1336["Dockerfile"]
    end
    subgraph dir_ansible_roles_miniray_tasks [ansible/roles/miniray/tasks]
        direction TB
        node_1335["main.yaml"]
    end
    subgraph dir_ansible_roles_miniray_templates [ansible/roles/miniray/templates]
        direction TB
        node_1334["miniray.nomad.j2"]
    end
    subgraph dir_ansible_roles_moe_gateway_files [ansible/roles/moe_gateway/files]
        direction TB
        node_1150["gateway.py"]
    end
    subgraph dir_ansible_roles_moe_gateway_files_static [ansible/roles/moe_gateway/files/static]
        direction TB
        node_1151["index.html"]
    end
    subgraph dir_ansible_roles_moe_gateway_handlers [ansible/roles/moe_gateway/handlers]
        direction TB
        node_1148["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_tasks [ansible/roles/moe_gateway/tasks]
        direction TB
        node_1149["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_templates [ansible/roles/moe_gateway/templates]
        direction TB
        node_1147["moe-gateway.nomad.j2"]
    end
    subgraph dir_ansible_roles_monitoring_defaults [ansible/roles/monitoring/defaults]
        direction TB
        node_1275["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_files [ansible/roles/monitoring/files]
        direction TB
        node_1276["llm_dashboard.json"]
    end
    subgraph dir_ansible_roles_monitoring_tasks [ansible/roles/monitoring/tasks]
        direction TB
        node_1274["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_templates [ansible/roles/monitoring/templates]
        direction TB
        node_1266["beszel-agent.nomad.j2"]
        node_1263["beszel-hub.nomad.j2"]
        node_1268["dashboards.yaml.j2"]
        node_1267["datasource.yaml.j2"]
        node_1273["grafana.nomad.j2"]
        node_1264["memory-audit.nomad.j2"]
        node_1265["mqtt-exporter.nomad.j2"]
        node_1272["node-exporter.nomad.j2"]
        node_1269["prometheus.nomad.j2"]
        node_1271["prometheus.yml.j2"]
        node_1270["statsping.nomad.j2"]
    end
    subgraph dir_ansible_roles_mqtt_meta [ansible/roles/mqtt/meta]
        direction TB
        node_1190["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_tasks [ansible/roles/mqtt/tasks]
        direction TB
        node_1189["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_templates [ansible/roles/mqtt/templates]
        direction TB
        node_1187["mosquitto.conf.j2"]
        node_1188["mqtt.nomad.j2"]
    end
    subgraph dir_ansible_roles_nanochat_defaults [ansible/roles/nanochat/defaults]
        direction TB
        node_1332["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_handlers [ansible/roles/nanochat/handlers]
        direction TB
        node_1330["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_tasks [ansible/roles/nanochat/tasks]
        direction TB
        node_1331["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_templates [ansible/roles/nanochat/templates]
        direction TB
        node_1329["nanochat.nomad.j2"]
    end
    subgraph dir_ansible_roles_nats_handlers [ansible/roles/nats/handlers]
        direction TB
        node_1223["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_tasks [ansible/roles/nats/tasks]
        direction TB
        node_1224["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_templates [ansible/roles/nats/templates]
        direction TB
        node_1222["nats.nomad.j2"]
    end
    subgraph dir_ansible_roles_nfs_handlers [ansible/roles/nfs/handlers]
        direction TB
        node_1321["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_tasks [ansible/roles/nfs/tasks]
        direction TB
        node_1322["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_templates [ansible/roles/nfs/templates]
        direction TB
        node_1320["exports.j2"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_handlers [ansible/roles/nixos_pxe_server/handlers]
        direction TB
        node_1358["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_tasks [ansible/roles/nixos_pxe_server/tasks]
        direction TB
        node_1359["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_templates [ansible/roles/nixos_pxe_server/templates]
        direction TB
        node_1357["boot.ipxe.nix.j2"]
        node_1356["configuration.nix.j2"]
    end
    subgraph dir_ansible_roles_nomad_defaults [ansible/roles/nomad/defaults]
        direction TB
        node_1040["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_handlers [ansible/roles/nomad/handlers]
        direction TB
        node_1036["main.yaml"]
        node_1037["restart_nomad_handler_tasks.yaml"]
    end
    subgraph dir_ansible_roles_nomad_tasks [ansible/roles/nomad/tasks]
        direction TB
        node_1038["main.yaml"]
        node_1039["tls.yaml"]
    end
    subgraph dir_ansible_roles_nomad_templates [ansible/roles/nomad/templates]
        direction TB
        node_1033["client.hcl.j2"]
        node_1031["nomad.hcl.server.j2"]
        node_1034["nomad.service.j2"]
        node_1035["nomad.sh.j2"]
        node_1032["server.hcl.j2"]
        node_1030["start_nomad.sh.j2"]
    end
    subgraph dir_ansible_roles_openclaw_files [ansible/roles/openclaw/files]
        direction TB
        node_1101["Dockerfile"]
        node_1102["pipecat_skill.md"]
    end
    subgraph dir_ansible_roles_openclaw_tasks [ansible/roles/openclaw/tasks]
        direction TB
        node_1100["main.yaml"]
    end
    subgraph dir_ansible_roles_openclaw_templates [ansible/roles/openclaw/templates]
        direction TB
        node_1098["load_image_task.nomad.j2"]
        node_1099["openclaw.nomad.j2"]
    end
    subgraph dir_ansible_roles_opencode_handlers [ansible/roles/opencode/handlers]
        direction TB
        node_1028["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_tasks [ansible/roles/opencode/tasks]
        direction TB
        node_1029["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_templates [ansible/roles/opencode/templates]
        direction TB
        node_1027["opencode.nomad.j2"]
    end
    subgraph dir_ansible_roles_opengist_handlers [ansible/roles/opengist/handlers]
        direction TB
        node_1217["main.yaml"]
    end
    subgraph dir_ansible_roles_opengist_tasks [ansible/roles/opengist/tasks]
        direction TB
        node_1218["main.yaml"]
    end
    subgraph dir_ansible_roles_opengist_templates [ansible/roles/opengist/templates]
        direction TB
        node_1216["opengist.nomad.j2"]
    end
    subgraph dir_ansible_roles_opengravity_meta [ansible/roles/opengravity/meta]
        direction TB
        node_1386["main.yaml"]
    end
    subgraph dir_ansible_roles_opengravity_tasks [ansible/roles/opengravity/tasks]
        direction TB
        node_1385["main.yaml"]
    end
    subgraph dir_ansible_roles_opengravity_templates [ansible/roles/opengravity/templates]
        direction TB
        node_1382["Dockerfile.j2"]
        node_1383["default.conf.j2"]
        node_1381["load_image_task.nomad.j2"]
        node_1384["opengravity.nomad.j2"]
    end
    subgraph dir_ansible_roles_openworkers_handlers [ansible/roles/openworkers/handlers]
        direction TB
        node_1176["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_tasks [ansible/roles/openworkers/tasks]
        direction TB
        node_1177["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_templates [ansible/roles/openworkers/templates]
        direction TB
        node_1174["openworkers-bootstrap.nomad.j2"]
        node_1175["openworkers-infra.nomad.j2"]
        node_1173["openworkers-runners.nomad.j2"]
    end
    subgraph dir_ansible_roles_paddler_tasks [ansible/roles/paddler/tasks]
        direction TB
        node_1235["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent [ansible/roles/paddler_agent]
        direction TB
        node_1360["README.md"]
    end
    subgraph dir_ansible_roles_paddler_agent_defaults [ansible/roles/paddler_agent/defaults]
        direction TB
        node_1363["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_tasks [ansible/roles/paddler_agent/tasks]
        direction TB
        node_1362["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_templates [ansible/roles/paddler_agent/templates]
        direction TB
        node_1361["paddler-agent.service.j2"]
    end
    subgraph dir_ansible_roles_paddler_balancer [ansible/roles/paddler_balancer]
        direction TB
        node_1118["README.md"]
    end
    subgraph dir_ansible_roles_paddler_balancer_defaults [ansible/roles/paddler_balancer/defaults]
        direction TB
        node_1121["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_tasks [ansible/roles/paddler_balancer/tasks]
        direction TB
        node_1120["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_templates [ansible/roles/paddler_balancer/templates]
        direction TB
        node_1119["paddler-balancer.service.j2"]
    end
    subgraph dir_ansible_roles_paperless_handlers [ansible/roles/paperless/handlers]
        direction TB
        node_1341["main.yaml"]
    end
    subgraph dir_ansible_roles_paperless_tasks [ansible/roles/paperless/tasks]
        direction TB
        node_1342["main.yaml"]
    end
    subgraph dir_ansible_roles_paperless_templates [ansible/roles/paperless/templates]
        direction TB
        node_1338["paperless-app.nomad.j2"]
        node_1339["paperless-db.nomad.j2"]
        node_1340["paperless-redis.nomad.j2"]
    end
    subgraph dir_ansible_roles_pds_tasks [ansible/roles/pds/tasks]
        direction TB
        node_1234["main.yaml"]
    end
    subgraph dir_ansible_roles_pds_templates [ansible/roles/pds/templates]
        direction TB
        node_1233["pds.nomad.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_defaults [ansible/roles/pipecatapp/defaults]
        direction TB
        node_1141["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_handlers [ansible/roles/pipecatapp/handlers]
        direction TB
        node_1139["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_tasks [ansible/roles/pipecatapp/tasks]
        direction TB
        node_1140["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates [ansible/roles/pipecatapp/templates]
        direction TB
        node_1126["architect.nomad.j2"]
        node_1123["archivist.nomad.j2"]
        node_1122["load_image_task.nomad.j2"]
        node_1127["pipecat.env.j2"]
        node_1124["pipecatapp.nomad.j2"]
        node_1128["seed-agent.nomad.j2"]
        node_1125["start_pipecatapp.sh.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_prompts [ansible/roles/pipecatapp/templates/prompts]
        direction TB
        node_1134["coding_expert.txt.j2"]
        node_1137["consolidation_expert.txt.j2"]
        node_1136["creative_expert.txt.j2"]
        node_1131["cynic_expert.txt.j2"]
        node_1132["ingestion_expert.txt.j2"]
        node_1135["memory_query_expert.txt.j2"]
        node_1133["router.txt.j2"]
        node_1138["tron_agent.txt.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_workflows [ansible/roles/pipecatapp/templates/workflows]
        direction TB
        node_1130["architect_loop.yaml.j2"]
        node_1129["default_agent_loop.yaml.j2"]
    end
    subgraph dir_ansible_roles_pollen [ansible/roles/pollen]
        direction TB
        node_1161["README.md"]
    end
    subgraph dir_ansible_roles_pollen_tasks [ansible/roles/pollen/tasks]
        direction TB
        node_1162["main.yml"]
    end
    subgraph dir_ansible_roles_polyphony_handlers [ansible/roles/polyphony/handlers]
        direction TB
        node_1214["main.yaml"]
    end
    subgraph dir_ansible_roles_polyphony_tasks [ansible/roles/polyphony/tasks]
        direction TB
        node_1215["main.yaml"]
    end
    subgraph dir_ansible_roles_polyphony_templates [ansible/roles/polyphony/templates]
        direction TB
        node_1213["polyphony.nomad.j2"]
    end
    subgraph dir_ansible_roles_postgres_handlers [ansible/roles/postgres/handlers]
        direction TB
        node_1379["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_tasks [ansible/roles/postgres/tasks]
        direction TB
        node_1380["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_templates [ansible/roles/postgres/templates]
        direction TB
        node_1378["postgres.nomad.j2"]
    end
    subgraph dir_ansible_roles_power_manager_defaults [ansible/roles/power_manager/defaults]
        direction TB
        node_1243["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_files [ansible/roles/power_manager/files]
        direction TB
        node_1244["power_agent.py"]
        node_1245["traffic_monitor.c"]
    end
    subgraph dir_ansible_roles_power_manager_handlers [ansible/roles/power_manager/handlers]
        direction TB
        node_1241["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_tasks [ansible/roles/power_manager/tasks]
        direction TB
        node_1242["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_templates [ansible/roles/power_manager/templates]
        direction TB
        node_1238["nomad-watchdog.service.j2"]
        node_1239["power-agent.service.j2"]
        node_1240["watchdog.sh.j2"]
    end
    subgraph dir_ansible_roles_preflight_checks_tasks [ansible/roles/preflight_checks/tasks]
        direction TB
        node_1348["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_files [ansible/roles/provisioning_api/files]
        direction TB
        node_1084["provisioning_api.py"]
    end
    subgraph dir_ansible_roles_provisioning_api_handlers [ansible/roles/provisioning_api/handlers]
        direction TB
        node_1082["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_tasks [ansible/roles/provisioning_api/tasks]
        direction TB
        node_1083["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_templates [ansible/roles/provisioning_api/templates]
        direction TB
        node_1081["provisioning-api.service.j2"]
    end
    subgraph dir_ansible_roles_pxe_server_defaults [ansible/roles/pxe_server/defaults]
        direction TB
        node_1230["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_handlers [ansible/roles/pxe_server/handlers]
        direction TB
        node_1228["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_tasks [ansible/roles/pxe_server/tasks]
        direction TB
        node_1229["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_templates [ansible/roles/pxe_server/templates]
        direction TB
        node_1225["boot.ipxe.j2"]
        node_1226["dhcpd.conf.j2"]
        node_1227["preseed.cfg.j2"]
    end
    subgraph dir_ansible_roles_pypi_proxy_tasks [ansible/roles/pypi_proxy/tasks]
        direction TB
        node_1232["main.yml"]
    end
    subgraph dir_ansible_roles_pypi_proxy_templates [ansible/roles/pypi_proxy/templates]
        direction TB
        node_1231["pypi_proxy.nomad.j2"]
    end
    subgraph dir_ansible_roles_python_deps_files [ansible/roles/python_deps/files]
        direction TB
        node_1325["requirements.txt"]
    end
    subgraph dir_ansible_roles_python_deps_meta [ansible/roles/python_deps/meta]
        direction TB
        node_1324["main.yaml"]
    end
    subgraph dir_ansible_roles_python_deps_tasks [ansible/roles/python_deps/tasks]
        direction TB
        node_1323["main.yaml"]
    end
    subgraph dir_ansible_roles_seed_models_files_reference_data [ansible/roles/seed_models/files/reference_data]
        direction TB
        node_1066["README.md"]
    end
    subgraph dir_ansible_roles_seed_models_tasks [ansible/roles/seed_models/tasks]
        direction TB
        node_1065["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_defaults [ansible/roles/semantic_router/defaults]
        direction TB
        node_1254["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_tasks [ansible/roles/semantic_router/tasks]
        direction TB
        node_1253["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_templates [ansible/roles/semantic_router/templates]
        direction TB
        node_1251["Dockerfile.j2"]
        node_1252["semantic-router.nomad.j2"]
    end
    subgraph dir_ansible_roles_smol_agent_server_tasks [ansible/roles/smol_agent_server/tasks]
        direction TB
        node_1080["main.yaml"]
    end
    subgraph dir_ansible_roles_smol_agent_server_templates [ansible/roles/smol_agent_server/templates]
        direction TB
        node_1079["smol-agent.nomad.j2"]
    end
    subgraph dir_ansible_roles_sunshine_defaults [ansible/roles/sunshine/defaults]
        direction TB
        node_1117["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_handlers [ansible/roles/sunshine/handlers]
        direction TB
        node_1115["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_tasks [ansible/roles/sunshine/tasks]
        direction TB
        node_1116["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_templates [ansible/roles/sunshine/templates]
        direction TB
        node_1114["sunshine.nomad.j2"]
    end
    subgraph dir_ansible_roles_system_deps_tasks [ansible/roles/system_deps/tasks]
        direction TB
        node_1060["main.yaml"]
    end
    subgraph dir_ansible_roles_tailscale_tasks [ansible/roles/tailscale/tasks]
        direction TB
        node_1333["main.yaml"]
    end
    subgraph dir_ansible_roles_telegraf [ansible/roles/telegraf]
        direction TB
        node_1193["README.md"]
    end
    subgraph dir_ansible_roles_telegraf_meta [ansible/roles/telegraf/meta]
        direction TB
        node_1197["main.yaml"]
    end
    subgraph dir_ansible_roles_telegraf_tasks [ansible/roles/telegraf/tasks]
        direction TB
        node_1196["main.yaml"]
    end
    subgraph dir_ansible_roles_telegraf_templates [ansible/roles/telegraf/templates]
        direction TB
        node_1195["telegraf.conf.j2"]
        node_1194["telegraf.nomad.j2"]
    end
    subgraph dir_ansible_roles_term_everything_tasks [ansible/roles/term_everything/tasks]
        direction TB
        node_1366["main.yml"]
    end
    subgraph dir_ansible_roles_tml_interaction [ansible/roles/tml_interaction]
        direction TB
        node_1236["README.md"]
    end
    subgraph dir_ansible_roles_tml_interaction_tasks [ansible/roles/tml_interaction/tasks]
        direction TB
        node_1237["main.yaml"]
    end
    subgraph dir_ansible_roles_tool_server [ansible/roles/tool_server]
        direction TB
        node_1284["Dockerfile"]
        node_1283["app.py"]
        node_1287["entrypoint.sh"]
        node_1285["pmm_memory.py"]
        node_1286["preload_models.py"]
    end
    subgraph dir_ansible_roles_tool_server_tasks [ansible/roles/tool_server/tasks]
        direction TB
        node_1290["main.yaml"]
    end
    subgraph dir_ansible_roles_tool_server_templates [ansible/roles/tool_server/templates]
        direction TB
        node_1288["load_image_task.nomad.j2"]
        node_1289["tool_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_tool_server_tools [ansible/roles/tool_server/tools]
        direction TB
        node_1313["ansible_tool.py"]
        node_1315["archivist_tool.py"]
        node_1294["claude_clone_tool.py"]
        node_1317["code_runner_tool.py"]
        node_1310["council_tool.py"]
        node_1308["desktop_control_tool.py"]
        node_1307["file_editor_tool.py"]
        node_1291["final_answer_tool.py"]
        node_1302["gemini_cli.py"]
        node_1301["get_nomad_job.py"]
        node_1312["git_tool.py"]
        node_1296["ha_tool.py"]
        node_1305["llxprt_code_tool.py"]
        node_1292["mcp_tool.py"]
        node_1300["opencode_tool.py"]
        node_1297["orchestrator_tool.py"]
        node_1319["planner_tool.py"]
        node_1299["power_tool.py"]
        node_1293["project_mapper_tool.py"]
        node_1318["prompt_improver_tool.py"]
        node_1314["rag_tool.py"]
        node_1316["sandbox.ts"]
        node_1298["smol_agent_tool.py"]
        node_1295["ssh_tool.py"]
        node_1311["summarizer_tool.py"]
        node_1303["swarm_tool.py"]
        node_1304["tap_service.py"]
        node_1306["term_everything_tool.py"]
        node_1309["web_browser_tool.py"]
    end
    subgraph dir_ansible_roles_tpm_ssh_handlers [ansible/roles/tpm_ssh/handlers]
        direction TB
        node_1346["main.yaml"]
    end
    subgraph dir_ansible_roles_tpm_ssh_tasks [ansible/roles/tpm_ssh/tasks]
        direction TB
        node_1347["main.yaml"]
    end
    subgraph dir_ansible_roles_tpm_ssh_templates [ansible/roles/tpm_ssh/templates]
        direction TB
        node_1343["tpm-ssh-agent.service.j2"]
        node_1344["tpm-ssh-agent.sh.j2"]
        node_1345["tpm_pins.j2"]
    end
    subgraph dir_ansible_roles_traceway_defaults [ansible/roles/traceway/defaults]
        direction TB
        node_1043["main.yaml"]
    end
    subgraph dir_ansible_roles_traceway_tasks [ansible/roles/traceway/tasks]
        direction TB
        node_1042["main.yaml"]
    end
    subgraph dir_ansible_roles_traceway_templates [ansible/roles/traceway/templates]
        direction TB
        node_1041["traceway.nomad.j2"]
    end
    subgraph dir_ansible_roles_traefik_defaults [ansible/roles/traefik/defaults]
        direction TB
        node_1206["main.yml"]
    end
    subgraph dir_ansible_roles_traefik_tasks [ansible/roles/traefik/tasks]
        direction TB
        node_1205["main.yml"]
    end
    subgraph dir_ansible_roles_traefik_templates [ansible/roles/traefik/templates]
        direction TB
        node_1204["headscale-router.yaml.j2"]
        node_1203["traefik.nomad.j2"]
    end
    subgraph dir_ansible_roles_unified_fs_defaults [ansible/roles/unified_fs/defaults]
        direction TB
        node_1201["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_files [ansible/roles/unified_fs/files]
        direction TB
        node_1202["unified_fs_agent.py"]
    end
    subgraph dir_ansible_roles_unified_fs_handlers [ansible/roles/unified_fs/handlers]
        direction TB
        node_1199["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_tasks [ansible/roles/unified_fs/tasks]
        direction TB
        node_1200["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_templates [ansible/roles/unified_fs/templates]
        direction TB
        node_1198["unified_fs.service.j2"]
    end
    subgraph dir_ansible_roles_vision_defaults [ansible/roles/vision/defaults]
        direction TB
        node_1146["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_handlers [ansible/roles/vision/handlers]
        direction TB
        node_1144["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_tasks [ansible/roles/vision/tasks]
        direction TB
        node_1145["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_templates [ansible/roles/vision/templates]
        direction TB
        node_1142["config.yml.j2"]
        node_1143["vision.nomad.j2"]
    end
    subgraph dir_ansible_roles_vllm_tasks [ansible/roles/vllm/tasks]
        direction TB
        node_1063["main.yaml"]
        node_1062["run_single_vllm_job.yaml"]
    end
    subgraph dir_ansible_roles_vllm_templates [ansible/roles/vllm/templates]
        direction TB
        node_1061["vllm-expert.nomad.j2"]
    end
    subgraph dir_ansible_roles_whisper_cpp_tasks [ansible/roles/whisper_cpp/tasks]
        direction TB
        node_1255["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service_files [ansible/roles/world_model_service/files]
        direction TB
        node_1106["Dockerfile"]
        node_1105["app.py"]
        node_1107["debug_world_model.sh"]
        node_1108["requirements.txt"]
    end
    subgraph dir_ansible_roles_world_model_service_tasks [ansible/roles/world_model_service/tasks]
        direction TB
        node_1104["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service_templates [ansible/roles/world_model_service/templates]
        direction TB
        node_1103["world_model.nomad.j2"]
    end
    subgraph dir_ansible_roles_zigbee2mqtt [ansible/roles/zigbee2mqtt]
        direction TB
        node_1277["README.md"]
    end
    subgraph dir_ansible_roles_zigbee2mqtt_meta [ansible/roles/zigbee2mqtt/meta]
        direction TB
        node_1280["main.yaml"]
    end
    subgraph dir_ansible_roles_zigbee2mqtt_tasks [ansible/roles/zigbee2mqtt/tasks]
        direction TB
        node_1279["main.yaml"]
    end
    subgraph dir_ansible_roles_zigbee2mqtt_templates [ansible/roles/zigbee2mqtt/templates]
        direction TB
        node_1278["zigbee2mqtt.nomad.j2"]
    end
    subgraph dir_ansible_tasks [ansible/tasks]
        direction TB
        node_998["README.md"]
        node_997["build_cached_image.yaml"]
        node_995["build_pipecatapp_image.yaml"]
        node_993["create_expert_job.yaml"]
        node_996["deploy_expert_wrapper.yaml"]
        node_994["deploy_model_gpu_provider.yaml"]
    end
    subgraph dir_ansible_templates_shared [ansible/templates/shared]
        direction TB
        node_990["load_image_task.nomad.j2"]
    end
    subgraph dir_ansible_tests [ansible/tests]
        direction TB
        node_1387["verify_grafana.yaml"]
        node_1388["verify_playbook_syntax.yaml"]
    end
    subgraph dir_assets [assets]
        direction TB
        node_761["llama_icon.png"]
    end
    subgraph dir_cluster_cache [cluster_cache]
        direction TB
        node_38["README.md"]
        node_36["app.py"]
        node_37["requirements.txt"]
    end
    subgraph dir_command_deck_backend [command_deck/backend]
        direction TB
        node_712["app.py"]
    end
    subgraph dir_command_deck_frontend [command_deck/frontend]
        direction TB
        node_714["index.html"]
        node_713["script.js"]
        node_715["style.css"]
    end
    subgraph dir_docker [docker]
        direction TB
        node_495["README.md"]
    end
    subgraph dir_docker_dev_container [docker/dev_container]
        direction TB
        node_497["Dockerfile"]
    end
    subgraph dir_docker_memory_service [docker/memory_service]
        direction TB
        node_496["Dockerfile"]
    end
    subgraph dir_docs [docs]
        direction TB
        node_498["DEAD_CODE_REVIEW.md"]
        node_499["README.md"]
    end
    subgraph dir_docs_analysis [docs/analysis]
        direction TB
        node_510["AGENT_LIGHTNING_ANALYSIS.md"]
        node_504["BENCHMARKING.MD"]
        node_523["CAPABILITY_ALIGNMENT_REPORT.md"]
        node_500["CEPH_EVALUATION.md"]
        node_517["CLAMAV_EVALUATION.md"]
        node_521["CLAUDE_CODE_ANALYSIS.md"]
        node_501["DIRAC_EVALUATION.md"]
        node_524["EVALUATION_LLMROUTER.md"]
        node_502["FLOWISE_ANALYSIS.md"]
        node_503["GCP_GENERATIVE_AI_REVIEW.md"]
        node_505["GNUTELLA_ANALYSIS.md"]
        node_515["HAYSTACK_ANALYSIS.md"]
        node_514["HELIXDB_EVALUATION.md"]
        node_508["IPV6_AUDIT.md"]
        node_511["LANGCHAIN_ANALYSIS.md"]
        node_516["LITEGRAPH_VS_REACTFLOW.md"]
        node_525["MEMENTO_SKILLS_ANALYSIS.md"]
        node_519["PASEO_ANALYSIS.md"]
        node_507["POLLEN_COMPARISON.md"]
        node_520["REFACTOR_PROPOSAL_hybrid_architecture.md"]
        node_509["SECURITY_AUDIT.md"]
        node_522["TOOL_EVALUATION.md"]
        node_513["VLLM_PROJECT_EVALUATION.md"]
        node_506["YAML_FILES_REPORT.md"]
        node_518["aid_e_log.txt"]
        node_512["heretic_evaluation.md"]
        node_526["review_report.md"]
    end
    subgraph dir_docs_manual [docs/manual]
        direction TB
        node_544["AGENTS.md"]
        node_553["AGENT_HANDBOOK.md"]
        node_531["AI_GOVERNANCE.md"]
        node_555["ARCHITECTURE.md"]
        node_539["DEPLOYMENT_AND_PROFILING.md"]
        node_548["DIRAC_TODO.md"]
        node_540["EXTERNAL_APP_HOSTING_GUIDE.md"]
        node_533["FRONTEND_VERIFICATION.md"]
        node_550["FRONTIER_AGENT_ROADMAP.md"]
        node_542["GASTOWN_TODO.md"]
        node_529["GEMINI.md"]
        node_534["LOAD_TESTING.md"]
        node_536["MCP_MIGRATION_PLAN.md"]
        node_546["MCP_SERVER_SETUP.md"]
        node_552["MEMORIES.md"]
        node_554["NETWORK.md"]
        node_543["NETWORK_ISOLATION.md"]
        node_535["NIXOS_PXE_BOOT_SETUP.md"]
        node_527["OBSIDIAN_TODO.md"]
        node_541["OBSIDIAN_WORKFLOW_DESIGN.md"]
        node_549["PERFORMANCE_OPTIMIZATION.md"]
        node_538["PROJECT_SUMMARY.md"]
        node_545["PXE_BOOT_SETUP.md"]
        node_528["REMOTE_WORKFLOW.md"]
        node_532["SCALING_TODO.md"]
        node_547["SPIRE_POC.md"]
        node_530["TODO_Hybrid_Architecture.md"]
        node_551["TROUBLESHOOTING.md"]
        node_537["TWINSERVICE_DEMONOLITHIZATION_DESIGN.md"]
    end
    subgraph dir_docs_media [docs/media]
        direction TB
        node_556["initial_state.png"]
        node_557["paused_state.png"]
    end
    subgraph dir_evaluations [evaluations]
        direction TB
        node_709["ds4_evaluation.md"]
        node_707["dspark_speculative_decoding_report.md"]
        node_705["ktx_evaluation.md"]
        node_711["longcat_2.0_evaluation.md"]
        node_710["mesh_llm_evaluation.md"]
        node_706["mindwalk_evaluation.md"]
        node_708["ornith-1-evaluation.md"]
    end
    subgraph dir_examples [examples]
        direction TB
        node_49["README.md"]
        node_48["chat-persistent.sh"]
    end
    subgraph dir_examples_external_apps [examples/external_apps]
        direction TB
        node_50["mesh_llm.json"]
    end
    subgraph dir_group_vars [group_vars]
        direction TB
        node_179["README.md"]
        node_180["all.yaml"]
        node_178["external_experts.yaml"]
        node_177["models.yaml"]
    end
    subgraph dir_host_vars [host_vars]
        direction TB
        node_754["README.md"]
        node_753["localhost.yaml"]
    end
    subgraph dir_initial_setup [initial-setup]
        direction TB
        node_977["README.md"]
        node_976["add_new_worker.sh"]
        node_975["setup.conf"]
        node_974["setup.sh"]
        node_973["update_inventory.sh"]
    end
    subgraph dir_initial_setup_modules [initial-setup/modules]
        direction TB
        node_982["01-network.sh"]
        node_978["02-hostname.sh"]
        node_979["03-user.sh"]
        node_981["04-ssh.sh"]
        node_980["05-auto-provision.sh"]
        node_983["README.md"]
    end
    subgraph dir_initial_setup_worker_setup [initial-setup/worker-setup]
        direction TB
        node_985["README.md"]
        node_984["setup.sh"]
    end
    subgraph dir_modules_keystone_polyphony [modules/keystone-polyphony]
        direction TB
        node_62[".flake8"]
        node_51[".gitignore"]
        node_66["AGENTS.md"]
        node_63["CODE_OF_CONDUCT.md"]
        node_58["CONTRIBUTING.md"]
        node_54["Dockerfile"]
        node_61["ENSEMBLE_TRIAL.md"]
        node_53["LICENSE"]
        node_70["README.md"]
        node_52["TODO.md"]
        node_65["WORK_ORDER.md"]
        node_67["docker-compose.yml"]
        node_64["install.sh"]
        node_68["jules_config.json"]
        node_56["keystone-polyphony.sh"]
        node_69["kp"]
        node_60["polyphony"]
        node_59["requirements.txt"]
        node_55["simulate_swarm.py"]
        node_57["simulation.log"]
    end
    subgraph dir_modules_keystone_polyphony__agents_workflows [modules/keystone-polyphony/.agents/workflows]
        direction TB
        node_143["0-click-boot.md"]
        node_141["boot.md"]
        node_142["swarm-communication.md"]
    end
    subgraph dir_modules_keystone_polyphony__devcontainer [modules/keystone-polyphony/.devcontainer]
        direction TB
        node_144["devcontainer.json"]
    end
    subgraph dir_modules_keystone_polyphony__githooks [modules/keystone-polyphony/.githooks]
        direction TB
        node_117["pre-commit"]
        node_116["pre-push"]
    end
    subgraph dir_modules_keystone_polyphony__github [modules/keystone-polyphony/.github]
        direction TB
        node_146["reviewers.yml"]
    end
    subgraph dir_modules_keystone_polyphony__github_workflows [modules/keystone-polyphony/.github/workflows]
        direction TB
        node_152["add-contributors.yml"]
        node_148["agent-issue-solver.yml"]
        node_156["agent-issue-triage.yml"]
        node_155["agent-parallel-solver.yml"]
        node_151["auto-merge-staging.yml"]
        node_157["daily-close-merged-issues.yml"]
        node_147["opencode.yml"]
        node_154["periodic-merge-main.yml"]
        node_153["swarm-node.yml"]
        node_149["workflow-review-dispatch.yml"]
        node_150["workflow-review.yml"]
    end
    subgraph dir_modules_keystone_polyphony_docs [modules/keystone-polyphony/docs]
        direction TB
        node_108["architecture.md"]
        node_104["ci-cd.md"]
        node_106["getting-started.md"]
        node_105["git-hooks-architecture.md"]
        node_103["hooks-interaction.md"]
        node_107["liminal-bridge.md"]
        node_109["swarm-coordination.md"]
        node_102["vscode-integration.md"]
        node_101["zed-integration.md"]
    end
    subgraph dir_modules_keystone_polyphony_docs_features [modules/keystone-polyphony/docs/features]
        direction TB
        node_115["git-hooks.feature"]
    end
    subgraph dir_modules_keystone_polyphony_docs_issues_pre_review [modules/keystone-polyphony/docs/issues-pre-review]
        direction TB
        node_114["vision-and-impact.md"]
    end
    subgraph dir_modules_keystone_polyphony_docs_swarm_discovery [modules/keystone-polyphony/docs/swarm-discovery]
        direction TB
        node_112["analysis.md"]
        node_111["architecture-diagram.md"]
        node_110["hardware-bom.md"]
        node_113["modality-matrix.md"]
    end
    subgraph dir_modules_keystone_polyphony_features [modules/keystone-polyphony/features]
        direction TB
        node_158["hooks.feature"]
    end
    subgraph dir_modules_keystone_polyphony_meta [modules/keystone-polyphony/meta]
        direction TB
        node_145["DISCOVERIES.md"]
    end
    subgraph dir_modules_keystone_polyphony_scripts [modules/keystone-polyphony/scripts]
        direction TB
        node_136["agent-boot.sh"]
        node_118["broadcast.py"]
        node_130["deduplicate.py"]
        node_120["dispatch-work-order.sh"]
        node_134["exchange_ssh_keys.py"]
        node_125["inject-secrets.sh"]
        node_122["install-hooks.sh"]
        node_140["lint.sh"]
        node_139["load_test.py"]
        node_137["package.json"]
        node_119["ping.py"]
        node_131["refine_issue.py"]
        node_135["run-tests.sh"]
        node_124["setup-ensemble.sh"]
        node_129["setup-swarm.js"]
        node_132["setup-vscode.sh"]
        node_126["setup-zed.sh"]
        node_128["share.py"]
        node_133["status.py"]
        node_121["swarm_status.py"]
        node_127["triage-dispatch.sh"]
        node_138["triage-lib.sh"]
        node_123["worker_loop.py"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge [modules/keystone-polyphony/src/liminal_bridge]
        direction TB
        node_77["__init__.py"]
        node_75["architect.py"]
        node_72["crdt.py"]
        node_81["dashboard.py"]
        node_71["mesh.py"]
        node_73["observability.py"]
        node_76["pulse.py"]
        node_74["server.py"]
        node_80["test_architect.py"]
        node_78["test_key_rotation.py"]
        node_79["test_mesh.py"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_dashboard_ui [modules/keystone-polyphony/src/liminal_bridge/dashboard_ui]
        direction TB
        node_83["index.html"]
        node_84["package.json"]
        node_82["vite.config.js"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_dashboard_ui_src [modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src]
        direction TB
        node_85["App.css"]
        node_87["App.jsx"]
        node_89["crypto.js"]
        node_86["index.css"]
        node_88["main.jsx"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_dashboard_ui_src_components [modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components]
        direction TB
        node_93["Backlog.jsx"]
        node_92["Batons.jsx"]
        node_98["Discussions.jsx"]
        node_95["KVStore.jsx"]
        node_91["Login.jsx"]
        node_90["Logs.jsx"]
        node_97["NetworkGraph.jsx"]
        node_96["Status.jsx"]
        node_94["Thoughts.jsx"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_sidecar [modules/keystone-polyphony/src/liminal_bridge/sidecar]
        direction TB
        node_99["bridge.js"]
        node_100["package.json"]
    end
    subgraph dir_modules_keystone_polyphony_tests [modules/keystone-polyphony/tests]
        direction TB
        node_163["issue_19_verification.txt"]
        node_164["test_activation.sh"]
        node_172["test_architect_commands.py"]
        node_171["test_architect_ollama.py"]
        node_162["test_attenuation.py"]
        node_169["test_crdt.py"]
        node_168["test_ensemble_chat.py"]
        node_173["test_fallback.py"]
        node_165["test_install.sh"]
        node_167["test_mesh_crdt.py"]
        node_161["test_mesh_encryption.py"]
        node_170["test_network_simulation.py"]
        node_166["test_ssh_exchange.py"]
        node_176["test_stigmergy.py"]
        node_160["test_tandem.py"]
        node_174["test_tasks.py"]
        node_159["test_unread_tracking.py"]
        node_175["test_vector_clock.py"]
    end
    subgraph dir_os_image [os-image]
        direction TB
        node_763["README.md"]
        node_762["build_iso.sh"]
    end
    subgraph dir_os_image_config_archives [os-image/config/archives]
        direction TB
        node_779["rocm.key.binary"]
        node_778["rocm.key.chroot"]
        node_780["rocm.list.binary"]
        node_777["rocm.list.chroot"]
    end
    subgraph dir_os_image_config_hooks_live [os-image/config/hooks/live]
        direction TB
        node_765["01-setup-users.chroot"]
        node_766["02-enable-services.chroot"]
        node_764["03-setup-command-deck.chroot"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_profile_d [os-image/config/includes.chroot/etc/profile.d]
        direction TB
        node_768["99-pipecat-welcome.sh"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_sddm_conf_d [os-image/config/includes.chroot/etc/sddm.conf.d]
        direction TB
        node_772["autologin.conf"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_systemd_system [os-image/config/includes.chroot/etc/systemd/system]
        direction TB
        node_770["pipecat-firstboot.service"]
        node_769["pipecat-hostname.service"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_systemd_system_multi_user_target_wants [os-image/config/includes.chroot/etc/systemd/system/multi-user.target.wants]
        direction TB
        node_771["pipecat-firstboot.service"]
    end
    subgraph dir_os_image_config_includes_chroot_usr_local_bin [os-image/config/includes.chroot/usr/local/bin]
        direction TB
        node_774["command-deck-session"]
        node_773["setup-ssh-keys.sh"]
    end
    subgraph dir_os_image_config_includes_chroot_usr_share_wayland_sessions [os-image/config/includes.chroot/usr/share/wayland-sessions]
        direction TB
        node_775["command-deck.desktop"]
    end
    subgraph dir_os_image_config_includes_installer [os-image/config/includes.installer]
        direction TB
        node_776["preseed.cfg"]
    end
    subgraph dir_os_image_config_package_lists [os-image/config/package-lists]
        direction TB
        node_767["pipecat.list.chroot"]
    end
    subgraph dir_pipecat_agent_extension [pipecat-agent-extension]
        direction TB
        node_971["README.md"]
        node_968["example.ts"]
        node_967["gemini-extension.json"]
        node_970["package.json"]
        node_969["tsconfig.json"]
    end
    subgraph dir_pipecat_agent_extension_commands_pipecat [pipecat-agent-extension/commands/pipecat]
        direction TB
        node_972["send.toml"]
    end
    subgraph dir_pipecatapp [pipecatapp]
        direction TB
        node_193["Dockerfile"]
        node_231["README.md"]
        node_190["TODO.md"]
        node_204["__init__.py"]
        node_207["agent_factory.py"]
        node_221["api_keys.py"]
        node_189["app.py"]
        node_198["archivist_service.py"]
        node_192["durable_execution.py"]
        node_210["expert_tracker.py"]
        node_209["file_ingestion.py"]
        node_227["generate_real_embeddings.py"]
        node_206["gossip_discovery.py"]
        node_225["janitor_agent.py"]
        node_187["judge_agent.py"]
        node_208["langchain_memory_wrappers.py"]
        node_200["llm_clients.py"]
        node_184["local_llm.py"]
        node_224["local_world_model.py"]
        node_182["manager_agent.py"]
        node_185["memory.py"]
        node_186["memory_backends.py"]
        node_222["memory_legacy.py"]
        node_219["models.py"]
        node_213["moondream_detector.py"]
        node_188["mqtt_world_model_client.py"]
        node_217["mtac_pipeline.py"]
        node_195["net_utils.py"]
        node_202["network_scanner.py"]
        node_201["ontology.py"]
        node_223["pmm_memory.py"]
        node_215["pmm_memory_client.py"]
        node_196["quality_control.py"]
        node_203["rate_limiter.py"]
        node_205["requirements.txt"]
        node_233["router_config.yaml"]
        node_218["router_train_embeddings.pt"]
        node_226["router_trained_model.pkl"]
        node_216["router_training_data.csv"]
        node_228["router_training_data.jsonl"]
        node_214["secret_manager.py"]
        node_212["security.py"]
        node_183["skill_library.py"]
        node_194["start_archivist.sh"]
        node_229["task_supervisor.py"]
        node_191["technician_agent.py"]
        node_220["test_moondream_detector.py"]
        node_232["test_pmm_memory.py"]
        node_197["test_server.py"]
        node_181["tool_server.py"]
        node_230["train_router.py"]
        node_211["web_server.py"]
        node_199["worker_agent.py"]
    end
    subgraph dir_pipecatapp_datasets [pipecatapp/datasets]
        direction TB
        node_328["sycophancy_prompts.json"]
    end
    subgraph dir_pipecatapp_integrations [pipecatapp/integrations]
        direction TB
        node_257["__init__.py"]
        node_258["openclaw.py"]
    end
    subgraph dir_pipecatapp_memory_backends_impl [pipecatapp/memory_backends_impl]
        direction TB
        node_492["__init__.py"]
        node_494["crdt_backend.py"]
        node_491["helix_backend.py"]
        node_493["helix_client.py"]
    end
    subgraph dir_pipecatapp_memory_graph_service [pipecatapp/memory_graph_service]
        direction TB
        node_234["Dockerfile"]
        node_236["helix_server.py"]
        node_235["server.py"]
    end
    subgraph dir_pipecatapp_mtac [pipecatapp/mtac]
        direction TB
        node_344["eval_sft.py"]
        node_346["torchtune_sft.py"]
        node_345["unsloth_sft.py"]
    end
    subgraph dir_pipecatapp_nomad_templates [pipecatapp/nomad_templates]
        direction TB
        node_292["immich.nomad.hcl"]
        node_290["readeck.nomad.hcl"]
        node_291["uptime-kuma.nomad.hcl"]
        node_293["vaultwarden.nomad.hcl"]
    end
    subgraph dir_pipecatapp_prompts [pipecatapp/prompts]
        direction TB
        node_321["coding_expert.txt"]
        node_327["consolidation_expert.txt"]
        node_325["creative_expert.txt"]
        node_323["ingestion_expert.txt"]
        node_326["memory_query_expert.txt"]
        node_324["router.txt"]
        node_322["tron_agent.txt"]
    end
    subgraph dir_pipecatapp_resources_apps [pipecatapp/resources/apps]
        direction TB
        node_455["mesh_llm.json"]
    end
    subgraph dir_pipecatapp_resources_skills [pipecatapp/resources/skills]
        direction TB
        node_457["backpass.md"]
        node_458["renovate.md"]
        node_456["scaffold-setup-skill.md"]
    end
    subgraph dir_pipecatapp_servers [pipecatapp/servers]
        direction TB
        node_320["shell_server.py"]
    end
    subgraph dir_pipecatapp_services [pipecatapp/services]
        direction TB
        node_238["__init__.py"]
        node_239["gemma_e2b_service.py"]
        node_237["obsidian_gardener.py"]
    end
    subgraph dir_pipecatapp_services_code_runner [pipecatapp/services/code_runner]
        direction TB
        node_255["Dockerfile"]
        node_256["code_runner_server.py"]
    end
    subgraph dir_pipecatapp_services_ipfs_apt_proxy [pipecatapp/services/ipfs_apt_proxy]
        direction TB
        node_251["Dockerfile"]
        node_250["main.py"]
        node_252["requirements.txt"]
    end
    subgraph dir_pipecatapp_services_ipfs_pypi_proxy [pipecatapp/services/ipfs_pypi_proxy]
        direction TB
        node_248["Dockerfile"]
        node_247["main.py"]
        node_249["requirements.txt"]
    end
    subgraph dir_pipecatapp_services_push_proxy [pipecatapp/services/push_proxy]
        direction TB
        node_246["README.md"]
        node_244["__init__.py"]
        node_245["client.py"]
        node_243["server.py"]
    end
    subgraph dir_pipecatapp_services_rag [pipecatapp/services/rag]
        direction TB
        node_253["Dockerfile"]
        node_254["rag_server.py"]
    end
    subgraph dir_pipecatapp_services_ternlight [pipecatapp/services/ternlight]
        direction TB
        node_240["Dockerfile"]
        node_242["package.json"]
        node_241["ternlight_server.js"]
    end
    subgraph dir_pipecatapp_static [pipecatapp/static]
        direction TB
        node_310["cluster.html"]
        node_306["cluster_viz.html"]
        node_311["index.html"]
        node_308["monitor.html"]
        node_312["terminal.js"]
        node_309["vr_index.html"]
        node_305["workflow.html"]
        node_307["workflow_3d.html"]
    end
    subgraph dir_pipecatapp_static_css [pipecatapp/static/css]
        direction TB
        node_313["litegraph.css"]
        node_314["styles.css"]
    end
    subgraph dir_pipecatapp_static_js [pipecatapp/static/js]
        direction TB
        node_316["dagre.min.js"]
        node_317["editor.js"]
        node_315["litegraph.js"]
        node_319["ternlight_client.js"]
        node_318["workflow.js"]
    end
    subgraph dir_pipecatapp_tests [pipecatapp/tests]
        direction TB
        node_462["test_audio_streamer.py"]
        node_477["test_browser_tool_security.py"]
        node_485["test_container_registry_tool.py"]
        node_481["test_cq_tool.py"]
        node_474["test_document_tool.py"]
        node_479["test_gemma_e2b_service.py"]
        node_488["test_git_tool_security.py"]
        node_467["test_llm_clients.py"]
        node_461["test_llm_clients_new.py"]
        node_486["test_metrics_cache.py"]
        node_478["test_mindwalk_exporter.py"]
        node_471["test_net_utils.py"]
        node_468["test_new_skills.py"]
        node_460["test_openclaw.py"]
        node_475["test_ouroboros.py"]
        node_465["test_piper_async.py"]
        node_459["test_proxy_security.py"]
        node_480["test_rag_pruning.py"]
        node_463["test_rag_tool.py"]
        node_470["test_rate_limiter.py"]
        node_487["test_schema_mapper_tool.py"]
        node_476["test_security.py"]
        node_464["test_stt_optimization.py"]
        node_473["test_technician_agent.py"]
        node_469["test_tool_server.py"]
        node_482["test_uilogger_redaction.py"]
        node_483["test_web_server_unit.py"]
        node_484["test_websocket_security.py"]
        node_466["test_xss_prevention.py"]
        node_472["test_yolo_optimization.py"]
    end
    subgraph dir_pipecatapp_tests_workflow [pipecatapp/tests/workflow]
        direction TB
        node_490["test_history.py"]
        node_489["test_serialization_perf.py"]
    end
    subgraph dir_pipecatapp_tools [pipecatapp/tools]
        direction TB
        node_377["__init__.py"]
        node_412["ansible_tool.py"]
        node_420["archivist_tool.py"]
        node_414["ast_editor_tool.py"]
        node_365["atproto_tool.py"]
        node_407["autoloop_tool.py"]
        node_372["autoresearch_tool.py"]
        node_360["claude_clone_tool.py"]
        node_359["cluster_status_tool.py"]
        node_425["code_runner_tool.py"]
        node_387["container_registry_tool.py"]
        node_353["context_upload_tool.py"]
        node_408["council_tool.py"]
        node_364["cq_tool.py"]
        node_370["dependency_scanner_tool.py"]
        node_405["desktop_control_tool.py"]
        node_385["document_tool.py"]
        node_427["dynamic_skill_tool.py"]
        node_378["execution_history.py"]
        node_401["experiment_tool.py"]
        node_397["external_app_manager_tool.py"]
        node_404["file_editor_tool.py"]
        node_348["final_answer_tool.py"]
        node_395["gemini_cli.py"]
        node_393["get_nomad_job.py"]
        node_411["git_tool.py"]
        node_367["ha_tool.py"]
        node_349["heretic_tool.py"]
        node_386["jules_tool.py"]
        node_352["langchain_adapter.py"]
        node_415["langchain_adapter_tool.py"]
        node_409["lightweight_project_mapper_tool.py"]
        node_402["llxprt_code_tool.py"]
        node_363["mcp_client_adapter.py"]
        node_350["mcp_tool.py"]
        node_382["mtac_tool.py"]
        node_375["ocr_tool.py"]
        node_424["open_workers_tool.py"]
        node_376["openclaw_tool.py"]
        node_347["opencode_provider_tool.py"]
        node_379["opencode_tool.py"]
        node_369["orchestrator_tool.py"]
        node_413["ouroboros_tool.py"]
        node_351["p2p_sync_tool.py"]
        node_358["personality_tool.py"]
        node_428["planner_tool.py"]
        node_388["polyphony_tool.py"]
        node_373["power_tool.py"]
        node_356["project_mapper_tool.py"]
        node_422["project_overview_tool.py"]
        node_426["prompt_improver_tool.py"]
        node_416["rag_tool.py"]
        node_355["remote_code_runner_tool.py"]
        node_362["remote_rag_tool.py"]
        node_354["remote_tool_proxy.py"]
        node_381["retry_utils.py"]
        node_421["sandbox.ts"]
        node_423["save_skill_tool.py"]
        node_390["scale_compute_tool.py"]
        node_374["scheduler_tool.py"]
        node_389["schema_mapper_tool.py"]
        node_398["search_skills_tool.py"]
        node_394["search_tool.py"]
        node_383["set_operational_mode_tool.py"]
        node_392["shell_tool.py"]
        node_384["skill_builder_tool.py"]
        node_371["smol_agent_tool.py"]
        node_418["spec_loader_tool.py"]
        node_361["ssh_tool.py"]
        node_419["submit_solution_tool.py"]
        node_410["summarizer_tool.py"]
        node_396["swarm_tool.py"]
        node_400["tap_service.py"]
        node_403["term_everything_tool.py"]
        node_391["ternlight_tool.py"]
        node_366["test_git_tool.py"]
        node_399["test_ssh_tool.py"]
        node_368["update_litellm_tool.py"]
        node_417["vr_tool.py"]
        node_357["wasm_tool.py"]
        node_406["web_browser_tool.py"]
        node_380["wol_tool.py"]
    end
    subgraph dir_pipecatapp_tools_repo_map_impl [pipecatapp/tools/repo_map_impl]
        direction TB
        node_433["__init__.py"]
        node_432["cache.py"]
        node_435["cli.py"]
        node_434["config.py"]
        node_436["discover.py"]
        node_437["languages.py"]
        node_431["model.py"]
        node_429["pipeline.py"]
        node_430["rank.py"]
    end
    subgraph dir_pipecatapp_tools_repo_map_impl_extract [pipecatapp/tools/repo_map_impl/extract]
        direction TB
        node_447["__init__.py"]
        node_446["python_ast.py"]
        node_448["tree_sitter.py"]
    end
    subgraph dir_pipecatapp_tools_repo_map_impl_queries [pipecatapp/tools/repo_map_impl/queries]
        direction TB
        node_440["ATTRIBUTION.md"]
        node_444["go-tags.scm"]
        node_445["javascript-tags.scm"]
        node_442["python-tags.scm"]
        node_438["rust-tags.scm"]
        node_441["swift-tags.scm"]
        node_439["tsx-tags.scm"]
        node_443["typescript-tags.scm"]
    end
    subgraph dir_pipecatapp_tools_repo_map_impl_render [pipecatapp/tools/repo_map_impl/render]
        direction TB
        node_450["__init__.py"]
        node_451["catalog.py"]
        node_454["file_index.py"]
        node_449["json_out.py"]
        node_453["navigation.py"]
        node_452["tree.py"]
    end
    subgraph dir_pipecatapp_ui_opengravity [pipecatapp/ui/opengravity]
        direction TB
        node_333["CONTRIBUTING.md"]
        node_330["LICENSE"]
        node_338["README.md"]
        node_331["_headers"]
        node_329["agent.js"]
        node_337["iconstyles.css"]
        node_335["index.html"]
        node_334["script.js"]
        node_332["server.py"]
        node_339["seti.woff"]
        node_336["style.css"]
    end
    subgraph dir_pipecatapp_ui_opengravity_assets [pipecatapp/ui/opengravity/assets]
        direction TB
        node_342["html site example.png"]
        node_341["icon.jpeg"]
        node_343["screenshot.png"]
    end
    subgraph dir_pipecatapp_ui_opengravity_webcontainer_connect [pipecatapp/ui/opengravity/webcontainer/connect]
        direction TB
        node_340["index.html"]
    end
    subgraph dir_pipecatapp_utils [pipecatapp/utils]
        direction TB
        node_265["__init__.py"]
        node_266["app_manager.py"]
        node_260["backon_utils.py"]
        node_263["command_runner.py"]
        node_261["coverage_check.py"]
        node_259["file_utils.py"]
        node_267["ingest_skills.py"]
        node_262["mindwalk_exporter.py"]
        node_264["rag_pruner.py"]
        node_268["ssh_utils.py"]
        node_269["terminal_cleanup.py"]
    end
    subgraph dir_pipecatapp_workflow [pipecatapp/workflow]
        direction TB
        node_274["__init__.py"]
        node_272["canvas_converter.py"]
        node_276["context.py"]
        node_273["crypto_receipts.py"]
        node_277["history.py"]
        node_275["node.py"]
        node_270["nodered_converter.py"]
        node_271["runner.py"]
    end
    subgraph dir_pipecatapp_workflow_nodes [pipecatapp/workflow/nodes]
        direction TB
        node_282["__init__.py"]
        node_281["base_nodes.py"]
        node_284["consolidation_nodes.py"]
        node_280["emperor_nodes.py"]
        node_289["langchain_nodes.py"]
        node_286["llm_nodes.py"]
        node_278["rag_nodes.py"]
        node_279["ralph_nodes.py"]
        node_283["registry.py"]
        node_287["system_nodes.py"]
        node_288["tasky_nodes.py"]
        node_285["tool_nodes.py"]
    end
    subgraph dir_pipecatapp_workflows [pipecatapp/workflows]
        direction TB
        node_297["adversarial_simulation.yaml"]
        node_296["deep_context.yaml"]
        node_294["default_agent_loop.yaml"]
        node_299["dft_workflow.yaml"]
        node_304["document_ingestion.yaml"]
        node_295["looped_reasoning.yaml"]
        node_301["manager.yaml"]
        node_302["poc_ensemble.yaml"]
        node_300["sandbox.yaml"]
        node_298["tiered_agent_loop.yaml"]
        node_303["update_litellm_workflow.yaml"]
    end
    subgraph dir_playbooks [playbooks]
        direction TB
        node_664["README.md"]
        node_650["app_jobs.yaml"]
        node_644["benchmark_single_model.yaml"]
        node_648["cluster_status.yaml"]
        node_657["common_setup.yaml"]
        node_645["controller.yaml"]
        node_638["debug_template.yaml"]
        node_643["deploy_app.yaml"]
        node_655["deploy_expert.yaml"]
        node_660["deploy_openclaw.yaml"]
        node_649["deploy_pds.yaml"]
        node_651["deploy_prompt_evolution.yaml"]
        node_641["developer_tools.yaml"]
        node_652["diagnose_failure.yaml"]
        node_647["fix_cluster.yaml"]
        node_646["heal_cluster.yaml"]
        node_663["heal_job.yaml"]
        node_642["health_check.yaml"]
        node_656["promote_controller.yaml"]
        node_665["promote_to_controller.yaml"]
        node_640["pxe_setup.yaml"]
        node_661["redeploy_pipecat.yaml"]
        node_662["run_config_manager.yaml"]
        node_639["run_consul.yaml"]
        node_659["run_health_check.yaml"]
        node_658["status-check.yaml"]
        node_654["wake.yaml"]
        node_653["worker.yaml"]
    end
    subgraph dir_playbooks_network [playbooks/network]
        direction TB
        node_686["mesh.yaml"]
        node_687["verify.yaml"]
    end
    subgraph dir_playbooks_ops [playbooks/ops]
        direction TB
        node_685["optimize_memory.yaml"]
    end
    subgraph dir_playbooks_preflight [playbooks/preflight]
        direction TB
        node_688["checks.yaml"]
    end
    subgraph dir_playbooks_services [playbooks/services]
        direction TB
        node_681["README.md"]
        node_676["ai_experts.yaml"]
        node_680["app_services.yaml"]
        node_678["apt_proxy.yaml"]
        node_673["consul.yaml"]
        node_679["core_ai_services.yaml"]
        node_677["core_infra.yaml"]
        node_671["distributed_compute.yaml"]
        node_682["docker.yaml"]
        node_670["final_verification.yaml"]
        node_669["ipfs.yaml"]
        node_683["model_services.yaml"]
        node_672["monitoring.yaml"]
        node_666["nomad.yaml"]
        node_675["nomad_client.yaml"]
        node_674["pypi_proxy.yaml"]
        node_668["seed_models_to_ipfs.yaml"]
        node_667["streaming_services.yaml"]
        node_684["training_services.yaml"]
    end
    subgraph dir_poc_crdt_memory [poc/crdt_memory]
        direction TB
        node_631["README.md"]
        node_630["run_poc.py"]
    end
    subgraph dir_poc_p2p_sync [poc/p2p_sync]
        direction TB
        node_628["README.md"]
        node_627["run_poc.py"]
        node_629["syncthing_manager.py"]
    end
    subgraph dir_poc_wasm_tool_bridge [poc/wasm_tool_bridge]
        direction TB
        node_634["README.md"]
        node_632["host.py"]
        node_633["python_tool.py"]
    end
    subgraph dir_poc_wasm_tool_bridge_text_processor [poc/wasm_tool_bridge/text_processor]
        direction TB
        node_635["Cargo.lock"]
        node_636["Cargo.toml"]
    end
    subgraph dir_poc_wasm_tool_bridge_text_processor_src [poc/wasm_tool_bridge/text_processor/src]
        direction TB
        node_637["lib.rs"]
    end
    subgraph dir_prompt_engineering [prompt_engineering]
        direction TB
        node_716["PROMPT_ENGINEERING.md"]
        node_728["README.md"]
        node_722["archive_server.py"]
        node_727["autoloop_evolve.py"]
        node_718["challenger.py"]
        node_726["create_evaluator.py"]
        node_720["evaluation_lib.py"]
        node_729["evaluator.py"]
        node_721["evolve.py"]
        node_725["promote_agent.py"]
        node_719["requirements-dev.txt"]
        node_717["run_campaign.py"]
        node_723["self_harness.py"]
        node_724["visualize_archive.py"]
    end
    subgraph dir_prompt_engineering_agents [prompt_engineering/agents]
        direction TB
        node_735["ADAPTATION_AGENT.md"]
        node_736["EVALUATOR_GENERATOR.md"]
        node_737["README.md"]
        node_732["architecture_review.md"]
        node_730["code_clean_up.md"]
        node_733["debug_and_analysis.md"]
        node_734["new_task_review.md"]
        node_731["problem_scope_framing.md"]
    end
    subgraph dir_prompt_engineering_archive [prompt_engineering/archive]
        direction TB
        node_738["agent_0.json"]
        node_740["agent_0.py"]
        node_742["agent_1.json"]
        node_743["agent_1.py"]
        node_744["agent_2.json"]
        node_739["agent_2.py"]
        node_741["agent_3.json"]
        node_745["agent_3.py"]
    end
    subgraph dir_prompt_engineering_evaluation_suite [prompt_engineering/evaluation_suite]
        direction TB
        node_747["README.md"]
        node_746["test_vision.yaml"]
    end
    subgraph dir_prompt_engineering_frontend [prompt_engineering/frontend]
        direction TB
        node_749["app.js"]
        node_750["index.html"]
        node_748["server.py"]
        node_751["style.css"]
    end
    subgraph dir_prompt_engineering_generated_evaluators [prompt_engineering/generated_evaluators]
        direction TB
        node_752[".gitignore"]
    end
    subgraph dir_prompts [prompts]
        direction TB
        node_695["README.md"]
        node_693["chat-with-bob.txt"]
        node_694["router.txt"]
    end
    subgraph dir_reflection [reflection]
        direction TB
        node_691["README.md"]
        node_690["adaptation_manager.py"]
        node_692["create_reflection.py"]
        node_689["reflect.py"]
    end
    subgraph dir_scenarios [scenarios]
        direction TB
        node_40["adr_template.md"]
        node_44["agent_behavior_template.md"]
        node_39["api_calls_template.md"]
        node_43["error_handling_template.md"]
        node_45["evaluation_scenario_template.md"]
        node_42["scheduled_task_code_quality.md"]
        node_41["ui_ux_design_template.md"]
        node_46["validation_format_template.md"]
        node_47["workflow_node_template.md"]
    end
    subgraph dir_scripts [scripts]
        direction TB
        node_609["README.md"]
        node_594["agent_fast_check.sh"]
        node_616["agent_preflight.sh"]
        node_588["agentic_workflow.sh"]
        node_595["analyze_nomad_allocs.py"]
        node_604["ansible_diff.sh"]
        node_606["app-manager.py"]
        node_593["benchmark_resources.py"]
        node_615["check_all_playbooks.sh"]
        node_566["check_deps.py"]
        node_583["ci_ansible_check.sh"]
        node_612["cleanup.sh"]
        node_589["compare_exo_llama.py"]
        node_560["create_assistant_prompts.py"]
        node_570["create_cynic_model.sh"]
        node_571["create_todo_issues.sh"]
        node_608["dance_loading.py"]
        node_600["debug_expert.sh"]
        node_564["debug_mesh.sh"]
        node_605["enroll-admin.sh"]
        node_587["evaluate_clamav.py"]
        node_568["fix_markdown.sh"]
        node_617["fix_verification_failures.sh"]
        node_581["fix_yaml.sh"]
        node_610["generate_assistant_vectors.sh"]
        node_613["generate_file_map.py"]
        node_591["generate_issue_script.py"]
        node_572["generate_signatures.py"]
        node_603["generate_tailscale_key.sh"]
        node_611["git-cleanup.sh"]
        node_561["heal_cluster.sh"]
        node_601["healer.py"]
        node_614["lint.sh"]
        node_607["lint_exclude.txt"]
        node_618["memory_audit.py"]
        node_569["nomad_checkpoint.sh"]
        node_599["profile_resources.sh"]
        node_576["provisioning.py"]
        node_602["prune_consul_services.py"]
        node_562["recover_node.py"]
        node_584["recover_os.py"]
        node_586["run_nomad.sh"]
        node_563["run_quibbler.sh"]
        node_597["run_smol_recovery.py"]
        node_578["run_tests.sh"]
        node_567["salvage_task.py"]
        node_585["setup_pxe_server.sh"]
        node_590["start_services.sh"]
        node_596["sudo_env.py"]
        node_598["supervisor.py"]
        node_577["test_playbooks_dry_run.sh"]
        node_574["test_playbooks_live_run.sh"]
        node_580["test_swarm_map_reduce.py"]
        node_575["troubleshoot.py"]
        node_582["uninstall.sh"]
        node_579["update_cluster.sh"]
        node_592["update_resource_limits.py"]
        node_565["verify_consul_attributes.sh"]
        node_573["verify_ui_accessibility.py"]
    end
    subgraph dir_scripts_debug [scripts/debug]
        direction TB
        node_620["README.md"]
        node_619["test_mqtt_connection.py"]
    end
    subgraph dir_tests [tests]
        direction TB
        node_801["README.md"]
        node_795["__init__.py"]
        node_797["test.wav"]
        node_796["test_agent_patterns.py"]
        node_788["test_canvas_integration.py"]
        node_791["test_deep_context.py"]
        node_793["test_event_bus.py"]
        node_802["test_experiment_tool.py"]
        node_787["test_gastown_judge.py"]
        node_792["test_gastown_memory.py"]
        node_794["test_gastown_stats.py"]
        node_786["test_imports.py"]
        node_790["test_manager_flow.py"]
        node_798["test_project_overview_tool.py"]
        node_789["test_spec_loader.py"]
        node_785["test_ssrf_validation.py"]
        node_799["test_websocket_security.py"]
        node_784["verify_config_load.py"]
        node_800["verify_dlq.py"]
    end
    subgraph dir_tests_e2e [tests/e2e]
        direction TB
        node_966["README.md"]
        node_961["__init__.py"]
        node_962["test_api.py"]
        node_959["test_intelligent_routing.py"]
        node_960["test_mission_control.py"]
        node_964["test_palette_command_history.py"]
        node_965["test_palette_ux.py"]
        node_963["test_regression.py"]
    end
    subgraph dir_tests_integration [tests/integration]
        direction TB
        node_812["README.md"]
        node_806["__init__.py"]
        node_811["stub_services.py"]
        node_805["test_consul_role.yaml"]
        node_804["test_helixdb_e2e.py"]
        node_807["test_mini_pipeline.py"]
        node_808["test_mqtt_exporter.py"]
        node_803["test_nomad_role.yaml"]
        node_809["test_pipecat_app.py"]
        node_810["test_preemption.py"]
    end
    subgraph dir_tests_playbooks [tests/playbooks]
        direction TB
        node_951["e2e-tests.yaml"]
        node_955["test_authentik.yml"]
        node_956["test_clamav_playbook.yml"]
        node_952["test_consul.yaml"]
        node_958["test_llama_cpp.yaml"]
        node_953["test_nomad.yaml"]
        node_954["test_playbook.yml"]
        node_957["verify_cluster_network.yaml"]
    end
    subgraph dir_tests_scripts [tests/scripts]
        direction TB
        node_949["run_unit_tests.sh"]
        node_948["stress_test_cluster.py"]
        node_947["test_duplicate_role_execution.sh"]
        node_950["test_paddler.sh"]
        node_944["test_piper.sh"]
        node_946["test_run.sh"]
        node_945["verify_components.py"]
    end
    subgraph dir_tests_unit [tests/unit]
        direction TB
        node_933["README.md"]
        node_866["__init__.py"]
        node_854["conftest.py"]
        node_863["test_adaptation_manager.py"]
        node_901["test_agent_definitions.py"]
        node_822["test_ansible_tool.py"]
        node_935["test_app_hybrid.py"]
        node_875["test_archivist_tool.py"]
        node_818["test_ast_editor_tool.py"]
        node_836["test_atproto_tool.py"]
        node_848["test_audio_download_limit.py"]
        node_936["test_autoloop_tool.py"]
        node_865["test_autoresearch_tool.py"]
        node_838["test_autoresearch_tool_pathing.py"]
        node_925["test_backon_integration.py"]
        node_830["test_batch_ast_editor.py"]
        node_881["test_batch_file_editor.py"]
        node_906["test_claude_clone_tool.py"]
        node_898["test_code_runner_security.py"]
        node_879["test_code_runner_timeout.py"]
        node_820["test_code_runner_tool.py"]
        node_885["test_command_deck.py"]
        node_928["test_container_registry_security.py"]
        node_927["test_container_registry_tool.py"]
        node_916["test_context_upload_tool.py"]
        node_938["test_council_tool.py"]
        node_921["test_cq_tool.py"]
        node_813["test_crdt_memory.py"]
        node_837["test_crypto_receipts.py"]
        node_816["test_dependency_scanner.py"]
        node_897["test_dependency_scanner_tool.py"]
        node_853["test_desktop_control_tool.py"]
        node_887["test_document_tool.py"]
        node_833["test_dynamic_skill_tool.py"]
        node_829["test_emperor_node.py"]
        node_884["test_experiment_tool_security.py"]
        node_867["test_expert_tracker.py"]
        node_931["test_external_app_manager.py"]
        node_819["test_file_editor_security.py"]
        node_904["test_file_editor_tool.py"]
        node_913["test_file_ingestion.py"]
        node_886["test_final_answer_tool.py"]
        node_932["test_gemini_cli.py"]
        node_839["test_get_nomad_job.py"]
        node_844["test_git_tool.py"]
        node_941["test_git_tool_security.py"]
        node_815["test_gossip_discovery.py"]
        node_862["test_ha_tool.py"]
        node_895["test_hashline_editor.py"]
        node_924["test_haystack_workflows.py"]
        node_852["test_heretic_tool.py"]
        node_930["test_infrastructure.py"]
        node_878["test_janitor.py"]
        node_900["test_jules_tool.py"]
        node_892["test_langchain_adapter_tool.py"]
        node_851["test_langchain_nodes.py"]
        node_899["test_langchain_wrappers.py"]
        node_868["test_lint_script.py"]
        node_827["test_llxprt_code_tool.py"]
        node_814["test_looped_reasoning_node.py"]
        node_861["test_mcp_tool.py"]
        node_849["test_memory.py"]
        node_855["test_memory_advanced.py"]
        node_920["test_mesh_llm_manifest.py"]
        node_876["test_mqtt_template.py"]
        node_823["test_nodered_converter.py"]
        node_831["test_nomad_sandbox.py"]
        node_841["test_obsidian_gardener.py"]
        node_894["test_open_workers_tool.py"]
        node_902["test_openclaw_tool.py"]
        node_842["test_opencode_provider_tool.py"]
        node_825["test_opencode_tool.py"]
        node_846["test_orchestrator_tool.py"]
        node_821["test_p2p_sync_tool.py"]
        node_919["test_personality_tool.py"]
        node_911["test_pipecat_app_unit.py"]
        node_874["test_planner_tool.py"]
        node_890["test_playbook_integration.py"]
        node_872["test_poc_ensemble.py"]
        node_824["test_polyphony_tool.py"]
        node_843["test_post_processor_node.py"]
        node_817["test_power_tool.py"]
        node_880["test_project_mapper_tool.py"]
        node_873["test_prompt_engineering.py"]
        node_914["test_prompt_improver_tool.py"]
        node_942["test_provisioning.py"]
        node_934["test_rag_caching.py"]
        node_826["test_rag_tool.py"]
        node_883["test_ralph_nodes.py"]
        node_922["test_recover_os.py"]
        node_918["test_reflection.py"]
        node_864["test_remote_ledgers.py"]
        node_857["test_safe_flatten.py"]
        node_877["test_save_skill_tool.py"]
        node_915["test_scale_compute_tool.py"]
        node_835["test_scheduler_tool.py"]
        node_940["test_search_skills_tool.py"]
        node_860["test_search_tool_security.py"]
        node_905["test_security.py"]
        node_847["test_shell_tool.py"]
        node_828["test_shell_tool_security.py"]
        node_845["test_simple_llm_node.py"]
        node_909["test_skill_builder_tool.py"]
        node_858["test_skill_library.py"]
        node_896["test_smol_agent_tool.py"]
        node_850["test_spec_loader_tool.py"]
        node_893["test_ssh_tool.py"]
        node_870["test_submit_solution_tool.py"]
        node_888["test_summarizer_tool.py"]
        node_859["test_supervisor.py"]
        node_939["test_supervisor_retries.py"]
        node_929["test_swarm_tool.py"]
        node_923["test_tap_service.py"]
        node_840["test_tasky_nodes.py"]
        node_908["test_tasky_poc.py"]
        node_926["test_term_everything_tool.py"]
        node_910["test_terminal_cleanup.py"]
        node_856["test_ternlight_tool.py"]
        node_834["test_troubleshoot.py"]
        node_871["test_ui_accessibility.py"]
        node_907["test_update_litellm_tool.py"]
        node_869["test_vision_failover.py"]
        node_937["test_vr_tool.py"]
        node_882["test_wasm_tool.py"]
        node_891["test_web_browser_tool.py"]
        node_832["test_web_server_personality.py"]
        node_912["test_web_server_sync.py"]
        node_889["test_wol_tool.py"]
        node_917["test_workflow.py"]
        node_903["test_world_model_service.py"]
    end
    subgraph dir_tests_unit_cluster_cache [tests/unit/cluster_cache]
        direction TB
        node_943["test_cluster_cache.py"]
    end
    subgraph dir_tools_log_vectorizer_mcp [tools/log-vectorizer-mcp]
        direction TB
        node_759["README.md"]
        node_757["generate_db.py"]
        node_758["requirements.txt"]
        node_756["server.py"]
        node_755["test_server.py"]
    end
    subgraph dir_tools_log_vectorizer_mcp_tests [tools/log-vectorizer-mcp/tests]
        direction TB
        node_760["test_server.py"]
    end
    subgraph dir_workflows [workflows]
        direction TB
        node_623["chaining_pattern.yaml"]
        node_625["continuous_consolidation.yaml"]
        node_621["default_agent_loop.yaml"]
        node_622["dream_workflow.yaml"]
        node_626["routing_pattern.yaml"]
        node_624["tasky_checklist_poc.yaml"]
    end

    node_576 --> node_1283
    node_499 --> node_515
    node_536 --> node_350
    node_138 --> node_146
    node_6 --> node_832
    node_506 --> node_1028
    node_613 --> node_137
    node_253 --> node_37
    node_456 --> node_205
    node_4 --> node_275
    node_66 --> node_754
    node_6 --> node_722
    node_552 --> node_1057
    node_422 --> node_985
    node_255 --> node_1108
    node_646 --> node_1352
    node_1185 --> node_249
    node_65 --> node_338
    node_800 --> node_1171
    node_356 --> node_436
    node_1140 --> node_198
    node_1253 --> node_1043
    node_498 --> node_602
    node_147 --> node_754
    node_231 --> node_758
    node_552 --> node_1179
    node_571 --> node_1171
    node_588 --> node_1236
    node_880 --> node_499
    node_102 --> node_664
    node_484 --> node_1105
    node_987 --> node_1037
    node_207 --> node_426
    node_1068 --> node_1071
    node_643 --> node_1125
    node_669 --> node_1191
    node_914 --> node_1318
    node_516 --> node_52
    node_0 --> node_1342
    node_506 --> node_1323
    node_6 --> node_1089
    node_1335 --> node_234
    node_520 --> node_555
    node_1125 --> node_1108
    node_657 --> node_1089
    node_646 --> node_1209
    node_999 --> node_756
    node_552 --> node_1047
    node_1254 --> node_1089
    node_568 --> node_30
    node_544 --> node_758
    node_1290 --> node_1105
    node_544 --> node_324
    node_1337 --> node_1121
    node_1253 --> node_1223
    node_542 --> node_223
    node_32 --> node_728
    node_52 --> node_172
    node_864 --> node_1285
    node_530 --> node_1178
    node_1337 --> node_1059
    node_712 --> node_332
    node_880 --> node_247
    node_1099 --> node_1381
    node_189 --> node_1313
    node_729 --> node_189
    node_613 --> node_84
    node_267 --> node_457
    node_680 --> node_1151
    node_526 --> node_235
    node_646 --> node_1348
    node_498 --> node_211
    node_789 --> node_1193
    node_189 --> node_271
    node_683 --> node_1096
    node_1179 --> node_584
    node_65 --> node_933
    node_958 --> node_1032
    node_552 --> node_1211
    node_679 --> node_1326
    node_768 --> node_977
    node_1337 --> node_1164
    node_67 --> node_332
    node_27 --> node_34
    node_104 --> node_148
    node_514 --> node_234
    node_530 --> node_1348
    node_1253 --> node_1248
    node_819 --> node_404
    node_516 --> node_317
    node_672 --> node_1201
    node_124 --> node_59
    node_788 --> node_272
    node_1253 --> node_1341
    node_670 --> node_1257
    node_588 --> node_1066
    node_701 --> node_255
    node_182 --> node_207
    node_680 --> node_1044
    node_1337 --> node_1331
    node_32 --> node_989
    node_985 --> node_984
    node_872 --> node_276
    node_1147 --> node_1150
    node_680 --> node_1045
    node_787 --> node_1172
    node_552 --> node_32
    node_1354 --> node_1008
    node_588 --> node_1020
    node_468 --> node_69
    node_193 --> node_205
    node_240 --> node_241
    node_506 --> node_1360
    node_1064 --> node_1325
    node_1253 --> node_1163
    node_108 --> node_107
    node_6 --> node_721
    node_646 --> node_1028
    node_506 --> node_985
    node_552 --> node_1116
    node_480 --> node_416
    node_1170 --> node_712
    node_189 --> node_1308
    node_429 --> node_432
    node_925 --> node_260
    node_1253 --> node_1192
    node_545 --> node_13
    node_456 --> node_1325
    node_542 --> node_245
    node_318 --> node_621
    node_946 --> node_48
    node_156 --> node_37
    node_536 --> node_74
    node_531 --> node_243
    node_210 --> node_332
    node_535 --> node_1322
    node_1337 --> node_1249
    node_20 --> node_1318
    node_1279 --> node_1278
    node_506 --> node_1083
    node_1120 --> node_1363
    node_529 --> node_36
    node_21 --> node_759
    node_812 --> node_1105
    node_576 --> node_712
    node_613 --> node_338
    node_680 --> node_1102
    node_116 --> node_135
    node_857 --> node_204
    node_6 --> node_189
    node_422 --> node_1026
    node_691 --> node_690
    node_456 --> node_681
    node_683 --> node_1093
    node_74 --> node_275
    node_670 --> node_1032
    node_785 --> node_195
    node_646 --> node_1189
    node_798 --> node_179
    node_20 --> node_587
    node_70 --> node_141
    node_1253 --> node_1379
    node_1254 --> node_1321
    node_88 --> node_87
    node_20 --> node_424
    node_861 --> node_350
    node_1064 --> node_252
    node_251 --> node_205
    node_571 --> node_190
    node_646 --> node_1323
    node_105 --> node_691
    node_542 --> node_215
    node_857 --> node_238
    node_945 --> node_1084
    node_509 --> node_463
    node_1383 --> node_714
    node_748 --> node_714
    node_1253 --> node_1053
    node_601 --> node_596
    node_332 --> node_748
    node_768 --> node_49
    node_1104 --> node_234
    node_1120 --> node_1235
    node_716 --> node_725
    node_1253 --> node_1280
    node_959 --> node_1105
    node_0 --> node_1347
    node_6 --> node_419
    node_1362 --> node_1242
    node_506 --> node_555
    node_105 --> node_628
    node_712 --> node_714
    node_6 --> node_399
    node_148 --> node_60
    node_691 --> node_689
    node_1185 --> node_205
    node_535 --> node_1029
    node_857 --> node_795
    node_20 --> node_748
    node_729 --> node_1171
    node_680 --> node_1315
    node_609 --> node_574
    node_1253 --> node_1060
    node_650 --> node_1205
    node_943 --> node_712
    node_498 --> node_350
    node_1337 --> node_1082
    node_680 --> node_1238
    node_490 --> node_277
    node_663 --> node_809
    node_656 --> node_1260
    node_117 --> node_140
    node_613 --> node_933
    node_1290 --> node_1285
    node_1382 --> node_311
    node_523 --> node_1303
    node_608 --> node_4
    node_958 --> node_1158
    node_1126 --> node_1167
    node_729 --> node_1070
    node_1313 --> node_13
    node_673 --> node_1256
    node_1341 --> node_1022
    node_1140 --> node_212
    node_1253 --> node_1224
    node_162 --> node_71
    node_650 --> node_1206
    node_912 --> node_221
    node_6 --> node_1170
    node_798 --> node_499
    node_1335 --> node_1069
    node_1362 --> node_1337
    node_1038 --> node_1030
    node_971 --> node_967
    node_680 --> node_1248
    node_0 --> node_1364
    node_1229 --> node_1227
    node_68 --> node_243
    node_156 --> node_138
    node_895 --> node_404
    node_207 --> node_1291
    node_931 --> node_492
    node_798 --> node_246
    node_374 --> node_211
    node_254 --> node_416
    node_456 --> node_106
    node_1384 --> node_1326
    node_712 --> node_659
    node_646 --> node_1083
    node_660 --> node_1100
    node_506 --> node_1026
    node_558 --> node_117
    node_181 --> node_1309
    node_499 --> node_500
    node_576 --> node_180
    node_924 --> node_281
    node_680 --> node_1163
    node_544 --> node_1325
    node_20 --> node_1312
    node_506 --> node_644
    node_680 --> node_1313
    node_1120 --> node_1156
    node_530 --> node_1083
    node_994 --> node_1258
    node_682 --> node_1160
    node_435 --> node_434
    node_514 --> node_1069
    node_535 --> node_180
    node_102 --> node_1193
    node_6 --> node_344
    node_495 --> node_234
    node_390 --> node_4
    node_207 --> node_367
    node_231 --> node_252
    node_6 --> node_1171
    node_1254 --> node_1169
    node_692 --> node_332
    node_1189 --> node_1187
    node_1283 --> node_410
    node_1038 --> node_1370
    node_789 --> node_985
    node_613 --> node_9
    node_933 --> node_690
    node_253 --> node_758
    node_13 --> node_683
    node_6 --> node_1121
    node_335 --> node_329
    node_535 --> node_1385
    node_692 --> node_518
    node_511 --> node_37
    node_530 --> node_431
    node_6 --> node_1059
    node_498 --> node_712
    node_1254 --> node_1121
    node_0 --> node_1148
    node_6 --> node_1070
    node_305 --> node_621
    node_32 --> node_971
    node_98 --> node_81
    node_211 --> node_221
    node_1337 --> node_1375
    node_456 --> node_1277
    node_508 --> node_34
    node_588 --> node_681
    node_1342 --> node_1339
    node_282 --> node_288
    node_853 --> node_1308
    node_1254 --> node_1091
    node_104 --> node_154
    node_1120 --> node_1115
    node_1120 --> node_1332
    node_0 --> node_1328
    node_553 --> node_397
    node_552 --> node_83
    node_1337 --> node_1234
    node_255 --> node_249
    node_552 --> node_1362
    node_6 --> node_1164
    node_676 --> node_178
    node_384 --> node_185
    node_680 --> node_1308
    node_531 --> node_756
    node_670 --> node_1033
    node_680 --> node_1280
    node_6 --> node_519
    node_456 --> node_54
    node_1111 --> node_1109
    node_312 --> node_751
    node_108 --> node_998
    node_530 --> node_1250
    node_1099 --> node_1070
    node_666 --> node_1035
    node_506 --> node_1241
    node_335 --> node_336
    node_499 --> node_502
    node_588 --> node_696
    node_6 --> node_1331
    node_6 --> node_1303
    node_103 --> node_243
    node_945 --> node_1107
    node_680 --> node_1060
    node_456 --> node_989
    node_1259 --> node_1262
    node_498 --> node_423
    node_1337 --> node_1100
    node_1362 --> node_1196
    node_280 --> node_1303
    node_1254 --> node_1140
    node_104 --> node_1201
    node_102 --> node_132
    node_1253 --> node_1230
    node_531 --> node_177
    node_675 --> node_1035
    node_285 --> node_349
    node_98 --> node_243
    node_538 --> node_689
    node_529 --> node_1283
    node_571 --> node_1377
    node_1335 --> node_248
    node_135 --> node_559
    node_1362 --> node_1218
    node_401 --> node_1303
    node_1337 --> node_1376
    node_236 --> node_74
    node_6 --> node_1249
    node_1283 --> node_369
    node_686 --> node_1057
    node_412 --> node_263
    node_653 --> node_676
    node_108 --> node_1044
    node_1140 --> node_1127
    node_1289 --> node_1326
    node_775 --> node_774
    node_530 --> node_1065
    node_388 --> node_60
    node_1170 --> node_223
    node_994 --> node_1256
    node_21 --> node_747
    node_679 --> node_1122
    node_1362 --> node_1120
    node_901 --> node_736
    node_1362 --> node_1220
    node_552 --> node_1242
    node_366 --> node_411
    node_530 --> node_1068
    node_506 --> node_1043
    node_679 --> node_177
    node_416 --> node_1285
    node_514 --> node_248
    node_541 --> node_311
    node_21 --> node_495
    node_914 --> node_426
    node_931 --> node_274
    node_1382 --> node_714
    node_101 --> node_1236
    node_156 --> node_758
    node_1046 --> node_1045
    node_1038 --> node_1032
    node_1283 --> node_412
    node_1337 --> node_1372
    node_1290 --> node_185
    node_789 --> node_1026
    node_768 --> node_32
    node_646 --> node_1346
    node_1120 --> node_1221
    node_68 --> node_756
    node_508 --> node_181
    node_506 --> node_1214
    node_535 --> node_1380
    node_32 --> node_737
    node_1253 --> node_1042
    node_1375 --> node_234
    node_6 --> node_1082
    node_526 --> node_74
    node_995 --> node_1106
    node_646 --> node_1241
    node_552 --> node_1337
    node_759 --> node_37
    node_60 --> node_243
    node_953 --> node_1030
    node_613 --> node_750
    node_1140 --> node_621
    node_977 --> node_982
    node_536 --> node_385
    node_588 --> node_728
    node_643 --> node_1122
    node_1216 --> node_1070
    node_689 --> node_690
    node_495 --> node_1069
    node_530 --> node_1241
    node_1120 --> node_1350
    node_499 --> node_520
    node_1104 --> node_1284
    node_643 --> node_177
    node_530 --> node_1166
    node_613 --> node_6
    node_1120 --> node_1335
    node_679 --> node_1080
    node_317 --> node_621
    node_506 --> node_1341
    node_6 --> node_365
    node_65 --> node_966
    node_523 --> node_192
    node_1362 --> node_1258
    node_552 --> node_890
    node_933 --> node_863
    node_533 --> node_100
    node_506 --> node_1217
    node_1020 --> node_1021
    node_102 --> node_1360
    node_81 --> node_83
    node_798 --> node_763
    node_615 --> node_643
    node_66 --> node_499
    node_102 --> node_985
    node_1120 --> node_1145
    node_1382 --> node_339
    node_498 --> node_386
    node_506 --> node_1040
    node_211 --> node_308
    node_101 --> node_1020
    node_253 --> node_1325
    node_13 --> node_686
    node_588 --> node_989
    node_156 --> node_205
    node_20 --> node_426
    node_207 --> node_1297
    node_182 --> node_396
    node_1084 --> node_34
    node_6 --> node_1296
    node_207 --> node_414
    node_101 --> node_609
    node_535 --> node_1180
    node_1150 --> node_714
    node_108 --> node_1161
    node_1337 --> node_1254
    node_529 --> node_712
    node_933 --> node_598
    node_535 --> node_640
    node_1337 --> node_1176
    node_646 --> node_1043
    node_1254 --> node_1358
    node_1253 --> node_1139
    node_102 --> node_332
    node_147 --> node_977
    node_1120 --> node_1080
    node_552 --> node_4
    node_1362 --> node_1169
    node_32 --> node_189
    node_60 --> node_124
    node_6 --> node_785
    node_498 --> node_567
    node_617 --> node_242
    node_1065 --> node_1365
    node_6 --> node_1375
    node_1362 --> node_1036
    node_1120 --> node_1215
    node_538 --> node_598
    node_646 --> node_1214
    node_6 --> node_417
    node_995 --> node_251
    node_523 --> node_425
    node_680 --> node_1046
    node_32 --> node_655
    node_105 --> node_998
    node_1120 --> node_1349
    node_7 --> node_1070
    node_508 --> node_332
    node_868 --> node_33
    node_6 --> node_883
    node_1384 --> node_1122
    node_552 --> node_495
    node_552 --> node_1196
    node_530 --> node_1214
    node_101 --> node_631
    node_495 --> node_1284
    node_1120 --> node_1179
    node_1253 --> node_1365
    node_942 --> node_576
    node_571 --> node_756
    node_1254 --> node_1279
    node_712 --> node_243
    node_933 --> node_809
    node_898 --> node_425
    node_506 --> node_656
    node_6 --> node_279
    node_227 --> node_218
    node_20 --> node_589
    node_552 --> node_1218
    node_422 --> node_1236
    node_189 --> node_1318
    node_680 --> node_1042
    node_511 --> node_758
    node_32 --> node_754
    node_537 --> node_748
    node_207 --> node_363
    node_337 --> node_339
    node_6 --> node_1100
    node_1120 --> node_1047
    node_646 --> node_1341
    node_918 --> node_689
    node_552 --> node_657
    node_530 --> node_38
    node_675 --> node_1039
    node_108 --> node_138
    node_1164 --> node_1142
    node_224 --> node_201
    node_594 --> node_857
    node_495 --> node_248
    node_1140 --> node_195
    node_816 --> node_425
    node_646 --> node_1217
    node_1092 --> node_1097
    node_1383 --> node_335
    node_613 --> node_30
    node_1362 --> node_1140
    node_1337 --> node_1342
    node_1164 --> node_1143
    node_1337 --> node_1104
    node_6 --> node_1376
    node_105 --> node_1044
    node_498 --> node_275
    node_646 --> node_1040
    node_571 --> node_177
    node_613 --> node_966
    node_653 --> node_675
    node_1362 --> node_1208
    node_1038 --> node_1041
    node_552 --> node_1120
    node_552 --> node_340
    node_506 --> node_1092
    node_207 --> node_413
    node_865 --> node_372
    node_552 --> node_1220
    node_530 --> node_1217
    node_147 --> node_49
    node_712 --> node_335
    node_552 --> node_1321
    node_199 --> node_419
    node_1385 --> node_1106
    node_552 --> node_983
    node_32 --> node_7
    node_416 --> node_185
    node_1038 --> node_1188
    node_1140 --> node_214
    node_530 --> node_1040
    node_1375 --> node_1069
    node_156 --> node_1325
    node_310 --> node_4
    node_102 --> node_1026
    node_677 --> node_1347
    node_154 --> node_970
    node_65 --> node_664
    node_498 --> node_245
    node_535 --> node_1063
    node_1114 --> node_1070
    node_60 --> node_756
    node_21 --> node_783
    node_260 --> node_381
    node_422 --> node_1066
    node_189 --> node_748
    node_552 --> node_719
    node_750 --> node_715
    node_953 --> node_1032
    node_1362 --> node_1229
    node_971 --> node_242
    node_390 --> node_263
    node_1065 --> node_1061
    node_680 --> node_1278
    node_181 --> node_1306
    node_108 --> node_127
    node_933 --> node_1314
    node_1120 --> node_1116
    node_757 --> node_243
    node_607 --> node_311
    node_422 --> node_1020
    node_609 --> node_595
    node_32 --> node_1171
    node_6 --> node_1372
    node_1239 --> node_1244
    node_429 --> node_436
    node_1205 --> node_1203
    node_511 --> node_205
    node_320 --> node_243
    node_498 --> node_385
    node_101 --> node_70
    node_1362 --> node_1038
    node_498 --> node_215
    node_231 --> node_255
    node_686 --> node_1056
    node_101 --> node_231
    node_613 --> node_252
    node_166 --> node_134
    node_1283 --> node_367
    node_705 --> node_1070
    node_1359 --> node_1357
    node_506 --> node_1236
    node_306 --> node_317
    node_1073 --> node_1070
    node_1253 --> node_253
    node_58 --> node_100
    node_907 --> node_368
    node_574 --> node_645
    node_535 --> node_1050
    node_800 --> node_36
    node_207 --> node_1292
    node_211 --> node_358
    node_615 --> node_28
    node_680 --> node_1325
    node_716 --> node_721
    node_813 --> node_275
    node_911 --> node_189
    node_1337 --> node_1057
    node_506 --> node_1243
    node_530 --> node_1363
    node_588 --> node_971
    node_535 --> node_1149
    node_20 --> node_1291
    node_790 --> node_332
    node_931 --> node_265
    node_144 --> node_253
    node_189 --> node_1312
    node_207 --> node_411
    node_0 --> node_1359
    node_847 --> node_392
    node_1374 --> node_1070
    node_8 --> node_750
    node_1020 --> node_1006
    node_670 --> node_1259
    node_542 --> node_1105
    node_506 --> node_552
    node_915 --> node_390
    node_646 --> node_1224
    node_552 --> node_234
    node_645 --> node_657
    node_646 --> node_1092
    node_1375 --> node_1284
    node_422 --> node_631
    node_553 --> node_544
    node_1170 --> node_1336
    node_211 --> node_306
    node_680 --> node_1146
    node_759 --> node_758
    node_787 --> node_223
    node_1337 --> node_1347
    node_1099 --> node_1167
    node_105 --> node_1161
    node_530 --> node_812
    node_760 --> node_332
    node_552 --> node_1169
    node_551 --> node_4
    node_976 --> node_984
    node_172 --> node_71
    node_499 --> node_533
    node_282 --> node_279
    node_577 --> node_657
    node_64 --> node_249
    node_6 --> node_1176
    node_516 --> node_1151
    node_456 --> node_970
    node_1254 --> node_1176
    node_1375 --> node_248
    node_32 --> node_294
    node_613 --> node_664
    node_1283 --> node_1285
    node_69 --> node_614
    node_1254 --> node_1228
    node_506 --> node_1020
    node_154 --> node_148
    node_1068 --> node_496
    node_736 --> node_36
    node_74 --> node_332
    node_382 --> node_217
    node_498 --> node_418
    node_1362 --> node_1058
    node_552 --> node_1091
    node_1337 --> node_1211
    node_197 --> node_36
    node_506 --> node_609
    node_552 --> node_52
    node_81 --> node_340
    node_534 --> node_999
    node_511 --> node_1325
    node_8 --> node_85
    node_1221 --> node_1219
    node_1253 --> node_1054
    node_144 --> node_1101
    node_520 --> node_207
    node_553 --> node_21
    node_952 --> node_1257
    node_65 --> node_1336
    node_404 --> node_259
    node_499 --> node_513
    node_1335 --> node_497
    node_0 --> node_1380
    node_1338 --> node_1070
    node_552 --> node_1140
    node_456 --> node_193
    node_552 --> node_568
    node_552 --> node_551
    node_1382 --> node_496
    node_1362 --> node_1279
    node_552 --> node_317
    node_552 --> node_1208
    node_874 --> node_1319
    node_20 --> node_1171
    node_688 --> node_1348
    node_696 --> node_4
    node_552 --> node_620
    node_58 --> node_1162
    node_826 --> node_416
    node_530 --> node_1156
    node_530 --> node_1243
    node_911 --> node_1171
    node_0 --> node_1258
    node_506 --> node_631
    node_108 --> node_992
    node_509 --> node_748
    node_6 --> node_1342
    node_535 --> node_1352
    node_6 --> node_1104
    node_101 --> node_728
    node_768 --> node_4
    node_757 --> node_756
    node_231 --> node_332
    node_506 --> node_1246
    node_676 --> node_993
    node_1120 --> node_1177
    node_422 --> node_681
    node_641 --> node_1208
    node_1337 --> node_1148
    node_498 --> node_348
    node_70 --> node_333
    node_514 --> node_497
    node_1112 --> node_1070
    node_1058 --> node_1055
    node_672 --> node_1263
    node_552 --> node_1229
    node_789 --> node_1236
    node_552 --> node_634
    node_1353 --> node_1030
    node_680 --> node_1216
    node_607 --> node_714
    node_1253 --> node_1367
    node_68 --> node_60
    node_147 --> node_32
    node_1170 --> node_255
    node_530 --> node_977
    node_1337 --> node_1328
    node_65 --> node_1193
    node_705 --> node_969
    node_729 --> node_36
    node_491 --> node_493
    node_411 --> node_268
    node_680 --> node_1277
    node_530 --> node_1115
    node_1104 --> node_36
    node_542 --> node_1285
    node_535 --> node_1209
    node_42 --> node_4
    node_83 --> node_88
    node_286 --> node_214
    node_527 --> node_307
    node_552 --> node_1038
    node_0 --> node_1180
    node_1347 --> node_1344
    node_663 --> node_36
    node_552 --> node_911
    node_1180 --> node_1070
    node_69 --> node_235
    node_6 --> node_428
    node_1253 --> node_1324
    node_0 --> node_1036
    node_1064 --> node_1108
    node_535 --> node_1348
    node_994 --> node_1262
    node_1362 --> node_1353
    node_1254 --> node_1155
    node_552 --> node_1069
    node_723 --> node_721
    node_1120 --> node_1253
    node_680 --> node_1312
    node_278 --> node_185
    node_21 --> node_179
    node_1140 --> node_211
    node_1274 --> node_1266
    node_789 --> node_1066
    node_800 --> node_1283
    node_506 --> node_665
    node_1253 --> node_240
    node_6 --> node_548
    node_335 --> node_751
    node_498 --> node_352
    node_863 --> node_721
    node_1254 --> node_1207
    node_197 --> node_211
    node_64 --> node_205
    node_182 --> node_1303
    node_483 --> node_36
    node_613 --> node_1336
    node_520 --> node_253
    node_1380 --> node_1070
    node_516 --> node_309
    node_958 --> node_1258
    node_506 --> node_70
    node_789 --> node_1020
    node_1049 --> node_1048
    node_768 --> node_983
    node_6 --> node_1057
    node_65 --> node_255
    node_1150 --> node_335
    node_653 --> node_683
    node_506 --> node_231
    node_1244 --> node_332
    node_759 --> node_1325
    node_1253 --> node_1178
    node_535 --> node_1028
    node_70 --> node_107
    node_613 --> node_330
    node_680 --> node_1305
    node_144 --> node_240
    node_1374 --> node_1326
    node_0 --> node_1111
    node_189 --> node_426
    node_1100 --> node_234
    node_1120 --> node_1259
    node_590 --> node_13
    node_1124 --> node_1070
    node_523 --> node_229
    node_6 --> node_36
    node_548 --> node_1232
    node_530 --> node_49
    node_670 --> node_1039
    node_1254 --> node_1237
    node_1140 --> node_37
    node_126 --> node_235
    node_516 --> node_502
    node_646 --> node_1246
    node_121 --> node_71
    node_20 --> node_364
    node_680 --> node_1099
    node_1362 --> node_1190
    node_613 --> node_53
    node_536 --> node_416
    node_20 --> node_414
    node_1077 --> node_1070
    node_1290 --> node_253
    node_6 --> node_1347
    node_506 --> node_1052
    node_657 --> node_1347
    node_1254 --> node_1347
    node_523 --> node_594
    node_1120 --> node_1337
    node_759 --> node_252
    node_552 --> node_1058
    node_535 --> node_1323
    node_107 --> node_76
    node_291 --> node_1070
    node_401 --> node_36
    node_211 --> node_277
    node_667 --> node_1052
    node_958 --> node_1036
    node_21 --> node_499
    node_530 --> node_1221
    node_101 --> node_759
    node_645 --> node_673
    node_613 --> node_1193
    node_545 --> node_640
    node_571 --> node_1106
    node_1069 --> node_1070
    node_422 --> node_728
    node_6 --> node_235
    node_499 --> node_546
    node_789 --> node_631
    node_0 --> node_1063
    node_21 --> node_246
    node_21 --> node_544
    node_880 --> node_749
    node_1254 --> node_1197
    node_1337 --> node_1362
    node_646 --> node_1139
    node_520 --> node_1101
    node_231 --> node_1108
    node_548 --> node_1184
    node_0 --> node_1038
    node_1208 --> node_1323
    node_577 --> node_673
    node_207 --> node_1309
    node_1385 --> node_234
    node_6 --> node_1364
    node_1254 --> node_1364
    node_506 --> node_1255
    node_148 --> node_544
    node_530 --> node_1335
    node_533 --> node_970
    node_1254 --> node_1141
    node_552 --> node_1279
    node_505 --> node_34
    node_680 --> node_1324
    node_553 --> node_235
    node_552 --> node_1127
    node_552 --> node_248
    node_807 --> node_271
    node_926 --> node_1306
    node_456 --> node_38
    node_422 --> node_989
    node_853 --> node_854
    node_958 --> node_1256
    node_70 --> node_102
    node_506 --> node_1110
    node_530 --> node_1145
    node_1353 --> node_1032
    node_667 --> node_1114
    node_58 --> node_1199
    node_339 --> node_69
    node_211 --> node_212
    node_234 --> node_235
    node_1225 --> node_776
    node_278 --> node_283
    node_102 --> node_1236
    node_981 --> node_975
    node_282 --> node_280
    node_555 --> node_721
    node_32 --> node_11
    node_181 --> node_1314
    node_548 --> node_1113
    node_60 --> node_69
    node_105 --> node_992
    node_70 --> node_143
    node_613 --> node_255
    node_800 --> node_712
    node_1283 --> node_406
    node_233 --> node_218
    node_21 --> node_1118
    node_530 --> node_231
    node_1356 --> node_69
    node_552 --> node_691
    node_1359 --> node_1356
    node_576 --> node_1105
    node_508 --> node_243
    node_280 --> node_349
    node_609 --> node_64
    node_65 --> node_1360
    node_32 --> node_977
    node_535 --> node_1083
    node_1362 --> node_1290
    node_65 --> node_985
    node_0 --> node_1149
    node_872 --> node_281
    node_6 --> node_1148
    node_176 --> node_71
    node_680 --> node_1247
    node_542 --> node_185
    node_555 --> node_189
    node_646 --> node_1052
    node_1337 --> node_1242
    node_677 --> node_1344
    node_108 --> node_106
    node_264 --> node_200
    node_552 --> node_628
    node_1140 --> node_244
    node_148 --> node_21
    node_729 --> node_1283
    node_8 --> node_336
    node_530 --> node_108
    node_6 --> node_1328
    node_645 --> node_650
    node_1254 --> node_1328
    node_30 --> node_614
    node_530 --> node_1052
    node_571 --> node_251
    node_530 --> node_1215
    node_663 --> node_1283
    node_792 --> node_223
    node_524 --> node_621
    node_207 --> node_391
    node_1274 --> node_1265
    node_684 --> node_1330
    node_1120 --> node_1218
    node_32 --> node_984
    node_531 --> node_598
    node_102 --> node_1066
    node_552 --> node_1353
    node_958 --> node_1038
    node_958 --> node_1085
    node_286 --> node_226
    node_530 --> node_1349
    node_1254 --> node_1333
    node_60 --> node_128
    node_789 --> node_681
    node_1100 --> node_1069
    node_530 --> node_1179
    node_552 --> node_618
    node_102 --> node_1020
    node_679 --> node_1128
    node_544 --> node_294
    node_6 --> node_203
    node_736 --> node_712
    node_781 --> node_698
    node_995 --> node_1336
    node_880 --> node_634
    node_646 --> node_1255
    node_498 --> node_213
    node_768 --> node_620
    node_102 --> node_609
    node_755 --> node_250
    node_70 --> node_125
    node_197 --> node_712
    node_189 --> node_1291
    node_1120 --> node_1321
    node_232 --> node_1285
    node_108 --> node_1277
    node_332 --> node_243
    node_483 --> node_1283
    node_40 --> node_45
    node_20 --> node_1292
    node_498 --> node_991
    node_1253 --> node_1117
    node_363 --> node_245
    node_786 --> node_189
    node_530 --> node_1255
    node_643 --> node_1129
    node_499 --> node_524
    node_520 --> node_240
    node_646 --> node_1110
    node_132 --> node_332
    node_32 --> node_49
    node_656 --> node_1034
    node_976 --> node_974
    node_680 --> node_1219
    node_20 --> node_411
    node_20 --> node_243
    node_768 --> node_634
    node_506 --> node_1386
    node_60 --> node_135
    node_709 --> node_177
    node_891 --> node_406
    node_552 --> node_1190
    node_6 --> node_1283
    node_530 --> node_1110
    node_1124 --> node_1326
    node_189 --> node_367
    node_552 --> node_652
    node_840 --> node_276
    node_1196 --> node_1070
    node_933 --> node_901
    node_667 --> node_1054
    node_817 --> node_1299
    node_69 --> node_131
    node_701 --> node_253
    node_1289 --> node_1288
    node_836 --> node_365
    node_456 --> node_812
    node_532 --> node_235
    node_500 --> node_584
    node_13 --> node_679
    node_6 --> node_505
    node_8 --> node_330
    node_1170 --> node_1285
    node_804 --> node_491
    node_1290 --> node_240
    node_1064 --> node_249
    node_102 --> node_631
    node_0 --> node_1088
    node_1385 --> node_1069
    node_613 --> node_985
    node_530 --> node_32
    node_680 --> node_1301
    node_401 --> node_1283
    node_2 --> node_762
    node_0 --> node_1352
    node_506 --> node_1330
    node_692 --> node_748
    node_1275 --> node_69
    node_181 --> node_1296
    node_65 --> node_1026
    node_829 --> node_276
    node_231 --> node_185
    node_552 --> node_1228
    node_679 --> node_1169
    node_101 --> node_737
    node_498 --> node_332
    node_920 --> node_397
    node_8 --> node_53
    node_555 --> node_1171
    node_20 --> node_425
    node_656 --> node_1031
    node_552 --> node_21
    node_592 --> node_661
    node_1038 --> node_1039
    node_6 --> node_1295
    node_32 --> node_177
    node_506 --> node_1355
    node_240 --> node_137
    node_888 --> node_1311
    node_180 --> node_1061
    node_1068 --> node_1101
    node_207 --> node_360
    node_58 --> node_970
    node_101 --> node_747
    node_1253 --> node_193
    node_107 --> node_748
    node_506 --> node_1367
    node_555 --> node_1070
    node_754 --> node_753
    node_6 --> node_1106
    node_1140 --> node_758
    node_729 --> node_712
    node_21 --> node_763
    node_6 --> node_1362
    node_422 --> node_971
    node_1104 --> node_712
    node_189 --> node_206
    node_0 --> node_1209
    node_551 --> node_564
    node_818 --> node_414
    node_1020 --> node_1004
    node_1374 --> node_1122
    node_1337 --> node_1196
    node_663 --> node_712
    node_506 --> node_759
    node_814 --> node_286
    node_851 --> node_276
    node_1337 --> node_1359
    node_1100 --> node_248
    node_671 --> node_1074
    node_456 --> node_496
    node_535 --> node_1241
    node_282 --> node_287
    node_736 --> node_720
    node_1362 --> node_1049
    node_552 --> node_13
    node_701 --> node_1101
    node_1120 --> node_1169
    node_995 --> node_255
    node_460 --> node_258
    node_881 --> node_259
    node_501 --> node_548
    node_1362 --> node_1141
    node_552 --> node_416
    node_789 --> node_728
    node_613 --> node_17
    node_873 --> node_724
    node_646 --> node_1054
    node_646 --> node_178
    node_646 --> node_1386
    node_1362 --> node_1144
    node_506 --> node_646
    node_552 --> node_1290
    node_786 --> node_1171
    node_1382 --> node_1101
    node_679 --> node_1140
    node_676 --> node_1257
    node_21 --> node_801
    node_240 --> node_84
    node_1337 --> node_1120
    node_292 --> node_1070
    node_1125 --> node_189
    node_483 --> node_712
    node_1254 --> node_1322
    node_102 --> node_70
    node_958 --> node_1088
    node_1337 --> node_1220
    node_1120 --> node_1091
    node_1038 --> node_1232
    node_207 --> node_1294
    node_529 --> node_642
    node_558 --> node_578
    node_20 --> node_286
    node_661 --> node_1134
    node_147 --> node_495
    node_582 --> node_612
    node_1006 --> node_1070
    node_456 --> node_977
    node_392 --> node_212
    node_791 --> node_287
    node_1126 --> node_1098
    node_789 --> node_989
    node_677 --> node_1180
    node_66 --> node_58
    node_330 --> node_53
    node_45 --> node_177
    node_6 --> node_1242
    node_231 --> node_249
    node_126 --> node_74
    node_20 --> node_394
    node_198 --> node_221
    node_646 --> node_1330
    node_1157 --> node_1070
    node_6 --> node_712
    node_1038 --> node_1036
    node_207 --> node_60
    node_548 --> node_1205
    node_552 --> node_614
    node_1354 --> node_1258
    node_193 --> node_59
    node_332 --> node_756
    node_1385 --> node_248
    node_535 --> node_1043
    node_613 --> node_1026
    node_530 --> node_1330
    node_926 --> node_403
    node_646 --> node_1355
    node_1253 --> node_1166
    node_1120 --> node_1140
    node_686 --> node_1058
    node_680 --> node_1291
    node_680 --> node_1250
    node_0 --> node_1189
    node_6 --> node_251
    node_643 --> node_1140
    node_486 --> node_1171
    node_880 --> node_691
    node_646 --> node_1367
    node_645 --> node_684
    node_401 --> node_712
    node_548 --> node_1206
    node_20 --> node_756
    node_530 --> node_1355
    node_1254 --> node_1029
    node_552 --> node_1155
    node_101 --> node_754
    node_428 --> node_202
    node_189 --> node_294
    node_604 --> node_28
    node_6 --> node_74
    node_535 --> node_1214
    node_147 --> node_983
    node_680 --> node_1302
    node_729 --> node_720
    node_105 --> node_1277
    node_880 --> node_628
    node_422 --> node_737
    node_527 --> node_275
    node_1337 --> node_1258
    node_552 --> node_1207
    node_768 --> node_691
    node_791 --> node_276
    node_1120 --> node_1229
    node_530 --> node_759
    node_69 --> node_120
    node_248 --> node_250
    node_499 --> node_555
    node_1140 --> node_223
    node_6 --> node_541
    node_662 --> node_180
    node_105 --> node_117
    node_571 --> node_234
    node_1227 --> node_984
    node_917 --> node_285
    node_189 --> node_1297
    node_917 --> node_276
    node_1313 --> node_34
    node_530 --> node_1177
    node_456 --> node_49
    node_768 --> node_628
    node_465 --> node_189
    node_641 --> node_1207
    node_535 --> node_1341
    node_705 --> node_389
    node_613 --> node_1108
    node_498 --> node_272
    node_1170 --> node_185
    node_6 --> node_401
    node_552 --> node_1237
    node_227 --> node_228
    node_952 --> node_1259
    node_1185 --> node_59
    node_535 --> node_1217
    node_958 --> node_1160
    node_576 --> node_676
    node_701 --> node_240
    node_945 --> node_242
    node_682 --> node_1154
    node_1283 --> node_1309
    node_468 --> node_356
    node_21 --> node_857
    node_371 --> node_1316
    node_535 --> node_1040
    node_231 --> node_210
    node_1106 --> node_36
    node_676 --> node_177
    node_577 --> node_13
    node_520 --> node_189
    node_529 --> node_1105
    node_588 --> node_51
    node_1347 --> node_1345
    node_1274 --> node_1270
    node_1337 --> node_1036
    node_953 --> node_1039
    node_1140 --> node_1325
    node_673 --> node_1261
    node_992 --> node_991
    node_207 --> node_398
    node_1354 --> node_1256
    node_571 --> node_52
    node_1254 --> node_1385
    node_0 --> node_1262
    node_452 --> node_431
    node_1156 --> node_1158
    node_552 --> node_998
    node_594 --> node_140
    node_1362 --> node_1192
    node_887 --> node_385
    node_21 --> node_338
    node_1031 --> node_1070
    node_129 --> node_756
    node_530 --> node_1253
    node_552 --> node_1197
    node_553 --> node_180
    node_932 --> node_435
    node_1140 --> node_1011
    node_506 --> node_301
    node_588 --> node_977
    node_710 --> node_455
    node_102 --> node_728
    node_506 --> node_1089
    node_1290 --> node_189
    node_104 --> node_1232
    node_181 --> node_405
    node_820 --> node_1317
    node_552 --> node_497
    node_1327 --> node_990
    node_552 --> node_1049
    node_506 --> node_737
    node_666 --> node_1034
    node_498 --> node_220
    node_430 --> node_431
    node_552 --> node_1141
    node_1124 --> node_1122
    node_609 --> node_600
    node_1140 --> node_252
    node_20 --> node_199
    node_1237 --> node_1010
    node_880 --> node_242
    node_1337 --> node_1111
    node_671 --> node_1072
    node_6 --> node_1359
    node_880 --> node_250
    node_552 --> node_1144
    node_859 --> node_642
    node_306 --> node_313
    node_54 --> node_235
    node_506 --> node_747
    node_1140 --> node_1025
    node_911 --> node_36
    node_530 --> node_1259
    node_661 --> node_1123
    node_863 --> node_247
    node_552 --> node_1044
    node_1224 --> node_1222
    node_1120 --> node_1358
    node_679 --> node_1127
    node_1337 --> node_1208
    node_337 --> node_69
    node_912 --> node_36
    node_54 --> node_137
    node_6 --> node_873
    node_932 --> node_395
    node_1190 --> node_1034
    node_552 --> node_695
    node_971 --> node_968
    node_1362 --> node_1280
    node_456 --> node_231
    node_1290 --> node_193
    node_789 --> node_971
    node_1113 --> node_1112
    node_422 --> node_754
    node_308 --> node_314
    node_392 --> node_269
    node_885 --> node_235
    node_21 --> node_933
    node_716 --> node_36
    node_891 --> node_1309
    node_207 --> node_358
    node_506 --> node_1117
    node_1283 --> node_361
    node_104 --> node_1184
    node_465 --> node_1171
    node_535 --> node_1224
    node_147 --> node_783
    node_666 --> node_1031
    node_1362 --> node_1322
    node_759 --> node_332
    node_531 --> node_621
    node_953 --> node_1036
    node_535 --> node_1092
    node_1211 --> node_177
    node_667 --> node_1117
    node_787 --> node_1285
    node_568 --> node_100
    node_798 --> node_1193
    node_1156 --> node_1157
    node_609 --> node_578
    node_576 --> node_667
    node_598 --> node_652
    node_509 --> node_294
    node_6 --> node_719
    node_588 --> node_49
    node_812 --> node_189
    node_985 --> node_13
    node_1120 --> node_1279
    node_1337 --> node_1038
    node_520 --> node_1171
    node_1342 --> node_1022
    node_552 --> node_211
    node_643 --> node_1127
    node_54 --> node_84
    node_1253 --> node_1363
    node_136 --> node_124
    node_147 --> node_620
    node_498 --> node_184
    node_104 --> node_1113
    node_571 --> node_1069
    node_66 --> node_634
    node_498 --> node_271
    node_189 --> node_192
    node_646 --> node_1089
    node_509 --> node_190
    node_498 --> node_185
    node_679 --> node_1353
    node_189 --> node_1292
    node_690 --> node_721
    node_676 --> node_995
    node_837 --> node_273
    node_1253 --> node_1234
    node_957 --> node_1203
    node_32 --> node_1018
    node_1254 --> node_1380
    node_20 --> node_221
    node_1104 --> node_252
    node_530 --> node_1089
    node_680 --> node_1297
    node_995 --> node_497
    node_1290 --> node_1171
    node_147 --> node_634
    node_189 --> node_411
    node_858 --> node_398
    node_191 --> node_192
    node_6 --> node_849
    node_987 --> node_1030
    node_189 --> node_243
    node_552 --> node_37
    node_253 --> node_243
    node_1253 --> node_1235
    node_181 --> node_1317
    node_6 --> node_1258
    node_862 --> node_367
    node_0 --> node_1346
    node_1164 --> node_1063
    node_552 --> node_615
    node_933 --> node_712
    node_952 --> node_1260
    node_498 --> node_1308
    node_506 --> node_754
    node_1335 --> node_54
    node_946 --> node_205
    node_466 --> node_36
    node_1253 --> node_1100
    node_548 --> node_1185
    node_279 --> node_1317
    node_530 --> node_747
    node_535 --> node_1243
    node_552 --> node_726
    node_855 --> node_185
    node_1347 --> node_1343
    node_977 --> node_981
    node_671 --> node_1336
    node_462 --> node_712
    node_65 --> node_1236
    node_552 --> node_1161
    node_677 --> node_1088
    node_1020 --> node_1019
    node_646 --> node_1117
    node_1253 --> node_1376
    node_1170 --> node_1168
    node_506 --> node_1170
    node_530 --> node_495
    node_1253 --> node_1377
    node_552 --> node_309
    node_456 --> node_32
    node_575 --> node_602
    node_684 --> node_1331
    node_207 --> node_380
    node_498 --> node_183
    node_67 --> node_1070
    node_189 --> node_425
    node_794 --> node_1172
    node_957 --> node_1040
    node_594 --> node_991
    node_912 --> node_211
    node_498 --> node_208
    node_6 --> node_1180
    node_672 --> node_1273
    node_656 --> node_1258
    node_514 --> node_54
    node_1337 --> node_1058
    node_181 --> node_1172
    node_953 --> node_1038
    node_1254 --> node_1180
    node_6 --> node_1036
    node_20 --> node_209
    node_813 --> node_185
    node_1020 --> node_1018
    node_42 --> node_614
    node_679 --> node_1135
    node_919 --> node_358
    node_1298 --> node_1316
    node_842 --> node_347
    node_106 --> node_243
    node_1168 --> node_1381
    node_207 --> node_427
    node_801 --> node_578
    node_499 --> node_526
    node_6 --> node_385
    node_1362 --> node_1230
    node_812 --> node_1171
    node_883 --> node_279
    node_21 --> node_558
    node_796 --> node_182
    node_408 --> node_180
    node_65 --> node_1066
    node_1362 --> node_1385
    node_20 --> node_285
    node_1100 --> node_497
    node_1253 --> node_1156
    node_108 --> node_7
    node_530 --> node_1321
    node_337 --> node_10
    node_672 --> node_1276
    node_530 --> node_983
    node_280 --> node_215
    node_0 --> node_1043
    node_1242 --> node_1239
    node_571 --> node_248
    node_759 --> node_1108
    node_65 --> node_1020
    node_506 --> node_1121
    node_613 --> node_249
    node_6 --> node_536
    node_102 --> node_971
    node_506 --> node_645
    node_255 --> node_59
    node_506 --> node_1059
    node_143 --> node_124
    node_499 --> node_545
    node_288 --> node_214
    node_911 --> node_1283
    node_656 --> node_1036
    node_6 --> node_1111
    node_20 --> node_368
    node_65 --> node_609
    node_498 --> node_283
    node_498 --> node_353
    node_207 --> node_382
    node_66 --> node_145
    node_154 --> node_60
    node_880 --> node_998
    node_537 --> node_756
    node_0 --> node_1223
    node_643 --> node_1135
    node_506 --> node_1164
    node_977 --> node_980
    node_631 --> node_627
    node_1120 --> node_1228
    node_87 --> node_85
    node_1253 --> node_1332
    node_1253 --> node_1115
    node_645 --> node_680
    node_1362 --> node_1046
    node_946 --> node_1325
    node_207 --> node_397
    node_1038 --> node_1190
    node_555 --> node_756
    node_615 --> node_656
    node_1337 --> node_1088
    node_886 --> node_348
    node_716 --> node_1283
    node_1290 --> node_1125
    node_189 --> node_286
    node_231 --> node_253
    node_1140 --> node_230
    node_1125 --> node_59
    node_552 --> node_1322
    node_680 --> node_1235
    node_506 --> node_1331
    node_679 --> node_1137
    node_101 --> node_179
    node_211 --> node_307
    node_20 --> node_1294
    node_12 --> node_180
    node_646 --> node_1170
    node_613 --> node_1236
    node_185 --> node_491
    node_686 --> node_1055
    node_768 --> node_998
    node_577 --> node_680
    node_857 --> node_282
    node_1100 --> node_1102
    node_0 --> node_1248
    node_535 --> node_1246
    node_1385 --> node_497
    node_656 --> node_1256
    node_498 --> node_224
    node_530 --> node_1170
    node_65 --> node_631
    node_6 --> node_1063
    node_248 --> node_37
    node_957 --> node_1030
    node_1253 --> node_1254
    node_880 --> node_1044
    node_613 --> node_335
    node_1254 --> node_1063
    node_988 --> node_178
    node_506 --> node_1249
    node_680 --> node_1292
    node_66 --> node_691
    node_1106 --> node_712
    node_789 --> node_754
    node_857 --> node_961
    node_683 --> node_1373
    node_189 --> node_756
    node_868 --> node_140
    node_1337 --> node_1353
    node_0 --> node_1163
    node_6 --> node_1038
    node_987 --> node_1032
    node_153 --> node_332
    node_657 --> node_1085
    node_6 --> node_911
    node_588 --> node_32
    node_477 --> node_406
    node_1283 --> node_1306
    node_0 --> node_1192
    node_147 --> node_691
    node_1227 --> node_974
    node_66 --> node_628
    node_207 --> node_1314
    node_448 --> node_437
    node_643 --> node_1137
    node_768 --> node_1044
    node_211 --> node_309
    node_32 --> node_4
    node_240 --> node_30
    node_224 --> node_23
    node_721 --> node_729
    node_613 --> node_1066
    node_768 --> node_695
    node_535 --> node_1139
    node_646 --> node_1059
    node_456 --> node_67
    node_101 --> node_499
    node_181 --> node_203
    node_1099 --> node_1098
    node_456 --> node_759
    node_231 --> node_1101
    node_0 --> node_1379
    node_509 --> node_354
    node_147 --> node_628
    node_680 --> node_1340
    node_613 --> node_1020
    node_1369 --> node_1070
    node_530 --> node_1121
    node_933 --> node_826
    node_737 --> node_733
    node_1353 --> node_1039
    node_101 --> node_246
    node_102 --> node_737
    node_656 --> node_1038
    node_104 --> node_1205
    node_466 --> node_1283
    node_813 --> node_494
    node_1104 --> node_1336
    node_495 --> node_54
    node_1212 --> node_1210
    node_969 --> node_968
    node_613 --> node_609
    node_646 --> node_1164
    node_0 --> node_1053
    node_32 --> node_495
    node_1337 --> node_1190
    node_69 --> node_140
    node_506 --> node_1082
    node_958 --> node_1090
    node_1253 --> node_1221
    node_1254 --> node_1149
    node_0 --> node_1280
    node_1282 --> node_1070
    node_583 --> node_577
    node_102 --> node_747
    node_1176 --> node_1173
    node_646 --> node_1331
    node_911 --> node_712
    node_499 --> node_525
    node_104 --> node_1206
    node_256 --> node_1317
    node_530 --> node_783
    node_912 --> node_712
    node_1253 --> node_1104
    node_857 --> node_433
    node_108 --> node_38
    node_498 --> node_237
    node_0 --> node_1060
    node_1382 --> node_337
    node_65 --> node_70
    node_158 --> node_135
    node_679 --> node_1237
    node_1120 --> node_1155
    node_613 --> node_205
    node_639 --> node_1261
    node_552 --> node_758
    node_1337 --> node_1189
    node_1253 --> node_1350
    node_716 --> node_712
    node_680 --> node_1257
    node_689 --> node_180
    node_516 --> node_311
    node_1350 --> node_1351
    node_535 --> node_1052
    node_880 --> node_356
    node_20 --> node_398
    node_65 --> node_681
    node_147 --> node_544
    node_646 --> node_1249
    node_0 --> node_1224
    node_1120 --> node_1207
    node_552 --> node_1385
    node_142 --> node_60
    node_613 --> node_631
    node_32 --> node_983
    node_6 --> node_951
    node_792 --> node_1285
    node_21 --> node_966
    node_250 --> node_331
    node_499 --> node_552
    node_880 --> node_1161
    node_1362 --> node_1146
    node_1140 --> node_181
    node_957 --> node_1257
    node_552 --> node_750
    node_995 --> node_249
    node_32 --> node_584
    node_181 --> node_1295
    node_6 --> node_1336
    node_1290 --> node_1377
    node_536 --> node_748
    node_359 --> node_263
    node_1289 --> node_1167
    node_686 --> node_1333
    node_499 --> node_512
    node_874 --> node_428
    node_127 --> node_138
    node_1120 --> node_1237
    node_271 --> node_283
    node_708 --> node_69
    node_571 --> node_590
    node_334 --> node_137
    node_1170 --> node_253
    node_1168 --> node_1070
    node_768 --> node_1161
    node_695 --> node_324
    node_535 --> node_1255
    node_786 --> node_36
    node_1253 --> node_1080
    node_1354 --> node_1262
    node_429 --> node_448
    node_552 --> node_1046
    node_552 --> node_992
    node_506 --> node_1375
    node_679 --> node_1141
    node_207 --> node_390
    node_1244 --> node_331
    node_722 --> node_36
    node_436 --> node_437
    node_101 --> node_756
    node_1185 --> node_1183
    node_207 --> node_1296
    node_1337 --> node_1290
    node_987 --> node_1033
    node_147 --> node_21
    node_1313 --> node_27
    node_646 --> node_1082
    node_1253 --> node_1057
    node_127 --> node_146
    node_498 --> node_202
    node_535 --> node_1110
    node_798 --> node_1044
    node_475 --> node_211
    node_958 --> node_1060
    node_106 --> node_108
    node_800 --> node_1105
    node_6 --> node_1088
    node_1104 --> node_255
    node_885 --> node_750
    node_231 --> node_240
    node_657 --> node_1088
    node_617 --> node_1150
    node_107 --> node_190
    node_6 --> node_484
    node_6 --> node_1352
    node_509 --> node_756
    node_102 --> node_754
    node_1120 --> node_1197
    node_407 --> node_263
    node_1254 --> node_1352
    node_1273 --> node_1070
    node_531 --> node_211
    node_466 --> node_712
    node_661 --> node_1136
    node_1253 --> node_1179
    node_1048 --> node_584
    node_392 --> node_211
    node_1284 --> node_1287
    node_733 --> node_1070
    node_680 --> node_1221
    node_506 --> node_1100
    node_1337 --> node_1262
    node_1362 --> node_1064
    node_422 --> node_977
    node_679 --> node_1213
    node_553 --> node_291
    node_1120 --> node_1364
    node_613 --> node_70
    node_129 --> node_74
    node_1120 --> node_1141
    node_1253 --> node_1047
    node_65 --> node_253
    node_827 --> node_1305
    node_506 --> node_179
    node_643 --> node_1141
    node_506 --> node_1376
    node_1120 --> node_1144
    node_509 --> node_905
    node_108 --> node_812
    node_1254 --> node_1209
    node_613 --> node_681
    node_1170 --> node_1101
    node_616 --> node_140
    node_189 --> node_221
    node_0 --> node_1230
    node_936 --> node_407
    node_106 --> node_66
    node_6 --> node_576
    node_8 --> node_335
    node_666 --> node_1036
    node_1140 --> node_322
    node_1253 --> node_1211
    node_501 --> node_52
    node_1068 --> node_1284
    node_1140 --> node_332
    node_661 --> node_1132
    node_617 --> node_970
    node_736 --> node_1105
    node_931 --> node_204
    node_816 --> node_370
    node_677 --> node_1346
    node_189 --> node_229
    node_65 --> node_728
    node_1140 --> node_431
    node_680 --> node_1145
    node_285 --> node_283
    node_553 --> node_753
    node_1231 --> node_1070
    node_530 --> node_1358
    node_6 --> node_255
    node_215 --> node_185
    node_552 --> node_28
    node_4 --> node_597
    node_248 --> node_758
    node_6 --> node_542
    node_1190 --> node_1036
    node_60 --> node_614
    node_553 --> node_266
    node_646 --> node_1375
    node_1353 --> node_1038
    node_498 --> node_1318
    node_506 --> node_1372
    node_456 --> node_747
    node_1253 --> node_1116
    node_494 --> node_185
    node_555 --> node_429
    node_646 --> node_1234
    node_32 --> node_783
    node_807 --> node_189
    node_996 --> node_995
    node_1253 --> node_1382
    node_613 --> node_100
    node_81 --> node_750
    node_211 --> node_750
    node_683 --> node_1063
    node_103 --> node_235
    node_6 --> node_1190
    node_1362 --> node_1050
    node_1254 --> node_1028
    node_552 --> node_1325
    node_334 --> node_715
    node_34 --> node_973
    node_1125 --> node_36
    node_506 --> node_499
    node_422 --> node_49
    node_65 --> node_989
    node_498 --> node_424
    node_535 --> node_1386
    node_995 --> node_205
    node_1382 --> node_1284
    node_54 --> node_30
    node_456 --> node_495
    node_1120 --> node_1333
    node_516 --> node_714
    node_105 --> node_38
    node_529 --> node_5
    node_255 --> node_235
    node_1283 --> node_403
    node_555 --> node_1283
    node_136 --> node_60
    node_32 --> node_551
    node_207 --> node_1307
    node_506 --> node_246
    node_98 --> node_235
    node_680 --> node_1309
    node_790 --> node_189
    node_646 --> node_1100
    node_0 --> node_1042
    node_199 --> node_215
    node_32 --> node_620
    node_69 --> node_332
    node_6 --> node_1189
    node_1140 --> node_196
    node_542 --> node_189
    node_1140 --> node_77
    node_189 --> node_360
    node_189 --> node_429
    node_1254 --> node_1189
    node_552 --> node_1146
    node_524 --> node_252
    node_646 --> node_1376
    node_535 --> node_1330
    node_680 --> node_1041
    node_20 --> node_198
    node_660 --> node_1102
    node_552 --> node_252
    node_189 --> node_285
    node_661 --> node_1138
    node_1254 --> node_1323
    node_64 --> node_59
    node_726 --> node_736
    node_613 --> node_253
    node_74 --> node_75
    node_104 --> node_1185
    node_957 --> node_1033
    node_680 --> node_1188
    node_857 --> node_991
    node_1106 --> node_252
    node_32 --> node_634
    node_552 --> node_729
    node_530 --> node_179
    node_108 --> node_977
    node_571 --> node_497
    node_419 --> node_189
    node_971 --> node_970
    node_6 --> node_869
    node_535 --> node_1355
    node_456 --> node_983
    node_13 --> node_657
    node_620 --> node_1107
    node_680 --> node_1047
    node_1196 --> node_1195
    node_828 --> node_392
    node_729 --> node_1105
    node_931 --> node_397
    node_977 --> node_984
    node_1042 --> node_1041
    node_1104 --> node_1105
    node_1278 --> node_1070
    node_477 --> node_1309
    node_506 --> node_1254
    node_1337 --> node_1049
    node_1337 --> node_1346
    node_499 --> node_108
    node_236 --> node_748
    node_535 --> node_1367
    node_555 --> node_69
    node_506 --> node_1176
    node_663 --> node_1105
    node_645 --> node_677
    node_752 --> node_2
    node_54 --> node_252
    node_786 --> node_1283
    node_668 --> node_1192
    node_1170 --> node_240
    node_66 --> node_998
    node_613 --> node_728
    node_1140 --> node_1006
    node_356 --> node_429
    node_646 --> node_1372
    node_7 --> node_330
    node_613 --> node_648
    node_1190 --> node_1038
    node_976 --> node_13
    node_577 --> node_677
    node_0 --> node_1139
    node_189 --> node_1294
    node_498 --> node_1312
    node_896 --> node_1298
    node_6 --> node_1290
    node_30 --> node_140
    node_38 --> node_505
    node_107 --> node_243
    node_147 --> node_998
    node_1242 --> node_1238
    node_124 --> node_249
    node_530 --> node_1372
    node_1140 --> node_217
    node_1140 --> node_219
    node_779 --> node_69
    node_553 --> node_290
    node_210 --> node_756
    node_483 --> node_1105
    node_1283 --> node_1314
    node_207 --> node_370
    node_338 --> node_235
    node_807 --> node_1171
    node_1140 --> node_1108
    node_588 --> node_4
    node_552 --> node_1064
    node_7 --> node_53
    node_207 --> node_402
    node_552 --> node_664
    node_498 --> node_408
    node_553 --> node_1150
    node_499 --> node_66
    node_613 --> node_989
    node_1254 --> node_1083
    node_66 --> node_1044
    node_1208 --> node_1324
    node_207 --> node_1300
    node_609 --> node_4
    node_520 --> node_36
    node_207 --> node_405
    node_526 --> node_748
    node_6 --> node_1262
    node_498 --> node_331
    node_383 --> node_183
    node_6 --> node_1105
    node_108 --> node_49
    node_530 --> node_246
    node_1375 --> node_255
    node_680 --> node_1287
    node_0 --> node_1365
    node_790 --> node_1171
    node_65 --> node_240
    node_645 --> node_672
    node_336 --> node_10
    node_506 --> node_1342
    node_147 --> node_1044
    node_105 --> node_812
    node_498 --> node_1319
    node_506 --> node_1104
    node_588 --> node_495
    node_231 --> node_189
    node_456 --> node_234
    node_523 --> node_355
    node_147 --> node_695
    node_542 --> node_1171
    node_1362 --> node_1178
    node_696 --> node_700
    node_552 --> node_1277
    node_553 --> node_332
    node_401 --> node_1105
    node_248 --> node_1325
    node_768 --> node_992
    node_883 --> node_276
    node_1253 --> node_1177
    node_106 --> node_122
    node_679 --> node_1327
    node_20 --> node_277
    node_646 --> node_1254
    node_21 --> node_140
    node_1120 --> node_1322
    node_1253 --> node_1362
    node_646 --> node_1176
    node_789 --> node_977
    node_923 --> node_400
    node_419 --> node_1171
    node_396 --> node_199
    node_132 --> node_60
    node_1337 --> node_1223
    node_656 --> node_1262
    node_234 --> node_332
    node_552 --> node_54
    node_1362 --> node_1348
    node_144 --> node_1106
    node_106 --> node_60
    node_65 --> node_971
    node_555 --> node_74
    node_530 --> node_1176
    node_282 --> node_281
    node_32 --> node_605
    node_530 --> node_1228
    node_1007 --> node_1070
    node_418 --> node_263
    node_676 --> node_1256
    node_21 --> node_1193
    node_530 --> node_1118
    node_553 --> node_555
    node_552 --> node_1050
    node_1233 --> node_1070
    node_553 --> node_549
    node_574 --> node_951
    node_824 --> node_60
    node_473 --> node_191
    node_588 --> node_983
    node_248 --> node_252
    node_576 --> node_653
    node_677 --> node_1060
    node_1125 --> node_1283
    node_1337 --> node_1248
    node_786 --> node_712
    node_712 --> node_235
    node_1259 --> node_1257
    node_456 --> node_783
    node_536 --> node_320
    node_1104 --> node_1108
    node_670 --> node_1261
    node_722 --> node_712
    node_1024 --> node_1070
    node_682 --> node_1156
    node_187 --> node_215
    node_58 --> node_60
    node_1120 --> node_1029
    node_763 --> node_4
    node_938 --> node_408
    node_1337 --> node_1163
    node_422 --> node_32
    node_778 --> node_69
    node_506 --> node_763
    node_791 --> node_281
    node_506 --> node_1057
    node_909 --> node_384
    node_108 --> node_231
    node_995 --> node_253
    node_67 --> node_235
    node_156 --> node_60
    node_1337 --> node_1192
    node_1384 --> node_990
    node_933 --> node_412
    node_1253 --> node_1242
    node_32 --> node_691
    node_66 --> node_1161
    node_692 --> node_756
    node_973 --> node_34
    node_456 --> node_620
    node_988 --> node_1164
    node_646 --> node_1342
    node_646 --> node_1104
    node_1283 --> node_1296
    node_858 --> node_250
    node_917 --> node_281
    node_207 --> node_1317
    node_789 --> node_49
    node_207 --> node_1298
    node_613 --> node_240
    node_105 --> node_977
    node_798 --> node_1066
    node_530 --> node_1342
    node_124 --> node_205
    node_1290 --> node_1287
    node_679 --> node_1385
    node_32 --> node_628
    node_147 --> node_1161
    node_1337 --> node_1379
    node_506 --> node_1347
    node_231 --> node_1171
    node_102 --> node_179
    node_412 --> node_268
    node_498 --> node_396
    node_737 --> node_112
    node_6 --> node_497
    node_189 --> node_296
    node_6 --> node_1049
    node_6 --> node_1346
    node_880 --> node_681
    node_535 --> node_1089
    node_657 --> node_1346
    node_680 --> node_1294
    node_1254 --> node_1346
    node_1337 --> node_1053
    node_144 --> node_251
    node_1253 --> node_1337
    node_32 --> node_621
    node_1140 --> node_184
    node_644 --> node_1070
    node_1337 --> node_1280
    node_164 --> node_56
    node_668 --> node_1066
    node_320 --> node_235
    node_1254 --> node_1241
    node_609 --> node_577
    node_6 --> node_16
    node_506 --> node_1211
    node_13 --> node_673
    node_613 --> node_971
    node_532 --> node_332
    node_1337 --> node_1060
    node_65 --> node_737
    node_1120 --> node_1385
    node_1140 --> node_1123
    node_498 --> node_426
    node_108 --> node_66
    node_530 --> node_1155
    node_180 --> node_177
    node_207 --> node_373
    node_1170 --> node_189
    node_520 --> node_1283
    node_115 --> node_559
    node_735 --> node_721
    node_6 --> node_893
    node_58 --> node_63
    node_535 --> node_1117
    node_680 --> node_1195
    node_286 --> node_219
    node_646 --> node_1057
    node_102 --> node_499
    node_530 --> node_1207
    node_1125 --> node_712
    node_0 --> node_1054
    node_105 --> node_49
    node_534 --> node_957
    node_1013 --> node_1070
    node_255 --> node_74
    node_1362 --> node_1083
    node_103 --> node_558
    node_576 --> node_189
    node_591 --> node_6
    node_530 --> node_763
    node_6 --> node_387
    node_6 --> node_793
    node_98 --> node_74
    node_588 --> node_783
    node_21 --> node_991
    node_680 --> node_1194
    node_555 --> node_584
    node_712 --> node_561
    node_108 --> node_32
    node_207 --> node_372
    node_585 --> node_640
    node_1140 --> node_208
    node_1254 --> node_1043
    node_609 --> node_604
    node_506 --> node_1148
    node_530 --> node_36
    node_646 --> node_1347
    node_506 --> node_661
    node_30 --> node_555
    node_412 --> node_27
    node_552 --> node_1348
    node_641 --> node_1209
    node_21 --> node_985
    node_1100 --> node_54
    node_506 --> node_1328
    node_680 --> node_1259
    node_530 --> node_1347
    node_101 --> node_74
    node_590 --> node_1006
    node_638 --> node_177
    node_958 --> node_1086
    node_520 --> node_1106
    node_70 --> node_7
    node_588 --> node_620
    node_6 --> node_1315
    node_613 --> node_782
    node_6 --> node_1223
    node_890 --> node_13
    node_1253 --> node_1196
    node_552 --> node_412
    node_1218 --> node_1216
    node_211 --> node_270
    node_224 --> node_245
    node_661 --> node_1129
    node_530 --> node_801
    node_13 --> node_650
    node_1362 --> node_1250
    node_768 --> node_664
    node_943 --> node_189
    node_646 --> node_1211
    node_957 --> node_1259
    node_0 --> node_1367
    node_334 --> node_30
    node_1253 --> node_1218
    node_519 --> node_185
    node_456 --> node_1284
    node_1383 --> node_83
    node_763 --> node_762
    node_957 --> node_1035
    node_588 --> node_634
    node_6 --> node_839
    node_530 --> node_1197
    node_552 --> node_1028
    node_880 --> node_1277
    node_6 --> node_1248
    node_576 --> node_668
    node_1140 --> node_243
    node_1335 --> node_496
    node_958 --> node_1154
    node_613 --> node_737
    node_1254 --> node_1341
    node_32 --> node_13
    node_1229 --> node_69
    node_530 --> node_1364
    node_0 --> node_1324
    node_20 --> node_1307
    node_1253 --> node_1120
    node_656 --> node_1037
    node_1254 --> node_1217
    node_1253 --> node_1220
    node_552 --> node_181
    node_1253 --> node_1321
    node_65 --> node_754
    node_6 --> node_1163
    node_105 --> node_231
    node_1254 --> node_1040
    node_727 --> node_36
    node_535 --> node_1170
    node_1120 --> node_1380
    node_514 --> node_243
    node_843 --> node_281
    node_338 --> node_74
    node_1362 --> node_1065
    node_1170 --> node_1171
    node_768 --> node_1277
    node_569 --> node_69
    node_1337 --> node_1230
    node_6 --> node_1313
    node_798 --> node_681
    node_6 --> node_1192
    node_1385 --> node_54
    node_825 --> node_379
    node_1064 --> node_59
    node_548 --> node_1274
    node_880 --> node_989
    node_552 --> node_1323
    node_987 --> node_1039
    node_514 --> node_496
    node_102 --> node_756
    node_1038 --> node_1261
    node_691 --> node_692
    node_520 --> node_712
    node_1362 --> node_1068
    node_576 --> node_1171
    node_727 --> node_716
    node_646 --> node_1148
    node_0 --> node_1178
    node_6 --> node_1379
    node_498 --> node_288
    node_1319 --> node_202
    node_789 --> node_32
    node_552 --> node_311
    node_576 --> node_645
    node_1254 --> node_1379
    node_76 --> node_75
    node_1140 --> node_210
    node_520 --> node_251
    node_555 --> node_52
    node_1060 --> node_1322
    node_498 --> node_189
    node_530 --> node_1148
    node_181 --> node_410
    node_755 --> node_332
    node_189 --> node_297
    node_597 --> node_1298
    node_1104 --> node_249
    node_172 --> node_75
    node_983 --> node_982
    node_6 --> node_1053
    node_784 --> node_178
    node_207 --> node_1299
    node_118 --> node_71
    node_1337 --> node_1046
    node_535 --> node_1121
    node_920 --> node_455
    node_530 --> node_1328
    node_6 --> node_1280
    node_535 --> node_1059
    node_1128 --> node_1070
    node_580 --> node_396
    node_21 --> node_1026
    node_1120 --> node_1180
    node_1156 --> node_1160
    node_506 --> node_1362
    node_530 --> node_1333
    node_421 --> node_1316
    node_552 --> node_1360
    node_1362 --> node_1241
    node_6 --> node_1060
    node_1337 --> node_1042
    node_943 --> node_1171
    node_105 --> node_66
    node_1362 --> node_1166
    node_535 --> node_1164
    node_108 --> node_759
    node_65 --> node_1070
    node_551 --> node_595
    node_171 --> node_75
    node_1253 --> node_234
    node_680 --> node_1218
    node_66 --> node_992
    node_535 --> node_1331
    node_552 --> node_1083
    node_474 --> node_385
    node_6 --> node_1224
    node_712 --> node_74
    node_20 --> node_405
    node_38 --> node_252
    node_456 --> node_246
    node_1254 --> node_1224
    node_456 --> node_333
    node_710 --> node_920
    node_60 --> node_120
    node_530 --> node_338
    node_1253 --> node_1169
    node_552 --> node_332
    node_1176 --> node_1175
    node_1254 --> node_1092
    node_108 --> node_60
    node_1140 --> node_1124
    node_613 --> node_754
    node_147 --> node_992
    node_231 --> node_59
    node_1322 --> node_1320
    node_103 --> node_559
    node_181 --> node_369
    node_1289 --> node_1373
    node_105 --> node_32
    node_1116 --> node_1114
    node_67 --> node_74
    node_1140 --> node_1004
    node_535 --> node_1249
    node_570 --> node_328
    node_520 --> node_4
    node_6 --> node_393
    node_1253 --> node_1091
    node_498 --> node_422
    node_20 --> node_416
    node_167 --> node_71
    node_1033 --> node_1070
    node_1068 --> node_1106
    node_506 --> node_1242
    node_54 --> node_332
    node_191 --> node_277
    node_985 --> node_34
    node_957 --> node_1260
    node_932 --> node_1302
    node_798 --> node_1277
    node_537 --> node_1024
    node_552 --> node_1250
    node_58 --> node_1232
    node_417 --> node_211
    node_391 --> node_241
    node_32 --> node_998
    node_684 --> node_180
    node_873 --> node_717
    node_456 --> node_1118
    node_1171 --> node_1172
    node_13 --> node_687
    node_873 --> node_725
    node_588 --> node_691
    node_685 --> node_177
    node_498 --> node_1171
    node_885 --> node_332
    node_1140 --> node_257
    node_530 --> node_933
    node_210 --> node_74
    node_280 --> node_283
    node_728 --> node_726
    node_1362 --> node_1214
    node_747 --> node_746
    node_1253 --> node_1140
    node_536 --> node_363
    node_1283 --> node_1317
    node_646 --> node_1362
    node_508 --> node_36
    node_461 --> node_200
    node_1339 --> node_1070
    node_701 --> node_1106
    node_1120 --> node_1063
    node_957 --> node_1039
    node_595 --> node_596
    node_790 --> node_756
    node_544 --> node_621
    node_189 --> node_212
    node_1253 --> node_1208
    node_320 --> node_74
    node_588 --> node_628
    node_798 --> node_989
    node_13 --> node_684
    node_535 --> node_1082
    node_911 --> node_1105
    node_1382 --> node_1106
    node_81 --> node_311
    node_552 --> node_1065
    node_933 --> node_463
    node_1337 --> node_1365
    node_653 --> node_657
    node_32 --> node_1044
    node_756 --> node_243
    node_1140 --> node_447
    node_1140 --> node_202
    node_32 --> node_695
    node_108 --> node_135
    node_896 --> node_371
    node_58 --> node_1184
    node_286 --> node_283
    node_1104 --> node_205
    node_552 --> node_644
    node_1253 --> node_1229
    node_1362 --> node_1217
    node_716 --> node_1105
    node_1337 --> node_1146
    node_147 --> node_966
    node_552 --> node_1068
    node_108 --> node_63
    node_508 --> node_235
    node_1219 --> node_1070
    node_6 --> node_1230
    node_649 --> node_1234
    node_1140 --> node_207
    node_1362 --> node_1040
    node_987 --> node_1038
    node_1065 --> node_1165
    node_231 --> node_755
    node_1283 --> node_1172
    node_552 --> node_714
    node_0 --> node_1117
    node_609 --> node_618
    node_1140 --> node_377
    node_207 --> node_423
    node_1120 --> node_1050
    node_230 --> node_226
    node_1253 --> node_1038
    node_124 --> node_134
    node_1383 --> node_340
    node_74 --> node_756
    node_529 --> node_189
    node_1068 --> node_251
    node_1120 --> node_1149
    node_422 --> node_983
    node_365 --> node_37
    node_58 --> node_1113
    node_646 --> node_1242
    node_672 --> node_1274
    node_539 --> node_1018
    node_1253 --> node_1069
    node_945 --> node_1150
    node_1191 --> node_1070
    node_680 --> node_1339
    node_524 --> node_1108
    node_1229 --> node_1226
    node_509 --> node_52
    node_530 --> node_712
    node_552 --> node_1108
    node_446 --> node_431
    node_661 --> node_1126
    node_6 --> node_1046
    node_994 --> node_1257
    node_552 --> node_1241
    node_541 --> node_307
    node_154 --> node_137
    node_1106 --> node_1108
    node_1150 --> node_83
    node_536 --> node_1292
    node_0 --> node_1250
    node_24 --> node_431
    node_701 --> node_251
    node_615 --> node_645
    node_225 --> node_712
    node_807 --> node_36
    node_535 --> node_1375
    node_885 --> node_714
    node_1245 --> node_1244
    node_341 --> node_69
    node_988 --> node_177
    node_666 --> node_1037
    node_498 --> node_1310
    node_553 --> node_540
    node_536 --> node_243
    node_1382 --> node_251
    node_105 --> node_759
    node_530 --> node_1029
    node_6 --> node_1042
    node_535 --> node_1234
    node_671 --> node_1076
    node_70 --> node_243
    node_506 --> node_1196
    node_251 --> node_250
    node_995 --> node_193
    node_1337 --> node_1064
    node_1362 --> node_1363
    node_503 --> node_185
    node_613 --> node_190
    node_20 --> node_373
    node_54 --> node_1108
    node_506 --> node_1359
    node_586 --> node_1022
    node_1170 --> node_1377
    node_692 --> node_74
    node_466 --> node_1105
    node_108 --> node_747
    node_231 --> node_756
    node_104 --> node_152
    node_189 --> node_1311
    node_153 --> node_60
    node_845 --> node_286
    node_945 --> node_970
    node_456 --> node_763
    node_32 --> node_1161
    node_1254 --> node_1246
    node_535 --> node_1100
    node_108 --> node_495
    node_1253 --> node_1058
    node_104 --> node_150
    node_154 --> node_84
    node_499 --> node_519
    node_506 --> node_1120
    node_20 --> node_372
    node_1104 --> node_1005
    node_536 --> node_425
    node_506 --> node_1220
    node_727 --> node_712
    node_878 --> node_225
    node_498 --> node_1202
    node_535 --> node_1376
    node_1290 --> node_234
    node_166 --> node_250
    node_376 --> node_258
    node_571 --> node_54
    node_147 --> node_664
    node_586 --> node_1016
    node_284 --> node_185
    node_609 --> node_13
    node_675 --> node_1040
    node_768 --> node_1360
    node_509 --> node_212
    node_529 --> node_1171
    node_609 --> node_590
    node_1120 --> node_1352
    node_207 --> node_371
    node_32 --> node_975
    node_530 --> node_180
    node_552 --> node_1214
    node_65 --> node_1377
    node_456 --> node_801
    node_1375 --> node_1374
    node_6 --> node_1139
    node_798 --> node_971
    node_1140 --> node_221
    node_1254 --> node_1139
    node_553 --> node_606
    node_144 --> node_1336
    node_1253 --> node_1279
    node_463 --> node_69
    node_832 --> node_36
    node_1323 --> node_37
    node_1283 --> node_203
    node_108 --> node_983
    node_1253 --> node_248
    node_81 --> node_714
    node_211 --> node_714
    node_508 --> node_1283
    node_66 --> node_1277
    node_1380 --> node_1378
    node_857 --> node_377
    node_683 --> node_1092
    node_880 --> node_970
    node_760 --> node_235
    node_79 --> node_71
    node_552 --> node_38
    node_453 --> node_431
    node_456 --> node_137
    node_535 --> node_1372
    node_385 --> node_263
    node_189 --> node_621
    node_1244 --> node_756
    node_646 --> node_1196
    node_672 --> node_1199
    node_1120 --> node_1209
    node_1337 --> node_1054
    node_938 --> node_1310
    node_338 --> node_329
    node_0 --> node_1166
    node_147 --> node_1277
    node_646 --> node_1359
    node_616 --> node_20
    node_20 --> node_211
    node_1335 --> node_1101
    node_952 --> node_1261
    node_552 --> node_1217
    node_646 --> node_1218
    node_6 --> node_1365
    node_1362 --> node_1156
    node_1289 --> node_1098
    node_506 --> node_1258
    node_695 --> node_693
    node_211 --> node_219
    node_20 --> node_378
    node_555 --> node_652
    node_1362 --> node_1243
    node_105 --> node_135
    node_934 --> node_1314
    node_552 --> node_1040
    node_609 --> node_614
    node_1120 --> node_1348
    node_530 --> node_1359
    node_1374 --> node_990
    node_338 --> node_343
    node_49 --> node_48
    node_1264 --> node_618
    node_6 --> node_315
    node_248 --> node_1108
    node_1274 --> node_1269
    node_456 --> node_695
    node_65 --> node_499
    node_6 --> node_1146
    node_728 --> node_720
    node_32 --> node_1244
    node_8 --> node_1070
    node_714 --> node_336
    node_231 --> node_36
    node_422 --> node_620
    node_878 --> node_712
    node_646 --> node_1120
    node_524 --> node_271
    node_1254 --> node_1052
    node_646 --> node_1220
    node_1140 --> node_209
    node_309 --> node_317
    node_514 --> node_1101
    node_1104 --> node_253
    node_1253 --> node_1353
    node_789 --> node_495
    node_175 --> node_118
    node_456 --> node_84
    node_1362 --> node_1115
    node_668 --> node_1191
    node_21 --> node_1236
    node_1329 --> node_1070
    node_225 --> node_386
    node_6 --> node_376
    node_1120 --> node_1028
    node_539 --> node_4
    node_544 --> node_563
    node_536 --> node_756
    node_422 --> node_634
    node_1283 --> node_1295
    node_794 --> node_1285
    node_506 --> node_1036
    node_535 --> node_1254
    node_20 --> node_1299
    node_181 --> node_1285
    node_330 --> node_7
    node_535 --> node_1176
    node_1284 --> node_195
    node_6 --> node_717
    node_613 --> node_59
    node_680 --> node_1284
    node_613 --> node_1377
    node_807 --> node_1283
    node_104 --> node_1274
    node_1254 --> node_1255
    node_284 --> node_283
    node_1189 --> node_1070
    node_126 --> node_748
    node_552 --> node_1363
    node_1337 --> node_1324
    node_189 --> node_402
    node_941 --> node_1312
    node_683 --> node_1094
    node_609 --> node_563
    node_552 --> node_656
    node_58 --> node_1205
    node_144 --> node_255
    node_231 --> node_200
    node_609 --> node_612
    node_789 --> node_983
    node_1120 --> node_1323
    node_680 --> node_1311
    node_282 --> node_278
    node_710 --> node_60
    node_1284 --> node_214
    node_106 --> node_544
    node_531 --> node_332
    node_680 --> node_1279
    node_189 --> node_405
    node_1253 --> node_1190
    node_236 --> node_243
    node_365 --> node_758
    node_21 --> node_1066
    node_588 --> node_801
    node_6 --> node_1064
    node_995 --> node_1125
    node_530 --> node_1380
    node_755 --> node_243
    node_1290 --> node_1069
    node_476 --> node_212
    node_790 --> node_1283
    node_506 --> node_1111
    node_508 --> node_712
    node_832 --> node_211
    node_105 --> node_747
    node_532 --> node_191
    node_646 --> node_1258
    node_115 --> node_116
    node_101 --> node_1193
    node_58 --> node_1206
    node_796 --> node_192
    node_588 --> node_998
    node_189 --> node_195
    node_456 --> node_338
    node_102 --> node_74
    node_21 --> node_1020
    node_1140 --> node_321
    node_552 --> node_812
    node_542 --> node_1283
    node_498 --> node_425
    node_530 --> node_966
    node_338 --> node_330
    node_6 --> node_748
    node_904 --> node_1307
    node_822 --> node_1313
    node_530 --> node_1258
    node_101 --> node_628
    node_1337 --> node_1178
    node_480 --> node_1314
    node_108 --> node_783
    node_105 --> node_495
    node_935 --> node_36
    node_71 --> node_72
    node_495 --> node_253
    node_524 --> node_249
    node_189 --> node_416
    node_1253 --> node_1228
    node_189 --> node_214
    node_60 --> node_140
    node_1150 --> node_340
    node_555 --> node_1105
    node_419 --> node_1283
    node_613 --> node_499
    node_13 --> node_680
    node_285 --> node_694
    node_498 --> node_247
    node_802 --> node_189
    node_1259 --> node_1039
    node_535 --> node_1342
    node_338 --> node_53
    node_535 --> node_1104
    node_508 --> node_74
    node_1106 --> node_249
    node_1362 --> node_1221
    node_506 --> node_673
    node_552 --> node_1292
    node_613 --> node_977
    node_689 --> node_393
    node_106 --> node_21
    node_588 --> node_1044
    node_6 --> node_310
    node_70 --> node_108
    node_646 --> node_1036
    node_588 --> node_695
    node_509 --> node_621
    node_526 --> node_243
    node_657 --> node_1086
    node_680 --> node_1307
    node_552 --> node_243
    node_530 --> node_1180
    node_541 --> node_750
    node_520 --> node_1336
    node_235 --> node_243
    node_859 --> node_663
    node_54 --> node_249
    node_1120 --> node_1083
    node_456 --> node_933
    node_506 --> node_1038
    node_105 --> node_983
    node_21 --> node_631
    node_552 --> node_496
    node_530 --> node_252
    node_857 --> node_492
    node_1362 --> node_1335
    node_499 --> node_528
    node_957 --> node_1205
    node_69 --> node_122
    node_1322 --> node_1321
    node_211 --> node_271
    node_1385 --> node_997
    node_68 --> node_332
    node_1198 --> node_1202
    node_786 --> node_1105
    node_552 --> node_1243
    node_1253 --> node_1290
    node_721 --> node_725
    node_869 --> node_36
    node_1362 --> node_1145
    node_917 --> node_275
    node_1020 --> node_1015
    node_6 --> node_1054
    node_933 --> node_926
    node_193 --> node_37
    node_0 --> node_1363
    node_436 --> node_51
    node_553 --> node_538
    node_32 --> node_992
    node_551 --> node_586
    node_1058 --> node_1056
    node_495 --> node_1101
    node_1254 --> node_1054
    node_225 --> node_215
    node_646 --> node_1111
    node_957 --> node_1206
    node_1254 --> node_1386
    node_807 --> node_712
    node_498 --> node_394
    node_70 --> node_66
    node_157 --> node_60
    node_680 --> node_1316
    node_873 --> node_721
    node_958 --> node_1040
    node_680 --> node_1338
    node_0 --> node_1234
    node_530 --> node_1111
    node_646 --> node_1208
    node_1290 --> node_248
    node_104 --> node_1199
    node_1323 --> node_758
    node_552 --> node_210
    node_1124 --> node_990
    node_535 --> node_1057
    node_231 --> node_1283
    node_533 --> node_137
    node_613 --> node_49
    node_728 --> node_729
    node_880 --> node_38
    node_0 --> node_1235
    node_181 --> node_1313
    node_548 --> node_185
    node_598 --> node_663
    node_20 --> node_423
    node_498 --> node_756
    node_254 --> node_1314
    node_1254 --> node_1330
    node_922 --> node_584
    node_789 --> node_783
    node_422 --> node_691
    node_1104 --> node_240
    node_251 --> node_37
    node_873 --> node_189
    node_668 --> node_1065
    node_794 --> node_185
    node_1362 --> node_1052
    node_646 --> node_1229
    node_588 --> node_338
    node_1362 --> node_1215
    node_0 --> node_1100
    node_71 --> node_99
    node_530 --> node_664
    node_240 --> node_100
    node_802 --> node_1171
    node_885 --> node_335
    node_1254 --> node_1355
    node_1253 --> node_1155
    node_1362 --> node_1349
    node_1009 --> node_1070
    node_552 --> node_609
    node_535 --> node_1347
    node_768 --> node_38
    node_995 --> node_1377
    node_6 --> node_1367
    node_416 --> node_263
    node_853 --> node_405
    node_422 --> node_628
    node_680 --> node_1142
    node_890 --> node_28
    node_609 --> node_615
    node_0 --> node_1376
    node_485 --> node_387
    node_1254 --> node_1367
    node_506 --> node_654
    node_1362 --> node_1179
    node_1375 --> node_253
    node_680 --> node_1300
    node_646 --> node_1038
    node_1177 --> node_1175
    node_588 --> node_1161
    node_673 --> node_1259
    node_790 --> node_74
    node_103 --> node_332
    node_1185 --> node_37
    node_530 --> node_1063
    node_789 --> node_620
    node_584 --> node_1070
    node_155 --> node_66
    node_207 --> node_348
    node_1340 --> node_1070
    node_670 --> node_1040
    node_943 --> node_36
    node_516 --> node_306
    node_365 --> node_1325
    node_1253 --> node_1207
    node_1259 --> node_1256
    node_812 --> node_805
    node_231 --> node_1106
    node_21 --> node_681
    node_1069 --> node_1077
    node_1274 --> node_1264
    node_1362 --> node_1047
    node_181 --> node_1308
    node_524 --> node_205
    node_613 --> node_177
    node_189 --> node_373
    node_552 --> node_578
    node_6 --> node_1324
    node_535 --> node_1211
    node_1254 --> node_1324
    node_1382 --> node_329
    node_498 --> node_1084
    node_1362 --> node_1255
    node_526 --> node_394
    node_832 --> node_712
    node_253 --> node_235
    node_498 --> node_280
    node_789 --> node_634
    node_32 --> node_966
    node_498 --> node_428
    node_509 --> node_416
    node_760 --> node_74
    node_1253 --> node_1237
    node_999 --> node_243
    node_451 --> node_247
    node_6 --> node_854
    node_679 --> node_1134
    node_1171 --> node_223
    node_13 --> node_667
    node_1362 --> node_1110
    node_435 --> node_436
    node_541 --> node_275
    node_0 --> node_1156
    node_211 --> node_283
    node_365 --> node_252
    node_1125 --> node_1105
    node_935 --> node_1283
    node_552 --> node_1246
    node_207 --> node_410
    node_54 --> node_205
    node_105 --> node_783
    node_1364 --> node_1365
    node_526 --> node_756
    node_709 --> node_1025
    node_857 --> node_274
    node_179 --> node_177
    node_1382 --> node_336
    node_6 --> node_1178
    node_958 --> node_1030
    node_514 --> node_1013
    node_495 --> node_240
    node_506 --> node_1088
    node_103 --> node_116
    node_530 --> node_1149
    node_1120 --> node_1241
    node_147 --> node_1360
    node_759 --> node_59
    node_308 --> node_318
    node_496 --> node_36
    node_506 --> node_1193
    node_1375 --> node_1101
    node_211 --> node_335
    node_132 --> node_235
    node_0 --> node_1115
    node_0 --> node_1332
    node_496 --> node_1172
    node_1253 --> node_1197
    node_58 --> node_1185
    node_38 --> node_1108
    node_1065 --> node_1144
    node_231 --> node_712
    node_105 --> node_620
    node_535 --> node_1148
    node_1068 --> node_1336
    node_1337 --> node_1250
    node_646 --> node_1058
    node_106 --> node_235
    node_873 --> node_1171
    node_280 --> node_396
    node_4 --> node_584
    node_5 --> node_66
    node_880 --> node_812
    node_20 --> node_386
    node_499 --> node_506
    node_1242 --> node_1006
    node_643 --> node_1134
    node_552 --> node_736
    node_1253 --> node_1049
    node_108 --> node_179
    node_4 --> node_719
    node_60 --> node_332
    node_552 --> node_1335
    node_683 --> node_1061
    node_1253 --> node_1141
    node_535 --> node_1328
    node_712 --> node_642
    node_217 --> node_346
    node_1080 --> node_1014
    node_32 --> node_1025
    node_1100 --> node_496
    node_401 --> node_396
    node_846 --> node_1297
    node_231 --> node_251
    node_607 --> node_750
    node_1253 --> node_1144
    node_679 --> node_1214
    node_144 --> node_497
    node_422 --> node_21
    node_548 --> node_1282
    node_634 --> node_633
    node_552 --> node_1145
    node_552 --> node_665
    node_736 --> node_189
    node_0 --> node_1254
    node_189 --> node_211
    node_768 --> node_812
    node_701 --> node_1336
    node_4 --> node_562
    node_279 --> node_283
    node_231 --> node_74
    node_680 --> node_1317
    node_966 --> node_963
    node_154 --> node_30
    node_197 --> node_189
    node_552 --> node_70
    node_1170 --> node_1283
    node_207 --> node_369
    node_798 --> node_38
    node_958 --> node_1156
    node_645 --> node_688
    node_552 --> node_231
    node_1120 --> node_1043
    node_1323 --> node_1325
    node_1337 --> node_1065
    node_1382 --> node_1336
    node_1140 --> node_204
    node_650 --> node_1368
    node_58 --> node_137
    node_610 --> node_560
    node_1290 --> node_195
    node_1084 --> node_6
    node_994 --> node_1259
    node_21 --> node_728
    node_498 --> node_200
    node_70 --> node_122
    node_20 --> node_278
    node_1140 --> node_238
    node_1337 --> node_1068
    node_20 --> node_223
    node_592 --> node_34
    node_1120 --> node_1214
    node_671 --> node_1070
    node_506 --> node_1190
    node_1089 --> node_1085
    node_548 --> node_1366
    node_1290 --> node_214
    node_646 --> node_1088
    node_32 --> node_664
    node_305 --> node_314
    node_552 --> node_1052
    node_552 --> node_1215
    node_35 --> node_816
    node_70 --> node_60
    node_189 --> node_356
    node_1314 --> node_223
    node_676 --> node_1261
    node_520 --> node_1105
    node_1385 --> node_496
    node_1323 --> node_252
    node_6 --> node_1301
    node_207 --> node_412
    node_552 --> node_1349
    node_1140 --> node_598
    node_530 --> node_1088
    node_108 --> node_246
    node_108 --> node_544
    node_958 --> node_1257
    node_1140 --> node_795
    node_108 --> node_333
    node_673 --> node_1260
    node_189 --> node_1299
    node_935 --> node_712
    node_193 --> node_758
    node_506 --> node_642
    node_530 --> node_1352
    node_20 --> node_1304
    node_21 --> node_989
    node_1170 --> node_1106
    node_680 --> node_1187
    node_1362 --> node_1330
    node_0 --> node_1221
    node_886 --> node_1291
    node_530 --> node_1193
    node_460 --> node_376
    node_1126 --> node_1326
    node_506 --> node_1189
    node_515 --> node_304
    node_1120 --> node_1341
    node_20 --> node_275
    node_486 --> node_211
    node_661 --> node_1131
    node_0 --> node_1104
    node_683 --> node_178
    node_1120 --> node_1217
    node_1362 --> node_1355
    node_880 --> node_977
    node_646 --> node_1353
    node_943 --> node_1283
    node_1375 --> node_240
    node_1067 --> node_1070
    node_544 --> node_180
    node_1244 --> node_74
    node_1068 --> node_255
    node_680 --> node_1197
    node_1120 --> node_1040
    node_337 --> node_26
    node_32 --> node_1277
    node_672 --> node_1272
    node_679 --> node_1123
    node_1337 --> node_1166
    node_552 --> node_1255
    node_552 --> node_66
    node_208 --> node_223
    node_1104 --> node_189
    node_498 --> node_287
    node_0 --> node_1350
    node_789 --> node_691
    node_530 --> node_1209
    node_639 --> node_178
    node_101 --> node_1044
    node_663 --> node_189
    node_251 --> node_758
    node_1045 --> node_1070
    node_535 --> node_1362
    node_552 --> node_1110
    node_54 --> node_100
    node_155 --> node_60
    node_108 --> node_1118
    node_771 --> node_4
    node_680 --> node_1144
    node_736 --> node_1171
    node_789 --> node_628
    node_468 --> node_1293
    node_613 --> node_591
    node_374 --> node_36
    node_108 --> node_21
    node_456 --> node_30
    node_197 --> node_1171
    node_1113 --> node_1070
    node_1362 --> node_1177
    node_13 --> node_677
    node_456 --> node_966
    node_65 --> node_1106
    node_1038 --> node_1040
    node_6 --> node_1117
    node_736 --> node_1070
    node_869 --> node_712
    node_900 --> node_386
    node_1185 --> node_758
    node_1382 --> node_255
    node_1254 --> node_1117
    node_726 --> node_36
    node_69 --> node_133
    node_506 --> node_1290
    node_646 --> node_1190
    node_798 --> node_812
    node_957 --> node_1204
    node_498 --> node_404
    node_1020 --> node_1001
    node_483 --> node_189
    node_548 --> node_1200
    node_643 --> node_1123
    node_552 --> node_361
    node_768 --> node_609
    node_0 --> node_1080
    node_70 --> node_63
    node_681 --> node_680
    node_530 --> node_1028
    node_552 --> node_221
    node_453 --> node_434
    node_714 --> node_751
    node_757 --> node_332
    node_1170 --> node_251
    node_880 --> node_49
    node_588 --> node_992
    node_0 --> node_1057
    node_498 --> node_1283
    node_0 --> node_1215
    node_160 --> node_71
    node_506 --> node_1262
    node_320 --> node_332
    node_54 --> node_748
    node_187 --> node_207
    node_588 --> node_700
    node_1249 --> node_1247
    node_6 --> node_1250
    node_1362 --> node_1253
    node_105 --> node_179
    node_958 --> node_177
    node_535 --> node_1242
    node_130 --> node_75
    node_6 --> node_874
    node_530 --> node_1189
    node_1140 --> node_694
    node_0 --> node_1179
    node_717 --> node_724
    node_520 --> node_497
    node_456 --> node_252
    node_1282 --> node_1281
    node_523 --> node_616
    node_716 --> node_717
    node_1120 --> node_1224
    node_857 --> node_265
    node_401 --> node_189
    node_530 --> node_1323
    node_69 --> node_130
    node_1327 --> node_1288
    node_13 --> node_672
    node_553 --> node_189
    node_1120 --> node_1092
    node_361 --> node_268
    node_422 --> node_998
    node_13 --> node_641
    node_552 --> node_1101
    node_0 --> node_1047
    node_548 --> node_1275
    node_957 --> node_1034
    node_714 --> node_334
    node_650 --> node_1370
    node_952 --> node_1262
    node_6 --> node_193
    node_356 --> node_449
    node_548 --> node_207
    node_994 --> node_1260
    node_6 --> node_367
    node_588 --> node_2
    node_613 --> node_988
    node_1362 --> node_1259
    node_1104 --> node_1171
    node_1383 --> node_1151
    node_748 --> node_1151
    node_20 --> node_418
    node_1084 --> node_52
    node_1253 --> node_1322
    node_552 --> node_178
    node_552 --> node_1386
    node_663 --> node_1171
    node_6 --> node_1065
    node_1274 --> node_1070
    node_1290 --> node_497
    node_65 --> node_251
    node_689 --> node_178
    node_712 --> node_1151
    node_1104 --> node_1070
    node_0 --> node_1211
    node_253 --> node_254
    node_38 --> node_249
    node_66 --> node_38
    node_613 --> node_83
    node_646 --> node_1290
    node_613 --> node_1106
    node_422 --> node_1044
    node_680 --> node_1299
    node_6 --> node_1068
    node_682 --> node_1152
    node_21 --> node_971
    node_1254 --> node_1170
    node_193 --> node_1325
    node_1301 --> node_393
    node_933 --> node_1306
    node_422 --> node_695
    node_32 --> node_34
    node_530 --> node_1360
    node_798 --> node_977
    node_530 --> node_985
    node_552 --> node_1330
    node_147 --> node_38
    node_499 --> node_501
    node_957 --> node_1031
    node_65 --> node_141
    node_74 --> node_71
    node_105 --> node_246
    node_456 --> node_664
    node_0 --> node_1116
    node_105 --> node_544
    node_483 --> node_1171
    node_958 --> node_1033
    node_880 --> node_231
    node_1327 --> node_1381
    node_588 --> node_966
    node_679 --> node_1109
    node_266 --> node_1070
    node_577 --> node_683
    node_276 --> node_275
    node_58 --> node_146
    node_108 --> node_763
    node_646 --> node_1262
    node_682 --> node_1153
    node_102 --> node_691
    node_552 --> node_1355
    node_576 --> node_4
    node_1120 --> node_1243
    node_1350 --> node_1349
    node_1176 --> node_1177
    node_1140 --> node_1000
    node_639 --> node_1259
    node_679 --> node_1168
    node_496 --> node_712
    node_6 --> node_514
    node_530 --> node_1262
    node_251 --> node_1325
    node_132 --> node_74
    node_721 --> node_189
    node_768 --> node_70
    node_484 --> node_211
    node_530 --> node_1105
    node_20 --> node_348
    node_768 --> node_231
    node_102 --> node_628
    node_1156 --> node_1154
    node_106 --> node_74
    node_552 --> node_759
    node_1092 --> node_644
    node_1337 --> node_1363
    node_6 --> node_1166
    node_759 --> node_235
    node_1362 --> node_1089
    node_156 --> node_127
    node_1254 --> node_1059
    node_609 --> node_566
    node_544 --> node_252
    node_129 --> node_748
    node_6 --> node_521
    node_1140 --> node_1126
    node_983 --> node_981
    node_401 --> node_1171
    node_506 --> node_1049
    node_506 --> node_1346
    node_553 --> node_1171
    node_552 --> node_1177
    node_653 --> node_680
    node_105 --> node_1118
    node_521 --> node_404
    node_1185 --> node_1325
    node_108 --> node_801
    node_374 --> node_1283
    node_953 --> node_1040
    node_105 --> node_21
    node_1254 --> node_1164
    node_924 --> node_304
    node_251 --> node_252
    node_535 --> node_1196
    node_423 --> node_183
    node_553 --> node_1070
    node_1337 --> node_1235
    node_798 --> node_49
    node_535 --> node_1359
    node_1335 --> node_1284
    node_506 --> node_1044
    node_498 --> node_74
    node_1254 --> node_1331
    node_613 --> node_251
    node_24 --> node_201
    node_723 --> node_729
    node_988 --> node_1165
    node_1126 --> node_1122
    node_1273 --> node_1267
    node_540 --> node_606
    node_6 --> node_862
    node_680 --> node_1244
    node_1125 --> node_249
    node_508 --> node_576
    node_459 --> node_331
    node_552 --> node_1103
    node_1253 --> node_1385
    node_422 --> node_1161
    node_826 --> node_1314
    node_21 --> node_737
    node_181 --> node_361
    node_533 --> node_30
    node_631 --> node_630
    node_535 --> node_1120
    node_189 --> node_371
    node_1273 --> node_1268
    node_552 --> node_1253
    node_66 --> node_812
    node_1254 --> node_1249
    node_535 --> node_1220
    node_20 --> node_259
    node_514 --> node_1284
    node_571 --> node_243
    node_104 --> node_151
    node_108 --> node_695
    node_530 --> node_1026
    node_643 --> node_1124
    node_211 --> node_331
    node_229 --> node_396
    node_372 --> node_263
    node_880 --> node_32
    node_6 --> node_1008
    node_1284 --> node_223
    node_571 --> node_496
    node_147 --> node_812
    node_1140 --> node_450
    node_1362 --> node_1321
    node_679 --> node_1133
    node_6 --> node_190
    node_588 --> node_664
    node_977 --> node_978
    node_552 --> node_1259
    node_710 --> node_50
    node_931 --> node_266
    node_1100 --> node_1101
    node_1140 --> node_59
    node_1253 --> node_1046
    node_1120 --> node_1246
    node_6 --> node_364
    node_983 --> node_980
    node_4 --> node_576
    node_1337 --> node_1156
    node_456 --> node_1336
    node_517 --> node_1351
    node_181 --> node_1312
    node_1385 --> node_1382
    node_646 --> node_1049
    node_701 --> node_497
    node_1354 --> node_1257
    node_668 --> node_177
    node_506 --> node_1223
    node_1298 --> node_421
    node_613 --> node_4
    node_312 --> node_715
    node_106 --> node_58
    node_646 --> node_1144
    node_508 --> node_973
    node_189 --> node_223
    node_463 --> node_416
    node_530 --> node_1346
    node_1254 --> node_1082
    node_499 --> node_509
    node_933 --> node_189
    node_1382 --> node_1151
    node_682 --> node_1155
    node_6 --> node_586
    node_0 --> node_1177
    node_672 --> node_1275
    node_815 --> node_206
    node_32 --> node_1360
    node_107 --> node_235
    node_530 --> node_1108
    node_0 --> node_1362
    node_535 --> node_1258
    node_789 --> node_998
    node_1284 --> node_1286
    node_607 --> node_140
    node_588 --> node_1277
    node_462 --> node_189
    node_643 --> node_1133
    node_374 --> node_712
    node_207 --> node_374
    node_1337 --> node_1115
    node_1337 --> node_1332
    node_1120 --> node_1139
    node_506 --> node_1248
    node_104 --> node_1282
    node_903 --> node_189
    node_1382 --> node_751
    node_101 --> node_1066
    node_1188 --> node_1070
    node_802 --> node_36
    node_1362 --> node_1170
    node_649 --> node_1233
    node_639 --> node_1260
    node_792 --> node_1172
    node_108 --> node_338
    node_8 --> node_69
    node_8 --> node_83
    node_726 --> node_712
    node_679 --> node_1215
    node_1385 --> node_1101
    node_117 --> node_614
    node_645 --> node_671
    node_221 --> node_212
    node_456 --> node_1193
    node_105 --> node_763
    node_506 --> node_1163
    node_255 --> node_205
    node_552 --> node_689
    node_553 --> node_1000
    node_267 --> node_183
    node_66 --> node_977
    node_506 --> node_1192
    node_65 --> node_234
    node_789 --> node_1044
    node_552 --> node_1089
    node_21 --> node_754
    node_66 --> node_124
    node_789 --> node_695
    node_535 --> node_1036
    node_646 --> node_1354
    node_985 --> node_974
    node_1104 --> node_59
    node_613 --> node_340
    node_32 --> node_555
    node_977 --> node_975
    node_104 --> node_1366
    node_1104 --> node_1377
    node_844 --> node_411
    node_20 --> node_181
    node_6 --> node_1363
    node_231 --> node_1336
    node_613 --> node_983
    node_530 --> node_1043
    node_1125 --> node_205
    node_506 --> node_1379
    node_0 --> node_1242
    node_882 --> node_357
    node_253 --> node_252
    node_1150 --> node_1151
    node_798 --> node_66
    node_933 --> node_403
    node_454 --> node_431
    node_552 --> node_747
    node_496 --> node_223
    node_1362 --> node_1121
    node_1120 --> node_1052
    node_105 --> node_801
    node_1254 --> node_1375
    node_877 --> node_423
    node_933 --> node_868
    node_646 --> node_1223
    node_6 --> node_1234
    node_108 --> node_933
    node_506 --> node_1053
    node_6 --> node_470
    node_1254 --> node_1234
    node_1362 --> node_1091
    node_614 --> node_666
    node_153 --> node_235
    node_64 --> node_37
    node_679 --> node_1136
    node_508 --> node_1105
    node_456 --> node_255
    node_1065 --> node_1146
    node_506 --> node_1280
    node_1099 --> node_1326
    node_679 --> node_1110
    node_681 --> node_677
    node_147 --> node_609
    node_52 --> node_168
    node_530 --> node_1223
    node_857 --> node_450
    node_667 --> node_1053
    node_207 --> node_185
    node_535 --> node_1111
    node_6 --> node_1235
    node_1254 --> node_1235
    node_412 --> node_269
    node_58 --> node_30
    node_933 --> node_1171
    node_568 --> node_242
    node_880 --> node_759
    node_552 --> node_721
    node_506 --> node_1060
    node_0 --> node_1337
    node_1126 --> node_229
    node_646 --> node_1248
    node_1337 --> node_1221
    node_798 --> node_32
    node_499 --> node_6
    node_868 --> node_607
    node_1253 --> node_1146
    node_1254 --> node_1100
    node_66 --> node_49
    node_555 --> node_748
    node_462 --> node_1171
    node_1120 --> node_1255
    node_1038 --> node_1033
    node_748 --> node_335
    node_650 --> node_1204
    node_873 --> node_36
    node_32 --> node_761
    node_530 --> node_1248
    node_679 --> node_1382
    node_530 --> node_1341
    node_903 --> node_1171
    node_506 --> node_1224
    node_1254 --> node_1376
    node_159 --> node_71
    node_646 --> node_1163
    node_679 --> node_1132
    node_6 --> node_1377
    node_768 --> node_759
    node_677 --> node_1179
    node_105 --> node_695
    node_365 --> node_1108
    node_65 --> node_620
    node_541 --> node_714
    node_470 --> node_203
    node_1069 --> node_1071
    node_1120 --> node_1110
    node_1170 --> node_1069
    node_646 --> node_1192
    node_1337 --> node_1350
    node_726 --> node_720
    node_1106 --> node_189
    node_643 --> node_1136
    node_1065 --> node_1062
    node_1337 --> node_1335
    node_530 --> node_1163
    node_6 --> node_243
    node_108 --> node_146
    node_1206 --> node_1070
    node_680 --> node_1261
    node_683 --> node_1164
    node_656 --> node_1030
    node_32 --> node_1006
    node_529 --> node_4
    node_613 --> node_234
    node_6 --> node_496
    node_65 --> node_634
    node_789 --> node_1161
    node_1337 --> node_1145
    node_535 --> node_1038
    node_104 --> node_1200
    node_958 --> node_1259
    node_646 --> node_1379
    node_957 --> node_1261
    node_108 --> node_158
    node_588 --> node_1095
    node_1072 --> node_1070
    node_958 --> node_1035
    node_20 --> node_332
    node_102 --> node_998
    node_6 --> node_1156
    node_1342 --> node_1340
    node_207 --> node_406
    node_1254 --> node_1372
    node_759 --> node_74
    node_530 --> node_1379
    node_156 --> node_252
    node_646 --> node_1053
    node_643 --> node_1132
    node_885 --> node_189
    node_807 --> node_1105
    node_646 --> node_1280
    node_1253 --> node_1064
    node_680 --> node_1304
    node_115 --> node_122
    node_1337 --> node_1080
    node_552 --> node_598
    node_32 --> node_659
    node_530 --> node_1053
    node_230 --> node_219
    node_1171 --> node_1285
    node_101 --> node_681
    node_422 --> node_992
    node_65 --> node_1069
    node_613 --> node_52
    node_552 --> node_1170
    node_646 --> node_1060
    node_506 --> node_643
    node_217 --> node_345
    node_931 --> node_77
    node_456 --> node_1360
    node_456 --> node_985
    node_69 --> node_756
    node_1337 --> node_1215
    node_0 --> node_1196
    node_679 --> node_1138
    node_6 --> node_1115
    node_6 --> node_1332
    node_66 --> node_231
    node_802 --> node_1283
    node_498 --> node_71
    node_790 --> node_1105
    node_912 --> node_189
    node_729 --> node_1004
    node_102 --> node_1044
    node_481 --> node_364
    node_680 --> node_1286
    node_530 --> node_1060
    node_1337 --> node_1349
    node_104 --> node_1275
    node_831 --> node_425
    node_105 --> node_338
    node_1232 --> node_1231
    node_0 --> node_1218
    node_207 --> node_353
    node_4 --> node_612
    node_147 --> node_70
    node_1337 --> node_1179
    node_478 --> node_247
    node_670 --> node_1035
    node_51 --> node_57
    node_147 --> node_231
    node_716 --> node_189
    node_1353 --> node_1040
    node_574 --> node_663
    node_189 --> node_348
    node_1083 --> node_1084
    node_66 --> node_108
    node_511 --> node_223
    node_189 --> node_1305
    node_530 --> node_1224
    node_725 --> node_189
    node_506 --> node_1230
    node_20 --> node_367
    node_1120 --> node_1386
    node_1337 --> node_1047
    node_419 --> node_1105
    node_530 --> node_1092
    node_613 --> node_620
    node_679 --> node_1355
    node_506 --> node_1066
    node_653 --> node_677
    node_6 --> node_1254
    node_0 --> node_1120
    node_958 --> node_1089
    node_1253 --> node_54
    node_103 --> node_748
    node_0 --> node_1220
    node_0 --> node_1321
    node_1106 --> node_1171
    node_1170 --> node_248
    node_1323 --> node_1108
    node_552 --> node_1121
    node_1089 --> node_1090
    node_412 --> node_13
    node_147 --> node_108
    node_552 --> node_645
    node_552 --> node_1059
    node_1140 --> node_36
    node_501 --> node_190
    node_412 --> node_214
    node_530 --> node_249
    node_1362 --> node_1358
    node_1253 --> node_1050
    node_643 --> node_1138
    node_255 --> node_748
    node_656 --> node_1257
    node_399 --> node_361
    node_231 --> node_213
    node_126 --> node_756
    node_613 --> node_634
    node_1140 --> node_1172
    node_456 --> node_17
    node_98 --> node_748
    node_552 --> node_949
    node_832 --> node_1105
    node_1168 --> node_990
    node_1247 --> node_1070
    node_105 --> node_933
    node_1120 --> node_1330
    node_6 --> node_394
    node_660 --> node_1101
    node_8 --> node_340
    node_1290 --> node_223
    node_552 --> node_1164
    node_280 --> node_286
    node_189 --> node_410
    node_552 --> node_783
    node_552 --> node_604
    node_406 --> node_195
    node_506 --> node_1046
    node_1203 --> node_1204
    node_383 --> node_69
    node_32 --> node_38
    node_536 --> node_1307
    node_552 --> node_1331
    node_1120 --> node_1355
    node_679 --> node_60
    node_1214 --> node_60
    node_4 --> node_16
    node_617 --> node_137
    node_714 --> node_713
    node_1337 --> node_1116
    node_885 --> node_1171
    node_1140 --> node_235
    node_1120 --> node_1367
    node_515 --> node_223
    node_58 --> node_117
    node_101 --> node_748
    node_662 --> node_177
    node_953 --> node_1033
    node_233 --> node_226
    node_530 --> node_1236
    node_6 --> node_756
    node_20 --> node_1285
    node_552 --> node_1314
    node_229 --> node_1303
    node_147 --> node_66
    node_418 --> node_268
    node_506 --> node_1042
    node_613 --> node_1069
    node_784 --> node_180
    node_6 --> node_1221
    node_20 --> node_219
    node_929 --> node_191
    node_343 --> node_69
    node_656 --> node_1032
    node_873 --> node_1283
    node_65 --> node_248
    node_880 --> node_747
    node_466 --> node_189
    node_1140 --> node_995
    node_1140 --> node_200
    node_552 --> node_694
    node_511 --> node_252
    node_535 --> node_1088
    node_598 --> node_690
    node_429 --> node_449
    node_514 --> node_235
    node_683 --> node_1097
    node_552 --> node_1249
    node_429 --> node_446
    node_456 --> node_1026
    node_912 --> node_1171
    node_983 --> node_984
    node_1254 --> node_1342
    node_66 --> node_32
    node_101 --> node_1277
    node_1254 --> node_1104
    node_1382 --> node_335
    node_64 --> node_758
    node_995 --> node_234
    node_231 --> node_1105
    node_880 --> node_495
    node_1316 --> node_421
    node_683 --> node_1375
    node_553 --> node_756
    node_1290 --> node_1286
    node_70 --> node_544
    node_530 --> node_224
    node_6 --> node_177
    node_552 --> node_1245
    node_802 --> node_712
    node_409 --> node_263
    node_646 --> node_1230
    node_588 --> node_1360
    node_958 --> node_1260
    node_6 --> node_1350
    node_65 --> node_691
    node_768 --> node_747
    node_32 --> node_545
    node_609 --> node_1150
    node_509 --> node_476
    node_716 --> node_1171
    node_6 --> node_1335
    node_523 --> node_66
    node_1310 --> node_202
    node_234 --> node_756
    node_617 --> node_84
    node_571 --> node_1101
    node_725 --> node_1171
    node_309 --> node_315
    node_1099 --> node_1122
    node_1385 --> node_1383
    node_189 --> node_369
    node_530 --> node_1066
    node_598 --> node_689
    node_535 --> node_1353
    node_338 --> node_748
    node_0 --> node_1169
    node_768 --> node_495
    node_6 --> node_1145
    node_65 --> node_628
    node_13 --> node_668
    node_101 --> node_989
    node_667 --> node_1051
    node_366 --> node_1312
    node_58 --> node_1274
    node_958 --> node_1039
    node_530 --> node_1020
    node_827 --> node_402
    node_506 --> node_1139
    node_908 --> node_624
    node_880 --> node_983
    node_552 --> node_1082
    node_530 --> node_609
    node_0 --> node_1091
    node_646 --> node_1046
    node_971 --> node_137
    node_456 --> node_1108
    node_1140 --> node_806
    node_1362 --> node_1372
    node_683 --> node_1376
    node_207 --> node_264
    node_6 --> node_1080
    node_32 --> node_656
    node_70 --> node_21
    node_537 --> node_181
    node_683 --> node_1377
    node_680 --> node_1149
    node_155 --> node_544
    node_670 --> node_1260
    node_189 --> node_412
    node_153 --> node_74
    node_20 --> node_374
    node_107 --> node_6
    node_911 --> node_294
    node_646 --> node_1042
    node_1327 --> node_1167
    node_735 --> node_652
    node_6 --> node_1215
    node_103 --> node_122
    node_6 --> node_532
    node_1254 --> node_1057
    node_802 --> node_401
    node_1140 --> node_203
    node_479 --> node_239
    node_530 --> node_205
    node_535 --> node_1190
    node_697 --> node_4
    node_282 --> node_286
    node_996 --> node_595
    node_105 --> node_558
    node_108 --> node_966
    node_32 --> node_812
    node_6 --> node_199
    node_530 --> node_1042
    node_6 --> node_1349
    node_506 --> node_1365
    node_181 --> node_403
    node_0 --> node_1140
    node_1283 --> node_1313
    node_577 --> node_604
    node_666 --> node_1030
    node_422 --> node_664
    node_613 --> node_248
    node_506 --> node_681
    node_935 --> node_1105
    node_552 --> node_581
    node_1229 --> node_776
    node_466 --> node_1171
    node_6 --> node_1179
    node_108 --> node_559
    node_0 --> node_1208
    node_576 --> node_684
    node_530 --> node_631
    node_789 --> node_992
    node_1253 --> node_1348
    node_612 --> node_4
    node_737 --> node_730
    node_799 --> node_211
    node_506 --> node_1146
    node_1060 --> node_1320
    node_873 --> node_712
    node_517 --> node_587
    node_971 --> node_84
    node_679 --> node_1381
    node_1104 --> node_1107
    node_535 --> node_1189
    node_819 --> node_1307
    node_108 --> node_104
    node_335 --> node_334
    node_6 --> node_1047
    node_530 --> node_1246
    node_552 --> node_1358
    node_671 --> node_1334
    node_1190 --> node_1030
    node_613 --> node_691
    node_1140 --> node_1283
    node_1232 --> node_1070
    node_712 --> node_748
    node_553 --> node_36
    node_736 --> node_1283
    node_155 --> node_21
    node_791 --> node_286
    node_520 --> node_54
    node_0 --> node_1229
    node_588 --> node_1026
    node_774 --> node_189
    node_271 --> node_212
    node_656 --> node_1033
    node_197 --> node_1283
    node_135 --> node_614
    node_1038 --> node_1035
    node_817 --> node_373
    node_1362 --> node_1176
    node_231 --> node_497
    node_1337 --> node_1177
    node_1362 --> node_1228
    node_422 --> node_1277
    node_532 --> node_756
    node_21 --> node_977
    node_650 --> node_4
    node_627 --> node_629
    node_1283 --> node_1308
    node_613 --> node_628
    node_6 --> node_1211
    node_857 --> node_866
    node_552 --> node_1284
    node_1253 --> node_1028
    node_1254 --> node_1211
    node_531 --> node_721
    node_67 --> node_748
    node_576 --> node_13
    node_498 --> node_576
    node_20 --> node_184
    node_5 --> node_544
    node_1140 --> node_225
    node_66 --> node_759
    node_475 --> node_189
    node_1303 --> node_199
    node_995 --> node_1069
    node_20 --> node_185
    node_530 --> node_1139
    node_1290 --> node_54
    node_1335 --> node_1106
    node_1156 --> node_1159
    node_199 --> node_192
    node_335 --> node_715
    node_798 --> node_495
    node_544 --> node_1108
    node_541 --> node_335
    node_6 --> node_1116
    node_1170 --> node_1105
    node_137 --> node_60
    node_531 --> node_189
    node_537 --> node_332
    node_1120 --> node_1089
    node_1176 --> node_1174
    node_60 --> node_122
    node_147 --> node_759
    node_64 --> node_1325
    node_679 --> node_1383
    node_1385 --> node_1384
    node_535 --> node_1290
    node_548 --> node_694
    node_189 --> node_1150
    node_1354 --> node_1259
    node_756 --> node_235
    node_231 --> node_760
    node_506 --> node_1064
    node_1253 --> node_1323
    node_6 --> node_859
    node_555 --> node_735
    node_1259 --> node_1261
    node_210 --> node_748
    node_536 --> node_1317
    node_646 --> node_1365
    node_1015 --> node_1070
    node_530 --> node_70
    node_1337 --> node_1253
    node_1384 --> node_1288
    node_606 --> node_266
    node_251 --> node_1108
    node_530 --> node_207
    node_207 --> node_1318
    node_524 --> node_59
    node_552 --> node_179
    node_1335 --> node_1334
    node_880 --> node_783
    node_552 --> node_528
    node_857 --> node_806
    node_147 --> node_60
    node_320 --> node_748
    node_789 --> node_966
    node_530 --> node_1365
    node_6 --> node_891
    node_1106 --> node_59
    node_1041 --> node_1070
    node_101 --> node_971
    node_646 --> node_1146
    node_530 --> node_681
    node_1362 --> node_1342
    node_535 --> node_1262
    node_1254 --> node_1148
    node_721 --> node_36
    node_5 --> node_21
    node_712 --> node_331
    node_798 --> node_983
    node_64 --> node_252
    node_1385 --> node_1251
    node_755 --> node_247
    node_21 --> node_49
    node_679 --> node_1129
    node_1104 --> node_1283
    node_108 --> node_664
    node_833 --> node_427
    node_189 --> node_332
    node_1337 --> node_1259
    node_253 --> node_332
    node_1120 --> node_1117
    node_768 --> node_783
    node_506 --> node_728
    node_429 --> node_454
    node_20 --> node_208
    node_498 --> node_250
    node_54 --> node_59
    node_506 --> node_1277
    node_498 --> node_281
    node_880 --> node_620
    node_1126 --> node_598
    node_32 --> node_609
    node_790 --> node_182
    node_523 --> node_69
    node_0 --> node_1058
    node_498 --> node_613
    node_20 --> node_406
    node_552 --> node_1372
    node_686 --> node_1059
    node_613 --> node_242
    node_750 --> node_749
    node_774 --> node_1171
    node_895 --> node_1307
    node_943 --> node_1105
    node_1140 --> node_712
    node_995 --> node_1284
    node_207 --> node_361
    node_336 --> node_339
    node_1140 --> node_188
    node_645 --> node_679
    node_499 --> node_504
    node_924 --> node_275
    node_1384 --> node_1381
    node_1335 --> node_251
    node_552 --> node_499
    node_666 --> node_1032
    node_527 --> node_541
    node_1253 --> node_1083
    node_1362 --> node_1155
    node_506 --> node_989
    node_1068 --> node_253
    node_841 --> node_237
    node_571 --> node_722
    node_536 --> node_235
    node_6 --> node_429
    node_70 --> node_235
    node_498 --> node_400
    node_683 --> node_177
    node_6 --> node_829
    node_552 --> node_246
    node_552 --> node_544
    node_1104 --> node_1106
    node_995 --> node_248
    node_577 --> node_679
    node_722 --> node_189
    node_509 --> node_181
    node_0 --> node_1279
    node_506 --> node_1054
    node_646 --> node_1064
    node_1362 --> node_1207
    node_498 --> node_416
    node_679 --> node_1170
    node_944 --> node_518
    node_105 --> node_966
    node_106 --> node_332
    node_1190 --> node_1032
    node_1140 --> node_74
    node_645 --> node_670
    node_20 --> node_353
    node_531 --> node_1171
    node_454 --> node_434
    node_609 --> node_617
    node_514 --> node_251
    node_189 --> node_196
    node_503 --> node_280
    node_105 --> node_559
    node_613 --> node_13
    node_6 --> node_368
    node_467 --> node_200
    node_677 --> node_1321
    node_555 --> node_1006
    node_554 --> node_180
    node_1170 --> node_497
    node_588 --> node_38
    node_680 --> node_1323
    node_552 --> node_33
    node_516 --> node_750
    node_1362 --> node_1237
    node_514 --> node_74
    node_577 --> node_670
    node_1382 --> node_253
    node_1274 --> node_1263
    node_1253 --> node_1250
    node_308 --> node_319
    node_540 --> node_1070
    node_1032 --> node_1070
    node_114 --> node_1070
    node_207 --> node_408
    node_180 --> node_1062
    node_553 --> node_1283
    node_1284 --> node_1285
    node_516 --> node_6
    node_953 --> node_1035
    node_552 --> node_1176
    node_456 --> node_249
    node_1284 --> node_219
    node_1194 --> node_1070
    node_552 --> node_1118
    node_1362 --> node_1347
    node_498 --> node_1105
    node_1353 --> node_1033
    node_20 --> node_224
    node_1120 --> node_1170
    node_679 --> node_1384
    node_524 --> node_286
    node_789 --> node_664
    node_20 --> node_392
    node_1100 --> node_1284
    node_544 --> node_271
    node_1378 --> node_1070
    node_530 --> node_728
    node_6 --> node_1177
    node_6 --> node_69
    node_20 --> node_210
    node_1387 --> node_180
    node_207 --> node_1319
    node_6 --> node_308
    node_820 --> node_425
    node_65 --> node_998
    node_535 --> node_1049
    node_535 --> node_1346
    node_248 --> node_59
    node_1254 --> node_1362
    node_701 --> node_54
    node_848 --> node_36
    node_0 --> node_1353
    node_933 --> node_36
    node_161 --> node_71
    node_1362 --> node_1197
    node_69 --> node_74
    node_680 --> node_1150
    node_1253 --> node_1065
    node_189 --> node_1285
    node_499 --> node_516
    node_144 --> node_193
    node_571 --> node_721
    node_646 --> node_1050
    node_983 --> node_974
    node_141 --> node_144
    node_531 --> node_694
    node_180 --> node_1063
    node_495 --> node_1106
    node_946 --> node_37
    node_207 --> node_388
    node_798 --> node_783
    node_609 --> node_599
    node_1289 --> node_1381
    node_456 --> node_1236
    node_1104 --> node_251
    node_1337 --> node_1218
    node_65 --> node_497
    node_462 --> node_36
    node_506 --> node_1324
    node_555 --> node_663
    node_2 --> node_604
    node_32 --> node_70
    node_66 --> node_747
    node_591 --> node_571
    node_1362 --> node_1364
    node_253 --> node_1108
    node_147 --> node_737
    node_32 --> node_231
    node_903 --> node_36
    node_108 --> node_330
    node_129 --> node_243
    node_530 --> node_989
    node_588 --> node_752
    node_1253 --> node_1068
    node_789 --> node_1277
    node_286 --> node_233
    node_835 --> node_374
    node_607 --> node_335
    node_929 --> node_396
    node_1120 --> node_1121
    node_680 --> node_1083
    node_937 --> node_417
    node_1120 --> node_1059
    node_66 --> node_495
    node_147 --> node_747
    node_65 --> node_1044
    node_509 --> node_332
    node_958 --> node_1087
    node_6 --> node_1253
    node_722 --> node_1171
    node_552 --> node_1342
    node_530 --> node_1054
    node_1092 --> node_1093
    node_363 --> node_212
    node_530 --> node_1386
    node_798 --> node_620
    node_1337 --> node_1321
    node_108 --> node_53
    node_207 --> node_1293
    node_1385 --> node_1284
    node_520 --> node_1021
    node_721 --> node_1283
    node_0 --> node_1190
    node_207 --> node_384
    node_54 --> node_756
    node_506 --> node_1178
    node_1120 --> node_1164
    node_555 --> node_294
    node_32 --> node_543
    node_548 --> node_1370
    node_102 --> node_681
    node_957 --> node_1262
    node_105 --> node_664
    node_456 --> node_1066
    node_750 --> node_336
    node_1254 --> node_1242
    node_1370 --> node_1070
    node_181 --> node_411
    node_614 --> node_987
    node_662 --> node_1337
    node_798 --> node_634
    node_1120 --> node_1331
    node_282 --> node_285
    node_26 --> node_60
    node_13 --> node_678
    node_108 --> node_1193
    node_931 --> node_257
    node_6 --> node_1259
    node_453 --> node_451
    node_1253 --> node_1241
    node_456 --> node_1020
    node_248 --> node_247
    node_21 --> node_32
    node_555 --> node_190
    node_1190 --> node_1033
    node_544 --> node_249
    node_588 --> node_812
    node_66 --> node_983
    node_1362 --> node_1328
    node_506 --> node_971
    node_552 --> node_901
    node_1383 --> node_311
    node_0 --> node_1228
    node_643 --> node_1130
    node_496 --> node_1285
    node_456 --> node_609
    node_576 --> node_680
    node_45 --> node_139
    node_553 --> node_712
    node_830 --> node_414
    node_173 --> node_71
    node_1362 --> node_1333
    node_729 --> node_4
    node_6 --> node_398
    node_1120 --> node_1249
    node_6 --> node_1337
    node_1020 --> node_1005
    node_495 --> node_251
    node_530 --> node_1367
    node_535 --> node_1223
    node_552 --> node_1317
    node_931 --> node_447
    node_934 --> node_416
    node_613 --> node_998
    node_1064 --> node_205
    node_958 --> node_1152
    node_768 --> node_179
    node_1068 --> node_240
    node_1140 --> node_1128
    node_181 --> node_425
    node_529 --> node_13
    node_646 --> node_1324
    node_207 --> node_396
    node_498 --> node_372
    node_6 --> node_527
    node_656 --> node_1259
    node_236 --> node_235
    node_374 --> node_1105
    node_755 --> node_235
    node_305 --> node_317
    node_422 --> node_1360
    node_656 --> node_1035
    node_613 --> node_1151
    node_552 --> node_763
    node_613 --> node_497
    node_1253 --> node_997
    node_617 --> node_30
    node_530 --> node_1324
    node_279 --> node_425
    node_553 --> node_74
    node_156 --> node_1108
    node_931 --> node_377
    node_535 --> node_1248
    node_21 --> node_594
    node_207 --> node_1306
    node_726 --> node_1105
    node_1038 --> node_1113
    node_958 --> node_1153
    node_13 --> node_688
    node_456 --> node_631
    node_552 --> node_36
    node_1089 --> node_1086
    node_234 --> node_74
    node_591 --> node_190
    node_672 --> node_1202
    node_756 --> node_74
    node_20 --> node_202
    node_1375 --> node_1106
    node_613 --> node_1044
    node_1284 --> node_185
    node_0 --> node_1290
    node_1145 --> node_1142
    node_65 --> node_1161
    node_1337 --> node_1169
    node_535 --> node_1163
    node_646 --> node_1178
    node_613 --> node_695
    node_1125 --> node_1171
    node_977 --> node_973
    node_552 --> node_1347
    node_1120 --> node_1082
    node_74 --> node_76
    node_1145 --> node_1143
    node_1382 --> node_240
    node_60 --> node_133
    node_535 --> node_1192
    node_1385 --> node_1017
    node_679 --> node_1126
    node_1253 --> node_1214
    node_880 --> node_246
    node_781 --> node_700
    node_102 --> node_748
    node_552 --> node_801
    node_6 --> node_4
    node_1242 --> node_1245
    node_677 --> node_1085
    node_768 --> node_499
    node_1337 --> node_1091
    node_680 --> node_1285
    node_1083 --> node_1081
    node_498 --> node_387
    node_721 --> node_712
    node_552 --> node_619
    node_189 --> node_184
    node_1038 --> node_1368
    node_552 --> node_235
    node_154 --> node_100
    node_338 --> node_7
    node_1140 --> node_245
    node_535 --> node_1379
    node_498 --> node_378
    node_628 --> node_627
    node_848 --> node_1283
    node_768 --> node_246
    node_680 --> node_1108
    node_933 --> node_1283
    node_696 --> node_697
    node_102 --> node_1277
    node_20 --> node_1309
    node_530 --> node_971
    node_523 --> node_598
    node_680 --> node_1241
    node_859 --> node_652
    node_520 --> node_193
    node_885 --> node_36
    node_508 --> node_748
    node_552 --> node_995
    node_987 --> node_1040
    node_552 --> node_1364
    node_535 --> node_1053
    node_6 --> node_1196
    node_526 --> node_372
    node_1253 --> node_1217
    node_673 --> node_1258
    node_458 --> node_69
    node_462 --> node_1283
    node_1254 --> node_1196
    node_1060 --> node_1321
    node_535 --> node_1280
    node_0 --> node_1155
    node_1253 --> node_1040
    node_231 --> node_205
    node_1254 --> node_1359
    node_1337 --> node_1140
    node_60 --> node_130
    node_903 --> node_1283
    node_996 --> node_1125
    node_6 --> node_1218
    node_880 --> node_1118
    node_1140 --> node_215
    node_971 --> node_30
    node_643 --> node_1126
    node_1254 --> node_1218
    node_1266 --> node_1070
    node_655 --> node_1021
    node_712 --> node_655
    node_1140 --> node_325
    node_588 --> node_609
    node_456 --> node_70
    node_535 --> node_1060
    node_675 --> node_1034
    node_102 --> node_989
    node_942 --> node_28
    node_552 --> node_1107
    node_66 --> node_783
    node_0 --> node_1207
    node_552 --> node_602
    node_70 --> node_74
    node_1324 --> node_1060
    node_508 --> node_310
    node_544 --> node_205
    node_613 --> node_37
    node_1375 --> node_251
    node_671 --> node_1069
    node_32 --> node_974
    node_6 --> node_1120
    node_1289 --> node_1070
    node_498 --> node_1299
    node_768 --> node_1118
    node_1120 --> node_1375
    node_6 --> node_1220
    node_1254 --> node_1120
    node_6 --> node_1321
    node_108 --> node_1360
    node_1254 --> node_1220
    node_676 --> node_996
    node_725 --> node_36
    node_798 --> node_691
    node_108 --> node_985
    node_1337 --> node_1229
    node_840 --> node_288
    node_552 --> node_1148
    node_1120 --> node_1234
    node_946 --> node_758
    node_21 --> node_69
    node_511 --> node_1285
    node_0 --> node_1237
    node_680 --> node_1043
    node_902 --> node_376
    node_537 --> node_243
    node_613 --> node_1161
    node_66 --> node_620
    node_532 --> node_74
    node_105 --> node_1193
    node_552 --> node_1328
    node_511 --> node_1108
    node_189 --> node_406
    node_555 --> node_243
    node_1185 --> node_1181
    node_526 --> node_211
    node_798 --> node_628
    node_538 --> node_69
    node_496 --> node_185
    node_429 --> node_430
    node_588 --> node_631
    node_675 --> node_1031
    node_6 --> node_380
    node_552 --> node_1333
    node_101 --> node_38
    node_681 --> node_676
    node_1120 --> node_1100
    node_253 --> node_249
    node_927 --> node_387
    node_24 --> node_23
    node_506 --> node_1250
    node_20 --> node_601
    node_553 --> node_584
    node_335 --> node_713
    node_1283 --> node_1312
    node_920 --> node_50
    node_456 --> node_100
    node_168 --> node_71
    node_958 --> node_1155
    node_552 --> node_203
    node_32 --> node_759
    node_1120 --> node_1376
    node_6 --> node_427
    node_506 --> node_655
    node_537 --> node_1003
    node_6 --> node_598
    node_0 --> node_1197
    node_1290 --> node_219
    node_1362 --> node_1029
    node_957 --> node_1037
    node_1140 --> node_282
    node_1263 --> node_1070
    node_994 --> node_1261
    node_1215 --> node_1213
    node_1265 --> node_69
    node_530 --> node_737
    node_552 --> node_338
    node_843 --> node_276
    node_1253 --> node_1092
    node_207 --> node_189
    node_0 --> node_1049
    node_848 --> node_712
    node_1353 --> node_1035
    node_231 --> node_1325
    node_1254 --> node_1258
    node_680 --> node_1341
    node_6 --> node_828
    node_515 --> node_1285
    node_999 --> node_235
    node_38 --> node_59
    node_0 --> node_1141
    node_32 --> node_646
    node_656 --> node_1039
    node_790 --> node_748
    node_1140 --> node_961
    node_680 --> node_1217
    node_798 --> node_544
    node_499 --> node_539
    node_1211 --> node_1212
    node_506 --> node_1065
    node_0 --> node_1144
    node_677 --> node_1087
    node_791 --> node_296
    node_552 --> node_1283
    node_6 --> node_234
    node_256 --> node_425
    node_807 --> node_811
    node_679 --> node_1167
    node_456 --> node_253
    node_523 --> node_1245
    node_903 --> node_712
    node_108 --> node_116
    node_1106 --> node_1283
    node_6 --> node_382
    node_8 --> node_1151
    node_52 --> node_139
    node_1120 --> node_1372
    node_207 --> node_419
    node_506 --> node_1068
    node_101 --> node_126
    node_975 --> node_978
    node_6 --> node_1169
    node_530 --> node_1117
    node_107 --> node_55
    node_760 --> node_748
    node_1337 --> node_1358
    node_189 --> node_224
    node_65 --> node_144
    node_332 --> node_331
    node_70 --> node_58
    node_696 --> node_1158
    node_808 --> node_69
    node_20 --> node_408
    node_588 --> node_70
    node_506 --> node_658
    node_915 --> node_4
    node_789 --> node_1360
    node_535 --> node_1230
    node_928 --> node_387
    node_683 --> node_1337
    node_588 --> node_231
    node_144 --> node_1377
    node_1177 --> node_1174
    node_1290 --> node_997
    node_880 --> node_763
    node_108 --> node_1026
    node_1254 --> node_1036
    node_552 --> node_933
    node_8 --> node_751
    node_945 --> node_137
    node_571 --> node_1284
    node_1253 --> node_496
    node_456 --> node_728
    node_1150 --> node_311
    node_74 --> node_748
    node_552 --> node_1295
    node_6 --> node_1091
    node_798 --> node_1118
    node_20 --> node_360
    node_958 --> node_1157
    node_552 --> node_350
    node_646 --> node_1250
    node_6 --> node_52
    node_107 --> node_332
    node_798 --> node_21
    node_20 --> node_1319
    node_1068 --> node_193
    node_681 --> node_666
    node_933 --> node_890
    node_552 --> node_1106
    node_885 --> node_1283
    node_530 --> node_189
    node_821 --> node_351
    node_144 --> node_496
    node_1253 --> node_1243
    node_613 --> node_784
    node_538 --> node_690
    node_282 --> node_284
    node_156 --> node_249
    node_929 --> node_1303
    node_768 --> node_763
    node_0 --> node_1333
    node_207 --> node_403
    node_520 --> node_1125
    node_1140 --> node_433
    node_1327 --> node_1373
    node_232 --> node_223
    node_1140 --> node_593
    node_225 --> node_189
    node_1337 --> node_1279
    node_680 --> node_1147
    node_728 --> node_721
    node_20 --> node_388
    node_506 --> node_1166
    node_650 --> node_1369
    node_1335 --> node_1336
    node_101 --> node_812
    node_535 --> node_1046
    node_506 --> node_659
    node_880 --> node_801
    node_1254 --> node_1111
    node_456 --> node_1101
    node_912 --> node_1283
    node_6 --> node_1140
    node_995 --> node_37
    node_701 --> node_193
    node_594 --> node_614
    node_255 --> node_243
    node_551 --> node_602
    node_422 --> node_38
    node_1120 --> node_1254
    node_1104 --> node_1069
    node_1362 --> node_1359
    node_6 --> node_1208
    node_1190 --> node_1035
    node_1120 --> node_1176
    node_646 --> node_1065
    node_945 --> node_84
    node_1254 --> node_1208
    node_65 --> node_992
    node_553 --> node_536
    node_207 --> node_1171
    node_535 --> node_1042
    node_1374 --> node_1288
    node_58 --> node_1282
    node_1382 --> node_193
    node_506 --> node_663
    node_880 --> node_137
    node_530 --> node_754
    node_21 --> node_4
    node_253 --> node_205
    node_511 --> node_271
    node_552 --> node_9
    node_755 --> node_74
    node_639 --> node_180
    node_158 --> node_122
    node_768 --> node_801
    node_511 --> node_185
    node_885 --> node_83
    node_211 --> node_203
    node_725 --> node_1283
    node_105 --> node_1360
    node_514 --> node_1336
    node_189 --> node_237
    node_552 --> node_312
    node_231 --> node_748
    node_0 --> node_1009
    node_105 --> node_985
    node_661 --> node_1124
    node_646 --> node_1068
    node_144 --> node_124
    node_802 --> node_1105
    node_6 --> node_1229
    node_1254 --> node_1229
    node_101 --> node_243
    node_727 --> node_189
    node_552 --> node_712
    node_20 --> node_60
    node_13 --> node_669
    node_883 --> node_425
    node_1036 --> node_1037
    node_66 --> node_179
    node_8 --> node_715
    node_946 --> node_252
    node_774 --> node_36
    node_880 --> node_695
    node_1177 --> node_1176
    node_6 --> node_212
    node_356 --> node_434
    node_116 --> node_559
    node_207 --> node_1303
    node_509 --> node_243
    node_1254 --> node_1038
    node_1068 --> node_1070
    node_58 --> node_1366
    node_429 --> node_431
    node_523 --> node_900
    node_933 --> node_873
    node_552 --> node_251
    node_958 --> node_1034
    node_613 --> node_758
    node_1384 --> node_1167
    node_576 --> node_28
    node_147 --> node_179
    node_552 --> node_1029
    node_231 --> node_54
    node_880 --> node_84
    node_6 --> node_800
    node_6 --> node_1069
    node_64 --> node_1108
    node_429 --> node_452
    node_1120 --> node_1342
    node_1374 --> node_1381
    node_552 --> node_74
    node_475 --> node_36
    node_1120 --> node_1104
    node_235 --> node_74
    node_609 --> node_601
    node_530 --> node_1171
    node_646 --> node_1166
    node_515 --> node_185
    node_680 --> node_1282
    node_20 --> node_396
    node_32 --> node_747
    node_104 --> node_1370
    node_133 --> node_71
    node_401 --> node_263
    node_506 --> node_38
    node_1362 --> node_1380
    node_661 --> node_1133
    node_531 --> node_36
    node_680 --> node_1243
    node_338 --> node_243
    node_885 --> node_712
    node_530 --> node_1059
    node_21 --> node_983
    node_1253 --> node_1246
    node_225 --> node_1171
    node_101 --> node_977
    node_661 --> node_1139
    node_1244 --> node_748
    node_179 --> node_180
    node_1335 --> node_255
    node_189 --> node_202
    node_576 --> node_672
    node_54 --> node_74
    node_958 --> node_1031
    node_211 --> node_83
    node_511 --> node_249
    node_530 --> node_1164
    node_105 --> node_116
    node_613 --> node_992
    node_670 --> node_1034
    node_1104 --> node_248
    node_189 --> node_207
    node_6 --> node_390
    node_535 --> node_1365
    node_456 --> node_240
    node_538 --> node_584
    node_207 --> node_1310
    node_66 --> node_246
    node_66 --> node_544
    node_422 --> node_812
    node_66 --> node_333
    node_530 --> node_1331
    node_878 --> node_189
    node_885 --> node_74
    node_147 --> node_499
    node_1065 --> node_1145
    node_0 --> node_1322
    node_680 --> node_1366
    node_873 --> node_1105
    node_531 --> node_235
    node_520 --> node_1377
    node_539 --> node_1006
    node_129 --> node_60
    node_552 --> node_180
    node_1208 --> node_1325
    node_880 --> node_338
    node_6 --> node_1358
    node_514 --> node_255
    node_191 --> node_207
    node_535 --> node_1146
    node_1337 --> node_1228
    node_679 --> node_1172
    node_1253 --> node_1335
    node_6 --> node_1058
    node_105 --> node_1026
    node_1254 --> node_1058
    node_147 --> node_246
    node_103 --> node_756
    node_676 --> node_1259
    node_750 --> node_751
    node_552 --> node_685
    node_725 --> node_712
    node_1362 --> node_1180
    node_727 --> node_1171
    node_1382 --> node_314
    node_189 --> node_1309
    node_552 --> node_720
    node_798 --> node_801
    node_1253 --> node_1145
    node_1100 --> node_1106
    node_58 --> node_1200
    node_530 --> node_1249
    node_255 --> node_756
    node_1120 --> node_1057
    node_520 --> node_496
    node_172 --> node_76
    node_13 --> node_671
    node_579 --> node_4
    node_613 --> node_2
    node_6 --> node_1284
    node_456 --> node_971
    node_768 --> node_338
    node_798 --> node_998
    node_6 --> node_900
    node_98 --> node_756
    node_670 --> node_1031
    node_552 --> node_6
    node_498 --> node_278
    node_109 --> node_60
    node_639 --> node_1258
    node_101 --> node_49
    node_412 --> node_34
    node_8 --> node_87
    node_207 --> node_365
    node_666 --> node_1039
    node_66 --> node_1118
    node_672 --> node_1266
    node_628 --> node_629
    node_170 --> node_71
    node_6 --> node_1279
    node_0 --> node_1029
    node_66 --> node_21
    node_495 --> node_1336
    node_506 --> node_1363
    node_523 --> node_544
    node_552 --> node_1359
    node_1205 --> node_1070
    node_6 --> node_248
    node_6 --> node_816
    node_1120 --> node_1347
    node_880 --> node_933
    node_1290 --> node_496
    node_1229 --> node_1225
    node_147 --> node_1118
    node_945 --> node_1244
    node_1190 --> node_1039
    node_506 --> node_1234
    node_1140 --> node_213
    node_508 --> node_189
    node_1362 --> node_1111
    node_498 --> node_1304
    node_1253 --> node_1052
    node_1253 --> node_1215
    node_530 --> node_1125
    node_127 --> node_131
    node_67 --> node_243
    node_657 --> node_1087
    node_613 --> node_28
    node_363 --> node_211
    node_535 --> node_1064
    node_1124 --> node_1288
    node_798 --> node_695
    node_506 --> node_651
    node_999 --> node_74
    node_1253 --> node_1349
    node_506 --> node_812
    node_1254 --> node_1088
    node_58 --> node_1275
    node_680 --> node_1246
    node_506 --> node_1235
    node_530 --> node_1082
    node_588 --> node_759
    node_613 --> node_972
    node_768 --> node_933
    node_683 --> node_1091
    node_1120 --> node_1211
    node_68 --> node_235
    node_267 --> node_456
    node_65 --> node_106
    node_1170 --> node_54
    node_789 --> node_38
    node_334 --> node_84
    node_613 --> node_1325
    node_1274 --> node_1273
    node_1038 --> node_1187
    node_207 --> node_417
    node_613 --> node_566
    node_995 --> node_758
    node_124 --> node_37
    node_759 --> node_249
    node_774 --> node_1283
    node_523 --> node_21
    node_436 --> node_2
    node_878 --> node_1171
    node_253 --> node_748
    node_594 --> node_615
    node_684 --> node_1332
    node_561 --> node_34
    node_1253 --> node_1255
    node_210 --> node_243
    node_1327 --> node_1098
    node_768 --> node_773
    node_189 --> node_361
    node_1100 --> node_251
    node_6 --> node_1353
    node_499 --> node_5
    node_338 --> node_756
    node_609 --> node_646
    node_679 --> node_1328
    node_1362 --> node_1063
    node_1254 --> node_1353
    node_345 --> node_69
    node_1337 --> node_1155
    node_435 --> node_429
    node_0 --> node_1385
    node_703 --> node_719
    node_422 --> node_609
    node_1253 --> node_1110
    node_475 --> node_1283
    node_1140 --> node_1105
    node_639 --> node_1256
    node_32 --> node_645
    node_552 --> node_1380
    node_885 --> node_340
    node_677 --> node_1049
    node_21 --> node_620
    node_1274 --> node_1276
    node_32 --> node_1070
    node_107 --> node_99
    node_65 --> node_1277
    node_1124 --> node_1381
    node_456 --> node_737
    node_197 --> node_1105
    node_20 --> node_288
    node_646 --> node_1363
    node_1337 --> node_1207
    node_714 --> node_177
    node_531 --> node_1283
    node_1289 --> node_1122
    node_711 --> node_258
    node_552 --> node_966
    node_931 --> node_238
    node_20 --> node_189
    node_1120 --> node_1148
    node_675 --> node_1036
    node_514 --> node_332
    node_868 --> node_614
    node_552 --> node_1258
    node_20 --> node_284
    node_671 --> node_1067
    node_506 --> node_1156
    node_65 --> node_54
    node_132 --> node_748
    node_21 --> node_634
    node_798 --> node_338
    node_495 --> node_255
    node_1120 --> node_1328
    node_571 --> node_36
    node_530 --> node_1375
    node_106 --> node_748
    node_568 --> node_970
    node_70 --> node_330
    node_0 --> node_1046
    node_1171 --> node_1070
    node_498 --> node_587
    node_1337 --> node_1237
    node_1342 --> node_1338
    node_535 --> node_1054
    node_1254 --> node_1190
    node_135 --> node_140
    node_530 --> node_1234
    node_931 --> node_795
    node_646 --> node_1235
    node_108 --> node_1236
    node_1062 --> node_1061
    node_508 --> node_1171
    node_189 --> node_408
    node_1385 --> node_251
    node_1362 --> node_1149
    node_879 --> node_425
    node_798 --> node_1161
    node_894 --> node_424
    node_1375 --> node_1336
    node_1068 --> node_1377
    node_673 --> node_1262
    node_924 --> node_271
    node_676 --> node_1260
    node_506 --> node_977
    node_6 --> node_420
    node_614 --> node_607
    node_924 --> node_185
    node_679 --> node_1131
    node_70 --> node_53
    node_683 --> node_1165
    node_530 --> node_1235
    node_66 --> node_763
    node_506 --> node_1115
    node_506 --> node_1332
    node_32 --> node_694
    node_285 --> node_324
    node_552 --> node_1180
    node_189 --> node_331
    node_207 --> node_354
    node_523 --> node_614
    node_958 --> node_180
    node_681 --> node_683
    node_6 --> node_1228
    node_6 --> node_370
    node_552 --> node_1036
    node_530 --> node_1100
    node_571 --> node_235
    node_189 --> node_1319
    node_472 --> node_189
    node_498 --> node_748
    node_667 --> node_1115
    node_506 --> node_662
    node_672 --> node_1265
    node_207 --> node_425
    node_712 --> node_756
    node_147 --> node_763
    node_32 --> node_1245
    node_1038 --> node_1034
    node_1126 --> node_990
    node_701 --> node_1377
    node_1337 --> node_1197
    node_798 --> node_933
    node_478 --> node_250
    node_1253 --> node_1101
    node_530 --> node_1376
    node_530 --> node_59
    node_552 --> node_703
    node_499 --> node_535
    node_789 --> node_812
    node_211 --> node_340
    node_680 --> node_1318
    node_108 --> node_1066
    node_199 --> node_277
    node_774 --> node_712
    node_1382 --> node_1377
    node_523 --> node_1317
    node_966 --> node_959
    node_1337 --> node_1364
    node_169 --> node_72
    node_666 --> node_1038
    node_717 --> node_721
    node_67 --> node_756
    node_229 --> node_215
    node_1337 --> node_1141
    node_66 --> node_801
    node_1253 --> node_1386
    node_20 --> node_422
    node_396 --> node_191
    node_692 --> node_243
    node_712 --> node_177
    node_863 --> node_690
    node_1168 --> node_1326
    node_643 --> node_1131
    node_108 --> node_1020
    node_701 --> node_496
    node_931 --> node_1070
    node_1196 --> node_1194
    node_1337 --> node_1144
    node_527 --> node_272
    node_115 --> node_135
    node_552 --> node_1111
    node_101 --> node_32
    node_613 --> node_1277
    node_6 --> node_13
    node_722 --> node_1283
    node_471 --> node_195
    node_898 --> node_1317
    node_832 --> node_189
    node_6 --> node_590
    node_646 --> node_1156
    node_108 --> node_609
    node_646 --> node_1243
    node_147 --> node_801
    node_759 --> node_205
    node_1253 --> node_1252
    node_475 --> node_712
    node_535 --> node_1324
    node_189 --> node_1293
    node_675 --> node_1038
    node_677 --> node_1090
    node_6 --> node_304
    node_60 --> node_235
    node_499 --> node_507
    node_506 --> node_49
    node_1038 --> node_1031
    node_456 --> node_754
    node_1140 --> node_1285
    node_305 --> node_313
    node_69 --> node_119
    node_422 --> node_70
    node_102 --> node_38
    node_613 --> node_54
    node_1254 --> node_1290
    node_422 --> node_231
    node_523 --> node_563
    node_530 --> node_354
    node_816 --> node_1317
    node_1253 --> node_1330
    node_531 --> node_712
    node_588 --> node_737
    node_995 --> node_1325
    node_70 --> node_132
    node_530 --> node_499
    node_1253 --> node_1355
    node_1362 --> node_1088
    node_645 --> node_682
    node_320 --> node_756
    node_1120 --> node_1362
    node_617 --> node_945
    node_646 --> node_1115
    node_646 --> node_1332
    node_588 --> node_747
    node_1020 --> node_1008
    node_1362 --> node_1352
    node_66 --> node_695
    node_506 --> node_1221
    node_149 --> node_66
    node_880 --> node_992
    node_1254 --> node_1262
    node_824 --> node_388
    node_207 --> node_394
    node_535 --> node_1178
    node_552 --> node_1063
    node_1164 --> node_1144
    node_530 --> node_1332
    node_108 --> node_631
    node_143 --> node_60
    node_534 --> node_948
    node_531 --> node_74
    node_577 --> node_682
    node_480 --> node_264
    node_1337 --> node_1333
    node_924 --> node_283
    node_20 --> node_1303
    node_958 --> node_1261
    node_995 --> node_252
    node_6 --> node_515
    node_387 --> node_451
    node_472 --> node_1171
    node_598 --> node_180
    node_1061 --> node_1070
    node_0 --> node_1146
    node_897 --> node_370
    node_506 --> node_1350
    node_945 --> node_30
    node_20 --> node_1314
    node_416 --> node_434
    node_553 --> node_1105
    node_1362 --> node_1209
    node_6 --> node_1155
    node_506 --> node_1335
    node_189 --> node_396
    node_1283 --> node_1297
    node_24 --> node_245
    node_611 --> node_612
    node_679 --> node_1029
    node_552 --> node_820
    node_756 --> node_332
    node_680 --> node_1101
    node_530 --> node_1254
    node_21 --> node_691
    node_506 --> node_1145
    node_6 --> node_1207
    node_422 --> node_66
    node_124 --> node_758
    node_231 --> node_193
    node_1103 --> node_1070
    node_144 --> node_60
    node_189 --> node_1306
    node_1020 --> node_1000
    node_402 --> node_263
    node_555 --> node_690
    node_1120 --> node_1242
    node_571 --> node_1283
    node_365 --> node_59
    node_951 --> node_1018
    node_616 --> node_614
    node_829 --> node_280
    node_1104 --> node_497
    node_1020 --> node_1210
    node_498 --> node_259
    node_21 --> node_628
    node_552 --> node_1149
    node_4 --> node_27
    node_58 --> node_122
    node_832 --> node_1171
    node_789 --> node_609
    node_399 --> node_1295
    node_858 --> node_247
    node_831 --> node_1317
    node_388 --> node_263
    node_677 --> node_1322
    node_671 --> node_1073
    node_6 --> node_1237
    node_105 --> node_1236
    node_655 --> node_177
    node_506 --> node_1080
    node_800 --> node_225
    node_20 --> node_1310
    node_680 --> node_1319
    node_499 --> node_538
    node_1362 --> node_1028
    node_66 --> node_338
    node_240 --> node_242
    node_880 --> node_30
    node_457 --> node_69
    node_108 --> node_70
    node_875 --> node_420
    node_646 --> node_1221
    node_555 --> node_689
    node_207 --> node_428
    node_880 --> node_966
    node_506 --> node_1215
    node_102 --> node_812
    node_1242 --> node_1244
    node_0 --> node_1064
    node_588 --> node_754
    node_1279 --> node_1070
    node_671 --> node_1077
    node_32 --> node_179
    node_953 --> node_1034
    node_147 --> node_338
    node_68 --> node_74
    node_1120 --> node_1119
    node_506 --> node_1349
    node_935 --> node_189
    node_588 --> node_704
    node_613 --> node_34
    node_687 --> node_564
    node_36 --> node_432
    node_987 --> node_1035
    node_454 --> node_451
    node_6 --> node_407
    node_108 --> node_681
    node_1253 --> node_1259
    node_506 --> node_1179
    node_552 --> node_951
    node_670 --> node_1258
    node_812 --> node_803
    node_721 --> node_1105
    node_1362 --> node_1189
    node_1126 --> node_1373
    node_680 --> node_1367
    node_646 --> node_177
    node_6 --> node_1197
    node_768 --> node_966
    node_1362 --> node_1323
    node_530 --> node_1104
    node_56 --> node_60
    node_646 --> node_1350
    node_368 --> node_1000
    node_105 --> node_1066
    node_536 --> node_332
    node_646 --> node_1335
    node_552 --> node_1336
    node_372 --> node_1070
    node_933 --> node_822
    node_708 --> node_1070
    node_70 --> node_332
    node_506 --> node_1047
    node_101 --> node_60
    node_680 --> node_1293
    node_804 --> node_236
    node_530 --> node_1350
    node_1254 --> node_1049
    node_6 --> node_1141
    node_66 --> node_933
    node_757 --> node_235
    node_105 --> node_1020
    node_6 --> node_372
    node_646 --> node_1145
    node_189 --> node_301
    node_1053 --> node_1051
    node_102 --> node_243
    node_6 --> node_1144
    node_851 --> node_289
    node_207 --> node_36
    node_995 --> node_54
    node_495 --> node_497
    node_1140 --> node_185
    node_953 --> node_1031
    node_1254 --> node_1144
    node_105 --> node_609
    node_838 --> node_372
    node_1084 --> node_190
    node_20 --> node_1296
    node_147 --> node_933
    node_798 --> node_992
    node_1290 --> node_1101
    node_6 --> node_349
    node_408 --> node_195
    node_552 --> node_140
    node_670 --> node_1036
    node_32 --> node_499
    node_135 --> node_116
    node_1337 --> node_1322
    node_429 --> node_434
    node_12 --> node_687
    node_1333 --> node_64
    node_514 --> node_185
    node_0 --> node_1050
    node_552 --> node_1088
    node_869 --> node_189
    node_1104 --> node_37
    node_646 --> node_1080
    node_425 --> node_1070
    node_552 --> node_1352
    node_32 --> node_246
    node_506 --> node_32
    node_1323 --> node_59
    node_1140 --> node_182
    node_552 --> node_1193
    node_103 --> node_74
    node_506 --> node_1116
    node_571 --> node_712
    node_483 --> node_211
    node_759 --> node_748
    node_530 --> node_1080
    node_468 --> node_383
    node_1284 --> node_189
    node_646 --> node_1215
    node_194 --> node_198
    node_680 --> node_1103
    node_498 --> node_181
    node_672 --> node_1270
    node_523 --> node_225
    node_20 --> node_417
    node_931 --> node_450
    node_506 --> node_859
    node_667 --> node_1116
    node_1253 --> node_1089
    node_1120 --> node_1196
    node_105 --> node_631
    node_646 --> node_1349
    node_789 --> node_70
    node_102 --> node_977
    node_530 --> node_1057
    node_207 --> node_200
    node_1120 --> node_1359
    node_6 --> node_211
    node_789 --> node_231
    node_1362 --> node_1262
    node_1168 --> node_1122
    node_1283 --> node_411
    node_933 --> node_416
    node_552 --> node_1209
    node_646 --> node_1179
    node_1140 --> node_183
    node_207 --> node_389
    node_670 --> node_1256
    node_6 --> node_1333
    node_104 --> node_146
    node_393 --> node_1301
    node_1062 --> node_1021
    node_394 --> node_263
    node_1374 --> node_1167
    node_544 --> node_694
    node_149 --> node_60
    node_935 --> node_1171
    node_1170 --> node_193
    node_1337 --> node_1029
    node_60 --> node_131
    node_20 --> node_279
    node_571 --> node_74
    node_880 --> node_664
    node_124 --> node_1325
    node_58 --> node_1186
    node_680 --> node_1306
    node_646 --> node_1047
    node_977 --> node_976
    node_535 --> node_1250
    node_32 --> node_1118
    node_946 --> node_219
    node_225 --> node_36
    node_242 --> node_241
    node_498 --> node_589
    node_650 --> node_677
    node_977 --> node_979
    node_6 --> node_500
    node_680 --> node_1288
    node_108 --> node_728
    node_946 --> node_1108
    node_1120 --> node_1220
    node_530 --> node_1047
    node_1140 --> node_249
    node_371 --> node_263
    node_552 --> node_255
    node_271 --> node_432
    node_516 --> node_335
    node_1254 --> node_1223
    node_1140 --> node_186
    node_618 --> node_596
    node_422 --> node_759
    node_1075 --> node_1070
    node_555 --> node_598
    node_848 --> node_1105
    node_933 --> node_1105
    node_613 --> node_311
    node_6 --> node_356
    node_106 --> node_105
    node_1283 --> node_425
    node_798 --> node_966
    node_657 --> node_1090
    node_748 --> node_83
    node_498 --> node_1150
    node_124 --> node_252
    node_523 --> node_1244
    node_530 --> node_1211
    node_462 --> node_1105
    node_1212 --> node_1019
    node_267 --> node_69
    node_21 --> node_614
    node_670 --> node_1038
    node_529 --> node_34
    node_535 --> node_1065
    node_1254 --> node_1248
    node_639 --> node_1262
    node_553 --> node_680
    node_712 --> node_83
    node_903 --> node_1105
    node_108 --> node_989
    node_65 --> node_193
    node_60 --> node_74
    node_571 --> node_180
    node_643 --> node_1128
    node_102 --> node_49
    node_940 --> node_398
    node_646 --> node_1116
    node_448 --> node_431
    node_105 --> node_70
    node_1375 --> node_497
    node_613 --> node_1360
    node_869 --> node_1171
    node_911 --> node_621
    node_977 --> node_974
    node_728 --> node_716
    node_552 --> node_642
    node_139 --> node_71
    node_1027 --> node_436
    node_535 --> node_1068
    node_1254 --> node_1163
    node_530 --> node_1116
    node_552 --> node_1189
    node_552 --> node_583
    node_888 --> node_410
    node_1384 --> node_1373
    node_790 --> node_243
    node_561 --> node_27
    node_555 --> node_344
    node_1212 --> node_1018
    node_983 --> node_978
    node_1337 --> node_1385
    node_74 --> node_81
    node_1254 --> node_1192
    node_131 --> node_75
    node_486 --> node_189
    node_105 --> node_681
    node_1284 --> node_1171
    node_6 --> node_502
    node_456 --> node_179
    node_1120 --> node_1258
    node_456 --> node_59
    node_189 --> node_403
    node_13 --> node_670
    node_498 --> node_431
    node_571 --> node_6
    node_456 --> node_1377
    node_1269 --> node_1271
    node_496 --> node_189
    node_1140 --> node_224
    node_207 --> node_404
    node_1100 --> node_1336
    node_1156 --> node_1152
    node_4 --> node_984
    node_703 --> node_583
    node_1140 --> node_324
    node_54 --> node_242
    node_236 --> node_332
    node_1038 --> node_1380
    node_760 --> node_243
    node_613 --> node_970
    node_508 --> node_756
    node_101 --> node_495
    node_857 --> node_244
    node_207 --> node_1283
    node_498 --> node_1291
    node_464 --> node_189
    node_1254 --> node_1053
    node_1140 --> node_227
    node_0 --> node_1348
    node_1362 --> node_1346
    node_181 --> node_1311
    node_535 --> node_1166
    node_1156 --> node_1153
    node_1254 --> node_1280
    node_1253 --> node_1170
    node_468 --> node_409
    node_482 --> node_189
    node_506 --> node_1177
    node_74 --> node_243
    node_104 --> node_157
    node_679 --> node_1111
    node_609 --> node_581
    node_1120 --> node_1036
    node_1099 --> node_990
    node_552 --> node_985
    node_1354 --> node_1261
    node_165 --> node_64
    node_1254 --> node_1060
    node_680 --> node_1289
    node_699 --> node_4
    node_6 --> node_1322
    node_141 --> node_124
    node_498 --> node_196
    node_498 --> node_367
    node_456 --> node_499
    node_108 --> node_122
    node_102 --> node_231
    node_21 --> node_998
    node_0 --> node_1028
    node_32 --> node_763
    node_207 --> node_1295
    node_1385 --> node_1336
    node_878 --> node_36
    node_101 --> node_983
    node_798 --> node_664
    node_613 --> node_193
    node_207 --> node_350
    node_526 --> node_332
    node_552 --> node_1262
    node_144 --> node_234
    node_189 --> node_1303
    node_305 --> node_315
    node_1140 --> node_205
    node_235 --> node_332
    node_591 --> node_52
    node_552 --> node_1105
    node_32 --> node_36
    node_1106 --> node_1105
    node_506 --> node_1253
    node_189 --> node_1314
    node_1120 --> node_1111
    node_1253 --> node_1121
    node_491 --> node_186
    node_980 --> node_975
    node_231 --> node_1377
    node_1253 --> node_1059
    node_709 --> node_200
    node_153 --> node_748
    node_680 --> node_1260
    node_530 --> node_1283
    node_661 --> node_1130
    node_1104 --> node_758
    node_189 --> node_300
    node_1120 --> node_1208
    node_1124 --> node_1167
    node_6 --> node_1029
    node_21 --> node_1044
    node_231 --> node_243
    node_0 --> node_1323
    node_544 --> node_59
    node_1337 --> node_1380
    node_1362 --> node_1043
    node_880 --> node_1193
    node_32 --> node_716
    node_21 --> node_695
    node_32 --> node_801
    node_225 --> node_1283
    node_496 --> node_1171
    node_613 --> node_714
    node_613 --> node_7
    node_1253 --> node_1164
    node_1178 --> node_64
    node_1100 --> node_255
    node_231 --> node_496
    node_105 --> node_728
    node_416 --> node_69
    node_908 --> node_271
    node_1038 --> node_1112
    node_6 --> node_423
    node_506 --> node_1259
    node_478 --> node_262
    node_1253 --> node_1251
    node_588 --> node_179
    node_1253 --> node_1331
    node_875 --> node_1315
    node_498 --> node_219
    node_251 --> node_59
    node_1140 --> node_191
    node_696 --> node_1095
    node_576 --> node_27
    node_256 --> node_212
    node_108 --> node_971
    node_885 --> node_1105
    node_1353 --> node_1034
    node_646 --> node_1177
    node_768 --> node_1193
    node_757 --> node_74
    node_523 --> node_386
    node_1362 --> node_1223
    node_712 --> node_4
    node_464 --> node_1171
    node_422 --> node_747
    node_198 --> node_203
    node_189 --> node_1310
    node_64 --> node_60
    node_42 --> node_140
    node_334 --> node_336
    node_1128 --> node_27
    node_506 --> node_1337
    node_1275 --> node_180
    node_482 --> node_1171
    node_156 --> node_130
    node_207 --> node_712
    node_449 --> node_431
    node_114 --> node_156
    node_1120 --> node_1038
    node_530 --> node_1362
    node_1382 --> node_83
    node_105 --> node_989
    node_65 --> node_38
    node_1253 --> node_1249
    node_8 --> node_311
    node_422 --> node_495
    node_66 --> node_966
    node_912 --> node_1105
    node_451 --> node_431
    node_374 --> node_189
    node_211 --> node_195
    node_1310 --> node_180
    node_552 --> node_1026
    node_661 --> node_1125
    node_727 --> node_1283
    node_1362 --> node_1248
    node_789 --> node_759
    node_20 --> node_280
    node_1362 --> node_1341
    node_1337 --> node_1180
    node_1290 --> node_1289
    node_20 --> node_428
    node_800 --> node_215
    node_6 --> node_180
    node_854 --> node_331
    node_1011 --> node_721
    node_1242 --> node_1240
    node_657 --> node_1344
    node_760 --> node_756
    node_910 --> node_269
    node_102 --> node_32
    node_726 --> node_189
    node_0 --> node_1083
    node_1385 --> node_255
    node_1244 --> node_243
    node_1353 --> node_1031
    node_1140 --> node_222
    node_606 --> node_1070
    node_646 --> node_1253
    node_66 --> node_104
    node_1254 --> node_1230
    node_1362 --> node_1163
    node_725 --> node_1105
    node_175 --> node_71
    node_6 --> node_1385
    node_939 --> node_229
    node_946 --> node_249
    node_20 --> node_1317
    node_1156 --> node_1155
    node_672 --> node_1198
    node_114 --> node_145
    node_287 --> node_283
    node_588 --> node_499
    node_484 --> node_189
    node_237 --> node_272
    node_532 --> node_182
    node_69 --> node_121
    node_748 --> node_340
    node_174 --> node_71
    node_548 --> node_1369
    node_307 --> node_294
    node_147 --> node_104
    node_588 --> node_246
    node_933 --> node_918
    node_660 --> node_1098
    node_251 --> node_247
    node_552 --> node_1151
    node_712 --> node_340
    node_303 --> node_1000
    node_20 --> node_289
    node_677 --> node_1086
    node_552 --> node_1346
    node_872 --> node_302
    node_101 --> node_783
    node_999 --> node_332
    node_1253 --> node_1082
    node_498 --> node_374
    node_506 --> node_4
    node_21 --> node_1161
    node_646 --> node_1259
    node_588 --> node_697
    node_189 --> node_1296
    node_678 --> node_1113
    node_530 --> node_1242
    node_1362 --> node_1379
    node_20 --> node_36
    node_207 --> node_401
    node_15 --> node_200
    node_6 --> node_530
    node_144 --> node_1069
    node_1254 --> node_1046
    node_535 --> node_1363
    node_677 --> node_1050
    node_552 --> node_16
    node_1164 --> node_1146
    node_933 --> node_1313
    node_20 --> node_1172
    node_1362 --> node_1053
    node_617 --> node_100
    node_1042 --> node_1070
    node_1253 --> node_1000
    node_690 --> node_689
    node_1120 --> node_1058
    node_6 --> node_386
    node_181 --> node_416
    node_646 --> node_1337
    node_498 --> node_364
    node_80 --> node_75
    node_101 --> node_620
    node_1099 --> node_1373
    node_332 --> node_235
    node_1200 --> node_1202
    node_108 --> node_737
    node_1314 --> node_1172
    node_506 --> node_495
    node_498 --> node_414
    node_680 --> node_1303
    node_1254 --> node_1042
    node_1384 --> node_1098
    node_32 --> node_338
    node_509 --> node_1314
    node_588 --> node_1118
    node_931 --> node_866
    node_703 --> node_16
    node_878 --> node_1283
    node_530 --> node_1337
    node_1362 --> node_1060
    node_166 --> node_247
    node_680 --> node_1314
    node_506 --> node_1218
    node_535 --> node_1235
    node_885 --> node_1151
    node_20 --> node_235
    node_613 --> node_38
    node_675 --> node_1037
    node_520 --> node_234
    node_846 --> node_369
    node_679 --> node_1352
    node_499 --> node_521
    node_101 --> node_634
    node_499 --> node_510
    node_634 --> node_632
    node_374 --> node_1171
    node_1337 --> node_1063
    node_32 --> node_1283
    node_872 --> node_271
    node_863 --> node_250
    node_0 --> node_1065
    node_609 --> node_607
    node_958 --> node_1262
    node_1104 --> node_1325
    node_680 --> node_1249
    node_613 --> node_27
    node_1253 --> node_1358
    node_472 --> node_36
    node_6 --> node_1022
    node_1362 --> node_1224
    node_20 --> node_200
    node_1335 --> node_253
    node_65 --> node_812
    node_468 --> node_183
    node_737 --> node_732
    node_108 --> node_105
    node_137 --> node_129
    node_1170 --> node_496
    node_1362 --> node_1092
    node_880 --> node_1360
    node_1164 --> node_1062
    node_66 --> node_664
    node_880 --> node_985
    node_1190 --> node_1031
    node_208 --> node_1172
    node_552 --> node_1043
    node_680 --> node_1245
    node_726 --> node_1171
    node_506 --> node_1321
    node_598 --> node_642
    node_0 --> node_1068
    node_506 --> node_983
    node_1253 --> node_1375
    node_536 --> node_392
    node_555 --> node_621
    node_1253 --> node_1284
    node_484 --> node_1171
    node_58 --> node_154
    node_1140 --> node_748
    node_1164 --> node_1061
    node_253 --> node_59
    node_6 --> node_1380
    node_726 --> node_1070
    node_1120 --> node_1088
    node_32 --> node_933
    node_920 --> node_266
    node_966 --> node_962
    node_825 --> node_1300
    node_20 --> node_602
    node_931 --> node_806
    node_959 --> node_189
    node_315 --> node_1070
    node_680 --> node_1310
    node_768 --> node_985
    node_544 --> node_177
    node_514 --> node_253
    node_524 --> node_37
    node_552 --> node_1223
    node_1168 --> node_1288
    node_144 --> node_1284
    node_541 --> node_83
    node_971 --> node_100
    node_105 --> node_971
    node_1337 --> node_1050
    node_530 --> node_4
    node_514 --> node_748
    node_858 --> node_423
    node_995 --> node_1108
    node_1106 --> node_37
    node_6 --> node_1016
    node_8 --> node_7
    node_8 --> node_714
    node_656 --> node_1261
    node_613 --> node_752
    node_529 --> node_659
    node_670 --> node_1262
    node_102 --> node_759
    node_230 --> node_233
    node_1337 --> node_1149
    node_680 --> node_1082
    node_737 --> node_734
    node_6 --> node_724
    node_534 --> node_34
    node_535 --> node_1156
    node_6 --> node_275
    node_58 --> node_1201
    node_65 --> node_496
    node_0 --> node_1241
    node_144 --> node_248
    node_20 --> node_287
    node_552 --> node_1248
    node_506 --> node_598
    node_1120 --> node_1353
    node_552 --> node_1341
    node_422 --> node_783
    node_1279 --> node_1188
    node_54 --> node_37
    node_81 --> node_1151
    node_211 --> node_1151
    node_677 --> node_1345
    node_679 --> node_1028
    node_814 --> node_276
    node_499 --> node_190
    node_681 --> node_679
    node_129 --> node_235
    node_102 --> node_60
    node_789 --> node_737
    node_530 --> node_1196
    node_911 --> node_211
    node_569 --> node_1070
    node_716 --> node_723
    node_1254 --> node_1365
    node_4 --> node_974
    node_552 --> node_1163
    node_861 --> node_1292
    node_108 --> node_754
    node_71 --> node_73
    node_498 --> node_81
    node_530 --> node_1218
    node_69 --> node_748
    node_132 --> node_243
    node_552 --> node_1313
    node_789 --> node_747
    node_998 --> node_993
    node_571 --> node_951
    node_535 --> node_1115
    node_535 --> node_1332
    node_552 --> node_1192
    node_588 --> node_1158
    node_1254 --> node_1146
    node_498 --> node_406
    node_1140 --> node_492
    node_334 --> node_242
    node_571 --> node_1336
    node_646 --> node_1321
    node_65 --> node_977
    node_681 --> node_670
    node_680 --> node_1296
    node_613 --> node_812
    node_812 --> node_809
    node_20 --> node_404
    node_181 --> node_373
    node_952 --> node_1258
    node_107 --> node_75
    node_267 --> node_261
    node_530 --> node_1120
    node_506 --> node_1169
    node_32 --> node_712
    node_65 --> node_124
    node_1253 --> node_1372
    node_530 --> node_1220
    node_552 --> node_1379
    node_1120 --> node_1190
    node_774 --> node_1105
    node_880 --> node_1026
    node_1382 --> node_340
    node_459 --> node_211
    node_807 --> node_429
    node_588 --> node_763
    node_498 --> node_1292
    node_436 --> node_752
    node_20 --> node_1283
    node_499 --> node_529
    node_156 --> node_59
    node_552 --> node_1053
    node_978 --> node_975
    node_498 --> node_411
    node_520 --> node_1069
    node_498 --> node_243
    node_923 --> node_1304
    node_506 --> node_1091
    node_672 --> node_1267
    node_552 --> node_1280
    node_397 --> node_1070
    node_959 --> node_1171
    node_58 --> node_1370
    node_768 --> node_1026
    node_475 --> node_1105
    node_0 --> node_1214
    node_1120 --> node_1189
    node_893 --> node_361
    node_555 --> node_13
    node_552 --> node_1060
    node_105 --> node_737
    node_506 --> node_783
    node_672 --> node_1268
    node_1104 --> node_54
    node_531 --> node_1105
    node_671 --> node_1071
    node_798 --> node_1360
    node_1337 --> node_1352
    node_798 --> node_985
    node_101 --> node_691
    node_1068 --> node_234
    node_1372 --> node_1371
    node_613 --> node_496
    node_106 --> node_124
    node_1254 --> node_1064
    node_100 --> node_99
    node_680 --> node_1100
    node_1362 --> node_1042
    node_506 --> node_1140
    node_1259 --> node_1260
    node_552 --> node_1224
    node_20 --> node_350
    node_1065 --> node_1142
    node_728 --> node_719
    node_65 --> node_49
    node_0 --> node_1341
    node_552 --> node_1092
    node_466 --> node_211
    node_506 --> node_1208
    node_613 --> node_51
    node_472 --> node_1283
    node_1065 --> node_1143
    node_1038 --> node_1189
    node_231 --> node_221
    node_506 --> node_620
    node_0 --> node_1217
    node_456 --> node_636
    node_536 --> node_207
    node_498 --> node_392
    node_535 --> node_1221
    node_6 --> node_418
    node_947 --> node_13
    node_1253 --> node_1176
    node_1337 --> node_1209
    node_1335 --> node_240
    node_0 --> node_1040
    node_498 --> node_210
    node_253 --> node_756
    node_1046 --> node_1070
    node_1362 --> node_1246
    node_552 --> node_249
    node_701 --> node_234
    node_66 --> node_1193
    node_1067 --> node_1071
    node_645 --> node_676
    node_164 --> node_60
    node_21 --> node_992
    node_892 --> node_415
    node_952 --> node_1256
    node_32 --> node_180
    node_646 --> node_1169
    node_1127 --> node_1168
    node_506 --> node_1229
    node_506 --> node_634
    node_553 --> node_748
    node_1337 --> node_1348
    node_1382 --> node_234
    node_1120 --> node_1290
    node_1038 --> node_1369
    node_6 --> node_942
    node_571 --> node_255
    node_609 --> node_582
    node_535 --> node_1350
    node_88 --> node_86
    node_501 --> node_6
    node_147 --> node_1193
    node_646 --> node_1121
    node_535 --> node_1335
    node_530 --> node_1169
    node_520 --> node_1284
    node_653 --> node_679
    node_141 --> node_60
    node_6 --> node_54
    node_577 --> node_676
    node_234 --> node_748
    node_756 --> node_748
    node_514 --> node_240
    node_661 --> node_1122
    node_832 --> node_1283
    node_958 --> node_1037
    node_646 --> node_1091
    node_530 --> node_1036
    node_677 --> node_1343
    node_680 --> node_1372
    node_661 --> node_177
    node_535 --> node_1145
    node_6 --> node_1050
    node_207 --> node_379
    node_523 --> node_140
    node_607 --> node_83
    node_1105 --> node_245
    node_1120 --> node_1262
    node_552 --> node_1236
    node_1140 --> node_274
    node_1254 --> node_1050
    node_1362 --> node_1139
    node_123 --> node_71
    node_613 --> node_984
    node_1337 --> node_1028
    node_69 --> node_134
    node_530 --> node_1091
    node_6 --> node_1149
    node_132 --> node_756
    node_456 --> node_1106
    node_520 --> node_248
    node_69 --> node_118
    node_674 --> node_1231
    node_20 --> node_712
    node_1290 --> node_1284
    node_653 --> node_670
    node_106 --> node_756
    node_498 --> node_286
    node_189 --> node_428
    node_552 --> node_335
    node_499 --> node_511
    node_722 --> node_1105
    node_1253 --> node_1342
    node_181 --> node_1299
    node_511 --> node_59
    node_646 --> node_1140
    node_535 --> node_1080
    node_613 --> node_578
    node_332 --> node_74
    node_1071 --> node_1070
    node_508 --> node_4
    node_555 --> node_36
    node_524 --> node_758
    node_65 --> node_231
    node_1284 --> node_36
    node_102 --> node_495
    node_105 --> node_754
    node_189 --> node_1317
    node_189 --> node_1298
    node_552 --> node_324
    node_798 --> node_1026
    node_233 --> node_228
    node_180 --> node_1070
    node_1362 --> node_1365
    node_1374 --> node_1373
    node_1284 --> node_1172
    node_530 --> node_1140
    node_541 --> node_340
    node_124 --> node_1108
    node_1106 --> node_758
    node_1337 --> node_1323
    node_535 --> node_1215
    node_552 --> node_1230
    node_670 --> node_1037
    node_20 --> node_74
    node_70 --> node_106
    node_101 --> node_1118
    node_552 --> node_1066
    node_530 --> node_1208
    node_1128 --> node_199
    node_1317 --> node_1070
    node_0 --> node_1092
    node_530 --> node_620
    node_535 --> node_1349
    node_422 --> node_179
    node_553 --> node_546
    node_862 --> node_1296
    node_671 --> node_1078
    node_489 --> node_271
    node_537 --> node_235
    node_552 --> node_1020
    node_535 --> node_1179
    node_645 --> node_666
    node_472 --> node_712
    node_54 --> node_758
    node_70 --> node_748
    node_555 --> node_235
    node_506 --> node_1358
    node_506 --> node_1058
    node_530 --> node_1229
    node_1068 --> node_1069
    node_530 --> node_634
    node_645 --> node_667
    node_535 --> node_1047
    node_102 --> node_983
    node_189 --> node_1172
    node_1353 --> node_1036
    node_609 --> node_561
    node_149 --> node_544
    node_217 --> node_344
    node_680 --> node_1143
    node_577 --> node_666
    node_884 --> node_401
    node_1140 --> node_1021
    node_398 --> node_183
    node_128 --> node_71
    node_1369 --> node_1368
    node_1078 --> node_1070
    node_338 --> node_341
    node_456 --> node_251
    node_530 --> node_1038
    node_533 --> node_84
    node_1140 --> node_187
    node_588 --> node_702
    node_532 --> node_748
    node_995 --> node_496
    node_576 --> node_683
    node_217 --> node_1070
    node_552 --> node_205
    node_248 --> node_249
    node_957 --> node_1032
    node_499 --> node_503
    node_701 --> node_1069
    node_189 --> node_235
    node_202 --> node_206
    node_521 --> node_392
    node_552 --> node_1042
    node_104 --> node_1369
    node_856 --> node_391
    node_1106 --> node_205
    node_334 --> node_751
    node_318 --> node_294
    node_509 --> node_482
    node_506 --> node_1279
    node_6 --> node_34
    node_558 --> node_4
    node_1337 --> node_1083
    node_588 --> node_933
    node_306 --> node_315
    node_422 --> node_499
    node_657 --> node_1345
    node_1382 --> node_1069
    node_571 --> node_332
    node_552 --> node_631
    node_571 --> node_1105
    node_796 --> node_191
    node_0 --> node_1243
    node_574 --> node_28
    node_104 --> node_147
    node_535 --> node_1116
    node_66 --> node_1360
    node_422 --> node_246
    node_1120 --> node_1049
    node_422 --> node_544
    node_1120 --> node_1346
    node_1253 --> node_1347
    node_66 --> node_985
    node_1375 --> node_54
    node_889 --> node_380
    node_149 --> node_21
    node_613 --> node_231
    node_680 --> node_1342
    node_486 --> node_36
    node_680 --> node_1104
    node_561 --> node_646
    node_883 --> node_1317
    node_1254 --> node_1178
    node_506 --> node_691
    node_65 --> node_32
    node_525 --> node_185
    node_6 --> node_1209
    node_207 --> node_1311
    node_1038 --> node_1378
    node_1065 --> node_1364
    node_498 --> node_1309
    node_147 --> node_985
    node_508 --> node_198
    node_555 --> node_211
    node_683 --> node_1062
    node_81 --> node_335
    node_656 --> node_34
    node_498 --> node_199
    node_679 --> node_1354
    node_320 --> node_269
    node_737 --> node_735
    node_592 --> node_593
    node_646 --> node_1358
    node_6 --> node_1348
    node_506 --> node_628
    node_974 --> node_975
    node_759 --> node_243
    node_451 --> node_434
    node_506 --> node_639
    node_684 --> node_1329
    node_1254 --> node_1348
    node_24 --> node_224
    node_553 --> node_1247
    node_849 --> node_185
    node_680 --> node_1084
    node_1253 --> node_1364
    node_671 --> node_1068
    node_552 --> node_1139
    node_464 --> node_36
    node_6 --> node_412
    node_966 --> node_960
    node_1123 --> node_194
    node_469 --> node_181
    node_305 --> node_316
    node_506 --> node_1353
    node_530 --> node_1058
    node_21 --> node_664
    node_422 --> node_1118
    node_547 --> node_1070
    node_650 --> node_1203
    node_482 --> node_36
    node_189 --> node_287
    node_1068 --> node_248
    node_1140 --> node_189
    node_701 --> node_1284
    node_576 --> node_669
    node_101 --> node_763
    node_524 --> node_1325
    node_6 --> node_1028
    node_869 --> node_1283
    node_680 --> node_1298
    node_20 --> node_567
    node_646 --> node_1279
    node_620 --> node_619
    node_65 --> node_1101
    node_1106 --> node_1325
    node_463 --> node_1314
    node_1335 --> node_193
    node_1284 --> node_1283
    node_487 --> node_389
    node_552 --> node_1365
    node_701 --> node_248
    node_102 --> node_783
    node_548 --> node_324
    node_552 --> node_681
    node_530 --> node_1279
    node_1362 --> node_1054
    node_706 --> node_262
    node_530 --> node_1127
    node_21 --> node_1277
    node_1362 --> node_1386
    node_839 --> node_393
    node_1253 --> node_1148
    node_552 --> node_315
    node_1382 --> node_248
    node_456 --> node_58
    node_880 --> node_1236
    node_864 --> node_1172
    node_54 --> node_1325
    node_1120 --> node_1223
    node_1124 --> node_1373
    node_867 --> node_210
    node_6 --> node_1323
    node_101 --> node_801
    node_1140 --> node_265
    node_506 --> node_652
    node_108 --> node_499
    node_1253 --> node_1328
    node_987 --> node_1034
    node_498 --> node_601
    node_1328 --> node_1327
    node_60 --> node_119
    node_607 --> node_340
    node_21 --> node_117
    node_1038 --> node_1043
    node_0 --> node_1246
    node_66 --> node_1026
    node_101 --> node_998
    node_514 --> node_193
    node_682 --> node_1159
    node_102 --> node_620
    node_101 --> node_235
    node_248 --> node_205
    node_613 --> node_32
    node_1253 --> node_1333
    node_530 --> node_691
    node_498 --> node_221
    node_871 --> node_573
    node_305 --> node_294
    node_158 --> node_559
    node_114 --> node_138
    node_38 --> node_37
    node_768 --> node_1236
    node_1281 --> node_1070
    node_499 --> node_554
    node_1120 --> node_1248
    node_6 --> node_912
    node_147 --> node_1026
    node_435 --> node_449
    node_506 --> node_1228
    node_58 --> node_84
    node_755 --> node_748
    node_762 --> node_776
    node_834 --> node_575
    node_506 --> node_1118
    node_1038 --> node_1037
    node_509 --> node_235
    node_530 --> node_628
    node_1203 --> node_1070
    node_1256 --> node_4
    node_102 --> node_634
    node_1337 --> node_1241
    node_710 --> node_1070
    node_676 --> node_1258
    node_657 --> node_1343
    node_1362 --> node_1367
    node_1120 --> node_1163
    node_880 --> node_1066
    node_1140 --> node_206
    node_789 --> node_179
    node_544 --> node_4
    node_126 --> node_332
    node_987 --> node_1031
    node_207 --> node_420
    node_876 --> node_1188
    node_530 --> node_1353
    node_0 --> node_1335
    node_609 --> node_1015
    node_1120 --> node_1192
    node_535 --> node_1177
    node_101 --> node_695
    node_535 --> node_69
    node_465 --> node_36
    node_189 --> node_1295
    node_880 --> node_1020
    node_65 --> node_759
    node_553 --> node_320
    node_189 --> node_350
    node_1374 --> node_1098
    node_1140 --> node_1171
    node_613 --> node_22
    node_0 --> node_1145
    node_1362 --> node_1324
    node_880 --> node_609
    node_628 --> node_630
    node_768 --> node_1066
    node_576 --> node_671
    node_6 --> node_1083
    node_506 --> node_13
    node_552 --> node_253
    node_20 --> node_385
    node_1093 --> node_1008
    node_613 --> node_1101
    node_1120 --> node_1379
    node_555 --> node_1244
    node_498 --> node_209
    node_20 --> node_215
    node_680 --> node_1107
    node_511 --> node_1172
    node_52 --> node_170
    node_1104 --> node_193
    node_759 --> node_756
    node_768 --> node_1020
    node_6 --> node_332
    node_486 --> node_1283
    node_552 --> node_748
    node_1380 --> node_1016
    node_235 --> node_748
    node_422 --> node_763
    node_498 --> node_360
    node_1120 --> node_1053
    node_429 --> node_451
    node_255 --> node_37
    node_496 --> node_1283
    node_1337 --> node_1043
    node_555 --> node_712
    node_1120 --> node_1280
    node_498 --> node_285
    node_484 --> node_36
    node_1284 --> node_712
    node_514 --> node_1070
    node_530 --> node_1190
    node_535 --> node_1253
    node_716 --> node_729
    node_680 --> node_1148
    node_499 --> node_508
    node_516 --> node_190
    node_789 --> node_499
    node_552 --> node_728
    node_672 --> node_1271
    node_613 --> node_974
    node_1290 --> node_36
    node_0 --> node_1052
    node_1038 --> node_1379
    node_498 --> node_388
    node_1120 --> node_1060
    node_207 --> node_416
    node_288 --> node_283
    node_794 --> node_223
    node_1253 --> node_1106
    node_182 --> node_215
    node_880 --> node_631
    node_904 --> node_404
    node_552 --> node_310
    node_78 --> node_71
    node_498 --> node_368
    node_1290 --> node_1172
    node_789 --> node_246
    node_646 --> node_1228
    node_13 --> node_682
    node_1337 --> node_1214
    node_0 --> node_1349
    node_464 --> node_1283
    node_181 --> node_223
    node_1254 --> node_1250
    node_207 --> node_383
    node_537 --> node_74
    node_32 --> node_951
    node_1125 --> node_37
    node_931 --> node_282
    node_729 --> node_1006
    node_857 --> node_77
    node_179 --> node_178
    node_422 --> node_801
    node_482 --> node_1283
    node_535 --> node_1259
    node_371 --> node_421
    node_885 --> node_748
    node_101 --> node_338
    node_683 --> node_1095
    node_544 --> node_719
    node_189 --> node_188
    node_153 --> node_243
    node_1140 --> node_294
    node_515 --> node_1172
    node_552 --> node_989
    node_768 --> node_631
    node_1089 --> node_1087
    node_506 --> node_1155
    node_32 --> node_330
    node_931 --> node_961
    node_498 --> node_1294
    node_488 --> node_1312
    node_770 --> node_4
    node_255 --> node_256
    node_798 --> node_1236
    node_531 --> node_324
    node_679 --> node_1236
    node_317 --> node_294
    node_1337 --> node_1341
    node_0 --> node_1255
    node_207 --> node_1105
    node_101 --> node_1161
    node_823 --> node_270
    node_552 --> node_1054
    node_613 --> node_67
    node_535 --> node_1337
    node_1337 --> node_1217
    node_613 --> node_759
    node_506 --> node_1207
    node_495 --> node_193
    node_879 --> node_1317
    node_1179 --> node_1070
    node_1254 --> node_1065
    node_207 --> node_359
    node_32 --> node_53
    node_1337 --> node_1040
    node_498 --> node_60
    node_789 --> node_1118
    node_189 --> node_74
    node_0 --> node_1110
    node_253 --> node_74
    node_342 --> node_69
    node_532 --> node_187
    node_1168 --> node_1167
    node_411 --> node_263
    node_680 --> node_1283
    node_812 --> node_36
    node_1140 --> node_1125
    node_645 --> node_683
    node_1254 --> node_1068
    node_105 --> node_499
    node_231 --> node_234
    node_506 --> node_1237
    node_101 --> node_933
    node_424 --> node_331
    node_506 --> node_638
    node_32 --> node_1193
    node_530 --> node_1290
    node_456 --> node_261
    node_714 --> node_715
    node_880 --> node_70
    node_945 --> node_100
    node_679 --> node_1366
    node_20 --> node_273
    node_1253 --> node_251
    node_486 --> node_712
    node_953 --> node_1037
    node_850 --> node_418
    node_107 --> node_756
    node_456 --> node_634
    node_349 --> node_263
    node_1253 --> node_1029
    node_1104 --> node_997
    node_798 --> node_1020
    node_959 --> node_36
    node_1189 --> node_1188
    node_210 --> node_235
    node_552 --> node_305
    node_6 --> node_217
    node_506 --> node_801
    node_931 --> node_433
    node_552 --> node_1367
    node_999 --> node_748
    node_193 --> node_252
    node_555 --> node_6
    node_680 --> node_1295
    node_870 --> node_419
    node_798 --> node_609
    node_506 --> node_998
    node_6 --> node_1241
    node_680 --> node_1106
    node_717 --> node_718
    node_506 --> node_1197
    node_207 --> node_347
    node_225 --> node_1105
    node_1254 --> node_1166
    node_646 --> node_1155
    node_465 --> node_1283
    node_1283 --> node_1311
    node_768 --> node_681
    node_552 --> node_1324
    node_1120 --> node_1230
    node_198 --> node_195
    node_464 --> node_712
    node_506 --> node_1364
    node_995 --> node_1101
    node_456 --> node_1069
    node_506 --> node_1141
    node_671 --> node_1075
    node_38 --> node_758
    node_482 --> node_712
    node_1124 --> node_1098
    node_646 --> node_1207
    node_211 --> node_310
    node_679 --> node_1124
    node_1100 --> node_253
    node_65 --> node_747
    node_506 --> node_1144
    node_1337 --> node_1224
    node_880 --> node_100
    node_498 --> node_398
    node_552 --> node_240
    node_1337 --> node_1092
    node_134 --> node_71
    node_726 --> node_1283
    node_422 --> node_338
    node_535 --> node_1218
    node_506 --> node_695
    node_798 --> node_631
    node_0 --> node_1386
    node_65 --> node_495
    node_240 --> node_970
    node_108 --> node_115
    node_207 --> node_409
    node_416 --> node_1172
    node_552 --> node_1178
    node_484 --> node_1283
    node_102 --> node_246
    node_646 --> node_1237
    node_58 --> node_558
    node_1289 --> node_990
    node_1362 --> node_1117
    node_20 --> node_352
    node_551 --> node_575
    node_1185 --> node_252
    node_1213 --> node_60
    node_1120 --> node_1046
    node_6 --> node_1043
    node_727 --> node_1105
    node_498 --> node_722
    node_1068 --> node_1067
    node_1290 --> node_1283
    node_32 --> node_642
    node_195 --> node_331
    node_1177 --> node_1173
    node_153 --> node_756
    node_309 --> node_313
    node_530 --> node_1237
    node_1375 --> node_193
    node_293 --> node_1070
    node_680 --> node_1242
    node_535 --> node_1321
    node_641 --> node_1178
    node_971 --> node_969
    node_6 --> node_374
    node_999 --> node_331
    node_672 --> node_1200
    node_0 --> node_1330
    node_21 --> node_1360
    node_552 --> node_971
    node_1120 --> node_1042
    node_1234 --> node_1233
    node_81 --> node_331
    node_1068 --> node_497
    node_6 --> node_1214
    node_789 --> node_763
    node_609 --> node_568
    node_1215 --> node_60
    node_311 --> node_312
    node_1254 --> node_1214
    node_1335 --> node_1377
    node_38 --> node_205
    node_1385 --> node_253
    node_0 --> node_1355
    node_852 --> node_349
    node_65 --> node_983
    node_506 --> node_1333
    node_422 --> node_933
    node_1140 --> node_192
    node_1253 --> node_1359
    node_646 --> node_1197
    node_548 --> node_1162
    node_1274 --> node_1272
    node_679 --> node_1139
    node_255 --> node_758
    node_721 --> node_1171
    node_509 --> node_74
    node_102 --> node_1118
    node_530 --> node_998
    node_149 --> node_146
    node_231 --> node_1069
    node_913 --> node_209
    node_692 --> node_235
    node_1337 --> node_1243
    node_880 --> node_728
    node_646 --> node_1364
    node_613 --> node_10
    node_1038 --> node_1042
    node_646 --> node_1141
    node_1290 --> node_1106
    node_735 --> node_598
    node_994 --> node_1008
    node_6 --> node_1341
    node_1170 --> node_234
    node_661 --> node_1128
    node_207 --> node_387
    node_506 --> node_647
    node_514 --> node_1377
    node_530 --> node_1049
    node_798 --> node_70
    node_848 --> node_189
    node_6 --> node_1217
    node_211 --> node_305
    node_506 --> node_338
    node_1382 --> node_497
    node_789 --> node_801
    node_530 --> node_1141
    node_798 --> node_231
    node_456 --> node_248
    node_66 --> node_1236
    node_6 --> node_1040
    node_465 --> node_712
    node_506 --> node_615
    node_1125 --> node_758
    node_682 --> node_1158
    node_613 --> node_747
    node_32 --> node_985
    node_881 --> node_404
    node_768 --> node_728
    node_530 --> node_1144
    node_20 --> node_576
    node_812 --> node_1283
    node_1100 --> node_1099
    node_995 --> node_240
    node_1244 --> node_1245
    node_947 --> node_28
    node_1331 --> node_1329
    node_530 --> node_1044
    node_1029 --> node_1027
    node_506 --> node_1161
    node_52 --> node_166
    node_575 --> node_595
    node_147 --> node_1236
    node_530 --> node_695
    node_878 --> node_1105
    node_267 --> node_458
    node_643 --> node_1139
    node_613 --> node_495
    node_456 --> node_691
    node_207 --> node_1315
    node_6 --> node_185
    node_552 --> node_1021
    node_689 --> node_1301
    node_154 --> node_242
    node_32 --> node_1105
    node_959 --> node_1283
    node_207 --> node_356
    node_768 --> node_989
    node_946 --> node_693
    node_536 --> node_1314
    node_656 --> node_1040
    node_484 --> node_712
    node_456 --> node_628
    node_535 --> node_1169
    node_646 --> node_1328
    node_1253 --> node_1380
    node_498 --> node_284
    node_0 --> node_1253
    node_66 --> node_1066
    node_506 --> node_933
    node_1283 --> node_405
    node_69 --> node_243
    node_189 --> node_245
    node_822 --> node_412
    node_941 --> node_411
    node_728 --> node_16
    node_1120 --> node_1365
    node_1290 --> node_712
    node_646 --> node_1333
    node_548 --> node_259
    node_552 --> node_737
    node_38 --> node_1325
    node_509 --> node_6
    node_1327 --> node_1070
    node_334 --> node_713
    node_66 --> node_1020
    node_101 --> node_992
    node_334 --> node_100
    node_231 --> node_1284
    node_1253 --> node_1258
    node_553 --> node_363
    node_1382 --> node_334
    node_669 --> node_1192
    node_535 --> node_1091
    node_147 --> node_1066
    node_1254 --> node_1363
    node_1120 --> node_1146
    node_66 --> node_609
    node_1290 --> node_251
    node_680 --> node_1196
    node_1362 --> node_1059
    node_531 --> node_748
    node_682 --> node_1157
    node_20 --> node_281
    node_207 --> node_1313
    node_189 --> node_215
    node_147 --> node_1020
    node_0 --> node_1259
    node_1283 --> node_416
    node_545 --> node_69
    node_231 --> node_248
    node_1104 --> node_496
    node_20 --> node_613
    node_1100 --> node_240
    node_47 --> node_46
    node_885 --> node_311
    node_981 --> node_984
    node_671 --> node_1335
    node_1337 --> node_1246
    node_1362 --> node_1164
    node_530 --> node_37
    node_552 --> node_1117
    node_6 --> node_1092
    node_191 --> node_215
    node_498 --> node_198
    node_499 --> node_522
    node_231 --> node_197
    node_987 --> node_1036
    node_535 --> node_1140
    node_65 --> node_783
    node_848 --> node_1171
    node_672 --> node_1269
    node_6 --> node_406
    node_880 --> node_1293
    node_1253 --> node_1180
    node_126 --> node_243
    node_1369 --> node_1009
    node_1362 --> node_1331
    node_598 --> node_178
    node_535 --> node_1208
    node_506 --> node_1322
    node_673 --> node_1257
    node_1382 --> node_715
    node_1253 --> node_1036
    node_680 --> node_1220
    node_20 --> node_400
    node_32 --> node_1026
    node_69 --> node_124
    node_102 --> node_763
    node_66 --> node_631
    node_661 --> node_1140
    node_530 --> node_1161
    node_509 --> node_826
    node_207 --> node_1308
    node_812 --> node_712
    node_21 --> node_616
    node_552 --> node_189
    node_6 --> node_799
    node_789 --> node_338
    node_798 --> node_728
    node_535 --> node_1229
    node_255 --> node_1325
    node_456 --> node_242
    node_681 --> node_682
    node_1140 --> node_756
    node_1362 --> node_1249
    node_147 --> node_631
    node_1120 --> node_1064
    node_1337 --> node_1139
    node_631 --> node_185
    node_495 --> node_1377
    node_864 --> node_223
    node_6 --> node_353
    node_54 --> node_970
    node_548 --> node_1199
    node_530 --> node_1192
    node_609 --> node_140
    node_1385 --> node_240
    node_101 --> node_966
    node_1253 --> node_1111
    node_541 --> node_1151
    node_181 --> node_412
    node_70 --> node_68
    node_102 --> node_801
    node_588 --> node_1193
    node_959 --> node_712
    node_514 --> node_756
    node_506 --> node_1029
    node_1383 --> node_750
    node_613 --> node_25
    node_0 --> node_1089
    node_748 --> node_750
    node_60 --> node_121
    node_68 --> node_748
    node_552 --> node_193
    node_737 --> node_736
    node_1125 --> node_1325
    node_70 --> node_126
    node_553 --> node_243
    node_20 --> node_1105
    node_680 --> node_1081
    node_6 --> node_1243
    node_538 --> node_663
    node_102 --> node_235
    node_495 --> node_496
    node_1254 --> node_1156
    node_255 --> node_252
    node_712 --> node_750
    node_1254 --> node_1243
    node_552 --> node_754
    node_924 --> node_276
    node_677 --> node_1320
    node_211 --> node_311
    node_664 --> node_657
    node_880 --> node_971
    node_1353 --> node_1037
    node_680 --> node_1258
    node_788 --> node_275
    node_1065 --> node_1063
    node_6 --> node_845
    node_234 --> node_243
    node_789 --> node_933
    node_679 --> node_1386
    node_679 --> node_178
    node_6 --> node_392
    node_729 --> node_1124
    node_676 --> node_1262
    node_1076 --> node_1070
    node_1362 --> node_1082
    node_529 --> node_721
    node_1149 --> node_1150
    node_530 --> node_1280
    node_498 --> node_1303
    node_921 --> node_364
    node_957 --> node_1258
    node_6 --> node_903
    node_66 --> node_70
    node_1337 --> node_1052
    node_677 --> node_1048
    node_646 --> node_1322
    node_1125 --> node_252
    node_768 --> node_971
    node_791 --> node_271
    node_1084 --> node_13
    node_1253 --> node_1063
    node_613 --> node_783
    node_609 --> node_576
    node_678 --> node_1112
    node_1254 --> node_1332
    node_1254 --> node_1115
    node_498 --> node_1314
    node_523 --> node_191
    node_1164 --> node_1145
    node_548 --> node_1186
    node_498 --> node_277
    node_102 --> node_695
    node_676 --> node_994
    node_220 --> node_213
    node_530 --> node_1322
    node_668 --> node_178
    node_946 --> node_59
    node_66 --> node_681
    node_158 --> node_116
    node_917 --> node_271
    node_472 --> node_1105
    node_710 --> node_12
    node_1170 --> node_1284
    node_1283 --> node_373
    node_21 --> node_38
    node_864 --> node_215
    node_1120 --> node_1054
    node_607 --> node_614
    node_535 --> node_1358
    node_147 --> node_681
    node_667 --> node_180
    node_552 --> node_1171
    node_506 --> node_1385
    node_576 --> node_679
    node_535 --> node_1058
    node_1355 --> node_180
    node_1337 --> node_1255
    node_1140 --> node_199
    node_957 --> node_1036
    node_1327 --> node_1326
    node_681 --> node_673
    node_552 --> node_1166
    node_646 --> node_1029
    node_552 --> node_1070
    node_129 --> node_332
    node_144 --> node_54
    node_798 --> node_759
    node_1078 --> node_69
    node_1337 --> node_1110
    node_530 --> node_520
    node_1253 --> node_1149
    node_1362 --> node_1361
    node_571 --> node_253
    node_576 --> node_670
    node_6 --> node_537
    node_680 --> node_1256
    node_1362 --> node_1375
    node_101 --> node_664
    node_1375 --> node_1377
    node_506 --> node_992
    node_609 --> node_583
    node_552 --> node_663
    node_571 --> node_748
    node_535 --> node_1279
    node_65 --> node_1284
    node_790 --> node_36
    node_859 --> node_689
    node_602 --> node_596
    node_839 --> node_1301
    node_1190 --> node_1037
    node_1362 --> node_1234
    node_422 --> node_966
    node_858 --> node_183
    node_613 --> node_797
    node_653 --> node_682
    node_508 --> node_211
    node_103 --> node_117
    node_880 --> node_737
    node_6 --> node_1246
    node_857 --> node_257
    node_542 --> node_36
    node_712 --> node_28
    node_499 --> node_52
    node_957 --> node_1256
    node_1200 --> node_1198
    node_102 --> node_338
    node_532 --> node_243
    node_541 --> node_309
    node_1362 --> node_1235
    node_680 --> node_1240
    node_542 --> node_1172
    node_107 --> node_74
    node_661 --> node_1127
    node_1375 --> node_496
    node_666 --> node_1040
    node_1254 --> node_1221
    node_680 --> node_1371
    node_974 --> node_973
    node_660 --> node_1099
    node_0 --> node_1170
    node_1314 --> node_1285
    node_419 --> node_36
    node_614 --> node_28
    node_6 --> node_191
    node_1362 --> node_1100
    node_524 --> node_294
    node_768 --> node_737
    node_1120 --> node_1324
    node_102 --> node_1161
    node_1140 --> node_866
    node_646 --> node_180
    node_790 --> node_235
    node_287 --> node_434
    node_568 --> node_137
    node_108 --> node_58
    node_791 --> node_283
    node_857 --> node_447
    node_1253 --> node_1336
    node_1126 --> node_1288
    node_20 --> node_272
    node_791 --> node_353
    node_65 --> node_179
    node_499 --> node_551
    node_1362 --> node_1376
    node_1190 --> node_1040
    node_588 --> node_985
    node_530 --> node_758
    node_545 --> node_1226
    node_552 --> node_1008
    node_646 --> node_1385
    node_1254 --> node_1350
    node_60 --> node_748
    node_70 --> node_124
    node_498 --> node_1296
    node_1254 --> node_1335
    node_32 --> node_185
    node_679 --> node_1027
    node_680 --> node_1098
    node_530 --> node_1230
    node_552 --> node_190
    node_456 --> node_998
    node_66 --> node_728
    node_672 --> node_1264
    node_530 --> node_1385
    node_197 --> node_221
    node_21 --> node_812
    node_1100 --> node_193
    node_38 --> node_34
    node_102 --> node_933
    node_208 --> node_1285
    node_957 --> node_1038
    node_1140 --> node_229
    node_1254 --> node_1145
    node_695 --> node_694
    node_1120 --> node_1178
    node_607 --> node_1151
    node_506 --> node_1380
    node_290 --> node_1070
    node_1185 --> node_1182
    node_916 --> node_353
    node_0 --> node_1121
    node_1382 --> node_750
    node_456 --> node_497
    node_575 --> node_596
    node_6 --> node_207
    node_147 --> node_728
    node_533 --> node_242
    node_679 --> node_1079
    node_0 --> node_1059
    node_1337 --> node_1386
    node_1192 --> node_1191
    node_552 --> node_27
    node_20 --> node_387
    node_1253 --> node_1088
    node_181 --> node_367
    node_74 --> node_235
    node_498 --> node_417
    node_506 --> node_966
    node_568 --> node_84
    node_1253 --> node_1352
    node_66 --> node_989
    node_1283 --> node_1299
    node_156 --> node_145
    node_365 --> node_249
    node_1254 --> node_1080
    node_456 --> node_1044
    node_0 --> node_1164
    node_4 --> node_561
    node_530 --> node_1046
    node_613 --> node_1284
    node_530 --> node_992
    node_1126 --> node_1381
    node_766 --> node_769
    node_555 --> node_642
    node_104 --> node_1162
    node_210 --> node_245
    node_6 --> node_1052
    node_498 --> node_279
    node_574 --> node_656
    node_0 --> node_1331
    node_6 --> node_1309
    node_1337 --> node_1330
    node_147 --> node_989
    node_1254 --> node_1215
    node_429 --> node_453
    node_65 --> node_246
    node_1253 --> node_1209
    node_880 --> node_754
    node_580 --> node_1303
    node_1254 --> node_1349
    node_1362 --> node_1332
    node_1337 --> node_1355
    node_1385 --> node_193
    node_1140 --> node_429
    node_506 --> node_1180
    node_152 --> node_60
    node_1254 --> node_1179
    node_6 --> node_507
    node_1337 --> node_1367
    node_70 --> node_756
    node_506 --> node_640
    node_0 --> node_1249
    node_516 --> node_83
    node_696 --> node_704
    node_416 --> node_223
    node_859 --> node_598
    node_185 --> node_222
    node_535 --> node_1228
    node_768 --> node_754
    node_613 --> node_179
    node_1254 --> node_1047
    node_675 --> node_1030
    node_981 --> node_974
    node_1253 --> node_255
    node_231 --> node_235
    node_1150 --> node_750
    node_683 --> node_1374
    node_6 --> node_1255
    node_6 --> node_725
    node_189 --> node_281
    node_661 --> node_1135
    node_1362 --> node_1254
    node_798 --> node_737
    node_307 --> node_621
    node_1140 --> node_194
    node_646 --> node_1380
    node_552 --> node_1375
    node_498 --> node_1307
    node_117 --> node_558
    node_65 --> node_1118
    node_6 --> node_1110
    node_106 --> node_333
    node_1064 --> node_37
    node_844 --> node_1312
    node_39 --> node_43
    node_1254 --> node_1110
    node_1168 --> node_1373
    node_552 --> node_1234
    node_193 --> node_1108
    node_499 --> node_517
    node_571 --> node_240
    node_798 --> node_747
    node_281 --> node_283
    node_613 --> node_3
    node_553 --> node_66
    node_32 --> node_1236
    node_189 --> node_213
    node_456 --> node_37
    node_20 --> node_271
    node_1368 --> node_1070
    node_6 --> node_253
    node_1104 --> node_1101
    node_911 --> node_271
    node_552 --> node_1235
    node_869 --> node_1105
    node_330 --> node_1070
    node_931 --> node_244
    node_0 --> node_1082
    node_639 --> node_1257
    node_513 --> node_177
    node_207 --> node_376
    node_21 --> node_609
    node_1254 --> node_1116
    node_1253 --> node_1189
    node_552 --> node_1100
    node_6 --> node_361
    node_60 --> node_134
    node_544 --> node_16
    node_60 --> node_118
    node_555 --> node_332
    node_456 --> node_1161
    node_1284 --> node_1105
    node_680 --> node_1193
    node_506 --> node_664
    node_530 --> node_1325
    node_1323 --> node_249
    node_20 --> node_1308
    node_757 --> node_748
    node_1327 --> node_1122
    node_552 --> node_1376
    node_32 --> node_324
    node_1038 --> node_1231
    node_552 --> node_59
    node_661 --> node_1137
    node_514 --> node_1106
    node_613 --> node_246
    node_552 --> node_1377
    node_646 --> node_1180
    node_334 --> node_970
    node_70 --> node_101
    node_600 --> node_1015
    node_1244 --> node_235
    node_108 --> node_620
    node_506 --> node_1063
    node_32 --> node_1066
    node_1362 --> node_1104
    node_737 --> node_731
    node_677 --> node_1089
    node_231 --> node_211
    node_662 --> node_178
    node_232 --> node_1172
    node_905 --> node_212
    node_208 --> node_185
    node_680 --> node_1239
    node_1185 --> node_1108
    node_365 --> node_205
    node_488 --> node_411
    node_32 --> node_1020
    node_530 --> node_1146
    node_58 --> node_242
    node_1259 --> node_1258
    node_1362 --> node_1350
    node_55 --> node_71
    node_108 --> node_634
    node_6 --> node_1101
    node_613 --> node_33
    node_0 --> node_1358
    node_66 --> node_971
    node_597 --> node_371
    node_13 --> node_676
    node_1226 --> node_69
    node_516 --> node_527
    node_552 --> node_1156
    node_535 --> node_1155
    node_181 --> node_1297
    node_54 --> node_243
    node_312 --> node_336
    node_1290 --> node_1336
    node_498 --> node_405
    node_1322 --> node_584
    node_516 --> node_541
    node_6 --> node_1386
    node_231 --> node_37
    node_1170 --> node_36
    node_69 --> node_60
    node_613 --> node_1118
    node_906 --> node_360
    node_119 --> node_71
    node_532 --> node_199
    node_58 --> node_1369
    node_147 --> node_971
    node_552 --> node_425
    node_798 --> node_754
    node_0 --> node_1375
    node_899 --> node_208
    node_408 --> node_202
    node_506 --> node_1050
    node_1170 --> node_1172
    node_1382 --> node_713
    node_535 --> node_1207
    node_1146 --> node_1070
    node_885 --> node_243
    node_107 --> node_52
    node_812 --> node_810
    node_506 --> node_1149
    node_680 --> node_1190
    node_1120 --> node_1250
    node_544 --> node_37
    node_6 --> node_1319
    node_552 --> node_977
    node_1149 --> node_1147
    node_1253 --> node_1262
    node_475 --> node_1171
    node_576 --> node_36
    node_102 --> node_992
    node_1362 --> node_1080
    node_552 --> node_1115
    node_552 --> node_1332
    node_790 --> node_712
    node_498 --> node_214
    node_6 --> node_1330
    node_20 --> node_283
    node_32 --> node_631
    node_958 --> node_1159
    node_675 --> node_1032
    node_523 --> node_396
    node_639 --> node_177
    node_893 --> node_1295
    node_535 --> node_1237
    node_680 --> node_1281
    node_289 --> node_283
    node_542 --> node_712
    node_65 --> node_763
    node_1362 --> node_1057
    node_609 --> node_588
    node_69 --> node_128
    node_860 --> node_394
    node_530 --> node_1064
    node_107 --> node_71
    node_798 --> node_422
    node_486 --> node_1105
    node_615 --> node_652
    node_422 --> node_1193
    node_613 --> node_590
    node_680 --> node_1189
    node_6 --> node_1355
    node_207 --> node_1312
    node_556 --> node_69
    node_499 --> node_544
    node_995 --> node_59
    node_1126 --> node_1070
    node_4 --> node_180
    node_646 --> node_1063
    node_727 --> node_729
    node_983 --> node_979
    node_845 --> node_276
    node_521 --> node_1307
    node_1337 --> node_1089
    node_496 --> node_1105
    node_21 --> node_70
    node_126 --> node_60
    node_236 --> node_756
    node_359 --> node_648
    node_419 --> node_712
    node_1120 --> node_1065
    node_906 --> node_1294
    node_1104 --> node_1103
    node_21 --> node_231
    node_755 --> node_756
    node_552 --> node_1254
    node_1068 --> node_54
    node_581 --> node_33
    node_555 --> node_217
    node_6 --> node_1293
    node_548 --> node_1201
    node_207 --> node_1305
    node_679 --> node_1171
    node_520 --> node_255
    node_255 --> node_332
    node_1120 --> node_1068
    node_6 --> node_384
    node_535 --> node_1197
    node_104 --> node_1186
    node_464 --> node_1105
    node_101 --> node_1360
    node_65 --> node_801
    node_98 --> node_332
    node_101 --> node_985
    node_69 --> node_135
    node_530 --> node_1277
    node_1323 --> node_205
    node_254 --> node_212
    node_13 --> node_666
    node_1254 --> node_1177
    node_482 --> node_1105
    node_535 --> node_1364
    node_552 --> node_49
    node_66 --> node_737
    node_535 --> node_1141
    node_1162 --> node_64
    node_1362 --> node_1211
    node_789 --> node_418
    node_976 --> node_34
    node_1354 --> node_1260
    node_0 --> node_1372
    node_1337 --> node_1117
    node_6 --> node_240
    node_499 --> node_21
    node_535 --> node_1144
    node_1290 --> node_255
    node_1382 --> node_54
    node_108 --> node_145
    node_680 --> node_1290
    node_498 --> node_1317
    node_646 --> node_1149
    node_516 --> node_340
    node_1282 --> node_1023
    node_101 --> node_332
    node_531 --> node_294
    node_800 --> node_189
    node_530 --> node_1050
    node_102 --> node_966
    node_661 --> node_1141
    node_615 --> node_13
    node_552 --> node_756
    node_235 --> node_756
    node_552 --> node_1221
    node_1270 --> node_1070
    node_181 --> node_406
    node_1116 --> node_1070
    node_506 --> node_34
    node_506 --> node_1352
    node_1063 --> node_1062
    node_752 --> node_51
    node_571 --> node_189
    node_1362 --> node_1116
    node_679 --> node_1130
    node_32 --> node_681
    node_1120 --> node_1166
    node_683 --> node_1255
    node_498 --> node_289
    node_1064 --> node_758
    node_1100 --> node_1377
    node_21 --> node_66
    node_6 --> node_396
    node_451 --> node_250
    node_680 --> node_1262
    node_552 --> node_1104
    node_536 --> node_404
    node_1019 --> node_1070
    node_18 --> node_200
    node_1254 --> node_1253
    node_106 --> node_125
    node_65 --> node_695
    node_680 --> node_1105
    node_508 --> node_28
    node_456 --> node_758
    node_498 --> node_36
    node_613 --> node_763
    node_552 --> node_177
    node_356 --> node_409
    node_666 --> node_1033
    node_1253 --> node_497
    node_552 --> node_1350
    node_148 --> node_66
    node_1253 --> node_1346
    node_193 --> node_249
    node_108 --> node_691
    node_199 --> node_207
    node_506 --> node_1209
    node_939 --> node_215
    node_1283 --> node_223
    node_1168 --> node_1098
    node_1362 --> node_1148
    node_571 --> node_193
    node_105 --> node_634
    node_338 --> node_332
    node_1038 --> node_1070
    node_885 --> node_756
    node_535 --> node_1333
    node_881 --> node_1307
    node_1254 --> node_1259
    node_670 --> node_1030
    node_675 --> node_1033
    node_506 --> node_1348
    node_498 --> node_373
    node_108 --> node_628
    node_397 --> node_266
    node_880 --> node_179
    node_0 --> node_1176
    node_167 --> node_72
    node_933 --> node_859
    node_988 --> node_180
    node_748 --> node_311
    node_674 --> node_1232
    node_498 --> node_235
    node_764 --> node_774
    node_659 --> node_1001
    node_613 --> node_801
    node_679 --> node_1125
    node_712 --> node_311
    node_251 --> node_249
    node_1099 --> node_1288
    node_1254 --> node_1337
    node_1385 --> node_1377
    node_101 --> node_1026
    node_465 --> node_1105
    node_456 --> node_992
    node_1020 --> node_1011
    node_993 --> node_1021
    node_552 --> node_1080
    node_1337 --> node_1170
```

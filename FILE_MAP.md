# Codebase File Map

This document maps every file in the repository, their description, and utilization status.

## File List

| File Path | Status | Description | Details |
| --- | --- | --- | --- |
| `.coverage` | 🟢 Referenced | File: .coverage |  |
| `.djlint.toml` | 🟢 Referenced | File: .djlint.toml |  |
| `.gitattributes` | 🟢 Referenced | Set the default behavior, in case people don't have core.autocrlf set. |  |
| `.githooks/pre-commit` | 🟢 Referenced | bin/bash |  |
| `.github/AGENTIC_README.md` | 🟢 Referenced | Agentic Validation Loop Architecture |  |
| `.github/workflows/auto-merge.yml` | 🟢 Referenced | File: auto-merge.yml |  |
| `.github/workflows/ci.yml` | 🟢 Referenced | File: ci.yml |  |
| `.github/workflows/create-issues-from-files.yml` | 🟢 Referenced | File: create-issues-from-files.yml |  |
| `.github/workflows/jules-queue.yml` | 🟢 Referenced | File: jules-queue.yml |  |
| `.github/workflows/remote-verify.yml` | 🟢 Referenced | File: remote-verify.yml |  |
| `.github/workflows/test-cluster.yml` | 🔴 Orphan | File: test-cluster.yml |  |
| `.gitignore` | 🟢 Referenced | Ignore all log files |  |
| `.husky/pre-push` | 🔴 Orphan | File: pre-push |  |
| `.markdownlint.json` | 🟢 Referenced | File: .markdownlint.json |  |
| `.opencode/README.md` | 🟢 Referenced | OpenCode Configuration |  |
| `.opencode/opencode.json` | 🟢 Referenced | File: opencode.json |  |
| `.yamllint` | 🟢 Referenced | File: .yamllint |  |
| `AGENTS.md` | 🟢 Referenced | AGENTS.md |  |
| `LANGCHAIN_ANALYSIS.md` | 🔵 Entry Point | LangChain Analysis and Hybrid Integration Report |  |
| `LICENSE` | 🟢 Referenced | File: LICENSE |  |
| `OBSIDIAN_TODO.md` | 🔵 Entry Point | Obsidian & 3D Workflow Integration Todo List |  |
| `README.md` | 🟢 Referenced | Distributed Conversational AI Pipeline for Legacy CPU Clusters |  |
| `TODO.md` | 🟢 Referenced | TODO |  |
| `aid_e_log.txt` | 🟢 Referenced | File: aid_e_log.txt |  |
| `ansible.cfg` | 🟢 Referenced | jinja2_extensions = jinja2.ext.do |  |
| `ansible/README.md` | 🟢 Referenced | Ansible |  |
| `ansible/filter_plugins/README.md` | 🟢 Referenced | Ansible Filter Plugins |  |
| `ansible/filter_plugins/safe_flatten.py` | 🟢 Referenced | File: safe_flatten.py | **Classes:** FilterModule<br>**Functions:** safe_flatten, filters |
| `ansible/jobs/README.md` | 🟢 Referenced | Ansible Jobs |  |
| `ansible/jobs/benchmark.nomad` | 🟢 Referenced | File: benchmark.nomad |  |
| `ansible/jobs/evolve-prompt.nomad.j2` | 🟢 Referenced | File: evolve-prompt.nomad.j2 |  |
| `ansible/jobs/expert-debug.nomad` | 🟢 Referenced | This is a Jinja2 template for a complete, distributed Llama expert. |  |
| `ansible/jobs/expert.nomad.j2` | 🟢 Referenced | This Nomad job file runs the main "expert" orchestrator service. |  |
| `ansible/jobs/filebrowser.nomad.j2` | 📄 Template | File: filebrowser.nomad.j2 |  |
| `ansible/jobs/health-check.nomad.j2` | 🟢 Referenced | File: health-check.nomad.j2 |  |
| `ansible/jobs/llamacpp-batch.nomad.j2` | 🟢 Referenced | File: llamacpp-batch.nomad.j2 |  |
| `ansible/jobs/llamacpp-rpc.nomad.j2` | 🟢 Referenced | This Nomad job file creates a pool of llama.cpp rpc-server providers. |  |
| `ansible/jobs/model-benchmark.nomad.j2` | 🟢 Referenced | File: model-benchmark.nomad.j2 |  |
| `ansible/jobs/pipecatapp.nomad` | 🟢 Referenced | File: pipecatapp.nomad |  |
| `ansible/jobs/router.nomad.j2` | 🟢 Referenced | This Nomad job file runs the "router" service. |  |
| `ansible/jobs/test-runner.nomad.j2` | 🟢 Referenced | File: test-runner.nomad.j2 |  |
| `ansible/jobs/vllm.nomad.j2` | 📄 Template | File: vllm.nomad.j2 |  |
| `ansible/lint_nomad.yaml` | 🟢 Referenced | File: lint_nomad.yaml |  |
| `ansible/roles/README.md` | 🟢 Referenced | Ansible Roles |  |
| `ansible/roles/benchmark_models/tasks/benchmark_loop.yaml` | 🟢 Referenced | File: benchmark_loop.yaml |  |
| `ansible/roles/benchmark_models/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/benchmark_models/templates/model-benchmark.nomad.j2` | 🟢 Referenced | This Nomad job file runs a benchmark for a single model. |  |
| `ansible/roles/bootstrap_agent/defaults/main.yaml` | 🟢 Referenced | No default variables needed for this role. |  |
| `ansible/roles/bootstrap_agent/tasks/deploy_llama_cpp_model.yaml` | 🟢 Referenced | File: deploy_llama_cpp_model.yaml |  |
| `ansible/roles/bootstrap_agent/tasks/main.yaml` | 🟢 Referenced | tasks file for bootstrap_agent |  |
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
| `ansible/roles/docker_registry/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/docker_registry/templates/docker-registry.nomad.j2` | 🟢 Referenced | File: docker-registry.nomad.j2 |  |
| `ansible/roles/download_models/files/download_hf_repo.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** main |
| `ansible/roles/download_models/tasks/main.yaml` | 🟢 Referenced | tasks file for download_models |  |
| `ansible/roles/exo/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/exo/files/Dockerfile` | 🟢 Referenced | Install system dependencies |  |
| `ansible/roles/exo/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/exo/templates/exo.nomad.j2` | 🟢 Referenced | File: exo.nomad.j2 |  |
| `ansible/roles/forgejo/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/forgejo/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/forgejo/templates/forgejo.nomad.j2` | 🟢 Referenced | File: forgejo.nomad.j2 |  |
| `ansible/roles/gemini_cli/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/gemini_cli/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/gemini_cli/templates/gemini.nomad.j2` | 🟢 Referenced | File: gemini.nomad.j2 |  |
| `ansible/roles/headscale/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/headscale/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/headscale/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/headscale/templates/config.yaml.j2` | 🟢 Referenced | File: config.yaml.j2 |  |
| `ansible/roles/headscale/templates/headscale.service.j2` | 🟢 Referenced | File: headscale.service.j2 |  |
| `ansible/roles/heretic_tool/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/heretic_tool/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/heretic_tool/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/home_assistant/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/home_assistant/meta/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/home_assistant/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/home_assistant/templates/configuration.yaml.j2` | 🟢 Referenced | Enables the default configuration for Home Assistant |  |
| `ansible/roles/home_assistant/templates/home_assistant.nomad.j2` | 🟢 Referenced | File: home_assistant.nomad.j2 |  |
| `ansible/roles/kittentts/tasks/main.yaml` | 🟢 Referenced | This role is deprecated and will be replaced by a Piper TTS implementation. |  |
| `ansible/roles/librarian/defaults/main.yml` | 🔵 Entry Point | File: main.yml |  |
| `ansible/roles/librarian/handlers/main.yml` | 🔵 Entry Point | File: main.yml |  |
| `ansible/roles/librarian/tasks/main.yml` | 🔵 Entry Point | File: main.yml |  |
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
| `ansible/roles/memory_graph/templates/memory-graph.nomad.j2` | 🟢 Referenced | File: memory-graph.nomad.j2 |  |
| `ansible/roles/memory_service/files/app.py` | 🟢 Referenced | File: app.py | **Classes:** Event, WorkItemCreate, WorkItemUpdate, DLQItemCreate, DLQClaimRequest, DLQItemUpdate<br>**Functions:** add_event, get_events, create_work_item, list_work_items, get_work_item... |
| `ansible/roles/memory_service/files/pmm_memory.py` | 🟢 Referenced | File: pmm_memory.py | **Classes:** PMMMemory<br>**Functions:** __init__, _init_db, _get_last_hash, _calculate_hash, add_event_sync... |
| `ansible/roles/memory_service/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/memory_service/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
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
| `ansible/roles/monitoring/templates/dashboards.yaml.j2` | 🟢 Referenced | File: dashboards.yaml.j2 |  |
| `ansible/roles/monitoring/templates/datasource.yaml.j2` | 🟢 Referenced | File: datasource.yaml.j2 |  |
| `ansible/roles/monitoring/templates/grafana.nomad.j2` | 🟢 Referenced | Update stanza for reliability |  |
| `ansible/roles/monitoring/templates/memory-audit.nomad.j2` | 🟢 Referenced | File: memory-audit.nomad.j2 |  |
| `ansible/roles/monitoring/templates/mqtt-exporter.nomad.j2` | 🟢 Referenced | Update stanza for reliability |  |
| `ansible/roles/monitoring/templates/node-exporter.nomad.j2` | 🟢 Referenced | File: node-exporter.nomad.j2 |  |
| `ansible/roles/monitoring/templates/prometheus.nomad.j2` | 🟢 Referenced | Update stanza for reliability |  |
| `ansible/roles/monitoring/templates/prometheus.yml.j2` | 🟢 Referenced | File: prometheus.yml.j2 |  |
| `ansible/roles/mqtt/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/mqtt/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/mqtt/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
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
| `ansible/roles/nomad/templates/client.hcl.j2` | 🟢 Referenced | Config generated by Ansible |  |
| `ansible/roles/nomad/templates/nomad.hcl.server.j2` | 🟢 Referenced | File: nomad.hcl.server.j2 |  |
| `ansible/roles/nomad/templates/nomad.service.j2` | 🟢 Referenced | File: nomad.service.j2 |  |
| `ansible/roles/nomad/templates/nomad.sh.j2` | 🟢 Referenced | bin/sh |  |
| `ansible/roles/nomad/templates/server.hcl.j2` | 🟢 Referenced | Config generated by Ansible |  |
| `ansible/roles/openclaw/files/Dockerfile` | 🟢 Referenced | Install system dependencies (curl for integration) |  |
| `ansible/roles/openclaw/files/pipecat_skill.md` | 🟢 Referenced | Pipecat Integration Skill |  |
| `ansible/roles/openclaw/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/openclaw/templates/openclaw.nomad.j2` | 🟢 Referenced | File: openclaw.nomad.j2 |  |
| `ansible/roles/opencode/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/opencode/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/opencode/templates/opencode.nomad.j2` | 🟢 Referenced | File: opencode.nomad.j2 |  |
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
| `ansible/roles/pds/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pds/templates/pds.nomad.j2` | 🟢 Referenced | File: pds.nomad.j2 |  |
| `ansible/roles/pipecatapp/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pipecatapp/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pipecatapp/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/pipecatapp/templates/archivist.nomad.j2` | 🟢 Referenced | File: archivist.nomad.j2 |  |
| `ansible/roles/pipecatapp/templates/pipecat.env.j2` | 🟢 Referenced | bin/sh |  |
| `ansible/roles/pipecatapp/templates/pipecatapp.nomad.j2` | 🟢 Referenced | File: pipecatapp.nomad.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/coding_expert.txt.j2` | 🟢 Referenced | File: coding_expert.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/creative_expert.txt.j2` | 🟢 Referenced | File: creative_expert.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/cynic_expert.txt.j2` | 🟢 Referenced | File: cynic_expert.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/router.txt.j2` | 🟢 Referenced | File: router.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/prompts/tron_agent.txt.j2` | 🟢 Referenced | File: tron_agent.txt.j2 |  |
| `ansible/roles/pipecatapp/templates/start_pipecatapp.sh.j2` | 🟢 Referenced | bin/bash |  |
| `ansible/roles/pipecatapp/templates/workflows/default_agent_loop.yaml.j2` | 🟢 Referenced | This workflow defines a single turn of the agent's reasoning loop. |  |
| `ansible/roles/postgres/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/postgres/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/postgres/templates/postgres.nomad.j2` | 🟢 Referenced | File: postgres.nomad.j2 |  |
| `ansible/roles/power_manager/defaults/main.yaml` | 🟢 Referenced | defaults file for power_manager |  |
| `ansible/roles/power_manager/files/power_agent.py` | 🟢 Referenced | Power management agent for sleeping and waking Nomad services. | **Classes:** HealthCheckHandler<br>**Functions:** run_health_check_server, load_config, put_service_to_sleep, wake_service_up, main... |
| `ansible/roles/power_manager/files/traffic_monitor.c` | 🟢 Referenced | File: traffic_monitor.c |  |
| `ansible/roles/power_manager/handlers/main.yaml` | 🟢 Referenced | handlers file for power_manager |  |
| `ansible/roles/power_manager/tasks/main.yaml` | 🟢 Referenced | tasks file for power_manager |  |
| `ansible/roles/power_manager/templates/power-agent.service.j2` | 🟢 Referenced | File: power-agent.service.j2 |  |
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
| `ansible/roles/python_deps/files/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `ansible/roles/python_deps/meta/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/python_deps/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/semantic_router/defaults/main.yaml` | 🟢 Referenced | defaults/main.yaml |  |
| `ansible/roles/semantic_router/tasks/main.yaml` | 🟢 Referenced | tasks/main.yaml |  |
| `ansible/roles/semantic_router/templates/Dockerfile.j2` | 🟢 Referenced | Install system dependencies if needed (e.g. for building wheels) |  |
| `ansible/roles/semantic_router/templates/semantic-router.nomad.j2` | 🟢 Referenced | File: semantic-router.nomad.j2 |  |
| `ansible/roles/sunshine/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/sunshine/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/sunshine/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/sunshine/templates/sunshine.nomad.j2` | 🟢 Referenced | File: sunshine.nomad.j2 |  |
| `ansible/roles/system_deps/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/tailscale/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/term_everything/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/tool_server/Dockerfile` | 🟢 Referenced | File: Dockerfile |  |
| `ansible/roles/tool_server/app.py` | 🟢 Referenced | File: app.py | **Classes:** ToolRequest<br>**Functions:** read_health, run_tool, list_tools |
| `ansible/roles/tool_server/entrypoint.sh` | 🟢 Referenced | bin/bash |  |
| `ansible/roles/tool_server/pmm_memory.py` | 🟢 Referenced | File: pmm_memory.py | **Classes:** PMMMemory<br>**Functions:** __init__, _init_db, _get_last_hash, _calculate_hash, add_event... |
| `ansible/roles/tool_server/preload_models.py` | 🟢 Referenced | Preload models to ensure they are cached in the Docker image |  |
| `ansible/roles/tool_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
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
| `ansible/roles/tool_server/tools/shell_tool.py` | 🟢 Referenced | File: shell_tool.py | **Classes:** ShellTool<br>**Functions:** __init__, _ensure_session, execute_command |
| `ansible/roles/tool_server/tools/smol_agent_tool.py` | 🟢 Referenced | File: smol_agent_tool.py | **Classes:** SmolAgentTool, CodeAgent, LiteLLMModel<br>**Functions:** __init__, _initialize, _execute_in_sandbox, run, __init__... |
| `ansible/roles/tool_server/tools/ssh_tool.py` | 🟢 Referenced | File: ssh_tool.py | **Classes:** SSH_Tool<br>**Functions:** __init__, run_command |
| `ansible/roles/tool_server/tools/summarizer_tool.py` | 🟢 Referenced | File: summarizer_tool.py | **Classes:** SummarizerTool<br>**Functions:** __init__, get_summary |
| `ansible/roles/tool_server/tools/swarm_tool.py` | 🟢 Referenced | File: swarm_tool.py | **Classes:** SwarmTool<br>**Functions:** __init__, spawn_workers, kill_worker |
| `ansible/roles/tool_server/tools/tap_service.py` | 🟢 Referenced | File: tap_service.py | **Classes:** TapService<br>**Functions:** __init__, process_frame |
| `ansible/roles/tool_server/tools/term_everything_tool.py` | 🟢 Referenced | File: term_everything_tool.py | **Classes:** TermEverythingTool<br>**Functions:** __init__, execute |
| `ansible/roles/tool_server/tools/web_browser_tool.py` | 🟢 Referenced | Mock playwright if it's not available | **Classes:** WebBrowserTool<br>**Functions:** __init__, goto, get_page_content, get_screenshot, click... |
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
| `ansible/run_download_models.yaml` | 🟢 Referenced | File: run_download_models.yaml |  |
| `ansible/tasks/README.md` | 🟢 Referenced | Ansible Tasks |  |
| `ansible/tasks/build_pipecatapp_image.yaml` | 🟢 Referenced | File: build_pipecatapp_image.yaml |  |
| `ansible/tasks/create_expert_job.yaml` | 🟢 Referenced | File: create_expert_job.yaml |  |
| `ansible/tasks/deploy_expert_wrapper.yaml` | 🟢 Referenced | File: deploy_expert_wrapper.yaml |  |
| `ansible/tasks/deploy_model_gpu_provider.yaml` | 🟢 Referenced | File: deploy_model_gpu_provider.yaml |  |
| `bootstrap.sh` | 🟢 Referenced | Easy Bootstrap Script for Single-Node Setup  This script simplifies the process of bootstrapping th |  |
| `docker/README.md` | 🟢 Referenced | Docker |  |
| `docker/dev_container/Dockerfile` | 🟢 Referenced | Install system dependencies |  |
| `docker/memory_service/Dockerfile` | 🟢 Referenced | Install dependencies |  |
| `docs/AGENTS.md` | 🟢 Referenced | AI Agent Architectures |  |
| `docs/AI_GOVERNANCE.md` | 📄 Documentation/Asset | AI Governance & Architecture Plan |  |
| `docs/ARCHITECTURE.md` | 🟢 Referenced | Holistic Project Architecture |  |
| `docs/BENCHMARKING.MD` | 🟢 Referenced | A Guide to Benchmarking Your AI Cluster |  |
| `docs/CLAMAV_EVALUATION.md` | 📄 Documentation/Asset | ClamAV Evaluation Report |  |
| `docs/DEPLOYMENT_AND_PROFILING.md` | 🟢 Referenced | Deploying and Profiling AI Services |  |
| `docs/EVALUATION_LLMROUTER.md` | 📄 Documentation/Asset | LLMRouter Evaluation Report |  |
| `docs/FRONTEND_VERIFICATION.md` | 🟢 Referenced | Frontend Verification Instructions with Playwright |  |
| `docs/FRONTIER_AGENT_ROADMAP.md` | 📄 Documentation/Asset | Frontier Agent Roadmap |  |
| `docs/GASTOWN_TODO.md` | 📄 Documentation/Asset | Gas Town Integration Todo |  |
| `docs/GCP_GENERATIVE_AI_REVIEW.md` | 📄 Documentation/Asset | Google Cloud Platform Generative AI Review |  |
| `docs/GEMINI.md` | 🟢 Referenced | GEMINI.md |  |
| `docs/IPV6_AUDIT.md` | 📄 Documentation/Asset | IPv6 Audit Report |  |
| `docs/MCP_SERVER_SETUP.md` | 🟢 Referenced | Building an MCP Server with Service Discovery |  |
| `docs/MEMORIES.md` | 🟢 Referenced | Agent Memories |  |
| `docs/NETWORK.md` | 🟢 Referenced | Network Architecture |  |
| `docs/NIXOS_PXE_BOOT_SETUP.md` | 🟢 Referenced | NixOS-based PXE Boot Server Setup |  |
| `docs/OBSIDIAN_WORKFLOW_DESIGN.md` | 🟢 Referenced | Obsidian Workflow Design: The "Active Vault" Architecture |  |
| `docs/PERFORMANCE_OPTIMIZATION.md` | 📄 Documentation/Asset | Performance & I/O Optimization |  |
| `docs/PROJECT_SUMMARY.md` | 🟢 Referenced | Project Summary: Architecting a Responsive, Distributed Conversational AI Pipeline |  |
| `docs/PXE_BOOT_SETUP.md` | 🟢 Referenced | iPXE Boot Server Setup for Automated Debian Installation |  |
| `docs/README.md` | 🟢 Referenced | Project Documentation |  |
| `docs/REFACTOR_PROPOSAL_hybrid_architecture.md` | 🟢 Referenced | Refactoring Proposal: Hybrid / Cluster-Native Architecture |  |
| `docs/REMOTE_WORKFLOW.md` | 🟢 Referenced | Improving Your Remote Workflow with Mosh and Tmux |  |
| `docs/SCALING_TODO.md` | 📄 Documentation/Asset | Scaling Long-Running Autonomous Coding - Implementation Scope |  |
| `docs/SECURITY_AUDIT.md` | 📄 Documentation/Asset | Security Audit Log |  |
| `docs/TODO_Hybrid_Architecture.md` | 🟢 Referenced | Hybrid Architecture Implementation To-Do List |  |
| `docs/TOOL_EVALUATION.md` | 🟢 Referenced | Tool Evaluation and Strategic Direction |  |
| `docs/TROUBLESHOOTING.md` | 🟢 Referenced | Troubleshooting Guide |  |
| `docs/VLLM_PROJECT_EVALUATION.md` | 📄 Documentation/Asset | vLLM Project Evaluation |  |
| `docs/YAML_FILES_REPORT.md` | 📄 Documentation/Asset | Report on YAML Files in Root Directory |  |
| `docs/heretic_evaluation.md` | 🟢 Referenced | Heretic Repository Evaluation |  |
| `examples/README.md` | 🟢 Referenced | Examples |  |
| `examples/chat-persistent.sh` | 🟢 Referenced | bin/bash |  |
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
| `initial_state.png` | 🔴 Orphan | File: initial_state.png |  |
| `inventory.yaml` | 🟢 Referenced | This inventory is dynamically generated by update_inventory.sh |  |
| `local_inventory.ini` | 🟢 Referenced | File: local_inventory.ini |  |
| `os-image/README.md` | 🟢 Referenced | Bootable Pipecat Cluster ISO Configuration |  |
| `os-image/build_iso.sh` | 🟢 Referenced | Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster. |  |
| `os-image/config/hooks/live/01-setup-users.chroot` | 🔴 Orphan | bin/sh |  |
| `os-image/config/hooks/live/02-enable-services.chroot` | 🔴 Orphan | bin/sh |  |
| `os-image/config/includes.chroot/etc/profile.d/99-pipecat-welcome.sh` | 🔴 Orphan | Wait up to 10 seconds for an IP address |  |
| `os-image/config/includes.chroot/etc/systemd/system/multi-user.target.wants/pipecat-firstboot.service` | 🔴 Orphan | File: pipecat-firstboot.service |  |
| `os-image/config/includes.chroot/etc/systemd/system/pipecat-firstboot.service` | 🔴 Orphan | File: pipecat-firstboot.service |  |
| `os-image/config/includes.chroot/etc/systemd/system/pipecat-hostname.service` | 🟢 Referenced | File: pipecat-hostname.service |  |
| `os-image/config/includes.chroot/usr/local/bin/setup-ssh-keys.sh` | 🟢 Referenced | Fetches SSH keys from a provided GitHub username |  |
| `os-image/config/includes.installer/preseed.cfg` | 🟢 Referenced | Default Locale and Keyboard |  |
| `os-image/config/package-lists/pipecat.list.chroot` | 🔴 Orphan | File: pipecat.list.chroot |  |
| `package.json` | 🟢 Referenced | File: package.json |  |
| `paused_state.png` | 🔴 Orphan | File: paused_state.png |  |
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
| `pipecatapp/generate_real_embeddings.py` | 🔴 Orphan | File: generate_real_embeddings.py | **Functions:** get_longformer_embedding |
| `pipecatapp/integrations/__init__.py` | 🟢 Referenced | This package contains integration modules for external services (e.g., OpenClaw). |  |
| `pipecatapp/integrations/openclaw.py` | 🟢 Referenced | File: openclaw.py | **Classes:** OpenClawClient<br>**Functions:** __init__, connect, disconnect, _listen, _handle_message... |
| `pipecatapp/janitor_agent.py` | 🟢 Referenced | File: janitor_agent.py | **Classes:** JanitorAgent<br>**Functions:** __init__, discover_services, process_item, run, stop |
| `pipecatapp/judge_agent.py` | 🟢 Referenced | File: judge_agent.py | **Classes:** JudgeAgent<br>**Functions:** __init__, discover_services, initialize_tools, report_event, call_llm... |
| `pipecatapp/langchain_memory_wrappers.py` | 🔴 Orphan | File: langchain_memory_wrappers.py | **Classes:** PMMChatMessageHistory, PipecatVectorStore<br>**Functions:** __init__, messages, add_message, clear, __init__... |
| `pipecatapp/llm_clients.py` | 🟢 Referenced | File: llm_clients.py | **Classes:** ExternalLLMClient<br>**Functions:** __init__, process_text |
| `pipecatapp/manager_agent.py` | 🟢 Referenced | File: manager_agent.py | **Classes:** ManagerAgent<br>**Functions:** __init__, discover_services, call_llm, get_agent_suitability, map_phase... |
| `pipecatapp/memory.py` | 🟢 Referenced | File: memory.py | **Classes:** MemoryStore<br>**Functions:** __init__, _load_index, _load_store, _save, _init_sqlite... |
| `pipecatapp/memory_graph_service/Dockerfile` | 🟢 Referenced | Install dependencies |  |
| `pipecatapp/memory_graph_service/server.py` | 🟢 Referenced | File: server.py | **Functions:** lifespan, store_memory, create_relationship, recall_memories, search_memories |
| `pipecatapp/models.py` | 🟢 Referenced | File: models.py | **Classes:** InternalChatRequest, SystemMessageRequest<br>**Functions:** check_content_present |
| `pipecatapp/moondream_detector.py` | 🟢 Referenced | File: moondream_detector.py | **Classes:** MoondreamDetector<br>**Functions:** __init__, process_frame, get_observation |
| `pipecatapp/net_utils.py` | 🟢 Referenced | File: net_utils.py | **Functions:** ensure_ipv6_brackets, format_url, _validate_url_logic, validate_url, resolve_and_validate_url... |
| `pipecatapp/nomad_templates/immich.nomad.hcl` | 🔵 Entry Point | File: immich.nomad.hcl |  |
| `pipecatapp/nomad_templates/readeck.nomad.hcl` | 🔵 Entry Point | File: readeck.nomad.hcl |  |
| `pipecatapp/nomad_templates/uptime-kuma.nomad.hcl` | 🔵 Entry Point | File: uptime-kuma.nomad.hcl |  |
| `pipecatapp/nomad_templates/vaultwarden.nomad.hcl` | 🔵 Entry Point | File: vaultwarden.nomad.hcl |  |
| `pipecatapp/pmm_memory.py` | 🟢 Referenced | File: pmm_memory.py | **Classes:** PMMMemory<br>**Functions:** __init__, _init_db, _get_last_hash, _calculate_hash, add_event_sync... |
| `pipecatapp/pmm_memory_client.py` | 🟢 Referenced | File: pmm_memory_client.py | **Classes:** PMMMemoryClient<br>**Functions:** __init__, add_event_sync, add_event, get_events_sync, get_events... |
| `pipecatapp/prompts/coding_expert.txt` | 🟢 Referenced | File: coding_expert.txt |  |
| `pipecatapp/prompts/creative_expert.txt` | 🟢 Referenced | File: creative_expert.txt |  |
| `pipecatapp/prompts/router.txt` | 🟢 Referenced | File: router.txt |  |
| `pipecatapp/prompts/tron_agent.txt` | 🟢 Referenced | File: tron_agent.txt |  |
| `pipecatapp/quality_control.py` | 🟢 Referenced | File: quality_control.py | **Classes:** ExpectimaxAgent, CodeQualityAnalyzer<br>**Functions:** __init__, decide, __init__, analyze |
| `pipecatapp/rate_limiter.py` | 🟢 Referenced | File: rate_limiter.py | **Classes:** RateLimiter<br>**Functions:** __init__, __call__, _cleanup |
| `pipecatapp/requirements.txt` | 🟢 Referenced | File: requirements.txt |  |
| `pipecatapp/router_config.yaml` | 🟢 Referenced | File: router_config.yaml |  |
| `pipecatapp/router_train_embeddings.pt` | 🟢 Referenced | File: router_train_embeddings.pt |  |
| `pipecatapp/router_trained_model.pkl` | 🟢 Referenced | File: router_trained_model.pkl |  |
| `pipecatapp/router_training_data.csv` | 🔴 Orphan | File: router_training_data.csv |  |
| `pipecatapp/router_training_data.jsonl` | 🟢 Referenced | File: router_training_data.jsonl |  |
| `pipecatapp/secret_manager.py` | 🟢 Referenced | File: secret_manager.py | **Classes:** SecretManager<br>**Functions:** __new__, initialize_from_env, get_secret, set_secret, get_all_secrets |
| `pipecatapp/security.py` | 🟢 Referenced | File: security.py | **Functions:** redact_sensitive_data, escape_html_content, sanitize_data |
| `pipecatapp/skill_library.py` | 🟢 Referenced | File: skill_library.py | **Classes:** SkillLibrary<br>**Functions:** __init__, _init_sqlite, save_skill, search_skills, get_skill |
| `pipecatapp/start_archivist.sh` | 🟢 Referenced | bin/bash |  |
| `pipecatapp/static/cluster.html` | 🟢 Referenced | File: cluster.html |  |
| `pipecatapp/static/cluster_viz.html` | 🟢 Referenced | A-Frame |  |
| `pipecatapp/static/css/litegraph.css` | 🟢 Referenced | File: litegraph.css |  |
| `pipecatapp/static/css/styles.css` | 🟢 Referenced | sidebar { |  |
| `pipecatapp/static/index.html` | 🟢 Referenced | File: index.html |  |
| `pipecatapp/static/js/editor.js` | 🟢 Referenced | Editor logic using LiteGraph.js |  |
| `pipecatapp/static/js/litegraph.js` | 🟢 Referenced | packer version |  |
| `pipecatapp/static/js/workflow.js` | 🟢 Referenced | File: workflow.js |  |
| `pipecatapp/static/monitor.html` | 🟢 Referenced | File: monitor.html |  |
| `pipecatapp/static/terminal.js` | 🟢 Referenced | Support authenticating via API key in localStorage |  |
| `pipecatapp/static/vr_index.html` | 🟢 Referenced | A-Frame |  |
| `pipecatapp/static/workflow.html` | 🟢 Referenced | File: workflow.html |  |
| `pipecatapp/static/workflow_3d.html` | 🟢 Referenced | File: workflow_3d.html |  |
| `pipecatapp/task_supervisor.py` | 🟢 Referenced | File: task_supervisor.py | **Classes:** TaskSupervisor<br>**Functions:** __init__, start, _check_tasks |
| `pipecatapp/technician_agent.py` | 🟢 Referenced | File: technician_agent.py | **Classes:** TechnicianAgent<br>**Functions:** __init__, rehydrate_and_resume, discover_services, initialize_tools, report_event... |
| `pipecatapp/test_memory.py` | 🟢 Referenced | File: test_memory.py | **Functions:** mock_sentence_transformer, mock_faiss, test_initialization_new, test_initialization_existing, test_add... |
| `pipecatapp/test_moondream_detector.py` | 🟢 Referenced | File: test_moondream_detector.py | **Functions:** mock_torch, mock_auto_model, test_initialization, test_process_frame, test_process_frame_error... |
| `pipecatapp/test_pmm_memory.py` | 🧪 Test | File: test_pmm_memory.py | **Functions:** memory, test_dlq_lifecycle, test_dlq_filtering, test_dlq_retry_mechanics |
| `pipecatapp/test_server.py` | 🟢 Referenced | File: test_server.py |  |
| `pipecatapp/tests/test_audio_streamer.py` | 🧪 Test | File: test_audio_streamer.py | **Classes:** TestWebsocketAudioStreamer<br>**Functions:** test_websocket_audio_streamer_wav_header |
| `pipecatapp/tests/test_browser_tool_security.py` | 🧪 Test | File: test_browser_tool_security.py | **Functions:** test_ssrf_protection, test_valid_urls |
| `pipecatapp/tests/test_container_registry_tool.py` | 🧪 Test | File: test_container_registry_tool.py | **Classes:** TestContainerRegistryTool<br>**Functions:** setUp, test_discover_registry_consul_success, test_discover_registry_consul_failure, test_list_repositories_success, test_list_tags_success... |
| `pipecatapp/tests/test_cq_tool.py` | 🧪 Test | File: test_cq_tool.py | **Functions:** test_cq_query, test_cq_propose, test_cq_confirm, test_cq_flag, test_cq_reflect |
| `pipecatapp/tests/test_document_tool.py` | 🧪 Test | File: test_document_tool.py | **Classes:** TestDocumentTool<br>**Functions:** setup_method, teardown_method, test_paperless_backend_search, test_paperless_backend_get_text, test_local_backend_search_and_get_text... |
| `pipecatapp/tests/test_git_tool_security.py` | 🧪 Test | File: test_git_tool_security.py | **Classes:** TestGitToolSecurity<br>**Functions:** setup_method, test_diff_security, test_branch_security, test_checkout_security, test_merge_security... |
| `pipecatapp/tests/test_metrics_cache.py` | 🧪 Test | File: test_metrics_cache.py | **Functions:** test_metrics_caching_behavior |
| `pipecatapp/tests/test_net_utils.py` | 🧪 Test | File: test_net_utils.py | **Classes:** TestNetUtils, TestValidateUrl<br>**Functions:** test_ensure_ipv6_brackets, test_format_url, test_validate_url_public, test_validate_url_private, test_validate_url_localhost... |
| `pipecatapp/tests/test_openclaw.py` | 🧪 Test | File: test_openclaw.py | **Functions:** test_openclaw_client_handshake_and_send, test_openclaw_tool, mock_iter, mock_send |
| `pipecatapp/tests/test_piper_async.py` | 🧪 Test | File: test_piper_async.py | **Classes:** MockFrameProcessor, MockTextFrame<br>**Functions:** test_piper_tts_async_execution, side_effect_synthesize, __init__, push_frame, __init__ |
| `pipecatapp/tests/test_proxy_security.py` | 🧪 Test | File: test_proxy_security.py | **Functions:** test_proxy_headers_respected_when_configured, test_proxy_headers_ignored_when_disabled, get_ip, get_ip |
| `pipecatapp/tests/test_rag_tool.py` | 🟢 Referenced | File: test_rag_tool.py | **Classes:** MockPMMMemory<br>**Functions:** rag_tool_class, mock_memory, test_dirs, test_rag_scope_security, test_rag_filtering... |
| `pipecatapp/tests/test_rate_limiter.py` | 🟢 Referenced | File: test_rate_limiter.py | **Classes:** MockClient, MockRequest<br>**Functions:** test_rate_limiter, test_rate_limiter_cleanup, sample_endpoint |
| `pipecatapp/tests/test_security.py` | 🟢 Referenced | Ensure pipecatapp is in path | **Functions:** test_redact_openai_key, test_redact_github_key, test_redact_bearer_token, test_redact_gitlab_key, test_redact_url_credentials |
| `pipecatapp/tests/test_spec_loader_security.py` | 🧪 Test | File: test_spec_loader_security.py | **Classes:** TestSpecLoaderSecurity<br>**Functions:** setUp, test_dangerous_protocol, test_argument_injection, test_path_traversal, test_symlink_path_traversal... |
| `pipecatapp/tests/test_stt_optimization.py` | 🧪 Test | File: test_stt_optimization.py | **Classes:** MockFrameProcessor, TestFasterWhisperSTTService<br>**Functions:** __init__, push_frame, test_convert_audio_bytes_to_float_array, test_transcribe_sync_refactoring, original_logic |
| `pipecatapp/tests/test_tool_server.py` | 🧪 Test | File: test_tool_server.py | **Classes:** TestToolServer<br>**Functions:** test_run_tool_valid_auth, test_run_tool_invalid_auth, test_run_tool_missing_auth |
| `pipecatapp/tests/test_uilogger_redaction.py` | 🟢 Referenced | File: test_uilogger_redaction.py | **Classes:** MockTextFrame, MockFrameProcessor<br>**Functions:** test_uilogger_redaction_verification, __init__, __init__, push_frame, run_test |
| `pipecatapp/tests/test_web_server_unit.py` | 🧪 Test | File: test_web_server_unit.py | **Functions:** test_health_check_init, test_health_check_ready, test_web_ui_routes, test_cluster_metrics, test_active_workflows_sanitization... |
| `pipecatapp/tests/test_websocket_security.py` | 🟢 Referenced | Mock out heavy dependencies that cause timeouts during import | **Functions:** test_websocket_accepts_trusted_origin, test_websocket_rejects_untrusted_origin, test_websocket_allows_wildcard, test_websocket_default_secure_same_origin_success, test_websocket_default_secure_same_origin_failure... |
| `pipecatapp/tests/test_xss_prevention.py` | 🧪 Test | File: test_xss_prevention.py | **Functions:** test_workflow_history_xss |
| `pipecatapp/tests/test_yolo_optimization.py` | 🧪 Test | File: test_yolo_optimization.py | **Classes:** MockFrameProcessor, MockVisionImageRawFrame<br>**Functions:** test_yolo_inference_optimization, __init__, push_frame, __init__ |
| `pipecatapp/tests/workflow/test_history.py` | 🧪 Test | File: test_history.py | **Functions:** temp_db_path, test_workflow_history_init, test_workflow_history_singleton_init |
| `pipecatapp/tests/workflow/test_serialization_perf.py` | 🧪 Test | File: test_serialization_perf.py | **Classes:** NonSerializable<br>**Functions:** test_make_serializable_primitives, test_make_serializable_dict, test_make_serializable_list, test_make_serializable_nested, test_make_serializable_non_serializable... |
| `pipecatapp/tool_server.py` | 🟢 Referenced | File: tool_server.py | **Classes:** ToolRequest<br>**Functions:** run_tool, list_tools |
| `pipecatapp/tools/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/tools/ansible_tool.py` | 🟢 Referenced | File: ansible_tool.py | **Classes:** Ansible_Tool<br>**Functions:** __init__, run_playbook |
| `pipecatapp/tools/archivist_tool.py` | 🟢 Referenced | File: archivist_tool.py | **Classes:** ArchivistTool<br>**Functions:** __init__, run, __call__ |
| `pipecatapp/tools/atproto_tool.py` | 🟢 Referenced | File: atproto_tool.py | **Classes:** ATProtoTool<br>**Functions:** __init__, _get_client, send_post, get_timeline |
| `pipecatapp/tools/autoresearch_tool.py` | 🟢 Referenced | File: autoresearch_tool.py | **Classes:** AutoresearchTool, MockLLM<br>**Functions:** __init__, run, _call_llm, _extract_code, _validate_path... |
| `pipecatapp/tools/claude_clone_tool.py` | 🟢 Referenced | File: claude_clone_tool.py | **Classes:** ClaudeCloneTool<br>**Functions:** __init__, _run_command, explain, report, generate... |
| `pipecatapp/tools/cluster_status_tool.py` | 🟢 Referenced | File: cluster_status_tool.py | **Classes:** ClusterStatusTool<br>**Functions:** __init__, get_status, execute |
| `pipecatapp/tools/code_runner_tool.py` | 🟢 Referenced | File: code_runner_tool.py | **Classes:** SandboxExecutor, DockerSandboxExecutor, NomadSandboxExecutor, CodeRunnerTool<br>**Functions:** execute, __init__, execute, execute_simple_python, __init__... |
| `pipecatapp/tools/container_registry_tool.py` | 🟢 Referenced | File: container_registry_tool.py | **Classes:** ContainerRegistryTool<br>**Functions:** __init__, _validate_repository, _discover_registry, list_repositories, list_tags... |
| `pipecatapp/tools/context_upload_tool.py` | 🟢 Referenced | File: context_upload_tool.py | **Classes:** ContextUploadTool<br>**Functions:** __init__, execute, get_definition |
| `pipecatapp/tools/council_tool.py` | 🟢 Referenced | File: council_tool.py | **Classes:** CouncilTool<br>**Functions:** __init__, _discover_local_experts, _query_model, convene |
| `pipecatapp/tools/cq_tool.py` | 🟢 Referenced | File: cq_tool.py | **Classes:** CQ_Tool<br>**Functions:** __init__, cq_query, cq_propose, cq_confirm, cq_flag... |
| `pipecatapp/tools/dependency_scanner_tool.py` | 🟢 Referenced | File: dependency_scanner_tool.py | **Classes:** DependencyScannerTool<br>**Functions:** __init__, _get_latest_version, scan_package |
| `pipecatapp/tools/desktop_control_tool.py` | 🟢 Referenced | File: desktop_control_tool.py | **Classes:** DesktopControlTool<br>**Functions:** __init__, get_desktop_screenshot, click_at, type_text |
| `pipecatapp/tools/document_tool.py` | 🟢 Referenced | File: document_tool.py | **Classes:** DocumentBackend, PaperlessBackend, LocalDirectoryBackend, DocumentTool<br>**Functions:** search, get_text, __init__, search, get_text... |
| `pipecatapp/tools/experiment_tool.py` | 🟢 Referenced | File: experiment_tool.py | **Classes:** ExperimentTool<br>**Functions:** __init__, run, _validate_path, _create_snapshot, _extract_artifact... |
| `pipecatapp/tools/file_editor_tool.py` | 🟢 Referenced | File: file_editor_tool.py | **Classes:** FileEditorTool<br>**Functions:** __init__, _validate_path, _calculate_line_hash, _save_for_undo, undo_edit... |
| `pipecatapp/tools/final_answer_tool.py` | 🟢 Referenced | File: final_answer_tool.py | **Classes:** FinalAnswerTool<br>**Functions:** __init__, submit_task |
| `pipecatapp/tools/gemini_cli.py` | 🟢 Referenced | File: gemini_cli.py | **Functions:** send_message |
| `pipecatapp/tools/get_nomad_job.py` | 🟢 Referenced | File: get_nomad_job.py | **Functions:** get_nomad_job_definition, main |
| `pipecatapp/tools/git_tool.py` | 🟢 Referenced | File: git_tool.py | **Classes:** Git_Tool<br>**Functions:** __init__, _validate_path, _validate_arg, _validate_protocol, _run_git_command... |
| `pipecatapp/tools/ha_tool.py` | 🟢 Referenced | File: ha_tool.py | **Classes:** HA_Tool<br>**Functions:** __init__, call_ai_task |
| `pipecatapp/tools/heretic_tool.py` | 🟢 Referenced | File: heretic_tool.py | **Classes:** HereticTool<br>**Functions:** __init__, align_model |
| `pipecatapp/tools/langchain_adapter.py` | 🔴 Orphan | File: langchain_adapter.py | **Classes:** LangChainToolAdapter<br>**Functions:** __init__, _create_execution_method, wrapped_execute |
| `pipecatapp/tools/llxprt_code_tool.py` | 🟢 Referenced | File: llxprt_code_tool.py | **Classes:** LLxprt_Code_Tool<br>**Functions:** __init__, run |
| `pipecatapp/tools/mcp_tool.py` | 🟢 Referenced | File: mcp_tool.py | **Classes:** MCP_Tool<br>**Functions:** __init__, get_status, get_memory_summary, clear_short_term_memory |
| `pipecatapp/tools/open_workers_tool.py` | 🟢 Referenced | File: open_workers_tool.py | **Classes:** OpenWorkersTool<br>**Functions:** __init__, _get_service_url, _get_api_url, run_javascript |
| `pipecatapp/tools/openclaw_tool.py` | 🟢 Referenced | File: openclaw_tool.py | **Classes:** OpenClawTool<br>**Functions:** __init__, send_message |
| `pipecatapp/tools/opencode_tool.py` | 🟢 Referenced | File: opencode_tool.py | **Classes:** OpencodeTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/orchestrator_tool.py` | 🟢 Referenced | File: orchestrator_tool.py | **Classes:** OrchestratorTool<br>**Functions:** __init__, dispatch_job |
| `pipecatapp/tools/personality_tool.py` | 🟢 Referenced | File: personality_tool.py | **Classes:** PersonalityTool<br>**Functions:** __init__, set_personality, reset_personality, get_current_personality |
| `pipecatapp/tools/planner_tool.py` | 🟢 Referenced | File: planner_tool.py | **Classes:** PlannerTool<br>**Functions:** __init__, _discover_llm_url, _call_llm, plan_and_execute |
| `pipecatapp/tools/power_tool.py` | 🟢 Referenced | File: power_tool.py | **Classes:** Power_Tool<br>**Functions:** __init__, set_idle_threshold |
| `pipecatapp/tools/project_mapper_tool.py` | 🟢 Referenced | File: project_mapper_tool.py | **Classes:** ProjectMapperTool<br>**Functions:** __init__, _is_ignored, scan, _list_files_git, _guess_type... |
| `pipecatapp/tools/prompt_improver_tool.py` | 🟢 Referenced | File: prompt_improver_tool.py | **Classes:** PromptImproverTool<br>**Functions:** __init__, _discover_llm, _call_llm, create_prompt_plan |
| `pipecatapp/tools/rag_tool.py` | 🟢 Referenced | File: rag_tool.py | **Classes:** RAG_Tool<br>**Functions:** __init__, set_scope, _build_knowledge_base, _list_files_git, search_knowledge_base |
| `pipecatapp/tools/remote_tool_proxy.py` | 🟢 Referenced | File: remote_tool_proxy.py | **Classes:** RemoteToolProxy<br>**Functions:** __init__, __getattr__, method |
| `pipecatapp/tools/sandbox.ts` | 🟢 Referenced | sandbox.ts |  |
| `pipecatapp/tools/save_skill_tool.py` | 🟢 Referenced | File: save_skill_tool.py | **Classes:** SaveSkillTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/scale_compute_tool.py` | 🟢 Referenced | File: scale_compute_tool.py | **Classes:** ScaleComputeTool<br>**Functions:** __init__, scale, execute |
| `pipecatapp/tools/scheduler_tool.py` | 🟢 Referenced | File: scheduler_tool.py | **Classes:** SchedulerTool<br>**Functions:** __init__, _inject_message, add_cron_job, add_interval_job, list_jobs... |
| `pipecatapp/tools/search_skills_tool.py` | 🟢 Referenced | File: search_skills_tool.py | **Classes:** SearchSkillsTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/search_tool.py` | 🟢 Referenced | File: search_tool.py | **Classes:** SearchTool<br>**Functions:** __init__, _validate_path, grep, find_file |
| `pipecatapp/tools/shell_tool.py` | 🟢 Referenced | File: shell_tool.py | **Classes:** ShellTool<br>**Functions:** __init__, load_approvals, save_approval, check_command_safety, _ensure_session... |
| `pipecatapp/tools/smol_agent_tool.py` | 🟢 Referenced | File: smol_agent_tool.py | **Classes:** SmolAgentTool, CodeAgent, LiteLLMModel<br>**Functions:** __init__, _initialize, _execute_in_sandbox, run, __init__... |
| `pipecatapp/tools/spec_loader_tool.py` | 🟢 Referenced | File: spec_loader_tool.py | **Classes:** SpecLoaderTool<br>**Functions:** __init__, _validate_protocol, _validate_arg, _validate_path, _validate_repo_name... |
| `pipecatapp/tools/ssh_tool.py` | 🟢 Referenced | File: ssh_tool.py | **Classes:** SSH_Tool<br>**Functions:** __init__, run_command |
| `pipecatapp/tools/submit_solution_tool.py` | 🟢 Referenced | File: submit_solution_tool.py | **Classes:** SubmitSolutionTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/summarizer_tool.py` | 🟢 Referenced | File: summarizer_tool.py | **Classes:** SummarizerTool<br>**Functions:** __init__, get_summary |
| `pipecatapp/tools/swarm_tool.py` | 🟢 Referenced | File: swarm_tool.py | **Classes:** SwarmTool<br>**Functions:** __init__, spawn_workers, wait_for_results, kill_worker |
| `pipecatapp/tools/tap_service.py` | 🟢 Referenced | File: tap_service.py | **Classes:** TapService<br>**Functions:** __init__, process_frame |
| `pipecatapp/tools/term_everything_tool.py` | 🟢 Referenced | File: term_everything_tool.py | **Classes:** TermEverythingTool<br>**Functions:** __init__, execute |
| `pipecatapp/tools/test_git_tool.py` | 🟢 Referenced | File: test_git_tool.py | **Classes:** TestGitTool<br>**Functions:** setUp, test_ls_files, test_ls_files_integration |
| `pipecatapp/tools/test_ssh_tool.py` | 🟢 Referenced | File: test_ssh_tool.py | **Functions:** ssh_tool, test_run_command_success, test_run_command_error |
| `pipecatapp/tools/update_litellm_tool.py` | 🔴 Orphan | File: update_litellm_tool.py | **Classes:** UpdateLitellmTool<br>**Functions:** __init__, schema, fetch_releases, update_nomad_file, execute |
| `pipecatapp/tools/vr_tool.py` | 🟢 Referenced | File: vr_tool.py | **Classes:** VRTool<br>**Functions:** __init__, get_tool_def, execute |
| `pipecatapp/tools/web_browser_tool.py` | 🟢 Referenced | File: web_browser_tool.py | **Classes:** WebBrowserTool<br>**Functions:** __init__, ensure_initialized, goto, get_page_content, get_screenshot... |
| `pipecatapp/tools/wol_tool.py` | 🟢 Referenced | File: wol_tool.py | **Classes:** WOLTool<br>**Functions:** __init__, _validate_mac, wake, execute |
| `pipecatapp/train_router.py` | 🔴 Orphan | Change working directory so that llmrouter loads relative to pipecatapp |  |
| `pipecatapp/web_server.py` | 🟢 Referenced | File: web_server.py | **Classes:** SecurityHeadersMiddleware, AsyncCache, WebSocketManager<br>**Functions:** is_origin_allowed, websocket_endpoint, internal_chat, internal_chat_sync, internal_system_message... |
| `pipecatapp/worker_agent.py` | 🟢 Referenced | File: worker_agent.py | **Functions:** main_async |
| `pipecatapp/workflow/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/workflow/canvas_converter.py` | 🟢 Referenced | File: canvas_converter.py | **Classes:** CanvasConverter<br>**Functions:** canvas_to_workflow, _infer_node_type, _extract_config, workflow_to_canvas |
| `pipecatapp/workflow/context.py` | 🟢 Referenced | File: context.py | **Classes:** WorkflowContext<br>**Functions:** __init__, set_global_input, get_input, set_output, _resolve_value... |
| `pipecatapp/workflow/history.py` | 🟢 Referenced | File: history.py | **Classes:** WorkflowHistory<br>**Functions:** __new__, __init__, _init_db, save_run, get_all_runs... |
| `pipecatapp/workflow/node.py` | 🟢 Referenced | File: node.py | **Classes:** Node<br>**Functions:** __init__, execute, get_input, set_output, get_spatial_data |
| `pipecatapp/workflow/nodes/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/workflow/nodes/base_nodes.py` | 🟢 Referenced | File: base_nodes.py | **Classes:** InputNode, OutputNode, MergeNode, ConditionalBranchNode, GateNode<br>**Functions:** execute, execute, execute, execute, execute |
| `pipecatapp/workflow/nodes/emperor_nodes.py` | 🟢 Referenced | File: emperor_nodes.py | **Classes:** EmperorAgentNode<br>**Functions:** resolve_abs_path, read_file_tool, list_files_tool, edit_file_tool, shell_tool... |
| `pipecatapp/workflow/nodes/langchain_nodes.py` | 🔴 Orphan | File: langchain_nodes.py | **Classes:** LangGraphNode<br>**Functions:** execute |
| `pipecatapp/workflow/nodes/llm_nodes.py` | 🟢 Referenced | File: llm_nodes.py | **Classes:** VisionLLMNode, PromptBuilderNode, SimpleLLMNode, ExpertRouterNode, ExternalLLMNode, LLMRouterNode, LoopedReasoningNode<br>**Functions:** discover_main_llm_service, execute, execute, execute, execute... |
| `pipecatapp/workflow/nodes/registry.py` | 🟢 Referenced | File: registry.py | **Classes:** NodeRegistry<br>**Functions:** __init__, register, get_node_class |
| `pipecatapp/workflow/nodes/system_nodes.py` | 🟢 Referenced | File: system_nodes.py | **Classes:** ConsulServiceDiscoveryNode, FileReadNode<br>**Functions:** execute, execute |
| `pipecatapp/workflow/nodes/tool_nodes.py` | 🟢 Referenced | File: tool_nodes.py | **Classes:** SystemPromptNode, ScreenshotNode, ToolParserNode, ToolExecutorNode<br>**Functions:** execute, execute, execute, execute |
| `pipecatapp/workflow/runner.py` | 🟢 Referenced | File: runner.py | **Classes:** ActiveWorkflows, OpenGates, WorkflowRunner<br>**Functions:** make_serializable, _safe_context_to_dict, _save_run_background, __new__, add_runner... |
| `pipecatapp/workflows/adversarial_simulation.yaml` | 🟢 Referenced | File: adversarial_simulation.yaml |  |
| `pipecatapp/workflows/deep_context.yaml` | 🟢 Referenced | File: deep_context.yaml |  |
| `pipecatapp/workflows/default_agent_loop.yaml` | 🟢 Referenced | File: default_agent_loop.yaml |  |
| `pipecatapp/workflows/looped_reasoning.yaml` | 📄 Workflow Config | File: looped_reasoning.yaml |  |
| `pipecatapp/workflows/manager.yaml` | 🟢 Referenced | File: manager.yaml |  |
| `pipecatapp/workflows/poc_ensemble.yaml` | 🟢 Referenced | File: poc_ensemble.yaml |  |
| `pipecatapp/workflows/sandbox.yaml` | 🟢 Referenced | File: sandbox.yaml |  |
| `pipecatapp/workflows/tiered_agent_loop.yaml` | 📄 Workflow Config | File: tiered_agent_loop.yaml |  |
| `pipecatapp/workflows/update_litellm_workflow.yaml` | 📄 Workflow Config | File: update_litellm_workflow.yaml |  |
| `plan.md` | 🔵 Entry Point | File: plan.md |  |
| `playbook.yaml` | 🟢 Referenced | File: playbook.yaml |  |
| `playbooks/README.md` | 🟢 Referenced | Ansible Playbooks |  |
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
| `playbooks/diagnose_and_log_home_assistant.yaml` | 🟢 Referenced | File: diagnose_and_log_home_assistant.yaml |  |
| `playbooks/diagnose_failure.yaml` | 🟢 Referenced | File: diagnose_failure.yaml |  |
| `playbooks/diagnose_home_assistant.yaml` | 🟢 Referenced | File: diagnose_home_assistant.yaml |  |
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
| `playbooks/run_ha_diag.yaml` | 🟢 Referenced | File: run_ha_diag.yaml |  |
| `playbooks/run_health_check.yaml` | 🟢 Referenced | File: run_health_check.yaml |  |
| `playbooks/services/README.md` | 🟢 Referenced | Ansible Service Playbooks |  |
| `playbooks/services/ai_experts.yaml` | 🟢 Referenced | File: ai_experts.yaml |  |
| `playbooks/services/app_services.yaml` | 🟢 Referenced | File: app_services.yaml |  |
| `playbooks/services/consul.yaml` | 🟢 Referenced | File: consul.yaml |  |
| `playbooks/services/core_ai_services.yaml` | 🟢 Referenced | File: core_ai_services.yaml |  |
| `playbooks/services/core_infra.yaml` | 🟢 Referenced | File: core_infra.yaml |  |
| `playbooks/services/distributed_compute.yaml` | 🟢 Referenced | Default variables can be overridden in inventory/group_vars |  |
| `playbooks/services/docker.yaml` | 🟢 Referenced | File: docker.yaml |  |
| `playbooks/services/final_verification.yaml` | 🟢 Referenced | File: final_verification.yaml |  |
| `playbooks/services/model_services.yaml` | 🟢 Referenced | File: model_services.yaml |  |
| `playbooks/services/monitoring.yaml` | 🟢 Referenced | File: monitoring.yaml |  |
| `playbooks/services/nomad.yaml` | 🟢 Referenced | File: nomad.yaml |  |
| `playbooks/services/nomad_client.yaml` | 🟢 Referenced | File: nomad_client.yaml |  |
| `playbooks/services/registry.yaml` | 🟢 Referenced | File: registry.yaml |  |
| `playbooks/services/streaming_services.yaml` | 🟢 Referenced | File: streaming_services.yaml |  |
| `playbooks/services/tasks/diagnose_home_assistant.yaml` | 🟢 Referenced | File: diagnose_home_assistant.yaml |  |
| `playbooks/services/training_services.yaml` | 🟢 Referenced | File: training_services.yaml |  |
| `playbooks/status-check.yaml` | 🟢 Referenced | File: status-check.yaml |  |
| `playbooks/wake.yaml` | 🟢 Referenced | File: wake.yaml |  |
| `playbooks/worker.yaml` | 🟢 Referenced | File: worker.yaml |  |
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
| `prompt_engineering/challenger.py` | 🟢 Referenced | File: challenger.py | **Classes:** Challenger<br>**Functions:** __init__, generate_challenge |
| `prompt_engineering/create_evaluator.py` | 🟢 Referenced | The template is based on the one defined in prompt_engineering/agents/EVALUATOR_GENERATOR.md | **Functions:** main |
| `prompt_engineering/evaluation_lib.py` | 🟢 Referenced | This file will contain the reusable functions for evaluating code. | **Functions:** render_nomad_job, wait_for_service_healthy, get_test_results, cleanup |
| `prompt_engineering/evaluation_suite/README.md` | 🟢 Referenced | Evaluation Suite |  |
| `prompt_engineering/evaluation_suite/test_vision.yaml` | 🟢 Referenced | File: test_vision.yaml |  |
| `prompt_engineering/evaluator.py` | 🟢 Referenced | File: evaluator.py | **Functions:** evaluate_code |
| `prompt_engineering/evolve.py` | 🟢 Referenced | File: evolve.py | **Functions:** load_archive_metadata, select_parent, select_parent_from_archive, run_evolution, get_fitness_score... |
| `prompt_engineering/frontend/app.js` | 🟢 Referenced | Frontend logic for Campaign Analysis UI |  |
| `prompt_engineering/frontend/index.html` | 🟢 Referenced | File: index.html |  |
| `prompt_engineering/frontend/server.py` | 🟢 Referenced | File: server.py | **Functions:** serve_index, get_evolutionary_tree |
| `prompt_engineering/frontend/style.css` | 🟢 Referenced | File: style.css |  |
| `prompt_engineering/generated_evaluators/.gitignore` | 🟢 Referenced | Ignore all files in this directory |  |
| `prompt_engineering/promote_agent.py` | 🟢 Referenced | File: promote_agent.py | **Functions:** find_best_agent, promote_agent, _perform_promotion |
| `prompt_engineering/requirements-dev.txt` | 🟢 Referenced | File: requirements-dev.txt |  |
| `prompt_engineering/run_campaign.py` | 🟢 Referenced | File: run_campaign.py | **Functions:** run_campaign, analyze_archive, _generate_report |
| `prompt_engineering/visualize_archive.py` | 🟢 Referenced | File: visualize_archive.py | **Functions:** visualize_archive, get_color_for_fitness, _save_graph |
| `prompts/README.md` | 🟢 Referenced | Prompts |  |
| `prompts/chat-with-bob.txt` | 🟢 Referenced | File: chat-with-bob.txt |  |
| `prompts/router.txt` | 🟢 Referenced | File: router.txt |  |
| `pytest.ini` | 🟢 Referenced | File: pytest.ini |  |
| `reflection/README.md` | 🟢 Referenced | Reflection |  |
| `reflection/adaptation_manager.py` | 🟢 Referenced | File: adaptation_manager.py | **Functions:** generate_test_case, main |
| `reflection/create_reflection.py` | 🟢 Referenced | File: create_reflection.py | **Functions:** create_reflection |
| `reflection/reflect.py` | 🟢 Referenced | File: reflect.py | **Functions:** load_llm_config, call_openai_llm, run_tool, analyze_failure_with_llm, main |
| `requirements-dev.txt` | 🟢 Referenced | File: requirements-dev.txt |  |
| `review_report.md` | 🔵 Entry Point | Project Review Report |  |
| `run_emperor_test.sh` | 🔵 Entry Point | bin/bash |  |
| `run_test.py` | 🟢 Referenced | File: run_test.py |  |
| `scripts/README.md` | 🟢 Referenced | `scripts/` Directory Overview |  |
| `scripts/agentic_workflow.sh` | 🟢 Referenced | --- Configuration --- |  |
| `scripts/analyze_nomad_allocs.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** format_timestamp, analyze_allocs |
| `scripts/ansible_diff.sh` | 🟢 Referenced | A script to compare Ansible playbook runs to detect changes over time. It establishes a baseline fro |  |
| `scripts/check_all_playbooks.sh` | 🟢 Referenced | --- Flexible Ansible Playbook Checker  This script recursively finds all .yaml and .yml files, filte |  |
| `scripts/check_deps.py` | 🟢 Referenced | Write the requirements to a temp file | **Functions:** check_versions |
| `scripts/ci_ansible_check.sh` | 🟢 Referenced | A CI/CD-friendly script to check for unintended changes in Ansible playbooks.  - It compares the pla |  |
| `scripts/cleanup.sh` | 🟢 Referenced | Cleanup script to free up disk space on the host machine. This script aggressively cleans Docker re |  |
| `scripts/compare_exo_llama.py` | 🔵 Entry Point | File: compare_exo_llama.py | **Functions:** print_color, check_health, run_inference, main |
| `scripts/create_assistant_prompts.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** generate_prompts |
| `scripts/create_cynic_model.sh` | 🔵 Entry Point | bin/bash |  |
| `scripts/create_todo_issues.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/debug/README.md` | 🟢 Referenced | Debug Scripts |  |
| `scripts/debug/test_mqtt_connection.py` | 🟢 Referenced | File: test_mqtt_connection.py | **Functions:** get_ip_addresses, check_port, main |
| `scripts/debug_expert.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/debug_mesh.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/evaluate_clamav.py` | 🟢 Referenced | File: evaluate_clamav.py | **Functions:** setup_test_files, run_scan, analyze_results |
| `scripts/fix_markdown.sh` | 🟢 Referenced | Automatic Markdown Linter Fixer  This script uses markdownlint-cli's --fix option to automatically |  |
| `scripts/fix_verification_failures.sh` | 🟢 Referenced | Scripts to help remediate failures reported by verify_components.py |  |
| `scripts/fix_yaml.sh` | 🟢 Referenced | Automatic YAML Linter Fixer  This script automatically fixes common, repetitive style issues report |  |
| `scripts/generate_assistant_vectors.sh` | 🔵 Entry Point | bin/bash |  |
| `scripts/generate_file_map.py` | 🔵 Entry Point | usr/bin/env python3 | **Functions:** get_rel_path, is_ignored, extract_python_info, extract_shell_info, extract_generic_desc... |
| `scripts/generate_issue_script.py` | 🟢 Referenced | File: generate_issue_script.py | **Functions:** parse_todo_file, create_issue_script |
| `scripts/generate_signatures.py` | 🔵 Entry Point | File: generate_signatures.py | **Functions:** to_hex, create_ldb_sig |
| `scripts/heal_cluster.sh` | 🟢 Referenced | Wrapper script to run the cluster healing playbook. This ensures core infrastructure (LlamaRPC, Pip |  |
| `scripts/healer.py` | 🟢 Referenced | File: healer.py | **Classes:** NomadWatcher, HealerAgent<br>**Functions:** run_local_mode, main, __init__, get_failed_allocs, get_logs... |
| `scripts/lint.sh` | 🟢 Referenced | Unified Linting Script  This script runs a series of linters to ensure code quality and consistency |  |
| `scripts/lint_exclude.txt` | 🟢 Referenced | Exclude problematic files from the linting process. |  |
| `scripts/memory_audit.py` | 🟢 Referenced | File: memory_audit.py | **Functions:** get_prometheus_metrics, get_job_spec, update_job_memory, main |
| `scripts/profile_resources.sh` | 🟢 Referenced | Profile resources usage and alignment of AI experts and models. |  |
| `scripts/provisioning.py` | 🟢 Referenced | Provisioning Script for Hybrid Architecture. | **Classes:** Colors<br>**Functions:** print_warning, print_error, print_header, print_task_header, load_playbooks_from_manifest... |
| `scripts/prune_consul_services.py` | 🟢 Referenced | Prune Stale Critical Services from Consul | **Functions:** get_consul_token, consul_request, main |
| `scripts/run_quibbler.sh` | 🟢 Referenced | A wrapper script to run quibbler for code review. Check for required arguments |  |
| `scripts/run_tests.sh` | 🟢 Referenced | usr/bin/env bash |  |
| `scripts/salvage_task.py` | 🔵 Entry Point | File: salvage_task.py | **Functions:** find_stalled_tasks, extract_partial_work, synthesize_summary, create_re_injection_prompt, main |
| `scripts/setup_pxe_server.sh` | 🔵 Entry Point | bin/bash |  |
| `scripts/start_services.sh` | 🟢 Referenced | This script is a legacy utility for manually starting services. ⚠️  DEPRECATED: Please use Ansible t |  |
| `scripts/supervisor.py` | 🟢 Referenced | File: supervisor.py | **Functions:** load_llm_config, run_playbook, run_script, cleanup_files, main |
| `scripts/test_playbooks_dry_run.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/test_playbooks_live_run.sh` | 🟢 Referenced | bin/bash |  |
| `scripts/test_swarm_map_reduce.py` | 🔵 Entry Point | File: test_swarm_map_reduce.py | **Classes:** MockMemoryClient<br>**Functions:** test_swarm_map_reduce, __init__, get_events, add_event, get_agent_stats... |
| `scripts/troubleshoot.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** get_consul_token, run_command, get_nomad_allocations, section, main |
| `scripts/uninstall.sh` | 🟢 Referenced | This script uninstalls all software and reverts all changes made by the playbook. |  |
| `scripts/verify_consul_attributes.sh` | 🔵 Entry Point | bin/bash |  |
| `test_autoresearch.py` | 🧪 Test | File: test_autoresearch.py | **Classes:** MockLLM<br>**Functions:** main, generate |
| `test_clamav_playbook.yml` | 🧪 Test | File: test_clamav_playbook.yml |  |
| `test_db.sqlite-shm` | 🧪 Test | File: test_db.sqlite-shm |  |
| `test_db.sqlite-wal` | 🧪 Test | File: test_db.sqlite-wal |  |
| `test_dlq.db-shm` | 🧪 Test | File: test_dlq.db-shm |  |
| `test_dlq.db-wal` | 🧪 Test | File: test_dlq.db-wal |  |
| `test_playbook.yml` | 🧪 Test | File: test_playbook.yml |  |
| `test_script.py` | 🧪 Test | File: test_script.py |  |
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
| `tests/integration/roles/test_home_assistant/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `tests/integration/stub_services.py` | 🟢 Referenced | File: stub_services.py | **Classes:** StubOutputService<br>**Functions:** __init__, process_frame, wait_for_frame |
| `tests/integration/test_consul_role.yaml` | 🟢 Referenced | File: test_consul_role.yaml |  |
| `tests/integration/test_home_assistant.yaml` | 🟢 Referenced | File: test_home_assistant.yaml |  |
| `tests/integration/test_mini_pipeline.py` | 🧪 Test | File: test_mini_pipeline.py | **Classes:** MockListAudioSource<br>**Functions:** test_stt_mini_pipeline, __init__, start |
| `tests/integration/test_mqtt_exporter.py` | 🧪 Test | File: test_mqtt_exporter.py | **Classes:** TestMqttExporter<br>**Functions:** setUpClass, setUp, tearDown, cleanup, test_metrics_collection |
| `tests/integration/test_nomad_role.yaml` | 🟢 Referenced | File: test_nomad_role.yaml |  |
| `tests/integration/test_pipecat_app.py` | 🟢 Referenced | File: test_pipecat_app.py | **Classes:** TestPipecatApp<br>**Functions:** setUp, test_health_check_eventually_healthy, test_main_page_loads |
| `tests/integration/test_preemption.py` | 🟢 Referenced | File: test_preemption.py | **Classes:** TestPreemption<br>**Functions:** setUp, tearDown, test_preemption |
| `tests/playbooks/e2e-tests.yaml` | 🟢 Referenced | File: e2e-tests.yaml |  |
| `tests/playbooks/test_consul.yaml` | 🧪 Test | File: test_consul.yaml |  |
| `tests/playbooks/test_llama_cpp.yaml` | 🧪 Test | File: test_llama_cpp.yaml |  |
| `tests/playbooks/test_nomad.yaml` | 🧪 Test | File: test_nomad.yaml |  |
| `tests/scripts/run_unit_tests.sh` | 🟢 Referenced | usr/bin/env bash |  |
| `tests/scripts/test_duplicate_role_execution.sh` | 🧪 Test | Test to verify that the bootstrap_agent role is not run twice using static analysis.  Move to the p |  |
| `tests/scripts/test_paddler.sh` | 🧪 Test | test_paddler.sh  This script performs basic tests to verify that Paddler (agent and balancer) is fun |  |
| `tests/scripts/test_piper.sh` | 🧪 Test | File: test_piper.sh |  |
| `tests/scripts/test_run.sh` | 🧪 Test | Start a new chat |  |
| `tests/scripts/verify_components.py` | 🟢 Referenced | usr/bin/env python3 | **Functions:** run_command, verify_systemd_service, verify_nomad_job, verify_file_exists, verify_command_available... |
| `tests/test.wav` | 🟢 Referenced | File: test.wav |  |
| `tests/test_agent_patterns.py` | 🧪 Test | File: test_agent_patterns.py | **Functions:** test_manager_agent_map_reduce, test_durable_technician |
| `tests/test_canvas_integration.py` | 🧪 Test | File: test_canvas_integration.py | **Classes:** TestCanvasIntegration, ConcreteNode<br>**Functions:** test_node_schema_3d, test_canvas_to_workflow, test_workflow_to_canvas, execute |
| `tests/test_deep_context.py` | 🧪 Test | File: test_deep_context.py | **Classes:** MockSimpleLLMNode, MaliciousTestNode, SiblingAttackNode<br>**Functions:** test_deep_context_workflow, execute, get_input, get_input |
| `tests/test_emperor_node.py` | 🟢 Referenced | File: test_emperor_node.py | **Functions:** test_emperor_node |
| `tests/test_event_bus.py` | 🧪 Test | File: test_event_bus.py | **Functions:** run_server, test_event_bus_flow |
| `tests/test_experiment_tool.py` | 🧪 Test | File: test_experiment_tool.py | **Functions:** test_experiment_tool_flow, mock_get |
| `tests/test_gastown_judge.py` | 🧪 Test | File: test_gastown_judge.py | **Functions:** test_gastown_judge |
| `tests/test_gastown_memory.py` | 🧪 Test | File: test_gastown_memory.py | **Functions:** test_gastown_memory |
| `tests/test_gastown_stats.py` | 🧪 Test | File: test_gastown_stats.py | **Functions:** test_gastown_stats |
| `tests/test_imports.py` | 🧪 Test | Add files dir to path |  |
| `tests/test_manager_flow.py` | 🧪 Test | File: test_manager_flow.py | **Classes:** MockSwarmTool, TestManagerFlow<br>**Functions:** run_server, mock_technician_task, spawn_workers, test_flow, mock_map... |
| `tests/test_spec_loader.py` | 🧪 Test | File: test_spec_loader.py | **Classes:** TestSpecLoader<br>**Functions:** setUp, tearDown, test_clone_new_repo, test_list_specs, test_scan_files_recursive... |
| `tests/test_ssrf_validation.py` | 🟢 Referenced | File: test_ssrf_validation.py | **Functions:** test_validate_url_safe, test_validate_url_unsafe_ip, test_validate_url_unsafe_scheme, test_allowlist |
| `tests/test_websocket_security.py` | 🟢 Referenced | File: test_websocket_security.py | **Functions:** test_websocket_ssrf_vulnerability |
| `tests/unit/README.md` | 🟢 Referenced | Unit Tests |  |
| `tests/unit/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `tests/unit/conftest.py` | 🟢 Referenced | List of modules to mock if they are missing in the test environment | **Functions:** mock_module_if_missing |
| `tests/unit/test_adaptation_manager.py` | 🟢 Referenced | File: test_adaptation_manager.py | **Classes:** TestAdaptationManager<br>**Functions:** test_import, test_main_flow |
| `tests/unit/test_agent_definitions.py` | 🟢 Referenced | Define the path to the agent definitions directory | **Functions:** parse_and_validate_agent_def, test_agent_definition_schema |
| `tests/unit/test_ansible_tool.py` | 🟢 Referenced | File: test_ansible_tool.py | **Functions:** test_ansible_tool_instantiation, test_run_playbook_success, test_run_playbook_with_args, test_run_playbook_failure, test_run_playbook_not_found... |
| `tests/unit/test_archivist_tool.py` | 🧪 Test | File: test_archivist_tool.py | **Functions:** test_archivist_tool_initialization, test_run_success, test_run_error_status, test_run_connection_failure |
| `tests/unit/test_audio_download_limit.py` | 🧪 Test | File: test_audio_download_limit.py | **Classes:** MockStream, MockClient, MockStreamSmall, MockClientSmall<br>**Functions:** test_download_limit_exceeded, test_download_within_limit, endless_stream, download_audio_safe, download_audio_safe... |
| `tests/unit/test_autoresearch_tool.py` | 🧪 Test | File: test_autoresearch_tool.py | **Functions:** test_autoresearch_tool_run, mock_eval |
| `tests/unit/test_autoresearch_tool_pathing.py` | 🧪 Test | File: test_autoresearch_tool_pathing.py | **Functions:** test_autoresearch_tool_pathing, mock_eval |
| `tests/unit/test_claude_clone_tool.py` | 🟢 Referenced | File: test_claude_clone_tool.py | **Functions:** test_explain_success, test_command_failure, test_directory_not_found, test_cli_not_found |
| `tests/unit/test_code_runner_security.py` | 🧪 Test | File: test_code_runner_security.py | **Functions:** test_code_runner_length_limit, test_code_runner_length_limit_ok |
| `tests/unit/test_code_runner_timeout.py` | 🧪 Test | File: test_code_runner_timeout.py | **Functions:** test_execution_timeout_logic |
| `tests/unit/test_code_runner_tool.py` | 🟢 Referenced | File: test_code_runner_tool.py | **Functions:** code_runner, test_run_code_in_sandbox_success, test_run_python_code_success, test_run_python_code_no_docker_client |
| `tests/unit/test_container_registry_security.py` | 🧪 Test | File: test_container_registry_security.py | **Classes:** TestContainerRegistrySecurity<br>**Functions:** setUp, test_list_tags_path_traversal, test_search_images_blocks_invalid_repos, test_list_tags_valid |
| `tests/unit/test_council_tool.py` | 🧪 Test | File: test_council_tool.py | **Classes:** MockTwinService<br>**Functions:** council_tool, test_discover_local_experts, test_convene_council_no_experts, test_query_model_success, test_convene_council_full_flow... |
| `tests/unit/test_dependency_scanner.py` | 🧪 Test | File: test_dependency_scanner.py | **Classes:** TestDependencyScanner<br>**Functions:** setUp, test_scan_safe_package, test_scan_vulnerable_package, test_code_runner_blocks_unsafe_lib, test_code_runner_allows_safe_lib |
| `tests/unit/test_desktop_control_tool.py` | 🟢 Referenced | File: test_desktop_control_tool.py | **Functions:** tool, mock_pyautogui, test_get_desktop_screenshot, test_click_at, test_type_text... |
| `tests/unit/test_experiment_tool_security.py` | 🧪 Test | File: test_experiment_tool_security.py | **Classes:** TestExperimentToolSecurity<br>**Functions:** setUp, tearDown, _mock_exists, test_command_injection_prevention, test_valid_command_execution... |
| `tests/unit/test_file_editor_security.py` | 🧪 Test | File: test_file_editor_security.py | **Classes:** TestFileEditorSecurity<br>**Functions:** setUp, tearDown, test_read_file_outside_root, test_write_file_outside_root, test_apply_patch_outside_root... |
| `tests/unit/test_file_editor_tool.py` | 🧪 Test | File: test_file_editor_tool.py | **Classes:** TestFileEditorTool<br>**Functions:** setUp, tearDown, test_read_file, test_write_file, test_apply_patch... |
| `tests/unit/test_final_answer_tool.py` | 🧪 Test | Add the tools directory to the python path | **Functions:** test_final_answer_tool_initialization, test_submit_task |
| `tests/unit/test_gemini_cli.py` | 🟢 Referenced | File: test_gemini_cli.py | **Functions:** test_gemini_cli_interaction, mock_server_handler |
| `tests/unit/test_get_nomad_job.py` | 🧪 Test | File: test_get_nomad_job.py | **Functions:** test_get_nomad_job_definition_success, test_get_nomad_job_definition_failure, test_get_nomad_job_definition_invalid_id |
| `tests/unit/test_git_tool.py` | 🟢 Referenced | File: test_git_tool.py | **Functions:** git_tool, test_clone_successful, test_pull_successful, test_push_successful, test_commit_successful... |
| `tests/unit/test_git_tool_security.py` | 🧪 Test | File: test_git_tool_security.py | **Classes:** TestGitToolSecurity<br>**Functions:** setUp, test_allowed_protocols, test_blocked_protocols, test_clone_with_dangerous_protocol |
| `tests/unit/test_ha_tool.py` | 🧪 Test | File: test_ha_tool.py | **Functions:** test_init_success, test_init_failure, test_call_ai_task_success, test_call_ai_task_failure |
| `tests/unit/test_hashline_editor.py` | 🧪 Test | File: test_hashline_editor.py | **Classes:** TestHashlineEditor<br>**Functions:** setUp, tearDown, get_hash, test_read_with_hashlines, test_apply_hash_edits_replace... |
| `tests/unit/test_heretic_tool.py` | 🧪 Test | File: test_heretic_tool.py | **Functions:** test_heretic_tool_align_model |
| `tests/unit/test_home_assistant_template.py` | 🟢 Referenced | File: test_home_assistant_template.py | **Functions:** test_home_assistant_template |
| `tests/unit/test_infrastructure.py` | 🧪 Test | File: test_infrastructure.py | **Classes:** TestInfrastructure<br>**Functions:** test_consul_running, test_nomad_running |
| `tests/unit/test_lint_script.py` | 🟢 Referenced | File: test_lint_script.py | **Classes:** TestLintScript<br>**Functions:** setUp, tearDown, test_lint_script |
| `tests/unit/test_llxprt_code_tool.py` | 🟢 Referenced | File: test_llxprt_code_tool.py | **Functions:** llxprt_tool, test_run_success, test_run_with_args_success, test_run_failure, test_run_timeout... |
| `tests/unit/test_looped_reasoning_node.py` | 🧪 Test | File: test_looped_reasoning_node.py | **Classes:** MockWorkflowContext<br>**Functions:** test_looped_reasoning_execution, __init__, get_input, set_output |
| `tests/unit/test_mcp_tool.py` | 🟢 Referenced | File: test_mcp_tool.py | **Functions:** mcp_tool, test_get_status_with_running_pipelines, test_get_status_with_no_pipelines, test_get_status_with_no_runner, test_get_memory_summary... |
| `tests/unit/test_memory.py` | 🟢 Referenced | File: test_memory.py | **Functions:** temp_store_file, temp_index_file, mock_embedding_model, mock_faiss_index, test_unencrypted_memory_store... |
| `tests/unit/test_mqtt_template.py` | 🧪 Test | File: test_mqtt_template.py | **Functions:** test_mqtt_template |
| `tests/unit/test_nomad_sandbox.py` | 🧪 Test | File: test_nomad_sandbox.py | **Functions:** nomad_executor, test_nomad_execution_success, test_nomad_template_injection_prevention, test_hybrid_mode_logic, test_docker_mode_logic |
| `tests/unit/test_open_workers_tool.py` | 🧪 Test | File: test_open_workers_tool.py | **Classes:** TestOpenWorkersTool<br>**Functions:** setUp, test_run_javascript_full_discovery |
| `tests/unit/test_opencode_tool.py` | 🧪 Test | File: test_opencode_tool.py | **Classes:** TestOpencodeTool<br>**Functions:** setUp, test_run_success, test_run_error |
| `tests/unit/test_orchestrator_tool.py` | 🧪 Test | File: test_orchestrator_tool.py | **Functions:** test_orchestrator_tool_instantiation, test_dispatch_job_success, test_dispatch_job_failure |
| `tests/unit/test_personality_tool.py` | 🧪 Test | File: test_personality_tool.py | **Functions:** test_set_personality, test_reset_personality, test_get_current_personality |
| `tests/unit/test_pipecat_app_unit.py` | 🟢 Referenced | File: test_pipecat_app_unit.py | **Classes:** MockFrameProcessor, MockTranscriptionFrame<br>**Functions:** client, test_read_main, test_health_check, test_workflow_runner_loads_definition, test_health_check_is_healthy... |
| `tests/unit/test_planner_tool.py` | 🧪 Test | File: test_planner_tool.py | **Functions:** mock_twin_service, planner_tool, test_discover_llm_url_router_llm, test_discover_llm_url_fallback, test_discover_llm_url_env_var... |
| `tests/unit/test_playbook_integration.py` | 🟢 Referenced | File: test_playbook_integration.py | **Functions:** test_playbook_integration_syntax_check |
| `tests/unit/test_poc_ensemble.py` | 🧪 Test | File: test_poc_ensemble.py | **Classes:** TestPoCEnsemble<br>**Functions:** setUp, test_workflow_execution, mock_post, mock_get, run_workflow |
| `tests/unit/test_power_tool.py` | 🟢 Referenced | File: test_power_tool.py | **Functions:** power_tool, test_set_idle_threshold_for_new_service, test_set_idle_threshold_for_existing_service, test_config_directory_not_found, test_file_io_error... |
| `tests/unit/test_project_mapper_tool.py` | 🧪 Test | File: test_project_mapper_tool.py | **Classes:** TestProjectMapperTool<br>**Functions:** tool, temp_project, test_is_ignored, test_guess_type, test_extract_imports_python... |
| `tests/unit/test_prompt_engineering.py` | 🟢 Referenced | File: test_prompt_engineering.py | **Classes:** TestEvolve, TestRunCampaign, TestPromoteAgent, TestVisualizeArchive<br>**Functions:** mock_archive, test_select_parent_from_archive_empty, test_select_parent_from_archive_populated, test_run_evolution, test_run_campaign_args... |
| `tests/unit/test_prompt_improver_tool.py` | 🧪 Test | File: test_prompt_improver_tool.py | **Classes:** TestPromptImproverTool<br>**Functions:** setUp, test_create_prompt_plan, test_discover_llm_failure |
| `tests/unit/test_provisioning.py` | 🟢 Referenced | File: test_provisioning.py | **Classes:** TestProvisioning<br>**Functions:** setUp, tearDown, test_load_playbooks_from_manifest, test_wait_for_ports_freed, test_cleanup_memory_for_core_ai... |
| `tests/unit/test_rag_tool.py` | 🟢 Referenced | File: test_rag_tool.py | **Classes:** SyncThread<br>**Functions:** mock_sentence_transformer, mock_faiss, mock_pmm_memory, sync_threading, test_rag_tool_initialization... |
| `tests/unit/test_reflection.py` | 🟢 Referenced | File: test_reflection.py | **Classes:** TestReflection<br>**Functions:** test_analyze_failure_out_of_memory_with_tool_use, test_analyze_failure_simple_restart, test_main_success, test_main_no_args, test_main_file_not_found... |
| `tests/unit/test_search_tool_security.py` | 🧪 Test | File: test_search_tool_security.py | **Classes:** TestSearchToolSecurity<br>**Functions:** setup_search_env, test_search_inside_root, test_search_traversal_via_symlink, test_find_traversal_via_symlink |
| `tests/unit/test_security.py` | 🟢 Referenced | Ensure pipecatapp is in path | **Classes:** TestSecurity<br>**Functions:** test_redact_sensitive_data, test_sanitize_data |
| `tests/unit/test_shell_tool.py` | 🧪 Test | File: test_shell_tool.py | **Functions:** test_shell_tool_initialization, test_execute_command_success, test_execute_command_timeout |
| `tests/unit/test_shell_tool_security.py` | 🟢 Referenced | File: test_shell_tool_security.py | **Classes:** TestShellToolLeak<br>**Functions:** test_leak, side_effect |
| `tests/unit/test_simple_llm_node.py` | 🧪 Test | Mock pipecat before importing the module under test | **Classes:** TestSimpleLLMNode<br>**Functions:** test_fast_tier_execution, test_balanced_tier_execution |
| `tests/unit/test_skill_library.py` | 🧪 Test | File: test_skill_library.py | **Functions:** temp_db, test_skill_library_save_and_retrieve, test_skill_library_update, test_skill_library_search, test_save_skill_tool... |
| `tests/unit/test_smol_agent_tool.py` | 🧪 Test | File: test_smol_agent_tool.py | **Functions:** smol_tool, test_run_success, test_run_multiple_code_blocks, test_deno_missing, test_empty_task... |
| `tests/unit/test_ssh_tool.py` | 🟢 Referenced | File: test_ssh_tool.py | **Functions:** ssh_tool, test_run_command_with_key_success, test_run_command_with_password_success, test_run_command_with_error, test_no_auth_method_provided... |
| `tests/unit/test_summarizer_tool.py` | 🟢 Referenced | File: test_summarizer_tool.py | **Functions:** mock_sentence_transformer_module, summarizer_tool, test_get_summary_with_history, test_get_summary_no_history, test_get_summary_less_than_k_history... |
| `tests/unit/test_supervisor.py` | 🟢 Referenced | File: test_supervisor.py | **Classes:** TestSupervisor<br>**Functions:** test_run_playbook_success, test_run_playbook_failure, test_run_playbook_with_extra_vars, test_run_script_success, test_run_script_failure... |
| `tests/unit/test_swarm_tool.py` | 🧪 Test | File: test_swarm_tool.py | **Functions:** test_swarm_tool_initialization, test_spawn_workers_success, test_spawn_workers_partial_failure, test_kill_worker_success, test_kill_worker_failure... |
| `tests/unit/test_tap_service.py` | 🧪 Test | File: test_tap_service.py | **Classes:** MockFrameProcessor<br>**Functions:** test_process_frame, __init__, push_frame |
| `tests/unit/test_term_everything_tool.py` | 🟢 Referenced | File: test_term_everything_tool.py | **Functions:** tool, test_execute_command_success, test_execute_command_failure, test_execute_exception |
| `tests/unit/test_vision_failover.py` | 🟢 Referenced | File: test_vision_failover.py | **Classes:** MockFrameProcessor, MockVisionImageRawFrame<br>**Functions:** test_vision_selection_primary_succeeds, test_vision_selection_fallback_succeeds, test_vision_selection_both_fail, test_yolo_internal_initialization_failover, test_yolo_internal_process_frame_failover... |
| `tests/unit/test_web_browser_tool.py` | 🟢 Referenced | File: test_web_browser_tool.py | **Classes:** TestWebBrowserTool<br>**Functions:** asyncSetUp, asyncTearDown, test_goto_success, test_goto_failure, test_get_page_content_success... |
| `tests/unit/test_web_server_personality.py` | 🧪 Test | File: test_web_server_personality.py | **Functions:** test_get_personality |
| `tests/unit/test_web_server_sync.py` | 🧪 Test | File: test_web_server_sync.py | **Functions:** test_internal_chat_sync_success, test_internal_chat_sync_timeout, responder |
| `tests/unit/test_workflow.py` | 🧪 Test | File: test_workflow.py | **Classes:** PromptBuilderNode<br>**Functions:** mock_registry, clear_workflow_cache, test_topological_sort_linear, test_topological_sort_with_cycle, test_workflow_execution_data_flow... |
| `tests/unit/test_world_model_service.py` | 🧪 Test | File: test_world_model_service.py | **Functions:** client, mock_mqtt_client, test_health_check, test_on_connect_successful, test_on_connect_failed... |
| `tests/verify_config_load.py` | 🟢 Referenced | File: verify_config_load.py | **Functions:** load_config |
| `tests/verify_dlq.py` | 🧪 Test | File: verify_dlq.py | **Functions:** run_server, test_server, run_test |
| `workflows/default_agent_loop.yaml` | 🟢 Referenced | File: default_agent_loop.yaml |  |

## Dependency Diagram

```mermaid
graph LR
    subgraph dir_Root [Root]
        direction TB
        node_17[".coverage"]
        node_3[".djlint.toml"]
        node_12[".gitattributes"]
        node_1[".gitignore"]
        node_26[".markdownlint.json"]
        node_33[".yamllint"]
        node_20["AGENTS.md"]
        node_14["LANGCHAIN_ANALYSIS.md"]
        node_9["LICENSE"]
        node_2["OBSIDIAN_TODO.md"]
        node_32["README.md"]
        node_8["TODO.md"]
        node_21["aid_e_log.txt"]
        node_27["ansible.cfg"]
        node_4["bootstrap.sh"]
        node_23["hostfile"]
        node_0["initial_state.png"]
        node_34["inventory.yaml"]
        node_28["local_inventory.ini"]
        node_31["package.json"]
        node_25["paused_state.png"]
        node_11["plan.md"]
        node_13["playbook.yaml"]
        node_10["pytest.ini"]
        node_15["requirements-dev.txt"]
        node_35["review_report.md"]
        node_24["run_emperor_test.sh"]
        node_7["run_test.py"]
        node_22["test_autoresearch.py"]
        node_30["test_clamav_playbook.yml"]
        node_29["test_db.sqlite-shm"]
        node_5["test_db.sqlite-wal"]
        node_16["test_dlq.db-shm"]
        node_18["test_dlq.db-wal"]
        node_19["test_playbook.yml"]
        node_6["test_script.py"]
    end
    subgraph dir__githooks [.githooks]
        direction TB
        node_252["pre-commit"]
    end
    subgraph dir__github [.github]
        direction TB
        node_357["AGENTIC_README.md"]
    end
    subgraph dir__github_workflows [.github/workflows]
        direction TB
        node_360["auto-merge.yml"]
        node_362["ci.yml"]
        node_361["create-issues-from-files.yml"]
        node_363["jules-queue.yml"]
        node_358["remote-verify.yml"]
        node_359["test-cluster.yml"]
    end
    subgraph dir__husky [.husky]
        direction TB
        node_253["pre-push"]
    end
    subgraph dir__opencode [.opencode]
        direction TB
        node_413["README.md"]
        node_412["opencode.json"]
    end
    subgraph dir_ansible [ansible]
        direction TB
        node_555["README.md"]
        node_553["lint_nomad.yaml"]
        node_554["run_download_models.yaml"]
    end
    subgraph dir_ansible_filter_plugins [ansible/filter_plugins]
        direction TB
        node_557["README.md"]
        node_556["safe_flatten.py"]
    end
    subgraph dir_ansible_jobs [ansible/jobs]
        direction TB
        node_575["README.md"]
        node_573["benchmark.nomad"]
        node_571["evolve-prompt.nomad.j2"]
        node_572["expert-debug.nomad"]
        node_576["expert.nomad.j2"]
        node_569["filebrowser.nomad.j2"]
        node_564["health-check.nomad.j2"]
        node_567["llamacpp-batch.nomad.j2"]
        node_570["llamacpp-rpc.nomad.j2"]
        node_574["model-benchmark.nomad.j2"]
        node_568["pipecatapp.nomad"]
        node_563["router.nomad.j2"]
        node_566["test-runner.nomad.j2"]
        node_565["vllm.nomad.j2"]
    end
    subgraph dir_ansible_roles [ansible/roles]
        direction TB
        node_577["README.md"]
    end
    subgraph dir_ansible_roles_benchmark_models_tasks [ansible/roles/benchmark_models/tasks]
        direction TB
        node_720["benchmark_loop.yaml"]
        node_719["main.yaml"]
    end
    subgraph dir_ansible_roles_benchmark_models_templates [ansible/roles/benchmark_models/templates]
        direction TB
        node_718["model-benchmark.nomad.j2"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_defaults [ansible/roles/bootstrap_agent/defaults]
        direction TB
        node_835["main.yaml"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_tasks [ansible/roles/bootstrap_agent/tasks]
        direction TB
        node_834["deploy_llama_cpp_model.yaml"]
        node_833["main.yaml"]
    end
    subgraph dir_ansible_roles_clamav_files [ansible/roles/clamav/files]
        direction TB
        node_832["rogue_agent.ldb"]
    end
    subgraph dir_ansible_roles_clamav_handlers [ansible/roles/clamav/handlers]
        direction TB
        node_830["main.yaml"]
    end
    subgraph dir_ansible_roles_clamav_tasks [ansible/roles/clamav/tasks]
        direction TB
        node_831["main.yaml"]
    end
    subgraph dir_ansible_roles_claude_clone_tasks [ansible/roles/claude_clone/tasks]
        direction TB
        node_686["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tools_tasks [ansible/roles/common-tools/tasks]
        direction TB
        node_689["main.yaml"]
    end
    subgraph dir_ansible_roles_common_handlers [ansible/roles/common/handlers]
        direction TB
        node_625["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tasks [ansible/roles/common/tasks]
        direction TB
        node_626["main.yaml"]
        node_627["network_repair.yaml"]
    end
    subgraph dir_ansible_roles_common_templates [ansible/roles/common/templates]
        direction TB
        node_622["cluster-ip-alias.service.j2"]
        node_623["hosts.j2"]
        node_624["update-ssh-authorized-keys.sh.j2"]
    end
    subgraph dir_ansible_roles_config_manager_tasks [ansible/roles/config_manager/tasks]
        direction TB
        node_828["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_defaults [ansible/roles/consul/defaults]
        direction TB
        node_763["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_handlers [ansible/roles/consul/handlers]
        direction TB
        node_759["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_tasks [ansible/roles/consul/tasks]
        direction TB
        node_761["acl.yaml"]
        node_760["main.yaml"]
        node_762["tls.yaml"]
    end
    subgraph dir_ansible_roles_consul_templates [ansible/roles/consul/templates]
        direction TB
        node_757["consul.hcl.j2"]
        node_758["consul.service.j2"]
    end
    subgraph dir_ansible_roles_desktop_extras_tasks [ansible/roles/desktop_extras/tasks]
        direction TB
        node_747["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_handlers [ansible/roles/docker/handlers]
        direction TB
        node_680["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_molecule_default [ansible/roles/docker/molecule/default]
        direction TB
        node_684["converge.yml"]
        node_682["molecule.yml"]
        node_685["prepare.yml"]
        node_683["verify.yml"]
    end
    subgraph dir_ansible_roles_docker_tasks [ansible/roles/docker/tasks]
        direction TB
        node_681["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_templates [ansible/roles/docker/templates]
        direction TB
        node_679["daemon.json.j2"]
    end
    subgraph dir_ansible_roles_docker_registry_tasks [ansible/roles/docker_registry/tasks]
        direction TB
        node_579["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_registry_templates [ansible/roles/docker_registry/templates]
        direction TB
        node_578["docker-registry.nomad.j2"]
    end
    subgraph dir_ansible_roles_download_models_files [ansible/roles/download_models/files]
        direction TB
        node_688["download_hf_repo.py"]
    end
    subgraph dir_ansible_roles_download_models_tasks [ansible/roles/download_models/tasks]
        direction TB
        node_687["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_defaults [ansible/roles/exo/defaults]
        direction TB
        node_850["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_files [ansible/roles/exo/files]
        direction TB
        node_851["Dockerfile"]
    end
    subgraph dir_ansible_roles_exo_tasks [ansible/roles/exo/tasks]
        direction TB
        node_849["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_templates [ansible/roles/exo/templates]
        direction TB
        node_848["exo.nomad.j2"]
    end
    subgraph dir_ansible_roles_forgejo_handlers [ansible/roles/forgejo/handlers]
        direction TB
        node_722["main.yaml"]
    end
    subgraph dir_ansible_roles_forgejo_tasks [ansible/roles/forgejo/tasks]
        direction TB
        node_723["main.yaml"]
    end
    subgraph dir_ansible_roles_forgejo_templates [ansible/roles/forgejo/templates]
        direction TB
        node_721["forgejo.nomad.j2"]
    end
    subgraph dir_ansible_roles_gemini_cli_handlers [ansible/roles/gemini_cli/handlers]
        direction TB
        node_646["main.yaml"]
    end
    subgraph dir_ansible_roles_gemini_cli_tasks [ansible/roles/gemini_cli/tasks]
        direction TB
        node_647["main.yaml"]
    end
    subgraph dir_ansible_roles_gemini_cli_templates [ansible/roles/gemini_cli/templates]
        direction TB
        node_645["gemini.nomad.j2"]
    end
    subgraph dir_ansible_roles_headscale_defaults [ansible/roles/headscale/defaults]
        direction TB
        node_600["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_handlers [ansible/roles/headscale/handlers]
        direction TB
        node_598["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_tasks [ansible/roles/headscale/tasks]
        direction TB
        node_599["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_templates [ansible/roles/headscale/templates]
        direction TB
        node_597["config.yaml.j2"]
        node_596["headscale.service.j2"]
    end
    subgraph dir_ansible_roles_heretic_tool_defaults [ansible/roles/heretic_tool/defaults]
        direction TB
        node_717["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_meta [ansible/roles/heretic_tool/meta]
        direction TB
        node_716["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_tasks [ansible/roles/heretic_tool/tasks]
        direction TB
        node_715["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_meta [ansible/roles/home_assistant/meta]
        direction TB
        node_738["main.yaml"]
        node_739["main.yml"]
    end
    subgraph dir_ansible_roles_home_assistant_tasks [ansible/roles/home_assistant/tasks]
        direction TB
        node_737["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_templates [ansible/roles/home_assistant/templates]
        direction TB
        node_735["configuration.yaml.j2"]
        node_736["home_assistant.nomad.j2"]
    end
    subgraph dir_ansible_roles_kittentts_tasks [ansible/roles/kittentts/tasks]
        direction TB
        node_605["main.yaml"]
    end
    subgraph dir_ansible_roles_librarian_defaults [ansible/roles/librarian/defaults]
        direction TB
        node_705["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_handlers [ansible/roles/librarian/handlers]
        direction TB
        node_703["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_tasks [ansible/roles/librarian/tasks]
        direction TB
        node_704["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_templates [ansible/roles/librarian/templates]
        direction TB
        node_702["librarian.service.j2"]
        node_700["librarian_agent.py.j2"]
        node_701["spacedrive.service.j2"]
    end
    subgraph dir_ansible_roles_llama_cpp_files [ansible/roles/llama_cpp/files]
        direction TB
        node_634["realtime_steering.patch"]
    end
    subgraph dir_ansible_roles_llama_cpp_handlers [ansible/roles/llama_cpp/handlers]
        direction TB
        node_628["main.yaml"]
    end
    subgraph dir_ansible_roles_llama_cpp_molecule_default [ansible/roles/llama_cpp/molecule/default]
        direction TB
        node_633["converge.yml"]
        node_631["molecule.yml"]
        node_632["verify.yml"]
    end
    subgraph dir_ansible_roles_llama_cpp_tasks [ansible/roles/llama_cpp/tasks]
        direction TB
        node_629["main.yaml"]
        node_630["run_single_rpc_job.yaml"]
    end
    subgraph dir_ansible_roles_llmfit_tasks [ansible/roles/llmfit/tasks]
        direction TB
        node_845["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_tasks [ansible/roles/llxprt_code/tasks]
        direction TB
        node_847["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_templates [ansible/roles/llxprt_code/templates]
        direction TB
        node_846["llxprt-code.env.j2"]
    end
    subgraph dir_ansible_roles_magic_mirror_defaults [ansible/roles/magic_mirror/defaults]
        direction TB
        node_595["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_handlers [ansible/roles/magic_mirror/handlers]
        direction TB
        node_593["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_tasks [ansible/roles/magic_mirror/tasks]
        direction TB
        node_594["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_templates [ansible/roles/magic_mirror/templates]
        direction TB
        node_592["magic_mirror.nomad.j2"]
    end
    subgraph dir_ansible_roles_mcp_server_defaults [ansible/roles/mcp_server/defaults]
        direction TB
        node_751["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_handlers [ansible/roles/mcp_server/handlers]
        direction TB
        node_749["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_tasks [ansible/roles/mcp_server/tasks]
        direction TB
        node_750["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_templates [ansible/roles/mcp_server/templates]
        direction TB
        node_748["mcp_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_graph_tasks [ansible/roles/memory_graph/tasks]
        direction TB
        node_819["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_graph_templates [ansible/roles/memory_graph/templates]
        direction TB
        node_818["memory-graph.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_service_files [ansible/roles/memory_service/files]
        direction TB
        node_693["app.py"]
        node_694["pmm_memory.py"]
    end
    subgraph dir_ansible_roles_memory_service_handlers [ansible/roles/memory_service/handlers]
        direction TB
        node_691["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_tasks [ansible/roles/memory_service/tasks]
        direction TB
        node_692["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_templates [ansible/roles/memory_service/templates]
        direction TB
        node_690["memory_service.nomad.j2"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files [ansible/roles/minikeyvalue/files]
        direction TB
        node_608["Dockerfile"]
        node_610["start_master.py"]
        node_609["volume"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files_src [ansible/roles/minikeyvalue/files/src]
        direction TB
        node_611["lib.go"]
        node_614["lib_test.go"]
        node_616["main.go"]
        node_617["rebalance.go"]
        node_612["rebuild.go"]
        node_613["s3api.go"]
        node_615["server.go"]
    end
    subgraph dir_ansible_roles_minikeyvalue_tasks [ansible/roles/minikeyvalue/tasks]
        direction TB
        node_607["main.yaml"]
    end
    subgraph dir_ansible_roles_minikeyvalue_templates [ansible/roles/minikeyvalue/templates]
        direction TB
        node_606["mkv.nomad.j2"]
    end
    subgraph dir_ansible_roles_miniray_files [ansible/roles/miniray/files]
        direction TB
        node_827["Dockerfile"]
    end
    subgraph dir_ansible_roles_miniray_tasks [ansible/roles/miniray/tasks]
        direction TB
        node_826["main.yaml"]
    end
    subgraph dir_ansible_roles_miniray_templates [ansible/roles/miniray/templates]
        direction TB
        node_825["miniray.nomad.j2"]
    end
    subgraph dir_ansible_roles_moe_gateway_files [ansible/roles/moe_gateway/files]
        direction TB
        node_677["gateway.py"]
    end
    subgraph dir_ansible_roles_moe_gateway_files_static [ansible/roles/moe_gateway/files/static]
        direction TB
        node_678["index.html"]
    end
    subgraph dir_ansible_roles_moe_gateway_handlers [ansible/roles/moe_gateway/handlers]
        direction TB
        node_675["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_tasks [ansible/roles/moe_gateway/tasks]
        direction TB
        node_676["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_templates [ansible/roles/moe_gateway/templates]
        direction TB
        node_674["moe-gateway.nomad.j2"]
    end
    subgraph dir_ansible_roles_monitoring_defaults [ansible/roles/monitoring/defaults]
        direction TB
        node_773["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_files [ansible/roles/monitoring/files]
        direction TB
        node_774["llm_dashboard.json"]
    end
    subgraph dir_ansible_roles_monitoring_tasks [ansible/roles/monitoring/tasks]
        direction TB
        node_772["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_templates [ansible/roles/monitoring/templates]
        direction TB
        node_767["dashboards.yaml.j2"]
        node_766["datasource.yaml.j2"]
        node_771["grafana.nomad.j2"]
        node_764["memory-audit.nomad.j2"]
        node_765["mqtt-exporter.nomad.j2"]
        node_770["node-exporter.nomad.j2"]
        node_768["prometheus.nomad.j2"]
        node_769["prometheus.yml.j2"]
    end
    subgraph dir_ansible_roles_mqtt_handlers [ansible/roles/mqtt/handlers]
        direction TB
        node_707["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_meta [ansible/roles/mqtt/meta]
        direction TB
        node_709["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_tasks [ansible/roles/mqtt/tasks]
        direction TB
        node_708["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_templates [ansible/roles/mqtt/templates]
        direction TB
        node_706["mqtt.nomad.j2"]
    end
    subgraph dir_ansible_roles_nanochat_defaults [ansible/roles/nanochat/defaults]
        direction TB
        node_823["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_handlers [ansible/roles/nanochat/handlers]
        direction TB
        node_821["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_tasks [ansible/roles/nanochat/tasks]
        direction TB
        node_822["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_templates [ansible/roles/nanochat/templates]
        direction TB
        node_820["nanochat.nomad.j2"]
    end
    subgraph dir_ansible_roles_nats_handlers [ansible/roles/nats/handlers]
        direction TB
        node_725["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_tasks [ansible/roles/nats/tasks]
        direction TB
        node_726["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_templates [ansible/roles/nats/templates]
        direction TB
        node_724["nats.nomad.j2"]
    end
    subgraph dir_ansible_roles_nfs_handlers [ansible/roles/nfs/handlers]
        direction TB
        node_813["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_tasks [ansible/roles/nfs/tasks]
        direction TB
        node_814["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_templates [ansible/roles/nfs/templates]
        direction TB
        node_812["exports.j2"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_handlers [ansible/roles/nixos_pxe_server/handlers]
        direction TB
        node_838["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_tasks [ansible/roles/nixos_pxe_server/tasks]
        direction TB
        node_839["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_templates [ansible/roles/nixos_pxe_server/templates]
        direction TB
        node_837["boot.ipxe.nix.j2"]
        node_836["configuration.nix.j2"]
    end
    subgraph dir_ansible_roles_nomad_defaults [ansible/roles/nomad/defaults]
        direction TB
        node_591["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_handlers [ansible/roles/nomad/handlers]
        direction TB
        node_588["main.yaml"]
        node_589["restart_nomad_handler_tasks.yaml"]
    end
    subgraph dir_ansible_roles_nomad_tasks [ansible/roles/nomad/tasks]
        direction TB
        node_590["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_templates [ansible/roles/nomad/templates]
        direction TB
        node_585["client.hcl.j2"]
        node_583["nomad.hcl.server.j2"]
        node_586["nomad.service.j2"]
        node_587["nomad.sh.j2"]
        node_584["server.hcl.j2"]
    end
    subgraph dir_ansible_roles_openclaw_files [ansible/roles/openclaw/files]
        direction TB
        node_637["Dockerfile"]
        node_638["pipecat_skill.md"]
    end
    subgraph dir_ansible_roles_openclaw_tasks [ansible/roles/openclaw/tasks]
        direction TB
        node_636["main.yaml"]
    end
    subgraph dir_ansible_roles_openclaw_templates [ansible/roles/openclaw/templates]
        direction TB
        node_635["openclaw.nomad.j2"]
    end
    subgraph dir_ansible_roles_opencode_handlers [ansible/roles/opencode/handlers]
        direction TB
        node_581["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_tasks [ansible/roles/opencode/tasks]
        direction TB
        node_582["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_templates [ansible/roles/opencode/templates]
        direction TB
        node_580["opencode.nomad.j2"]
    end
    subgraph dir_ansible_roles_openworkers_handlers [ansible/roles/openworkers/handlers]
        direction TB
        node_698["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_tasks [ansible/roles/openworkers/tasks]
        direction TB
        node_699["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_templates [ansible/roles/openworkers/templates]
        direction TB
        node_696["openworkers-bootstrap.nomad.j2"]
        node_697["openworkers-infra.nomad.j2"]
        node_695["openworkers-runners.nomad.j2"]
    end
    subgraph dir_ansible_roles_paddler_tasks [ansible/roles/paddler/tasks]
        direction TB
        node_740["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent [ansible/roles/paddler_agent]
        direction TB
        node_840["README.md"]
    end
    subgraph dir_ansible_roles_paddler_agent_defaults [ansible/roles/paddler_agent/defaults]
        direction TB
        node_843["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_tasks [ansible/roles/paddler_agent/tasks]
        direction TB
        node_842["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_templates [ansible/roles/paddler_agent/templates]
        direction TB
        node_841["paddler-agent.service.j2"]
    end
    subgraph dir_ansible_roles_paddler_balancer [ansible/roles/paddler_balancer]
        direction TB
        node_652["README.md"]
    end
    subgraph dir_ansible_roles_paddler_balancer_defaults [ansible/roles/paddler_balancer/defaults]
        direction TB
        node_655["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_tasks [ansible/roles/paddler_balancer/tasks]
        direction TB
        node_654["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_templates [ansible/roles/paddler_balancer/templates]
        direction TB
        node_653["paddler-balancer.service.j2"]
    end
    subgraph dir_ansible_roles_pds_tasks [ansible/roles/pds/tasks]
        direction TB
        node_734["main.yaml"]
    end
    subgraph dir_ansible_roles_pds_templates [ansible/roles/pds/templates]
        direction TB
        node_733["pds.nomad.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_defaults [ansible/roles/pipecatapp/defaults]
        direction TB
        node_668["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_handlers [ansible/roles/pipecatapp/handlers]
        direction TB
        node_666["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_tasks [ansible/roles/pipecatapp/tasks]
        direction TB
        node_667["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates [ansible/roles/pipecatapp/templates]
        direction TB
        node_656["archivist.nomad.j2"]
        node_659["pipecat.env.j2"]
        node_657["pipecatapp.nomad.j2"]
        node_658["start_pipecatapp.sh.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_prompts [ansible/roles/pipecatapp/templates/prompts]
        direction TB
        node_663["coding_expert.txt.j2"]
        node_664["creative_expert.txt.j2"]
        node_661["cynic_expert.txt.j2"]
        node_662["router.txt.j2"]
        node_665["tron_agent.txt.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_workflows [ansible/roles/pipecatapp/templates/workflows]
        direction TB
        node_660["default_agent_loop.yaml.j2"]
    end
    subgraph dir_ansible_roles_postgres_handlers [ansible/roles/postgres/handlers]
        direction TB
        node_853["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_tasks [ansible/roles/postgres/tasks]
        direction TB
        node_854["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_templates [ansible/roles/postgres/templates]
        direction TB
        node_852["postgres.nomad.j2"]
    end
    subgraph dir_ansible_roles_power_manager_defaults [ansible/roles/power_manager/defaults]
        direction TB
        node_744["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_files [ansible/roles/power_manager/files]
        direction TB
        node_745["power_agent.py"]
        node_746["traffic_monitor.c"]
    end
    subgraph dir_ansible_roles_power_manager_handlers [ansible/roles/power_manager/handlers]
        direction TB
        node_742["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_tasks [ansible/roles/power_manager/tasks]
        direction TB
        node_743["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_templates [ansible/roles/power_manager/templates]
        direction TB
        node_741["power-agent.service.j2"]
    end
    subgraph dir_ansible_roles_preflight_checks_tasks [ansible/roles/preflight_checks/tasks]
        direction TB
        node_829["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_files [ansible/roles/provisioning_api/files]
        direction TB
        node_621["provisioning_api.py"]
    end
    subgraph dir_ansible_roles_provisioning_api_handlers [ansible/roles/provisioning_api/handlers]
        direction TB
        node_619["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_tasks [ansible/roles/provisioning_api/tasks]
        direction TB
        node_620["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_templates [ansible/roles/provisioning_api/templates]
        direction TB
        node_618["provisioning-api.service.j2"]
    end
    subgraph dir_ansible_roles_pxe_server_defaults [ansible/roles/pxe_server/defaults]
        direction TB
        node_732["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_handlers [ansible/roles/pxe_server/handlers]
        direction TB
        node_730["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_tasks [ansible/roles/pxe_server/tasks]
        direction TB
        node_731["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_templates [ansible/roles/pxe_server/templates]
        direction TB
        node_727["boot.ipxe.j2"]
        node_728["dhcpd.conf.j2"]
        node_729["preseed.cfg.j2"]
    end
    subgraph dir_ansible_roles_python_deps_files [ansible/roles/python_deps/files]
        direction TB
        node_817["requirements.txt"]
    end
    subgraph dir_ansible_roles_python_deps_meta [ansible/roles/python_deps/meta]
        direction TB
        node_816["main.yaml"]
    end
    subgraph dir_ansible_roles_python_deps_tasks [ansible/roles/python_deps/tasks]
        direction TB
        node_815["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_defaults [ansible/roles/semantic_router/defaults]
        direction TB
        node_755["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_tasks [ansible/roles/semantic_router/tasks]
        direction TB
        node_754["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_templates [ansible/roles/semantic_router/templates]
        direction TB
        node_752["Dockerfile.j2"]
        node_753["semantic-router.nomad.j2"]
    end
    subgraph dir_ansible_roles_sunshine_defaults [ansible/roles/sunshine/defaults]
        direction TB
        node_651["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_handlers [ansible/roles/sunshine/handlers]
        direction TB
        node_649["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_tasks [ansible/roles/sunshine/tasks]
        direction TB
        node_650["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_templates [ansible/roles/sunshine/templates]
        direction TB
        node_648["sunshine.nomad.j2"]
    end
    subgraph dir_ansible_roles_system_deps_tasks [ansible/roles/system_deps/tasks]
        direction TB
        node_601["main.yaml"]
    end
    subgraph dir_ansible_roles_tailscale_tasks [ansible/roles/tailscale/tasks]
        direction TB
        node_824["main.yaml"]
    end
    subgraph dir_ansible_roles_term_everything_tasks [ansible/roles/term_everything/tasks]
        direction TB
        node_844["main.yml"]
    end
    subgraph dir_ansible_roles_tool_server [ansible/roles/tool_server]
        direction TB
        node_776["Dockerfile"]
        node_775["app.py"]
        node_779["entrypoint.sh"]
        node_777["pmm_memory.py"]
        node_778["preload_models.py"]
    end
    subgraph dir_ansible_roles_tool_server_tasks [ansible/roles/tool_server/tasks]
        direction TB
        node_781["main.yaml"]
    end
    subgraph dir_ansible_roles_tool_server_templates [ansible/roles/tool_server/templates]
        direction TB
        node_780["tool_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_tool_server_tools [ansible/roles/tool_server/tools]
        direction TB
        node_805["ansible_tool.py"]
        node_807["archivist_tool.py"]
        node_785["claude_clone_tool.py"]
        node_809["code_runner_tool.py"]
        node_802["council_tool.py"]
        node_800["desktop_control_tool.py"]
        node_799["file_editor_tool.py"]
        node_782["final_answer_tool.py"]
        node_794["gemini_cli.py"]
        node_793["get_nomad_job.py"]
        node_804["git_tool.py"]
        node_787["ha_tool.py"]
        node_797["llxprt_code_tool.py"]
        node_783["mcp_tool.py"]
        node_791["opencode_tool.py"]
        node_788["orchestrator_tool.py"]
        node_811["planner_tool.py"]
        node_790["power_tool.py"]
        node_784["project_mapper_tool.py"]
        node_810["prompt_improver_tool.py"]
        node_806["rag_tool.py"]
        node_808["sandbox.ts"]
        node_792["shell_tool.py"]
        node_789["smol_agent_tool.py"]
        node_786["ssh_tool.py"]
        node_803["summarizer_tool.py"]
        node_795["swarm_tool.py"]
        node_796["tap_service.py"]
        node_798["term_everything_tool.py"]
        node_801["web_browser_tool.py"]
    end
    subgraph dir_ansible_roles_unified_fs_defaults [ansible/roles/unified_fs/defaults]
        direction TB
        node_713["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_files [ansible/roles/unified_fs/files]
        direction TB
        node_714["unified_fs_agent.py"]
    end
    subgraph dir_ansible_roles_unified_fs_handlers [ansible/roles/unified_fs/handlers]
        direction TB
        node_711["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_tasks [ansible/roles/unified_fs/tasks]
        direction TB
        node_712["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_templates [ansible/roles/unified_fs/templates]
        direction TB
        node_710["unified_fs.service.j2"]
    end
    subgraph dir_ansible_roles_vision_defaults [ansible/roles/vision/defaults]
        direction TB
        node_673["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_handlers [ansible/roles/vision/handlers]
        direction TB
        node_671["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_tasks [ansible/roles/vision/tasks]
        direction TB
        node_672["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_templates [ansible/roles/vision/templates]
        direction TB
        node_669["config.yml.j2"]
        node_670["vision.nomad.j2"]
    end
    subgraph dir_ansible_roles_vllm_tasks [ansible/roles/vllm/tasks]
        direction TB
        node_604["main.yaml"]
        node_603["run_single_vllm_job.yaml"]
    end
    subgraph dir_ansible_roles_vllm_templates [ansible/roles/vllm/templates]
        direction TB
        node_602["vllm-expert.nomad.j2"]
    end
    subgraph dir_ansible_roles_whisper_cpp_tasks [ansible/roles/whisper_cpp/tasks]
        direction TB
        node_756["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service_files [ansible/roles/world_model_service/files]
        direction TB
        node_642["Dockerfile"]
        node_641["app.py"]
        node_643["debug_world_model.sh"]
        node_644["requirements.txt"]
    end
    subgraph dir_ansible_roles_world_model_service_tasks [ansible/roles/world_model_service/tasks]
        direction TB
        node_640["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service_templates [ansible/roles/world_model_service/templates]
        direction TB
        node_639["world_model.nomad.j2"]
    end
    subgraph dir_ansible_tasks [ansible/tasks]
        direction TB
        node_562["README.md"]
        node_560["build_pipecatapp_image.yaml"]
        node_558["create_expert_job.yaml"]
        node_561["deploy_expert_wrapper.yaml"]
        node_559["deploy_model_gpu_provider.yaml"]
    end
    subgraph dir_docker [docker]
        direction TB
        node_217["README.md"]
    end
    subgraph dir_docker_dev_container [docker/dev_container]
        direction TB
        node_219["Dockerfile"]
    end
    subgraph dir_docker_memory_service [docker/memory_service]
        direction TB
        node_218["Dockerfile"]
    end
    subgraph dir_docs [docs]
        direction TB
        node_238["AGENTS.md"]
        node_223["AI_GOVERNANCE.md"]
        node_251["ARCHITECTURE.md"]
        node_227["BENCHMARKING.MD"]
        node_240["CLAMAV_EVALUATION.md"]
        node_233["DEPLOYMENT_AND_PROFILING.md"]
        node_248["EVALUATION_LLMROUTER.md"]
        node_226["FRONTEND_VERIFICATION.md"]
        node_245["FRONTIER_AGENT_ROADMAP.md"]
        node_237["GASTOWN_TODO.md"]
        node_225["GCP_GENERATIVE_AI_REVIEW.md"]
        node_221["GEMINI.md"]
        node_230["IPV6_AUDIT.md"]
        node_241["MCP_SERVER_SETUP.md"]
        node_247["MEMORIES.md"]
        node_249["NETWORK.md"]
        node_229["NIXOS_PXE_BOOT_SETUP.md"]
        node_235["OBSIDIAN_WORKFLOW_DESIGN.md"]
        node_244["PERFORMANCE_OPTIMIZATION.md"]
        node_232["PROJECT_SUMMARY.md"]
        node_239["PXE_BOOT_SETUP.md"]
        node_250["README.md"]
        node_242["REFACTOR_PROPOSAL_hybrid_architecture.md"]
        node_220["REMOTE_WORKFLOW.md"]
        node_224["SCALING_TODO.md"]
        node_231["SECURITY_AUDIT.md"]
        node_222["TODO_Hybrid_Architecture.md"]
        node_243["TOOL_EVALUATION.md"]
        node_246["TROUBLESHOOTING.md"]
        node_236["VLLM_PROJECT_EVALUATION.md"]
        node_228["YAML_FILES_REPORT.md"]
        node_234["heretic_evaluation.md"]
    end
    subgraph dir_examples [examples]
        direction TB
        node_37["README.md"]
        node_36["chat-persistent.sh"]
    end
    subgraph dir_group_vars [group_vars]
        direction TB
        node_40["README.md"]
        node_41["all.yaml"]
        node_39["external_experts.yaml"]
        node_38["models.yaml"]
    end
    subgraph dir_host_vars [host_vars]
        direction TB
        node_400["README.md"]
        node_399["localhost.yaml"]
    end
    subgraph dir_initial_setup [initial-setup]
        direction TB
        node_544["README.md"]
        node_543["add_new_worker.sh"]
        node_542["setup.conf"]
        node_541["setup.sh"]
        node_540["update_inventory.sh"]
    end
    subgraph dir_initial_setup_modules [initial-setup/modules]
        direction TB
        node_549["01-network.sh"]
        node_545["02-hostname.sh"]
        node_546["03-user.sh"]
        node_548["04-ssh.sh"]
        node_547["05-auto-provision.sh"]
        node_550["README.md"]
    end
    subgraph dir_initial_setup_worker_setup [initial-setup/worker-setup]
        direction TB
        node_552["README.md"]
        node_551["setup.sh"]
    end
    subgraph dir_os_image [os-image]
        direction TB
        node_402["README.md"]
        node_401["build_iso.sh"]
    end
    subgraph dir_os_image_config_hooks_live [os-image/config/hooks/live]
        direction TB
        node_403["01-setup-users.chroot"]
        node_404["02-enable-services.chroot"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_profile_d [os-image/config/includes.chroot/etc/profile.d]
        direction TB
        node_406["99-pipecat-welcome.sh"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_systemd_system [os-image/config/includes.chroot/etc/systemd/system]
        direction TB
        node_408["pipecat-firstboot.service"]
        node_407["pipecat-hostname.service"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_systemd_system_multi_user_target_wants [os-image/config/includes.chroot/etc/systemd/system/multi-user.target.wants]
        direction TB
        node_409["pipecat-firstboot.service"]
    end
    subgraph dir_os_image_config_includes_chroot_usr_local_bin [os-image/config/includes.chroot/usr/local/bin]
        direction TB
        node_410["setup-ssh-keys.sh"]
    end
    subgraph dir_os_image_config_includes_installer [os-image/config/includes.installer]
        direction TB
        node_411["preseed.cfg"]
    end
    subgraph dir_os_image_config_package_lists [os-image/config/package-lists]
        direction TB
        node_405["pipecat.list.chroot"]
    end
    subgraph dir_pipecat_agent_extension [pipecat-agent-extension]
        direction TB
        node_538["README.md"]
        node_535["example.ts"]
        node_534["gemini-extension.json"]
        node_537["package.json"]
        node_536["tsconfig.json"]
    end
    subgraph dir_pipecat_agent_extension_commands_pipecat [pipecat-agent-extension/commands/pipecat]
        direction TB
        node_539["send.toml"]
    end
    subgraph dir_pipecatapp [pipecatapp]
        direction TB
        node_51["Dockerfile"]
        node_83["README.md"]
        node_48["TODO.md"]
        node_61["__init__.py"]
        node_63["agent_factory.py"]
        node_75["api_keys.py"]
        node_47["app.py"]
        node_56["archivist_service.py"]
        node_50["durable_execution.py"]
        node_65["expert_tracker.py"]
        node_79["generate_real_embeddings.py"]
        node_77["janitor_agent.py"]
        node_46["judge_agent.py"]
        node_64["langchain_memory_wrappers.py"]
        node_59["llm_clients.py"]
        node_43["manager_agent.py"]
        node_45["memory.py"]
        node_73["models.py"]
        node_68["moondream_detector.py"]
        node_53["net_utils.py"]
        node_76["pmm_memory.py"]
        node_70["pmm_memory_client.py"]
        node_54["quality_control.py"]
        node_60["rate_limiter.py"]
        node_62["requirements.txt"]
        node_85["router_config.yaml"]
        node_72["router_train_embeddings.pt"]
        node_78["router_trained_model.pkl"]
        node_71["router_training_data.csv"]
        node_80["router_training_data.jsonl"]
        node_69["secret_manager.py"]
        node_67["security.py"]
        node_44["skill_library.py"]
        node_52["start_archivist.sh"]
        node_81["task_supervisor.py"]
        node_49["technician_agent.py"]
        node_58["test_memory.py"]
        node_74["test_moondream_detector.py"]
        node_84["test_pmm_memory.py"]
        node_55["test_server.py"]
        node_42["tool_server.py"]
        node_82["train_router.py"]
        node_66["web_server.py"]
        node_57["worker_agent.py"]
    end
    subgraph dir_pipecatapp_datasets [pipecatapp/datasets]
        direction TB
        node_134["sycophancy_prompts.json"]
    end
    subgraph dir_pipecatapp_integrations [pipecatapp/integrations]
        direction TB
        node_88["__init__.py"]
        node_89["openclaw.py"]
    end
    subgraph dir_pipecatapp_memory_graph_service [pipecatapp/memory_graph_service]
        direction TB
        node_86["Dockerfile"]
        node_87["server.py"]
    end
    subgraph dir_pipecatapp_nomad_templates [pipecatapp/nomad_templates]
        direction TB
        node_106["immich.nomad.hcl"]
        node_104["readeck.nomad.hcl"]
        node_105["uptime-kuma.nomad.hcl"]
        node_107["vaultwarden.nomad.hcl"]
    end
    subgraph dir_pipecatapp_prompts [pipecatapp/prompts]
        direction TB
        node_130["coding_expert.txt"]
        node_133["creative_expert.txt"]
        node_132["router.txt"]
        node_131["tron_agent.txt"]
    end
    subgraph dir_pipecatapp_static [pipecatapp/static]
        direction TB
        node_122["cluster.html"]
        node_118["cluster_viz.html"]
        node_123["index.html"]
        node_120["monitor.html"]
        node_124["terminal.js"]
        node_121["vr_index.html"]
        node_117["workflow.html"]
        node_119["workflow_3d.html"]
    end
    subgraph dir_pipecatapp_static_css [pipecatapp/static/css]
        direction TB
        node_125["litegraph.css"]
        node_126["styles.css"]
    end
    subgraph dir_pipecatapp_static_js [pipecatapp/static/js]
        direction TB
        node_128["editor.js"]
        node_127["litegraph.js"]
        node_129["workflow.js"]
    end
    subgraph dir_pipecatapp_tests [pipecatapp/tests]
        direction TB
        node_195["test_audio_streamer.py"]
        node_206["test_browser_tool_security.py"]
        node_211["test_container_registry_tool.py"]
        node_207["test_cq_tool.py"]
        node_204["test_document_tool.py"]
        node_214["test_git_tool_security.py"]
        node_212["test_metrics_cache.py"]
        node_202["test_net_utils.py"]
        node_194["test_openclaw.py"]
        node_198["test_piper_async.py"]
        node_193["test_proxy_security.py"]
        node_196["test_rag_tool.py"]
        node_201["test_rate_limiter.py"]
        node_205["test_security.py"]
        node_213["test_spec_loader_security.py"]
        node_197["test_stt_optimization.py"]
        node_200["test_tool_server.py"]
        node_208["test_uilogger_redaction.py"]
        node_209["test_web_server_unit.py"]
        node_210["test_websocket_security.py"]
        node_199["test_xss_prevention.py"]
        node_203["test_yolo_optimization.py"]
    end
    subgraph dir_pipecatapp_tests_workflow [pipecatapp/tests/workflow]
        direction TB
        node_216["test_history.py"]
        node_215["test_serialization_perf.py"]
    end
    subgraph dir_pipecatapp_tools [pipecatapp/tools]
        direction TB
        node_158["__init__.py"]
        node_181["ansible_tool.py"]
        node_186["archivist_tool.py"]
        node_147["atproto_tool.py"]
        node_154["autoresearch_tool.py"]
        node_144["claude_clone_tool.py"]
        node_143["cluster_status_tool.py"]
        node_190["code_runner_tool.py"]
        node_162["container_registry_tool.py"]
        node_139["context_upload_tool.py"]
        node_178["council_tool.py"]
        node_146["cq_tool.py"]
        node_152["dependency_scanner_tool.py"]
        node_176["desktop_control_tool.py"]
        node_161["document_tool.py"]
        node_172["experiment_tool.py"]
        node_175["file_editor_tool.py"]
        node_135["final_answer_tool.py"]
        node_167["gemini_cli.py"]
        node_165["get_nomad_job.py"]
        node_180["git_tool.py"]
        node_149["ha_tool.py"]
        node_136["heretic_tool.py"]
        node_138["langchain_adapter.py"]
        node_173["llxprt_code_tool.py"]
        node_137["mcp_tool.py"]
        node_189["open_workers_tool.py"]
        node_157["openclaw_tool.py"]
        node_159["opencode_tool.py"]
        node_151["orchestrator_tool.py"]
        node_142["personality_tool.py"]
        node_192["planner_tool.py"]
        node_155["power_tool.py"]
        node_141["project_mapper_tool.py"]
        node_191["prompt_improver_tool.py"]
        node_182["rag_tool.py"]
        node_140["remote_tool_proxy.py"]
        node_187["sandbox.ts"]
        node_188["save_skill_tool.py"]
        node_163["scale_compute_tool.py"]
        node_156["scheduler_tool.py"]
        node_169["search_skills_tool.py"]
        node_166["search_tool.py"]
        node_164["shell_tool.py"]
        node_153["smol_agent_tool.py"]
        node_184["spec_loader_tool.py"]
        node_145["ssh_tool.py"]
        node_185["submit_solution_tool.py"]
        node_179["summarizer_tool.py"]
        node_168["swarm_tool.py"]
        node_171["tap_service.py"]
        node_174["term_everything_tool.py"]
        node_148["test_git_tool.py"]
        node_170["test_ssh_tool.py"]
        node_150["update_litellm_tool.py"]
        node_183["vr_tool.py"]
        node_177["web_browser_tool.py"]
        node_160["wol_tool.py"]
    end
    subgraph dir_pipecatapp_workflow [pipecatapp/workflow]
        direction TB
        node_92["__init__.py"]
        node_91["canvas_converter.py"]
        node_94["context.py"]
        node_95["history.py"]
        node_93["node.py"]
        node_90["runner.py"]
    end
    subgraph dir_pipecatapp_workflow_nodes [pipecatapp/workflow/nodes]
        direction TB
        node_98["__init__.py"]
        node_97["base_nodes.py"]
        node_96["emperor_nodes.py"]
        node_103["langchain_nodes.py"]
        node_101["llm_nodes.py"]
        node_99["registry.py"]
        node_102["system_nodes.py"]
        node_100["tool_nodes.py"]
    end
    subgraph dir_pipecatapp_workflows [pipecatapp/workflows]
        direction TB
        node_111["adversarial_simulation.yaml"]
        node_110["deep_context.yaml"]
        node_108["default_agent_loop.yaml"]
        node_109["looped_reasoning.yaml"]
        node_114["manager.yaml"]
        node_115["poc_ensemble.yaml"]
        node_113["sandbox.yaml"]
        node_112["tiered_agent_loop.yaml"]
        node_116["update_litellm_workflow.yaml"]
    end
    subgraph dir_playbooks [playbooks]
        direction TB
        node_327["README.md"]
        node_305["benchmark_single_model.yaml"]
        node_310["cluster_status.yaml"]
        node_319["common_setup.yaml"]
        node_306["controller.yaml"]
        node_299["debug_template.yaml"]
        node_304["deploy_app.yaml"]
        node_317["deploy_expert.yaml"]
        node_322["deploy_openclaw.yaml"]
        node_311["deploy_pds.yaml"]
        node_313["deploy_prompt_evolution.yaml"]
        node_302["developer_tools.yaml"]
        node_309["diagnose_and_log_home_assistant.yaml"]
        node_314["diagnose_failure.yaml"]
        node_312["diagnose_home_assistant.yaml"]
        node_308["fix_cluster.yaml"]
        node_307["heal_cluster.yaml"]
        node_326["heal_job.yaml"]
        node_303["health_check.yaml"]
        node_318["promote_controller.yaml"]
        node_328["promote_to_controller.yaml"]
        node_301["pxe_setup.yaml"]
        node_324["redeploy_pipecat.yaml"]
        node_325["run_config_manager.yaml"]
        node_300["run_consul.yaml"]
        node_323["run_ha_diag.yaml"]
        node_321["run_health_check.yaml"]
        node_320["status-check.yaml"]
        node_316["wake.yaml"]
        node_315["worker.yaml"]
    end
    subgraph dir_playbooks_network [playbooks/network]
        direction TB
        node_347["mesh.yaml"]
        node_348["verify.yaml"]
    end
    subgraph dir_playbooks_ops [playbooks/ops]
        direction TB
        node_346["optimize_memory.yaml"]
    end
    subgraph dir_playbooks_preflight [playbooks/preflight]
        direction TB
        node_349["checks.yaml"]
    end
    subgraph dir_playbooks_services [playbooks/services]
        direction TB
        node_341["README.md"]
        node_337["ai_experts.yaml"]
        node_340["app_services.yaml"]
        node_334["consul.yaml"]
        node_339["core_ai_services.yaml"]
        node_338["core_infra.yaml"]
        node_332["distributed_compute.yaml"]
        node_342["docker.yaml"]
        node_331["final_verification.yaml"]
        node_343["model_services.yaml"]
        node_333["monitoring.yaml"]
        node_329["nomad.yaml"]
        node_336["nomad_client.yaml"]
        node_335["registry.yaml"]
        node_330["streaming_services.yaml"]
        node_344["training_services.yaml"]
    end
    subgraph dir_playbooks_services_tasks [playbooks/services/tasks]
        direction TB
        node_345["diagnose_home_assistant.yaml"]
    end
    subgraph dir_prompt_engineering [prompt_engineering]
        direction TB
        node_364["PROMPT_ENGINEERING.md"]
        node_374["README.md"]
        node_370["archive_server.py"]
        node_366["challenger.py"]
        node_373["create_evaluator.py"]
        node_368["evaluation_lib.py"]
        node_375["evaluator.py"]
        node_369["evolve.py"]
        node_372["promote_agent.py"]
        node_367["requirements-dev.txt"]
        node_365["run_campaign.py"]
        node_371["visualize_archive.py"]
    end
    subgraph dir_prompt_engineering_agents [prompt_engineering/agents]
        direction TB
        node_381["ADAPTATION_AGENT.md"]
        node_382["EVALUATOR_GENERATOR.md"]
        node_383["README.md"]
        node_378["architecture_review.md"]
        node_376["code_clean_up.md"]
        node_379["debug_and_analysis.md"]
        node_380["new_task_review.md"]
        node_377["problem_scope_framing.md"]
    end
    subgraph dir_prompt_engineering_archive [prompt_engineering/archive]
        direction TB
        node_384["agent_0.json"]
        node_386["agent_0.py"]
        node_388["agent_1.json"]
        node_389["agent_1.py"]
        node_390["agent_2.json"]
        node_385["agent_2.py"]
        node_387["agent_3.json"]
        node_391["agent_3.py"]
    end
    subgraph dir_prompt_engineering_evaluation_suite [prompt_engineering/evaluation_suite]
        direction TB
        node_393["README.md"]
        node_392["test_vision.yaml"]
    end
    subgraph dir_prompt_engineering_frontend [prompt_engineering/frontend]
        direction TB
        node_395["app.js"]
        node_396["index.html"]
        node_394["server.py"]
        node_397["style.css"]
    end
    subgraph dir_prompt_engineering_generated_evaluators [prompt_engineering/generated_evaluators]
        direction TB
        node_398[".gitignore"]
    end
    subgraph dir_prompts [prompts]
        direction TB
        node_356["README.md"]
        node_354["chat-with-bob.txt"]
        node_355["router.txt"]
    end
    subgraph dir_reflection [reflection]
        direction TB
        node_352["README.md"]
        node_351["adaptation_manager.py"]
        node_353["create_reflection.py"]
        node_350["reflect.py"]
    end
    subgraph dir_scripts [scripts]
        direction TB
        node_288["README.md"]
        node_276["agentic_workflow.sh"]
        node_280["analyze_nomad_allocs.py"]
        node_286["ansible_diff.sh"]
        node_293["check_all_playbooks.sh"]
        node_259["check_deps.py"]
        node_273["ci_ansible_check.sh"]
        node_290["cleanup.sh"]
        node_277["compare_exo_llama.py"]
        node_254["create_assistant_prompts.py"]
        node_262["create_cynic_model.sh"]
        node_263["create_todo_issues.sh"]
        node_283["debug_expert.sh"]
        node_257["debug_mesh.sh"]
        node_275["evaluate_clamav.py"]
        node_261["fix_markdown.sh"]
        node_294["fix_verification_failures.sh"]
        node_271["fix_yaml.sh"]
        node_289["generate_assistant_vectors.sh"]
        node_291["generate_file_map.py"]
        node_279["generate_issue_script.py"]
        node_264["generate_signatures.py"]
        node_255["heal_cluster.sh"]
        node_284["healer.py"]
        node_292["lint.sh"]
        node_287["lint_exclude.txt"]
        node_295["memory_audit.py"]
        node_282["profile_resources.sh"]
        node_267["provisioning.py"]
        node_285["prune_consul_services.py"]
        node_256["run_quibbler.sh"]
        node_269["run_tests.sh"]
        node_260["salvage_task.py"]
        node_274["setup_pxe_server.sh"]
        node_278["start_services.sh"]
        node_281["supervisor.py"]
        node_268["test_playbooks_dry_run.sh"]
        node_265["test_playbooks_live_run.sh"]
        node_270["test_swarm_map_reduce.py"]
        node_266["troubleshoot.py"]
        node_272["uninstall.sh"]
        node_258["verify_consul_attributes.sh"]
    end
    subgraph dir_scripts_debug [scripts/debug]
        direction TB
        node_297["README.md"]
        node_296["test_mqtt_connection.py"]
    end
    subgraph dir_tests [tests]
        direction TB
        node_431["README.md"]
        node_426["__init__.py"]
        node_428["test.wav"]
        node_427["test_agent_patterns.py"]
        node_418["test_canvas_integration.py"]
        node_422["test_deep_context.py"]
        node_419["test_emperor_node.py"]
        node_424["test_event_bus.py"]
        node_432["test_experiment_tool.py"]
        node_417["test_gastown_judge.py"]
        node_423["test_gastown_memory.py"]
        node_425["test_gastown_stats.py"]
        node_416["test_imports.py"]
        node_421["test_manager_flow.py"]
        node_420["test_spec_loader.py"]
        node_415["test_ssrf_validation.py"]
        node_429["test_websocket_security.py"]
        node_414["verify_config_load.py"]
        node_430["verify_dlq.py"]
    end
    subgraph dir_tests_e2e [tests/e2e]
        direction TB
        node_533["README.md"]
        node_528["__init__.py"]
        node_529["test_api.py"]
        node_526["test_intelligent_routing.py"]
        node_527["test_mission_control.py"]
        node_531["test_palette_command_history.py"]
        node_532["test_palette_ux.py"]
        node_530["test_regression.py"]
    end
    subgraph dir_tests_integration [tests/integration]
        direction TB
        node_442["README.md"]
        node_435["__init__.py"]
        node_441["stub_services.py"]
        node_434["test_consul_role.yaml"]
        node_436["test_home_assistant.yaml"]
        node_437["test_mini_pipeline.py"]
        node_438["test_mqtt_exporter.py"]
        node_433["test_nomad_role.yaml"]
        node_439["test_pipecat_app.py"]
        node_440["test_preemption.py"]
    end
    subgraph dir_tests_integration_roles_test_home_assistant_tasks [tests/integration/roles/test_home_assistant/tasks]
        direction TB
        node_443["main.yaml"]
    end
    subgraph dir_tests_playbooks [tests/playbooks]
        direction TB
        node_522["e2e-tests.yaml"]
        node_523["test_consul.yaml"]
        node_525["test_llama_cpp.yaml"]
        node_524["test_nomad.yaml"]
    end
    subgraph dir_tests_scripts [tests/scripts]
        direction TB
        node_520["run_unit_tests.sh"]
        node_519["test_duplicate_role_execution.sh"]
        node_521["test_paddler.sh"]
        node_516["test_piper.sh"]
        node_518["test_run.sh"]
        node_517["verify_components.py"]
    end
    subgraph dir_tests_unit [tests/unit]
        direction TB
        node_512["README.md"]
        node_474["__init__.py"]
        node_466["conftest.py"]
        node_472["test_adaptation_manager.py"]
        node_494["test_agent_definitions.py"]
        node_449["test_ansible_tool.py"]
        node_480["test_archivist_tool.py"]
        node_462["test_audio_download_limit.py"]
        node_473["test_autoresearch_tool.py"]
        node_456["test_autoresearch_tool_pathing.py"]
        node_498["test_claude_clone_tool.py"]
        node_493["test_code_runner_security.py"]
        node_482["test_code_runner_timeout.py"]
        node_448["test_code_runner_tool.py"]
        node_508["test_container_registry_security.py"]
        node_513["test_council_tool.py"]
        node_445["test_dependency_scanner.py"]
        node_465["test_desktop_control_tool.py"]
        node_484["test_experiment_tool_security.py"]
        node_447["test_file_editor_security.py"]
        node_496["test_file_editor_tool.py"]
        node_485["test_final_answer_tool.py"]
        node_511["test_gemini_cli.py"]
        node_457["test_get_nomad_job.py"]
        node_458["test_git_tool.py"]
        node_514["test_git_tool_security.py"]
        node_471["test_ha_tool.py"]
        node_491["test_hashline_editor.py"]
        node_464["test_heretic_tool.py"]
        node_499["test_home_assistant_template.py"]
        node_510["test_infrastructure.py"]
        node_475["test_lint_script.py"]
        node_452["test_llxprt_code_tool.py"]
        node_444["test_looped_reasoning_node.py"]
        node_470["test_mcp_tool.py"]
        node_463["test_memory.py"]
        node_481["test_mqtt_template.py"]
        node_454["test_nomad_sandbox.py"]
        node_490["test_open_workers_tool.py"]
        node_450["test_opencode_tool.py"]
        node_460["test_orchestrator_tool.py"]
        node_505["test_personality_tool.py"]
        node_500["test_pipecat_app_unit.py"]
        node_479["test_planner_tool.py"]
        node_487["test_playbook_integration.py"]
        node_477["test_poc_ensemble.py"]
        node_446["test_power_tool.py"]
        node_483["test_project_mapper_tool.py"]
        node_478["test_prompt_engineering.py"]
        node_502["test_prompt_improver_tool.py"]
        node_515["test_provisioning.py"]
        node_451["test_rag_tool.py"]
        node_504["test_reflection.py"]
        node_469["test_search_tool_security.py"]
        node_497["test_security.py"]
        node_461["test_shell_tool.py"]
        node_453["test_shell_tool_security.py"]
        node_459["test_simple_llm_node.py"]
        node_467["test_skill_library.py"]
        node_492["test_smol_agent_tool.py"]
        node_489["test_ssh_tool.py"]
        node_486["test_summarizer_tool.py"]
        node_468["test_supervisor.py"]
        node_509["test_swarm_tool.py"]
        node_506["test_tap_service.py"]
        node_507["test_term_everything_tool.py"]
        node_476["test_vision_failover.py"]
        node_488["test_web_browser_tool.py"]
        node_455["test_web_server_personality.py"]
        node_501["test_web_server_sync.py"]
        node_503["test_workflow.py"]
        node_495["test_world_model_service.py"]
    end
    subgraph dir_workflows [workflows]
        direction TB
        node_298["default_agent_loop.yaml"]
    end

    node_247 --> node_271
    node_20 --> node_374
    node_22 --> node_154
    node_222 --> node_593
    node_772 --> node_771
    node_8 --> node_743
    node_755 --> node_620
    node_828 --> node_719
    node_247 --> node_522
    node_828 --> node_742
    node_229 --> node_716
    node_63 --> node_176
    node_659 --> node_690
    node_775 --> node_155
    node_642 --> node_817
    node_8 --> node_709
    node_17 --> node_58
    node_32 --> node_555
    node_553 --> node_583
    node_11 --> node_604
    node_356 --> node_354
    node_524 --> node_583
    node_842 --> node_821
    node_32 --> node_355
    node_247 --> node_747
    node_55 --> node_75
    node_168 --> node_49
    node_306 --> node_349
    node_357 --> node_632
    node_828 --> node_816
    node_228 --> node_324
    node_427 --> node_49
    node_525 --> node_590
    node_276 --> node_327
    node_98 --> node_100
    node_483 --> node_383
    node_842 --> node_671
    node_170 --> node_145
    node_383 --> node_382
    node_420 --> node_550
    node_460 --> node_151
    node_828 --> node_629
    node_8 --> node_693
    node_654 --> node_829
    node_604 --> node_603
    node_805 --> node_34
    node_654 --> node_854
    node_17 --> node_87
    node_222 --> node_652
    node_291 --> node_827
    node_333 --> node_710
    node_421 --> node_693
    node_228 --> node_297
    node_716 --> node_816
    node_667 --> node_59
    node_222 --> node_533
    node_222 --> node_650
    node_289 --> node_254
    node_228 --> node_650
    node_49 --> node_70
    node_247 --> node_843
    node_63 --> node_162
    node_291 --> node_26
    node_291 --> node_279
    node_13 --> node_348
    node_835 --> node_41
    node_247 --> node_500
    node_831 --> node_832
    node_8 --> node_57
    node_842 --> node_730
    node_238 --> node_298
    node_228 --> node_83
    node_307 --> node_781
    node_102 --> node_99
    node_343 --> node_688
    node_626 --> node_624
    node_383 --> node_378
    node_525 --> node_763
    node_229 --> node_821
    node_11 --> node_600
    node_11 --> node_340
    node_525 --> node_680
    node_228 --> node_819
    node_773 --> node_41
    node_63 --> node_789
    node_307 --> node_591
    node_755 --> node_759
    node_775 --> node_181
    node_599 --> node_597
    node_199 --> node_693
    node_238 --> node_41
    node_340 --> node_787
    node_291 --> node_123
    node_8 --> node_835
    node_229 --> node_692
    node_406 --> node_442
    node_339 --> node_580
    node_13 --> node_329
    node_237 --> node_70
    node_222 --> node_763
    node_222 --> node_327
    node_247 --> node_719
    node_229 --> node_655
    node_640 --> node_642
    node_247 --> node_742
    node_374 --> node_368
    node_32 --> node_4
    node_226 --> node_31
    node_607 --> node_86
    node_247 --> node_640
    node_667 --> node_50
    node_828 --> node_651
    node_842 --> node_647
    node_17 --> node_151
    node_842 --> node_619
    node_11 --> node_821
    node_654 --> node_755
    node_754 --> node_604
    node_2 --> node_235
    node_406 --> node_413
    node_483 --> node_652
    node_218 --> node_777
    node_667 --> node_355
    node_483 --> node_17
    node_617 --> node_609
    node_692 --> node_851
    node_340 --> node_777
    node_32 --> node_374
    node_455 --> node_693
    node_738 --> node_591
    node_247 --> node_673
    node_229 --> node_850
    node_483 --> node_533
    node_654 --> node_687
    node_709 --> node_590
    node_291 --> node_86
    node_483 --> node_577
    node_575 --> node_572
    node_704 --> node_700
    node_229 --> node_730
    node_712 --> node_714
    node_828 --> node_604
    node_11 --> node_671
    node_63 --> node_141
    node_430 --> node_47
    node_247 --> node_816
    node_42 --> node_155
    node_525 --> node_41
    node_654 --> node_734
    node_654 --> node_814
    node_228 --> node_760
    node_228 --> node_699
    node_291 --> node_27
    node_451 --> node_182
    node_47 --> node_179
    node_311 --> node_733
    node_640 --> node_641
    node_247 --> node_786
    node_842 --> node_826
    node_63 --> node_805
    node_247 --> node_629
    node_422 --> node_97
    node_247 --> node_809
    node_229 --> node_722
    node_312 --> node_609
    node_775 --> node_145
    node_506 --> node_171
    node_304 --> node_660
    node_512 --> node_693
    node_307 --> node_843
    node_340 --> node_796
    node_357 --> node_683
    node_820 --> node_609
    node_17 --> node_463
    node_228 --> node_595
    node_222 --> node_41
    node_230 --> node_775
    node_648 --> node_609
    node_544 --> node_540
    node_842 --> node_636
    node_17 --> node_498
    node_654 --> node_824
    node_442 --> node_440
    node_704 --> node_702
    node_11 --> node_730
    node_233 --> node_573
    node_654 --> node_667
    node_329 --> node_590
    node_736 --> node_609
    node_304 --> node_668
    node_181 --> node_34
    node_781 --> node_69
    node_229 --> node_647
    node_117 --> node_127
    node_329 --> node_586
    node_590 --> node_585
    node_343 --> node_629
    node_197 --> node_693
    node_550 --> node_549
    node_578 --> node_609
    node_754 --> node_600
    node_8 --> node_822
    node_340 --> node_785
    node_20 --> node_562
    node_842 --> node_738
    node_754 --> node_588
    node_425 --> node_777
    node_447 --> node_799
    node_341 --> node_338
    node_488 --> node_177
    node_288 --> node_287
    node_828 --> node_600
    node_842 --> node_707
    node_247 --> node_625
    node_57 --> node_70
    node_682 --> node_609
    node_8 --> node_186
    node_333 --> node_713
    node_307 --> node_719
    node_394 --> node_396
    node_406 --> node_400
    node_13 --> node_335
    node_483 --> node_537
    node_755 --> node_829
    node_826 --> node_851
    node_307 --> node_742
    node_17 --> node_446
    node_416 --> node_47
    node_667 --> node_694
    node_755 --> node_854
    node_533 --> node_526
    node_667 --> node_693
    node_294 --> node_31
    node_776 --> node_45
    node_11 --> node_619
    node_11 --> node_647
    node_247 --> node_830
    node_66 --> node_396
    node_251 --> node_641
    node_842 --> node_715
    node_375 --> node_775
    node_228 --> node_326
    node_247 --> node_651
    node_267 --> node_332
    node_754 --> node_821
    node_42 --> node_181
    node_755 --> node_591
    node_100 --> node_132
    node_222 --> node_62
    node_341 --> node_340
    node_692 --> node_51
    node_842 --> node_649
    node_842 --> node_740
    node_506 --> node_796
    node_222 --> node_723
    node_416 --> node_775
    node_512 --> node_499
    node_230 --> node_56
    node_307 --> node_816
    node_290 --> node_4
    node_450 --> node_159
    node_754 --> node_743
    node_525 --> node_622
    node_250 --> node_220
    node_754 --> node_671
    node_337 --> node_558
    node_640 --> node_86
    node_247 --> node_732
    node_307 --> node_629
    node_11 --> node_826
    node_658 --> node_775
    node_667 --> node_57
    node_32 --> node_542
    node_507 --> node_798
    node_828 --> node_743
    node_247 --> node_293
    node_247 --> node_314
    node_842 --> node_749
    node_229 --> node_738
    node_423 --> node_76
    node_615 --> node_609
    node_32 --> node_303
    node_828 --> node_671
    node_100 --> node_99
    node_424 --> node_394
    node_47 --> node_178
    node_13 --> node_339
    node_229 --> node_707
    node_291 --> node_817
    node_63 --> node_168
    node_250 --> node_239
    node_281 --> node_314
    node_525 --> node_759
    node_828 --> node_709
    node_690 --> node_609
    node_11 --> node_636
    node_607 --> node_851
    node_8 --> node_581
    node_228 --> node_605
    node_754 --> node_730
    node_472 --> node_369
    node_63 --> node_159
    node_242 --> node_776
    node_222 --> node_666
    node_229 --> node_715
    node_8 --> node_582
    node_228 --> node_305
    node_11 --> node_738
    node_467 --> node_169
    node_274 --> node_301
    node_276 --> node_550
    node_229 --> node_740
    node_291 --> node_851
    node_743 --> node_568
    node_83 --> node_62
    node_414 --> node_41
    node_755 --> node_687
    node_483 --> node_352
    node_11 --> node_707
    node_247 --> node_639
    node_17 --> node_144
    node_505 --> node_142
    node_247 --> node_127
    node_755 --> node_734
    node_755 --> node_814
    node_590 --> node_588
    node_828 --> node_609
    node_834 --> node_763
    node_222 --> node_675
    node_47 --> node_788
    node_224 --> node_394
    node_251 --> node_351
    node_222 --> node_833
    node_478 --> node_369
    node_229 --> node_749
    node_247 --> node_588
    node_247 --> node_355
    node_208 --> node_775
    node_228 --> node_833
    node_231 --> node_196
    node_291 --> node_37
    node_737 --> node_736
    node_476 --> node_693
    node_307 --> node_651
    node_11 --> node_715
    node_8 --> node_823
    node_13 --> node_334
    node_247 --> node_676
    node_267 --> node_13
    node_406 --> node_250
    node_754 --> node_647
    node_754 --> node_619
    node_32 --> node_562
    node_569 --> node_609
    node_11 --> node_649
    node_738 --> node_585
    node_247 --> node_20
    node_8 --> node_642
    node_828 --> node_619
    node_755 --> node_824
    node_47 --> node_803
    node_47 --> node_798
    node_324 --> node_667
    node_307 --> node_604
    node_318 --> node_762
    node_63 --> node_186
    node_252 --> node_4
    node_842 --> node_626
    node_842 --> node_708
    node_17 --> node_794
    node_775 --> node_801
    node_55 --> node_641
    node_250 --> node_227
    node_70 --> node_45
    node_11 --> node_749
    node_37 --> node_36
    node_228 --> node_737
    node_291 --> node_402
    node_754 --> node_826
    node_828 --> node_835
    node_291 --> node_341
    node_228 --> node_538
    node_47 --> node_182
    node_222 --> node_847
    node_247 --> node_743
    node_291 --> node_396
    node_337 --> node_757
    node_228 --> node_847
    node_647 --> node_645
    node_543 --> node_551
    node_608 --> node_616
    node_369 --> node_375
    node_828 --> node_826
    node_340 --> node_846
    node_222 --> node_550
    node_704 --> node_644
    node_590 --> node_709
    node_818 --> node_609
    node_833 --> node_584
    node_247 --> node_285
    node_20 --> node_544
    node_607 --> node_51
    node_47 --> node_70
    node_754 --> node_636
    node_247 --> node_805
    node_340 --> node_844
    node_247 --> node_709
    node_640 --> node_817
    node_445 --> node_190
    node_415 --> node_53
    node_318 --> node_763
    node_336 --> node_589
    node_522 --> node_436
    node_808 --> node_187
    node_828 --> node_636
    node_150 --> node_563
    node_370 --> node_775
    node_228 --> node_756
    node_340 --> node_776
    node_357 --> node_360
    node_291 --> node_51
    node_251 --> node_87
    node_512 --> node_494
    node_338 --> node_622
    node_342 --> node_683
    node_334 --> node_762
    node_340 --> node_797
    node_8 --> node_838
    node_640 --> node_851
    node_8 --> node_607
    node_525 --> node_591
    node_247 --> node_693
    node_754 --> node_707
    node_307 --> node_600
    node_81 --> node_168
    node_221 --> node_13
    node_229 --> node_708
    node_590 --> node_609
    node_307 --> node_588
    node_11 --> node_839
    node_452 --> node_797
    node_222 --> node_431
    node_477 --> node_97
    node_654 --> node_821
    node_228 --> node_431
    node_247 --> node_609
    node_828 --> node_707
    node_222 --> node_781
    node_63 --> node_137
    node_229 --> node_813
    node_262 --> node_134
    node_776 --> node_778
    node_63 --> node_180
    node_654 --> node_692
    node_754 --> node_649
    node_8 --> node_38
    node_178 --> node_53
    node_334 --> node_763
    node_11 --> node_626
    node_47 --> node_113
    node_654 --> node_655
    node_11 --> node_708
    node_96 --> node_99
    node_291 --> node_352
    node_828 --> node_649
    node_74 --> node_68
    node_482 --> node_190
    node_228 --> node_318
    node_738 --> node_588
    node_383 --> node_379
    node_331 --> node_587
    node_754 --> node_726
    node_307 --> node_743
    node_251 --> node_281
    node_8 --> node_267
    node_333 --> node_769
    node_218 --> node_76
    node_307 --> node_671
    node_17 --> node_148
    node_222 --> node_747
    node_96 --> node_101
    node_247 --> node_835
    node_654 --> node_850
    node_228 --> node_747
    node_406 --> node_297
    node_741 --> node_745
    node_422 --> node_139
    node_654 --> node_730
    node_842 --> node_686
    node_17 --> node_92
    node_8 --> node_731
    node_307 --> node_709
    node_82 --> node_78
    node_755 --> node_604
    node_599 --> node_596
    node_525 --> node_685
    node_775 --> node_174
    node_842 --> node_598
    node_17 --> node_190
    node_247 --> node_499
    node_406 --> node_83
    node_654 --> node_722
    node_20 --> node_297
    node_17 --> node_787
    node_32 --> node_775
    node_63 --> node_152
    node_489 --> node_145
    node_101 --> node_69
    node_63 --> node_135
    node_229 --> node_689
    node_20 --> node_533
    node_526 --> node_47
    node_340 --> node_735
    node_834 --> node_759
    node_202 --> node_53
    node_372 --> node_47
    node_242 --> node_218
    node_459 --> node_94
    node_640 --> node_51
    node_507 --> node_174
    node_228 --> node_13
    node_709 --> node_591
    node_20 --> node_83
    node_32 --> node_38
    node_181 --> node_27
    node_344 --> node_820
    node_52 --> node_56
    node_654 --> node_653
    node_32 --> node_544
    node_148 --> node_180
    node_8 --> node_49
    node_332 --> node_608
    node_692 --> node_777
    node_51 --> node_644
    node_417 --> node_694
    node_300 --> node_39
    node_654 --> node_647
    node_543 --> node_13
    node_228 --> node_750
    node_590 --> node_583
    node_382 --> node_641
    node_754 --> node_839
    node_729 --> node_541
    node_17 --> node_777
    node_442 --> node_439
    node_339 --> node_844
    node_63 --> node_799
    node_242 --> node_608
    node_340 --> node_722
    node_828 --> node_839
    node_842 --> node_593
    node_425 --> node_76
    node_229 --> node_686
    node_754 --> node_637
    node_222 --> node_601
    node_340 --> node_804
    node_47 --> node_191
    node_228 --> node_601
    node_343 --> node_630
    node_512 --> node_775
    node_278 --> node_568
    node_318 --> node_584
    node_307 --> node_619
    node_203 --> node_47
    node_8 --> node_87
    node_20 --> node_327
    node_187 --> node_808
    node_536 --> node_535
    node_120 --> node_126
    node_229 --> node_598
    node_329 --> node_591
    node_754 --> node_626
    node_396 --> node_397
    node_754 --> node_708
    node_122 --> node_4
    node_292 --> node_329
    node_658 --> node_62
    node_17 --> node_170
    node_247 --> node_822
    node_17 --> node_796
    node_222 --> node_742
    node_421 --> node_87
    node_340 --> node_619
    node_17 --> node_42
    node_222 --> node_640
    node_185 --> node_775
    node_247 --> node_442
    node_828 --> node_626
    node_307 --> node_835
    node_775 --> node_800
    node_754 --> node_823
    node_458 --> node_180
    node_281 --> node_303
    node_544 --> node_543
    node_11 --> node_686
    node_307 --> node_826
    node_267 --> node_330
    node_333 --> node_770
    node_222 --> node_673
    node_771 --> node_766
    node_32 --> node_745
    node_233 --> node_568
    node_247 --> node_413
    node_374 --> node_369
    node_828 --> node_823
    node_333 --> node_768
    node_755 --> node_821
    node_17 --> node_785
    node_11 --> node_598
    node_222 --> node_816
    node_364 --> node_641
    node_8 --> node_443
    node_654 --> node_738
    node_8 --> node_819
    node_304 --> node_667
    node_446 --> node_790
    node_307 --> node_636
    node_340 --> node_806
    node_229 --> node_593
    node_654 --> node_707
    node_755 --> node_671
    node_229 --> node_849
    node_698 --> node_697
    node_754 --> node_691
    node_842 --> node_650
    node_789 --> node_808
    node_406 --> node_341
    node_525 --> node_585
    node_525 --> node_757
    node_558 --> node_576
    node_14 --> node_644
    node_271 --> node_33
    node_143 --> node_310
    node_340 --> node_674
    node_525 --> node_625
    node_654 --> node_715
    node_228 --> node_828
    node_481 --> node_706
    node_330 --> node_593
    node_429 --> node_66
    node_450 --> node_791
    node_676 --> node_677
    node_170 --> node_786
    node_32 --> node_297
    node_553 --> node_584
    node_49 --> node_63
    node_307 --> node_707
    node_238 --> node_644
    node_226 --> node_537
    node_654 --> node_740
    node_842 --> node_594
    node_465 --> node_176
    node_8 --> node_851
    node_340 --> node_738
    node_760 --> node_763
    node_43 --> node_795
    node_478 --> node_47
    node_11 --> node_593
    node_755 --> node_730
    node_693 --> node_694
    node_228 --> node_698
    node_8 --> node_371
    node_247 --> node_581
    node_340 --> node_707
    node_8 --> node_760
    node_8 --> node_699
    node_32 --> node_83
    node_247 --> node_494
    node_500 --> node_66
    node_575 --> node_570
    node_222 --> node_625
    node_654 --> node_749
    node_228 --> node_325
    node_476 --> node_641
    node_554 --> node_41
    node_693 --> node_609
    node_842 --> node_763
    node_40 --> node_38
    node_247 --> node_582
    node_223 --> node_369
    node_307 --> node_649
    node_500 --> node_641
    node_422 --> node_110
    node_687 --> node_688
    node_230 --> node_122
    node_83 --> node_68
    node_222 --> node_830
    node_121 --> node_125
    node_229 --> node_725
    node_242 --> node_637
    node_247 --> node_400
    node_228 --> node_830
    node_63 --> node_791
    node_229 --> node_590
    node_195 --> node_693
    node_8 --> node_595
    node_338 --> node_624
    node_340 --> node_748
    node_738 --> node_583
    node_209 --> node_641
    node_340 --> node_740
    node_815 --> node_62
    node_35 --> node_166
    node_267 --> node_693
    node_288 --> node_273
    node_268 --> node_339
    node_117 --> node_123
    node_420 --> node_442
    node_754 --> node_686
    node_755 --> node_619
    node_755 --> node_647
    node_32 --> node_327
    node_300 --> node_762
    node_291 --> node_10
    node_247 --> node_823
    node_331 --> node_590
    node_238 --> node_355
    node_222 --> node_732
    node_229 --> node_594
    node_332 --> node_827
    node_263 --> node_369
    node_8 --> node_668
    node_332 --> node_613
    node_340 --> node_749
    node_754 --> node_598
    node_511 --> node_794
    node_224 --> node_43
    node_512 --> node_798
    node_228 --> node_293
    node_247 --> node_642
    node_11 --> node_650
    node_222 --> node_691
    node_14 --> node_90
    node_709 --> node_585
    node_228 --> node_726
    node_228 --> node_691
    node_242 --> node_827
    node_279 --> node_8
    node_755 --> node_826
    node_14 --> node_76
    node_229 --> node_763
    node_288 --> node_283
    node_330 --> node_594
    node_8 --> node_672
    node_8 --> node_853
    node_228 --> node_744
    node_291 --> node_541
    node_544 --> node_548
    node_667 --> node_87
    node_229 --> node_680
    node_512 --> node_182
    node_398 --> node_1
    node_238 --> node_90
    node_544 --> node_546
    node_339 --> node_835
    node_47 --> node_81
    node_300 --> node_763
    node_11 --> node_594
    node_294 --> node_537
    node_424 --> node_693
    node_42 --> node_60
    node_288 --> node_269
    node_525 --> node_588
    node_755 --> node_636
    node_500 --> node_47
    node_498 --> node_144
    node_582 --> node_580
    node_307 --> node_839
    node_754 --> node_593
    node_4 --> node_541
    node_63 --> node_182
    node_833 --> node_585
    node_654 --> node_708
    node_775 --> node_809
    node_63 --> node_151
    node_809 --> node_609
    node_501 --> node_775
    node_11 --> node_763
    node_291 --> node_28
    node_692 --> node_219
    node_687 --> node_673
    node_755 --> node_738
    node_579 --> node_609
    node_300 --> node_760
    node_432 --> node_641
    node_603 --> node_576
    node_654 --> node_813
    node_677 --> node_123
    node_247 --> node_678
    node_228 --> node_717
    node_8 --> node_620
    node_465 --> node_466
    node_755 --> node_707
    node_784 --> node_17
    node_57 --> node_63
    node_247 --> node_39
    node_247 --> node_838
    node_228 --> node_716
    node_222 --> node_676
    node_242 --> node_47
    node_406 --> node_538
    node_307 --> node_626
    node_340 --> node_637
    node_737 --> node_609
    node_229 --> node_41
    node_247 --> node_607
    node_351 --> node_350
    node_468 --> node_314
    node_692 --> node_776
    node_842 --> node_723
    node_667 --> node_817
    node_8 --> node_605
    node_210 --> node_693
    node_247 --> node_250
    node_335 --> node_684
    node_420 --> node_400
    node_276 --> node_4
    node_281 --> node_39
    node_41 --> node_38
    node_667 --> node_281
    node_755 --> node_715
    node_238 --> node_4
    node_340 --> node_708
    node_307 --> node_823
    node_393 --> node_392
    node_35 --> node_154
    node_268 --> node_286
    node_20 --> node_538
    node_340 --> node_792
    node_755 --> node_649
    node_667 --> node_70
    node_17 --> node_797
    node_755 --> node_740
    node_229 --> node_842
    node_231 --> node_87
    node_20 --> node_550
    node_667 --> node_576
    node_228 --> node_300
    node_343 --> node_39
    node_247 --> node_38
    node_369 --> node_47
    node_422 --> node_94
    node_169 --> node_44
    node_754 --> node_650
    node_608 --> node_610
    node_17 --> node_458
    node_755 --> node_749
    node_444 --> node_94
    node_340 --> node_779
    node_17 --> node_528
    node_760 --> node_759
    node_83 --> node_219
    node_828 --> node_650
    node_739 --> node_707
    node_248 --> node_817
    node_222 --> node_709
    node_247 --> node_286
    node_842 --> node_666
    node_291 --> node_356
    node_273 --> node_268
    node_483 --> node_555
    node_568 --> node_609
    node_654 --> node_689
    node_709 --> node_588
    node_47 --> node_177
    node_457 --> node_793
    node_826 --> node_219
    node_754 --> node_594
    node_381 --> node_369
    node_822 --> node_820
    node_834 --> node_757
    node_212 --> node_66
    node_263 --> node_48
    node_781 --> node_219
    node_229 --> node_723
    node_247 --> node_731
    node_343 --> node_38
    node_814 --> node_812
    node_247 --> node_643
    node_828 --> node_819
    node_221 --> node_369
    node_327 --> node_319
    node_544 --> node_547
    node_47 --> node_786
    node_20 --> node_431
    node_222 --> node_693
    node_324 --> node_656
    node_560 --> node_644
    node_842 --> node_675
    node_8 --> node_737
    node_842 --> node_833
    node_247 --> node_628
    node_231 --> node_182
    node_322 --> node_635
    node_754 --> node_763
    node_826 --> node_776
    node_288 --> node_4
    node_17 --> node_76
    node_299 --> node_38
    node_8 --> node_847
    node_228 --> node_692
    node_307 --> node_39
    node_287 --> node_123
    node_523 --> node_763
    node_603 --> node_602
    node_781 --> node_776
    node_833 --> node_588
    node_471 --> node_787
    node_654 --> node_686
    node_667 --> node_52
    node_676 --> node_674
    node_667 --> node_560
    node_467 --> node_44
    node_63 --> node_802
    node_218 --> node_47
    node_656 --> node_52
    node_11 --> node_723
    node_123 --> node_678
    node_325 --> node_41
    node_66 --> node_75
    node_222 --> node_575
    node_755 --> node_839
    node_228 --> node_575
    node_215 --> node_90
    node_223 --> node_66
    node_654 --> node_598
    node_86 --> node_394
    node_251 --> node_568
    node_336 --> node_586
    node_716 --> node_817
    node_601 --> node_814
    node_518 --> node_817
    node_574 --> node_609
    node_8 --> node_372
    node_315 --> node_339
    node_8 --> node_756
    node_47 --> node_164
    node_343 --> node_628
    node_373 --> node_775
    node_776 --> node_779
    node_746 --> node_745
    node_420 --> node_250
    node_607 --> node_219
    node_828 --> node_760
    node_229 --> node_759
    node_263 --> node_637
    node_755 --> node_626
    node_755 --> node_708
    node_307 --> node_598
    node_247 --> node_87
    node_318 --> node_585
    node_324 --> node_659
    node_340 --> node_686
    node_692 --> node_690
    node_229 --> node_675
    node_32 --> node_108
    node_238 --> node_367
    node_339 --> node_645
    node_340 --> node_782
    node_178 --> node_41
    node_607 --> node_776
    node_83 --> node_75
    node_32 --> node_551
    node_247 --> node_297
    node_828 --> node_595
    node_757 --> node_4
    node_11 --> node_666
    node_331 --> node_759
    node_32 --> node_538
    node_212 --> node_47
    node_437 --> node_47
    node_654 --> node_593
    node_17 --> node_804
    node_63 --> node_144
    node_654 --> node_849
    node_337 --> node_761
    node_190 --> node_609
    node_337 --> node_39
    node_47 --> node_176
    node_32 --> node_550
    node_47 --> node_63
    node_517 --> node_31
    node_64 --> node_45
    node_117 --> node_396
    node_247 --> node_83
    node_353 --> node_394
    node_293 --> node_314
    node_525 --> node_583
    node_206 --> node_177
    node_291 --> node_269
    node_222 --> node_288
    node_291 --> node_512
    node_228 --> node_288
    node_11 --> node_675
    node_247 --> node_443
    node_233 --> node_4
    node_462 --> node_641
    node_247 --> node_819
    node_11 --> node_833
    node_100 --> node_355
    node_117 --> node_121
    node_268 --> node_343
    node_342 --> node_685
    node_544 --> node_541
    node_842 --> node_781
    node_63 --> node_156
    node_554 --> node_688
    node_739 --> node_708
    node_422 --> node_90
    node_326 --> node_775
    node_453 --> node_164
    node_304 --> node_658
    node_334 --> node_757
    node_98 --> node_102
    node_247 --> node_182
    node_247 --> node_817
    node_249 --> node_41
    node_318 --> node_758
    node_324 --> node_657
    node_223 --> node_47
    node_267 --> node_339
    node_852 --> node_609
    node_291 --> node_555
    node_242 --> node_222
    node_337 --> node_38
    node_83 --> node_65
    node_13 --> node_331
    node_776 --> node_775
    node_754 --> node_723
    node_342 --> node_682
    node_198 --> node_47
    node_13 --> node_337
    node_63 --> node_139
    node_32 --> node_431
    node_687 --> node_671
    node_343 --> node_634
    node_492 --> node_789
    node_605 --> node_644
    node_17 --> node_806
    node_681 --> node_679
    node_739 --> node_587
    node_247 --> node_576
    node_247 --> node_851
    node_552 --> node_541
    node_654 --> node_725
    node_692 --> node_218
    node_496 --> node_175
    node_448 --> node_809
    node_222 --> node_822
    node_654 --> node_590
    node_775 --> node_694
    node_267 --> node_641
    node_261 --> node_31
    node_228 --> node_822
    node_345 --> node_609
    node_373 --> node_382
    node_475 --> node_287
    node_842 --> node_747
    node_222 --> node_442
    node_8 --> node_13
    node_228 --> node_442
    node_247 --> node_328
    node_247 --> node_699
    node_198 --> node_775
    node_17 --> node_74
    node_247 --> node_760
    node_250 --> node_247
    node_172 --> node_168
    node_263 --> node_47
    node_85 --> node_80
    node_217 --> node_642
    node_340 --> node_746
    node_667 --> node_566
    node_17 --> node_98
    node_498 --> node_785
    node_8 --> node_750
    node_32 --> node_318
    node_692 --> node_608
    node_222 --> node_413
    node_513 --> node_802
    node_228 --> node_413
    node_229 --> node_781
    node_339 --> node_39
    node_654 --> node_594
    node_307 --> node_650
    node_640 --> node_219
    node_118 --> node_127
    node_333 --> node_712
    node_304 --> node_661
    node_8 --> node_370
    node_754 --> node_666
    node_247 --> node_595
    node_343 --> node_851
    node_276 --> node_400
    node_263 --> node_775
    node_674 --> node_677
    node_755 --> node_686
    node_828 --> node_605
    node_247 --> node_33
    node_833 --> node_589
    node_229 --> node_591
    node_420 --> node_297
    node_8 --> node_601
    node_117 --> node_125
    node_828 --> node_666
    node_612 --> node_609
    node_755 --> node_598
    node_654 --> node_763
    node_222 --> node_552
    node_195 --> node_775
    node_842 --> node_843
    node_228 --> node_552
    node_228 --> node_845
    node_307 --> node_819
    node_640 --> node_776
    node_654 --> node_680
    node_523 --> node_759
    node_46 --> node_70
    node_247 --> node_668
    node_420 --> node_83
    node_754 --> node_675
    node_247 --> node_341
    node_754 --> node_833
    node_11 --> node_781
    node_247 --> node_560
    node_331 --> node_591
    node_720 --> node_573
    node_590 --> node_706
    node_754 --> node_753
    node_17 --> node_149
    node_335 --> node_679
    node_47 --> node_141
    node_357 --> node_4
    node_477 --> node_94
    node_538 --> node_31
    node_828 --> node_833
    node_468 --> node_303
    node_32 --> node_13
    node_66 --> node_53
    node_307 --> node_763
    node_485 --> node_782
    node_833 --> node_583
    node_483 --> node_784
    node_267 --> node_315
    node_402 --> node_4
    node_826 --> node_218
    node_47 --> node_805
    node_247 --> node_672
    node_247 --> node_853
    node_222 --> node_581
    node_781 --> node_218
    node_228 --> node_654
    node_228 --> node_581
    node_525 --> node_626
    node_247 --> node_326
    node_291 --> node_374
    node_321 --> node_564
    node_340 --> node_763
    node_83 --> node_608
    node_430 --> node_693
    node_842 --> node_719
    node_755 --> node_593
    node_842 --> node_742
    node_222 --> node_582
    node_230 --> node_693
    node_842 --> node_640
    node_515 --> node_28
    node_8 --> node_667
    node_281 --> node_326
    node_826 --> node_608
    node_11 --> node_747
    node_307 --> node_760
    node_13 --> node_333
    node_223 --> node_132
    node_228 --> node_557
    node_222 --> node_400
    node_247 --> node_292
    node_754 --> node_847
    node_210 --> node_641
    node_781 --> node_608
    node_828 --> node_737
    node_291 --> node_310
    node_424 --> node_775
    node_229 --> node_843
    node_47 --> node_75
    node_63 --> node_190
    node_340 --> node_312
    node_842 --> node_673
    node_849 --> node_642
    node_828 --> node_847
    node_63 --> node_787
    node_8 --> node_828
    node_842 --> node_816
    node_291 --> node_34
    node_340 --> node_780
    node_63 --> node_142
    node_228 --> node_393
    node_228 --> node_217
    node_590 --> node_584
    node_247 --> node_620
    node_382 --> node_368
    node_654 --> node_842
    node_842 --> node_629
    node_228 --> node_751
    node_307 --> node_41
    node_333 --> node_714
    node_65 --> node_394
    node_196 --> node_182
    node_781 --> node_53
    node_8 --> node_698
    node_483 --> node_562
    node_607 --> node_218
    node_667 --> node_81
    node_228 --> node_646
    node_247 --> node_605
    node_406 --> node_40
    node_11 --> node_843
    node_217 --> node_86
    node_375 --> node_693
    node_291 --> node_31
    node_640 --> node_567
    node_229 --> node_719
    node_760 --> node_757
    node_250 --> node_233
    node_304 --> node_659
    node_743 --> node_746
    node_13 --> node_349
    node_229 --> node_742
    node_406 --> node_32
    node_636 --> node_637
    node_375 --> node_609
    node_755 --> node_650
    node_147 --> node_817
    node_221 --> node_47
    node_416 --> node_693
    node_621 --> node_34
    node_754 --> node_781
    node_340 --> node_783
    node_607 --> node_608
    node_642 --> node_47
    node_831 --> node_830
    node_247 --> node_246
    node_237 --> node_641
    node_654 --> node_723
    node_550 --> node_547
    node_337 --> node_760
    node_276 --> node_544
    node_340 --> node_801
    node_315 --> node_343
    node_229 --> node_673
    node_291 --> node_840
    node_239 --> node_301
    node_17 --> node_66
    node_66 --> node_67
    node_222 --> node_641
    node_483 --> node_400
    node_571 --> node_369
    node_658 --> node_693
    node_692 --> node_641
    node_842 --> node_625
    node_229 --> node_816
    node_775 --> node_790
    node_17 --> node_465
    node_667 --> node_777
    node_268 --> node_319
    node_755 --> node_594
    node_418 --> node_93
    node_11 --> node_719
    node_518 --> node_354
    node_229 --> node_629
    node_11 --> node_742
    node_47 --> node_168
    node_119 --> node_298
    node_11 --> node_640
    node_307 --> node_723
    node_692 --> node_827
    node_842 --> node_830
    node_13 --> node_338
    node_318 --> node_589
    node_404 --> node_407
    node_8 --> node_726
    node_8 --> node_691
    node_704 --> node_62
    node_842 --> node_651
    node_754 --> node_747
    node_222 --> node_838
    node_288 --> node_572
    node_63 --> node_177
    node_339 --> node_819
    node_63 --> node_785
    node_83 --> node_642
    node_228 --> node_334
    node_228 --> node_838
    node_222 --> node_607
    node_11 --> node_673
    node_235 --> node_123
    node_340 --> node_723
    node_8 --> node_744
    node_228 --> node_607
    node_246 --> node_266
    node_247 --> node_737
    node_304 --> node_657
    node_47 --> node_102
    node_223 --> node_298
    node_362 --> node_273
    node_525 --> node_38
    node_324 --> node_660
    node_63 --> node_172
    node_828 --> node_747
    node_247 --> node_319
    node_222 --> node_250
    node_11 --> node_816
    node_247 --> node_538
    node_228 --> node_250
    node_228 --> node_320
    node_17 --> node_155
    node_247 --> node_847
    node_842 --> node_732
    node_4 --> node_367
    node_337 --> node_560
    node_477 --> node_90
    node_11 --> node_629
    node_13 --> node_340
    node_228 --> node_345
    node_654 --> node_759
    node_228 --> node_579
    node_338 --> node_626
    node_318 --> node_583
    node_621 --> node_8
    node_654 --> node_675
    node_83 --> node_641
    node_307 --> node_666
    node_849 --> node_86
    node_329 --> node_587
    node_8 --> node_219
    node_291 --> node_48
    node_394 --> node_123
    node_560 --> node_637
    node_247 --> node_756
    node_692 --> node_47
    node_331 --> node_585
    node_8 --> node_717
    node_331 --> node_757
    node_848 --> node_609
    node_8 --> node_716
    node_781 --> node_641
    node_66 --> node_123
    node_83 --> node_827
    node_17 --> node_47
    node_154 --> node_609
    node_229 --> node_651
    node_640 --> node_218
    node_738 --> node_584
    node_828 --> node_750
    node_8 --> node_776
    node_247 --> node_362
    node_332 --> node_614
    node_340 --> node_759
    node_263 --> node_41
    node_307 --> node_833
    node_826 --> node_827
    node_222 --> node_731
    node_288 --> node_284
    node_291 --> node_562
    node_333 --> node_774
    node_11 --> node_625
    node_781 --> node_827
    node_553 --> node_589
    node_222 --> node_815
    node_406 --> node_575
    node_229 --> node_604
    node_340 --> node_675
    node_276 --> node_297
    node_228 --> node_815
    node_84 --> node_76
    node_294 --> node_677
    node_343 --> node_756
    node_755 --> node_842
    node_251 --> node_369
    node_330 --> node_651
    node_687 --> node_603
    node_828 --> node_601
    node_621 --> node_48
    node_842 --> node_600
    node_13 --> node_342
    node_222 --> node_628
    node_330 --> node_592
    node_607 --> node_637
    node_640 --> node_608
    node_842 --> node_588
    node_17 --> node_173
    node_228 --> node_628
    node_754 --> node_742
    node_11 --> node_830
    node_231 --> node_42
    node_333 --> node_711
    node_442 --> node_47
    node_379 --> node_609
    node_754 --> node_640
    node_217 --> node_851
    node_11 --> node_651
    node_842 --> node_676
    node_276 --> node_83
    node_381 --> node_281
    node_561 --> node_280
    node_20 --> node_575
    node_300 --> node_758
    node_17 --> node_181
    node_772 --> node_770
    node_247 --> node_350
    node_307 --> node_737
    node_247 --> node_318
    node_291 --> node_637
    node_828 --> node_640
    node_754 --> node_673
    node_370 --> node_693
    node_772 --> node_768
    node_480 --> node_807
    node_483 --> node_544
    node_307 --> node_847
    node_754 --> node_816
    node_172 --> node_47
    node_11 --> node_732
    node_828 --> node_673
    node_268 --> node_13
    node_755 --> node_723
    node_754 --> node_629
    node_414 --> node_39
    node_420 --> node_538
    node_764 --> node_295
    node_842 --> node_743
    node_247 --> node_368
    node_607 --> node_827
    node_795 --> node_57
    node_98 --> node_97
    node_775 --> node_179
    node_83 --> node_86
    node_11 --> node_302
    node_525 --> node_762
    node_699 --> node_695
    node_291 --> node_554
    node_302 --> node_717
    node_51 --> node_62
    node_47 --> node_137
    node_667 --> node_63
    node_302 --> node_716
    node_229 --> node_600
    node_654 --> node_781
    node_56 --> node_53
    node_291 --> node_428
    node_406 --> node_288
    node_826 --> node_86
    node_842 --> node_709
    node_229 --> node_588
    node_8 --> node_692
    node_47 --> node_180
    node_222 --> node_297
    node_781 --> node_86
    node_247 --> node_13
    node_654 --> node_591
    node_228 --> node_681
    node_8 --> node_655
    node_17 --> node_158
    node_340 --> node_793
    node_20 --> node_288
    node_247 --> node_750
    node_156 --> node_66
    node_222 --> node_83
    node_331 --> node_588
    node_755 --> node_666
    node_523 --> node_757
    node_754 --> node_625
    node_340 --> node_800
    node_340 --> node_736
    node_156 --> node_641
    node_828 --> node_698
    node_8 --> node_850
    node_222 --> node_443
    node_222 --> node_819
    node_228 --> node_443
    node_11 --> node_588
    node_420 --> node_431
    node_340 --> node_781
    node_552 --> node_34
    node_247 --> node_601
    node_828 --> node_625
    node_315 --> node_319
    node_229 --> node_743
    node_11 --> node_676
    node_217 --> node_51
    node_754 --> node_830
    node_165 --> node_793
    node_849 --> node_851
    node_339 --> node_666
    node_229 --> node_671
    node_755 --> node_675
    node_222 --> node_817
    node_47 --> node_67
    node_8 --> node_453
    node_247 --> node_755
    node_8 --> node_722
    node_247 --> node_42
    node_519 --> node_28
    node_754 --> node_651
    node_755 --> node_833
    node_223 --> node_108
    node_228 --> node_281
    node_32 --> node_693
    node_828 --> node_830
    node_63 --> node_797
    node_83 --> node_87
    node_525 --> node_760
    node_228 --> node_725
    node_47 --> node_135
    node_229 --> node_709
    node_247 --> node_687
    node_230 --> node_641
    node_406 --> node_840
    node_228 --> node_590
    node_47 --> node_66
    node_255 --> node_307
    node_307 --> node_747
    node_673 --> node_609
    node_8 --> node_419
    node_20 --> node_238
    node_754 --> node_732
    node_819 --> node_818
    node_483 --> node_297
    node_20 --> node_442
    node_512 --> node_805
    node_251 --> node_48
    node_32 --> node_307
    node_339 --> node_833
    node_493 --> node_809
    node_8 --> node_168
    node_340 --> node_747
    node_11 --> node_743
    node_8 --> node_369
    node_654 --> node_843
    node_471 --> node_149
    node_218 --> node_45
    node_32 --> node_575
    node_828 --> node_732
    node_842 --> node_835
    node_222 --> node_599
    node_517 --> node_537
    node_222 --> node_760
    node_222 --> node_699
    node_14 --> node_62
    node_228 --> node_599
    node_292 --> node_28
    node_228 --> node_328
    node_339 --> node_664
    node_544 --> node_542
    node_483 --> node_83
    node_20 --> node_413
    node_223 --> node_394
    node_406 --> node_552
    node_11 --> node_709
    node_228 --> node_37
    node_343 --> node_687
    node_495 --> node_641
    node_828 --> node_691
    node_225 --> node_96
    node_96 --> node_136
    node_238 --> node_62
    node_247 --> node_667
    node_291 --> node_544
    node_340 --> node_618
    node_454 --> node_809
    node_247 --> node_220
    node_432 --> node_172
    node_828 --> node_744
    node_430 --> node_775
    node_442 --> node_436
    node_222 --> node_595
    node_640 --> node_827
    node_235 --> node_396
    node_20 --> node_552
    node_83 --> node_817
    node_383 --> node_380
    node_318 --> node_761
    node_847 --> node_846
    node_32 --> node_321
    node_247 --> node_828
    node_525 --> node_684
    node_417 --> node_777
    node_654 --> node_719
    node_185 --> node_693
    node_229 --> node_619
    node_235 --> node_121
    node_483 --> node_327
    node_512 --> node_196
    node_654 --> node_742
    node_291 --> node_383
    node_263 --> node_394
    node_610 --> node_609
    node_8 --> node_218
    node_383 --> node_377
    node_222 --> node_668
    node_228 --> node_402
    node_228 --> node_308
    node_222 --> node_341
    node_228 --> node_668
    node_238 --> node_15
    node_247 --> node_698
    node_307 --> node_601
    node_228 --> node_341
    node_333 --> node_773
    node_559 --> node_763
    node_601 --> node_813
    node_83 --> node_851
    node_658 --> node_641
    node_849 --> node_51
    node_222 --> node_831
    node_654 --> node_673
    node_229 --> node_835
    node_261 --> node_537
    node_276 --> node_398
    node_228 --> node_831
    node_754 --> node_676
    node_775 --> node_788
    node_406 --> node_557
    node_230 --> node_267
    node_32 --> node_288
    node_425 --> node_45
    node_828 --> node_717
    node_654 --> node_816
    node_270 --> node_168
    node_229 --> node_826
    node_251 --> node_66
    node_343 --> node_828
    node_755 --> node_781
    node_8 --> node_608
    node_222 --> node_672
    node_222 --> node_853
    node_307 --> node_640
    node_781 --> node_851
    node_828 --> node_676
    node_228 --> node_672
    node_228 --> node_853
    node_228 --> node_313
    node_288 --> node_276
    node_350 --> node_41
    node_654 --> node_629
    node_667 --> node_75
    node_35 --> node_87
    node_228 --> node_754
    node_250 --> node_229
    node_406 --> node_393
    node_362 --> node_367
    node_340 --> node_742
    node_364 --> node_375
    node_406 --> node_217
    node_640 --> node_47
    node_842 --> node_822
    node_307 --> node_673
    node_340 --> node_640
    node_775 --> node_798
    node_775 --> node_803
    node_20 --> node_400
    node_229 --> node_636
    node_229 --> node_301
    node_499 --> node_736
    node_11 --> node_835
    node_422 --> node_99
    node_525 --> node_584
    node_8 --> node_845
    node_698 --> node_695
    node_340 --> node_673
    node_8 --> node_740
    node_32 --> node_364
    node_263 --> node_522
    node_17 --> node_783
    node_47 --> node_782
    node_63 --> node_804
    node_63 --> node_140
    node_85 --> node_72
    node_263 --> node_278
    node_340 --> node_816
    node_775 --> node_182
    node_755 --> node_747
    node_276 --> node_1
    node_422 --> node_101
    node_754 --> node_709
    node_17 --> node_801
    node_222 --> node_620
    node_247 --> node_726
    node_247 --> node_691
    node_228 --> node_620
    node_483 --> node_395
    node_32 --> node_442
    node_340 --> node_809
    node_66 --> node_73
    node_208 --> node_641
    node_444 --> node_101
    node_806 --> node_777
    node_834 --> node_762
    node_247 --> node_744
    node_291 --> node_652
    node_654 --> node_625
    node_538 --> node_537
    node_8 --> node_654
    node_238 --> node_108
    node_222 --> node_605
    node_349 --> node_829
    node_291 --> node_533
    node_291 --> node_577
    node_32 --> node_413
    node_182 --> node_694
    node_276 --> node_538
    node_739 --> node_591
    node_228 --> node_352
    node_47 --> node_97
    node_47 --> node_100
    node_230 --> node_87
    node_247 --> node_40
    node_42 --> node_145
    node_307 --> node_698
    node_315 --> node_331
    node_229 --> node_649
    node_654 --> node_651
    node_442 --> node_433
    node_468 --> node_326
    node_83 --> node_51
    node_755 --> node_843
    node_307 --> node_625
    node_47 --> node_87
    node_251 --> node_47
    node_502 --> node_810
    node_693 --> node_777
    node_247 --> node_32
    node_340 --> node_757
    node_129 --> node_298
    node_32 --> node_552
    node_63 --> node_806
    node_46 --> node_63
    node_247 --> node_219
    node_333 --> node_766
    node_826 --> node_51
    node_723 --> node_721
    node_842 --> node_581
    node_654 --> node_604
    node_781 --> node_51
    node_247 --> node_717
    node_307 --> node_830
    node_330 --> node_649
    node_374 --> node_373
    node_500 --> node_90
    node_247 --> node_716
    node_8 --> node_751
    node_116 --> node_563
    node_494 --> node_382
    node_842 --> node_582
    node_11 --> node_822
    node_291 --> node_327
    node_148 --> node_804
    node_204 --> node_161
    node_247 --> node_776
    node_340 --> node_807
    node_8 --> node_646
    node_538 --> node_534
    node_55 --> node_66
    node_709 --> node_584
    node_370 --> node_641
    node_350 --> node_165
    node_276 --> node_431
    node_834 --> node_760
    node_754 --> node_835
    node_307 --> node_732
    node_755 --> node_719
    node_8 --> node_67
    node_20 --> node_250
    node_335 --> node_578
    node_364 --> node_369
    node_755 --> node_742
    node_47 --> node_69
    node_222 --> node_737
    node_755 --> node_640
    node_32 --> node_9
    node_509 --> node_795
    node_340 --> node_778
    node_17 --> node_474
    node_291 --> node_537
    node_222 --> node_538
    node_307 --> node_691
    node_611 --> node_609
    node_842 --> node_823
    node_8 --> node_66
    node_480 --> node_186
    node_42 --> node_803
    node_42 --> node_798
    node_575 --> node_576
    node_755 --> node_673
    node_32 --> node_400
    node_231 --> node_140
    node_47 --> node_151
    node_340 --> node_644
    node_501 --> node_693
    node_575 --> node_573
    node_340 --> node_795
    node_340 --> node_677
    node_501 --> node_75
    node_8 --> node_641
    node_267 --> node_331
    node_121 --> node_128
    node_63 --> node_811
    node_729 --> node_551
    node_755 --> node_816
    node_347 --> node_596
    node_406 --> node_410
    node_8 --> node_813
    node_229 --> node_839
    node_639 --> node_609
    node_654 --> node_600
    node_329 --> node_584
    node_554 --> node_39
    node_559 --> node_759
    node_560 --> node_62
    node_828 --> node_588
    node_421 --> node_641
    node_620 --> node_621
    node_755 --> node_629
    node_654 --> node_588
    node_14 --> node_45
    node_458 --> node_804
    node_17 --> node_448
    node_63 --> node_149
    node_222 --> node_756
    node_8 --> node_827
    node_17 --> node_174
    node_318 --> node_586
    node_721 --> node_609
    node_420 --> node_40
    node_340 --> node_638
    node_229 --> node_626
    node_449 --> node_805
    node_247 --> node_75
    node_687 --> node_602
    node_242 --> node_693
    node_11 --> node_581
    node_66 --> node_118
    node_318 --> node_760
    node_199 --> node_66
    node_516 --> node_21
    node_667 --> node_53
    node_247 --> node_692
    node_437 --> node_441
    node_554 --> node_38
    node_420 --> node_32
    node_307 --> node_676
    node_231 --> node_806
    node_337 --> node_758
    node_229 --> node_823
    node_8 --> node_579
    node_199 --> node_641
    node_11 --> node_582
    node_55 --> node_47
    node_247 --> node_655
    node_483 --> node_538
    node_658 --> node_817
    node_654 --> node_743
    node_340 --> node_789
    node_406 --> node_383
    node_754 --> node_822
    node_247 --> node_575
    node_654 --> node_671
    node_340 --> node_676
    node_755 --> node_625
    node_483 --> node_550
    node_842 --> node_838
    node_32 --> node_641
    node_288 --> node_271
    node_842 --> node_607
    node_17 --> node_394
    node_828 --> node_822
    node_8 --> node_689
    node_369 --> node_693
    node_654 --> node_709
    node_455 --> node_66
    node_247 --> node_850
    node_350 --> node_793
    node_288 --> node_278
    node_755 --> node_830
    node_330 --> node_648
    node_374 --> node_375
    node_455 --> node_641
    node_755 --> node_651
    node_8 --> node_210
    node_11 --> node_823
    node_332 --> node_826
    node_17 --> node_793
    node_247 --> node_65
    node_240 --> node_275
    node_421 --> node_47
    node_297 --> node_643
    node_232 --> node_281
    node_247 --> node_722
    node_854 --> node_852
    node_508 --> node_162
    node_8 --> node_86
    node_228 --> node_829
    node_334 --> node_760
    node_340 --> node_743
    node_667 --> node_656
    node_524 --> node_590
    node_17 --> node_800
    node_222 --> node_854
    node_228 --> node_854
    node_339 --> node_665
    node_27 --> node_34
    node_340 --> node_671
    node_545 --> node_542
    node_553 --> node_586
    node_8 --> node_815
    node_590 --> node_589
    node_42 --> node_801
    node_755 --> node_732
    node_17 --> node_171
    node_32 --> node_250
    node_524 --> node_586
    node_344 --> node_821
    node_739 --> node_585
    node_343 --> node_850
    node_483 --> node_431
    node_512 --> node_641
    node_8 --> node_628
    node_340 --> node_709
    node_47 --> node_802
    node_681 --> node_683
    node_548 --> node_541
    node_335 --> node_579
    node_828 --> node_845
    node_47 --> node_783
    node_247 --> node_369
    node_24 --> node_7
    node_4 --> node_15
    node_525 --> node_682
    node_247 --> node_288
    node_237 --> node_777
    node_129 --> node_108
    node_525 --> node_601
    node_185 --> node_641
    node_265 --> node_306
    node_66 --> node_142
    node_373 --> node_693
    node_842 --> node_731
    node_437 --> node_90
    node_300 --> node_761
    node_222 --> node_750
    node_340 --> node_810
    node_197 --> node_641
    node_417 --> node_76
    node_654 --> node_619
    node_605 --> node_62
    node_754 --> node_581
    node_268 --> node_329
    node_496 --> node_799
    node_339 --> node_691
    node_66 --> node_60
    node_347 --> node_599
    node_526 --> node_775
    node_373 --> node_609
    node_667 --> node_67
    node_223 --> node_355
    node_372 --> node_775
    node_515 --> node_267
    node_550 --> node_546
    node_406 --> node_577
    node_828 --> node_654
    node_828 --> node_581
    node_754 --> node_582
    node_309 --> node_609
    node_17 --> node_45
    node_667 --> node_659
    node_667 --> node_644
    node_654 --> node_835
    node_337 --> node_561
    node_667 --> node_66
    node_247 --> node_806
    node_11 --> node_838
    node_32 --> node_251
    node_11 --> node_607
    node_231 --> node_497
    node_654 --> node_826
    node_667 --> node_641
    node_755 --> node_600
    node_63 --> node_155
    node_222 --> node_755
    node_815 --> node_817
    node_828 --> node_582
    node_306 --> node_334
    node_228 --> node_114
    node_228 --> node_755
    node_251 --> node_298
    node_755 --> node_588
    node_420 --> node_575
    node_487 --> node_13
    node_8 --> node_849
    node_247 --> node_218
    node_47 --> node_144
    node_300 --> node_38
    node_445 --> node_809
    node_247 --> node_238
    node_755 --> node_676
    node_222 --> node_687
    node_8 --> node_681
    node_228 --> node_687
    node_406 --> node_37
    node_543 --> node_541
    node_231 --> node_208
    node_561 --> node_560
    node_90 --> node_67
    node_654 --> node_636
    node_203 --> node_775
    node_222 --> node_734
    node_222 --> node_814
    node_247 --> node_840
    node_291 --> node_551
    node_228 --> node_734
    node_228 --> node_814
    node_335 --> node_683
    node_247 --> node_124
    node_118 --> node_125
    node_247 --> node_608
    node_575 --> node_566
    node_754 --> node_642
    node_828 --> node_751
    node_340 --> node_741
    node_512 --> node_351
    node_232 --> node_326
    node_291 --> node_550
    node_326 --> node_693
    node_240 --> node_832
    node_760 --> node_762
    node_828 --> node_646
    node_4 --> node_551
    node_291 --> node_12
    node_776 --> node_694
    node_667 --> node_657
    node_755 --> node_743
    node_776 --> node_693
    node_222 --> node_824
    node_231 --> node_67
    node_382 --> node_47
    node_720 --> node_574
    node_222 --> node_667
    node_228 --> node_824
    node_322 --> node_638
    node_247 --> node_715
    node_406 --> node_402
    node_228 --> node_667
    node_781 --> node_777
    node_247 --> node_552
    node_247 --> node_845
    node_806 --> node_76
    node_834 --> node_570
    node_325 --> node_39
    node_739 --> node_588
    node_43 --> node_63
    node_8 --> node_281
    node_247 --> node_740
    node_340 --> node_636
    node_11 --> node_731
    node_755 --> node_709
    node_315 --> node_342
    node_8 --> node_725
    node_223 --> node_693
    node_8 --> node_590
    node_222 --> node_828
    node_42 --> node_174
    node_228 --> node_468
    node_63 --> node_173
    node_771 --> node_609
    node_217 --> node_219
    node_307 --> node_834
    node_420 --> node_288
    node_382 --> node_775
    node_341 --> node_339
    node_482 --> node_809
    node_842 --> node_443
    node_842 --> node_819
    node_654 --> node_649
    node_738 --> node_589
    node_20 --> node_341
    node_198 --> node_693
    node_63 --> node_782
    node_63 --> node_181
    node_17 --> node_488
    node_335 --> node_681
    node_706 --> node_609
    node_667 --> node_563
    node_518 --> node_36
    node_222 --> node_698
    node_247 --> node_654
    node_693 --> node_76
    node_375 --> node_566
    node_8 --> node_599
    node_47 --> node_54
    node_217 --> node_776
    node_754 --> node_838
    node_325 --> node_38
    node_276 --> node_357
    node_336 --> node_587
    node_754 --> node_607
    node_263 --> node_693
    node_247 --> node_137
    node_307 --> node_822
    node_478 --> node_775
    node_17 --> node_809
    node_342 --> node_684
    node_828 --> node_838
    node_209 --> node_66
    node_276 --> node_40
    node_247 --> node_557
    node_642 --> node_644
    node_332 --> node_617
    node_288 --> node_295
    node_681 --> node_680
    node_828 --> node_607
    node_339 --> node_694
    node_228 --> node_356
    node_17 --> node_489
    node_229 --> node_650
    node_339 --> node_693
    node_364 --> node_47
    node_291 --> node_278
    node_525 --> node_758
    node_8 --> node_680
    node_235 --> node_119
    node_739 --> node_709
    node_418 --> node_91
    node_276 --> node_32
    node_340 --> node_784
    node_20 --> node_292
    node_85 --> node_78
    node_250 --> node_8
    node_374 --> node_367
    node_222 --> node_63
    node_247 --> node_393
    node_842 --> node_699
    node_842 --> node_760
    node_247 --> node_217
    node_828 --> node_579
    node_341 --> node_334
    node_337 --> node_559
    node_247 --> node_751
    node_330 --> node_650
    node_229 --> node_819
    node_123 --> node_124
    node_419 --> node_94
    node_17 --> node_449
    node_406 --> node_352
    node_293 --> node_318
    node_331 --> node_762
    node_420 --> node_413
    node_247 --> node_646
    node_501 --> node_641
    node_42 --> node_800
    node_32 --> node_573
    node_755 --> node_835
    node_307 --> node_845
    node_8 --> node_831
    node_842 --> node_595
    node_288 --> node_677
    node_222 --> node_726
    node_340 --> node_790
    node_517 --> node_677
    node_216 --> node_95
    node_654 --> node_839
    node_8 --> node_515
    node_514 --> node_180
    node_772 --> node_774
    node_222 --> node_744
    node_754 --> node_86
    node_559 --> node_757
    node_754 --> node_731
    node_8 --> node_754
    node_324 --> node_658
    node_420 --> node_552
    node_839 --> node_836
    node_457 --> node_165
    node_745 --> node_87
    node_849 --> node_219
    node_743 --> node_741
    node_775 --> node_177
    node_11 --> node_443
    node_247 --> node_659
    node_66 --> node_119
    node_11 --> node_819
    node_247 --> node_66
    node_339 --> node_690
    node_447 --> node_175
    node_512 --> node_281
    node_533 --> node_527
    node_201 --> node_60
    node_117 --> node_126
    node_250 --> node_48
    node_263 --> node_499
    node_8 --> node_51
    node_311 --> node_734
    node_339 --> node_662
    node_476 --> node_47
    node_222 --> node_40
    node_268 --> node_334
    node_47 --> node_190
    node_544 --> node_545
    node_754 --> node_628
    node_228 --> node_40
    node_332 --> node_825
    node_247 --> node_641
    node_331 --> node_763
    node_235 --> node_93
    node_307 --> node_581
    node_828 --> node_815
    node_47 --> node_787
    node_58 --> node_45
    node_250 --> node_249
    node_335 --> node_680
    node_276 --> node_363
    node_228 --> node_604
    node_247 --> node_813
    node_654 --> node_626
    node_229 --> node_760
    node_229 --> node_699
    node_775 --> node_786
    node_828 --> node_628
    node_8 --> node_842
    node_849 --> node_776
    node_329 --> node_585
    node_222 --> node_32
    node_293 --> node_13
    node_209 --> node_47
    node_251 --> node_108
    node_228 --> node_32
    node_307 --> node_582
    node_117 --> node_128
    node_419 --> node_96
    node_470 --> node_137
    node_842 --> node_853
    node_247 --> node_520
    node_842 --> node_672
    node_247 --> node_827
    node_98 --> node_96
    node_654 --> node_823
    node_500 --> node_775
    node_340 --> node_808
    node_222 --> node_717
    node_14 --> node_694
    node_32 --> node_341
    node_550 --> node_541
    node_153 --> node_187
    node_343 --> node_632
    node_222 --> node_716
    node_247 --> node_261
    node_716 --> node_815
    node_229 --> node_595
    node_446 --> node_155
    node_575 --> node_568
    node_17 --> node_435
    node_47 --> node_777
    node_49 --> node_95
    node_1 --> node_401
    node_338 --> node_625
    node_677 --> node_678
    node_734 --> node_733
    node_315 --> node_336
    node_420 --> node_557
    node_63 --> node_169
    node_375 --> node_368
    node_11 --> node_760
    node_11 --> node_699
    node_324 --> node_661
    node_339 --> node_834
    node_626 --> node_627
    node_228 --> node_512
    node_263 --> node_8
    node_307 --> node_751
    node_251 --> node_394
    node_288 --> node_259
    node_737 --> node_735
    node_755 --> node_822
    node_247 --> node_579
    node_242 --> node_775
    node_47 --> node_110
    node_330 --> node_41
    node_230 --> node_42
    node_420 --> node_393
    node_636 --> node_638
    node_420 --> node_217
    node_247 --> node_123
    node_276 --> node_575
    node_56 --> node_60
    node_11 --> node_595
    node_322 --> node_636
    node_47 --> node_114
    node_362 --> node_15
    node_232 --> node_350
    node_228 --> node_555
    node_224 --> node_57
    node_247 --> node_689
    node_340 --> node_642
    node_221 --> node_4
    node_544 --> node_551
    node_842 --> node_605
    node_461 --> node_792
    node_739 --> node_583
    node_828 --> node_681
    node_523 --> node_762
    node_172 --> node_795
    node_775 --> node_176
    node_369 --> node_775
    node_11 --> node_668
    node_754 --> node_443
    node_754 --> node_819
    node_47 --> node_785
    node_247 --> node_86
    node_432 --> node_47
    node_373 --> node_641
    node_237 --> node_76
    node_828 --> node_443
    node_242 --> node_251
    node_83 --> node_776
    node_228 --> node_299
    node_228 --> node_821
    node_247 --> node_815
    node_247 --> node_27
    node_281 --> node_351
    node_479 --> node_811
    node_513 --> node_178
    node_524 --> node_591
    node_552 --> node_551
    node_66 --> node_95
    node_667 --> node_660
    node_692 --> node_76
    node_286 --> node_28
    node_8 --> node_759
    node_11 --> node_672
    node_11 --> node_853
    node_442 --> node_434
    node_247 --> node_181
    node_222 --> node_692
    node_432 --> node_775
    node_221 --> node_34
    node_307 --> node_838
    node_217 --> node_218
    node_340 --> node_799
    node_66 --> node_90
    node_288 --> node_294
    node_307 --> node_607
    node_250 --> node_232
    node_222 --> node_655
    node_329 --> node_588
    node_276 --> node_288
    node_288 --> node_307
    node_228 --> node_655
    node_32 --> node_246
    node_340 --> node_678
    node_754 --> node_851
    node_42 --> node_786
    node_755 --> node_581
    node_287 --> node_678
    node_336 --> node_590
    node_63 --> node_783
    node_229 --> node_605
    node_79 --> node_80
    node_42 --> node_809
    node_448 --> node_190
    node_483 --> node_141
    node_247 --> node_383
    node_754 --> node_699
    node_754 --> node_760
    node_63 --> node_801
    node_229 --> node_666
    node_307 --> node_579
    node_755 --> node_582
    node_842 --> node_737
    node_533 --> node_530
    node_217 --> node_608
    node_222 --> node_850
    node_331 --> node_584
    node_523 --> node_760
    node_228 --> node_850
    node_222 --> node_730
    node_218 --> node_775
    node_828 --> node_599
    node_834 --> node_758
    node_339 --> node_581
    node_228 --> node_730
    node_828 --> node_699
    node_842 --> node_847
    node_11 --> node_620
    node_340 --> node_775
    node_561 --> node_658
    node_307 --> node_38
    node_525 --> node_589
    node_332 --> node_616
    node_341 --> node_343
    node_754 --> node_595
    node_339 --> node_582
    node_17 --> node_693
    node_222 --> node_722
    node_127 --> node_609
    node_228 --> node_722
    node_291 --> node_644
    node_11 --> node_605
    node_247 --> node_849
    node_667 --> node_73
    node_229 --> node_833
    node_710 --> node_714
    node_452 --> node_173
    node_755 --> node_823
    node_222 --> node_140
    node_228 --> node_374
    node_776 --> node_641
    node_247 --> node_681
    node_842 --> node_756
    node_276 --> node_442
    node_247 --> node_306
    node_106 --> node_609
    node_754 --> node_668
    node_66 --> node_117
    node_307 --> node_731
    node_781 --> node_76
    node_120 --> node_129
    node_117 --> node_298
    node_222 --> node_647
    node_288 --> node_280
    node_228 --> node_619
    node_228 --> node_647
    node_263 --> node_642
    node_265 --> node_522
    node_307 --> node_815
    node_276 --> node_413
    node_828 --> node_668
    node_250 --> node_241
    node_421 --> node_394
    node_483 --> node_575
    node_231 --> node_298
    node_212 --> node_775
    node_307 --> node_628
    node_229 --> node_737
    node_343 --> node_849
    node_221 --> node_303
    node_437 --> node_775
    node_805 --> node_13
    node_340 --> node_643
    node_828 --> node_831
    node_754 --> node_672
    node_754 --> node_853
    node_107 --> node_609
    node_228 --> node_34
    node_42 --> node_176
    node_322 --> node_637
    node_229 --> node_847
    node_276 --> node_358
    node_63 --> node_163
    node_667 --> node_571
    node_477 --> node_115
    node_408 --> node_4
    node_849 --> node_218
    node_543 --> node_34
    node_775 --> node_805
    node_8 --> node_829
    node_828 --> node_853
    node_17 --> node_486
    node_276 --> node_552
    node_828 --> node_672
    node_754 --> node_51
    node_247 --> node_281
    node_17 --> node_452
    node_828 --> node_754
    node_63 --> node_160
    node_8 --> node_854
    node_687 --> node_670
    node_247 --> node_725
    node_347 --> node_824
    node_687 --> node_669
    node_500 --> node_298
    node_247 --> node_590
    node_247 --> node_577
    node_590 --> node_586
    node_340 --> node_745
    node_8 --> node_591
    node_11 --> node_737
    node_849 --> node_608
    node_195 --> node_641
    node_223 --> node_775
    node_228 --> node_301
    node_242 --> node_576
    node_654 --> node_650
    node_8 --> node_60
    node_11 --> node_847
    node_755 --> node_838
    node_709 --> node_589
    node_306 --> node_319
    node_731 --> node_727
    node_755 --> node_607
    node_247 --> node_599
    node_754 --> node_620
    node_223 --> node_38
    node_222 --> node_840
    node_222 --> node_738
    node_228 --> node_840
    node_228 --> node_738
    node_854 --> node_609
    node_247 --> node_37
    node_483 --> node_288
    node_828 --> node_620
    node_451 --> node_806
    node_754 --> node_605
    node_654 --> node_819
    node_63 --> node_174
    node_518 --> node_73
    node_228 --> node_707
    node_640 --> node_644
    node_276 --> node_557
    node_334 --> node_758
    node_11 --> node_756
    node_265 --> node_28
    node_538 --> node_535
    node_462 --> node_47
    node_340 --> node_788
    node_247 --> node_680
    node_630 --> node_570
    node_323 --> node_309
    node_288 --> node_268
    node_709 --> node_583
    node_554 --> node_687
    node_47 --> node_797
    node_584 --> node_609
    node_205 --> node_67
    node_329 --> node_589
    node_222 --> node_715
    node_502 --> node_191
    node_228 --> node_715
    node_222 --> node_845
    node_276 --> node_393
    node_8 --> node_755
    node_263 --> node_38
    node_276 --> node_217
    node_288 --> node_282
    node_307 --> node_443
    node_340 --> node_762
    node_222 --> node_740
    node_503 --> node_97
    node_503 --> node_100
    node_842 --> node_750
    node_228 --> node_649
    node_228 --> node_740
    node_63 --> node_175
    node_247 --> node_402
    node_681 --> node_685
    node_424 --> node_641
    node_340 --> node_803
    node_340 --> node_798
    node_572 --> node_609
    node_607 --> node_609
    node_667 --> node_54
    node_8 --> node_687
    node_247 --> node_396
    node_339 --> node_38
    node_340 --> node_621
    node_83 --> node_218
    node_239 --> node_728
    node_629 --> node_305
    node_229 --> node_747
    node_247 --> node_831
    node_217 --> node_827
    node_842 --> node_841
    node_8 --> node_734
    node_8 --> node_814
    node_291 --> node_4
    node_406 --> node_356
    node_590 --> node_853
    node_755 --> node_731
    node_222 --> node_749
    node_483 --> node_442
    node_8 --> node_478
    node_654 --> node_699
    node_489 --> node_786
    node_228 --> node_749
    node_654 --> node_760
    node_842 --> node_601
    node_247 --> node_121
    node_267 --> node_47
    node_329 --> node_583
    node_222 --> node_654
    node_704 --> node_817
    node_247 --> node_754
    node_181 --> node_13
    node_483 --> node_413
    node_211 --> node_162
    node_247 --> node_51
    node_276 --> node_632
    node_754 --> node_737
    node_17 --> node_790
    node_210 --> node_66
    node_512 --> node_439
    node_420 --> node_577
    node_626 --> node_623
    node_8 --> node_824
    node_251 --> node_314
    node_63 --> node_143
    node_654 --> node_595
    node_839 --> node_837
    node_32 --> node_568
    node_47 --> node_90
    node_63 --> node_800
    node_128 --> node_298
    node_222 --> node_557
    node_307 --> node_599
    node_42 --> node_805
    node_307 --> node_699
    node_247 --> node_783
    node_47 --> node_76
    node_667 --> node_394
    node_247 --> node_842
    node_575 --> node_567
    node_8 --> node_468
    node_229 --> node_750
    node_483 --> node_552
    node_340 --> node_760
    node_228 --> node_562
    node_32 --> node_541
    node_222 --> node_393
    node_222 --> node_217
    node_731 --> node_411
    node_738 --> node_586
    node_307 --> node_595
    node_743 --> node_745
    node_222 --> node_751
    node_420 --> node_37
    node_335 --> node_685
    node_754 --> node_756
    node_346 --> node_38
    node_228 --> node_839
    node_229 --> node_601
    node_842 --> node_667
    node_222 --> node_646
    node_117 --> node_108
    node_575 --> node_564
    node_776 --> node_69
    node_828 --> node_756
    node_247 --> node_352
    node_276 --> node_250
    node_541 --> node_542
    node_692 --> node_637
    node_17 --> node_61
    node_263 --> node_87
    node_11 --> node_750
    node_307 --> node_668
    node_720 --> node_718
    node_842 --> node_828
    node_560 --> node_827
    node_188 --> node_44
    node_540 --> node_34
    node_291 --> node_23
    node_229 --> node_640
    node_104 --> node_609
    node_401 --> node_411
    node_121 --> node_127
    node_307 --> node_831
    node_20 --> node_40
    node_222 --> node_659
    node_9 --> node_609
    node_849 --> node_827
    node_228 --> node_708
    node_667 --> node_60
    node_344 --> node_41
    node_420 --> node_402
    node_842 --> node_698
    node_420 --> node_341
    node_11 --> node_601
    node_123 --> node_396
    node_238 --> node_38
    node_307 --> node_672
    node_2 --> node_91
    node_307 --> node_853
    node_699 --> node_698
    node_47 --> node_804
    node_525 --> node_761
    node_307 --> node_754
    node_500 --> node_108
    node_20 --> node_32
    node_340 --> node_706
    node_13 --> node_302
    node_222 --> node_813
    node_614 --> node_609
    node_11 --> node_755
    node_755 --> node_443
    node_333 --> node_767
    node_228 --> node_813
    node_63 --> node_153
    node_210 --> node_47
    node_221 --> node_775
    node_231 --> node_394
    node_488 --> node_801
    node_606 --> node_609
    node_755 --> node_819
    node_512 --> node_478
    node_642 --> node_775
    node_123 --> node_121
    node_406 --> node_512
    node_483 --> node_393
    node_267 --> node_306
    node_343 --> node_633
    node_32 --> node_239
    node_291 --> node_8
    node_636 --> node_642
    node_430 --> node_77
    node_230 --> node_34
    node_755 --> node_763
    node_667 --> node_568
    node_727 --> node_411
    node_654 --> node_605
    node_525 --> node_627
    node_575 --> node_574
    node_20 --> node_512
    node_760 --> node_758
    node_247 --> node_759
    node_157 --> node_89
    node_406 --> node_555
    node_754 --> node_854
    node_654 --> node_666
    node_83 --> node_637
    node_307 --> node_620
    node_47 --> node_111
    node_828 --> node_829
    node_13 --> node_330
    node_51 --> node_817
    node_424 --> node_87
    node_32 --> node_356
    node_222 --> node_579
    node_512 --> node_468
    node_826 --> node_637
    node_828 --> node_854
    node_601 --> node_812
    node_251 --> node_381
    node_47 --> node_806
    node_83 --> node_66
    node_229 --> node_698
    node_288 --> node_272
    node_11 --> node_667
    node_781 --> node_637
    node_225 --> node_45
    node_8 --> node_604
    node_307 --> node_605
    node_755 --> node_699
    node_755 --> node_760
    node_842 --> node_726
    node_842 --> node_691
    node_229 --> node_625
    node_365 --> node_371
    node_224 --> node_49
    node_336 --> node_591
    node_654 --> node_833
    node_237 --> node_47
    node_357 --> node_358
    node_842 --> node_744
    node_251 --> node_693
    node_222 --> node_689
    node_228 --> node_304
    node_775 --> node_180
    node_11 --> node_828
    node_182 --> node_777
    node_228 --> node_689
    node_588 --> node_589
    node_17 --> node_179
    node_222 --> node_47
    node_348 --> node_257
    node_350 --> node_39
    node_374 --> node_15
    node_748 --> node_609
    node_754 --> node_750
    node_402 --> node_401
    node_229 --> node_830
    node_351 --> node_369
    node_420 --> node_352
    node_459 --> node_101
    node_755 --> node_595
    node_394 --> node_678
    node_247 --> node_296
    node_8 --> node_93
    node_288 --> node_286
    node_288 --> node_267
    node_11 --> node_698
    node_754 --> node_601
    node_224 --> node_87
    node_692 --> node_775
    node_63 --> node_809
    node_654 --> node_737
    node_781 --> node_779
    node_304 --> node_38
    node_517 --> node_643
    node_754 --> node_755
    node_229 --> node_732
    node_17 --> node_775
    node_369 --> node_372
    node_483 --> node_250
    node_339 --> node_660
    node_654 --> node_847
    node_228 --> node_686
    node_560 --> node_642
    node_7 --> node_419
    node_347 --> node_597
    node_816 --> node_601
    node_842 --> node_717
    node_247 --> node_394
    node_32 --> node_40
    node_47 --> node_811
    node_842 --> node_716
    node_128 --> node_108
    node_754 --> node_687
    node_828 --> node_755
    node_8 --> node_600
    node_229 --> node_691
    node_47 --> node_53
    node_228 --> node_598
    node_383 --> node_376
    node_207 --> node_146
    node_754 --> node_734
    node_754 --> node_814
    node_755 --> node_672
    node_64 --> node_694
    node_339 --> node_668
    node_755 --> node_853
    node_229 --> node_744
    node_47 --> node_149
    node_828 --> node_687
    node_230 --> node_540
    node_406 --> node_4
    node_517 --> node_745
    node_42 --> node_790
    node_493 --> node_190
    node_331 --> node_758
    node_87 --> node_394
    node_291 --> node_400
    node_325 --> node_828
    node_442 --> node_775
    node_826 --> node_825
    node_14 --> node_817
    node_828 --> node_734
    node_828 --> node_814
    node_83 --> node_47
    node_222 --> node_383
    node_340 --> node_737
    node_281 --> node_350
    node_667 --> node_133
    node_228 --> node_383
    node_772 --> node_764
    node_421 --> node_43
    node_341 --> node_331
    node_406 --> node_374
    node_590 --> node_854
    node_478 --> node_365
    node_247 --> node_829
    node_490 --> node_189
    node_636 --> node_86
    node_340 --> node_847
    node_228 --> node_309
    node_525 --> node_681
    node_512 --> node_472
    node_84 --> node_694
    node_238 --> node_817
    node_247 --> node_190
    node_247 --> node_854
    node_486 --> node_179
    node_8 --> node_821
    node_11 --> node_726
    node_11 --> node_691
    node_754 --> node_824
    node_35 --> node_66
    node_754 --> node_667
    node_781 --> node_47
    node_460 --> node_788
    node_32 --> node_512
    node_172 --> node_775
    node_11 --> node_744
    node_247 --> node_591
    node_307 --> node_756
    node_63 --> node_147
    node_141 --> node_17
    node_828 --> node_824
    node_704 --> node_701
    node_43 --> node_70
    node_828 --> node_667
    node_228 --> node_593
    node_222 --> node_849
    node_291 --> node_642
    node_228 --> node_849
    node_229 --> node_717
    node_8 --> node_671
    node_247 --> node_60
    node_739 --> node_706
    node_754 --> node_828
    node_83 --> node_55
    node_228 --> node_247
    node_364 --> node_365
    node_338 --> node_627
    node_222 --> node_681
    node_229 --> node_676
    node_781 --> node_775
    node_339 --> node_663
    node_17 --> node_145
    node_228 --> node_306
    node_755 --> node_605
    node_236 --> node_38
    node_55 --> node_693
    node_340 --> node_739
    node_754 --> node_698
    node_268 --> node_331
    node_276 --> node_37
    node_337 --> node_759
    node_251 --> node_8
    node_324 --> node_666
    node_247 --> node_10
    node_519 --> node_13
    node_42 --> node_180
    node_654 --> node_640
    node_63 --> node_795
    node_268 --> node_337
    node_517 --> node_621
    node_8 --> node_730
    node_11 --> node_717
    node_119 --> node_108
    node_251 --> node_303
    node_594 --> node_592
    node_654 --> node_747
    node_842 --> node_692
    node_11 --> node_716
    node_525 --> node_586
    node_8 --> node_4
    node_834 --> node_761
    node_842 --> node_655
    node_230 --> node_66
    node_228 --> node_652
    node_359 --> node_4
    node_650 --> node_609
    node_430 --> node_641
    node_222 --> node_725
    node_291 --> node_678
    node_276 --> node_402
    node_222 --> node_590
    node_17 --> node_788
    node_222 --> node_577
    node_228 --> node_533
    node_306 --> node_338
    node_63 --> node_188
    node_79 --> node_72
    node_228 --> node_577
    node_101 --> node_78
    node_276 --> node_341
    node_288 --> node_265
    node_324 --> node_664
    node_640 --> node_637
    node_657 --> node_609
    node_842 --> node_850
    node_616 --> node_609
    node_47 --> node_792
    node_307 --> node_829
    node_560 --> node_86
    node_247 --> node_734
    node_247 --> node_814
    node_288 --> node_290
    node_307 --> node_854
    node_291 --> node_250
    node_317 --> node_38
    node_8 --> node_619
    node_8 --> node_647
    node_20 --> node_840
    node_373 --> node_368
    node_526 --> node_693
    node_222 --> node_594
    node_336 --> node_585
    node_17 --> node_803
    node_17 --> node_798
    node_523 --> node_758
    node_228 --> node_594
    node_247 --> node_28
    node_365 --> node_366
    node_372 --> node_693
    node_98 --> node_101
    node_654 --> node_750
    node_755 --> node_737
    node_771 --> node_767
    node_842 --> node_722
    node_754 --> node_744
    node_559 --> node_762
    node_222 --> node_37
    node_755 --> node_847
    node_828 --> node_726
    node_247 --> node_824
    node_291 --> node_38
    node_318 --> node_587
    node_276 --> node_360
    node_248 --> node_644
    node_194 --> node_157
    node_8 --> node_826
    node_654 --> node_601
    node_17 --> node_182
    node_156 --> node_47
    node_228 --> node_763
    node_228 --> node_327
    node_47 --> node_155
    node_214 --> node_180
    node_222 --> node_680
    node_307 --> node_750
    node_375 --> node_641
    node_228 --> node_680
    node_42 --> node_179
    node_780 --> node_609
    node_755 --> node_756
    node_512 --> node_504
    node_250 --> node_234
    node_340 --> node_750
    node_416 --> node_641
    node_468 --> node_281
    node_8 --> node_636
    node_291 --> node_412
    node_203 --> node_693
    node_156 --> node_775
    node_293 --> node_304
    node_636 --> node_851
    node_222 --> node_402
    node_228 --> node_312
    node_642 --> node_62
    node_11 --> node_692
    node_709 --> node_586
    node_754 --> node_717
    node_230 --> node_47
    node_183 --> node_66
    node_575 --> node_563
    node_4 --> node_267
    node_453 --> node_792
    node_754 --> node_716
    node_719 --> node_720
    node_11 --> node_655
    node_307 --> node_755
    node_8 --> node_738
    node_340 --> node_601
    node_276 --> node_352
    node_754 --> node_776
    node_17 --> node_167
    node_306 --> node_342
    node_828 --> node_716
    node_307 --> node_687
    node_667 --> node_76
    node_326 --> node_439
    node_8 --> node_707
    node_222 --> node_754
    node_247 --> node_356
    node_708 --> node_706
    node_32 --> node_34
    node_525 --> node_623
    node_375 --> node_657
    node_406 --> node_562
    node_833 --> node_590
    node_11 --> node_850
    node_81 --> node_795
    node_307 --> node_734
    node_307 --> node_814
    node_97 --> node_99
    node_483 --> node_37
    node_486 --> node_803
    node_518 --> node_644
    node_559 --> node_760
    node_63 --> node_810
    node_20 --> node_557
    node_833 --> node_586
    node_334 --> node_761
    node_495 --> node_47
    node_339 --> node_818
    node_8 --> node_715
    node_247 --> node_373
    node_47 --> node_173
    node_242 --> node_63
    node_553 --> node_587
    node_382 --> node_693
    node_11 --> node_722
    node_288 --> node_292
    node_524 --> node_587
    node_654 --> node_828
    node_8 --> node_649
    node_222 --> node_842
    node_228 --> node_842
    node_20 --> node_393
    node_164 --> node_67
    node_331 --> node_589
    node_20 --> node_217
    node_640 --> node_775
    node_375 --> node_47
    node_47 --> node_181
    node_248 --> node_90
    node_307 --> node_824
    node_382 --> node_609
    node_307 --> node_667
    node_560 --> node_817
    node_495 --> node_775
    node_776 --> node_777
    node_775 --> node_151
    node_340 --> node_786
    node_483 --> node_402
    node_164 --> node_66
    node_654 --> node_698
    node_177 --> node_53
    node_336 --> node_588
    node_483 --> node_341
    node_8 --> node_749
    node_247 --> node_295
    node_333 --> node_765
    node_213 --> node_184
    node_332 --> node_606
    node_307 --> node_828
    node_291 --> node_297
    node_32 --> node_840
    node_41 --> node_604
    node_478 --> node_693
    node_512 --> node_507
    node_658 --> node_47
    node_842 --> node_845
    node_247 --> node_273
    node_560 --> node_851
    node_222 --> node_352
    node_182 --> node_76
    node_331 --> node_583
    node_781 --> node_780
    node_636 --> node_51
    node_512 --> node_806
    node_118 --> node_128
    node_654 --> node_830
    node_304 --> node_663
    node_828 --> node_821
    node_228 --> node_723
    node_229 --> node_822
    node_291 --> node_83
    node_456 --> node_154
    node_247 --> node_604
    node_754 --> node_692
    node_315 --> node_337
    node_268 --> node_338
    node_423 --> node_694
    node_640 --> node_643
    node_247 --> node_644
    node_754 --> node_655
    node_63 --> node_192
    node_364 --> node_693
    node_755 --> node_750
    node_828 --> node_692
    node_293 --> node_306
    node_842 --> node_654
    node_242 --> node_219
    node_512 --> node_451
    node_47 --> node_145
    node_654 --> node_732
    node_828 --> node_655
    node_317 --> node_576
    node_2 --> node_119
    node_232 --> node_351
    node_251 --> node_775
    node_304 --> node_666
    node_302 --> node_715
    node_461 --> node_164
    node_754 --> node_850
    node_755 --> node_601
    node_8 --> node_839
    node_263 --> node_370
    node_396 --> node_395
    node_654 --> node_726
    node_654 --> node_691
    node_268 --> node_340
    node_781 --> node_73
    node_343 --> node_604
    node_306 --> node_329
    node_420 --> node_356
    node_247 --> node_269
    node_42 --> node_788
    node_247 --> node_512
    node_228 --> node_666
    node_654 --> node_744
    node_229 --> node_845
    node_504 --> node_350
    node_828 --> node_850
    node_667 --> node_658
    node_828 --> node_730
    node_8 --> node_637
    node_208 --> node_47
    node_341 --> node_342
    node_548 --> node_551
    node_754 --> node_722
    node_222 --> node_759
    node_17 --> node_165
    node_343 --> node_848
    node_228 --> node_759
    node_17 --> node_511
    node_8 --> node_626
    node_307 --> node_726
    node_430 --> node_70
    node_8 --> node_708
    node_828 --> node_722
    node_842 --> node_751
    node_247 --> node_600
    node_32 --> node_557
    node_4 --> node_290
    node_247 --> node_555
    node_340 --> node_811
    node_228 --> node_675
    node_340 --> node_758
    node_304 --> node_664
    node_307 --> node_744
    node_842 --> node_646
    node_229 --> node_654
    node_338 --> node_623
    node_229 --> node_581
    node_500 --> node_693
    node_247 --> node_375
    node_11 --> node_845
    node_347 --> node_598
    node_267 --> node_337
    node_11 --> node_740
    node_32 --> node_393
    node_340 --> node_744
    node_560 --> node_51
    node_32 --> node_217
    node_63 --> node_784
    node_654 --> node_717
    node_2 --> node_93
    node_42 --> node_182
    node_291 --> node_33
    node_650 --> node_648
    node_318 --> node_590
    node_229 --> node_582
    node_828 --> node_647
    node_654 --> node_716
    node_755 --> node_667
    node_209 --> node_693
    node_687 --> node_672
    node_605 --> node_817
    node_42 --> node_151
    node_47 --> node_101
    node_654 --> node_676
    node_193 --> node_66
    node_268 --> node_342
    node_503 --> node_94
    node_247 --> node_821
    node_332 --> node_612
    node_81 --> node_57
    node_31 --> node_251
    node_332 --> node_609
    node_406 --> node_544
    node_267 --> node_28
    node_755 --> node_828
    node_251 --> node_745
    node_11 --> node_654
    node_469 --> node_166
    node_629 --> node_630
    node_307 --> node_717
    node_340 --> node_639
    node_339 --> node_667
    node_842 --> node_813
    node_63 --> node_790
    node_465 --> node_800
    node_247 --> node_671
    node_307 --> node_716
    node_712 --> node_710
    node_370 --> node_47
    node_760 --> node_761
    node_228 --> node_550
    node_229 --> node_751
    node_356 --> node_355
    node_14 --> node_777
    node_283 --> node_572
    node_755 --> node_698
    node_805 --> node_27
    node_754 --> node_218
    node_431 --> node_269
    node_229 --> node_646
    node_544 --> node_549
    node_291 --> node_62
    node_522 --> node_573
    node_731 --> node_729
    node_63 --> node_183
    node_41 --> node_609
    node_754 --> node_738
    node_231 --> node_451
    node_8 --> node_47
    node_55 --> node_775
    node_247 --> node_730
    node_20 --> node_383
    node_699 --> node_697
    node_324 --> node_665
    node_47 --> node_298
    node_420 --> node_512
    node_754 --> node_608
    node_11 --> node_751
    node_491 --> node_175
    node_828 --> node_738
    node_842 --> node_579
    node_247 --> node_4
    node_525 --> node_679
    node_341 --> node_329
    node_526 --> node_641
    node_222 --> node_829
    node_247 --> node_117
    node_11 --> node_646
    node_250 --> node_20
    node_340 --> node_670
    node_340 --> node_669
    node_553 --> node_590
    node_372 --> node_641
    node_336 --> node_583
    node_8 --> node_775
    node_228 --> node_781
    node_231 --> node_8
    node_247 --> node_374
    node_432 --> node_693
    node_754 --> node_715
    node_420 --> node_555
    node_503 --> node_93
    node_754 --> node_845
    node_842 --> node_689
    node_8 --> node_686
    node_559 --> node_570
    node_222 --> node_591
    node_421 --> node_775
    node_754 --> node_740
    node_228 --> node_591
    node_340 --> node_805
    node_66 --> node_122
    node_828 --> node_715
    node_246 --> node_285
    node_291 --> node_398
    node_228 --> node_317
    node_755 --> node_726
    node_307 --> node_821
    node_755 --> node_691
    node_247 --> node_619
    node_77 --> node_70
    node_8 --> node_598
    node_247 --> node_647
    node_828 --> node_740
    node_147 --> node_644
    node_229 --> node_838
    node_63 --> node_792
    node_267 --> node_333
    node_83 --> node_394
    node_755 --> node_744
    node_199 --> node_47
    node_229 --> node_607
    node_288 --> node_13
    node_47 --> node_801
    node_342 --> node_681
    node_352 --> node_350
    node_754 --> node_749
    node_218 --> node_694
    node_11 --> node_813
    node_218 --> node_693
    node_203 --> node_641
    node_237 --> node_45
    node_307 --> node_692
    node_406 --> node_652
    node_550 --> node_548
    node_315 --> node_338
    node_754 --> node_654
    node_101 --> node_99
    node_32 --> node_47
    node_842 --> node_815
    node_828 --> node_749
    node_692 --> node_45
    node_247 --> node_346
    node_468 --> node_350
    node_331 --> node_761
    node_229 --> node_579
    node_307 --> node_655
    node_247 --> node_826
    node_406 --> node_533
    node_575 --> node_571
    node_842 --> node_628
    node_199 --> node_775
    node_514 --> node_804
    node_231 --> node_48
    node_550 --> node_545
    node_455 --> node_47
    node_17 --> node_426
    node_20 --> node_652
    node_86 --> node_87
    node_307 --> node_850
    node_291 --> node_1
    node_8 --> node_593
    node_315 --> node_340
    node_20 --> node_577
    node_247 --> node_636
    node_307 --> node_730
    node_263 --> node_219
    node_13 --> node_344
    node_755 --> node_717
    node_755 --> node_716
    node_562 --> node_558
    node_640 --> node_62
    node_66 --> node_120
    node_503 --> node_90
    node_163 --> node_4
    node_222 --> node_843
    node_511 --> node_167
    node_525 --> node_624
    node_11 --> node_579
    node_228 --> node_843
    node_455 --> node_775
    node_278 --> node_13
    node_754 --> node_751
    node_224 --> node_46
    node_307 --> node_722
    node_512 --> node_47
    node_212 --> node_693
    node_247 --> node_738
    node_437 --> node_693
    node_291 --> node_538
    node_406 --> node_327
    node_590 --> node_707
    node_229 --> node_731
    node_263 --> node_776
    node_754 --> node_646
    node_63 --> node_179
    node_247 --> node_707
    node_229 --> node_815
    node_17 --> node_470
    node_425 --> node_694
    node_11 --> node_689
    node_20 --> node_37
    node_276 --> node_356
    node_32 --> node_383
    node_185 --> node_47
    node_333 --> node_764
    node_842 --> node_849
    node_229 --> node_628
    node_509 --> node_168
    node_247 --> node_8
    node_83 --> node_45
    node_828 --> node_849
    node_833 --> node_591
    node_353 --> node_21
    node_420 --> node_374
    node_307 --> node_647
    node_197 --> node_47
    node_776 --> node_76
    node_247 --> node_367
    node_842 --> node_681
    node_353 --> node_87
    node_13 --> node_343
    node_478 --> node_641
    node_222 --> node_719
    node_247 --> node_303
    node_228 --> node_719
    node_231 --> node_205
    node_247 --> node_649
    node_228 --> node_742
    node_512 --> node_181
    node_667 --> node_131
    node_35 --> node_394
    node_781 --> node_45
    node_228 --> node_640
    node_550 --> node_551
    node_8 --> node_650
    node_828 --> node_708
    node_333 --> node_771
    node_11 --> node_815
    node_342 --> node_680
    node_197 --> node_775
    node_206 --> node_801
    node_754 --> node_813
    node_20 --> node_402
    node_654 --> node_822
    node_251 --> node_326
    node_318 --> node_759
    node_667 --> node_47
    node_775 --> node_190
    node_512 --> node_475
    node_11 --> node_628
    node_267 --> node_340
    node_228 --> node_673
    node_200 --> node_42
    node_775 --> node_787
    node_247 --> node_749
    node_291 --> node_431
    node_487 --> node_28
    node_733 --> node_609
    node_754 --> node_827
    node_17 --> node_177
    node_32 --> node_306
    node_828 --> node_813
    node_228 --> node_816
    node_381 --> node_314
    node_8 --> node_594
    node_101 --> node_73
    node_47 --> node_174
    node_222 --> node_629
    node_247 --> node_48
    node_228 --> node_629
    node_667 --> node_775
    node_842 --> node_725
    node_585 --> node_609
    node_755 --> node_692
    node_17 --> node_786
    node_523 --> node_761
    node_32 --> node_132
    node_806 --> node_694
    node_17 --> node_68
    node_842 --> node_590
    node_32 --> node_746
    node_8 --> node_222
    node_47 --> node_108
    node_105 --> node_609
    node_699 --> node_696
    node_222 --> node_356
    node_472 --> node_351
    node_229 --> node_681
    node_755 --> node_655
    node_775 --> node_777
    node_338 --> node_601
    node_8 --> node_763
    node_276 --> node_361
    node_291 --> node_539
    node_40 --> node_39
    node_238 --> node_256
    node_307 --> node_738
    node_754 --> node_579
    node_31 --> node_292
    node_654 --> node_845
    node_101 --> node_85
    node_181 --> node_69
    node_462 --> node_693
    node_247 --> node_562
    node_32 --> node_652
    node_339 --> node_692
    node_374 --> node_364
    node_842 --> node_599
    node_524 --> node_584
    node_230 --> node_394
    node_334 --> node_759
    node_755 --> node_850
    node_32 --> node_533
    node_32 --> node_577
    node_153 --> node_808
    node_229 --> node_443
    node_420 --> node_840
    node_501 --> node_66
    node_364 --> node_775
    node_793 --> node_165
    node_11 --> node_849
    node_754 --> node_689
    node_117 --> node_678
    node_344 --> node_822
    node_607 --> node_610
    node_63 --> node_178
    node_47 --> node_394
    node_247 --> node_839
    node_250 --> node_238
    node_63 --> node_145
    node_11 --> node_681
    node_272 --> node_290
    node_288 --> node_293
    node_228 --> node_625
    node_307 --> node_715
    node_196 --> node_806
    node_828 --> node_689
    node_41 --> node_603
    node_242 --> node_642
    node_304 --> node_665
    node_420 --> node_184
    node_754 --> node_563
    node_755 --> node_722
    node_352 --> node_353
    node_307 --> node_740
    node_276 --> node_512
    node_842 --> node_680
    node_324 --> node_662
    node_654 --> node_581
    node_247 --> node_637
    node_57 --> node_185
    node_340 --> node_635
    node_20 --> node_352
    node_340 --> node_845
    node_265 --> node_326
    node_590 --> node_708
    node_667 --> node_56
    node_222 --> node_651
    node_32 --> node_37
    node_291 --> node_13
    node_103 --> node_99
    node_8 --> node_41
    node_228 --> node_651
    node_654 --> node_582
    node_247 --> node_626
    node_47 --> node_800
    node_754 --> node_815
    node_247 --> node_708
    node_267 --> node_4
    node_842 --> node_668
    node_307 --> node_749
    node_849 --> node_848
    node_483 --> node_356
    node_789 --> node_187
    node_276 --> node_555
    node_307 --> node_654
    node_17 --> node_176
    node_222 --> node_604
    node_239 --> node_13
    node_242 --> node_641
    node_288 --> node_256
    node_590 --> node_587
    node_229 --> node_599
    node_828 --> node_686
    node_63 --> node_157
    node_842 --> node_831
    node_63 --> node_788
    node_228 --> node_732
    node_365 --> node_369
    node_463 --> node_45
    node_331 --> node_586
    node_49 --> node_50
    node_222 --> node_644
    node_228 --> node_314
    node_11 --> node_725
    node_681 --> node_684
    node_476 --> node_775
    node_575 --> node_718
    node_464 --> node_136
    node_11 --> node_590
    node_828 --> node_598
    node_654 --> node_751
    node_842 --> node_754
    node_339 --> node_647
    node_332 --> node_607
    node_667 --> node_132
    node_32 --> node_402
    node_42 --> node_190
    node_318 --> node_591
    node_343 --> node_603
    node_621 --> node_13
    node_42 --> node_787
    node_745 --> node_746
    node_331 --> node_760
    node_654 --> node_646
    node_32 --> node_298
    node_63 --> node_803
    node_63 --> node_798
    node_209 --> node_775
    node_369 --> node_641
    node_492 --> node_153
    node_479 --> node_192
    node_42 --> node_166
    node_11 --> node_599
    node_501 --> node_47
    node_559 --> node_758
    node_739 --> node_589
    node_222 --> node_512
    node_8 --> node_723
    node_32 --> node_41
    node_330 --> node_595
    node_420 --> node_562
    node_229 --> node_668
    node_65 --> node_87
    node_339 --> node_658
    node_307 --> node_646
    node_754 --> node_849
    node_776 --> node_53
    node_263 --> node_218
    node_802 --> node_41
    node_340 --> node_751
    node_842 --> node_620
    node_229 --> node_831
    node_483 --> node_40
    node_754 --> node_681
    node_828 --> node_593
    node_222 --> node_600
    node_221 --> node_693
    node_11 --> node_680
    node_47 --> node_153
    node_222 --> node_555
    node_228 --> node_600
    node_228 --> node_323
    node_279 --> node_263
    node_222 --> node_588
    node_636 --> node_219
    node_642 --> node_693
    node_228 --> node_588
    node_279 --> node_48
    node_83 --> node_59
    node_229 --> node_672
    node_229 --> node_853
    node_247 --> node_47
    node_83 --> node_644
    node_483 --> node_32
    node_229 --> node_754
    node_606 --> node_610
    node_228 --> node_676
    node_263 --> node_608
    node_307 --> node_708
    node_754 --> node_219
    node_781 --> node_778
    node_344 --> node_823
    node_427 --> node_50
    node_293 --> node_28
    node_13 --> node_319
    node_406 --> node_550
    node_230 --> node_28
    node_583 --> node_609
    node_375 --> node_568
    node_636 --> node_776
    node_300 --> node_41
    node_654 --> node_838
    node_755 --> node_845
    node_8 --> node_666
    node_90 --> node_99
    node_11 --> node_831
    node_242 --> node_86
    node_247 --> node_775
    node_307 --> node_813
    node_222 --> node_821
    node_620 --> node_618
    node_427 --> node_43
    node_654 --> node_607
    node_533 --> node_529
    node_218 --> node_641
    node_553 --> node_591
    node_276 --> node_374
    node_340 --> node_641
    node_247 --> node_686
    node_32 --> node_352
    node_251 --> node_350
    node_340 --> node_721
    node_483 --> node_512
    node_248 --> node_101
    node_339 --> node_661
    node_222 --> node_743
    node_11 --> node_754
    node_754 --> node_725
    node_42 --> node_177
    node_726 --> node_724
    node_228 --> node_743
    node_247 --> node_544
    node_654 --> node_579
    node_698 --> node_696
    node_754 --> node_590
    node_222 --> node_671
    node_629 --> node_634
    node_247 --> node_598
    node_228 --> node_671
    node_229 --> node_620
    node_194 --> node_89
    node_8 --> node_675
    node_8 --> node_833
    node_828 --> node_725
    node_43 --> node_168
    node_221 --> node_321
    node_478 --> node_371
    node_667 --> node_298
    node_755 --> node_654
    node_828 --> node_590
    node_708 --> node_609
    node_247 --> node_128
    node_228 --> node_709
    node_340 --> node_761
    node_406 --> node_431
    node_13 --> node_332
    node_17 --> node_805
    node_11 --> node_842
    node_698 --> node_699
    node_754 --> node_599
    node_292 --> node_553
    node_738 --> node_587
    node_842 --> node_759
    node_449 --> node_181
    node_237 --> node_694
    node_297 --> node_296
    node_383 --> node_381
    node_237 --> node_693
    node_294 --> node_517
    node_828 --> node_594
    node_212 --> node_641
    node_557 --> node_556
    node_437 --> node_641
    node_340 --> node_345
    node_692 --> node_694
    node_692 --> node_693
    node_47 --> node_68
    node_560 --> node_219
    node_47 --> node_809
    node_222 --> node_4
    node_251 --> node_13
    node_750 --> node_748
    node_343 --> node_631
    node_17 --> node_694
    node_228 --> node_4
    node_307 --> node_689
    node_654 --> node_731
    node_247 --> node_593
    node_754 --> node_680
    node_326 --> node_641
    node_654 --> node_815
    node_248 --> node_298
    node_332 --> node_615
    node_687 --> node_604
    node_373 --> node_47
    node_755 --> node_751
    node_828 --> node_763
    node_222 --> node_374
    node_654 --> node_628
    node_247 --> node_145
    node_228 --> node_307
    node_339 --> node_656
    node_607 --> node_606
    node_828 --> node_680
    node_560 --> node_776
    node_672 --> node_670
    node_672 --> node_669
    node_266 --> node_285
    node_755 --> node_646
    node_40 --> node_41
    node_8 --> node_394
    node_276 --> node_840
    node_222 --> node_619
    node_223 --> node_641
    node_168 --> node_57
    node_442 --> node_693
    node_754 --> node_831
    node_342 --> node_679
    node_265 --> node_318
    node_81 --> node_70
    node_307 --> node_686
    node_247 --> node_382
    node_247 --> node_132
    node_291 --> node_40
    node_247 --> node_746
    node_409 --> node_4
    node_667 --> node_62
    node_198 --> node_641
    node_339 --> node_646
    node_304 --> node_662
    node_828 --> node_731
    node_340 --> node_815
    node_222 --> node_835
    node_318 --> node_757
    node_228 --> node_835
    node_291 --> node_32
    node_300 --> node_759
    node_602 --> node_609
    node_291 --> node_219
    node_228 --> node_321
    node_8 --> node_122
    node_222 --> node_826
    node_475 --> node_33
    node_63 --> node_191
    node_83 --> node_693
    node_172 --> node_693
    node_228 --> node_826
    node_247 --> node_652
    node_8 --> node_781
    node_420 --> node_544
    node_755 --> node_813
    node_250 --> node_251
    node_579 --> node_578
    node_222 --> node_658
    node_64 --> node_777
    node_247 --> node_533
    node_247 --> node_650
    node_263 --> node_641
    node_339 --> node_659
    node_548 --> node_542
    node_781 --> node_694
    node_291 --> node_414
    node_754 --> node_842
    node_781 --> node_693
    node_11 --> node_759
    node_250 --> node_243
    node_229 --> node_756
    node_291 --> node_776
    node_467 --> node_188
    node_222 --> node_636
    node_483 --> node_374
    node_326 --> node_47
    node_485 --> node_135
    node_654 --> node_681
    node_228 --> node_636
    node_248 --> node_62
    node_242 --> node_851
    node_552 --> node_13
    node_263 --> node_827
    node_775 --> node_76
    node_8 --> node_522
    node_291 --> node_259
    node_420 --> node_383
    node_512 --> node_174
    node_8 --> node_278
    node_356 --> node_132
    node_828 --> node_842
    node_340 --> node_791
    node_247 --> node_594
    node_13 --> node_347
    node_84 --> node_777
    node_772 --> node_765
    node_8 --> node_201
    node_776 --> node_47
    node_842 --> node_829
    node_307 --> node_593
    node_47 --> node_677
    node_47 --> node_795
    node_307 --> node_849
    node_842 --> node_854
    node_8 --> node_747
    node_754 --> node_752
    node_654 --> node_443
    node_217 --> node_637
    node_307 --> node_681
    node_222 --> node_707
    node_755 --> node_579
    node_8 --> node_45
    node_842 --> node_591
    node_17 --> node_88
    node_247 --> node_763
    node_247 --> node_327
    node_332 --> node_611
    node_357 --> node_363
    node_512 --> node_487
    node_8 --> node_120
    node_324 --> node_38
    node_475 --> node_292
    node_276 --> node_562
    node_339 --> node_657
    node_553 --> node_585
    node_755 --> node_689
    node_828 --> node_723
    node_524 --> node_585
    node_1 --> node_286
    node_228 --> node_303
    node_266 --> node_280
    node_222 --> node_649
    node_636 --> node_218
    node_82 --> node_73
    node_462 --> node_775
    node_8 --> node_235
    node_483 --> node_31
    node_47 --> node_50
    node_8 --> node_843
    node_32 --> node_317
    node_518 --> node_62
    node_32 --> node_522
    node_47 --> node_789
    node_229 --> node_829
    node_667 --> node_108
    node_775 --> node_804
    node_640 --> node_639
    node_654 --> node_599
    node_195 --> node_47
    node_677 --> node_396
    node_307 --> node_725
    node_658 --> node_644
    node_681 --> node_682
    node_229 --> node_854
    node_636 --> node_608
    node_307 --> node_590
    node_755 --> node_815
    node_263 --> node_86
    node_340 --> node_817
    node_20 --> node_252
    node_336 --> node_584
    node_483 --> node_840
    node_318 --> node_588
    node_82 --> node_85
    node_842 --> node_755
    node_247 --> node_41
    node_420 --> node_652
    node_755 --> node_628
    node_772 --> node_609
    node_32 --> node_45
    node_291 --> node_575
    node_20 --> node_356
    node_754 --> node_759
    node_420 --> node_533
    node_400 --> node_399
    node_842 --> node_687
    node_242 --> node_51
    node_250 --> node_226
    node_281 --> node_41
    node_636 --> node_635
    node_267 --> node_775
    node_307 --> node_594
    node_8 --> node_719
    node_842 --> node_734
    node_842 --> node_814
    node_828 --> node_759
    node_11 --> node_829
    node_333 --> node_772
    node_8 --> node_742
    node_484 --> node_172
    node_8 --> node_640
    node_11 --> node_854
    node_745 --> node_394
    node_156 --> node_693
    node_223 --> node_87
    node_94 --> node_93
    node_248 --> node_108
    node_222 --> node_562
    node_738 --> node_590
    node_828 --> node_675
    node_478 --> node_372
    node_445 --> node_152
    node_849 --> node_637
    node_8 --> node_415
    node_654 --> node_668
    node_11 --> node_591
    node_8 --> node_673
    node_41 --> node_602
    node_775 --> node_806
    node_560 --> node_658
    node_307 --> node_680
    node_422 --> node_102
    node_654 --> node_831
    node_221 --> node_641
    node_222 --> node_839
    node_8 --> node_816
    node_424 --> node_47
    node_842 --> node_824
    node_642 --> node_641
    node_247 --> node_62
    node_8 --> node_629
    node_420 --> node_327
    node_8 --> node_476
    node_229 --> node_755
    node_304 --> node_656
    node_560 --> node_218
    node_228 --> node_582
    node_231 --> node_108
    node_473 --> node_154
    node_654 --> node_853
    node_654 --> node_672
    node_654 --> node_754
    node_755 --> node_849
    node_230 --> node_4
    node_247 --> node_723
    node_8 --> node_365
    node_337 --> node_762
    node_335 --> node_682
    node_222 --> node_242
    node_17 --> node_137
    node_47 --> node_810
    node_47 --> node_694
    node_364 --> node_372
    node_755 --> node_681
    node_228 --> node_400
    node_229 --> node_687
    node_34 --> node_540
    node_525 --> node_587
    node_814 --> node_813
    node_291 --> node_288
    node_17 --> node_180
    node_222 --> node_626
    node_222 --> node_708
    node_553 --> node_588
    node_228 --> node_626
    node_292 --> node_287
    node_229 --> node_734
    node_229 --> node_814
    node_524 --> node_588
    node_483 --> node_557
    node_560 --> node_608
    node_626 --> node_622
    node_287 --> node_396
    node_640 --> node_693
    node_358 --> node_4
    node_247 --> node_15
    node_223 --> node_281
    node_222 --> node_823
    node_63 --> node_166
    node_542 --> node_545
    node_228 --> node_823
    node_495 --> node_693
    node_347 --> node_600
    node_667 --> node_130
    node_343 --> node_602
    node_640 --> node_609
    node_815 --> node_644
    node_340 --> node_672
    node_547 --> node_542
    node_692 --> node_642
    node_483 --> node_217
    node_654 --> node_620
    node_337 --> node_763
    node_75 --> node_67
    node_11 --> node_687
    node_667 --> node_45
    node_8 --> node_625
    node_229 --> node_824
    node_229 --> node_667
    node_247 --> node_666
    node_42 --> node_804
    node_247 --> node_305
    node_11 --> node_734
    node_11 --> node_814
    node_307 --> node_842
    node_375 --> node_4
    node_470 --> node_783
    node_775 --> node_149
    node_288 --> node_261
    node_56 --> node_75
    node_210 --> node_775
    node_291 --> node_218
    node_340 --> node_802
    node_755 --> node_725
    node_754 --> node_829
    node_755 --> node_590
    node_8 --> node_830
    node_124 --> node_397
    node_8 --> node_807
    node_768 --> node_769
    node_229 --> node_828
    node_291 --> node_442
    node_8 --> node_651
    node_287 --> node_292
    node_590 --> node_852
    node_235 --> node_678
    node_608 --> node_609
    node_842 --> node_839
    node_247 --> node_675
    node_828 --> node_781
    node_318 --> node_34
    node_541 --> node_540
    node_754 --> node_591
    node_247 --> node_833
    node_276 --> node_683
    node_291 --> node_3
    node_11 --> node_824
    node_47 --> node_192
    node_263 --> node_851
    node_291 --> node_413
    node_291 --> node_608
    node_340 --> node_620
    node_755 --> node_599
    node_17 --> node_641
    node_497 --> node_67
    node_20 --> node_555
    node_247 --> node_448
    node_8 --> node_732
    node_828 --> node_591
    node_276 --> node_383
    node_8 --> node_795
    node_8 --> node_429
    node_636 --> node_827
    node_267 --> node_344
    node_709 --> node_587
    node_42 --> node_806
    node_63 --> node_185
    node_291 --> node_552
    node_182 --> node_45
    node_755 --> node_680
    node_739 --> node_590
    node_442 --> node_641
    node_237 --> node_775
    node_826 --> node_642
    node_228 --> node_316
    node_247 --> node_487
    node_288 --> node_255
    node_842 --> node_604
    node_423 --> node_777
    node_63 --> node_786
    node_66 --> node_678
    node_739 --> node_586
    node_525 --> node_683
    node_781 --> node_642
    node_222 --> node_775
    node_247 --> node_550
    node_559 --> node_761
    node_755 --> node_668
    node_324 --> node_668
    node_222 --> node_686
    node_250 --> node_221
    node_214 --> node_804
    node_491 --> node_799
    node_776 --> node_73
    node_833 --> node_587
    node_208 --> node_693
    node_172 --> node_641
    node_512 --> node_449
    node_755 --> node_831
    node_63 --> node_154
    node_222 --> node_544
    node_8 --> node_127
    node_300 --> node_757
    node_228 --> node_544
    node_754 --> node_843
    node_222 --> node_598
    node_229 --> node_726
    node_250 --> node_246
    node_291 --> node_9
    node_267 --> node_343
    node_8 --> node_588
    node_307 --> node_759
    node_47 --> node_784
    node_340 --> node_794
    node_64 --> node_76
    node_755 --> node_754
    node_828 --> node_843
    node_719 --> node_38
    node_291 --> node_557
    node_667 --> node_68
    node_8 --> node_676
    node_350 --> node_351
    node_238 --> node_132
    node_63 --> node_164
    node_247 --> node_570
    node_731 --> node_728
    node_654 --> node_756
    node_307 --> node_675
    node_306 --> node_333
    node_692 --> node_86
    node_247 --> node_122
    node_270 --> node_795
    node_247 --> node_431
    node_352 --> node_351
    node_228 --> node_731
    node_228 --> node_251
    node_247 --> node_781
    node_263 --> node_51
    node_291 --> node_393
    node_147 --> node_62
    node_20 --> node_4
    node_276 --> node_652
    node_291 --> node_217
    node_42 --> node_149
    node_341 --> node_337
    node_524 --> node_589
    node_607 --> node_642
    node_739 --> node_584
    node_47 --> node_790
    node_590 --> node_591
    node_332 --> node_610
    node_454 --> node_190
    node_276 --> node_533
    node_324 --> node_663
    node_538 --> node_536
    node_754 --> node_719
    node_276 --> node_577
    node_83 --> node_775
    node_63 --> node_807
```

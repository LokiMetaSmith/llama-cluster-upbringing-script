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
| `.github/workflows/docker-publish.yml` | 🔴 Orphan | File: docker-publish.yml |  |
| `.github/workflows/jules-queue.yml` | 🟢 Referenced | File: jules-queue.yml |  |
| `.github/workflows/remote-verify.yml` | 🟢 Referenced | File: remote-verify.yml |  |
| `.github/workflows/test-cluster.yml` | 🔴 Orphan | File: test-cluster.yml |  |
| `.gitignore` | 🟢 Referenced | Ignore all log files |  |
| `.gitmodules` | 🔴 Orphan | File: .gitmodules |  |
| `.husky/pre-push` | 🟢 Referenced | File: pre-push |  |
| `.markdownlint.json` | 🟢 Referenced | File: .markdownlint.json |  |
| `.opencode/README.md` | 🟢 Referenced | OpenCode Configuration |  |
| `.opencode/opencode.json` | 🟢 Referenced | File: opencode.json |  |
| `.sops.yaml` | 🟢 Referenced | File: .sops.yaml |  |
| `.yamllint` | 🟢 Referenced | File: .yamllint |  |
| `AGENTS.md` | 🟢 Referenced | AGENTS.md |  |
| `LICENSE` | 🟢 Referenced | File: LICENSE |  |
| `README.md` | 🟢 Referenced | Distributed Conversational AI Pipeline for Legacy CPU Clusters |  |
| `TODO.md` | 🟢 Referenced | TODO |  |
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
| `ansible/requirements.yml` | 🔴 Orphan | File: requirements.yml |  |
| `ansible/roles/README.md` | 🟢 Referenced | Ansible Roles |  |
| `ansible/roles/authentik/defaults/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/authentik/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/authentik/templates/authentik.nomad.j2` | 🟢 Referenced | File: authentik.nomad.j2 |  |
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
| `ansible/roles/monitoring/templates/beszel.nomad.j2` | 🟢 Referenced | File: beszel.nomad.j2 |  |
| `ansible/roles/monitoring/templates/dashboards.yaml.j2` | 🟢 Referenced | File: dashboards.yaml.j2 |  |
| `ansible/roles/monitoring/templates/datasource.yaml.j2` | 🟢 Referenced | File: datasource.yaml.j2 |  |
| `ansible/roles/monitoring/templates/grafana.nomad.j2` | 🟢 Referenced | Update stanza for reliability |  |
| `ansible/roles/monitoring/templates/memory-audit.nomad.j2` | 🟢 Referenced | File: memory-audit.nomad.j2 |  |
| `ansible/roles/monitoring/templates/mqtt-exporter.nomad.j2` | 🟢 Referenced | Update stanza for reliability |  |
| `ansible/roles/monitoring/templates/node-exporter.nomad.j2` | 🟢 Referenced | File: node-exporter.nomad.j2 |  |
| `ansible/roles/monitoring/templates/prometheus.nomad.j2` | 🟢 Referenced | Update stanza for reliability |  |
| `ansible/roles/monitoring/templates/prometheus.yml.j2` | 🟢 Referenced | File: prometheus.yml.j2 |  |
| `ansible/roles/monitoring/templates/statsping.nomad.j2` | 🟢 Referenced | File: statsping.nomad.j2 |  |
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
| `ansible/roles/paperless/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/paperless/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/paperless/templates/paperless.nomad.j2` | 🟢 Referenced | File: paperless.nomad.j2 |  |
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
| `ansible/roles/tpm_ssh/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/tpm_ssh/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |  |
| `ansible/roles/tpm_ssh/templates/tpm-ssh-agent.service.j2` | 🟢 Referenced | File: tpm-ssh-agent.service.j2 |  |
| `ansible/roles/tpm_ssh/templates/tpm-ssh-agent.sh.j2` | 🟢 Referenced | bin/bash |  |
| `ansible/roles/tpm_ssh/templates/tpm_pins.j2` | 🟢 Referenced | This file contains the PINs required to unlock the TPM PKCS#11 token. |  |
| `ansible/roles/traefik/defaults/main.yml` | 🟢 Referenced | File: main.yml |  |
| `ansible/roles/traefik/tasks/main.yml` | 🟢 Referenced | File: main.yml |  |
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
| `docs/manual/AGENTS.md` | 🟢 Referenced | AI Agent Architectures |  |
| `docs/AGENT_LIGHTNING_ANALYSIS.md` | 📄 Documentation/Asset | Agent Lightning Analysis |  |
| `docs/AI_GOVERNANCE.md` | 📄 Documentation/Asset | AI Governance & Architecture Plan |  |
| `docs/manual/ARCHITECTURE.md` | 🟢 Referenced | Holistic Project Architecture |  |
| `docs/BENCHMARKING.MD` | 🟢 Referenced | A Guide to Benchmarking Your AI Cluster |  |
| `docs/CLAMAV_EVALUATION.md` | 📄 Documentation/Asset | ClamAV Evaluation Report |  |
| `docs/CLAUDE_CODE_ANALYSIS.md` | 🟢 Referenced | Claude Code CLI Analysis |  |
| `docs/DEPLOYMENT_AND_PROFILING.md` | 🟢 Referenced | Deploying and Profiling AI Services |  |
| `docs/EVALUATION_LLMROUTER.md` | 📄 Documentation/Asset | LLMRouter Evaluation Report |  |
| `docs/FLOWISE_ANALYSIS.md` | 🟢 Referenced | Flowise Architecture & UI Analysis |  |
| `docs/FRONTEND_VERIFICATION.md` | 🟢 Referenced | Frontend Verification Instructions with Playwright |  |
| `docs/FRONTIER_AGENT_ROADMAP.md` | 📄 Documentation/Asset | Frontier Agent Roadmap |  |
| `docs/GASTOWN_TODO.md` | 📄 Documentation/Asset | Gas Town Integration Todo |  |
| `docs/GCP_GENERATIVE_AI_REVIEW.md` | 📄 Documentation/Asset | Google Cloud Platform Generative AI Review |  |
| `docs/GEMINI.md` | 🟢 Referenced | GEMINI.md |  |
| `docs/IPV6_AUDIT.md` | 📄 Documentation/Asset | IPv6 Audit Report |  |
| `docs/LANGCHAIN_ANALYSIS.md` | 📄 Documentation/Asset | LangChain Analysis and Hybrid Integration Report |  |
| `docs/MCP_SERVER_SETUP.md` | 🟢 Referenced | Building an MCP Server with Service Discovery |  |
| `docs/MEMENTO_SKILLS_ANALYSIS.md` | 📄 Documentation/Asset | Memento-Skills Architecture Analysis |  |
| `docs/MEMORIES.md` | 🟢 Referenced | Agent Memories |  |
| `docs/NETWORK.md` | 🟢 Referenced | Network Architecture |  |
| `docs/NIXOS_PXE_BOOT_SETUP.md` | 🟢 Referenced | NixOS-based PXE Boot Server Setup |  |
| `docs/OBSIDIAN_TODO.md` | 📄 Documentation/Asset | Obsidian & 3D Workflow Integration Todo List |  |
| `docs/OBSIDIAN_WORKFLOW_DESIGN.md` | 🟢 Referenced | Obsidian Workflow Design: The "Active Vault" Architecture |  |
| `docs/PASEO_ANALYSIS.md` | 🟢 Referenced | Paseo Analysis: Architecture and Concepts for PipecatApp Integration |  |
| `docs/PERFORMANCE_OPTIMIZATION.md` | 📄 Documentation/Asset | Performance & I/O Optimization |  |
| `docs/PROJECT_SUMMARY.md` | 🟢 Referenced | Project Summary: Architecting a Responsive, Distributed Conversational AI Pipeline |  |
| `docs/manual/PXE_BOOT_SETUP.md` | 🟢 Referenced | iPXE Boot Server Setup for Automated Debian Installation |  |
| `docs/README.md` | 🟢 Referenced | Project Documentation |  |
| `docs/REFACTOR_PROPOSAL_hybrid_architecture.md` | 🟢 Referenced | Refactoring Proposal: Hybrid / Cluster-Native Architecture |  |
| `docs/REMOTE_WORKFLOW.md` | 🟢 Referenced | Improving Your Remote Workflow with Mosh and Tmux |  |
| `docs/SCALING_TODO.md` | 📄 Documentation/Asset | Scaling Long-Running Autonomous Coding - Implementation Scope |  |
| `docs/SECURITY_AUDIT.md` | 📄 Documentation/Asset | Security Audit Log |  |
| `docs/TODO_Hybrid_Architecture.md` | 🟢 Referenced | Hybrid Architecture Implementation To-Do List |  |
| `docs/TOOL_EVALUATION.md` | 🟢 Referenced | Tool Evaluation and Strategic Direction |  |
| `docs/manual/TROUBLESHOOTING.md` | 🟢 Referenced | Troubleshooting Guide |  |
| `docs/VLLM_PROJECT_EVALUATION.md` | 📄 Documentation/Asset | vLLM Project Evaluation |  |
| `docs/YAML_FILES_REPORT.md` | 📄 Documentation/Asset | Report on YAML Files in Root Directory |  |
| `docs/analysis/aid_e_log.txt` | 🟢 Referenced | File: aid_e_log.txt |  |
| `docs/heretic_evaluation.md` | 🟢 Referenced | Heretic Repository Evaluation |  |
| `docs/media/initial_state.png` | 📄 Documentation/Asset | File: initial_state.png |  |
| `docs/media/paused_state.png` | 📄 Documentation/Asset | File: paused_state.png |  |
| `docs/review_report.md` | 📄 Documentation/Asset | Project Review Report |  |
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
| `inventory.yaml` | 🟢 Referenced | This inventory is dynamically generated by update_inventory.sh |  |
| `local_inventory.ini` | 🟢 Referenced | File: local_inventory.ini |  |
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
| `os-image/README.md` | 🟢 Referenced | Bootable Pipecat Cluster ISO Configuration |  |
| `os-image/build_iso.sh` | 🟢 Referenced | Builds a custom, bootable, headless Debian ISO for the Pipecat agent cluster. |  |
| `os-image/config/archives/rocm.key.binary` | 🔴 Orphan | File: rocm.key.binary |  |
| `os-image/config/archives/rocm.key.chroot` | 🔴 Orphan | File: rocm.key.chroot |  |
| `os-image/config/archives/rocm.list.binary` | 🔴 Orphan | File: rocm.list.binary |  |
| `os-image/config/archives/rocm.list.chroot` | 🔴 Orphan | File: rocm.list.chroot |  |
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
| `pipecatapp/services/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/services/gemma_e2b_service.py` | 🟢 Referenced | File: gemma_e2b_service.py | **Classes:** GemmaE2BService<br>**Functions:** _resolve_model_path, __init__, _load_model, process_frame, _generate_response... |
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
| `pipecatapp/tool_server.py` | 🟢 Referenced | File: tool_server.py | **Classes:** ToolRequest<br>**Functions:** validation_exception_handler, run_tool, list_tools |
| `pipecatapp/tools/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/tools/ansible_tool.py` | 🟢 Referenced | File: ansible_tool.py | **Classes:** Ansible_Tool<br>**Functions:** __init__, run_playbook |
| `pipecatapp/tools/archivist_tool.py` | 🟢 Referenced | File: archivist_tool.py | **Classes:** ArchivistTool<br>**Functions:** __init__, run, __call__ |
| `pipecatapp/tools/atproto_tool.py` | 🟢 Referenced | File: atproto_tool.py | **Classes:** ATProtoTool<br>**Functions:** __init__, _get_client, send_post, get_timeline |
| `pipecatapp/tools/autoloop_tool.py` | 🔴 Orphan | File: autoloop_tool.py | **Classes:** AutoloopTool<br>**Functions:** __init__, run, main, local_metric |
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
| `pipecatapp/tools/opencode_provider_tool.py` | 🟢 Referenced | File: opencode_provider_tool.py | **Classes:** OpenCodeProviderTool<br>**Functions:** __init__, _parse_opencode_output, run |
| `pipecatapp/tools/opencode_tool.py` | 🟢 Referenced | File: opencode_tool.py | **Classes:** OpencodeTool<br>**Functions:** __init__, run |
| `pipecatapp/tools/orchestrator_tool.py` | 🟢 Referenced | File: orchestrator_tool.py | **Classes:** OrchestratorTool<br>**Functions:** __init__, dispatch_job |
| `pipecatapp/tools/personality_tool.py` | 🟢 Referenced | File: personality_tool.py | **Classes:** PersonalityTool<br>**Functions:** __init__, set_personality, reset_personality, get_current_personality |
| `pipecatapp/tools/planner_tool.py` | 🟢 Referenced | File: planner_tool.py | **Classes:** PlannerTool<br>**Functions:** __init__, _discover_llm_url, _call_llm, plan_and_execute |
| `pipecatapp/tools/polyphony_tool.py` | 🟢 Referenced | File: polyphony_tool.py | **Classes:** PolyphonyTool<br>**Functions:** __init__, execute, _run_cmd, get_info |
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
| `pipecatapp/tools/skill_builder_tool.py` | 🟢 Referenced | File: skill_builder_tool.py | **Classes:** SkillBuilderTool<br>**Functions:** __init__, execute |
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
| `pipecatapp/workflow/crypto_receipts.py` | 🟢 Referenced | File: crypto_receipts.py | **Classes:** ToolExecutionSigner<br>**Functions:** __init__, _normalize_payload, sign, verify |
| `pipecatapp/workflow/history.py` | 🟢 Referenced | File: history.py | **Classes:** WorkflowHistory<br>**Functions:** __new__, __init__, _init_db, save_run, get_all_runs... |
| `pipecatapp/workflow/node.py` | 🟢 Referenced | File: node.py | **Classes:** Node<br>**Functions:** __init__, execute, get_input, set_output, get_spatial_data |
| `pipecatapp/workflow/nodes/__init__.py` | 🟢 Referenced | File: __init__.py |  |
| `pipecatapp/workflow/nodes/base_nodes.py` | 🟢 Referenced | File: base_nodes.py | **Classes:** InputNode, OutputNode, MergeNode, ConditionalBranchNode, GateNode, PostProcessorNode<br>**Functions:** execute, execute, execute, execute, execute... |
| `pipecatapp/workflow/nodes/emperor_nodes.py` | 🟢 Referenced | File: emperor_nodes.py | **Classes:** EmperorAgentNode<br>**Functions:** resolve_abs_path, read_file_tool, list_files_tool, edit_file_tool, shell_tool... |
| `pipecatapp/workflow/nodes/langchain_nodes.py` | 🔴 Orphan | File: langchain_nodes.py | **Classes:** LangGraphNode<br>**Functions:** execute |
| `pipecatapp/workflow/nodes/llm_nodes.py` | 🟢 Referenced | File: llm_nodes.py | **Classes:** VisionLLMNode, PromptBuilderNode, SimpleLLMNode, ExpertRouterNode, ExternalLLMNode, LLMRouterNode, LoopedReasoningNode<br>**Functions:** discover_main_llm_service, execute, execute, execute, execute... |
| `pipecatapp/workflow/nodes/ralph_nodes.py` | 🟢 Referenced | File: ralph_nodes.py | **Classes:** RalphLoopNode<br>**Functions:** execute |
| `pipecatapp/workflow/nodes/registry.py` | 🟢 Referenced | File: registry.py | **Classes:** NodeRegistry<br>**Functions:** __init__, register, get_node_class, get_all_nodes_metadata |
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
| `prompt_engineering/autoloop_evolve.py` | 📄 Documentation/Asset | File: autoloop_evolve.py | **Functions:** run_pytest_metric, main |
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
| `replace_runner_merge.txt` | 🔵 Entry Point | Interpolate variables before node instantiation (do not permanently mutate self.workflow_definition) |  |
| `requirements-dev.txt` | 🟢 Referenced | File: requirements-dev.txt |  |
| `resolve_conflict.py` | 🔴 Orphan | I know what the text looks like exactly. |  |
| `run_emperor_test.sh` | 🔵 Entry Point | bin/bash |  |
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
| `scripts/recover_node.py` | 🔵 Entry Point | Robust Remote Node Recovery | **Functions:** ping_node, ipmi_set_pxe_boot, ipmi_reboot, main |
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
| `scripts/update_cluster.sh` | 🔵 Entry Point | update_cluster.sh  This script updates the pipecat-cluster base image from the git repository witho |  |
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
| `tests/unit/test_crypto_receipts.py` | 🧪 Test | Add the necessary path to import the workflow modules | **Functions:** test_sign_receipt, test_verify_receipt |
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
| `tests/unit/test_opencode_provider_tool.py` | 🧪 Test | File: test_opencode_provider_tool.py | **Functions:** test_parse_opencode_output, test_opencode_provider_run_success |
| `tests/unit/test_opencode_tool.py` | 🧪 Test | File: test_opencode_tool.py | **Classes:** TestOpencodeTool<br>**Functions:** setUp, test_run_success, test_run_error |
| `tests/unit/test_orchestrator_tool.py` | 🧪 Test | File: test_orchestrator_tool.py | **Functions:** test_orchestrator_tool_instantiation, test_dispatch_job_success, test_dispatch_job_failure |
| `tests/unit/test_personality_tool.py` | 🧪 Test | File: test_personality_tool.py | **Functions:** test_set_personality, test_reset_personality, test_get_current_personality |
| `tests/unit/test_pipecat_app_unit.py` | 🟢 Referenced | File: test_pipecat_app_unit.py | **Classes:** MockFrameProcessor, MockTranscriptionFrame<br>**Functions:** client, test_read_main, test_health_check, test_workflow_runner_loads_definition, test_health_check_is_healthy... |
| `tests/unit/test_planner_tool.py` | 🧪 Test | File: test_planner_tool.py | **Functions:** mock_twin_service, planner_tool, test_discover_llm_url_router_llm, test_discover_llm_url_fallback, test_discover_llm_url_env_var... |
| `tests/unit/test_playbook_integration.py` | 🟢 Referenced | File: test_playbook_integration.py | **Functions:** test_playbook_integration_syntax_check |
| `tests/unit/test_poc_ensemble.py` | 🧪 Test | File: test_poc_ensemble.py | **Classes:** TestPoCEnsemble<br>**Functions:** setUp, test_workflow_execution, mock_post, mock_get, run_workflow |
| `tests/unit/test_polyphony_tool.py` | 🧪 Test | File: test_polyphony_tool.py | **Classes:** TestPolyphonyTool<br>**Functions:** test_share_action, test_ping_action, test_task_list, test_missing_cli |
| `tests/unit/test_power_tool.py` | 🟢 Referenced | File: test_power_tool.py | **Functions:** power_tool, test_set_idle_threshold_for_new_service, test_set_idle_threshold_for_existing_service, test_config_directory_not_found, test_file_io_error... |
| `tests/unit/test_project_mapper_tool.py` | 🧪 Test | File: test_project_mapper_tool.py | **Classes:** TestProjectMapperTool<br>**Functions:** tool, temp_project, test_is_ignored, test_guess_type, test_extract_imports_python... |
| `tests/unit/test_prompt_engineering.py` | 🟢 Referenced | File: test_prompt_engineering.py | **Classes:** TestEvolve, TestRunCampaign, TestPromoteAgent, TestVisualizeArchive<br>**Functions:** mock_archive, test_select_parent_from_archive_empty, test_select_parent_from_archive_populated, test_run_evolution, test_run_campaign_args... |
| `tests/unit/test_prompt_improver_tool.py` | 🧪 Test | File: test_prompt_improver_tool.py | **Classes:** TestPromptImproverTool<br>**Functions:** setUp, test_create_prompt_plan, test_discover_llm_failure |
| `tests/unit/test_provisioning.py` | 🟢 Referenced | File: test_provisioning.py | **Classes:** TestProvisioning<br>**Functions:** setUp, tearDown, test_load_playbooks_from_manifest, test_wait_for_ports_freed, test_cleanup_memory_for_core_ai... |
| `tests/unit/test_rag_tool.py` | 🟢 Referenced | File: test_rag_tool.py | **Classes:** SyncThread<br>**Functions:** mock_sentence_transformer, mock_faiss, mock_pmm_memory, sync_threading, test_rag_tool_initialization... |
| `tests/unit/test_ralph_nodes.py` | 🧪 Test | File: test_ralph_nodes.py | **Functions:** test_ralph_loop_success, test_ralph_loop_failure_then_success |
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
        node_14[".coverage"]
        node_1[".djlint.toml"]
        node_9[".gitattributes"]
        node_0[".gitignore"]
        node_23[".gitmodules"]
        node_22[".markdownlint.json"]
        node_10[".sops.yaml"]
        node_30[".yamllint"]
        node_18["AGENTS.md"]
        node_7["LICENSE"]
        node_29["README.md"]
        node_6["TODO.md"]
        node_24["ansible.cfg"]
        node_2["bootstrap.sh"]
        node_20["hostfile"]
        node_31["inventory.yaml"]
        node_25["local_inventory.ini"]
        node_28["package.json"]
        node_11["playbook.yaml"]
        node_8["pytest.ini"]
        node_3["replace_runner_merge.txt"]
        node_12["requirements-dev.txt"]
        node_16["resolve_conflict.py"]
        node_21["run_emperor_test.sh"]
        node_19["test_autoresearch.py"]
        node_27["test_clamav_playbook.yml"]
        node_26["test_db.sqlite-shm"]
        node_4["test_db.sqlite-wal"]
        node_13["test_dlq.db-shm"]
        node_15["test_dlq.db-wal"]
        node_17["test_playbook.yml"]
        node_5["test_script.py"]
    end
    subgraph dir__githooks [.githooks]
        direction TB
        node_394["pre-commit"]
    end
    subgraph dir__github [.github]
        direction TB
        node_501["AGENTIC_README.md"]
    end
    subgraph dir__github_workflows [.github/workflows]
        direction TB
        node_504["auto-merge.yml"]
        node_507["ci.yml"]
        node_506["create-issues-from-files.yml"]
        node_505["docker-publish.yml"]
        node_508["jules-queue.yml"]
        node_502["remote-verify.yml"]
        node_503["test-cluster.yml"]
    end
    subgraph dir__husky [.husky]
        direction TB
        node_395["pre-push"]
    end
    subgraph dir__opencode [.opencode]
        direction TB
        node_563["README.md"]
        node_562["opencode.json"]
    end
    subgraph dir_ansible [ansible]
        direction TB
        node_710["README.md"]
        node_708["lint_nomad.yaml"]
        node_707["requirements.yml"]
        node_709["run_download_models.yaml"]
    end
    subgraph dir_ansible_filter_plugins [ansible/filter_plugins]
        direction TB
        node_712["README.md"]
        node_711["safe_flatten.py"]
    end
    subgraph dir_ansible_jobs [ansible/jobs]
        direction TB
        node_730["README.md"]
        node_728["benchmark.nomad"]
        node_726["evolve-prompt.nomad.j2"]
        node_727["expert-debug.nomad"]
        node_731["expert.nomad.j2"]
        node_724["filebrowser.nomad.j2"]
        node_719["health-check.nomad.j2"]
        node_722["llamacpp-batch.nomad.j2"]
        node_725["llamacpp-rpc.nomad.j2"]
        node_729["model-benchmark.nomad.j2"]
        node_723["pipecatapp.nomad"]
        node_718["router.nomad.j2"]
        node_721["test-runner.nomad.j2"]
        node_720["vllm.nomad.j2"]
    end
    subgraph dir_ansible_roles [ansible/roles]
        direction TB
        node_732["README.md"]
    end
    subgraph dir_ansible_roles_authentik_defaults [ansible/roles/authentik/defaults]
        direction TB
        node_1019["main.yml"]
    end
    subgraph dir_ansible_roles_authentik_tasks [ansible/roles/authentik/tasks]
        direction TB
        node_1018["main.yml"]
    end
    subgraph dir_ansible_roles_authentik_templates [ansible/roles/authentik/templates]
        direction TB
        node_1017["authentik.nomad.j2"]
    end
    subgraph dir_ansible_roles_benchmark_models_tasks [ansible/roles/benchmark_models/tasks]
        direction TB
        node_878["benchmark_loop.yaml"]
        node_877["main.yaml"]
    end
    subgraph dir_ansible_roles_benchmark_models_templates [ansible/roles/benchmark_models/templates]
        direction TB
        node_876["model-benchmark.nomad.j2"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_defaults [ansible/roles/bootstrap_agent/defaults]
        direction TB
        node_1006["main.yaml"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_tasks [ansible/roles/bootstrap_agent/tasks]
        direction TB
        node_1005["deploy_llama_cpp_model.yaml"]
        node_1004["main.yaml"]
    end
    subgraph dir_ansible_roles_clamav_files [ansible/roles/clamav/files]
        direction TB
        node_1003["rogue_agent.ldb"]
    end
    subgraph dir_ansible_roles_clamav_handlers [ansible/roles/clamav/handlers]
        direction TB
        node_1001["main.yaml"]
    end
    subgraph dir_ansible_roles_clamav_tasks [ansible/roles/clamav/tasks]
        direction TB
        node_1002["main.yaml"]
    end
    subgraph dir_ansible_roles_claude_clone_tasks [ansible/roles/claude_clone/tasks]
        direction TB
        node_841["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tools_tasks [ansible/roles/common-tools/tasks]
        direction TB
        node_844["main.yaml"]
    end
    subgraph dir_ansible_roles_common_handlers [ansible/roles/common/handlers]
        direction TB
        node_780["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tasks [ansible/roles/common/tasks]
        direction TB
        node_781["main.yaml"]
        node_782["network_repair.yaml"]
    end
    subgraph dir_ansible_roles_common_templates [ansible/roles/common/templates]
        direction TB
        node_777["cluster-ip-alias.service.j2"]
        node_778["hosts.j2"]
        node_779["update-ssh-authorized-keys.sh.j2"]
    end
    subgraph dir_ansible_roles_config_manager_tasks [ansible/roles/config_manager/tasks]
        direction TB
        node_991["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_defaults [ansible/roles/consul/defaults]
        direction TB
        node_924["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_handlers [ansible/roles/consul/handlers]
        direction TB
        node_920["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_tasks [ansible/roles/consul/tasks]
        direction TB
        node_922["acl.yaml"]
        node_921["main.yaml"]
        node_923["tls.yaml"]
    end
    subgraph dir_ansible_roles_consul_templates [ansible/roles/consul/templates]
        direction TB
        node_918["consul.hcl.j2"]
        node_919["consul.service.j2"]
    end
    subgraph dir_ansible_roles_desktop_extras_tasks [ansible/roles/desktop_extras/tasks]
        direction TB
        node_908["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_handlers [ansible/roles/docker/handlers]
        direction TB
        node_835["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_molecule_default [ansible/roles/docker/molecule/default]
        direction TB
        node_839["converge.yml"]
        node_837["molecule.yml"]
        node_840["prepare.yml"]
        node_838["verify.yml"]
    end
    subgraph dir_ansible_roles_docker_tasks [ansible/roles/docker/tasks]
        direction TB
        node_836["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_templates [ansible/roles/docker/templates]
        direction TB
        node_834["daemon.json.j2"]
    end
    subgraph dir_ansible_roles_docker_registry_tasks [ansible/roles/docker_registry/tasks]
        direction TB
        node_734["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_registry_templates [ansible/roles/docker_registry/templates]
        direction TB
        node_733["docker-registry.nomad.j2"]
    end
    subgraph dir_ansible_roles_download_models_files [ansible/roles/download_models/files]
        direction TB
        node_843["download_hf_repo.py"]
    end
    subgraph dir_ansible_roles_download_models_tasks [ansible/roles/download_models/tasks]
        direction TB
        node_842["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_defaults [ansible/roles/exo/defaults]
        direction TB
        node_1024["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_files [ansible/roles/exo/files]
        direction TB
        node_1025["Dockerfile"]
    end
    subgraph dir_ansible_roles_exo_tasks [ansible/roles/exo/tasks]
        direction TB
        node_1023["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_templates [ansible/roles/exo/templates]
        direction TB
        node_1022["exo.nomad.j2"]
    end
    subgraph dir_ansible_roles_forgejo_handlers [ansible/roles/forgejo/handlers]
        direction TB
        node_883["main.yaml"]
    end
    subgraph dir_ansible_roles_forgejo_tasks [ansible/roles/forgejo/tasks]
        direction TB
        node_884["main.yaml"]
    end
    subgraph dir_ansible_roles_forgejo_templates [ansible/roles/forgejo/templates]
        direction TB
        node_882["forgejo.nomad.j2"]
    end
    subgraph dir_ansible_roles_gemini_cli_handlers [ansible/roles/gemini_cli/handlers]
        direction TB
        node_801["main.yaml"]
    end
    subgraph dir_ansible_roles_gemini_cli_tasks [ansible/roles/gemini_cli/tasks]
        direction TB
        node_802["main.yaml"]
    end
    subgraph dir_ansible_roles_gemini_cli_templates [ansible/roles/gemini_cli/templates]
        direction TB
        node_800["gemini.nomad.j2"]
    end
    subgraph dir_ansible_roles_headscale_defaults [ansible/roles/headscale/defaults]
        direction TB
        node_755["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_handlers [ansible/roles/headscale/handlers]
        direction TB
        node_753["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_tasks [ansible/roles/headscale/tasks]
        direction TB
        node_754["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_templates [ansible/roles/headscale/templates]
        direction TB
        node_752["config.yaml.j2"]
        node_751["headscale.service.j2"]
    end
    subgraph dir_ansible_roles_heretic_tool_defaults [ansible/roles/heretic_tool/defaults]
        direction TB
        node_875["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_meta [ansible/roles/heretic_tool/meta]
        direction TB
        node_874["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_tasks [ansible/roles/heretic_tool/tasks]
        direction TB
        node_873["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_meta [ansible/roles/home_assistant/meta]
        direction TB
        node_899["main.yaml"]
        node_900["main.yml"]
    end
    subgraph dir_ansible_roles_home_assistant_tasks [ansible/roles/home_assistant/tasks]
        direction TB
        node_898["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_templates [ansible/roles/home_assistant/templates]
        direction TB
        node_896["configuration.yaml.j2"]
        node_897["home_assistant.nomad.j2"]
    end
    subgraph dir_ansible_roles_kittentts_tasks [ansible/roles/kittentts/tasks]
        direction TB
        node_760["main.yaml"]
    end
    subgraph dir_ansible_roles_librarian_defaults [ansible/roles/librarian/defaults]
        direction TB
        node_860["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_handlers [ansible/roles/librarian/handlers]
        direction TB
        node_858["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_tasks [ansible/roles/librarian/tasks]
        direction TB
        node_859["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_templates [ansible/roles/librarian/templates]
        direction TB
        node_857["librarian.service.j2"]
        node_855["librarian_agent.py.j2"]
        node_856["spacedrive.service.j2"]
    end
    subgraph dir_ansible_roles_llama_cpp_files [ansible/roles/llama_cpp/files]
        direction TB
        node_789["realtime_steering.patch"]
    end
    subgraph dir_ansible_roles_llama_cpp_handlers [ansible/roles/llama_cpp/handlers]
        direction TB
        node_783["main.yaml"]
    end
    subgraph dir_ansible_roles_llama_cpp_molecule_default [ansible/roles/llama_cpp/molecule/default]
        direction TB
        node_788["converge.yml"]
        node_786["molecule.yml"]
        node_787["verify.yml"]
    end
    subgraph dir_ansible_roles_llama_cpp_tasks [ansible/roles/llama_cpp/tasks]
        direction TB
        node_784["main.yaml"]
        node_785["run_single_rpc_job.yaml"]
    end
    subgraph dir_ansible_roles_llmfit_tasks [ansible/roles/llmfit/tasks]
        direction TB
        node_1016["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_tasks [ansible/roles/llxprt_code/tasks]
        direction TB
        node_1021["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_templates [ansible/roles/llxprt_code/templates]
        direction TB
        node_1020["llxprt-code.env.j2"]
    end
    subgraph dir_ansible_roles_magic_mirror_defaults [ansible/roles/magic_mirror/defaults]
        direction TB
        node_750["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_handlers [ansible/roles/magic_mirror/handlers]
        direction TB
        node_748["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_tasks [ansible/roles/magic_mirror/tasks]
        direction TB
        node_749["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_templates [ansible/roles/magic_mirror/templates]
        direction TB
        node_747["magic_mirror.nomad.j2"]
    end
    subgraph dir_ansible_roles_mcp_server_defaults [ansible/roles/mcp_server/defaults]
        direction TB
        node_912["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_handlers [ansible/roles/mcp_server/handlers]
        direction TB
        node_910["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_tasks [ansible/roles/mcp_server/tasks]
        direction TB
        node_911["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_templates [ansible/roles/mcp_server/templates]
        direction TB
        node_909["mcp_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_graph_tasks [ansible/roles/memory_graph/tasks]
        direction TB
        node_982["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_graph_templates [ansible/roles/memory_graph/templates]
        direction TB
        node_981["memory-graph.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_service_files [ansible/roles/memory_service/files]
        direction TB
        node_848["app.py"]
        node_849["pmm_memory.py"]
    end
    subgraph dir_ansible_roles_memory_service_handlers [ansible/roles/memory_service/handlers]
        direction TB
        node_846["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_tasks [ansible/roles/memory_service/tasks]
        direction TB
        node_847["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_templates [ansible/roles/memory_service/templates]
        direction TB
        node_845["memory_service.nomad.j2"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files [ansible/roles/minikeyvalue/files]
        direction TB
        node_763["Dockerfile"]
        node_765["start_master.py"]
        node_764["volume"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files_src [ansible/roles/minikeyvalue/files/src]
        direction TB
        node_766["lib.go"]
        node_769["lib_test.go"]
        node_771["main.go"]
        node_772["rebalance.go"]
        node_767["rebuild.go"]
        node_768["s3api.go"]
        node_770["server.go"]
    end
    subgraph dir_ansible_roles_minikeyvalue_tasks [ansible/roles/minikeyvalue/tasks]
        direction TB
        node_762["main.yaml"]
    end
    subgraph dir_ansible_roles_minikeyvalue_templates [ansible/roles/minikeyvalue/templates]
        direction TB
        node_761["mkv.nomad.j2"]
    end
    subgraph dir_ansible_roles_miniray_files [ansible/roles/miniray/files]
        direction TB
        node_990["Dockerfile"]
    end
    subgraph dir_ansible_roles_miniray_tasks [ansible/roles/miniray/tasks]
        direction TB
        node_989["main.yaml"]
    end
    subgraph dir_ansible_roles_miniray_templates [ansible/roles/miniray/templates]
        direction TB
        node_988["miniray.nomad.j2"]
    end
    subgraph dir_ansible_roles_moe_gateway_files [ansible/roles/moe_gateway/files]
        direction TB
        node_832["gateway.py"]
    end
    subgraph dir_ansible_roles_moe_gateway_files_static [ansible/roles/moe_gateway/files/static]
        direction TB
        node_833["index.html"]
    end
    subgraph dir_ansible_roles_moe_gateway_handlers [ansible/roles/moe_gateway/handlers]
        direction TB
        node_830["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_tasks [ansible/roles/moe_gateway/tasks]
        direction TB
        node_831["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_templates [ansible/roles/moe_gateway/templates]
        direction TB
        node_829["moe-gateway.nomad.j2"]
    end
    subgraph dir_ansible_roles_monitoring_defaults [ansible/roles/monitoring/defaults]
        direction TB
        node_936["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_files [ansible/roles/monitoring/files]
        direction TB
        node_937["llm_dashboard.json"]
    end
    subgraph dir_ansible_roles_monitoring_tasks [ansible/roles/monitoring/tasks]
        direction TB
        node_935["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_templates [ansible/roles/monitoring/templates]
        direction TB
        node_933["beszel.nomad.j2"]
        node_928["dashboards.yaml.j2"]
        node_927["datasource.yaml.j2"]
        node_934["grafana.nomad.j2"]
        node_925["memory-audit.nomad.j2"]
        node_926["mqtt-exporter.nomad.j2"]
        node_932["node-exporter.nomad.j2"]
        node_929["prometheus.nomad.j2"]
        node_931["prometheus.yml.j2"]
        node_930["statsping.nomad.j2"]
    end
    subgraph dir_ansible_roles_mqtt_handlers [ansible/roles/mqtt/handlers]
        direction TB
        node_862["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_meta [ansible/roles/mqtt/meta]
        direction TB
        node_864["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_tasks [ansible/roles/mqtt/tasks]
        direction TB
        node_863["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_templates [ansible/roles/mqtt/templates]
        direction TB
        node_861["mqtt.nomad.j2"]
    end
    subgraph dir_ansible_roles_nanochat_defaults [ansible/roles/nanochat/defaults]
        direction TB
        node_986["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_handlers [ansible/roles/nanochat/handlers]
        direction TB
        node_984["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_tasks [ansible/roles/nanochat/tasks]
        direction TB
        node_985["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_templates [ansible/roles/nanochat/templates]
        direction TB
        node_983["nanochat.nomad.j2"]
    end
    subgraph dir_ansible_roles_nats_handlers [ansible/roles/nats/handlers]
        direction TB
        node_886["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_tasks [ansible/roles/nats/tasks]
        direction TB
        node_887["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_templates [ansible/roles/nats/templates]
        direction TB
        node_885["nats.nomad.j2"]
    end
    subgraph dir_ansible_roles_nfs_handlers [ansible/roles/nfs/handlers]
        direction TB
        node_976["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_tasks [ansible/roles/nfs/tasks]
        direction TB
        node_977["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_templates [ansible/roles/nfs/templates]
        direction TB
        node_975["exports.j2"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_handlers [ansible/roles/nixos_pxe_server/handlers]
        direction TB
        node_1009["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_tasks [ansible/roles/nixos_pxe_server/tasks]
        direction TB
        node_1010["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_templates [ansible/roles/nixos_pxe_server/templates]
        direction TB
        node_1008["boot.ipxe.nix.j2"]
        node_1007["configuration.nix.j2"]
    end
    subgraph dir_ansible_roles_nomad_defaults [ansible/roles/nomad/defaults]
        direction TB
        node_746["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_handlers [ansible/roles/nomad/handlers]
        direction TB
        node_743["main.yaml"]
        node_744["restart_nomad_handler_tasks.yaml"]
    end
    subgraph dir_ansible_roles_nomad_tasks [ansible/roles/nomad/tasks]
        direction TB
        node_745["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_templates [ansible/roles/nomad/templates]
        direction TB
        node_740["client.hcl.j2"]
        node_738["nomad.hcl.server.j2"]
        node_741["nomad.service.j2"]
        node_742["nomad.sh.j2"]
        node_739["server.hcl.j2"]
    end
    subgraph dir_ansible_roles_openclaw_files [ansible/roles/openclaw/files]
        direction TB
        node_792["Dockerfile"]
        node_793["pipecat_skill.md"]
    end
    subgraph dir_ansible_roles_openclaw_tasks [ansible/roles/openclaw/tasks]
        direction TB
        node_791["main.yaml"]
    end
    subgraph dir_ansible_roles_openclaw_templates [ansible/roles/openclaw/templates]
        direction TB
        node_790["openclaw.nomad.j2"]
    end
    subgraph dir_ansible_roles_opencode_handlers [ansible/roles/opencode/handlers]
        direction TB
        node_736["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_tasks [ansible/roles/opencode/tasks]
        direction TB
        node_737["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_templates [ansible/roles/opencode/templates]
        direction TB
        node_735["opencode.nomad.j2"]
    end
    subgraph dir_ansible_roles_openworkers_handlers [ansible/roles/openworkers/handlers]
        direction TB
        node_853["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_tasks [ansible/roles/openworkers/tasks]
        direction TB
        node_854["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_templates [ansible/roles/openworkers/templates]
        direction TB
        node_851["openworkers-bootstrap.nomad.j2"]
        node_852["openworkers-infra.nomad.j2"]
        node_850["openworkers-runners.nomad.j2"]
    end
    subgraph dir_ansible_roles_paddler_tasks [ansible/roles/paddler/tasks]
        direction TB
        node_901["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent [ansible/roles/paddler_agent]
        direction TB
        node_1011["README.md"]
    end
    subgraph dir_ansible_roles_paddler_agent_defaults [ansible/roles/paddler_agent/defaults]
        direction TB
        node_1014["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_tasks [ansible/roles/paddler_agent/tasks]
        direction TB
        node_1013["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_templates [ansible/roles/paddler_agent/templates]
        direction TB
        node_1012["paddler-agent.service.j2"]
    end
    subgraph dir_ansible_roles_paddler_balancer [ansible/roles/paddler_balancer]
        direction TB
        node_807["README.md"]
    end
    subgraph dir_ansible_roles_paddler_balancer_defaults [ansible/roles/paddler_balancer/defaults]
        direction TB
        node_810["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_tasks [ansible/roles/paddler_balancer/tasks]
        direction TB
        node_809["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_templates [ansible/roles/paddler_balancer/templates]
        direction TB
        node_808["paddler-balancer.service.j2"]
    end
    subgraph dir_ansible_roles_paperless_handlers [ansible/roles/paperless/handlers]
        direction TB
        node_993["main.yaml"]
    end
    subgraph dir_ansible_roles_paperless_tasks [ansible/roles/paperless/tasks]
        direction TB
        node_994["main.yaml"]
    end
    subgraph dir_ansible_roles_paperless_templates [ansible/roles/paperless/templates]
        direction TB
        node_992["paperless.nomad.j2"]
    end
    subgraph dir_ansible_roles_pds_tasks [ansible/roles/pds/tasks]
        direction TB
        node_895["main.yaml"]
    end
    subgraph dir_ansible_roles_pds_templates [ansible/roles/pds/templates]
        direction TB
        node_894["pds.nomad.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_defaults [ansible/roles/pipecatapp/defaults]
        direction TB
        node_823["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_handlers [ansible/roles/pipecatapp/handlers]
        direction TB
        node_821["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_tasks [ansible/roles/pipecatapp/tasks]
        direction TB
        node_822["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates [ansible/roles/pipecatapp/templates]
        direction TB
        node_811["archivist.nomad.j2"]
        node_814["pipecat.env.j2"]
        node_812["pipecatapp.nomad.j2"]
        node_813["start_pipecatapp.sh.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_prompts [ansible/roles/pipecatapp/templates/prompts]
        direction TB
        node_818["coding_expert.txt.j2"]
        node_819["creative_expert.txt.j2"]
        node_816["cynic_expert.txt.j2"]
        node_817["router.txt.j2"]
        node_820["tron_agent.txt.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_workflows [ansible/roles/pipecatapp/templates/workflows]
        direction TB
        node_815["default_agent_loop.yaml.j2"]
    end
    subgraph dir_ansible_roles_polyphony_handlers [ansible/roles/polyphony/handlers]
        direction TB
        node_880["main.yaml"]
    end
    subgraph dir_ansible_roles_polyphony_tasks [ansible/roles/polyphony/tasks]
        direction TB
        node_881["main.yaml"]
    end
    subgraph dir_ansible_roles_polyphony_templates [ansible/roles/polyphony/templates]
        direction TB
        node_879["polyphony.nomad.j2"]
    end
    subgraph dir_ansible_roles_postgres_handlers [ansible/roles/postgres/handlers]
        direction TB
        node_1027["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_tasks [ansible/roles/postgres/tasks]
        direction TB
        node_1028["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_templates [ansible/roles/postgres/templates]
        direction TB
        node_1026["postgres.nomad.j2"]
    end
    subgraph dir_ansible_roles_power_manager_defaults [ansible/roles/power_manager/defaults]
        direction TB
        node_905["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_files [ansible/roles/power_manager/files]
        direction TB
        node_906["power_agent.py"]
        node_907["traffic_monitor.c"]
    end
    subgraph dir_ansible_roles_power_manager_handlers [ansible/roles/power_manager/handlers]
        direction TB
        node_903["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_tasks [ansible/roles/power_manager/tasks]
        direction TB
        node_904["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_templates [ansible/roles/power_manager/templates]
        direction TB
        node_902["power-agent.service.j2"]
    end
    subgraph dir_ansible_roles_preflight_checks_tasks [ansible/roles/preflight_checks/tasks]
        direction TB
        node_1000["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_files [ansible/roles/provisioning_api/files]
        direction TB
        node_776["provisioning_api.py"]
    end
    subgraph dir_ansible_roles_provisioning_api_handlers [ansible/roles/provisioning_api/handlers]
        direction TB
        node_774["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_tasks [ansible/roles/provisioning_api/tasks]
        direction TB
        node_775["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_templates [ansible/roles/provisioning_api/templates]
        direction TB
        node_773["provisioning-api.service.j2"]
    end
    subgraph dir_ansible_roles_pxe_server_defaults [ansible/roles/pxe_server/defaults]
        direction TB
        node_893["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_handlers [ansible/roles/pxe_server/handlers]
        direction TB
        node_891["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_tasks [ansible/roles/pxe_server/tasks]
        direction TB
        node_892["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_templates [ansible/roles/pxe_server/templates]
        direction TB
        node_888["boot.ipxe.j2"]
        node_889["dhcpd.conf.j2"]
        node_890["preseed.cfg.j2"]
    end
    subgraph dir_ansible_roles_python_deps_files [ansible/roles/python_deps/files]
        direction TB
        node_980["requirements.txt"]
    end
    subgraph dir_ansible_roles_python_deps_meta [ansible/roles/python_deps/meta]
        direction TB
        node_979["main.yaml"]
    end
    subgraph dir_ansible_roles_python_deps_tasks [ansible/roles/python_deps/tasks]
        direction TB
        node_978["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_defaults [ansible/roles/semantic_router/defaults]
        direction TB
        node_916["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_tasks [ansible/roles/semantic_router/tasks]
        direction TB
        node_915["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_templates [ansible/roles/semantic_router/templates]
        direction TB
        node_913["Dockerfile.j2"]
        node_914["semantic-router.nomad.j2"]
    end
    subgraph dir_ansible_roles_sunshine_defaults [ansible/roles/sunshine/defaults]
        direction TB
        node_806["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_handlers [ansible/roles/sunshine/handlers]
        direction TB
        node_804["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_tasks [ansible/roles/sunshine/tasks]
        direction TB
        node_805["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_templates [ansible/roles/sunshine/templates]
        direction TB
        node_803["sunshine.nomad.j2"]
    end
    subgraph dir_ansible_roles_system_deps_tasks [ansible/roles/system_deps/tasks]
        direction TB
        node_756["main.yaml"]
    end
    subgraph dir_ansible_roles_tailscale_tasks [ansible/roles/tailscale/tasks]
        direction TB
        node_987["main.yaml"]
    end
    subgraph dir_ansible_roles_term_everything_tasks [ansible/roles/term_everything/tasks]
        direction TB
        node_1015["main.yml"]
    end
    subgraph dir_ansible_roles_tool_server [ansible/roles/tool_server]
        direction TB
        node_939["Dockerfile"]
        node_938["app.py"]
        node_942["entrypoint.sh"]
        node_940["pmm_memory.py"]
        node_941["preload_models.py"]
    end
    subgraph dir_ansible_roles_tool_server_tasks [ansible/roles/tool_server/tasks]
        direction TB
        node_944["main.yaml"]
    end
    subgraph dir_ansible_roles_tool_server_templates [ansible/roles/tool_server/templates]
        direction TB
        node_943["tool_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_tool_server_tools [ansible/roles/tool_server/tools]
        direction TB
        node_968["ansible_tool.py"]
        node_970["archivist_tool.py"]
        node_948["claude_clone_tool.py"]
        node_972["code_runner_tool.py"]
        node_965["council_tool.py"]
        node_963["desktop_control_tool.py"]
        node_962["file_editor_tool.py"]
        node_945["final_answer_tool.py"]
        node_957["gemini_cli.py"]
        node_956["get_nomad_job.py"]
        node_967["git_tool.py"]
        node_950["ha_tool.py"]
        node_960["llxprt_code_tool.py"]
        node_946["mcp_tool.py"]
        node_954["opencode_tool.py"]
        node_951["orchestrator_tool.py"]
        node_974["planner_tool.py"]
        node_953["power_tool.py"]
        node_947["project_mapper_tool.py"]
        node_973["prompt_improver_tool.py"]
        node_969["rag_tool.py"]
        node_971["sandbox.ts"]
        node_955["shell_tool.py"]
        node_952["smol_agent_tool.py"]
        node_949["ssh_tool.py"]
        node_966["summarizer_tool.py"]
        node_958["swarm_tool.py"]
        node_959["tap_service.py"]
        node_961["term_everything_tool.py"]
        node_964["web_browser_tool.py"]
    end
    subgraph dir_ansible_roles_tpm_ssh_handlers [ansible/roles/tpm_ssh/handlers]
        direction TB
        node_998["main.yaml"]
    end
    subgraph dir_ansible_roles_tpm_ssh_tasks [ansible/roles/tpm_ssh/tasks]
        direction TB
        node_999["main.yaml"]
    end
    subgraph dir_ansible_roles_tpm_ssh_templates [ansible/roles/tpm_ssh/templates]
        direction TB
        node_995["tpm-ssh-agent.service.j2"]
        node_996["tpm-ssh-agent.sh.j2"]
        node_997["tpm_pins.j2"]
    end
    subgraph dir_ansible_roles_traefik_defaults [ansible/roles/traefik/defaults]
        direction TB
        node_872["main.yml"]
    end
    subgraph dir_ansible_roles_traefik_tasks [ansible/roles/traefik/tasks]
        direction TB
        node_871["main.yml"]
    end
    subgraph dir_ansible_roles_traefik_templates [ansible/roles/traefik/templates]
        direction TB
        node_870["traefik.nomad.j2"]
    end
    subgraph dir_ansible_roles_unified_fs_defaults [ansible/roles/unified_fs/defaults]
        direction TB
        node_868["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_files [ansible/roles/unified_fs/files]
        direction TB
        node_869["unified_fs_agent.py"]
    end
    subgraph dir_ansible_roles_unified_fs_handlers [ansible/roles/unified_fs/handlers]
        direction TB
        node_866["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_tasks [ansible/roles/unified_fs/tasks]
        direction TB
        node_867["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_templates [ansible/roles/unified_fs/templates]
        direction TB
        node_865["unified_fs.service.j2"]
    end
    subgraph dir_ansible_roles_vision_defaults [ansible/roles/vision/defaults]
        direction TB
        node_828["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_handlers [ansible/roles/vision/handlers]
        direction TB
        node_826["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_tasks [ansible/roles/vision/tasks]
        direction TB
        node_827["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_templates [ansible/roles/vision/templates]
        direction TB
        node_824["config.yml.j2"]
        node_825["vision.nomad.j2"]
    end
    subgraph dir_ansible_roles_vllm_tasks [ansible/roles/vllm/tasks]
        direction TB
        node_759["main.yaml"]
        node_758["run_single_vllm_job.yaml"]
    end
    subgraph dir_ansible_roles_vllm_templates [ansible/roles/vllm/templates]
        direction TB
        node_757["vllm-expert.nomad.j2"]
    end
    subgraph dir_ansible_roles_whisper_cpp_tasks [ansible/roles/whisper_cpp/tasks]
        direction TB
        node_917["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service_files [ansible/roles/world_model_service/files]
        direction TB
        node_797["Dockerfile"]
        node_796["app.py"]
        node_798["debug_world_model.sh"]
        node_799["requirements.txt"]
    end
    subgraph dir_ansible_roles_world_model_service_tasks [ansible/roles/world_model_service/tasks]
        direction TB
        node_795["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service_templates [ansible/roles/world_model_service/templates]
        direction TB
        node_794["world_model.nomad.j2"]
    end
    subgraph dir_ansible_tasks [ansible/tasks]
        direction TB
        node_717["README.md"]
        node_715["build_pipecatapp_image.yaml"]
        node_713["create_expert_job.yaml"]
        node_716["deploy_expert_wrapper.yaml"]
        node_714["deploy_model_gpu_provider.yaml"]
    end
    subgraph dir_docker [docker]
        direction TB
        node_348["README.md"]
    end
    subgraph dir_docker_dev_container [docker/dev_container]
        direction TB
        node_350["Dockerfile"]
    end
    subgraph dir_docker_memory_service [docker/memory_service]
        direction TB
        node_349["Dockerfile"]
    end
    subgraph dir_docs [docs]
        direction TB
        node_373["AGENTS.md"]
        node_365["AGENT_LIGHTNING_ANALYSIS.md"]
        node_355["AI_GOVERNANCE.md"]
        node_391["ARCHITECTURE.md"]
        node_360["BENCHMARKING.MD"]
        node_375["CLAMAV_EVALUATION.md"]
        node_380["CLAUDE_CODE_ANALYSIS.md"]
        node_367["DEPLOYMENT_AND_PROFILING.md"]
        node_386["EVALUATION_LLMROUTER.md"]
        node_357["FLOWISE_ANALYSIS.md"]
        node_359["FRONTEND_VERIFICATION.md"]
        node_383["FRONTIER_AGENT_ROADMAP.md"]
        node_372["GASTOWN_TODO.md"]
        node_358["GCP_GENERATIVE_AI_REVIEW.md"]
        node_353["GEMINI.md"]
        node_363["IPV6_AUDIT.md"]
        node_368["LANGCHAIN_ANALYSIS.md"]
        node_377["MCP_SERVER_SETUP.md"]
        node_389["MEMENTO_SKILLS_ANALYSIS.md"]
        node_385["MEMORIES.md"]
        node_387["NETWORK.md"]
        node_362["NIXOS_PXE_BOOT_SETUP.md"]
        node_351["OBSIDIAN_TODO.md"]
        node_370["OBSIDIAN_WORKFLOW_DESIGN.md"]
        node_378["PASEO_ANALYSIS.md"]
        node_382["PERFORMANCE_OPTIMIZATION.md"]
        node_366["PROJECT_SUMMARY.md"]
        node_374["PXE_BOOT_SETUP.md"]
        node_388["README.md"]
        node_379["REFACTOR_PROPOSAL_hybrid_architecture.md"]
        node_352["REMOTE_WORKFLOW.md"]
        node_356["SCALING_TODO.md"]
        node_364["SECURITY_AUDIT.md"]
        node_354["TODO_Hybrid_Architecture.md"]
        node_381["TOOL_EVALUATION.md"]
        node_384["TROUBLESHOOTING.md"]
        node_371["VLLM_PROJECT_EVALUATION.md"]
        node_361["YAML_FILES_REPORT.md"]
        node_376["aid_e_log.txt"]
        node_369["heretic_evaluation.md"]
        node_390["review_report.md"]
    end
    subgraph dir_docs_media [docs/media]
        direction TB
        node_392["initial_state.png"]
        node_393["paused_state.png"]
    end
    subgraph dir_examples [examples]
        direction TB
        node_33["README.md"]
        node_32["chat-persistent.sh"]
    end
    subgraph dir_group_vars [group_vars]
        direction TB
        node_162["README.md"]
        node_163["all.yaml"]
        node_161["external_experts.yaml"]
        node_160["models.yaml"]
    end
    subgraph dir_host_vars [host_vars]
        direction TB
        node_546["README.md"]
        node_545["localhost.yaml"]
    end
    subgraph dir_initial_setup [initial-setup]
        direction TB
        node_698["README.md"]
        node_697["add_new_worker.sh"]
        node_696["setup.conf"]
        node_695["setup.sh"]
        node_694["update_inventory.sh"]
    end
    subgraph dir_initial_setup_modules [initial-setup/modules]
        direction TB
        node_703["01-network.sh"]
        node_699["02-hostname.sh"]
        node_700["03-user.sh"]
        node_702["04-ssh.sh"]
        node_701["05-auto-provision.sh"]
        node_704["README.md"]
    end
    subgraph dir_initial_setup_worker_setup [initial-setup/worker-setup]
        direction TB
        node_706["README.md"]
        node_705["setup.sh"]
    end
    subgraph dir_modules_keystone_polyphony [modules/keystone-polyphony]
        direction TB
        node_45[".flake8"]
        node_34[".gitignore"]
        node_49["AGENTS.md"]
        node_46["CODE_OF_CONDUCT.md"]
        node_41["CONTRIBUTING.md"]
        node_37["Dockerfile"]
        node_44["ENSEMBLE_TRIAL.md"]
        node_36["LICENSE"]
        node_53["README.md"]
        node_35["TODO.md"]
        node_48["WORK_ORDER.md"]
        node_50["docker-compose.yml"]
        node_47["install.sh"]
        node_51["jules_config.json"]
        node_39["keystone-polyphony.sh"]
        node_52["kp"]
        node_43["polyphony"]
        node_42["requirements.txt"]
        node_38["simulate_swarm.py"]
        node_40["simulation.log"]
    end
    subgraph dir_modules_keystone_polyphony__agents_workflows [modules/keystone-polyphony/.agents/workflows]
        direction TB
        node_126["0-click-boot.md"]
        node_124["boot.md"]
        node_125["swarm-communication.md"]
    end
    subgraph dir_modules_keystone_polyphony__devcontainer [modules/keystone-polyphony/.devcontainer]
        direction TB
        node_127["devcontainer.json"]
    end
    subgraph dir_modules_keystone_polyphony__githooks [modules/keystone-polyphony/.githooks]
        direction TB
        node_100["pre-commit"]
        node_99["pre-push"]
    end
    subgraph dir_modules_keystone_polyphony__github [modules/keystone-polyphony/.github]
        direction TB
        node_129["reviewers.yml"]
    end
    subgraph dir_modules_keystone_polyphony__github_workflows [modules/keystone-polyphony/.github/workflows]
        direction TB
        node_135["add-contributors.yml"]
        node_131["agent-issue-solver.yml"]
        node_139["agent-issue-triage.yml"]
        node_138["agent-parallel-solver.yml"]
        node_134["auto-merge-staging.yml"]
        node_140["daily-close-merged-issues.yml"]
        node_130["opencode.yml"]
        node_137["periodic-merge-main.yml"]
        node_136["swarm-node.yml"]
        node_132["workflow-review-dispatch.yml"]
        node_133["workflow-review.yml"]
    end
    subgraph dir_modules_keystone_polyphony_docs [modules/keystone-polyphony/docs]
        direction TB
        node_91["architecture.md"]
        node_87["ci-cd.md"]
        node_89["getting-started.md"]
        node_88["git-hooks-architecture.md"]
        node_86["hooks-interaction.md"]
        node_90["liminal-bridge.md"]
        node_92["swarm-coordination.md"]
        node_85["vscode-integration.md"]
        node_84["zed-integration.md"]
    end
    subgraph dir_modules_keystone_polyphony_docs_features [modules/keystone-polyphony/docs/features]
        direction TB
        node_98["git-hooks.feature"]
    end
    subgraph dir_modules_keystone_polyphony_docs_issues_pre_review [modules/keystone-polyphony/docs/issues-pre-review]
        direction TB
        node_97["vision-and-impact.md"]
    end
    subgraph dir_modules_keystone_polyphony_docs_swarm_discovery [modules/keystone-polyphony/docs/swarm-discovery]
        direction TB
        node_95["analysis.md"]
        node_94["architecture-diagram.md"]
        node_93["hardware-bom.md"]
        node_96["modality-matrix.md"]
    end
    subgraph dir_modules_keystone_polyphony_features [modules/keystone-polyphony/features]
        direction TB
        node_141["hooks.feature"]
    end
    subgraph dir_modules_keystone_polyphony_meta [modules/keystone-polyphony/meta]
        direction TB
        node_128["DISCOVERIES.md"]
    end
    subgraph dir_modules_keystone_polyphony_scripts [modules/keystone-polyphony/scripts]
        direction TB
        node_119["agent-boot.sh"]
        node_101["broadcast.py"]
        node_113["deduplicate.py"]
        node_103["dispatch-work-order.sh"]
        node_117["exchange_ssh_keys.py"]
        node_108["inject-secrets.sh"]
        node_105["install-hooks.sh"]
        node_123["lint.sh"]
        node_122["load_test.py"]
        node_120["package.json"]
        node_102["ping.py"]
        node_114["refine_issue.py"]
        node_118["run-tests.sh"]
        node_107["setup-ensemble.sh"]
        node_112["setup-swarm.js"]
        node_115["setup-vscode.sh"]
        node_109["setup-zed.sh"]
        node_111["share.py"]
        node_116["status.py"]
        node_104["swarm_status.py"]
        node_110["triage-dispatch.sh"]
        node_121["triage-lib.sh"]
        node_106["worker_loop.py"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge [modules/keystone-polyphony/src/liminal_bridge]
        direction TB
        node_60["__init__.py"]
        node_58["architect.py"]
        node_55["crdt.py"]
        node_64["dashboard.py"]
        node_54["mesh.py"]
        node_56["observability.py"]
        node_59["pulse.py"]
        node_57["server.py"]
        node_63["test_architect.py"]
        node_61["test_key_rotation.py"]
        node_62["test_mesh.py"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_dashboard_ui [modules/keystone-polyphony/src/liminal_bridge/dashboard_ui]
        direction TB
        node_66["index.html"]
        node_67["package.json"]
        node_65["vite.config.js"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_dashboard_ui_src [modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src]
        direction TB
        node_68["App.css"]
        node_70["App.jsx"]
        node_72["crypto.js"]
        node_69["index.css"]
        node_71["main.jsx"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_dashboard_ui_src_components [modules/keystone-polyphony/src/liminal_bridge/dashboard_ui/src/components]
        direction TB
        node_76["Backlog.jsx"]
        node_75["Batons.jsx"]
        node_81["Discussions.jsx"]
        node_78["KVStore.jsx"]
        node_74["Login.jsx"]
        node_73["Logs.jsx"]
        node_80["NetworkGraph.jsx"]
        node_79["Status.jsx"]
        node_77["Thoughts.jsx"]
    end
    subgraph dir_modules_keystone_polyphony_src_liminal_bridge_sidecar [modules/keystone-polyphony/src/liminal_bridge/sidecar]
        direction TB
        node_82["bridge.js"]
        node_83["package.json"]
    end
    subgraph dir_modules_keystone_polyphony_tests [modules/keystone-polyphony/tests]
        direction TB
        node_146["issue_19_verification.txt"]
        node_147["test_activation.sh"]
        node_155["test_architect_commands.py"]
        node_154["test_architect_ollama.py"]
        node_145["test_attenuation.py"]
        node_152["test_crdt.py"]
        node_151["test_ensemble_chat.py"]
        node_156["test_fallback.py"]
        node_148["test_install.sh"]
        node_150["test_mesh_crdt.py"]
        node_144["test_mesh_encryption.py"]
        node_153["test_network_simulation.py"]
        node_149["test_ssh_exchange.py"]
        node_159["test_stigmergy.py"]
        node_143["test_tandem.py"]
        node_157["test_tasks.py"]
        node_142["test_unread_tracking.py"]
        node_158["test_vector_clock.py"]
    end
    subgraph dir_os_image [os-image]
        direction TB
        node_548["README.md"]
        node_547["build_iso.sh"]
    end
    subgraph dir_os_image_config_archives [os-image/config/archives]
        direction TB
        node_560["rocm.key.binary"]
        node_559["rocm.key.chroot"]
        node_561["rocm.list.binary"]
        node_558["rocm.list.chroot"]
    end
    subgraph dir_os_image_config_hooks_live [os-image/config/hooks/live]
        direction TB
        node_549["01-setup-users.chroot"]
        node_550["02-enable-services.chroot"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_profile_d [os-image/config/includes.chroot/etc/profile.d]
        direction TB
        node_552["99-pipecat-welcome.sh"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_systemd_system [os-image/config/includes.chroot/etc/systemd/system]
        direction TB
        node_554["pipecat-firstboot.service"]
        node_553["pipecat-hostname.service"]
    end
    subgraph dir_os_image_config_includes_chroot_etc_systemd_system_multi_user_target_wants [os-image/config/includes.chroot/etc/systemd/system/multi-user.target.wants]
        direction TB
        node_555["pipecat-firstboot.service"]
    end
    subgraph dir_os_image_config_includes_chroot_usr_local_bin [os-image/config/includes.chroot/usr/local/bin]
        direction TB
        node_556["setup-ssh-keys.sh"]
    end
    subgraph dir_os_image_config_includes_installer [os-image/config/includes.installer]
        direction TB
        node_557["preseed.cfg"]
    end
    subgraph dir_os_image_config_package_lists [os-image/config/package-lists]
        direction TB
        node_551["pipecat.list.chroot"]
    end
    subgraph dir_pipecat_agent_extension [pipecat-agent-extension]
        direction TB
        node_692["README.md"]
        node_689["example.ts"]
        node_688["gemini-extension.json"]
        node_691["package.json"]
        node_690["tsconfig.json"]
    end
    subgraph dir_pipecat_agent_extension_commands_pipecat [pipecat-agent-extension/commands/pipecat]
        direction TB
        node_693["send.toml"]
    end
    subgraph dir_pipecatapp [pipecatapp]
        direction TB
        node_173["Dockerfile"]
        node_204["README.md"]
        node_170["TODO.md"]
        node_182["__init__.py"]
        node_184["agent_factory.py"]
        node_196["api_keys.py"]
        node_169["app.py"]
        node_178["archivist_service.py"]
        node_172["durable_execution.py"]
        node_186["expert_tracker.py"]
        node_200["generate_real_embeddings.py"]
        node_198["janitor_agent.py"]
        node_168["judge_agent.py"]
        node_185["langchain_memory_wrappers.py"]
        node_180["llm_clients.py"]
        node_165["manager_agent.py"]
        node_167["memory.py"]
        node_194["models.py"]
        node_189["moondream_detector.py"]
        node_175["net_utils.py"]
        node_197["pmm_memory.py"]
        node_191["pmm_memory_client.py"]
        node_176["quality_control.py"]
        node_181["rate_limiter.py"]
        node_183["requirements.txt"]
        node_206["router_config.yaml"]
        node_193["router_train_embeddings.pt"]
        node_199["router_trained_model.pkl"]
        node_192["router_training_data.csv"]
        node_201["router_training_data.jsonl"]
        node_190["secret_manager.py"]
        node_188["security.py"]
        node_166["skill_library.py"]
        node_174["start_archivist.sh"]
        node_202["task_supervisor.py"]
        node_171["technician_agent.py"]
        node_195["test_moondream_detector.py"]
        node_205["test_pmm_memory.py"]
        node_177["test_server.py"]
        node_164["tool_server.py"]
        node_203["train_router.py"]
        node_187["web_server.py"]
        node_179["worker_agent.py"]
    end
    subgraph dir_pipecatapp_datasets [pipecatapp/datasets]
        direction TB
        node_259["sycophancy_prompts.json"]
    end
    subgraph dir_pipecatapp_integrations [pipecatapp/integrations]
        direction TB
        node_211["__init__.py"]
        node_212["openclaw.py"]
    end
    subgraph dir_pipecatapp_memory_graph_service [pipecatapp/memory_graph_service]
        direction TB
        node_207["Dockerfile"]
        node_208["server.py"]
    end
    subgraph dir_pipecatapp_nomad_templates [pipecatapp/nomad_templates]
        direction TB
        node_231["immich.nomad.hcl"]
        node_229["readeck.nomad.hcl"]
        node_230["uptime-kuma.nomad.hcl"]
        node_232["vaultwarden.nomad.hcl"]
    end
    subgraph dir_pipecatapp_prompts [pipecatapp/prompts]
        direction TB
        node_255["coding_expert.txt"]
        node_258["creative_expert.txt"]
        node_257["router.txt"]
        node_256["tron_agent.txt"]
    end
    subgraph dir_pipecatapp_services [pipecatapp/services]
        direction TB
        node_209["__init__.py"]
        node_210["gemma_e2b_service.py"]
    end
    subgraph dir_pipecatapp_static [pipecatapp/static]
        direction TB
        node_247["cluster.html"]
        node_243["cluster_viz.html"]
        node_248["index.html"]
        node_245["monitor.html"]
        node_249["terminal.js"]
        node_246["vr_index.html"]
        node_242["workflow.html"]
        node_244["workflow_3d.html"]
    end
    subgraph dir_pipecatapp_static_css [pipecatapp/static/css]
        direction TB
        node_250["litegraph.css"]
        node_251["styles.css"]
    end
    subgraph dir_pipecatapp_static_js [pipecatapp/static/js]
        direction TB
        node_253["editor.js"]
        node_252["litegraph.js"]
        node_254["workflow.js"]
    end
    subgraph dir_pipecatapp_tests [pipecatapp/tests]
        direction TB
        node_325["test_audio_streamer.py"]
        node_336["test_browser_tool_security.py"]
        node_342["test_container_registry_tool.py"]
        node_338["test_cq_tool.py"]
        node_334["test_document_tool.py"]
        node_337["test_gemma_e2b_service.py"]
        node_345["test_git_tool_security.py"]
        node_343["test_metrics_cache.py"]
        node_332["test_net_utils.py"]
        node_324["test_openclaw.py"]
        node_328["test_piper_async.py"]
        node_323["test_proxy_security.py"]
        node_326["test_rag_tool.py"]
        node_331["test_rate_limiter.py"]
        node_335["test_security.py"]
        node_344["test_spec_loader_security.py"]
        node_327["test_stt_optimization.py"]
        node_330["test_tool_server.py"]
        node_339["test_uilogger_redaction.py"]
        node_340["test_web_server_unit.py"]
        node_341["test_websocket_security.py"]
        node_329["test_xss_prevention.py"]
        node_333["test_yolo_optimization.py"]
    end
    subgraph dir_pipecatapp_tests_workflow [pipecatapp/tests/workflow]
        direction TB
        node_347["test_history.py"]
        node_346["test_serialization_perf.py"]
    end
    subgraph dir_pipecatapp_tools [pipecatapp/tools]
        direction TB
        node_284["__init__.py"]
        node_310["ansible_tool.py"]
        node_315["archivist_tool.py"]
        node_273["atproto_tool.py"]
        node_306["autoloop_tool.py"]
        node_280["autoresearch_tool.py"]
        node_270["claude_clone_tool.py"]
        node_269["cluster_status_tool.py"]
        node_319["code_runner_tool.py"]
        node_289["container_registry_tool.py"]
        node_265["context_upload_tool.py"]
        node_307["council_tool.py"]
        node_272["cq_tool.py"]
        node_278["dependency_scanner_tool.py"]
        node_304["desktop_control_tool.py"]
        node_288["document_tool.py"]
        node_321["dynamic_skill_tool.py"]
        node_300["experiment_tool.py"]
        node_303["file_editor_tool.py"]
        node_261["final_answer_tool.py"]
        node_295["gemini_cli.py"]
        node_293["get_nomad_job.py"]
        node_309["git_tool.py"]
        node_275["ha_tool.py"]
        node_262["heretic_tool.py"]
        node_264["langchain_adapter.py"]
        node_301["llxprt_code_tool.py"]
        node_263["mcp_tool.py"]
        node_318["open_workers_tool.py"]
        node_283["openclaw_tool.py"]
        node_260["opencode_provider_tool.py"]
        node_285["opencode_tool.py"]
        node_277["orchestrator_tool.py"]
        node_268["personality_tool.py"]
        node_322["planner_tool.py"]
        node_290["polyphony_tool.py"]
        node_281["power_tool.py"]
        node_267["project_mapper_tool.py"]
        node_320["prompt_improver_tool.py"]
        node_311["rag_tool.py"]
        node_266["remote_tool_proxy.py"]
        node_316["sandbox.ts"]
        node_317["save_skill_tool.py"]
        node_291["scale_compute_tool.py"]
        node_282["scheduler_tool.py"]
        node_297["search_skills_tool.py"]
        node_294["search_tool.py"]
        node_292["shell_tool.py"]
        node_287["skill_builder_tool.py"]
        node_279["smol_agent_tool.py"]
        node_313["spec_loader_tool.py"]
        node_271["ssh_tool.py"]
        node_314["submit_solution_tool.py"]
        node_308["summarizer_tool.py"]
        node_296["swarm_tool.py"]
        node_299["tap_service.py"]
        node_302["term_everything_tool.py"]
        node_274["test_git_tool.py"]
        node_298["test_ssh_tool.py"]
        node_276["update_litellm_tool.py"]
        node_312["vr_tool.py"]
        node_305["web_browser_tool.py"]
        node_286["wol_tool.py"]
    end
    subgraph dir_pipecatapp_workflow [pipecatapp/workflow]
        direction TB
        node_216["__init__.py"]
        node_214["canvas_converter.py"]
        node_218["context.py"]
        node_215["crypto_receipts.py"]
        node_219["history.py"]
        node_217["node.py"]
        node_213["runner.py"]
    end
    subgraph dir_pipecatapp_workflow_nodes [pipecatapp/workflow/nodes]
        direction TB
        node_223["__init__.py"]
        node_222["base_nodes.py"]
        node_221["emperor_nodes.py"]
        node_228["langchain_nodes.py"]
        node_226["llm_nodes.py"]
        node_220["ralph_nodes.py"]
        node_224["registry.py"]
        node_227["system_nodes.py"]
        node_225["tool_nodes.py"]
    end
    subgraph dir_pipecatapp_workflows [pipecatapp/workflows]
        direction TB
        node_236["adversarial_simulation.yaml"]
        node_235["deep_context.yaml"]
        node_233["default_agent_loop.yaml"]
        node_234["looped_reasoning.yaml"]
        node_239["manager.yaml"]
        node_240["poc_ensemble.yaml"]
        node_238["sandbox.yaml"]
        node_237["tiered_agent_loop.yaml"]
        node_241["update_litellm_workflow.yaml"]
    end
    subgraph dir_playbooks [playbooks]
        direction TB
        node_471["README.md"]
        node_449["benchmark_single_model.yaml"]
        node_454["cluster_status.yaml"]
        node_463["common_setup.yaml"]
        node_450["controller.yaml"]
        node_443["debug_template.yaml"]
        node_448["deploy_app.yaml"]
        node_461["deploy_expert.yaml"]
        node_466["deploy_openclaw.yaml"]
        node_455["deploy_pds.yaml"]
        node_457["deploy_prompt_evolution.yaml"]
        node_446["developer_tools.yaml"]
        node_453["diagnose_and_log_home_assistant.yaml"]
        node_458["diagnose_failure.yaml"]
        node_456["diagnose_home_assistant.yaml"]
        node_452["fix_cluster.yaml"]
        node_451["heal_cluster.yaml"]
        node_470["heal_job.yaml"]
        node_447["health_check.yaml"]
        node_462["promote_controller.yaml"]
        node_472["promote_to_controller.yaml"]
        node_445["pxe_setup.yaml"]
        node_468["redeploy_pipecat.yaml"]
        node_469["run_config_manager.yaml"]
        node_444["run_consul.yaml"]
        node_467["run_ha_diag.yaml"]
        node_465["run_health_check.yaml"]
        node_464["status-check.yaml"]
        node_460["wake.yaml"]
        node_459["worker.yaml"]
    end
    subgraph dir_playbooks_network [playbooks/network]
        direction TB
        node_491["mesh.yaml"]
        node_492["verify.yaml"]
    end
    subgraph dir_playbooks_ops [playbooks/ops]
        direction TB
        node_490["optimize_memory.yaml"]
    end
    subgraph dir_playbooks_preflight [playbooks/preflight]
        direction TB
        node_493["checks.yaml"]
    end
    subgraph dir_playbooks_services [playbooks/services]
        direction TB
        node_485["README.md"]
        node_481["ai_experts.yaml"]
        node_484["app_services.yaml"]
        node_478["consul.yaml"]
        node_483["core_ai_services.yaml"]
        node_482["core_infra.yaml"]
        node_476["distributed_compute.yaml"]
        node_486["docker.yaml"]
        node_475["final_verification.yaml"]
        node_487["model_services.yaml"]
        node_477["monitoring.yaml"]
        node_473["nomad.yaml"]
        node_480["nomad_client.yaml"]
        node_479["registry.yaml"]
        node_474["streaming_services.yaml"]
        node_488["training_services.yaml"]
    end
    subgraph dir_playbooks_services_tasks [playbooks/services/tasks]
        direction TB
        node_489["diagnose_home_assistant.yaml"]
    end
    subgraph dir_prompt_engineering [prompt_engineering]
        direction TB
        node_509["PROMPT_ENGINEERING.md"]
        node_520["README.md"]
        node_515["archive_server.py"]
        node_519["autoloop_evolve.py"]
        node_511["challenger.py"]
        node_518["create_evaluator.py"]
        node_513["evaluation_lib.py"]
        node_521["evaluator.py"]
        node_514["evolve.py"]
        node_517["promote_agent.py"]
        node_512["requirements-dev.txt"]
        node_510["run_campaign.py"]
        node_516["visualize_archive.py"]
    end
    subgraph dir_prompt_engineering_agents [prompt_engineering/agents]
        direction TB
        node_527["ADAPTATION_AGENT.md"]
        node_528["EVALUATOR_GENERATOR.md"]
        node_529["README.md"]
        node_524["architecture_review.md"]
        node_522["code_clean_up.md"]
        node_525["debug_and_analysis.md"]
        node_526["new_task_review.md"]
        node_523["problem_scope_framing.md"]
    end
    subgraph dir_prompt_engineering_archive [prompt_engineering/archive]
        direction TB
        node_530["agent_0.json"]
        node_532["agent_0.py"]
        node_534["agent_1.json"]
        node_535["agent_1.py"]
        node_536["agent_2.json"]
        node_531["agent_2.py"]
        node_533["agent_3.json"]
        node_537["agent_3.py"]
    end
    subgraph dir_prompt_engineering_evaluation_suite [prompt_engineering/evaluation_suite]
        direction TB
        node_539["README.md"]
        node_538["test_vision.yaml"]
    end
    subgraph dir_prompt_engineering_frontend [prompt_engineering/frontend]
        direction TB
        node_541["app.js"]
        node_542["index.html"]
        node_540["server.py"]
        node_543["style.css"]
    end
    subgraph dir_prompt_engineering_generated_evaluators [prompt_engineering/generated_evaluators]
        direction TB
        node_544[".gitignore"]
    end
    subgraph dir_prompts [prompts]
        direction TB
        node_500["README.md"]
        node_498["chat-with-bob.txt"]
        node_499["router.txt"]
    end
    subgraph dir_reflection [reflection]
        direction TB
        node_496["README.md"]
        node_495["adaptation_manager.py"]
        node_497["create_reflection.py"]
        node_494["reflect.py"]
    end
    subgraph dir_scripts [scripts]
        direction TB
        node_432["README.md"]
        node_420["agentic_workflow.sh"]
        node_424["analyze_nomad_allocs.py"]
        node_430["ansible_diff.sh"]
        node_437["check_all_playbooks.sh"]
        node_402["check_deps.py"]
        node_417["ci_ansible_check.sh"]
        node_434["cleanup.sh"]
        node_421["compare_exo_llama.py"]
        node_396["create_assistant_prompts.py"]
        node_405["create_cynic_model.sh"]
        node_406["create_todo_issues.sh"]
        node_427["debug_expert.sh"]
        node_400["debug_mesh.sh"]
        node_419["evaluate_clamav.py"]
        node_404["fix_markdown.sh"]
        node_438["fix_verification_failures.sh"]
        node_415["fix_yaml.sh"]
        node_433["generate_assistant_vectors.sh"]
        node_435["generate_file_map.py"]
        node_423["generate_issue_script.py"]
        node_407["generate_signatures.py"]
        node_397["heal_cluster.sh"]
        node_428["healer.py"]
        node_436["lint.sh"]
        node_431["lint_exclude.txt"]
        node_439["memory_audit.py"]
        node_426["profile_resources.sh"]
        node_410["provisioning.py"]
        node_429["prune_consul_services.py"]
        node_398["recover_node.py"]
        node_399["run_quibbler.sh"]
        node_412["run_tests.sh"]
        node_403["salvage_task.py"]
        node_418["setup_pxe_server.sh"]
        node_422["start_services.sh"]
        node_425["supervisor.py"]
        node_411["test_playbooks_dry_run.sh"]
        node_408["test_playbooks_live_run.sh"]
        node_414["test_swarm_map_reduce.py"]
        node_409["troubleshoot.py"]
        node_416["uninstall.sh"]
        node_413["update_cluster.sh"]
        node_401["verify_consul_attributes.sh"]
    end
    subgraph dir_scripts_debug [scripts/debug]
        direction TB
        node_441["README.md"]
        node_440["test_mqtt_connection.py"]
    end
    subgraph dir_tests [tests]
        direction TB
        node_581["README.md"]
        node_576["__init__.py"]
        node_578["test.wav"]
        node_577["test_agent_patterns.py"]
        node_568["test_canvas_integration.py"]
        node_572["test_deep_context.py"]
        node_569["test_emperor_node.py"]
        node_574["test_event_bus.py"]
        node_582["test_experiment_tool.py"]
        node_567["test_gastown_judge.py"]
        node_573["test_gastown_memory.py"]
        node_575["test_gastown_stats.py"]
        node_566["test_imports.py"]
        node_571["test_manager_flow.py"]
        node_570["test_spec_loader.py"]
        node_565["test_ssrf_validation.py"]
        node_579["test_websocket_security.py"]
        node_564["verify_config_load.py"]
        node_580["verify_dlq.py"]
    end
    subgraph dir_tests_e2e [tests/e2e]
        direction TB
        node_687["README.md"]
        node_682["__init__.py"]
        node_683["test_api.py"]
        node_680["test_intelligent_routing.py"]
        node_681["test_mission_control.py"]
        node_685["test_palette_command_history.py"]
        node_686["test_palette_ux.py"]
        node_684["test_regression.py"]
    end
    subgraph dir_tests_integration [tests/integration]
        direction TB
        node_592["README.md"]
        node_585["__init__.py"]
        node_591["stub_services.py"]
        node_584["test_consul_role.yaml"]
        node_586["test_home_assistant.yaml"]
        node_587["test_mini_pipeline.py"]
        node_588["test_mqtt_exporter.py"]
        node_583["test_nomad_role.yaml"]
        node_589["test_pipecat_app.py"]
        node_590["test_preemption.py"]
    end
    subgraph dir_tests_integration_roles_test_home_assistant_tasks [tests/integration/roles/test_home_assistant/tasks]
        direction TB
        node_593["main.yaml"]
    end
    subgraph dir_tests_playbooks [tests/playbooks]
        direction TB
        node_676["e2e-tests.yaml"]
        node_677["test_consul.yaml"]
        node_679["test_llama_cpp.yaml"]
        node_678["test_nomad.yaml"]
    end
    subgraph dir_tests_scripts [tests/scripts]
        direction TB
        node_674["run_unit_tests.sh"]
        node_673["test_duplicate_role_execution.sh"]
        node_675["test_paddler.sh"]
        node_670["test_piper.sh"]
        node_672["test_run.sh"]
        node_671["verify_components.py"]
    end
    subgraph dir_tests_unit [tests/unit]
        direction TB
        node_666["README.md"]
        node_627["__init__.py"]
        node_619["conftest.py"]
        node_625["test_adaptation_manager.py"]
        node_648["test_agent_definitions.py"]
        node_599["test_ansible_tool.py"]
        node_633["test_archivist_tool.py"]
        node_615["test_audio_download_limit.py"]
        node_626["test_autoresearch_tool.py"]
        node_608["test_autoresearch_tool_pathing.py"]
        node_652["test_claude_clone_tool.py"]
        node_647["test_code_runner_security.py"]
        node_635["test_code_runner_timeout.py"]
        node_598["test_code_runner_tool.py"]
        node_662["test_container_registry_security.py"]
        node_667["test_council_tool.py"]
        node_607["test_crypto_receipts.py"]
        node_595["test_dependency_scanner.py"]
        node_618["test_desktop_control_tool.py"]
        node_638["test_experiment_tool_security.py"]
        node_597["test_file_editor_security.py"]
        node_650["test_file_editor_tool.py"]
        node_639["test_final_answer_tool.py"]
        node_665["test_gemini_cli.py"]
        node_609["test_get_nomad_job.py"]
        node_611["test_git_tool.py"]
        node_668["test_git_tool_security.py"]
        node_624["test_ha_tool.py"]
        node_645["test_hashline_editor.py"]
        node_617["test_heretic_tool.py"]
        node_653["test_home_assistant_template.py"]
        node_664["test_infrastructure.py"]
        node_628["test_lint_script.py"]
        node_603["test_llxprt_code_tool.py"]
        node_594["test_looped_reasoning_node.py"]
        node_623["test_mcp_tool.py"]
        node_616["test_memory.py"]
        node_634["test_mqtt_template.py"]
        node_605["test_nomad_sandbox.py"]
        node_644["test_open_workers_tool.py"]
        node_610["test_opencode_provider_tool.py"]
        node_601["test_opencode_tool.py"]
        node_613["test_orchestrator_tool.py"]
        node_659["test_personality_tool.py"]
        node_654["test_pipecat_app_unit.py"]
        node_632["test_planner_tool.py"]
        node_641["test_playbook_integration.py"]
        node_630["test_poc_ensemble.py"]
        node_600["test_polyphony_tool.py"]
        node_596["test_power_tool.py"]
        node_636["test_project_mapper_tool.py"]
        node_631["test_prompt_engineering.py"]
        node_656["test_prompt_improver_tool.py"]
        node_669["test_provisioning.py"]
        node_602["test_rag_tool.py"]
        node_637["test_ralph_nodes.py"]
        node_658["test_reflection.py"]
        node_622["test_search_tool_security.py"]
        node_651["test_security.py"]
        node_614["test_shell_tool.py"]
        node_604["test_shell_tool_security.py"]
        node_612["test_simple_llm_node.py"]
        node_620["test_skill_library.py"]
        node_646["test_smol_agent_tool.py"]
        node_643["test_ssh_tool.py"]
        node_640["test_summarizer_tool.py"]
        node_621["test_supervisor.py"]
        node_663["test_swarm_tool.py"]
        node_660["test_tap_service.py"]
        node_661["test_term_everything_tool.py"]
        node_629["test_vision_failover.py"]
        node_642["test_web_browser_tool.py"]
        node_606["test_web_server_personality.py"]
        node_655["test_web_server_sync.py"]
        node_657["test_workflow.py"]
        node_649["test_world_model_service.py"]
    end
    subgraph dir_workflows [workflows]
        direction TB
        node_442["default_agent_loop.yaml"]
    end

    node_49 --> node_388
    node_1013 --> node_985
    node_122 --> node_54
    node_385 --> node_8
    node_29 --> node_728
    node_570 --> node_388
    node_90 --> node_82
    node_59 --> node_58
    node_364 --> node_233
    node_48 --> node_53
    node_915 --> node_864
    node_564 --> node_163
    node_730 --> node_728
    node_385 --> node_514
    node_916 --> node_1016
    node_477 --> node_930
    node_892 --> node_888
    node_348 --> node_1025
    node_81 --> node_208
    node_173 --> node_980
    node_349 --> node_849
    node_254 --> node_442
    node_354 --> node_184
    node_477 --> node_926
    node_164 --> node_964
    node_385 --> node_1014
    node_1013 --> node_806
    node_152 --> node_55
    node_207 --> node_57
    node_87 --> node_867
    node_29 --> node_465
    node_795 --> node_169
    node_900 --> node_740
    node_243 --> node_253
    node_361 --> node_746
    node_6 --> node_877
    node_361 --> node_908
    node_847 --> node_990
    node_14 --> node_293
    node_435 --> node_207
    node_916 --> node_881
    node_6 --> node_1000
    node_468 --> node_814
    node_411 --> node_487
    node_451 --> node_756
    node_29 --> node_348
    node_169 --> node_964
    node_379 --> node_792
    node_385 --> node_821
    node_385 --> node_404
    node_372 --> node_796
    node_355 --> node_848
    node_420 --> node_539
    node_451 --> node_853
    node_938 --> node_305
    node_385 --> node_999
    node_470 --> node_589
    node_184 --> node_271
    node_514 --> node_938
    node_451 --> node_886
    node_385 --> node_827
    node_48 --> node_764
    node_297 --> node_166
    node_791 --> node_37
    node_406 --> node_207
    node_809 --> node_853
    node_333 --> node_169
    node_473 --> node_742
    node_6 --> node_292
    node_708 --> node_743
    node_859 --> node_183
    node_126 --> node_43
    node_6 --> node_748
    node_385 --> node_470
    node_280 --> node_764
    node_81 --> node_540
    node_391 --> node_6
    node_552 --> node_692
    node_410 --> node_459
    node_483 --> node_845
    node_570 --> node_485
    node_354 --> node_748
    node_388 --> node_49
    node_697 --> node_705
    node_916 --> node_1001
    node_715 --> node_37
    node_435 --> node_25
    node_361 --> node_836
    node_487 --> node_1025
    node_41 --> node_100
    node_364 --> node_969
    node_813 --> node_980
    node_385 --> node_980
    node_520 --> node_518
    node_713 --> node_731
    node_420 --> node_732
    node_991 --> node_828
    node_187 --> node_213
    node_388 --> node_360
    node_656 --> node_320
    node_48 --> node_29
    node_287 --> node_167
    node_432 --> node_424
    node_854 --> node_850
    node_915 --> node_1024
    node_519 --> node_521
    node_991 --> node_884
    node_1013 --> node_743
    node_528 --> node_764
    node_203 --> node_199
    node_636 --> node_529
    node_109 --> node_540
    node_477 --> node_868
    node_410 --> node_475
    node_349 --> node_796
    node_916 --> node_775
    node_391 --> node_906
    node_451 --> node_1005
    node_155 --> node_59
    node_354 --> node_1028
    node_385 --> node_462
    node_85 --> node_432
    node_451 --> node_755
    node_385 --> node_877
    node_809 --> node_1013
    node_991 --> node_976
    node_1023 --> node_763
    node_745 --> node_764
    node_944 --> node_349
    node_385 --> node_373
    node_672 --> node_32
    node_492 --> node_400
    node_1013 --> node_823
    node_406 --> node_208
    node_354 --> node_1006
    node_11 --> node_478
    node_520 --> node_521
    node_85 --> node_730
    node_385 --> node_1000
    node_348 --> node_37
    node_451 --> node_1009
    node_809 --> node_986
    node_29 --> node_666
    node_441 --> node_440
    node_88 --> node_539
    node_482 --> node_872
    node_88 --> node_704
    node_666 --> node_599
    node_991 --> node_873
    node_938 --> node_961
    node_636 --> node_548
    node_49 --> node_496
    node_51 --> node_208
    node_88 --> node_394
    node_518 --> node_938
    node_570 --> node_496
    node_354 --> node_993
    node_362 --> node_924
    node_362 --> node_743
    node_326 --> node_969
    node_184 --> node_945
    node_451 --> node_904
    node_204 --> node_37
    node_178 --> node_181
    node_548 --> node_2
    node_208 --> node_540
    node_938 --> node_950
    node_935 --> node_937
    node_1013 --> node_915
    node_698 --> node_696
    node_795 --> node_42
    node_385 --> node_748
    node_745 --> node_742
    node_385 --> node_653
    node_185 --> node_197
    node_666 --> node_425
    node_362 --> node_823
    node_978 --> node_980
    node_575 --> node_167
    node_6 --> node_593
    node_48 --> node_704
    node_1013 --> node_998
    node_480 --> node_746
    node_571 --> node_169
    node_566 --> node_169
    node_822 --> node_811
    node_354 --> node_593
    node_373 --> node_512
    node_1005 --> node_923
    node_225 --> node_224
    node_1013 --> node_875
    node_6 --> node_920
    node_385 --> node_471
    node_88 --> node_732
    node_85 --> node_441
    node_832 --> node_248
    node_451 --> node_994
    node_865 --> node_869
    node_361 --> node_444
    node_364 --> node_651
    node_435 --> node_183
    node_29 --> node_509
    node_935 --> node_934
    node_359 --> node_83
    node_386 --> node_226
    node_130 --> node_348
    node_809 --> node_994
    node_169 --> node_213
    node_673 --> node_11
    node_53 --> node_36
    node_41 --> node_900
    node_6 --> node_977
    node_1013 --> node_917
    node_1007 --> node_52
    node_361 --> node_830
    node_476 --> node_771
    node_451 --> node_826
    node_521 --> node_513
    node_451 --> node_863
    node_354 --> node_977
    node_84 --> node_520
    node_991 --> node_898
    node_91 --> node_204
    node_98 --> node_118
    node_832 --> node_542
    node_915 --> node_753
    node_162 --> node_160
    node_57 --> node_540
    node_90 --> node_6
    node_361 --> node_781
    node_890 --> node_705
    node_388 --> node_6
    node_476 --> node_770
    node_1013 --> node_780
    node_809 --> node_863
    node_423 --> node_35
    node_356 --> node_57
    node_552 --> node_717
    node_204 --> node_196
    node_362 --> node_875
    node_451 --> node_809
    node_130 --> node_581
    node_340 --> node_796
    node_362 --> node_982
    node_636 --> node_563
    node_408 --> node_25
    node_362 --> node_52
    node_666 --> node_648
    node_435 --> node_173
    node_482 --> node_998
    node_391 --> node_540
    node_361 --> node_734
    node_791 --> node_350
    node_944 --> node_792
    node_809 --> node_835
    node_1013 --> node_895
    node_6 --> node_736
    node_132 --> node_18
    node_379 --> node_169
    node_632 --> node_974
    node_734 --> node_733
    node_348 --> node_349
    node_307 --> node_163
    node_361 --> node_388
    node_1013 --> node_854
    node_636 --> node_687
    node_337 --> node_210
    node_354 --> node_978
    node_679 --> node_920
    node_269 --> node_454
    node_552 --> node_500
    node_444 --> node_918
    node_574 --> node_938
    node_361 --> node_432
    node_391 --> node_425
    node_435 --> node_349
    node_916 --> node_1021
    node_85 --> node_57
    node_88 --> node_118
    node_362 --> node_917
    node_6 --> node_822
    node_385 --> node_593
    node_628 --> node_436
    node_385 --> node_49
    node_391 --> node_35
    node_361 --> node_449
    node_2 --> node_410
    node_362 --> node_910
    node_184 --> node_307
    node_715 --> node_350
    node_361 --> node_887
    node_704 --> node_695
    node_53 --> node_90
    node_552 --> node_162
    node_385 --> node_920
    node_373 --> node_160
    node_601 --> node_954
    node_112 --> node_540
    node_938 --> node_967
    node_991 --> node_985
    node_29 --> node_462
    node_354 --> node_379
    node_406 --> node_349
    node_361 --> node_862
    node_420 --> node_563
    node_325 --> node_796
    node_894 --> node_764
    node_709 --> node_843
    node_169 --> node_319
    node_130 --> node_666
    node_915 --> node_821
    node_482 --> node_780
    node_362 --> node_895
    node_385 --> node_968
    node_822 --> node_196
    node_484 --> node_791
    node_484 --> node_949
    node_354 --> node_1011
    node_666 --> node_310
    node_587 --> node_938
    node_361 --> node_762
    node_361 --> node_831
    node_515 --> node_938
    node_6 --> node_804
    node_760 --> node_183
    node_385 --> node_977
    node_631 --> node_938
    node_809 --> node_774
    node_916 --> node_756
    node_326 --> node_52
    node_477 --> node_932
    node_495 --> node_494
    node_759 --> node_758
    node_35 --> node_153
    node_485 --> node_483
    node_18 --> node_348
    node_991 --> node_806
    node_906 --> node_57
    node_339 --> node_938
    node_628 --> node_123
    node_6 --> node_987
    node_1018 --> node_764
    node_348 --> node_350
    node_809 --> node_899
    node_361 --> node_457
    node_451 --> node_883
    node_491 --> node_755
    node_361 --> node_745
    node_916 --> node_759
    node_842 --> node_758
    node_388 --> node_391
    node_463 --> node_997
    node_354 --> node_987
    node_6 --> node_1025
    node_822 --> node_799
    node_888 --> node_557
    node_809 --> node_883
    node_361 --> node_737
    node_444 --> node_161
    node_847 --> node_167
    node_505 --> node_990
    node_451 --> node_1028
    node_451 --> node_905
    node_916 --> node_842
    node_361 --> node_467
    node_84 --> node_807
    node_1013 --> node_901
    node_420 --> node_710
    node_6 --> node_315
    node_362 --> node_880
    node_410 --> node_938
    node_6 --> node_801
    node_809 --> node_905
    node_483 --> node_879
    node_18 --> node_581
    node_154 --> node_58
    node_463 --> node_998
    node_385 --> node_822
    node_6 --> node_795
    node_1013 --> node_760
    node_767 --> node_764
    node_85 --> node_706
    node_16 --> node_213
    node_361 --> node_805
    node_568 --> node_217
    node_474 --> node_750
    node_1013 --> node_754
    node_915 --> node_877
    node_944 --> node_194
    node_84 --> node_712
    node_164 --> node_966
    node_89 --> node_107
    node_361 --> node_912
    node_48 --> node_692
    node_205 --> node_197
    node_432 --> node_832
    node_184 --> node_974
    node_809 --> node_979
    node_124 --> node_107
    node_136 --> node_43
    node_184 --> node_953
    node_444 --> node_923
    node_6 --> node_676
    node_500 --> node_499
    node_342 --> node_289
    node_678 --> node_743
    node_915 --> node_1000
    node_348 --> node_792
    node_385 --> node_1011
    node_1013 --> node_1016
    node_696 --> node_699
    node_837 --> node_764
    node_52 --> node_57
    node_292 --> node_187
    node_435 --> node_520
    node_435 --> node_792
    node_361 --> node_783
    node_390 --> node_294
    node_385 --> node_804
    node_81 --> node_64
    node_90 --> node_540
    node_552 --> node_388
    node_916 --> node_1009
    node_420 --> node_717
    node_582 --> node_848
    node_822 --> node_167
    node_915 --> node_924
    node_420 --> node_787
    node_463 --> node_780
    node_991 --> node_743
    node_18 --> node_666
    node_385 --> node_987
    node_14 --> node_964
    node_483 --> node_160
    node_6 --> node_847
    node_385 --> node_6
    node_809 --> node_749
    node_481 --> node_918
    node_406 --> node_792
    node_486 --> node_837
    node_354 --> node_1027
    node_53 --> node_124
    node_49 --> node_529
    node_692 --> node_690
    node_385 --> node_1025
    node_1013 --> node_881
    node_276 --> node_718
    node_354 --> node_847
    node_364 --> node_6
    node_2 --> node_512
    node_90 --> node_35
    node_354 --> node_874
    node_570 --> node_529
    node_139 --> node_110
    node_899 --> node_738
    node_361 --> node_841
    node_916 --> node_904
    node_19 --> node_280
    node_991 --> node_823
    node_475 --> node_921
    node_916 --> node_1014
    node_6 --> node_844
    node_704 --> node_703
    node_476 --> node_990
    node_362 --> node_1016
    node_85 --> node_539
    node_569 --> node_218
    node_354 --> node_844
    node_483 --> node_813
    node_361 --> node_802
    node_88 --> node_710
    node_766 --> node_764
    node_385 --> node_801
    node_311 --> node_167
    node_938 --> node_311
    node_420 --> node_162
    node_451 --> node_784
    node_91 --> node_141
    node_385 --> node_795
    node_169 --> node_953
    node_338 --> node_272
    node_179 --> node_191
    node_1023 --> node_939
    node_944 --> node_169
    node_184 --> node_283
    node_519 --> node_848
    node_165 --> node_184
    node_809 --> node_989
    node_130 --> node_373
    node_614 --> node_955
    node_143 --> node_54
    node_49 --> node_548
    node_528 --> node_796
    node_809 --> node_784
    node_570 --> node_548
    node_6 --> node_37
    node_305 --> node_175
    node_14 --> node_848
    node_991 --> node_915
    node_29 --> node_696
    node_385 --> node_676
    node_362 --> node_881
    node_1013 --> node_1001
    node_385 --> node_946
    node_202 --> node_179
    node_431 --> node_66
    node_1004 --> node_742
    node_822 --> node_57
    node_480 --> node_745
    node_520 --> node_12
    node_244 --> node_442
    node_991 --> node_998
    node_85 --> node_732
    node_1013 --> node_893
    node_353 --> node_796
    node_451 --> node_978
    node_916 --> node_826
    node_484 --> node_903
    node_809 --> node_911
    node_991 --> node_875
    node_6 --> node_380
    node_6 --> node_540
    node_41 --> node_129
    node_620 --> node_317
    node_88 --> node_717
    node_354 --> node_750
    node_677 --> node_924
    node_355 --> node_233
    node_1013 --> node_991
    node_409 --> node_424
    node_552 --> node_485
    node_714 --> node_919
    node_385 --> node_249
    node_184 --> node_312
    node_354 --> node_546
    node_916 --> node_809
    node_385 --> node_847
    node_363 --> node_164
    node_127 --> node_797
    node_29 --> node_461
    node_6 --> node_425
    node_379 --> node_990
    node_361 --> node_706
    node_934 --> node_928
    node_490 --> node_160
    node_435 --> node_807
    node_639 --> node_945
    node_364 --> node_208
    node_364 --> node_339
    node_362 --> node_1001
    node_88 --> node_500
    node_991 --> node_917
    node_795 --> node_799
    node_385 --> node_844
    node_487 --> node_1022
    node_915 --> node_910
    node_130 --> node_471
    node_373 --> node_399
    node_679 --> node_741
    node_354 --> node_846
    node_484 --> node_992
    node_354 --> node_814
    node_169 --> node_955
    node_91 --> node_388
    node_877 --> node_160
    node_915 --> node_920
    node_184 --> node_963
    node_592 --> node_590
    node_708 --> node_739
    node_938 --> node_271
    node_435 --> node_712
    node_991 --> node_780
    node_91 --> node_432
    node_388 --> node_362
    node_88 --> node_162
    node_118 --> node_99
    node_1013 --> node_864
    node_462 --> node_742
    node_362 --> node_775
    node_575 --> node_849
    node_435 --> node_578
    node_169 --> node_233
    node_411 --> node_430
    node_354 --> node_791
    node_680 --> node_848
    node_6 --> node_916
    node_327 --> node_796
    node_385 --> node_37
    node_991 --> node_895
    node_475 --> node_742
    node_48 --> node_500
    node_29 --> node_1011
    node_242 --> node_66
    node_991 --> node_854
    node_354 --> node_698
    node_363 --> node_938
    node_459 --> node_484
    node_164 --> node_950
    node_11 --> node_477
    node_552 --> node_496
    node_432 --> node_427
    node_37 --> node_120
    node_507 --> node_512
    node_451 --> node_746
    node_49 --> node_107
    node_49 --> node_687
    node_18 --> node_373
    node_187 --> node_242
    node_631 --> node_514
    node_451 --> node_908
    node_570 --> node_687
    node_435 --> node_30
    node_187 --> node_219
    node_559 --> node_52
    node_136 --> node_540
    node_692 --> node_689
    node_0 --> node_430
    node_666 --> node_169
    node_484 --> node_909
    node_191 --> node_167
    node_484 --> node_940
    node_599 --> node_310
    node_385 --> node_540
    node_97 --> node_128
    node_385 --> node_546
    node_797 --> node_938
    node_169 --> node_958
    node_364 --> node_540
    node_915 --> node_736
    node_354 --> node_730
    node_169 --> node_302
    node_915 --> node_880
    node_420 --> node_33
    node_497 --> node_57
    node_87 --> node_858
    node_130 --> node_49
    node_385 --> node_425
    node_37 --> node_691
    node_758 --> node_731
    node_204 --> node_186
    node_915 --> node_822
    node_385 --> node_35
    node_813 --> node_183
    node_842 --> node_843
    node_662 --> node_289
    node_916 --> node_1028
    node_6 --> node_188
    node_41 --> node_936
    node_385 --> node_814
    node_772 --> node_764
    node_468 --> node_816
    node_37 --> node_67
    node_84 --> node_204
    node_91 --> node_441
    node_164 --> node_969
    node_822 --> node_178
    node_916 --> node_1006
    node_406 --> node_169
    node_162 --> node_161
    node_385 --> node_196
    node_361 --> node_2
    node_847 --> node_797
    node_300 --> node_296
    node_900 --> node_741
    node_87 --> node_129
    node_487 --> node_843
    node_432 --> node_428
    node_341 --> node_187
    node_809 --> node_944
    node_18 --> node_471
    node_341 --> node_169
    node_483 --> node_1004
    node_29 --> node_676
    node_184 --> node_270
    node_385 --> node_916
    node_385 --> node_698
    node_809 --> node_836
    node_48 --> node_763
    node_184 --> node_292
    node_762 --> node_1025
    node_169 --> node_969
    node_915 --> node_804
    node_621 --> node_425
    node_916 --> node_993
    node_1013 --> node_1021
    node_6 --> node_350
    node_991 --> node_901
    node_84 --> node_43
    node_354 --> node_1023
    node_847 --> node_845
    node_6 --> node_853
    node_370 --> node_246
    node_408 --> node_450
    node_991 --> node_760
    node_484 --> node_774
    node_420 --> node_485
    node_738 --> node_764
    node_649 --> node_169
    node_655 --> node_187
    node_1005 --> node_924
    node_991 --> node_754
    node_762 --> node_207
    node_385 --> node_648
    node_915 --> node_1025
    node_853 --> node_854
    node_435 --> node_423
    node_479 --> node_839
    node_484 --> node_899
    node_85 --> node_563
    node_106 --> node_54
    node_518 --> node_513
    node_663 --> node_296
    node_52 --> node_118
    node_938 --> node_309
    node_715 --> node_42
    node_164 --> node_281
    node_48 --> node_127
    node_481 --> node_713
    node_991 --> node_1016
    node_164 --> node_967
    node_164 --> node_275
    node_415 --> node_30
    node_881 --> node_43
    node_88 --> node_33
    node_615 --> node_796
    node_139 --> node_183
    node_86 --> node_57
    node_361 --> node_529
    node_795 --> node_848
    node_1010 --> node_1008
    node_915 --> node_801
    node_48 --> node_388
    node_605 --> node_972
    node_361 --> node_892
    node_6 --> node_579
    node_859 --> node_857
    node_915 --> node_795
    node_438 --> node_28
    node_351 --> node_214
    node_476 --> node_762
    node_476 --> node_769
    node_364 --> node_188
    node_14 --> node_209
    node_1013 --> node_759
    node_6 --> node_1013
    node_944 --> node_990
    node_372 --> node_938
    node_169 --> node_270
    node_18 --> node_49
    node_130 --> node_1011
    node_169 --> node_281
    node_482 --> node_1018
    node_500 --> node_257
    node_935 --> node_925
    node_754 --> node_752
    node_991 --> node_881
    node_451 --> node_750
    node_127 --> node_107
    node_1013 --> node_842
    node_484 --> node_979
    node_361 --> node_548
    node_385 --> node_310
    node_6 --> node_986
    node_333 --> node_848
    node_385 --> node_592
    node_204 --> node_189
    node_85 --> node_710
    node_14 --> node_849
    node_41 --> node_872
    node_354 --> node_986
    node_184 --> node_260
    node_385 --> node_350
    node_822 --> node_726
    node_354 --> node_903
    node_362 --> node_756
    node_915 --> node_810
    node_385 --> node_853
    node_864 --> node_741
    node_361 --> node_884
    node_87 --> node_936
    node_482 --> node_777
    node_916 --> node_978
    node_640 --> node_966
    node_362 --> node_886
    node_88 --> node_485
    node_204 --> node_42
    node_354 --> node_1002
    node_451 --> node_846
    node_482 --> node_756
    node_362 --> node_759
    node_29 --> node_546
    node_451 --> node_830
    node_836 --> node_837
    node_488 --> node_984
    node_679 --> node_839
    node_477 --> node_937
    node_473 --> node_738
    node_915 --> node_844
    node_809 --> node_830
    node_388 --> node_377
    node_14 --> node_966
    node_991 --> node_1001
    node_552 --> node_2
    node_634 --> node_861
    node_362 --> node_842
    node_6 --> node_354
    node_349 --> node_938
    node_435 --> node_204
    node_459 --> node_463
    node_446 --> node_874
    node_64 --> node_833
    node_809 --> node_781
    node_679 --> node_744
    node_164 --> node_308
    node_91 --> node_706
    node_863 --> node_764
    node_184 --> node_968
    node_934 --> node_927
    node_85 --> node_717
    node_991 --> node_893
    node_385 --> node_53
    node_187 --> node_175
    node_130 --> node_91
    node_697 --> node_11
    node_1005 --> node_920
    node_809 --> node_734
    node_6 --> node_994
    node_385 --> node_1013
    node_364 --> node_326
    node_483 --> node_161
    node_361 --> node_891
    node_147 --> node_39
    node_448 --> node_815
    node_1013 --> node_1014
    node_119 --> node_107
    node_385 --> node_654
    node_311 --> node_849
    node_847 --> node_796
    node_362 --> node_755
    node_521 --> node_764
    node_487 --> node_784
    node_714 --> node_921
    node_29 --> node_698
    node_451 --> node_887
    node_385 --> node_986
    node_618 --> node_304
    node_570 --> node_471
    node_88 --> node_496
    node_361 --> node_563
    node_571 --> node_57
    node_864 --> node_739
    node_781 --> node_778
    node_496 --> node_495
    node_831 --> node_832
    node_110 --> node_129
    node_483 --> node_815
    node_6 --> node_863
    node_451 --> node_862
    node_18 --> node_1011
    node_85 --> node_162
    node_362 --> node_1009
    node_361 --> node_472
    node_552 --> node_529
    node_854 --> node_853
    node_48 --> node_124
    node_916 --> node_908
    node_1013 --> node_821
    node_809 --> node_862
    node_484 --> node_911
    node_361 --> node_687
    node_6 --> node_835
    node_451 --> node_762
    node_451 --> node_831
    node_672 --> node_42
    node_1013 --> node_999
    node_621 --> node_494
    node_479 --> node_840
    node_29 --> node_730
    node_678 --> node_739
    node_354 --> node_835
    node_245 --> node_254
    node_776 --> node_170
    node_206 --> node_199
    node_1013 --> node_827
    node_795 --> node_794
    node_394 --> node_100
    node_706 --> node_695
    node_809 --> node_762
    node_809 --> node_831
    node_385 --> node_764
    node_435 --> node_990
    node_661 --> node_302
    node_938 --> node_953
    node_362 --> node_904
    node_48 --> node_496
    node_362 --> node_1014
    node_53 --> node_107
    node_476 --> node_767
    node_479 --> node_834
    node_573 --> node_197
    node_361 --> node_239
    node_107 --> node_980
    node_463 --> node_777
    node_53 --> node_109
    node_51 --> node_43
    node_915 --> node_718
    node_592 --> node_584
    node_892 --> node_52
    node_404 --> node_28
    node_329 --> node_848
    node_477 --> node_928
    node_552 --> node_548
    node_745 --> node_738
    node_657 --> node_213
    node_451 --> node_737
    node_822 --> node_796
    node_809 --> node_745
    node_242 --> node_253
    node_390 --> node_280
    node_666 --> node_625
    node_406 --> node_990
    node_939 --> node_940
    node_666 --> node_658
    node_110 --> node_121
    node_336 --> node_964
    node_466 --> node_793
    node_353 --> node_11
    node_712 --> node_711
    node_354 --> node_539
    node_364 --> node_442
    node_915 --> node_916
    node_385 --> node_994
    node_900 --> node_744
    node_89 --> node_91
    node_354 --> node_704
    node_386 --> node_233
    node_476 --> node_772
    node_83 --> node_82
    node_483 --> node_812
    node_762 --> node_349
    node_654 --> node_169
    node_484 --> node_897
    node_385 --> node_29
    node_6 --> node_774
    node_91 --> node_732
    node_14 --> node_682
    node_43 --> node_103
    node_482 --> node_999
    node_698 --> node_697
    node_916 --> node_1027
    node_679 --> node_835
    node_451 --> node_912
    node_809 --> node_1004
    node_809 --> node_805
    node_6 --> node_899
    node_130 --> node_546
    node_916 --> node_874
    node_385 --> node_863
    node_362 --> node_826
    node_669 --> node_25
    node_520 --> node_512
    node_410 --> node_481
    node_355 --> node_499
    node_915 --> node_349
    node_411 --> node_463
    node_451 --> node_921
    node_354 --> node_899
    node_84 --> node_432
    node_184 --> node_315
    node_6 --> node_883
    node_484 --> node_898
    node_660 --> node_959
    node_361 --> node_985
    node_54 --> node_82
    node_385 --> node_972
    node_385 --> node_835
    node_451 --> node_783
    node_730 --> node_727
    node_362 --> node_809
    node_643 --> node_271
    node_505 --> node_797
    node_89 --> node_208
    node_84 --> node_730
    node_354 --> node_732
    node_488 --> node_985
    node_6 --> node_905
    node_791 --> node_763
    node_552 --> node_581
    node_991 --> node_1021
    node_437 --> node_458
    node_89 --> node_105
    node_361 --> node_453
    node_203 --> node_194
    node_184 --> node_946
    node_391 --> node_458
    node_652 --> node_948
    node_859 --> node_799
    node_325 --> node_938
    node_1013 --> node_748
    node_809 --> node_808
    node_14 --> node_950
    node_177 --> node_938
    node_762 --> node_350
    node_451 --> node_841
    node_567 --> node_940
    node_529 --> node_525
    node_432 --> node_408
    node_6 --> node_979
    node_487 --> node_788
    node_679 --> node_838
    node_484 --> node_960
    node_385 --> node_263
    node_385 --> node_704
    node_48 --> node_939
    node_809 --> node_841
    node_882 --> node_764
    node_484 --> node_961
    node_11 --> node_481
    node_451 --> node_802
    node_2 --> node_695
    node_85 --> node_33
    node_451 --> node_1002
    node_493 --> node_1000
    node_552 --> node_687
    node_444 --> node_920
    node_672 --> node_498
    node_363 --> node_187
    node_916 --> node_750
    node_484 --> node_944
    node_915 --> node_350
    node_361 --> node_385
    node_385 --> node_774
    node_187 --> node_244
    node_484 --> node_489
    node_915 --> node_853
    node_385 --> node_186
    node_740 --> node_764
    node_221 --> node_296
    node_385 --> node_437
    node_184 --> node_269
    node_84 --> node_441
    node_388 --> node_384
    node_915 --> node_886
    node_1013 --> node_1006
    node_386 --> node_980
    node_813 --> node_169
    node_385 --> node_899
    node_900 --> node_863
    node_484 --> node_952
    node_864 --> node_744
    node_6 --> node_749
    node_484 --> node_954
    node_935 --> node_933
    node_802 --> node_800
    node_435 --> node_412
    node_991 --> node_759
    node_484 --> node_798
    node_300 --> node_796
    node_385 --> node_66
    node_169 --> node_197
    node_938 --> node_963
    node_14 --> node_969
    node_600 --> node_43
    node_944 --> node_167
    node_355 --> node_208
    node_385 --> node_883
    node_314 --> node_796
    node_916 --> node_846
    node_14 --> node_603
    node_323 --> node_187
    node_762 --> node_792
    node_6 --> node_515
    node_991 --> node_842
    node_432 --> node_412
    node_420 --> node_544
    node_1013 --> node_993
    node_18 --> node_546
    node_370 --> node_833
    node_1019 --> node_764
    node_580 --> node_169
    node_11 --> node_446
    node_362 --> node_1028
    node_53 --> node_373
    node_14 --> node_627
    node_827 --> node_824
    node_916 --> node_791
    node_85 --> node_485
    node_636 --> node_592
    node_6 --> node_989
    node_204 --> node_763
    node_847 --> node_763
    node_915 --> node_792
    node_362 --> node_1006
    node_6 --> node_784
    node_716 --> node_424
    node_361 --> node_743
    node_915 --> node_1013
    node_173 --> node_42
    node_186 --> node_540
    node_242 --> node_248
    node_822 --> node_172
    node_354 --> node_989
    node_37 --> node_83
    node_14 --> node_623
    node_597 --> node_962
    node_1013 --> node_593
    node_385 --> node_979
    node_354 --> node_984
    node_915 --> node_755
    node_47 --> node_980
    node_141 --> node_395
    node_384 --> node_2
    node_130 --> node_592
    node_29 --> node_705
    node_665 --> node_295
    node_169 --> node_208
    node_822 --> node_813
    node_361 --> node_823
    node_14 --> node_274
    node_677 --> node_922
    node_84 --> node_57
    node_354 --> node_976
    node_479 --> node_733
    node_892 --> node_890
    node_362 --> node_993
    node_242 --> node_250
    node_420 --> node_348
    node_356 --> node_168
    node_944 --> node_190
    node_667 --> node_965
    node_164 --> node_309
    node_6 --> node_911
    node_14 --> node_281
    node_367 --> node_2
    node_432 --> node_434
    node_14 --> node_967
    node_14 --> node_275
    node_354 --> node_692
    node_242 --> node_542
    node_49 --> node_91
    node_18 --> node_698
    node_435 --> node_432
    node_354 --> node_911
    node_435 --> node_799
    node_355 --> node_540
    node_91 --> node_563
    node_385 --> node_749
    node_354 --> node_873
    node_14 --> node_652
    node_1013 --> node_977
    node_812 --> node_764
    node_394 --> node_2
    node_379 --> node_797
    node_915 --> node_904
    node_435 --> node_730
    node_355 --> node_425
    node_361 --> node_915
    node_375 --> node_419
    node_202 --> node_296
    node_991 --> node_1014
    node_91 --> node_7
    node_636 --> node_520
    node_791 --> node_793
    node_420 --> node_581
    node_482 --> node_779
    node_169 --> node_965
    node_354 --> node_796
    node_130 --> node_53
    node_31 --> node_694
    node_361 --> node_998
    node_606 --> node_169
    node_466 --> node_790
    node_137 --> node_131
    node_595 --> node_972
    node_48 --> node_529
    node_300 --> node_958
    node_655 --> node_196
    node_687 --> node_680
    node_361 --> node_875
    node_859 --> node_855
    node_709 --> node_163
    node_361 --> node_982
    node_149 --> node_117
    node_385 --> node_989
    node_770 --> node_764
    node_41 --> node_105
    node_385 --> node_784
    node_81 --> node_57
    node_915 --> node_994
    node_991 --> node_821
    node_745 --> node_864
    node_916 --> node_1023
    node_432 --> node_430
    node_385 --> node_42
    node_477 --> node_927
    node_474 --> node_806
    node_991 --> node_999
    node_29 --> node_704
    node_448 --> node_819
    node_761 --> node_764
    node_221 --> node_262
    node_991 --> node_827
    node_878 --> node_728
    node_361 --> node_917
    node_521 --> node_796
    node_633 --> node_315
    node_435 --> node_441
    node_48 --> node_548
    node_915 --> node_826
    node_486 --> node_839
    node_890 --> node_695
    node_915 --> node_863
    node_385 --> node_692
    node_420 --> node_666
    node_385 --> node_911
    node_87 --> node_131
    node_708 --> node_746
    node_361 --> node_780
    node_916 --> node_912
    node_1004 --> node_738
    node_354 --> node_898
    node_968 --> node_11
    node_915 --> node_809
    node_385 --> node_384
    node_53 --> node_49
    node_267 --> node_14
    node_14 --> node_308
    node_362 --> node_978
    node_916 --> node_921
    node_354 --> node_710
    node_169 --> node_202
    node_248 --> node_249
    node_220 --> node_224
    node_361 --> node_895
    node_760 --> node_799
    node_651 --> node_188
    node_432 --> node_727
    node_597 --> node_303
    node_610 --> node_260
    node_1013 --> node_987
    node_480 --> node_743
    node_88 --> node_581
    node_969 --> node_849
    node_184 --> node_310
    node_52 --> node_436
    node_468 --> node_815
    node_374 --> node_11
    node_483 --> node_821
    node_898 --> node_896
    node_571 --> node_796
    node_566 --> node_796
    node_952 --> node_971
    node_978 --> node_42
    node_89 --> node_88
    node_463 --> node_779
    node_41 --> node_868
    node_6 --> node_944
    node_473 --> node_740
    node_1023 --> node_1025
    node_130 --> node_29
    node_410 --> node_474
    node_552 --> node_471
    node_916 --> node_903
    node_184 --> node_279
    node_636 --> node_807
    node_18 --> node_53
    node_6 --> node_836
    node_354 --> node_944
    node_842 --> node_757
    node_84 --> node_539
    node_484 --> node_959
    node_704 --> node_701
    node_673 --> node_25
    node_391 --> node_723
    node_915 --> node_774
    node_1005 --> node_922
    node_666 --> node_848
    node_361 --> node_880
    node_354 --> node_717
    node_432 --> node_431
    node_916 --> node_802
    node_462 --> node_738
    node_809 --> node_892
    node_484 --> node_942
    node_206 --> node_201
    node_916 --> node_1002
    node_939 --> node_941
    node_459 --> node_482
    node_37 --> node_42
    node_1023 --> node_207
    node_169 --> node_188
    node_636 --> node_712
    node_475 --> node_738
    node_48 --> node_563
    node_629 --> node_169
    node_184 --> node_951
    node_355 --> node_257
    node_406 --> node_57
    node_991 --> node_748
    node_437 --> node_11
    node_362 --> node_746
    node_88 --> node_666
    node_938 --> node_968
    node_431 --> node_833
    node_391 --> node_11
    node_353 --> node_465
    node_362 --> node_908
    node_915 --> node_883
    node_354 --> node_500
    node_646 --> node_279
    node_169 --> node_176
    node_484 --> node_793
    node_609 --> node_293
    node_48 --> node_107
    node_48 --> node_687
    node_679 --> node_919
    node_204 --> node_848
    node_791 --> node_939
    node_451 --> node_828
    node_636 --> node_541
    node_29 --> node_10
    node_248 --> node_246
    node_14 --> node_596
    node_51 --> node_57
    node_484 --> node_964
    node_831 --> node_829
    node_41 --> node_860
    node_915 --> node_905
    node_185 --> node_167
    node_184 --> node_304
    node_451 --> node_884
    node_354 --> node_162
    node_379 --> node_796
    node_84 --> node_732
    node_385 --> node_458
    node_52 --> node_113
    node_1013 --> node_847
    node_809 --> node_884
    node_1013 --> node_874
    node_384 --> node_409
    node_435 --> node_22
    node_477 --> node_935
    node_991 --> node_1006
    node_361 --> node_460
    node_139 --> node_43
    node_944 --> node_797
    node_679 --> node_836
    node_481 --> node_716
    node_187 --> node_181
    node_715 --> node_939
    node_915 --> node_979
    node_245 --> node_251
    node_486 --> node_835
    node_1013 --> node_844
    node_343 --> node_848
    node_385 --> node_944
    node_514 --> node_169
    node_385 --> node_521
    node_169 --> node_832
    node_296 --> node_179
    node_435 --> node_705
    node_814 --> node_845
    node_6 --> node_629
    node_451 --> node_873
    node_385 --> node_836
    node_361 --> node_1016
    node_991 --> node_993
    node_385 --> node_253
    node_14 --> node_271
    node_391 --> node_848
    node_469 --> node_160
    node_475 --> node_918
    node_362 --> node_1027
    node_459 --> node_475
    node_29 --> node_692
    node_385 --> node_798
    node_18 --> node_29
    node_362 --> node_874
    node_915 --> node_749
    node_900 --> node_746
    node_71 --> node_70
    node_936 --> node_163
    node_385 --> node_500
    node_791 --> node_790
    node_6 --> node_422
    node_615 --> node_938
    node_49 --> node_592
    node_809 --> node_891
    node_14 --> node_211
    node_570 --> node_592
    node_991 --> node_593
    node_904 --> node_906
    node_6 --> node_830
    node_361 --> node_881
    node_438 --> node_120
    node_156 --> node_54
    node_388 --> node_18
    node_486 --> node_838
    node_361 --> node_456
    node_153 --> node_54
    node_6 --> node_781
    node_198 --> node_191
    node_704 --> node_702
    node_87 --> node_866
    node_53 --> node_91
    node_41 --> node_46
    node_115 --> node_540
    node_204 --> node_939
    node_164 --> node_181
    node_647 --> node_319
    node_474 --> node_747
    node_697 --> node_31
    node_944 --> node_849
    node_41 --> node_1015
    node_177 --> node_187
    node_915 --> node_784
    node_6 --> node_734
    node_355 --> node_442
    node_411 --> node_482
    node_420 --> node_471
    node_354 --> node_734
    node_435 --> node_833
    node_987 --> node_47
    node_91 --> node_33
    node_438 --> node_691
    node_991 --> node_977
    node_435 --> node_539
    node_435 --> node_704
    node_989 --> node_207
    node_451 --> node_898
    node_173 --> node_799
    node_592 --> node_796
    node_874 --> node_978
    node_368 --> node_940
    node_164 --> node_963
    node_361 --> node_1001
    node_438 --> node_67
    node_384 --> node_429
    node_184 --> node_317
    node_906 --> node_907
    node_100 --> node_436
    node_116 --> node_54
    node_362 --> node_750
    node_125 --> node_43
    node_184 --> node_972
    node_50 --> node_764
    node_18 --> node_704
    node_88 --> node_373
    node_423 --> node_406
    node_49 --> node_520
    node_53 --> node_208
    node_87 --> node_860
    node_809 --> node_753
    node_570 --> node_520
    node_127 --> node_173
    node_361 --> node_893
    node_6 --> node_862
    node_388 --> node_367
    node_28 --> node_391
    node_1013 --> node_916
    node_509 --> node_169
    node_14 --> node_208
    node_226 --> node_190
    node_361 --> node_775
    node_484 --> node_939
    node_582 --> node_938
    node_163 --> node_759
    node_462 --> node_923
    node_53 --> node_105
    node_169 --> node_442
    node_346 --> node_213
    node_130 --> node_87
    node_432 --> node_426
    node_679 --> node_781
    node_6 --> node_762
    node_6 --> node_831
    node_14 --> node_164
    node_477 --> node_931
    node_187 --> node_247
    node_362 --> node_846
    node_435 --> node_797
    node_101 --> node_54
    node_14 --> node_957
    node_385 --> node_830
    node_475 --> node_923
    node_435 --> node_732
    node_446 --> node_873
    node_484 --> node_956
    node_848 --> node_940
    node_437 --> node_448
    node_184 --> node_263
    node_150 --> node_55
    node_85 --> node_348
    node_864 --> node_746
    node_385 --> node_781
    node_87 --> node_137
    node_822 --> node_721
    node_6 --> node_745
    node_451 --> node_985
    node_361 --> node_621
    node_529 --> node_528
    node_484 --> node_923
    node_100 --> node_123
    node_362 --> node_791
    node_704 --> node_705
    node_406 --> node_797
    node_569 --> node_221
    node_353 --> node_31
    node_847 --> node_938
    node_385 --> node_734
    node_14 --> node_309
    node_1023 --> node_349
    node_411 --> node_475
    node_141 --> node_118
    node_762 --> node_990
    node_678 --> node_746
    node_88 --> node_471
    node_385 --> node_388
    node_546 --> node_545
    node_899 --> node_741
    node_944 --> node_796
    node_519 --> node_938
    node_86 --> node_100
    node_813 --> node_799
    node_53 --> node_540
    node_85 --> node_581
    node_97 --> node_139
    node_29 --> node_717
    node_130 --> node_692
    node_451 --> node_806
    node_636 --> node_204
    node_87 --> node_135
    node_184 --> node_300
    node_14 --> node_938
    node_354 --> node_485
    node_14 --> node_223
    node_187 --> node_243
    node_991 --> node_987
    node_6 --> node_1004
    node_448 --> node_822
    node_6 --> node_805
    node_385 --> node_248
    node_484 --> node_790
    node_915 --> node_746
    node_836 --> node_839
    node_6 --> node_11
    node_355 --> node_169
    node_483 --> node_736
    node_542 --> node_543
    node_362 --> node_887
    node_354 --> node_1004
    node_915 --> node_908
    node_354 --> node_805
    node_451 --> node_160
    node_273 --> node_42
    node_730 --> node_725
    node_385 --> node_862
    node_29 --> node_500
    node_822 --> node_812
    node_1013 --> node_1023
    node_87 --> node_1015
    node_483 --> node_822
    node_404 --> node_120
    node_692 --> node_688
    node_385 --> node_430
    node_104 --> node_54
    node_650 --> node_962
    node_385 --> node_762
    node_385 --> node_831
    node_521 --> node_723
    node_1013 --> node_853
    node_679 --> node_745
    node_84 --> node_710
    node_822 --> node_938
    node_385 --> node_542
    node_29 --> node_162
    node_49 --> node_807
    node_484 --> node_864
    node_916 --> node_828
    node_570 --> node_807
    node_354 --> node_1010
    node_1023 --> node_350
    node_91 --> node_41
    node_916 --> node_984
    node_85 --> node_666
    node_184 --> node_273
    node_374 --> node_445
    node_385 --> node_745
    node_468 --> node_819
    node_169 --> node_187
    node_654 --> node_848
    node_899 --> node_739
    node_88 --> node_49
    node_916 --> node_976
    node_404 --> node_691
    node_87 --> node_133
    node_49 --> node_712
    node_6 --> node_841
    node_354 --> node_496
    node_362 --> node_737
    node_570 --> node_712
    node_432 --> node_410
    node_362 --> node_1023
    node_978 --> node_799
    node_915 --> node_836
    node_404 --> node_67
    node_6 --> node_848
    node_679 --> node_778
    node_139 --> node_799
    node_339 --> node_169
    node_680 --> node_938
    node_420 --> node_1011
    node_577 --> node_171
    node_361 --> node_1021
    node_451 --> node_743
    node_916 --> node_873
    node_84 --> node_717
    node_991 --> node_1027
    node_385 --> node_1004
    node_296 --> node_171
    node_795 --> node_207
    node_991 --> node_847
    node_929 --> node_931
    node_385 --> node_805
    node_991 --> node_874
    node_494 --> node_161
    node_809 --> node_924
    node_97 --> node_121
    node_809 --> node_743
    node_29 --> node_36
    node_221 --> node_226
    node_385 --> node_11
    node_481 --> node_714
    node_282 --> node_169
    node_361 --> node_348
    node_451 --> node_823
    node_362 --> node_912
    node_900 --> node_862
    node_1023 --> node_792
    node_989 --> node_173
    node_354 --> node_760
    node_1013 --> node_986
    node_477 --> node_933
    node_489 --> node_764
    node_991 --> node_844
    node_483 --> node_801
    node_881 --> node_879
    node_1013 --> node_903
    node_671 --> node_28
    node_18 --> node_692
    node_518 --> node_796
    node_362 --> node_921
    node_809 --> node_823
    node_354 --> node_754
    node_184 --> node_962
    node_41 --> node_859
    node_362 --> node_783
    node_43 --> node_118
    node_361 --> node_756
    node_385 --> node_436
    node_999 --> node_996
    node_84 --> node_162
    node_939 --> node_848
    node_514 --> node_521
    node_636 --> node_947
    node_368 --> node_42
    node_223 --> node_221
    node_900 --> node_745
    node_451 --> node_915
    node_453 --> node_764
    node_206 --> node_193
    node_361 --> node_759
    node_364 --> node_57
    node_385 --> node_496
    node_632 --> node_322
    node_35 --> node_151
    node_185 --> node_849
    node_124 --> node_43
    node_708 --> node_742
    node_331 --> node_181
    node_406 --> node_796
    node_385 --> node_841
    node_592 --> node_583
    node_242 --> node_233
    node_451 --> node_998
    node_29 --> node_388
    node_362 --> node_903
    node_598 --> node_319
    node_435 --> node_7
    node_361 --> node_842
    node_385 --> node_848
    node_666 --> node_631
    node_594 --> node_226
    node_654 --> node_213
    node_451 --> node_875
    node_916 --> node_898
    node_621 --> node_447
    node_362 --> node_802
    node_341 --> node_796
    node_300 --> node_938
    node_650 --> node_303
    node_184 --> node_970
    node_362 --> node_1002
    node_626 --> node_280
    node_6 --> node_939
    node_53 --> node_46
    node_88 --> node_1011
    node_130 --> node_500
    node_314 --> node_938
    node_809 --> node_982
    node_836 --> node_840
    node_525 --> node_764
    node_158 --> node_54
    node_484 --> node_953
    node_482 --> node_870
    node_385 --> node_123
    node_24 --> node_31
    node_938 --> node_310
    node_361 --> node_520
    node_91 --> node_105
    node_11 --> node_487
    node_836 --> node_834
    node_451 --> node_917
    node_1021 --> node_1020
    node_361 --> node_666
    node_496 --> node_494
    node_649 --> node_796
    node_944 --> node_943
    node_915 --> node_830
    node_435 --> node_710
    node_765 --> node_764
    node_477 --> node_869
    node_655 --> node_796
    node_486 --> node_836
    node_527 --> node_514
    node_6 --> node_163
    node_420 --> node_502
    node_809 --> node_917
    node_1010 --> node_1007
    node_184 --> node_294
    node_915 --> node_781
    node_354 --> node_163
    node_805 --> node_803
    node_451 --> node_780
    node_572 --> node_235
    node_809 --> node_910
    node_475 --> node_740
    node_602 --> node_311
    node_1013 --> node_835
    node_944 --> node_763
    node_361 --> node_1009
    node_714 --> node_918
    node_795 --> node_938
    node_35 --> node_122
    node_469 --> node_161
    node_915 --> node_734
    node_916 --> node_944
    node_451 --> node_895
    node_916 --> node_985
    node_971 --> node_316
    node_991 --> node_916
    node_477 --> node_867
    node_666 --> node_302
    node_451 --> node_854
    node_938 --> node_951
    node_171 --> node_219
    node_628 --> node_30
    node_580 --> node_198
    node_385 --> node_706
    node_467 --> node_453
    node_899 --> node_744
    node_29 --> node_723
    node_509 --> node_521
    node_361 --> node_1014
    node_521 --> node_721
    node_435 --> node_709
    node_435 --> node_717
    node_29 --> node_485
    node_410 --> node_483
    node_795 --> node_183
    node_915 --> node_887
    node_730 --> node_723
    node_864 --> node_745
    node_29 --> node_451
    node_642 --> node_964
    node_126 --> node_107
    node_470 --> node_848
    node_469 --> node_163
    node_916 --> node_806
    node_938 --> node_304
    node_333 --> node_938
    node_87 --> node_859
    node_184 --> node_303
    node_484 --> node_955
    node_968 --> node_31
    node_385 --> node_939
    node_6 --> node_2
    node_552 --> node_592
    node_14 --> node_616
    node_915 --> node_862
    node_11 --> node_492
    node_29 --> node_11
    node_178 --> node_175
    node_771 --> node_764
    node_679 --> node_163
    node_520 --> node_514
    node_48 --> node_207
    node_85 --> node_471
    node_519 --> node_509
    node_391 --> node_233
    node_483 --> node_814
    node_1013 --> node_774
    node_1002 --> node_1003
    node_915 --> node_762
    node_915 --> node_831
    node_98 --> node_105
    node_84 --> node_33
    node_482 --> node_1019
    node_416 --> node_434
    node_420 --> node_546
    node_666 --> node_969
    node_809 --> node_880
    node_132 --> node_373
    node_354 --> node_864
    node_952 --> node_316
    node_18 --> node_500
    node_385 --> node_163
    node_1013 --> node_899
    node_477 --> node_865
    node_645 --> node_962
    node_117 --> node_54
    node_435 --> node_162
    node_435 --> node_160
    node_795 --> node_173
    node_698 --> node_699
    node_390 --> node_208
    node_915 --> node_745
    node_1013 --> node_883
    node_49 --> node_204
    node_636 --> node_432
    node_14 --> node_963
    node_1005 --> node_919
    node_521 --> node_812
    node_361 --> node_450
    node_570 --> node_204
    node_915 --> node_737
    node_89 --> node_108
    node_871 --> node_870
    node_130 --> node_388
    node_200 --> node_201
    node_165 --> node_191
    node_918 --> node_2
    node_568 --> node_214
    node_29 --> node_496
    node_618 --> node_619
    node_406 --> node_160
    node_636 --> node_730
    node_462 --> node_31
    node_609 --> node_956
    node_991 --> node_1023
    node_361 --> node_809
    node_480 --> node_740
    node_451 --> node_901
    node_385 --> node_715
    node_473 --> node_741
    node_204 --> node_980
    node_552 --> node_520
    node_6 --> node_892
    node_451 --> node_760
    node_371 --> node_160
    node_359 --> node_120
    node_354 --> node_529
    node_29 --> node_848
    node_420 --> node_698
    node_169 --> node_322
    node_451 --> node_754
    node_177 --> node_196
    node_84 --> node_485
    node_1013 --> node_979
    node_972 --> node_764
    node_363 --> node_694
    node_438 --> node_83
    node_915 --> node_912
    node_205 --> node_849
    node_505 --> node_173
    node_646 --> node_952
    node_385 --> node_2
    node_811 --> node_174
    node_944 --> node_942
    node_451 --> node_1016
    node_915 --> node_921
    node_385 --> node_319
    node_435 --> node_763
    node_915 --> node_783
    node_435 --> node_562
    node_809 --> node_1016
    node_359 --> node_691
    node_354 --> node_548
    node_432 --> node_438
    node_938 --> node_940
    node_91 --> node_348
    node_88 --> node_546
    node_867 --> node_865
    node_496 --> node_497
    node_571 --> node_938
    node_169 --> node_947
    node_566 --> node_938
    node_636 --> node_441
    node_372 --> node_940
    node_359 --> node_67
    node_494 --> node_495
    node_1013 --> node_749
    node_6 --> node_884
    node_822 --> node_184
    node_484 --> node_980
    node_406 --> node_763
    node_310 --> node_11
    node_991 --> node_1013
    node_517 --> node_796
    node_938 --> node_972
    node_822 --> node_980
    node_451 --> node_881
    node_354 --> node_1024
    node_437 --> node_462
    node_451 --> node_161
    node_107 --> node_42
    node_915 --> node_841
    node_916 --> node_915
    node_809 --> node_881
    node_991 --> node_986
    node_542 --> node_541
    node_633 --> node_970
    node_2 --> node_434
    node_991 --> node_903
    node_187 --> node_196
    node_385 --> node_440
    node_462 --> node_924
    node_915 --> node_802
    node_827 --> node_825
    node_936 --> node_52
    node_385 --> node_529
    node_629 --> node_848
    node_763 --> node_771
    node_14 --> node_187
    node_385 --> node_892
    node_207 --> node_540
    node_1013 --> node_989
    node_361 --> node_1028
    node_1013 --> node_784
    node_98 --> node_395
    node_18 --> node_388
    node_1013 --> node_984
    node_809 --> node_810
    node_91 --> node_46
    node_132 --> node_49
    node_745 --> node_741
    node_645 --> node_303
    node_6 --> node_378
    node_483 --> node_1015
    node_361 --> node_1006
    node_91 --> node_99
    node_290 --> node_43
    node_242 --> node_252
    node_6 --> node_891
    node_991 --> node_764
    node_484 --> node_924
    node_435 --> node_33
    node_451 --> node_1001
    node_349 --> node_940
    node_379 --> node_938
    node_354 --> node_581
    node_487 --> node_789
    node_677 --> node_921
    node_565 --> node_175
    node_552 --> node_807
    node_385 --> node_548
    node_809 --> node_1001
    node_1013 --> node_911
    node_91 --> node_88
    node_451 --> node_893
    node_139 --> node_128
    node_88 --> node_395
    node_29 --> node_163
    node_678 --> node_742
    node_361 --> node_993
    node_85 --> node_1011
    node_85 --> node_43
    node_91 --> node_666
    node_704 --> node_700
    node_362 --> node_828
    node_451 --> node_991
    node_89 --> node_18
    node_483 --> node_1005
    node_730 --> node_721
    node_385 --> node_884
    node_552 --> node_712
    node_362 --> node_984
    node_130 --> node_496
    node_184 --> node_261
    node_514 --> node_848
    node_809 --> node_775
    node_169 --> node_320
    node_374 --> node_52
    node_418 --> node_445
    node_354 --> node_687
    node_797 --> node_42
    node_420 --> node_53
    node_362 --> node_976
    node_616 --> node_167
    node_164 --> node_949
    node_444 --> node_919
    node_361 --> node_593
    node_127 --> node_43
    node_247 --> node_2
    node_916 --> node_854
    node_902 --> node_906
    node_48 --> node_349
    node_6 --> node_631
    node_367 --> node_728
    node_630 --> node_218
    node_654 --> node_233
    node_6 --> node_955
    node_87 --> node_871
    node_361 --> node_469
    node_187 --> node_268
    node_745 --> node_739
    node_435 --> node_485
    node_510 --> node_514
    node_436 --> node_708
    node_6 --> node_753
    node_362 --> node_873
    node_502 --> node_2
    node_726 --> node_514
    node_184 --> node_266
    node_991 --> node_835
    node_354 --> node_753
    node_379 --> node_173
    node_88 --> node_592
    node_169 --> node_949
    node_29 --> node_2
    node_391 --> node_52
    node_98 --> node_99
    node_450 --> node_473
    node_169 --> node_225
    node_596 --> node_953
    node_385 --> node_891
    node_916 --> node_1010
    node_813 --> node_796
    node_14 --> node_948
    node_388 --> node_385
    node_361 --> node_977
    node_414 --> node_958
    node_520 --> node_513
    node_14 --> node_299
    node_462 --> node_920
    node_478 --> node_923
    node_114 --> node_58
    node_386 --> node_42
    node_385 --> node_507
    node_385 --> node_563
    node_18 --> node_100
    node_644 --> node_318
    node_636 --> node_706
    node_791 --> node_1025
    node_432 --> node_399
    node_475 --> node_920
    node_595 --> node_319
    node_48 --> node_592
    node_11 --> node_488
    node_487 --> node_917
    node_385 --> node_472
    node_484 --> node_910
    node_6 --> node_958
    node_361 --> node_461
    node_435 --> node_24
    node_89 --> node_57
    node_385 --> node_687
    node_580 --> node_796
    node_1023 --> node_990
    node_130 --> node_706
    node_361 --> node_978
    node_484 --> node_920
    node_18 --> node_436
    node_739 --> node_764
    node_762 --> node_797
    node_361 --> node_204
    node_791 --> node_207
    node_52 --> node_103
    node_781 --> node_777
    node_991 --> node_774
    node_474 --> node_748
    node_88 --> node_53
    node_119 --> node_43
    node_484 --> node_896
    node_14 --> node_642
    node_354 --> node_821
    node_473 --> node_744
    node_510 --> node_516
    node_916 --> node_901
    node_476 --> node_768
    node_484 --> node_968
    node_29 --> node_529
    node_18 --> node_496
    node_509 --> node_848
    node_991 --> node_899
    node_362 --> node_898
    node_184 --> node_964
    node_916 --> node_760
    node_420 --> node_29
    node_47 --> node_42
    node_385 --> node_753
    node_2 --> node_12
    node_991 --> node_883
    node_1013 --> node_944
    node_715 --> node_207
    node_482 --> node_871
    node_916 --> node_754
    node_484 --> node_776
    node_91 --> node_98
    node_358 --> node_167
    node_361 --> node_1011
    node_1013 --> node_836
    node_425 --> node_447
    node_49 --> node_432
    node_979 --> node_756
    node_570 --> node_432
    node_434 --> node_2
    node_636 --> node_539
    node_772 --> node_52
    node_451 --> node_1021
    node_1005 --> node_921
    node_48 --> node_520
    node_29 --> node_548
    node_48 --> node_792
    node_448 --> node_818
    node_18 --> node_123
    node_49 --> node_730
    node_366 --> node_470
    node_38 --> node_54
    node_461 --> node_731
    node_356 --> node_540
    node_354 --> node_980
    node_14 --> node_576
    node_679 --> node_837
    node_361 --> node_987
    node_854 --> node_851
    node_540 --> node_66
    node_459 --> node_481
    node_638 --> node_300
    node_749 --> node_747
    node_355 --> node_57
    node_991 --> node_979
    node_483 --> node_818
    node_944 --> node_938
    node_213 --> node_224
    node_388 --> node_369
    node_348 --> node_207
    node_606 --> node_796
    node_572 --> node_226
    node_204 --> node_1025
    node_847 --> node_1025
    node_529 --> node_522
    node_892 --> node_889
    node_362 --> node_985
    node_354 --> node_877
    node_109 --> node_208
    node_43 --> node_436
    node_127 --> node_37
    node_450 --> node_463
    node_340 --> node_169
    node_85 --> node_540
    node_897 --> node_764
    node_423 --> node_6
    node_2 --> node_705
    node_85 --> node_546
    node_49 --> node_18
    node_405 --> node_259
    node_53 --> node_51
    node_636 --> node_732
    node_915 --> node_892
    node_420 --> node_704
    node_354 --> node_1000
    node_921 --> node_924
    node_809 --> node_756
    node_204 --> node_207
    node_373 --> node_42
    node_1028 --> node_1026
    node_169 --> node_190
    node_451 --> node_759
    node_991 --> node_749
    node_388 --> node_353
    node_6 --> node_924
    node_6 --> node_743
    node_435 --> node_20
    node_184 --> node_280
    node_574 --> node_848
    node_420 --> node_838
    node_362 --> node_806
    node_88 --> node_29
    node_745 --> node_744
    node_49 --> node_441
    node_809 --> node_886
    node_354 --> node_924
    node_570 --> node_441
    node_809 --> node_759
    node_163 --> node_758
    node_169 --> node_57
    node_361 --> node_443
    node_899 --> node_746
    node_451 --> node_842
    node_29 --> node_581
    node_52 --> node_116
    node_6 --> node_823
    node_410 --> node_11
    node_466 --> node_792
    node_385 --> node_429
    node_409 --> node_429
    node_385 --> node_969
    node_169 --> node_296
    node_607 --> node_215
    node_43 --> node_123
    node_989 --> node_990
    node_915 --> node_828
    node_481 --> node_160
    node_552 --> node_204
    node_279 --> node_971
    node_944 --> node_173
    node_915 --> node_884
    node_991 --> node_989
    node_85 --> node_698
    node_587 --> node_848
    node_227 --> node_224
    node_991 --> node_784
    node_248 --> node_542
    node_916 --> node_893
    node_361 --> node_1027
    node_991 --> node_984
    node_459 --> node_486
    node_515 --> node_848
    node_354 --> node_471
    node_631 --> node_848
    node_361 --> node_874
    node_916 --> node_991
    node_695 --> node_696
    node_1004 --> node_741
    node_484 --> node_795
    node_169 --> node_301
    node_484 --> node_906
    node_1013 --> node_830
    node_29 --> node_687
    node_385 --> node_242
    node_43 --> node_113
    node_204 --> node_208
    node_339 --> node_848
    node_48 --> node_807
    node_507 --> node_12
    node_130 --> node_529
    node_14 --> node_298
    node_1013 --> node_781
    node_809 --> node_755
    node_187 --> node_833
    node_435 --> node_695
    node_679 --> node_924
    node_679 --> node_743
    node_977 --> node_976
    node_991 --> node_911
    node_484 --> node_946
    node_14 --> node_598
    node_84 --> node_348
    node_671 --> node_906
    node_282 --> node_848
    node_1013 --> node_734
    node_484 --> node_456
    node_6 --> node_875
    node_666 --> node_621
    node_715 --> node_183
    node_809 --> node_1009
    node_48 --> node_712
    node_6 --> node_982
    node_671 --> node_120
    node_63 --> node_58
    node_410 --> node_848
    node_6 --> node_52
    node_385 --> node_731
    node_599 --> node_968
    node_388 --> node_374
    node_385 --> node_924
    node_385 --> node_743
    node_57 --> node_208
    node_916 --> node_864
    node_730 --> node_876
    node_915 --> node_891
    node_225 --> node_499
    node_29 --> node_233
    node_847 --> node_37
    node_592 --> node_589
    node_130 --> node_548
    node_451 --> node_1014
    node_52 --> node_540
    node_448 --> node_817
    node_52 --> node_111
    node_629 --> node_796
    node_334 --> node_288
    node_435 --> node_1
    node_623 --> node_946
    node_809 --> node_904
    node_390 --> node_187
    node_385 --> node_823
    node_594 --> node_218
    node_6 --> node_917
    node_391 --> node_208
    node_84 --> node_581
    node_53 --> node_108
    node_379 --> node_184
    node_18 --> node_2
    node_921 --> node_920
    node_462 --> node_741
    node_6 --> node_910
    node_791 --> node_349
    node_361 --> node_750
    node_745 --> node_863
    node_6 --> node_252
    node_671 --> node_691
    node_483 --> node_817
    node_354 --> node_910
    node_715 --> node_173
    node_361 --> node_546
    node_451 --> node_821
    node_204 --> node_540
    node_298 --> node_949
    node_406 --> node_938
    node_475 --> node_741
    node_671 --> node_67
    node_451 --> node_999
    node_485 --> node_487
    node_1013 --> node_831
    node_354 --> node_920
    node_448 --> node_816
    node_329 --> node_187
    node_451 --> node_827
    node_329 --> node_169
    node_727 --> node_764
    node_37 --> node_980
    node_6 --> node_895
    node_484 --> node_775
    node_842 --> node_824
    node_341 --> node_938
    node_715 --> node_349
    node_573 --> node_849
    node_362 --> node_915
    node_482 --> node_995
    node_112 --> node_208
    node_361 --> node_846
    node_204 --> node_183
    node_509 --> node_517
    node_775 --> node_776
    node_483 --> node_816
    node_989 --> node_37
    node_1013 --> node_745
    node_435 --> node_28
    node_184 --> node_319
    node_723 --> node_764
    node_362 --> node_998
    node_385 --> node_528
    node_243 --> node_250
    node_484 --> node_824
    node_484 --> node_965
    node_84 --> node_666
    node_708 --> node_738
    node_822 --> node_258
    node_572 --> node_227
    node_701 --> node_696
    node_809 --> node_826
    node_29 --> node_31
    node_348 --> node_173
    node_904 --> node_902
    node_649 --> node_938
    node_784 --> node_785
    node_385 --> node_982
    node_361 --> node_791
    node_49 --> node_706
    node_18 --> node_529
    node_900 --> node_743
    node_655 --> node_938
    node_570 --> node_706
    node_420 --> node_692
    node_375 --> node_1003
    node_361 --> node_698
    node_85 --> node_53
    node_411 --> node_486
    node_669 --> node_410
    node_169 --> node_235
    node_448 --> node_820
    node_822 --> node_540
    node_435 --> node_544
    node_6 --> node_880
    node_462 --> node_739
    node_130 --> node_563
    node_528 --> node_169
    node_354 --> node_736
    node_1013 --> node_1004
    node_716 --> node_715
    node_1013 --> node_805
    node_612 --> node_226
    node_91 --> node_1011
    node_628 --> node_431
    node_91 --> node_43
    node_354 --> node_880
    node_385 --> node_917
    node_916 --> node_1024
    node_483 --> node_981
    node_406 --> node_173
    node_14 --> node_949
    node_822 --> node_425
    node_385 --> node_910
    node_483 --> node_820
    node_354 --> node_822
    node_385 --> node_252
    node_459 --> node_480
    node_130 --> node_687
    node_18 --> node_548
    node_361 --> node_730
    node_213 --> node_188
    node_362 --> node_780
    node_204 --> node_349
    node_822 --> node_814
    node_847 --> node_349
    node_915 --> node_985
    node_11 --> node_476
    node_991 --> node_944
    node_822 --> node_718
    node_795 --> node_990
    node_353 --> node_169
    node_6 --> node_604
    node_41 --> node_935
    node_991 --> node_836
    node_1013 --> node_1010
    node_636 --> node_710
    node_177 --> node_796
    node_41 --> node_394
    node_730 --> node_719
    node_822 --> node_202
    node_372 --> node_191
    node_435 --> node_348
    node_85 --> node_115
    node_435 --> node_170
    node_362 --> node_854
    node_672 --> node_183
    node_49 --> node_539
    node_939 --> node_175
    node_911 --> node_909
    node_791 --> node_792
    node_570 --> node_539
    node_484 --> node_882
    node_451 --> node_748
    node_915 --> node_806
    node_11 --> node_493
    node_354 --> node_804
    node_999 --> node_997
    node_781 --> node_779
    node_463 --> node_995
    node_364 --> node_311
    node_90 --> node_208
    node_529 --> node_526
    node_603 --> node_960
    node_406 --> node_170
    node_53 --> node_18
    node_435 --> node_454
    node_730 --> node_731
    node_88 --> node_692
    node_715 --> node_792
    node_361 --> node_1023
    node_138 --> node_43
    node_435 --> node_581
    node_6 --> node_1016
    node_361 --> node_441
    node_385 --> node_736
    node_410 --> node_2
    node_362 --> node_1010
    node_385 --> node_880
    node_204 --> node_350
    node_847 --> node_350
    node_636 --> node_717
    node_327 --> node_169
    node_809 --> node_1028
    node_495 --> node_514
    node_451 --> node_1006
    node_310 --> node_31
    node_6 --> node_207
    node_87 --> node_900
    node_147 --> node_43
    node_164 --> node_277
    node_864 --> node_743
    node_49 --> node_732
    node_575 --> node_940
    node_6 --> node_569
    node_85 --> node_29
    node_904 --> node_723
    node_354 --> node_801
    node_501 --> node_2
    node_570 --> node_732
    node_822 --> node_255
    node_363 --> node_848
    node_204 --> node_180
    node_354 --> node_795
    node_29 --> node_471
    node_809 --> node_1006
    node_204 --> node_177
    node_462 --> node_922
    node_14 --> node_167
    node_169 --> node_849
    node_637 --> node_218
    node_666 --> node_326
    node_822 --> node_188
    node_444 --> node_163
    node_448 --> node_811
    node_330 --> node_164
    node_1004 --> node_744
    node_899 --> node_745
    node_497 --> node_540
    node_6 --> node_881
    node_391 --> node_170
    node_354 --> node_91
    node_451 --> node_993
    node_49 --> node_128
    node_577 --> node_172
    node_361 --> node_921
    node_326 --> node_311
    node_169 --> node_277
    node_18 --> node_687
    node_97 --> node_764
    node_916 --> node_753
    node_48 --> node_204
    node_483 --> node_811
    node_361 --> node_447
    node_809 --> node_993
    node_165 --> node_958
    node_636 --> node_162
    node_362 --> node_901
    node_484 --> node_922
    node_435 --> node_666
    node_859 --> node_980
    node_391 --> node_527
    node_478 --> node_924
    node_6 --> node_810
    node_956 --> node_293
    node_441 --> node_798
    node_432 --> node_439
    node_169 --> node_966
    node_915 --> node_743
    node_484 --> node_756
    node_362 --> node_760
    node_223 --> node_220
    node_354 --> node_810
    node_552 --> node_432
    node_204 --> node_792
    node_847 --> node_792
    node_698 --> node_695
    node_451 --> node_593
    node_795 --> node_37
    node_385 --> node_499
    node_362 --> node_754
    node_468 --> node_818
    node_943 --> node_764
    node_991 --> node_830
    node_435 --> node_8
    node_6 --> node_208
    node_328 --> node_169
    node_355 --> node_796
    node_473 --> node_746
    node_915 --> node_823
    node_939 --> node_197
    node_630 --> node_222
    node_361 --> node_986
    node_822 --> node_257
    node_6 --> node_1001
    node_822 --> node_180
    node_293 --> node_956
    node_892 --> node_557
    node_420 --> node_500
    node_242 --> node_442
    node_361 --> node_903
    node_28 --> node_436
    node_487 --> node_759
    node_991 --> node_781
    node_385 --> node_1016
    node_53 --> node_57
    node_484 --> node_832
    node_517 --> node_938
    node_420 --> node_506
    node_85 --> node_704
    node_757 --> node_764
    node_488 --> node_986
    node_462 --> node_744
    node_484 --> node_1015
    node_14 --> node_57
    node_484 --> node_951
    node_361 --> node_1002
    node_432 --> node_416
    node_991 --> node_734
    node_385 --> node_207
    node_487 --> node_842
    node_11 --> node_463
    node_647 --> node_972
    node_776 --> node_11
    node_6 --> node_775
    node_164 --> node_305
    node_451 --> node_977
    node_938 --> node_964
    node_1026 --> node_764
    node_475 --> node_744
    node_406 --> node_514
    node_184 --> node_955
    node_916 --> node_821
    node_84 --> node_471
    node_391 --> node_494
    node_916 --> node_999
    node_1028 --> node_764
    node_91 --> node_546
    node_385 --> node_881
    node_86 --> node_540
    node_505 --> node_37
    node_484 --> node_792
    node_48 --> node_990
    node_916 --> node_827
    node_654 --> node_938
    node_273 --> node_980
    node_915 --> node_998
    node_737 --> node_735
    node_43 --> node_107
    node_335 --> node_188
    node_6 --> node_621
    node_14 --> node_301
    node_169 --> node_305
    node_552 --> node_441
    node_28 --> node_123
    node_915 --> node_875
    node_220 --> node_319
    node_658 --> node_494
    node_915 --> node_982
    node_481 --> node_161
    node_385 --> node_810
    node_925 --> node_439
    node_832 --> node_833
    node_425 --> node_458
    node_432 --> node_404
    node_225 --> node_257
    node_809 --> node_978
    node_933 --> node_764
    node_385 --> node_25
    node_136 --> node_208
    node_391 --> node_514
    node_410 --> node_477
    node_379 --> node_1025
    node_567 --> node_197
    node_385 --> node_208
    node_450 --> node_482
    node_915 --> node_917
    node_372 --> node_848
    node_385 --> node_1001
    node_540 --> node_248
    node_173 --> node_183
    node_184 --> node_958
    node_184 --> node_302
    node_484 --> node_904
    node_169 --> node_239
    node_91 --> node_698
    node_991 --> node_745
    node_847 --> node_940
    node_354 --> node_183
    node_745 --> node_746
    node_845 --> node_764
    node_478 --> node_920
    node_364 --> node_164
    node_435 --> node_980
    node_916 --> node_877
    node_90 --> node_170
    node_366 --> node_425
    node_481 --> node_923
    node_915 --> node_780
    node_476 --> node_766
    node_388 --> node_170
    node_362 --> node_893
    node_1023 --> node_797
    node_385 --> node_775
    node_362 --> node_991
    node_916 --> node_1000
    node_509 --> node_510
    node_636 --> node_33
    node_164 --> node_961
    node_678 --> node_738
    node_915 --> node_895
    node_391 --> node_442
    node_666 --> node_661
    node_14 --> node_940
    node_540 --> node_542
    node_49 --> node_563
    node_57 --> node_64
    node_91 --> node_730
    node_144 --> node_54
    node_570 --> node_563
    node_363 --> node_2
    node_386 --> node_213
    node_451 --> node_987
    node_86 --> node_395
    node_354 --> node_916
    node_484 --> node_994
    node_481 --> node_715
    node_6 --> node_173
    node_991 --> node_1004
    node_698 --> node_703
    node_991 --> node_805
    node_842 --> node_826
    node_420 --> node_388
    node_184 --> node_321
    node_657 --> node_225
    node_184 --> node_969
    node_468 --> node_817
    node_813 --> node_938
    node_169 --> node_961
    node_809 --> node_746
    node_916 --> node_748
    node_349 --> node_848
    node_361 --> node_539
    node_361 --> node_704
    node_636 --> node_267
    node_809 --> node_908
    node_6 --> node_349
    node_484 --> node_826
    node_769 --> node_764
    node_484 --> node_863
    node_822 --> node_940
    node_935 --> node_764
    node_29 --> node_499
    node_355 --> node_160
    node_362 --> node_864
    node_91 --> node_18
    node_1013 --> node_892
    node_368 --> node_980
    node_169 --> node_950
    node_991 --> node_1010
    node_595 --> node_278
    node_571 --> node_540
    node_484 --> node_972
    node_679 --> node_739
    node_361 --> node_437
    node_312 --> node_187
    node_49 --> node_710
    node_14 --> node_263
    node_385 --> node_183
    node_580 --> node_938
    node_385 --> node_907
    node_636 --> node_485
    node_570 --> node_710
    node_483 --> node_737
    node_204 --> node_187
    node_560 --> node_52
    node_204 --> node_169
    node_847 --> node_169
    node_221 --> node_224
    node_37 --> node_208
    node_672 --> node_194
    node_29 --> node_906
    node_435 --> node_471
    node_406 --> node_653
    node_706 --> node_11
    node_311 --> node_940
    node_921 --> node_922
    node_85 --> node_692
    node_361 --> node_732
    node_760 --> node_980
    node_379 --> node_37
    node_34 --> node_40
    node_671 --> node_83
    node_915 --> node_901
    node_184 --> node_281
    node_135 --> node_43
    node_451 --> node_1027
    node_184 --> node_275
    node_6 --> node_756
    node_1013 --> node_1024
    node_354 --> node_592
    node_451 --> node_847
    node_84 --> node_1011
    node_169 --> node_172
    node_362 --> node_445
    node_451 --> node_874
    node_343 --> node_187
    node_552 --> node_706
    node_343 --> node_169
    node_809 --> node_1027
    node_408 --> node_470
    node_162 --> node_163
    node_88 --> node_388
    node_49 --> node_717
    node_572 --> node_218
    node_6 --> node_886
    node_809 --> node_874
    node_354 --> node_853
    node_756 --> node_977
    node_6 --> node_759
    node_468 --> node_820
    node_480 --> node_742
    node_88 --> node_432
    node_451 --> node_844
    node_138 --> node_18
    node_391 --> node_187
    node_880 --> node_43
    node_354 --> node_886
    node_391 --> node_169
    node_623 --> node_263
    node_385 --> node_349
    node_279 --> node_316
    node_958 --> node_179
    node_822 --> node_169
    node_916 --> node_593
    node_915 --> node_1016
    node_6 --> node_842
    node_916 --> node_910
    node_29 --> node_391
    node_978 --> node_183
    node_484 --> node_883
    node_989 --> node_797
    node_37 --> node_540
    node_708 --> node_740
    node_916 --> node_920
    node_854 --> node_852
    node_351 --> node_244
    node_606 --> node_938
    node_915 --> node_207
    node_408 --> node_462
    node_362 --> node_1021
    node_665 --> node_957
    node_362 --> node_1024
    node_420 --> node_34
    node_48 --> node_432
    node_1013 --> node_891
    node_484 --> node_905
    node_938 --> node_319
    node_411 --> node_484
    node_476 --> node_761
    node_49 --> node_162
    node_340 --> node_848
    node_900 --> node_739
    node_944 --> node_1025
    node_354 --> node_53
    node_679 --> node_922
    node_6 --> node_792
    node_679 --> node_777
    node_373 --> node_163
    node_483 --> node_848
    node_413 --> node_2
    node_483 --> node_802
    node_915 --> node_881
    node_48 --> node_730
    node_37 --> node_183
    node_226 --> node_199
    node_679 --> node_756
    node_916 --> node_977
    node_354 --> node_1013
    node_169 --> node_967
    node_169 --> node_275
    node_364 --> node_170
    node_473 --> node_745
    node_6 --> node_755
    node_552 --> node_539
    node_598 --> node_972
    node_366 --> node_494
    node_420 --> node_496
    node_354 --> node_755
    node_187 --> node_245
    node_809 --> node_750
    node_385 --> node_756
    node_677 --> node_918
    node_6 --> node_1009
    node_361 --> node_828
    node_361 --> node_989
    node_184 --> node_308
    node_361 --> node_984
    node_6 --> node_514
    node_109 --> node_43
    node_916 --> node_736
    node_385 --> node_886
    node_184 --> node_267
    node_385 --> node_257
    node_636 --> node_14
    node_385 --> node_759
    node_14 --> node_277
    node_111 --> node_54
    node_232 --> node_764
    node_246 --> node_253
    node_325 --> node_848
    node_361 --> node_976
    node_734 --> node_764
    node_6 --> node_904
    node_809 --> node_846
    node_432 --> node_47
    node_163 --> node_160
    node_6 --> node_181
    node_915 --> node_1001
    node_6 --> node_1014
    node_916 --> node_822
    node_178 --> node_196
    node_354 --> node_904
    node_1013 --> node_753
    node_791 --> node_990
    node_552 --> node_732
    node_938 --> node_849
    node_582 --> node_796
    node_373 --> node_2
    node_43 --> node_52
    node_361 --> node_692
    node_654 --> node_442
    node_48 --> node_441
    node_451 --> node_791
    node_88 --> node_100
    node_507 --> node_417
    node_52 --> node_101
    node_53 --> node_126
    node_468 --> node_811
    node_915 --> node_893
    node_361 --> node_873
    node_745 --> node_862
    node_809 --> node_791
    node_411 --> node_473
    node_915 --> node_775
    node_510 --> node_511
    node_385 --> node_439
    node_822 --> node_189
    node_730 --> node_718
    node_385 --> node_494
    node_385 --> node_520
    node_131 --> node_18
    node_385 --> node_792
    node_715 --> node_990
    node_477 --> node_934
    node_484 --> node_962
    node_324 --> node_283
    node_916 --> node_804
    node_354 --> node_994
    node_89 --> node_41
    node_85 --> node_500
    node_385 --> node_755
    node_390 --> node_57
    node_435 --> node_1011
    node_822 --> node_42
    node_169 --> node_308
    node_354 --> node_29
    node_916 --> node_987
    node_989 --> node_988
    node_169 --> node_267
    node_379 --> node_350
    node_64 --> node_66
    node_519 --> node_796
    node_6 --> node_516
    node_6 --> node_826
    node_809 --> node_887
    node_385 --> node_1009
    node_1004 --> node_746
    node_934 --> node_764
    node_629 --> node_938
    node_354 --> node_826
    node_652 --> node_270
    node_354 --> node_863
    node_354 --> node_807
    node_944 --> node_37
    node_14 --> node_796
    node_661 --> node_961
    node_484 --> node_971
    node_6 --> node_809
    node_991 --> node_864
    node_164 --> node_311
    node_435 --> node_6
    node_348 --> node_990
    node_84 --> node_540
    node_354 --> node_809
    node_484 --> node_978
    node_14 --> node_305
    node_84 --> node_546
    node_435 --> node_1025
    node_91 --> node_539
    node_677 --> node_923
    node_695 --> node_694
    node_916 --> node_801
    node_91 --> node_704
    node_385 --> node_904
    node_49 --> node_33
    node_385 --> node_181
    node_53 --> node_7
    node_444 --> node_924
    node_139 --> node_121
    node_916 --> node_795
    node_570 --> node_33
    node_485 --> node_484
    node_484 --> node_970
    node_459 --> node_483
    node_354 --> node_712
    node_476 --> node_764
    node_898 --> node_897
    node_361 --> node_898
    node_724 --> node_764
    node_527 --> node_458
    node_406 --> node_6
    node_148 --> node_47
    node_204 --> node_990
    node_762 --> node_173
    node_406 --> node_1025
    node_87 --> node_872
    node_169 --> node_311
    node_361 --> node_710
    node_451 --> node_1023
    node_795 --> node_797
    node_363 --> node_31
    node_809 --> node_737
    node_184 --> node_278
    node_474 --> node_749
    node_435 --> node_120
    node_362 --> node_821
    node_900 --> node_861
    node_484 --> node_829
    node_809 --> node_1023
    node_939 --> node_194
    node_612 --> node_218
    node_362 --> node_999
    node_991 --> node_892
    node_654 --> node_187
    node_462 --> node_746
    node_169 --> node_175
    node_361 --> node_458
    node_756 --> node_975
    node_169 --> node_227
    node_362 --> node_827
    node_916 --> node_810
    node_915 --> node_173
    node_29 --> node_592
    node_618 --> node_963
    node_6 --> node_247
    node_151 --> node_54
    node_84 --> node_698
    node_354 --> node_774
    node_353 --> node_447
    node_475 --> node_746
    node_1013 --> node_877
    node_14 --> node_640
    node_88 --> node_706
    node_1005 --> node_918
    node_6 --> node_187
    node_141 --> node_105
    node_6 --> node_169
    node_916 --> node_847
    node_385 --> node_826
    node_385 --> node_450
    node_11 --> node_482
    node_184 --> node_289
    node_107 --> node_117
    node_385 --> node_807
    node_49 --> node_485
    node_572 --> node_265
    node_354 --> node_169
    node_435 --> node_691
    node_406 --> node_676
    node_680 --> node_796
    node_528 --> node_848
    node_809 --> node_912
    node_292 --> node_188
    node_1013 --> node_1000
    node_361 --> node_944
    node_29 --> node_257
    node_127 --> node_763
    node_307 --> node_175
    node_112 --> node_43
    node_91 --> node_128
    node_916 --> node_844
    node_361 --> node_489
    node_385 --> node_809
    node_361 --> node_717
    node_781 --> node_782
    node_6 --> node_179
    node_484 --> node_908
    node_164 --> node_271
    node_809 --> node_921
    node_435 --> node_67
    node_462 --> node_919
    node_354 --> node_883
    node_420 --> node_2
    node_803 --> node_764
    node_14 --> node_960
    node_57 --> node_54
    node_679 --> node_840
    node_581 --> node_412
    node_385 --> node_712
    node_809 --> node_783
    node_485 --> node_473
    node_915 --> node_1021
    node_797 --> node_980
    node_14 --> node_961
    node_6 --> node_1028
    node_636 --> node_28
    node_451 --> node_1013
    node_1013 --> node_924
    node_48 --> node_706
    node_730 --> node_722
    node_2 --> node_163
    node_475 --> node_919
    node_484 --> node_941
    node_389 --> node_167
    node_85 --> node_388
    node_991 --> node_1024
    node_379 --> node_354
    node_171 --> node_191
    node_368 --> node_197
    node_354 --> node_905
    node_679 --> node_834
    node_353 --> node_848
    node_668 --> node_309
    node_361 --> node_500
    node_6 --> node_1006
    node_362 --> node_877
    node_477 --> node_866
    node_361 --> node_806
    node_246 --> node_250
    node_29 --> node_53
    node_521 --> node_169
    node_587 --> node_591
    node_435 --> node_564
    node_451 --> node_986
    node_621 --> node_470
    node_430 --> node_25
    node_552 --> node_563
    node_169 --> node_271
    node_484 --> node_919
    node_70 --> node_68
    node_425 --> node_161
    node_451 --> node_903
    node_29 --> node_520
    node_939 --> node_169
    node_478 --> node_922
    node_362 --> node_1000
    node_242 --> node_246
    node_354 --> node_979
    node_361 --> node_162
    node_91 --> node_118
    node_809 --> node_903
    node_483 --> node_849
    node_385 --> node_30
    node_864 --> node_740
    node_186 --> node_208
    node_388 --> node_359
    node_435 --> node_37
    node_273 --> node_183
    node_163 --> node_757
    node_6 --> node_993
    node_915 --> node_756
    node_809 --> node_802
    node_91 --> node_87
    node_92 --> node_43
    node_809 --> node_1002
    node_484 --> node_947
    node_729 --> node_764
    node_733 --> node_764
    node_385 --> node_247
    node_450 --> node_477
    node_84 --> node_592
    node_848 --> node_197
    node_420 --> node_529
    node_938 --> node_302
    node_425 --> node_163
    node_411 --> node_483
    node_253 --> node_233
    node_385 --> node_187
    node_991 --> node_891
    node_915 --> node_759
    node_385 --> node_169
    node_49 --> node_41
    node_678 --> node_740
    node_406 --> node_37
    node_509 --> node_938
    node_362 --> node_748
    node_11 --> node_475
    node_481 --> node_924
    node_992 --> node_764
    node_223 --> node_227
    node_354 --> node_749
    node_435 --> node_546
    node_48 --> node_539
    node_327 --> node_848
    node_139 --> node_980
    node_915 --> node_842
    node_463 --> node_999
    node_552 --> node_710
    node_620 --> node_166
    node_944 --> node_350
    node_636 --> node_348
    node_702 --> node_705
    node_969 --> node_940
    node_373 --> node_233
    node_1013 --> node_982
    node_43 --> node_116
    node_574 --> node_208
    node_385 --> node_1028
    node_385 --> node_905
    node_671 --> node_798
    node_715 --> node_799
    node_420 --> node_548
    node_406 --> node_540
    node_435 --> node_35
    node_776 --> node_31
    node_159 --> node_54
    node_184 --> node_309
    node_43 --> node_208
    node_345 --> node_967
    node_408 --> node_676
    node_184 --> node_965
    node_385 --> node_1006
    node_91 --> node_692
    node_539 --> node_538
    node_938 --> node_969
    node_14 --> node_585
    node_29 --> node_442
    node_482 --> node_997
    node_84 --> node_53
    node_120 --> node_43
    node_354 --> node_784
    node_488 --> node_983
    node_43 --> node_105
    node_51 --> node_540
    node_354 --> node_42
    node_48 --> node_797
    node_406 --> node_35
    node_636 --> node_581
    node_1013 --> node_910
    node_795 --> node_796
    node_48 --> node_732
    node_687 --> node_681
    node_169 --> node_945
    node_50 --> node_208
    node_991 --> node_753
    node_1013 --> node_920
    node_435 --> node_698
    node_385 --> node_993
    node_370 --> node_66
    node_451 --> node_835
    node_679 --> node_779
    node_494 --> node_293
    node_915 --> node_1009
    node_754 --> node_751
    node_635 --> node_972
    node_328 --> node_848
    node_355 --> node_938
    node_226 --> node_224
    node_842 --> node_825
    node_692 --> node_28
    node_29 --> node_450
    node_613 --> node_951
    node_6 --> node_978
    node_184 --> node_290
    node_29 --> node_807
    node_88 --> node_529
    node_157 --> node_54
    node_243 --> node_252
    node_899 --> node_743
    node_470 --> node_169
    node_6 --> node_970
    node_333 --> node_796
    node_164 --> node_319
    node_385 --> node_513
    node_354 --> node_204
    node_368 --> node_183
    node_915 --> node_1014
    node_362 --> node_593
    node_204 --> node_799
    node_574 --> node_540
    node_484 --> node_825
    node_90 --> node_54
    node_989 --> node_763
    node_54 --> node_55
    node_410 --> node_25
    node_785 --> node_725
    node_85 --> node_496
    node_169 --> node_309
    node_29 --> node_712
    node_43 --> node_540
    node_822 --> node_256
    node_43 --> node_111
    node_636 --> node_666
    node_484 --> node_902
    node_606 --> node_187
    node_484 --> node_830
    node_362 --> node_920
    node_938 --> node_281
    node_361 --> node_33
    node_938 --> node_275
    node_1004 --> node_745
    node_88 --> node_548
    node_130 --> node_520
    node_174 --> node_178
    node_926 --> node_52
    node_822 --> node_191
    node_1013 --> node_736
    node_853 --> node_851
    node_451 --> node_774
    node_481 --> node_920
    node_1013 --> node_880
    node_373 --> node_980
    node_915 --> node_999
    node_230 --> node_764
    node_476 --> node_989
    node_981 --> node_764
    node_353 --> node_2
    node_50 --> node_540
    node_915 --> node_827
    node_667 --> node_307
    node_362 --> node_977
    node_1013 --> node_822
    node_420 --> node_687
    node_451 --> node_899
    node_91 --> node_710
    node_657 --> node_217
    node_916 --> node_853
    node_615 --> node_848
    node_374 --> node_889
    node_364 --> node_602
    node_476 --> node_988
    node_435 --> node_592
    node_916 --> node_886
    node_874 --> node_980
    node_141 --> node_99
    node_484 --> node_799
    node_84 --> node_29
    node_483 --> node_819
    node_6 --> node_746
    node_435 --> node_350
    node_432 --> node_411
    node_109 --> node_57
    node_6 --> node_990
    node_388 --> node_387
    node_676 --> node_586
    node_572 --> node_224
    node_6 --> node_908
    node_18 --> node_592
    node_29 --> node_169
    node_354 --> node_746
    node_204 --> node_167
    node_356 --> node_165
    node_282 --> node_938
    node_362 --> node_736
    node_385 --> node_978
    node_354 --> node_908
    node_648 --> node_528
    node_385 --> node_204
    node_169 --> node_307
    node_1013 --> node_804
    node_484 --> node_862
    node_361 --> node_485
    node_487 --> node_758
    node_52 --> node_102
    node_406 --> node_350
    node_361 --> node_478
    node_361 --> node_451
    node_462 --> node_745
    node_672 --> node_799
    node_362 --> node_822
    node_921 --> node_919
    node_361 --> node_854
    node_944 --> node_940
    node_361 --> node_1004
    node_544 --> node_34
    node_484 --> node_831
    node_795 --> node_798
    node_451 --> node_979
    node_91 --> node_717
    node_572 --> node_222
    node_14 --> node_959
    node_6 --> node_171
    node_361 --> node_11
    node_592 --> node_169
    node_475 --> node_745
    node_487 --> node_786
    node_916 --> node_1013
    node_991 --> node_877
    node_763 --> node_765
    node_687 --> node_684
    node_706 --> node_31
    node_853 --> node_850
    node_435 --> node_53
    node_916 --> node_755
    node_110 --> node_114
    node_88 --> node_563
    node_938 --> node_308
    node_208 --> node_57
    node_991 --> node_1000
    node_113 --> node_58
    node_916 --> node_986
    node_91 --> node_500
    node_448 --> node_160
    node_730 --> node_729
    node_600 --> node_290
    node_1013 --> node_801
    node_361 --> node_1010
    node_420 --> node_0
    node_362 --> node_804
    node_249 --> node_543
    node_1013 --> node_795
    node_679 --> node_746
    node_84 --> node_704
    node_319 --> node_764
    node_88 --> node_687
    node_329 --> node_796
    node_451 --> node_749
    node_18 --> node_520
    node_14 --> node_311
    node_41 --> node_28
    node_354 --> node_836
    node_487 --> node_1023
    node_991 --> node_924
    node_6 --> node_1027
    node_822 --> node_723
    node_91 --> node_162
    node_130 --> node_807
    node_362 --> node_987
    node_462 --> node_921
    node_6 --> node_874
    node_204 --> node_57
    node_164 --> node_953
    node_915 --> node_748
    node_425 --> node_495
    node_448 --> node_813
    node_298 --> node_271
    node_361 --> node_496
    node_127 --> node_939
    node_385 --> node_746
    node_385 --> node_990
    node_784 --> node_789
    node_388 --> node_35
    node_385 --> node_908
    node_518 --> node_764
    node_509 --> node_514
    node_552 --> node_33
    node_52 --> node_123
    node_130 --> node_712
    node_484 --> node_912
    node_118 --> node_395
    node_847 --> node_848
    node_1013 --> node_810
    node_451 --> node_989
    node_362 --> node_801
    node_484 --> node_921
    node_915 --> node_1028
    node_168 --> node_184
    node_169 --> node_974
    node_588 --> node_52
    node_385 --> node_518
    node_362 --> node_795
    node_451 --> node_984
    node_184 --> node_285
    node_391 --> node_447
    node_361 --> node_901
    node_809 --> node_828
    node_242 --> node_251
    node_1018 --> node_1017
    node_53 --> node_41
    node_41 --> node_858
    node_708 --> node_741
    node_915 --> node_1006
    node_809 --> node_984
    node_361 --> node_760
    node_487 --> node_783
    node_795 --> node_763
    node_451 --> node_976
    node_916 --> node_994
    node_930 --> node_764
    node_115 --> node_208
    node_91 --> node_36
    node_391 --> node_57
    node_361 --> node_754
    node_809 --> node_976
    node_41 --> node_1018
    node_48 --> node_710
    node_451 --> node_911
    node_878 --> node_876
    node_387 --> node_163
    node_477 --> node_925
    node_64 --> node_248
    node_336 --> node_305
    node_363 --> node_25
    node_448 --> node_823
    node_380 --> node_955
    node_179 --> node_314
    node_915 --> node_993
    node_6 --> node_750
    node_484 --> node_841
    node_916 --> node_863
    node_362 --> node_810
    node_435 --> node_29
    node_991 --> node_982
    node_363 --> node_208
    node_1013 --> node_775
    node_49 --> node_348
    node_743 --> node_744
    node_809 --> node_873
    node_137 --> node_28
    node_385 --> node_1027
    node_570 --> node_348
    node_486 --> node_840
    node_822 --> node_848
    node_385 --> node_598
    node_916 --> node_835
    node_483 --> node_823
    node_362 --> node_847
    node_385 --> node_874
    node_636 --> node_471
    node_355 --> node_514
    node_57 --> node_58
    node_112 --> node_57
    node_242 --> node_833
    node_11 --> node_491
    node_486 --> node_834
    node_915 --> node_593
    node_29 --> node_384
    node_64 --> node_542
    node_505 --> node_763
    node_6 --> node_846
    node_29 --> node_204
    node_362 --> node_844
    node_18 --> node_807
    node_991 --> node_910
    node_791 --> node_797
    node_480 --> node_738
    node_87 --> node_868
    node_48 --> node_717
    node_354 --> node_830
    node_637 --> node_972
    node_107 --> node_183
    node_49 --> node_581
    node_698 --> node_701
    node_91 --> node_90
    node_570 --> node_581
    node_714 --> node_725
    node_991 --> node_920
    node_435 --> node_83
    node_484 --> node_773
    node_847 --> node_939
    node_6 --> node_791
    node_354 --> node_781
    node_85 --> node_529
    node_687 --> node_683
    node_474 --> node_805
    node_18 --> node_712
    node_641 --> node_11
    node_89 --> node_373
    node_776 --> node_6
    node_145 --> node_54
    node_1017 --> node_764
    node_420 --> node_501
    node_715 --> node_797
    node_915 --> node_977
    node_484 --> node_900
    node_164 --> node_302
    node_848 --> node_764
    node_916 --> node_774
    node_361 --> node_448
    node_363 --> node_540
    node_805 --> node_764
    node_354 --> node_388
    node_483 --> node_982
    node_425 --> node_470
    node_354 --> node_432
    node_48 --> node_162
    node_354 --> node_799
    node_385 --> node_750
    node_916 --> node_899
    node_518 --> node_169
    node_809 --> node_898
    node_385 --> node_412
    node_488 --> node_163
    node_35 --> node_149
    node_85 --> node_548
    node_938 --> node_197
    node_6 --> node_887
    node_14 --> node_956
    node_916 --> node_883
    node_354 --> node_887
    node_372 --> node_197
    node_49 --> node_666
    node_385 --> node_246
    node_915 --> node_978
    node_444 --> node_922
    node_570 --> node_666
    node_361 --> node_468
    node_991 --> node_736
    node_84 --> node_692
    node_14 --> node_182
    node_1002 --> node_1001
    node_184 --> node_973
    node_361 --> node_991
    node_345 --> node_309
    node_435 --> node_693
    node_354 --> node_862
    node_989 --> node_939
    node_991 --> node_880
    node_348 --> node_797
    node_411 --> node_478
    node_435 --> node_66
    node_169 --> node_963
    node_473 --> node_743
    node_859 --> node_42
    node_476 --> node_763
    node_916 --> node_905
    node_385 --> node_846
    node_432 --> node_437
    node_378 --> node_167
    node_991 --> node_822
    node_87 --> node_1018
    node_364 --> node_35
    node_354 --> node_762
    node_354 --> node_831
    node_797 --> node_183
    node_436 --> node_25
    node_411 --> node_11
    node_985 --> node_983
    node_354 --> node_266
    node_373 --> node_499
    node_328 --> node_796
    node_822 --> node_815
    node_677 --> node_920
    node_1023 --> node_173
    node_90 --> node_57
    node_451 --> node_944
    node_91 --> node_485
    node_388 --> node_381
    node_204 --> node_797
    node_916 --> node_979
    node_185 --> node_940
    node_385 --> node_791
    node_451 --> node_836
    node_385 --> node_949
    node_169 --> node_236
    node_484 --> node_833
    node_354 --> node_745
    node_283 --> node_212
    node_300 --> node_848
    node_6 --> node_737
    node_6 --> node_167
    node_809 --> node_985
    node_614 --> node_292
    node_362 --> node_916
    node_6 --> node_1023
    node_361 --> node_864
    node_314 --> node_848
    node_859 --> node_856
    node_501 --> node_508
    node_354 --> node_737
    node_631 --> node_516
    node_169 --> node_184
    node_354 --> node_441
    node_991 --> node_804
    node_349 --> node_197
    node_385 --> node_432
    node_450 --> node_486
    node_385 --> node_799
    node_484 --> node_794
    node_915 --> node_987
    node_14 --> node_618
    node_659 --> node_268
    node_14 --> node_319
    node_385 --> node_449
    node_822 --> node_715
    node_655 --> node_169
    node_916 --> node_749
    node_14 --> node_611
    node_698 --> node_702
    node_169 --> node_973
    node_355 --> node_187
    node_380 --> node_292
    node_756 --> node_976
    node_385 --> node_887
    node_809 --> node_806
    node_385 --> node_730
    node_386 --> node_183
    node_915 --> node_990
    node_184 --> node_265
    node_6 --> node_912
    node_90 --> node_58
    node_130 --> node_204
    node_483 --> node_880
    node_904 --> node_907
    node_354 --> node_912
    node_379 --> node_763
    node_484 --> node_797
    node_6 --> node_921
    node_410 --> node_450
    node_574 --> node_169
    node_1013 --> node_756
    node_617 --> node_262
    node_91 --> node_496
    node_85 --> node_687
    node_354 --> node_921
    node_89 --> node_49
    node_6 --> node_783
    node_226 --> node_206
    node_991 --> node_801
    node_636 --> node_1011
    node_939 --> node_167
    node_52 --> node_104
    node_991 --> node_795
    node_478 --> node_919
    node_354 --> node_783
    node_1013 --> node_886
    node_414 --> node_296
    node_361 --> node_445
    node_709 --> node_160
    node_847 --> node_849
    node_916 --> node_989
    node_745 --> node_743
    node_485 --> node_482
    node_132 --> node_129
    node_385 --> node_18
    node_155 --> node_54
    node_916 --> node_784
    node_130 --> node_43
    node_6 --> node_57
    node_169 --> node_292
    node_550 --> node_553
    node_708 --> node_744
    node_48 --> node_33
    node_226 --> node_194
    node_944 --> node_941
    node_587 --> node_169
    node_385 --> node_737
    node_6 --> node_903
    node_406 --> node_515
    node_6 --> node_296
    node_47 --> node_183
    node_385 --> node_1023
    node_515 --> node_169
    node_385 --> node_441
    node_33 --> node_32
    node_370 --> node_248
    node_631 --> node_169
    node_435 --> node_42
    node_354 --> node_841
    node_6 --> node_802
    node_916 --> node_911
    node_776 --> node_35
    node_481 --> node_922
    node_991 --> node_810
    node_6 --> node_1002
    node_362 --> node_853
    node_653 --> node_897
    node_354 --> node_848
    node_474 --> node_163
    node_49 --> node_373
    node_361 --> node_465
    node_915 --> node_1027
    node_354 --> node_802
    node_361 --> node_1024
    node_915 --> node_847
    node_915 --> node_874
    node_679 --> node_921
    node_485 --> node_478
    node_939 --> node_190
    node_435 --> node_692
    node_100 --> node_394
    node_184 --> node_948
    node_1013 --> node_755
    node_282 --> node_187
    node_698 --> node_705
    node_385 --> node_912
    node_37 --> node_799
    node_370 --> node_542
    node_822 --> node_849
    node_636 --> node_120
    node_451 --> node_781
    node_678 --> node_741
    node_775 --> node_773
    node_762 --> node_37
    node_410 --> node_169
    node_570 --> node_313
    node_666 --> node_796
    node_385 --> node_921
    node_84 --> node_500
    node_432 --> node_420
    node_1013 --> node_1009
    node_842 --> node_828
    node_99 --> node_395
    node_385 --> node_447
    node_451 --> node_734
    node_385 --> node_783
    node_494 --> node_956
    node_521 --> node_848
    node_48 --> node_485
    node_795 --> node_939
    node_18 --> node_204
    node_694 --> node_31
    node_221 --> node_191
    node_991 --> node_775
    node_494 --> node_163
    node_136 --> node_57
    node_483 --> node_881
    node_476 --> node_765
    node_410 --> node_487
    node_485 --> node_475
    node_915 --> node_37
    node_367 --> node_723
    node_121 --> node_129
    node_484 --> node_966
    node_362 --> node_1013
    node_468 --> node_160
    node_484 --> node_828
    node_361 --> node_581
    node_636 --> node_691
    node_385 --> node_57
    node_14 --> node_665
    node_1013 --> node_904
    node_484 --> node_884
    node_373 --> node_183
    node_89 --> node_43
    node_204 --> node_796
    node_14 --> node_953
    node_52 --> node_107
    node_49 --> node_471
    node_479 --> node_835
    node_636 --> node_67
    node_809 --> node_915
    node_362 --> node_986
    node_385 --> node_903
    node_354 --> node_706
    node_164 --> node_968
    node_915 --> node_750
    node_468 --> node_813
    node_29 --> node_432
    node_385 --> node_12
    node_916 --> node_746
    node_809 --> node_998
    node_205 --> node_940
    node_385 --> node_802
    node_438 --> node_832
    node_829 --> node_832
    node_169 --> node_948
    node_385 --> node_1002
    node_220 --> node_972
    node_140 --> node_43
    node_809 --> node_875
    node_760 --> node_42
    node_1013 --> node_994
    node_571 --> node_848
    node_505 --> node_939
    node_895 --> node_894
    node_566 --> node_848
    node_679 --> node_782
    node_343 --> node_796
    node_274 --> node_967
    node_169 --> node_968
    node_517 --> node_169
    node_915 --> node_846
    node_666 --> node_641
    node_451 --> node_745
    node_86 --> node_394
    node_248 --> node_66
    node_57 --> node_217
    node_391 --> node_796
    node_62 --> node_54
    node_184 --> node_43
    node_484 --> node_796
    node_1013 --> node_826
    node_1013 --> node_863
    node_171 --> node_172
    node_448 --> node_812
    node_479 --> node_838
    node_361 --> node_753
    node_915 --> node_791
    node_666 --> node_961
    node_679 --> node_742
    node_899 --> node_740
    node_1013 --> node_809
    node_809 --> node_780
    node_630 --> node_213
    node_362 --> node_994
    node_43 --> node_101
    node_491 --> node_751
    node_468 --> node_823
    node_187 --> node_224
    node_916 --> node_836
    node_636 --> node_546
    node_451 --> node_1004
    node_544 --> node_0
    node_29 --> node_167
    node_809 --> node_895
    node_340 --> node_938
    node_451 --> node_805
    node_698 --> node_694
    node_29 --> node_441
    node_202 --> node_191
    node_809 --> node_854
    node_552 --> node_348
    node_692 --> node_120
    node_37 --> node_57
    node_379 --> node_848
    node_84 --> node_388
    node_362 --> node_863
    node_828 --> node_764
    node_762 --> node_761
    node_571 --> node_165
    node_6 --> node_797
    node_203 --> node_206
    node_487 --> node_785
    node_555 --> node_2
    node_362 --> node_835
    node_715 --> node_813
    node_451 --> node_1010
    node_184 --> node_322
    node_354 --> node_2
    node_361 --> node_821
    node_435 --> node_500
    node_809 --> node_1010
    node_692 --> node_691
    node_361 --> node_999
    node_386 --> node_442
    node_822 --> node_233
    node_87 --> node_140
    node_474 --> node_803
    node_361 --> node_827
    node_373 --> node_257
    node_361 --> node_31
    node_636 --> node_698
    node_29 --> node_447
    node_14 --> node_302
    node_692 --> node_67
    node_471 --> node_463
    node_91 --> node_529
    node_218 --> node_217
    node_385 --> node_833
    node_520 --> node_509
    node_431 --> node_248
    node_853 --> node_852
    node_385 --> node_539
    node_184 --> node_947
    node_361 --> node_470
    node_130 --> node_698
    node_715 --> node_763
    node_363 --> node_247
    node_983 --> node_764
    node_521 --> node_2
    node_915 --> node_1023
    node_363 --> node_169
    node_6 --> node_517
    node_1013 --> node_1028
    node_130 --> node_432
    node_484 --> node_958
    node_1013 --> node_905
    node_794 --> node_764
    node_385 --> node_794
    node_900 --> node_742
    node_991 --> node_756
    node_246 --> node_252
    node_362 --> node_774
    node_529 --> node_523
    node_484 --> node_950
    node_14 --> node_643
    node_41 --> node_43
    node_14 --> node_195
    node_991 --> node_853
    node_809 --> node_901
    node_431 --> node_542
    node_91 --> node_548
    node_714 --> node_923
    node_130 --> node_730
    node_487 --> node_787
    node_552 --> node_666
    node_991 --> node_886
    node_362 --> node_899
    node_354 --> node_892
    node_49 --> node_1011
    node_89 --> node_540
    node_809 --> node_760
    node_432 --> node_397
    node_570 --> node_1011
    node_797 --> node_169
    node_361 --> node_462
    node_1006 --> node_163
    node_385 --> node_674
    node_361 --> node_877
    node_1004 --> node_743
    node_379 --> node_939
    node_207 --> node_208
    node_385 --> node_797
    node_362 --> node_883
    node_435 --> node_36
    node_809 --> node_754
    node_697 --> node_695
    node_348 --> node_763
    node_478 --> node_921
    node_87 --> node_130
    node_620 --> node_297
    node_385 --> node_732
    node_484 --> node_1020
    node_916 --> node_830
    node_52 --> node_117
    node_169 --> node_946
    node_361 --> node_1000
    node_678 --> node_744
    node_6 --> node_410
    node_169 --> node_222
    node_501 --> node_504
    node_273 --> node_799
    node_592 --> node_848
    node_291 --> node_2
    node_435 --> node_422
    node_916 --> node_781
    node_362 --> node_905
    node_601 --> node_285
    node_443 --> node_160
    node_130 --> node_18
    node_487 --> node_160
    node_6 --> node_828
    node_484 --> node_969
    node_91 --> node_129
    node_361 --> node_924
    node_916 --> node_734
    node_6 --> node_984
    node_354 --> node_828
    node_39 --> node_43
    node_872 --> node_764
    node_432 --> node_422
    node_432 --> node_415
    node_630 --> node_240
    node_354 --> node_884
    node_253 --> node_442
    node_406 --> node_422
    node_362 --> node_979
    node_361 --> node_748
    node_11 --> node_486
    node_6 --> node_976
    node_130 --> node_441
    node_939 --> node_849
    node_991 --> node_755
    node_329 --> node_938
    node_41 --> node_120
    node_385 --> node_463
    node_915 --> node_986
    node_915 --> node_903
    node_473 --> node_739
    node_169 --> node_238
    node_184 --> node_320
    node_90 --> node_38
    node_29 --> node_706
    node_91 --> node_581
    node_84 --> node_496
    node_762 --> node_764
    node_14 --> node_270
    node_462 --> node_743
    node_435 --> node_388
    node_484 --> node_943
    node_916 --> node_887
    node_991 --> node_1009
    node_310 --> node_190
    node_915 --> node_1002
    node_373 --> node_442
    node_361 --> node_471
    node_935 --> node_929
    node_6 --> node_873
    node_137 --> node_43
    node_431 --> node_436
    node_916 --> node_862
    node_475 --> node_924
    node_475 --> node_743
    node_654 --> node_796
    node_420 --> node_592
    node_432 --> node_417
    node_709 --> node_161
    node_362 --> node_749
    node_435 --> node_248
    node_18 --> node_432
    node_41 --> node_691
    node_451 --> node_163
    node_636 --> node_53
    node_91 --> node_121
    node_916 --> node_762
    node_864 --> node_742
    node_916 --> node_831
    node_991 --> node_904
    node_6 --> node_796
    node_870 --> node_764
    node_91 --> node_687
    node_822 --> node_731
    node_41 --> node_67
    node_354 --> node_891
    node_944 --> node_848
    node_155 --> node_58
    node_18 --> node_730
    node_14 --> node_216
    node_484 --> node_967
    node_184 --> node_949
    node_528 --> node_938
    node_702 --> node_695
    node_6 --> node_217
    node_916 --> node_745
    node_354 --> node_563
    node_501 --> node_502
    node_435 --> node_542
    node_1013 --> node_978
    node_385 --> node_828
    node_362 --> node_989
    node_372 --> node_169
    node_916 --> node_737
    node_169 --> node_540
    node_624 --> node_950
    node_809 --> node_893
    node_362 --> node_784
    node_385 --> node_984
    node_813 --> node_42
    node_29 --> node_539
    node_48 --> node_173
    node_991 --> node_994
    node_223 --> node_222
    node_52 --> node_114
    node_431 --> node_123
    node_809 --> node_991
    node_567 --> node_849
    node_187 --> node_188
    node_353 --> node_938
    node_657 --> node_218
    node_385 --> node_976
    node_676 --> node_728
    node_368 --> node_799
    node_554 --> node_2
    node_137 --> node_120
    node_420 --> node_520
    node_640 --> node_308
    node_61 --> node_54
    node_361 --> node_910
    node_916 --> node_1004
    node_410 --> node_488
    node_88 --> node_348
    node_916 --> node_805
    node_84 --> node_706
    node_6 --> node_898
    node_939 --> node_796
    node_991 --> node_826
    node_991 --> node_863
    node_362 --> node_911
    node_663 --> node_958
    node_359 --> node_28
    node_361 --> node_920
    node_18 --> node_441
    node_115 --> node_43
    node_385 --> node_873
    node_635 --> node_319
    node_915 --> node_835
    node_666 --> node_311
    node_547 --> node_557
    node_451 --> node_864
    node_169 --> node_196
    node_165 --> node_296
    node_991 --> node_809
    node_575 --> node_197
    node_435 --> node_11
    node_809 --> node_864
    node_29 --> node_732
    node_916 --> node_783
    node_137 --> node_691
    node_448 --> node_821
    node_127 --> node_1025
    node_432 --> node_451
    node_11 --> node_479
    node_344 --> node_313
    node_385 --> node_796
    node_349 --> node_169
    node_316 --> node_971
    node_184 --> node_268
    node_48 --> node_348
    node_548 --> node_547
    node_99 --> node_118
    node_49 --> node_546
    node_625 --> node_495
    node_137 --> node_67
    node_479 --> node_836
    node_877 --> node_878
    node_570 --> node_546
    node_179 --> node_184
    node_432 --> node_11
    node_435 --> node_34
    node_1013 --> node_746
    node_636 --> node_29
    node_327 --> node_938
    node_690 --> node_689
    node_184 --> node_167
    node_491 --> node_754
    node_944 --> node_939
    node_1013 --> node_908
    node_968 --> node_24
    node_420 --> node_508
    node_184 --> node_287
    node_127 --> node_207
    node_14 --> node_968
    node_139 --> node_42
    node_252 --> node_764
    node_368 --> node_167
    node_916 --> node_841
    node_356 --> node_208
    node_461 --> node_160
    node_6 --> node_985
    node_88 --> node_99
    node_451 --> node_892
    node_41 --> node_866
    node_361 --> node_736
    node_35 --> node_155
    node_354 --> node_985
    node_48 --> node_581
    node_254 --> node_233
    node_518 --> node_848
    node_435 --> node_496
    node_311 --> node_52
    node_432 --> node_436
    node_274 --> node_309
    node_795 --> node_980
    node_730 --> node_726
    node_500 --> node_498
    node_361 --> node_822
    node_164 --> node_310
    node_915 --> node_899
    node_422 --> node_723
    node_88 --> node_520
    node_85 --> node_208
    node_385 --> node_898
    node_636 --> node_83
    node_6 --> node_806
    node_487 --> node_757
    node_624 --> node_275
    node_49 --> node_698
    node_698 --> node_700
    node_915 --> node_797
    node_570 --> node_698
    node_385 --> node_512
    node_385 --> node_710
    node_433 --> node_396
    node_354 --> node_806
    node_186 --> node_57
    node_422 --> node_11
    node_6 --> node_160
    node_370 --> node_217
    node_328 --> node_938
    node_385 --> node_641
    node_420 --> node_807
    node_406 --> node_848
    node_468 --> node_812
    node_169 --> node_310
    node_611 --> node_967
    node_874 --> node_979
    node_625 --> node_514
    node_11 --> node_474
    node_636 --> node_704
    node_861 --> node_764
    node_991 --> node_1028
    node_991 --> node_905
    node_451 --> node_1024
    node_228 --> node_224
    node_1013 --> node_1027
    node_425 --> node_494
    node_361 --> node_804
    node_91 --> node_373
    node_7 --> node_764
    node_456 --> node_764
    node_470 --> node_796
    node_48 --> node_666
    node_53 --> node_43
    node_164 --> node_951
    node_432 --> node_123
    node_809 --> node_1021
    node_570 --> node_730
    node_809 --> node_1024
    node_822 --> node_175
    node_671 --> node_776
    node_341 --> node_848
    node_130 --> node_539
    node_130 --> node_704
    node_169 --> node_279
    node_43 --> node_102
    node_420 --> node_712
    node_184 --> node_296
    node_699 --> node_696
    node_223 --> node_225
    node_354 --> node_813
    node_481 --> node_919
    node_906 --> node_208
    node_6 --> node_510
    node_573 --> node_940
    node_362 --> node_944
    node_385 --> node_985
    node_41 --> node_137
    node_462 --> node_918
    node_385 --> node_717
    node_164 --> node_304
    node_592 --> node_586
    node_362 --> node_836
    node_649 --> node_848
    node_340 --> node_187
    node_574 --> node_57
    node_169 --> node_951
    node_745 --> node_740
    node_655 --> node_848
    node_184 --> node_301
    node_435 --> node_706
    node_385 --> node_725
    node_889 --> node_52
    node_361 --> node_801
    node_435 --> node_50
    node_43 --> node_57
    node_621 --> node_458
    node_529 --> node_524
    node_361 --> node_795
    node_451 --> node_891
    node_847 --> node_207
    node_47 --> node_43
    node_6 --> node_763
    node_18 --> node_706
    node_679 --> node_160
    node_84 --> node_529
    node_484 --> node_901
    node_348 --> node_939
    node_130 --> node_732
    node_847 --> node_197
    node_385 --> node_806
    node_745 --> node_861
    node_484 --> node_918
    node_552 --> node_556
    node_169 --> node_304
    node_1023 --> node_37
    node_642 --> node_305
    node_91 --> node_471
    node_354 --> node_743
    node_435 --> node_939
    node_479 --> node_734
    node_1013 --> node_750
    node_50 --> node_57
    node_138 --> node_373
    node_385 --> node_162
    node_385 --> node_160
    node_491 --> node_752
    node_187 --> node_194
    node_351 --> node_217
    node_29 --> node_796
    node_822 --> node_499
    node_88 --> node_807
    node_809 --> node_842
    node_14 --> node_197
    node_354 --> node_823
    node_483 --> node_1006
    node_989 --> node_1025
    node_52 --> node_208
    node_361 --> node_810
    node_200 --> node_193
    node_325 --> node_169
    node_406 --> node_939
    node_915 --> node_989
    node_53 --> node_89
    node_906 --> node_540
    node_84 --> node_548
    node_484 --> node_1016
    node_29 --> node_563
    node_177 --> node_169
    node_915 --> node_984
    node_514 --> node_517
    node_14 --> node_946
    node_709 --> node_842
    node_52 --> node_105
    node_118 --> node_436
    node_361 --> node_847
    node_1013 --> node_846
    node_88 --> node_712
    node_692 --> node_83
    node_915 --> node_976
    node_29 --> node_7
    node_361 --> node_391
    node_6 --> node_915
    node_196 --> node_188
    node_406 --> node_163
    node_353 --> node_514
    node_49 --> node_53
    node_392 --> node_52
    node_451 --> node_753
    node_361 --> node_844
    node_822 --> node_197
    node_483 --> node_735
    node_18 --> node_539
    node_570 --> node_53
    node_354 --> node_915
    node_915 --> node_911
    node_107 --> node_799
    node_552 --> node_1011
    node_1013 --> node_791
    node_6 --> node_998
    node_18 --> node_394
    node_915 --> node_873
    node_354 --> node_998
    node_487 --> node_161
    node_991 --> node_978
    node_368 --> node_213
    node_613 --> node_277
    node_354 --> node_33
    node_91 --> node_49
    node_385 --> node_763
    node_666 --> node_938
    node_354 --> node_875
    node_385 --> node_415
    node_29 --> node_710
    node_354 --> node_982
    node_455 --> node_895
    node_791 --> node_173
    node_127 --> node_349
    node_437 --> node_25
    node_435 --> node_2
    node_118 --> node_123
    node_411 --> node_481
    node_362 --> node_830
    node_164 --> node_972
    node_311 --> node_197
    node_317 --> node_166
    node_410 --> node_484
    node_637 --> node_220
    node_809 --> node_1014
    node_1013 --> node_887
    node_187 --> node_66
    node_527 --> node_425
    node_362 --> node_781
    node_596 --> node_281
    node_637 --> node_319
    node_907 --> node_906
    node_484 --> node_945
    node_18 --> node_732
    node_354 --> node_917
    node_169 --> node_940
    node_432 --> node_2
    node_708 --> node_745
    node_822 --> node_208
    node_1013 --> node_862
    node_474 --> node_804
    node_204 --> node_938
    node_6 --> node_245
    node_6 --> node_780
    node_1004 --> node_739
    node_444 --> node_921
    node_85 --> node_592
    node_714 --> node_924
    node_84 --> node_563
    node_362 --> node_734
    node_482 --> node_781
    node_636 --> node_692
    node_484 --> node_957
    node_385 --> node_417
    node_6 --> node_370
    node_354 --> node_780
    node_1013 --> node_762
    node_169 --> node_972
    node_602 --> node_969
    node_580 --> node_191
    node_915 --> node_913
    node_809 --> node_821
    node_221 --> node_958
    node_361 --> node_425
    node_14 --> node_599
    node_809 --> node_999
    node_639 --> node_261
    node_84 --> node_687
    node_916 --> node_892
    node_385 --> node_915
    node_84 --> node_109
    node_131 --> node_373
    node_6 --> node_854
    node_587 --> node_213
    node_354 --> node_895
    node_809 --> node_827
    node_797 --> node_799
    node_487 --> node_991
    node_14 --> node_284
    node_14 --> node_540
    node_915 --> node_898
    node_354 --> node_854
    node_91 --> node_110
    node_138 --> node_49
    node_991 --> node_746
    node_385 --> node_998
    node_358 --> node_221
    node_435 --> node_529
    node_347 --> node_219
    node_410 --> node_476
    node_127 --> node_350
    node_11 --> node_484
    node_343 --> node_938
    node_514 --> node_796
    node_385 --> node_33
    node_991 --> node_908
    node_1013 --> node_737
    node_517 --> node_848
    node_49 --> node_29
    node_362 --> node_862
    node_184 --> node_291
    node_48 --> node_471
    node_385 --> node_875
    node_503 --> node_2
    node_570 --> node_29
    node_935 --> node_930
    node_379 --> node_731
    node_169 --> node_263
    node_622 --> node_294
    node_391 --> node_938
    node_484 --> node_938
    node_935 --> node_926
    node_822 --> node_174
    node_361 --> node_916
    node_362 --> node_762
    node_362 --> node_831
    node_482 --> node_996
    node_163 --> node_764
    node_6 --> node_1010
    node_41 --> node_1019
    node_29 --> node_160
    node_364 --> node_266
    node_939 --> node_942
    node_85 --> node_520
    node_231 --> node_764
    node_679 --> node_780
    node_204 --> node_173
    node_847 --> node_173
    node_916 --> node_884
    node_420 --> node_204
    node_435 --> node_548
    node_451 --> node_877
    node_483 --> node_43
    node_878 --> node_729
    node_41 --> node_83
    node_1013 --> node_912
    node_362 --> node_745
    node_475 --> node_739
    node_150 --> node_54
    node_386 --> node_799
    node_809 --> node_877
    node_484 --> node_907
    node_451 --> node_1000
    node_915 --> node_944
    node_822 --> node_183
    node_1013 --> node_921
    node_385 --> node_780
    node_795 --> node_1025
    node_241 --> node_718
    node_465 --> node_719
    node_127 --> node_792
    node_809 --> node_1000
    node_641 --> node_25
    node_1013 --> node_783
    node_385 --> node_485
    node_385 --> node_895
    node_921 --> node_918
    node_679 --> node_738
    node_451 --> node_924
    node_745 --> node_1028
    node_497 --> node_208
    node_385 --> node_854
    node_6 --> node_901
    node_158 --> node_101
    node_463 --> node_781
    node_480 --> node_741
    node_368 --> node_849
    node_362 --> node_1004
    node_938 --> node_949
    node_49 --> node_704
    node_362 --> node_805
    node_999 --> node_995
    node_354 --> node_901
    node_115 --> node_57
    node_570 --> node_704
    node_11 --> node_473
    node_130 --> node_710
    node_6 --> node_760
    node_184 --> node_277
    node_385 --> node_311
    node_485 --> node_481
    node_202 --> node_958
    node_229 --> node_764
    node_420 --> node_504
    node_468 --> node_821
    node_714 --> node_920
    node_916 --> node_891
    node_1013 --> node_841
    node_809 --> node_748
    node_6 --> node_754
    node_1022 --> node_764
    node_482 --> node_778
    node_501 --> node_838
    node_477 --> node_936
    node_184 --> node_966
    node_47 --> node_799
    node_491 --> node_753
    node_552 --> node_546
    node_666 --> node_495
    node_1013 --> node_802
    node_361 --> node_592
    node_505 --> node_1025
    node_363 --> node_57
    node_1013 --> node_1002
    node_605 --> node_319
    node_385 --> node_1010
    node_423 --> node_170
    node_509 --> node_796
    node_481 --> node_921
    node_989 --> node_349
    node_57 --> node_59
    node_6 --> node_341
    node_354 --> node_1016
    node_677 --> node_919
    node_1004 --> node_740
    node_909 --> node_764
    node_385 --> node_24
    node_361 --> node_853
    node_91 --> node_89
    node_848 --> node_849
    node_604 --> node_955
    node_88 --> node_204
    node_131 --> node_49
    node_435 --> node_563
    node_528 --> node_513
    node_361 --> node_886
    node_631 --> node_517
    node_463 --> node_996
    node_977 --> node_975
    node_43 --> node_104
    node_484 --> node_1021
    node_505 --> node_207
    node_137 --> node_83
    node_380 --> node_962
    node_14 --> node_310
    node_836 --> node_835
    node_438 --> node_671
    node_1023 --> node_1022
    node_130 --> node_717
    node_487 --> node_1024
    node_248 --> node_833
    node_142 --> node_54
    node_362 --> node_841
    node_666 --> node_589
    node_18 --> node_563
    node_879 --> node_43
    node_762 --> node_763
    node_435 --> node_687
    node_636 --> node_500
    node_679 --> node_918
    node_813 --> node_848
    node_85 --> node_807
    node_475 --> node_922
    node_480 --> node_739
    node_991 --> node_750
    node_572 --> node_213
    node_388 --> node_366
    node_704 --> node_699
    node_451 --> node_982
    node_822 --> node_176
    node_354 --> node_881
    node_483 --> node_847
    node_797 --> node_848
    node_169 --> node_189
    node_611 --> node_309
    node_789 --> node_52
    node_552 --> node_698
    node_87 --> node_1019
    node_385 --> node_901
    node_86 --> node_208
    node_361 --> node_53
    node_484 --> node_974
    node_670 --> node_376
    node_915 --> node_763
    node_477 --> node_929
    node_85 --> node_712
    node_842 --> node_759
    node_29 --> node_33
    node_385 --> node_760
    node_485 --> node_486
    node_900 --> node_738
    node_361 --> node_1013
    node_385 --> node_271
    node_657 --> node_222
    node_989 --> node_350
    node_14 --> node_951
    node_580 --> node_848
    node_86 --> node_105
    node_184 --> node_305
    node_373 --> node_799
    node_130 --> node_162
    node_921 --> node_923
    node_991 --> node_846
    node_385 --> node_754
    node_372 --> node_167
    node_462 --> node_740
    node_529 --> node_95
    node_451 --> node_910
    node_361 --> node_755
    node_809 --> node_593
    node_171 --> node_184
    node_552 --> node_730
    node_244 --> node_233
    node_836 --> node_838
    node_391 --> node_495
    node_451 --> node_920
    node_48 --> node_1011
    node_18 --> node_710
    node_702 --> node_696
    node_884 --> node_882
    node_87 --> node_935
    node_354 --> node_1001
    node_482 --> node_782
    node_14 --> node_304
    node_991 --> node_791
    node_574 --> node_796
    node_763 --> node_764
    node_809 --> node_920
    node_463 --> node_778
    node_66 --> node_71
    node_351 --> node_370
    node_6 --> node_893
    node_49 --> node_87
    node_965 --> node_163
    node_6 --> node_991
    node_354 --> node_893
    node_356 --> node_179
    node_671 --> node_832
    node_436 --> node_431
    node_354 --> node_775
    node_354 --> node_991
    node_6 --> node_565
    node_361 --> node_904
    node_435 --> node_0
    node_164 --> node_294
    node_809 --> node_977
    node_48 --> node_1025
    node_656 --> node_973
    node_484 --> node_861
    node_53 --> node_115
    node_989 --> node_792
    node_448 --> node_814
    node_385 --> node_161
    node_131 --> node_43
    node_715 --> node_980
    node_587 --> node_796
    node_991 --> node_887
    node_363 --> node_178
    node_660 --> node_299
    node_349 --> node_167
    node_515 --> node_796
    node_18 --> node_717
    node_483 --> node_800
    node_631 --> node_796
    node_23 --> node_43
    node_451 --> node_736
    node_784 --> node_449
    node_6 --> node_938
    node_991 --> node_862
    node_898 --> node_764
    node_483 --> node_846
    node_615 --> node_169
    node_451 --> node_880
    node_679 --> node_923
    node_435 --> node_31
    node_339 --> node_796
    node_354 --> node_938
    node_678 --> node_745
    node_606 --> node_848
    node_809 --> node_736
    node_6 --> node_864
    node_361 --> node_994
    node_867 --> node_869
    node_184 --> node_960
    node_717 --> node_713
    node_991 --> node_762
    node_991 --> node_831
    node_451 --> node_822
    node_49 --> node_692
    node_139 --> node_113
    node_184 --> node_961
    node_427 --> node_727
    node_6 --> node_357
    node_361 --> node_29
    node_380 --> node_303
    node_915 --> node_914
    node_570 --> node_692
    node_29 --> node_374
    node_982 --> node_981
    node_469 --> node_991
    node_362 --> node_163
    node_446 --> node_875
    node_608 --> node_280
    node_90 --> node_59
    node_809 --> node_822
    node_636 --> node_388
    node_435 --> node_9
    node_282 --> node_796
    node_48 --> node_89
    node_385 --> node_164
    node_864 --> node_738
    node_410 --> node_796
    node_184 --> node_950
    node_361 --> node_826
    node_361 --> node_863
    node_168 --> node_191
    node_361 --> node_807
    node_11 --> node_483
    node_18 --> node_162
    node_571 --> node_208
    node_666 --> node_628
    node_822 --> node_181
    node_887 --> node_885
    node_379 --> node_207
    node_14 --> node_295
    node_991 --> node_737
    node_795 --> node_349
    node_184 --> node_952
    node_385 --> node_893
    node_521 --> node_938
    node_184 --> node_954
    node_832 --> node_66
    node_385 --> node_490
    node_361 --> node_835
    node_552 --> node_53
    node_604 --> node_292
    node_385 --> node_991
    node_451 --> node_804
    node_842 --> node_827
    node_939 --> node_938
    node_463 --> node_782
    node_935 --> node_932
    node_361 --> node_712
    node_994 --> node_992
    node_915 --> node_854
    node_91 --> node_395
    node_809 --> node_804
    node_484 --> node_963
    node_745 --> node_1026
    node_822 --> node_442
    node_915 --> node_1004
    node_482 --> node_1017
    node_915 --> node_805
    node_899 --> node_742
    node_450 --> node_478
    node_668 --> node_967
    node_130 --> node_33
    node_1005 --> node_725
    node_480 --> node_744
    node_916 --> node_743
    node_916 --> node_924
    node_484 --> node_827
    node_762 --> node_765
    node_14 --> node_972
    node_809 --> node_987
    node_969 --> node_197
    node_991 --> node_912
    node_169 --> node_960
    node_420 --> node_432
    node_582 --> node_169
    node_385 --> node_938
    node_437 --> node_450
    node_7 --> node_36
    node_41 --> node_871
    node_391 --> node_470
    node_991 --> node_921
    node_666 --> node_653
    node_388 --> node_352
    node_916 --> node_823
    node_373 --> node_12
    node_385 --> node_864
    node_582 --> node_300
    node_420 --> node_730
    node_451 --> node_801
    node_505 --> node_349
    node_915 --> node_1010
    node_390 --> node_540
    node_991 --> node_783
    node_579 --> node_187
    node_451 --> node_795
    node_822 --> node_194
    node_48 --> node_37
    node_379 --> node_391
    node_361 --> node_774
    node_809 --> node_801
    node_436 --> node_473
    node_795 --> node_350
    node_809 --> node_795
    node_370 --> node_244
    node_6 --> node_1021
    node_745 --> node_1027
    node_6 --> node_1024
    node_169 --> node_952
    node_91 --> node_592
    node_354 --> node_1021
    node_222 --> node_224
    node_361 --> node_899
    node_53 --> node_85
    node_484 --> node_973
    node_124 --> node_127
    node_991 --> node_841
    node_361 --> node_883
    node_795 --> node_722
    node_120 --> node_112
    node_130 --> node_485
    node_944 --> node_175
    node_519 --> node_169
    node_48 --> node_546
    node_468 --> node_822
    node_354 --> node_348
    node_672 --> node_980
    node_417 --> node_411
    node_451 --> node_810
    node_761 --> node_765
    node_916 --> node_998
    node_991 --> node_802
    node_1013 --> node_828
    node_14 --> node_169
    node_991 --> node_1002
    node_362 --> node_892
    node_518 --> node_528
    node_361 --> node_905
    node_478 --> node_918
    node_310 --> node_24
    node_1013 --> node_884
    node_85 --> node_204
    node_916 --> node_875
    node_53 --> node_84
    node_184 --> node_967
    node_916 --> node_982
    node_420 --> node_441
    node_552 --> node_29
    node_88 --> node_698
    node_385 --> node_173
    node_915 --> node_760
    node_184 --> node_297
    node_363 --> node_410
    node_354 --> node_756
    node_505 --> node_350
    node_1013 --> node_976
    node_0 --> node_547
    node_809 --> node_847
    node_86 --> node_99
    node_795 --> node_792
    node_716 --> node_813
    node_915 --> node_754
    node_570 --> node_717
    node_361 --> node_979
    node_324 --> node_212
    node_501 --> node_787
    node_91 --> node_53
    node_187 --> node_248
    node_354 --> node_759
    node_470 --> node_938
    node_900 --> node_864
    node_916 --> node_917
    node_822 --> node_187
    node_18 --> node_33
    node_947 --> node_14
    node_809 --> node_844
    node_636 --> node_496
    node_6 --> node_669
    node_91 --> node_520
    node_88 --> node_730
    node_1013 --> node_873
    node_631 --> node_510
    node_529 --> node_527
    node_49 --> node_500
    node_451 --> node_775
    node_397 --> node_451
    node_48 --> node_698
    node_354 --> node_842
    node_43 --> node_117
    node_570 --> node_500
    node_184 --> node_314
    node_916 --> node_780
    node_366 --> node_495
    node_362 --> node_884
    node_373 --> node_213
    node_385 --> node_1021
    node_385 --> node_1024
    node_822 --> node_179
    node_169 --> node_226
    node_361 --> node_749
    node_762 --> node_939
    node_435 --> node_402
    node_187 --> node_542
    node_916 --> node_895
    node_570 --> node_162
    node_643 --> node_949
    node_603 --> node_301
    node_666 --> node_968
    node_29 --> node_695
    node_385 --> node_348
    node_385 --> node_170
    node_71 --> node_69
    node_354 --> node_520
    node_505 --> node_792
    node_795 --> node_764
    node_88 --> node_18
    node_87 --> node_134
    node_354 --> node_666
    node_41 --> node_867
    node_432 --> node_402
    node_552 --> node_704
    node_680 --> node_169
    node_666 --> node_602
    node_169 --> node_191
    node_356 --> node_171
    node_915 --> node_939
    node_863 --> node_861
    node_455 --> node_894
    node_404 --> node_83
    node_944 --> node_207
    node_102 --> node_54
    node_54 --> node_56
    node_363 --> node_796
    node_459 --> node_487
    node_37 --> node_28
    node_18 --> node_485
    node_88 --> node_441
    node_944 --> node_197
    node_484 --> node_993
    node_361 --> node_784
    node_1013 --> node_1012
    node_354 --> node_1009
    node_385 --> node_581
    node_450 --> node_493
    node_497 --> node_376
    node_758 --> node_757
    node_362 --> node_891
    node_577 --> node_165
    node_29 --> node_938
    node_127 --> node_990
    node_6 --> node_331
    node_466 --> node_791
    node_14 --> node_189
    node_706 --> node_705
    node_14 --> node_60
    node_916 --> node_880
    node_679 --> node_740
    node_379 --> node_349
    node_195 --> node_189
    node_797 --> node_796
    node_479 --> node_837
    node_132 --> node_43
    node_1013 --> node_898
    node_385 --> node_352
    node_177 --> node_848
    node_491 --> node_987
    node_184 --> node_286
    node_714 --> node_922
    node_169 --> node_261
    node_385 --> node_842
    node_184 --> node_282
    node_354 --> node_1014
    node_84 --> node_208
    node_361 --> node_911
    node_91 --> node_29
    node_592 --> node_938
    node_372 --> node_849
    node_388 --> node_373
    node_29 --> node_907
    node_48 --> node_350
    node_444 --> node_160
    node_484 --> node_948
    node_451 --> node_916
    node_361 --> node_464
    node_332 --> node_175
    node_915 --> node_991
    node_6 --> node_821
    node_938 --> node_277
    node_809 --> node_916
    node_715 --> node_1025
    node_91 --> node_807
    node_564 --> node_161
    node_6 --> node_999
    node_385 --> node_666
    node_364 --> node_335
    node_184 --> node_311
    node_52 --> node_43
    node_6 --> node_827
    node_354 --> node_999
    node_43 --> node_114
    node_223 --> node_226
    node_938 --> node_966
    node_300 --> node_169
    node_540 --> node_833
    node_354 --> node_827
    node_420 --> node_706
    node_314 --> node_169
    node_362 --> node_753
    node_361 --> node_452
    node_91 --> node_712
```

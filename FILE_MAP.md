# Codebase File Map

This document maps every file in the repository, their description, and utilization status.

## File List

| File Path | Status | Description |
| --- | --- | --- |
| `.coverage` | 🟢 Referenced | File: .coverage |
| `.djlint.toml` | 🟢 Referenced | File: .djlint.toml |
| `.gitattributes` | 🟢 Referenced | Set the default behavior, in case people don't have core.autocrlf set. |
| `.github/AGENTIC_README.md` | 🟢 Referenced | Agentic Validation Loop Architecture |
| `.github/workflows/auto-merge.yml` | 🟢 Referenced | File: auto-merge.yml |
| `.github/workflows/ci.yml` | 🟢 Referenced | File: ci.yml |
| `.github/workflows/create-issues-from-files.yml` | 🟢 Referenced | File: create-issues-from-files.yml |
| `.github/workflows/jules-queue.yml` | 🟢 Referenced | File: jules-queue.yml |
| `.github/workflows/remote-verify.yml` | 🟢 Referenced | File: remote-verify.yml |
| `.gitignore` | 🟢 Referenced | Ignore all log files |
| `.husky/pre-push` | 🟢 Referenced | File: pre-push |
| `.markdownlint.json` | 🟢 Referenced | File: .markdownlint.json |
| `.opencode/README.md` | 🟢 Referenced | OpenCode Configuration |
| `.opencode/opencode.json` | 🟢 Referenced | File: opencode.json |
| `.yamllint` | 🟢 Referenced | File: .yamllint |
| `=0.9.4` | 🟢 Referenced | File: =0.9.4 |
| `IPV6_AUDIT.md` | 🔵 Entry Point | IPv6 Audit Report |
| `LICENSE` | 🟢 Referenced | File: LICENSE |
| `README.md` | 🟢 Referenced | Distributed Conversational AI Pipeline for Legacy CPU Clusters |
| `TODO.md` | 🟢 Referenced | TODO |
| `YAML_FILES_REPORT.md` | 🔵 Entry Point | Report on YAML Files in Root Directory |
| `agentic_workflow.sh` | 🔵 Entry Point | --- Configuration --- Standardizing on ISSUES directory for task generation |
| `aid_e_log.txt` | 🟢 Referenced | File: aid_e_log.txt |
| `ansible.cfg` | 🟢 Referenced | jinja2_extensions = jinja2.ext.do |
| `ansible/README.md` | 🟢 Referenced | Ansible |
| `ansible/filter_plugins/README.md` | 🟢 Referenced | Ansible Filter Plugins |
| `ansible/filter_plugins/safe_flatten.py` | 🟢 Referenced | File: safe_flatten.py |
| `ansible/jobs/README.md` | 🟢 Referenced | Ansible Jobs |
| `ansible/jobs/benchmark.nomad` | 🟢 Referenced | File: benchmark.nomad |
| `ansible/jobs/evolve-prompt.nomad.j2` | 🟢 Referenced | File: evolve-prompt.nomad.j2 |
| `ansible/jobs/expert-debug.nomad` | 🟢 Referenced | This is a Jinja2 template for a complete, distributed Llama expert. |
| `ansible/jobs/expert.nomad.j2` | 🟢 Referenced | This Nomad job file runs the main "expert" orchestrator service. |
| `ansible/jobs/filebrowser.nomad.j2` | 📄 Template | File: filebrowser.nomad.j2 |
| `ansible/jobs/health-check.nomad.j2` | 🟢 Referenced | File: health-check.nomad.j2 |
| `ansible/jobs/llamacpp-batch.nomad.j2` | 🟢 Referenced | File: llamacpp-batch.nomad.j2 |
| `ansible/jobs/llamacpp-rpc.nomad.j2` | 🟢 Referenced | This Nomad job file creates a pool of llama.cpp rpc-server providers. |
| `ansible/jobs/model-benchmark.nomad.j2` | 🟢 Referenced | File: model-benchmark.nomad.j2 |
| `ansible/jobs/pipecatapp.nomad` | 🟢 Referenced | File: pipecatapp.nomad |
| `ansible/jobs/router.nomad.j2` | 🟢 Referenced | This Nomad job file runs the "router" service. |
| `ansible/jobs/test-runner.nomad.j2` | 🟢 Referenced | File: test-runner.nomad.j2 |
| `ansible/jobs/vllm.nomad.j2` | 📄 Template | File: vllm.nomad.j2 |
| `ansible/lint_nomad.yaml` | 🟢 Referenced | File: lint_nomad.yaml |
| `ansible/paddler_agent/README.md` | 🟢 Referenced | Ansible Role: paddler_agent |
| `ansible/paddler_agent/defaults/main.yaml` | 🟢 Referenced | Defaults for the paddler_agent role |
| `ansible/paddler_agent/tasks/paddler_agent.yaml` | 🔴 Orphan | File: paddler_agent.yaml |
| `ansible/paddler_agent/templates/paddler-agent.service.j2` | 🟢 Referenced | Assuming llama.cpp service is named llama-cpp.service or similar |
| `ansible/paddler_balancer/README.md` | 🟢 Referenced | Ansible Role: paddler_balancer |
| `ansible/paddler_balancer/defaults/main.yaml` | 🟢 Referenced | Defaults for the paddler_balancer role |
| `ansible/paddler_balancer/tasks/paddler_balancer.yaml` | 🔴 Orphan | File: paddler_balancer.yaml |
| `ansible/paddler_balancer/templates/paddler-balancer.service.j2` | 🟢 Referenced | File: paddler-balancer.service.j2 |
| `ansible/roles/README.md` | 🟢 Referenced | Ansible Roles |
| `ansible/roles/benchmark_models/tasks/benchmark_loop.yaml` | 🟢 Referenced | File: benchmark_loop.yaml |
| `ansible/roles/benchmark_models/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/benchmark_models/templates/model-benchmark.nomad.j2` | 🟢 Referenced | This Nomad job file runs a benchmark for a single model. |
| `ansible/roles/bootstrap_agent/defaults/main.yaml` | 🟢 Referenced | No default variables needed for this role. |
| `ansible/roles/bootstrap_agent/tasks/deploy_llama_cpp_model.yaml` | 🟢 Referenced | File: deploy_llama_cpp_model.yaml |
| `ansible/roles/bootstrap_agent/tasks/main.yaml` | 🟢 Referenced | tasks file for bootstrap_agent |
| `ansible/roles/claude_clone/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/common-tools/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/common/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/common/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/common/tasks/network_repair.yaml` | 🟢 Referenced | File: network_repair.yaml |
| `ansible/roles/common/templates/cluster-ip-alias.service.j2` | 🟢 Referenced | File: cluster-ip-alias.service.j2 |
| `ansible/roles/common/templates/hosts.j2` | 🟢 Referenced | File: hosts.j2 |
| `ansible/roles/common/templates/update-ssh-authorized-keys.sh.j2` | 🟢 Referenced | bin/bash |
| `ansible/roles/config_manager/tasks/main.yaml` | 🟢 Referenced | tasks file for ansible/roles/config_manager/tasks/main.yaml |
| `ansible/roles/consul/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/consul/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/consul/tasks/acl.yaml` | 🟢 Referenced | File: acl.yaml |
| `ansible/roles/consul/tasks/main.yaml` | 🟢 Referenced | Task 0: Cleanup previous installation if requested |
| `ansible/roles/consul/tasks/tls.yaml` | 🟢 Referenced | File: tls.yaml |
| `ansible/roles/consul/templates/consul.hcl.j2` | 🟢 Referenced | File: consul.hcl.j2 |
| `ansible/roles/consul/templates/consul.service.j2` | 🟢 Referenced | File: consul.service.j2 |
| `ansible/roles/desktop_extras/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/docker/handlers/main.yaml` | 🟢 Referenced | handlers file for docker |
| `ansible/roles/docker/molecule/default/converge.yml` | 🟢 Referenced | File: converge.yml |
| `ansible/roles/docker/molecule/default/molecule.yml` | 🟢 Referenced | File: molecule.yml |
| `ansible/roles/docker/molecule/default/prepare.yml` | 🟢 Referenced | File: prepare.yml |
| `ansible/roles/docker/molecule/default/verify.yml` | 🟢 Referenced | File: verify.yml |
| `ansible/roles/docker/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/docker/templates/daemon.json.j2` | 🟢 Referenced | File: daemon.json.j2 |
| `ansible/roles/download_models/files/download_hf_repo.py` | 🟢 Referenced | usr/bin/env python3 |
| `ansible/roles/download_models/tasks/main.yaml` | 🟢 Referenced | tasks file for download_models |
| `ansible/roles/exo/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/exo/files/Dockerfile` | 🟢 Referenced | Install system dependencies |
| `ansible/roles/exo/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/exo/templates/exo.nomad.j2` | 🟢 Referenced | File: exo.nomad.j2 |
| `ansible/roles/headscale/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/headscale/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/headscale/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/headscale/templates/config.yaml.j2` | 🟢 Referenced | File: config.yaml.j2 |
| `ansible/roles/headscale/templates/headscale.service.j2` | 🟢 Referenced | File: headscale.service.j2 |
| `ansible/roles/heretic_tool/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/heretic_tool/meta/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/heretic_tool/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/home_assistant/meta/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/home_assistant/meta/main.yml` | 🟢 Referenced | File: main.yml |
| `ansible/roles/home_assistant/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/home_assistant/templates/configuration.yaml.j2` | 🟢 Referenced | Enables the default configuration for Home Assistant |
| `ansible/roles/home_assistant/templates/home_assistant.nomad.j2` | 🟢 Referenced | File: home_assistant.nomad.j2 |
| `ansible/roles/kittentts/tasks/main.yaml` | 🟢 Referenced | This role is deprecated and will be replaced by a Piper TTS implementation. |
| `ansible/roles/librarian/defaults/main.yml` | 🔵 Entry Point | File: main.yml |
| `ansible/roles/librarian/tasks/main.yml` | 🔵 Entry Point | File: main.yml |
| `ansible/roles/librarian/templates/librarian.service.j2` | 🟢 Referenced | File: librarian.service.j2 |
| `ansible/roles/librarian/templates/librarian_agent.py.j2` | 🟢 Referenced | usr/bin/env python3 |
| `ansible/roles/librarian/templates/spacedrive.service.j2` | 🟢 Referenced | File: spacedrive.service.j2 |
| `ansible/roles/llama_cpp/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/llama_cpp/molecule/default/converge.yml` | 🟢 Referenced | File: converge.yml |
| `ansible/roles/llama_cpp/molecule/default/molecule.yml` | 🟢 Referenced | File: molecule.yml |
| `ansible/roles/llama_cpp/molecule/default/verify.yml` | 🟢 Referenced | File: verify.yml |
| `ansible/roles/llama_cpp/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/llama_cpp/tasks/run_single_rpc_job.yaml` | 🟢 Referenced | File: run_single_rpc_job.yaml |
| `ansible/roles/llxprt_code/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/llxprt_code/templates/llxprt-code.env.j2` | 🟢 Referenced | File: llxprt-code.env.j2 |
| `ansible/roles/magic_mirror/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/magic_mirror/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/magic_mirror/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/magic_mirror/templates/magic_mirror.nomad.j2` | 🟢 Referenced | File: magic_mirror.nomad.j2 |
| `ansible/roles/mcp_server/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/mcp_server/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/mcp_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/mcp_server/templates/mcp_server.nomad.j2` | 🟢 Referenced | File: mcp_server.nomad.j2 |
| `ansible/roles/memory_graph/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/memory_graph/templates/memory-graph.nomad.j2` | 🟢 Referenced | File: memory-graph.nomad.j2 |
| `ansible/roles/memory_service/files/app.py` | 🟢 Referenced | File: app.py |
| `ansible/roles/memory_service/files/pmm_memory.py` | 🟢 Referenced | File: pmm_memory.py |
| `ansible/roles/memory_service/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/memory_service/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/memory_service/templates/memory_service.nomad.j2` | 🟢 Referenced | File: memory_service.nomad.j2 |
| `ansible/roles/moe_gateway/files/gateway.py` | 🟢 Referenced | File: gateway.py |
| `ansible/roles/moe_gateway/files/static/index.html` | 🟢 Referenced | File: index.html |
| `ansible/roles/moe_gateway/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/moe_gateway/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/moe_gateway/templates/moe-gateway.nomad.j2` | 🟢 Referenced | File: moe-gateway.nomad.j2 |
| `ansible/roles/monitoring/defaults/main.yml` | 🟢 Referenced | File: main.yml |
| `ansible/roles/monitoring/files/llm_dashboard.json` | 🟢 Referenced | File: llm_dashboard.json |
| `ansible/roles/monitoring/tasks/main.yml` | 🟢 Referenced | File: main.yml |
| `ansible/roles/monitoring/templates/dashboards.yaml.j2` | 🟢 Referenced | File: dashboards.yaml.j2 |
| `ansible/roles/monitoring/templates/datasource.yaml.j2` | 🟢 Referenced | File: datasource.yaml.j2 |
| `ansible/roles/monitoring/templates/grafana.nomad.j2` | 🟢 Referenced | Update stanza for reliability |
| `ansible/roles/monitoring/templates/memory-audit.nomad.j2` | 🟢 Referenced | File: memory-audit.nomad.j2 |
| `ansible/roles/monitoring/templates/mqtt-exporter.nomad.j2` | 🟢 Referenced | Update stanza for reliability |
| `ansible/roles/monitoring/templates/node-exporter.nomad.j2` | 🟢 Referenced | File: node-exporter.nomad.j2 |
| `ansible/roles/monitoring/templates/prometheus.nomad.j2` | 🟢 Referenced | Update stanza for reliability |
| `ansible/roles/monitoring/templates/prometheus.yml.j2` | 🟢 Referenced | File: prometheus.yml.j2 |
| `ansible/roles/mqtt/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/mqtt/meta/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/mqtt/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/mqtt/templates/mqtt.nomad.j2` | 🟢 Referenced | File: mqtt.nomad.j2 |
| `ansible/roles/nanochat/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nanochat/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nanochat/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nanochat/templates/nanochat.nomad.j2` | 🟢 Referenced | File: nanochat.nomad.j2 |
| `ansible/roles/nats/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nats/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nats/templates/nats.nomad.j2` | 🟢 Referenced | File: nats.nomad.j2 |
| `ansible/roles/nfs/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nixos_pxe_server/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nixos_pxe_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nixos_pxe_server/templates/boot.ipxe.nix.j2` | 🟢 Referenced | ipxe |
| `ansible/roles/nixos_pxe_server/templates/configuration.nix.j2` | 🟢 Referenced | etc/nixos/configuration.nix |
| `ansible/roles/nomad/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nomad/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nomad/handlers/restart_nomad_handler_tasks.yaml` | 🟢 Referenced | File: restart_nomad_handler_tasks.yaml |
| `ansible/roles/nomad/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nomad/templates/client.hcl.j2` | 🟢 Referenced | Config generated by Ansible |
| `ansible/roles/nomad/templates/nomad.hcl.server.j2` | 🟢 Referenced | File: nomad.hcl.server.j2 |
| `ansible/roles/nomad/templates/nomad.service.j2` | 🟢 Referenced | File: nomad.service.j2 |
| `ansible/roles/nomad/templates/nomad.sh.j2` | 🟢 Referenced | bin/sh |
| `ansible/roles/nomad/templates/server.hcl.j2` | 🟢 Referenced | Config generated by Ansible |
| `ansible/roles/opencode/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/opencode/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/opencode/templates/opencode.nomad.j2` | 🟢 Referenced | File: opencode.nomad.j2 |
| `ansible/roles/openworkers/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/openworkers/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/openworkers/templates/openworkers-bootstrap.nomad.j2` | 🟢 Referenced | File: openworkers-bootstrap.nomad.j2 |
| `ansible/roles/openworkers/templates/openworkers-infra.nomad.j2` | 🟢 Referenced | Postgate (HTTP proxy for Postgres) |
| `ansible/roles/openworkers/templates/openworkers-runners.nomad.j2` | 🟢 Referenced | File: openworkers-runners.nomad.j2 |
| `ansible/roles/paddler/tasks/main.yaml` | 🟢 Referenced | Note: Choose the libc version appropriate for your systems. |
| `ansible/roles/pipecatapp/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/pipecatapp/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/pipecatapp/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/pipecatapp/templates/archivist.nomad.j2` | 🟢 Referenced | File: archivist.nomad.j2 |
| `ansible/roles/pipecatapp/templates/pipecat.env.j2` | 🟢 Referenced | bin/sh |
| `ansible/roles/pipecatapp/templates/pipecatapp.nomad.j2` | 🟢 Referenced | File: pipecatapp.nomad.j2 |
| `ansible/roles/pipecatapp/templates/prompts/coding_expert.txt.j2` | 🟢 Referenced | File: coding_expert.txt.j2 |
| `ansible/roles/pipecatapp/templates/prompts/creative_expert.txt.j2` | 🟢 Referenced | File: creative_expert.txt.j2 |
| `ansible/roles/pipecatapp/templates/prompts/cynic_expert.txt.j2` | 🟢 Referenced | File: cynic_expert.txt.j2 |
| `ansible/roles/pipecatapp/templates/prompts/router.txt.j2` | 🟢 Referenced | File: router.txt.j2 |
| `ansible/roles/pipecatapp/templates/prompts/tron_agent.txt.j2` | 🟢 Referenced | File: tron_agent.txt.j2 |
| `ansible/roles/pipecatapp/templates/start_pipecatapp.sh.j2` | 🟢 Referenced | bin/bash |
| `ansible/roles/pipecatapp/templates/workflows/default_agent_loop.yaml.j2` | 🟢 Referenced | This workflow defines a single turn of the agent's reasoning loop. |
| `ansible/roles/postgres/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/postgres/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/postgres/templates/postgres.nomad.j2` | 🟢 Referenced | File: postgres.nomad.j2 |
| `ansible/roles/power_manager/defaults/main.yaml` | 🟢 Referenced | defaults file for power_manager |
| `ansible/roles/power_manager/files/power_agent.py` | 🟢 Referenced | Power management agent for sleeping and waking Nomad services. |
| `ansible/roles/power_manager/files/traffic_monitor.c` | 🟢 Referenced | File: traffic_monitor.c |
| `ansible/roles/power_manager/handlers/main.yaml` | 🟢 Referenced | handlers file for power_manager |
| `ansible/roles/power_manager/tasks/main.yaml` | 🟢 Referenced | tasks file for power_manager |
| `ansible/roles/power_manager/templates/power-agent.service.j2` | 🟢 Referenced | File: power-agent.service.j2 |
| `ansible/roles/preflight_checks/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/provisioning_api/files/provisioning_api.py` | 🟢 Referenced | File: provisioning_api.py |
| `ansible/roles/provisioning_api/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/provisioning_api/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/provisioning_api/templates/provisioning-api.service.j2` | 🟢 Referenced | Make it wait for the network and Consul to be ready |
| `ansible/roles/pxe_server/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/pxe_server/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/pxe_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/pxe_server/templates/boot.ipxe.j2` | 🟢 Referenced | ipxe |
| `ansible/roles/pxe_server/templates/dhcpd.conf.j2` | 🟢 Referenced | File: dhcpd.conf.j2 |
| `ansible/roles/pxe_server/templates/preseed.cfg.j2` | 🟢 Referenced | Preconfiguration file for Debian installation |
| `ansible/roles/python_deps/files/requirements.txt` | 🟢 Referenced | File: requirements.txt |
| `ansible/roles/python_deps/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/semantic_router/defaults/main.yaml` | 🟢 Referenced | defaults/main.yaml |
| `ansible/roles/semantic_router/tasks/main.yaml` | 🟢 Referenced | tasks/main.yaml |
| `ansible/roles/semantic_router/templates/Dockerfile.j2` | 🟢 Referenced | Install system dependencies if needed (e.g. for building wheels) |
| `ansible/roles/semantic_router/templates/semantic-router.nomad.j2` | 🟢 Referenced | File: semantic-router.nomad.j2 |
| `ansible/roles/sunshine/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/sunshine/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/sunshine/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/sunshine/templates/sunshine.nomad.j2` | 🟢 Referenced | File: sunshine.nomad.j2 |
| `ansible/roles/system_deps/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/tailscale/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/term_everything/tasks/main.yml` | 🟢 Referenced | File: main.yml |
| `ansible/roles/tool_server/Dockerfile` | 🟢 Referenced | File: Dockerfile |
| `ansible/roles/tool_server/app.py` | 🟢 Referenced | File: app.py |
| `ansible/roles/tool_server/entrypoint.sh` | 🟢 Referenced | bin/bash |
| `ansible/roles/tool_server/pmm_memory.py` | 🟢 Referenced | File: pmm_memory.py |
| `ansible/roles/tool_server/preload_models.py` | 🟢 Referenced | Preload models to ensure they are cached in the Docker image |
| `ansible/roles/tool_server/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/tool_server/templates/tool_server.nomad.j2` | 🟢 Referenced | File: tool_server.nomad.j2 |
| `ansible/roles/tool_server/tools/ansible_tool.py` | 🟢 Referenced | File: ansible_tool.py |
| `ansible/roles/tool_server/tools/archivist_tool.py` | 🟢 Referenced | File: archivist_tool.py |
| `ansible/roles/tool_server/tools/claude_clone_tool.py` | 🟢 Referenced | File: claude_clone_tool.py |
| `ansible/roles/tool_server/tools/code_runner_tool.py` | 🟢 Referenced | File: code_runner_tool.py |
| `ansible/roles/tool_server/tools/council_tool.py` | 🟢 Referenced | File: council_tool.py |
| `ansible/roles/tool_server/tools/desktop_control_tool.py` | 🟢 Referenced | File: desktop_control_tool.py |
| `ansible/roles/tool_server/tools/file_editor_tool.py` | 🟢 Referenced | File: file_editor_tool.py |
| `ansible/roles/tool_server/tools/final_answer_tool.py` | 🟢 Referenced | File: final_answer_tool.py |
| `ansible/roles/tool_server/tools/gemini_cli.py` | 🟢 Referenced | File: gemini_cli.py |
| `ansible/roles/tool_server/tools/get_nomad_job.py` | 🟢 Referenced | File: get_nomad_job.py |
| `ansible/roles/tool_server/tools/git_tool.py` | 🟢 Referenced | File: git_tool.py |
| `ansible/roles/tool_server/tools/ha_tool.py` | 🟢 Referenced | File: ha_tool.py |
| `ansible/roles/tool_server/tools/llxprt_code_tool.py` | 🟢 Referenced | File: llxprt_code_tool.py |
| `ansible/roles/tool_server/tools/mcp_tool.py` | 🟢 Referenced | File: mcp_tool.py |
| `ansible/roles/tool_server/tools/opencode_tool.py` | 🟢 Referenced | File: opencode_tool.py |
| `ansible/roles/tool_server/tools/orchestrator_tool.py` | 🟢 Referenced | File: orchestrator_tool.py |
| `ansible/roles/tool_server/tools/planner_tool.py` | 🟢 Referenced | File: planner_tool.py |
| `ansible/roles/tool_server/tools/power_tool.py` | 🟢 Referenced | File: power_tool.py |
| `ansible/roles/tool_server/tools/project_mapper_tool.py` | 🟢 Referenced | File: project_mapper_tool.py |
| `ansible/roles/tool_server/tools/prompt_improver_tool.py` | 🟢 Referenced | File: prompt_improver_tool.py |
| `ansible/roles/tool_server/tools/rag_tool.py` | 🟢 Referenced | File: rag_tool.py |
| `ansible/roles/tool_server/tools/sandbox.ts` | 🟢 Referenced | sandbox.ts |
| `ansible/roles/tool_server/tools/shell_tool.py` | 🟢 Referenced | File: shell_tool.py |
| `ansible/roles/tool_server/tools/smol_agent_tool.py` | 🟢 Referenced | File: smol_agent_tool.py |
| `ansible/roles/tool_server/tools/ssh_tool.py` | 🟢 Referenced | File: ssh_tool.py |
| `ansible/roles/tool_server/tools/summarizer_tool.py` | 🟢 Referenced | File: summarizer_tool.py |
| `ansible/roles/tool_server/tools/swarm_tool.py` | 🟢 Referenced | File: swarm_tool.py |
| `ansible/roles/tool_server/tools/tap_service.py` | 🟢 Referenced | File: tap_service.py |
| `ansible/roles/tool_server/tools/term_everything_tool.py` | 🟢 Referenced | File: term_everything_tool.py |
| `ansible/roles/tool_server/tools/web_browser_tool.py` | 🟢 Referenced | Mock playwright if it's not available |
| `ansible/roles/unified_fs/defaults/main.yml` | 🟢 Referenced | File: main.yml |
| `ansible/roles/unified_fs/files/unified_fs_agent.py` | 🟢 Referenced | usr/bin/env python3 |
| `ansible/roles/unified_fs/handlers/main.yml` | 🟢 Referenced | File: main.yml |
| `ansible/roles/unified_fs/tasks/main.yml` | 🟢 Referenced | File: main.yml |
| `ansible/roles/unified_fs/templates/unified_fs.service.j2` | 🟢 Referenced | File: unified_fs.service.j2 |
| `ansible/roles/vision/defaults/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/vision/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/vision/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/vision/templates/config.yml.j2` | 🟢 Referenced | File: config.yml.j2 |
| `ansible/roles/vision/templates/vision.nomad.j2` | 🟢 Referenced | File: vision.nomad.j2 |
| `ansible/roles/vllm/tasks/main.yaml` | 🟢 Referenced | tasks file for vllm |
| `ansible/roles/vllm/tasks/run_single_vllm_job.yaml` | 🟢 Referenced | tasks/run_single_vllm_job.yaml |
| `ansible/roles/vllm/templates/vllm-expert.nomad.j2` | 🟢 Referenced | File: vllm-expert.nomad.j2 |
| `ansible/roles/whisper_cpp/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/world_model_service/files/Dockerfile` | 🟢 Referenced | Use an official Python runtime as a parent image |
| `ansible/roles/world_model_service/files/app.py` | 🟢 Referenced | File: app.py |
| `ansible/roles/world_model_service/files/debug_world_model.sh` | 🟢 Referenced | bin/bash |
| `ansible/roles/world_model_service/files/requirements.txt` | 🟢 Referenced | File: requirements.txt |
| `ansible/roles/world_model_service/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/world_model_service/world_model.nomad.j2` | 🟢 Referenced | File: world_model.nomad.j2 |
| `ansible/run_download_models.yaml` | 🟢 Referenced | File: run_download_models.yaml |
| `ansible/tasks/README.md` | 🟢 Referenced | Ansible Tasks |
| `ansible/tasks/build_pipecatapp_image.yaml` | 🟢 Referenced | File: build_pipecatapp_image.yaml |
| `ansible/tasks/create_expert_job.yaml` | 🟢 Referenced | File: create_expert_job.yaml |
| `ansible/tasks/deploy_expert_wrapper.yaml` | 🟢 Referenced | File: deploy_expert_wrapper.yaml |
| `ansible/tasks/deploy_model_gpu_provider.yaml` | 🟢 Referenced | File: deploy_model_gpu_provider.yaml |
| `bootstrap.sh` | 🟢 Referenced | Easy Bootstrap Script for Single-Node Setup  This script simplifies the process of bootstrapping th |
| `check_all_playbooks.sh` | 🟢 Referenced | --- Flexible Ansible Playbook Checker  This script recursively finds all .yaml and .yml files, filte |
| `check_deps.py` | 🟢 Referenced | Write the requirements to a temp file |
| `create_todo_issues.sh` | 🟢 Referenced | bin/bash |
| `debug_expert.sh` | 🔵 Entry Point | bin/bash |
| `distributed-llama-repo/README.md` | 🟢 Referenced | Distributed Llama Repo |
| `docker/README.md` | 🟢 Referenced | Docker |
| `docker/dev_container/Dockerfile` | 🟢 Referenced | Install system dependencies |
| `docker/memory_service/Dockerfile` | 🟢 Referenced | Install dependencies |
| `docs/AGENTS.md` | 🟢 Referenced | AI Agent Architectures |
| `docs/ARCHITECTURE.md` | 🟢 Referenced | Holistic Project Architecture |
| `docs/BENCHMARKING.MD` | 🟢 Referenced | A Guide to Benchmarking Your AI Cluster |
| `docs/DEPLOYMENT_AND_PROFILING.md` | 🟢 Referenced | Deploying and Profiling AI Services |
| `docs/EVALUATION_LLMROUTER.md` | 🟢 Referenced | LLMRouter Evaluation Report |
| `docs/FRONTEND_VERIFICATION.md` | 🟢 Referenced | Frontend Verification Instructions with Playwright |
| `docs/FRONTIER_AGENT_ROADMAP.md` | 📄 Documentation/Asset | Frontier Agent Roadmap |
| `docs/GEMINI.md` | 🟢 Referenced | GEMINI.md |
| `docs/MCP_SERVER_SETUP.md` | 🟢 Referenced | Building an MCP Server with Service Discovery |
| `docs/MEMORIES.md` | 🟢 Referenced | Agent Memories |
| `docs/NETWORK.md` | 🟢 Referenced | Network Architecture |
| `docs/NIXOS_PXE_BOOT_SETUP.md` | 🟢 Referenced | NixOS-based PXE Boot Server Setup |
| `docs/PROJECT_SUMMARY.md` | 🟢 Referenced | Project Summary: Architecting a Responsive, Distributed Conversational AI Pipeline |
| `docs/PXE_BOOT_SETUP.md` | 🟢 Referenced | iPXE Boot Server Setup for Automated Debian Installation |
| `docs/README.md` | 🟢 Referenced | Project Documentation |
| `docs/REFACTOR_PROPOSAL_hybrid_architecture.md` | 🟢 Referenced | Refactoring Proposal: Hybrid / Cluster-Native Architecture |
| `docs/REMOTE_WORKFLOW.md` | 🟢 Referenced | Improving Your Remote Workflow with Mosh and Tmux |
| `docs/TODO_Hybrid_Architecture.md` | 🟢 Referenced | Hybrid Architecture Implementation To-Do List |
| `docs/TOOL_EVALUATION.md` | 🟢 Referenced | Tool Evaluation and Strategic Direction |
| `docs/TROUBLESHOOTING.md` | 🟢 Referenced | Troubleshooting Guide |
| `docs/VLLM_PROJECT_EVALUATION.md` | 🟢 Referenced | vLLM Project Evaluation |
| `docs/heretic_evaluation.md` | 🟢 Referenced | Heretic Repository Evaluation |
| `examples/README.md` | 🟢 Referenced | Examples |
| `examples/chat-persistent.sh` | 🟢 Referenced | bin/bash |
| `generate_issue_script.py` | 🟢 Referenced | File: generate_issue_script.py |
| `group_vars/README.md` | 🟢 Referenced | Ansible Group Variables |
| `group_vars/all.yaml` | 🟢 Referenced | This file contains variables that are common to all hosts in the inventory. |
| `group_vars/external_experts.yaml` | 🟢 Referenced | Configuration for external, third-party LLM experts. |
| `group_vars/models.yaml` | 🟢 Referenced | This file centralizes the configuration for all AI models used in the project. |
| `host_vars/README.md` | 🟢 Referenced | Ansible Host Variables |
| `host_vars/localhost.yaml` | 🟢 Referenced | BEGIN ANSIBLE MANAGED BLOCK |
| `hostfile` | 🟢 Referenced | File: hostfile |
| `initial-setup/README.md` | 🟢 Referenced | Initial Machine Setup |
| `initial-setup/add_new_worker.sh` | 🟢 Referenced | Script to manually provision a new worker node for the cluster. This script automates the process o |
| `initial-setup/modules/01-network.sh` | 🟢 Referenced | bin/bash |
| `initial-setup/modules/02-hostname.sh` | 🟢 Referenced | Ensure CONFIG_FILE is defined (fallback if run standalone) |
| `initial-setup/modules/03-user.sh` | 🟢 Referenced | bin/bash |
| `initial-setup/modules/04-ssh.sh` | 🟢 Referenced | bin/bash |
| `initial-setup/modules/05-auto-provision.sh` | 🟢 Referenced | bin/bash |
| `initial-setup/modules/README.md` | 🟢 Referenced | Initial Setup Modules |
| `initial-setup/setup.conf` | 🟢 Referenced | File: setup.conf |
| `initial-setup/setup.sh` | 🟢 Referenced | Exit immediately if a command exits with a non-zero status. |
| `initial-setup/update_inventory.sh` | 🟢 Referenced | This script dynamically generates the Ansible inventory.yaml file by querying the Consul API for the |
| `initial-setup/worker-setup/README.md` | 🟢 Referenced | Manual Worker Node Setup |
| `initial-setup/worker-setup/setup.sh` | 🟢 Referenced | This script performs the absolute minimal setup required for a new Debian machine to be provisioned |
| `inventory.yaml` | 🟢 Referenced | This inventory is dynamically generated by update_inventory.sh |
| `local_inventory.ini` | 🟢 Referenced | File: local_inventory.ini |
| `package.json` | 🟢 Referenced | File: package.json |
| `pipecat-agent-extension/README.md` | 🟢 Referenced | Pipecat Agent Extension |
| `pipecat-agent-extension/commands/pipecat/send.toml` | 🟢 Referenced | File: send.toml |
| `pipecat-agent-extension/example.ts` | 🟢 Referenced | File: example.ts |
| `pipecat-agent-extension/gemini-extension.json` | 🟢 Referenced | File: gemini-extension.json |
| `pipecat-agent-extension/package.json` | 🟢 Referenced | File: package.json |
| `pipecat-agent-extension/tsconfig.json` | 🟢 Referenced | File: tsconfig.json |
| `pipecatapp/Dockerfile` | 🟢 Referenced | Use an official Python runtime as a parent image |
| `pipecatapp/README.md` | 🟢 Referenced | Docker Pipecat App |
| `pipecatapp/TODO.md` | 🟢 Referenced | VR Mission Control TODO |
| `pipecatapp/__init__.py` | 🟢 Referenced | File: __init__.py |
| `pipecatapp/agent_factory.py` | 🟢 Referenced | File: agent_factory.py |
| `pipecatapp/api_keys.py` | 🟢 Referenced | File: api_keys.py |
| `pipecatapp/app.py` | 🟢 Referenced | Set config dir before importing ultralytics to avoid permission errors |
| `pipecatapp/archivist_service.py` | 🟢 Referenced | File: archivist_service.py |
| `pipecatapp/datasets/sycophancy_prompts.json` | 🟢 Referenced | File: sycophancy_prompts.json |
| `pipecatapp/durable_execution.py` | 🟢 Referenced | File: durable_execution.py |
| `pipecatapp/expert_tracker.py` | 🟢 Referenced | File: expert_tracker.py |
| `pipecatapp/llm_clients.py` | 🟢 Referenced | File: llm_clients.py |
| `pipecatapp/manager_agent.py` | 🟢 Referenced | File: manager_agent.py |
| `pipecatapp/memory.py` | 🟢 Referenced | File: memory.py |
| `pipecatapp/memory_graph_service/Dockerfile` | 🟢 Referenced | Install dependencies |
| `pipecatapp/memory_graph_service/server.py` | 🟢 Referenced | File: server.py |
| `pipecatapp/models.py` | 🟢 Referenced | File: models.py |
| `pipecatapp/moondream_detector.py` | 🟢 Referenced | File: moondream_detector.py |
| `pipecatapp/net_utils.py` | 🟢 Referenced | File: net_utils.py |
| `pipecatapp/nomad_templates/immich.nomad.hcl` | 🔵 Entry Point | File: immich.nomad.hcl |
| `pipecatapp/nomad_templates/readeck.nomad.hcl` | 🔵 Entry Point | File: readeck.nomad.hcl |
| `pipecatapp/nomad_templates/uptime-kuma.nomad.hcl` | 🔵 Entry Point | File: uptime-kuma.nomad.hcl |
| `pipecatapp/nomad_templates/vaultwarden.nomad.hcl` | 🔵 Entry Point | File: vaultwarden.nomad.hcl |
| `pipecatapp/pmm_memory.py` | 🟢 Referenced | File: pmm_memory.py |
| `pipecatapp/pmm_memory_client.py` | 🟢 Referenced | File: pmm_memory_client.py |
| `pipecatapp/prompts/coding_expert.txt` | 🟢 Referenced | File: coding_expert.txt |
| `pipecatapp/prompts/creative_expert.txt` | 🟢 Referenced | File: creative_expert.txt |
| `pipecatapp/prompts/router.txt` | 🟢 Referenced | File: router.txt |
| `pipecatapp/prompts/tron_agent.txt` | 🟢 Referenced | File: tron_agent.txt |
| `pipecatapp/quality_control.py` | 🟢 Referenced | File: quality_control.py |
| `pipecatapp/rate_limiter.py` | 🟢 Referenced | File: rate_limiter.py |
| `pipecatapp/requirements.txt` | 🟢 Referenced | File: requirements.txt |
| `pipecatapp/security.py` | 🟢 Referenced | Pre-compile regex for redaction to improve performance |
| `pipecatapp/start_archivist.sh` | 🟢 Referenced | bin/bash |
| `pipecatapp/static/cluster.html` | 🟢 Referenced | File: cluster.html |
| `pipecatapp/static/cluster_viz.html` | 🟢 Referenced | A-Frame |
| `pipecatapp/static/css/litegraph.css` | 🟢 Referenced | File: litegraph.css |
| `pipecatapp/static/index.html` | 🟢 Referenced | File: index.html |
| `pipecatapp/static/js/editor.js` | 🟢 Referenced | Editor logic using LiteGraph.js |
| `pipecatapp/static/js/litegraph.js` | 🟢 Referenced | packer version |
| `pipecatapp/static/js/workflow.js` | 🔴 Orphan | File: workflow.js |
| `pipecatapp/static/terminal.js` | 🟢 Referenced | File: terminal.js |
| `pipecatapp/static/vr_index.html` | 🟢 Referenced | A-Frame |
| `pipecatapp/static/workflow.html` | 🟢 Referenced | File: workflow.html |
| `pipecatapp/task_supervisor.py` | 🟢 Referenced | File: task_supervisor.py |
| `pipecatapp/technician_agent.py` | 🟢 Referenced | File: technician_agent.py |
| `pipecatapp/test_memory.py` | 🟢 Referenced | File: test_memory.py |
| `pipecatapp/test_moondream_detector.py` | 🟢 Referenced | File: test_moondream_detector.py |
| `pipecatapp/test_server.py` | 🟢 Referenced | File: test_server.py |
| `pipecatapp/tests/test_audio_streamer.py` | 🧪 Test | File: test_audio_streamer.py |
| `pipecatapp/tests/test_metrics_cache.py` | 🧪 Test | File: test_metrics_cache.py |
| `pipecatapp/tests/test_net_utils.py` | 🧪 Test | File: test_net_utils.py |
| `pipecatapp/tests/test_piper_async.py` | 🧪 Test | File: test_piper_async.py |
| `pipecatapp/tests/test_rate_limiter.py` | 🧪 Test | File: test_rate_limiter.py |
| `pipecatapp/tests/test_stt_optimization.py` | 🧪 Test | File: test_stt_optimization.py |
| `pipecatapp/tests/test_web_server_unit.py` | 🧪 Test | File: test_web_server_unit.py |
| `pipecatapp/tests/test_websocket_security.py` | 🧪 Test | Mock out heavy dependencies that cause timeouts during import |
| `pipecatapp/tests/workflow/test_history.py` | 🧪 Test | File: test_history.py |
| `pipecatapp/tool_server.py` | 🟢 Referenced | File: tool_server.py |
| `pipecatapp/tools/__init__.py` | 🟢 Referenced | File: __init__.py |
| `pipecatapp/tools/ansible_tool.py` | 🟢 Referenced | File: ansible_tool.py |
| `pipecatapp/tools/archivist_tool.py` | 🟢 Referenced | File: archivist_tool.py |
| `pipecatapp/tools/claude_clone_tool.py` | 🟢 Referenced | File: claude_clone_tool.py |
| `pipecatapp/tools/code_runner_tool.py` | 🟢 Referenced | File: code_runner_tool.py |
| `pipecatapp/tools/council_tool.py` | 🟢 Referenced | File: council_tool.py |
| `pipecatapp/tools/dependency_scanner_tool.py` | 🟢 Referenced | File: dependency_scanner_tool.py |
| `pipecatapp/tools/desktop_control_tool.py` | 🟢 Referenced | File: desktop_control_tool.py |
| `pipecatapp/tools/file_editor_tool.py` | 🟢 Referenced | File: file_editor_tool.py |
| `pipecatapp/tools/final_answer_tool.py` | 🟢 Referenced | File: final_answer_tool.py |
| `pipecatapp/tools/gemini_cli.py` | 🟢 Referenced | File: gemini_cli.py |
| `pipecatapp/tools/get_nomad_job.py` | 🟢 Referenced | File: get_nomad_job.py |
| `pipecatapp/tools/git_tool.py` | 🟢 Referenced | File: git_tool.py |
| `pipecatapp/tools/ha_tool.py` | 🟢 Referenced | File: ha_tool.py |
| `pipecatapp/tools/llxprt_code_tool.py` | 🟢 Referenced | File: llxprt_code_tool.py |
| `pipecatapp/tools/mcp_tool.py` | 🟢 Referenced | File: mcp_tool.py |
| `pipecatapp/tools/open_workers_tool.py` | 🟢 Referenced | File: open_workers_tool.py |
| `pipecatapp/tools/opencode_tool.py` | 🟢 Referenced | File: opencode_tool.py |
| `pipecatapp/tools/orchestrator_tool.py` | 🟢 Referenced | File: orchestrator_tool.py |
| `pipecatapp/tools/planner_tool.py` | 🟢 Referenced | File: planner_tool.py |
| `pipecatapp/tools/power_tool.py` | 🟢 Referenced | File: power_tool.py |
| `pipecatapp/tools/project_mapper_tool.py` | 🟢 Referenced | File: project_mapper_tool.py |
| `pipecatapp/tools/prompt_improver_tool.py` | 🟢 Referenced | File: prompt_improver_tool.py |
| `pipecatapp/tools/rag_tool.py` | 🟢 Referenced | File: rag_tool.py |
| `pipecatapp/tools/remote_tool_proxy.py` | 🟢 Referenced | File: remote_tool_proxy.py |
| `pipecatapp/tools/sandbox.ts` | 🟢 Referenced | sandbox.ts |
| `pipecatapp/tools/shell_tool.py` | 🟢 Referenced | File: shell_tool.py |
| `pipecatapp/tools/smol_agent_tool.py` | 🟢 Referenced | File: smol_agent_tool.py |
| `pipecatapp/tools/ssh_tool.py` | 🟢 Referenced | File: ssh_tool.py |
| `pipecatapp/tools/summarizer_tool.py` | 🟢 Referenced | File: summarizer_tool.py |
| `pipecatapp/tools/swarm_tool.py` | 🟢 Referenced | File: swarm_tool.py |
| `pipecatapp/tools/tap_service.py` | 🟢 Referenced | File: tap_service.py |
| `pipecatapp/tools/term_everything_tool.py` | 🟢 Referenced | File: term_everything_tool.py |
| `pipecatapp/tools/test_code_runner_tool.py` | 🟢 Referenced | File: test_code_runner_tool.py |
| `pipecatapp/tools/test_ssh_tool.py` | 🟢 Referenced | File: test_ssh_tool.py |
| `pipecatapp/tools/vr_tool.py` | 🟢 Referenced | File: vr_tool.py |
| `pipecatapp/tools/web_browser_tool.py` | 🟢 Referenced | Mock playwright if it's not available |
| `pipecatapp/web_server.py` | 🟢 Referenced | File: web_server.py |
| `pipecatapp/worker_agent.py` | 🟢 Referenced | File: worker_agent.py |
| `pipecatapp/workflow/__init__.py` | 🟢 Referenced | File: __init__.py |
| `pipecatapp/workflow/context.py` | 🟢 Referenced | File: context.py |
| `pipecatapp/workflow/history.py` | 🟢 Referenced | File: history.py |
| `pipecatapp/workflow/node.py` | 🟢 Referenced | File: node.py |
| `pipecatapp/workflow/nodes/__init__.py` | 🟢 Referenced | File: __init__.py |
| `pipecatapp/workflow/nodes/base_nodes.py` | 🟢 Referenced | File: base_nodes.py |
| `pipecatapp/workflow/nodes/emperor_nodes.py` | 🟢 Referenced | File: emperor_nodes.py |
| `pipecatapp/workflow/nodes/llm_nodes.py` | 🟢 Referenced | File: llm_nodes.py |
| `pipecatapp/workflow/nodes/registry.py` | 🟢 Referenced | File: registry.py |
| `pipecatapp/workflow/nodes/system_nodes.py` | 🟢 Referenced | File: system_nodes.py |
| `pipecatapp/workflow/nodes/tool_nodes.py` | 🟢 Referenced | File: tool_nodes.py |
| `pipecatapp/workflow/runner.py` | 🟢 Referenced | File: runner.py |
| `pipecatapp/workflows/default_agent_loop.yaml` | 🟢 Referenced | File: default_agent_loop.yaml |
| `pipecatapp/workflows/poc_ensemble.yaml` | 🟢 Referenced | File: poc_ensemble.yaml |
| `pipecatapp/workflows/tiered_agent_loop.yaml` | 📄 Workflow Config | File: tiered_agent_loop.yaml |
| `playbook.yaml` | 🟢 Referenced | File: playbook.yaml |
| `playbooks/README.md` | 🟢 Referenced | Ansible Playbooks |
| `playbooks/benchmark_single_model.yaml` | 🟢 Referenced | File: benchmark_single_model.yaml |
| `playbooks/cluster_status.yaml` | 🟢 Referenced | File: cluster_status.yaml |
| `playbooks/common_setup.yaml` | 🟢 Referenced | File: common_setup.yaml |
| `playbooks/controller.yaml` | 🟢 Referenced | File: controller.yaml |
| `playbooks/debug_template.yaml` | 🟢 Referenced | File: debug_template.yaml |
| `playbooks/deploy_app.yaml` | 🟢 Referenced | File: deploy_app.yaml |
| `playbooks/deploy_expert.yaml` | 🟢 Referenced | File: deploy_expert.yaml |
| `playbooks/deploy_prompt_evolution.yaml` | 🟢 Referenced | File: deploy_prompt_evolution.yaml |
| `playbooks/developer_tools.yaml` | 🟢 Referenced | File: developer_tools.yaml |
| `playbooks/diagnose_and_log_home_assistant.yaml` | 🟢 Referenced | File: diagnose_and_log_home_assistant.yaml |
| `playbooks/diagnose_failure.yaml` | 🟢 Referenced | File: diagnose_failure.yaml |
| `playbooks/diagnose_home_assistant.yaml` | 🟢 Referenced | File: diagnose_home_assistant.yaml |
| `playbooks/fix_cluster.yaml` | 🟢 Referenced | File: fix_cluster.yaml |
| `playbooks/heal_cluster.yaml` | 🟢 Referenced | File: heal_cluster.yaml |
| `playbooks/heal_job.yaml` | 🟢 Referenced | This variable would be passed in from the orchestrator script |
| `playbooks/health_check.yaml` | 🟢 Referenced | File: health_check.yaml |
| `playbooks/network/mesh.yaml` | 🟢 Referenced | File: mesh.yaml |
| `playbooks/network/verify.yaml` | 🟢 Referenced | File: verify.yaml |
| `playbooks/ops/optimize_memory.yaml` | 🟢 Referenced | File: optimize_memory.yaml |
| `playbooks/preflight/checks.yaml` | 🟢 Referenced | File: checks.yaml |
| `playbooks/promote_controller.yaml` | 🟢 Referenced | File: promote_controller.yaml |
| `playbooks/promote_to_controller.yaml` | 🟢 Referenced | File: promote_to_controller.yaml |
| `playbooks/pxe_setup.yaml` | 🟢 Referenced | File: pxe_setup.yaml |
| `playbooks/redeploy_pipecat.yaml` | 🟢 Referenced | File: redeploy_pipecat.yaml |
| `playbooks/run_config_manager.yaml` | 🟢 Referenced | File: run_config_manager.yaml |
| `playbooks/run_consul.yaml` | 🟢 Referenced | File: run_consul.yaml |
| `playbooks/run_ha_diag.yaml` | 🟢 Referenced | File: run_ha_diag.yaml |
| `playbooks/run_health_check.yaml` | 🟢 Referenced | File: run_health_check.yaml |
| `playbooks/services/README.md` | 🟢 Referenced | Ansible Service Playbooks |
| `playbooks/services/ai_experts.yaml` | 🟢 Referenced | File: ai_experts.yaml |
| `playbooks/services/app_services.yaml` | 🟢 Referenced | File: app_services.yaml |
| `playbooks/services/consul.yaml` | 🟢 Referenced | File: consul.yaml |
| `playbooks/services/core_ai_services.yaml` | 🟢 Referenced | File: core_ai_services.yaml |
| `playbooks/services/core_infra.yaml` | 🟢 Referenced | File: core_infra.yaml |
| `playbooks/services/docker.yaml` | 🟢 Referenced | File: docker.yaml |
| `playbooks/services/final_verification.yaml` | 🟢 Referenced | File: final_verification.yaml |
| `playbooks/services/model_services.yaml` | 🟢 Referenced | File: model_services.yaml |
| `playbooks/services/monitoring.yaml` | 🟢 Referenced | File: monitoring.yaml |
| `playbooks/services/nomad.yaml` | 🟢 Referenced | File: nomad.yaml |
| `playbooks/services/nomad_client.yaml` | 🟢 Referenced | File: nomad_client.yaml |
| `playbooks/services/streaming_services.yaml` | 🟢 Referenced | File: streaming_services.yaml |
| `playbooks/services/tasks/diagnose_home_assistant.yaml` | 🟢 Referenced | File: diagnose_home_assistant.yaml |
| `playbooks/services/training_services.yaml` | 🟢 Referenced | File: training_services.yaml |
| `playbooks/status-check.yaml` | 🟢 Referenced | File: status-check.yaml |
| `playbooks/wake.yaml` | 🟢 Referenced | File: wake.yaml |
| `playbooks/worker.yaml` | 🟢 Referenced | File: worker.yaml |
| `prompt_engineering/PROMPT_ENGINEERING.md` | 🟢 Referenced | Prompt Engineering Workflow |
| `prompt_engineering/README.md` | 🟢 Referenced | Prompt Engineering |
| `prompt_engineering/agents/ADAPTATION_AGENT.md` | 🟢 Referenced | The Self-Adaptation Agent |
| `prompt_engineering/agents/EVALUATOR_GENERATOR.md` | 🟢 Referenced | Agent Task: Generate a Custom Code Evaluator Script |
| `prompt_engineering/agents/README.md` | 🟢 Referenced | Agent Definitions |
| `prompt_engineering/agents/architecture_review.md` | 🟢 Referenced | Agent: Architecture Review |
| `prompt_engineering/agents/code_clean_up.md` | 🟢 Referenced | Agent: Code Clean Up |
| `prompt_engineering/agents/debug_and_analysis.md` | 🟢 Referenced | Agent: Debug and Analysis |
| `prompt_engineering/agents/new_task_review.md` | 🟢 Referenced | Agent: New Task Review |
| `prompt_engineering/agents/problem_scope_framing.md` | 🟢 Referenced | Agent: Problem Scope Framing |
| `prompt_engineering/archive/agent_0.json` | 📄 Documentation/Asset | File: agent_0.json |
| `prompt_engineering/archive/agent_0.py` | 📄 Documentation/Asset | File: agent_0.py |
| `prompt_engineering/archive/agent_1.json` | 📄 Documentation/Asset | File: agent_1.json |
| `prompt_engineering/archive/agent_1.py` | 📄 Documentation/Asset | File: agent_1.py |
| `prompt_engineering/archive/agent_2.json` | 📄 Documentation/Asset | File: agent_2.json |
| `prompt_engineering/archive/agent_2.py` | 📄 Documentation/Asset | File: agent_2.py |
| `prompt_engineering/archive/agent_3.json` | 📄 Documentation/Asset | File: agent_3.json |
| `prompt_engineering/archive/agent_3.py` | 📄 Documentation/Asset | File: agent_3.py |
| `prompt_engineering/challenger.py` | 🟢 Referenced | File: challenger.py |
| `prompt_engineering/create_evaluator.py` | 🟢 Referenced | The template is based on the one defined in prompt_engineering/agents/EVALUATOR_GENERATOR.md |
| `prompt_engineering/evaluation_lib.py` | 🟢 Referenced | This file will contain the reusable functions for evaluating code. |
| `prompt_engineering/evaluation_suite/README.md` | 🟢 Referenced | Evaluation Suite |
| `prompt_engineering/evaluation_suite/test_vision.yaml` | 🟢 Referenced | File: test_vision.yaml |
| `prompt_engineering/evaluator.py` | 🟢 Referenced | File: evaluator.py |
| `prompt_engineering/evolve.py` | 🟢 Referenced | File: evolve.py |
| `prompt_engineering/frontend/index.html` | 🟢 Referenced | File: index.html |
| `prompt_engineering/frontend/server.py` | 🟢 Referenced | File: server.py |
| `prompt_engineering/generated_evaluators/.gitignore` | 🟢 Referenced | Ignore all files in this directory |
| `prompt_engineering/promote_agent.py` | 🟢 Referenced | File: promote_agent.py |
| `prompt_engineering/requirements-dev.txt` | 🟢 Referenced | File: requirements-dev.txt |
| `prompt_engineering/run_campaign.py` | 🟢 Referenced | File: run_campaign.py |
| `prompt_engineering/visualize_archive.py` | 🟢 Referenced | File: visualize_archive.py |
| `prompts/README.md` | 🟢 Referenced | Prompts |
| `prompts/chat-with-bob.txt` | 🟢 Referenced | File: chat-with-bob.txt |
| `prompts/router.txt` | 🟢 Referenced | File: router.txt |
| `provisioning.py` | 🟢 Referenced | Provisioning Script for Hybrid Architecture. |
| `pytest.ini` | 🟢 Referenced | File: pytest.ini |
| `reflection/README.md` | 🟢 Referenced | Reflection |
| `reflection/adaptation_manager.py` | 🟢 Referenced | File: adaptation_manager.py |
| `reflection/create_reflection.py` | 🟢 Referenced | File: create_reflection.py |
| `reflection/reflect.py` | 🟢 Referenced | File: reflect.py |
| `requirements-dev.txt` | 🟢 Referenced | File: requirements-dev.txt |
| `run_tests.sh` | 🟢 Referenced | usr/bin/env bash |
| `scripts/README.md` | 🟢 Referenced | Project Linting and Formatting |
| `scripts/ansible_diff.sh` | 🟢 Referenced | A script to compare Ansible playbook runs to detect changes over time. It establishes a baseline fro |
| `scripts/ci_ansible_check.sh` | 🟢 Referenced | A CI/CD-friendly script to check for unintended changes in Ansible playbooks.  - It compares the pla |
| `scripts/cleanup.sh` | 🟢 Referenced | This script cleans up temporary files created by the project. |
| `scripts/compare_exo_llama.py` | 🔵 Entry Point | File: compare_exo_llama.py |
| `scripts/create_cynic_model.sh` | 🔵 Entry Point | bin/bash |
| `scripts/debug/README.md` | 🟢 Referenced | Debug Scripts |
| `scripts/debug/test_mqtt_connection.py` | 🟢 Referenced | File: test_mqtt_connection.py |
| `scripts/debug_mesh.sh` | 🟢 Referenced | bin/bash |
| `scripts/fix_markdown.sh` | 🟢 Referenced | Automatic Markdown Linter Fixer  This script uses markdownlint-cli's --fix option to automatically |
| `scripts/fix_verification_failures.sh` | 🔵 Entry Point | Scripts to help remediate failures reported by verify_components.py |
| `scripts/fix_yaml.sh` | 🟢 Referenced | Automatic YAML Linter Fixer  This script automatically fixes common, repetitive style issues report |
| `scripts/generate_file_map.py` | 🔵 Entry Point | usr/bin/env python3 |
| `scripts/healer.py` | 🔵 Entry Point | File: healer.py |
| `scripts/lint.sh` | 🟢 Referenced | Unified Linting Script  This script runs a series of linters to ensure code quality and consistency |
| `scripts/lint_exclude.txt` | 🟢 Referenced | Exclude problematic files from the linting process. |
| `scripts/memory_audit.py` | 🟢 Referenced | File: memory_audit.py |
| `scripts/profile_resources.sh` | 🔵 Entry Point | Profile resources usage and alignment of AI experts and models. |
| `scripts/prune_consul_services.py` | 🟢 Referenced | Prune Stale Critical Services from Consul |
| `scripts/run_quibbler.sh` | 🟢 Referenced | A wrapper script to run quibbler for code review. Check for required arguments |
| `scripts/test_playbooks_dry_run.sh` | 🟢 Referenced | bin/bash |
| `scripts/test_playbooks_live_run.sh` | 🔵 Entry Point | bin/bash |
| `scripts/uninstall.sh` | 🔵 Entry Point | This script uninstalls all software and reverts all changes made by the playbook. |
| `scripts/verify_consul_attributes.sh` | 🔵 Entry Point | bin/bash |
| `start_services.sh` | 🟢 Referenced | This script is a legacy utility for manually starting services. ⚠️  DEPRECATED: Please use Ansible t |
| `supervisor.py` | 🟢 Referenced | File: supervisor.py |
| `test.wav` | 🟢 Referenced | File: test.wav |
| `test_imports.py` | 🧪 Test | Add files dir to path |
| `test_playbook.yml` | 🧪 Test | File: test_playbook.yml |
| `tests/README.md` | 🟢 Referenced | Testing |
| `tests/__init__.py` | 🟢 Referenced | File: __init__.py |
| `tests/e2e/README.md` | 🟢 Referenced | End-to-End Tests |
| `tests/e2e/__init__.py` | 🟢 Referenced | File: __init__.py |
| `tests/e2e/test_api.py` | 🟢 Referenced | File: test_api.py |
| `tests/e2e/test_intelligent_routing.py` | 🟢 Referenced | File: test_intelligent_routing.py |
| `tests/e2e/test_mission_control.py` | 🟢 Referenced | File: test_mission_control.py |
| `tests/e2e/test_palette_command_history.py` | 🧪 Test | File: test_palette_command_history.py |
| `tests/e2e/test_palette_ux.py` | 🧪 Test | File: test_palette_ux.py |
| `tests/e2e/test_regression.py` | 🟢 Referenced | File: test_regression.py |
| `tests/integration/README.md` | 🟢 Referenced | Integration Tests |
| `tests/integration/__init__.py` | 🟢 Referenced | File: __init__.py |
| `tests/integration/roles/test_home_assistant/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `tests/integration/stub_services.py` | 🟢 Referenced | File: stub_services.py |
| `tests/integration/test_consul_role.yaml` | 🟢 Referenced | File: test_consul_role.yaml |
| `tests/integration/test_home_assistant.yaml` | 🟢 Referenced | File: test_home_assistant.yaml |
| `tests/integration/test_mini_pipeline.py` | 🧪 Test | File: test_mini_pipeline.py |
| `tests/integration/test_mqtt_exporter.py` | 🧪 Test | File: test_mqtt_exporter.py |
| `tests/integration/test_nomad_role.yaml` | 🟢 Referenced | File: test_nomad_role.yaml |
| `tests/integration/test_pipecat_app.py` | 🟢 Referenced | File: test_pipecat_app.py |
| `tests/integration/test_preemption.py` | 🟢 Referenced | File: test_preemption.py |
| `tests/playbooks/e2e-tests.yaml` | 🟢 Referenced | File: e2e-tests.yaml |
| `tests/playbooks/test_consul.yaml` | 🧪 Test | File: test_consul.yaml |
| `tests/playbooks/test_llama_cpp.yaml` | 🧪 Test | File: test_llama_cpp.yaml |
| `tests/playbooks/test_nomad.yaml` | 🧪 Test | File: test_nomad.yaml |
| `tests/scripts/run_unit_tests.sh` | 🟢 Referenced | usr/bin/env bash |
| `tests/scripts/test_distributed_llama.sh` | 🧪 Test | Exit immediately if a command exits with a non-zero status. set -e # We'll handle errors manually to |
| `tests/scripts/test_duplicate_role_execution.sh` | 🧪 Test | Test to verify that the bootstrap_agent role is not run twice using static analysis.  Move to the p |
| `tests/scripts/test_paddler.sh` | 🧪 Test | test_paddler.sh  This script performs basic tests to verify that Paddler (agent and balancer) is fun |
| `tests/scripts/test_piper.sh` | 🧪 Test | File: test_piper.sh |
| `tests/scripts/test_run.sh` | 🧪 Test | Start a new chat |
| `tests/scripts/verify_components.py` | 🟢 Referenced | usr/bin/env python3 |
| `tests/test_agent_patterns.py` | 🧪 Test | File: test_agent_patterns.py |
| `tests/test_emperor_node.py` | 🧪 Test | File: test_emperor_node.py |
| `tests/unit/README.md` | 🟢 Referenced | Unit Tests |
| `tests/unit/__init__.py` | 🟢 Referenced | File: __init__.py |
| `tests/unit/conftest.py` | 🟢 Referenced | List of modules to mock if they are missing in the test environment |
| `tests/unit/test_adaptation_manager.py` | 🟢 Referenced | File: test_adaptation_manager.py |
| `tests/unit/test_agent_definitions.py` | 🟢 Referenced | Define the path to the agent definitions directory |
| `tests/unit/test_ansible_tool.py` | 🟢 Referenced | File: test_ansible_tool.py |
| `tests/unit/test_archivist_tool.py` | 🧪 Test | File: test_archivist_tool.py |
| `tests/unit/test_claude_clone_tool.py` | 🟢 Referenced | File: test_claude_clone_tool.py |
| `tests/unit/test_code_runner_tool.py` | 🟢 Referenced | File: test_code_runner_tool.py |
| `tests/unit/test_council_tool.py` | 🧪 Test | File: test_council_tool.py |
| `tests/unit/test_dependency_scanner.py` | 🧪 Test | File: test_dependency_scanner.py |
| `tests/unit/test_desktop_control_tool.py` | 🟢 Referenced | File: test_desktop_control_tool.py |
| `tests/unit/test_file_editor_security.py` | 🧪 Test | File: test_file_editor_security.py |
| `tests/unit/test_file_editor_tool.py` | 🧪 Test | File: test_file_editor_tool.py |
| `tests/unit/test_final_answer_tool.py` | 🧪 Test | Add the tools directory to the python path |
| `tests/unit/test_gemini_cli.py` | 🟢 Referenced | File: test_gemini_cli.py |
| `tests/unit/test_get_nomad_job.py` | 🧪 Test | File: test_get_nomad_job.py |
| `tests/unit/test_git_tool.py` | 🟢 Referenced | File: test_git_tool.py |
| `tests/unit/test_ha_tool.py` | 🧪 Test | File: test_ha_tool.py |
| `tests/unit/test_home_assistant_template.py` | 🟢 Referenced | File: test_home_assistant_template.py |
| `tests/unit/test_infrastructure.py` | 🧪 Test | File: test_infrastructure.py |
| `tests/unit/test_lint_script.py` | 🟢 Referenced | File: test_lint_script.py |
| `tests/unit/test_llxprt_code_tool.py` | 🟢 Referenced | File: test_llxprt_code_tool.py |
| `tests/unit/test_mcp_tool.py` | 🟢 Referenced | File: test_mcp_tool.py |
| `tests/unit/test_mqtt_template.py` | 🧪 Test | File: test_mqtt_template.py |
| `tests/unit/test_open_workers_tool.py` | 🧪 Test | File: test_open_workers_tool.py |
| `tests/unit/test_opencode_tool.py` | 🧪 Test | File: test_opencode_tool.py |
| `tests/unit/test_orchestrator_tool.py` | 🧪 Test | File: test_orchestrator_tool.py |
| `tests/unit/test_pipecat_app_unit.py` | 🟢 Referenced | File: test_pipecat_app_unit.py |
| `tests/unit/test_planner_tool.py` | 🧪 Test | File: test_planner_tool.py |
| `tests/unit/test_playbook_integration.py` | 🟢 Referenced | File: test_playbook_integration.py |
| `tests/unit/test_poc_ensemble.py` | 🧪 Test | File: test_poc_ensemble.py |
| `tests/unit/test_power_tool.py` | 🟢 Referenced | File: test_power_tool.py |
| `tests/unit/test_project_mapper_tool.py` | 🧪 Test | File: test_project_mapper_tool.py |
| `tests/unit/test_prompt_engineering.py` | 🟢 Referenced | File: test_prompt_engineering.py |
| `tests/unit/test_prompt_improver_tool.py` | 🧪 Test | File: test_prompt_improver_tool.py |
| `tests/unit/test_provisioning.py` | 🧪 Test | File: test_provisioning.py |
| `tests/unit/test_rag_tool.py` | 🟢 Referenced | File: test_rag_tool.py |
| `tests/unit/test_reflection.py` | 🟢 Referenced | File: test_reflection.py |
| `tests/unit/test_security.py` | 🧪 Test | Ensure pipecatapp is in path |
| `tests/unit/test_shell_tool.py` | 🧪 Test | File: test_shell_tool.py |
| `tests/unit/test_simple_llm_node.py` | 🧪 Test | Mock pipecat before importing the module under test |
| `tests/unit/test_smol_agent_tool.py` | 🧪 Test | File: test_smol_agent_tool.py |
| `tests/unit/test_ssh_tool.py` | 🟢 Referenced | File: test_ssh_tool.py |
| `tests/unit/test_summarizer_tool.py` | 🟢 Referenced | File: test_summarizer_tool.py |
| `tests/unit/test_supervisor.py` | 🟢 Referenced | File: test_supervisor.py |
| `tests/unit/test_swarm_tool.py` | 🧪 Test | File: test_swarm_tool.py |
| `tests/unit/test_tap_service.py` | 🧪 Test | File: test_tap_service.py |
| `tests/unit/test_term_everything_tool.py` | 🟢 Referenced | File: test_term_everything_tool.py |
| `tests/unit/test_vision_failover.py` | 🧪 Test | File: test_vision_failover.py |
| `tests/unit/test_web_browser_tool.py` | 🟢 Referenced | File: test_web_browser_tool.py |
| `tests/unit/test_workflow.py` | 🧪 Test | File: test_workflow.py |
| `tests/unit/test_world_model_service.py` | 🧪 Test | File: test_world_model_service.py |
| `verification/save_success.png` | 🟢 Referenced | File: save_success.png |
| `verification/verify_workflow_save.py` | 📄 Documentation/Asset | Mock APIs |
| `verify_config_load.py` | 🟢 Referenced | File: verify_config_load.py |
| `workflows/default_agent_loop.yaml` | 🟢 Referenced | File: default_agent_loop.yaml |

## Dependency Diagram

```mermaid
graph LR
    subgraph dir_Root [Root]
        direction TB
        node_16[".coverage"]
        node_34[".djlint.toml"]
        node_0[".gitattributes"]
        node_14[".gitignore"]
        node_2[".markdownlint.json"]
        node_26[".yamllint"]
        node_12["=0.9.4"]
        node_27["IPV6_AUDIT.md"]
        node_30["LICENSE"]
        node_7["README.md"]
        node_4["TODO.md"]
        node_17["YAML_FILES_REPORT.md"]
        node_9["agentic_workflow.sh"]
        node_3["aid_e_log.txt"]
        node_31["ansible.cfg"]
        node_20["bootstrap.sh"]
        node_29["check_all_playbooks.sh"]
        node_24["check_deps.py"]
        node_19["create_todo_issues.sh"]
        node_11["debug_expert.sh"]
        node_5["generate_issue_script.py"]
        node_1["hostfile"]
        node_33["inventory.yaml"]
        node_32["local_inventory.ini"]
        node_25["package.json"]
        node_22["playbook.yaml"]
        node_35["provisioning.py"]
        node_23["pytest.ini"]
        node_13["requirements-dev.txt"]
        node_15["run_tests.sh"]
        node_8["start_services.sh"]
        node_18["supervisor.py"]
        node_21["test.wav"]
        node_6["test_imports.py"]
        node_10["test_playbook.yml"]
        node_28["verify_config_load.py"]
    end
    subgraph dir__github [.github]
        direction TB
        node_60["AGENTIC_README.md"]
    end
    subgraph dir__github_workflows [.github/workflows]
        direction TB
        node_64["auto-merge.yml"]
        node_65["ci.yml"]
        node_61["create-issues-from-files.yml"]
        node_63["jules-queue.yml"]
        node_62["remote-verify.yml"]
    end
    subgraph dir__husky [.husky]
        direction TB
        node_420["pre-push"]
    end
    subgraph dir__opencode [.opencode]
        direction TB
        node_543["README.md"]
        node_544["opencode.json"]
    end
    subgraph dir_ansible [ansible]
        direction TB
        node_98["README.md"]
        node_99["lint_nomad.yaml"]
        node_100["run_download_models.yaml"]
    end
    subgraph dir_ansible_filter_plugins [ansible/filter_plugins]
        direction TB
        node_115["README.md"]
        node_116["safe_flatten.py"]
    end
    subgraph dir_ansible_jobs [ansible/jobs]
        direction TB
        node_105["README.md"]
        node_110["benchmark.nomad"]
        node_102["evolve-prompt.nomad.j2"]
        node_109["expert-debug.nomad"]
        node_106["expert.nomad.j2"]
        node_104["filebrowser.nomad.j2"]
        node_101["health-check.nomad.j2"]
        node_107["llamacpp-batch.nomad.j2"]
        node_103["llamacpp-rpc.nomad.j2"]
        node_114["model-benchmark.nomad.j2"]
        node_113["pipecatapp.nomad"]
        node_112["router.nomad.j2"]
        node_108["test-runner.nomad.j2"]
        node_111["vllm.nomad.j2"]
    end
    subgraph dir_ansible_paddler_agent [ansible/paddler_agent]
        direction TB
        node_353["README.md"]
    end
    subgraph dir_ansible_paddler_agent_defaults [ansible/paddler_agent/defaults]
        direction TB
        node_354["main.yaml"]
    end
    subgraph dir_ansible_paddler_agent_tasks [ansible/paddler_agent/tasks]
        direction TB
        node_356["paddler_agent.yaml"]
    end
    subgraph dir_ansible_paddler_agent_templates [ansible/paddler_agent/templates]
        direction TB
        node_355["paddler-agent.service.j2"]
    end
    subgraph dir_ansible_paddler_balancer [ansible/paddler_balancer]
        direction TB
        node_117["README.md"]
    end
    subgraph dir_ansible_paddler_balancer_defaults [ansible/paddler_balancer/defaults]
        direction TB
        node_118["main.yaml"]
    end
    subgraph dir_ansible_paddler_balancer_tasks [ansible/paddler_balancer/tasks]
        direction TB
        node_120["paddler_balancer.yaml"]
    end
    subgraph dir_ansible_paddler_balancer_templates [ansible/paddler_balancer/templates]
        direction TB
        node_119["paddler-balancer.service.j2"]
    end
    subgraph dir_ansible_roles [ansible/roles]
        direction TB
        node_121["README.md"]
    end
    subgraph dir_ansible_roles_benchmark_models_tasks [ansible/roles/benchmark_models/tasks]
        direction TB
        node_155["benchmark_loop.yaml"]
        node_154["main.yaml"]
    end
    subgraph dir_ansible_roles_benchmark_models_templates [ansible/roles/benchmark_models/templates]
        direction TB
        node_153["model-benchmark.nomad.j2"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_defaults [ansible/roles/bootstrap_agent/defaults]
        direction TB
        node_219["main.yaml"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_tasks [ansible/roles/bootstrap_agent/tasks]
        direction TB
        node_220["deploy_llama_cpp_model.yaml"]
        node_221["main.yaml"]
    end
    subgraph dir_ansible_roles_claude_clone_tasks [ansible/roles/claude_clone/tasks]
        direction TB
        node_249["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tools_tasks [ansible/roles/common-tools/tasks]
        direction TB
        node_208["main.yaml"]
    end
    subgraph dir_ansible_roles_common_handlers [ansible/roles/common/handlers]
        direction TB
        node_146["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tasks [ansible/roles/common/tasks]
        direction TB
        node_150["main.yaml"]
        node_151["network_repair.yaml"]
    end
    subgraph dir_ansible_roles_common_templates [ansible/roles/common/templates]
        direction TB
        node_149["cluster-ip-alias.service.j2"]
        node_148["hosts.j2"]
        node_147["update-ssh-authorized-keys.sh.j2"]
    end
    subgraph dir_ansible_roles_config_manager_tasks [ansible/roles/config_manager/tasks]
        direction TB
        node_241["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_defaults [ansible/roles/consul/defaults]
        direction TB
        node_157["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_handlers [ansible/roles/consul/handlers]
        direction TB
        node_156["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_tasks [ansible/roles/consul/tasks]
        direction TB
        node_162["acl.yaml"]
        node_160["main.yaml"]
        node_161["tls.yaml"]
    end
    subgraph dir_ansible_roles_consul_templates [ansible/roles/consul/templates]
        direction TB
        node_159["consul.hcl.j2"]
        node_158["consul.service.j2"]
    end
    subgraph dir_ansible_roles_desktop_extras_tasks [ansible/roles/desktop_extras/tasks]
        direction TB
        node_127["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_handlers [ansible/roles/docker/handlers]
        direction TB
        node_209["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_molecule_default [ansible/roles/docker/molecule/default]
        direction TB
        node_212["converge.yml"]
        node_213["molecule.yml"]
        node_215["prepare.yml"]
        node_214["verify.yml"]
    end
    subgraph dir_ansible_roles_docker_tasks [ansible/roles/docker/tasks]
        direction TB
        node_211["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_templates [ansible/roles/docker/templates]
        direction TB
        node_210["daemon.json.j2"]
    end
    subgraph dir_ansible_roles_download_models_files [ansible/roles/download_models/files]
        direction TB
        node_144["download_hf_repo.py"]
    end
    subgraph dir_ansible_roles_download_models_tasks [ansible/roles/download_models/tasks]
        direction TB
        node_145["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_defaults [ansible/roles/exo/defaults]
        direction TB
        node_250["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_files [ansible/roles/exo/files]
        direction TB
        node_251["Dockerfile"]
    end
    subgraph dir_ansible_roles_exo_tasks [ansible/roles/exo/tasks]
        direction TB
        node_253["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_templates [ansible/roles/exo/templates]
        direction TB
        node_252["exo.nomad.j2"]
    end
    subgraph dir_ansible_roles_headscale_defaults [ansible/roles/headscale/defaults]
        direction TB
        node_272["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_handlers [ansible/roles/headscale/handlers]
        direction TB
        node_271["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_tasks [ansible/roles/headscale/tasks]
        direction TB
        node_275["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_templates [ansible/roles/headscale/templates]
        direction TB
        node_274["config.yaml.j2"]
        node_273["headscale.service.j2"]
    end
    subgraph dir_ansible_roles_heretic_tool_defaults [ansible/roles/heretic_tool/defaults]
        direction TB
        node_222["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_meta [ansible/roles/heretic_tool/meta]
        direction TB
        node_223["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_tasks [ansible/roles/heretic_tool/tasks]
        direction TB
        node_224["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_meta [ansible/roles/home_assistant/meta]
        direction TB
        node_256["main.yaml"]
        node_255["main.yml"]
    end
    subgraph dir_ansible_roles_home_assistant_tasks [ansible/roles/home_assistant/tasks]
        direction TB
        node_259["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_templates [ansible/roles/home_assistant/templates]
        direction TB
        node_258["configuration.yaml.j2"]
        node_257["home_assistant.nomad.j2"]
    end
    subgraph dir_ansible_roles_kittentts_tasks [ansible/roles/kittentts/tasks]
        direction TB
        node_163["main.yaml"]
    end
    subgraph dir_ansible_roles_librarian_defaults [ansible/roles/librarian/defaults]
        direction TB
        node_129["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_tasks [ansible/roles/librarian/tasks]
        direction TB
        node_133["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_templates [ansible/roles/librarian/templates]
        direction TB
        node_130["librarian.service.j2"]
        node_132["librarian_agent.py.j2"]
        node_131["spacedrive.service.j2"]
    end
    subgraph dir_ansible_roles_llama_cpp_handlers [ansible/roles/llama_cpp/handlers]
        direction TB
        node_202["main.yaml"]
    end
    subgraph dir_ansible_roles_llama_cpp_molecule_default [ansible/roles/llama_cpp/molecule/default]
        direction TB
        node_205["converge.yml"]
        node_206["molecule.yml"]
        node_207["verify.yml"]
    end
    subgraph dir_ansible_roles_llama_cpp_tasks [ansible/roles/llama_cpp/tasks]
        direction TB
        node_203["main.yaml"]
        node_204["run_single_rpc_job.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_tasks [ansible/roles/llxprt_code/tasks]
        direction TB
        node_243["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_templates [ansible/roles/llxprt_code/templates]
        direction TB
        node_242["llxprt-code.env.j2"]
    end
    subgraph dir_ansible_roles_magic_mirror_defaults [ansible/roles/magic_mirror/defaults]
        direction TB
        node_294["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_handlers [ansible/roles/magic_mirror/handlers]
        direction TB
        node_293["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_tasks [ansible/roles/magic_mirror/tasks]
        direction TB
        node_296["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_templates [ansible/roles/magic_mirror/templates]
        direction TB
        node_295["magic_mirror.nomad.j2"]
    end
    subgraph dir_ansible_roles_mcp_server_defaults [ansible/roles/mcp_server/defaults]
        direction TB
        node_199["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_handlers [ansible/roles/mcp_server/handlers]
        direction TB
        node_198["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_tasks [ansible/roles/mcp_server/tasks]
        direction TB
        node_201["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_templates [ansible/roles/mcp_server/templates]
        direction TB
        node_200["mcp_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_graph_tasks [ansible/roles/memory_graph/tasks]
        direction TB
        node_240["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_graph_templates [ansible/roles/memory_graph/templates]
        direction TB
        node_239["memory-graph.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_service_files [ansible/roles/memory_service/files]
        direction TB
        node_179["app.py"]
        node_180["pmm_memory.py"]
    end
    subgraph dir_ansible_roles_memory_service_handlers [ansible/roles/memory_service/handlers]
        direction TB
        node_178["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_tasks [ansible/roles/memory_service/tasks]
        direction TB
        node_182["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_templates [ansible/roles/memory_service/templates]
        direction TB
        node_181["memory_service.nomad.j2"]
    end
    subgraph dir_ansible_roles_moe_gateway_files [ansible/roles/moe_gateway/files]
        direction TB
        node_174["gateway.py"]
    end
    subgraph dir_ansible_roles_moe_gateway_files_static [ansible/roles/moe_gateway/files/static]
        direction TB
        node_175["index.html"]
    end
    subgraph dir_ansible_roles_moe_gateway_handlers [ansible/roles/moe_gateway/handlers]
        direction TB
        node_173["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_tasks [ansible/roles/moe_gateway/tasks]
        direction TB
        node_177["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_templates [ansible/roles/moe_gateway/templates]
        direction TB
        node_176["moe-gateway.nomad.j2"]
    end
    subgraph dir_ansible_roles_monitoring_defaults [ansible/roles/monitoring/defaults]
        direction TB
        node_187["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_files [ansible/roles/monitoring/files]
        direction TB
        node_188["llm_dashboard.json"]
    end
    subgraph dir_ansible_roles_monitoring_tasks [ansible/roles/monitoring/tasks]
        direction TB
        node_197["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_templates [ansible/roles/monitoring/templates]
        direction TB
        node_189["dashboards.yaml.j2"]
        node_192["datasource.yaml.j2"]
        node_195["grafana.nomad.j2"]
        node_190["memory-audit.nomad.j2"]
        node_193["mqtt-exporter.nomad.j2"]
        node_196["node-exporter.nomad.j2"]
        node_194["prometheus.nomad.j2"]
        node_191["prometheus.yml.j2"]
    end
    subgraph dir_ansible_roles_mqtt_handlers [ansible/roles/mqtt/handlers]
        direction TB
        node_276["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_meta [ansible/roles/mqtt/meta]
        direction TB
        node_277["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_tasks [ansible/roles/mqtt/tasks]
        direction TB
        node_279["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_templates [ansible/roles/mqtt/templates]
        direction TB
        node_278["mqtt.nomad.j2"]
    end
    subgraph dir_ansible_roles_nanochat_defaults [ansible/roles/nanochat/defaults]
        direction TB
        node_268["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_handlers [ansible/roles/nanochat/handlers]
        direction TB
        node_267["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_tasks [ansible/roles/nanochat/tasks]
        direction TB
        node_270["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_templates [ansible/roles/nanochat/templates]
        direction TB
        node_269["nanochat.nomad.j2"]
    end
    subgraph dir_ansible_roles_nats_handlers [ansible/roles/nats/handlers]
        direction TB
        node_233["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_tasks [ansible/roles/nats/tasks]
        direction TB
        node_235["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_templates [ansible/roles/nats/templates]
        direction TB
        node_234["nats.nomad.j2"]
    end
    subgraph dir_ansible_roles_nfs_tasks [ansible/roles/nfs/tasks]
        direction TB
        node_128["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_handlers [ansible/roles/nixos_pxe_server/handlers]
        direction TB
        node_263["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_tasks [ansible/roles/nixos_pxe_server/tasks]
        direction TB
        node_266["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_templates [ansible/roles/nixos_pxe_server/templates]
        direction TB
        node_265["boot.ipxe.nix.j2"]
        node_264["configuration.nix.j2"]
    end
    subgraph dir_ansible_roles_nomad_defaults [ansible/roles/nomad/defaults]
        direction TB
        node_166["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_handlers [ansible/roles/nomad/handlers]
        direction TB
        node_165["main.yaml"]
        node_164["restart_nomad_handler_tasks.yaml"]
    end
    subgraph dir_ansible_roles_nomad_tasks [ansible/roles/nomad/tasks]
        direction TB
        node_172["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_templates [ansible/roles/nomad/templates]
        direction TB
        node_171["client.hcl.j2"]
        node_168["nomad.hcl.server.j2"]
        node_167["nomad.service.j2"]
        node_169["nomad.sh.j2"]
        node_170["server.hcl.j2"]
    end
    subgraph dir_ansible_roles_opencode_handlers [ansible/roles/opencode/handlers]
        direction TB
        node_216["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_tasks [ansible/roles/opencode/tasks]
        direction TB
        node_218["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_templates [ansible/roles/opencode/templates]
        direction TB
        node_217["opencode.nomad.j2"]
    end
    subgraph dir_ansible_roles_openworkers_handlers [ansible/roles/openworkers/handlers]
        direction TB
        node_122["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_tasks [ansible/roles/openworkers/tasks]
        direction TB
        node_126["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_templates [ansible/roles/openworkers/templates]
        direction TB
        node_125["openworkers-bootstrap.nomad.j2"]
        node_123["openworkers-infra.nomad.j2"]
        node_124["openworkers-runners.nomad.j2"]
    end
    subgraph dir_ansible_roles_paddler_tasks [ansible/roles/paddler/tasks]
        direction TB
        node_262["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_defaults [ansible/roles/pipecatapp/defaults]
        direction TB
        node_341["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_handlers [ansible/roles/pipecatapp/handlers]
        direction TB
        node_340["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_tasks [ansible/roles/pipecatapp/tasks]
        direction TB
        node_352["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates [ansible/roles/pipecatapp/templates]
        direction TB
        node_345["archivist.nomad.j2"]
        node_342["pipecat.env.j2"]
        node_343["pipecatapp.nomad.j2"]
        node_344["start_pipecatapp.sh.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_prompts [ansible/roles/pipecatapp/templates/prompts]
        direction TB
        node_348["coding_expert.txt.j2"]
        node_349["creative_expert.txt.j2"]
        node_347["cynic_expert.txt.j2"]
        node_346["router.txt.j2"]
        node_350["tron_agent.txt.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_workflows [ansible/roles/pipecatapp/templates/workflows]
        direction TB
        node_351["default_agent_loop.yaml.j2"]
    end
    subgraph dir_ansible_roles_postgres_handlers [ansible/roles/postgres/handlers]
        direction TB
        node_236["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_tasks [ansible/roles/postgres/tasks]
        direction TB
        node_238["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_templates [ansible/roles/postgres/templates]
        direction TB
        node_237["postgres.nomad.j2"]
    end
    subgraph dir_ansible_roles_power_manager_defaults [ansible/roles/power_manager/defaults]
        direction TB
        node_287["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_files [ansible/roles/power_manager/files]
        direction TB
        node_288["power_agent.py"]
        node_289["traffic_monitor.c"]
    end
    subgraph dir_ansible_roles_power_manager_handlers [ansible/roles/power_manager/handlers]
        direction TB
        node_286["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_tasks [ansible/roles/power_manager/tasks]
        direction TB
        node_291["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_templates [ansible/roles/power_manager/templates]
        direction TB
        node_290["power-agent.service.j2"]
    end
    subgraph dir_ansible_roles_preflight_checks_tasks [ansible/roles/preflight_checks/tasks]
        direction TB
        node_339["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_files [ansible/roles/provisioning_api/files]
        direction TB
        node_226["provisioning_api.py"]
    end
    subgraph dir_ansible_roles_provisioning_api_handlers [ansible/roles/provisioning_api/handlers]
        direction TB
        node_225["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_tasks [ansible/roles/provisioning_api/tasks]
        direction TB
        node_228["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_templates [ansible/roles/provisioning_api/templates]
        direction TB
        node_227["provisioning-api.service.j2"]
    end
    subgraph dir_ansible_roles_pxe_server_defaults [ansible/roles/pxe_server/defaults]
        direction TB
        node_281["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_handlers [ansible/roles/pxe_server/handlers]
        direction TB
        node_280["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_tasks [ansible/roles/pxe_server/tasks]
        direction TB
        node_285["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_templates [ansible/roles/pxe_server/templates]
        direction TB
        node_282["boot.ipxe.j2"]
        node_284["dhcpd.conf.j2"]
        node_283["preseed.cfg.j2"]
    end
    subgraph dir_ansible_roles_python_deps_files [ansible/roles/python_deps/files]
        direction TB
        node_260["requirements.txt"]
    end
    subgraph dir_ansible_roles_python_deps_tasks [ansible/roles/python_deps/tasks]
        direction TB
        node_261["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_defaults [ansible/roles/semantic_router/defaults]
        direction TB
        node_134["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_tasks [ansible/roles/semantic_router/tasks]
        direction TB
        node_137["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_templates [ansible/roles/semantic_router/templates]
        direction TB
        node_135["Dockerfile.j2"]
        node_136["semantic-router.nomad.j2"]
    end
    subgraph dir_ansible_roles_sunshine_defaults [ansible/roles/sunshine/defaults]
        direction TB
        node_230["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_handlers [ansible/roles/sunshine/handlers]
        direction TB
        node_229["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_tasks [ansible/roles/sunshine/tasks]
        direction TB
        node_232["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_templates [ansible/roles/sunshine/templates]
        direction TB
        node_231["sunshine.nomad.j2"]
    end
    subgraph dir_ansible_roles_system_deps_tasks [ansible/roles/system_deps/tasks]
        direction TB
        node_152["main.yaml"]
    end
    subgraph dir_ansible_roles_tailscale_tasks [ansible/roles/tailscale/tasks]
        direction TB
        node_254["main.yaml"]
    end
    subgraph dir_ansible_roles_term_everything_tasks [ansible/roles/term_everything/tasks]
        direction TB
        node_292["main.yml"]
    end
    subgraph dir_ansible_roles_tool_server [ansible/roles/tool_server]
        direction TB
        node_300["Dockerfile"]
        node_298["app.py"]
        node_299["entrypoint.sh"]
        node_301["pmm_memory.py"]
        node_297["preload_models.py"]
    end
    subgraph dir_ansible_roles_tool_server_tasks [ansible/roles/tool_server/tasks]
        direction TB
        node_303["main.yaml"]
    end
    subgraph dir_ansible_roles_tool_server_templates [ansible/roles/tool_server/templates]
        direction TB
        node_302["tool_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_tool_server_tools [ansible/roles/tool_server/tools]
        direction TB
        node_308["ansible_tool.py"]
        node_312["archivist_tool.py"]
        node_317["claude_clone_tool.py"]
        node_319["code_runner_tool.py"]
        node_315["council_tool.py"]
        node_325["desktop_control_tool.py"]
        node_307["file_editor_tool.py"]
        node_324["final_answer_tool.py"]
        node_332["gemini_cli.py"]
        node_306["get_nomad_job.py"]
        node_304["git_tool.py"]
        node_310["ha_tool.py"]
        node_311["llxprt_code_tool.py"]
        node_330["mcp_tool.py"]
        node_318["opencode_tool.py"]
        node_313["orchestrator_tool.py"]
        node_329["planner_tool.py"]
        node_305["power_tool.py"]
        node_309["project_mapper_tool.py"]
        node_322["prompt_improver_tool.py"]
        node_316["rag_tool.py"]
        node_326["sandbox.ts"]
        node_328["shell_tool.py"]
        node_314["smol_agent_tool.py"]
        node_320["ssh_tool.py"]
        node_327["summarizer_tool.py"]
        node_321["swarm_tool.py"]
        node_333["tap_service.py"]
        node_331["term_everything_tool.py"]
        node_323["web_browser_tool.py"]
    end
    subgraph dir_ansible_roles_unified_fs_defaults [ansible/roles/unified_fs/defaults]
        direction TB
        node_245["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_files [ansible/roles/unified_fs/files]
        direction TB
        node_246["unified_fs_agent.py"]
    end
    subgraph dir_ansible_roles_unified_fs_handlers [ansible/roles/unified_fs/handlers]
        direction TB
        node_244["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_tasks [ansible/roles/unified_fs/tasks]
        direction TB
        node_248["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_templates [ansible/roles/unified_fs/templates]
        direction TB
        node_247["unified_fs.service.j2"]
    end
    subgraph dir_ansible_roles_vision_defaults [ansible/roles/vision/defaults]
        direction TB
        node_335["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_handlers [ansible/roles/vision/handlers]
        direction TB
        node_334["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_tasks [ansible/roles/vision/tasks]
        direction TB
        node_338["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_templates [ansible/roles/vision/templates]
        direction TB
        node_337["config.yml.j2"]
        node_336["vision.nomad.j2"]
    end
    subgraph dir_ansible_roles_vllm_tasks [ansible/roles/vllm/tasks]
        direction TB
        node_184["main.yaml"]
        node_185["run_single_vllm_job.yaml"]
    end
    subgraph dir_ansible_roles_vllm_templates [ansible/roles/vllm/templates]
        direction TB
        node_183["vllm-expert.nomad.j2"]
    end
    subgraph dir_ansible_roles_whisper_cpp_tasks [ansible/roles/whisper_cpp/tasks]
        direction TB
        node_186["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service [ansible/roles/world_model_service]
        direction TB
        node_138["world_model.nomad.j2"]
    end
    subgraph dir_ansible_roles_world_model_service_files [ansible/roles/world_model_service/files]
        direction TB
        node_142["Dockerfile"]
        node_141["app.py"]
        node_140["debug_world_model.sh"]
        node_139["requirements.txt"]
    end
    subgraph dir_ansible_roles_world_model_service_tasks [ansible/roles/world_model_service/tasks]
        direction TB
        node_143["main.yaml"]
    end
    subgraph dir_ansible_tasks [ansible/tasks]
        direction TB
        node_357["README.md"]
        node_358["build_pipecatapp_image.yaml"]
        node_360["create_expert_job.yaml"]
        node_361["deploy_expert_wrapper.yaml"]
        node_359["deploy_model_gpu_provider.yaml"]
    end
    subgraph dir_distributed_llama_repo [distributed-llama-repo]
        direction TB
        node_448["README.md"]
    end
    subgraph dir_docker [docker]
        direction TB
        node_411["README.md"]
    end
    subgraph dir_docker_dev_container [docker/dev_container]
        direction TB
        node_413["Dockerfile"]
    end
    subgraph dir_docker_memory_service [docker/memory_service]
        direction TB
        node_412["Dockerfile"]
    end
    subgraph dir_docs [docs]
        direction TB
        node_47["AGENTS.md"]
        node_59["ARCHITECTURE.md"]
        node_40["BENCHMARKING.MD"]
        node_50["DEPLOYMENT_AND_PROFILING.md"]
        node_54["EVALUATION_LLMROUTER.md"]
        node_43["FRONTEND_VERIFICATION.md"]
        node_46["FRONTIER_AGENT_ROADMAP.md"]
        node_42["GEMINI.md"]
        node_38["MCP_SERVER_SETUP.md"]
        node_39["MEMORIES.md"]
        node_45["NETWORK.md"]
        node_44["NIXOS_PXE_BOOT_SETUP.md"]
        node_58["PROJECT_SUMMARY.md"]
        node_49["PXE_BOOT_SETUP.md"]
        node_41["README.md"]
        node_56["REFACTOR_PROPOSAL_hybrid_architecture.md"]
        node_52["REMOTE_WORKFLOW.md"]
        node_51["TODO_Hybrid_Architecture.md"]
        node_48["TOOL_EVALUATION.md"]
        node_55["TROUBLESHOOTING.md"]
        node_57["VLLM_PROJECT_EVALUATION.md"]
        node_53["heretic_evaluation.md"]
    end
    subgraph dir_examples [examples]
        direction TB
        node_418["README.md"]
        node_419["chat-persistent.sh"]
    end
    subgraph dir_group_vars [group_vars]
        direction TB
        node_671["README.md"]
        node_672["all.yaml"]
        node_673["external_experts.yaml"]
        node_674["models.yaml"]
    end
    subgraph dir_host_vars [host_vars]
        direction TB
        node_410["README.md"]
        node_409["localhost.yaml"]
    end
    subgraph dir_initial_setup [initial-setup]
        direction TB
        node_545["README.md"]
        node_547["add_new_worker.sh"]
        node_548["setup.conf"]
        node_546["setup.sh"]
        node_549["update_inventory.sh"]
    end
    subgraph dir_initial_setup_modules [initial-setup/modules]
        direction TB
        node_554["01-network.sh"]
        node_556["02-hostname.sh"]
        node_552["03-user.sh"]
        node_555["04-ssh.sh"]
        node_557["05-auto-provision.sh"]
        node_553["README.md"]
    end
    subgraph dir_initial_setup_worker_setup [initial-setup/worker-setup]
        direction TB
        node_550["README.md"]
        node_551["setup.sh"]
    end
    subgraph dir_pipecat_agent_extension [pipecat-agent-extension]
        direction TB
        node_537["README.md"]
        node_540["example.ts"]
        node_538["gemini-extension.json"]
        node_539["package.json"]
        node_541["tsconfig.json"]
    end
    subgraph dir_pipecat_agent_extension_commands_pipecat [pipecat-agent-extension/commands/pipecat]
        direction TB
        node_542["send.toml"]
    end
    subgraph dir_pipecatapp [pipecatapp]
        direction TB
        node_581["Dockerfile"]
        node_566["README.md"]
        node_562["TODO.md"]
        node_570["__init__.py"]
        node_572["agent_factory.py"]
        node_564["api_keys.py"]
        node_576["app.py"]
        node_575["archivist_service.py"]
        node_583["durable_execution.py"]
        node_586["expert_tracker.py"]
        node_582["llm_clients.py"]
        node_585["manager_agent.py"]
        node_588["memory.py"]
        node_567["models.py"]
        node_571["moondream_detector.py"]
        node_558["net_utils.py"]
        node_584["pmm_memory.py"]
        node_580["pmm_memory_client.py"]
        node_578["quality_control.py"]
        node_561["rate_limiter.py"]
        node_560["requirements.txt"]
        node_568["security.py"]
        node_569["start_archivist.sh"]
        node_579["task_supervisor.py"]
        node_573["technician_agent.py"]
        node_565["test_memory.py"]
        node_559["test_moondream_detector.py"]
        node_577["test_server.py"]
        node_587["tool_server.py"]
        node_563["web_server.py"]
        node_574["worker_agent.py"]
    end
    subgraph dir_pipecatapp_datasets [pipecatapp/datasets]
        direction TB
        node_599["sycophancy_prompts.json"]
    end
    subgraph dir_pipecatapp_memory_graph_service [pipecatapp/memory_graph_service]
        direction TB
        node_633["Dockerfile"]
        node_632["server.py"]
    end
    subgraph dir_pipecatapp_nomad_templates [pipecatapp/nomad_templates]
        direction TB
        node_630["immich.nomad.hcl"]
        node_628["readeck.nomad.hcl"]
        node_629["uptime-kuma.nomad.hcl"]
        node_631["vaultwarden.nomad.hcl"]
    end
    subgraph dir_pipecatapp_prompts [pipecatapp/prompts]
        direction TB
        node_614["coding_expert.txt"]
        node_615["creative_expert.txt"]
        node_613["router.txt"]
        node_612["tron_agent.txt"]
    end
    subgraph dir_pipecatapp_static [pipecatapp/static]
        direction TB
        node_594["cluster.html"]
        node_593["cluster_viz.html"]
        node_589["index.html"]
        node_592["terminal.js"]
        node_591["vr_index.html"]
        node_590["workflow.html"]
    end
    subgraph dir_pipecatapp_static_css [pipecatapp/static/css]
        direction TB
        node_598["litegraph.css"]
    end
    subgraph dir_pipecatapp_static_js [pipecatapp/static/js]
        direction TB
        node_596["editor.js"]
        node_595["litegraph.js"]
        node_597["workflow.js"]
    end
    subgraph dir_pipecatapp_tests [pipecatapp/tests]
        direction TB
        node_617["test_audio_streamer.py"]
        node_623["test_metrics_cache.py"]
        node_622["test_net_utils.py"]
        node_621["test_piper_async.py"]
        node_619["test_rate_limiter.py"]
        node_616["test_stt_optimization.py"]
        node_618["test_web_server_unit.py"]
        node_620["test_websocket_security.py"]
    end
    subgraph dir_pipecatapp_tests_workflow [pipecatapp/tests/workflow]
        direction TB
        node_624["test_history.py"]
    end
    subgraph dir_pipecatapp_tools [pipecatapp/tools]
        direction TB
        node_649["__init__.py"]
        node_640["ansible_tool.py"]
        node_646["archivist_tool.py"]
        node_653["claude_clone_tool.py"]
        node_656["code_runner_tool.py"]
        node_650["council_tool.py"]
        node_643["dependency_scanner_tool.py"]
        node_662["desktop_control_tool.py"]
        node_639["file_editor_tool.py"]
        node_661["final_answer_tool.py"]
        node_669["gemini_cli.py"]
        node_637["get_nomad_job.py"]
        node_634["git_tool.py"]
        node_642["ha_tool.py"]
        node_645["llxprt_code_tool.py"]
        node_667["mcp_tool.py"]
        node_654["open_workers_tool.py"]
        node_655["opencode_tool.py"]
        node_647["orchestrator_tool.py"]
        node_666["planner_tool.py"]
        node_635["power_tool.py"]
        node_641["project_mapper_tool.py"]
        node_659["prompt_improver_tool.py"]
        node_652["rag_tool.py"]
        node_636["remote_tool_proxy.py"]
        node_663["sandbox.ts"]
        node_665["shell_tool.py"]
        node_648["smol_agent_tool.py"]
        node_657["ssh_tool.py"]
        node_664["summarizer_tool.py"]
        node_658["swarm_tool.py"]
        node_670["tap_service.py"]
        node_668["term_everything_tool.py"]
        node_638["test_code_runner_tool.py"]
        node_644["test_ssh_tool.py"]
        node_651["vr_tool.py"]
        node_660["web_browser_tool.py"]
    end
    subgraph dir_pipecatapp_workflow [pipecatapp/workflow]
        direction TB
        node_600["__init__.py"]
        node_601["context.py"]
        node_603["history.py"]
        node_602["node.py"]
        node_604["runner.py"]
    end
    subgraph dir_pipecatapp_workflow_nodes [pipecatapp/workflow/nodes]
        direction TB
        node_607["__init__.py"]
        node_608["base_nodes.py"]
        node_611["emperor_nodes.py"]
        node_609["llm_nodes.py"]
        node_606["registry.py"]
        node_610["system_nodes.py"]
        node_605["tool_nodes.py"]
    end
    subgraph dir_pipecatapp_workflows [pipecatapp/workflows]
        direction TB
        node_626["default_agent_loop.yaml"]
        node_627["poc_ensemble.yaml"]
        node_625["tiered_agent_loop.yaml"]
    end
    subgraph dir_playbooks [playbooks]
        direction TB
        node_370["README.md"]
        node_385["benchmark_single_model.yaml"]
        node_376["cluster_status.yaml"]
        node_369["common_setup.yaml"]
        node_388["controller.yaml"]
        node_366["debug_template.yaml"]
        node_379["deploy_app.yaml"]
        node_371["deploy_expert.yaml"]
        node_367["deploy_prompt_evolution.yaml"]
        node_364["developer_tools.yaml"]
        node_374["diagnose_and_log_home_assistant.yaml"]
        node_372["diagnose_failure.yaml"]
        node_362["diagnose_home_assistant.yaml"]
        node_378["fix_cluster.yaml"]
        node_373["heal_cluster.yaml"]
        node_363["heal_job.yaml"]
        node_386["health_check.yaml"]
        node_381["promote_controller.yaml"]
        node_384["promote_to_controller.yaml"]
        node_380["pxe_setup.yaml"]
        node_383["redeploy_pipecat.yaml"]
        node_377["run_config_manager.yaml"]
        node_365["run_consul.yaml"]
        node_375["run_ha_diag.yaml"]
        node_387["run_health_check.yaml"]
        node_368["status-check.yaml"]
        node_382["wake.yaml"]
        node_389["worker.yaml"]
    end
    subgraph dir_playbooks_network [playbooks/network]
        direction TB
        node_392["mesh.yaml"]
        node_391["verify.yaml"]
    end
    subgraph dir_playbooks_ops [playbooks/ops]
        direction TB
        node_390["optimize_memory.yaml"]
    end
    subgraph dir_playbooks_preflight [playbooks/preflight]
        direction TB
        node_393["checks.yaml"]
    end
    subgraph dir_playbooks_services [playbooks/services]
        direction TB
        node_395["README.md"]
        node_402["ai_experts.yaml"]
        node_405["app_services.yaml"]
        node_404["consul.yaml"]
        node_394["core_ai_services.yaml"]
        node_403["core_infra.yaml"]
        node_401["docker.yaml"]
        node_399["final_verification.yaml"]
        node_398["model_services.yaml"]
        node_406["monitoring.yaml"]
        node_407["nomad.yaml"]
        node_397["nomad_client.yaml"]
        node_400["streaming_services.yaml"]
        node_396["training_services.yaml"]
    end
    subgraph dir_playbooks_services_tasks [playbooks/services/tasks]
        direction TB
        node_408["diagnose_home_assistant.yaml"]
    end
    subgraph dir_prompt_engineering [prompt_engineering]
        direction TB
        node_73["PROMPT_ENGINEERING.md"]
        node_68["README.md"]
        node_74["challenger.py"]
        node_67["create_evaluator.py"]
        node_76["evaluation_lib.py"]
        node_72["evaluator.py"]
        node_71["evolve.py"]
        node_66["promote_agent.py"]
        node_70["requirements-dev.txt"]
        node_69["run_campaign.py"]
        node_75["visualize_archive.py"]
    end
    subgraph dir_prompt_engineering_agents [prompt_engineering/agents]
        direction TB
        node_89["ADAPTATION_AGENT.md"]
        node_88["EVALUATOR_GENERATOR.md"]
        node_83["README.md"]
        node_85["architecture_review.md"]
        node_87["code_clean_up.md"]
        node_86["debug_and_analysis.md"]
        node_82["new_task_review.md"]
        node_84["problem_scope_framing.md"]
    end
    subgraph dir_prompt_engineering_archive [prompt_engineering/archive]
        direction TB
        node_90["agent_0.json"]
        node_97["agent_0.py"]
        node_93["agent_1.json"]
        node_91["agent_1.py"]
        node_92["agent_2.json"]
        node_95["agent_2.py"]
        node_94["agent_3.json"]
        node_96["agent_3.py"]
    end
    subgraph dir_prompt_engineering_evaluation_suite [prompt_engineering/evaluation_suite]
        direction TB
        node_80["README.md"]
        node_81["test_vision.yaml"]
    end
    subgraph dir_prompt_engineering_frontend [prompt_engineering/frontend]
        direction TB
        node_77["index.html"]
        node_78["server.py"]
    end
    subgraph dir_prompt_engineering_generated_evaluators [prompt_engineering/generated_evaluators]
        direction TB
        node_79[".gitignore"]
    end
    subgraph dir_prompts [prompts]
        direction TB
        node_446["README.md"]
        node_447["chat-with-bob.txt"]
        node_445["router.txt"]
    end
    subgraph dir_reflection [reflection]
        direction TB
        node_415["README.md"]
        node_416["adaptation_manager.py"]
        node_414["create_reflection.py"]
        node_417["reflect.py"]
    end
    subgraph dir_scripts [scripts]
        direction TB
        node_427["README.md"]
        node_424["ansible_diff.sh"]
        node_441["ci_ansible_check.sh"]
        node_437["cleanup.sh"]
        node_436["compare_exo_llama.py"]
        node_429["create_cynic_model.sh"]
        node_426["debug_mesh.sh"]
        node_440["fix_markdown.sh"]
        node_433["fix_verification_failures.sh"]
        node_422["fix_yaml.sh"]
        node_425["generate_file_map.py"]
        node_428["healer.py"]
        node_435["lint.sh"]
        node_438["lint_exclude.txt"]
        node_431["memory_audit.py"]
        node_430["profile_resources.sh"]
        node_432["prune_consul_services.py"]
        node_421["run_quibbler.sh"]
        node_439["test_playbooks_dry_run.sh"]
        node_434["test_playbooks_live_run.sh"]
        node_442["uninstall.sh"]
        node_423["verify_consul_attributes.sh"]
    end
    subgraph dir_scripts_debug [scripts/debug]
        direction TB
        node_444["README.md"]
        node_443["test_mqtt_connection.py"]
    end
    subgraph dir_tests [tests]
        direction TB
        node_449["README.md"]
        node_450["__init__.py"]
        node_452["test_agent_patterns.py"]
        node_451["test_emperor_node.py"]
    end
    subgraph dir_tests_e2e [tests/e2e]
        direction TB
        node_455["README.md"]
        node_456["__init__.py"]
        node_453["test_api.py"]
        node_458["test_intelligent_routing.py"]
        node_460["test_mission_control.py"]
        node_457["test_palette_command_history.py"]
        node_459["test_palette_ux.py"]
        node_454["test_regression.py"]
    end
    subgraph dir_tests_integration [tests/integration]
        direction TB
        node_474["README.md"]
        node_476["__init__.py"]
        node_481["stub_services.py"]
        node_479["test_consul_role.yaml"]
        node_477["test_home_assistant.yaml"]
        node_475["test_mini_pipeline.py"]
        node_473["test_mqtt_exporter.py"]
        node_472["test_nomad_role.yaml"]
        node_478["test_pipecat_app.py"]
        node_480["test_preemption.py"]
    end
    subgraph dir_tests_integration_roles_test_home_assistant_tasks [tests/integration/roles/test_home_assistant/tasks]
        direction TB
        node_482["main.yaml"]
    end
    subgraph dir_tests_playbooks [tests/playbooks]
        direction TB
        node_463["e2e-tests.yaml"]
        node_461["test_consul.yaml"]
        node_462["test_llama_cpp.yaml"]
        node_464["test_nomad.yaml"]
    end
    subgraph dir_tests_scripts [tests/scripts]
        direction TB
        node_471["run_unit_tests.sh"]
        node_470["test_distributed_llama.sh"]
        node_469["test_duplicate_role_execution.sh"]
        node_468["test_paddler.sh"]
        node_467["test_piper.sh"]
        node_465["test_run.sh"]
        node_466["verify_components.py"]
    end
    subgraph dir_tests_unit [tests/unit]
        direction TB
        node_496["README.md"]
        node_501["__init__.py"]
        node_510["conftest.py"]
        node_486["test_adaptation_manager.py"]
        node_525["test_agent_definitions.py"]
        node_506["test_ansible_tool.py"]
        node_495["test_archivist_tool.py"]
        node_509["test_claude_clone_tool.py"]
        node_485["test_code_runner_tool.py"]
        node_507["test_council_tool.py"]
        node_502["test_dependency_scanner.py"]
        node_523["test_desktop_control_tool.py"]
        node_497["test_file_editor_security.py"]
        node_504["test_file_editor_tool.py"]
        node_514["test_final_answer_tool.py"]
        node_531["test_gemini_cli.py"]
        node_519["test_get_nomad_job.py"]
        node_524["test_git_tool.py"]
        node_513["test_ha_tool.py"]
        node_498["test_home_assistant_template.py"]
        node_526["test_infrastructure.py"]
        node_520["test_lint_script.py"]
        node_530["test_llxprt_code_tool.py"]
        node_503["test_mcp_tool.py"]
        node_488["test_mqtt_template.py"]
        node_499["test_open_workers_tool.py"]
        node_535["test_opencode_tool.py"]
        node_505["test_orchestrator_tool.py"]
        node_494["test_pipecat_app_unit.py"]
        node_532["test_planner_tool.py"]
        node_516["test_playbook_integration.py"]
        node_527["test_poc_ensemble.py"]
        node_517["test_power_tool.py"]
        node_512["test_project_mapper_tool.py"]
        node_493["test_prompt_engineering.py"]
        node_521["test_prompt_improver_tool.py"]
        node_484["test_provisioning.py"]
        node_529["test_rag_tool.py"]
        node_483["test_reflection.py"]
        node_500["test_security.py"]
        node_515["test_shell_tool.py"]
        node_522["test_simple_llm_node.py"]
        node_491["test_smol_agent_tool.py"]
        node_490["test_ssh_tool.py"]
        node_489["test_summarizer_tool.py"]
        node_492["test_supervisor.py"]
        node_508["test_swarm_tool.py"]
        node_528["test_tap_service.py"]
        node_487["test_term_everything_tool.py"]
        node_511["test_vision_failover.py"]
        node_518["test_web_browser_tool.py"]
        node_534["test_workflow.py"]
        node_533["test_world_model_service.py"]
    end
    subgraph dir_verification [verification]
        direction TB
        node_37["save_success.png"]
        node_36["verify_workflow_save.py"]
    end
    subgraph dir_workflows [workflows]
        direction TB
        node_536["default_agent_loop.yaml"]
    end

    node_405 --> node_176
    node_39 --> node_106
    node_51 --> node_228
    node_400 --> node_231
    node_356 --> node_156
    node_54 --> node_536
    node_197 --> node_196
    node_589 --> node_77
    node_39 --> node_561
    node_9 --> node_7
    node_241 --> node_335
    node_373 --> node_334
    node_405 --> node_225
    node_373 --> node_267
    node_303 --> node_299
    node_16 --> node_509
    node_298 --> node_308
    node_29 --> node_381
    node_134 --> node_163
    node_379 --> node_347
    node_401 --> node_209
    node_51 --> node_271
    node_42 --> node_387
    node_134 --> node_281
    node_527 --> node_604
    node_17 --> node_115
    node_51 --> node_128
    node_17 --> node_22
    node_17 --> node_410
    node_71 --> node_141
    node_576 --> node_610
    node_17 --> node_249
    node_389 --> node_398
    node_44 --> node_166
    node_566 --> node_563
    node_51 --> node_134
    node_658 --> node_574
    node_137 --> node_145
    node_394 --> node_178
    node_308 --> node_31
    node_17 --> node_266
    node_22 --> node_399
    node_17 --> node_293
    node_51 --> node_370
    node_241 --> node_224
    node_14 --> node_424
    node_404 --> node_161
    node_105 --> node_107
    node_35 --> node_179
    node_412 --> node_588
    node_241 --> node_199
    node_441 --> node_439
    node_137 --> node_228
    node_475 --> node_141
    node_120 --> node_177
    node_7 --> node_298
    node_22 --> node_396
    node_373 --> node_184
    node_51 --> node_268
    node_226 --> node_562
    node_514 --> node_661
    node_134 --> node_280
    node_16 --> node_523
    node_39 --> node_52
    node_300 --> node_297
    node_398 --> node_204
    node_352 --> node_558
    node_39 --> node_550
    node_172 --> node_168
    node_241 --> node_291
    node_4 --> node_235
    node_395 --> node_402
    node_572 --> node_318
    node_373 --> node_293
    node_134 --> node_253
    node_160 --> node_157
    node_464 --> node_170
    node_572 --> node_662
    node_137 --> node_271
    node_326 --> node_663
    node_388 --> node_403
    node_39 --> node_31
    node_462 --> node_211
    node_137 --> node_202
    node_401 --> node_212
    node_39 --> node_235
    node_39 --> node_352
    node_39 --> node_276
    node_373 --> node_122
    node_576 --> node_604
    node_137 --> node_128
    node_587 --> node_647
    node_373 --> node_150
    node_407 --> node_172
    node_4 --> node_198
    node_145 --> node_185
    node_56 --> node_51
    node_512 --> node_543
    node_17 --> node_39
    node_51 --> node_671
    node_19 --> node_562
    node_238 --> node_237
    node_359 --> node_159
    node_648 --> node_663
    node_644 --> node_657
    node_7 --> node_415
    node_383 --> node_341
    node_137 --> node_134
    node_577 --> node_564
    node_39 --> node_455
    node_7 --> node_388
    node_288 --> node_632
    node_425 --> node_581
    node_44 --> node_335
    node_39 --> node_198
    node_39 --> node_256
    node_574 --> node_572
    node_356 --> node_228
    node_4 --> node_216
    node_241 --> node_340
    node_607 --> node_608
    node_241 --> node_263
    node_220 --> node_158
    node_417 --> node_416
    node_4 --> node_254
    node_51 --> node_238
    node_462 --> node_146
    node_137 --> node_268
    node_496 --> node_316
    node_16 --> node_506
    node_458 --> node_179
    node_474 --> node_576
    node_444 --> node_443
    node_502 --> node_319
    node_62 --> node_20
    node_51 --> node_270
    node_39 --> node_216
    node_44 --> node_233
    node_39 --> node_219
    node_405 --> node_255
    node_404 --> node_162
    node_415 --> node_416
    node_356 --> node_143
    node_365 --> node_673
    node_512 --> node_16
    node_67 --> node_179
    node_512 --> node_68
    node_356 --> node_271
    node_392 --> node_254
    node_17 --> node_156
    node_39 --> node_545
    node_425 --> node_251
    node_356 --> node_202
    node_134 --> node_173
    node_381 --> node_167
    node_51 --> node_165
    node_576 --> node_667
    node_44 --> node_126
    node_44 --> node_224
    node_587 --> node_635
    node_352 --> node_588
    node_51 --> node_342
    node_39 --> node_223
    node_17 --> node_415
    node_671 --> node_674
    node_17 --> node_388
    node_548 --> node_556
    node_298 --> node_660
    node_51 --> node_160
    node_27 --> node_563
    node_134 --> node_482
    node_241 --> node_272
    node_44 --> node_291
    node_373 --> node_163
    node_255 --> node_170
    node_576 --> node_608
    node_402 --> node_359
    node_172 --> node_277
    node_4 --> node_312
    node_427 --> node_106
    node_9 --> node_357
    node_51 --> node_182
    node_83 --> node_86
    node_241 --> node_225
    node_241 --> node_352
    node_73 --> node_179
    node_398 --> node_673
    node_356 --> node_268
    node_465 --> node_419
    node_137 --> node_238
    node_406 --> node_193
    node_182 --> node_412
    node_425 --> node_175
    node_39 --> node_67
    node_41 --> node_47
    node_9 --> node_62
    node_7 --> node_110
    node_137 --> node_270
    node_51 --> node_186
    node_51 --> node_7
    node_120 --> node_199
    node_39 --> node_353
    node_577 --> node_576
    node_49 --> node_284
    node_308 --> node_33
    node_566 --> node_577
    node_17 --> node_385
    node_414 --> node_3
    node_4 --> node_232
    node_391 --> node_426
    node_352 --> node_342
    node_137 --> node_165
    node_44 --> node_340
    node_7 --> node_463
    node_373 --> node_280
    node_44 --> node_263
    node_39 --> node_413
    node_388 --> node_406
    node_20 --> node_70
    node_241 --> node_219
    node_566 --> node_260
    node_120 --> node_287
    node_120 --> node_154
    node_27 --> node_587
    node_51 --> node_229
    node_16 --> node_485
    node_9 --> node_117
    node_137 --> node_160
    node_39 --> node_218
    node_16 --> node_647
    node_373 --> node_672
    node_579 --> node_574
    node_137 --> node_182
    node_4 --> node_275
    node_356 --> node_238
    node_576 --> node_656
    node_241 --> node_223
    node_465 --> node_447
    node_488 --> node_278
    node_356 --> node_270
    node_39 --> node_341
    node_39 --> node_594
    node_394 --> node_217
    node_557 --> node_548
    node_484 --> node_32
    node_134 --> node_338
    node_438 --> node_77
    node_39 --> node_275
    node_36 --> node_590
    node_137 --> node_186
    node_400 --> node_230
    node_17 --> node_228
    node_143 --> node_413
    node_572 --> node_643
    node_4 --> node_259
    node_289 --> node_288
    node_39 --> node_285
    node_379 --> node_342
    node_405 --> node_334
    node_356 --> node_165
    node_134 --> node_172
    node_373 --> node_145
    node_44 --> node_225
    node_496 --> node_640
    node_4 --> node_146
    node_44 --> node_352
    node_17 --> node_143
    node_425 --> node_589
    node_373 --> node_228
    node_425 --> node_8
    node_17 --> node_271
    node_17 --> node_202
    node_406 --> node_194
    node_560 --> node_12
    node_137 --> node_229
    node_17 --> node_383
    node_401 --> node_215
    node_487 --> node_668
    node_4 --> node_300
    node_16 --> node_635
    node_373 --> node_173
    node_22 --> node_406
    node_425 --> node_68
    node_534 --> node_604
    node_105 --> node_110
    node_241 --> node_211
    node_425 --> node_566
    node_39 --> node_448
    node_461 --> node_158
    node_577 --> node_298
    node_266 --> node_265
    node_120 --> node_272
    node_411 --> node_413
    node_356 --> node_186
    node_120 --> node_277
    node_462 --> node_212
    node_4 --> node_221
    node_39 --> node_15
    node_373 --> node_128
    node_512 --> node_537
    node_576 --> node_174
    node_9 --> node_550
    node_204 --> node_103
    node_241 --> node_218
    node_44 --> node_219
    node_512 --> node_641
    node_17 --> node_268
    node_373 --> node_134
    node_356 --> node_243
    node_464 --> node_172
    node_65 --> node_13
    node_22 --> node_400
    node_155 --> node_153
    node_41 --> node_45
    node_60 --> node_64
    node_211 --> node_210
    node_462 --> node_167
    node_553 --> node_551
    node_42 --> node_20
    node_572 --> node_668
    node_120 --> node_354
    node_39 --> node_372
    node_7 --> node_551
    node_576 --> node_659
    node_7 --> node_381
    node_241 --> node_341
    node_352 --> node_445
    node_611 --> node_606
    node_405 --> node_162
    node_44 --> node_223
    node_464 --> node_165
    node_464 --> node_169
    node_585 --> node_572
    node_134 --> node_230
    node_356 --> node_229
    node_545 --> node_548
    node_241 --> node_250
    node_9 --> node_455
    node_405 --> node_292
    node_137 --> node_142
    node_7 --> node_537
    node_399 --> node_170
    node_563 --> node_593
    node_300 --> node_141
    node_51 --> node_335
    node_403 --> node_152
    node_566 --> node_412
    node_51 --> node_357
    node_134 --> node_152
    node_412 --> node_180
    node_39 --> node_560
    node_425 --> node_98
    node_425 --> node_23
    node_405 --> node_141
    node_120 --> node_222
    node_120 --> node_241
    node_640 --> node_31
    node_462 --> node_156
    node_389 --> node_402
    node_241 --> node_296
    node_425 --> node_474
    node_516 --> node_22
    node_504 --> node_307
    node_637 --> node_306
    node_241 --> node_294
    node_556 --> node_548
    node_576 --> node_650
    node_51 --> node_233
    node_359 --> node_161
    node_51 --> node_418
    node_17 --> node_384
    node_47 --> node_560
    node_576 --> node_311
    node_553 --> node_556
    node_39 --> node_667
    node_381 --> node_157
    node_9 --> node_545
    node_298 --> node_313
    node_300 --> node_298
    node_576 --> node_308
    node_17 --> node_270
    node_651 --> node_563
    node_17 --> node_381
    node_22 --> node_392
    node_42 --> node_576
    node_4 --> node_236
    node_50 --> node_113
    node_425 --> node_446
    node_59 --> node_563
    node_576 --> node_558
    node_4 --> node_209
    node_16 --> node_456
    node_51 --> node_126
    node_356 --> node_166
    node_59 --> node_4
    node_440 --> node_539
    node_563 --> node_558
    node_19 --> node_300
    node_446 --> node_447
    node_298 --> node_180
    node_17 --> node_537
    node_120 --> node_232
    node_373 --> node_238
    node_587 --> node_657
    node_644 --> node_320
    node_4 --> node_249
    node_42 --> node_22
    node_51 --> node_291
    node_51 --> node_117
    node_44 --> node_218
    node_137 --> node_335
    node_373 --> node_172
    node_425 --> node_21
    node_463 --> node_477
    node_405 --> node_337
    node_120 --> node_261
    node_4 --> node_127
    node_39 --> node_150
    node_56 --> node_300
    node_179 --> node_584
    node_425 --> node_427
    node_440 --> node_25
    node_576 --> node_317
    node_241 --> node_334
    node_4 --> node_266
    node_241 --> node_267
    node_365 --> node_158
    node_197 --> node_188
    node_255 --> node_165
    node_373 --> node_165
    node_255 --> node_169
    node_44 --> node_341
    node_39 --> node_581
    node_220 --> node_156
    node_394 --> node_344
    node_120 --> node_211
    node_137 --> node_233
    node_17 --> node_368
    node_275 --> node_273
    node_352 --> node_575
    node_134 --> node_177
    node_405 --> node_175
    node_512 --> node_449
    node_9 --> node_353
    node_44 --> node_250
    node_587 --> node_310
    node_261 --> node_560
    node_572 --> node_314
    node_44 --> node_285
    node_537 --> node_541
    node_566 --> node_582
    node_402 --> node_156
    node_373 --> node_160
    node_25 --> node_435
    node_4 --> node_201
    node_17 --> node_7
    node_405 --> node_333
    node_572 --> node_304
    node_638 --> node_656
    node_4 --> node_251
    node_4 --> node_633
    node_373 --> node_182
    node_47 --> node_141
    node_137 --> node_126
    node_126 --> node_123
    node_60 --> node_63
    node_134 --> node_240
    node_553 --> node_555
    node_44 --> node_296
    node_512 --> node_105
    node_410 --> node_409
    node_586 --> node_632
    node_17 --> node_243
    node_39 --> node_303
    node_572 --> node_636
    node_394 --> node_181
    node_405 --> node_307
    node_356 --> node_335
    node_608 --> node_606
    node_44 --> node_294
    node_405 --> node_174
    node_39 --> node_656
    node_137 --> node_291
    node_7 --> node_674
    node_120 --> node_146
    node_241 --> node_184
    node_7 --> node_449
    node_373 --> node_186
    node_352 --> node_106
    node_143 --> node_581
    node_226 --> node_22
    node_4 --> node_281
    node_17 --> node_229
    node_425 --> node_24
    node_352 --> node_612
    node_616 --> node_179
    node_39 --> node_179
    node_352 --> node_561
    node_39 --> node_498
    node_241 --> node_293
    node_417 --> node_306
    node_356 --> node_233
    node_39 --> node_163
    node_496 --> node_486
    node_42 --> node_298
    node_617 --> node_179
    node_566 --> node_78
    node_439 --> node_404
    node_39 --> node_363
    node_288 --> node_78
    node_555 --> node_546
    node_587 --> node_319
    node_7 --> node_105
    node_572 --> node_667
    node_241 --> node_122
    node_150 --> node_147
    node_439 --> node_394
    node_241 --> node_150
    node_4 --> node_139
    node_203 --> node_204
    node_17 --> node_382
    node_564 --> node_568
    node_120 --> node_178
    node_462 --> node_215
    node_122 --> node_125
    node_4 --> node_118
    node_356 --> node_126
    node_120 --> node_262
    node_356 --> node_224
    node_572 --> node_655
    node_576 --> node_331
    node_39 --> node_175
    node_56 --> node_576
    node_143 --> node_251
    node_585 --> node_321
    node_439 --> node_398
    node_4 --> node_279
    node_4 --> node_66
    node_590 --> node_595
    node_51 --> node_235
    node_51 --> node_276
    node_587 --> node_325
    node_640 --> node_33
    node_591 --> node_598
    node_6 --> node_179
    node_303 --> node_297
    node_283 --> node_551
    node_491 --> node_648
    node_44 --> node_267
    node_444 --> node_140
    node_576 --> node_653
    node_395 --> node_401
    node_356 --> node_291
    node_411 --> node_581
    node_51 --> node_455
    node_405 --> node_228
    node_179 --> node_301
    node_143 --> node_179
    node_576 --> node_660
    node_4 --> node_208
    node_596 --> node_626
    node_533 --> node_179
    node_39 --> node_280
    node_51 --> node_198
    node_17 --> node_166
    node_17 --> node_377
    node_51 --> node_256
    node_163 --> node_560
    node_429 --> node_599
    node_4 --> node_658
    node_150 --> node_148
    node_405 --> node_173
    node_9 --> node_448
    node_394 --> node_182
    node_16 --> node_657
    node_365 --> node_161
    node_405 --> node_308
    node_587 --> node_664
    node_39 --> node_253
    node_17 --> node_105
    node_4 --> node_339
    node_39 --> node_672
    node_527 --> node_627
    node_60 --> node_214
    node_51 --> node_216
    node_253 --> node_300
    node_51 --> node_219
    node_435 --> node_438
    node_7 --> node_30
    node_19 --> node_251
    node_19 --> node_633
    node_512 --> node_395
    node_143 --> node_139
    node_51 --> node_545
    node_44 --> node_184
    node_35 --> node_405
    node_467 --> node_3
    node_356 --> node_340
    node_356 --> node_263
    node_59 --> node_417
    node_39 --> node_613
    node_145 --> node_144
    node_47 --> node_672
    node_381 --> node_166
    node_137 --> node_235
    node_137 --> node_276
    node_172 --> node_170
    node_241 --> node_163
    node_187 --> node_672
    node_56 --> node_633
    node_4 --> node_286
    node_16 --> node_310
    node_58 --> node_416
    node_405 --> node_317
    node_672 --> node_674
    node_506 --> node_640
    node_396 --> node_269
    node_72 --> node_113
    node_455 --> node_458
    node_352 --> node_626
    node_314 --> node_326
    node_572 --> node_648
    node_572 --> node_656
    node_39 --> node_289
    node_44 --> node_122
    node_576 --> node_330
    node_137 --> node_198
    node_137 --> node_256
    node_658 --> node_573
    node_44 --> node_150
    node_134 --> node_154
    node_418 --> node_419
    node_16 --> node_518
    node_120 --> node_249
    node_8 --> node_22
    node_405 --> node_226
    node_373 --> node_240
    node_399 --> node_165
    node_593 --> node_595
    node_399 --> node_169
    node_17 --> node_335
    node_394 --> node_348
    node_4 --> node_493
    node_425 --> node_0
    node_383 --> node_342
    node_587 --> node_305
    node_39 --> node_173
    node_512 --> node_80
    node_56 --> node_298
    node_4 --> node_137
    node_137 --> node_216
    node_39 --> node_308
    node_137 --> node_219
    node_27 --> node_78
    node_241 --> node_280
    node_51 --> node_353
    node_39 --> node_566
    node_120 --> node_293
    node_399 --> node_160
    node_545 --> node_554
    node_356 --> node_352
    node_220 --> node_157
    node_39 --> node_128
    node_39 --> node_482
    node_303 --> node_300
    node_4 --> node_463
    node_137 --> node_223
    node_576 --> node_328
    node_39 --> node_134
    node_266 --> node_264
    node_425 --> node_444
    node_4 --> node_203
    node_17 --> node_224
    node_356 --> node_256
    node_16 --> node_325
    node_17 --> node_199
    node_352 --> node_351
    node_373 --> node_233
    node_363 --> node_141
    node_512 --> node_539
    node_211 --> node_209
    node_100 --> node_144
    node_566 --> node_571
    node_589 --> node_175
    node_403 --> node_147
    node_563 --> node_77
    node_66 --> node_179
    node_17 --> node_291
    node_9 --> node_63
    node_226 --> node_4
    node_405 --> node_331
    node_572 --> node_651
    node_512 --> node_83
    node_39 --> node_18
    node_44 --> node_163
    node_51 --> node_341
    node_373 --> node_126
    node_338 --> node_336
    node_356 --> node_219
    node_241 --> node_145
    node_68 --> node_73
    node_277 --> node_167
    node_51 --> node_275
    node_512 --> node_25
    node_39 --> node_98
    node_572 --> node_659
    node_364 --> node_223
    node_16 --> node_664
    node_512 --> node_121
    node_51 --> node_285
    node_241 --> node_228
    node_39 --> node_474
    node_356 --> node_223
    node_83 --> node_82
    node_400 --> node_232
    node_405 --> node_160
    node_537 --> node_540
    node_496 --> node_668
    node_134 --> node_254
    node_7 --> node_550
    node_137 --> node_413
    node_19 --> node_4
    node_403 --> node_148
    node_105 --> node_103
    node_4 --> node_338
    node_425 --> node_562
    node_7 --> node_83
    node_587 --> node_320
    node_54 --> node_626
    node_381 --> node_168
    node_379 --> node_351
    node_17 --> node_340
    node_120 --> node_156
    node_17 --> node_263
    node_4 --> node_157
    node_425 --> node_395
    node_392 --> node_273
    node_241 --> node_271
    node_39 --> node_446
    node_194 --> node_191
    node_16 --> node_327
    node_44 --> node_280
    node_253 --> node_251
    node_253 --> node_633
    node_563 --> node_567
    node_241 --> node_128
    node_39 --> node_338
    node_51 --> node_448
    node_388 --> node_404
    node_398 --> node_251
    node_54 --> node_609
    node_211 --> node_212
    node_7 --> node_455
    node_569 --> node_575
    node_241 --> node_134
    node_44 --> node_253
    node_424 --> node_32
    node_303 --> node_576
    node_137 --> node_341
    node_39 --> node_172
    node_44 --> node_672
    node_493 --> node_179
    node_572 --> node_308
    node_137 --> node_275
    node_315 --> node_672
    node_39 --> node_427
    node_511 --> node_179
    node_83 --> node_89
    node_19 --> node_463
    node_137 --> node_285
    node_512 --> node_411
    node_16 --> node_305
    node_576 --> node_313
    node_17 --> node_550
    node_485 --> node_656
    node_405 --> node_330
    node_516 --> node_32
    node_16 --> node_576
    node_462 --> node_166
    node_492 --> node_18
    node_672 --> node_185
    node_298 --> node_304
    node_41 --> node_52
    node_17 --> node_83
    node_83 --> node_88
    node_406 --> node_187
    node_575 --> node_558
    node_316 --> node_301
    node_425 --> node_80
    node_4 --> node_260
    node_221 --> node_167
    node_17 --> node_225
    node_572 --> node_317
    node_51 --> node_636
    node_356 --> node_218
    node_576 --> node_180
    node_182 --> node_141
    node_44 --> node_145
    node_17 --> node_352
    node_515 --> node_328
    node_397 --> node_167
    node_298 --> node_642
    node_134 --> node_232
    node_493 --> node_66
    node_20 --> node_546
    node_17 --> node_455
    node_7 --> node_411
    node_39 --> node_440
    node_356 --> node_341
    node_39 --> node_586
    node_466 --> node_140
    node_9 --> node_60
    node_133 --> node_130
    node_44 --> node_173
    node_255 --> node_276
    node_22 --> node_364
    node_373 --> node_235
    node_373 --> node_276
    node_303 --> node_633
    node_405 --> node_328
    node_356 --> node_285
    node_7 --> node_371
    node_182 --> node_298
    node_321 --> node_574
    node_39 --> node_390
    node_22 --> node_394
    node_405 --> node_258
    node_39 --> node_230
    node_389 --> node_401
    node_172 --> node_238
    node_412 --> node_584
    node_241 --> node_238
    node_7 --> node_113
    node_17 --> node_219
    node_461 --> node_157
    node_563 --> node_561
    node_142 --> node_179
    node_44 --> node_128
    node_373 --> node_198
    node_373 --> node_256
    node_241 --> node_270
    node_241 --> node_172
    node_487 --> node_331
    node_632 --> node_78
    node_394 --> node_340
    node_496 --> node_516
    node_39 --> node_152
    node_120 --> node_228
    node_620 --> node_179
    node_356 --> node_294
    node_44 --> node_134
    node_143 --> node_260
    node_160 --> node_162
    node_41 --> node_50
    node_134 --> node_259
    node_172 --> node_165
    node_303 --> node_298
    node_17 --> node_223
    node_172 --> node_169
    node_241 --> node_165
    node_373 --> node_216
    node_18 --> node_372
    node_17 --> node_411
    node_439 --> node_402
    node_219 --> node_672
    node_373 --> node_254
    node_59 --> node_78
    node_403 --> node_146
    node_16 --> node_320
    node_120 --> node_143
    node_474 --> node_477
    node_134 --> node_146
    node_142 --> node_139
    node_120 --> node_271
    node_586 --> node_78
    node_16 --> node_637
    node_120 --> node_202
    node_344 --> node_179
    node_241 --> node_160
    node_275 --> node_274
    node_17 --> node_371
    node_298 --> node_584
    node_41 --> node_53
    node_495 --> node_646
    node_550 --> node_546
    node_16 --> node_298
    node_572 --> node_331
    node_241 --> node_182
    node_425 --> node_100
    node_566 --> node_560
    node_16 --> node_638
    node_7 --> node_33
    node_99 --> node_167
    node_9 --> node_566
    node_253 --> node_252
    node_412 --> node_179
    node_572 --> node_653
    node_7 --> node_59
    node_492 --> node_417
    node_197 --> node_193
    node_352 --> node_345
    node_398 --> node_252
    node_623 --> node_141
    node_356 --> node_267
    node_572 --> node_321
    node_407 --> node_167
    node_474 --> node_479
    node_241 --> node_186
    node_72 --> node_179
    node_572 --> node_639
    node_394 --> node_352
    node_39 --> node_445
    node_134 --> node_221
    node_51 --> node_303
    node_298 --> node_634
    node_152 --> node_128
    node_4 --> node_177
    node_120 --> node_268
    node_462 --> node_168
    node_240 --> node_239
    node_401 --> node_211
    node_4 --> node_674
    node_4 --> node_412
    node_298 --> node_656
    node_522 --> node_601
    node_9 --> node_370
    node_494 --> node_179
    node_425 --> node_496
    node_425 --> node_79
    node_39 --> node_177
    node_438 --> node_175
    node_4 --> node_166
    node_47 --> node_445
    node_405 --> node_313
    node_499 --> node_654
    node_618 --> node_576
    node_17 --> node_218
    node_51 --> node_179
    node_27 --> node_35
    node_405 --> node_318
    node_51 --> node_163
    node_517 --> node_635
    node_44 --> node_172
    node_496 --> node_141
    node_505 --> node_313
    node_17 --> node_33
    node_137 --> node_581
    node_72 --> node_108
    node_51 --> node_281
    node_54 --> node_604
    node_398 --> node_203
    node_412 --> node_301
    node_256 --> node_167
    node_17 --> node_59
    node_211 --> node_215
    node_587 --> node_316
    node_394 --> node_219
    node_39 --> node_240
    node_22 --> node_369
    node_17 --> node_341
    node_465 --> node_567
    node_44 --> node_165
    node_27 --> node_20
    node_42 --> node_71
    node_566 --> node_141
    node_17 --> node_250
    node_41 --> node_59
    node_379 --> node_349
    node_399 --> node_159
    node_365 --> node_157
    node_9 --> node_671
    node_220 --> node_103
    node_120 --> node_238
    node_137 --> node_303
    node_51 --> node_118
    node_44 --> node_380
    node_530 --> node_311
    node_39 --> node_673
    node_44 --> node_160
    node_54 --> node_560
    node_120 --> node_270
    node_9 --> node_446
    node_352 --> node_358
    node_356 --> node_150
    node_44 --> node_182
    node_462 --> node_159
    node_51 --> node_280
    node_17 --> node_296
    node_373 --> node_275
    node_352 --> node_179
    node_134 --> node_236
    node_509 --> node_317
    node_134 --> node_209
    node_17 --> node_294
    node_373 --> node_285
    node_404 --> node_158
    node_449 --> node_15
    node_512 --> node_115
    node_394 --> node_351
    node_566 --> node_298
    node_298 --> node_301
    node_51 --> node_253
    node_496 --> node_498
    node_39 --> node_444
    node_137 --> node_163
    node_576 --> node_329
    node_352 --> node_112
    node_115 --> node_116
    node_373 --> node_259
    node_134 --> node_249
    node_137 --> node_281
    node_9 --> node_427
    node_466 --> node_539
    node_143 --> node_140
    node_576 --> node_661
    node_572 --> node_328
    node_134 --> node_127
    node_51 --> node_339
    node_27 --> node_576
    node_572 --> node_646
    node_474 --> node_478
    node_134 --> node_266
    node_58 --> node_18
    node_35 --> node_576
    node_18 --> node_363
    node_352 --> node_108
    node_425 --> node_5
    node_356 --> node_303
    node_466 --> node_25
    node_67 --> node_76
    node_19 --> node_674
    node_19 --> node_412
    node_425 --> node_300
    node_51 --> node_572
    node_17 --> node_372
    node_494 --> node_563
    node_17 --> node_334
    node_17 --> node_267
    node_120 --> node_186
    node_51 --> node_286
    node_137 --> node_280
    node_16 --> node_632
    node_285 --> node_282
    node_394 --> node_218
    node_145 --> node_335
    node_134 --> node_201
    node_4 --> node_199
    node_56 --> node_412
    node_298 --> node_652
    node_572 --> node_665
    node_16 --> node_645
    node_100 --> node_674
    node_356 --> node_163
    node_39 --> node_562
    node_120 --> node_243
    node_4 --> node_69
    node_39 --> node_431
    node_137 --> node_253
    node_255 --> node_171
    node_442 --> node_437
    node_621 --> node_576
    node_51 --> node_173
    node_4 --> node_78
    node_56 --> node_142
    node_182 --> node_181
    node_394 --> node_341
    node_402 --> node_159
    node_405 --> node_276
    node_610 --> node_606
    node_51 --> node_566
    node_555 --> node_551
    node_4 --> node_287
    node_4 --> node_154
    node_39 --> node_596
    node_120 --> node_229
    node_352 --> node_613
    node_218 --> node_217
    node_563 --> node_594
    node_352 --> node_568
    node_7 --> node_141
    node_550 --> node_22
    node_383 --> node_351
    node_18 --> node_672
    node_51 --> node_482
    node_573 --> node_572
    node_241 --> node_233
    node_352 --> node_572
    node_16 --> node_316
    node_405 --> node_198
    node_405 --> node_256
    node_17 --> node_184
    node_509 --> node_653
    node_49 --> node_380
    node_496 --> node_520
    node_458 --> node_576
    node_422 --> node_26
    node_587 --> node_640
    node_405 --> node_227
    node_356 --> node_280
    node_576 --> node_319
    node_395 --> node_399
    node_67 --> node_576
    node_298 --> node_323
    node_439 --> node_405
    node_4 --> node_263
    node_241 --> node_126
    node_134 --> node_118
    node_255 --> node_164
    node_134 --> node_156
    node_356 --> node_253
    node_134 --> node_279
    node_306 --> node_637
    node_512 --> node_415
    node_512 --> node_309
    node_17 --> node_122
    node_580 --> node_588
    node_371 --> node_674
    node_31 --> node_33
    node_17 --> node_150
    node_27 --> node_298
    node_137 --> node_173
    node_572 --> node_313
    node_532 --> node_329
    node_496 --> node_308
    node_172 --> node_237
    node_621 --> node_141
    node_51 --> node_98
    node_120 --> node_166
    node_352 --> node_569
    node_277 --> node_166
    node_134 --> node_208
    node_618 --> node_563
    node_512 --> node_41
    node_44 --> node_240
    node_58 --> node_417
    node_142 --> node_260
    node_373 --> node_209
    node_405 --> node_200
    node_547 --> node_546
    node_71 --> node_179
    node_51 --> node_474
    node_590 --> node_598
    node_672 --> node_184
    node_425 --> node_115
    node_576 --> node_314
    node_137 --> node_482
    node_425 --> node_22
    node_425 --> node_410
    node_365 --> node_674
    node_60 --> node_207
    node_545 --> node_547
    node_134 --> node_339
    node_576 --> node_304
    node_563 --> node_604
    node_356 --> node_145
    node_566 --> node_632
    node_4 --> node_272
    node_405 --> node_329
    node_392 --> node_274
    node_621 --> node_298
    node_427 --> node_99
    node_373 --> node_127
    node_4 --> node_277
    node_4 --> node_225
    node_51 --> node_446
    node_475 --> node_179
    node_20 --> node_13
    node_545 --> node_546
    node_35 --> node_388
    node_7 --> node_41
    node_51 --> node_338
    node_576 --> node_642
    node_19 --> node_78
    node_352 --> node_18
    node_512 --> node_553
    node_392 --> node_272
    node_356 --> node_173
    node_134 --> node_286
    node_39 --> node_441
    node_51 --> node_172
    node_4 --> node_354
    node_71 --> node_66
    node_314 --> node_663
    node_405 --> node_302
    node_253 --> node_412
    node_39 --> node_254
    node_51 --> node_427
    node_373 --> node_303
    node_406 --> node_245
    node_425 --> node_633
    node_398 --> node_674
    node_17 --> node_163
    node_373 --> node_201
    node_298 --> node_331
    node_356 --> node_128
    node_17 --> node_363
    node_120 --> node_335
    node_56 --> node_106
    node_434 --> node_388
    node_7 --> node_672
    node_4 --> node_609
    node_67 --> node_298
    node_356 --> node_134
    node_7 --> node_553
    node_597 --> node_536
    node_4 --> node_222
    node_4 --> node_241
    node_394 --> node_345
    node_22 --> node_403
    node_134 --> node_137
    node_495 --> node_312
    node_221 --> node_166
    node_270 --> node_269
    node_590 --> node_536
    node_120 --> node_233
    node_17 --> node_41
    node_172 --> node_276
    node_373 --> node_281
    node_241 --> node_235
    node_241 --> node_276
    node_137 --> node_338
    node_397 --> node_166
    node_381 --> node_156
    node_593 --> node_598
    node_16 --> node_640
    node_394 --> node_292
    node_389 --> node_369
    node_381 --> node_170
    node_399 --> node_171
    node_399 --> node_161
    node_17 --> node_280
    node_591 --> node_596
    node_59 --> node_576
    node_120 --> node_126
    node_137 --> node_172
    node_120 --> node_224
    node_9 --> node_418
    node_425 --> node_139
    node_609 --> node_606
    node_316 --> node_180
    node_633 --> node_632
    node_474 --> node_141
    node_134 --> node_203
    node_59 --> node_288
    node_241 --> node_198
    node_241 --> node_256
    node_576 --> node_584
    node_182 --> node_142
    node_496 --> node_331
    node_405 --> node_259
    node_39 --> node_496
    node_393 --> node_339
    node_373 --> node_118
    node_51 --> node_230
    node_405 --> node_319
    node_462 --> node_171
    node_525 --> node_88
    node_120 --> node_291
    node_59 --> node_22
    node_416 --> node_417
    node_496 --> node_487
    node_277 --> node_168
    node_17 --> node_553
    node_89 --> node_71
    node_16 --> node_332
    node_39 --> node_590
    node_4 --> node_261
    node_303 --> node_412
    node_241 --> node_216
    node_622 --> node_558
    node_18 --> node_386
    node_39 --> node_232
    node_51 --> node_152
    node_406 --> node_189
    node_512 --> node_370
    node_427 --> node_438
    node_546 --> node_548
    node_73 --> node_66
    node_587 --> node_662
    node_373 --> node_253
    node_373 --> node_208
    node_576 --> node_634
    node_474 --> node_298
    node_27 --> node_632
    node_303 --> node_142
    node_4 --> node_211
    node_399 --> node_164
    node_576 --> node_648
    node_17 --> node_145
    node_105 --> node_153
    node_260 --> node_12
    node_356 --> node_172
    node_373 --> node_339
    node_425 --> node_543
    node_383 --> node_345
    node_490 --> node_320
    node_405 --> node_314
    node_120 --> node_340
    node_394 --> node_179
    node_120 --> node_263
    node_359 --> node_158
    node_466 --> node_288
    node_7 --> node_370
    node_41 --> node_42
    node_405 --> node_161
    node_405 --> node_304
    node_434 --> node_463
    node_462 --> node_164
    node_576 --> node_322
    node_439 --> node_401
    node_638 --> node_319
    node_134 --> node_157
    node_383 --> node_349
    node_59 --> node_141
    node_512 --> node_671
    node_42 --> node_33
    node_399 --> node_162
    node_17 --> node_173
    node_99 --> node_166
    node_137 --> node_230
    node_396 --> node_268
    node_577 --> node_141
    node_493 --> node_69
    node_373 --> node_286
    node_44 --> node_235
    node_44 --> node_276
    node_521 --> node_322
    node_39 --> node_259
    node_439 --> node_407
    node_39 --> node_319
    node_68 --> node_67
    node_425 --> node_4
    node_137 --> node_152
    node_4 --> node_250
    node_356 --> node_160
    node_394 --> node_347
    node_407 --> node_166
    node_303 --> node_567
    node_462 --> node_162
    node_17 --> node_128
    node_291 --> node_288
    node_356 --> node_182
    node_547 --> node_22
    node_39 --> node_146
    node_563 --> node_175
    node_462 --> node_150
    node_452 --> node_585
    node_44 --> node_198
    node_44 --> node_256
    node_59 --> node_298
    node_17 --> node_134
    node_572 --> node_329
    node_83 --> node_84
    node_7 --> node_671
    node_16 --> node_530
    node_7 --> node_588
    node_4 --> node_296
    node_51 --> node_177
    node_221 --> node_168
    node_298 --> node_647
    node_39 --> node_564
    node_39 --> node_300
    node_452 --> node_573
    node_572 --> node_312
    node_585 --> node_658
    node_4 --> node_178
    node_20 --> node_551
    node_120 --> node_225
    node_4 --> node_262
    node_576 --> node_301
    node_17 --> node_370
    node_572 --> node_661
    node_182 --> node_180
    node_397 --> node_168
    node_373 --> node_482
    node_7 --> node_446
    node_44 --> node_216
    node_120 --> node_352
    node_400 --> node_229
    node_39 --> node_435
    node_44 --> node_254
    node_133 --> node_139
    node_356 --> node_230
    node_398 --> node_185
    node_398 --> node_207
    node_51 --> node_240
    node_4 --> node_20
    node_553 --> node_554
    node_39 --> node_221
    node_256 --> node_166
    node_489 --> node_664
    node_396 --> node_270
    node_389 --> node_399
    node_226 --> node_33
    node_241 --> node_275
    node_7 --> node_386
    node_27 --> node_549
    node_7 --> node_427
    node_572 --> node_310
    node_465 --> node_560
    node_521 --> node_659
    node_517 --> node_305
    node_241 --> node_285
    node_576 --> node_568
    node_143 --> node_300
    node_16 --> node_531
    node_17 --> node_671
    node_520 --> node_26
    node_16 --> node_524
    node_576 --> node_572
    node_120 --> node_219
    node_563 --> node_568
    node_22 --> node_405
    node_405 --> node_127
    node_425 --> node_28
    node_4 --> node_334
    node_512 --> node_7
    node_16 --> node_662
    node_4 --> node_267
    node_228 --> node_226
    node_241 --> node_259
    node_298 --> node_635
    node_137 --> node_177
    node_417 --> node_637
    node_576 --> node_652
    node_7 --> node_373
    node_566 --> node_142
    node_402 --> node_162
    node_462 --> node_170
    node_17 --> node_446
    node_27 --> node_32
    node_51 --> node_444
    node_383 --> node_347
    node_491 --> node_314
    node_60 --> node_20
    node_59 --> node_89
    node_120 --> node_223
    node_17 --> node_238
    node_300 --> node_12
    node_406 --> node_244
    node_16 --> node_78
    node_563 --> node_589
    node_506 --> node_308
    node_4 --> node_576
    node_550 --> node_551
    node_137 --> node_240
    node_17 --> node_172
    node_405 --> node_303
    node_486 --> node_71
    node_405 --> node_201
    node_17 --> node_386
    node_56 --> node_59
    node_17 --> node_427
    node_377 --> node_672
    node_572 --> node_319
    node_99 --> node_168
    node_373 --> node_338
    node_411 --> node_300
    node_616 --> node_576
    node_39 --> node_576
    node_379 --> node_346
    node_4 --> node_22
    node_17 --> node_165
    node_145 --> node_334
    node_39 --> node_236
    node_300 --> node_179
    node_617 --> node_576
    node_39 --> node_209
    node_4 --> node_184
    node_434 --> node_32
    node_4 --> node_574
    node_255 --> node_172
    node_439 --> node_424
    node_8 --> node_113
    node_172 --> node_171
    node_572 --> node_325
    node_405 --> node_322
    node_407 --> node_168
    node_356 --> node_355
    node_379 --> node_674
    node_39 --> node_410
    node_17 --> node_373
    node_576 --> node_323
    node_17 --> node_160
    node_39 --> node_249
    node_4 --> node_293
    node_641 --> node_16
    node_17 --> node_182
    node_195 --> node_189
    node_462 --> node_672
    node_18 --> node_673
    node_6 --> node_576
    node_39 --> node_127
    node_466 --> node_174
    node_398 --> node_241
    node_51 --> node_395
    node_44 --> node_275
    node_4 --> node_122
    node_143 --> node_107
    node_39 --> node_592
    node_531 --> node_332
    node_39 --> node_266
    node_356 --> node_240
    node_39 --> node_422
    node_9 --> node_496
    node_9 --> node_79
    node_381 --> node_165
    node_381 --> node_169
    node_405 --> node_139
    node_143 --> node_576
    node_185 --> node_106
    node_435 --> node_99
    node_496 --> node_525
    node_17 --> node_186
    node_533 --> node_576
    node_120 --> node_218
    node_59 --> node_632
    node_134 --> node_166
    node_4 --> node_141
    node_145 --> node_184
    node_404 --> node_157
    node_425 --> node_260
    node_42 --> node_141
    node_44 --> node_259
    node_16 --> node_670
    node_256 --> node_168
    node_300 --> node_301
    node_381 --> node_160
    node_425 --> node_537
    node_51 --> node_154
    node_39 --> node_201
    node_172 --> node_164
    node_590 --> node_591
    node_39 --> node_251
    node_39 --> node_633
    node_405 --> node_301
    node_572 --> node_642
    node_587 --> node_668
    node_120 --> node_341
    node_39 --> node_29
    node_160 --> node_159
    node_16 --> node_490
    node_255 --> node_278
    node_425 --> node_32
    node_39 --> node_358
    node_9 --> node_61
    node_120 --> node_250
    node_36 --> node_37
    node_7 --> node_445
    node_120 --> node_285
    node_373 --> node_230
    node_4 --> node_298
    node_388 --> node_401
    node_427 --> node_435
    node_39 --> node_320
    node_19 --> node_576
    node_39 --> node_281
    node_672 --> node_183
    node_373 --> node_152
    node_120 --> node_296
    node_439 --> node_22
    node_388 --> node_407
    node_581 --> node_560
    node_69 --> node_71
    node_47 --> node_179
    node_120 --> node_294
    node_617 --> node_298
    node_44 --> node_221
    node_4 --> node_156
    node_36 --> node_536
    node_143 --> node_633
    node_16 --> node_565
    node_241 --> node_127
    node_39 --> node_139
    node_405 --> node_289
    node_405 --> node_286
    node_512 --> node_357
    node_394 --> node_342
    node_455 --> node_460
    node_39 --> node_494
    node_39 --> node_118
    node_137 --> node_154
    node_39 --> node_156
    node_39 --> node_279
    node_576 --> node_321
    node_565 --> node_588
    node_605 --> node_606
    node_9 --> node_64
    node_105 --> node_102
    node_47 --> node_139
    node_512 --> node_418
    node_433 --> node_539
    node_414 --> node_632
    node_39 --> node_388
    node_405 --> node_306
    node_545 --> node_557
    node_143 --> node_298
    node_39 --> node_208
    node_241 --> node_303
    node_16 --> node_571
    node_51 --> node_277
    node_79 --> node_14
    node_39 --> node_443
    node_533 --> node_298
    node_182 --> node_413
    node_398 --> node_250
    node_277 --> node_171
    node_7 --> node_357
    node_145 --> node_337
    node_120 --> node_334
    node_652 --> node_180
    node_120 --> node_267
    node_411 --> node_251
    node_411 --> node_633
    node_433 --> node_25
    node_51 --> node_254
    node_485 --> node_319
    node_466 --> node_226
    node_388 --> node_393
    node_39 --> node_339
    node_134 --> node_224
    node_174 --> node_77
    node_359 --> node_156
    node_59 --> node_386
    node_51 --> node_354
    node_39 --> node_543
    node_134 --> node_199
    node_512 --> node_117
    node_405 --> node_323
    node_7 --> node_418
    node_587 --> node_327
    node_66 --> node_576
    node_17 --> node_240
    node_56 --> node_141
    node_22 --> node_407
    node_133 --> node_260
    node_373 --> node_177
    node_241 --> node_281
    node_633 --> node_78
    node_379 --> node_343
    node_44 --> node_236
    node_425 --> node_412
    node_425 --> node_674
    node_39 --> node_385
    node_399 --> node_172
    node_44 --> node_209
    node_425 --> node_449
    node_33 --> node_549
    node_589 --> node_592
    node_39 --> node_286
    node_504 --> node_639
    node_39 --> node_652
    node_47 --> node_613
    node_19 --> node_298
    node_134 --> node_287
    node_39 --> node_563
    node_126 --> node_125
    node_39 --> node_589
    node_69 --> node_75
    node_277 --> node_164
    node_39 --> node_4
    node_579 --> node_321
    node_16 --> node_668
    node_120 --> node_184
    node_572 --> node_322
    node_572 --> node_320
    node_462 --> node_172
    node_17 --> node_357
    node_241 --> node_118
    node_7 --> node_117
    node_4 --> node_145
    node_425 --> node_105
    node_461 --> node_156
    node_298 --> node_657
    node_44 --> node_127
    node_39 --> node_68
    node_44 --> node_266
    node_300 --> node_588
    node_137 --> node_254
    node_590 --> node_77
    node_366 --> node_674
    node_462 --> node_165
    node_4 --> node_228
    node_51 --> node_496
    node_405 --> node_362
    node_462 --> node_169
    node_134 --> node_340
    node_17 --> node_233
    node_134 --> node_263
    node_356 --> node_235
    node_356 --> node_276
    node_17 --> node_418
    node_39 --> node_137
    node_300 --> node_299
    node_137 --> node_354
    node_241 --> node_253
    node_241 --> node_208
    node_120 --> node_122
    node_400 --> node_295
    node_88 --> node_76
    node_120 --> node_150
    node_405 --> node_299
    node_547 --> node_551
    node_462 --> node_160
    node_51 --> node_232
    node_44 --> node_303
    node_221 --> node_171
    node_4 --> node_143
    node_405 --> node_338
    node_44 --> node_201
    node_4 --> node_632
    node_17 --> node_126
    node_316 --> node_584
    node_5 --> node_19
    node_493 --> node_576
    node_298 --> node_310
    node_4 --> node_271
    node_356 --> node_198
    node_39 --> node_463
    node_4 --> node_202
    node_241 --> node_339
    node_405 --> node_157
    node_345 --> node_569
    node_51 --> node_261
    node_511 --> node_576
    node_39 --> node_587
    node_9 --> node_410
    node_89 --> node_372
    node_451 --> node_611
    node_512 --> node_550
    node_39 --> node_203
    node_17 --> node_117
    node_415 --> node_417
    node_392 --> node_271
    node_545 --> node_551
    node_576 --> node_647
    node_474 --> node_480
    node_356 --> node_216
    node_545 --> node_549
    node_572 --> node_658
    node_39 --> node_55
    node_425 --> node_30
    node_576 --> node_665
    node_356 --> node_254
    node_379 --> node_350
    node_39 --> node_23
    node_44 --> node_281
    node_134 --> node_272
    node_66 --> node_298
    node_190 --> node_431
    node_241 --> node_286
    node_398 --> node_184
    node_39 --> node_70
    node_405 --> node_336
    node_134 --> node_277
    node_134 --> node_225
    node_405 --> node_321
    node_134 --> node_352
    node_4 --> node_268
    node_394 --> node_240
    node_512 --> node_455
    node_221 --> node_164
    node_41 --> node_562
    node_241 --> node_173
    node_51 --> node_259
    node_163 --> node_139
    node_435 --> node_407
    node_47 --> node_70
    node_137 --> node_232
    node_134 --> node_354
    node_44 --> node_118
    node_298 --> node_319
    node_405 --> node_260
    node_39 --> node_316
    node_100 --> node_672
    node_438 --> node_435
    node_88 --> node_576
    node_44 --> node_279
    node_120 --> node_163
    node_51 --> node_146
    node_220 --> node_160
    node_363 --> node_179
    node_572 --> node_652
    node_394 --> node_673
    node_277 --> node_170
    node_566 --> node_413
    node_49 --> node_22
    node_446 --> node_613
    node_241 --> node_482
    node_122 --> node_124
    node_176 --> node_174
    node_352 --> node_615
    node_405 --> node_278
    node_298 --> node_325
    node_402 --> node_160
    node_259 --> node_257
    node_39 --> node_157
    node_518 --> node_323
    node_576 --> node_635
    node_44 --> node_208
    node_105 --> node_106
    node_142 --> node_576
    node_512 --> node_545
    node_134 --> node_222
    node_134 --> node_241
    node_483 --> node_417
    node_496 --> node_416
    node_601 --> node_602
    node_365 --> node_156
    node_620 --> node_576
    node_59 --> node_71
    node_73 --> node_69
    node_99 --> node_171
    node_522 --> node_609
    node_373 --> node_287
    node_405 --> node_290
    node_100 --> node_145
    node_373 --> node_154
    node_285 --> node_283
    node_51 --> node_178
    node_405 --> node_152
    node_4 --> node_238
    node_160 --> node_161
    node_44 --> node_339
    node_51 --> node_262
    node_51 --> node_221
    node_493 --> node_298
    node_57 --> node_674
    node_18 --> node_416
    node_4 --> node_270
    node_19 --> node_632
    node_120 --> node_280
    node_298 --> node_664
    node_401 --> node_213
    node_137 --> node_259
    node_9 --> node_214
    node_39 --> node_384
    node_394 --> node_180
    node_406 --> node_246
    node_7 --> node_545
    node_182 --> node_584
    node_42 --> node_386
    node_344 --> node_576
    node_572 --> node_323
    node_120 --> node_253
    node_17 --> node_235
    node_17 --> node_276
    node_182 --> node_581
    node_359 --> node_157
    node_4 --> node_165
    node_120 --> node_119
    node_137 --> node_146
    node_16 --> node_667
    node_235 --> node_234
    node_68 --> node_70
    node_44 --> node_286
    node_381 --> node_159
    node_88 --> node_141
    node_39 --> node_260
    node_352 --> node_564
    node_412 --> node_576
    node_39 --> node_417
    node_425 --> node_2
    node_389 --> node_397
    node_512 --> node_353
    node_559 --> node_571
    node_39 --> node_537
    node_572 --> node_645
    node_137 --> node_300
    node_17 --> node_198
    node_17 --> node_256
    node_99 --> node_164
    node_4 --> node_160
    node_134 --> node_261
    node_356 --> node_275
    node_377 --> node_673
    node_400 --> node_296
    node_514 --> node_324
    node_72 --> node_576
    node_4 --> node_595
    node_4 --> node_182
    node_16 --> node_559
    node_22 --> node_404
    node_400 --> node_294
    node_398 --> node_144
    node_303 --> node_141
    node_256 --> node_171
    node_395 --> node_394
    node_5 --> node_562
    node_47 --> node_260
    node_572 --> node_634
    node_221 --> node_170
    node_241 --> node_338
    node_515 --> node_665
    node_134 --> node_211
    node_35 --> node_389
    node_120 --> node_145
    node_17 --> node_216
    node_137 --> node_262
    node_137 --> node_221
    node_425 --> node_539
    node_88 --> node_298
    node_9 --> node_543
    node_425 --> node_550
    node_44 --> node_137
    node_356 --> node_259
    node_494 --> node_576
    node_439 --> node_399
    node_397 --> node_170
    node_44 --> node_482
    node_22 --> node_398
    node_17 --> node_254
    node_126 --> node_124
    node_4 --> node_186
    node_259 --> node_258
    node_534 --> node_605
    node_17 --> node_545
    node_298 --> node_305
    node_375 --> node_374
    node_425 --> node_83
    node_7 --> node_353
    node_51 --> node_576
    node_182 --> node_179
    node_16 --> node_141
    node_572 --> node_316
    node_425 --> node_31
    node_51 --> node_236
    node_425 --> node_25
    node_51 --> node_209
    node_405 --> node_177
    node_373 --> node_277
    node_4 --> node_243
    node_142 --> node_298
    node_484 --> node_35
    node_120 --> node_173
    node_425 --> node_121
    node_505 --> node_647
    node_462 --> node_149
    node_51 --> node_115
    node_545 --> node_552
    node_51 --> node_410
    node_51 --> node_249
    node_44 --> node_203
    node_507 --> node_315
    node_4 --> node_229
    node_373 --> node_354
    node_256 --> node_164
    node_39 --> node_640
    node_427 --> node_70
    node_51 --> node_127
    node_120 --> node_128
    node_134 --> node_250
    node_9 --> node_68
    node_29 --> node_388
    node_597 --> node_626
    node_671 --> node_672
    node_51 --> node_266
    node_145 --> node_183
    node_184 --> node_185
    node_16 --> node_501
    node_16 --> node_656
    node_120 --> node_134
    node_356 --> node_221
    node_405 --> node_140
    node_27 --> node_33
    node_344 --> node_298
    node_425 --> node_376
    node_590 --> node_626
    node_587 --> node_308
    node_17 --> node_353
    node_134 --> node_296
    node_352 --> node_576
    node_373 --> node_222
    node_182 --> node_301
    node_373 --> node_241
    node_27 --> node_594
    node_134 --> node_178
    node_172 --> node_278
    node_503 --> node_330
    node_524 --> node_304
    node_134 --> node_294
    node_134 --> node_262
    node_398 --> node_145
    node_494 --> node_536
    node_406 --> node_247
    node_512 --> node_448
    node_51 --> node_201
    node_137 --> node_236
    node_137 --> node_209
    node_241 --> node_230
    node_461 --> node_160
    node_39 --> node_485
    node_425 --> node_411
    node_475 --> node_481
    node_44 --> node_338
    node_99 --> node_170
    node_352 --> node_574
    node_137 --> node_249
    node_285 --> node_284
    node_402 --> node_673
    node_241 --> node_152
    node_44 --> node_157
    node_4 --> node_142
    node_576 --> node_583
    node_39 --> node_138
    node_39 --> node_674
    node_39 --> node_412
    node_39 --> node_449
    node_400 --> node_293
    node_550 --> node_33
    node_247 --> node_246
    node_494 --> node_298
    node_137 --> node_127
    node_298 --> node_320
    node_572 --> node_641
    node_300 --> node_180
    node_16 --> node_333
    node_105 --> node_113
    node_407 --> node_170
    node_425 --> node_546
    node_507 --> node_650
    node_9 --> node_98
    node_39 --> node_166
    node_358 --> node_344
    node_394 --> node_216
    node_7 --> node_448
    node_137 --> node_266
    node_373 --> node_232
    node_398 --> node_202
    node_406 --> node_190
    node_623 --> node_179
    node_309 --> node_16
    node_9 --> node_474
    node_17 --> node_275
    node_4 --> node_71
    node_134 --> node_334
    node_414 --> node_78
    node_519 --> node_306
    node_134 --> node_267
    node_383 --> node_343
    node_373 --> node_261
    node_39 --> node_105
    node_566 --> node_581
    node_65 --> node_441
    node_620 --> node_563
    node_35 --> node_20
    node_17 --> node_285
    node_39 --> node_140
    node_51 --> node_139
    node_356 --> node_236
    node_425 --> node_542
    node_356 --> node_209
    node_352 --> node_536
    node_137 --> node_201
    node_51 --> node_156
    node_137 --> node_251
    node_137 --> node_633
    node_51 --> node_279
    node_17 --> node_259
    node_120 --> node_172
    node_143 --> node_138
    node_381 --> node_33
    node_143 --> node_412
    node_277 --> node_172
    node_535 --> node_655
    node_4 --> node_573
    node_163 --> node_260
    node_396 --> node_267
    node_256 --> node_170
    node_16 --> node_450
    node_496 --> node_179
    node_356 --> node_127
    node_120 --> node_165
    node_51 --> node_208
    node_143 --> node_142
    node_490 --> node_657
    node_572 --> node_640
    node_277 --> node_165
    node_373 --> node_220
    node_277 --> node_169
    node_462 --> node_213
    node_4 --> node_335
    node_17 --> node_448
    node_356 --> node_266
    node_425 --> node_33
    node_618 --> node_141
    node_73 --> node_72
    node_576 --> node_657
    node_134 --> node_184
    node_137 --> node_112
    node_44 --> node_230
    node_120 --> node_160
    node_241 --> node_177
    node_405 --> node_287
    node_566 --> node_179
    node_373 --> node_146
    node_352 --> node_139
    node_51 --> node_543
    node_120 --> node_182
    node_438 --> node_589
    node_4 --> node_233
    node_134 --> node_293
    node_89 --> node_18
    node_356 --> node_201
    node_44 --> node_152
    node_16 --> node_311
    node_411 --> node_412
    node_137 --> node_118
    node_403 --> node_150
    node_618 --> node_298
    node_134 --> node_122
    node_137 --> node_156
    node_16 --> node_308
    node_241 --> node_240
    node_652 --> node_584
    node_134 --> node_150
    node_137 --> node_279
    node_433 --> node_174
    node_35 --> node_22
    node_576 --> node_310
    node_572 --> node_647
    node_4 --> node_126
    node_563 --> node_590
    node_4 --> node_224
    node_19 --> node_142
    node_365 --> node_160
    node_587 --> node_660
    node_220 --> node_159
    node_373 --> node_178
    node_383 --> node_350
    node_71 --> node_576
    node_446 --> node_445
    node_4 --> node_75
    node_373 --> node_262
    node_373 --> node_221
    node_133 --> node_132
    node_137 --> node_208
    node_498 --> node_257
    node_4 --> node_291
    node_39 --> node_224
    node_572 --> node_324
    node_356 --> node_281
    node_39 --> node_395
    node_39 --> node_199
    node_51 --> node_68
    node_182 --> node_588
    node_425 --> node_20
    node_19 --> node_71
    node_59 --> node_113
    node_623 --> node_563
    node_16 --> node_317
    node_155 --> node_114
    node_60 --> node_62
    node_221 --> node_172
    node_381 --> node_171
    node_425 --> node_15
    node_137 --> node_339
    node_39 --> node_78
    node_387 --> node_101
    node_502 --> node_643
    node_51 --> node_137
    node_475 --> node_576
    node_527 --> node_601
    node_394 --> node_220
    node_27 --> node_141
    node_221 --> node_165
    node_356 --> node_118
    node_221 --> node_169
    node_39 --> node_287
    node_39 --> node_154
    node_400 --> node_672
    node_356 --> node_279
    node_35 --> node_141
    node_7 --> node_548
    node_303 --> node_588
    node_397 --> node_165
    node_397 --> node_169
    node_352 --> node_563
    node_359 --> node_103
    node_663 --> node_326
    node_572 --> node_635
    node_137 --> node_286
    node_4 --> node_340
    node_405 --> node_277
    node_469 --> node_22
    node_496 --> node_652
    node_105 --> node_101
    node_17 --> node_236
    node_55 --> node_432
    node_51 --> node_143
    node_17 --> node_209
    node_44 --> node_177
    node_356 --> node_208
    node_39 --> node_80
    node_51 --> node_203
    node_389 --> node_394
    node_398 --> node_183
    node_17 --> node_404
    node_398 --> node_186
    node_576 --> node_325
    node_51 --> node_202
    node_399 --> node_158
    node_39 --> node_340
    node_425 --> node_560
    node_39 --> node_263
    node_16 --> node_588
    node_576 --> node_564
    node_381 --> node_164
    node_288 --> node_289
    node_35 --> node_298
    node_425 --> node_1
    node_464 --> node_167
    node_100 --> node_673
    node_356 --> node_339
    node_59 --> node_416
    node_496 --> node_493
    node_373 --> node_236
    node_563 --> node_564
    node_650 --> node_672
    node_7 --> node_179
    node_17 --> node_127
    node_154 --> node_674
    node_462 --> node_158
    node_54 --> node_139
    node_29 --> node_32
    node_27 --> node_179
    node_394 --> node_221
    node_4 --> node_54
    node_73 --> node_576
    node_425 --> node_544
    node_576 --> node_664
    node_373 --> node_249
    node_652 --> node_301
    node_381 --> node_162
    node_51 --> node_344
    node_71 --> node_298
    node_291 --> node_113
    node_356 --> node_286
    node_298 --> node_316
    node_16 --> node_331
    node_458 --> node_141
    node_405 --> node_312
    node_405 --> node_297
    node_352 --> node_632
    node_4 --> node_352
    node_4 --> node_276
    node_17 --> node_303
    node_22 --> node_391
    node_99 --> node_172
    node_373 --> node_266
    node_17 --> node_201
    node_22 --> node_402
    node_405 --> node_408
    node_16 --> node_653
    node_39 --> node_83
    node_39 --> node_272
    node_28 --> node_672
    node_67 --> node_141
    node_137 --> node_143
    node_120 --> node_240
    node_17 --> node_29
    node_137 --> node_203
    node_241 --> node_287
    node_51 --> node_157
    node_241 --> node_154
    node_39 --> node_277
    node_39 --> node_225
    node_576 --> node_327
    node_9 --> node_449
    node_496 --> node_18
    node_16 --> node_660
    node_621 --> node_179
    node_475 --> node_298
    node_99 --> node_165
    node_99 --> node_169
    node_4 --> node_256
    node_39 --> node_121
    node_137 --> node_136
    node_405 --> node_158
    node_434 --> node_363
    node_433 --> node_466
    node_458 --> node_298
    node_16 --> node_570
    node_356 --> node_137
    node_547 --> node_33
    node_532 --> node_666
    node_39 --> node_354
    node_356 --> node_482
    node_405 --> node_310
    node_527 --> node_608
    node_41 --> node_39
    node_17 --> node_281
    node_253 --> node_142
    node_370 --> node_369
    node_78 --> node_77
    node_396 --> node_672
    node_9 --> node_105
    node_407 --> node_165
    node_407 --> node_169
    node_650 --> node_558
    node_352 --> node_344
    node_4 --> node_219
    node_405 --> node_261
    node_395 --> node_403
    node_134 --> node_145
    node_59 --> node_372
    node_576 --> node_305
    node_73 --> node_141
    node_223 --> node_261
    node_255 --> node_167
    node_523 --> node_325
    node_402 --> node_158
    node_7 --> node_543
    node_394 --> node_349
    node_7 --> node_613
    node_493 --> node_71
    node_134 --> node_228
    node_39 --> node_222
    node_39 --> node_241
    node_17 --> node_118
    node_401 --> node_214
    node_4 --> node_223
    node_51 --> node_260
    node_256 --> node_172
    node_356 --> node_203
    node_7 --> node_73
    node_461 --> node_159
    node_566 --> node_588
    node_17 --> node_279
    node_39 --> node_657
    node_51 --> node_537
    node_137 --> node_157
    node_512 --> node_566
    node_36 --> node_626
    node_102 --> node_71
    node_9 --> node_444
    node_7 --> node_289
    node_134 --> node_143
    node_133 --> node_131
    node_174 --> node_175
    node_44 --> node_199
    node_16 --> node_330
    node_73 --> node_298
    node_256 --> node_165
    node_256 --> node_169
    node_133 --> node_560
    node_39 --> node_411
    node_134 --> node_271
    node_17 --> node_253
    node_17 --> node_208
    node_134 --> node_202
    node_607 --> node_611
    node_105 --> node_112
    node_425 --> node_14
    node_373 --> node_156
    node_134 --> node_128
    node_255 --> node_279
    node_462 --> node_161
    node_373 --> node_279
    node_587 --> node_313
    node_379 --> node_344
    node_241 --> node_277
    node_185 --> node_183
    node_7 --> node_68
    node_425 --> node_415
    node_371 --> node_106
    node_44 --> node_287
    node_17 --> node_339
    node_594 --> node_20
    node_44 --> node_154
    node_7 --> node_566
    node_405 --> node_325
    node_508 --> node_321
    node_241 --> node_254
    node_17 --> node_543
    node_201 --> node_200
    node_105 --> node_108
    node_41 --> node_48
    node_29 --> node_379
    node_352 --> node_260
    node_405 --> node_300
    node_39 --> node_261
    node_356 --> node_338
    node_425 --> node_41
    node_241 --> node_354
    node_671 --> node_673
    node_39 --> node_65
    node_4 --> node_413
    node_134 --> node_268
    node_356 --> node_157
    node_576 --> node_536
    node_512 --> node_98
    node_553 --> node_557
    node_51 --> node_243
    node_17 --> node_286
    node_590 --> node_175
    node_17 --> node_378
    node_39 --> node_211
    node_462 --> node_151
    node_9 --> node_395
    node_4 --> node_218
    node_203 --> node_385
    node_404 --> node_156
    node_405 --> node_262
    node_474 --> node_179
    node_512 --> node_474
    node_67 --> node_88
    node_496 --> node_506
    node_298 --> node_640
    node_576 --> node_320
    node_537 --> node_538
    node_497 --> node_307
    node_39 --> node_72
    node_18 --> node_417
    node_241 --> node_222
    node_566 --> node_586
    node_17 --> node_68
    node_493 --> node_75
    node_4 --> node_341
    node_7 --> node_55
    node_41 --> node_4
    node_425 --> node_553
    node_220 --> node_161
    node_17 --> node_566
    node_500 --> node_568
    node_512 --> node_446
    node_7 --> node_98
    node_427 --> node_539
    node_462 --> node_209
    node_4 --> node_285
    node_17 --> node_137
    node_405 --> node_327
    node_435 --> node_32
    node_174 --> node_589
    node_17 --> node_482
    node_402 --> node_161
    node_425 --> node_34
    node_7 --> node_474
    node_392 --> node_275
    node_134 --> node_238
    node_39 --> node_250
    node_534 --> node_601
    node_427 --> node_25
    node_427 --> node_441
    node_572 --> node_657
    node_9 --> node_80
    node_44 --> node_272
    node_134 --> node_270
    node_512 --> node_427
    node_611 --> node_609
    node_241 --> node_232
    node_16 --> node_600
    node_137 --> node_243
    node_9 --> node_207
    node_365 --> node_159
    node_16 --> node_503
    node_44 --> node_277
    node_4 --> node_294
    node_373 --> node_137
    node_576 --> node_309
    node_51 --> node_449
    node_120 --> node_235
    node_120 --> node_276
    node_59 --> node_179
    node_16 --> node_517
    node_17 --> node_203
    node_39 --> node_296
    node_51 --> node_166
    node_241 --> node_261
    node_300 --> node_576
    node_352 --> node_102
    node_134 --> node_165
    node_17 --> node_366
    node_405 --> node_305
    node_576 --> node_658
    node_577 --> node_179
    node_39 --> node_178
    node_17 --> node_18
    node_59 --> node_363
    node_39 --> node_294
    node_39 --> node_262
    node_39 --> node_76
    node_39 --> node_424
    node_44 --> node_354
    node_232 --> node_231
    node_17 --> node_98
    node_69 --> node_74
    node_120 --> node_198
    node_120 --> node_256
    node_405 --> node_288
    node_51 --> node_105
    node_356 --> node_152
    node_604 --> node_606
    node_406 --> node_248
    node_41 --> node_55
    node_134 --> node_160
    node_373 --> node_143
    node_576 --> node_315
    node_39 --> node_20
    node_590 --> node_589
    node_303 --> node_180
    node_373 --> node_203
    node_17 --> node_474
    node_373 --> node_271
    node_11 --> node_109
    node_19 --> node_413
    node_134 --> node_182
    node_300 --> node_584
    node_373 --> node_202
    node_399 --> node_167
    node_405 --> node_249
    node_563 --> node_603
    node_16 --> node_313
    node_342 --> node_181
    node_17 --> node_362
    node_54 --> node_260
    node_120 --> node_216
    node_220 --> node_162
    node_395 --> node_405
    node_68 --> node_72
    node_44 --> node_222
    node_44 --> node_241
    node_24 --> node_12
    node_165 --> node_164
    node_502 --> node_656
    node_523 --> node_510
    node_120 --> node_254
    node_9 --> node_83
    node_489 --> node_327
    node_56 --> node_413
    node_47 --> node_20
    node_427 --> node_407
    node_134 --> node_186
    node_211 --> node_213
    node_576 --> node_563
    node_16 --> node_180
    node_150 --> node_149
    node_572 --> node_666
    node_137 --> node_412
    node_425 --> node_370
    node_17 --> node_338
    node_39 --> node_334
    node_35 --> node_32
    node_241 --> node_146
    node_9 --> node_121
    node_39 --> node_267
    node_416 --> node_71
    node_39 --> node_516
    node_5 --> node_4
    node_434 --> node_381
    node_4 --> node_560
    node_134 --> node_243
    node_137 --> node_166
    node_308 --> node_22
    node_17 --> node_157
    node_399 --> node_156
    node_177 --> node_176
    node_373 --> node_268
    node_379 --> node_348
    node_406 --> node_196
    node_462 --> node_214
    node_579 --> node_658
    node_134 --> node_229
    node_122 --> node_123
    node_44 --> node_232
    node_537 --> node_539
    node_373 --> node_157
    node_415 --> node_414
    node_241 --> node_178
    node_241 --> node_262
    node_241 --> node_221
    node_425 --> node_671
    node_25 --> node_59
    node_44 --> node_261
    node_405 --> node_320
    node_534 --> node_608
    node_39 --> node_115
    node_352 --> node_579
    node_356 --> node_177
    node_39 --> node_22
    node_155 --> node_110
    node_17 --> node_380
    node_68 --> node_76
    node_290 --> node_288
    node_47 --> node_576
    node_537 --> node_25
    node_39 --> node_184
    node_381 --> node_172
    node_520 --> node_438
    node_405 --> node_298
    node_352 --> node_567
    node_298 --> node_662
    node_51 --> node_224
    node_44 --> node_211
    node_503 --> node_667
    node_402 --> node_358
    node_51 --> node_199
    node_577 --> node_563
    node_469 --> node_32
    node_9 --> node_411
    node_4 --> node_150
    node_143 --> node_560
    node_576 --> node_645
    node_39 --> node_293
    node_338 --> node_337
    node_389 --> node_403
    node_572 --> node_664
    node_425 --> node_551
    node_72 --> node_343
    node_373 --> node_270
    node_39 --> node_122
    node_405 --> node_156
    node_352 --> node_582
    node_405 --> node_279
    node_4 --> node_581
    node_461 --> node_161
    node_492 --> node_372
    node_417 --> node_672
    node_17 --> node_230
    node_51 --> node_287
    node_126 --> node_122
    node_243 --> node_242
    node_65 --> node_70
    node_528 --> node_670
    node_405 --> node_309
    node_616 --> node_141
    node_39 --> node_141
    node_44 --> node_146
    node_363 --> node_478
    node_496 --> node_529
    node_17 --> node_152
    node_120 --> node_275
    node_496 --> node_492
    node_576 --> node_316
    node_617 --> node_141
    node_572 --> node_327
    node_17 --> node_374
    node_279 --> node_278
    node_497 --> node_639
    node_4 --> node_303
    node_51 --> node_80
    node_402 --> node_361
    node_172 --> node_236
    node_241 --> node_236
    node_359 --> node_162
    node_241 --> node_209
    node_51 --> node_340
    node_51 --> node_263
    node_137 --> node_224
    node_451 --> node_601
    node_120 --> node_259
    node_405 --> node_315
    node_137 --> node_199
    node_427 --> node_424
    node_6 --> node_141
    node_59 --> node_18
    node_616 --> node_298
    node_39 --> node_298
    node_352 --> node_78
    node_253 --> node_413
    node_44 --> node_178
    node_465 --> node_139
    node_39 --> node_638
    node_241 --> node_249
    node_44 --> node_262
    node_398 --> node_205
    node_137 --> node_135
    node_4 --> node_179
    node_352 --> node_614
    node_425 --> node_7
    node_452 --> node_583
    node_464 --> node_166
    node_572 --> node_305
    node_42 --> node_179
    node_4 --> node_163
    node_291 --> node_289
    node_143 --> node_141
    node_533 --> node_141
    node_28 --> node_673
    node_80 --> node_81
    node_137 --> node_287
    node_16 --> node_669
    node_134 --> node_335
    node_241 --> node_266
    node_47 --> node_298
    node_373 --> node_243
    node_535 --> node_318
    node_41 --> node_40
    node_352 --> node_343
    node_403 --> node_149
    node_6 --> node_298
    node_404 --> node_160
    node_461 --> node_162
    node_51 --> node_550
    node_512 --> node_444
    node_16 --> node_489
    node_364 --> node_224
    node_406 --> node_191
    node_197 --> node_195
    node_553 --> node_552
    node_39 --> node_415
    node_50 --> node_20
    node_51 --> node_83
    node_51 --> node_272
    node_373 --> node_229
    node_406 --> node_192
    node_134 --> node_233
    node_120 --> node_221
    node_51 --> node_225
    node_241 --> node_201
    node_546 --> node_549
    node_356 --> node_199
    node_137 --> node_340
    node_51 --> node_352
    node_137 --> node_263
    node_474 --> node_472
    node_44 --> node_334
    node_4 --> node_280
    node_17 --> node_177
    node_51 --> node_121
    node_39 --> node_41
    node_383 --> node_344
    node_494 --> node_626
    node_607 --> node_605
    node_39 --> node_47
    node_19 --> node_141
    node_22 --> node_401
    node_19 --> node_581
    node_83 --> node_85
    node_576 --> node_641
    node_134 --> node_126
    node_17 --> node_449
    node_4 --> node_253
    node_352 --> node_580
    node_7 --> node_444
    node_405 --> node_311
    node_4 --> node_672
    node_172 --> node_167
    node_303 --> node_302
    node_356 --> node_287
    node_39 --> node_13
    node_39 --> node_369
    node_356 --> node_154
    node_395 --> node_407
    node_56 --> node_581
    node_9 --> node_20
    node_39 --> node_432
    node_134 --> node_291
    node_303 --> node_413
    node_399 --> node_157
    node_197 --> node_190
    node_405 --> node_143
    node_587 --> node_304
    node_27 --> node_575
    node_373 --> node_674
    node_648 --> node_326
    node_402 --> node_360
    node_17 --> node_379
    node_51 --> node_222
    node_39 --> node_553
    node_255 --> node_166
    node_16 --> node_649
    node_51 --> node_241
    node_373 --> node_166
    node_379 --> node_340
    node_154 --> node_155
    node_47 --> node_13
    node_425 --> node_77
    node_425 --> node_142
    node_44 --> node_249
    node_462 --> node_157
    node_39 --> node_88
    node_261 --> node_139
    node_137 --> node_272
    node_587 --> node_642
    node_137 --> node_277
    node_137 --> node_225
    node_172 --> node_279
    node_241 --> node_156
    node_241 --> node_279
    node_576 --> node_605
    node_137 --> node_352
    node_56 --> node_251
    node_51 --> node_223
    node_19 --> node_179
    node_248 --> node_246
    node_19 --> node_498
    node_492 --> node_363
    node_51 --> node_411
    node_576 --> node_640
    node_44 --> node_293
    node_17 --> node_444
    node_120 --> node_236
    node_4 --> node_8
    node_39 --> node_145
    node_120 --> node_209
    node_363 --> node_576
    node_160 --> node_158
    node_406 --> node_197
    node_405 --> node_316
    node_4 --> node_173
    node_7 --> node_395
    node_41 --> node_44
    node_56 --> node_179
    node_39 --> node_228
    node_389 --> node_405
    node_464 --> node_168
    node_73 --> node_71
    node_22 --> node_393
    node_182 --> node_300
    node_66 --> node_141
    node_397 --> node_171
    node_120 --> node_127
    node_549 --> node_33
    node_4 --> node_128
    node_529 --> node_652
    node_4 --> node_482
    node_9 --> node_115
    node_83 --> node_87
    node_137 --> node_222
    node_572 --> node_309
    node_356 --> node_272
    node_16 --> node_607
    node_120 --> node_266
    node_137 --> node_241
    node_39 --> node_143
    node_365 --> node_162
    node_379 --> node_352
    node_394 --> node_346
    node_39 --> node_632
    node_439 --> node_369
    node_513 --> node_310
    node_7 --> node_387
    node_356 --> node_277
    node_356 --> node_225
    node_4 --> node_134
    node_39 --> node_271
    node_39 --> node_202
    node_581 --> node_139
    node_17 --> node_492
    node_352 --> node_571
    node_373 --> node_335
    node_425 --> node_357
    node_427 --> node_420
    node_68 --> node_13
    node_16 --> node_319
    node_51 --> node_211
    node_624 --> node_603
    node_394 --> node_674
    node_16 --> node_644
    node_298 --> node_668
    node_120 --> node_303
    node_29 --> node_372
    node_19 --> node_672
    node_402 --> node_157
    node_120 --> node_201
    node_356 --> node_354
    node_7 --> node_80
    node_576 --> node_324
    node_134 --> node_235
    node_134 --> node_276
    node_572 --> node_315
    node_17 --> node_395
    node_425 --> node_418
    node_51 --> node_218
    node_640 --> node_22
    node_534 --> node_602
    node_43 --> node_539
    node_520 --> node_435
    node_39 --> node_370
    node_462 --> node_152
    node_572 --> node_307
    node_16 --> node_476
    node_364 --> node_222
    node_352 --> node_113
    node_397 --> node_164
    node_39 --> node_268
    node_496 --> node_483
    node_4 --> node_57
    node_44 --> node_156
    node_134 --> node_198
    node_134 --> node_256
    node_41 --> node_43
    node_223 --> node_260
    node_43 --> node_25
    node_373 --> node_224
    node_356 --> node_222
    node_425 --> node_26
    node_587 --> node_634
    node_356 --> node_241
    node_137 --> node_261
    node_241 --> node_137
    node_373 --> node_199
    node_17 --> node_287
    node_17 --> node_387
    node_17 --> node_154
    node_120 --> node_281
    node_493 --> node_141
    node_545 --> node_556
    node_51 --> node_250
    node_72 --> node_76
    node_39 --> node_471
    node_253 --> node_581
    node_142 --> node_560
    node_511 --> node_141
    node_425 --> node_117
    node_587 --> node_656
    node_16 --> node_304
    node_496 --> node_478
    node_134 --> node_216
    node_373 --> node_291
    node_363 --> node_298
    node_255 --> node_168
    node_29 --> node_22
    node_134 --> node_219
    node_383 --> node_348
    node_576 --> node_579
    node_137 --> node_211
    node_56 --> node_572
    node_72 --> node_20
    node_19 --> node_8
    node_291 --> node_290
    node_39 --> node_671
    node_182 --> node_576
    node_248 --> node_247
    node_17 --> node_80
    node_51 --> node_296
    node_16 --> node_642
    node_120 --> node_118
    node_531 --> node_669
    node_241 --> node_143
    node_541 --> node_540
    node_51 --> node_294
    node_383 --> node_346
    node_241 --> node_203
    node_120 --> node_279
    node_427 --> node_13
    node_134 --> node_223
    node_405 --> node_257
    node_195 --> node_192
    node_137 --> node_218
    node_401 --> node_210
    node_377 --> node_674
    node_486 --> node_416
    node_241 --> node_202
    node_4 --> node_172
    node_407 --> node_171
    node_394 --> node_239
    node_619 --> node_561
    node_511 --> node_298
    node_555 --> node_548
    node_356 --> node_232
    node_7 --> node_121
    node_572 --> node_650
    node_39 --> node_238
    node_51 --> node_20
    node_383 --> node_674
    node_39 --> node_591
    node_572 --> node_311
    node_465 --> node_260
    node_529 --> node_316
    node_120 --> node_208
    node_17 --> node_365
    node_9 --> node_14
    node_356 --> node_261
    node_39 --> node_270
    node_39 --> node_381
    node_373 --> node_340
    node_405 --> node_243
    node_373 --> node_263
    node_494 --> node_604
    node_399 --> node_166
    node_39 --> node_386
    node_405 --> node_242
    node_137 --> node_250
    node_9 --> node_415
    node_41 --> node_58
    node_4 --> node_321
    node_405 --> node_326
    node_298 --> node_327
    node_462 --> node_674
    node_590 --> node_596
    node_39 --> node_165
    node_145 --> node_338
    node_513 --> node_642
    node_120 --> node_339
    node_17 --> node_367
    node_356 --> node_211
    node_512 --> node_496
    node_241 --> node_268
    node_390 --> node_674
    node_395 --> node_404
    node_39 --> node_342
    node_303 --> node_584
    node_51 --> node_334
    node_576 --> node_662
    node_7 --> node_49
    node_9 --> node_41
    node_51 --> node_267
    node_17 --> node_272
    node_142 --> node_141
    node_545 --> node_555
    node_303 --> node_581
    node_39 --> node_32
    node_137 --> node_296
    node_365 --> node_672
    node_78 --> node_175
    node_182 --> node_251
    node_182 --> node_633
    node_17 --> node_277
    node_406 --> node_188
    node_150 --> node_151
    node_39 --> node_160
    node_137 --> node_178
    node_407 --> node_164
    node_620 --> node_141
    node_519 --> node_637
    node_405 --> node_332
    node_137 --> node_294
    node_566 --> node_564
    node_566 --> node_300
    node_39 --> node_595
    node_241 --> node_157
    node_39 --> node_182
    node_17 --> node_121
    node_211 --> node_214
    node_395 --> node_398
    node_120 --> node_286
    node_379 --> node_341
    node_51 --> node_560
    node_16 --> node_584
    node_44 --> node_228
    node_145 --> node_336
    node_373 --> node_272
    node_7 --> node_496
    node_134 --> node_218
    node_17 --> node_354
    node_228 --> node_227
    node_17 --> node_375
    node_356 --> node_146
    node_255 --> node_277
    node_4 --> node_230
    node_373 --> node_225
    node_50 --> node_110
    node_39 --> node_186
    node_39 --> node_7
    node_88 --> node_179
    node_373 --> node_352
    node_303 --> node_251
    node_356 --> node_250
    node_344 --> node_141
    node_405 --> node_138
    node_9 --> node_553
    node_553 --> node_546
    node_620 --> node_298
    node_398 --> node_253
    node_425 --> node_455
    node_405 --> node_324
    node_44 --> node_143
    node_7 --> node_546
    node_623 --> node_576
    node_134 --> node_341
    node_4 --> node_152
    node_394 --> node_343
    node_404 --> node_159
    node_39 --> node_243
    node_51 --> node_184
    node_44 --> node_271
    node_159 --> node_20
    node_359 --> node_160
    node_134 --> node_275
    node_44 --> node_202
    node_412 --> node_141
    node_16 --> node_634
    node_405 --> node_142
    node_587 --> node_652
    node_120 --> node_137
    node_177 --> node_174
    node_17 --> node_222
    node_17 --> node_241
    node_303 --> node_179
    node_120 --> node_482
    node_356 --> node_296
    node_417 --> node_673
    node_134 --> node_285
    node_137 --> node_334
    node_59 --> node_562
    node_58 --> node_363
    node_137 --> node_267
    node_356 --> node_178
    node_51 --> node_293
    node_356 --> node_262
    node_72 --> node_141
    node_39 --> node_330
    node_261 --> node_260
    node_492 --> node_386
    node_39 --> node_229
    node_41 --> node_49
    node_455 --> node_454
    node_402 --> node_674
    node_352 --> node_560
    node_17 --> node_408
    node_51 --> node_122
    node_373 --> node_219
    node_605 --> node_445
    node_51 --> node_150
    node_518 --> node_660
    node_406 --> node_195
    node_17 --> node_496
    node_16 --> node_179
    node_425 --> node_545
    node_593 --> node_596
    node_494 --> node_141
    node_412 --> node_298
    node_496 --> node_576
    node_120 --> node_203
    node_44 --> node_268
    node_71 --> node_72
    node_576 --> node_580
    node_388 --> node_369
    node_51 --> node_141
    node_596 --> node_536
    node_78 --> node_589
    node_72 --> node_298
    node_357 --> node_360
    node_4 --> node_646
    node_17 --> node_232
    node_300 --> node_567
    node_373 --> node_223
    node_523 --> node_662
    node_566 --> node_576
    node_587 --> node_323
    node_296 --> node_295
    node_607 --> node_609
    node_137 --> node_184
    node_399 --> node_168
    node_605 --> node_613
    node_303 --> node_301
    node_17 --> node_261
    node_356 --> node_334
    node_589 --> node_591
    node_405 --> node_335
    node_572 --> node_660
    node_20 --> node_35
    node_439 --> node_403
    node_39 --> node_77
    node_137 --> node_293
    node_39 --> node_142
    node_51 --> node_298
    node_528 --> node_333
    node_17 --> node_211
    node_381 --> node_158
    node_581 --> node_260
    node_47 --> node_674
    node_241 --> node_243
    node_16 --> node_301
    node_137 --> node_122
    node_425 --> node_353
    node_394 --> node_350
    node_137 --> node_150
    node_120 --> node_338
    node_576 --> node_626
    node_160 --> node_156
    node_576 --> node_578
    node_44 --> node_238
    node_352 --> node_141
    node_623 --> node_298
    node_122 --> node_126
    node_39 --> node_71
    node_383 --> node_340
    node_4 --> node_240
    node_120 --> node_157
    node_241 --> node_229
    node_425 --> node_413
    node_44 --> node_270
    node_373 --> node_211
    node_356 --> node_249
    node_576 --> node_609
    node_105 --> node_114
    node_356 --> node_184
    node_405 --> node_199
    node_51 --> node_415
    node_379 --> node_345
    node_579 --> node_580
    node_7 --> node_20
    node_17 --> node_146
    node_403 --> node_151
    node_566 --> node_251
    node_566 --> node_633
    node_373 --> node_218
    node_462 --> node_210
    node_405 --> node_291
    node_591 --> node_595
    node_51 --> node_56
    node_352 --> node_298
    node_356 --> node_293
    node_41 --> node_38
    node_51 --> node_41
    node_464 --> node_171
    node_572 --> node_330
    node_47 --> node_421
    node_496 --> node_298
    node_463 --> node_110
    node_576 --> node_571
    node_16 --> node_652
    node_356 --> node_122
    node_373 --> node_341
    node_39 --> node_335
    node_16 --> node_563
    node_39 --> node_357
    node_587 --> node_331
    node_373 --> node_250
    node_17 --> node_178
    node_17 --> node_262
    node_172 --> node_166
    node_17 --> node_221
    node_241 --> node_166
    node_512 --> node_410
    node_524 --> node_634
    node_197 --> node_194
    node_530 --> node_645
    node_462 --> node_147
    node_383 --> node_352
    node_16 --> node_306
    node_39 --> node_233
    node_51 --> node_672
    node_44 --> node_186
    node_39 --> node_418
    node_475 --> node_604
    node_411 --> node_142
    node_105 --> node_109
    node_17 --> node_20
    node_51 --> node_553
    node_373 --> node_296
    node_566 --> node_139
    node_7 --> node_576
    node_39 --> node_525
    node_179 --> node_180
    node_9 --> node_537
    node_120 --> node_230
    node_373 --> node_294
    node_44 --> node_243
    node_283 --> node_546
    node_7 --> node_288
    node_618 --> node_179
    node_39 --> node_126
    node_464 --> node_164
    node_39 --> node_103
    node_398 --> node_206
    node_425 --> node_448
    node_39 --> node_26
    node_7 --> node_115
    node_68 --> node_71
    node_508 --> node_658
    node_7 --> node_410
    node_7 --> node_22
    node_120 --> node_152
    node_377 --> node_241
    node_16 --> node_323
    node_576 --> node_668
    node_607 --> node_610
    node_405 --> node_159
    node_576 --> node_666
    node_462 --> node_148
    node_44 --> node_229
    node_381 --> node_161
    node_39 --> node_291
    node_39 --> node_117
    node_51 --> node_145
    node_16 --> node_587
    node_35 --> node_394
    node_360 --> node_106
    node_397 --> node_172
    node_134 --> node_303
    node_455 --> node_453
```

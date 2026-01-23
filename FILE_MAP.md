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
| `plan.md` | 🔵 Entry Point | File: plan.md |
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
        node_17[".coverage"]
        node_35[".djlint.toml"]
        node_0[".gitattributes"]
        node_15[".gitignore"]
        node_2[".markdownlint.json"]
        node_27[".yamllint"]
        node_13["=0.9.4"]
        node_28["IPV6_AUDIT.md"]
        node_31["LICENSE"]
        node_8["README.md"]
        node_4["TODO.md"]
        node_18["YAML_FILES_REPORT.md"]
        node_10["agentic_workflow.sh"]
        node_3["aid_e_log.txt"]
        node_32["ansible.cfg"]
        node_21["bootstrap.sh"]
        node_30["check_all_playbooks.sh"]
        node_25["check_deps.py"]
        node_20["create_todo_issues.sh"]
        node_12["debug_expert.sh"]
        node_5["generate_issue_script.py"]
        node_1["hostfile"]
        node_34["inventory.yaml"]
        node_33["local_inventory.ini"]
        node_26["package.json"]
        node_7["plan.md"]
        node_23["playbook.yaml"]
        node_36["provisioning.py"]
        node_24["pytest.ini"]
        node_14["requirements-dev.txt"]
        node_16["run_tests.sh"]
        node_9["start_services.sh"]
        node_19["supervisor.py"]
        node_22["test.wav"]
        node_6["test_imports.py"]
        node_11["test_playbook.yml"]
        node_29["verify_config_load.py"]
    end
    subgraph dir__github [.github]
        direction TB
        node_61["AGENTIC_README.md"]
    end
    subgraph dir__github_workflows [.github/workflows]
        direction TB
        node_65["auto-merge.yml"]
        node_66["ci.yml"]
        node_62["create-issues-from-files.yml"]
        node_64["jules-queue.yml"]
        node_63["remote-verify.yml"]
    end
    subgraph dir__husky [.husky]
        direction TB
        node_413["pre-push"]
    end
    subgraph dir__opencode [.opencode]
        direction TB
        node_536["README.md"]
        node_537["opencode.json"]
    end
    subgraph dir_ansible [ansible]
        direction TB
        node_99["README.md"]
        node_100["lint_nomad.yaml"]
        node_101["run_download_models.yaml"]
    end
    subgraph dir_ansible_filter_plugins [ansible/filter_plugins]
        direction TB
        node_116["README.md"]
        node_117["safe_flatten.py"]
    end
    subgraph dir_ansible_jobs [ansible/jobs]
        direction TB
        node_106["README.md"]
        node_111["benchmark.nomad"]
        node_103["evolve-prompt.nomad.j2"]
        node_110["expert-debug.nomad"]
        node_107["expert.nomad.j2"]
        node_105["filebrowser.nomad.j2"]
        node_102["health-check.nomad.j2"]
        node_108["llamacpp-batch.nomad.j2"]
        node_104["llamacpp-rpc.nomad.j2"]
        node_115["model-benchmark.nomad.j2"]
        node_114["pipecatapp.nomad"]
        node_113["router.nomad.j2"]
        node_109["test-runner.nomad.j2"]
        node_112["vllm.nomad.j2"]
    end
    subgraph dir_ansible_roles [ansible/roles]
        direction TB
        node_118["README.md"]
    end
    subgraph dir_ansible_roles_benchmark_models_tasks [ansible/roles/benchmark_models/tasks]
        direction TB
        node_152["benchmark_loop.yaml"]
        node_151["main.yaml"]
    end
    subgraph dir_ansible_roles_benchmark_models_templates [ansible/roles/benchmark_models/templates]
        direction TB
        node_150["model-benchmark.nomad.j2"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_defaults [ansible/roles/bootstrap_agent/defaults]
        direction TB
        node_216["main.yaml"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_tasks [ansible/roles/bootstrap_agent/tasks]
        direction TB
        node_217["deploy_llama_cpp_model.yaml"]
        node_218["main.yaml"]
    end
    subgraph dir_ansible_roles_claude_clone_tasks [ansible/roles/claude_clone/tasks]
        direction TB
        node_246["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tools_tasks [ansible/roles/common-tools/tasks]
        direction TB
        node_205["main.yaml"]
    end
    subgraph dir_ansible_roles_common_handlers [ansible/roles/common/handlers]
        direction TB
        node_143["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tasks [ansible/roles/common/tasks]
        direction TB
        node_147["main.yaml"]
        node_148["network_repair.yaml"]
    end
    subgraph dir_ansible_roles_common_templates [ansible/roles/common/templates]
        direction TB
        node_146["cluster-ip-alias.service.j2"]
        node_145["hosts.j2"]
        node_144["update-ssh-authorized-keys.sh.j2"]
    end
    subgraph dir_ansible_roles_config_manager_tasks [ansible/roles/config_manager/tasks]
        direction TB
        node_238["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_defaults [ansible/roles/consul/defaults]
        direction TB
        node_154["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_handlers [ansible/roles/consul/handlers]
        direction TB
        node_153["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_tasks [ansible/roles/consul/tasks]
        direction TB
        node_159["acl.yaml"]
        node_157["main.yaml"]
        node_158["tls.yaml"]
    end
    subgraph dir_ansible_roles_consul_templates [ansible/roles/consul/templates]
        direction TB
        node_156["consul.hcl.j2"]
        node_155["consul.service.j2"]
    end
    subgraph dir_ansible_roles_desktop_extras_tasks [ansible/roles/desktop_extras/tasks]
        direction TB
        node_124["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_handlers [ansible/roles/docker/handlers]
        direction TB
        node_206["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_molecule_default [ansible/roles/docker/molecule/default]
        direction TB
        node_209["converge.yml"]
        node_210["molecule.yml"]
        node_212["prepare.yml"]
        node_211["verify.yml"]
    end
    subgraph dir_ansible_roles_docker_tasks [ansible/roles/docker/tasks]
        direction TB
        node_208["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_templates [ansible/roles/docker/templates]
        direction TB
        node_207["daemon.json.j2"]
    end
    subgraph dir_ansible_roles_download_models_files [ansible/roles/download_models/files]
        direction TB
        node_141["download_hf_repo.py"]
    end
    subgraph dir_ansible_roles_download_models_tasks [ansible/roles/download_models/tasks]
        direction TB
        node_142["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_defaults [ansible/roles/exo/defaults]
        direction TB
        node_247["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_files [ansible/roles/exo/files]
        direction TB
        node_248["Dockerfile"]
    end
    subgraph dir_ansible_roles_exo_tasks [ansible/roles/exo/tasks]
        direction TB
        node_250["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_templates [ansible/roles/exo/templates]
        direction TB
        node_249["exo.nomad.j2"]
    end
    subgraph dir_ansible_roles_headscale_defaults [ansible/roles/headscale/defaults]
        direction TB
        node_269["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_handlers [ansible/roles/headscale/handlers]
        direction TB
        node_268["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_tasks [ansible/roles/headscale/tasks]
        direction TB
        node_272["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_templates [ansible/roles/headscale/templates]
        direction TB
        node_271["config.yaml.j2"]
        node_270["headscale.service.j2"]
    end
    subgraph dir_ansible_roles_heretic_tool_defaults [ansible/roles/heretic_tool/defaults]
        direction TB
        node_219["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_meta [ansible/roles/heretic_tool/meta]
        direction TB
        node_220["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_tasks [ansible/roles/heretic_tool/tasks]
        direction TB
        node_221["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_meta [ansible/roles/home_assistant/meta]
        direction TB
        node_253["main.yaml"]
        node_252["main.yml"]
    end
    subgraph dir_ansible_roles_home_assistant_tasks [ansible/roles/home_assistant/tasks]
        direction TB
        node_256["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_templates [ansible/roles/home_assistant/templates]
        direction TB
        node_255["configuration.yaml.j2"]
        node_254["home_assistant.nomad.j2"]
    end
    subgraph dir_ansible_roles_kittentts_tasks [ansible/roles/kittentts/tasks]
        direction TB
        node_160["main.yaml"]
    end
    subgraph dir_ansible_roles_librarian_defaults [ansible/roles/librarian/defaults]
        direction TB
        node_126["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_tasks [ansible/roles/librarian/tasks]
        direction TB
        node_130["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_templates [ansible/roles/librarian/templates]
        direction TB
        node_127["librarian.service.j2"]
        node_129["librarian_agent.py.j2"]
        node_128["spacedrive.service.j2"]
    end
    subgraph dir_ansible_roles_llama_cpp_handlers [ansible/roles/llama_cpp/handlers]
        direction TB
        node_199["main.yaml"]
    end
    subgraph dir_ansible_roles_llama_cpp_molecule_default [ansible/roles/llama_cpp/molecule/default]
        direction TB
        node_202["converge.yml"]
        node_203["molecule.yml"]
        node_204["verify.yml"]
    end
    subgraph dir_ansible_roles_llama_cpp_tasks [ansible/roles/llama_cpp/tasks]
        direction TB
        node_200["main.yaml"]
        node_201["run_single_rpc_job.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_tasks [ansible/roles/llxprt_code/tasks]
        direction TB
        node_240["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_templates [ansible/roles/llxprt_code/templates]
        direction TB
        node_239["llxprt-code.env.j2"]
    end
    subgraph dir_ansible_roles_magic_mirror_defaults [ansible/roles/magic_mirror/defaults]
        direction TB
        node_291["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_handlers [ansible/roles/magic_mirror/handlers]
        direction TB
        node_290["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_tasks [ansible/roles/magic_mirror/tasks]
        direction TB
        node_293["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_templates [ansible/roles/magic_mirror/templates]
        direction TB
        node_292["magic_mirror.nomad.j2"]
    end
    subgraph dir_ansible_roles_mcp_server_defaults [ansible/roles/mcp_server/defaults]
        direction TB
        node_196["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_handlers [ansible/roles/mcp_server/handlers]
        direction TB
        node_195["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_tasks [ansible/roles/mcp_server/tasks]
        direction TB
        node_198["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_templates [ansible/roles/mcp_server/templates]
        direction TB
        node_197["mcp_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_graph_tasks [ansible/roles/memory_graph/tasks]
        direction TB
        node_237["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_graph_templates [ansible/roles/memory_graph/templates]
        direction TB
        node_236["memory-graph.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_service_files [ansible/roles/memory_service/files]
        direction TB
        node_176["app.py"]
        node_177["pmm_memory.py"]
    end
    subgraph dir_ansible_roles_memory_service_handlers [ansible/roles/memory_service/handlers]
        direction TB
        node_175["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_tasks [ansible/roles/memory_service/tasks]
        direction TB
        node_179["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_templates [ansible/roles/memory_service/templates]
        direction TB
        node_178["memory_service.nomad.j2"]
    end
    subgraph dir_ansible_roles_moe_gateway_files [ansible/roles/moe_gateway/files]
        direction TB
        node_171["gateway.py"]
    end
    subgraph dir_ansible_roles_moe_gateway_files_static [ansible/roles/moe_gateway/files/static]
        direction TB
        node_172["index.html"]
    end
    subgraph dir_ansible_roles_moe_gateway_handlers [ansible/roles/moe_gateway/handlers]
        direction TB
        node_170["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_tasks [ansible/roles/moe_gateway/tasks]
        direction TB
        node_174["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_templates [ansible/roles/moe_gateway/templates]
        direction TB
        node_173["moe-gateway.nomad.j2"]
    end
    subgraph dir_ansible_roles_monitoring_defaults [ansible/roles/monitoring/defaults]
        direction TB
        node_184["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_files [ansible/roles/monitoring/files]
        direction TB
        node_185["llm_dashboard.json"]
    end
    subgraph dir_ansible_roles_monitoring_tasks [ansible/roles/monitoring/tasks]
        direction TB
        node_194["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_templates [ansible/roles/monitoring/templates]
        direction TB
        node_186["dashboards.yaml.j2"]
        node_189["datasource.yaml.j2"]
        node_192["grafana.nomad.j2"]
        node_187["memory-audit.nomad.j2"]
        node_190["mqtt-exporter.nomad.j2"]
        node_193["node-exporter.nomad.j2"]
        node_191["prometheus.nomad.j2"]
        node_188["prometheus.yml.j2"]
    end
    subgraph dir_ansible_roles_mqtt_handlers [ansible/roles/mqtt/handlers]
        direction TB
        node_273["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_meta [ansible/roles/mqtt/meta]
        direction TB
        node_274["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_tasks [ansible/roles/mqtt/tasks]
        direction TB
        node_276["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_templates [ansible/roles/mqtt/templates]
        direction TB
        node_275["mqtt.nomad.j2"]
    end
    subgraph dir_ansible_roles_nanochat_defaults [ansible/roles/nanochat/defaults]
        direction TB
        node_265["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_handlers [ansible/roles/nanochat/handlers]
        direction TB
        node_264["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_tasks [ansible/roles/nanochat/tasks]
        direction TB
        node_267["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_templates [ansible/roles/nanochat/templates]
        direction TB
        node_266["nanochat.nomad.j2"]
    end
    subgraph dir_ansible_roles_nats_handlers [ansible/roles/nats/handlers]
        direction TB
        node_230["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_tasks [ansible/roles/nats/tasks]
        direction TB
        node_232["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_templates [ansible/roles/nats/templates]
        direction TB
        node_231["nats.nomad.j2"]
    end
    subgraph dir_ansible_roles_nfs_tasks [ansible/roles/nfs/tasks]
        direction TB
        node_125["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_handlers [ansible/roles/nixos_pxe_server/handlers]
        direction TB
        node_260["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_tasks [ansible/roles/nixos_pxe_server/tasks]
        direction TB
        node_263["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_templates [ansible/roles/nixos_pxe_server/templates]
        direction TB
        node_262["boot.ipxe.nix.j2"]
        node_261["configuration.nix.j2"]
    end
    subgraph dir_ansible_roles_nomad_defaults [ansible/roles/nomad/defaults]
        direction TB
        node_163["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_handlers [ansible/roles/nomad/handlers]
        direction TB
        node_162["main.yaml"]
        node_161["restart_nomad_handler_tasks.yaml"]
    end
    subgraph dir_ansible_roles_nomad_tasks [ansible/roles/nomad/tasks]
        direction TB
        node_169["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_templates [ansible/roles/nomad/templates]
        direction TB
        node_168["client.hcl.j2"]
        node_165["nomad.hcl.server.j2"]
        node_164["nomad.service.j2"]
        node_166["nomad.sh.j2"]
        node_167["server.hcl.j2"]
    end
    subgraph dir_ansible_roles_opencode_handlers [ansible/roles/opencode/handlers]
        direction TB
        node_213["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_tasks [ansible/roles/opencode/tasks]
        direction TB
        node_215["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_templates [ansible/roles/opencode/templates]
        direction TB
        node_214["opencode.nomad.j2"]
    end
    subgraph dir_ansible_roles_openworkers_handlers [ansible/roles/openworkers/handlers]
        direction TB
        node_119["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_tasks [ansible/roles/openworkers/tasks]
        direction TB
        node_123["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_templates [ansible/roles/openworkers/templates]
        direction TB
        node_122["openworkers-bootstrap.nomad.j2"]
        node_120["openworkers-infra.nomad.j2"]
        node_121["openworkers-runners.nomad.j2"]
    end
    subgraph dir_ansible_roles_paddler_tasks [ansible/roles/paddler/tasks]
        direction TB
        node_259["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_defaults [ansible/roles/pipecatapp/defaults]
        direction TB
        node_338["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_handlers [ansible/roles/pipecatapp/handlers]
        direction TB
        node_337["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_tasks [ansible/roles/pipecatapp/tasks]
        direction TB
        node_349["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates [ansible/roles/pipecatapp/templates]
        direction TB
        node_342["archivist.nomad.j2"]
        node_339["pipecat.env.j2"]
        node_340["pipecatapp.nomad.j2"]
        node_341["start_pipecatapp.sh.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_prompts [ansible/roles/pipecatapp/templates/prompts]
        direction TB
        node_345["coding_expert.txt.j2"]
        node_346["creative_expert.txt.j2"]
        node_344["cynic_expert.txt.j2"]
        node_343["router.txt.j2"]
        node_347["tron_agent.txt.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_workflows [ansible/roles/pipecatapp/templates/workflows]
        direction TB
        node_348["default_agent_loop.yaml.j2"]
    end
    subgraph dir_ansible_roles_postgres_handlers [ansible/roles/postgres/handlers]
        direction TB
        node_233["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_tasks [ansible/roles/postgres/tasks]
        direction TB
        node_235["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_templates [ansible/roles/postgres/templates]
        direction TB
        node_234["postgres.nomad.j2"]
    end
    subgraph dir_ansible_roles_power_manager_defaults [ansible/roles/power_manager/defaults]
        direction TB
        node_284["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_files [ansible/roles/power_manager/files]
        direction TB
        node_285["power_agent.py"]
        node_286["traffic_monitor.c"]
    end
    subgraph dir_ansible_roles_power_manager_handlers [ansible/roles/power_manager/handlers]
        direction TB
        node_283["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_tasks [ansible/roles/power_manager/tasks]
        direction TB
        node_288["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_templates [ansible/roles/power_manager/templates]
        direction TB
        node_287["power-agent.service.j2"]
    end
    subgraph dir_ansible_roles_preflight_checks_tasks [ansible/roles/preflight_checks/tasks]
        direction TB
        node_336["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_files [ansible/roles/provisioning_api/files]
        direction TB
        node_223["provisioning_api.py"]
    end
    subgraph dir_ansible_roles_provisioning_api_handlers [ansible/roles/provisioning_api/handlers]
        direction TB
        node_222["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_tasks [ansible/roles/provisioning_api/tasks]
        direction TB
        node_225["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_templates [ansible/roles/provisioning_api/templates]
        direction TB
        node_224["provisioning-api.service.j2"]
    end
    subgraph dir_ansible_roles_pxe_server_defaults [ansible/roles/pxe_server/defaults]
        direction TB
        node_278["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_handlers [ansible/roles/pxe_server/handlers]
        direction TB
        node_277["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_tasks [ansible/roles/pxe_server/tasks]
        direction TB
        node_282["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_templates [ansible/roles/pxe_server/templates]
        direction TB
        node_279["boot.ipxe.j2"]
        node_281["dhcpd.conf.j2"]
        node_280["preseed.cfg.j2"]
    end
    subgraph dir_ansible_roles_python_deps_files [ansible/roles/python_deps/files]
        direction TB
        node_257["requirements.txt"]
    end
    subgraph dir_ansible_roles_python_deps_tasks [ansible/roles/python_deps/tasks]
        direction TB
        node_258["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_defaults [ansible/roles/semantic_router/defaults]
        direction TB
        node_131["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_tasks [ansible/roles/semantic_router/tasks]
        direction TB
        node_134["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_templates [ansible/roles/semantic_router/templates]
        direction TB
        node_132["Dockerfile.j2"]
        node_133["semantic-router.nomad.j2"]
    end
    subgraph dir_ansible_roles_sunshine_defaults [ansible/roles/sunshine/defaults]
        direction TB
        node_227["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_handlers [ansible/roles/sunshine/handlers]
        direction TB
        node_226["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_tasks [ansible/roles/sunshine/tasks]
        direction TB
        node_229["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_templates [ansible/roles/sunshine/templates]
        direction TB
        node_228["sunshine.nomad.j2"]
    end
    subgraph dir_ansible_roles_system_deps_tasks [ansible/roles/system_deps/tasks]
        direction TB
        node_149["main.yaml"]
    end
    subgraph dir_ansible_roles_tailscale_tasks [ansible/roles/tailscale/tasks]
        direction TB
        node_251["main.yaml"]
    end
    subgraph dir_ansible_roles_term_everything_tasks [ansible/roles/term_everything/tasks]
        direction TB
        node_289["main.yml"]
    end
    subgraph dir_ansible_roles_tool_server [ansible/roles/tool_server]
        direction TB
        node_297["Dockerfile"]
        node_295["app.py"]
        node_296["entrypoint.sh"]
        node_298["pmm_memory.py"]
        node_294["preload_models.py"]
    end
    subgraph dir_ansible_roles_tool_server_tasks [ansible/roles/tool_server/tasks]
        direction TB
        node_300["main.yaml"]
    end
    subgraph dir_ansible_roles_tool_server_templates [ansible/roles/tool_server/templates]
        direction TB
        node_299["tool_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_tool_server_tools [ansible/roles/tool_server/tools]
        direction TB
        node_305["ansible_tool.py"]
        node_309["archivist_tool.py"]
        node_314["claude_clone_tool.py"]
        node_316["code_runner_tool.py"]
        node_312["council_tool.py"]
        node_322["desktop_control_tool.py"]
        node_304["file_editor_tool.py"]
        node_321["final_answer_tool.py"]
        node_329["gemini_cli.py"]
        node_303["get_nomad_job.py"]
        node_301["git_tool.py"]
        node_307["ha_tool.py"]
        node_308["llxprt_code_tool.py"]
        node_327["mcp_tool.py"]
        node_315["opencode_tool.py"]
        node_310["orchestrator_tool.py"]
        node_326["planner_tool.py"]
        node_302["power_tool.py"]
        node_306["project_mapper_tool.py"]
        node_319["prompt_improver_tool.py"]
        node_313["rag_tool.py"]
        node_323["sandbox.ts"]
        node_325["shell_tool.py"]
        node_311["smol_agent_tool.py"]
        node_317["ssh_tool.py"]
        node_324["summarizer_tool.py"]
        node_318["swarm_tool.py"]
        node_330["tap_service.py"]
        node_328["term_everything_tool.py"]
        node_320["web_browser_tool.py"]
    end
    subgraph dir_ansible_roles_unified_fs_defaults [ansible/roles/unified_fs/defaults]
        direction TB
        node_242["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_files [ansible/roles/unified_fs/files]
        direction TB
        node_243["unified_fs_agent.py"]
    end
    subgraph dir_ansible_roles_unified_fs_handlers [ansible/roles/unified_fs/handlers]
        direction TB
        node_241["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_tasks [ansible/roles/unified_fs/tasks]
        direction TB
        node_245["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_templates [ansible/roles/unified_fs/templates]
        direction TB
        node_244["unified_fs.service.j2"]
    end
    subgraph dir_ansible_roles_vision_defaults [ansible/roles/vision/defaults]
        direction TB
        node_332["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_handlers [ansible/roles/vision/handlers]
        direction TB
        node_331["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_tasks [ansible/roles/vision/tasks]
        direction TB
        node_335["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_templates [ansible/roles/vision/templates]
        direction TB
        node_334["config.yml.j2"]
        node_333["vision.nomad.j2"]
    end
    subgraph dir_ansible_roles_vllm_tasks [ansible/roles/vllm/tasks]
        direction TB
        node_181["main.yaml"]
        node_182["run_single_vllm_job.yaml"]
    end
    subgraph dir_ansible_roles_vllm_templates [ansible/roles/vllm/templates]
        direction TB
        node_180["vllm-expert.nomad.j2"]
    end
    subgraph dir_ansible_roles_whisper_cpp_tasks [ansible/roles/whisper_cpp/tasks]
        direction TB
        node_183["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service [ansible/roles/world_model_service]
        direction TB
        node_135["world_model.nomad.j2"]
    end
    subgraph dir_ansible_roles_world_model_service_files [ansible/roles/world_model_service/files]
        direction TB
        node_139["Dockerfile"]
        node_138["app.py"]
        node_137["debug_world_model.sh"]
        node_136["requirements.txt"]
    end
    subgraph dir_ansible_roles_world_model_service_tasks [ansible/roles/world_model_service/tasks]
        direction TB
        node_140["main.yaml"]
    end
    subgraph dir_ansible_tasks [ansible/tasks]
        direction TB
        node_350["README.md"]
        node_351["build_pipecatapp_image.yaml"]
        node_353["create_expert_job.yaml"]
        node_354["deploy_expert_wrapper.yaml"]
        node_352["deploy_model_gpu_provider.yaml"]
    end
    subgraph dir_distributed_llama_repo [distributed-llama-repo]
        direction TB
        node_441["README.md"]
    end
    subgraph dir_docker [docker]
        direction TB
        node_404["README.md"]
    end
    subgraph dir_docker_dev_container [docker/dev_container]
        direction TB
        node_406["Dockerfile"]
    end
    subgraph dir_docker_memory_service [docker/memory_service]
        direction TB
        node_405["Dockerfile"]
    end
    subgraph dir_docs [docs]
        direction TB
        node_48["AGENTS.md"]
        node_60["ARCHITECTURE.md"]
        node_41["BENCHMARKING.MD"]
        node_51["DEPLOYMENT_AND_PROFILING.md"]
        node_55["EVALUATION_LLMROUTER.md"]
        node_44["FRONTEND_VERIFICATION.md"]
        node_47["FRONTIER_AGENT_ROADMAP.md"]
        node_43["GEMINI.md"]
        node_39["MCP_SERVER_SETUP.md"]
        node_40["MEMORIES.md"]
        node_46["NETWORK.md"]
        node_45["NIXOS_PXE_BOOT_SETUP.md"]
        node_59["PROJECT_SUMMARY.md"]
        node_50["PXE_BOOT_SETUP.md"]
        node_42["README.md"]
        node_57["REFACTOR_PROPOSAL_hybrid_architecture.md"]
        node_53["REMOTE_WORKFLOW.md"]
        node_52["TODO_Hybrid_Architecture.md"]
        node_49["TOOL_EVALUATION.md"]
        node_56["TROUBLESHOOTING.md"]
        node_58["VLLM_PROJECT_EVALUATION.md"]
        node_54["heretic_evaluation.md"]
    end
    subgraph dir_examples [examples]
        direction TB
        node_411["README.md"]
        node_412["chat-persistent.sh"]
    end
    subgraph dir_group_vars [group_vars]
        direction TB
        node_663["README.md"]
        node_664["all.yaml"]
        node_665["external_experts.yaml"]
        node_666["models.yaml"]
    end
    subgraph dir_host_vars [host_vars]
        direction TB
        node_403["README.md"]
        node_402["localhost.yaml"]
    end
    subgraph dir_initial_setup [initial-setup]
        direction TB
        node_538["README.md"]
        node_540["add_new_worker.sh"]
        node_541["setup.conf"]
        node_539["setup.sh"]
        node_542["update_inventory.sh"]
    end
    subgraph dir_initial_setup_modules [initial-setup/modules]
        direction TB
        node_547["01-network.sh"]
        node_549["02-hostname.sh"]
        node_545["03-user.sh"]
        node_548["04-ssh.sh"]
        node_550["05-auto-provision.sh"]
        node_546["README.md"]
    end
    subgraph dir_initial_setup_worker_setup [initial-setup/worker-setup]
        direction TB
        node_543["README.md"]
        node_544["setup.sh"]
    end
    subgraph dir_pipecat_agent_extension [pipecat-agent-extension]
        direction TB
        node_530["README.md"]
        node_533["example.ts"]
        node_531["gemini-extension.json"]
        node_532["package.json"]
        node_534["tsconfig.json"]
    end
    subgraph dir_pipecat_agent_extension_commands_pipecat [pipecat-agent-extension/commands/pipecat]
        direction TB
        node_535["send.toml"]
    end
    subgraph dir_pipecatapp [pipecatapp]
        direction TB
        node_574["Dockerfile"]
        node_559["README.md"]
        node_555["TODO.md"]
        node_563["__init__.py"]
        node_565["agent_factory.py"]
        node_557["api_keys.py"]
        node_569["app.py"]
        node_568["archivist_service.py"]
        node_576["durable_execution.py"]
        node_579["expert_tracker.py"]
        node_575["llm_clients.py"]
        node_578["manager_agent.py"]
        node_581["memory.py"]
        node_560["models.py"]
        node_564["moondream_detector.py"]
        node_551["net_utils.py"]
        node_577["pmm_memory.py"]
        node_573["pmm_memory_client.py"]
        node_571["quality_control.py"]
        node_554["rate_limiter.py"]
        node_553["requirements.txt"]
        node_561["security.py"]
        node_562["start_archivist.sh"]
        node_572["task_supervisor.py"]
        node_566["technician_agent.py"]
        node_558["test_memory.py"]
        node_552["test_moondream_detector.py"]
        node_570["test_server.py"]
        node_580["tool_server.py"]
        node_556["web_server.py"]
        node_567["worker_agent.py"]
    end
    subgraph dir_pipecatapp_datasets [pipecatapp/datasets]
        direction TB
        node_591["sycophancy_prompts.json"]
    end
    subgraph dir_pipecatapp_memory_graph_service [pipecatapp/memory_graph_service]
        direction TB
        node_625["Dockerfile"]
        node_624["server.py"]
    end
    subgraph dir_pipecatapp_nomad_templates [pipecatapp/nomad_templates]
        direction TB
        node_622["immich.nomad.hcl"]
        node_620["readeck.nomad.hcl"]
        node_621["uptime-kuma.nomad.hcl"]
        node_623["vaultwarden.nomad.hcl"]
    end
    subgraph dir_pipecatapp_prompts [pipecatapp/prompts]
        direction TB
        node_606["coding_expert.txt"]
        node_607["creative_expert.txt"]
        node_605["router.txt"]
        node_604["tron_agent.txt"]
    end
    subgraph dir_pipecatapp_static [pipecatapp/static]
        direction TB
        node_587["cluster.html"]
        node_586["cluster_viz.html"]
        node_582["index.html"]
        node_585["terminal.js"]
        node_584["vr_index.html"]
        node_583["workflow.html"]
    end
    subgraph dir_pipecatapp_static_css [pipecatapp/static/css]
        direction TB
        node_590["litegraph.css"]
    end
    subgraph dir_pipecatapp_static_js [pipecatapp/static/js]
        direction TB
        node_589["editor.js"]
        node_588["litegraph.js"]
    end
    subgraph dir_pipecatapp_tests [pipecatapp/tests]
        direction TB
        node_609["test_audio_streamer.py"]
        node_615["test_metrics_cache.py"]
        node_614["test_net_utils.py"]
        node_613["test_piper_async.py"]
        node_611["test_rate_limiter.py"]
        node_608["test_stt_optimization.py"]
        node_610["test_web_server_unit.py"]
        node_612["test_websocket_security.py"]
    end
    subgraph dir_pipecatapp_tests_workflow [pipecatapp/tests/workflow]
        direction TB
        node_616["test_history.py"]
    end
    subgraph dir_pipecatapp_tools [pipecatapp/tools]
        direction TB
        node_641["__init__.py"]
        node_632["ansible_tool.py"]
        node_638["archivist_tool.py"]
        node_645["claude_clone_tool.py"]
        node_648["code_runner_tool.py"]
        node_642["council_tool.py"]
        node_635["dependency_scanner_tool.py"]
        node_654["desktop_control_tool.py"]
        node_631["file_editor_tool.py"]
        node_653["final_answer_tool.py"]
        node_661["gemini_cli.py"]
        node_629["get_nomad_job.py"]
        node_626["git_tool.py"]
        node_634["ha_tool.py"]
        node_637["llxprt_code_tool.py"]
        node_659["mcp_tool.py"]
        node_646["open_workers_tool.py"]
        node_647["opencode_tool.py"]
        node_639["orchestrator_tool.py"]
        node_658["planner_tool.py"]
        node_627["power_tool.py"]
        node_633["project_mapper_tool.py"]
        node_651["prompt_improver_tool.py"]
        node_644["rag_tool.py"]
        node_628["remote_tool_proxy.py"]
        node_655["sandbox.ts"]
        node_657["shell_tool.py"]
        node_640["smol_agent_tool.py"]
        node_649["ssh_tool.py"]
        node_656["summarizer_tool.py"]
        node_650["swarm_tool.py"]
        node_662["tap_service.py"]
        node_660["term_everything_tool.py"]
        node_630["test_code_runner_tool.py"]
        node_636["test_ssh_tool.py"]
        node_643["vr_tool.py"]
        node_652["web_browser_tool.py"]
    end
    subgraph dir_pipecatapp_workflow [pipecatapp/workflow]
        direction TB
        node_592["__init__.py"]
        node_593["context.py"]
        node_595["history.py"]
        node_594["node.py"]
        node_596["runner.py"]
    end
    subgraph dir_pipecatapp_workflow_nodes [pipecatapp/workflow/nodes]
        direction TB
        node_599["__init__.py"]
        node_600["base_nodes.py"]
        node_603["emperor_nodes.py"]
        node_601["llm_nodes.py"]
        node_598["registry.py"]
        node_602["system_nodes.py"]
        node_597["tool_nodes.py"]
    end
    subgraph dir_pipecatapp_workflows [pipecatapp/workflows]
        direction TB
        node_618["default_agent_loop.yaml"]
        node_619["poc_ensemble.yaml"]
        node_617["tiered_agent_loop.yaml"]
    end
    subgraph dir_playbooks [playbooks]
        direction TB
        node_363["README.md"]
        node_378["benchmark_single_model.yaml"]
        node_369["cluster_status.yaml"]
        node_362["common_setup.yaml"]
        node_381["controller.yaml"]
        node_359["debug_template.yaml"]
        node_372["deploy_app.yaml"]
        node_364["deploy_expert.yaml"]
        node_360["deploy_prompt_evolution.yaml"]
        node_357["developer_tools.yaml"]
        node_367["diagnose_and_log_home_assistant.yaml"]
        node_365["diagnose_failure.yaml"]
        node_355["diagnose_home_assistant.yaml"]
        node_371["fix_cluster.yaml"]
        node_366["heal_cluster.yaml"]
        node_356["heal_job.yaml"]
        node_379["health_check.yaml"]
        node_374["promote_controller.yaml"]
        node_377["promote_to_controller.yaml"]
        node_373["pxe_setup.yaml"]
        node_376["redeploy_pipecat.yaml"]
        node_370["run_config_manager.yaml"]
        node_358["run_consul.yaml"]
        node_368["run_ha_diag.yaml"]
        node_380["run_health_check.yaml"]
        node_361["status-check.yaml"]
        node_375["wake.yaml"]
        node_382["worker.yaml"]
    end
    subgraph dir_playbooks_network [playbooks/network]
        direction TB
        node_385["mesh.yaml"]
        node_384["verify.yaml"]
    end
    subgraph dir_playbooks_ops [playbooks/ops]
        direction TB
        node_383["optimize_memory.yaml"]
    end
    subgraph dir_playbooks_preflight [playbooks/preflight]
        direction TB
        node_386["checks.yaml"]
    end
    subgraph dir_playbooks_services [playbooks/services]
        direction TB
        node_388["README.md"]
        node_395["ai_experts.yaml"]
        node_398["app_services.yaml"]
        node_397["consul.yaml"]
        node_387["core_ai_services.yaml"]
        node_396["core_infra.yaml"]
        node_394["docker.yaml"]
        node_392["final_verification.yaml"]
        node_391["model_services.yaml"]
        node_399["monitoring.yaml"]
        node_400["nomad.yaml"]
        node_390["nomad_client.yaml"]
        node_393["streaming_services.yaml"]
        node_389["training_services.yaml"]
    end
    subgraph dir_playbooks_services_tasks [playbooks/services/tasks]
        direction TB
        node_401["diagnose_home_assistant.yaml"]
    end
    subgraph dir_prompt_engineering [prompt_engineering]
        direction TB
        node_74["PROMPT_ENGINEERING.md"]
        node_69["README.md"]
        node_75["challenger.py"]
        node_68["create_evaluator.py"]
        node_77["evaluation_lib.py"]
        node_73["evaluator.py"]
        node_72["evolve.py"]
        node_67["promote_agent.py"]
        node_71["requirements-dev.txt"]
        node_70["run_campaign.py"]
        node_76["visualize_archive.py"]
    end
    subgraph dir_prompt_engineering_agents [prompt_engineering/agents]
        direction TB
        node_90["ADAPTATION_AGENT.md"]
        node_89["EVALUATOR_GENERATOR.md"]
        node_84["README.md"]
        node_86["architecture_review.md"]
        node_88["code_clean_up.md"]
        node_87["debug_and_analysis.md"]
        node_83["new_task_review.md"]
        node_85["problem_scope_framing.md"]
    end
    subgraph dir_prompt_engineering_archive [prompt_engineering/archive]
        direction TB
        node_91["agent_0.json"]
        node_98["agent_0.py"]
        node_94["agent_1.json"]
        node_92["agent_1.py"]
        node_93["agent_2.json"]
        node_96["agent_2.py"]
        node_95["agent_3.json"]
        node_97["agent_3.py"]
    end
    subgraph dir_prompt_engineering_evaluation_suite [prompt_engineering/evaluation_suite]
        direction TB
        node_81["README.md"]
        node_82["test_vision.yaml"]
    end
    subgraph dir_prompt_engineering_frontend [prompt_engineering/frontend]
        direction TB
        node_78["index.html"]
        node_79["server.py"]
    end
    subgraph dir_prompt_engineering_generated_evaluators [prompt_engineering/generated_evaluators]
        direction TB
        node_80[".gitignore"]
    end
    subgraph dir_prompts [prompts]
        direction TB
        node_439["README.md"]
        node_440["chat-with-bob.txt"]
        node_438["router.txt"]
    end
    subgraph dir_reflection [reflection]
        direction TB
        node_408["README.md"]
        node_409["adaptation_manager.py"]
        node_407["create_reflection.py"]
        node_410["reflect.py"]
    end
    subgraph dir_scripts [scripts]
        direction TB
        node_420["README.md"]
        node_417["ansible_diff.sh"]
        node_434["ci_ansible_check.sh"]
        node_430["cleanup.sh"]
        node_429["compare_exo_llama.py"]
        node_422["create_cynic_model.sh"]
        node_419["debug_mesh.sh"]
        node_433["fix_markdown.sh"]
        node_426["fix_verification_failures.sh"]
        node_415["fix_yaml.sh"]
        node_418["generate_file_map.py"]
        node_421["healer.py"]
        node_428["lint.sh"]
        node_431["lint_exclude.txt"]
        node_424["memory_audit.py"]
        node_423["profile_resources.sh"]
        node_425["prune_consul_services.py"]
        node_414["run_quibbler.sh"]
        node_432["test_playbooks_dry_run.sh"]
        node_427["test_playbooks_live_run.sh"]
        node_435["uninstall.sh"]
        node_416["verify_consul_attributes.sh"]
    end
    subgraph dir_scripts_debug [scripts/debug]
        direction TB
        node_437["README.md"]
        node_436["test_mqtt_connection.py"]
    end
    subgraph dir_tests [tests]
        direction TB
        node_442["README.md"]
        node_443["__init__.py"]
        node_445["test_agent_patterns.py"]
        node_444["test_emperor_node.py"]
    end
    subgraph dir_tests_e2e [tests/e2e]
        direction TB
        node_448["README.md"]
        node_449["__init__.py"]
        node_446["test_api.py"]
        node_451["test_intelligent_routing.py"]
        node_453["test_mission_control.py"]
        node_450["test_palette_command_history.py"]
        node_452["test_palette_ux.py"]
        node_447["test_regression.py"]
    end
    subgraph dir_tests_integration [tests/integration]
        direction TB
        node_467["README.md"]
        node_469["__init__.py"]
        node_474["stub_services.py"]
        node_472["test_consul_role.yaml"]
        node_470["test_home_assistant.yaml"]
        node_468["test_mini_pipeline.py"]
        node_466["test_mqtt_exporter.py"]
        node_465["test_nomad_role.yaml"]
        node_471["test_pipecat_app.py"]
        node_473["test_preemption.py"]
    end
    subgraph dir_tests_integration_roles_test_home_assistant_tasks [tests/integration/roles/test_home_assistant/tasks]
        direction TB
        node_475["main.yaml"]
    end
    subgraph dir_tests_playbooks [tests/playbooks]
        direction TB
        node_456["e2e-tests.yaml"]
        node_454["test_consul.yaml"]
        node_455["test_llama_cpp.yaml"]
        node_457["test_nomad.yaml"]
    end
    subgraph dir_tests_scripts [tests/scripts]
        direction TB
        node_464["run_unit_tests.sh"]
        node_463["test_distributed_llama.sh"]
        node_462["test_duplicate_role_execution.sh"]
        node_461["test_paddler.sh"]
        node_460["test_piper.sh"]
        node_458["test_run.sh"]
        node_459["verify_components.py"]
    end
    subgraph dir_tests_unit [tests/unit]
        direction TB
        node_489["README.md"]
        node_494["__init__.py"]
        node_503["conftest.py"]
        node_479["test_adaptation_manager.py"]
        node_518["test_agent_definitions.py"]
        node_499["test_ansible_tool.py"]
        node_488["test_archivist_tool.py"]
        node_502["test_claude_clone_tool.py"]
        node_478["test_code_runner_tool.py"]
        node_500["test_council_tool.py"]
        node_495["test_dependency_scanner.py"]
        node_516["test_desktop_control_tool.py"]
        node_490["test_file_editor_security.py"]
        node_497["test_file_editor_tool.py"]
        node_507["test_final_answer_tool.py"]
        node_524["test_gemini_cli.py"]
        node_512["test_get_nomad_job.py"]
        node_517["test_git_tool.py"]
        node_506["test_ha_tool.py"]
        node_491["test_home_assistant_template.py"]
        node_519["test_infrastructure.py"]
        node_513["test_lint_script.py"]
        node_523["test_llxprt_code_tool.py"]
        node_496["test_mcp_tool.py"]
        node_481["test_mqtt_template.py"]
        node_492["test_open_workers_tool.py"]
        node_528["test_opencode_tool.py"]
        node_498["test_orchestrator_tool.py"]
        node_487["test_pipecat_app_unit.py"]
        node_525["test_planner_tool.py"]
        node_509["test_playbook_integration.py"]
        node_520["test_poc_ensemble.py"]
        node_510["test_power_tool.py"]
        node_505["test_project_mapper_tool.py"]
        node_486["test_prompt_engineering.py"]
        node_514["test_prompt_improver_tool.py"]
        node_477["test_provisioning.py"]
        node_522["test_rag_tool.py"]
        node_476["test_reflection.py"]
        node_493["test_security.py"]
        node_508["test_shell_tool.py"]
        node_515["test_simple_llm_node.py"]
        node_484["test_smol_agent_tool.py"]
        node_483["test_ssh_tool.py"]
        node_482["test_summarizer_tool.py"]
        node_485["test_supervisor.py"]
        node_501["test_swarm_tool.py"]
        node_521["test_tap_service.py"]
        node_480["test_term_everything_tool.py"]
        node_504["test_vision_failover.py"]
        node_511["test_web_browser_tool.py"]
        node_527["test_workflow.py"]
        node_526["test_world_model_service.py"]
    end
    subgraph dir_verification [verification]
        direction TB
        node_38["save_success.png"]
        node_37["verify_workflow_save.py"]
    end
    subgraph dir_workflows [workflows]
        direction TB
        node_529["default_agent_loop.yaml"]
    end

    node_252 --> node_163
    node_499 --> node_305
    node_20 --> node_138
    node_36 --> node_295
    node_238 --> node_269
    node_295 --> node_320
    node_17 --> node_637
    node_23 --> node_387
    node_395 --> node_154
    node_131 --> node_288
    node_418 --> node_538
    node_580 --> node_649
    node_427 --> node_374
    node_52 --> node_467
    node_40 --> node_199
    node_252 --> node_274
    node_515 --> node_593
    node_349 --> node_109
    node_349 --> node_606
    node_374 --> node_165
    node_18 --> node_372
    node_48 --> node_21
    node_391 --> node_204
    node_527 --> node_596
    node_400 --> node_166
    node_376 --> node_342
    node_40 --> node_154
    node_418 --> node_406
    node_8 --> node_286
    node_488 --> node_309
    node_18 --> node_237
    node_488 --> node_638
    node_131 --> node_215
    node_18 --> node_229
    node_17 --> node_659
    node_366 --> node_335
    node_267 --> node_266
    node_398 --> node_319
    node_134 --> node_336
    node_45 --> node_232
    node_420 --> node_532
    node_18 --> node_259
    node_17 --> node_644
    node_52 --> node_263
    node_23 --> node_384
    node_418 --> node_9
    node_131 --> node_349
    node_182 --> node_180
    node_252 --> node_161
    node_398 --> node_157
    node_10 --> node_489
    node_20 --> node_569
    node_495 --> node_635
    node_52 --> node_142
    node_458 --> node_136
    node_398 --> node_196
    node_18 --> node_408
    node_602 --> node_598
    node_366 --> node_216
    node_415 --> node_27
    node_455 --> node_166
    node_17 --> node_510
    node_40 --> node_536
    node_45 --> node_274
    node_36 --> node_382
    node_131 --> node_269
    node_274 --> node_167
    node_45 --> node_174
    node_8 --> node_295
    node_18 --> node_230
    node_45 --> node_264
    node_134 --> node_297
    node_398 --> node_223
    node_18 --> node_373
    node_349 --> node_114
    node_403 --> node_402
    node_610 --> node_138
    node_40 --> node_14
    node_398 --> node_225
    node_10 --> node_467
    node_420 --> node_100
    node_17 --> node_627
    node_18 --> node_364
    node_4 --> node_293
    node_84 --> node_86
    node_385 --> node_251
    node_366 --> node_140
    node_288 --> node_286
    node_300 --> node_574
    node_398 --> node_155
    node_40 --> node_124
    node_398 --> node_153
    node_30 --> node_372
    node_432 --> node_362
    node_258 --> node_553
    node_18 --> node_282
    node_569 --> node_551
    node_40 --> node_253
    node_295 --> node_644
    node_57 --> node_107
    node_45 --> node_258
    node_580 --> node_656
    node_60 --> node_23
    node_613 --> node_295
    node_4 --> node_267
    node_610 --> node_569
    node_253 --> node_161
    node_52 --> node_151
    node_84 --> node_90
    node_457 --> node_163
    node_45 --> node_220
    node_60 --> node_285
    node_418 --> node_663
    node_106 --> node_109
    node_238 --> node_268
    node_74 --> node_569
    node_420 --> node_434
    node_152 --> node_111
    node_235 --> node_234
    node_431 --> node_582
    node_398 --> node_299
    node_505 --> node_559
    node_366 --> node_475
    node_238 --> node_213
    node_40 --> node_123
    node_45 --> node_332
    node_18 --> node_489
    node_26 --> node_60
    node_131 --> node_198
    node_134 --> node_288
    node_18 --> node_374
    node_418 --> node_26
    node_542 --> node_34
    node_194 --> node_190
    node_295 --> node_627
    node_238 --> node_290
    node_4 --> node_222
    node_432 --> node_398
    node_252 --> node_162
    node_18 --> node_183
    node_404 --> node_297
    node_18 --> node_277
    node_40 --> node_582
    node_134 --> node_215
    node_40 --> node_200
    node_397 --> node_153
    node_147 --> node_148
    node_134 --> node_349
    node_57 --> node_139
    node_45 --> node_237
    node_89 --> node_569
    node_356 --> node_471
    node_45 --> node_229
    node_131 --> node_268
    node_151 --> node_152
    node_572 --> node_650
    node_418 --> node_363
    node_8 --> node_581
    node_455 --> node_167
    node_106 --> node_114
    node_4 --> node_272
    node_253 --> node_164
    node_29 --> node_665
    node_540 --> node_539
    node_4 --> node_153
    node_10 --> node_530
    node_59 --> node_356
    node_131 --> node_213
    node_4 --> node_405
    node_134 --> node_269
    node_381 --> node_396
    node_398 --> node_140
    node_349 --> node_556
    node_505 --> node_448
    node_394 --> node_208
    node_418 --> node_666
    node_52 --> node_538
    node_18 --> node_375
    node_18 --> node_260
    node_556 --> node_172
    node_40 --> node_116
    node_389 --> node_266
    node_455 --> node_168
    node_387 --> node_178
    node_8 --> node_111
    node_131 --> node_290
    node_8 --> node_42
    node_293 --> node_292
    node_45 --> node_230
    node_398 --> node_302
    node_8 --> node_546
    node_300 --> node_625
    node_398 --> node_316
    node_546 --> node_549
    node_18 --> node_143
    node_123 --> node_120
    node_182 --> node_107
    node_398 --> node_326
    node_18 --> node_355
    node_565 --> node_634
    node_385 --> node_271
    node_40 --> node_337
    node_418 --> node_15
    node_45 --> node_373
    node_387 --> node_342
    node_4 --> node_335
    node_4 --> node_218
    node_40 --> node_276
    node_376 --> node_345
    node_40 --> node_554
    node_398 --> node_312
    node_432 --> node_417
    node_527 --> node_600
    node_398 --> node_275
    node_18 --> node_338
    node_169 --> node_164
    node_79 --> node_78
    node_583 --> node_584
    node_4 --> node_216
    node_19 --> node_379
    node_569 --> node_649
    node_40 --> node_417
    node_418 --> node_553
    node_40 --> node_351
    node_130 --> node_127
    node_18 --> node_125
    node_18 --> node_238
    node_45 --> node_282
    node_508 --> node_657
    node_398 --> node_320
    node_44 --> node_532
    node_546 --> node_550
    node_8 --> node_350
    node_23 --> node_393
    node_40 --> node_48
    node_8 --> node_285
    node_55 --> node_601
    node_250 --> node_405
    node_238 --> node_265
    node_398 --> node_173
    node_52 --> node_293
    node_10 --> node_538
    node_10 --> node_63
    node_40 --> node_273
    node_418 --> node_388
    node_398 --> node_288
    node_40 --> node_138
    node_608 --> node_176
    node_18 --> node_397
    node_17 --> node_314
    node_34 --> node_542
    node_297 --> node_177
    node_40 --> node_543
    node_134 --> node_198
    node_335 --> node_333
    node_457 --> node_162
    node_358 --> node_664
    node_614 --> node_551
    node_40 --> node_170
    node_106 --> node_108
    node_57 --> node_565
    node_559 --> node_564
    node_18 --> node_530
    node_60 --> node_4
    node_18 --> node_250
    node_376 --> node_339
    node_372 --> node_666
    node_42 --> node_39
    node_17 --> node_629
    node_17 --> node_307
    node_580 --> node_301
    node_559 --> node_570
    node_238 --> node_232
    node_52 --> node_134
    node_192 --> node_189
    node_42 --> node_54
    node_40 --> node_569
    node_394 --> node_212
    node_398 --> node_315
    node_52 --> node_157
    node_427 --> node_356
    node_45 --> node_183
    node_45 --> node_277
    node_52 --> node_196
    node_40 --> node_437
    node_52 --> node_663
    node_134 --> node_268
    node_418 --> node_172
    node_18 --> node_240
    node_583 --> node_589
    node_131 --> node_251
    node_18 --> node_359
    node_288 --> node_285
    node_396 --> node_147
    node_238 --> node_274
    node_489 --> node_485
    node_580 --> node_660
    node_4 --> node_221
    node_40 --> node_579
    node_366 --> node_147
    node_134 --> node_213
    node_399 --> node_192
    node_238 --> node_174
    node_455 --> node_156
    node_565 --> node_626
    node_372 --> node_341
    node_18 --> node_119
    node_52 --> node_222
    node_366 --> node_256
    node_238 --> node_264
    node_565 --> node_316
    node_394 --> node_206
    node_84 --> node_88
    node_253 --> node_166
    node_352 --> node_156
    node_134 --> node_290
    node_140 --> node_569
    node_569 --> node_656
    node_459 --> node_532
    node_608 --> node_295
    node_52 --> node_225
    node_366 --> node_226
    node_52 --> node_219
    node_8 --> node_118
    node_131 --> node_232
    node_520 --> node_593
    node_455 --> node_211
    node_40 --> node_142
    node_43 --> node_72
    node_18 --> node_401
    node_131 --> node_163
    node_45 --> node_143
    node_48 --> node_138
    node_349 --> node_348
    node_40 --> node_415
    node_52 --> node_153
    node_295 --> node_307
    node_391 --> node_665
    node_8 --> node_559
    node_52 --> node_363
    node_36 --> node_21
    node_134 --> node_133
    node_131 --> node_274
    node_238 --> node_258
    node_391 --> node_247
    node_339 --> node_178
    node_10 --> node_663
    node_6 --> node_138
    node_530 --> node_532
    node_398 --> node_285
    node_131 --> node_264
    node_352 --> node_157
    node_366 --> node_247
    node_427 --> node_456
    node_300 --> node_560
    node_398 --> node_330
    node_410 --> node_409
    node_10 --> node_81
    node_131 --> node_154
    node_101 --> node_141
    node_116 --> node_117
    node_169 --> node_166
    node_20 --> node_79
    node_74 --> node_70
    node_18 --> node_360
    node_17 --> node_328
    node_238 --> node_220
    node_398 --> node_159
    node_418 --> node_80
    node_45 --> node_125
    node_57 --> node_406
    node_52 --> node_339
    node_18 --> node_283
    node_37 --> node_618
    node_134 --> node_574
    node_433 --> node_26
    node_18 --> node_370
    node_238 --> node_332
    node_252 --> node_165
    node_505 --> node_408
    node_147 --> node_145
    node_418 --> node_42
    node_366 --> node_300
    node_559 --> node_139
    node_20 --> node_405
    node_40 --> node_169
    node_40 --> node_383
    node_40 --> node_257
    node_179 --> node_139
    node_256 --> node_254
    node_407 --> node_3
    node_17 --> node_649
    node_370 --> node_664
    node_40 --> node_305
    node_297 --> node_138
    node_349 --> node_529
    node_455 --> node_155
    node_176 --> node_177
    node_569 --> node_576
    node_565 --> node_315
    node_68 --> node_89
    node_139 --> node_138
    node_616 --> node_595
    node_40 --> node_151
    node_52 --> node_553
    node_366 --> node_331
    node_569 --> node_318
    node_398 --> node_256
    node_432 --> node_396
    node_352 --> node_155
    node_45 --> node_250
    node_18 --> node_356
    node_352 --> node_153
    node_300 --> node_139
    node_569 --> node_317
    node_10 --> node_8
    node_565 --> node_631
    node_455 --> node_666
    node_418 --> node_23
    node_181 --> node_182
    node_52 --> node_388
    node_134 --> node_251
    node_556 --> node_586
    node_584 --> node_588
    node_596 --> node_598
    node_52 --> node_140
    node_90 --> node_365
    node_295 --> node_328
    node_297 --> node_569
    node_45 --> node_240
    node_418 --> node_5
    node_418 --> node_350
    node_238 --> node_162
    node_432 --> node_391
    node_520 --> node_596
    node_548 --> node_544
    node_208 --> node_210
    node_451 --> node_295
    node_467 --> node_473
    node_583 --> node_590
    node_220 --> node_258
    node_238 --> node_230
    node_625 --> node_624
    node_69 --> node_73
    node_372 --> node_349
    node_18 --> node_99
    node_45 --> node_119
    node_574 --> node_136
    node_8 --> node_366
    node_408 --> node_409
    node_580 --> node_313
    node_134 --> node_232
    node_40 --> node_221
    node_40 --> node_149
    node_295 --> node_649
    node_311 --> node_323
    node_409 --> node_410
    node_387 --> node_339
    node_391 --> node_182
    node_18 --> node_81
    node_428 --> node_431
    node_297 --> node_296
    node_455 --> node_144
    node_157 --> node_153
    node_420 --> node_431
    node_399 --> node_244
    node_42 --> node_4
    node_393 --> node_293
    node_349 --> node_554
    node_565 --> node_633
    node_131 --> node_123
    node_134 --> node_274
    node_387 --> node_216
    node_187 --> node_424
    node_52 --> node_475
    node_505 --> node_489
    node_582 --> node_172
    node_134 --> node_174
    node_48 --> node_257
    node_540 --> node_34
    node_615 --> node_556
    node_131 --> node_162
    node_238 --> node_282
    node_432 --> node_394
    node_17 --> node_656
    node_19 --> node_665
    node_134 --> node_264
    node_4 --> node_147
    node_485 --> node_410
    node_169 --> node_167
    node_245 --> node_243
    node_131 --> node_230
    node_134 --> node_625
    node_4 --> node_256
    node_134 --> node_154
    node_366 --> node_208
    node_457 --> node_165
    node_217 --> node_156
    node_398 --> node_331
    node_9 --> node_23
    node_4 --> node_226
    node_349 --> node_138
    node_18 --> node_179
    node_457 --> node_169
    node_18 --> node_8
    node_55 --> node_136
    node_45 --> node_283
    node_489 --> node_328
    node_8 --> node_536
    node_60 --> node_72
    node_392 --> node_169
    node_489 --> node_476
    node_556 --> node_551
    node_4 --> node_309
    node_140 --> node_406
    node_549 --> node_541
    node_40 --> node_404
    node_4 --> node_638
    node_106 --> node_110
    node_134 --> node_258
    node_599 --> node_603
    node_169 --> node_234
    node_366 --> node_284
    node_84 --> node_83
    node_418 --> node_24
    node_569 --> node_596
    node_486 --> node_70
    node_40 --> node_293
    node_418 --> node_559
    node_512 --> node_629
    node_238 --> node_183
    node_4 --> node_247
    node_18 --> node_403
    node_139 --> node_257
    node_217 --> node_157
    node_392 --> node_168
    node_349 --> node_569
    node_131 --> node_337
    node_240 --> node_239
    node_295 --> node_656
    node_18 --> node_336
    node_398 --> node_314
    node_521 --> node_662
    node_565 --> node_309
    node_629 --> node_303
    node_565 --> node_638
    node_580 --> node_654
    node_567 --> node_565
    node_455 --> node_210
    node_238 --> node_291
    node_52 --> node_42
    node_40 --> node_267
    node_395 --> node_157
    node_36 --> node_387
    node_4 --> node_300
    node_418 --> node_574
    node_538 --> node_541
    node_238 --> node_278
    node_36 --> node_398
    node_505 --> node_306
    node_398 --> node_307
    node_518 --> node_89
    node_40 --> node_157
    node_17 --> node_317
    node_28 --> node_33
    node_40 --> node_196
    node_485 --> node_19
    node_4 --> node_331
    node_238 --> node_143
    node_40 --> node_585
    node_418 --> node_4
    node_418 --> node_448
    node_217 --> node_155
    node_398 --> node_174
    node_570 --> node_176
    node_522 --> node_644
    node_559 --> node_406
    node_352 --> node_104
    node_217 --> node_153
    node_57 --> node_295
    node_68 --> node_176
    node_179 --> node_406
    node_134 --> node_123
    node_418 --> node_1
    node_40 --> node_222
    node_10 --> node_80
    node_57 --> node_297
    node_609 --> node_569
    node_366 --> node_237
    node_131 --> node_291
    node_366 --> node_229
    node_134 --> node_162
    node_366 --> node_246
    node_257 --> node_13
    node_131 --> node_170
    node_570 --> node_557
    node_42 --> node_46
    node_366 --> node_259
    node_40 --> node_79
    node_67 --> node_138
    node_505 --> node_530
    node_40 --> node_225
    node_131 --> node_278
    node_395 --> node_153
    node_507 --> node_653
    node_134 --> node_230
    node_23 --> node_385
    node_106 --> node_102
    node_238 --> node_125
    node_130 --> node_128
    node_10 --> node_42
    node_48 --> node_438
    node_543 --> node_539
    node_10 --> node_546
    node_456 --> node_470
    node_40 --> node_272
    node_366 --> node_206
    node_612 --> node_138
    node_349 --> node_568
    node_420 --> node_428
    node_569 --> node_298
    node_40 --> node_153
    node_511 --> node_320
    node_40 --> node_405
    node_40 --> node_363
    node_131 --> node_143
    node_603 --> node_598
    node_528 --> node_315
    node_398 --> node_258
    node_18 --> node_40
    node_4 --> node_199
    node_169 --> node_233
    node_295 --> node_317
    node_45 --> node_179
    node_300 --> node_248
    node_382 --> node_362
    node_489 --> node_480
    node_67 --> node_569
    node_297 --> node_294
    node_52 --> node_256
    node_4 --> node_76
    node_285 --> node_79
    node_420 --> node_71
    node_238 --> node_181
    node_238 --> node_250
    node_17 --> node_301
    node_36 --> node_138
    node_372 --> node_346
    node_398 --> node_328
    node_40 --> node_335
    node_45 --> node_664
    node_51 --> node_111
    node_40 --> node_339
    node_131 --> node_125
    node_570 --> node_295
    node_10 --> node_350
    node_350 --> node_353
    node_398 --> node_332
    node_569 --> node_313
    node_134 --> node_337
    node_18 --> node_215
    node_4 --> node_208
    node_398 --> node_224
    node_418 --> node_625
    node_40 --> node_216
    node_238 --> node_175
    node_238 --> node_240
    node_18 --> node_349
    node_84 --> node_89
    node_455 --> node_159
    node_17 --> node_660
    node_40 --> node_377
    node_534 --> node_533
    node_539 --> node_542
    node_48 --> node_176
    node_394 --> node_211
    node_352 --> node_159
    node_37 --> node_38
    node_8 --> node_374
    node_17 --> node_449
    node_18 --> node_269
    node_238 --> node_119
    node_382 --> node_398
    node_381 --> node_399
    node_392 --> node_157
    node_123 --> node_122
    node_357 --> node_220
    node_6 --> node_176
    node_48 --> node_664
    node_131 --> node_181
    node_4 --> node_284
    node_398 --> node_259
    node_405 --> node_295
    node_524 --> node_329
    node_418 --> node_537
    node_8 --> node_138
    node_486 --> node_295
    node_4 --> node_124
    node_556 --> node_78
    node_374 --> node_163
    node_18 --> node_546
    node_8 --> node_543
    node_391 --> node_183
    node_455 --> node_146
    node_504 --> node_295
    node_295 --> node_301
    node_140 --> node_553
    node_131 --> node_175
    node_40 --> node_379
    node_134 --> node_291
    node_366 --> node_277
    node_580 --> node_644
    node_556 --> node_560
    node_489 --> node_513
    node_526 --> node_295
    node_84 --> node_87
    node_556 --> node_595
    node_428 --> node_400
    node_28 --> node_587
    node_40 --> node_316
    node_40 --> node_584
    node_134 --> node_278
    node_458 --> node_257
    node_303 --> node_629
    node_295 --> node_660
    node_358 --> node_154
    node_374 --> node_154
    node_52 --> node_331
    node_139 --> node_176
    node_445 --> node_576
    node_385 --> node_272
    node_392 --> node_155
    node_10 --> node_118
    node_61 --> node_63
    node_160 --> node_136
    node_392 --> node_153
    node_43 --> node_176
    node_134 --> node_143
    node_366 --> node_260
    node_613 --> node_138
    node_489 --> node_409
    node_238 --> node_283
    node_52 --> node_448
    node_40 --> node_475
    node_650 --> node_566
    node_467 --> node_295
    node_79 --> node_172
    node_366 --> node_263
    node_130 --> node_136
    node_366 --> node_205
    node_10 --> node_559
    node_18 --> node_367
    node_10 --> node_65
    node_300 --> node_176
    node_439 --> node_440
    node_220 --> node_257
    node_569 --> node_321
    node_52 --> node_265
    node_18 --> node_198
    node_387 --> node_665
    node_217 --> node_104
    node_460 --> node_3
    node_391 --> node_201
    node_287 --> node_285
    node_8 --> node_56
    node_4 --> node_246
    node_459 --> node_137
    node_572 --> node_318
    node_23 --> node_399
    node_134 --> node_125
    node_18 --> node_378
    node_4 --> node_259
    node_418 --> node_408
    node_393 --> node_228
    node_17 --> node_298
    node_131 --> node_221
    node_131 --> node_149
    node_559 --> node_553
    node_505 --> node_81
    node_142 --> node_180
    node_366 --> node_338
    node_391 --> node_238
    node_274 --> node_161
    node_40 --> node_137
    node_381 --> node_400
    node_4 --> node_206
    node_40 --> node_589
    node_45 --> node_215
    node_18 --> node_160
    node_18 --> node_268
    node_366 --> node_238
    node_548 --> node_541
    node_372 --> node_347
    node_40 --> node_104
    node_445 --> node_566
    node_20 --> node_555
    node_398 --> node_139
    node_72 --> node_176
    node_405 --> node_581
    node_569 --> node_645
    node_18 --> node_365
    node_18 --> node_213
    node_179 --> node_295
    node_418 --> node_78
    node_19 --> node_410
    node_489 --> node_660
    node_61 --> node_64
    node_565 --> node_653
    node_134 --> node_181
    node_134 --> node_250
    node_17 --> node_313
    node_45 --> node_269
    node_18 --> node_290
    node_4 --> node_276
    node_140 --> node_137
    node_18 --> node_84
    node_18 --> node_411
    node_103 --> node_72
    node_556 --> node_587
    node_52 --> node_174
    node_366 --> node_131
    node_399 --> node_185
    node_496 --> node_327
    node_60 --> node_356
    node_435 --> node_430
    node_300 --> node_295
    node_52 --> node_264
    node_18 --> node_118
    node_468 --> node_295
    node_300 --> node_297
    node_569 --> node_618
    node_509 --> node_33
    node_420 --> node_14
    node_505 --> node_8
    node_134 --> node_175
    node_565 --> node_308
    node_569 --> node_626
    node_100 --> node_168
    node_487 --> node_596
    node_407 --> node_79
    node_295 --> node_298
    node_40 --> node_442
    node_580 --> node_632
    node_400 --> node_163
    node_37 --> node_529
    node_418 --> node_29
    node_390 --> node_168
    node_398 --> node_318
    node_569 --> node_577
    node_349 --> node_79
    node_323 --> node_655
    node_217 --> node_159
    node_218 --> node_166
    node_432 --> node_23
    node_398 --> node_355
    node_611 --> node_554
    node_40 --> node_630
    node_17 --> node_563
    node_462 --> node_33
    node_505 --> node_403
    node_418 --> node_489
    node_17 --> node_176
    node_17 --> node_443
    node_52 --> node_258
    node_17 --> node_580
    node_4 --> node_195
    node_23 --> node_400
    node_238 --> node_179
    node_418 --> node_139
    node_295 --> node_313
    node_579 --> node_624
    node_372 --> node_344
    node_393 --> node_226
    node_664 --> node_182
    node_131 --> node_267
    node_52 --> node_220
    node_398 --> node_306
    node_74 --> node_73
    node_527 --> node_594
    node_4 --> node_569
    node_57 --> node_574
    node_147 --> node_146
    node_45 --> node_198
    node_274 --> node_162
    node_52 --> node_332
    node_18 --> node_21
    node_349 --> node_604
    node_18 --> node_227
    node_455 --> node_161
    node_134 --> node_221
    node_134 --> node_149
    node_349 --> node_339
    node_300 --> node_577
    node_497 --> node_304
    node_569 --> node_651
    node_565 --> node_643
    node_559 --> node_581
    node_17 --> node_654
    node_482 --> node_324
    node_512 --> node_303
    node_179 --> node_581
    node_134 --> node_248
    node_40 --> node_147
    node_42 --> node_49
    node_60 --> node_176
    node_18 --> node_251
    node_10 --> node_536
    node_131 --> node_179
    node_40 --> node_256
    node_381 --> node_362
    node_478 --> node_316
    node_4 --> node_263
    node_45 --> node_160
    node_45 --> node_268
    node_19 --> node_409
    node_272 --> node_270
    node_52 --> node_237
    node_4 --> node_205
    node_52 --> node_229
    node_428 --> node_33
    node_349 --> node_553
    node_366 --> node_283
    node_372 --> node_337
    node_489 --> node_518
    node_398 --> node_301
    node_556 --> node_596
    node_52 --> node_259
    node_17 --> node_295
    node_374 --> node_34
    node_238 --> node_218
    node_40 --> node_226
    node_418 --> node_0
    node_52 --> node_408
    node_565 --> node_324
    node_131 --> node_272
    node_398 --> node_240
    node_272 --> node_271
    node_395 --> node_665
    node_42 --> node_41
    node_18 --> node_366
    node_45 --> node_290
    node_21 --> node_36
    node_17 --> node_592
    node_387 --> node_214
    node_410 --> node_665
    node_454 --> node_156
    node_612 --> node_176
    node_608 --> node_138
    node_52 --> node_230
    node_18 --> node_163
    node_565 --> node_639
    node_4 --> node_338
    node_40 --> node_665
    node_134 --> node_132
    node_17 --> node_645
    node_8 --> node_404
    node_18 --> node_235
    node_8 --> node_420
    node_418 --> node_532
    node_382 --> node_391
    node_366 --> node_233
    node_18 --> node_274
    node_4 --> node_238
    node_40 --> node_24
    node_40 --> node_247
    node_17 --> node_558
    node_8 --> node_438
    node_218 --> node_167
    node_295 --> node_654
    node_570 --> node_556
    node_8 --> node_99
    node_131 --> node_335
    node_134 --> node_113
    node_131 --> node_218
    node_420 --> node_417
    node_398 --> node_401
    node_400 --> node_162
    node_18 --> node_154
    node_225 --> node_223
    node_60 --> node_295
    node_218 --> node_168
    node_608 --> node_569
    node_439 --> node_605
    node_366 --> node_134
    node_101 --> node_664
    node_569 --> node_633
    node_52 --> node_282
    node_17 --> node_626
    node_40 --> node_300
    node_418 --> node_530
    node_131 --> node_216
    node_4 --> node_131
    node_57 --> node_625
    node_134 --> node_267
    node_171 --> node_78
    node_455 --> node_162
    node_387 --> node_237
    node_382 --> node_394
    node_8 --> node_50
    node_17 --> node_577
    node_18 --> node_536
    node_392 --> node_159
    node_40 --> node_331
    node_68 --> node_77
    node_580 --> node_310
    node_151 --> node_666
    node_42 --> node_44
    node_487 --> node_176
    node_376 --> node_338
    node_455 --> node_148
    node_398 --> node_283
    node_517 --> node_626
    node_52 --> node_489
    node_45 --> node_227
    node_366 --> node_219
    node_238 --> node_215
    node_505 --> node_546
    node_8 --> node_176
    node_40 --> node_555
    node_134 --> node_179
    node_399 --> node_243
    node_454 --> node_155
    node_40 --> node_73
    node_562 --> node_568
    node_52 --> node_183
    node_52 --> node_277
    node_569 --> node_632
    node_45 --> node_251
    node_40 --> node_424
    node_501 --> node_318
    node_502 --> node_645
    node_391 --> node_666
    node_8 --> node_664
    node_18 --> node_253
    node_398 --> node_252
    node_40 --> node_27
    node_366 --> node_666
    node_23 --> node_398
    node_342 --> node_562
    node_357 --> node_221
    node_134 --> node_272
    node_17 --> node_624
    node_8 --> node_403
    node_295 --> node_577
    node_134 --> node_405
    node_489 --> node_295
    node_505 --> node_350
    node_10 --> node_62
    node_52 --> node_260
    node_565 --> node_325
    node_349 --> node_605
    node_613 --> node_176
    node_374 --> node_169
    node_4 --> node_406
    node_192 --> node_186
    node_20 --> node_139
    node_28 --> node_295
    node_52 --> node_205
    node_487 --> node_295
    node_45 --> node_163
    node_18 --> node_123
    node_477 --> node_36
    node_569 --> node_556
    node_4 --> node_9
    node_45 --> node_235
    node_18 --> node_162
    node_366 --> node_336
    node_418 --> node_248
    node_396 --> node_144
    node_398 --> node_313
    node_40 --> node_208
    node_540 --> node_23
    node_130 --> node_129
    node_74 --> node_72
    node_134 --> node_335
    node_134 --> node_218
    node_586 --> node_588
    node_559 --> node_574
    node_565 --> node_652
    node_119 --> node_121
    node_374 --> node_168
    node_179 --> node_574
    node_397 --> node_156
    node_18 --> node_200
    node_52 --> node_338
    node_45 --> node_154
    node_134 --> node_216
    node_574 --> node_257
    node_274 --> node_165
    node_10 --> node_543
    node_60 --> node_624
    node_253 --> node_163
    node_4 --> node_70
    node_52 --> node_125
    node_52 --> node_238
    node_341 --> node_176
    node_142 --> node_181
    node_8 --> node_106
    node_556 --> node_557
    node_40 --> node_284
    node_40 --> node_478
    node_372 --> node_342
    node_238 --> node_198
    node_194 --> node_192
    node_43 --> node_21
    node_540 --> node_544
    node_4 --> node_233
    node_18 --> node_116
    node_250 --> node_406
    node_569 --> node_327
    node_487 --> node_618
    node_106 --> node_104
    node_52 --> node_565
    node_505 --> node_84
    node_393 --> node_229
    node_40 --> node_362
    node_456 --> node_111
    node_397 --> node_157
    node_455 --> node_143
    node_17 --> node_636
    node_52 --> node_131
    node_18 --> node_337
    node_483 --> node_649
    node_404 --> node_405
    node_505 --> node_118
    node_149 --> node_125
    node_282 --> node_280
    node_388 --> node_392
    node_52 --> node_530
    node_52 --> node_250
    node_418 --> node_99
    node_4 --> node_134
    node_238 --> node_160
    node_17 --> node_329
    node_18 --> node_361
    node_4 --> node_157
    node_516 --> node_654
    node_4 --> node_196
    node_418 --> node_81
    node_55 --> node_257
    node_169 --> node_274
    node_52 --> node_240
    node_492 --> node_646
    node_45 --> node_253
    node_565 --> node_319
    node_398 --> node_286
    node_70 --> node_72
    node_640 --> node_655
    node_17 --> node_662
    node_341 --> node_295
    node_5 --> node_20
    node_366 --> node_288
    node_387 --> node_338
    node_397 --> node_155
    node_18 --> node_273
    node_52 --> node_119
    node_55 --> node_596
    node_4 --> node_79
    node_398 --> node_321
    node_30 --> node_33
    node_4 --> node_225
    node_142 --> node_334
    node_169 --> node_161
    node_4 --> node_219
    node_40 --> node_237
    node_40 --> node_229
    node_48 --> node_14
    node_400 --> node_165
    node_17 --> node_632
    node_40 --> node_246
    node_18 --> node_543
    node_131 --> node_160
    node_162 --> node_161
    node_349 --> node_607
    node_40 --> node_259
    node_559 --> node_625
    node_18 --> node_291
    node_398 --> node_295
    node_179 --> node_625
    node_18 --> node_170
    node_60 --> node_365
    node_45 --> node_123
    node_398 --> node_297
    node_569 --> node_310
    node_40 --> node_33
    node_400 --> node_169
    node_489 --> node_644
    node_366 --> node_349
    node_18 --> node_278
    node_418 --> node_8
    node_40 --> node_206
    node_431 --> node_78
    node_45 --> node_162
    node_455 --> node_165
    node_489 --> node_509
    node_4 --> node_666
    node_455 --> node_145
    node_15 --> node_417
    node_366 --> node_269
    node_8 --> node_69
    node_580 --> node_317
    node_643 --> node_556
    node_45 --> node_200
    node_288 --> node_287
    node_119 --> node_122
    node_61 --> node_65
    node_8 --> node_439
    node_79 --> node_582
    node_208 --> node_207
    node_258 --> node_136
    node_17 --> node_556
    node_418 --> node_403
    node_565 --> node_648
    node_40 --> node_107
    node_398 --> node_172
    node_486 --> node_72
    node_52 --> node_283
    node_252 --> node_276
    node_253 --> node_162
    node_358 --> node_157
    node_374 --> node_157
    node_565 --> node_647
    node_426 --> node_26
    node_295 --> node_632
    node_238 --> node_227
    node_349 --> node_573
    node_4 --> node_336
    node_498 --> node_310
    node_432 --> node_395
    node_569 --> node_177
    node_587 --> node_21
    node_18 --> node_142
    node_4 --> node_553
    node_398 --> node_171
    node_570 --> node_138
    node_20 --> node_406
    node_583 --> node_172
    node_68 --> node_138
    node_625 --> node_79
    node_8 --> node_442
    node_45 --> node_337
    node_238 --> node_251
    node_40 --> node_410
    node_418 --> node_297
    node_20 --> node_9
    node_252 --> node_273
    node_61 --> node_21
    node_349 --> node_572
    node_381 --> node_394
    node_131 --> node_247
    node_52 --> node_233
    node_569 --> node_529
    node_40 --> node_441
    node_392 --> node_164
    node_17 --> node_327
    node_4 --> node_140
    node_60 --> node_556
    node_398 --> node_287
    node_40 --> node_195
    node_40 --> node_489
    node_23 --> node_396
    node_353 --> node_107
    node_398 --> node_136
    node_169 --> node_162
    node_18 --> node_181
    node_8 --> node_114
    node_454 --> node_159
    node_372 --> node_345
    node_123 --> node_119
    node_131 --> node_227
    node_358 --> node_153
    node_374 --> node_153
    node_570 --> node_569
    node_40 --> node_139
    node_68 --> node_569
    node_131 --> node_300
    node_497 --> node_631
    node_300 --> node_177
    node_399 --> node_242
    node_40 --> node_277
    node_238 --> node_163
    node_17 --> node_499
    node_45 --> node_273
    node_134 --> node_160
    node_486 --> node_138
    node_18 --> node_175
    node_480 --> node_328
    node_238 --> node_235
    node_280 --> node_539
    node_18 --> node_169
    node_505 --> node_536
    node_565 --> node_657
    node_504 --> node_138
    node_23 --> node_391
    node_612 --> node_556
    node_395 --> node_354
    node_40 --> node_467
    node_52 --> node_81
    node_45 --> node_291
    node_238 --> node_199
    node_514 --> node_651
    node_396 --> node_146
    node_366 --> node_268
    node_4 --> node_475
    node_50 --> node_281
    node_18 --> node_151
    node_489 --> node_632
    node_565 --> node_302
    node_66 --> node_434
    node_140 --> node_139
    node_45 --> node_170
    node_663 --> node_665
    node_8 --> node_84
    node_8 --> node_411
    node_522 --> node_313
    node_565 --> node_326
    node_380 --> node_102
    node_40 --> node_260
    node_238 --> node_154
    node_45 --> node_278
    node_538 --> node_539
    node_10 --> node_64
    node_366 --> node_213
    node_580 --> node_322
    node_40 --> node_263
    node_455 --> node_207
    node_40 --> node_205
    node_17 --> node_599
    node_593 --> node_594
    node_4 --> node_650
    node_565 --> node_312
    node_527 --> node_597
    node_4 --> node_288
    node_399 --> node_241
    node_366 --> node_290
    node_10 --> node_404
    node_10 --> node_420
    node_131 --> node_235
    node_523 --> node_308
    node_17 --> node_310
    node_418 --> node_136
    node_42 --> node_59
    node_467 --> node_138
    node_569 --> node_571
    node_23 --> node_394
    node_106 --> node_150
    node_399 --> node_188
    node_73 --> node_295
    node_644 --> node_577
    node_565 --> node_320
    node_10 --> node_99
    node_40 --> node_19
    node_52 --> node_8
    node_131 --> node_199
    node_40 --> node_338
    node_565 --> node_650
    node_4 --> node_349
    node_18 --> node_221
    node_18 --> node_149
    node_398 --> node_311
    node_487 --> node_556
    node_40 --> node_238
    node_451 --> node_176
    node_157 --> node_156
    node_20 --> node_456
    node_398 --> node_198
    node_48 --> node_569
    node_432 --> node_397
    node_45 --> node_142
    node_237 --> node_236
    node_297 --> node_560
    node_142 --> node_335
    node_160 --> node_257
    node_569 --> node_658
    node_52 --> node_403
    node_238 --> node_124
    node_263 --> node_262
    node_52 --> node_341
    node_418 --> node_69
    node_418 --> node_546
    node_557 --> node_561
    node_238 --> node_253
    node_130 --> node_257
    node_131 --> node_208
    node_6 --> node_569
    node_52 --> node_336
    node_8 --> node_21
    node_43 --> node_34
    node_391 --> node_249
    node_57 --> node_248
    node_8 --> node_539
    node_252 --> node_169
    node_17 --> node_177
    node_40 --> node_32
    node_40 --> node_131
    node_20 --> node_666
    node_134 --> node_227
    node_392 --> node_166
    node_295 --> node_310
    node_43 --> node_138
    node_134 --> node_300
    node_45 --> node_181
    node_398 --> node_329
    node_565 --> node_637
    node_18 --> node_380
    node_389 --> node_265
    node_409 --> node_72
    node_52 --> node_295
    node_300 --> node_138
    node_252 --> node_168
    node_349 --> node_564
    node_131 --> node_284
    node_238 --> node_123
    node_4 --> node_23
    node_18 --> node_404
    node_45 --> node_175
    node_18 --> node_420
    node_131 --> node_124
    node_366 --> node_265
    node_455 --> node_664
    node_45 --> node_169
    node_569 --> node_324
    node_40 --> node_583
    node_505 --> node_116
    node_397 --> node_159
    node_489 --> node_499
    node_139 --> node_569
    node_565 --> node_659
    node_131 --> node_253
    node_387 --> node_666
    node_565 --> node_644
    node_391 --> node_141
    node_43 --> node_569
    node_664 --> node_666
    node_10 --> node_403
    node_17 --> node_469
    node_655 --> node_323
    node_45 --> node_151
    node_40 --> node_16
    node_486 --> node_67
    node_238 --> node_200
    node_253 --> node_165
    node_398 --> node_333
    node_157 --> node_155
    node_295 --> node_177
    node_134 --> node_163
    node_528 --> node_647
    node_18 --> node_267
    node_20 --> node_295
    node_134 --> node_235
    node_72 --> node_138
    node_253 --> node_169
    node_387 --> node_341
    node_40 --> node_538
    node_366 --> node_232
    node_349 --> node_107
    node_55 --> node_618
    node_282 --> node_279
    node_10 --> node_204
    node_74 --> node_176
    node_349 --> node_561
    node_509 --> node_23
    node_134 --> node_199
    node_442 --> node_16
    node_565 --> node_627
    node_391 --> node_180
    node_389 --> node_264
    node_650 --> node_567
    node_349 --> node_560
    node_40 --> node_406
    node_300 --> node_296
    node_366 --> node_274
    node_171 --> node_172
    node_366 --> node_174
    node_393 --> node_292
    node_52 --> node_288
    node_238 --> node_337
    node_131 --> node_200
    node_45 --> node_221
    node_45 --> node_149
    node_366 --> node_264
    node_4 --> node_213
    node_169 --> node_165
    node_72 --> node_569
    node_238 --> node_276
    node_131 --> node_246
    node_391 --> node_203
    node_418 --> node_84
    node_44 --> node_26
    node_18 --> node_222
    node_10 --> node_106
    node_418 --> node_411
    node_505 --> node_543
    node_516 --> node_503
    node_42 --> node_53
    node_521 --> node_330
    node_569 --> node_305
    node_52 --> node_215
    node_52 --> node_136
    node_134 --> node_208
    node_395 --> node_156
    node_418 --> node_118
    node_390 --> node_161
    node_89 --> node_176
    node_578 --> node_650
    node_559 --> node_575
    node_57 --> node_176
    node_392 --> node_167
    node_52 --> node_349
    node_565 --> node_640
    node_580 --> node_634
    node_18 --> node_272
    node_17 --> node_138
    node_40 --> node_425
    node_457 --> node_168
    node_610 --> node_295
    node_448 --> node_451
    node_569 --> node_322
    node_225 --> node_224
    node_543 --> node_544
    node_238 --> node_273
    node_21 --> node_71
    node_52 --> node_269
    node_366 --> node_258
    node_405 --> node_298
    node_40 --> node_433
    node_40 --> node_233
    node_74 --> node_295
    node_134 --> node_284
    node_131 --> node_276
    node_366 --> node_220
    node_398 --> node_327
    node_134 --> node_124
    node_57 --> node_405
    node_391 --> node_202
    node_238 --> node_170
    node_52 --> node_546
    node_40 --> node_518
    node_134 --> node_253
    node_546 --> node_539
    node_8 --> node_31
    node_313 --> node_298
    node_18 --> node_335
    node_17 --> node_569
    node_366 --> node_332
    node_572 --> node_567
    node_18 --> node_218
    node_40 --> node_134
    node_100 --> node_164
    node_569 --> node_325
    node_633 --> node_17
    node_106 --> node_107
    node_4 --> node_574
    node_63 --> node_21
    node_45 --> node_293
    node_10 --> node_61
    node_505 --> node_532
    node_40 --> node_663
    node_487 --> node_529
    node_390 --> node_164
    node_398 --> node_274
    node_131 --> node_273
    node_18 --> node_216
    node_418 --> node_21
    node_459 --> node_26
    node_23 --> node_389
    node_418 --> node_539
    node_60 --> node_138
    node_468 --> node_596
    node_426 --> node_459
    node_36 --> node_33
    node_18 --> node_377
    node_398 --> node_289
    node_21 --> node_539
    node_89 --> node_295
    node_69 --> node_68
    node_459 --> node_223
    node_17 --> node_324
    node_18 --> node_106
    node_45 --> node_267
    node_398 --> node_154
    node_52 --> node_350
    node_569 --> node_652
    node_131 --> node_195
    node_480 --> node_660
    node_395 --> node_155
    node_387 --> node_349
    node_349 --> node_19
    node_4 --> node_265
    node_40 --> node_219
    node_366 --> node_123
    node_559 --> node_248
    node_395 --> node_353
    node_179 --> node_248
    node_52 --> node_198
    node_467 --> node_471
    node_10 --> node_69
    node_372 --> node_340
    node_134 --> node_200
    node_60 --> node_569
    node_238 --> node_142
    node_366 --> node_162
    node_530 --> node_26
    node_72 --> node_67
    node_395 --> node_666
    node_73 --> node_340
    node_358 --> node_665
    node_134 --> node_246
    node_10 --> node_439
    node_366 --> node_230
    node_565 --> node_635
    node_229 --> node_228
    node_396 --> node_148
    node_18 --> node_379
    node_405 --> node_176
    node_250 --> node_574
    node_566 --> node_565
    node_398 --> node_310
    node_580 --> node_626
    node_40 --> node_648
    node_376 --> node_346
    node_486 --> node_176
    node_624 --> node_79
    node_250 --> node_249
    node_467 --> node_472
    node_297 --> node_13
    node_40 --> node_666
    node_45 --> node_222
    node_349 --> node_565
    node_8 --> node_116
    node_504 --> node_176
    node_496 --> node_659
    node_589 --> node_618
    node_4 --> node_232
    node_52 --> node_268
    node_349 --> node_562
    node_179 --> node_298
    node_392 --> node_156
    node_526 --> node_176
    node_612 --> node_569
    node_565 --> node_314
    node_131 --> node_263
    node_52 --> node_213
    node_142 --> node_333
    node_218 --> node_161
    node_43 --> node_380
    node_45 --> node_272
    node_69 --> node_72
    node_131 --> node_142
    node_4 --> node_274
    node_366 --> node_282
    node_10 --> node_442
    node_17 --> node_303
    node_388 --> node_387
    node_45 --> node_153
    node_4 --> node_174
    node_349 --> node_575
    node_134 --> node_276
    node_52 --> node_290
    node_388 --> node_398
    node_489 --> node_138
    node_52 --> node_84
    node_17 --> node_305
    node_40 --> node_286
    node_300 --> node_294
    node_4 --> node_264
    node_238 --> node_169
    node_40 --> node_336
    node_300 --> node_298
    node_351 --> node_341
    node_565 --> node_307
    node_569 --> node_319
    node_73 --> node_21
    node_4 --> node_625
    node_216 --> node_664
    node_506 --> node_634
    node_52 --> node_118
    node_40 --> node_553
    node_487 --> node_138
    node_467 --> node_176
    node_130 --> node_553
    node_36 --> node_569
    node_238 --> node_151
    node_8 --> node_34
    node_556 --> node_582
    node_579 --> node_79
    node_432 --> node_392
    node_597 --> node_438
    node_17 --> node_322
    node_418 --> node_536
    node_306 --> node_17
    node_45 --> node_335
    node_52 --> node_559
    node_45 --> node_218
    node_40 --> node_388
    node_42 --> node_51
    node_134 --> node_273
    node_100 --> node_166
    node_40 --> node_140
    node_18 --> node_69
    node_372 --> node_343
    node_4 --> node_258
    node_8 --> node_441
    node_583 --> node_588
    node_390 --> node_166
    node_45 --> node_216
    node_431 --> node_172
    node_285 --> node_286
    node_18 --> node_439
    node_524 --> node_661
    node_101 --> node_142
    node_131 --> node_169
    node_366 --> node_183
    node_487 --> node_569
    node_218 --> node_164
    node_134 --> node_195
    node_42 --> node_45
    node_134 --> node_170
    node_17 --> node_552
    node_4 --> node_220
    node_454 --> node_158
    node_399 --> node_191
    node_439 --> node_438
    node_10 --> node_84
    node_420 --> node_400
    node_10 --> node_411
    node_157 --> node_159
    node_191 --> node_188
    node_630 --> node_316
    node_295 --> node_305
    node_140 --> node_295
    node_131 --> node_151
    node_569 --> node_634
    node_559 --> node_176
    node_8 --> node_569
    node_140 --> node_297
    node_366 --> node_291
    node_250 --> node_625
    node_238 --> node_221
    node_179 --> node_176
    node_238 --> node_149
    node_387 --> node_213
    node_599 --> node_601
    node_4 --> node_332
    node_636 --> node_649
    node_200 --> node_201
    node_8 --> node_437
    node_40 --> node_172
    node_17 --> node_641
    node_366 --> node_278
    node_28 --> node_36
    node_556 --> node_554
    node_370 --> node_665
    node_418 --> node_31
    node_52 --> node_21
    node_559 --> node_557
    node_52 --> node_227
    node_459 --> node_171
    node_295 --> node_322
    node_398 --> node_135
    node_408 --> node_407
    node_18 --> node_442
    node_252 --> node_275
    node_274 --> node_163
    node_642 --> node_551
    node_505 --> node_404
    node_17 --> node_652
    node_396 --> node_143
    node_263 --> node_261
    node_505 --> node_420
    node_468 --> node_176
    node_119 --> node_120
    node_565 --> node_328
    node_366 --> node_143
    node_485 --> node_356
    node_583 --> node_78
    node_4 --> node_588
    node_223 --> node_555
    node_48 --> node_553
    node_305 --> node_34
    node_382 --> node_395
    node_444 --> node_593
    node_52 --> node_251
    node_405 --> node_577
    node_4 --> node_237
    node_20 --> node_574
    node_4 --> node_229
    node_40 --> node_288
    node_505 --> node_99
    node_644 --> node_177
    node_134 --> node_263
    node_444 --> node_603
    node_613 --> node_569
    node_134 --> node_142
    node_387 --> node_236
    node_565 --> node_649
    node_70 --> node_75
    node_40 --> node_66
    node_341 --> node_138
    node_20 --> node_4
    node_300 --> node_405
    node_313 --> node_577
    node_366 --> node_125
    node_418 --> node_582
    node_12 --> node_110
    node_4 --> node_230
    node_40 --> node_349
    node_52 --> node_232
    node_559 --> node_295
    node_276 --> node_275
    node_559 --> node_297
    node_10 --> node_21
    node_52 --> node_163
    node_179 --> node_297
    node_387 --> node_346
    node_398 --> node_273
    node_238 --> node_293
    node_398 --> node_138
    node_40 --> node_269
    node_372 --> node_348
    node_52 --> node_235
    node_398 --> node_158
    node_295 --> node_652
    node_52 --> node_274
    node_100 --> node_167
    node_404 --> node_139
    node_4 --> node_72
    node_140 --> node_136
    node_569 --> node_597
    node_391 --> node_250
    node_391 --> node_181
    node_418 --> node_116
    node_569 --> node_657
    node_17 --> node_496
    node_18 --> node_147
    node_139 --> node_553
    node_390 --> node_167
    node_478 --> node_648
    node_40 --> node_605
    node_40 --> node_42
    node_398 --> node_170
    node_66 --> node_71
    node_366 --> node_181
    node_366 --> node_250
    node_398 --> node_255
    node_238 --> node_267
    node_4 --> node_282
    node_52 --> node_154
    node_599 --> node_602
    node_134 --> node_169
    node_569 --> node_302
    node_374 --> node_164
    node_396 --> node_145
    node_569 --> node_316
    node_42 --> node_56
    node_569 --> node_326
    node_40 --> node_659
    node_8 --> node_60
    node_30 --> node_23
    node_18 --> node_226
    node_40 --> node_644
    node_51 --> node_21
    node_318 --> node_567
    node_437 --> node_436
    node_366 --> node_175
    node_134 --> node_151
    node_366 --> node_240
    node_238 --> node_157
    node_418 --> node_369
    node_398 --> node_317
    node_131 --> node_293
    node_238 --> node_196
    node_40 --> node_509
    node_52 --> node_536
    node_459 --> node_285
    node_40 --> node_23
    node_366 --> node_119
    node_455 --> node_163
    node_43 --> node_379
    node_286 --> node_285
    node_586 --> node_590
    node_565 --> node_656
    node_395 --> node_159
    node_238 --> node_222
    node_40 --> node_350
    node_398 --> node_296
    node_17 --> node_79
    node_20 --> node_625
    node_179 --> node_577
    node_18 --> node_247
    node_4 --> node_139
    node_569 --> node_650
    node_393 --> node_290
    node_238 --> node_225
    node_258 --> node_257
    node_4 --> node_183
    node_4 --> node_277
    node_17 --> node_634
    node_538 --> node_542
    node_394 --> node_210
    node_559 --> node_136
    node_418 --> node_543
    node_349 --> node_557
    node_455 --> node_154
    node_131 --> node_157
    node_238 --> node_272
    node_131 --> node_196
    node_4 --> node_55
    node_543 --> node_34
    node_238 --> node_153
    node_352 --> node_154
    node_29 --> node_664
    node_18 --> node_300
    node_664 --> node_180
    node_398 --> node_197
    node_599 --> node_597
    node_349 --> node_341
    node_48 --> node_605
    node_388 --> node_396
    node_4 --> node_260
    node_131 --> node_222
    node_505 --> node_106
    node_90 --> node_19
    node_40 --> node_268
    node_305 --> node_32
    node_391 --> node_248
    node_4 --> node_318
    node_60 --> node_79
    node_131 --> node_225
    node_398 --> node_323
    node_40 --> node_213
    node_131 --> node_219
    node_134 --> node_406
    node_238 --> node_335
    node_4 --> node_143
    node_559 --> node_624
    node_609 --> node_176
    node_489 --> node_471
    node_8 --> node_74
    node_52 --> node_123
    node_55 --> node_529
    node_89 --> node_77
    node_250 --> node_139
    node_40 --> node_290
    node_398 --> node_257
    node_52 --> node_162
    node_398 --> node_303
    node_28 --> node_542
    node_349 --> node_295
    node_131 --> node_153
    node_297 --> node_581
    node_8 --> node_380
    node_238 --> node_216
    node_295 --> node_634
    node_516 --> node_322
    node_387 --> node_347
    node_489 --> node_313
    node_565 --> node_318
    node_489 --> node_522
    node_244 --> node_243
    node_523 --> node_637
    node_45 --> node_147
    node_61 --> node_204
    node_52 --> node_200
    node_530 --> node_534
    node_4 --> node_125
    node_45 --> node_256
    node_393 --> node_227
    node_420 --> node_107
    node_458 --> node_412
    node_398 --> node_322
    node_374 --> node_166
    node_40 --> node_559
    node_18 --> node_199
    node_134 --> node_293
    node_59 --> node_410
    node_45 --> node_226
    node_73 --> node_138
    node_4 --> node_566
    node_238 --> node_140
    node_565 --> node_306
    node_17 --> node_302
    node_17 --> node_316
    node_398 --> node_334
    node_5 --> node_555
    node_152 --> node_115
    node_609 --> node_295
    node_40 --> node_574
    node_489 --> node_176
    node_4 --> node_250
    node_52 --> node_337
    node_223 --> node_34
    node_23 --> node_362
    node_18 --> node_208
    node_398 --> node_149
    node_45 --> node_247
    node_28 --> node_176
    node_427 --> node_33
    node_43 --> node_23
    node_28 --> node_580
    node_134 --> node_157
    node_418 --> node_257
    node_404 --> node_406
    node_458 --> node_553
    node_134 --> node_196
    node_20 --> node_72
    node_40 --> node_4
    node_663 --> node_666
    node_4 --> node_240
    node_40 --> node_448
    node_131 --> node_140
    node_505 --> node_69
    node_238 --> node_475
    node_387 --> node_344
    node_140 --> node_574
    node_45 --> node_300
    node_349 --> node_136
    node_40 --> node_265
    node_4 --> node_119
    node_134 --> node_222
    node_60 --> node_379
    node_505 --> node_439
    node_18 --> node_284
    node_538 --> node_547
    node_565 --> node_301
    node_18 --> node_368
    node_18 --> node_124
    node_569 --> node_640
    node_10 --> node_116
    node_52 --> node_138
    node_18 --> node_358
    node_70 --> node_76
    node_134 --> node_225
    node_295 --> node_626
    node_484 --> node_640
    node_134 --> node_219
    node_25 --> node_13
    node_295 --> node_302
    node_349 --> node_581
    node_45 --> node_331
    node_366 --> node_179
    node_40 --> node_487
    node_295 --> node_316
    node_389 --> node_664
    node_52 --> node_543
    node_398 --> node_294
    node_398 --> node_298
    node_565 --> node_660
    node_52 --> node_291
    node_451 --> node_138
    node_8 --> node_363
    node_134 --> node_153
    node_52 --> node_170
    node_366 --> node_664
    node_52 --> node_278
    node_410 --> node_629
    node_59 --> node_19
    node_131 --> node_475
    node_40 --> node_232
    node_217 --> node_154
    node_505 --> node_442
    node_42 --> node_50
    node_366 --> node_272
    node_311 --> node_655
    node_479 --> node_409
    node_215 --> node_214
    node_374 --> node_167
    node_52 --> node_143
    node_19 --> node_356
    node_59 --> node_409
    node_40 --> node_274
    node_366 --> node_217
    node_40 --> node_174
    node_451 --> node_569
    node_520 --> node_619
    node_493 --> node_561
    node_4 --> node_283
    node_507 --> node_321
    node_399 --> node_193
    node_4 --> node_248
    node_40 --> node_264
    node_45 --> node_199
    node_589 --> node_529
    node_632 --> node_34
    node_398 --> node_239
    node_40 --> node_625
    node_578 --> node_318
    node_40 --> node_30
    node_455 --> node_158
    node_505 --> node_633
    node_559 --> node_556
    node_10 --> node_441
    node_18 --> node_246
    node_366 --> node_218
    node_514 --> node_319
    node_352 --> node_158
    node_486 --> node_76
    node_4 --> node_601
    node_37 --> node_583
    node_17 --> node_630
    node_274 --> node_169
    node_18 --> node_206
    node_50 --> node_23
    node_569 --> node_573
    node_23 --> node_395
    node_45 --> node_208
    node_8 --> node_388
    node_140 --> node_625
    node_40 --> node_258
    node_505 --> node_411
    node_30 --> node_381
    node_418 --> node_404
    node_506 --> node_307
    node_538 --> node_545
    node_418 --> node_420
    node_398 --> node_222
    node_10 --> node_437
    node_134 --> node_140
    node_644 --> node_298
    node_485 --> node_365
    node_17 --> node_330
    node_428 --> node_100
    node_274 --> node_168
    node_40 --> node_220
    node_8 --> node_379
    node_417 --> node_33
    node_569 --> node_572
    node_52 --> node_181
    node_603 --> node_601
    node_18 --> node_276
    node_250 --> node_248
    node_615 --> node_176
    node_40 --> node_381
    node_58 --> node_666
    node_232 --> node_231
    node_578 --> node_565
    node_169 --> node_163
    node_74 --> node_138
    node_40 --> node_332
    node_45 --> node_284
    node_573 --> node_581
    node_106 --> node_111
    node_157 --> node_158
    node_569 --> node_314
    node_169 --> node_235
    node_45 --> node_124
    node_52 --> node_175
    node_40 --> node_68
    node_17 --> node_661
    node_52 --> node_169
    node_52 --> node_257
    node_18 --> node_34
    node_252 --> node_164
    node_370 --> node_238
    node_476 --> node_410
    node_405 --> node_177
    node_597 --> node_598
    node_40 --> node_649
    node_381 --> node_397
    node_60 --> node_114
    node_433 --> node_532
    node_134 --> node_475
    node_569 --> node_307
    node_238 --> node_147
    node_601 --> node_598
    node_40 --> node_588
    node_19 --> node_664
    node_17 --> node_511
    node_4 --> node_456
    node_238 --> node_256
    node_392 --> node_163
    node_565 --> node_313
    node_398 --> node_335
    node_18 --> node_441
    node_7 --> node_107
    node_89 --> node_138
    node_366 --> node_215
    node_313 --> node_177
    node_357 --> node_219
    node_18 --> node_195
    node_28 --> node_624
    node_57 --> node_138
    node_349 --> node_340
    node_382 --> node_392
    node_238 --> node_226
    node_40 --> node_408
    node_358 --> node_156
    node_374 --> node_156
    node_40 --> node_162
    node_584 --> node_590
    node_432 --> node_387
    node_4 --> node_176
    node_400 --> node_167
    node_4 --> node_179
    node_359 --> node_666
    node_510 --> node_302
    node_40 --> node_230
    node_42 --> node_40
    node_615 --> node_295
    node_457 --> node_161
    node_392 --> node_154
    node_418 --> node_35
    node_489 --> node_486
    node_7 --> node_395
    node_392 --> node_161
    node_18 --> node_437
    node_131 --> node_147
    node_455 --> node_169
    node_400 --> node_168
    node_4 --> node_664
    node_664 --> node_181
    node_52 --> node_221
    node_52 --> node_149
    node_131 --> node_256
    node_45 --> node_246
    node_57 --> node_569
    node_238 --> node_247
    node_418 --> node_405
    node_18 --> node_467
    node_72 --> node_73
    node_280 --> node_544
    node_45 --> node_259
    node_40 --> node_78
    node_445 --> node_578
    node_40 --> node_72
    node_36 --> node_23
    node_580 --> node_324
    node_60 --> node_90
    node_387 --> node_175
    node_131 --> node_226
    node_385 --> node_270
    node_398 --> node_254
    node_632 --> node_32
    node_40 --> node_135
    node_45 --> node_206
    node_40 --> node_282
    node_18 --> node_263
    node_580 --> node_639
    node_18 --> node_371
    node_8 --> node_605
    node_18 --> node_205
    node_538 --> node_544
    node_17 --> node_483
    node_238 --> node_300
    node_23 --> node_397
    node_546 --> node_547
    node_399 --> node_187
    node_393 --> node_291
    node_565 --> node_628
    node_448 --> node_446
    node_569 --> node_328
    node_30 --> node_374
    node_515 --> node_601
    node_376 --> node_666
    node_457 --> node_164
    node_45 --> node_276
    node_208 --> node_211
    node_238 --> node_331
    node_200 --> node_378
    node_395 --> node_351
    node_4 --> node_295
    node_583 --> node_618
    node_217 --> node_158
    node_18 --> node_19
    node_140 --> node_135
    node_23 --> node_357
    node_4 --> node_297
    node_179 --> node_177
    node_565 --> node_654
    node_525 --> node_658
    node_20 --> node_248
    node_8 --> node_23
    node_40 --> node_374
    node_455 --> node_149
    node_358 --> node_155
    node_374 --> node_155
    node_565 --> node_321
    node_418 --> node_106
    node_52 --> node_404
    node_52 --> node_420
    node_349 --> node_551
    node_366 --> node_198
    node_73 --> node_176
    node_356 --> node_176
    node_395 --> node_158
    node_252 --> node_166
    node_364 --> node_666
    node_405 --> node_138
    node_74 --> node_67
    node_569 --> node_564
    node_40 --> node_183
    node_376 --> node_341
    node_399 --> node_189
    node_4 --> node_58
    node_52 --> node_99
    node_358 --> node_666
    node_483 --> node_317
    node_17 --> node_494
    node_569 --> node_653
    node_580 --> node_305
    node_420 --> node_26
    node_131 --> node_331
    node_40 --> node_291
    node_18 --> node_131
    node_101 --> node_665
    node_398 --> node_137
    node_18 --> node_60
    node_80 --> node_15
    node_366 --> node_160
    node_392 --> node_162
    node_45 --> node_195
    node_52 --> node_267
    node_8 --> node_544
    node_526 --> node_138
    node_40 --> node_278
    node_565 --> node_645
    node_489 --> node_491
    node_569 --> node_308
    node_405 --> node_569
    node_140 --> node_138
    node_250 --> node_297
    node_57 --> node_60
    node_60 --> node_555
    node_134 --> node_147
    node_486 --> node_569
    node_553 --> node_13
    node_288 --> node_114
    node_131 --> node_265
    node_642 --> node_664
    node_40 --> node_143
    node_134 --> node_256
    node_40 --> node_317
    node_40 --> node_587
    node_504 --> node_569
    node_372 --> node_339
    node_420 --> node_413
    node_569 --> node_561
    node_17 --> node_517
    node_169 --> node_276
    node_18 --> node_376
    node_552 --> node_564
    node_238 --> node_208
    node_526 --> node_569
    node_134 --> node_226
    node_356 --> node_295
    node_546 --> node_545
    node_582 --> node_585
    node_52 --> node_176
    node_4 --> node_215
    node_52 --> node_179
    node_305 --> node_23
    node_4 --> node_136
    node_386 --> node_336
    node_40 --> node_56
    node_45 --> node_260
    node_84 --> node_85
    node_510 --> node_627
    node_28 --> node_556
    node_40 --> node_125
    node_349 --> node_567
    node_45 --> node_263
    node_52 --> node_664
    node_10 --> node_211
    node_17 --> node_478
    node_45 --> node_205
    node_408 --> node_410
    node_574 --> node_553
    node_28 --> node_21
    node_4 --> node_269
    node_52 --> node_272
    node_69 --> node_71
    node_169 --> node_273
    node_238 --> node_284
    node_52 --> node_628
    node_18 --> node_538
    node_467 --> node_569
    node_152 --> node_150
    node_539 --> node_541
    node_134 --> node_247
    node_511 --> node_652
    node_467 --> node_470
    node_40 --> node_464
    node_502 --> node_314
    node_580 --> node_652
    node_455 --> node_157
    node_282 --> node_281
    node_131 --> node_174
    node_20 --> node_176
    node_457 --> node_166
    node_4 --> node_624
    node_559 --> node_138
    node_399 --> node_190
    node_418 --> node_439
    node_530 --> node_533
    node_179 --> node_138
    node_426 --> node_171
    node_45 --> node_338
    node_40 --> node_530
    node_252 --> node_167
    node_40 --> node_181
    node_40 --> node_250
    node_45 --> node_238
    node_20 --> node_664
    node_52 --> node_335
    node_448 --> node_453
    node_52 --> node_218
    node_17 --> node_524
    node_366 --> node_227
    node_370 --> node_666
    node_565 --> node_651
    node_392 --> node_158
    node_410 --> node_303
    node_363 --> node_362
    node_376 --> node_349
    node_468 --> node_138
    node_40 --> node_175
    node_40 --> node_240
    node_4 --> node_486
    node_134 --> node_331
    node_52 --> node_216
    node_559 --> node_569
    node_387 --> node_176
    node_179 --> node_569
    node_387 --> node_179
    node_387 --> node_345
    node_8 --> node_448
    node_366 --> node_251
    node_418 --> node_442
    node_131 --> node_258
    node_18 --> node_293
    node_55 --> node_553
    node_40 --> node_119
    node_45 --> node_131
    node_399 --> node_245
    node_40 --> node_89
    node_455 --> node_153
    node_10 --> node_363
    node_569 --> node_639
    node_52 --> node_106
    node_559 --> node_579
    node_17 --> node_564
    node_131 --> node_220
    node_19 --> node_365
    node_156 --> node_21
    node_18 --> node_233
    node_238 --> node_237
    node_134 --> node_265
    node_238 --> node_229
    node_4 --> node_198
    node_238 --> node_246
    node_300 --> node_569
    node_69 --> node_77
    node_468 --> node_569
    node_140 --> node_257
    node_238 --> node_259
    node_40 --> node_434
    node_610 --> node_176
    node_131 --> node_332
    node_20 --> node_297
    node_100 --> node_163
    node_572 --> node_573
    node_238 --> node_206
    node_398 --> node_309
    node_366 --> node_163
    node_253 --> node_167
    node_565 --> node_311
    node_18 --> node_134
    node_10 --> node_15
    node_387 --> node_217
    node_384 --> node_419
    node_546 --> node_544
    node_18 --> node_157
    node_388 --> node_400
    node_17 --> node_308
    node_366 --> node_235
    node_390 --> node_163
    node_569 --> node_306
    node_50 --> node_373
    node_18 --> node_196
    node_600 --> node_598
    node_18 --> node_663
    node_4 --> node_160
    node_4 --> node_268
    node_391 --> node_199
    node_543 --> node_23
    node_253 --> node_168
    node_467 --> node_465
    node_498 --> node_639
    node_501 --> node_650
    node_366 --> node_199
    node_582 --> node_584
    node_387 --> node_218
    node_131 --> node_237
    node_131 --> node_229
    node_462 --> node_23
    node_418 --> node_544
    node_505 --> node_441
    node_569 --> node_565
    node_404 --> node_574
    node_366 --> node_154
    node_21 --> node_544
    node_100 --> node_161
    node_40 --> node_283
    node_131 --> node_259
    node_454 --> node_154
    node_40 --> node_248
    node_4 --> node_290
    node_73 --> node_109
    node_57 --> node_52
    node_174 --> node_171
    node_174 --> node_173
    node_457 --> node_167
    node_194 --> node_191
    node_18 --> node_225
    node_18 --> node_219
    node_42 --> node_555
    node_398 --> node_300
    node_10 --> node_388
    node_131 --> node_206
    node_208 --> node_209
    node_349 --> node_351
    node_36 --> node_381
    node_559 --> node_257
    node_569 --> node_301
    node_18 --> node_153
    node_18 --> node_363
    node_17 --> node_482
    node_505 --> node_437
    node_392 --> node_165
    node_580 --> node_648
    node_140 --> node_248
    node_179 --> node_178
    node_40 --> node_356
    node_565 --> node_642
    node_169 --> node_168
    node_349 --> node_103
    node_9 --> node_114
    node_505 --> node_467
    node_358 --> node_159
    node_374 --> node_159
    node_569 --> node_660
    node_238 --> node_195
    node_52 --> node_69
    node_17 --> node_502
    node_548 --> node_539
    node_23 --> node_392
    node_40 --> node_420
    node_73 --> node_114
    node_422 --> node_591
    node_69 --> node_14
    node_131 --> node_282
    node_52 --> node_439
    node_565 --> node_632
    node_40 --> node_438
    node_366 --> node_124
    node_490 --> node_304
    node_134 --> node_220
    node_40 --> node_99
    node_119 --> node_123
    node_366 --> node_253
    node_238 --> node_277
    node_458 --> node_560
    node_8 --> node_381
    node_40 --> node_313
    node_60 --> node_410
    node_45 --> node_233
    node_40 --> node_81
    node_134 --> node_332
    node_393 --> node_664
    node_4 --> node_21
    node_387 --> node_215
    node_4 --> node_227
    node_376 --> node_340
    node_223 --> node_23
    node_383 --> node_666
    node_123 --> node_121
    node_20 --> node_624
    node_499 --> node_632
    node_609 --> node_138
    node_640 --> node_323
    node_238 --> node_260
    node_17 --> node_639
    node_52 --> node_442
    node_40 --> node_456
    node_17 --> node_523
    node_45 --> node_134
    node_18 --> node_388
    node_238 --> node_263
    node_4 --> node_251
    node_238 --> node_205
    node_404 --> node_625
    node_100 --> node_162
    node_45 --> node_157
    node_194 --> node_185
    node_18 --> node_140
    node_437 --> node_137
    node_45 --> node_196
    node_131 --> node_183
    node_134 --> node_237
    node_131 --> node_277
    node_134 --> node_229
    node_390 --> node_162
    node_513 --> node_431
    node_218 --> node_163
    node_391 --> node_200
    node_134 --> node_259
    node_312 --> node_664
    node_418 --> node_22
    node_580 --> node_302
    node_8 --> node_408
    node_40 --> node_176
    node_418 --> node_555
    node_455 --> node_209
    node_40 --> node_179
    node_40 --> node_580
    node_366 --> node_200
    node_580 --> node_316
    node_630 --> node_648
    node_40 --> node_8
    node_106 --> node_103
    node_134 --> node_206
    node_410 --> node_664
    node_238 --> node_338
    node_52 --> node_160
    node_40 --> node_557
    node_569 --> node_601
    node_131 --> node_260
    node_45 --> node_225
    node_40 --> node_664
    node_4 --> node_163
    node_45 --> node_219
    node_295 --> node_324
    node_300 --> node_406
    node_398 --> node_284
    node_418 --> node_27
    node_4 --> node_235
    node_131 --> node_205
    node_565 --> node_327
    node_398 --> node_124
    node_397 --> node_154
    node_18 --> node_475
    node_140 --> node_176
    node_40 --> node_403
    node_8 --> node_364
    node_295 --> node_639
    node_398 --> node_253
    node_28 --> node_34
    node_520 --> node_600
    node_580 --> node_320
    node_52 --> node_411
    node_394 --> node_207
    node_160 --> node_553
    node_8 --> node_541
    node_366 --> node_337
    node_381 --> node_386
    node_349 --> node_257
    node_4 --> node_154
    node_52 --> node_147
    node_28 --> node_138
    node_238 --> node_131
    node_60 --> node_19
    node_18 --> node_288
    node_147 --> node_144
    node_366 --> node_276
    node_134 --> node_282
    node_297 --> node_298
    node_131 --> node_338
    node_568 --> node_551
    node_376 --> node_343
    node_26 --> node_428
    node_40 --> node_218
    node_140 --> node_405
    node_368 --> node_367
    node_131 --> node_238
    node_68 --> node_295
    node_558 --> node_581
    node_632 --> node_23
    node_40 --> node_295
    node_52 --> node_226
    node_60 --> node_409
    node_349 --> node_342
    node_40 --> node_297
    node_489 --> node_569
    node_17 --> node_516
    node_73 --> node_77
    node_505 --> node_538
    node_28 --> node_569
    node_45 --> node_336
    node_366 --> node_273
    node_8 --> node_489
    node_4 --> node_567
    node_21 --> node_14
    node_48 --> node_666
    node_40 --> node_106
    node_382 --> node_387
    node_517 --> node_301
    node_495 --> node_648
    node_525 --> node_326
    node_583 --> node_529
    node_398 --> node_246
    node_52 --> node_247
    node_51 --> node_114
    node_538 --> node_540
    node_586 --> node_589
    node_134 --> node_139
    node_131 --> node_250
    node_173 --> node_171
    node_366 --> node_195
    node_565 --> node_310
    node_366 --> node_170
    node_455 --> node_147
    node_142 --> node_331
    node_134 --> node_183
    node_505 --> node_17
    node_134 --> node_277
    node_18 --> node_42
    node_569 --> node_648
    node_559 --> node_79
    node_20 --> node_491
    node_569 --> node_602
    node_583 --> node_582
    node_45 --> node_140
    node_4 --> node_253
    node_388 --> node_395
    node_468 --> node_474
    node_556 --> node_561
    node_8 --> node_467
    node_399 --> node_184
    node_131 --> node_240
    node_569 --> node_600
    node_223 --> node_4
    node_52 --> node_300
    node_569 --> node_557
    node_23 --> node_386
    node_42 --> node_48
    node_398 --> node_308
    node_218 --> node_162
    node_559 --> node_405
    node_179 --> node_405
    node_134 --> node_260
    node_131 --> node_119
    node_489 --> node_19
    node_297 --> node_176
    node_387 --> node_340
    node_18 --> node_23
    node_398 --> node_276
    node_376 --> node_347
    node_134 --> node_205
    node_513 --> node_428
    node_374 --> node_161
    node_4 --> node_123
    node_142 --> node_141
    node_538 --> node_548
    node_48 --> node_295
    node_382 --> node_390
    node_18 --> node_350
    node_4 --> node_162
    node_40 --> node_215
    node_40 --> node_136
    node_391 --> node_142
    node_90 --> node_72
    node_569 --> node_654
    node_45 --> node_475
    node_376 --> node_348
    node_28 --> node_568
    node_142 --> node_182
    node_366 --> node_142
    node_580 --> node_627
    node_6 --> node_295
    node_4 --> node_200
    node_134 --> node_338
    node_489 --> node_305
    node_505 --> node_663
    node_45 --> node_288
    node_349 --> node_438
    node_418 --> node_33
    node_134 --> node_238
    node_349 --> node_113
    node_176 --> node_298
    node_300 --> node_299
    node_495 --> node_316
    node_238 --> node_233
    node_341 --> node_569
    node_491 --> node_254
    node_52 --> node_199
    node_398 --> node_195
    node_500 --> node_312
    node_615 --> node_138
    node_505 --> node_26
    node_40 --> node_624
    node_131 --> node_283
    node_40 --> node_69
    node_18 --> node_256
    node_40 --> node_546
    node_530 --> node_531
    node_100 --> node_165
    node_184 --> node_664
    node_297 --> node_295
    node_418 --> node_535
    node_482 --> node_656
    node_45 --> node_349
    node_448 --> node_447
    node_40 --> node_439
    node_390 --> node_165
    node_139 --> node_295
    node_599 --> node_600
    node_134 --> node_131
    node_10 --> node_448
    node_610 --> node_556
    node_238 --> node_134
    node_4 --> node_337
    node_8 --> node_530
    node_100 --> node_169
    node_43 --> node_295
    node_335 --> node_334
    node_366 --> node_169
    node_550 --> node_541
    node_569 --> node_312
    node_376 --> node_344
    node_418 --> node_2
    node_390 --> node_169
    node_52 --> node_208
    node_61 --> node_211
    node_395 --> node_352
    node_505 --> node_363
    node_201 --> node_104
    node_615 --> node_569
    node_387 --> node_343
    node_366 --> node_151
    node_131 --> node_233
    node_418 --> node_34
    node_169 --> node_275
    node_398 --> node_324
    node_134 --> node_240
    node_285 --> node_624
    node_569 --> node_320
    node_18 --> node_485
    node_48 --> node_136
    node_349 --> node_176
    node_569 --> node_171
    node_397 --> node_158
    node_374 --> node_162
    node_388 --> node_397
    node_18 --> node_559
    node_274 --> node_164
    node_238 --> node_219
    node_134 --> node_119
    node_4 --> node_273
    node_40 --> node_198
    node_434 --> node_432
    node_52 --> node_284
    node_131 --> node_134
    node_4 --> node_138
    node_418 --> node_441
    node_194 --> node_193
    node_541 --> node_549
    node_52 --> node_124
    node_142 --> node_332
    node_387 --> node_289
    node_17 --> node_648
    node_40 --> node_378
    node_52 --> node_253
    node_4 --> node_291
    node_208 --> node_212
    node_364 --> node_107
    node_376 --> node_337
    node_72 --> node_295
    node_4 --> node_170
    node_396 --> node_149
    node_8 --> node_538
    node_30 --> node_365
    node_297 --> node_577
    node_42 --> node_60
    node_400 --> node_161
    node_4 --> node_278
    node_106 --> node_113
    node_366 --> node_221
    node_366 --> node_149
    node_431 --> node_428
    node_636 --> node_317
    node_455 --> node_208
    node_40 --> node_160
    node_198 --> node_197
    node_18 --> node_331
    node_418 --> node_437
    node_513 --> node_27
    node_40 --> node_365
    node_385 --> node_269
    node_479 --> node_72
    node_565 --> node_658
    node_208 --> node_206
    node_139 --> node_136
    node_18 --> node_448
    node_418 --> node_467
    node_458 --> node_440
    node_505 --> node_388
    node_569 --> node_637
    node_388 --> node_391
    node_40 --> node_428
    node_40 --> node_84
    node_40 --> node_411
    node_18 --> node_265
    node_398 --> node_305
    node_134 --> node_283
    node_238 --> node_336
    node_157 --> node_154
    node_556 --> node_583
    node_40 --> node_118
    node_569 --> node_659
    node_398 --> node_304
    node_477 --> node_33
    node_427 --> node_381
    node_565 --> node_317
    node_295 --> node_648
    node_569 --> node_644
    node_69 --> node_74
    node_387 --> node_348
    node_52 --> node_246
    node_481 --> node_275
    node_4 --> node_142
    node_40 --> node_632
    node_394 --> node_209
    node_382 --> node_396
    node_40 --> node_71
    node_300 --> node_581
    node_400 --> node_164
    node_45 --> node_213
    node_485 --> node_379
    node_40 --> node_491
    node_67 --> node_176
    node_356 --> node_138
    node_245 --> node_244
    node_171 --> node_582
    node_48 --> node_414
    node_52 --> node_206
    node_218 --> node_165
    node_388 --> node_394
    node_18 --> node_232
    node_134 --> node_233
    node_489 --> node_479
    node_52 --> node_116
    node_5 --> node_4
    node_580 --> node_307
    node_366 --> node_293
    node_358 --> node_158
    node_374 --> node_158
    node_597 --> node_605
    node_490 --> node_631
    node_52 --> node_57
    node_131 --> node_336
    node_387 --> node_177
    node_569 --> node_311
    node_455 --> node_164
    node_218 --> node_169
    node_484 --> node_311
    node_349 --> node_618
    node_389 --> node_267
    node_569 --> node_627
    node_4 --> node_181
    node_527 --> node_593
    node_398 --> node_325
    node_106 --> node_115
    node_18 --> node_174
    node_52 --> node_276
    node_73 --> node_569
    node_40 --> node_556
    node_56 --> node_425
    node_66 --> node_14
    node_356 --> node_569
    node_411 --> node_412
    node_366 --> node_267
    node_18 --> node_264
    node_101 --> node_666
    node_418 --> node_25
    node_8 --> node_663
    node_455 --> node_212
    node_32 --> node_34
    node_546 --> node_548
    node_274 --> node_166
    node_4 --> node_175
    node_18 --> node_30
    node_40 --> node_21
    node_418 --> node_101
    node_36 --> node_176
    node_4 --> node_169
    node_4 --> node_257
    node_28 --> node_79
    node_40 --> node_227
    node_418 --> node_32
    node_582 --> node_78
    node_8 --> node_81
    node_256 --> node_255
    node_140 --> node_108
    node_17 --> node_320
    node_366 --> node_157
    node_454 --> node_157
    node_500 --> node_642
    node_366 --> node_196
    node_663 --> node_664
    node_10 --> node_408
    node_404 --> node_248
    node_4 --> node_151
    node_538 --> node_549
    node_385 --> node_268
    node_4 --> node_67
    node_432 --> node_400
    node_40 --> node_251
    node_455 --> node_206
    node_52 --> node_273
    node_426 --> node_532
    node_67 --> node_295
    node_81 --> node_82
    node_176 --> node_577
    node_8 --> node_456
    node_238 --> node_288
    node_508 --> node_325
    node_42 --> node_43
    node_18 --> node_258
    node_40 --> node_77
    node_366 --> node_222
    node_52 --> node_441
    node_565 --> node_305
    node_48 --> node_71
    node_569 --> node_642
    node_40 --> node_436
    node_612 --> node_295
    node_40 --> node_53
    node_407 --> node_624
    node_40 --> node_327
    node_52 --> node_195
    node_505 --> node_42
    node_565 --> node_304
    node_18 --> node_220
    node_366 --> node_225
    node_194 --> node_187
    node_18 --> node_381
    node_418 --> node_16
    node_580 --> node_328
    node_372 --> node_338
    node_8 --> node_666
    node_349 --> node_624
    node_538 --> node_550
    node_238 --> node_349
    node_565 --> node_322
    node_17 --> node_581
    node_45 --> node_265
    node_40 --> node_163
    node_18 --> node_332
    node_52 --> node_569
    node_398 --> node_156
    node_366 --> node_153
    node_454 --> node_153
    node_387 --> node_337
    node_584 --> node_589
    node_399 --> node_186
    node_399 --> node_194
    node_40 --> node_235
    node_4 --> node_149
    node_52 --> node_437
```

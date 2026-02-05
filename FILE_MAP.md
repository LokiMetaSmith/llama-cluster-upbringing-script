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
| `.husky/pre-push` | 🔴 Orphan | File: pre-push |
| `.markdownlint.json` | 🟢 Referenced | File: .markdownlint.json |
| `.opencode/README.md` | 🟢 Referenced | OpenCode Configuration |
| `.opencode/opencode.json` | 🟢 Referenced | File: opencode.json |
| `.yamllint` | 🟢 Referenced | File: .yamllint |
| `LICENSE` | 🟢 Referenced | File: LICENSE |
| `README.md` | 🟢 Referenced | Distributed Conversational AI Pipeline for Legacy CPU Clusters |
| `TODO.md` | 🟢 Referenced | TODO |
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
| `ansible/roles/docker_registry/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/docker_registry/templates/docker-registry.nomad.j2` | 🟢 Referenced | File: docker-registry.nomad.j2 |
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
| `ansible/roles/librarian/handlers/main.yml` | 🔵 Entry Point | File: main.yml |
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
| `ansible/roles/minikeyvalue/files/Dockerfile` | 🟢 Referenced | File: Dockerfile |
| `ansible/roles/minikeyvalue/files/src/lib.go` | 🟢 Referenced | File: lib.go |
| `ansible/roles/minikeyvalue/files/src/lib_test.go` | 🟢 Referenced | File: lib_test.go |
| `ansible/roles/minikeyvalue/files/src/main.go` | 🟢 Referenced | File: main.go |
| `ansible/roles/minikeyvalue/files/src/rebalance.go` | 🟢 Referenced | File: rebalance.go |
| `ansible/roles/minikeyvalue/files/src/rebuild.go` | 🟢 Referenced | File: rebuild.go |
| `ansible/roles/minikeyvalue/files/src/s3api.go` | 🟢 Referenced | File: s3api.go |
| `ansible/roles/minikeyvalue/files/src/server.go` | 🟢 Referenced | File: server.go |
| `ansible/roles/minikeyvalue/files/start_master.py` | 🟢 Referenced | usr/bin/env python3 |
| `ansible/roles/minikeyvalue/files/volume` | 🟢 Referenced | bin/bash -e |
| `ansible/roles/minikeyvalue/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/minikeyvalue/templates/mkv.nomad.j2` | 🟢 Referenced | File: mkv.nomad.j2 |
| `ansible/roles/miniray/files/Dockerfile` | 🟢 Referenced | File: Dockerfile |
| `ansible/roles/miniray/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/miniray/templates/miniray.nomad.j2` | 🟢 Referenced | File: miniray.nomad.j2 |
| `ansible/roles/moe_gateway/files/gateway.py` | 🟢 Referenced | File: gateway.py |
| `ansible/roles/moe_gateway/files/static/index.html` | 🟢 Referenced | File: index.html |
| `ansible/roles/moe_gateway/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/moe_gateway/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/moe_gateway/templates/moe-gateway.nomad.j2` | 🟢 Referenced | File: moe-gateway.nomad.j2 |
| `ansible/roles/moltbot/files/Dockerfile` | 🟢 Referenced | Install system dependencies (curl for integration) |
| `ansible/roles/moltbot/files/pipecat_skill.md` | 🟢 Referenced | Pipecat Integration Skill |
| `ansible/roles/moltbot/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/moltbot/templates/moltbot.nomad.j2` | 🟢 Referenced | File: moltbot.nomad.j2 |
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
| `ansible/roles/nfs/handlers/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nfs/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/nfs/templates/exports.j2` | 🟢 Referenced | File: exports.j2 |
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
| `ansible/roles/paddler_agent/README.md` | 🟢 Referenced | Ansible Role: paddler_agent |
| `ansible/roles/paddler_agent/defaults/main.yaml` | 🟢 Referenced | Defaults for the paddler_agent role |
| `ansible/roles/paddler_agent/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/paddler_agent/templates/paddler-agent.service.j2` | 🟢 Referenced | Assuming llama.cpp service is named llama-cpp.service or similar |
| `ansible/roles/paddler_balancer/README.md` | 🟢 Referenced | Ansible Role: paddler_balancer |
| `ansible/roles/paddler_balancer/defaults/main.yaml` | 🟢 Referenced | Defaults for the paddler_balancer role |
| `ansible/roles/paddler_balancer/tasks/main.yaml` | 🟢 Referenced | File: main.yaml |
| `ansible/roles/paddler_balancer/templates/paddler-balancer.service.j2` | 🟢 Referenced | File: paddler-balancer.service.j2 |
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
| `docs/GASTOWN_TODO.md` | 📄 Documentation/Asset | Gas Town Integration Todo |
| `docs/GEMINI.md` | 🟢 Referenced | GEMINI.md |
| `docs/IPV6_AUDIT.md` | 📄 Documentation/Asset | IPv6 Audit Report |
| `docs/MCP_SERVER_SETUP.md` | 🟢 Referenced | Building an MCP Server with Service Discovery |
| `docs/MEMORIES.md` | 🟢 Referenced | Agent Memories |
| `docs/NETWORK.md` | 🟢 Referenced | Network Architecture |
| `docs/NIXOS_PXE_BOOT_SETUP.md` | 🟢 Referenced | NixOS-based PXE Boot Server Setup |
| `docs/PERFORMANCE_OPTIMIZATION.md` | 📄 Documentation/Asset | Performance & I/O Optimization |
| `docs/PROJECT_SUMMARY.md` | 🟢 Referenced | Project Summary: Architecting a Responsive, Distributed Conversational AI Pipeline |
| `docs/PXE_BOOT_SETUP.md` | 🟢 Referenced | iPXE Boot Server Setup for Automated Debian Installation |
| `docs/README.md` | 🟢 Referenced | Project Documentation |
| `docs/REFACTOR_PROPOSAL_hybrid_architecture.md` | 🟢 Referenced | Refactoring Proposal: Hybrid / Cluster-Native Architecture |
| `docs/REMOTE_WORKFLOW.md` | 🟢 Referenced | Improving Your Remote Workflow with Mosh and Tmux |
| `docs/SCALING_TODO.md` | 📄 Documentation/Asset | Scaling Long-Running Autonomous Coding - Implementation Scope |
| `docs/SECURITY_AUDIT.md` | 📄 Documentation/Asset | Security Audit Log |
| `docs/TODO_Hybrid_Architecture.md` | 🟢 Referenced | Hybrid Architecture Implementation To-Do List |
| `docs/TOOL_EVALUATION.md` | 🟢 Referenced | Tool Evaluation and Strategic Direction |
| `docs/TROUBLESHOOTING.md` | 🟢 Referenced | Troubleshooting Guide |
| `docs/VLLM_PROJECT_EVALUATION.md` | 🟢 Referenced | vLLM Project Evaluation |
| `docs/YAML_FILES_REPORT.md` | 📄 Documentation/Asset | Report on YAML Files in Root Directory |
| `docs/heretic_evaluation.md` | 🟢 Referenced | Heretic Repository Evaluation |
| `examples/README.md` | 🟢 Referenced | Examples |
| `examples/chat-persistent.sh` | 🟢 Referenced | bin/bash |
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
| `initial_state.png` | 🔴 Orphan | File: initial_state.png |
| `inventory.yaml` | 🟢 Referenced | This inventory is dynamically generated by update_inventory.sh |
| `local_inventory.ini` | 🟢 Referenced | File: local_inventory.ini |
| `package.json` | 🟢 Referenced | File: package.json |
| `paused_state.png` | 🔴 Orphan | File: paused_state.png |
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
| `pipecatapp/integrations/__init__.py` | 🟢 Referenced | This package contains integration modules for external services (e.g., OpenClaw). |
| `pipecatapp/integrations/openclaw.py` | 🟢 Referenced | File: openclaw.py |
| `pipecatapp/janitor_agent.py` | 🟢 Referenced | File: janitor_agent.py |
| `pipecatapp/judge_agent.py` | 🟢 Referenced | File: judge_agent.py |
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
| `pipecatapp/security.py` | 🟢 Referenced | File: security.py |
| `pipecatapp/start_archivist.sh` | 🟢 Referenced | bin/bash |
| `pipecatapp/static/cluster.html` | 🟢 Referenced | File: cluster.html |
| `pipecatapp/static/cluster_viz.html` | 🟢 Referenced | A-Frame |
| `pipecatapp/static/css/litegraph.css` | 🟢 Referenced | File: litegraph.css |
| `pipecatapp/static/css/styles.css` | 🟢 Referenced | sidebar { |
| `pipecatapp/static/index.html` | 🟢 Referenced | File: index.html |
| `pipecatapp/static/js/editor.js` | 🟢 Referenced | Editor logic using LiteGraph.js |
| `pipecatapp/static/js/litegraph.js` | 🟢 Referenced | packer version |
| `pipecatapp/static/js/workflow.js` | 🟢 Referenced | File: workflow.js |
| `pipecatapp/static/monitor.html` | 🟢 Referenced | File: monitor.html |
| `pipecatapp/static/terminal.js` | 🟢 Referenced | File: terminal.js |
| `pipecatapp/static/vr_index.html` | 🟢 Referenced | A-Frame |
| `pipecatapp/static/workflow.html` | 🟢 Referenced | File: workflow.html |
| `pipecatapp/task_supervisor.py` | 🟢 Referenced | File: task_supervisor.py |
| `pipecatapp/technician_agent.py` | 🟢 Referenced | File: technician_agent.py |
| `pipecatapp/test_memory.py` | 🟢 Referenced | File: test_memory.py |
| `pipecatapp/test_moondream_detector.py` | 🟢 Referenced | File: test_moondream_detector.py |
| `pipecatapp/test_pmm_memory.py` | 🧪 Test | File: test_pmm_memory.py |
| `pipecatapp/test_server.py` | 🟢 Referenced | File: test_server.py |
| `pipecatapp/tests/test_audio_streamer.py` | 🧪 Test | File: test_audio_streamer.py |
| `pipecatapp/tests/test_browser_tool_security.py` | 🧪 Test | File: test_browser_tool_security.py |
| `pipecatapp/tests/test_container_registry_tool.py` | 🧪 Test | File: test_container_registry_tool.py |
| `pipecatapp/tests/test_git_tool_security.py` | 🧪 Test | File: test_git_tool_security.py |
| `pipecatapp/tests/test_metrics_cache.py` | 🧪 Test | File: test_metrics_cache.py |
| `pipecatapp/tests/test_net_utils.py` | 🧪 Test | File: test_net_utils.py |
| `pipecatapp/tests/test_openclaw.py` | 🧪 Test | File: test_openclaw.py |
| `pipecatapp/tests/test_piper_async.py` | 🧪 Test | File: test_piper_async.py |
| `pipecatapp/tests/test_proxy_security.py` | 🧪 Test | File: test_proxy_security.py |
| `pipecatapp/tests/test_rag_tool.py` | 🟢 Referenced | File: test_rag_tool.py |
| `pipecatapp/tests/test_rate_limiter.py` | 🧪 Test | File: test_rate_limiter.py |
| `pipecatapp/tests/test_security.py` | 🟢 Referenced | Ensure pipecatapp is in path |
| `pipecatapp/tests/test_stt_optimization.py` | 🧪 Test | File: test_stt_optimization.py |
| `pipecatapp/tests/test_uilogger_redaction.py` | 🟢 Referenced | File: test_uilogger_redaction.py |
| `pipecatapp/tests/test_web_server_unit.py` | 🧪 Test | File: test_web_server_unit.py |
| `pipecatapp/tests/test_websocket_security.py` | 🧪 Test | Mock out heavy dependencies that cause timeouts during import |
| `pipecatapp/tests/test_xss_prevention.py` | 🧪 Test | File: test_xss_prevention.py |
| `pipecatapp/tests/test_yolo_optimization.py` | 🧪 Test | File: test_yolo_optimization.py |
| `pipecatapp/tests/workflow/test_history.py` | 🧪 Test | File: test_history.py |
| `pipecatapp/tests/workflow/test_serialization_perf.py` | 🧪 Test | File: test_serialization_perf.py |
| `pipecatapp/tool_server.py` | 🟢 Referenced | File: tool_server.py |
| `pipecatapp/tools/__init__.py` | 🟢 Referenced | File: __init__.py |
| `pipecatapp/tools/ansible_tool.py` | 🟢 Referenced | File: ansible_tool.py |
| `pipecatapp/tools/archivist_tool.py` | 🟢 Referenced | File: archivist_tool.py |
| `pipecatapp/tools/claude_clone_tool.py` | 🟢 Referenced | File: claude_clone_tool.py |
| `pipecatapp/tools/code_runner_tool.py` | 🟢 Referenced | File: code_runner_tool.py |
| `pipecatapp/tools/container_registry_tool.py` | 🟢 Referenced | File: container_registry_tool.py |
| `pipecatapp/tools/council_tool.py` | 🟢 Referenced | File: council_tool.py |
| `pipecatapp/tools/dependency_scanner_tool.py` | 🟢 Referenced | File: dependency_scanner_tool.py |
| `pipecatapp/tools/desktop_control_tool.py` | 🟢 Referenced | File: desktop_control_tool.py |
| `pipecatapp/tools/experiment_tool.py` | 🟢 Referenced | File: experiment_tool.py |
| `pipecatapp/tools/file_editor_tool.py` | 🟢 Referenced | File: file_editor_tool.py |
| `pipecatapp/tools/final_answer_tool.py` | 🟢 Referenced | File: final_answer_tool.py |
| `pipecatapp/tools/gemini_cli.py` | 🟢 Referenced | File: gemini_cli.py |
| `pipecatapp/tools/get_nomad_job.py` | 🟢 Referenced | File: get_nomad_job.py |
| `pipecatapp/tools/git_tool.py` | 🟢 Referenced | File: git_tool.py |
| `pipecatapp/tools/ha_tool.py` | 🟢 Referenced | File: ha_tool.py |
| `pipecatapp/tools/llxprt_code_tool.py` | 🟢 Referenced | File: llxprt_code_tool.py |
| `pipecatapp/tools/mcp_tool.py` | 🟢 Referenced | File: mcp_tool.py |
| `pipecatapp/tools/miniray_tool.py` | 🟢 Referenced | File: miniray_tool.py |
| `pipecatapp/tools/mkv_tool.py` | 🟢 Referenced | File: mkv_tool.py |
| `pipecatapp/tools/open_workers_tool.py` | 🟢 Referenced | File: open_workers_tool.py |
| `pipecatapp/tools/openclaw_tool.py` | 🟢 Referenced | File: openclaw_tool.py |
| `pipecatapp/tools/opencode_tool.py` | 🟢 Referenced | File: opencode_tool.py |
| `pipecatapp/tools/orchestrator_tool.py` | 🟢 Referenced | File: orchestrator_tool.py |
| `pipecatapp/tools/planner_tool.py` | 🟢 Referenced | File: planner_tool.py |
| `pipecatapp/tools/power_tool.py` | 🟢 Referenced | File: power_tool.py |
| `pipecatapp/tools/project_mapper_tool.py` | 🟢 Referenced | File: project_mapper_tool.py |
| `pipecatapp/tools/prompt_improver_tool.py` | 🟢 Referenced | File: prompt_improver_tool.py |
| `pipecatapp/tools/rag_tool.py` | 🟢 Referenced | File: rag_tool.py |
| `pipecatapp/tools/remote_tool_proxy.py` | 🟢 Referenced | File: remote_tool_proxy.py |
| `pipecatapp/tools/sandbox.ts` | 🟢 Referenced | sandbox.ts |
| `pipecatapp/tools/search_tool.py` | 🟢 Referenced | File: search_tool.py |
| `pipecatapp/tools/shell_tool.py` | 🟢 Referenced | File: shell_tool.py |
| `pipecatapp/tools/smol_agent_tool.py` | 🟢 Referenced | File: smol_agent_tool.py |
| `pipecatapp/tools/spec_loader_tool.py` | 🟢 Referenced | File: spec_loader_tool.py |
| `pipecatapp/tools/ssh_tool.py` | 🟢 Referenced | File: ssh_tool.py |
| `pipecatapp/tools/submit_solution_tool.py` | 🟢 Referenced | File: submit_solution_tool.py |
| `pipecatapp/tools/summarizer_tool.py` | 🟢 Referenced | File: summarizer_tool.py |
| `pipecatapp/tools/swarm_tool.py` | 🟢 Referenced | File: swarm_tool.py |
| `pipecatapp/tools/tap_service.py` | 🟢 Referenced | File: tap_service.py |
| `pipecatapp/tools/term_everything_tool.py` | 🟢 Referenced | File: term_everything_tool.py |
| `pipecatapp/tools/test_code_runner_tool.py` | 🟢 Referenced | File: test_code_runner_tool.py |
| `pipecatapp/tools/test_git_tool.py` | 🟢 Referenced | File: test_git_tool.py |
| `pipecatapp/tools/test_ssh_tool.py` | 🟢 Referenced | File: test_ssh_tool.py |
| `pipecatapp/tools/vr_tool.py` | 🟢 Referenced | File: vr_tool.py |
| `pipecatapp/tools/web_browser_tool.py` | 🟢 Referenced | File: web_browser_tool.py |
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
| `playbooks/deploy_moltbot.yaml` | 🔴 Orphan | File: deploy_moltbot.yaml |
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
| `playbooks/services/distributed_compute.yaml` | 🟢 Referenced | Default variables can be overridden in inventory/group_vars |
| `playbooks/services/docker.yaml` | 🟢 Referenced | File: docker.yaml |
| `playbooks/services/final_verification.yaml` | 🟢 Referenced | File: final_verification.yaml |
| `playbooks/services/model_services.yaml` | 🟢 Referenced | File: model_services.yaml |
| `playbooks/services/monitoring.yaml` | 🟢 Referenced | File: monitoring.yaml |
| `playbooks/services/nomad.yaml` | 🟢 Referenced | File: nomad.yaml |
| `playbooks/services/nomad_client.yaml` | 🟢 Referenced | File: nomad_client.yaml |
| `playbooks/services/registry.yaml` | 🟢 Referenced | File: registry.yaml |
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
| `pytest.ini` | 🟢 Referenced | File: pytest.ini |
| `reflection/README.md` | 🟢 Referenced | Reflection |
| `reflection/adaptation_manager.py` | 🟢 Referenced | File: adaptation_manager.py |
| `reflection/create_reflection.py` | 🟢 Referenced | File: create_reflection.py |
| `reflection/reflect.py` | 🟢 Referenced | File: reflect.py |
| `requirements-dev.txt` | 🟢 Referenced | File: requirements-dev.txt |
| `scripts/README.md` | 🟢 Referenced | `scripts/` Directory Overview |
| `scripts/agentic_workflow.sh` | 🟢 Referenced | --- Configuration --- |
| `scripts/analyze_nomad_allocs.py` | 🟢 Referenced | usr/bin/env python3 |
| `scripts/ansible_diff.sh` | 🟢 Referenced | A script to compare Ansible playbook runs to detect changes over time. It establishes a baseline fro |
| `scripts/check_all_playbooks.sh` | 🟢 Referenced | --- Flexible Ansible Playbook Checker  This script recursively finds all .yaml and .yml files, filte |
| `scripts/check_deps.py` | 🟢 Referenced | Write the requirements to a temp file |
| `scripts/ci_ansible_check.sh` | 🟢 Referenced | A CI/CD-friendly script to check for unintended changes in Ansible playbooks.  - It compares the pla |
| `scripts/cleanup.sh` | 🟢 Referenced | Cleanup script to free up disk space on the host machine. This script aggressively cleans Docker re |
| `scripts/compare_exo_llama.py` | 🔵 Entry Point | File: compare_exo_llama.py |
| `scripts/create_cynic_model.sh` | 🔵 Entry Point | bin/bash |
| `scripts/create_todo_issues.sh` | 🟢 Referenced | bin/bash |
| `scripts/debug/README.md` | 🟢 Referenced | Debug Scripts |
| `scripts/debug/test_mqtt_connection.py` | 🟢 Referenced | File: test_mqtt_connection.py |
| `scripts/debug_expert.sh` | 🟢 Referenced | bin/bash |
| `scripts/debug_mesh.sh` | 🟢 Referenced | bin/bash |
| `scripts/fix_markdown.sh` | 🟢 Referenced | Automatic Markdown Linter Fixer  This script uses markdownlint-cli's --fix option to automatically |
| `scripts/fix_verification_failures.sh` | 🟢 Referenced | Scripts to help remediate failures reported by verify_components.py |
| `scripts/fix_yaml.sh` | 🟢 Referenced | Automatic YAML Linter Fixer  This script automatically fixes common, repetitive style issues report |
| `scripts/generate_file_map.py` | 🔵 Entry Point | usr/bin/env python3 |
| `scripts/generate_issue_script.py` | 🟢 Referenced | File: generate_issue_script.py |
| `scripts/heal_cluster.sh` | 🟢 Referenced | Wrapper script to run the cluster healing playbook. This ensures core infrastructure (LlamaRPC, Pip |
| `scripts/healer.py` | 🟢 Referenced | File: healer.py |
| `scripts/lint.sh` | 🟢 Referenced | Unified Linting Script  This script runs a series of linters to ensure code quality and consistency |
| `scripts/lint_exclude.txt` | 🟢 Referenced | Exclude problematic files from the linting process. |
| `scripts/memory_audit.py` | 🟢 Referenced | File: memory_audit.py |
| `scripts/profile_resources.sh` | 🟢 Referenced | Profile resources usage and alignment of AI experts and models. |
| `scripts/provisioning.py` | 🟢 Referenced | Provisioning Script for Hybrid Architecture. |
| `scripts/prune_consul_services.py` | 🟢 Referenced | Prune Stale Critical Services from Consul |
| `scripts/run_quibbler.sh` | 🟢 Referenced | A wrapper script to run quibbler for code review. Check for required arguments |
| `scripts/run_tests.sh` | 🟢 Referenced | usr/bin/env bash |
| `scripts/start_services.sh` | 🟢 Referenced | This script is a legacy utility for manually starting services. ⚠️  DEPRECATED: Please use Ansible t |
| `scripts/supervisor.py` | 🟢 Referenced | File: supervisor.py |
| `scripts/test_playbooks_dry_run.sh` | 🟢 Referenced | bin/bash |
| `scripts/test_playbooks_live_run.sh` | 🟢 Referenced | bin/bash |
| `scripts/troubleshoot.py` | 🟢 Referenced | usr/bin/env python3 |
| `scripts/uninstall.sh` | 🟢 Referenced | This script uninstalls all software and reverts all changes made by the playbook. |
| `scripts/verify_consul_attributes.sh` | 🔵 Entry Point | bin/bash |
| `test_dlq.db-shm` | 🧪 Test | File: test_dlq.db-shm |
| `test_dlq.db-wal` | 🧪 Test | File: test_dlq.db-wal |
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
| `tests/scripts/test_duplicate_role_execution.sh` | 🧪 Test | Test to verify that the bootstrap_agent role is not run twice using static analysis.  Move to the p |
| `tests/scripts/test_paddler.sh` | 🧪 Test | test_paddler.sh  This script performs basic tests to verify that Paddler (agent and balancer) is fun |
| `tests/scripts/test_piper.sh` | 🧪 Test | File: test_piper.sh |
| `tests/scripts/test_run.sh` | 🧪 Test | Start a new chat |
| `tests/scripts/verify_components.py` | 🟢 Referenced | usr/bin/env python3 |
| `tests/test.wav` | 🟢 Referenced | File: test.wav |
| `tests/test_agent_patterns.py` | 🧪 Test | File: test_agent_patterns.py |
| `tests/test_emperor_node.py` | 🧪 Test | File: test_emperor_node.py |
| `tests/test_event_bus.py` | 🧪 Test | File: test_event_bus.py |
| `tests/test_experiment_tool.py` | 🧪 Test | File: test_experiment_tool.py |
| `tests/test_gastown_judge.py` | 🧪 Test | File: test_gastown_judge.py |
| `tests/test_gastown_memory.py` | 🧪 Test | File: test_gastown_memory.py |
| `tests/test_gastown_stats.py` | 🧪 Test | File: test_gastown_stats.py |
| `tests/test_imports.py` | 🧪 Test | Add files dir to path |
| `tests/test_manager_flow.py` | 🧪 Test | File: test_manager_flow.py |
| `tests/test_spec_loader.py` | 🧪 Test | File: test_spec_loader.py |
| `tests/test_ssrf_validation.py` | 🧪 Test | Add repo root to path so we can import pipecatapp |
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
| `tests/unit/test_security.py` | 🟢 Referenced | Ensure pipecatapp is in path |
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
| `tests/unit/test_web_server_sync.py` | 🧪 Test | File: test_web_server_sync.py |
| `tests/unit/test_workflow.py` | 🧪 Test | File: test_workflow.py |
| `tests/unit/test_world_model_service.py` | 🧪 Test | File: test_world_model_service.py |
| `tests/verify_config_load.py` | 🟢 Referenced | File: verify_config_load.py |
| `tests/verify_dlq.py` | 🧪 Test | File: verify_dlq.py |
| `workflows/default_agent_loop.yaml` | 🟢 Referenced | File: default_agent_loop.yaml |

## Dependency Diagram

```mermaid
graph LR
    subgraph dir_Root [Root]
        direction TB
        node_11[".coverage"]
        node_23[".djlint.toml"]
        node_2[".gitattributes"]
        node_10[".gitignore"]
        node_4[".markdownlint.json"]
        node_18[".yamllint"]
        node_19["LICENSE"]
        node_7["README.md"]
        node_6["TODO.md"]
        node_5["aid_e_log.txt"]
        node_20["ansible.cfg"]
        node_13["bootstrap.sh"]
        node_3["hostfile"]
        node_1["initial_state.png"]
        node_22["inventory.yaml"]
        node_21["local_inventory.ini"]
        node_17["package.json"]
        node_12["paused_state.png"]
        node_14["playbook.yaml"]
        node_15["pytest.ini"]
        node_9["requirements-dev.txt"]
        node_0["test_dlq.db-shm"]
        node_16["test_dlq.db-wal"]
        node_8["test_playbook.yml"]
    end
    subgraph dir__github [.github]
        direction TB
        node_52["AGENTIC_README.md"]
    end
    subgraph dir__github_workflows [.github/workflows]
        direction TB
        node_56["auto-merge.yml"]
        node_57["ci.yml"]
        node_53["create-issues-from-files.yml"]
        node_55["jules-queue.yml"]
        node_54["remote-verify.yml"]
    end
    subgraph dir__husky [.husky]
        direction TB
        node_439["pre-push"]
    end
    subgraph dir__opencode [.opencode]
        direction TB
        node_586["README.md"]
        node_587["opencode.json"]
    end
    subgraph dir_ansible [ansible]
        direction TB
        node_90["README.md"]
        node_91["lint_nomad.yaml"]
        node_92["run_download_models.yaml"]
    end
    subgraph dir_ansible_filter_plugins [ansible/filter_plugins]
        direction TB
        node_107["README.md"]
        node_108["safe_flatten.py"]
    end
    subgraph dir_ansible_jobs [ansible/jobs]
        direction TB
        node_97["README.md"]
        node_102["benchmark.nomad"]
        node_94["evolve-prompt.nomad.j2"]
        node_101["expert-debug.nomad"]
        node_98["expert.nomad.j2"]
        node_96["filebrowser.nomad.j2"]
        node_93["health-check.nomad.j2"]
        node_99["llamacpp-batch.nomad.j2"]
        node_95["llamacpp-rpc.nomad.j2"]
        node_106["model-benchmark.nomad.j2"]
        node_105["pipecatapp.nomad"]
        node_104["router.nomad.j2"]
        node_100["test-runner.nomad.j2"]
        node_103["vllm.nomad.j2"]
    end
    subgraph dir_ansible_roles [ansible/roles]
        direction TB
        node_109["README.md"]
    end
    subgraph dir_ansible_roles_benchmark_models_tasks [ansible/roles/benchmark_models/tasks]
        direction TB
        node_164["benchmark_loop.yaml"]
        node_163["main.yaml"]
    end
    subgraph dir_ansible_roles_benchmark_models_templates [ansible/roles/benchmark_models/templates]
        direction TB
        node_162["model-benchmark.nomad.j2"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_defaults [ansible/roles/bootstrap_agent/defaults]
        direction TB
        node_232["main.yaml"]
    end
    subgraph dir_ansible_roles_bootstrap_agent_tasks [ansible/roles/bootstrap_agent/tasks]
        direction TB
        node_233["deploy_llama_cpp_model.yaml"]
        node_234["main.yaml"]
    end
    subgraph dir_ansible_roles_claude_clone_tasks [ansible/roles/claude_clone/tasks]
        direction TB
        node_266["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tools_tasks [ansible/roles/common-tools/tasks]
        direction TB
        node_221["main.yaml"]
    end
    subgraph dir_ansible_roles_common_handlers [ansible/roles/common/handlers]
        direction TB
        node_151["main.yaml"]
    end
    subgraph dir_ansible_roles_common_tasks [ansible/roles/common/tasks]
        direction TB
        node_155["main.yaml"]
        node_156["network_repair.yaml"]
    end
    subgraph dir_ansible_roles_common_templates [ansible/roles/common/templates]
        direction TB
        node_154["cluster-ip-alias.service.j2"]
        node_153["hosts.j2"]
        node_152["update-ssh-authorized-keys.sh.j2"]
    end
    subgraph dir_ansible_roles_config_manager_tasks [ansible/roles/config_manager/tasks]
        direction TB
        node_258["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_defaults [ansible/roles/consul/defaults]
        direction TB
        node_166["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_handlers [ansible/roles/consul/handlers]
        direction TB
        node_165["main.yaml"]
    end
    subgraph dir_ansible_roles_consul_tasks [ansible/roles/consul/tasks]
        direction TB
        node_171["acl.yaml"]
        node_169["main.yaml"]
        node_170["tls.yaml"]
    end
    subgraph dir_ansible_roles_consul_templates [ansible/roles/consul/templates]
        direction TB
        node_168["consul.hcl.j2"]
        node_167["consul.service.j2"]
    end
    subgraph dir_ansible_roles_desktop_extras_tasks [ansible/roles/desktop_extras/tasks]
        direction TB
        node_115["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_handlers [ansible/roles/docker/handlers]
        direction TB
        node_222["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_molecule_default [ansible/roles/docker/molecule/default]
        direction TB
        node_225["converge.yml"]
        node_226["molecule.yml"]
        node_228["prepare.yml"]
        node_227["verify.yml"]
    end
    subgraph dir_ansible_roles_docker_tasks [ansible/roles/docker/tasks]
        direction TB
        node_224["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_templates [ansible/roles/docker/templates]
        direction TB
        node_223["daemon.json.j2"]
    end
    subgraph dir_ansible_roles_docker_registry_tasks [ansible/roles/docker_registry/tasks]
        direction TB
        node_130["main.yaml"]
    end
    subgraph dir_ansible_roles_docker_registry_templates [ansible/roles/docker_registry/templates]
        direction TB
        node_129["docker-registry.nomad.j2"]
    end
    subgraph dir_ansible_roles_download_models_files [ansible/roles/download_models/files]
        direction TB
        node_149["download_hf_repo.py"]
    end
    subgraph dir_ansible_roles_download_models_tasks [ansible/roles/download_models/tasks]
        direction TB
        node_150["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_defaults [ansible/roles/exo/defaults]
        direction TB
        node_267["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_files [ansible/roles/exo/files]
        direction TB
        node_268["Dockerfile"]
    end
    subgraph dir_ansible_roles_exo_tasks [ansible/roles/exo/tasks]
        direction TB
        node_270["main.yaml"]
    end
    subgraph dir_ansible_roles_exo_templates [ansible/roles/exo/templates]
        direction TB
        node_269["exo.nomad.j2"]
    end
    subgraph dir_ansible_roles_headscale_defaults [ansible/roles/headscale/defaults]
        direction TB
        node_289["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_handlers [ansible/roles/headscale/handlers]
        direction TB
        node_288["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_tasks [ansible/roles/headscale/tasks]
        direction TB
        node_292["main.yaml"]
    end
    subgraph dir_ansible_roles_headscale_templates [ansible/roles/headscale/templates]
        direction TB
        node_291["config.yaml.j2"]
        node_290["headscale.service.j2"]
    end
    subgraph dir_ansible_roles_heretic_tool_defaults [ansible/roles/heretic_tool/defaults]
        direction TB
        node_235["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_meta [ansible/roles/heretic_tool/meta]
        direction TB
        node_236["main.yaml"]
    end
    subgraph dir_ansible_roles_heretic_tool_tasks [ansible/roles/heretic_tool/tasks]
        direction TB
        node_237["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_meta [ansible/roles/home_assistant/meta]
        direction TB
        node_273["main.yaml"]
        node_272["main.yml"]
    end
    subgraph dir_ansible_roles_home_assistant_tasks [ansible/roles/home_assistant/tasks]
        direction TB
        node_276["main.yaml"]
    end
    subgraph dir_ansible_roles_home_assistant_templates [ansible/roles/home_assistant/templates]
        direction TB
        node_275["configuration.yaml.j2"]
        node_274["home_assistant.nomad.j2"]
    end
    subgraph dir_ansible_roles_kittentts_tasks [ansible/roles/kittentts/tasks]
        direction TB
        node_172["main.yaml"]
    end
    subgraph dir_ansible_roles_librarian_defaults [ansible/roles/librarian/defaults]
        direction TB
        node_120["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_handlers [ansible/roles/librarian/handlers]
        direction TB
        node_119["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_tasks [ansible/roles/librarian/tasks]
        direction TB
        node_124["main.yml"]
    end
    subgraph dir_ansible_roles_librarian_templates [ansible/roles/librarian/templates]
        direction TB
        node_121["librarian.service.j2"]
        node_123["librarian_agent.py.j2"]
        node_122["spacedrive.service.j2"]
    end
    subgraph dir_ansible_roles_llama_cpp_handlers [ansible/roles/llama_cpp/handlers]
        direction TB
        node_215["main.yaml"]
    end
    subgraph dir_ansible_roles_llama_cpp_molecule_default [ansible/roles/llama_cpp/molecule/default]
        direction TB
        node_218["converge.yml"]
        node_219["molecule.yml"]
        node_220["verify.yml"]
    end
    subgraph dir_ansible_roles_llama_cpp_tasks [ansible/roles/llama_cpp/tasks]
        direction TB
        node_216["main.yaml"]
        node_217["run_single_rpc_job.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_tasks [ansible/roles/llxprt_code/tasks]
        direction TB
        node_260["main.yaml"]
    end
    subgraph dir_ansible_roles_llxprt_code_templates [ansible/roles/llxprt_code/templates]
        direction TB
        node_259["llxprt-code.env.j2"]
    end
    subgraph dir_ansible_roles_magic_mirror_defaults [ansible/roles/magic_mirror/defaults]
        direction TB
        node_311["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_handlers [ansible/roles/magic_mirror/handlers]
        direction TB
        node_310["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_tasks [ansible/roles/magic_mirror/tasks]
        direction TB
        node_313["main.yaml"]
    end
    subgraph dir_ansible_roles_magic_mirror_templates [ansible/roles/magic_mirror/templates]
        direction TB
        node_312["magic_mirror.nomad.j2"]
    end
    subgraph dir_ansible_roles_mcp_server_defaults [ansible/roles/mcp_server/defaults]
        direction TB
        node_208["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_handlers [ansible/roles/mcp_server/handlers]
        direction TB
        node_207["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_tasks [ansible/roles/mcp_server/tasks]
        direction TB
        node_210["main.yaml"]
    end
    subgraph dir_ansible_roles_mcp_server_templates [ansible/roles/mcp_server/templates]
        direction TB
        node_209["mcp_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_graph_tasks [ansible/roles/memory_graph/tasks]
        direction TB
        node_257["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_graph_templates [ansible/roles/memory_graph/templates]
        direction TB
        node_256["memory-graph.nomad.j2"]
    end
    subgraph dir_ansible_roles_memory_service_files [ansible/roles/memory_service/files]
        direction TB
        node_188["app.py"]
        node_189["pmm_memory.py"]
    end
    subgraph dir_ansible_roles_memory_service_handlers [ansible/roles/memory_service/handlers]
        direction TB
        node_187["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_tasks [ansible/roles/memory_service/tasks]
        direction TB
        node_191["main.yaml"]
    end
    subgraph dir_ansible_roles_memory_service_templates [ansible/roles/memory_service/templates]
        direction TB
        node_190["memory_service.nomad.j2"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files [ansible/roles/minikeyvalue/files]
        direction TB
        node_133["Dockerfile"]
        node_132["start_master.py"]
        node_131["volume"]
    end
    subgraph dir_ansible_roles_minikeyvalue_files_src [ansible/roles/minikeyvalue/files/src]
        direction TB
        node_138["lib.go"]
        node_137["lib_test.go"]
        node_135["main.go"]
        node_134["rebalance.go"]
        node_140["rebuild.go"]
        node_136["s3api.go"]
        node_139["server.go"]
    end
    subgraph dir_ansible_roles_minikeyvalue_tasks [ansible/roles/minikeyvalue/tasks]
        direction TB
        node_142["main.yaml"]
    end
    subgraph dir_ansible_roles_minikeyvalue_templates [ansible/roles/minikeyvalue/templates]
        direction TB
        node_141["mkv.nomad.j2"]
    end
    subgraph dir_ansible_roles_miniray_files [ansible/roles/miniray/files]
        direction TB
        node_357["Dockerfile"]
    end
    subgraph dir_ansible_roles_miniray_tasks [ansible/roles/miniray/tasks]
        direction TB
        node_359["main.yaml"]
    end
    subgraph dir_ansible_roles_miniray_templates [ansible/roles/miniray/templates]
        direction TB
        node_358["miniray.nomad.j2"]
    end
    subgraph dir_ansible_roles_moe_gateway_files [ansible/roles/moe_gateway/files]
        direction TB
        node_183["gateway.py"]
    end
    subgraph dir_ansible_roles_moe_gateway_files_static [ansible/roles/moe_gateway/files/static]
        direction TB
        node_184["index.html"]
    end
    subgraph dir_ansible_roles_moe_gateway_handlers [ansible/roles/moe_gateway/handlers]
        direction TB
        node_182["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_tasks [ansible/roles/moe_gateway/tasks]
        direction TB
        node_186["main.yaml"]
    end
    subgraph dir_ansible_roles_moe_gateway_templates [ansible/roles/moe_gateway/templates]
        direction TB
        node_185["moe-gateway.nomad.j2"]
    end
    subgraph dir_ansible_roles_moltbot_files [ansible/roles/moltbot/files]
        direction TB
        node_159["Dockerfile"]
        node_158["pipecat_skill.md"]
    end
    subgraph dir_ansible_roles_moltbot_tasks [ansible/roles/moltbot/tasks]
        direction TB
        node_161["main.yaml"]
    end
    subgraph dir_ansible_roles_moltbot_templates [ansible/roles/moltbot/templates]
        direction TB
        node_160["moltbot.nomad.j2"]
    end
    subgraph dir_ansible_roles_monitoring_defaults [ansible/roles/monitoring/defaults]
        direction TB
        node_196["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_files [ansible/roles/monitoring/files]
        direction TB
        node_197["llm_dashboard.json"]
    end
    subgraph dir_ansible_roles_monitoring_tasks [ansible/roles/monitoring/tasks]
        direction TB
        node_206["main.yml"]
    end
    subgraph dir_ansible_roles_monitoring_templates [ansible/roles/monitoring/templates]
        direction TB
        node_198["dashboards.yaml.j2"]
        node_201["datasource.yaml.j2"]
        node_204["grafana.nomad.j2"]
        node_199["memory-audit.nomad.j2"]
        node_202["mqtt-exporter.nomad.j2"]
        node_205["node-exporter.nomad.j2"]
        node_203["prometheus.nomad.j2"]
        node_200["prometheus.yml.j2"]
    end
    subgraph dir_ansible_roles_mqtt_handlers [ansible/roles/mqtt/handlers]
        direction TB
        node_293["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_meta [ansible/roles/mqtt/meta]
        direction TB
        node_294["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_tasks [ansible/roles/mqtt/tasks]
        direction TB
        node_296["main.yaml"]
    end
    subgraph dir_ansible_roles_mqtt_templates [ansible/roles/mqtt/templates]
        direction TB
        node_295["mqtt.nomad.j2"]
    end
    subgraph dir_ansible_roles_nanochat_defaults [ansible/roles/nanochat/defaults]
        direction TB
        node_285["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_handlers [ansible/roles/nanochat/handlers]
        direction TB
        node_284["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_tasks [ansible/roles/nanochat/tasks]
        direction TB
        node_287["main.yaml"]
    end
    subgraph dir_ansible_roles_nanochat_templates [ansible/roles/nanochat/templates]
        direction TB
        node_286["nanochat.nomad.j2"]
    end
    subgraph dir_ansible_roles_nats_handlers [ansible/roles/nats/handlers]
        direction TB
        node_250["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_tasks [ansible/roles/nats/tasks]
        direction TB
        node_252["main.yaml"]
    end
    subgraph dir_ansible_roles_nats_templates [ansible/roles/nats/templates]
        direction TB
        node_251["nats.nomad.j2"]
    end
    subgraph dir_ansible_roles_nfs_handlers [ansible/roles/nfs/handlers]
        direction TB
        node_116["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_tasks [ansible/roles/nfs/tasks]
        direction TB
        node_118["main.yaml"]
    end
    subgraph dir_ansible_roles_nfs_templates [ansible/roles/nfs/templates]
        direction TB
        node_117["exports.j2"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_handlers [ansible/roles/nixos_pxe_server/handlers]
        direction TB
        node_280["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_tasks [ansible/roles/nixos_pxe_server/tasks]
        direction TB
        node_283["main.yaml"]
    end
    subgraph dir_ansible_roles_nixos_pxe_server_templates [ansible/roles/nixos_pxe_server/templates]
        direction TB
        node_282["boot.ipxe.nix.j2"]
        node_281["configuration.nix.j2"]
    end
    subgraph dir_ansible_roles_nomad_defaults [ansible/roles/nomad/defaults]
        direction TB
        node_175["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_handlers [ansible/roles/nomad/handlers]
        direction TB
        node_174["main.yaml"]
        node_173["restart_nomad_handler_tasks.yaml"]
    end
    subgraph dir_ansible_roles_nomad_tasks [ansible/roles/nomad/tasks]
        direction TB
        node_181["main.yaml"]
    end
    subgraph dir_ansible_roles_nomad_templates [ansible/roles/nomad/templates]
        direction TB
        node_180["client.hcl.j2"]
        node_177["nomad.hcl.server.j2"]
        node_176["nomad.service.j2"]
        node_178["nomad.sh.j2"]
        node_179["server.hcl.j2"]
    end
    subgraph dir_ansible_roles_opencode_handlers [ansible/roles/opencode/handlers]
        direction TB
        node_229["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_tasks [ansible/roles/opencode/tasks]
        direction TB
        node_231["main.yaml"]
    end
    subgraph dir_ansible_roles_opencode_templates [ansible/roles/opencode/templates]
        direction TB
        node_230["opencode.nomad.j2"]
    end
    subgraph dir_ansible_roles_openworkers_handlers [ansible/roles/openworkers/handlers]
        direction TB
        node_110["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_tasks [ansible/roles/openworkers/tasks]
        direction TB
        node_114["main.yaml"]
    end
    subgraph dir_ansible_roles_openworkers_templates [ansible/roles/openworkers/templates]
        direction TB
        node_113["openworkers-bootstrap.nomad.j2"]
        node_111["openworkers-infra.nomad.j2"]
        node_112["openworkers-runners.nomad.j2"]
    end
    subgraph dir_ansible_roles_paddler_tasks [ansible/roles/paddler/tasks]
        direction TB
        node_279["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent [ansible/roles/paddler_agent]
        direction TB
        node_246["README.md"]
    end
    subgraph dir_ansible_roles_paddler_agent_defaults [ansible/roles/paddler_agent/defaults]
        direction TB
        node_247["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_tasks [ansible/roles/paddler_agent/tasks]
        direction TB
        node_249["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_agent_templates [ansible/roles/paddler_agent/templates]
        direction TB
        node_248["paddler-agent.service.j2"]
    end
    subgraph dir_ansible_roles_paddler_balancer [ansible/roles/paddler_balancer]
        direction TB
        node_211["README.md"]
    end
    subgraph dir_ansible_roles_paddler_balancer_defaults [ansible/roles/paddler_balancer/defaults]
        direction TB
        node_212["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_tasks [ansible/roles/paddler_balancer/tasks]
        direction TB
        node_214["main.yaml"]
    end
    subgraph dir_ansible_roles_paddler_balancer_templates [ansible/roles/paddler_balancer/templates]
        direction TB
        node_213["paddler-balancer.service.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_defaults [ansible/roles/pipecatapp/defaults]
        direction TB
        node_361["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_handlers [ansible/roles/pipecatapp/handlers]
        direction TB
        node_360["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_tasks [ansible/roles/pipecatapp/tasks]
        direction TB
        node_372["main.yaml"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates [ansible/roles/pipecatapp/templates]
        direction TB
        node_365["archivist.nomad.j2"]
        node_362["pipecat.env.j2"]
        node_363["pipecatapp.nomad.j2"]
        node_364["start_pipecatapp.sh.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_prompts [ansible/roles/pipecatapp/templates/prompts]
        direction TB
        node_368["coding_expert.txt.j2"]
        node_369["creative_expert.txt.j2"]
        node_367["cynic_expert.txt.j2"]
        node_366["router.txt.j2"]
        node_370["tron_agent.txt.j2"]
    end
    subgraph dir_ansible_roles_pipecatapp_templates_workflows [ansible/roles/pipecatapp/templates/workflows]
        direction TB
        node_371["default_agent_loop.yaml.j2"]
    end
    subgraph dir_ansible_roles_postgres_handlers [ansible/roles/postgres/handlers]
        direction TB
        node_253["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_tasks [ansible/roles/postgres/tasks]
        direction TB
        node_255["main.yaml"]
    end
    subgraph dir_ansible_roles_postgres_templates [ansible/roles/postgres/templates]
        direction TB
        node_254["postgres.nomad.j2"]
    end
    subgraph dir_ansible_roles_power_manager_defaults [ansible/roles/power_manager/defaults]
        direction TB
        node_304["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_files [ansible/roles/power_manager/files]
        direction TB
        node_305["power_agent.py"]
        node_306["traffic_monitor.c"]
    end
    subgraph dir_ansible_roles_power_manager_handlers [ansible/roles/power_manager/handlers]
        direction TB
        node_303["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_tasks [ansible/roles/power_manager/tasks]
        direction TB
        node_308["main.yaml"]
    end
    subgraph dir_ansible_roles_power_manager_templates [ansible/roles/power_manager/templates]
        direction TB
        node_307["power-agent.service.j2"]
    end
    subgraph dir_ansible_roles_preflight_checks_tasks [ansible/roles/preflight_checks/tasks]
        direction TB
        node_356["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_files [ansible/roles/provisioning_api/files]
        direction TB
        node_239["provisioning_api.py"]
    end
    subgraph dir_ansible_roles_provisioning_api_handlers [ansible/roles/provisioning_api/handlers]
        direction TB
        node_238["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_tasks [ansible/roles/provisioning_api/tasks]
        direction TB
        node_241["main.yaml"]
    end
    subgraph dir_ansible_roles_provisioning_api_templates [ansible/roles/provisioning_api/templates]
        direction TB
        node_240["provisioning-api.service.j2"]
    end
    subgraph dir_ansible_roles_pxe_server_defaults [ansible/roles/pxe_server/defaults]
        direction TB
        node_298["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_handlers [ansible/roles/pxe_server/handlers]
        direction TB
        node_297["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_tasks [ansible/roles/pxe_server/tasks]
        direction TB
        node_302["main.yaml"]
    end
    subgraph dir_ansible_roles_pxe_server_templates [ansible/roles/pxe_server/templates]
        direction TB
        node_299["boot.ipxe.j2"]
        node_301["dhcpd.conf.j2"]
        node_300["preseed.cfg.j2"]
    end
    subgraph dir_ansible_roles_python_deps_files [ansible/roles/python_deps/files]
        direction TB
        node_277["requirements.txt"]
    end
    subgraph dir_ansible_roles_python_deps_tasks [ansible/roles/python_deps/tasks]
        direction TB
        node_278["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_defaults [ansible/roles/semantic_router/defaults]
        direction TB
        node_125["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_tasks [ansible/roles/semantic_router/tasks]
        direction TB
        node_128["main.yaml"]
    end
    subgraph dir_ansible_roles_semantic_router_templates [ansible/roles/semantic_router/templates]
        direction TB
        node_126["Dockerfile.j2"]
        node_127["semantic-router.nomad.j2"]
    end
    subgraph dir_ansible_roles_sunshine_defaults [ansible/roles/sunshine/defaults]
        direction TB
        node_243["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_handlers [ansible/roles/sunshine/handlers]
        direction TB
        node_242["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_tasks [ansible/roles/sunshine/tasks]
        direction TB
        node_245["main.yaml"]
    end
    subgraph dir_ansible_roles_sunshine_templates [ansible/roles/sunshine/templates]
        direction TB
        node_244["sunshine.nomad.j2"]
    end
    subgraph dir_ansible_roles_system_deps_tasks [ansible/roles/system_deps/tasks]
        direction TB
        node_157["main.yaml"]
    end
    subgraph dir_ansible_roles_tailscale_tasks [ansible/roles/tailscale/tasks]
        direction TB
        node_271["main.yaml"]
    end
    subgraph dir_ansible_roles_term_everything_tasks [ansible/roles/term_everything/tasks]
        direction TB
        node_309["main.yml"]
    end
    subgraph dir_ansible_roles_tool_server [ansible/roles/tool_server]
        direction TB
        node_317["Dockerfile"]
        node_315["app.py"]
        node_316["entrypoint.sh"]
        node_318["pmm_memory.py"]
        node_314["preload_models.py"]
    end
    subgraph dir_ansible_roles_tool_server_tasks [ansible/roles/tool_server/tasks]
        direction TB
        node_320["main.yaml"]
    end
    subgraph dir_ansible_roles_tool_server_templates [ansible/roles/tool_server/templates]
        direction TB
        node_319["tool_server.nomad.j2"]
    end
    subgraph dir_ansible_roles_tool_server_tools [ansible/roles/tool_server/tools]
        direction TB
        node_325["ansible_tool.py"]
        node_329["archivist_tool.py"]
        node_334["claude_clone_tool.py"]
        node_336["code_runner_tool.py"]
        node_332["council_tool.py"]
        node_342["desktop_control_tool.py"]
        node_324["file_editor_tool.py"]
        node_341["final_answer_tool.py"]
        node_349["gemini_cli.py"]
        node_323["get_nomad_job.py"]
        node_321["git_tool.py"]
        node_327["ha_tool.py"]
        node_328["llxprt_code_tool.py"]
        node_347["mcp_tool.py"]
        node_335["opencode_tool.py"]
        node_330["orchestrator_tool.py"]
        node_346["planner_tool.py"]
        node_322["power_tool.py"]
        node_326["project_mapper_tool.py"]
        node_339["prompt_improver_tool.py"]
        node_333["rag_tool.py"]
        node_343["sandbox.ts"]
        node_345["shell_tool.py"]
        node_331["smol_agent_tool.py"]
        node_337["ssh_tool.py"]
        node_344["summarizer_tool.py"]
        node_338["swarm_tool.py"]
        node_350["tap_service.py"]
        node_348["term_everything_tool.py"]
        node_340["web_browser_tool.py"]
    end
    subgraph dir_ansible_roles_unified_fs_defaults [ansible/roles/unified_fs/defaults]
        direction TB
        node_262["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_files [ansible/roles/unified_fs/files]
        direction TB
        node_263["unified_fs_agent.py"]
    end
    subgraph dir_ansible_roles_unified_fs_handlers [ansible/roles/unified_fs/handlers]
        direction TB
        node_261["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_tasks [ansible/roles/unified_fs/tasks]
        direction TB
        node_265["main.yml"]
    end
    subgraph dir_ansible_roles_unified_fs_templates [ansible/roles/unified_fs/templates]
        direction TB
        node_264["unified_fs.service.j2"]
    end
    subgraph dir_ansible_roles_vision_defaults [ansible/roles/vision/defaults]
        direction TB
        node_352["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_handlers [ansible/roles/vision/handlers]
        direction TB
        node_351["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_tasks [ansible/roles/vision/tasks]
        direction TB
        node_355["main.yaml"]
    end
    subgraph dir_ansible_roles_vision_templates [ansible/roles/vision/templates]
        direction TB
        node_354["config.yml.j2"]
        node_353["vision.nomad.j2"]
    end
    subgraph dir_ansible_roles_vllm_tasks [ansible/roles/vllm/tasks]
        direction TB
        node_193["main.yaml"]
        node_194["run_single_vllm_job.yaml"]
    end
    subgraph dir_ansible_roles_vllm_templates [ansible/roles/vllm/templates]
        direction TB
        node_192["vllm-expert.nomad.j2"]
    end
    subgraph dir_ansible_roles_whisper_cpp_tasks [ansible/roles/whisper_cpp/tasks]
        direction TB
        node_195["main.yaml"]
    end
    subgraph dir_ansible_roles_world_model_service [ansible/roles/world_model_service]
        direction TB
        node_143["world_model.nomad.j2"]
    end
    subgraph dir_ansible_roles_world_model_service_files [ansible/roles/world_model_service/files]
        direction TB
        node_147["Dockerfile"]
        node_146["app.py"]
        node_145["debug_world_model.sh"]
        node_144["requirements.txt"]
    end
    subgraph dir_ansible_roles_world_model_service_tasks [ansible/roles/world_model_service/tasks]
        direction TB
        node_148["main.yaml"]
    end
    subgraph dir_ansible_tasks [ansible/tasks]
        direction TB
        node_373["README.md"]
        node_374["build_pipecatapp_image.yaml"]
        node_376["create_expert_job.yaml"]
        node_377["deploy_expert_wrapper.yaml"]
        node_375["deploy_model_gpu_provider.yaml"]
    end
    subgraph dir_docker [docker]
        direction TB
        node_430["README.md"]
    end
    subgraph dir_docker_dev_container [docker/dev_container]
        direction TB
        node_432["Dockerfile"]
    end
    subgraph dir_docker_memory_service [docker/memory_service]
        direction TB
        node_431["Dockerfile"]
    end
    subgraph dir_docs [docs]
        direction TB
        node_35["AGENTS.md"]
        node_50["ARCHITECTURE.md"]
        node_26["BENCHMARKING.MD"]
        node_39["DEPLOYMENT_AND_PROFILING.md"]
        node_44["EVALUATION_LLMROUTER.md"]
        node_30["FRONTEND_VERIFICATION.md"]
        node_34["FRONTIER_AGENT_ROADMAP.md"]
        node_36["GASTOWN_TODO.md"]
        node_29["GEMINI.md"]
        node_46["IPV6_AUDIT.md"]
        node_24["MCP_SERVER_SETUP.md"]
        node_25["MEMORIES.md"]
        node_33["NETWORK.md"]
        node_32["NIXOS_PXE_BOOT_SETUP.md"]
        node_31["PERFORMANCE_OPTIMIZATION.md"]
        node_49["PROJECT_SUMMARY.md"]
        node_38["PXE_BOOT_SETUP.md"]
        node_28["README.md"]
        node_47["REFACTOR_PROPOSAL_hybrid_architecture.md"]
        node_41["REMOTE_WORKFLOW.md"]
        node_27["SCALING_TODO.md"]
        node_51["SECURITY_AUDIT.md"]
        node_40["TODO_Hybrid_Architecture.md"]
        node_37["TOOL_EVALUATION.md"]
        node_45["TROUBLESHOOTING.md"]
        node_48["VLLM_PROJECT_EVALUATION.md"]
        node_42["YAML_FILES_REPORT.md"]
        node_43["heretic_evaluation.md"]
    end
    subgraph dir_examples [examples]
        direction TB
        node_437["README.md"]
        node_438["chat-persistent.sh"]
    end
    subgraph dir_group_vars [group_vars]
        direction TB
        node_741["README.md"]
        node_742["all.yaml"]
        node_743["external_experts.yaml"]
        node_744["models.yaml"]
    end
    subgraph dir_host_vars [host_vars]
        direction TB
        node_429["README.md"]
        node_428["localhost.yaml"]
    end
    subgraph dir_initial_setup [initial-setup]
        direction TB
        node_588["README.md"]
        node_590["add_new_worker.sh"]
        node_591["setup.conf"]
        node_589["setup.sh"]
        node_592["update_inventory.sh"]
    end
    subgraph dir_initial_setup_modules [initial-setup/modules]
        direction TB
        node_597["01-network.sh"]
        node_599["02-hostname.sh"]
        node_595["03-user.sh"]
        node_598["04-ssh.sh"]
        node_600["05-auto-provision.sh"]
        node_596["README.md"]
    end
    subgraph dir_initial_setup_worker_setup [initial-setup/worker-setup]
        direction TB
        node_593["README.md"]
        node_594["setup.sh"]
    end
    subgraph dir_pipecat_agent_extension [pipecat-agent-extension]
        direction TB
        node_580["README.md"]
        node_583["example.ts"]
        node_581["gemini-extension.json"]
        node_582["package.json"]
        node_584["tsconfig.json"]
    end
    subgraph dir_pipecat_agent_extension_commands_pipecat [pipecat-agent-extension/commands/pipecat]
        direction TB
        node_585["send.toml"]
    end
    subgraph dir_pipecatapp [pipecatapp]
        direction TB
        node_626["Dockerfile"]
        node_609["README.md"]
        node_605["TODO.md"]
        node_613["__init__.py"]
        node_615["agent_factory.py"]
        node_607["api_keys.py"]
        node_621["app.py"]
        node_620["archivist_service.py"]
        node_629["durable_execution.py"]
        node_632["expert_tracker.py"]
        node_617["janitor_agent.py"]
        node_618["judge_agent.py"]
        node_627["llm_clients.py"]
        node_631["manager_agent.py"]
        node_634["memory.py"]
        node_610["models.py"]
        node_614["moondream_detector.py"]
        node_601["net_utils.py"]
        node_630["pmm_memory.py"]
        node_625["pmm_memory_client.py"]
        node_623["quality_control.py"]
        node_604["rate_limiter.py"]
        node_603["requirements.txt"]
        node_611["security.py"]
        node_612["start_archivist.sh"]
        node_624["task_supervisor.py"]
        node_616["technician_agent.py"]
        node_608["test_memory.py"]
        node_602["test_moondream_detector.py"]
        node_628["test_pmm_memory.py"]
        node_622["test_server.py"]
        node_633["tool_server.py"]
        node_606["web_server.py"]
        node_619["worker_agent.py"]
    end
    subgraph dir_pipecatapp_datasets [pipecatapp/datasets]
        direction TB
        node_649["sycophancy_prompts.json"]
    end
    subgraph dir_pipecatapp_integrations [pipecatapp/integrations]
        direction TB
        node_635["__init__.py"]
        node_636["openclaw.py"]
    end
    subgraph dir_pipecatapp_memory_graph_service [pipecatapp/memory_graph_service]
        direction TB
        node_694["Dockerfile"]
        node_693["server.py"]
    end
    subgraph dir_pipecatapp_nomad_templates [pipecatapp/nomad_templates]
        direction TB
        node_691["immich.nomad.hcl"]
        node_689["readeck.nomad.hcl"]
        node_690["uptime-kuma.nomad.hcl"]
        node_692["vaultwarden.nomad.hcl"]
    end
    subgraph dir_pipecatapp_prompts [pipecatapp/prompts]
        direction TB
        node_664["coding_expert.txt"]
        node_665["creative_expert.txt"]
        node_663["router.txt"]
        node_662["tron_agent.txt"]
    end
    subgraph dir_pipecatapp_static [pipecatapp/static]
        direction TB
        node_643["cluster.html"]
        node_642["cluster_viz.html"]
        node_637["index.html"]
        node_641["monitor.html"]
        node_640["terminal.js"]
        node_639["vr_index.html"]
        node_638["workflow.html"]
    end
    subgraph dir_pipecatapp_static_css [pipecatapp/static/css]
        direction TB
        node_648["litegraph.css"]
        node_647["styles.css"]
    end
    subgraph dir_pipecatapp_static_js [pipecatapp/static/js]
        direction TB
        node_645["editor.js"]
        node_644["litegraph.js"]
        node_646["workflow.js"]
    end
    subgraph dir_pipecatapp_tests [pipecatapp/tests]
        direction TB
        node_671["test_audio_streamer.py"]
        node_670["test_browser_tool_security.py"]
        node_669["test_container_registry_tool.py"]
        node_673["test_git_tool_security.py"]
        node_682["test_metrics_cache.py"]
        node_678["test_net_utils.py"]
        node_680["test_openclaw.py"]
        node_677["test_piper_async.py"]
        node_679["test_proxy_security.py"]
        node_681["test_rag_tool.py"]
        node_675["test_rate_limiter.py"]
        node_672["test_security.py"]
        node_667["test_stt_optimization.py"]
        node_666["test_uilogger_redaction.py"]
        node_674["test_web_server_unit.py"]
        node_676["test_websocket_security.py"]
        node_683["test_xss_prevention.py"]
        node_668["test_yolo_optimization.py"]
    end
    subgraph dir_pipecatapp_tests_workflow [pipecatapp/tests/workflow]
        direction TB
        node_684["test_history.py"]
        node_685["test_serialization_perf.py"]
    end
    subgraph dir_pipecatapp_tools [pipecatapp/tools]
        direction TB
        node_711["__init__.py"]
        node_701["ansible_tool.py"]
        node_707["archivist_tool.py"]
        node_715["claude_clone_tool.py"]
        node_718["code_runner_tool.py"]
        node_723["container_registry_tool.py"]
        node_712["council_tool.py"]
        node_704["dependency_scanner_tool.py"]
        node_726["desktop_control_tool.py"]
        node_739["experiment_tool.py"]
        node_700["file_editor_tool.py"]
        node_725["final_answer_tool.py"]
        node_736["gemini_cli.py"]
        node_698["get_nomad_job.py"]
        node_695["git_tool.py"]
        node_703["ha_tool.py"]
        node_706["llxprt_code_tool.py"]
        node_733["mcp_tool.py"]
        node_732["miniray_tool.py"]
        node_735["mkv_tool.py"]
        node_716["open_workers_tool.py"]
        node_740["openclaw_tool.py"]
        node_717["opencode_tool.py"]
        node_708["orchestrator_tool.py"]
        node_731["planner_tool.py"]
        node_696["power_tool.py"]
        node_702["project_mapper_tool.py"]
        node_722["prompt_improver_tool.py"]
        node_714["rag_tool.py"]
        node_697["remote_tool_proxy.py"]
        node_727["sandbox.ts"]
        node_721["search_tool.py"]
        node_730["shell_tool.py"]
        node_709["smol_agent_tool.py"]
        node_710["spec_loader_tool.py"]
        node_719["ssh_tool.py"]
        node_737["submit_solution_tool.py"]
        node_729["summarizer_tool.py"]
        node_720["swarm_tool.py"]
        node_738["tap_service.py"]
        node_734["term_everything_tool.py"]
        node_699["test_code_runner_tool.py"]
        node_728["test_git_tool.py"]
        node_705["test_ssh_tool.py"]
        node_713["vr_tool.py"]
        node_724["web_browser_tool.py"]
    end
    subgraph dir_pipecatapp_workflow [pipecatapp/workflow]
        direction TB
        node_650["__init__.py"]
        node_651["context.py"]
        node_653["history.py"]
        node_652["node.py"]
        node_654["runner.py"]
    end
    subgraph dir_pipecatapp_workflow_nodes [pipecatapp/workflow/nodes]
        direction TB
        node_657["__init__.py"]
        node_658["base_nodes.py"]
        node_661["emperor_nodes.py"]
        node_659["llm_nodes.py"]
        node_656["registry.py"]
        node_660["system_nodes.py"]
        node_655["tool_nodes.py"]
    end
    subgraph dir_pipecatapp_workflows [pipecatapp/workflows]
        direction TB
        node_687["default_agent_loop.yaml"]
        node_688["poc_ensemble.yaml"]
        node_686["tiered_agent_loop.yaml"]
    end
    subgraph dir_playbooks [playbooks]
        direction TB
        node_386["README.md"]
        node_402["benchmark_single_model.yaml"]
        node_392["cluster_status.yaml"]
        node_385["common_setup.yaml"]
        node_405["controller.yaml"]
        node_382["debug_template.yaml"]
        node_396["deploy_app.yaml"]
        node_387["deploy_expert.yaml"]
        node_393["deploy_moltbot.yaml"]
        node_383["deploy_prompt_evolution.yaml"]
        node_380["developer_tools.yaml"]
        node_390["diagnose_and_log_home_assistant.yaml"]
        node_388["diagnose_failure.yaml"]
        node_378["diagnose_home_assistant.yaml"]
        node_395["fix_cluster.yaml"]
        node_389["heal_cluster.yaml"]
        node_379["heal_job.yaml"]
        node_403["health_check.yaml"]
        node_398["promote_controller.yaml"]
        node_401["promote_to_controller.yaml"]
        node_397["pxe_setup.yaml"]
        node_400["redeploy_pipecat.yaml"]
        node_394["run_config_manager.yaml"]
        node_381["run_consul.yaml"]
        node_391["run_ha_diag.yaml"]
        node_404["run_health_check.yaml"]
        node_384["status-check.yaml"]
        node_399["wake.yaml"]
        node_406["worker.yaml"]
    end
    subgraph dir_playbooks_network [playbooks/network]
        direction TB
        node_409["mesh.yaml"]
        node_408["verify.yaml"]
    end
    subgraph dir_playbooks_ops [playbooks/ops]
        direction TB
        node_407["optimize_memory.yaml"]
    end
    subgraph dir_playbooks_preflight [playbooks/preflight]
        direction TB
        node_410["checks.yaml"]
    end
    subgraph dir_playbooks_services [playbooks/services]
        direction TB
        node_413["README.md"]
        node_421["ai_experts.yaml"]
        node_424["app_services.yaml"]
        node_423["consul.yaml"]
        node_411["core_ai_services.yaml"]
        node_422["core_infra.yaml"]
        node_416["distributed_compute.yaml"]
        node_420["docker.yaml"]
        node_418["final_verification.yaml"]
        node_417["model_services.yaml"]
        node_425["monitoring.yaml"]
        node_426["nomad.yaml"]
        node_415["nomad_client.yaml"]
        node_412["registry.yaml"]
        node_419["streaming_services.yaml"]
        node_414["training_services.yaml"]
    end
    subgraph dir_playbooks_services_tasks [playbooks/services/tasks]
        direction TB
        node_427["diagnose_home_assistant.yaml"]
    end
    subgraph dir_prompt_engineering [prompt_engineering]
        direction TB
        node_65["PROMPT_ENGINEERING.md"]
        node_60["README.md"]
        node_66["challenger.py"]
        node_59["create_evaluator.py"]
        node_68["evaluation_lib.py"]
        node_64["evaluator.py"]
        node_63["evolve.py"]
        node_58["promote_agent.py"]
        node_62["requirements-dev.txt"]
        node_61["run_campaign.py"]
        node_67["visualize_archive.py"]
    end
    subgraph dir_prompt_engineering_agents [prompt_engineering/agents]
        direction TB
        node_81["ADAPTATION_AGENT.md"]
        node_80["EVALUATOR_GENERATOR.md"]
        node_75["README.md"]
        node_77["architecture_review.md"]
        node_79["code_clean_up.md"]
        node_78["debug_and_analysis.md"]
        node_74["new_task_review.md"]
        node_76["problem_scope_framing.md"]
    end
    subgraph dir_prompt_engineering_archive [prompt_engineering/archive]
        direction TB
        node_82["agent_0.json"]
        node_89["agent_0.py"]
        node_85["agent_1.json"]
        node_83["agent_1.py"]
        node_84["agent_2.json"]
        node_87["agent_2.py"]
        node_86["agent_3.json"]
        node_88["agent_3.py"]
    end
    subgraph dir_prompt_engineering_evaluation_suite [prompt_engineering/evaluation_suite]
        direction TB
        node_72["README.md"]
        node_73["test_vision.yaml"]
    end
    subgraph dir_prompt_engineering_frontend [prompt_engineering/frontend]
        direction TB
        node_69["index.html"]
        node_70["server.py"]
    end
    subgraph dir_prompt_engineering_generated_evaluators [prompt_engineering/generated_evaluators]
        direction TB
        node_71[".gitignore"]
    end
    subgraph dir_prompts [prompts]
        direction TB
        node_478["README.md"]
        node_479["chat-with-bob.txt"]
        node_477["router.txt"]
    end
    subgraph dir_reflection [reflection]
        direction TB
        node_434["README.md"]
        node_435["adaptation_manager.py"]
        node_433["create_reflection.py"]
        node_436["reflect.py"]
    end
    subgraph dir_scripts [scripts]
        direction TB
        node_448["README.md"]
        node_451["agentic_workflow.sh"]
        node_442["analyze_nomad_allocs.py"]
        node_445["ansible_diff.sh"]
        node_471["check_all_playbooks.sh"]
        node_463["check_deps.py"]
        node_472["ci_ansible_check.sh"]
        node_466["cleanup.sh"]
        node_465["compare_exo_llama.py"]
        node_455["create_cynic_model.sh"]
        node_459["create_todo_issues.sh"]
        node_453["debug_expert.sh"]
        node_447["debug_mesh.sh"]
        node_470["fix_markdown.sh"]
        node_461["fix_verification_failures.sh"]
        node_441["fix_yaml.sh"]
        node_446["generate_file_map.py"]
        node_444["generate_issue_script.py"]
        node_469["heal_cluster.sh"]
        node_450["healer.py"]
        node_464["lint.sh"]
        node_467["lint_exclude.txt"]
        node_457["memory_audit.py"]
        node_456["profile_resources.sh"]
        node_474["provisioning.py"]
        node_460["prune_consul_services.py"]
        node_440["run_quibbler.sh"]
        node_454["run_tests.sh"]
        node_449["start_services.sh"]
        node_458["supervisor.py"]
        node_468["test_playbooks_dry_run.sh"]
        node_462["test_playbooks_live_run.sh"]
        node_452["troubleshoot.py"]
        node_473["uninstall.sh"]
        node_443["verify_consul_attributes.sh"]
    end
    subgraph dir_scripts_debug [scripts/debug]
        direction TB
        node_476["README.md"]
        node_475["test_mqtt_connection.py"]
    end
    subgraph dir_tests [tests]
        direction TB
        node_484["README.md"]
        node_487["__init__.py"]
        node_490["test.wav"]
        node_494["test_agent_patterns.py"]
        node_488["test_emperor_node.py"]
        node_495["test_event_bus.py"]
        node_491["test_experiment_tool.py"]
        node_492["test_gastown_judge.py"]
        node_489["test_gastown_memory.py"]
        node_481["test_gastown_stats.py"]
        node_483["test_imports.py"]
        node_486["test_manager_flow.py"]
        node_480["test_spec_loader.py"]
        node_485["test_ssrf_validation.py"]
        node_493["verify_config_load.py"]
        node_482["verify_dlq.py"]
    end
    subgraph dir_tests_e2e [tests/e2e]
        direction TB
        node_498["README.md"]
        node_499["__init__.py"]
        node_496["test_api.py"]
        node_501["test_intelligent_routing.py"]
        node_503["test_mission_control.py"]
        node_500["test_palette_command_history.py"]
        node_502["test_palette_ux.py"]
        node_497["test_regression.py"]
    end
    subgraph dir_tests_integration [tests/integration]
        direction TB
        node_516["README.md"]
        node_518["__init__.py"]
        node_523["stub_services.py"]
        node_521["test_consul_role.yaml"]
        node_519["test_home_assistant.yaml"]
        node_517["test_mini_pipeline.py"]
        node_515["test_mqtt_exporter.py"]
        node_514["test_nomad_role.yaml"]
        node_520["test_pipecat_app.py"]
        node_522["test_preemption.py"]
    end
    subgraph dir_tests_integration_roles_test_home_assistant_tasks [tests/integration/roles/test_home_assistant/tasks]
        direction TB
        node_524["main.yaml"]
    end
    subgraph dir_tests_playbooks [tests/playbooks]
        direction TB
        node_506["e2e-tests.yaml"]
        node_504["test_consul.yaml"]
        node_505["test_llama_cpp.yaml"]
        node_507["test_nomad.yaml"]
    end
    subgraph dir_tests_scripts [tests/scripts]
        direction TB
        node_513["run_unit_tests.sh"]
        node_512["test_duplicate_role_execution.sh"]
        node_511["test_paddler.sh"]
        node_510["test_piper.sh"]
        node_508["test_run.sh"]
        node_509["verify_components.py"]
    end
    subgraph dir_tests_unit [tests/unit]
        direction TB
        node_538["README.md"]
        node_543["__init__.py"]
        node_553["conftest.py"]
        node_528["test_adaptation_manager.py"]
        node_568["test_agent_definitions.py"]
        node_549["test_ansible_tool.py"]
        node_537["test_archivist_tool.py"]
        node_552["test_claude_clone_tool.py"]
        node_527["test_code_runner_tool.py"]
        node_550["test_council_tool.py"]
        node_544["test_dependency_scanner.py"]
        node_566["test_desktop_control_tool.py"]
        node_539["test_file_editor_security.py"]
        node_547["test_file_editor_tool.py"]
        node_557["test_final_answer_tool.py"]
        node_574["test_gemini_cli.py"]
        node_562["test_get_nomad_job.py"]
        node_567["test_git_tool.py"]
        node_556["test_ha_tool.py"]
        node_540["test_home_assistant_template.py"]
        node_569["test_infrastructure.py"]
        node_563["test_lint_script.py"]
        node_573["test_llxprt_code_tool.py"]
        node_546["test_mcp_tool.py"]
        node_530["test_mqtt_template.py"]
        node_541["test_open_workers_tool.py"]
        node_578["test_opencode_tool.py"]
        node_548["test_orchestrator_tool.py"]
        node_536["test_pipecat_app_unit.py"]
        node_575["test_planner_tool.py"]
        node_559["test_playbook_integration.py"]
        node_570["test_poc_ensemble.py"]
        node_560["test_power_tool.py"]
        node_555["test_project_mapper_tool.py"]
        node_535["test_prompt_engineering.py"]
        node_564["test_prompt_improver_tool.py"]
        node_526["test_provisioning.py"]
        node_572["test_rag_tool.py"]
        node_525["test_reflection.py"]
        node_542["test_security.py"]
        node_558["test_shell_tool.py"]
        node_565["test_simple_llm_node.py"]
        node_533["test_smol_agent_tool.py"]
        node_532["test_ssh_tool.py"]
        node_531["test_summarizer_tool.py"]
        node_534["test_supervisor.py"]
        node_551["test_swarm_tool.py"]
        node_571["test_tap_service.py"]
        node_529["test_term_everything_tool.py"]
        node_554["test_vision_failover.py"]
        node_561["test_web_browser_tool.py"]
        node_545["test_web_server_sync.py"]
        node_577["test_workflow.py"]
        node_576["test_world_model_service.py"]
    end
    subgraph dir_workflows [workflows]
        direction TB
        node_579["default_agent_loop.yaml"]
    end

    node_424 --> node_309
    node_621 --> node_337
    node_411 --> node_370
    node_317 --> node_188
    node_128 --> node_214
    node_40 --> node_580
    node_389 --> node_320
    node_417 --> node_195
    node_125 --> node_163
    node_389 --> node_266
    node_545 --> node_621
    node_446 --> node_587
    node_389 --> node_294
    node_671 --> node_315
    node_125 --> node_115
    node_11 --> node_621
    node_128 --> node_245
    node_40 --> node_351
    node_42 --> node_289
    node_6 --> node_231
    node_417 --> node_218
    node_42 --> node_252
    node_320 --> node_133
    node_424 --> node_169
    node_674 --> node_146
    node_128 --> node_166
    node_11 --> node_726
    node_258 --> node_222
    node_375 --> node_165
    node_561 --> node_724
    node_40 --> node_224
    node_480 --> node_434
    node_424 --> node_352
    node_536 --> node_579
    node_40 --> node_90
    node_474 --> node_315
    node_509 --> node_145
    node_11 --> node_635
    node_11 --> node_334
    node_480 --> node_413
    node_396 --> node_371
    node_25 --> node_633
    node_389 --> node_287
    node_32 --> node_232
    node_372 --> node_664
    node_575 --> node_346
    node_25 --> node_407
    node_125 --> node_361
    node_446 --> node_107
    node_424 --> node_273
    node_547 --> node_700
    node_493 --> node_742
    node_657 --> node_660
    node_534 --> node_436
    node_372 --> node_579
    node_65 --> node_146
    node_255 --> node_254
    node_426 --> node_177
    node_411 --> node_365
    node_128 --> node_258
    node_699 --> node_336
    node_40 --> node_231
    node_214 --> node_271
    node_11 --> node_350
    node_25 --> node_701
    node_6 --> node_150
    node_364 --> node_603
    node_128 --> node_235
    node_615 --> node_714
    node_249 --> node_293
    node_596 --> node_598
    node_249 --> node_150
    node_258 --> node_255
    node_433 --> node_693
    node_11 --> node_330
    node_258 --> node_247
    node_459 --> node_147
    node_596 --> node_599
    node_75 --> node_76
    node_638 --> node_647
    node_51 --> node_579
    node_258 --> node_187
    node_657 --> node_655
    node_258 --> node_165
    node_320 --> node_630
    node_214 --> node_114
    node_389 --> node_125
    node_181 --> node_177
    node_588 --> node_594
    node_28 --> node_32
    node_568 --> node_80
    node_380 --> node_235
    node_389 --> node_372
    node_25 --> node_6
    node_214 --> node_260
    node_424 --> node_319
    node_389 --> node_285
    node_40 --> node_293
    node_128 --> node_283
    node_32 --> node_210
    node_273 --> node_181
    node_42 --> node_229
    node_40 --> node_150
    node_424 --> node_323
    node_25 --> node_379
    node_421 --> node_171
    node_417 --> node_744
    node_416 --> node_134
    node_424 --> node_351
    node_128 --> node_126
    node_249 --> node_181
    node_615 --> node_344
    node_400 --> node_366
    node_42 --> node_28
    node_504 --> node_165
    node_35 --> node_13
    node_6 --> node_212
    node_7 --> node_146
    node_555 --> node_741
    node_258 --> node_118
    node_505 --> node_170
    node_415 --> node_174
    node_40 --> node_249
    node_446 --> node_432
    node_241 --> node_240
    node_430 --> node_133
    node_40 --> node_484
    node_42 --> node_235
    node_191 --> node_147
    node_169 --> node_165
    node_11 --> node_531
    node_32 --> node_276
    node_287 --> node_286
    node_615 --> node_724
    node_214 --> node_238
    node_621 --> node_336
    node_125 --> node_174
    node_258 --> node_303
    node_425 --> node_205
    node_507 --> node_181
    node_690 --> node_131
    node_40 --> node_181
    node_7 --> node_38
    node_128 --> node_524
    node_50 --> node_436
    node_555 --> node_596
    node_622 --> node_188
    node_451 --> node_429
    node_40 --> node_212
    node_273 --> node_176
    node_6 --> node_603
    node_386 --> node_385
    node_42 --> node_283
    node_555 --> node_498
    node_416 --> node_135
    node_214 --> node_298
    node_555 --> node_7
    node_128 --> node_104
    node_563 --> node_18
    node_128 --> node_130
    node_25 --> node_298
    node_272 --> node_180
    node_446 --> node_626
    node_125 --> node_304
    node_125 --> node_161
    node_249 --> node_148
    node_128 --> node_221
    node_400 --> node_744
    node_596 --> node_597
    node_6 --> node_243
    node_555 --> node_11
    node_459 --> node_506
    node_676 --> node_606
    node_125 --> node_215
    node_446 --> node_516
    node_40 --> node_434
    node_737 --> node_188
    node_424 --> node_314
    node_552 --> node_334
    node_40 --> node_413
    node_270 --> node_268
    node_42 --> node_355
    node_507 --> node_176
    node_621 --> node_332
    node_11 --> node_714
    node_29 --> node_22
    node_75 --> node_81
    node_92 --> node_743
    node_42 --> node_297
    node_42 --> node_296
    node_42 --> node_195
    node_125 --> node_155
    node_580 --> node_582
    node_40 --> node_148
    node_615 --> node_715
    node_727 --> node_343
    node_125 --> node_151
    node_272 --> node_174
    node_11 --> node_736
    node_720 --> node_616
    node_674 --> node_621
    node_125 --> node_289
    node_667 --> node_188
    node_249 --> node_110
    node_7 --> node_477
    node_467 --> node_184
    node_40 --> node_243
    node_270 --> node_317
    node_489 --> node_630
    node_272 --> node_295
    node_446 --> node_23
    node_6 --> node_222
    node_389 --> node_267
    node_660 --> node_656
    node_25 --> node_308
    node_555 --> node_437
    node_25 --> node_277
    node_258 --> node_172
    node_14 --> node_425
    node_400 --> node_360
    node_273 --> node_173
    node_459 --> node_744
    node_406 --> node_418
    node_737 --> node_146
    node_25 --> node_145
    node_343 --> node_727
    node_157 --> node_118
    node_148 --> node_694
    node_461 --> node_509
    node_65 --> node_621
    node_11 --> node_344
    node_621 --> node_607
    node_621 --> node_625
    node_446 --> node_392
    node_25 --> node_20
    node_642 --> node_645
    node_446 --> node_10
    node_389 --> node_270
    node_40 --> node_222
    node_128 --> node_292
    node_11 --> node_724
    node_142 --> node_141
    node_216 --> node_402
    node_6 --> node_255
    node_40 --> node_109
    node_389 --> node_241
    node_32 --> node_271
    node_273 --> node_179
    node_286 --> node_131
    node_6 --> node_247
    node_555 --> node_75
    node_735 --> node_655
    node_424 --> node_341
    node_214 --> node_216
    node_233 --> node_169
    node_25 --> node_131
    node_418 --> node_170
    node_44 --> node_654
    node_249 --> node_187
    node_125 --> node_166
    node_25 --> node_216
    node_249 --> node_165
    node_422 --> node_157
    node_448 --> node_472
    node_128 --> node_250
    node_377 --> node_374
    node_25 --> node_193
    node_372 --> node_687
    node_446 --> node_609
    node_638 --> node_184
    node_25 --> node_157
    node_125 --> node_229
    node_137 --> node_131
    node_128 --> node_175
    node_51 --> node_572
    node_481 --> node_630
    node_609 --> node_606
    node_30 --> node_17
    node_148 --> node_268
    node_6 --> node_279
    node_42 --> node_169
    node_505 --> node_167
    node_677 --> node_315
    node_7 --> node_621
    node_468 --> node_423
    node_462 --> node_506
    node_508 --> node_438
    node_25 --> node_107
    node_97 --> node_106
    node_40 --> node_247
    node_40 --> node_742
    node_544 --> node_704
    node_40 --> node_187
    node_42 --> node_352
    node_125 --> node_258
    node_40 --> node_165
    node_6 --> node_118
    node_42 --> node_313
    node_276 --> node_275
    node_204 --> node_201
    node_125 --> node_235
    node_249 --> node_302
    node_431 --> node_188
    node_451 --> node_596
    node_148 --> node_317
    node_40 --> node_586
    node_273 --> node_178
    node_32 --> node_356
    node_42 --> node_273
    node_35 --> node_477
    node_50 --> node_315
    node_25 --> node_699
    node_6 --> node_634
    node_416 --> node_142
    node_50 --> node_579
    node_14 --> node_417
    node_424 --> node_306
    node_633 --> node_327
    node_6 --> node_303
    node_484 --> node_454
    node_47 --> node_432
    node_11 --> node_715
    node_58 --> node_188
    node_372 --> node_623
    node_451 --> node_498
    node_498 --> node_497
    node_32 --> node_238
    node_422 --> node_152
    node_676 --> node_188
    node_505 --> node_228
    node_451 --> node_7
    node_535 --> node_61
    node_7 --> node_14
    node_42 --> node_142
    node_621 --> node_579
    node_258 --> node_310
    node_164 --> node_106
    node_419 --> node_245
    node_272 --> node_177
    node_437 --> node_438
    node_40 --> node_302
    node_40 --> node_118
    node_398 --> node_174
    node_125 --> node_283
    node_483 --> node_315
    node_389 --> node_257
    node_25 --> node_320
    node_214 --> node_266
    node_206 --> node_131
    node_42 --> node_396
    node_406 --> node_415
    node_214 --> node_294
    node_7 --> node_593
    node_516 --> node_146
    node_25 --> node_294
    node_42 --> node_580
    node_42 --> node_288
    node_534 --> node_458
    node_413 --> node_420
    node_538 --> node_188
    node_372 --> node_189
    node_40 --> node_303
    node_25 --> node_432
    node_448 --> node_471
    node_498 --> node_501
    node_535 --> node_67
    node_588 --> node_591
    node_615 --> node_695
    node_512 --> node_14
    node_32 --> node_311
    node_42 --> node_351
    node_258 --> node_207
    node_308 --> node_307
    node_161 --> node_147
    node_320 --> node_188
    node_446 --> node_246
    node_47 --> node_626
    node_593 --> node_594
    node_740 --> node_636
    node_25 --> node_287
    node_32 --> node_208
    node_42 --> node_388
    node_214 --> node_280
    node_436 --> node_698
    node_42 --> node_224
    node_214 --> node_237
    node_125 --> node_524
    node_400 --> node_362
    node_474 --> node_424
    node_561 --> node_340
    node_125 --> node_195
    node_214 --> node_284
    node_148 --> node_144
    node_451 --> node_437
    node_128 --> node_293
    node_381 --> node_742
    node_128 --> node_150
    node_381 --> node_165
    node_424 --> node_346
    node_270 --> node_159
    node_624 --> node_720
    node_424 --> node_316
    node_60 --> node_59
    node_258 --> node_308
    node_424 --> node_342
    node_6 --> node_172
    node_125 --> node_130
    node_128 --> node_249
    node_42 --> node_231
    node_29 --> node_63
    node_480 --> node_538
    node_315 --> node_729
    node_214 --> node_125
    node_424 --> node_279
    node_554 --> node_146
    node_186 --> node_183
    node_25 --> node_59
    node_25 --> node_626
    node_25 --> node_125
    node_516 --> node_519
    node_128 --> node_127
    node_539 --> node_700
    node_28 --> node_50
    node_538 --> node_534
    node_11 --> node_614
    node_372 --> node_634
    node_446 --> node_429
    node_25 --> node_372
    node_373 --> node_376
    node_224 --> node_222
    node_6 --> node_431
    node_46 --> node_13
    node_544 --> node_336
    node_606 --> node_641
    node_25 --> node_516
    node_48 --> node_744
    node_615 --> node_707
    node_25 --> node_285
    node_411 --> node_232
    node_32 --> node_116
    node_505 --> node_168
    node_128 --> node_181
    node_421 --> node_374
    node_596 --> node_589
    node_615 --> node_731
    node_7 --> node_246
    node_14 --> node_426
    node_609 --> node_188
    node_214 --> node_128
    node_64 --> node_146
    node_315 --> node_337
    node_418 --> node_167
    node_25 --> node_639
    node_411 --> node_230
    node_181 --> node_293
    node_424 --> node_303
    node_42 --> node_293
    node_396 --> node_364
    node_59 --> node_131
    node_42 --> node_150
    node_577 --> node_658
    node_258 --> node_131
    node_565 --> node_651
    node_424 --> node_427
    node_359 --> node_357
    node_258 --> node_193
    node_426 --> node_181
    node_6 --> node_61
    node_11 --> node_348
    node_446 --> node_19
    node_258 --> node_157
    node_580 --> node_581
    node_214 --> node_252
    node_209 --> node_131
    node_389 --> node_191
    node_400 --> node_369
    node_448 --> node_453
    node_118 --> node_117
    node_485 --> node_601
    node_32 --> node_115
    node_615 --> node_340
    node_615 --> node_697
    node_323 --> node_698
    node_148 --> node_133
    node_338 --> node_619
    node_147 --> node_621
    node_406 --> node_424
    node_555 --> node_211
    node_179 --> node_131
    node_405 --> node_420
    node_29 --> node_403
    node_7 --> node_60
    node_42 --> node_181
    node_118 --> node_116
    node_42 --> node_390
    node_214 --> node_278
    node_421 --> node_743
    node_128 --> node_148
    node_598 --> node_589
    node_125 --> node_292
    node_60 --> node_68
    node_389 --> node_182
    node_42 --> node_212
    node_505 --> node_156
    node_566 --> node_726
    node_6 --> node_67
    node_389 --> node_359
    node_654 --> node_611
    node_609 --> node_693
    node_480 --> node_710
    node_673 --> node_321
    node_25 --> node_68
    node_426 --> node_176
    node_125 --> node_250
    node_628 --> node_189
    node_411 --> node_190
    node_436 --> node_743
    node_6 --> node_310
    node_633 --> node_719
    node_538 --> node_528
    node_7 --> node_19
    node_25 --> node_632
    node_44 --> node_603
    node_622 --> node_607
    node_25 --> node_609
    node_621 --> node_341
    node_42 --> node_434
    node_128 --> node_110
    node_42 --> node_395
    node_516 --> node_621
    node_46 --> node_146
    node_7 --> node_476
    node_7 --> node_97
    node_75 --> node_80
    node_638 --> node_645
    node_639 --> node_644
    node_42 --> node_413
    node_181 --> node_176
    node_535 --> node_146
    node_451 --> node_53
    node_424 --> node_275
    node_615 --> node_723
    node_615 --> node_720
    node_249 --> node_298
    node_406 --> node_422
    node_658 --> node_656
    node_214 --> node_267
    node_446 --> node_589
    node_527 --> node_131
    node_46 --> node_643
    node_25 --> node_267
    node_588 --> node_590
    node_6 --> node_338
    node_633 --> node_708
    node_389 --> node_236
    node_6 --> node_207
    node_446 --> node_741
    node_42 --> node_243
    node_258 --> node_287
    node_44 --> node_144
    node_411 --> node_234
    node_125 --> node_224
    node_81 --> node_388
    node_28 --> node_45
    node_150 --> node_353
    node_142 --> node_147
    node_315 --> node_336
    node_396 --> node_366
    node_418 --> node_168
    node_32 --> node_284
    node_424 --> node_327
    node_364 --> node_146
    node_11 --> node_518
    node_258 --> node_215
    node_51 --> node_6
    node_25 --> node_475
    node_51 --> node_672
    node_168 --> node_13
    node_214 --> node_241
    node_25 --> node_270
    node_6 --> node_308
    node_426 --> node_173
    node_446 --> node_596
    node_554 --> node_621
    node_128 --> node_187
    node_27 --> node_618
    node_626 --> node_277
    node_128 --> node_165
    node_25 --> node_241
    node_615 --> node_347
    node_125 --> node_231
    node_32 --> node_174
    node_40 --> node_207
    node_272 --> node_175
    node_516 --> node_522
    node_618 --> node_625
    node_185 --> node_183
    node_265 --> node_264
    node_25 --> node_644
    node_668 --> node_315
    node_446 --> node_386
    node_6 --> node_163
    node_7 --> node_90
    node_42 --> node_222
    node_331 --> node_343
    node_6 --> node_357
    node_258 --> node_155
    node_42 --> node_109
    node_11 --> node_340
    node_448 --> node_474
    node_446 --> node_498
    node_258 --> node_372
    node_258 --> node_151
    node_538 --> node_549
    node_446 --> node_7
    node_377 --> node_364
    node_181 --> node_173
    node_607 --> node_611
    node_191 --> node_189
    node_387 --> node_98
    node_64 --> node_621
    node_615 --> node_700
    node_40 --> node_47
    node_40 --> node_308
    node_446 --> node_694
    node_448 --> node_442
    node_25 --> node_464
    node_32 --> node_304
    node_32 --> node_161
    node_128 --> node_302
    node_468 --> node_417
    node_155 --> node_152
    node_125 --> node_293
    node_505 --> node_171
    node_563 --> node_467
    node_555 --> node_448
    node_125 --> node_150
    node_699 --> node_718
    node_615 --> node_701
    node_374 --> node_147
    node_42 --> node_397
    node_181 --> node_255
    node_6 --> node_361
    node_396 --> node_744
    node_42 --> node_255
    node_452 --> node_460
    node_712 --> node_601
    node_214 --> node_297
    node_42 --> node_247
    node_214 --> node_296
    node_249 --> node_216
    node_628 --> node_630
    node_6 --> node_193
    node_46 --> node_70
    node_181 --> node_179
    node_125 --> node_249
    node_64 --> node_100
    node_258 --> node_214
    node_249 --> node_193
    node_474 --> node_13
    node_415 --> node_181
    node_633 --> node_321
    node_495 --> node_188
    node_621 --> node_346
    node_249 --> node_157
    node_588 --> node_600
    node_42 --> node_586
    node_675 --> node_604
    node_320 --> node_147
    node_446 --> node_454
    node_494 --> node_631
    node_742 --> node_192
    node_32 --> node_289
    node_258 --> node_245
    node_92 --> node_744
    node_621 --> node_342
    node_32 --> node_252
    node_25 --> node_429
    node_214 --> node_257
    node_6 --> node_146
    node_11 --> node_703
    node_125 --> node_181
    node_258 --> node_166
    node_389 --> node_232
    node_128 --> node_159
    node_424 --> node_338
    node_505 --> node_225
    node_398 --> node_169
    node_684 --> node_653
    node_424 --> node_207
    node_191 --> node_634
    node_7 --> node_22
    node_446 --> node_268
    node_40 --> node_193
    node_7 --> node_484
    node_273 --> node_180
    node_396 --> node_360
    node_42 --> node_118
    node_628 --> node_318
    node_59 --> node_68
    node_40 --> node_157
    node_421 --> node_377
    node_393 --> node_161
    node_161 --> node_160
    node_412 --> node_228
    node_44 --> node_659
    node_11 --> node_718
    node_655 --> node_477
    node_272 --> node_293
    node_425 --> node_261
    node_141 --> node_131
    node_47 --> node_98
    node_471 --> node_21
    node_739 --> node_338
    node_446 --> node_21
    node_206 --> node_203
    node_446 --> node_317
    node_531 --> node_729
    node_415 --> node_176
    node_615 --> node_326
    node_671 --> node_188
    node_42 --> node_303
    node_424 --> node_308
    node_446 --> node_75
    node_615 --> node_696
    node_274 --> node_131
    node_11 --> node_630
    node_46 --> node_621
    node_192 --> node_131
    node_446 --> node_2
    node_11 --> node_347
    node_51 --> node_681
    node_249 --> node_320
    node_535 --> node_621
    node_555 --> node_72
    node_42 --> node_427
    node_609 --> node_147
    node_474 --> node_188
    node_249 --> node_266
    node_6 --> node_174
    node_495 --> node_693
    node_455 --> node_649
    node_224 --> node_227
    node_389 --> node_210
    node_249 --> node_294
    node_125 --> node_148
    node_45 --> node_460
    node_214 --> node_169
    node_413 --> node_411
    node_459 --> node_431
    node_25 --> node_98
    node_35 --> node_62
    node_148 --> node_277
    node_11 --> node_633
    node_272 --> node_181
    node_423 --> node_169
    node_468 --> node_426
    node_32 --> node_229
    node_619 --> node_737
    node_671 --> node_146
    node_372 --> node_627
    node_424 --> node_185
    node_25 --> node_175
    node_25 --> node_95
    node_6 --> node_287
    node_214 --> node_313
    node_504 --> node_170
    node_40 --> node_320
    node_13 --> node_9
    node_270 --> node_269
    node_249 --> node_287
    node_430 --> node_147
    node_536 --> node_146
    node_451 --> node_54
    node_389 --> node_276
    node_6 --> node_161
    node_214 --> node_273
    node_11 --> node_701
    node_474 --> node_146
    node_326 --> node_11
    node_169 --> node_170
    node_364 --> node_621
    node_32 --> node_235
    node_631 --> node_720
    node_389 --> node_242
    node_6 --> node_215
    node_459 --> node_6
    node_258 --> node_270
    node_7 --> node_687
    node_372 --> node_146
    node_448 --> node_466
    node_214 --> node_142
    node_359 --> node_147
    node_415 --> node_173
    node_424 --> node_331
    node_431 --> node_315
    node_418 --> node_171
    node_446 --> node_144
    node_555 --> node_588
    node_40 --> node_287
    node_6 --> node_70
    node_270 --> node_432
    node_317 --> node_189
    node_214 --> node_360
    node_258 --> node_524
    node_191 --> node_318
    node_191 --> node_431
    node_372 --> node_601
    node_742 --> node_194
    node_6 --> node_155
    node_42 --> node_172
    node_424 --> node_146
    node_249 --> node_125
    node_272 --> node_176
    node_639 --> node_648
    node_6 --> node_372
    node_6 --> node_151
    node_390 --> node_131
    node_32 --> node_283
    node_480 --> node_593
    node_249 --> node_372
    node_451 --> node_448
    node_214 --> node_288
    node_638 --> node_579
    node_538 --> node_734
    node_214 --> node_191
    node_633 --> node_322
    node_249 --> node_285
    node_25 --> node_741
    node_60 --> node_62
    node_25 --> node_191
    node_389 --> node_234
    node_317 --> node_316
    node_258 --> node_130
    node_414 --> node_284
    node_424 --> node_335
    node_415 --> node_179
    node_609 --> node_607
    node_7 --> node_405
    node_258 --> node_221
    node_584 --> node_583
    node_61 --> node_67
    node_645 --> node_579
    node_40 --> node_155
    node_125 --> node_247
    node_486 --> node_693
    node_40 --> node_372
    node_40 --> node_151
    node_125 --> node_187
    node_25 --> node_182
    node_621 --> node_702
    node_32 --> node_355
    node_125 --> node_165
    node_47 --> node_694
    node_11 --> node_698
    node_270 --> node_626
    node_25 --> node_596
    node_25 --> node_359
    node_6 --> node_214
    node_65 --> node_63
    node_32 --> node_297
    node_32 --> node_296
    node_32 --> node_195
    node_308 --> node_305
    node_606 --> node_604
    node_320 --> node_315
    node_25 --> node_386
    node_621 --> node_327
    node_396 --> node_362
    node_317 --> node_634
    node_422 --> node_153
    node_50 --> node_305
    node_283 --> node_281
    node_538 --> node_435
    node_6 --> node_621
    node_398 --> node_22
    node_6 --> node_245
    node_25 --> node_498
    node_75 --> node_78
    node_25 --> node_540
    node_75 --> node_79
    node_273 --> node_177
    node_411 --> node_743
    node_214 --> node_213
    node_446 --> node_449
    node_25 --> node_7
    node_325 --> node_20
    node_424 --> node_295
    node_42 --> node_379
    node_545 --> node_606
    node_742 --> node_131
    node_6 --> node_166
    node_25 --> node_733
    node_7 --> node_742
    node_11 --> node_606
    node_608 --> node_634
    node_363 --> node_131
    node_424 --> node_259
    node_65 --> node_64
    node_128 --> node_298
    node_415 --> node_178
    node_91 --> node_174
    node_125 --> node_302
    node_742 --> node_193
    node_372 --> node_477
    node_25 --> node_694
    node_451 --> node_13
    node_446 --> node_133
    node_40 --> node_214
    node_555 --> node_373
    node_398 --> node_181
    node_480 --> node_246
    node_555 --> node_478
    node_35 --> node_687
    node_549 --> node_325
    node_148 --> node_432
    node_375 --> node_95
    node_28 --> node_29
    node_40 --> node_621
    node_372 --> node_70
    node_40 --> node_245
    node_389 --> node_271
    node_47 --> node_268
    node_6 --> node_258
    node_6 --> node_14
    node_25 --> node_236
    node_6 --> node_235
    node_462 --> node_379
    node_422 --> node_156
    node_400 --> node_361
    node_458 --> node_403
    node_214 --> node_253
    node_355 --> node_354
    node_528 --> node_63
    node_42 --> node_310
    node_42 --> node_538
    node_25 --> node_458
    node_25 --> node_454
    node_389 --> node_114
    node_365 --> node_612
    node_51 --> node_70
    node_214 --> node_186
    node_47 --> node_317
    node_424 --> node_328
    node_7 --> node_398
    node_459 --> node_357
    node_258 --> node_250
    node_97 --> node_100
    node_389 --> node_260
    node_7 --> node_634
    node_526 --> node_21
    node_693 --> node_70
    node_421 --> node_167
    node_183 --> node_184
    node_265 --> node_263
    node_398 --> node_176
    node_40 --> node_258
    node_249 --> node_267
    node_25 --> node_268
    node_124 --> node_603
    node_258 --> node_175
    node_446 --> node_211
    node_40 --> node_609
    node_478 --> node_663
    node_480 --> node_60
    node_7 --> node_430
    node_32 --> node_169
    node_425 --> node_202
    node_536 --> node_621
    node_42 --> node_384
    node_621 --> node_338
    node_396 --> node_369
    node_11 --> node_527
    node_633 --> node_734
    node_169 --> node_167
    node_32 --> node_352
    node_214 --> node_212
    node_42 --> node_207
    node_32 --> node_313
    node_377 --> node_442
    node_389 --> node_356
    node_616 --> node_625
    node_40 --> node_593
    node_425 --> node_198
    node_451 --> node_588
    node_641 --> node_647
    node_25 --> node_21
    node_25 --> node_317
    node_508 --> node_144
    node_372 --> node_621
    node_14 --> node_380
    node_25 --> node_75
    node_32 --> node_273
    node_419 --> node_242
    node_606 --> node_611
    node_6 --> node_270
    node_421 --> node_169
    node_80 --> node_131
    node_389 --> node_238
    node_491 --> node_739
    node_59 --> node_315
    node_421 --> node_744
    node_417 --> node_215
    node_249 --> node_270
    node_672 --> node_611
    node_567 --> node_321
    node_25 --> node_333
    node_128 --> node_216
    node_249 --> node_241
    node_35 --> node_742
    node_577 --> node_655
    node_598 --> node_594
    node_448 --> node_462
    node_556 --> node_327
    node_6 --> node_524
    node_42 --> node_308
    node_7 --> node_403
    node_128 --> node_193
    node_416 --> node_357
    node_32 --> node_142
    node_615 --> node_706
    node_473 --> node_466
    node_677 --> node_188
    node_424 --> node_166
    node_474 --> node_14
    node_128 --> node_157
    node_480 --> node_476
    node_480 --> node_97
    node_459 --> node_146
    node_42 --> node_163
    node_372 --> node_100
    node_414 --> node_286
    node_589 --> node_592
    node_517 --> node_146
    node_42 --> node_381
    node_40 --> node_270
    node_615 --> node_729
    node_739 --> node_621
    node_394 --> node_742
    node_6 --> node_130
    node_32 --> node_288
    node_51 --> node_605
    node_25 --> node_325
    node_398 --> node_173
    node_412 --> node_222
    node_544 --> node_718
    node_545 --> node_188
    node_6 --> node_221
    node_214 --> node_243
    node_180 --> node_131
    node_389 --> node_208
    node_25 --> node_232
    node_424 --> node_350
    node_574 --> node_736
    node_174 --> node_173
    node_32 --> node_351
    node_258 --> node_182
    node_677 --> node_146
    node_181 --> node_131
    node_417 --> node_149
    node_692 --> node_131
    node_25 --> node_80
    node_32 --> node_224
    node_638 --> node_687
    node_424 --> node_330
    node_25 --> node_144
    node_483 --> node_188
    node_425 --> node_196
    node_555 --> node_28
    node_147 --> node_144
    node_40 --> node_246
    node_234 --> node_174
    node_381 --> node_170
    node_42 --> node_193
    node_28 --> node_43
    node_400 --> node_368
    node_398 --> node_165
    node_669 --> node_723
    node_398 --> node_179
    node_161 --> node_431
    node_673 --> node_695
    node_128 --> node_320
    node_40 --> node_221
    node_50 --> node_146
    node_451 --> node_373
    node_538 --> node_572
    node_573 --> node_706
    node_480 --> node_90
    node_621 --> node_719
    node_426 --> node_180
    node_451 --> node_478
    node_128 --> node_266
    node_52 --> node_56
    node_32 --> node_231
    node_128 --> node_294
    node_258 --> node_249
    node_416 --> node_136
    node_416 --> node_132
    node_49 --> node_435
    node_317 --> node_610
    node_214 --> node_210
    node_10 --> node_445
    node_128 --> node_432
    node_389 --> node_116
    node_461 --> node_582
    node_417 --> node_219
    node_615 --> node_726
    node_504 --> node_168
    node_25 --> node_210
    node_424 --> node_322
    node_621 --> node_601
    node_615 --> node_334
    node_47 --> node_50
    node_181 --> node_180
    node_60 --> node_63
    node_128 --> node_287
    node_11 --> node_693
    node_169 --> node_168
    node_424 --> node_143
    node_557 --> node_725
    node_7 --> node_594
    node_47 --> node_133
    node_621 --> node_708
    node_417 --> node_258
    node_416 --> node_139
    node_6 --> node_292
    node_505 --> node_154
    node_25 --> node_63
    node_214 --> node_255
    node_525 --> node_436
    node_19 --> node_131
    node_398 --> node_178
    node_32 --> node_150
    node_25 --> node_276
    node_459 --> node_70
    node_60 --> node_64
    node_362 --> node_190
    node_148 --> node_99
    node_372 --> node_104
    node_389 --> node_743
    node_615 --> node_329
    node_46 --> node_22
    node_6 --> node_250
    node_25 --> node_242
    node_11 --> node_499
    node_315 --> node_342
    node_409 --> node_291
    node_564 --> node_722
    node_389 --> node_115
    node_273 --> node_175
    node_372 --> node_365
    node_128 --> node_626
    node_609 --> node_603
    node_128 --> node_125
    node_709 --> node_343
    node_621 --> node_722
    node_14 --> node_418
    node_25 --> node_402
    node_6 --> node_175
    node_148 --> node_147
    node_181 --> node_295
    node_25 --> node_133
    node_214 --> node_279
    node_11 --> node_729
    node_128 --> node_372
    node_469 --> node_389
    node_27 --> node_616
    node_724 --> node_601
    node_128 --> node_285
    node_379 --> node_146
    node_509 --> node_305
    node_480 --> node_484
    node_495 --> node_315
    node_40 --> node_476
    node_411 --> node_364
    node_130 --> node_131
    node_63 --> node_621
    node_214 --> node_118
    node_42 --> node_287
    node_702 --> node_11
    node_294 --> node_173
    node_130 --> node_129
    node_14 --> node_414
    node_258 --> node_148
    node_40 --> node_250
    node_32 --> node_212
    node_25 --> node_234
    node_505 --> node_174
    node_191 --> node_626
    node_51 --> node_714
    node_155 --> node_153
    node_11 --> node_337
    node_507 --> node_175
    node_214 --> node_303
    node_40 --> node_175
    node_425 --> node_199
    node_50 --> node_70
    node_42 --> node_215
    node_615 --> node_336
    node_125 --> node_308
    node_25 --> node_718
    node_424 --> node_343
    node_620 --> node_601
    node_25 --> node_403
    node_448 --> node_469
    node_302 --> node_300
    node_459 --> node_621
    node_576 --> node_188
    node_529 --> node_348
    node_11 --> node_552
    node_446 --> node_72
    node_621 --> node_70
    node_448 --> node_451
    node_294 --> node_179
    node_517 --> node_621
    node_393 --> node_160
    node_54 --> node_13
    node_80 --> node_621
    node_42 --> node_155
    node_446 --> node_184
    node_258 --> node_110
    node_458 --> node_743
    node_621 --> node_328
    node_25 --> node_211
    node_606 --> node_642
    node_42 --> node_372
    node_25 --> node_347
    node_42 --> node_151
    node_621 --> node_321
    node_164 --> node_102
    node_320 --> node_316
    node_682 --> node_146
    node_57 --> node_472
    node_190 --> node_131
    node_249 --> node_191
    node_375 --> node_171
    node_459 --> node_605
    node_633 --> node_695
    node_139 --> node_131
    node_468 --> node_420
    node_128 --> node_278
    node_163 --> node_744
    node_451 --> node_28
    node_615 --> node_725
    node_590 --> node_14
    node_6 --> node_616
    node_80 --> node_68
    node_59 --> node_80
    node_155 --> node_156
    node_317 --> node_146
    node_32 --> node_243
    node_381 --> node_167
    node_249 --> node_182
    node_389 --> node_280
    node_389 --> node_237
    node_565 --> node_659
    node_434 --> node_435
    node_40 --> node_741
    node_249 --> node_359
    node_615 --> node_332
    node_191 --> node_621
    node_389 --> node_284
    node_125 --> node_193
    node_161 --> node_357
    node_400 --> node_370
    node_448 --> node_445
    node_637 --> node_69
    node_233 --> node_166
    node_6 --> node_293
    node_42 --> node_214
    node_125 --> node_157
    node_20 --> node_22
    node_294 --> node_178
    node_25 --> node_271
    node_72 --> node_73
    node_417 --> node_220
    node_446 --> node_588
    node_142 --> node_431
    node_486 --> node_315
    node_7 --> node_387
    node_42 --> node_391
    node_509 --> node_239
    node_214 --> node_172
    node_46 --> node_592
    node_42 --> node_245
    node_40 --> node_182
    node_25 --> node_401
    node_196 --> node_742
    node_415 --> node_180
    node_6 --> node_249
    node_482 --> node_617
    node_694 --> node_70
    node_40 --> node_596
    node_50 --> node_605
    node_446 --> node_15
    node_40 --> node_359
    node_32 --> node_222
    node_25 --> node_114
    node_42 --> node_166
    node_376 --> node_98
    node_560 --> node_322
    node_128 --> node_267
    node_42 --> node_394
    node_482 --> node_315
    node_25 --> node_260
    node_40 --> node_386
    node_411 --> node_257
    node_598 --> node_591
    node_25 --> node_45
    node_406 --> node_385
    node_40 --> node_498
    node_25 --> node_536
    node_416 --> node_138
    node_50 --> node_14
    node_425 --> node_263
    node_40 --> node_7
    node_6 --> node_181
    node_424 --> node_209
    node_504 --> node_171
    node_29 --> node_315
    node_389 --> node_128
    node_480 --> node_109
    node_7 --> node_107
    node_606 --> node_654
    node_22 --> node_592
    node_249 --> node_236
    node_555 --> node_580
    node_681 --> node_714
    node_400 --> node_365
    node_258 --> node_302
    node_25 --> node_441
    node_42 --> node_258
    node_42 --> node_14
    node_172 --> node_277
    node_214 --> node_356
    node_258 --> node_276
    node_169 --> node_171
    node_537 --> node_329
    node_32 --> node_397
    node_615 --> node_345
    node_609 --> node_634
    node_42 --> node_609
    node_25 --> node_356
    node_125 --> node_320
    node_11 --> node_336
    node_32 --> node_255
    node_128 --> node_270
    node_315 --> node_327
    node_36 --> node_188
    node_32 --> node_247
    node_32 --> node_742
    node_258 --> node_242
    node_305 --> node_693
    node_501 --> node_315
    node_128 --> node_241
    node_668 --> node_188
    node_550 --> node_712
    node_270 --> node_694
    node_125 --> node_294
    node_633 --> node_340
    node_25 --> node_238
    node_418 --> node_174
    node_97 --> node_93
    node_42 --> node_593
    node_389 --> node_289
    node_35 --> node_277
    node_374 --> node_431
    node_6 --> node_268
    node_389 --> node_252
    node_633 --> node_342
    node_148 --> node_315
    node_412 --> node_227
    node_408 --> node_447
    node_666 --> node_315
    node_382 --> node_744
    node_379 --> node_621
    node_508 --> node_277
    node_448 --> node_470
    node_433 --> node_70
    node_125 --> node_287
    node_32 --> node_279
    node_150 --> node_355
    node_389 --> node_278
    node_446 --> node_373
    node_6 --> node_317
    node_25 --> node_606
    node_480 --> node_586
    node_535 --> node_63
    node_668 --> node_146
    node_6 --> node_148
    node_411 --> node_744
    node_446 --> node_478
    node_25 --> node_448
    node_258 --> node_234
    node_621 --> node_322
    node_32 --> node_118
    node_278 --> node_277
    node_214 --> node_311
    node_214 --> node_208
    node_622 --> node_146
    node_424 --> node_293
    node_491 --> node_188
    node_425 --> node_265
    node_42 --> node_270
    node_25 --> node_208
    node_381 --> node_168
    node_292 --> node_290
    node_32 --> node_303
    node_214 --> node_310
    node_441 --> node_18
    node_416 --> node_140
    node_236 --> node_278
    node_42 --> node_524
    node_682 --> node_621
    node_272 --> node_294
    node_6 --> node_110
    node_40 --> node_75
    node_125 --> node_372
    node_444 --> node_605
    node_7 --> node_591
    node_472 --> node_468
    node_125 --> node_285
    node_396 --> node_361
    node_411 --> node_360
    node_563 --> node_464
    node_128 --> node_257
    node_389 --> node_229
    node_14 --> node_424
    node_25 --> node_374
    node_42 --> node_246
    node_52 --> node_54
    node_712 --> node_742
    node_720 --> node_619
    node_480 --> node_430
    node_147 --> node_277
    node_317 --> node_621
    node_42 --> node_130
    node_135 --> node_131
    node_295 --> node_131
    node_545 --> node_607
    node_6 --> node_707
    node_249 --> node_232
    node_411 --> node_191
    node_577 --> node_654
    node_609 --> node_431
    node_42 --> node_221
    node_580 --> node_583
    node_214 --> node_116
    node_626 --> node_144
    node_570 --> node_688
    node_494 --> node_629
    node_25 --> node_116
    node_7 --> node_516
    node_40 --> node_110
    node_25 --> node_527
    node_61 --> node_66
    node_714 --> node_189
    node_562 --> node_698
    node_667 --> node_146
    node_125 --> node_214
    node_621 --> node_714
    node_415 --> node_177
    node_142 --> node_357
    node_258 --> node_271
    node_552 --> node_715
    node_637 --> node_640
    node_25 --> node_72
    node_417 --> node_150
    node_536 --> node_687
    node_40 --> node_232
    node_6 --> node_742
    node_50 --> node_81
    node_125 --> node_245
    node_468 --> node_418
    node_6 --> node_187
    node_25 --> node_184
    node_6 --> node_165
    node_320 --> node_610
    node_150 --> node_352
    node_405 --> node_410
    node_418 --> node_177
    node_258 --> node_114
    node_418 --> node_166
    node_42 --> node_60
    node_47 --> node_188
    node_214 --> node_163
    node_615 --> node_733
    node_40 --> node_144
    node_32 --> node_172
    node_46 --> node_633
    node_25 --> node_743
    node_474 --> node_411
    node_534 --> node_388
    node_14 --> node_422
    node_258 --> node_260
    node_451 --> node_580
    node_214 --> node_115
    node_527 --> node_718
    node_359 --> node_431
    node_249 --> node_210
    node_424 --> node_317
    node_540 --> node_274
    node_641 --> node_646
    node_424 --> node_148
    node_555 --> node_434
    node_283 --> node_282
    node_701 --> node_22
    node_555 --> node_413
    node_574 --> node_349
    node_615 --> node_735
    node_6 --> node_63
    node_51 --> node_687
    node_6 --> node_302
    node_398 --> node_180
    node_25 --> node_604
    node_389 --> node_355
    node_448 --> node_14
    node_621 --> node_734
    node_249 --> node_276
    node_214 --> node_361
    node_25 --> node_188
    node_42 --> node_292
    node_538 --> node_681
    node_40 --> node_697
    node_389 --> node_297
    node_25 --> node_588
    node_389 --> node_195
    node_389 --> node_296
    node_426 --> node_175
    node_446 --> node_28
    node_374 --> node_357
    node_545 --> node_315
    node_559 --> node_14
    node_42 --> node_476
    node_42 --> node_97
    node_249 --> node_242
    node_11 --> node_315
    node_44 --> node_579
    node_596 --> node_600
    node_505 --> node_169
    node_315 --> node_719
    node_300 --> node_594
    node_631 --> node_625
    node_42 --> node_250
    node_422 --> node_154
    node_25 --> node_15
    node_505 --> node_744
    node_142 --> node_132
    node_6 --> node_133
    node_75 --> node_77
    node_52 --> node_13
    node_302 --> node_299
    node_7 --> node_609
    node_615 --> node_348
    node_6 --> node_720
    node_40 --> node_276
    node_50 --> node_435
    node_150 --> node_351
    node_181 --> node_175
    node_396 --> node_368
    node_42 --> node_175
    node_431 --> node_146
    node_320 --> node_357
    node_741 --> node_743
    node_128 --> node_191
    node_492 --> node_189
    node_458 --> node_436
    node_6 --> node_159
    node_148 --> node_603
    node_413 --> node_421
    node_551 --> node_338
    node_25 --> node_266
    node_446 --> node_147
    node_40 --> node_242
    node_258 --> node_298
    node_161 --> node_158
    node_6 --> node_234
    node_506 --> node_102
    node_57 --> node_62
    node_42 --> node_400
    node_249 --> node_234
    node_622 --> node_621
    node_555 --> node_109
    node_315 --> node_708
    node_58 --> node_146
    node_424 --> node_183
    node_50 --> node_388
    node_409 --> node_271
    node_676 --> node_146
    node_633 --> node_696
    node_71 --> node_10
    node_419 --> node_312
    node_125 --> node_270
    node_40 --> node_430
    node_128 --> node_182
    node_91 --> node_173
    node_516 --> node_520
    node_125 --> node_241
    node_206 --> node_197
    node_570 --> node_651
    node_498 --> node_503
    node_411 --> node_362
    node_224 --> node_223
    node_128 --> node_359
    node_406 --> node_411
    node_615 --> node_333
    node_25 --> node_693
    node_40 --> node_615
    node_270 --> node_133
    node_589 --> node_591
    node_621 --> node_715
    node_11 --> node_608
    node_424 --> node_165
    node_25 --> node_280
    node_42 --> node_90
    node_381 --> node_171
    node_6 --> node_535
    node_25 --> node_237
    node_63 --> node_58
    node_615 --> node_721
    node_590 --> node_22
    node_32 --> node_310
    node_25 --> node_284
    node_40 --> node_234
    node_538 --> node_146
    node_615 --> node_730
    node_467 --> node_69
    node_241 --> node_239
    node_214 --> node_174
    node_424 --> node_340
    node_11 --> node_733
    node_49 --> node_379
    node_94 --> node_63
    node_42 --> node_741
    node_64 --> node_131
    node_420 --> node_228
    node_737 --> node_621
    node_51 --> node_697
    node_609 --> node_357
    node_615 --> node_339
    node_389 --> node_169
    node_91 --> node_179
    node_25 --> node_373
    node_6 --> node_44
    node_210 --> node_209
    node_70 --> node_184
    node_128 --> node_694
    node_389 --> node_744
    node_320 --> node_146
    node_615 --> node_325
    node_25 --> node_478
    node_181 --> node_254
    node_106 --> node_131
    node_125 --> node_221
    node_389 --> node_352
    node_505 --> node_224
    node_448 --> node_473
    node_389 --> node_313
    node_555 --> node_586
    node_40 --> node_211
    node_667 --> node_621
    node_32 --> node_207
    node_451 --> node_56
    node_42 --> node_182
    node_389 --> node_273
    node_214 --> node_304
    node_214 --> node_161
    node_532 --> node_337
    node_128 --> node_236
    node_294 --> node_180
    node_430 --> node_357
    node_493 --> node_743
    node_249 --> node_271
    node_25 --> node_128
    node_194 --> node_192
    node_214 --> node_215
    node_42 --> node_386
    node_609 --> node_627
    node_60 --> node_9
    node_612 --> node_620
    node_389 --> node_142
    node_372 --> node_615
    node_25 --> node_337
    node_258 --> node_216
    node_451 --> node_434
    node_389 --> node_360
    node_32 --> node_308
    node_25 --> node_9
    node_372 --> node_665
    node_315 --> node_321
    node_91 --> node_178
    node_249 --> node_114
    node_451 --> node_413
    node_446 --> node_444
    node_411 --> node_369
    node_448 --> node_457
    node_214 --> node_151
    node_42 --> node_249
    node_42 --> node_22
    node_538 --> node_559
    node_638 --> node_69
    node_128 --> node_268
    node_42 --> node_484
    node_129 --> node_131
    node_32 --> node_163
    node_138 --> node_131
    node_214 --> node_289
    node_394 --> node_258
    node_249 --> node_260
    node_389 --> node_288
    node_398 --> node_177
    node_40 --> node_271
    node_398 --> node_166
    node_294 --> node_174
    node_555 --> node_582
    node_609 --> node_146
    node_459 --> node_317
    node_424 --> node_240
    node_418 --> node_169
    node_25 --> node_252
    node_14 --> node_416
    node_224 --> node_226
    node_492 --> node_630
    node_25 --> node_663
    node_576 --> node_315
    node_7 --> node_429
    node_739 --> node_720
    node_389 --> node_351
    node_372 --> node_630
    node_128 --> node_317
    node_59 --> node_188
    node_40 --> node_114
    node_42 --> node_423
    node_389 --> node_224
    node_25 --> node_278
    node_249 --> node_356
    node_451 --> node_55
    node_446 --> node_744
    node_40 --> node_260
    node_191 --> node_268
    node_364 --> node_277
    node_615 --> node_739
    node_409 --> node_290
    node_11 --> node_333
    node_638 --> node_639
    node_32 --> node_361
    node_415 --> node_175
    node_36 --> node_625
    node_488 --> node_661
    node_674 --> node_315
    node_424 --> node_347
    node_249 --> node_238
    node_32 --> node_193
    node_110 --> node_114
    node_492 --> node_318
    node_25 --> node_645
    node_276 --> node_131
    node_468 --> node_424
    node_396 --> node_370
    node_389 --> node_231
    node_431 --> node_621
    node_191 --> node_317
    node_494 --> node_616
    node_410 --> node_356
    node_125 --> node_175
    node_258 --> node_320
    node_355 --> node_353
    node_372 --> node_318
    node_451 --> node_109
    node_11 --> node_711
    node_214 --> node_166
    node_542 --> node_611
    node_25 --> node_472
    node_234 --> node_173
    node_423 --> node_166
    node_258 --> node_266
    node_134 --> node_131
    node_65 --> node_315
    node_6 --> node_298
    node_51 --> node_633
    node_258 --> node_294
    node_11 --> node_325
    node_40 --> node_238
    node_50 --> node_687
    node_58 --> node_621
    node_615 --> node_703
    node_214 --> node_229
    node_424 --> node_318
    node_676 --> node_621
    node_471 --> node_396
    node_128 --> node_232
    node_7 --> node_102
    node_25 --> node_229
    node_42 --> node_148
    node_42 --> node_75
    node_480 --> node_107
    node_621 --> node_695
    node_621 --> node_687
    node_47 --> node_147
    node_446 --> node_580
    node_606 --> node_638
    node_249 --> node_208
    node_25 --> node_28
    node_308 --> node_306
    node_214 --> node_235
    node_234 --> node_179
    node_258 --> node_280
    node_615 --> node_718
    node_467 --> node_637
    node_258 --> node_237
    node_459 --> node_742
    node_538 --> node_621
    node_389 --> node_253
    node_40 --> node_298
    node_258 --> node_284
    node_124 --> node_122
    node_396 --> node_365
    node_11 --> node_573
    node_471 --> node_388
    node_133 --> node_132
    node_389 --> node_186
    node_619 --> node_625
    node_25 --> node_336
    node_468 --> node_422
    node_424 --> node_260
    node_505 --> node_223
    node_609 --> node_70
    node_451 --> node_586
    node_125 --> node_191
    node_42 --> node_110
    node_405 --> node_385
    node_538 --> node_529
    node_6 --> node_277
    node_11 --> node_728
    node_555 --> node_702
    node_622 --> node_606
    node_97 --> node_101
    node_25 --> node_147
    node_317 --> node_314
    node_609 --> node_622
    node_36 --> node_315
    node_214 --> node_283
    node_258 --> node_125
    node_464 --> node_91
    node_63 --> node_64
    node_42 --> node_405
    node_217 --> node_95
    node_128 --> node_210
    node_294 --> node_177
    node_7 --> node_589
    node_419 --> node_313
    node_17 --> node_50
    node_14 --> node_408
    node_25 --> node_436
    node_621 --> node_623
    node_315 --> node_322
    node_459 --> node_63
    node_125 --> node_182
    node_389 --> node_212
    node_258 --> node_285
    node_14 --> node_412
    node_249 --> node_116
    node_621 --> node_731
    node_32 --> node_287
    node_125 --> node_359
    node_7 --> node_741
    node_78 --> node_131
    node_61 --> node_63
    node_412 --> node_130
    node_234 --> node_178
    node_233 --> node_165
    node_424 --> node_326
    node_387 --> node_744
    node_642 --> node_648
    node_258 --> node_128
    node_25 --> node_471
    node_40 --> node_277
    node_621 --> node_183
    node_446 --> node_490
    node_155 --> node_154
    node_128 --> node_276
    node_417 --> node_192
    node_214 --> node_355
    node_505 --> node_222
    node_621 --> node_189
    node_638 --> node_637
    node_32 --> node_215
    node_6 --> node_216
    node_25 --> node_355
    node_359 --> node_626
    node_128 --> node_242
    node_214 --> node_524
    node_64 --> node_68
    node_462 --> node_405
    node_11 --> node_349
    node_214 --> node_195
    node_602 --> node_614
    node_505 --> node_173
    node_7 --> node_596
    node_42 --> node_187
    node_35 --> node_654
    node_42 --> node_165
    node_25 --> node_297
    node_25 --> node_296
    node_25 --> node_195
    node_65 --> node_58
    node_609 --> node_621
    node_6 --> node_157
    node_64 --> node_363
    node_491 --> node_315
    node_32 --> node_155
    node_7 --> node_386
    node_128 --> node_133
    node_459 --> node_159
    node_258 --> node_252
    node_621 --> node_340
    node_40 --> node_72
    node_32 --> node_372
    node_32 --> node_151
    node_413 --> node_423
    node_555 --> node_538
    node_7 --> node_498
    node_446 --> node_437
    node_550 --> node_332
    node_214 --> node_130
    node_375 --> node_170
    node_191 --> node_190
    node_27 --> node_693
    node_125 --> node_236
    node_418 --> node_181
    node_25 --> node_257
    node_6 --> node_604
    node_389 --> node_243
    node_40 --> node_216
    node_678 --> node_601
    node_505 --> node_742
    node_615 --> node_712
    node_258 --> node_278
    node_461 --> node_17
    node_128 --> node_234
    node_505 --> node_179
    node_480 --> node_516
    node_42 --> node_302
    node_315 --> node_714
    node_505 --> node_226
    node_25 --> node_607
    node_81 --> node_458
    node_547 --> node_324
    node_191 --> node_133
    node_372 --> node_277
    node_495 --> node_146
    node_42 --> node_398
    node_42 --> node_242
    node_40 --> node_107
    node_25 --> node_506
    node_570 --> node_654
    node_32 --> node_214
    node_206 --> node_204
    node_448 --> node_463
    node_191 --> node_159
    node_424 --> node_277
    node_6 --> node_320
    node_7 --> node_105
    node_424 --> node_145
    node_389 --> node_222
    node_42 --> node_430
    node_429 --> node_428
    node_448 --> node_468
    node_633 --> node_726
    node_6 --> node_266
    node_32 --> node_245
    node_29 --> node_13
    node_6 --> node_294
    node_29 --> node_404
    node_418 --> node_176
    node_411 --> node_371
    node_478 --> node_479
    node_621 --> node_615
    node_32 --> node_166
    node_398 --> node_175
    node_464 --> node_467
    node_6 --> node_432
    node_258 --> node_267
    node_505 --> node_178
    node_462 --> node_398
    node_42 --> node_234
    node_446 --> node_603
    node_558 --> node_345
    node_606 --> node_610
    node_25 --> node_169
    node_47 --> node_315
    node_214 --> node_352
    node_315 --> node_734
    node_510 --> node_5
    node_42 --> node_389
    node_538 --> node_714
    node_25 --> node_744
    node_191 --> node_630
    node_617 --> node_625
    node_420 --> node_225
    node_25 --> node_352
    node_421 --> node_166
    node_25 --> node_313
    node_161 --> node_268
    node_534 --> node_379
    node_214 --> node_292
    node_389 --> node_255
    node_424 --> node_354
    node_40 --> node_266
    node_578 --> node_717
    node_417 --> node_194
    node_42 --> node_403
    node_32 --> node_258
    node_486 --> node_188
    node_389 --> node_247
    node_40 --> node_294
    node_249 --> node_280
    node_670 --> node_724
    node_249 --> node_237
    node_128 --> node_271
    node_633 --> node_330
    node_25 --> node_273
    node_249 --> node_284
    node_7 --> node_75
    node_621 --> node_630
    node_125 --> node_110
    node_409 --> node_289
    node_42 --> node_211
    node_424 --> node_157
    node_381 --> node_743
    node_161 --> node_317
    node_683 --> node_606
    node_258 --> node_241
    node_412 --> node_224
    node_372 --> node_604
    node_482 --> node_188
    node_25 --> node_315
    node_480 --> node_609
    node_25 --> node_142
    node_128 --> node_114
    node_147 --> node_315
    node_333 --> node_189
    node_6 --> node_626
    node_6 --> node_125
    node_590 --> node_594
    node_125 --> node_232
    node_302 --> node_301
    node_389 --> node_279
    node_40 --> node_280
    node_25 --> node_360
    node_405 --> node_423
    node_128 --> node_260
    node_29 --> node_188
    node_40 --> node_237
    node_114 --> node_113
    node_231 --> node_230
    node_150 --> node_192
    node_416 --> node_137
    node_418 --> node_173
    node_40 --> node_284
    node_148 --> node_357
    node_6 --> node_285
    node_512 --> node_21
    node_389 --> node_118
    node_606 --> node_184
    node_615 --> node_740
    node_52 --> node_220
    node_25 --> node_580
    node_25 --> node_288
    node_495 --> node_70
    node_621 --> node_318
    node_193 --> node_194
    node_11 --> node_532
    node_6 --> node_128
    node_560 --> node_696
    node_42 --> node_383
    node_501 --> node_188
    node_621 --> node_701
    node_741 --> node_744
    node_214 --> node_351
    node_571 --> node_738
    node_249 --> node_128
    node_448 --> node_183
    node_482 --> node_146
    node_728 --> node_321
    node_40 --> node_478
    node_42 --> node_271
    node_92 --> node_150
    node_128 --> node_356
    node_257 --> node_256
    node_25 --> node_351
    node_40 --> node_125
    node_389 --> node_303
    node_533 --> node_331
    node_245 --> node_244
    node_214 --> node_224
    node_32 --> node_270
    node_25 --> node_388
    node_50 --> node_6
    node_148 --> node_188
    node_448 --> node_467
    node_451 --> node_227
    node_417 --> node_216
    node_91 --> node_180
    node_393 --> node_158
    node_128 --> node_238
    node_258 --> node_296
    node_40 --> node_516
    node_42 --> node_401
    node_418 --> node_179
    node_40 --> node_285
    node_418 --> node_165
    node_424 --> node_320
    node_516 --> node_315
    node_11 --> node_327
    node_526 --> node_474
    node_417 --> node_193
    node_42 --> node_114
    node_424 --> node_266
    node_32 --> node_524
    node_239 --> node_605
    node_50 --> node_379
    node_28 --> node_38
    node_125 --> node_210
    node_424 --> node_294
    node_375 --> node_167
    node_40 --> node_128
    node_42 --> node_260
    node_249 --> node_252
    node_657 --> node_661
    node_214 --> node_231
    node_372 --> node_693
    node_258 --> node_257
    node_239 --> node_14
    node_11 --> node_657
    node_204 --> node_198
    node_433 --> node_5
    node_294 --> node_175
    node_419 --> node_243
    node_32 --> node_130
    node_527 --> node_336
    node_6 --> node_278
    node_148 --> node_146
    node_81 --> node_63
    node_188 --> node_189
    node_588 --> node_595
    node_666 --> node_146
    node_320 --> node_319
    node_125 --> node_276
    node_249 --> node_278
    node_32 --> node_221
    node_400 --> node_367
    node_51 --> node_693
    node_372 --> node_624
    node_375 --> node_169
    node_633 --> node_714
    node_40 --> node_252
    node_128 --> node_208
    node_125 --> node_242
    node_621 --> node_326
    node_14 --> node_420
    node_418 --> node_178
    node_416 --> node_358
    node_11 --> node_561
    node_411 --> node_188
    node_554 --> node_315
    node_214 --> node_293
    node_509 --> node_183
    node_621 --> node_696
    node_214 --> node_150
    node_411 --> node_361
    node_319 --> node_131
    node_28 --> node_25
    node_6 --> node_329
    node_42 --> node_382
    node_11 --> node_487
    node_11 --> node_560
    node_11 --> node_546
    node_606 --> node_643
    node_548 --> node_708
    node_40 --> node_278
    node_389 --> node_172
    node_36 --> node_189
    node_25 --> node_253
    node_214 --> node_249
    node_615 --> node_719
    node_25 --> node_437
    node_317 --> node_630
    node_333 --> node_630
    node_25 --> node_186
    node_508 --> node_603
    node_638 --> node_648
    node_446 --> node_582
    node_592 --> node_22
    node_64 --> node_315
    node_406 --> node_420
    node_683 --> node_188
    node_42 --> node_298
    node_6 --> node_267
    node_7 --> node_50
    node_11 --> node_567
    node_125 --> node_234
    node_172 --> node_144
    node_570 --> node_658
    node_671 --> node_621
    node_504 --> node_167
    node_249 --> node_229
    node_480 --> node_429
    node_633 --> node_344
    node_705 --> node_337
    node_214 --> node_181
    node_128 --> node_116
    node_258 --> node_313
    node_505 --> node_227
    node_474 --> node_621
    node_161 --> node_133
    node_101 --> node_131
    node_633 --> node_724
    node_35 --> node_144
    node_538 --> node_540
    node_615 --> node_708
    node_25 --> node_212
    node_412 --> node_223
    node_258 --> node_273
    node_444 --> node_6
    node_421 --> node_376
    node_372 --> node_663
    node_546 --> node_347
    node_32 --> node_292
    node_25 --> node_362
    node_317 --> node_318
    node_333 --> node_318
    node_206 --> node_205
    node_40 --> node_364
    node_40 --> node_267
    node_504 --> node_169
    node_161 --> node_159
    node_7 --> node_389
    node_6 --> node_241
    node_28 --> node_26
    node_320 --> node_314
    node_6 --> node_644
    node_40 --> node_28
    node_32 --> node_250
    node_124 --> node_123
    node_258 --> node_360
    node_461 --> node_183
    node_509 --> node_582
    node_615 --> node_722
    node_278 --> node_144
    node_97 --> node_99
    node_128 --> node_115
    node_375 --> node_168
    node_32 --> node_175
    node_606 --> node_69
    node_25 --> node_603
    node_424 --> node_278
    node_25 --> node_413
    node_147 --> node_603
    node_7 --> node_211
    node_424 --> node_334
    node_315 --> node_695
    node_258 --> node_191
    node_296 --> node_295
    node_372 --> node_363
    node_234 --> node_180
    node_214 --> node_148
    node_413 --> node_417
    node_615 --> node_709
    node_529 --> node_734
    node_40 --> node_241
    node_150 --> node_193
    node_91 --> node_177
    node_389 --> node_311
    node_125 --> node_271
    node_416 --> node_131
    node_685 --> node_654
    node_25 --> node_568
    node_11 --> node_188
    node_294 --> node_181
    node_42 --> node_72
    node_25 --> node_243
    node_300 --> node_589
    node_374 --> node_268
    node_434 --> node_433
    node_446 --> node_431
    node_558 --> node_730
    node_372 --> node_629
    node_42 --> node_387
    node_92 --> node_742
    node_27 --> node_619
    node_28 --> node_605
    node_249 --> node_355
    node_270 --> node_147
    node_424 --> node_329
    node_452 --> node_442
    node_47 --> node_40
    node_389 --> node_310
    node_498 --> node_496
    node_258 --> node_359
    node_488 --> node_651
    node_424 --> node_170
    node_535 --> node_315
    node_405 --> node_425
    node_125 --> node_114
    node_42 --> node_216
    node_615 --> node_337
    node_249 --> node_297
    node_249 --> node_296
    node_249 --> node_195
    node_372 --> node_364
    node_631 --> node_338
    node_97 --> node_104
    node_571 --> node_350
    node_124 --> node_121
    node_125 --> node_260
    node_374 --> node_317
    node_464 --> node_426
    node_11 --> node_719
    node_42 --> node_157
    node_64 --> node_105
    node_188 --> node_318
    node_621 --> node_331
    node_545 --> node_146
    node_615 --> node_321
    node_6 --> node_257
    node_11 --> node_146
    node_459 --> node_432
    node_214 --> node_222
    node_645 --> node_687
    node_680 --> node_636
    node_436 --> node_435
    node_674 --> node_606
    node_42 --> node_107
    node_249 --> node_257
    node_412 --> node_226
    node_25 --> node_222
    node_11 --> node_738
    node_555 --> node_593
    node_476 --> node_475
    node_40 --> node_297
    node_40 --> node_296
    node_400 --> node_372
    node_389 --> node_207
    node_436 --> node_323
    node_539 --> node_324
    node_294 --> node_176
    node_480 --> node_741
    node_483 --> node_146
    node_364 --> node_315
    node_7 --> node_45
    node_444 --> node_459
    node_11 --> node_708
    node_424 --> node_336
    node_125 --> node_238
    node_40 --> node_429
    node_315 --> node_189
    node_258 --> node_236
    node_446 --> node_448
    node_40 --> node_257
    node_128 --> node_280
    node_424 --> node_241
    node_128 --> node_237
    node_618 --> node_615
    node_431 --> node_189
    node_389 --> node_233
    node_32 --> node_293
    node_128 --> node_284
    node_389 --> node_308
    node_425 --> node_203
    node_214 --> node_247
    node_25 --> node_255
    node_214 --> node_187
    node_258 --> node_253
    node_480 --> node_596
    node_214 --> node_165
    node_25 --> node_247
    node_191 --> node_432
    node_423 --> node_165
    node_42 --> node_320
    node_459 --> node_626
    node_701 --> node_14
    node_315 --> node_340
    node_258 --> node_186
    node_389 --> node_163
    node_609 --> node_268
    node_417 --> node_217
    node_480 --> node_386
    node_42 --> node_266
    node_380 --> node_237
    node_409 --> node_288
    node_125 --> node_298
    node_181 --> node_294
    node_32 --> node_249
    node_194 --> node_98
    node_42 --> node_294
    node_413 --> node_426
    node_183 --> node_69
    node_480 --> node_498
    node_505 --> node_180
    node_446 --> node_538
    node_670 --> node_340
    node_632 --> node_70
    node_480 --> node_7
    node_417 --> node_267
    node_249 --> node_169
    node_52 --> node_55
    node_624 --> node_625
    node_609 --> node_317
    node_125 --> node_208
    node_25 --> node_279
    node_249 --> node_352
    node_249 --> node_313
    node_411 --> node_229
    node_214 --> node_302
    node_32 --> node_181
    node_39 --> node_102
    node_424 --> node_332
    node_535 --> node_58
    node_555 --> node_246
    node_25 --> node_118
    node_448 --> node_101
    node_7 --> node_448
    node_389 --> node_361
    node_42 --> node_280
    node_451 --> node_52
    node_249 --> node_273
    node_42 --> node_237
    node_97 --> node_102
    node_97 --> node_98
    node_42 --> node_284
    node_379 --> node_520
    node_406 --> node_421
    node_530 --> node_295
    node_40 --> node_169
    node_431 --> node_634
    node_97 --> node_95
    node_400 --> node_363
    node_417 --> node_270
    node_446 --> node_13
    node_6 --> node_315
    node_142 --> node_159
    node_633 --> node_348
    node_320 --> node_189
    node_359 --> node_268
    node_148 --> node_143
    node_621 --> node_706
    node_624 --> node_619
    node_679 --> node_606
    node_13 --> node_474
    node_25 --> node_303
    node_11 --> node_70
    node_40 --> node_313
    node_249 --> node_142
    node_606 --> node_637
    node_575 --> node_731
    node_482 --> node_625
    node_621 --> node_624
    node_234 --> node_177
    node_666 --> node_188
    node_249 --> node_360
    node_11 --> node_321
    node_40 --> node_273
    node_42 --> node_125
    node_128 --> node_289
    node_446 --> node_585
    node_128 --> node_252
    node_28 --> node_39
    node_125 --> node_116
    node_359 --> node_317
    node_6 --> node_191
    node_150 --> node_149
    node_25 --> node_638
    node_249 --> node_288
    node_42 --> node_516
    node_46 --> node_21
    node_536 --> node_654
    node_42 --> node_285
    node_555 --> node_60
    node_424 --> node_344
    node_40 --> node_315
    node_646 --> node_579
    node_446 --> node_357
    node_32 --> node_148
    node_419 --> node_311
    node_258 --> node_232
    node_633 --> node_333
    node_674 --> node_188
    node_424 --> node_345
    node_42 --> node_128
    node_677 --> node_621
    node_40 --> node_360
    node_249 --> node_351
    node_424 --> node_167
    node_140 --> node_131
    node_576 --> node_146
    node_6 --> node_182
    node_633 --> node_721
    node_374 --> node_133
    node_694 --> node_693
    node_451 --> node_609
    node_49 --> node_458
    node_11 --> node_566
    node_249 --> node_224
    node_6 --> node_359
    node_315 --> node_630
    node_125 --> node_216
    node_505 --> node_155
    node_419 --> node_310
    node_7 --> node_13
    node_239 --> node_22
    node_7 --> node_404
    node_40 --> node_288
    node_372 --> node_98
    node_480 --> node_75
    node_505 --> node_151
    node_40 --> node_191
    node_431 --> node_630
    node_320 --> node_634
    node_110 --> node_113
    node_11 --> node_705
    node_374 --> node_159
    node_47 --> node_431
    node_50 --> node_621
    node_451 --> node_593
    node_65 --> node_188
    node_7 --> node_72
    node_389 --> node_174
    node_606 --> node_607
    node_633 --> node_325
    node_32 --> node_110
    node_713 --> node_606
    node_555 --> node_476
    node_249 --> node_231
    node_555 --> node_97
    node_451 --> node_71
    node_536 --> node_315
    node_405 --> node_426
    node_45 --> node_452
    node_381 --> node_169
    node_25 --> node_172
    node_6 --> node_694
    node_483 --> node_621
    node_621 --> node_726
    node_381 --> node_744
    node_315 --> node_318
    node_128 --> node_229
    node_320 --> node_159
    node_555 --> node_17
    node_258 --> node_210
    node_615 --> node_346
    node_188 --> node_131
    node_42 --> node_278
    node_25 --> node_57
    node_621 --> node_334
    node_315 --> node_701
    node_372 --> node_315
    node_431 --> node_318
    node_245 --> node_131
    node_637 --> node_639
    node_615 --> node_324
    node_389 --> node_304
    node_389 --> node_161
    node_91 --> node_175
    node_25 --> node_431
    node_233 --> node_170
    node_418 --> node_180
    node_411 --> node_366
    node_654 --> node_656
    node_11 --> node_549
    node_6 --> node_236
    node_97 --> node_162
    node_6 --> node_58
    node_538 --> node_535
    node_14 --> node_411
    node_389 --> node_215
    node_424 --> node_315
    node_407 --> node_744
    node_714 --> node_630
    node_505 --> node_177
    node_505 --> node_166
    node_6 --> node_253
    node_7 --> node_188
    node_17 --> node_464
    node_183 --> node_637
    node_249 --> node_253
    node_42 --> node_399
    node_7 --> node_588
    node_6 --> node_186
    node_489 --> node_189
    node_621 --> node_330
    node_35 --> node_440
    node_125 --> node_266
    node_32 --> node_187
    node_389 --> node_155
    node_508 --> node_610
    node_32 --> node_165
    node_249 --> node_186
    node_551 --> node_720
    node_609 --> node_133
    node_389 --> node_151
    node_411 --> node_309
    node_128 --> node_147
    node_39 --> node_105
    node_621 --> node_629
    node_468 --> node_385
    node_739 --> node_315
    node_625 --> node_634
    node_40 --> node_236
    node_555 --> node_90
    node_451 --> node_246
    node_164 --> node_162
    node_445 --> node_21
    node_97 --> node_105
    node_42 --> node_267
    node_27 --> node_631
    node_609 --> node_159
    node_364 --> node_144
    node_258 --> node_279
    node_538 --> node_701
    node_40 --> node_253
    node_421 --> node_165
    node_313 --> node_312
    node_40 --> node_437
    node_11 --> node_322
    node_40 --> node_186
    node_424 --> node_182
    node_615 --> node_717
    node_125 --> node_280
    node_36 --> node_146
    node_249 --> node_212
    node_320 --> node_318
    node_224 --> node_228
    node_125 --> node_237
    node_320 --> node_431
    node_424 --> node_272
    node_32 --> node_302
    node_615 --> node_734
    node_644 --> node_131
    node_13 --> node_466
    node_125 --> node_284
    node_315 --> node_696
    node_424 --> node_307
    node_389 --> node_214
    node_424 --> node_168
    node_128 --> node_355
    node_25 --> node_311
    node_436 --> node_742
    node_742 --> node_744
    node_430 --> node_159
    node_396 --> node_367
    node_32 --> node_242
    node_451 --> node_220
    node_359 --> node_133
    node_42 --> node_241
    node_128 --> node_297
    node_128 --> node_296
    node_128 --> node_195
    node_161 --> node_432
    node_599 --> node_591
    node_728 --> node_695
    node_389 --> node_245
    node_572 --> node_714
    node_626 --> node_603
    node_451 --> node_60
    node_25 --> node_310
    node_372 --> node_614
    node_25 --> node_538
    node_600 --> node_591
    node_555 --> node_386
    node_389 --> node_166
    node_446 --> node_69
    node_40 --> node_362
    node_508 --> node_479
    node_633 --> node_703
    node_359 --> node_159
    node_481 --> node_189
    node_96 --> node_131
    node_28 --> node_24
    node_305 --> node_70
    node_124 --> node_277
    node_372 --> node_105
    node_621 --> node_725
    node_491 --> node_146
    node_7 --> node_373
    node_6 --> node_232
    node_125 --> node_128
    node_42 --> node_471
    node_576 --> node_621
    node_32 --> node_234
    node_372 --> node_458
    node_394 --> node_743
    node_555 --> node_484
    node_7 --> node_478
    node_633 --> node_718
    node_659 --> node_656
    node_249 --> node_243
    node_214 --> node_207
    node_389 --> node_258
    node_683 --> node_315
    node_25 --> node_207
    node_28 --> node_35
    node_40 --> node_603
    node_6 --> node_144
    node_389 --> node_235
    node_161 --> node_626
    node_25 --> node_13
    node_47 --> node_357
    node_181 --> node_296
    node_451 --> node_476
    node_451 --> node_97
    node_91 --> node_181
    node_424 --> node_186
    node_474 --> node_21
    node_646 --> node_687
    node_125 --> node_252
    node_424 --> node_348
    node_430 --> node_431
    node_214 --> node_308
    node_517 --> node_654
    node_234 --> node_175
    node_412 --> node_129
    node_615 --> node_737
    node_42 --> node_429
    node_449 --> node_14
    node_481 --> node_634
    node_249 --> node_222
    node_372 --> node_362
    node_114 --> node_112
    node_389 --> node_283
    node_655 --> node_656
    node_42 --> node_257
    node_63 --> node_315
    node_616 --> node_615
    node_51 --> node_666
    node_480 --> node_211
    node_6 --> node_210
    node_25 --> node_163
    node_125 --> node_278
    node_557 --> node_341
    node_233 --> node_167
    node_411 --> node_231
    node_25 --> node_357
    node_393 --> node_159
    node_128 --> node_169
    node_142 --> node_131
    node_25 --> node_115
    node_7 --> node_65
    node_128 --> node_352
    node_446 --> node_92
    node_7 --> node_663
    node_128 --> node_313
    node_633 --> node_701
    node_621 --> node_344
    node_52 --> node_227
    node_11 --> node_734
    node_424 --> node_333
    node_446 --> node_4
    node_91 --> node_176
    node_489 --> node_318
    node_621 --> node_345
    node_372 --> node_603
    node_446 --> node_605
    node_51 --> node_333
    node_128 --> node_273
    node_6 --> node_276
    node_374 --> node_277
    node_459 --> node_315
    node_486 --> node_631
    node_258 --> node_356
    node_474 --> node_405
    node_249 --> node_255
    node_47 --> node_146
    node_507 --> node_173
    node_451 --> node_90
    node_621 --> node_724
    node_147 --> node_188
    node_40 --> node_210
    node_6 --> node_449
    node_249 --> node_247
    node_389 --> node_524
    node_517 --> node_315
    node_590 --> node_589
    node_6 --> node_242
    node_25 --> node_361
    node_471 --> node_14
    node_80 --> node_315
    node_233 --> node_95
    node_25 --> node_445
    node_214 --> node_193
    node_425 --> node_262
    node_532 --> node_719
    node_446 --> node_14
    node_258 --> node_238
    node_128 --> node_142
    node_32 --> node_114
    node_214 --> node_157
    node_424 --> node_339
    node_621 --> node_654
    node_451 --> node_741
    node_128 --> node_360
    node_424 --> node_325
    node_125 --> node_267
    node_417 --> node_268
    node_32 --> node_260
    node_567 --> node_695
    node_40 --> node_255
    node_25 --> node_719
    node_389 --> node_130
    node_372 --> node_144
    node_446 --> node_593
    node_249 --> node_279
    node_128 --> node_288
    node_36 --> node_621
    node_389 --> node_221
    node_507 --> node_179
    node_668 --> node_621
    node_25 --> node_146
    node_147 --> node_146
    node_470 --> node_582
    node_249 --> node_118
    node_11 --> node_323
    node_191 --> node_315
    node_446 --> node_71
    node_580 --> node_584
    node_424 --> node_144
    node_414 --> node_742
    node_128 --> node_351
    node_516 --> node_188
    node_258 --> node_311
    node_396 --> node_372
    node_25 --> node_643
    node_28 --> node_33
    node_451 --> node_386
    node_6 --> node_659
    node_128 --> node_224
    node_258 --> node_208
    node_642 --> node_644
    node_40 --> node_279
    node_325 --> node_22
    node_7 --> node_28
    node_359 --> node_358
    node_28 --> node_41
    node_481 --> node_318
    node_249 --> node_303
    node_64 --> node_13
    node_446 --> node_637
    node_35 --> node_9
    node_459 --> node_540
    node_424 --> node_171
    node_446 --> node_18
    node_505 --> node_175
    node_578 --> node_335
    node_689 --> node_131
    node_424 --> node_353
    node_142 --> node_432
    node_214 --> node_320
    node_42 --> node_360
    node_391 --> node_390
    node_609 --> node_277
    node_451 --> node_484
    node_615 --> node_341
    node_46 --> node_606
    node_459 --> node_694
    node_424 --> node_210
    node_35 --> node_663
    node_128 --> node_231
    node_491 --> node_621
    node_507 --> node_178
    node_252 --> node_251
    node_25 --> node_174
    node_42 --> node_191
    node_32 --> node_298
    node_234 --> node_181
    node_538 --> node_520
    node_25 --> node_470
    node_448 --> node_464
    node_714 --> node_318
    node_468 --> node_411
    node_331 --> node_727
    node_233 --> node_168
    node_214 --> node_287
    node_416 --> node_359
    node_554 --> node_188
    node_25 --> node_559
    node_125 --> node_355
    node_258 --> node_116
    node_92 --> node_149
    node_424 --> node_276
    node_480 --> node_448
    node_681 --> node_333
    node_389 --> node_292
    node_125 --> node_297
    node_125 --> node_296
    node_239 --> node_6
    node_42 --> node_596
    node_142 --> node_626
    node_517 --> node_523
    node_42 --> node_359
    node_25 --> node_304
    node_6 --> node_271
    node_25 --> node_161
    node_424 --> node_349
    node_425 --> node_201
    node_143 --> node_131
    node_389 --> node_250
    node_25 --> node_477
    node_191 --> node_694
    node_64 --> node_188
    node_25 --> node_215
    node_128 --> node_253
    node_25 --> node_69
    node_13 --> node_594
    node_42 --> node_498
    node_374 --> node_432
    node_379 --> node_315
    node_538 --> node_563
    node_588 --> node_598
    node_459 --> node_268
    node_42 --> node_7
    node_380 --> node_236
    node_97 --> node_94
    node_421 --> node_375
    node_128 --> node_186
    node_125 --> node_257
    node_422 --> node_155
    node_6 --> node_114
    node_621 --> node_733
    node_422 --> node_151
    node_588 --> node_599
    node_389 --> node_175
    node_249 --> node_172
    node_234 --> node_176
    node_396 --> node_363
    node_639 --> node_645
    node_25 --> node_70
    node_258 --> node_163
    node_214 --> node_155
    node_435 --> node_63
    node_60 --> node_65
    node_214 --> node_372
    node_6 --> node_260
    node_25 --> node_155
    node_258 --> node_115
    node_25 --> node_151
    node_214 --> node_285
    node_25 --> node_289
    node_555 --> node_430
    node_105 --> node_131
    node_320 --> node_432
    node_446 --> node_60
    node_308 --> node_105
    node_451 --> node_75
    node_621 --> node_614
    node_448 --> node_450
    node_615 --> node_732
    node_50 --> node_105
    node_378 --> node_131
    node_128 --> node_212
    node_420 --> node_224
    node_643 --> node_13
    node_40 --> node_172
    node_42 --> node_236
    node_47 --> node_621
    node_50 --> node_458
    node_6 --> node_356
    node_505 --> node_153
    node_272 --> node_296
    node_258 --> node_361
    node_374 --> node_626
    node_181 --> node_253
    node_682 --> node_315
    node_42 --> node_253
    node_42 --> node_458
    node_572 --> node_333
    node_6 --> node_238
    node_32 --> node_216
    node_42 --> node_437
    node_615 --> node_713
    node_411 --> node_189
    node_114 --> node_111
    node_466 --> node_13
    node_42 --> node_186
    node_480 --> node_72
    node_224 --> node_225
    node_25 --> node_214
    node_398 --> node_170
    node_424 --> node_378
    node_7 --> node_506
    node_606 --> node_653
    node_411 --> node_187
    node_132 --> node_131
    node_621 --> node_348
    node_32 --> node_157
    node_125 --> node_169
    node_157 --> node_117
    node_270 --> node_431
    node_214 --> node_245
    node_317 --> node_315
    node_315 --> node_726
    node_372 --> node_94
    node_446 --> node_97
    node_446 --> node_476
    node_505 --> node_181
    node_320 --> node_626
    node_418 --> node_175
    node_25 --> node_621
    node_59 --> node_146
    node_25 --> node_245
    node_40 --> node_356
    node_125 --> node_352
    node_133 --> node_131
    node_615 --> node_342
    node_125 --> node_313
    node_6 --> node_606
    node_596 --> node_595
    node_157 --> node_116
    node_25 --> node_166
    node_446 --> node_17
    node_609 --> node_432
    node_38 --> node_397
    node_11 --> node_543
    node_46 --> node_188
    node_11 --> node_695
    node_148 --> node_159
    node_306 --> node_305
    node_125 --> node_273
    node_44 --> node_687
    node_458 --> node_435
    node_621 --> node_658
    node_535 --> node_188
    node_25 --> node_605
    node_128 --> node_243
    node_6 --> node_311
    node_249 --> node_311
    node_6 --> node_208
    node_254 --> node_131
    node_7 --> node_744
    node_25 --> node_460
    node_588 --> node_597
    node_621 --> node_333
    node_389 --> node_293
    node_214 --> node_258
    node_125 --> node_142
    node_389 --> node_150
    node_25 --> node_258
    node_25 --> node_14
    node_430 --> node_432
    node_315 --> node_330
    node_680 --> node_740
    node_458 --> node_388
    node_125 --> node_360
    node_480 --> node_588
    node_25 --> node_235
    node_249 --> node_310
    node_40 --> node_448
    node_505 --> node_176
    node_621 --> node_730
    node_423 --> node_170
    node_389 --> node_249
    node_564 --> node_339
    node_32 --> node_320
    node_40 --> node_311
    node_125 --> node_288
    node_258 --> node_174
    node_462 --> node_21
    node_25 --> node_593
    node_609 --> node_626
    node_32 --> node_266
    node_446 --> node_90
    node_621 --> node_339
    node_128 --> node_222
    node_359 --> node_432
    node_40 --> node_208
    node_32 --> node_294
    node_320 --> node_621
    node_364 --> node_188
    node_7 --> node_315
    node_621 --> node_325
    node_70 --> node_69
    node_206 --> node_202
    node_509 --> node_17
    node_7 --> node_579
    node_125 --> node_351
    node_40 --> node_310
    node_389 --> node_181
    node_28 --> node_6
    node_25 --> node_283
    node_40 --> node_538
    node_42 --> node_232
    node_11 --> node_650
    node_6 --> node_116
    node_6 --> node_13
    node_249 --> node_207
    node_46 --> node_693
    node_233 --> node_171
    node_536 --> node_606
    node_7 --> node_580
    node_430 --> node_626
    node_258 --> node_304
    node_258 --> node_161
    node_372 --> node_371
    node_148 --> node_431
    node_467 --> node_464
    node_25 --> node_637
    node_32 --> node_280
    node_528 --> node_435
    node_25 --> node_18
    node_32 --> node_237
    node_459 --> node_449
    node_424 --> node_238
    node_541 --> node_716
    node_11 --> node_189
    node_214 --> node_270
    node_128 --> node_255
    node_413 --> node_418
    node_39 --> node_13
    node_546 --> node_733
    node_128 --> node_247
    node_406 --> node_417
    node_25 --> node_143
    node_374 --> node_364
    node_372 --> node_606
    node_464 --> node_21
    node_651 --> node_652
    node_249 --> node_308
    node_451 --> node_430
    node_459 --> node_133
    node_555 --> node_326
    node_332 --> node_742
    node_204 --> node_131
    node_25 --> node_640
    node_40 --> node_116
    node_40 --> node_13
    node_424 --> node_305
    node_449 --> node_105
    node_25 --> node_524
    node_633 --> node_729
    node_249 --> node_163
    node_537 --> node_707
    node_32 --> node_125
    node_534 --> node_403
    node_6 --> node_115
    node_420 --> node_223
    node_258 --> node_289
    node_11 --> node_342
    node_638 --> node_644
    node_42 --> node_210
    node_624 --> node_338
    node_249 --> node_115
    node_622 --> node_315
    node_128 --> node_279
    node_389 --> node_148
    node_35 --> node_744
    node_480 --> node_373
    node_50 --> node_63
    node_32 --> node_285
    node_25 --> node_246
    node_426 --> node_179
    node_446 --> node_493
    node_446 --> node_22
    node_14 --> node_410
    node_480 --> node_478
    node_446 --> node_484
    node_375 --> node_166
    node_25 --> node_130
    node_128 --> node_118
    node_214 --> node_221
    node_372 --> node_610
    node_424 --> node_208
    node_32 --> node_128
    node_6 --> node_188
    node_25 --> node_221
    node_633 --> node_337
    node_505 --> node_165
    node_40 --> node_163
    node_38 --> node_301
    node_42 --> node_276
    node_125 --> node_253
    node_372 --> node_374
    node_398 --> node_167
    node_249 --> node_361
    node_40 --> node_115
    node_11 --> node_634
    node_75 --> node_74
    node_476 --> node_145
    node_394 --> node_744
    node_448 --> node_454
    node_110 --> node_112
    node_125 --> node_186
    node_161 --> node_694
    node_128 --> node_303
    node_609 --> node_632
    node_615 --> node_702
    node_451 --> node_211
    node_25 --> node_714
    node_270 --> node_357
    node_244 --> node_131
    node_416 --> node_133
    node_389 --> node_110
    node_737 --> node_315
    node_35 --> node_579
    node_42 --> node_50
    node_255 --> node_131
    node_420 --> node_222
    node_59 --> node_621
    node_199 --> node_457
    node_615 --> node_327
    node_42 --> node_402
    node_28 --> node_37
    node_30 --> node_582
    node_40 --> node_188
    node_446 --> node_3
    node_42 --> node_279
    node_40 --> node_361
    node_25 --> node_60
    node_40 --> node_588
    node_426 --> node_178
    node_446 --> node_463
    node_621 --> node_720
    node_7 --> node_437
    node_661 --> node_656
    node_25 --> node_457
    node_621 --> node_703
    node_667 --> node_315
    node_125 --> node_212
    node_315 --> node_344
    node_258 --> node_229
    node_446 --> node_434
    node_32 --> node_278
    node_566 --> node_553
    node_446 --> node_413
    node_425 --> node_200
    node_50 --> node_403
    node_25 --> node_385
    node_559 --> node_21
    node_307 --> node_305
    node_181 --> node_178
    node_315 --> node_724
    node_6 --> node_693
    node_661 --> node_659
    node_621 --> node_718
    node_27 --> node_70
    node_232 --> node_742
    node_40 --> node_146
    node_423 --> node_167
    node_424 --> node_239
    node_6 --> node_280
    node_424 --> node_184
    node_504 --> node_166
    node_621 --> node_659
    node_258 --> node_235
    node_6 --> node_237
    node_425 --> node_197
    node_420 --> node_226
    node_389 --> node_742
    node_25 --> node_292
    node_657 --> node_658
    node_6 --> node_284
    node_389 --> node_187
    node_389 --> node_165
    node_536 --> node_188
    node_169 --> node_166
    node_273 --> node_174
    node_51 --> node_542
    node_25 --> node_476
    node_70 --> node_637
    node_25 --> node_97
    node_507 --> node_180
    node_621 --> node_347
    node_214 --> node_250
    node_424 --> node_115
    node_655 --> node_663
    node_42 --> node_378
    node_249 --> node_174
    node_25 --> node_250
    node_128 --> node_172
    node_400 --> node_371
    node_305 --> node_306
    node_372 --> node_188
    node_214 --> node_175
    node_258 --> node_283
    node_32 --> node_267
    node_125 --> node_243
    node_148 --> node_145
    node_474 --> node_406
    node_7 --> node_434
    node_141 --> node_132
    node_421 --> node_170
    node_486 --> node_146
    node_128 --> node_431
    node_7 --> node_413
    node_11 --> node_318
    node_389 --> node_302
    node_471 --> node_405
    node_615 --> node_338
    node_6 --> node_304
    node_507 --> node_174
    node_555 --> node_107
    node_446 --> node_109
    node_40 --> node_174
    node_249 --> node_304
    node_249 --> node_161
    node_633 --> node_336
    node_705 --> node_719
    node_588 --> node_589
    node_206 --> node_199
    node_40 --> node_373
    node_631 --> node_615
    node_480 --> node_28
    node_701 --> node_20
    node_249 --> node_215
    node_258 --> node_355
    node_739 --> node_188
    node_11 --> node_574
    node_398 --> node_168
    node_29 --> node_146
    node_32 --> node_241
    node_25 --> node_224
    node_125 --> node_222
    node_148 --> node_131
    node_593 --> node_14
    node_258 --> node_297
    node_258 --> node_195
    node_25 --> node_90
    node_458 --> node_742
    node_292 --> node_291
    node_417 --> node_743
    node_186 --> node_185
    node_40 --> node_304
    node_40 --> node_161
    node_249 --> node_155
    node_411 --> node_233
    node_58 --> node_315
    node_6 --> node_289
    node_676 --> node_315
    node_414 --> node_287
    node_249 --> node_151
    node_6 --> node_252
    node_7 --> node_306
    node_249 --> node_289
    node_501 --> node_146
    node_556 --> node_703
    node_40 --> node_215
    node_264 --> node_263
    node_25 --> node_231
    node_621 --> node_712
    node_538 --> node_525
    node_739 --> node_146
    node_25 --> node_62
    node_446 --> node_586
    node_411 --> node_367
    node_7 --> node_109
    node_28 --> node_30
    node_468 --> node_445
    node_125 --> node_255
    node_214 --> node_182
    node_538 --> node_315
    node_495 --> node_621
    node_42 --> node_356
    node_128 --> node_311
    node_214 --> node_359
    node_14 --> node_421
    node_40 --> node_289
    node_732 --> node_655
    node_11 --> node_696
    node_172 --> node_603
    node_216 --> node_217
    node_448 --> node_449
    node_46 --> node_620
    node_142 --> node_694
    node_249 --> node_214
    node_413 --> node_424
    node_42 --> node_238
    node_419 --> node_244
    node_133 --> node_135
    node_296 --> node_131
    node_423 --> node_168
    node_698 --> node_323
    node_417 --> node_269
    node_128 --> node_310
    node_372 --> node_611
    node_425 --> node_206
    node_25 --> node_293
    node_414 --> node_285
    node_471 --> node_398
    node_478 --> node_477
    node_606 --> node_601
    node_25 --> node_150
    node_6 --> node_48
    node_163 --> node_164
    node_50 --> node_606
    node_276 --> node_274
    node_49 --> node_436
    node_249 --> node_245
    node_125 --> node_279
    node_615 --> node_331
    node_35 --> node_603
    node_486 --> node_70
    node_177 --> node_131
    node_249 --> node_166
    node_272 --> node_173
    node_691 --> node_131
    node_32 --> node_257
    node_25 --> node_249
    node_125 --> node_118
    node_51 --> node_611
    node_621 --> node_606
    node_25 --> node_484
    node_150 --> node_194
    node_427 --> node_131
    node_6 --> node_229
    node_446 --> node_430
    node_42 --> node_448
    node_372 --> node_612
    node_7 --> node_586
    node_562 --> node_323
    node_25 --> node_35
    node_424 --> node_304
    node_258 --> node_169
    node_709 --> node_727
    node_256 --> node_131
    node_577 --> node_652
    node_128 --> node_207
    node_258 --> node_352
    node_42 --> node_311
    node_214 --> node_236
    node_336 --> node_131
    node_446 --> node_159
    node_110 --> node_111
    node_448 --> node_389
    node_451 --> node_72
    node_125 --> node_303
    node_25 --> node_181
    node_507 --> node_177
    node_555 --> node_516
    node_42 --> node_208
    node_278 --> node_603
    node_615 --> node_335
    node_718 --> node_131
    node_40 --> node_166
    node_249 --> node_258
    node_424 --> node_337
    node_258 --> node_292
    node_142 --> node_268
    node_272 --> node_179
    node_14 --> node_409
    node_249 --> node_235
    node_419 --> node_742
    node_413 --> node_422
    node_596 --> node_594
    node_609 --> node_315
    node_25 --> node_513
    node_40 --> node_229
    node_374 --> node_694
    node_448 --> node_461
    node_533 --> node_709
    node_683 --> node_146
    node_315 --> node_348
    node_63 --> node_188
    node_128 --> node_308
    node_44 --> node_277
    node_424 --> node_321
    node_258 --> node_142
    node_142 --> node_317
    node_6 --> node_147
    node_657 --> node_659
    node_36 --> node_634
    node_107 --> node_108
    node_372 --> node_662
    node_128 --> node_163
    node_6 --> node_283
    node_451 --> node_107
    node_486 --> node_621
    node_128 --> node_357
    node_40 --> node_235
    node_425 --> node_264
    node_249 --> node_283
    node_25 --> node_434
    node_148 --> node_626
    node_320 --> node_694
    node_14 --> node_419
    node_150 --> node_354
    node_14 --> node_385
    node_258 --> node_288
    node_451 --> node_538
    node_459 --> node_188
    node_42 --> node_116
    node_42 --> node_13
    node_42 --> node_404
    node_63 --> node_146
    node_482 --> node_621
    node_188 --> node_630
    node_315 --> node_333
    node_25 --> node_148
    node_517 --> node_188
    node_538 --> node_458
    node_272 --> node_178
    node_80 --> node_188
    node_258 --> node_351
    node_11 --> node_602
    node_29 --> node_621
    node_6 --> node_355
    node_40 --> node_283
    node_191 --> node_357
    node_11 --> node_613
    node_128 --> node_361
    node_404 --> node_93
    node_420 --> node_227
    node_46 --> node_315
    node_258 --> node_224
    node_124 --> node_144
    node_538 --> node_348
    node_6 --> node_297
    node_6 --> node_296
    node_6 --> node_195
    node_125 --> node_172
    node_580 --> node_17
    node_531 --> node_344
    node_249 --> node_524
    node_411 --> node_368
    node_416 --> node_141
    node_453 --> node_101
    node_226 --> node_131
    node_588 --> node_592
    node_398 --> node_171
    node_32 --> node_360
    node_501 --> node_621
    node_214 --> node_110
    node_315 --> node_325
    node_381 --> node_166
    node_25 --> node_306
    node_389 --> node_298
    node_36 --> node_630
    node_555 --> node_609
    node_25 --> node_110
    node_320 --> node_268
    node_615 --> node_328
    node_42 --> node_115
    node_80 --> node_146
    node_114 --> node_110
    node_621 --> node_660
    node_191 --> node_188
    node_258 --> node_231
    node_682 --> node_606
    node_609 --> node_694
    node_32 --> node_191
    node_40 --> node_355
    node_148 --> node_621
    node_446 --> node_6
    node_458 --> node_379
    node_411 --> node_372
    node_29 --> node_14
    node_249 --> node_130
    node_50 --> node_188
    node_214 --> node_232
    node_448 --> node_456
    node_666 --> node_621
    node_25 --> node_405
    node_28 --> node_49
    node_65 --> node_61
    node_609 --> node_614
    node_25 --> node_109
    node_40 --> node_524
    node_203 --> node_200
    node_40 --> node_195
    node_249 --> node_221
    node_249 --> node_248
    node_538 --> node_333
    node_409 --> node_292
    node_434 --> node_436
    node_448 --> node_441
    node_125 --> node_356
    node_320 --> node_317
    node_459 --> node_693
    node_11 --> node_699
    node_480 --> node_580
    node_516 --> node_521
    node_621 --> node_655
    node_25 --> node_41
    node_260 --> node_259
    node_446 --> node_594
    node_42 --> node_361
    node_32 --> node_182
    node_42 --> node_588
    node_374 --> node_603
    node_619 --> node_615
    node_505 --> node_157
    node_6 --> node_506
    node_615 --> node_704
    node_32 --> node_359
    node_430 --> node_694
    node_36 --> node_318
    node_637 --> node_184
    node_632 --> node_693
    node_191 --> node_146
    node_258 --> node_293
    node_40 --> node_130
    node_405 --> node_422
    node_411 --> node_256
    node_258 --> node_150
    node_412 --> node_225
    node_424 --> node_147
    node_423 --> node_171
    node_538 --> node_325
    node_425 --> node_204
    node_6 --> node_619
    node_25 --> node_742
    node_25 --> node_187
    node_46 --> node_474
    node_359 --> node_694
    node_25 --> node_165
    node_538 --> node_568
    node_128 --> node_174
    node_577 --> node_651
    node_593 --> node_589
    node_451 --> node_516
    node_548 --> node_330
    node_374 --> node_144
    node_421 --> node_168
    node_573 --> node_328
    node_25 --> node_586
    node_6 --> node_169
    node_6 --> node_744
    node_125 --> node_311
    node_468 --> node_14
    node_6 --> node_352
    node_50 --> node_693
    node_6 --> node_313
    node_258 --> node_181
    node_352 --> node_131
    node_236 --> node_277
    node_566 --> node_342
    node_7 --> node_305
    node_470 --> node_17
    node_40 --> node_60
    node_372 --> node_620
    node_426 --> node_174
    node_505 --> node_152
    node_42 --> node_534
    node_424 --> node_355
    node_32 --> node_236
    node_258 --> node_212
    node_13 --> node_589
    node_128 --> node_304
    node_128 --> node_161
    node_214 --> node_276
    node_430 --> node_268
    node_621 --> node_693
    node_6 --> node_273
    node_125 --> node_310
    node_25 --> node_302
    node_142 --> node_133
    node_249 --> node_292
    node_379 --> node_188
    node_424 --> node_274
    node_683 --> node_621
    node_389 --> node_216
    node_47 --> node_615
    node_424 --> node_296
    node_435 --> node_436
    node_411 --> node_363
    node_47 --> node_159
    node_128 --> node_215
    node_214 --> node_242
    node_389 --> node_193
    node_11 --> node_706
    node_32 --> node_253
    node_25 --> node_398
    node_549 --> node_701
    node_615 --> node_330
    node_389 --> node_157
    node_6 --> node_142
    node_57 --> node_9
    node_32 --> node_186
    node_430 --> node_317
    node_181 --> node_174
    node_249 --> node_250
    node_40 --> node_352
    node_448 --> node_440
    node_25 --> node_64
    node_42 --> node_174
    node_13 --> node_62
    node_269 --> node_131
    node_6 --> node_360
    node_42 --> node_373
    node_128 --> node_155
    node_372 --> node_607
    node_372 --> node_625
    node_741 --> node_742
    node_315 --> node_703
    node_11 --> node_328
    node_40 --> node_292
    node_128 --> node_151
    node_25 --> node_430
    node_42 --> node_478
    node_249 --> node_175
    node_7 --> node_538
    node_480 --> node_437
    node_125 --> node_207
    node_451 --> node_10
    node_621 --> node_611
    node_6 --> node_288
    node_38 --> node_14
    node_40 --> node_97
    node_424 --> node_324
    node_446 --> node_277
    node_621 --> node_729
    node_621 --> node_709
    node_591 --> node_599
    node_555 --> node_429
    node_593 --> node_22
    node_25 --> node_159
    node_42 --> node_25
    node_325 --> node_14
    node_448 --> node_13
    node_214 --> node_234
    node_400 --> node_364
    node_468 --> node_421
    node_506 --> node_519
    node_516 --> node_514
    node_40 --> node_142
    node_682 --> node_188
    node_42 --> node_304
    node_42 --> node_161
    node_315 --> node_718
    node_14 --> node_423
    node_6 --> node_351
    node_615 --> node_322
    node_258 --> node_243
    node_609 --> node_144
    node_372 --> node_619
    node_446 --> node_20
    node_6 --> node_224
```

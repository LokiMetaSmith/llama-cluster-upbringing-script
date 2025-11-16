The `bootstrap.sh` script is failing with a 'Failed due to progress deadline' error for the `world_model_service` Nomad job. This issue has resurfaced after a previous attempt to fix a Nomad job parsing error related to `initial_delay`.

A previous agent has done a lot of debugging and has fixed a number of issues with the `bootstrap.sh` script and the Ansible playbooks. However, the `world_model_service` job is still not being submitted to Nomad.

The `app_services.yaml` playbook is failing on the "Run mqtt job" task. The `mqtt` job is a dependency for the `world_model_service`, so the `world_model_service` job is never submitted. The `mqtt` job is failing with a "failed to create container" error, which suggests a problem with the Docker integration.

The previous agent has tried the following:
*   Verifying that the `bootstrap.sh` script is running the `app_services` playbook.
*   Verifying that the `world_model_service` role is being executed.
*   Verifying that the `world_model_service` job is being submitted to Nomad.
*   Investigating the `mqtt` job's Nomad file, host volume permissions, and `mosquitto.conf` file.
*   Switching the `mqtt` job to use the `exec` driver instead of the `docker` driver.

The `exec` driver also failed, which suggests that the problem is not with the Docker integration, but with the `mosquitto` application itself, or with the host environment.

Your task is to:
1.  Investigate the `mqtt` job to understand why it's failing.
2.  Fix the `mqtt` job so that it deploys successfully.
3.  Verify that the `world_model_service` job is deployed successfully.
4.  Submit your changes with a descriptive commit message.
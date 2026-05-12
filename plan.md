# Plan to update Traefik configuration

1.  **Remove Traefik tags from internal services**
    *   `ansible/jobs/filebrowser.nomad.j2`
    *   `ansible/roles/docker_registry/templates/docker-registry.nomad.j2`
    *   `ansible/roles/monitoring/templates/beszel-hub.nomad.j2`
    *   `ansible/roles/monitoring/templates/statsping.nomad.j2`
    *   Remove `traefik.enable=true` and all related tags from these files so they are not exposed externally.

2.  **Update `pipecatapp` to use internal CA**
    *   Modify `ansible/roles/pipecatapp/templates/pipecatapp.nomad.j2`
    *   Keep `traefik.enable=true`, `entrypoints=websecure`, and `tls=true`.
    *   Remove `tls.certresolver=local`.
    *   Strictly restrict host routing to `Host(\`pipecatapp.{{ cluster_domain | default('local.mesh') }}\`)` (remove `localhost` and `127.0.0.1`).

3.  **Update `authentik` to use internal CA**
    *   Modify `ansible/roles/authentik/templates/authentik.nomad.j2`
    *   Keep `traefik.enable=true`.
    *   Add `traefik.http.routers.authentik.entrypoints=websecure` and `traefik.http.routers.authentik.tls=true` tags if not present.

4.  **Update `tml-interaction` to use internal CA**
    *   Modify `ansible/jobs/tml-interaction.nomad.j2`
    *   Ensure `tls=true` and `entrypoints=websecure` are present. (They already are). Remove any `certresolver` if present.

5.  **Create placeholder templates for `opengravity` and `e2a`**
    *   Create `ansible/jobs/opengravity.nomad.j2` and `ansible/jobs/e2a.nomad.j2` (already created via bash). Ensure their configurations include `traefik.enable=true`, `tls=true`, `entrypoints=websecure`, and routing based on Host.
    *   Format them assuming a stateless architecture designed for future IPFS-backed storage deployments.

6.  **Configure Traefik dynamic file provider for internal certificates**
    *   Modify `ansible/roles/traefik/templates/traefik.nomad.j2` to add a dynamic file provider configuration that loads TLS certificates dynamically.
    *   We will provide placeholder paths like `certs/mesh/tls.crt` and `certs/mesh/tls.key` within a generated `tls.yml` file.

7.  **Pre-commit checks**
    *   Run `pre_commit_instructions` tool and complete all required checks.

8.  **Submit changes**
    *   Commit changes and submit for approval.

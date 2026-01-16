
1.  **Modify `playbooks/services/ai_experts.yaml`**
    -   Insert a new task after "Verify pipecatapp Docker image exists" to explicitly test running the image:
        ```yaml
        - name: Verify pipecatapp Docker image is runnable
          ansible.builtin.command: docker run --rm --entrypoint /bin/true pipecatapp:local
          changed_when: false
          tags:
            - deploy-expert
        ```
    -   This step confirms Docker can run the image locally before Nomad tries.

2.  **Modify `ansible/jobs/expert.nomad.j2`**
    -   Remove the line `force_pull = false` from the `config` block of the `docker` driver task. This reverts to default behavior (pull if missing).

3.  **Complete pre-commit steps**
    -   Complete pre commit steps to make sure proper testing, verifications, reviews and reflections are done.

4.  **Submit the change.**
    -   Submit the code with a descriptive message.

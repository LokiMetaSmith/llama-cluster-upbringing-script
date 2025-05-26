# Manual Testing Guide for distributed-llama Service

This guide will walk you through the steps to manually test the `distributed-llama` service on your Debian server. It assumes you have already followed the `SERVICE_SETUP_AND_USAGE.MD` guide for installation and initial configuration.

## 1. Prerequisites

Before you begin testing, ensure the following conditions are met:

*   **Service Installed:** The `distributed-llama` service has been installed and configured according to the `SERVICE_SETUP_AND_USAGE.MD` document.
*   **Configuration File Populated:** The `/etc/default/distributed-llama` configuration file is present and correctly populated. Crucially:
    *   `MODEL_PATH` points to a valid, readable language model file.
    *   `TOKENIZER_PATH` points to a valid, readable tokenizer file.
    *   `INSTALL_DIR` points to the correct base directory of your `distributed-llama` application.
*   **Service User:** The `SERVICE_USER` specified in `/etc/default/distributed-llama` (e.g., `llamauser`) exists, owns relevant directories (like `INSTALL_DIR`, `/var/run/distributed-llama`, `/var/log/distributed-llama`), and has necessary permissions.
*   **Application Compiled:** The `dllama-api` executable is compiled and located within the `INSTALL_DIR` (e.g., at `$INSTALL_DIR/distributed-llama-repo/dllama-api`).

## 2. Testing Steps

Follow these steps sequentially to test the service.

### 2.1. Initial Status Check

Verify the initial state of the service before starting any tests.

*   **Command:**
    ```bash
    sudo service distributed-llama status
    ```
*   **Expected Outcome:**
    The service should be reported as "not running" or "stopped". If it's reported as running, and this is a fresh setup, you might want to stop it (`sudo service distributed-llama stop`) before proceeding to ensure a clean test.

### 2.2. Start the Service

Attempt to start the `distributed-llama` service.

*   **Command:**
    ```bash
    sudo service distributed-llama start
    ```
*   **Expected Outcome:**
    The command should execute without immediate errors. You should see a message like:
    `[ ok ] Starting distributed-llama: dllama-api.`
*   **Action:**
    Wait for about 10-30 seconds (depending on model size and system speed) for the `dllama-api` to initialize.

### 2.3. Verify Service is Running

Confirm that the service has started successfully and the daemon is operational.

*   **Command 1: Service Status**
    ```bash
    sudo service distributed-llama status
    ```
    *   **Expected Outcome:** The service should be reported as "running" or "active", and it should display a Process ID (PID). Example:
        `● distributed-llama.service - LSB: Start daemon at boot time
           Loaded: loaded (/etc/init.d/distributed-llama; generated)
           Active: active (running) since Mon YYYY-MM-DD HH:MM:SS UTC; Xs ago
             Docs: man:systemd-sysv-generator(8)
          Process: [PID] ExecStart=/etc/init.d/distributed-llama start (code=exited, status=0/SUCCESS)
            Tasks: N (limit: ...)
           Memory: XM
           CGroup: /system.slice/distributed-llama.service
                   └─[PID_OF_DAEMON] /opt/distributed-llama/distributed-llama-repo/dllama-api --model /path/to/model --tokenizer /path/to/tokenizer ...`

*   **Command 2 (Optional): Process Check**
    ```bash
    ps aux | grep dllama-api
    ```
    *   **Expected Outcome:** You should see at least one process related to `dllama-api` (excluding the `grep` command itself) running under the configured `SERVICE_USER` (e.g., `llamauser`).

*   **Command 3: Check Logs**
    ```bash
    sudo tail -n 50 /var/log/distributed-llama/dllama-api.log
    ```
    (Adjust the path if `LOG_DIR_BASE` or `DAEMON_NAME` were changed in the init script or config.)
    *   **Expected Outcome:** The log file should show startup messages from `dllama-api`. Look for messages indicating the model and tokenizer were loaded successfully. If the API server is configured to listen on a network port, you might see a message like "llama_new_context_with_model: ..., "HTTP server listening on host:port 0.0.0.0:8080" or similar. Critically, check for any error messages like "model file not found", "tokenizer file not found", or permission issues.

### 2.4. Test API Functionality (if applicable)

If the `dllama-api` exposes an HTTP endpoint, test its basic connectivity. The default configuration in the init script and `/etc/default/distributed-llama` sets the API to listen on `0.0.0.0:8080`.

*   **Command (from the server itself):**
    ```bash
    curl http://localhost:8080/
    ```
    Or, if you know a specific health check or basic API endpoint for `dllama-api` (e.g., `/health`, `/v1/models`), use that:
    ```bash
    curl http://localhost:8080/health
    ```
*   **Expected Outcome:**
    You should receive a valid response from the API. This could be a JSON message, HTML, or plain text, depending on how `dllama-api` is implemented. A "connection refused" error means the API server is likely not running or not listening on the expected address/port. Check the logs from step 2.3 carefully if this occurs.
    *Note: If testing from another machine, ensure your server's firewall allows connections to the specified port (e.g., 8080).*

### 2.5. Stop the Service

Test the service shutdown procedure.

*   **Command:**
    ```bash
    sudo service distributed-llama stop
    ```
*   **Expected Outcome:**
    The command should execute without immediate errors. You should see a message like:
    `[ ok ] Stopping distributed-llama: dllama-api.`
*   **Action:**
    Wait a few seconds for the service to shut down completely.

### 2.6. Verify Service is Stopped

Confirm that the service has stopped as expected.

*   **Command 1: Service Status**
    ```bash
    sudo service distributed-llama status
    ```
    *   **Expected Outcome:** The service should be reported as "not running" or "inactive".

*   **Command 2 (Optional): Process Check**
    ```bash
    ps aux | grep dllama-api
    ```
    *   **Expected Outcome:** The `dllama-api` process(es) should no longer be listed (or if one appears momentarily, it should be in a defunct state and disappear quickly).

*   **Command 3: Check Logs**
    ```bash
    sudo tail -n 20 /var/log/distributed-llama/dllama-api.log
    ```
    *   **Expected Outcome:** The log file might show shutdown messages or indicate the process terminated.

### 2.7. Restart the Service

Test the restart functionality.

*   **Command:**
    ```bash
    sudo service distributed-llama restart
    ```
*   **Expected Outcome:**
    The command should execute. You'll typically see messages indicating the service is being stopped and then started.
    `[ ok ] Restarting distributed-llama: dllama-api.`
*   **Action:**
    Wait for about 10-30 seconds for the service to fully restart.
*   **Verify:**
    1.  Repeat the checks in **Step 2.3 (Verify Service is Running)** to ensure it's operational again.
    2.  Optionally, repeat **Step 2.4 (Test API Functionality)** to confirm the API is responsive.

### 2.8. Test Boot Behavior (System Reboot)

This is a crucial test to ensure the service starts automatically after a system reboot.

*   **Command:**
    ```bash
    sudo reboot
    ```
*   **Action:**
    Wait for the server to reboot completely and then log back in. This may take a few minutes.
*   **Verify:**
    Once logged back in:
    *   **Command 1: Service Status**
        ```bash
        sudo service distributed-llama status
        ```
        *   **Expected Outcome:** The service should be reported as "running" or "active".
    *   **Command 2: Check Logs**
        ```bash
        sudo tail -n 50 /var/log/distributed-llama/dllama-api.log
        ```
        *   **Expected Outcome:** The logs should indicate that the `dllama-api` service started up as part of the boot process. You should see the familiar startup messages.
    *   **Command 3 (Optional): Test API Functionality**
        Repeat **Step 2.4 (Test API Functionality)** to confirm the API is responsive after a reboot.

## 3. Troubleshooting Reminders

If any of the above tests fail, refer to the following:

*   **`SERVICE_SETUP_AND_USAGE.MD`:** This document contains a detailed troubleshooting section. Review it for common issues and solutions.
*   **Log Files:** The primary source of error information is `/var/log/distributed-llama/dllama-api.log`. Examine it carefully for any error messages, permission issues, or path problems.
*   **Paths and Permissions:** Double-check all file paths in `/etc/default/distributed-llama`. Ensure the `SERVICE_USER` has correct read/write/execute permissions for all relevant files and directories as outlined in the setup guide.
*   **Manual Execution:** Try running the `dllama-api` command directly as the `SERVICE_USER` (see troubleshooting section in `SERVICE_SETUP_AND_USAGE.MD`) to isolate issues with the application itself versus the service script.

This concludes the manual testing guide. If all steps pass, your `distributed-llama` service should be correctly installed and operational.

Last updated: 2025-10-12

# Setting Up and Managing the distributed-llama Service

## 1. Overview

The `distributed-llama` service is designed to run the `dllama-api` application as a background daemon. This allows the API server to start automatically on boot and be managed using standard service commands.

It utilizes:

* An **init script**: Located at `/etc/init.d/distributed-llama`, which controls the starting, stopping, and status of the service.
* A **configuration file**: Located at `/etc/default/distributed-llama`, which stores settings like model paths, user to run as, and installation directory.

## 2. Prerequisites

* A Debian-based Linux system (e.g., Ubuntu, Debian).
* `sudo` or root access to the system.
* The `distributed-llama` application code must be cloned and the `dllama-api` executable compiled. This is typically done by following the main project's setup instructions (e.g., running a script like `setup_distributed_llama.sh` from the `distributed-llama` GitHub repository).

## 3. Installation Steps

Follow these steps to set up the `distributed-llama` service:

### Step 1: Install `distributed-llama` Application

Before setting up the service, the `dllama-api` application itself must be compiled and available on your system.

1. **Choose an installation location:** A common location is `/opt`. We'll use `/opt/distributed-llama` as the base for the application.

    ```bash
    sudo mkdir -p /opt/distributed-llama
    ```

2. **Clone the repository:**

    ```bash
    sudo git clone https://github.com/b4rtaz/distributed-llama.git /opt/distributed-llama/distributed-llama-repo
    ```

3. **Compile the application:**
    Navigate to the repository directory and compile the `dllama-api` executable.

    ```bash
    cd /opt/distributed-llama/distributed-llama-repo
    sudo make dllama-api 
    ```

    (Alternatively, if the project provides a comprehensive setup script like `setup_distributed_llama.sh`, you might run that within `/opt/distributed-llama` according to its instructions.)
4. **Set ownership for the application directory (important for the service user later):**

    ```bash
    sudo chown -R llamauser:llamauser /opt/distributed-llama # Assuming 'llamauser' will be the service user
    ```

    *(Note: Create the `llamauser` first if it doesn't exist, as shown in Step 2, then run this chown command.)*

### Step 2: Create Service User

It's good practice to run services under a dedicated, non-privileged user for security.

1. **Create the user and group:**

    ```bash
    sudo adduser --system --group llamauser
    ```

    This command creates a system user named `llamauser` and a corresponding group.

### Step 3: Create Necessary Directories

The service requires specific directories for its operation:

1. **Application Installation Directory (if not already created in Step 1):**
    This is where the `distributed-llama-repo` (containing `dllama-api`) is located.

    ```bash
    sudo mkdir -p /opt/distributed-llama 
    sudo chown llamauser:llamauser /opt/distributed-llama 
    ```

    *(Ensure the contents, like `distributed-llama-repo`, are also owned by `llamauser` as per Step 1.4)*

2. **PID Directory:**
    This directory will store the process ID file of the running daemon.

    ```bash
    sudo mkdir -p /var/run/distributed-llama
    sudo chown llamauser:llamauser /var/run/distributed-llama
    sudo chmod 755 /var/run/distributed-llama 
    ```

3. **Log Directory:**
    This directory will store the service's log files.

    ```bash
    sudo mkdir -p /var/log/distributed-llama
    sudo chown llamauser:llamauser /var/log/distributed-llama
    sudo chmod 755 /var/log/distributed-llama
    ```

### Step 4: Deploy Service Files

You will need two files:

* The init script (e.g., previously generated as `distributed-llama-init-script/distributed-llama` in your workspace).
* The default configuration file (e.g., previously generated as `distributed-llama-default-config` in your workspace).

1. **Copy the init script:**
    Assuming the generated init script is available at `path/to/your/workspace/distributed-llama-init-script/distributed-llama`:

    ```bash
    sudo cp path/to/your/workspace/distributed-llama-init-script/distributed-llama /etc/init.d/distributed-llama
    ```

2. **Copy the configuration file:**
    Assuming the generated configuration file is available at `path/to/your/workspace/distributed-llama-default-config`:

    ```bash
    sudo cp path/to/your/workspace/distributed-llama-default-config /etc/default/distributed-llama
    ```

### Step 5: Set Permissions

The init script needs to be executable:

```bash
sudo chmod +x /etc/init.d/distributed-llama
```

### Step 6: Configure the Service

Edit the configuration file to match your setup. This is a **critical step**.

```bash
sudo nano /etc/default/distributed-llama
```

Key variables you **must** review and likely change:

* `SERVICE_USER`: Should match the user created in Step 2 (e.g., `llamauser`).
* `INSTALL_DIR`: The base directory where `distributed-llama-repo` is located (e.g., `/opt/distributed-llama`). The init script will look for the executable at `$INSTALL_DIR/$REPO_DIR_NAME/$DAEMON_EXECUTABLE_NAME`.
* `MODEL_PATH`: **Required.** Absolute path to your downloaded language model file (e.g., `/opt/distributed-llama/distributed-llama-repo/models/your_model.gguf`).
* `TOKENIZER_PATH`: **Required.** Absolute path to your tokenizer file (e.g., `/opt/distributed-llama/distributed-llama-repo/tokenizers/your_tokenizer.model`).
* `API_HOST`: Host IP for the API (default is `0.0.0.0`).
* `API_PORT`: Port for the API (default is `8080`).
* `DAEMON_OPTS`: Any additional command-line options for `dllama-api`.
* `REPO_DIR_NAME`: Name of the repository directory within `INSTALL_DIR` (default `distributed-llama-repo`).
* `DAEMON_EXECUTABLE_NAME`: Name of the executable (default `dllama-api`).

Ensure all paths are correct and the `SERVICE_USER` has read access to the model and tokenizer files, and read/execute access to the `dllama-api` executable.

### Step 7: Enable the Service

To make the service start automatically on boot:

```bash
sudo update-rc.d distributed-llama defaults
```

For systems using systemd, this command should still enable the SysVinit script. For more robust systemd integration, creating a native systemd unit file would be the next step, but this init script provides compatibility.

## 4. Managing the Service

Once installed and configured, you can manage the `distributed-llama` service using the following commands:

* **Start the service:**

    ```bash
    sudo service distributed-llama start
    ```

* **Stop the service:**

    ```bash
    sudo service distributed-llama stop
    ```

* **Restart the service:**
    (This will stop and then start the service)

    ```bash
    sudo service distributed-llama restart
    ```

* **Check the status of the service:**

    ```bash
    sudo service distributed-llama status
    ```

## 5. Checking Logs

Logs from the `dllama-api` daemon are written to a file specified by the `LOG_FILE` variable in the init script, which defaults to being constructed from `LOG_DIR_BASE` and `DAEMON_NAME`. Typically, this will be:

`/var/log/distributed-llama/dllama-api.log`

You can monitor the logs in real-time using:

```bash
tail -f /var/log/distributed-llama/dllama-api.log
```

Check these logs if the service fails to start or if you encounter issues.

## 6. Troubleshooting

If you encounter problems with the service:

1. **Check Service Status:**
    Run `sudo service distributed-llama status`. This will often tell you if the service is running, stopped, or failed.

2. **Examine Logs:**
    The primary source of information is the log file: `/var/log/distributed-llama/dllama-api.log`. Look for error messages.

3. **Verify Configuration (`/etc/default/distributed-llama`):**
    * Are `INSTALL_DIR`, `MODEL_PATH`, and `TOKENIZER_PATH` correct?
    * Does `MODEL_PATH` point to a valid, readable model file?
    * Does `TOKENIZER_PATH` point to a valid, readable tokenizer file?
    * Is `SERVICE_USER` set to the correct user (e.g., `llamauser`)?

4. **Permissions:**
    * Ensure the `SERVICE_USER` (e.g., `llamauser`) has:
        * Read and execute permissions on the `dllama-api` executable (e.g., `/opt/distributed-llama/distributed-llama-repo/dllama-api`).
        * Read permissions for the model and tokenizer files.
        * Read/write permissions for the `PID_DIR_BASE` (`/var/run/distributed-llama`) and `LOG_DIR_BASE` (`/var/log/distributed-llama`).
        * Read permissions for the entire `INSTALL_DIR` path.
    * Ensure `/etc/init.d/distributed-llama` is executable.

5. **Manual Execution:**
    Try running the `dllama-api` command directly as the `SERVICE_USER` to see if there are errors.

    ```bash
    sudo -u llamauser /opt/distributed-llama/distributed-llama-repo/dllama-api --model "/path/to/model" --tokenizer "/path/to/tokenizer" --host "0.0.0.0" --port "8080"
    ```

    Adjust paths and options according to your configuration. Check for any output or errors.

6. **Path to Executable in Init Script:**
    The init script constructs `FULL_EXECUTABLE_PATH` using variables from `/etc/default/distributed-llama` (`INSTALL_DIR`, `REPO_DIR_NAME`, `DAEMON_EXECUTABLE_NAME`). Double-check these are correctly defined if the error is "executable not found".
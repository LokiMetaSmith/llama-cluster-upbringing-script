# Bootable Pipecat Cluster ISO Configuration

This directory contains the `live-build` configurations to generate a slimmed-down, bootable Debian ISO that packages the Pipecat agent cluster for rapid installation on new bare-metal machines.

## Building the ISO

To generate the ISO, run the wrapper script from the `os-image` directory:

```bash
cd os-image
sudo ./build_iso.sh
```

**Requirements:**
You must have `live-build` and `rsync` installed on your host system:
`sudo apt install live-build rsync`

## What's Included

*   **Headless Debian (Trixie)**: Slimmed down distribution with essential networking tools.
*   **Project Source**: Automatically bundled into `/opt/pipecat-cluster`.
*   **Dependencies**: Packages like `ansible-core`, `python3`, `git`, `curl` are pre-installed.
*   **Default User**: A default user `pipecatapp` (password: `pipecat`) with `sudo` access is created to immediately run the bootstrap scripts.

## Usage

Booting the ISO will drop you into a shell with a welcome message guiding you to:

```bash
cd /opt/pipecat-cluster
sudo ./bootstrap.sh
```

`bootstrap.sh` will auto-profile the system resources and determine if it should configure as a `controller` or `worker` based on CPU/RAM constraints.

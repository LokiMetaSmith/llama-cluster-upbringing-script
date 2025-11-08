#!/bin/bash
# This script uninstalls all software and reverts all changes made by the playbook.

set -e

# Check for username argument
if [ -z "$1" ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

TARGET_USER=$1

echo "Starting uninstall process for user '$TARGET_USER'..."

# Call cleanup script
echo "Running cleanup script..."
"$(dirname "$0")"/cleanup.sh

# Stop and disable services
echo "Stopping and disabling services..."
sudo systemctl stop nomad || true
sudo systemctl disable nomad || true
sudo systemctl stop consul || true
sudo systemctl disable consul || true
sudo systemctl stop docker || true
sudo systemctl disable docker || true

# Remove services
echo "Removing systemd service files..."
sudo rm -f /etc/systemd/system/nomad.service
sudo rm -f /etc/systemd/system/consul.service
sudo rm -rf /etc/systemd/system/nomad.service.d

# Purge packages
echo "Purging installed packages..."
sudo apt-get purge -y \
    acl build-essential cmake cargo chrony cmatrix cowsay curl figlet fio \
    fortune-mod fuse-overlayfs gstreamer1.0-libav git hollywood htop iperf3 jq \
    libavif16 libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev \
    libavfilter-dev libswscale-dev libswresample-dev libcurl4-openssl-dev \
    libevent-2.1-7t64 libflite1 libgstreamer-plugins-bad1.0-0 libmecab-dev \
    lolcat make mecab mecab-ipadic-utf8 mosh ncdu nfs-common openssh-server \
    pkg-config portaudio19-dev python3 python3-dev python3-full python3-pip \
    python3-venv python3-virtualenv rsync rustc sl sshpass sysbench toilet \
    tmux ufw unzip yq docker.io docker-doc docker-compose podman-docker \
    containerd runc
sudo apt-get autoremove -y

# Remove binaries
echo "Removing binaries..."
sudo rm -f /usr/local/bin/nomad
sudo rm -f /usr/local/bin/consul
sudo rm -f /usr/local/bin/update-ssh-authorized-keys.sh

# Remove directories
echo "Removing directories..."
sudo rm -rf /opt/cluster-infra
sudo rm -rf /opt/nomad
sudo rm -rf /opt/consul
sudo rm -rf /etc/consul.d
sudo rm -rf /etc/nomad.d
sudo rm -rf /opt/cni
sudo rm -rf /opt/pipecatapp
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
sudo rm -rf /etc/docker

# Remove user and sudoers file
echo "Removing user '$TARGET_USER' and sudoers file..."
sudo userdel -r "$TARGET_USER" || true
sudo rm -f "/etc/sudoers.d/ansible-$TARGET_USER-nopasswd"

# Remove environment file
echo "Removing environment file..."
sudo rm -f /etc/profile.d/nomad.sh

# Revert /etc/hosts
echo "Reverting /etc/hosts..."
echo "WARNING: This will remove any lines containing '# ANSIBLE MANAGED BLOCK' from /etc/hosts."
sudo sed -i '/# ANSIBLE MANAGED BLOCK/d' /etc/hosts

echo "Uninstall complete."
echo "Please reboot the system to ensure all changes are applied."

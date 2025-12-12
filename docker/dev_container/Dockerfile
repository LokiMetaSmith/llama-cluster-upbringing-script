FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    systemd \
    systemd-sysv \
    curl \
    wget \
    git \
    sudo \
    python3 \
    python3-pip \
    python3-venv \
    software-properties-common \
    gnupg \
    ca-certificates \
    apt-transport-https \
    lsb-release \
    net-tools \
    iproute2 \
    dnsutils \
    vim \
    nano \
    rsync \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CE (Client and Engine)
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (LTS) for Gemini CLI
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Gemini CLI
RUN npm install -g @google/gemini-cli

# Install Ansible Core
RUN pip3 install ansible-core

# Create user pipecatapp
RUN useradd -m -s /bin/bash pipecatapp && \
    usermod -aG sudo pipecatapp && \
    usermod -aG docker pipecatapp && \
    echo "pipecatapp ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Configure systemd to run inside container
# (We rely on standard systemd behavior but mask units that fail in containers)
RUN systemctl mask \
    dev-hugepages.mount \
    sys-fs-fuse-connections.mount

# Set working directory
WORKDIR /opt/cluster-infra

# Set the stop signal
STOPSIGNAL SIGRTMIN+3

# Start systemd as the entrypoint
ENTRYPOINT ["/lib/systemd/systemd"]

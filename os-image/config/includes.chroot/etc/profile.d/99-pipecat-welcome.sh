#!/bin/bash
# Wait up to 10 seconds for an IP address
max_attempts=10
attempt=0
IP=""
while [ $attempt -lt $max_attempts ]; do
    IP=$(hostname -I | awk '{print $1}')
    if [ -n "$IP" ]; then
        break
    fi
    sleep 1
    attempt=$((attempt+1))
done

if [ -z "$IP" ]; then
    IP="No IP found (check network)"
fi

echo ""
echo "================================================================"
echo " Welcome to the Pipecat Cluster Installer!                      "
echo "================================================================"
echo ""

# SSH Key Provisioning
if [ ! -f /etc/pipecat_github_user ] && [ ! -f /home/pipecatapp/.ssh/.skip_github_keys ]; then
    echo "SSH keys for the 'pipecatapp' user have not been configured yet."
    echo "To enable SSH access, please enter your GitHub username (or press Enter to use default 'LokiMetaSmith'):"
    read -r -t 30 github_user
    echo ""
    if [ -z "$github_user" ]; then
        github_user="LokiMetaSmith"
        echo "No input provided. Using default GitHub user: $github_user"
    fi

    if [ -n "$github_user" ] && [ "$github_user" != "skip" ]; then
        sudo /usr/local/bin/setup-ssh-keys.sh "$github_user"
    elif [ "$github_user" = "skip" ]; then
        echo "Skipping SSH key setup. You can run 'sudo setup-ssh-keys.sh <github_username>' later."
        touch /home/pipecatapp/.ssh/.skip_github_keys
    fi
elif [ -f /etc/pipecat_github_user ] && [ ! -f /home/pipecatapp/.ssh/.keys_fetched ]; then
    # Automatically fetch keys on first boot if pre-configured
    github_user=$(cat /etc/pipecat_github_user)
    sudo /usr/local/bin/setup-ssh-keys.sh "$github_user" >/dev/null 2>&1
    touch /home/pipecatapp/.ssh/.keys_fetched
fi
echo ""
echo " System Details:"
echo "   Hostname: $(hostname)"
echo "   IP Address: $IP"
echo ""
echo " The system is running from the bootable media."
echo " To install and configure the cluster agent or control node, run:"
echo ""
echo "   cd /opt/pipecat-cluster && sudo ./bootstrap.sh"
echo ""
echo " For more details, see the README.md in the project directory."
echo "================================================================"
echo ""

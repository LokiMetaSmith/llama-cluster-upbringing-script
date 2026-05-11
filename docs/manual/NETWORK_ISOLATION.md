# AI Cluster Network Isolation Guide

When an autonomous AI agent is capable of writing and executing infrastructure scripts, implementing hard network boundaries is essential. Operating the cluster on a flat home network introduces significant security risks.

This guide outlines how to establish a "DMZ" (Demilitarized Zone) for your AI cluster, ensuring the agent has necessary outbound access without exposing your personal home network to automated scans or unintended intrusion.

## The Topology Trap: Avoid "Double NAT"

If you simply plug the WAN port of a *new* cluster router into a LAN port on your *existing* home router, you **do not** achieve isolation. In that setup, the cluster router treats your home network as "the internet." An autonomous agent would still be able to scan your subnet, reach your personal devices, and attempt connections.

## Ideal Architectures

The following are the two recommended methods to lock down the cluster securely.

### 1. The Dedicated Router Interface (Recommended)

If your primary home firewall/router has an unused physical interface, dedicate it entirely to the cluster.

* **Physical Layer:** Connect this dedicated router interface directly to a high-throughput managed switch to handle intra-node traffic.
* **Network Layer:** Assign this interface its own distinct subnet (e.g., `10.99.99.0/24`).
* **Firewall Rules:** Create a rule that **blocks** all traffic originating from the cluster subnet destined for your home subnet, but **allows** traffic out to the WAN (Internet).

### 2. The VLAN Approach (Layer 2 Isolation)

If you don't have a spare physical port on the router, but your switch and router support 802.1Q VLAN tagging, you can achieve identical security logically.

#### Switch Configuration (Example: UniFi EdgeSwitch CLI)

Assuming we use VLAN 99 for the cluster, port 1 connects to your EdgeRouter (Trunk), and ports 2-10 connect to your AI nodes (Access):

```text
enable
configure

# Create the Cluster VLAN
vlan database
vlan 99
vlan name 99 "AI-Cluster"
quit

# Configure the Uplink Port (Port 1) as a Trunk to the EdgeRouter
interface 0/1
vlan pvid 1
vlan participation include 1,99
vlan tagging 99
quit

# Configure Cluster Node Ports (Ports 2-10) as Access Ports on VLAN 99
interface range 0/2-0/10
vlan pvid 99
vlan participation include 99
vlan participation exclude 1
quit

write memory
```

#### Router Configuration (Example: Ubiquiti EdgeRouter CLI)

Assuming `eth1` is the physical interface connected to the EdgeSwitch, and your Home LAN is `192.168.1.0/24`:

```text
configure

# 1. Create the VLAN 99 Virtual Interface & Assign IP
set interfaces ethernet eth1 vif 99 address 10.99.99.1/24
set interfaces ethernet eth1 vif 99 description "AI-Cluster-VLAN"

# 2. Configure DHCP Server for the Cluster Subnet
set service dhcp-server shared-network-name CLUSTER-VLAN subnet 10.99.99.0/24 default-router 10.99.99.1
set service dhcp-server shared-network-name CLUSTER-VLAN subnet 10.99.99.0/24 dns-server 1.1.1.1
set service dhcp-server shared-network-name CLUSTER-VLAN subnet 10.99.99.0/24 start 10.99.99.50 stop 10.99.99.200

# 3. Create the Firewall Ruleset for the Cluster (Inbound from cluster's perspective)
set firewall name CLUSTER_IN default-action drop
set firewall name CLUSTER_IN description "Traffic from Cluster VLAN"

# Rule 1: Allow Established/Related traffic (so pinging Google works)
set firewall name CLUSTER_IN rule 10 action accept
set firewall name CLUSTER_IN rule 10 state established enable
set firewall name CLUSTER_IN rule 10 state related enable

# Rule 2: Deny traffic destined for your Home LAN (CRITICAL SECURITY RULE)
set firewall name CLUSTER_IN rule 20 action drop
set firewall name CLUSTER_IN rule 20 destination address 192.168.1.0/24
set firewall name CLUSTER_IN rule 20 description "Block Cluster from accessing Home LAN"

# Rule 3: Allow outbound WAN traffic (Internet access for downloading models, etc.)
set firewall name CLUSTER_IN rule 30 action accept
set firewall name CLUSTER_IN rule 30 description "Allow outbound Internet"

# 4. Apply the Ruleset to the VLAN Interface
set interfaces ethernet eth1 vif 99 firewall in name CLUSTER_IN

commit
save
quit
```

## The Management "Pinhole"

Regardless of whether you use a dedicated physical interface or a logical VLAN, your routing rules must be strictly asymmetric.

You must establish a single firewall rule that allows your admin machine on the home network to initiate SSH and Web UI connections *into* the cluster subnet. Conversely, the cluster must be explicitly denied from initiating any connections *back* into your home network.

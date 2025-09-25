/**
 * @file traffic_monitor.c
 * @brief An eBPF program to monitor and count TCP packets by destination port.
 *
 * This program is designed to be attached to a network interface using XDP
 * (eXpress Data Path). It efficiently inspects incoming packets at the kernel
 * level, parses them to identify TCP packets, and increments a counter for
 * each unique destination port in a BPF hash map. This allows a userspace
 * application (like power_agent.py) to monitor service activity with very
 * low overhead.
 */
#include <uapi/linux/bpf.h>
#include <uapi/linux/if_ether.h>
#include <uapi/linux/ip.h>
#include <uapi/linux/tcp.h>

/**
 * @brief BPF hash map to store packet counts per destination port.
 *
 * This map is the interface between the eBPF kernel program and the userspace
 * monitoring application.
 * - The key is the destination port number (u16).
 * - The value is the total packet count for that port (u64).
 */
BPF_HASH(packet_counts, u16, u64);

/**
 * @brief The main eBPF/XDP function to process incoming packets.
 *
 * This function is attached to a network interface and is executed for every
 * packet received. It performs the following steps:
 * 1. Parses the Ethernet, IP, and TCP headers.
 * 2. Checks packet boundaries to prevent out-of-bounds access.
 * 3. Filters for TCP/IP packets.
 * 4. Extracts the destination port from the TCP header.
 * 5. Increments the corresponding counter in the `packet_counts` hash map.
 *
 * @param ctx A pointer to the XDP metadata context.
 * @return Returns XDP_PASS to allow the packet to continue up the network
 *         stack, as this program is only for monitoring.
 */
int xdp_traffic_monitor(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;

    struct ethhdr *eth = data;

    // Ensure the packet has a valid Ethernet header.
    if ((void *)eth + sizeof(*eth) > data_end) {
        return XDP_PASS;
    }

    // We only care about IP packets.
    if (eth->h_proto != __constant_htons(ETH_P_IP)) {
        return XDP_PASS;
    }

    struct iphdr *ip = data + sizeof(*eth);
    // Ensure the packet has a valid IP header.
    if ((void *)ip + sizeof(*ip) > data_end) {
        return XDP_PASS;
    }

    // We only care about TCP packets.
    if (ip->protocol != IPPROTO_TCP) {
        return XDP_PASS;
    }

    struct tcphdr *tcp = (void *)ip + sizeof(*ip);
    // Ensure the packet has a valid TCP header.
    if ((void *)tcp + sizeof(*tcp) > data_end) {
        return XDP_PASS;
    }

    // Get the destination port from the TCP header.
    u16 dport = tcp->dest;

    // Increment the packet count for this destination port in the hash map.
    u64 *count = packet_counts.lookup(&dport);
    if (count) {
        // If an entry exists, increment it.
        *count += 1;
    } else {
        // If no entry exists, create one with a count of 1.
        u64 one = 1;
        packet_counts.update(&dport, &one);
    }

    // Pass the packet up the network stack. We are only monitoring.
    return XDP_PASS;
}

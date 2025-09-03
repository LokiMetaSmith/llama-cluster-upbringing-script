#include <uapi/linux/bpf.h>
#include <uapi/linux/if_ether.h>
#include <uapi/linux/ip.h>
#include <uapi/linux/tcp.h>

// A hash map to store packet counts per destination port.
// The key is the destination port (u16), and the value is the packet count (u64).
BPF_HASH(packet_counts, u16, u64);

// This is the main eBPF program function that will be attached to a network interface.
// For now, it's a simple placeholder.
int xdp_traffic_monitor(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;

    struct ethhdr *eth = data;

    // Ensure the packet has an Ethernet header.
    if ((void *)eth + sizeof(*eth) > data_end) {
        return XDP_PASS;
    }

    // We only care about IP packets.
    if (eth->h_proto != __constant_htons(ETH_P_IP)) {
        return XDP_PASS;
    }

    struct iphdr *ip = data + sizeof(*eth);
    // Ensure the packet has an IP header.
    if ((void *)ip + sizeof(*ip) > data_end) {
        return XDP_PASS;
    }

    // We only care about TCP packets.
    if (ip->protocol != IPPROTO_TCP) {
        return XDP_PASS;
    }

    struct tcphdr *tcp = (void *)ip + sizeof(*ip);
    // Ensure the packet has a TCP header.
    if ((void *)tcp + sizeof(*tcp) > data_end) {
        return XDP_PASS;
    }

    // Get the destination port.
    u16 dport = tcp->dest;

    // Increment the packet count for this destination port.
    u64 *count = packet_counts.lookup(&dport);
    if (count) {
        *count += 1;
    } else {
        u64 one = 1;
        packet_counts.update(&dport, &one);
    }

    return XDP_PASS;
}

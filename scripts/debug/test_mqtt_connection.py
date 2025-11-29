import socket
import time
import sys
import subprocess
import os

def get_ip_addresses():
    """Get all non-loopback IP addresses."""
    ips = set()
    try:
        # Try to get hostname IPs
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            ips.add(ip)
    except:
        pass

    # Try to get interface IPs using ip command (linux specific)
    try:
        output = subprocess.check_output(['hostname', '-I']).decode().strip()
        for ip in output.split():
            ips.add(ip)
    except:
        pass

    ips.add('127.0.0.1')
    return list(ips)

def check_port(host, port, timeout=2):
    """Check if a port is open on a host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                return True
    except:
        pass
    return False

def main():
    port = 1883
    ips = get_ip_addresses()
    print(f"Checking connectivity to MQTT port {port} on IPs: {ips}")
    print("Press Ctrl+C to stop.")

    start_time = time.time()
    # Run indefinitely until user stops, as they are debugging a restart loop

    try:
        while True:
            found_open = False
            for ip in ips:
                if check_port(ip, port):
                    print(f"[{time.strftime('%H:%M:%S')}] SUCCESS: Connected to {ip}:{port}")
                    found_open = True

            if not found_open:
                # Optional: print failure every once in a while
                # print(f"[{time.strftime('%H:%M:%S')}] No connection on any IP")
                pass

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()

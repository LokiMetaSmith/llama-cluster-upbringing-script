#!/usr/bin/env python3
"""
Robust Remote Node Recovery
A tool to monitor and recover cluster nodes when their network stack fails,
utilizing IPMI (Intelligent Platform Management Interface) to force a hardware reset.
"""

import argparse
import subprocess
import time
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ping_node(ip, count=3, timeout=2):
    """Pings a node to verify network connectivity."""
    logging.info(f"Pinging node {ip}...")
    success_count = 0
    for _ in range(count):
        try:
            # -W is timeout in seconds, -c is packet count
            subprocess.check_output(
                ['ping', '-c', '1', '-W', str(timeout), ip],
                stderr=subprocess.STDOUT
            )
            success_count += 1
        except subprocess.CalledProcessError:
            pass
        time.sleep(1)

    return success_count > 0

def ipmi_set_pxe_boot(ipmi_host, user, password):
    """Configures the hardware to boot from PXE on the next restart."""
    logging.warning(f"Setting boot device to PXE for {ipmi_host}...")
    try:
        subprocess.check_call([
            'ipmitool', '-I', 'lanplus', '-H', ipmi_host,
            '-U', user, '-P', password, 'chassis', 'bootdev', 'pxe'
        ])
        logging.info("IPMI boot device set to PXE successfully.")
        return True
    except FileNotFoundError:
        logging.error("ipmitool is not installed. Please install it (e.g., apt-get install ipmitool).")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute IPMI command to set PXE boot: {e}")
        return False

def ipmi_reboot(ipmi_host, user, password):
    """Sends an IPMI power cycle/reset command to the target hardware."""
    logging.warning(f"Initiating IPMI power reset for {ipmi_host}...")
    try:
        subprocess.check_call([
            'ipmitool', '-I', 'lanplus', '-H', ipmi_host,
            '-U', user, '-P', password, 'power', 'reset'
        ])
        logging.info("IPMI reset command sent successfully.")
        return True
    except FileNotFoundError:
        logging.error("ipmitool is not installed. Please install it (e.g., apt-get install ipmitool).")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute IPMI command: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Robust Remote Node Recovery via IPMI")
    parser.add_argument("--node-ip", required=True, help="IP address of the node to check")
    parser.add_argument("--ipmi-host", required=True, help="IPMI network address (BMC IP)")
    parser.add_argument("--ipmi-user", required=True, help="IPMI username")
    parser.add_argument("--ipmi-password", required=True, help="IPMI password")
    parser.add_argument("--retries", type=int, default=3, help="Number of ping retries before reset")
    parser.add_argument("--force-pxe", action="store_true", help="Force the node to boot into PXE on reset")
    parser.add_argument("--pxe-server-ip", type=str, help="IP address of the PXE server to check availability before forcing PXE")

    args = parser.parse_args()

    if ping_node(args.node_ip, count=args.retries):
        logging.info(f"Node {args.node_ip} is reachable. No recovery action needed.")
        sys.exit(0)
    else:
        logging.error(f"Node {args.node_ip} is unreachable! Network stack might be down.")

        if args.force_pxe:
            if args.pxe_server_ip:
                logging.info(f"Checking PXE server availability at {args.pxe_server_ip}...")
                if not ping_node(args.pxe_server_ip, count=1, timeout=2):
                    logging.error(f"PXE server {args.pxe_server_ip} is unreachable. Aborting PXE reset to prevent bricking.")
                    sys.exit(1)
                else:
                    logging.info(f"PXE server {args.pxe_server_ip} is available.")

            pxe_success = ipmi_set_pxe_boot(args.ipmi_host, args.ipmi_user, args.ipmi_password)
            if not pxe_success:
                logging.error("Failed to set PXE boot. Aborting recovery to avoid unwanted state.")
                sys.exit(1)

        success = ipmi_reboot(args.ipmi_host, args.ipmi_user, args.ipmi_password)
        if success:
            logging.info("Recovery action completed. Wait for the node to reboot.")
            sys.exit(0)
        else:
            logging.error("Recovery action failed. Manual intervention required.")
            sys.exit(1)

if __name__ == "__main__":
    main()

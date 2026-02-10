#!/usr/bin/env python3
"""Starter template for the port knocking server."""

import argparse
import logging
import socket
import time
import argparse
import subprocess
import sys

DEFAULT_KNOCK_SEQUENCE = [1234, 5678, 9012]
DEFAULT_PROTECTED_PORT = 2222
DEFAULT_SEQUENCE_WINDOW = 10.0


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def open_protected_port(protected_port, ip):
    """Open the protected port using firewall rules."""
    # TODO: Use iptables/nftables to allow access to protected_port.
    logging.info("TODO: Open firewall for %s on port %s", ip, protected_port)
    try:
        cmd = ["iptables", "-I", "INPUT", "1", "-s", ip, "-p", "tcp", "--dport", str(protected_port), "-j", "ACCEPT"]
        subprocess.run(cmd, check=True)
    except Exception as e:
        logging.error(f"Failed to open port: {e}")


def close_protected_port(protected_port):
    """Close the protected port using firewall rules."""
    # TODO: Remove firewall rules for protected_port.
    logging.info("TODO: Close firewall for port %s", protected_port)
    try:
        # Flush existing rules to start clean
        subprocess.run(["iptables", "-F"], check=False)
        # Allow established connections
        subprocess.run(["iptables", "-A", "INPUT", "-m", "conntrack", "--ctstate", "ESTABLISHED,RELATED", "-j", "ACCEPT"], check=False)
        # Drop new connections to the hidden port
        cmd = ["iptables", "-A", "INPUT", "-p", "tcp", "--dport", str(protected_port), "-j", "DROP"]
        subprocess.run(cmd, check=True) 
    except Exception as e:
        logging.error(f"Failed to open port: {e}")


def listen_for_knocks(sequence, window_seconds, protected_port):
    """Listen for knock sequence and open the protected port."""
    logger = logging.getLogger("KnockServer")
    logger.info("Listening for knocks: %s", sequence)
    logger.info("Protected port: %s", protected_port)

    # Make sure port is closed
    close_protected_port(protected_port)

    # TODO: Create UDP or TCP listeners for each knock port.
    socks = []
    socks_map = {}
    for port in sequence:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', port))
            s.listen(5)
            s.setblocking(False)
            socks.append(s)
            socks_map[s] = port
        except Exception as e:
            logger.error(f"Failed to bind {port}: {e}")
            return

    # TODO: Track each source IP and its progress through the sequence.
    client_state = {}

    while True:
        current_time = time.time()

        for s in socks:
            try:
                conn, addr = s.accept()

                ip = addr[0]
                knock_port = socks_map[s]
                conn.close() # Close immediately

                if ip not in client_state:
                    client_state[ip] = {'index': 0, 'last_seen': current_time}

                state = client_state[ip]

                # TODO: Enforce timing window per sequence.
                if current_time - state['last_seen'] > window_seconds:
                    logger.info(f"Timeout for {ip}")
                    state['index'] = 0

                state['last_seen'] = current_time
                expected_port = sequence[state['index']]

                # TODO: On correct sequence, call open_protected_port().
                if knock_port == expected_port:
                    logger.info(f"Correct knock: {knock_port} from {ip}")
                    state['index'] += 1

                    if state['index'] == len(sequence):
                        open_protected_port(ip, protected_port)
                        del client_state[ip] # Reset state after success

                # TODO: On incorrect sequence, reset progress.
                else:
                    logger.info(f"Wrong knock: {knock_port} from {ip}. Resetting.")
                    state['index'] = 0
            
            except Exception as e:
                logger.error(f"Error handling knock: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description="Port knocking server starter")
    parser.add_argument(
        "--sequence",
        default=",".join(str(port) for port in DEFAULT_KNOCK_SEQUENCE),
        help="Comma-separated knock ports",
    )
    parser.add_argument(
        "--protected-port",
        type=int,
        default=DEFAULT_PROTECTED_PORT,
        help="Protected service port",
    )
    parser.add_argument(
        "--window",
        type=float,
        default=DEFAULT_SEQUENCE_WINDOW,
        help="Seconds allowed to complete the sequence",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging()

    try:
        sequence = [int(port) for port in args.sequence.split(",")]
    except ValueError:
        raise SystemExit("Invalid sequence. Use comma-separated integers.")

    listen_for_knocks(sequence, args.window, args.protected_port)


if __name__ == "__main__":
    main()

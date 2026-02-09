#!/usr/bin/env python3
"""
Port Scanner - Starter Template for Students
Assignment 2: Network Security

This is a STARTER TEMPLATE to help you get started.
You should expand and improve upon this basic implementation.

TODO for students:
1. Implement multi-threading for faster scans
2. Add banner grabbing to detect services
3. Add support for CIDR notation (e.g., 192.168.1.0/24)
4. Add different scan types (SYN scan, UDP scan, etc.)
5. Add output formatting (JSON, CSV, etc.)
6. Implement timeout and error handling
7. Add progress indicators
8. Add service fingerprinting
"""

import socket
import sys
import concurrent.futures
import argparse
import ipaddress


def scan_port(target, port, timeout=1.0):
    """
    Scan a single port on the target host

    Args:
        target (str): IP address or hostname to scan
        port (int): Port number to scan
        timeout (float): Connection timeout in seconds

    Returns:
        bool: True if port is open, False otherwise
    """
    try:
        # TODO: Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO: Set timeout
        s.settimeout(timeout)
        # TODO: Try to connect to target:port
        connection = s.connect_ex((target, port))
        # TODO: Close the socket
        s.close()
        # TODO: Return True if connection successful
        return connection == 0 

        #pass  # Remove this and implement

    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def scan_range(target, start_port, end_port, max_threads=2000):
    """
    Scan a range of ports on the target host

    Args:
        target (str): IP address or hostname to scan
        start_port (int): Starting port number
        end_port (int): Ending port number

    Returns:
        list: List of open ports
    """
    open_ports = []

    print(f"[*] Scanning {target} from port {start_port} to {end_port}")
    print(f"[*] This may take a while...")

    # TODO: Implement the scanning logic
    # Hint: Loop through port range and call scan_port()
    # Hint: Consider using threading for better performance
    

    
    with concurrent.futures.ThreadPoolExecutor(max_threads) as threads:
        ports_threads = {
            # TODO: Scan this port
            threads.submit(scan_port,target,port): port
            for port in range(start_port,end_port +1)
        }

        for finished_thread in concurrent.futures.as_completed(ports_threads):
            port = ports_threads[finished_thread]

            is_port_open = finished_thread.result()

            # TODO: If open, add to open_ports list
            if is_port_open == True:
                open_ports.append(port)

            # TODO: Print progress (optional)
            #pass  # Remove this and implement

    return open_ports


def main():
    """Main function"""
    # TODO: Parse command-line arguments

    parser = argparse.ArgumentParser()

    # Command line arguments
    parser.add_argument("--target", required=True)
    parser.add_argument("--ports", required = True)
    parser.add_argument("--threads", type=int, default=100)

    args = parser.parse_args()
    # TODO: Validate inputs

    # Validate target arg 
    targets = []
    if "/" in args.target:
        # Network range
        try:
            network = ipaddress.ip_network(args.target, strict=False)
            targets = [str(ip) for ip in network.hosts()]
        except ValueError:
            print("Error: Invalid target argument.")
            sys.exit(1)
    else:
        # IP 
        targets = [args.target]

    # Validate port arg 
    try:
        if "-" in args.ports:
            start_port, end_port = map(int, args.ports.split("-"))
        else:
            start_port = int(args.ports)
            end_port = int(args.ports)
    except ValueError:
        print("Error: Invalid ports argument")
        sys.exit(1)

    
    # TODO: Call scan_range()
    total_open_ports = 0
    
    for target in targets:
        open_ports = scan_range(target, start_port, end_port, args.threads)

        # TODO: Display results
        if open_ports:
            print(f"\n[+] Results for {target}:")
            for port in open_ports:
                print(f"    Port {port}: open")
            total_open_ports += len(open_ports)

    print(f"\n[+] Scan complete!")
    print(f"[+] Found {total_open_ports} open ports:")


if __name__ == "__main__":
    main()

## Port Knocking Starter Template

This directory is a starter template for the port knocking portion of the assignment.

### What you need to implement
- Protected service/port: 3306.
- Define a knock sequence: 1234, 5678, 9012
- Implement a server that listens for knocks and validates the sequence.
- Open the protected port only after a valid sequence.
- Add timing constraints and reset on incorrect sequences.
- Implement a client to send the knock sequence.

### Getting started
1. Implement your server logic in `knock_server.py`.
2. Implement your client logic in `knock_client.py`.
3. Update `demo.sh` to demonstrate your flow.
4. Run from the repo root with `docker compose up port_knocking`.

### Usage
```bash
python3 knock_client.py --target 172.20.0.40 --sequence 1234,5678,9012 --check
```

### Implementation ###
I implemented the port knocking using knockd and iptables commands to drop all the incoming connections by default and allows already connections that properly "knock" onto the correct ports. The sequence that it should go through is 1234,5678,9012 and then the database port 3306 should open to the user. It does this by updating the firewall which was previously rejecting all packets and allows the usses to access the hidden port. 
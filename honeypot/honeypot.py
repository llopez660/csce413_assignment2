#!/usr/bin/env python3
"""Starter template for the honeypot assignment."""

import logging
import os
import time
import socket
import paramiko
import threading
from logger import setup_logging


LOG_PATH = "/app/logs/honeypot.log"

# Generate host key to start an SSH server
HOST_KEY = paramiko.RSAKey.generate(2048)

class HoneypotServer(paramiko.ServerInterface):
    def __init__(self, client_ip, logger):
        self.client_ip = client_ip
        self.logger = logger
        self.start_time = time.time()
        self.event = threading.Event()

    # Seeing what kind of request they're making and if its a session use paramiko to trick attacker 
    def check_channel_request(self, request_kind, channel_id):
        if request_kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # Logging the credentials being used from attacker
    def check_auth_password(self, username, password):
        log_message = f"Attacker's IP: {self.client_ip} attempted to log in with username: {username} and password: {password}"
    
        # Log the message
        self.logger.info(log_message, extra={'client_ip': self.client_ip})
        
        # Keep attacker guessing
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"
    
def handle_connection(client, addr, logger):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    
    # Start the SSH server with genereated Host Key from beginning
    server = HoneypotServer(addr[0], logger)
    try:
        transport.start_server(server=server)
        
        # 35sec timeout if nothing close connection
        channel = transport.accept(35)
        if channel is None:
            transport.close()
            return

        transport.close()
        
    except Exception as e:
        pass
    finally:
        transport.close()


def run_honeypot():
    logger = setup_logging()

    # The docker-compose maps this to port 2222 (external) to 22 (internal) 
    bind_ip = '0.0.0.0'
    bind_port = 22

    log_message = f"SSH Honeypot is now running on IP: {bind_ip} and listening on Port: {bind_port}"
    
    logger.info(log_message, extra={'client_ip': 'SYSTEM'})

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind_ip, bind_port))
        sock.listen(100)
        
        while True:
            try:
                client, addr = sock.accept()
                logger.info(f"Connection from {addr[0]}:{addr[1]}", extra={'client_ip': addr[0]})
                
                # Handle each attacker in a new thread
                t = threading.Thread(target=handle_connection, args=(client, addr, logger))
                t.start()
            except Exception as e:
                logger.error(f"Socket Error: {e}", extra={'client_ip': 'SYSTEM'})

    except Exception as e:
        logger.error(f"Failed to bind port: {e}", extra={'client_ip': 'SYSTEM'})

if __name__ == "__main__":
    run_honeypot()

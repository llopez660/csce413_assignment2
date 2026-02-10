"""Logging helpers for the honeypot."""

import logging
import os
import sys

LOG_PATH = "/app/logs/honeypot.log"


def setup_logging():
    # Ensure log exists
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    # Create a custom logger
    logger = logging.getLogger("Honeypot")
    logger.setLevel(logging.INFO)
    
    # Different handlers for console and file 
    if not logger.handlers:
        # File Handler
        file_handler = logging.FileHandler(LOG_PATH)
        file_formatter = logging.Formatter('%(asctime)s - IP:%(client_ip)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter('%(asctime)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
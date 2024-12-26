import psutil
import platform
import uuid
import socket
import subprocess
import threading
from datetime import datetime
import hashlib
import os
import sys
import logging

Set up logging
logging.basicConfig(filename='hardware_check.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def check_hardware_drives():
    # Get disk partitions
    partitions = psutil.disk_partitions()

    # Iterate through partitions and check if they're working
    for partition in partitions:
        try:
            # Get disk usage statistics
            usage = psutil.disk_usage(partition.mountpoint)

            # Check if disk is working
            if usage.percent < 100:
                logging.info(f"Disk {partition.device} is working")
            else:
                logging.warning(f"Disk {partition.device} is full")
        except Exception as e:
            logging.error(f"Error checking disk {partition.device}: {e}")

def check_internet_connectivity():
    # Try to ping Google's DNS server
    try:
        subprocess.check_call(['ping', '-c', '1', '8.8.8.8'])
        logging.info("Internet connectivity is working")
    except subprocess.CalledProcessError:
        logging.warning("Internet connectivity is not working")

def check_network_interfaces():
    # Get network interfaces
    interfaces = psutil.net_if_addrs()

    # Iterate through interfaces and check if they're working
    for interface, snics in interfaces.items():
        for snic in snics:
            if snic.family == socket.AF_INET:
                # Check if interface is working
                try:
                    socket.inet_aton(snic.address)
                    logging.info(f"Network interface {interface} is working")
                except socket.error:
                    logging.warning(f"Network interface {interface} is not working")

def check_system_info():
    # Get system info
    system_info = platform.system()
    release_info = platform.release()
    version_info = platform.version()

    # Log system info
    logging.info(f"System: {system_info}")
    logging.info(f"Release: {release_info}")
    logging.info(f"Version: {version_info}")

def check_uuid():
    # Get UUID
    uuid_value = uuid.getnode()

    # Log UUID
    logging.info(f"UUID: {uuid_value}")

def check_hash():
    # Get current date and time
    current_datetime = datetime.now()

    # Create hash object
    hash_object = hashlib.sha256(str(current_datetime).encode())

    # Log hash
    logging.info(f"Hash: {hash_object.hexdigest()}")

def main():
    # Create threads for each function
    threads = [
        threading.Thread(target=check_hardware_drives),
        threading.Thread(target=check_internet_connectivity),
        threading.Thread(target=check_network_interfaces),
        threading.Thread(target=check_system_info),
        threading.Thread(target=check_uuid),
        threading.Thread(target=check_hash)
    ]

    # Start threads
    for thread in threads:
        thread.start()

    # Wait for threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

import daemon
from daemon.pidfile import TimeoutPIDLockFile
from _logging import get_logger_manager, get_logger
from linux_socket import LinuxSocket
import signal
import sys
import time
import os
import socket

logger = get_logger(__name__)

class LinuxDaemon:
    def __init__(self, pidfile='/tmp/task-log-daemon.pid'):
        self.pidfile = pidfile
        self.linux_socket = LinuxSocket()
        self.running = True

    def run(self):
        self.linux_socket.setup_socket()
        logger.info("Daemon is running with socket communication...")

        while self.running:
            try:
                conn, _ = self.linux_socket.server_socket.accept()
                with conn:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        continue
                    logger.info(f"Received message: {data}")
                    conn.sendall(f"ACK: {data}".encode())

                    # if data.lower() == "stop":
                    #     self.running = False
            except socket.timeout:
                continue
            except socket.error as e:
                logger.error(f"Socket error: {e}")
                break
        logger.info("Daemon is stopped")
        self.linux_socket.cleanup_socket()

    def stop(self): 
        logger.info("Daemon is stopping...")
        try:
            with open(self.pidfile, 'r') as f:
                pid = int(f.read().strip())
                os.kill(pid, signal.SIGTERM)
        except Exception as e:
            message = "Error occurred while opening the PID file."
            logger.error(e)
            raise Exception(message)

    def signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}, stopping daemon loop...")
        self.running = False

    def start(self):
        logger_manager = get_logger_manager()
        with daemon.DaemonContext(
            stdout = open(logger_manager.stdout_path, 'a+', buffering=1),
            stderr = open(logger_manager.stderr_path, 'a+', buffering=1),
            pidfile=TimeoutPIDLockFile(self.pidfile),
            signal_map={
                signal.SIGTERM: self.signal_handler,
                signal.SIGINT: self.signal_handler,
            },
            files_preserve=logger_manager.fileno_list
        ):
            self.run()
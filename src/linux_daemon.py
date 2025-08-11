import daemon
from daemon.pidfile import TimeoutPIDLockFile
from _logging import get_logger_manager, get_logger
import signal
import sys
import time
import os

logger = get_logger(__name__)

class LinuxDaemon:
    def __init__(self, pidfile='/tmp/task-log-daemon.pid'):
        self.pidfile = pidfile
        self.running = True

    def run(self):
        logger.info("Daemon is running...")
        while self.running:
            time.sleep(10)
        
        logger.info("Daemon is stoped")

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

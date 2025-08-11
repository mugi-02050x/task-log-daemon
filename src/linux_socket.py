import daemon
from daemon.pidfile import TimeoutPIDLockFile
from _logging import get_logger_manager, get_logger
import signal
import sys
import time
import os
import socket

logger = get_logger(__name__)

class LinuxSocket:
    def __init__(self, sock_path='/tmp/task-log-daemon.sock'):
        self.sock_path = sock_path

    def setup_socket(self):
        """UNIXドメインソケットの準備"""
        if os.path.exists(self.sock_path):
            os.remove(self.sock_path)

        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_socket.bind(self.sock_path)
        self.server_socket.listen(5)
        self.server_socket.settimeout(1)
        logger.info(f"Socket listening on {self.sock_path}")

    def cleanup_socket(self):
        """ソケットファイルのクリーンアップ"""
        logger.info("cleanUp Socket")
        if self.server_socket:
            self.server_socket.close()
        if os.path.exists(self.sock_path):
            os.remove(self.sock_path)
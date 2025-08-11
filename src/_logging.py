import os
import logging
from threading import Lock

class LoggerManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._setup_done = False
            return cls._instance

    def setup(self, stdout_redirect_file_name='task-log-daemon.log', stderr_redirect_file_name='task-log-daemon.err'):
        if self._setup_done:
            return  # 既に初期化済みならスキップ

        self.log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tmp', 'logs'))
        os.makedirs(self.log_dir, exist_ok=True)

        self.stdout_path = os.path.join(self.log_dir, stdout_redirect_file_name)
        self.stderr_path = os.path.join(self.log_dir, stderr_redirect_file_name)

        self._setup_logger(self.stdout_path, self.stderr_path)
        self._setup_done = True

    def _setup_logger(self, stdout, stderr):
        log_format = '%(asctime)s %(name)s %(levelname)s %(message)s'
        formatter = logging.Formatter(log_format)
    
        # 標準出力ログファイル（DEBUG以上全部）
        std_handler = logging.FileHandler(stdout)
        std_handler.setLevel(logging.DEBUG)
        std_handler.setFormatter(formatter)
    
        # エラーログファイル（ERROR以上）
        err_handler = logging.FileHandler(stderr)
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(formatter)
    
        logging.basicConfig(
            level=logging.DEBUG,  # 全体のログレベルをDEBUGに
            format=log_format,
            handlers=[std_handler, err_handler]
        )

    def get_logger(self, name):
        if not self._setup_done:
            self.setup()
        return logging.getLogger(name)

    @property
    def fileno_list(self):
        return [handler.stream.fileno() for handler in logging.getLogger().handlers]

# モジュールレベルでシングルトン取得関数を用意
def get_logger(name):
    manager = LoggerManager()
    return manager.get_logger(name)

def get_logger_manager():
    return LoggerManager()
from linux_daemon import LinuxDaemon
from _logging import get_logger_manager, get_logger
import sys

if __name__ == '__main__':
    logger_manager = get_logger_manager()
    logger_manager.setup()
    logger = get_logger(__name__)
    
    logger.info("Process started.")    
    
    daemon = LinuxDaemon()

    if len(sys.argv) != 2 or sys.argv[1] == '':
        message = f"Usage: {sys.argv[0]} start|stop"
        print(message)
        logger.warning(message)

        sys.exit(1)

    cmd = sys.argv[1].lower()

    try:
        if cmd == 'start':
            daemon.start()
        elif cmd == 'stop':
            daemon.stop()
        else:
            message = "Unknown command"
            print(message)
            logger.warning(message)
    except Exception as e:
        message = "An unexpected error has occurred."
        print(message)
        logger.error(f"{message}, {e}")


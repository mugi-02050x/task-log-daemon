#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)   # 1階層上がプロジェクトルート想定
ENV_DIR="$ROOT_DIR/venv"

DAEMON_NAME="task-log-daemon"
PIDFILE="/tmp/task-log-daemon.pid"
PYTHON_BIN="$ENV_DIR/bin/python"
DAEMON_SCRIPT="$ROOT_DIR/src/main.py"   # main.py のパス（ルート基準で指定）

activate_venv() {
    if [ ! -d "$ENV_DIR" ]; then
        echo "Virtual environment not found. Please run setup_env.sh first."
        exit 1
    fi
    # 今は特に処理なし。必要あればここに初期化コードを追加可能
}

start() {
    activate_venv

    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if kill -0 $PID > /dev/null 2>&1; then
            echo "$DAEMON_NAME is already running (PID: $PID)"
            exit 1
        else
            echo "Removing stale PID file"
            rm -f "$PIDFILE"
        fi
    fi

    echo "Starting $DAEMON_NAME..."
    "$PYTHON_BIN" "$DAEMON_SCRIPT" start &
    sleep 1
    if [ -f "$PIDFILE" ]; then
        echo "$DAEMON_NAME started successfully (PID: $(cat $PIDFILE))"
    else
        echo "Failed to start $DAEMON_NAME"
        exit 1
    fi
}

stop() {
    activate_venv
    echo "Stopping $DAEMON_NAME..."
    "$PYTHON_BIN" "$DAEMON_SCRIPT" stop &
    echo "$DAEMON_NAME stopped"
}

status() {
    activate_venv

    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if kill -0 $PID > /dev/null 2>&1; then
            echo "$DAEMON_NAME is running (PID: $PID)"
            exit 0
        else
            echo "Stale PID file found"
            exit 1
        fi
    else
        echo "$DAEMON_NAME is not running"
        exit 3
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    status)
        status
        ;;
    *)
        "$PYTHON_BIN" "$DAEMON_SCRIPT" "$1"
        ;;
esac


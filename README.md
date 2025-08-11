It records the start and end times of tasks.

## cmd
- start
    - scripts/task-log-daemon-control.sh start
- send
    - echo "hello daemon" | socat - UNIX-CONNECT:/tmp/task-log-daemon.sock
- end
    - scripts/task-log-daemon-control.sh stop

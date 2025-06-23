#!/bin/sh

# Ждем запуска Mosquitto
sleep 5

echo "[MQTT] Starting data publisher with PID $$" >&2

while true; do
    # Генерируем данные
    TEMP=$((20 + RANDOM % 10))
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    # Форматируем сообщение для логов
    LOG_MSG="[$TIMESTAMP] Published: temperature=$TEMP°C, status=online"
    echo "$LOG_MSG" >&2  # Выводим в stderr (попадет в docker logs)

    # Отправляем данные в MQTT
    mosquitto_pub -h 127.0.0.1 -t "camera/temperature" -m "$TEMP" -q 1 -i "camera_sensor" -r
    mosquitto_pub -h 127.0.0.1 -t "camera/status" -m "online" -q 1 -i "camera_sensor" -r

    sleep 5
done
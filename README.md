# iot-botnet

Запуск
docker-compose up -d

Начать сканирование и подбор учетных данных
curl http://localhost:8080/start_scan
curl http://localhost:8080/stop_scan
curl http://localhost:8080/list_bots

Загрузить и выполнить скрипт на ботах
curl http://localhost:8080/deploy_scripts
curl http://localhost:8080/execute_scripts

Посмотреть логи атакуемого сервера
docker exec -it victim_server tail -f /var/log/victim/access.loger tail -f /var/log/victim/access.log

Зайти в web-интерфейс ip-камеры через браузер
http://localhost:8081/

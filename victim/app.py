from flask import Flask, request, jsonify
import logging
import os
import time

app = Flask(__name__)

# Конфигурация
LOG_FILE = "/var/log/victim/access.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Настройка логов
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)


@app.route('/')
def home():
    client_ip = request.remote_addr
    logging.info(f"Access from {client_ip}")
    return "Welcome to Vulnerable IoT Device v1.0"


@app.route('/api/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        # Имитация уязвимости (SQL-инъекция)
        query = request.json.get('query', '')
        logging.warning(f"Possible SQLi attempt: {query}")
        return jsonify({"status": "processed"})

    return jsonify({"data": "sensitive_info_here"})


@app.route('/attack', methods=['POST'])
def attack():
    # Эндпоинт для теста DDoS от ботнета
    time.sleep(0.5)  # Имитация нагрузки
    return jsonify({"status": "under_attack"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
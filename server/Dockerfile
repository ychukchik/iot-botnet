FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    nmap \
    net-tools \
    sshpass \
    iputils-ping \
    telnet \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
COPY cnc_server.py .
COPY malicious_script.sh .

RUN pip install -r requirements.txt && \
    chmod 644 malicious_script.sh

EXPOSE 8080
CMD ["python3", "cnc_server.py"]

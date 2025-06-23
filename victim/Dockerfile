FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p /var/log/victim && \
    touch /var/log/victim/access.log && \
    chmod 666 /var/log/victim/access.log

EXPOSE 80
CMD ["python", "app.py"]

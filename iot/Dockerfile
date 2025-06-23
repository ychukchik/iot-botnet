FROM alpine:latest

RUN apk add --no-cache \
    lighttpd \
    openssh \
    mosquitto \
    mosquitto-clients \
    busybox-extras \
    tftp-hpa \
    curl \
    bash \
    jq \
    openssl \
    iputils \
    nmap \
    net-tools \
    shadow

# Создаем пользователя для lighttpd
RUN adduser -D -H -s /bin/false -G www-data www-data && \
    adduser www-data www-data

# Создаем начального пользователя admin
RUN adduser -D admin && \
    echo "admin:12345678" | chpasswd && \
    adduser admin wheel && \
    ssh-keygen -A

# Настройка SSH
RUN sed -i 's/#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    echo "AllowUsers admin" >> /etc/ssh/sshd_config

# Настройка Telnet
RUN echo "#!/bin/bash" > /start_telnet.sh && \
    echo "telnetd -F -l /bin/login" >> /start_telnet.sh && \
    chmod +x /start_telnet.sh

# Создаем структуру директорий
RUN mkdir -p /var/www/localhost/cgi-bin && \
    mkdir -p /etc/lighttpd && \
    mkdir -p /etc/mosquitto && \
    mkdir -p /var/log/lighttpd && \
    touch /var/log/lighttpd/error.log && \
    mkdir -p /var/www/localhost/htdocs && \
    touch /var/www/localhost/creds.json && \
    chown -R www-data:www-data /var/www/localhost && \
    chmod -R 755 /var/www/localhost

# Копируем файлы
COPY lighttpd.conf /etc/lighttpd/
COPY mosquitto.conf /etc/mosquitto/
COPY www/ /var/www/localhost/htdocs/
COPY scripts/ /var/www/localhost/cgi-bin/

# Настраиваем права
RUN chmod +x /var/www/localhost/cgi-bin/*.sh && \
    chmod +x /start_telnet.sh && \
    ln -s /var/www/localhost/cgi-bin/fake_data.sh /usr/local/bin/ && \
    chown -R www-data:www-data /var/www/localhost/cgi-bin

# Инициализация учетных данных
RUN echo '12345678' | openssl passwd -6 -stdin > /tmp/pass.hash && \
    echo "{\"login\":\"admin\",\"password\":\"$(cat /tmp/pass.hash)\",\"token\":\"\"}" > /var/www/localhost/creds.json && \
    chown www-data:www-data /var/www/localhost/creds.json && \
    chmod 644 /var/www/localhost/creds.json && \
    rm /tmp/pass.hash

EXPOSE 80 22 23 1883 69

CMD ["sh", "-c", "lighttpd -f /etc/lighttpd/lighttpd.conf & \
     /usr/sbin/sshd -D & \
     /start_telnet.sh & \
     /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf & \
     fake_data.sh & \
     tail -f /dev/null"]
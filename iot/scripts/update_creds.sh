#!/bin/bash

CREDS_FILE="/var/www/localhost/creds.json"
CHANGE_CREDS_HTML="/var/www/localhost/htdocs/change_creds.html"
OLD_LOGIN=$(jq -r '.login' "$CREDS_FILE")

if [ -n "$HTTP_COOKIE" ]; then
    TOKEN=$(echo "$HTTP_COOKIE" | grep -o 'token=[^;]*' | cut -d'=' -f2)
    STORED_TOKEN=$(jq -r '.token' "$CREDS_FILE")

    if [ "$TOKEN" != "$STORED_TOKEN" ] || [ -z "$TOKEN" ]; then
        echo "Content-type: text/html"
        echo "Location: /login"
        echo ""
        exit 0
    fi
else
    echo "Content-type: text/html"
    echo "Location: /login"
    echo ""
    exit 0
fi

if [ "$REQUEST_METHOD" = "POST" ]; then
    read -r POST_DATA
    NEW_LOGIN=$(echo "$POST_DATA" | awk -F'&' '{print $1}' | awk -F'=' '{print $2}')
    NEW_PASSWORD=$(echo "$POST_DATA" | awk -F'&' '{print $2}' | awk -F'=' '{print $2}')

    # Генерация хеша пароля
    HASHED_PASS=$(openssl passwd -6 "$NEW_PASSWORD")

    # Обновляем creds.json
    jq --arg login "$NEW_LOGIN" --arg password "$HASHED_PASS" \
       '.login = $login | .password = $password' \
       "$CREDS_FILE" > /tmp/creds.json && mv /tmp/creds.json "$CREDS_FILE"

    # Удаляем старого пользователя (если логин изменился)
    if [ "$OLD_LOGIN" != "$NEW_LOGIN" ] && id "$OLD_LOGIN" &>/dev/null; then
        deluser "$OLD_LOGIN"
        sed -i "/^$OLD_LOGIN:/d" /etc/shadow
    fi

    # Создаем/обновляем системного пользователя
    if ! id "$NEW_LOGIN" &>/dev/null; then
        adduser -D "$NEW_LOGIN"
        adduser "$NEW_LOGIN" wheel
    fi

    # Устанавливаем новый пароль
    echo "$NEW_LOGIN:$NEW_PASSWORD" | chpasswd

    # Чистим старые сессии SSH (перезапуск не требуется)
    pkill -u "$OLD_LOGIN" || true

    echo "Content-type: text/html"
    echo ""
    echo "<html><body><h1>Credentials Updated Successfully</h1><a href='/admin'>Back to Admin Panel</a></body></html>"
else
    echo "Content-type: text/html"
    echo ""
    cat "$CHANGE_CREDS_HTML"
fi
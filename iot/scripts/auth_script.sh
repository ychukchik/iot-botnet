#!/bin/bash

CREDS_FILE="/var/www/localhost/creds.json"
LOGIN_HTML="/var/www/localhost/htdocs/login.html"
ADMIN_HTML="/var/www/localhost/htdocs/admin.html"

check_password() {
    local input_pass=$1
    local stored_hash=$2
    local salt=$(echo "$stored_hash" | cut -d'$' -f3)
    local new_hash=$(openssl passwd -6 -salt "$salt" "$input_pass")
    [ "$new_hash" = "$stored_hash" ] && return 0 || return 1
}

if [ "$REQUEST_METHOD" = "POST" ]; then
    read -r POST_DATA
    LOGIN=$(echo "$POST_DATA" | awk -F'&' '{print $1}' | awk -F'=' '{print $2}')
    PASSWORD=$(echo "$POST_DATA" | awk -F'&' '{print $2}' | awk -F'=' '{print $2}')

    STORED_LOGIN=$(jq -r '.login' "$CREDS_FILE")
    STORED_HASH=$(jq -r '.password' "$CREDS_FILE")

    if [ "$LOGIN" = "$STORED_LOGIN" ] && check_password "$PASSWORD" "$STORED_HASH"; then
        TOKEN=$(date +%s | sha256sum | base64 | head -c 32)
        jq --arg token "$TOKEN" '.token = $token' "$CREDS_FILE" > /tmp/creds.json && mv /tmp/creds.json "$CREDS_FILE"

        echo "Set-Cookie: token=$TOKEN; Path=/"
        echo "Content-type: text/html"
        echo "Location: /admin"
        echo ""
    else
        echo "Content-type: text/html"
        echo ""
        echo "<html><body><h1>Login Failed</h1><a href='/login'>Try again</a></body></html>"
    fi
else
    if [ -n "$HTTP_COOKIE" ]; then
        TOKEN=$(echo "$HTTP_COOKIE" | grep -o 'token=[^;]*' | cut -d'=' -f2)
        STORED_TOKEN=$(jq -r '.token' "$CREDS_FILE")

        if [ "$TOKEN" = "$STORED_TOKEN" ] && [ -n "$TOKEN" ]; then
            echo "Content-type: text/html"
            echo ""
            cat "$ADMIN_HTML"
            exit 0
        fi
    fi

    echo "Content-type: text/html"
    echo ""
    cat "$LOGIN_HTML"
fi

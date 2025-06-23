#!/bin/bash

CREDS_FILE="/var/www/localhost/creds.json"

# Удаляем токен
jq '.token = ""' "$CREDS_FILE" > /tmp/creds.json && mv /tmp/creds.json "$CREDS_FILE"

# Удаляем куки и перенаправляем на главную
echo "Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/"
echo "Content-type: text/html"
echo "Location: /"
echo ""
#!/bin/bash
set -Eeuo pipefail

path="/opt/star_burger_dkr"

cd "$path"

source .env

docker compose down

git pull

docker compose up --build -d
systemctl reload nginx
curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token="${ROLLBAR_ACCESS_TOKEN:?ROLLBAR_ACCESS_TOKEN is not set}" \
  -F revision=$(git rev-parse HEAD) \
  -F status=succeeded \
  -F environment=production \
  -F local_username=$(whoami)
echo "Данные отправлены в Rollbar"
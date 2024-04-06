#!/bin/bash

apt-get update -y > /dev/null 2>&1
apt-get install zip -y > /dev/null 2>&1
curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | exec "$SHELL"

python init_db.py && \
source scripts/create_yc_func.sh && \
echo "0 * * * * /github_parser/scripts/trigger_yc_func > /dev/null 2>&1" > /etc/crontabs/root

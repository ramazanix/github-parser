#!/bin/bash

apt-get update -y > /dev/null 2>&1
apt-get install cron -y
apt-get install zip -y > /dev/null 2>&1
curl https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash -s -- -i /opt/yc -n

python init_db.py && \
source scripts/create_yc_func.sh && \
(crontab -l 2>/dev/null; echo "0 * * * * /github_parser/scripts/trigger_yc_func") | crontab -
exec "$@"

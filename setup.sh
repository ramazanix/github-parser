#!/bin/bash

python init_db.py && \
source scripts/create_yc_func.sh && \
echo "0 * * * * /github_parser/scripts/trigger_yc_func > /dev/null 2>&1" > /etc/crontabs/root

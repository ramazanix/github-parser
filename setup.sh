python3 init_db.py && \
source scripts/create_yc_func.sh && \
echo "0 * * * * /path/to/script >/dev/null 2>&1" > /etc/crontabs/root
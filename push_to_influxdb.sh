. ./setup.sh

python influxdb.py

which crontab &>/dev/null
if [ $? -eq 0 ]; then
    echo -e '\n==run "crontab -e" to edit cron jobs==\n'
    crontab -l
fi

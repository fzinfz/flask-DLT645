n=flask-dlt645

ls /dev/ttyUSB*
[ $? -ne 0 ] && echo 'USB not found!' && exit

docker stop $n 2>/dev/null; docker rm $n 2>/dev/null

# logic in __init__.py
read -p "Load lib/conf_prod? (y/n) " a
[ "$a" = "y" ] && METER_ENV=prod || METER_ENV=dev

read -p "Port: (Default: 5000) " p

s="docker run --name $n -d --restart unless-stopped \
    --net host \
    -e FLASK_DLT645_PORT=${p:-5000} \
    -v $PWD:/app \
    -e METER_ENV=$METER_ENV \
    --device=/dev/ttyUSB0:/dev/ttyUSB0 \
    fzinfz/tools:python3 \
    sh -c 'cd /app && ./start_web.sh' \
"

echo "$s" && eval "$s"

docker logs -f $n
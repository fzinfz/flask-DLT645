custom_config=/data/conf/flask-DLT645/*.py # to replace lib/conf.py , ignore if not existing
n=flask-dlt645 # container name

. ./setup.sh 

select_file $custom_config
custom_config=$selected_file

select_file /dev/ttyUSB*
dev_usb=$selected_file
[ ! -c $dev_usb ] && exit_err "$dev_usb not found!"

run "docker stop $n 2>/dev/null; docker rm $n 2>/dev/null"

q "Port: (Default: 5000) " p

q "Debug mode? ([n]/y) " m
[[ $m =~ [Yy] ]] && FLASK_ENV=development || FLASK_ENV=production
echo_debug "FLASK_ENV=$FLASK_ENV"

s="docker run --name $n -d --restart unless-stopped \
    --net host \
    -e FLASK_DLT645_PORT=${p:-5000} \
    -e FLASK_ENV=${FLASK_ENV} \
    --device=$dev_usb:/dev/ttyUSB0 \
    -v $PWD:/app \
"

[ -n "$custom_config" ] && echo_debug "Loaded: $custom_config" && s="$s -v $custom_config:/app/lib/conf.py "

s="$s fzinfz/tools:python3 bash -c 'cd /app && ./start_web.sh' "

run "$s"
run "docker logs -f $n"
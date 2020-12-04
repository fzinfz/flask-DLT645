if [ ! -f lib/forked/dlt645.py ]; then
    mkdir -p lib/forked
    wget https://raw.githubusercontent.com/glx-technologies/meter-dlt645/master/dlt645.py -P lib/forked
fi

if [ -f lib/conf_prod.py ]; then
       read -p 'Load lib/conf_prod.py? (y/n) ' a
	[ "$a" = "y" ] && export METER_ENV=prod || unset METER_ENV
else
	unset METER_ENV
fi
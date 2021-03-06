if [ ! -f ./lib/forked/dlt645.py ]; then
    mkdir -p lib/forked
    wget https://raw.githubusercontent.com/glx-technologies/meter-dlt645/master/dlt645.py -P lib/forked
fi

if [ ! -f ./lib/init.sh ]; then
    wget https://raw.githubusercontent.com/fzinfz/scripts/master/linux/init.sh -P lib
fi
. ./lib/init.sh
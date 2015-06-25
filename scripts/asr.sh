export PATH="$PATH:~/scripts"

clear

echo "***************** INITIALIZING ASR *****************"

sudo bash -c 'echo -1 > /sys/module/usbcore/parameters/autosuspend'

xterm -e "roscore" &

sleep 10s

xterm -e "roslaunch asr asr.launch" &

exit 0

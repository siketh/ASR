export PATH="$PATH:~/scripts"

clear

echo "SLAM TEST"

sudo bash -c 'echo -1 > /sys/module/usbcore/parameters/autosuspend'

xterm -hold -e "roscore" &

sleep 10s

xterm -hold -e "roslaunch asr asr.launch" &

exit 0

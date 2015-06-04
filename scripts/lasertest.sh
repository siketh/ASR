export PATH="$PATH:~/scripts"

clear

echo "KINECT LASER SCAN TEST"

sudo bash -c 'echo -1 > /sys/module/usbcore/parameters/autosuspend'

xterm -hold -e "roscore" &

sleep 10s

xterm -hold -e "roslaunch openni_launch openni.launch" &

sleep 10s

xterm -hold -e "rosrun depthimage_to_laserscan depthimage_to_laserscan image:=/camera/depth/image_raw" &

sleep 10s

xterm -hold -e "rosrun rviz rviz"

exit 0

export PATH="$PATH:~/scripts"

cd

clear

echo "INITIALIZING ROS ENVIRONMENT"

echo "Performing catkin_make and source"

cd ROS/catkin_ws

catkin_make

source /home/trevor/ROS/catkin_ws/devel/setup.bash

echo "Turning off USB autosuspend"

sudo bash -c 'echo -1 > /sys/module/usbcore/parameters/autosuspend'

exit 0

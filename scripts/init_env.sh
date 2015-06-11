cd

clear

echo "INITIALIZING ROS ENVIRONMENT"

echo "COMPILING"

cd ROS/catkin_ws

catkin_make

echo "SOURCING"

source devel/setup.bash
source devel/setup.bash
source devel/setup.bash

echo "TURNING OFF USB AUTOSUSPEND"

sudo bash -c 'echo -1 > /sys/module/usbcore/parameters/autosuspend'

exit 0

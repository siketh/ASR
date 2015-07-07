export PATH="$PATH:~/scripts"

cd

clear

echo "TESTING"

source /home/trevor/ROS/catkin_ws/devel/setup.bash

xterm -hold -e "roscore" &

sleep 10s

xterm -hold -e "rosrun asr talker.py" &

sleep 10s

xterm -hold -e "rosrun asr listener.py" &

exit 0

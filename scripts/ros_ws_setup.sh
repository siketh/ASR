mkdir -p catkin_ws/src
cd catkin_ws/src
catkin_init_workspace
cd ..
catkin_make
source devel/setup.bash
echo $ROS_PACKAGE_PATH

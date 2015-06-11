#!/usr/bin/env python

import os

def asr():
    os.system
    os.system("cd")
    os.system("cd ROS/catkin_ws")
    os.system("catkin_make")
    os.system("source devel/setup.bash")
    os.system("xterm -hold -e roscore & roslaunch asr.launch")

if __name__ == '__main__':
    asr()



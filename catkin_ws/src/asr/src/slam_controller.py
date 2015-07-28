#!/usr/bin/env python

import rospy, os, signal, subprocess
from std_msgs.msg import String
from std_msgs.msg import Bool


def state_callback(data):
    if data.data == "Shutdown":
        rospy.signal_shutdown(shutdown_hook())


def mapping_callback(data):
    global mapping
    mapping = data.data
 


def shutdown_hook():
    print("\n...SYSTEM SHUTTING DOWN...")

    if slam_process is not False:
        os.killpg(slam_process.pid, signal.SIGTERM)


def slam_controller():
    global mapping, slam_process
    slam_cmd = "roslaunch asr asr_mapping.launch"
    launched = False
    mapping = False
    slam_process = False

    rospy.init_node('slam_controller', anonymous=False)

    rospy.Subscriber("current_state", String, state_callback, queue_size=10)
    rospy.Subscriber("mapping_active", Bool, mapping_callback, queue_size=10)

    rate = rospy.Rate(10) # 10hz

    print("********** [SLAM CONTROLLER] **********")

    while not rospy.is_shutdown():
        if mapping == True and launched == False:
            print("\nINITIATING SLAM")
            slam_process = subprocess.Popen(slam_cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            launched = True

        if mapping == False and launched == True:
            print("\nQUITTING SLAM")
            os.killpg(slam_process.pid, signal.SIGTERM)
            slam_process = False
            launched = False

        if mapping == True:
            print("Performing SLAM...")

        rate.sleep()


if __name__ == '__main__':
    try:
        slam_controller()
    except rospy.ROSInterruptException:
        pass



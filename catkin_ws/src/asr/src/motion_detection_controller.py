#!/usr/bin/env python

import cv2, rospy, roslib, os, signal, subprocess
roslib.load_manifest('asr')
import sys
import smtplib
from std_msgs.msg import String
from std_msgs.msg import Bool


def state_callback(data):
    if data.data == "Shutdown":
        rospy.signal_shutdown(shutdown_hook())


def md_callback(data):
    global motion_detection
    motion_detection = data.data


def alerts_callback(data):
    global alert
    alert = data.data


def shutdown_hook():
    print("\n...SYSTEM SHUTTING DOWN...")

    if md_process is not False:
        os.killpg(md_process.pid, signal.SIGTERM)


def motion_detection_controller():
    global motion_detection, md_process, alert

    md_launch = "roslaunch asr asr_motion_detection.launch"
    md_process = False
    launched = False
    motion_detection = False
    alert = None
    previous = alert

    rospy.init_node('motion_detection_controller', anonymous=False)

    state_sub = rospy.Subscriber("current_state", String, state_callback, queue_size=10)
    md_sub = rospy.Subscriber("md_active", Bool, md_callback, queue_size=10)
    alert_sub = rospy.Subscriber("user_alerts", String, alerts_callback)

    rate = rospy.Rate(10)  # 10hz

    print("********** [MOTION DETECTION CONTROLLER] **********")

    while not rospy.is_shutdown():
        if motion_detection == True and launched == False:
            print("\nINITIATING MOTION DETECTION\n")
            md_process = subprocess.Popen(md_launch, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            launched = True
            print("Performing Motion Detection...")
        if motion_detection == False and launched == True:
            print("\nQUITTING MOTION DETECTION")
            os.killpg(md_process.pid, signal.SIGTERM)
            md_process = False
            launched = False
        if motion_detection == True and previous != alert:
            print("\nPerforming Motion Detection...")
            print(alert)
            previous = alert
        rate.sleep()


if __name__ == '__main__':
    try:
        motion_detection_controller()
    except rospy.ROSInterruptException:
        pass



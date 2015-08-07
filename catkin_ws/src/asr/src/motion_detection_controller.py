#!/usr/bin/env python

import cv2, rospy, roslib, os, signal, subprocess
roslib.load_manifest('asr')
from std_msgs.msg import String, Bool

motion_detection = False
md_process = False
alert = None

def md_callback(data):
    global motion_detection
    motion_detection = data.data


def alerts_callback(data):
    global alert
    alert = data.data


def state_callback(data):
    if data.data == "Shutdown":
        rospy.signal_shutdown(shutdown_hook())


def shutdown_hook():
    print("\n...MOTION DETECTION CONTROLLER SHUTTING DOWN...")

    if md_process is not False:
        os.killpg(md_process.pid, signal.SIGTERM)


def motion_detection_controller():
    global motion_detection, md_process, alert

    #md_launch = "roslaunch asr asr_motion_detection.launch"
    launched = False
    previous = alert

    rospy.init_node('motion_detection_controller', anonymous=False)

    rospy.Subscriber("current_state", String, state_callback, queue_size=10)
    rospy.Subscriber("md_active", Bool, md_callback, queue_size=10)
    rospy.Subscriber("user_alerts", String, alerts_callback, queue_size=10)

    rate = rospy.Rate(10)  # 10hz

    print("********** [MOTION DETECTION CONTROLLER] **********")

    while not rospy.is_shutdown():
        if motion_detection and not launched:
            print("\nINITIATING MOTION DETECTION\n")
            #md_process = subprocess.Popen(md_launch, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            launched = True
        elif not motion_detection and launched:
            print("\nQUITTING MOTION DETECTION")
            #os.killpg(md_process.pid, signal.SIGTERM)
            #md_process = False
            launched = False
        elif motion_detection and previous != alert:
            print("\nALERT!")
            print(alert)
            previous = alert
        else:
            print("\nMOTION DETECTION INACTIVE")

        rate.sleep()

    rospy.spin()


if __name__ == '__main__':
    try:
        motion_detection_controller()
    except rospy.ROSInterruptException:
        pass



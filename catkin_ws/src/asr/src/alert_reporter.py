#!/usr/bin/env python

import cv2, rospy, roslib, tf
roslib.load_manifest('asr')
import sys
from std_msgs.msg import String
import yagmail
import time
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def alerts_callback(data):
    global alert
    alert = data.data


def motion_callback(data):
    global motion_img, img_index, sender, pwd, receiver, yag

    now = time.strftime("%c")

    try:
        bridge = CvBridge()
        motion_img = bridge.imgmsg_to_cv2(data, "bgr8")

        if motion_img is not None:
            img = motion_img.copy()
            dir = "/home/trevor/ROS/catkin_ws/src/asr/pictures/motion_" + str(img_index) + ".png"
            cv2.imwrite(dir, img)
            #cv2.imshow("Motion Image", img)
            #cv2.waitKey(3)
            yag.send(receiver, subject="MOTION DETECTED: " + str(now), contents=[dir])

    except CvBridgeError, e:
        print e

    img_index += 1

    if img_index == 10:
        img_index = 0


def alert_reporter():
    global alert, img_index, now, sender, pwd, receiver, yag

    alert = None
    img_index = 0
    sender = 'asr.one.zero@gmail.com'
    pwd = 'hal.9000'
    receiver = 'asr.one.zero@gmail.com'
    yag = yagmail.SMTP(sender)

    rospy.init_node('alert_reporter', anonymous=False)

    alert_sub = rospy.Subscriber("/user_alerts", String, alerts_callback, queue_size=10)
    motion_sub = rospy.Subscriber("/motion_image", Image, motion_callback, queue_size=10)

    rate = rospy.Rate(10)  # 10hz

    while alert is None:
        print "Waiting for connection to alerts..."

    while not rospy.is_shutdown():
        if "MOTION DETECTED" in alert:
            print alert

    rate.sleep()

if __name__ == '__main__':
    try:
        alert_reporter()
    except rospy.ROSInterruptException:
        pass




#!/usr/bin/env python

import cv2, rospy, roslib
import yagmail, time, numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String, Bool
from cv_bridge import CvBridge, CvBridgeError
roslib.load_manifest('asr')

state = None
alert = None
motion_detection = False
capture = False
submit_alerts = False
sender = ""
receiver = sender
connection = None
motion_img_index = 0
capture_img_index = 0
motion_images = []
captured_images = []
bridge = CvBridge()

def state_callback(data):
    global state

    state = data.data
    if state == "Shutdown":
        rospy.signal_shutdown(shutdown_hook())


def shutdown_hook():
    print("\n...ALERT REPORTER SHUTTING DOWN...")


def alerts_callback(data):
    global alert
    alert = data.data


def md_callback(data):
    global motion_detection
    motion_detection = data.data


def capture_command_callback(data):
    global capture
    capture = data.data


def submit_callback(data):
    global submit_alerts
    submit_alerts = data.data


def motion_callback(data):
    global motion_img_index, motion_images, bridge, sender, receiver, connection

    now = time.strftime("%c")
    try:
        motion_img = bridge.imgmsg_to_cv2(data, "bgr8")

        if motion_img is not None:
            img = motion_img.copy()
            dir = "/home/trevor/ROS/catkin_ws/src/asr/pictures/motion_" + str(motion_img_index) + ".png"
            motion_images.append(dir)
            cv2.imwrite(dir, img)

        if (motion_img_index+1) % 5.0 == 0.0:
            img4 = motion_images[motion_img_index]
            img3 = motion_images[motion_img_index-1]
            img2 = motion_images[motion_img_index-2]
            img1 = motion_images[motion_img_index-3]
            img0 = motion_images[motion_img_index-4]
            if connection is not None:
                connection.send(receiver, subject="MOTION DETECTED: " + str(now), contents=[img0, img1, img2, img3, img4])
    except CvBridgeError, e:
        print e

    motion_img_index += 1
    if motion_img_index == 10:
        motion_img_index = 0


def capture_callback(data):
    global capture_img_index, capture, captured_images, bridge, sender, receiver, connection

    if capture is True:
        now = time.strftime("%c")

        try:
            capture_img = bridge.imgmsg_to_cv2(data, "bgr8")

            if capture_img is not None:
                img = capture_img.copy()
                dir = "/home/trevor/ROS/catkin_ws/src/asr/pictures/capture_" + str(capture_img_index) + ".png"
                captured_images.append(dir)
                cv2.imwrite(dir, img)

                img0 = captured_images[capture_img_index]

                if connection is not None:
                    connection.send(receiver, subject="IMAGE CAPTURED: " + str(now), contents=[img0])

        except CvBridgeError, e:
            print e

        capture_img_index += 1
        if capture_img_index == 5:
            capture_img_index = 0


def alert_reporter():
    global alert, capture, capture_img_index, sender, receiver, connection

    md_initialized = False
    cap_initialized = False

    rospy.init_node('alert_reporter', anonymous=False)

    rospy.Subscriber("current_state", String, state_callback, queue_size=10)
    rospy.Subscriber("user_alerts", String, alerts_callback, queue_size=10)
    rospy.Subscriber("md_active", Bool, md_callback, queue_size=10)
    rospy.Subscriber("cam_capture", Bool, capture_command_callback, queue_size=10)
    rospy.Subscriber("submit_alerts", Bool, submit_callback, queue_size=10)

    rate = rospy.Rate(10)  # 10hz

    print("********** [ALERT REPORTER] **********")

    while not rospy.is_shutdown():
        if not submit_alerts:
            sender = ""
            receiver = sender
            connection = None
        elif submit_alerts:
            sender = "asr.one.zero@gmail.com"
            receiver = sender
            connection = yagmail.SMTP(sender)

        if motion_detection is True:
            if alert is None and not md_initialized:
                print "Waiting for connection to alerts..."
            elif alert is not None and not md_initialized:
                print "Connected to alerts..."
                motion_sub = rospy.Subscriber("motion_image", Image, motion_callback, queue_size=10)
                md_initialized = True
            if md_initialized:
                print "Reporting alerts..."

            if capture is None and cap_initialized is False:
                print "Waiting for capture listener to connect..."
            if capture is not None and cap_initialized is False:
                print "Capture listener connected..."
                capture_sub = rospy.Subscriber("/camera/rgb/image_color", Image, capture_callback, queue_size=10)
                cap_initialized = True
            if cap_initialized:
                if capture is True:
                    print "Capturing images from camera..."
                if capture is False:
                    print "Listening for 'capture' command..."
        elif motion_detection is False and md_initialized:
            print "Disconnecting from alerts..."
            motion_sub.unregister()
            md_initialized = False
            alert = None
            print "Disconnected from alerts..."
        elif motion_detection is False and cap_initialized:
            print "Disconnecting capture listener..."
            capture_sub.unregister()
            cap_initialized = False
            capture = None
            print "Capture listener disconnected..."
        else:
            print "\nALERT REPORTER INACTIVE"

        rate.sleep()

    rospy.spin()

if __name__ == '__main__':
    try:
        alert_reporter()
    except rospy.ROSInterruptException:
        pass




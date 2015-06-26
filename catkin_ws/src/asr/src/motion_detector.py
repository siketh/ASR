#!/usr/bin/env python

import cv2, rospy, roslib, tf
roslib.load_manifest('asr')
import sys
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


# motion tracking function which detects largest contour in thresholded/blurred image and draws a bounding target
# around it
def track_motion(t_b_image, bgr_img):

    # find contours in the image
    image, contours, hierarchy = cv2.findContours(t_b_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # if countours exist, there there is motion in the image
    if len(contours) > 0:

        # the largest contour is the best candidate for the moving object, this is the last item in the
        # contour vector
        largest_con = contours[-1]

        # set parameters for the bounding circle
        (x, y), radius = cv2.minEnclosingCircle(largest_con)
        center = (int(x), int(y))
        text_center = (int(x-125), int(y+100))
        radius = int(radius)

        # draw crosshair on image with text indicating the centroid of motion
        bgr_img = cv2.circle(bgr_img, center, 50, (0, 255, 0), 2)
        bgr_img = cv2.line(bgr_img, center, (int(x), int(y-75)), (0, 255, 0), 2)
        bgr_img = cv2.line(bgr_img, center, (int(x), int(y+75)), (0, 255, 0), 2)
        bgr_img = cv2.line(bgr_img, center, (int(x-75), int(y)), (0, 255, 0), 2)
        bgr_img = cv2.line(bgr_img, center, (int(x+75), int(y)), (0, 255, 0), 2)
        bgr_img = cv2.putText(bgr_img, "MOTION DETECTED: " + str(center), text_center, 1, 1, (0, 255, 0), 2)

    # return the image
    return bgr_img


# perform differential imaging
def get_diff_img(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def callback(data):
    global camera_img, image_sub

    try:
        bridge = CvBridge()
        camera_img = bridge.imgmsg_to_cv2(data, "bgr8")
        image_sub.unregister()
    except CvBridgeError, e:
        print e


def motion_detector():
    global camera_img, image_sub

    camera_img = "EMPTY"
    threshold = 30
    blur = (10, 10)

    rospy.init_node('motion_detector', anonymous=False)

    image_sub = rospy.Subscriber("camera/rgb/image_color", Image, callback, queue_size=10)
    image_pub = rospy.Publisher("/motion_image", Image, queue_size=10)

    rate = rospy.Rate(120) # 120hz

    while camera_img is "EMPTY":
        print "Waiting for camera frames..."

    # grab 3 identical images to initialize
    t_minus = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)
    t = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)
    t_plus = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)

    while not rospy.is_shutdown():

        # get differential image
        diff_img = get_diff_img(t_minus, t, t_plus)

        # perform thresholding and blurring
        retrieved, thresh_img = cv2.threshold(diff_img, threshold, 255, cv2.THRESH_BINARY)
        blur_img = cv2.blur(thresh_img, blur)

        # if thresholding failed something went wrong, warn and exit
        if not retrieved:
            print "Unable to perform thresholding on image"
            break

        # perform thresholding again on blurred image
        status, blur_thresh_img = cv2.threshold(blur_img, threshold, 255, cv2.THRESH_BINARY)

        # create motion image
        motion_img = track_motion(blur_thresh_img, camera_img)

        # show/publish motion image
        try:
            bridge = CvBridge()
            image_pub.publish(bridge.cv2_to_imgmsg(motion_img, "bgr8"))
        except CvBridgeError, e:
            print e

        #cv2.imshow("MOTION TRACKING", motion_img)
        #cv2.waitKey(3)

        # DEBUG
        #cv2.imshow("BGR IMAGE", img)
        #cv2.imshow("DIFF IMAGE", diff_img)
        #cv2.imshow("THRESH IMAGE", thresh_img)
        #cv2.imshow("BLUR IMAGE", blur_img)
        #cv2.imshow("BLUR + THRESH IMAGE", blur_thresh_img)

        # retrieve a bgr image from the kinect
        image_sub = rospy.Subscriber("camera/rgb/image_color", Image, callback, queue_size=10)

        # increment the images
        t_minus = t
        t = t_plus
        t_plus = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)

    rate.sleep()

if __name__ == '__main__':
    try:
        motion_detector()
    except rospy.ROSInterruptException:
        pass




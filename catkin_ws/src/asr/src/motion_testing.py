import cv2


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
        #y = y + 50
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


if __name__== "__main__":
    THRESHOLD = 30
    BLUR = (10,10)

    # TESTING: EMAIL SERVER


    # set up kinect camera
    capture = cv2.VideoCapture(cv2.CAP_OPENNI)
    capture.set(cv2.CAP_OPENNI_IMAGE_GENERATOR_OUTPUT_MODE, cv2.CAP_OPENNI_VGA_30HZ )

    # verify registration
    print capture.get(cv2.CAP_PROP_OPENNI_REGISTRATION)

    # if frames can't be grabbed, warn and exit
    if not capture.grab():
        print "Unable to grab frames from camera"

    # else proceed with motion detection
    else:
        # retrieve a bgr image from the kinect
        retrieved, img = capture.retrieve(0, cv2.CAP_OPENNI_BGR_IMAGE)

        # if image wasn't retrieved, warn and exit
        if not retrieved:
            print "Unable to retrieve BGR image from device"

        # else proceed with motion detection
        else:
            # grab 3 identical images to initialize
            t_minus = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            t = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            t_plus = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # TO DO; Integrate with ROS, create flag that can be set from state manager
            while True:

                # get differential image
                diff_img = get_diff_img(t_minus, t, t_plus)

                # perform thresholding and blurring
                retrieved, thresh_img = cv2.threshold(diff_img, THRESHOLD, 255, cv2.THRESH_BINARY)
                blur_img = cv2.blur(thresh_img, BLUR)

                # if thresholding failed something went wrong, warn and exit
                if not retrieved:
                    print "Unable to perform thresholding on image"
                    break

                # perform thresholding again on blurred image
                status, blur_thresh_img = cv2.threshold(blur_img, THRESHOLD, 255, cv2.THRESH_BINARY)

                # TO DO: Integrate with ROS, view in RVIZ instead
                # track and show motion
                motion_img = track_motion(blur_thresh_img, img)
                cv2.imshow("MOTION TRACKING", motion_img)

                # DEBUG
                #cv2.imshow("BGR IMAGE", img)
                #cv2.imshow("DIFF IMAGE", diff_img)
                #cv2.imshow("THRESH IMAGE", thresh_img)
                #cv2.imshow("BLUR IMAGE", blur_img)
                #cv2.imshow("BLUR + THRESH IMAGE", blur_thresh_img)

                # if frames can't be grabbed, warn and exit
                if not capture.grab():
                    print "Unable to grab frames from camera"
                    break

                # retrieve a bgr image from the kinect
                retrieved, img = capture.retrieve(0, cv2.CAP_OPENNI_BGR_IMAGE)

                # if image wasn't retrieved, warn and exit
                if not retrieved:
                    print "Unable to retrieve BGR image from device"
                    break

                # increment the images
                t_minus = t
                t = t_plus
                t_plus = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # if exit key is pressed, destroy windows and release video feed
                key = cv2.waitKey(10)
                if key == 27:
                    cv2.destroyAllWindows()
                    cv2.VideoCapture.release()
                    break

    print "EXITING MOTION DETECTION"



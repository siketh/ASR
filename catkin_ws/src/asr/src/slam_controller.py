#!/usr/bin/env python

import rospy
from std_msgs.msg import String


mapping = "False"


def callback(data):
    global mapping

    mapping = data.data
    rospy.loginfo("Mapping: %s", mapping)


def slam_controller():
    global mapping

    rospy.init_node('slam_controller', anonymous=False)

    mapping_sub = rospy.Subscriber("mapping_active", String, callback, queue_size=10)

    rate = rospy.Rate(10) # 10hz

    rospy.loginfo("SLAM NODE INITIATED\nMapping: %s", mapping)

    while not rospy.is_shutdown():
        if mapping == "True":
            rospy.loginfo("PERFORMING SLAM")

            if mapping == "False":
                rospy.loginfo("EXITING SLAM")

            rate.sleep()

    rate.sleep()


if __name__ == '__main__':
    try:
        slam_controller()
    except rospy.ROSInterruptException:
        pass



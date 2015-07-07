#!/usr/bin/env python

import rospy, os
from std_msgs.msg import String

mapping = "False"
navigation = "False"
autonomous = "False"
manual = "False"
motion_detection = "False"
command = "Standby"
sys_comm = ""


def command_parser(cmd):
    global mapping, navigation, autonomous, manual, motion_detection, sys_comm, command

    if cmd == "map -m":
        mapping = "True"
        navigation = "True"
        motion_detection = "False"
        autonomous = "False"
        manual = "True"
        return "Manual Mapping"

    if cmd == "map -a":
        mapping = "True"
        navigation = "True"
        motion_detection = "False"
        autonomous = "True"
        manual = "False"
        return "Autonomous Mapping"

    if cmd == "map -s":
        print("\nSAVING MAP...")
        os.system("rosrun map_server map_saver -f /home/trevor/ROS/catkin_ws/src/asr/maps/asr_map && echo '\n'")
        return command

    if cmd == "map -r":
        print("\nRESETTING MAP...")
        sys_comm = "reset"
        return command

    if cmd == "patrol -m":
        mapping = "False"
        navigation = "True"
        motion_detection = "True"
        autonomous = "False"
        manual = "True"
        return "Manual Patrol"

    if cmd == "patrol -a":
        mapping = "False"
        navigation = "True"
        motion_detection = "True"
        autonomous = "False"
        manual = "True"
        return "Autonomous Patrol"

    if cmd == "standby":
        mapping = "False"
        navigation = "False"
        motion_detection = "False"
        autonomous = "False"
        manual = "False"
        return "Standby"

    if cmd == "shutdown":
        mapping = "False"
        navigation = "False"
        motion_detection = "False"
        autonomous = "False"
        manual = "False"
        return "Shutdown"

    else:
        print("\nInvalid command, valid commands are:\n\tmap -m\n\tmap -a\n\tmap -s\n\tmap -r\n\tpatrol -m\n\tpatrol -a\n\tstandby\n\tshutdown")
        return command


def print_state():
    global mapping, motion_detection, autonomous, manual, command

    print("\nCurrent State:          " + command)
    print("    Autonomous:         " + autonomous)
    print("    Manual:             " + manual)
    print("    Mapping:            " + mapping)
    print("    Navigation:         " + navigation)
    print("    Motion Detection:   " + motion_detection)


def shutdown_hook():
    print("\n...SYSTEM SHUTTING DOWN...")


def state_manager():
    global mapping, navigation, autonomous, manual, command, sys_comm

    rospy.init_node('state_manager', anonymous=False)

    state_pub = rospy.Publisher('current_state', String, queue_size=10)
    mapping_pub = rospy.Publisher('mapping_active', String, queue_size=10)
    nav_pub = rospy.Publisher('nav_active', String, queue_size=10)
    md_pub = rospy.Publisher('md_active', String, queue_size=10)
    autonomous_pub = rospy.Publisher('autonomous_active', String, queue_size=10)
    manual_pub = rospy.Publisher('manual_active', String, queue_size=10)
    sys_pub = rospy.Publisher('syscommand', String, queue_size=10)

    rate = rospy.Rate(10)  # 10hz

    print("*********** [STATE MANAGER] ***********")

    print_state()

    while not rospy.is_shutdown():
        command = command_parser(raw_input("\nasr$: "))

        print_state()

        state_pub.publish(command)
        mapping_pub.publish(mapping)
        nav_pub.publish(navigation)
        md_pub.publish(motion_detection)
        autonomous_pub.publish(autonomous)
        manual_pub.publish(manual)
        sys_pub.publish(sys_comm)

        if command == "Shutdown":
            rospy.signal_shutdown(shutdown_hook())

        rate.sleep()


if __name__ == '__main__':
    try:
        state_manager()
    except rospy.ROSInterruptException:
        pass

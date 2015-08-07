#!/usr/bin/env python

import rospy, os
from std_msgs.msg import String
from std_msgs.msg import Bool

mapping = False
navigation = False
autonomous = False
manual = False
motion_detection = False
capture = False
submit = False
command = "Standby"
sys_comm = ""
timer = 0.0


def command_parser(cmd):
    global mapping, navigation, autonomous, manual, motion_detection, sys_comm, capture, timer, submit

    last_cmd = command

    if cmd == "map -m" and last_cmd == "Standby":
        mapping = True
        navigation = True
        motion_detection = False
        autonomous = False
        manual = True
        return "Manual Mapping"

    if cmd == "map -a" and last_cmd == "Standby":
        mapping = True
        navigation = True
        motion_detection = False
        autonomous = True
        manual = False
        return "Autonomous Mapping"

    if cmd == "map -s":
        if mapping is True:
            print("\nSAVING MAP...")
            os.system("rosrun map_server map_saver -f /home/trevor/ROS/catkin_ws/src/asr/maps/asr_map && echo '\n'")
        else:
            print("\nERROR: MAP CAN ONLY BE SAVED WHILE THE MAPPING STATE IS ACTIVE")
        return last_cmd

    if cmd == "map -r":
        if mapping is True:
            print("\nRESETTING MAP...")
            sys_comm = "reset"
        else:
            print("\nERROR: MAP CAN ONLY BE RESET WHILE THE MAPPING STATE IS ACTIVE")
        return last_cmd

    if cmd == "capture":
        if motion_detection is True:
            print("\nCAPTURING IMAGE FROM CAMERA...")
            capture = True
            timer = rospy.get_time()
        else:
            print("\nERROR: IMAGES CAN ONLY BE MANUALLY CAPTURED WHILE THE PATROL STATE IS ACTIVE")
            capture = False
        return last_cmd

    if cmd == "submit_alerts -t":
        submit = True
        print "\nALERTS WILL BE EMAILED AND SAVED LOCALLY"

    if cmd == "submit_alerts -f":
        print "\nALERTS WILL NOT BE EMAILED BUT THEY WILL BE SAVED LOCALLY"
        submit = False

    if cmd == "patrol -m" and last_cmd == "Standby":
        mapping = False
        navigation = True
        motion_detection = True
        autonomous = False
        manual = True
        return "Manual Patrol"

    if cmd == "patrol -a" and last_cmd == "Standby":
        mapping = False
        navigation = True
        motion_detection = True
        autonomous = True
        manual = False
        return "Autonomous Patrol"

    if cmd == "standby":
        mapping = False
        navigation = False
        motion_detection = False
        autonomous = False
        manual = False
        return "Standby"

    if cmd == "shutdown":
        mapping = False
        navigation = False
        motion_detection = False
        autonomous = False
        manual = False
        return "Shutdown"

    if cmd == "help":
        print("\n**************************** HELP ****************************\n")
        print_usage()
        return last_cmd
    else:
        print("\n************************ USAGE ERROR *************************\n")
        print_usage()
        return last_cmd


def print_state():
    global mapping, motion_detection, autonomous, manual, command

    print("\nCurrent State:          " + str(command))
    print("    Autonomous:         " + str(autonomous))
    print("    Manual:             " + str(manual))
    print("    Mapping:            " + str(mapping))
    print("    Navigation:         " + str(navigation))
    print("    Motion Detection:   " + str(motion_detection))


def print_usage():
    print("USAGE:")
    print("1) User must execute 'standby' command before switching states")
    print("2) User must enter only valid commands")
    print("   Valid commands are:\n\tmap -m\n\tmap -a\n\tmap -s\n\tmap -r\n\tpatrol -m\n\tpatrol -a"
          "\n\tsubmit_alerts -t\n\tsubmit_alerts -f\n\tstandby\n\tshutdown\n\thelp")
    print("\n****************************************************************")


def shutdown_hook():
    print("\n...SYSTEM SHUTTING DOWN...")


def state_manager():
    global mapping, navigation, autonomous, manual, command, sys_comm, capture, timer, submit

    rospy.init_node('state_manager', anonymous=False)

    state_pub = rospy.Publisher('current_state', String, queue_size=10)
    mapping_pub = rospy.Publisher('mapping_active', Bool, queue_size=10)
    nav_pub = rospy.Publisher('nav_active', Bool, queue_size=10)
    md_pub = rospy.Publisher('md_active', Bool, queue_size=10)
    autonomous_pub = rospy.Publisher('autonomous_active', Bool, queue_size=10)
    manual_pub = rospy.Publisher('manual_active', Bool, queue_size=10)
    sys_pub = rospy.Publisher('syscommand', String, queue_size=10)
    capture_pub = rospy.Publisher('cam_capture', Bool, queue_size=10)
    submit_pub = rospy.Publisher('submit_alerts', Bool, queue_size=10)

    rate = rospy.Rate(10)  # 10hz

    print("************************** ASR ONLINE **************************\n")
    print_usage()

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
        capture_pub.publish(capture)
        submit_pub.publish(submit)

        if capture is True:
            time_since_capture = abs(rospy.get_time() - timer)
            print "\nImages being captured, please wait..."

            while not time_since_capture >= 3:
                time_since_capture = abs(rospy.get_time() - timer)

            print "\nImage capture complete!"
            capture = False
            capture_pub.publish(capture)
            timer = 0.0

        if command == "Shutdown":
            rospy.signal_shutdown(shutdown_hook())

        rate.sleep()

if __name__ == '__main__':
    try:
        state_manager()
    except rospy.ROSInterruptException:
        pass

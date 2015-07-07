#!/bin/sh -x

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

cd "/home/trevor/ROS/catkin_ws/src/navigation/base_local_planner"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
/usr/bin/env \
    PYTHONPATH="/home/trevor/ROS/catkin_ws/install/lib/python2.7/dist-packages:/home/trevor/ROS/catkin_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/trevor/ROS/catkin_ws/build" \
    "/usr/bin/python" \
    "/home/trevor/ROS/catkin_ws/src/navigation/base_local_planner/setup.py" \
    build --build-base "/home/trevor/ROS/catkin_ws/build/navigation/base_local_planner" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/trevor/ROS/catkin_ws/install" --install-scripts="/home/trevor/ROS/catkin_ws/install/bin"

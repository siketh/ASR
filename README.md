########################################################################################

This is a Senior Design project by students at the University of Central Florida 
completed in August of 2015. Below is a summary of our project.

########################################################################################

SUMMARY

The Autonomous Sentry Robot is an automated home surveillance system with mapping and 
motion detection capabilities, powered by ROS and OpenCV. The ASR utilizes a Kinect 
for it's depth sensor and webcam, two ultra sonic sensors and four tactile sensors 
for it's reactive navigation system, and a laptop which acts as a server. The 
repository is available here.

FEATURES

Motion Detection:
The ASR has a robust motion detection algorithm powered by OpenCV. As the ASR operates 
autonomously, it will periodically stop and orient itself towards the greatest distance 
it can detect. It will then detect motion for a specified time interval.

Alert Reporting:
If the ASR detects motion, or the user captures an image while operating the ASR manually, 
the image will be saved locally and sent to the user's GMail account. Images are sent 
with a time stamp and edited with a target over the area that motion was detected.

Mapping and Localization:
The ASR has the ability to map and localize itself within its surroundings as it operates 
manually or autonomously. We utilize a SLAM algorithm called HectorSLAM developed by 
Stefan Kohlbrecher and Johannes Meyer.

Autonomous Navigation:
The ASR's autonomous navigation algorithm is powered by a reactive system of ultrasonic 
sensors and tactile sensors. The ASR will wander until certain range thresholds are crossed 
and dynamically determine a new bearing or orientation.

Manual Navigation:
The ASR uses a simple control scheme and user interface for manual navigation. While the 
user navigates, they can see from the robot's perspective via its webcam video stream.

TEAM:

Brian Dodge - Electrical Engineer - bgdodge@gmail.com

Nick Musco - Electrical Engineer - nicholas.musco@gmail.com

Trevor Roman - Computer Engineer - troman360@gmail.com

SPONSORS:

Boeing


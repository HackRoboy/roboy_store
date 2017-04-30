#!/usr/bin/env python

import rospy
import json
import subprocess
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'Installing %s...', data.data)
    
    with open('/home/dennj/catkin_ws/src/roboy_store/app_list.json') as data_file:    
        apps = json.load(data_file)

    pkg = data.data
    cmd = "git clone '"+apps[pkg]+"' '/home/dennj/catkin_ws/src/"+pkg+"'"
    print cmd
    output = subprocess.check_output(['bash','-c', cmd])

def store():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('store', anonymous=True)
    rospy.Subscriber('telegram', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    store()

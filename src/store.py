#!/usr/bin/env python

import rospy
import json
import subprocess
import os
import shutil
from std_msgs.msg import String

def getPaths():
    parser = os.path.dirname(os.path.abspath(__file__)).split("/")
    str=""
    path_src = ""
    path_store = ""
    path_catkin_ws = ""
    parser_len = len(parser)
    for i in range(parser_len):
	str = str + parser[i] +"/"
	if (i==parser_len-4):
	    path_catkin_ws = str
	elif(i==parser_len-3):
	    path_src = str
        elif(i==parser_len-2):
            path_store= str
    return [path_src, path_store, path_catkin_ws]


def installcall(data):
    rospy.loginfo(rospy.get_caller_id() + 'Installing %s...', data.data)
    
    path = getPaths()
    path_src = path[0]
    path_store = path[1]
    path_catkin_ws = path[2]

    with open(path_store+'app_list.json') as data_file:    
        apps = json.load(data_file)

    pkg = data.data

    # Download pkg
    cmd = "git clone "+apps[pkg]+" "+path_src+pkg

    try:
        output = subprocess.check_output(['bash','-c', cmd])
        print "Done"
    except:
        print "Already exist!"

    # Catkin_make
    cmd = "catkin_make -C "+path_catkin_ws
    output = subprocess.check_output(['bash','-c', cmd])

    # Launch pkg
    try:
        cmd = "roslaunch "+pkg+" *"
        output = subprocess.check_output(['bash','-c', cmd])
        print "Running"
    except:
        print "launch file doesn't work!"

def removecall(data):
    rospy.loginfo(rospy.get_caller_id() + 'Removing %s...', data.data)
	
    path = getPaths()
    path_src = path[0]
    path_store = path[1]
    path_catkin_ws = path[2]

    with open(path_store+'app_list.json') as data_file:    
      	apps = json.load(data_file)
	
    pkg = data.data
    shutil.rmtree(path_src + pkg)
	

def store():
    rospy.init_node('store', anonymous=True)
    rospy.Subscriber('telegram_install', String, installcall)
    rospy.Subscriber('telegram_remove', String, removecall)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    store()

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
    print("path_src:"+path_src)
    print("path_store:"+path_store)
    print("path_catkin_ws:"+path_catkin_ws)
 #   print("path: "+os.path.dirname(os.path.abspath(__file__)))
	
	
    return [path_src, path_store, path_catkin_ws]
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'Installing %s...', data.data)
    
    path = getPaths()
    path_src = path[0]
    path_store = path[1]
    path_catkin_ws = path[2]


    with open(path_store+'app_list.json') as data_file:    
        apps = json.load(data_file)

    pkg = data.data
    cmd = "git clone "+apps[pkg]+" "+path_src+"src/"+pkg
    output = subprocess.check_output(['bash','-c', cmd])

    print "Done"

    cmd = "roslaunch "+pkg+" "+"*.launcher"

def removecall(data):
    rospy.loginfo(rospy.get_caller_id() + 'Removing %s...', data.data)
	
    path = getPaths()
    path_src = path[0]
    path_store = path[1]
    path_catkin_ws = path[2]

    with open(path_store+'app_list.json') as data_file:    
      	apps = json.load(data_file)
	
    pkg = data.data
    #cmd = "rmdir " + path_src + pkg + ' -r';

    #output = subprocess.check_output(['bash','-c', cmd])
    shutil.rmtree(path_src + pkg)
	

def store():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('store', anonymous=True)
    rospy.Subscriber('telegram_install', String, callback)
    rospy.Subscriber('telegram_remove', String, removecall)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    store()

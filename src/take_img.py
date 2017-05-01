#!/usr/bin/env python

import rospy
import json
import subprocess
import os
import shutil
from std_msgs.msg import String
from std_msgs.msg import Bool

def takecall(data):
    print "foto"
    try:
	print "foto"
        output = subprocess.check_output(['bash','-c', 'rostopic pub /trigger std_msgs/Bool "data: true" >> /dev/null &'])
	print output
	#pp.publish("true")
    except:
        print ""
    print "..."

def take_pic():
    print "foto"
    rospy.init_node('get_image', anonymous=True)
    rospy.Subscriber('new_image', String, takecall)
    #pp = rospy.Publisher('/trigger', Bool, queue_size=10)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    take_pic()

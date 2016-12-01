#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2016
# Modified by: Student name and number

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

x_ant = 0
y_ant = 0
obj_ant = ''
question =''

# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant
	x=data.pose.pose.position.x
	y=data.pose.pose.position.y
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1faala" % (x,y)
	x_ant = x
	y_ant = y

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant
	obj = data.data
	if obj != obj_ant:
		print "object is %s" % data.data
	obj_ant = obj
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	print "question is %s" % data.data
	question = data.data

# ---------------------------------------------------------------
def agent():
	rospy.init_node('agent')

	rospy.Subscriber("questions_keyboard", String, callback2)
	rospy.Subscriber("object_recognition", String, callback1)
	rospy.Subscriber("odom", Odometry, callback)

	rospy.spin()

# ---------------------------------------------------------------
if __name__ == '__main__':
	agent()

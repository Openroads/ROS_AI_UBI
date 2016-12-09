#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2016
# Modified by: Student name and number

#imports

#-----
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

x_ant = 0
y_ant = 0
obj_ant = ''
question =''


def designateRoom():
	# first row
	if(x_ant > -1 and x_ant <= 3.5 and y_ant > -3 and y_ant <= 1.5 ): 
		return 1;
	if(x_ant > -6 and x_ant <= -1 and y_ant > -3 and y_ant <= 1.5 ): 
		return 2;
	if(x_ant > -11 and x_ant <= -6 and y_ant > -3 and y_ant <= 1.5 ): 
		return 3;
	if(x_ant > -16 and x_ant <= -11 and y_ant > -3 and y_ant < 1.5 ): 
		return 4;
	# second row
	if(x_ant > -1 and x_ant <=3.5 and y_ant > 1.5 and y_ant <= 6.5 ): 
		return 5;
	if(x_ant > -6 and x_ant <= -1 and y_ant > 1.5 and y_ant <= 6.5 ): 
		return 6;
	if(x_ant > -11 and x_ant <= -6 and y_ant > 1.5 and y_ant <= 6.5 ): 
		return 7;
	if(x_ant > -16 and x_ant <= -11 and y_ant > 1.5 and y_ant <= 6.5 ): 
		return 8;
	#third row
	if(x_ant > -1 and x_ant <=3.5 and y_ant > 6.5 and y_ant <= 11): 
		return 9;
	if(x_ant > -6 and x_ant <= -1 and y_ant > 6.5 and y_ant <= 11 ): 
		return 10;
	if(x_ant > -11 and x_ant <= -6 and y_ant > 6.5 and y_ant <= 11 ): 
		return 11;
	if(x_ant > -16 and x_ant <= -11 and y_ant > 6.5 and y_ant <= 11 ): 
		return 12;

		
def saveObject():
	numberRoom = designateRoom()
	print numberRoom


# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant
	x=data.pose.pose.position.x
	y=data.pose.pose.position.y
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1f" % (x,y)
	x_ant = x
	y_ant = y

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant
	obj = data.data
	if obj != obj_ant:
		print "object is %s" % data.data
		saveObject()
	obj_ant = obj
	
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	global question
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


# --------------------Our implementation -------------------------	
#g = rdflib.Graph()

roomObjects ={'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[]}





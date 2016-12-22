#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2016
# Modified by: Student name and number

#imports

#-----
import sys
import rospy
import numpy as np
import csv
from std_msgs.msg import String
from nav_msgs.msg import Odometry

x_ant = 0
y_ant = 0
obj_ant = ''
#question =''

# --------------------Our implementation -------------------------	
#g = rdflib.Graph()

roomObjects ={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
visitedRoom =[False]*12;
lastObject =''

def lastMetObject():
	print lastObject
	if(len(lastObject)>0):
		print "The last saw object is: %s" % lastObject
	else:
		print "I haven't seen any object yet"

def countRecognizedObjects():
	counter =0;
	for x in range(1,13):
		objList=roomObjects[x]
		counter=counter + len(objList)

	if(counter>1):
		print "I have already recognized %d objects" % counter
	else:
		print "I have already recognized %d object" % counter	
def showVisitedRoom():
	print("I have already visited room: ")
	for x in range(0,len(visitedRoom)):
		if(visitedRoom[x] is True):
			sys.stdout.write(str(x+1) + " ")
			sys.stdout.flush()
	print ""

def answerToQuestion(question):
	functions ={
		'a':lastMetObject,
		'b':countRecognizedObjects,
		'i':showVisitedRoom,
		}

	fun = functions.get(question,0)
	if(fun != 0):
		fun()



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
	return 1
		
def saveObject(dictionary,objectadd):
	numberRoom = designateRoom()
	roomListObj = dictionary[numberRoom];
	objectsToAdd = objectadd.split(",")
	global lastObject
	last = objectsToAdd[len(objectsToAdd)-1]
	if(len(last)>1):
		lastObject = last
	for o in objectsToAdd:
		if(o not in roomListObj and len(o) >1):
			dictionary[numberRoom].append(o)

def saveToCSVFile(x,y,objects):

	objL = objects.split(",")
	for o in objL:
		if(len(o) >1):
			with open('/home/viki/catkin_ws/src/ia/output/data.csv','ab') as csvfile:
				wr = csv.writer(csvfile,delimiter=",",quoting=csv.QUOTE_NONE)
				data=[]
				data.append(x) 
				data.append(y) 
				data.append(o)
				wr.writerow(data)








# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant
	x=data.pose.pose.position.x
	y=data.pose.pose.position.y
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1f" % (x,y)
		visitedRoom[designateRoom()-1]=True;
	x_ant = x
	y_ant = y

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global x_ant, y_ant
	global obj_ant
	obj = data.data
	if obj != obj_ant:
		print "object is %s" % data.data
		saveObject(roomObjects,obj)
		saveToCSVFile(x_ant,y_ant,obj)
	obj_ant = obj
	
		
# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	print "question is %s" % data.data
	question = data.data
	answerToQuestion(question);

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








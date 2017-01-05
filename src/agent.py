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
import ast
import os.path
import os

from std_msgs.msg import String
from nav_msgs.msg import Odometry

#########       Paths for filename :    ########
FILE_OBJECTS_CSV = '/home/viki/catkin_ws/src/ia/output/objects.csv'
FILE_VISITED_CSV = '/home/viki/catkin_ws/src/ia/output/visited.csv'
FILE_LASTOBJ_CSV = '/home/viki/catkin_ws/src/ia/output/lastobj.csv'


### helpful global variable ###

RESET_FLAG = False
lastRoom=0


x_ant = 0
y_ant = 0
obj_ant = ''
#question =''

# --------------------Our implementation -------------------------	
#g = rdflib.Graph()
#######  stored data  ######
roomObjects ={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
visitedRoom =[False]*12
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
	print roomObjects
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
#How many books did you found
def countBooks():
        counter = 0;
        for x in range(1, 13):
                objList = roomObjects[x]
                for n in objList:
                        if(n[0] == 'book'):
                                counter = counter + 1;
        if(counter>0):
                print "I have already seen %d books" %counter
        else:
                print "I haven't seen any books yet"

def getPositioOfObject(seachObject):
	print roomObjects
	for x in range(1, 13):
                objList = roomObjects[x]
                for n in objList:
                        if(n[0] == seachObject):
                        	return n[2],n[3]


def cleanData():
	print "Robot is reseting...."
	global RESET_FLAG
	RESET_FLAG = True
	if(os.path.exists(FILE_VISITED_CSV)  and os.path.exists(FILE_OBJECTS_CSV) and os.path.exists(FILE_LASTOBJ_CSV)):
		os.remove(FILE_OBJECTS_CSV)
		os.remove(FILE_VISITED_CSV)
		os.remove(FILE_LASTOBJ_CSV)
	roomObjects ={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
	print 'Reseted.\n'
	os.system('kill $PPID')
	print "Run agent again."
	
def answerToQuestion(question):
	functions ={
		'a':lastMetObject,
		'b':countRecognizedObjects,
		'i':showVisitedRoom,
		'e':countBooks,
		'#':cleanData,
		}

	fun = functions.get(question,0)
	if(fun != 0):
		fun()



def designateRoom(x_a,y_a):
	# first row
	if(x_a > -1 and x_a <= 3.5 and y_a > -3 and y_a <= 1.5 ): 
		return 1;
	if(x_a > -6 and x_a <= -1 and y_a > -3 and y_a <= 1.5 ): 
		return 2;
	if(x_a > -11 and x_a <= -6 and y_a > -3 and y_a <= 1.5 ): 
		return 3;
	if(x_a > -16 and x_a <= -11 and y_a > -3 and y_a < 1.5 ): 
		return 4;
	# second row
	if(x_a > -1 and x_a <=3.5 and y_a > 1.5 and y_a <= 6.5 ): 
		return 5;
	if(x_a > -6 and x_a <= -1 and y_a > 1.5 and y_a <= 6.5 ): 
		return 6;
	if(x_a > -11 and x_a <= -6 and y_a > 1.5 and y_a <= 6.5 ): 
		return 7;
	if(x_a > -16 and x_a <= -11 and y_a > 1.5 and y_a <= 6.5 ): 
		return 8;
	#third row
	if(x_a > -1 and x_a <=3.5 and y_a > 6.5 and y_a <= 11): 
		return 9;
	if(x_a > -6 and x_a <= -1 and y_a > 6.5 and y_a <= 11 ): 
		return 10;
	if(x_a > -11 and x_a <= -6 and y_a > 6.5 and y_a <= 11 ): 
		return 11;
	if(x_a > -16 and x_a <= -11 and y_a > 6.5 and y_a <= 11 ): 
		return 12;
	return 1
		
def saveObject(dictionary,objectadd,x,y):
	numberRoom = designateRoom(x,y)
	roomListObj = dictionary[numberRoom];
	objectsToAdd = objectadd.split(",")
	global lastObject
	last = objectsToAdd[len(objectsToAdd)-1]
	if(len(last)>1):
		lastObject = last
	for o in objectsToAdd:
		if(len(o) > 1):
			obj = o.split("_")
			category=obj.pop(0)
			objstr=''
			for e in obj:
				objstr +=e+" "
			
			for roomobj in roomListObj:
				if(objstr in roomobj):
					return
			objPut =[category,objstr,x,y]		
			obj.append(x)
			obj.append(y)
			dictionary[numberRoom].append(objPut)


def saveData():
	print "Save data to files....."
	with open(FILE_OBJECTS_CSV,'wb') as csvfile:
		wr = csv.DictWriter(csvfile,fieldnames=roomObjects.keys())
		wr.writerow(roomObjects)
	csvfile.close()


	with open(FILE_VISITED_CSV,'wb') as csvfile:
		wr = csv.writer(csvfile,delimiter=",",quoting=csv.QUOTE_NONE)
		wr.writerow(visitedRoom)
	csvfile.close()

	with open(FILE_LASTOBJ_CSV,'wb') as csvfile:
		wr = csv.writer(csvfile,delimiter=",",quoting=csv.QUOTE_NONE)
		wr.writerow(lastObject)
	csvfile.close()

	print "Finish."
	print "Shutting down..."
	print "Agent switched off."

def loadData(roomObjects,visitedRoom,lastObject):
	print "Load data from files......"
#read rooms with encountered objects
	with open(FILE_OBJECTS_CSV,'rb') as csvfile:
		reader = csv.DictReader(csvfile,fieldnames =roomObjects.keys())
		
		for row in reader:
			roomObjectsfile = row
		for x in roomObjectsfile:
			roomObjects[x] = ast.literal_eval(roomObjectsfile[x])
			#print roomObjects
# read visited room
	with open(FILE_VISITED_CSV, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		statusArray = reader.next()
		for x in range(0,len(statusArray)):
			if statusArray[x] == 'True':
				visitedRoom[x] = True
			elif statusArray[x] == 'False':
				visitedRoom[x] = False
			else:
			 print "Incorect data in visited.csv file. "
	csvfile.close()

	with open(FILE_LASTOBJ_CSV, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		lastObject = reader.next()
	csvfile.close()

	
# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant
	x=data.pose.pose.position.x
	y=data.pose.pose.position.y
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1f" % (x,y)
		visitedRoom[designateRoom(x,y)-1]=True;
		lastRoom = designateRoom(x,y)
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
		saveObject(roomObjects,obj,x_ant,y_ant)
		print roomObjects
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
	if(os.path.exists('/home/viki/catkin_ws/src/ia/output/')):
		if(os.path.exists(FILE_VISITED_CSV)  and os.path.exists(FILE_OBJECTS_CSV) and os.path.exists(FILE_LASTOBJ_CSV)):
			loadData(roomObjects,visitedRoom,lastObject)
		
		agent()
		if(not RESET_FLAG):
			saveData()
	
	else:
		print 'Create a directory with name "output" inside src/ia/ folder. The file path should be: "/home/viki/catkin_ws/src/ia/output/ . \nIt is neccesary to store the data collected by agent.'








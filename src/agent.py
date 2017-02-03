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
import math
import networkx as nx

from std_msgs.msg import String
from nav_msgs.msg import Odometry


# --------------------Our implementation -------------------------	

#########       Paths for filename :    ########
FILE_OBJECTS_CSV = '/home/viki/catkin_ws/src/ia/output/objects.csv'
FILE_VISITED_CSV = '/home/viki/catkin_ws/src/ia/output/visited.csv'
FILE_LASTOBJ_CSV = '/home/viki/catkin_ws/src/ia/output/lastobj.csv'
FILE_ROOMDOR_CSV = '/home/viki/catkin_ws/src/ia/output/roomdor.csv'


### helpful global variable ###
COOR_FLAG = True
RESET_FLAG = False

x_ant = 0
y_ant = 0
obj_ant = ''


G = nx.Graph()
#######  stored data  ######
roomObjects ={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
visitedRoom =[False]*12
lastObject ='a'
lastRoom = -1
roomDoors =[]

#####################################  Function to answer the questions ##############################################

# A) What was the last object that you saw?
def lastMetObject():
	
	if(len(lastObject)>0 and lastObject != 'a'):
		print "The last saw object is: %s" % lastObject
	else:
		print "I haven't seen any object yet"
# B) How many objects did you recognize until now?'
def countRecognizedObjects():
	counter =0;
	for x in range(1,13):
		objList=roomObjects[x]
		counter=counter + len(objList)
	if(counter>1):
		print "I have already recognized %d objects" % counter
	else:
		print "I have already recognized %d object" % counter

# C) What is the object that is closer to you?
def whatIsCloserToMe():
	closestObject = ''
	minDistance = 1000000
	myPosition = [x_ant, y_ant]
	for x in range(1,13):
		objList = roomObjects[x]
		for n in objList:
			positionOfObject = getPositionOfObject(n[1])
			distance = distanceBetweeneObjects(myPosition, positionOfObject)
			if(distance < minDistance):
				closestObject = n[1]
				minDistance = distance
	if(closestObject == ''):
		print "I haven't seen any object around me :("
	else:
		print "The closest object I have seen is %s" %closestObject

# D) What is the object that is closer to Joe?
def whatIsCloserToJoe():
	closestObject = ''
	minDistance = 100000
	if(haveIseenSomeone('joe') == 1):
		joePosition = getPositionOfObject('joe')
		for x in range(1,len(roomObjects)+1):
			objList = roomObjects[x]
			for n in objList:
				if(n[1] != 'joe'):
					positionOfObject = getPositionOfObject(n[1])
					distance = distanceBetweeneObjects(joePosition, positionOfObject)
					if(distance < minDistance):
						closestObject = n[1]
						minDistance = distance
		if(closestObject != ''):
			print "The closest object I have seen to Joe is: %s" %closestObject
		else:
			print "I haven't seen any objects around Joe, but I know where he is"
	else:
		print "I haven't seen Joe yet, so I dont know what is around him :("
# E) How many books did you found ?
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

# F) Have you seen Mary?
def haveIseenMary():
	if(haveIseenSomeone('mary') == 0):
		print 'No, I haven\'t seen Mary yet'
	else:
		maryRoom = -1
		for x in range(1, len(roomObjects)+1):
			objList = roomObjects[x]
			for n in objList:
				if(n[1] == 'mary'):
					maryRoom = x
		print 'Yes, I\'ve seen Mary\nShe is in room number %s' %maryRoom

# G) In which room is Joe?
def inWhichRoomIsJoe():
	flag = 0
	room = -125
	for x in range(1, len(roomObjects)+1):
		objList = roomObjects[x]
		for n in objList:
			if(n[1] == 'joe'):
				flag = 1
				room = x
	if(flag == 0):
		print "I don't know where is Joe, I haven't seen him yet"
	else:
		print "Joe is in a room number: %d" %room

# H) Is there any room that has a table?
def isThereRoomContainsTable():
	roomsContainsTable = []
	for x in range(1, len(roomObjects)+1):
		objList = roomObjects[x]
		for n in objList:
			if(n[0] == 'table'):
				if x not in roomsContainsTable:
					roomsContainsTable.append(x)
	if not roomsContainsTable:
		print 'I didn\'t find yet any room wich contains table'
	else:
		if(len(roomsContainsTable) == 1):
			print 'I found one room which contains table and it\'s room number: %s' %roomsContainsTable[0]
		else:
			print 'I know, that in each of %s rooms you can find at least one table' %roomsContainsTable

# I) Which rooms have you visited already?
def showVisitedRoom():
	print("I have already visited room: ")
	for x in range(0,len(visitedRoom)):
		if(visitedRoom[x] is True):
			sys.stdout.write(str(x+1) + " ")
			sys.stdout.flush()
	print ""
# J)What is the probability of finding a person in a room given that the room contains a chair and does not contain a table?
def probabilityFindPersoneInRoomHavingChairsWithoutTable():
	roomsContainsChairsAndNotContaisTable = []
	counterCase = 0
	countPeople = 0
	for x in range(1, len(roomObjects)+1):
		objList = roomObjects[x]
		if(checkObject(objList, 'chair')):
			if(checkObject(objList, 'table') == False):
				roomsContainsChairsAndNotContaisTable.append(x)
				counterCase += 1
				if(checkObject(objList, 'person')):
					countPeople += 1
	if(counterCase == 0):
		print 'Ohhh... until now I haven\'t seen any rooms which have chairs and don\'t contain any table'
	else:
		if(countPeople == 0):
			print 'I haven\'t seen in that rooms any people, so in this case propability equals 0'
		else:
			probability = countPeople/float(counterCase)
			print 'Having exciting knowledge I can say, that probability you have asked equals %.2f' %probability

# K) How probable is to find a person in a room that has a table?
def probableFindPersonInRoomWithTable():
	roomsWithTable = []
	peopleInRoomWithTable = 0
	for x in range(1, len(roomObjects)+1):
			objList = roomObjects[x]
			for n in objList:
				if(n[0] == 'table'):
					if(x not in roomsWithTable):
						roomsWithTable.append(x)
	if not roomsWithTable:
		print 'Ohhh... until now I haven\'t seen any room with table, I can\'t answere this question :('
	else:
		for o in roomsWithTable:
			if(checkObject(roomObjects[o], 'person')):
				peopleInRoomWithTable = peopleInRoomWithTable + 1
		probability = peopleInRoomWithTable/float((len(roomsWithTable)))
		print 'Having exicting knowledge I can say, that probability you have asked equals %.2f' %probability
# L)  In what type of room are you?
def whatTypeOfRoomAmI():
	staff = {'chairs': 0, 'computers': 0, 'tables': 0, 'people': 0, 'books': 0}
	roomIam = designateRoom(x_ant,y_ant)
	objList = roomObjects[roomIam]
	for n in objList:
		if(n[0] == 'chair'):
			staff['chairs'] = staff['chairs'] + 1
		if(n[0] == 'computer'):
			staff['computers'] = staff['computers'] + 1
		if(n[0] == 'table'):
			staff['tables'] = staff['tables'] + 1
		if(n[0] == 'person'):
			staff['people'] = staff['people'] + 1
		if(n[0] == 'book'):
			staff['books'] = staff['books'] + 1
	if((staff['chairs'] == 0) and (staff['computers'] == 0) and (staff['tables']== 0) and (staff['people'] == 0) and (staff['books'] == 0)):
		print 'I haven\'t seen any objects there, so I just don\'t know the answer of this question :('
	else:
		if((staff['chairs'] > 0) and (staff['computers'] == 0) and (staff['tables'] == 0) and (staff['people'] == 0)):
			print 'I think, I\'m right now in the waiting room'
		else:
			if((staff['chairs'] > 0) and (staff['tables'] > 0) and (staff['books'] > 0) and (staff['computers'] == 0)):
				print 'Having the knowledge as I have right now, I can tell you I\'m in study room'
			else:
				if((staff['computers'] > 0) and (staff['tables'] > 0) and (staff['chairs'] > 0)):
					print 'I think I\'m in computer lab'
				else:
					if((staff['tables'] == 1) and staff['chairs'] > 0):
						print 'I\'m in the meeting room'
					else:
						print 'I\'m thinking I\'m in the generic room\nBut I also can have not enough data'

# M) Which rooms are free (not occupied)?
def whichRoomisNotOccupied():
	occupatedRooms = []
	notOccupatedRooms = []
	for x in range(1, len(roomObjects)+1):
		objList = roomObjects[x]
		for n in objList:
			if(n[0] == 'person'):
				occupatedRooms.append(x)
	for p in range(1, 13):
		if(p not in occupatedRooms and visitedRoom[p-1] is True):
			notOccupatedRooms.append(p)
	if not notOccupatedRooms:
		print "I've seen people in every rooms, so no one is free"
	else:
		if(len(notOccupatedRooms) == 1):
			print "From the all rooms which I visited only in %s room I haven't seen any people" %notOccupatedRooms
		else:
			print 'I\'ve been in rooms number: %s and I haven\'t seen there any people, so probably those are not occupied' %notOccupatedRooms
			if occupatedRooms:
				if(len(occupatedRooms) > 1):
					print 'But I am sure that rooms: %s are occupied' %occupatedRooms
				else:
					print 'But I am sure that room: %s is occupied' %occupatedRooms

# N) Do you think Mary prefers Apple or Windows computers?
def whatOperatingSystemPrefereMary():
	maryRoom = -1
	doIknowMary = False
	whatComputerMaryHas = []
	if(haveIseenSomeone('mary') == 0):
		print 'Who is Mary ? I haven\'t seen her yet'
	else: 
		for x in range(1, len(roomObjects)+1):
			objList = roomObjects[x]
			for n in objList:
				if(n[1] == 'mary'):
					maryRoom = x
					doIknowMary = True
		objLista = roomObjects[maryRoom]
		for n in objLista:
			if(n[0] == 'computer'):
				whatComputerMaryHas.append(n[1])
		if not whatComputerMaryHas:
			print 'I don\'t know, I haven\'t seen any computer in Mary\'s room'
		else:
			if(len(whatComputerMaryHas) == 1):
				operSys = whatComputerMaryHas[0]
				print 'I\'m almost sure, that she preferes %s operating system\nI didn\'t find any other computers there' %operSys[0:len(operSys)-1]
			else:
				oppourtunities = {'windows': 0, 'linux': 0, 'apple': 0}
				for n in whatComputerMaryHas:
					if(n[0:len(n)-1] == 'windows'):
						oppourtunities['windows'] = oppourtunities['windows'] + 1
					if(n[1:len(n)-1] == 'linux'):
						oppourtunities['linux'] = oppourtunities['linux'] + 1
					if(n[1:len(n)-1] == 'apple'):
						oppourtunities['apple'] = oppourtunities['apple'] + 1
				mxValues = [key for key,val in oppourtunities.iteritems() if val == max(oppourtunities.values())]
				if(len(mxValues)>1):
					print 'It\'s difficult to choose which operating system she preferes.\nShe has %s of %s computers' %(oppourtunities[mxValues], mxValues)
				else:
					print 'Mary preferes %s computers' %mxValues
# O) -Do I need to pass by room 7 to go to room 9?
def toRoom9():
	G.add_edges_from(roomDoors)
	myRoom = designateRoom(x_ant,y_ant)
	searchFlag = True
	roomWas = False
	nodes = G.nodes()
	if (9 not in nodes):
		print 'I don\'t know where is room number 9.'
		return
	paths = nx.all_simple_paths(G,myRoom,9)
	paths = list(paths)
	shortPath = 1000
	counter = 0
	pathWithout7 = []
	numberPath = len(paths)
	# Case when agent don't know about door leading to room 9
	if(numberPath == 0):
		print 'I don\'t know how to get room 9 yet.'
		return
	for x in range(0,numberPath):
		l=len(paths[x])
		if shortPath > l:
			shortPath = l
			position = x
	if(paths[0][0]==7):
		print 'I\'m in room 7. The shortest path to room 9 is:' + '-'.join(str(x) for x in paths[position][1:-1])
		return
	shortPath = 1000
	for p in range(0,numberPath):
		searchFlag = True
		pat=paths[p]
		for r in pat:
			if(r == 7):
				searchFlag = False
		if(searchFlag == True):
			counter += 1
			roomWas = True
			pathWithout7.append(pat)
			if counter == 1:
				print '\nNo, I don\'t need to pass room 7.'
			pathLength = len(pat)
			if(pathLength < shortPath):
				shortPath = pathLength
				position = p
			if 9 == pat[0]:
				print 'I\'m in room 9 ! '
				return
			elif (pathLength == 2):
				print 'I can go straight to room 9, through door between rooms %d and %d'%(pat[0],pat[1])
			else:
				if(counter > 1):
					print 'or through room: ' + '-'.join(str(x) for x in pat[1:-1])
				else:
					print 'To go to room 9 I can go through room: ' + '-'.join(str(x) for x in pat[1:-1])

	if(not pathWithout7):
		print 'I must pass room 7.'
	else:
		length = len(pathWithout7)
		lengths = [len(x) for x in pathWithout7]
		if(not (all(a==lengths[0] for a in lengths))):	
			if length > 1:
				if shortPath == 2:
					print 'But the shortest path is going straight through door between rooms %d and %d'%(paths[position][0],paths[position][1])
				elif shortPath == 3:
					print'But the shortest path is go through room ' + str(paths[position][1])
				else:
					print 'But the shortest path is ' + '-'.join(str(x) for x in paths[position][1:-1])

# P) - Wchich room is needed to pass to achieve computer lab
def passRoomToComputerLab():
	flagFirstTime  = True
	myRoom = designateRoom(x_ant,y_ant)
	computerLab = findComputerLab()
	if computerLab:
		G.add_edges_from(roomDoors,weight =float(1))
		print computerLab
		#compRoom - destination room, comp laboratory 
		for compRoom in computerLab:
			print 'To computer lab in room: %d' % compRoom
			paths = nx.all_simple_paths(G,myRoom,compRoom)
			paths = list(paths)
			if len(paths) == 0:
				print 'I don\'t know about any path to computer lab in room: %d. ' % (compRoom)
				break
			for roomToPass in paths:
				
				pathLength = len(roomToPass)
				if pathLength == 1 :
					print 'I\'m in computer lab at room %d! ' % (compRoom)
					print roomToPass
					break
				elif (pathLength == 2):
					if flagFirstTime:
						print 'I can go straight to computer lab, through door between rooms %d and %d'%(roomToPass[0],roomToPass[1])
					else:
						print 'or i go straight, through door between rooms %d and %d'%(roomToPass[0],roomToPass[1])
				else:
					if flagFirstTime:
						print 'To go to computer lab in room %d I need to pass room: ' %(compRoom) + '-'.join(str(x) for x in roomToPass[1:-1])
					else:
						print 'or I can go through room: ' + '-'.join(str(x) for x in roomToPass[1:-1])
				flagFirstTime = False
	else:
		print "I am not sure exactly, if there is any computer lab."	

# Q)What is the shortest path what I must pass to go to computer lab ?
def theShortestToComputerLab():
	global COOR_FLAG 
	myRoom = designateRoom(x_ant,y_ant)
	computerLab = findComputerLab()
	if computerLab:	
		G.add_edges_from(roomDoors,weight =float(1))
		#compRoom - destination room, comp laboratory 
		for compRoom in computerLab:
			roomToPass = nx.astar_path(G,myRoom,compRoom,astar_heuristic)
			pathLength = len(roomToPass)
			if pathLength == 0:
				print 'I don\'t know about any computer lab. '
			elif pathLength == 1 :
				print 'I\'m in computer lab at room %d! ' % (compRoom)
			elif (pathLength == 2):
				print 'I can go straight to computer lab, through door between rooms %d and %d'%(roomToPass[0],roomToPass[1])
			else:
				print 'To go to computer lab in room %d I need to pass room: ' %(compRoom) + '-'.join(str(x) for x in roomToPass[1:-1])
	else:
		print "I am not sure exactly, if there is any computer lab."

# R) What is the shortest path what I must pass to find  book sports illustrated review 

def findTheShortestPathToObject():
	objectToSearch = 'sports illustrated review'
	myRoom = designateRoom(x_ant,y_ant)
	positionObject = getPositionOfObject(objectToSearch)
	if(not positionObject):
		print 'I don\'t know that object'
		return
	destinationRoom = designateRoom(positionObject[0],positionObject[1])
	#for row in content:
	G.add_edges_from(roomDoors,weight =float(1))
	#compRoom - destination room, comp laboratory 

	roomToPass = nx.astar_path(G,myRoom,destinationRoom,astar_heuristic)
	pathLength = len(roomToPass)
	if pathLength == 0:
		print 'I don\'t know about any path to computer lab. '
	elif pathLength == 1 :
		print 'The %s is in room, where I\'m now. ! ' % (objectToSearch)
	elif (pathLength == 2):
		print 'I can go straight to the room, through door between rooms %d and %d'%(roomToPass[0],roomToPass[1])
	else:
		print 'To go to the room,where is  %s I need to pass room: ' %(objectToSearch) + '-'.join(str(x) for x in roomToPass[1:-1])
		print roomToPass
# S) What do you know about objects in every room ?'
def	showWhatYouKnow():
	print 'What I know about world:'
	for x in range(1,len(roomObjects)+1):
		for obj in roomObjects[x]:
			if(len(obj)>0):
				print 'Room %d:' % x
				print '\t  %s   %s   %s   %s' %(obj[0],obj[1],obj[2],obj[3])
#T) show known door
def showKnownDoor():
	print 'Door:'
	for x in roomDoors:
		print x

#######################################        Helpful function  ##########################################################
def astar_heuristic(object1, object2):
	
	coor1 = giveRoomCoordinates(object1)
	agentroom = designateRoom(x_ant,y_ant)
	neighbors = G.neighbors(agentroom)
	coor2 = giveRoomCoordinates(object2)
	#print 'Node(obj1): %d' % object1

	if(object1 in neighbors):
		distance =  math.hypot(x_ant - coor1[0], y_ant - coor1[1])

		#print 'Distance (coordinates):'
		#print distance
	else:
		distance = math.hypot(coor1[0] - coor2[0], coor1[1]- coor2[1])
		#print 'Distance:'
		#print distance
	return distance

def getPositionOfObject(seachObject):
        for x in range(1, len(roomObjects)+1):
                objList = roomObjects[x]
                for n in objList:
                        if(n[1] == seachObject):
                                return n[2],n[3]
#Object1[x][y] Object[x][y] 
def distanceBetweeneObjects(object1, object2):
	distance = math.hypot(object2[0] - object1[0], object2[1] - object1[1])
	return distance

def findComputerLab():
	computerLab =[]
	for x in range(1,len(roomObjects)+1):
		objList = roomObjects[x]
                for n in objList:
                        if(n[0] == 'computer'):
                        	if(checkObject(objList,'table') and checkObject(objList,'chair')):
                        		if x not in computerLab: 
                        			computerLab.append(x)

    	return computerLab

def checkObject(listObj,objCategory):
	for obj in listObj:
		if(obj[0] == objCategory):
			return True
	return False

def haveIseenSomeone(someone):
    flag = 0
    for x in range(1, len(roomObjects)+1):
            objList = roomObjects[x]
            for n in objList:
                    if(n[1] == someone):
                            flag = 1
    return flag

def findDoor(x,y):
	global roomDoors
	global lastRoom
	room = designateRoom(x,y)
	if(lastRoom != room):
		print roomDoors
		if not roomDoors:
			roomDoors.append([lastRoom,room])
		else:
			for row in roomDoors:
				print row
				if((lastRoom == row[0] and room == row[1]) or (lastRoom == row[1] and room ==  row[0])):
					lastRoom = room
					return
			print 'I found a new door !'		
			roomDoors.append([lastRoom,room])	

		lastRoom = room
################     # - resetowanie robota z wszystkich danych
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
		'c':whatIsCloserToMe,
		'd':whatIsCloserToJoe,
		'e':countBooks,
		'f':haveIseenMary,
		'g':inWhichRoomIsJoe,
		'h':isThereRoomContainsTable,
		'i':showVisitedRoom,
		'j':probabilityFindPersoneInRoomHavingChairsWithoutTable,
		'k':probableFindPersonInRoomWithTable,
		'l':whatTypeOfRoomAmI,
		'm':whichRoomisNotOccupied,
		'n':whatOperatingSystemPrefereMary,
		'o':toRoom9,
		'p':passRoomToComputerLab,
		'q':theShortestToComputerLab,
		'r':findTheShortestPathToObject,
		's':showWhatYouKnow,
		't':showKnownDoor,
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
def giveRoomCoordinates(ask):
	room ={
		1:[1.5,-1.0],
		2:[-3.5,-1.0],
		3:[-8.5,-1.0],
		4:[-13.5,-1],
		5:[1.5,4.0],
		6:[-3.5,4.0],
		7:[-8.5,4.0],
		8:[-13.5,4.0],
		9:[1.5,9],
		10:[-3.5,9],
		11:[-8.5,9],
		12:[-13.5,9]
		}

	coordinates = room.get(ask,0)
	if(coordinates):
		return coordinates
	else:
		print 'Incorect room (giveRoomCoordinates function)'

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
			objstr=' '.join(obj)
			
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
		wr.writerow([lastObject])
	csvfile.close()

	with open(FILE_ROOMDOR_CSV,'wb') as csvfile:
		wr = csv.writer(csvfile,delimiter=",",quoting=csv.QUOTE_NONE)
		for row in roomDoors:
			wr.writerow(row)
	csvfile.close()
	print "Finish."
	print "Shutting down..."
	print "Agent switched off."

def loadData():
	global roomObjects
	global visitedRoom
	global lastObject
	#global lastRoom
	global roomDoors
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
# read last object and room  
	with open(FILE_LASTOBJ_CSV, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		lastObject = reader.next()
		#lastRoom = int(readdat[1])
		lastObject = lastObject[0]
	csvfile.close()
# read doors between rooms
	with open(FILE_ROOMDOR_CSV, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			row = [int(x) for x in row]
			roomDoors.append(row)

	csvfile.close()
	
# ---------------------------------------------------------------
# odometry callback
def callback(data):
	global x_ant, y_ant
	global lastRoom
	x=data.pose.pose.position.x
	y=data.pose.pose.position.y
	# show coordinates only when they change
	if x != x_ant or y != y_ant:
		print " x=%.1f y=%.1f" % (x,y)
		visitedRoom[designateRoom(x,y)-1]=True;
		if(lastRoom == -1):
			lastRoom = designateRoom(x,y)
		else:
			findDoor(x,y)
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
		if(os.path.exists(FILE_VISITED_CSV)  and os.path.exists(FILE_OBJECTS_CSV) and os.path.exists(FILE_LASTOBJ_CSV) and os.path.exists(FILE_ROOMDOR_CSV)):
			loadData()

		agent()
		if(not RESET_FLAG):
			saveData()
	
	else:
		print 'Create a directory with name "output" inside src/ia/ folder. The file path should be: "/home/viki/catkin_ws/src/ia/output/ . \nIt is neccesary to store the data collected by agent.'








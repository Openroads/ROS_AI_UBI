#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32,String
import sys
import tty

# ---------------------------------------------------------------
def questions():
	# node name
	rospy.init_node('questions_keyboard')
	pub=rospy.Publisher('questions_keyboard',String,queue_size=10)
	r = rospy.Rate(10)
	
	# show questions
	print '  a-What was the last object that you saw?'
	print '  b-How many objects did you recognize until now?'
	print '  c-What is the object that is closer to you?'
	print '  d-What is the object that is closer to Joe?'
	print '  e-How many books did you found?'
	print '  f-Have you seen Mary?'
	print '  g-In which room is Joe?'
	print '  h-Is there any room that has a table?'
	print '  i-Which rooms have you visited already?'
	print '  j-What is the probability of finding a person in a room given that the room contains a chair and does not contain a table?'
	print '  k-How probable is to find a person in a room that has a table?'
	print '  l-In what type of room are you?'
	print '  m-Which rooms are free (not occupied)?'
	print '  n-Do you think Mary prefers Apple or Windows computers?'
	print '  o-Do I need to pass by room 7 to go to room 9?'
	print '  p-What rooms must I pass to go to a computer lab?'
	print '  q-What is the shortest path what I must pass to go to computer lab ?' 
	print '  r-What is the shortest path what I must pass to find  book sports illustrated review ?' 
	print '  s-What do you know about objects in every room ?'
	print '  t-Show known door'
	print '  #-To restet the robot'
	tty.setcbreak(sys.stdin)

	while not rospy.is_shutdown():
		# read from keyboard
		k=sys.stdin.read(1)
		pub.publish(k)
		#print 'Asked question: ' , k
		
# ---------------------------------------------------------------
if __name__ == '__main__':
	questions()

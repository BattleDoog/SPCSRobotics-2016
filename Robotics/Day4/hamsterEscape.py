import time
import Tkinter as tk
from threading import Thread
import Queue
from HamsterAPI.comm_usb import RobotComm

global gQuit

gQuit = False
gMaxRobotNum = 1;
gRobotList = []

watcherQueue = Queue.Queue()
handleQueue = Queue.Queue()

def watcher():
	while not gQuit:
		if (len(gRobotList) > 0):
			robot = gRobotList[0]
			leftProx = robot.get_proximity(0)
			rightProx = robot.get_proximity(1)
			leftFloor = robot.get_floor(0)
			rightFloor = robot.get_floor(1)

			watcherQueue.put([leftProx, rightProx, leftFloor, rightFloor])
			handleQueue.put([leftProx, rightProx])

			time.sleep(0.1)

def stopRobot(robot):
	global gQuit
	gQuit = True
	robot.set_wheel(0, 0)
	robot.set_wheel(1, 0)
	robot.set_musical_note(40)
	time.sleep(0.05)
	robot.set_musical_note(0)

def alertHandle(mycanvas, event = None):
	if not watcherQueue.empty():
		leftLaserIndicator = (125, 125, 125, 125)
		rightLaserIndicator = (175, 125, 175, 125)
	   
		leftFloorIndicator = (128, 128, 165 , 165)
		rightFloorIndicator = (165, 128, 182, 165)

		hamsterSize = (125, 125, 175, 175)
		mycanvas.create_rectangle(hamsterSize, fill = "blue")

		leftFloor = mycanvas.create_rectangle(leftFloorIndicator, fill = "yellow")
		rightFloor = mycanvas.create_rectangle(rightFloorIndicator, fill = "yellow")
	   
		leftLaser = mycanvas.create_line(leftLaserIndicator, fill = "red")
		rightLaser = mycanvas.create_line(rightLaserIndicator, fill = "red")

		while not gQuit:
			if (len(gRobotList) > 0):
				robot = gRobotList[0]

				floorInfo = watcherQueue.get()
				leftFloor = floorInfo[2]
				rightFloor = floorInfo[3]

				proxInfo = handleQueue.get()
				leftProx = proxInfo[0]
				rightProx = proxInfo[1]

				leftLaserObstruct = (125, 125, 125, proxInfo[0])
				rightLaserObstruct = (175, 125, 175, proxInfo[1])
				
				if(proxInfo[0] > 10):
					mycanvas.coords(leftLaser, leftLaserObstruct)
				else:
					mycanvas.coords(leftLaser, leftLaserIndicator)
				if(proxInfo[1] > 10):
					mycanvas.coords(rightLaser, rightLaserObstruct)
				else:
					mycanvas.coords(rightLaser, leftLaserIndicator)

				if(floorInfo[2] < 50):
					mycanvas.itemconfig(leftFloor, fill = "green")
				else:
					mycanvas.itemconfig(leftFloor, fill = "yellow")
				if(floorInfo[3] < 50):
					mycanvas.itemconfig(rightFloor, fill = "green")   
				else:
					mycanvas.itemconfig(rightFloor, fill = "yellow")

				if(floorInfo[2] < 30 or floorInfo[3] < 30):
					stopRobot(robot)
			time.sleep(0.05)

def motionHandle():
	while not gQuit:
		if (len(gRobotList) > 0):
			robot = gRobotList[0]
			if not handleQueue.empty():

				proxInfo = handleQueue.get()
				leftProx = proxInfo[0]
				rightProx = proxInfo[1]
				
				floorInfo = watcherQueue.get()
				leftFloor = floorInfo[2]
				rightFloor = floorInfo[3]
				floorSensor = (floorInfo[2], floorInfo[3])

				if(leftProx < 20 and rightProx < 20):
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)
					print "straight"
				elif(leftProx > rightProx): #turn left
					robot.set_wheel(0, 10)
					robot.set_wheel(1, -10)
					print "right"
				elif(leftProx < rightProx): #turn right
					robot.set_wheel(0, -10)
					robot.set_wheel(1, 10)
					print "left"
		#print proxInfo
		time.sleep(0.01)

def stopProg(event = None):	
	global gQuit
	gQuit = True
	print "Exit \n"
	m.quit()

def main():
	global gMaxRobotNum # max number of robots to control
	global gRobotList
	global m

	gQuit = False

	gMaxRobotNum = 1
	# thread to scan and connect to robot
	comm = RobotComm(gMaxRobotNum)
	comm.start()
	print 'Bluetooth starts'

	gRobotList = comm.robotList

	m = tk.Tk() #root
	mycanvas = tk.Canvas(m, bg="white", width=300, height= 300)
	mycanvas.pack()

	watcherThread = Thread(name = 'watcherThread', target = watcher)
	watcherThread.daemon = True
	watcherThread.start()

	alertThread = Thread(name = 'alerts', target = alertHandle, args = (mycanvas,))
	alertThread.daemon = True
	alertThread.start()

	motionThread = Thread(name = 'motion', target = motionHandle)
	motionThread.daemon = True
	motionThread.start()
	
	button = tk.Button(m,text="Exit")
	button.pack()
	button.bind('<Button-1>', stopProg)

	m.mainloop()

	watcherThread.join()
	alertThread.join()
	motionThread.join()

	for robot in gRobotList:
		robot.reset()

	comm.stop()
	comm.join()

# This is required by python to run the main function
if __name__== "__main__":
	main()
		
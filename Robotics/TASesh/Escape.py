import time  # sleep
import Queue
from threading import Thread
import Tkinter as tk
from HamsterAPI.comm_usb import RobotComm

gMaxRobotNum = 1; # max number of robots to control
gRobotList = None

eventQueue = Queue.Queue()
movementQueue = Queue.Queue()

gQuit = False

def watcher():
    while not gQuit:
        if(len(gRobotList) > 0):
            for robot in gRobotList: 
                leftProx = robot.get_proximity(0)
                rightProx = robot.get_proximity(1)
                leftFloor = robot.get_floor(0)
                rightFloor = robot.get_floor(1)

                eventQueue.put([leftProx, rightProx, leftFloor, rightFloor])
                movementQueue.put([leftProx, rightProx])
        time.sleep(0.1)

def stopRobot(robot):
    global gQuit
    gQuit = True
    robot.set_wheel(0, 0)
    robot.set_wheel(1, 0)
    robot.set_musical_note(40)
    time.sleep(0.05)
    robot.set_musical_note(0)

def alertHandle(canvas):
    canvas.create_rectangle(200, 200 , 100, 100, fill = "blue")
    
    while not gQuit:
        if not eventQueue.empty():
            if(len(gRobotList) > 0):
                for robot in gRobotList:
                    data = eventQueue.get()
                    leftFloor = data[2]
                    rightFloor = data[3]
                    if(leftFloor < 30 or rightFloor < 30):
                        stopRobot(robot)
            time.sleep(0.05)
def motionHandle():
    while not gQuit:
        if not movementQueue.empty():
            if(len(gRobotList) > 0):
                for robot in gRobotList:
                   proxInfo = movementQueue.get()
                   leftProx = proxInfo[0]
                   rightProx = proxInfo[1]
                   if (leftProx > 30 and rightProx > 30):
                        robot.set_wheel(0, 40)
                        robot.set_wheel(1, 40)
                   elif(leftProx < rightProx):
                        robot.set_wheel(0, 10)
                        robot.set_wheel(1, 50)
                   elif(leftProx > rightProx):
                    robot.set_wheel(0, 50)
                    robot.set_wheel(1, 10)
        time.sleep(0.05)

def main():
    global gMaxRobotNum # max number of robots to control
    global gRobotList
    global m

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

    m.mainloop()

    for robot in gRobotList:
        robot.reset()

    comm.stop()
    comm.join()
    sensor_display_thread.join()



# This is required by python to run the main function
if __name__== "__main__":
    main()


'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Joystick for Hamster
   By:    David Zhu
   Last Updated:  6/10/16

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import threading
import Tkinter as tk  # using Python 3
import time  # sleep
from HamsterAPI.comm_usb import RobotComm
#for PC, need to import from commm_usb

def move_up(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
            robot.set_wheel(0,30)
            robot.set_wheel(1,30)
    else:
        print "waiting for robot"

def move_down(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
          robot.set_wheel(0,-30)
          robot.set_wheel(1,-30)
    else:
        print "waiting for robot"

def move_left(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
            robot.set_wheel(0,10)
            robot.set_wheel(1,-10)
    else:
        print "waiting for robot"

def move_right(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
            robot.set_wheel(0,-10)
            robot.set_wheel(1,10)
    else:
        print "waiting for robot"

def stop_move(event=None):
    if (len(gRobotList) > 0):
        for robot in gRobotList:
            robot.set_wheel(0,0)
            robot.set_wheel(1,0)
    else:
        print "waiting for robot"

def display_sensors(canvas):
 
    leftLaserIndicator = (125, 125, 125, 125)
    rightLaserIndicator = (175, 125, 175, 125)
   
    leftFloorIndicator = (128, 128, 165 , 165)
    rightFloorIndicator = (165, 128, 182, 165)

    leftFloor = canvas.create_rectangle(leftFloorIndicator, fill = "yellow")
    rightFloor = canvas.create_rectangle(rightFloorIndicator, fill = "yellow")
   
    leftLaser = canvas.create_line(leftLaserIndicator, fill = "red")
    rightLaser = canvas.create_line(rightLaserIndicator, fill = "red")

    while not gQuit:
        if (len(gRobotList) > 0):
            robot = gRobotList[0]
            # display proximity sensors
            prox_l = robot.get_proximity(0)
            prox_r = robot.get_proximity(1)
            
            leftLaserObstruct = (125, 125, 125, prox_l)
            rightLaserObstruct = (175, 125, 175, prox_r)
            print "proximity sensors", prox_l, prox_r
            if(prox_l > 10):
                canvas.coords(leftLaser, leftLaserObstruct)
            else:
                canvas.coords(leftLaser, leftLaserIndicator)
            if(prox_r > 10):
                canvas.coords(rightLaser, rightLaserObstruct)
            else:
                canvas.coords(rightLaser, leftLaserIndicator)
        
            floor_l = robot.get_floor(0)
            floor_r = robot.get_floor(1)
            print "floor sensors", floor_l, floor_r

            if(floor_l < 50):
                canvas.itemconfig(leftFloor, fill = "green")
            else:
                canvas.itemconfig(leftFloor, fill = "yellow")
            if(floor_r < 50):
                canvas.itemconfig(rightFloor, fill = "green")   
            else:
                canvas.itemconfig(rightFloor, fill = "yellow")
        else:
            print "waiting for robot"
        time.sleep(0.1)
    print "quiting"
    m.quit()

def stopProg(event=None):
    global gQuit

    gQuit = True
    print "Exit"

def main():
    global gMaxRobotNum; # max number of robots to control
    global gRobotList
    global gQuit
    global m

    gMaxRobotNum = 1
    # thread to scan and connect to robot
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'

    gRobotList = comm.robotList

    gQuit = False 

    hamsterSize = (125, 125, 175, 175)
    mycanvas.create_rectangle(hamsterSize, fill = "blue")
    
    m = tk.Tk() #root
    mycanvas = tk.Canvas(m, bg="white", width=300, height= 300)
    mycanvas.pack()

  # start a watcher thread
    sensor_display_thread = threading.Thread(target=display_sensors, args=(mycanvas,))
    sensor_display_thread.daemon = True
    sensor_display_thread.start()

    # put code here to bind "wasd" and "x" to the robot motion function defined above 
    # bind "w" to move_up()....
    mycanvas.bind_all('<w>', move_up)
    mycanvas.bind_all('<d>', move_left)
    mycanvas.bind_all('<s>', move_down)
    mycanvas.bind_all('<a>', move_right)
    mycanvas.bind_all('<space>', stop_move)
    mycanvas.bind_all('<x>', stopProg)

    button = tk.Button(m,text="Exit")
    button.pack()
    button.bind('<Button-1>', stopProg)

    m.mainloop()

    for robot in gRobotList:
        robot.reset()

    comm.stop()
    comm.join()
    sensor_display_thread.join()


if __name__== "__main__":
    main()
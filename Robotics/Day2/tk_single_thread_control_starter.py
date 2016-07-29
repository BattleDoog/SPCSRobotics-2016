'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Joystick for Hamster
   By:            David Zhu, Qin Chen
   Last Updated:  6/10/16

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time  # sleep
import threading
import Tkinter as tk
#from HamsterAPI.comm_ble import RobotComm
from HamsterAPI.comm_usb import RobotComm

# one thread is created for motion control
class ThreadedController(object):
    def __init__(self):
        self.behavior='Pause'
        self.gQuit = False
        self.doneP = False
        t = threading.Thread(target=self.controller)
        t.daemon = True
        t.start()
        self.controller_thread = t
        return

    def controller(self):
        while not self.gQuit:
            if self.behavior == 'Bang-Bang':
                self.bang_bang_control()
            elif self.behavior == 'P-Control':
                self.p_control_1wheel()
            elif self.behavior == 'Pause':
                self.pause()       
            else:
                print 'waiting for robot...'
        print "exiting controller loop"
        return

    def Pause(self, event=None):
        self.behavior = 'Pause'

    def FollowLine(self, event=None):
        self.behavior = "Bang-Bang"    # binary control

    def FollowLineP(self, event=None):
        self.behavior = "P-Control"

    def pause(self):
        if len(gRobotList) > 0:
            for robot in gRobotList:
                robot.set_wheel(0,0)
                robot.set_wheel(1,0)
                robot.set_musical_note(0)
        time.sleep(0.1)
        return
           
    # 2 sensors used in bang-bang control
    def bang_bang_control(self):
        if len(gRobotList) > 0:                    
            for robot in gRobotList:
                floor_l = robot.get_floor(0)
                floor_r = robot.get_floor(1)
                print('sensor readings l/r %d %d', floor_l, floor_r)
                        
                if floor_r > floor_l:
                    robot.set_wheel(0, 20)
                    robot.set_wheel(1, 30)
                elif floor_r < floor_l:
                    robot.set_wheel(0, 30)
                    robot.set_wheel(1, 20)
                else:
                    robot.set_wheel(0, 30)
                    robot.set_wheel(1, 30)    
                time.sleep(0.2)        
        else:
            print "Waiting for robot"
        return
    

    ###################################################
    # 1 sensor used. Left wheel on edge of the track. 
    ###################################################
    def p_control_1wheel(self):
        
        if len(gRobotList) > 0:
            for robot in gRobotList:
                leftFloor = robot.get_floor(0)
                rightFloor = robot.get_floor(1)
                errorOne = (150 - rightFloor) / 2
                errorTwo = (150 - leftFloor) / 2
                if(rightFloor < leftFloor - 10):
                    robot.set_wheel(0, errorOne + 10)
                    robot.set_wheel(1, 0)
                elif(leftFloor < rightFloor - 10):
                    robot.set_wheel(0, 0)
                    robot.set_wheel(1, errorTwo + 10)
                else:
                    robot.set_wheel(0, errorOne)
                    robot.set_wheel(1, errorTwo)
                
                print (leftFloor, rightFloor)
                time.sleep(0.01)
        return

class GUI(object):
    def __init__(self, root, behaviors):
        self.root = root
        self.behaviors = behaviors
        self.initUI()

    def initUI(self):
        frame = self.root
        frame.geometry('300x200')
  
        button1 = tk.Button(frame,text="Bang-Bang")
        button1.pack(side='left')
        button1.bind('<Button-1>', self.behaviors.FollowLine)

        button0 = tk.Button(frame,text="P-control")
        button0.pack(side='left')
        button0.bind('<Button-1>', self.behaviors.FollowLineP)

        button5 = tk.Button(frame,text="Exit")
        button5.pack(side='left')
        button5.bind('<Button-1>', self.stopProg)

    def stopProg(self, event=None):
        self.behaviors.gQuit = True
        self.behaviors.doneP = True
        for robot in gRobotList:
            robot.reset()
        self.behaviors.controller_thread.join()
        self.root.quit()
        return

gMaxRobotNum = 1
gRobotList = []
def main(argv=None):
    # instantiate COMM object
    global gRobotList

    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'  
    gRobotList = comm.robotList

    behaviors = ThreadedController()
    
    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()

    print("terminated!")

if __name__ == "__main__":
    sys.exit(main())
'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Joystick for Hamster
   By:            David Zhu, Qin Chen
   Last Updated:  6/10/16

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
# This is a utility program. The purpose of this program is to help students understand hamster APIs.
#
import time
import threading
import Tkinter as tk
#from HamsterAPI.comm_ble import RobotComm
from HamsterAPI.comm_usb import RobotComm

gMaxRobotNum = 1
done = False

def robotAPIs():
	global done
	while not done:
		if len(gRobotList) > 0:
			robot = gRobotList[0]
			#############################################
			# APIs such as set_wheel(), get_proximity() #
			#############################################
			robot.set_wheel(0, 100)
			robot.set_wheel(1, 100)
			p_l=robot.get_proximity(0)
			p_r=robot.get_proximity(1)
			print 'proximity readings are:', p_l, p_r
			time.sleep(0.01)	
	return

class GUI(object):
	def __init__(self, root):
		self.root = root
		root.geometry('200x100')
		b = tk.Button(root, text='Exit')
		b.pack()
		b.bind('<Button-1>', self.stopProg)
	
	def stopProg(self, event=None):
		global done
		done = True
		for robot in gRobotList:
			robot.reset()
		self.root.quit() 	# close window
		return


# low level communication with hamster
comm = RobotComm(gMaxRobotNum)
comm.start()
print 'Bluetooth starts'
gRobotList = comm.robotList

# command to hamster 
t_handle = threading.Thread(target=robotAPIs)
t_handle.start()

m = tk.Tk() # gui root
GUI(m)
m.mainloop()

comm.stop()	# 
comm.join()	# wait for comm to finish


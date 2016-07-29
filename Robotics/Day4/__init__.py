Lab4 - multiple threads, event-driven programming:
- Warm up: Modify the simple_threads.py program so that one thread will put strings into a queue periodically,
  and the other thread will read from the queue and print the strings. Check off with TA.

- Students implement 'hamster escape'. 
The implementation uses:
	. 3 threads. One for each of these purposes: motion handler, event watcher, 
	  and alert handler. Alert handler displays proximity sensors.
	. 2 event queues. event watcher thread puts event in the queues while alert and motion handlers get
	  events and take appropriate actions.

	'Escape' includes these functionalities: 
	. GUI window shows a square representing hamster. One button to start hamster escape and one for exit program.
	. Display line segment when proximity sensors 'see' obstacle.
	. Acknowledge (sound) when border is reached.
	. Hamster avoids obstacle when it detects any.

No starter code is provided today. The following is pseudocode:

'''

PSEUDOCODE

'''

# import statements


# global variables/define all required queues

# These are used for connecting to the robot
gMaxRobotNum = 1; # max number of robots to control
gRobotList = None

def watcher:
	This thread will read sensor data and put sensor data into queues
	IMPORTANT! This is the only thread that should directly read robot sensors

# Needs access to Canvas, pass from main function
def alert_handler:
	This thread will read information from the queue and update the gui accordingly, and also handle events
    such as reaching the border

def motion_handler:
	This thread will read information from the queue and update robot movement accordingly

'''
The main function is not pseudocode, and includes the minimum setup for the GUI/hamster connection
'''
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

    '''

    Set up threads here

    '''

    m.mainloop()

    for robot in gRobotList:
        robot.reset()

    comm.stop()
    comm.join()
    sensor_display_thread.join()



# This is required by python to run the main function
if __name__== "__main__":
    main()


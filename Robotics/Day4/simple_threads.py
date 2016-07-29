import time
import Queue
from threading import Thread

myQueue = Queue.Queue()

# Modify this function to put a string into myQueue periodically
def worker1():
    for i in range(10):
       	myQueue.put("cat")
        time.sleep(2)

# Modify this function to read from myQueue and print the strings
def worker2():
    for i in range(20):
        if not myQueue.empty():
    		print myQueue.get()
        time.sleep(1)

t1 = Thread(name='thread1', target=worker1)
t1.daemon = True # Setting this to True will terminate the thread when the main program exits
t1.start()

t2 = Thread(name='thread2', target=worker2)
t2.daemon = False
t2.start()


'''

IMPORTANT CONSIDERATIONS

When reading from the queue, you should always check if the queue is not empty before continuing.
	Attempting to read from the queue when it is empty can cause the program to hang.
	Example:
		if not myQueue.empty():
			x = myQueue.get()

Always make sure that you read from the queue faster than you put information into the queue.
	Not doing so can cause the queue to fill up, causing high latency

How to pass parameters to threads:
	myThread = Thread(name='myThread', target=myFunction, args=(arg1, arg2,))

'''
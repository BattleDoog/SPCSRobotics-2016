# Robot Programming
# graph display

import sys
import pdb
import Queue
import Tkinter as tk
import time
from threading import Thread
from HamsterAPI.comm_usb import RobotComm
import PID

noPath = False
global currentNode
class GraphDisplay(object):
	def __init__(self, graph, nodes_location, obstacles, start_node=None, goal_node=None, frame = None, canvas = None):
		self.node_dist = 60
		self.node_size = 20
		self.canvas = canvas
		self.graph = graph
		self.nodes_location = nodes_location
		self.start_node = start_node
		self.goal_node = goal_node
		self.obstacles = obstacles
		self.frame = frame
		#self.dist = {}
		#return

	def display_graph(self, cDir):
		for node in self.nodes_location:
			#get list of names of connected nodes
			connected_nodes = self.graph[node[0]]
			# find location for each connected node and draw edge
			if connected_nodes:
				for connected_node in connected_nodes:
					# step into node locations
					for a_node in self.nodes_location:
						if connected_node == a_node[0]:
							self.draw_edge(node, a_node,'black')

			if node[0] == self.start_node:
				self.draw_node(node, 'red')
			elif node[0] == self.goal_node:
				self.draw_node(node, 'green')
			else:
				self.draw_node(node, 'blue')

		#BFS(self, cDir)
		#print pathL
		t1 = Thread(name='BFSThread', target=BFS, args = (self, cDir))
		t1.daemon = True # Setting this to True will terminate the thread when the main program exits
		t1.start()

		print"display_graph"
		self.frame.mainloop()
		return
	
	# takes in node_location for node
	def draw_node(self, node, n_color):
		#print "node" +str(node)
		node_name = node[0]
		x = node[1][0]
		y = node[1][1]
		dist = self.node_dist
		size = self.node_size
		self.canvas.create_oval(x*dist-size, y*dist-size, x*dist+size, y*dist+size, fill=n_color)
		self.canvas.create_text(x*dist, y*dist,fill="white",text=node[0])
		return

	def draw_edge(self, node1, node2, e_color):
		x1 = node1[1][0]
		y1 = node1[1][1]
		x2 = node2[1][0]
		y2 = node2[1][1]
		dist = self.node_dist
		self.canvas.create_line(x1*dist, y1*dist, x2*dist, y2*dist, fill=e_color)
		#create dictionary for distances between nodes
		#node1 ('A', [2,1])
		self.dist = {sc(node1[0],node2[0]): 1}
		return

##############
# Data types used in this implementation: dictionary, set, list.
##############

	'''uses Breadth First Search to find shortest path
	returns a list of nodes in path'''
def BFS(displayGraph, direct):
	global noPath
	global currentNode
	noPath = False
	dg = displayGraph
	print "BFS"
	visited = set()
	q = [(dg.start_node, [dg.start_node])] #current node and path to this node
	#print self.dist
	#print self.obstacles
	while q:
		(node, path) = q.pop(0)
		#node ('nodename',[x,y])
		if node not in visited:
			for next in dg.graph[node]-visited :
				if next not in obs: #check if node is not an obstacle
					if next == dg.goal_node:
						#print path + [next]

						for t in path: #draws the path
							if t != dg.start_node:
								xy = t.split(',') #parses string to get x,y
								nl = (t, [int(xy[0]), int(xy[1])]) #creates node tuple ('name',[x,y])
								dg.draw_node(nl, 'purple')
						pathL = path + [next]
						print pathL
						moveBot(pathL, dg, dg.canvas, dg.frame, direct)
						print "after movebot()"
						# t1 = Thread(name='BFSThread', target=BFS)
						# t1.daemon = True # Setting this to True will terminate the thread when the main program exits
						# t1.start()
						return
					else :
						xy = next.split(',') #parses string to get x,y
						nl = (str(next), [int(xy[0]), int(xy[1])]) #creates node tuple ('name',[x,y])
						dg.draw_node(nl, 'cyan')

						q.append((next, path + [next]))
						#print path
						time.sleep(0.02)

				visited.add(node)
	fricked = True
	if fricked == True:
		obs.clear() #delete all obstacles
		print obs
		print "noPath"
		Ng, Nnl = constructGraph(gridWidth, gridLength, obs)
		ndisplay=GraphDisplay(Ng, Nnl, obs, currentNode, dg.goal_node, dg.frame, dg.canvas)
		ndisplay.display_graph(direct)


def moveBot(path, dg, canvas, fr, dir):
	print "movebot"
	quit = False
	global obs
	j = False
	i = 0
	cDir = dir #0 north, 1 is east, 2 is south, 3 is west
	print path

	while not quit:
		#print "loop"
		if (len(gRobotList) > 0):
			for robot in gRobotList:
				print i
				cNode = path[i]
				if not i == len(path)-1:
					nNode = path[i+1]

				xy = cNode.split(',')
				cx = int(xy[0])
				cy = int(xy[1])

				xy2 = nNode.split(',')
				nx = int(xy2[0])
				ny = int(xy2[1])
				print (cx, cy)
				print (nx, ny)

				while not j:
					#print "not junction"
					floor_l = robot.get_floor(0)
					floor_r = robot.get_floor(1)
					prox_l = robot.get_proximity(0)
					prox_r = robot.get_proximity(1)
					#print (floor_l, floor_r, prox_l, prox_r)
					time.sleep(0.01)
					adjust = PID.PID_controller(0.25, 0.1, 0.1, floor_l, floor_r)

					robot.set_wheel(0,20 + int(adjust +0.5))
					robot.set_wheel(1,20 - int(adjust +0.5))  							

					if junction():
						print "junction"
						robot.set_musical_note(40)
						time.sleep(0.05)
						stopMove()
						i +=1
						if i == len(path):
							robot.set_musical_note(50)
							time.sleep(0.5)
							robot.set_musical_note(0)
							print "final node"
							stopMove()
							return
						j = True

					if prox_l > 70 and prox_r > 70:
						print "obstacle ahead"
						stopMove()
						robot.set_wheel(0, 30)
						robot.set_wheel(1, -30)
						time.sleep(1.0)
						robot.set_wheel(0, -30)
						robot.set_wheel(1, -30)
						time.sleep(1.0)
						stopMove()
						obs.add(sc(cx,cy))
						print obs
						cDir = cDir +1
						print str(cDir) + "cdir"
						canvas.delete('all')
						start = path[i-1]
						global currentNode
						currentNode = start
						print start
						#if noPath == False:
						Ng, Nnl = constructGraph(gridWidth, gridLength, obs)
						ndisplay=GraphDisplay(Ng, Nnl, obs, start, dg.goal_node, fr, canvas)
						ndisplay.display_graph(cDir)
						# else :
						# 	del obs[:] #delete all obstacles
						# 	print "noPath"
						#BFS(ndisplay, cDir)
						return

				robot.set_wheel(0,30)
				robot.set_wheel(1,30)
				time.sleep(0.5)
				robot.set_musical_note(0)
				if cDir == 1: #east
					if cy == ny and cx < nx : #next node is east
						print "east to east"
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)
						time.sleep(0.5)
						cDir = 1
					elif cx == nx and cy < ny :#next node is south
						print "east to south"
						robot.set_wheel(0, 30)
						robot.set_wheel(1, -30)
						time.sleep(1.0)
						cDir = 2
					elif cx == nx and cy > ny : #next node is north
						print "east to north"
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 30)
						time.sleep(1.0)
						cDir = 0
					else : #next node is west
						print "east to west"
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 30)
						time.sleep(2.0)
						cDir = 3
					#i += 1
					j = False

				elif cDir == 0 : #north
					if cy == ny and cx < nx : #next node is east
						print "north to east"
						robot.set_wheel(0, 30)
						robot.set_wheel(1, -30)
						time.sleep(1.0)
						cDir = 1
					elif cx == nx and cy < ny :#next node is south
						print "north to south"
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 30)
						time.sleep(2.0)
						cDir = 2
					elif cx == nx and cy > ny : #next node is north
						print "north to north"
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)
						time.sleep(0.5)
						cDir = 0
					else : #next node is west
						print "north to west"
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 30)
						time.sleep(1.0)
						cDir = 3
					#i += 1
					j = False
				elif cDir == 2: #south
					if cy == ny and cx < nx : #next node is east
						print "south to east"
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 30)
						time.sleep(1.0)
						cDir = 1
					elif cx == nx and cy < ny :#next node is south
						print "south to south"
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)
						time.sleep(0.5)
						cDir = 2
					elif cx == nx and cy > ny : #next node is north
						print "south to north"
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 30)
						time.sleep(2.0)
						cDir = 0
					else : #next node is west
						print "south to west"
						robot.set_wheel(0, 30)
						robot.set_wheel(1, -30)
						time.sleep(1.0)
						cDir = 3
					#i += 1
					j = False
				elif cDir == 3: #west
					if cy == ny and cx < nx : #next node is east
						print "west to east"
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 30)
						time.sleep(2.0)
						cDir = 1
					elif cx == nx and cy < ny :#next node is south
						print "west to south"
						robot.set_wheel(0, -30)
						robot.set_wheel(1, 30)
						time.sleep(1.0)
						cDir = 2
					elif cx == nx and cy > ny : #next node is north
						print "west to north"
						robot.set_wheel(0, 30)
						robot.set_wheel(1, -30)
						time.sleep(1.0)
						cDir = 0
					else : #next node is west
						print "west to east"
						robot.set_wheel(0, 30)
						robot.set_wheel(1, 30)
						time.sleep(0.5)
						cDir = 3
					#i += 1
					j = False
				else:
					return
# graph = {'A': set(['D', 'C', 'F', 'B']),
#         'B': set(['A', 'E']),
#         'C': set(['A']),
#         'D': set(['A','F']),
#         'E': set(['B','F','G']),
#         'F': set(['A','D','E']),
#         'G': set(['E'])}
	
# nodes_location = [('A', [2,1]),
#                 ('C', [1,2]),
#                 ('B', [4,1]),
#                 ('D', [3,2]),
#                 ('F', [2,3]),
#                 ('E', [5,2]),
#                 ('G', [4,3])]
	

'''return string literal 'x,y' '''
def sc(x,y):
	return str(x) +","+str(y)

def stopMove():
	if (len(gRobotList) > 0):
		for robot in gRobotList:
			robot.set_wheel(0, 0)
			robot.set_wheel(1, 0)

def junction():
	if (len(gRobotList) > 0):
		for robot in gRobotList:
			floor_l = robot.get_floor(0)
			floor_r = robot.get_floor(1)
			if floor_l < 30 and floor_r < 30 :
				#robot.set_musical_note(40)
				#print "junction"
				return True
			else :
				#robot.set_musical_note(0)
				return False

def constructGraph(gridWidth, gridLength, obstacles):
	nodes_location = []
	graph = {}
	for x in range(1, gridWidth+1):
		for y in range(1, gridLength+1):
			#print sc(x,y)

			l = (sc(x,y), [x,y])
			nodes_location.append(l)

			#corner node case
			if x == 1 and y == 1: #top left
				graph[sc(x,y)] = set([sc(x+1,y), sc(x,y+1)])
			elif x == gridWidth and y == 1: #top right
				graph[sc(x,y)] = set([sc(x-1,y), sc(x,y+1)])
			elif x == gridWidth and y == gridLength: #bottom right
				graph[sc(x,y)] = set([sc(x,y-1), sc(x-1,y)])
			elif x == 1 and y == gridLength: #bottom left
				graph[sc(x,y)] = set([sc(x,y-1), sc(x+1,y)])

			#center node case
			elif x > 1 and y > 1 and x < gridWidth and y < gridLength:
				graph[sc(x,y)] = set([sc(x,y-1), sc(x+1,y), sc(x,y+1), sc(x-1,y)])

			#edge node case
			elif x == 1 and y > 1 and y < gridLength: #left edge
				graph[sc(x,y)] = set([sc(x,y-1), sc(x,y+1), sc(x+1,y)])
			elif y == 1 and x > 1 and x < gridWidth: #top edge
				graph[sc(x,y)] = set([sc(x+1,y), sc(x-1,y), sc(x,y+1)])
			elif x == gridWidth and y > 1 and y < gridLength: #right edge
				graph[sc(x,y)] = set([sc(x-1,y), sc(x,y+1), sc(x,y-1)])
			elif y == gridLength and x > 1 and x < gridWidth : #bottom edge
				graph[sc(x,y)] = set([sc(x+1,y), sc(x,y-1), sc(x-1,y)])

			if sc(x,y) in obstacles :
				#print "obs " + sc(x,y)
				nodes_location.remove( (sc(x,y), [x,y]) )
				del graph[sc(x,y)]

	return (graph, nodes_location)

def main(argv=None) :
	#begin robot navigation
	global gMaxRobotNum; # max number of robots to control
	global gRobotList
	global gQuit

	gMaxRobotNum = 1
	# thread to scan and connect to robot
	comm = RobotComm(gMaxRobotNum)
	comm.start()
	print 'Bluetooth starts'
	gRobotList = comm.robotList
	gQuit = False

	#grid setup
	global gridWidth
	global gridLength
	gridWidth = input("gridWidth: ")
	gridLength = input("gridLength: ")

	#obs = input("obstacles ex.['3,3']: ")
	# print obs
	global obs #need
	obs = set() #obstacle coordinates
	print "obstacles: "+str(obs)

	graph, nodes_location = constructGraph(gridWidth, gridLength, obs)
	# print graph
	# print nodes_location
	
	start = raw_input("start node: ")
	goal = raw_input("goal node: ")
	#display.BFS()

	frame = tk.Tk()
	canvas = tk.Canvas(frame, bg="white", width=1000, height=1000)
	canvas.pack(expand=1, fill='both')

	display=GraphDisplay(graph, nodes_location, obs, start, goal,frame, canvas)
	display.display_graph(1)
	print "in main"
	#moveBot()

	exit = raw_input("exit: (y)" )
	if exit is 'y':
		print "exiting"
		gQuit = True
		frame.quit()


	comm.join()
	comm.stop()

if __name__ == "__main__":
	main()
	# t2 = Thread(name='MainThread', target=main)
	# t2.daemon = True # Setting this to True will terminate the thread when the main program exits
	# t2.start()
	
	
	





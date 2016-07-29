import Tkinter as tk
import sys
import time
import Queue
import math
import threading
from HamsterAPI.comm_usb import RobotComm

class GraphDisplay(object):
	def __init__(self, graph, nodes_location, obstacles, start_node=None, goal_node=None, root=None):
		self.node_dist = 60
		self.node_size = 20
		self.canvas = None
		self.graph = graph
		self.nodes_location = nodes_location
		self.start_node = start_node
		self.goal_node = goal_node
		self.display_graph(root)
		self.obstacles = obstacles
		#self.dist = {}
		return

	def display_graph(self, frame):
		
		self.canvas = tk.Canvas(frame, bg="white", width=1000, height=1000)
		self.canvas.pack(expand=1, fill='both')
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

		self.BFS()
		#print pathL
		# t1 = Thread(name='BFSThread', target=self.BFS)
		# t1.daemon = True # Setting this to True will terminate the thread when the main program exits
		# t1.start()
		#frame.mainloop()
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
	def BFS(self):
		print "BFS"
		visited = set()
		q = [(self.start_node, [self.start_node])] #current node and path to this node
		#print self.dist
		#print self.obstacles
		while q:
			(node, path) = q.pop(0)
			#node ('nodename',[x,y])
			if node not in visited:
				for next in self.graph[node]-visited :
					if next not in obs: #check if node is not an obstacle
						if next == self.goal_node:
							#print path + [next]

							for t in path: #draws the path
								if t != self.start_node:
									xy = t.split(',') #parses string to get x,y
									nl = (t, [int(xy[0]), int(xy[1])]) #creates node tuple ('name',[x,y])
									self.draw_node(nl, 'purple')
							global pathL
							pathL = path + [next]
							# print pathL
							return path + [next]
						else :
							xy = next.split(',') #parses string to get x,y
							nl = (str(next), [int(xy[0]), int(xy[1])]) #creates node tuple ('name',[x,y])
							self.draw_node(nl, 'cyan')

							q.append((next, path + [next]))
							#print path
							time.sleep(0.02)

					visited.add(node)	


					
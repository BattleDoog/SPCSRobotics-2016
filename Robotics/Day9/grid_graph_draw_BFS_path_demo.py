import Queue
import Tkinter as tk
import time

class Node:
    def __init__(self):
      self.name = ''
      self.data =[]
      #self.f_cost = 0
      #self.h_cost = 0
      self.back_pointer = False
      self.closed = False
      self.edges = []

class Graph:
    def __init__(self, canvas):
        self.nodes = {}
        self.startNode = None
        self.goalNode = None
        self.path = []
        #self.path_cost = False
        self.queue = Queue.Queue()
        #self.lifo_queue = Queue.LifoQueue()
        #self.priority_queue = Queue.PriorityQueue()
        self.canvas = canvas
        self.node_dist = 60
        self.node_size = 20

    def draw_node(self, a_node, n_color):
        if a_node.data: # coordinate to draw
          x = a_node.data[0]+1
          y = a_node.data[1]+1
          canvas = self.canvas
          dist = self.node_dist
          size = self.node_size
          canvas.create_oval(x*dist-size, y*dist-size, x*dist+size, y*dist+size, fill=n_color)
          canvas.create_text(x*dist, y*dist,fill="white",text=a_node.name)

    def draw_edge(self, node1, node2, e_color):
      if (node1.data and node2.data):
          x1 = node1.data[0]+1
          y1 = node1.data[1]+1
          x2 = node2.data[0]+1
          y2 = node2.data[1]+1
          dist = self.node_dist
          canvas = self.canvas
          canvas.create_line(x1*dist, y1*dist, x2*dist, y2*dist, fill=e_color)

    def add_node(self, name, data):
        a_node = Node()
        a_node.name = name
        a_node.data = data
        self.nodes[name] = a_node
        self.draw_node(a_node, "blue")
        return a_node

    def set_start(self, name):
        self.startNode = name
        self.draw_node(self.nodes[name], "red")
        #self.nodes[name].f_cost = 0
        self.queue.put(self.nodes[name])

    def set_goal(self, name):
        self.goalNode = name
        self.draw_node(self.nodes[name], "green")

    def add_edge(self, node1, node2, g_cost):
        self.nodes[node1].edges.append([node2, g_cost])
        self.nodes[node2].edges.append([node1, g_cost])
        self.draw_edge(self.nodes[node1], self.nodes[node2], "blue")

    def BFS(self): # Breadth First Search
      print "Breadth First Search"
      while not self.queue.empty():
        current_node = self.queue.get()
        if (current_node.closed != True):
          print "expand current node: ", current_node.name
          print "edges from node: ",current_node.edges
          for an_edge in current_node.edges:
            a_node_name = an_edge[0]
            if not self.nodes[a_node_name].closed: #has been "expanded"
              self.queue.put(self.nodes[a_node_name])
              print "put queue: ", a_node_name
              self.nodes[a_node_name].back_pointer = current_node

              # check if path to goal is found, if so, extract path
              if a_node_name == self.goalNode:
                print "found path to ", a_node_name
                path = [a_node_name]
                #path_cost = 0
                path_node = self.nodes[a_node_name]
                while path_node.back_pointer != False:
                  self.draw_edge(path_node, path_node.back_pointer, "red")
                  path_node = path_node.back_pointer
                  path.append(path_node.name)

                if not self.path:
                  self.path = path
                  self.path.reverse()
                  print "path: ", self.path
            else:
              print "node closed: ", a_node_name
        current_node.closed = True

def make_grid (a_graph, m, n, obs_list):
  for i in range (0,m):
    for j in range (0, n):
      node_free = True
      for obs in obs_list:
        if i == obs[0] and j == obs[1]:
          node_free = False
          #print "obs node", obs
      if node_free:
        node_name = str(i)+"-"+str(j)
        a_node = a_graph.add_node(node_name, [i,n-j])
        #a_node.data = [i,j]
        #print "created a node", a_node.name, a_node.data

def connect_nodes(a_graph, m, n):
  #print "connecting nodes"
  for i in range (0,m):
    for j in range (0, n):
      node_name = str(i)+"-"+str(j)
      if (a_graph.nodes.has_key(node_name a_node = a_graph.nodes[node_name]):
        #print a_node.name, "connecting to"
        if (i > 0):
          b_node_name = str(i-1)+"-"+str(j)
          if (a_graph.nodes.has_key(b_node_name)):
            b_node = a_graph.nodes[b_node_name]
            #print b_node.name
            a_graph.add_edge(node_name, b_node_name, 1)
        if (i < m):
          b_node_name = str(i+1)+"-"+str(j)
          if (a_graph.nodes.has_key(b_node_name)):
            b_node = a_graph.nodes[b_node_name]
            #print b_node.name
            a_graph.add_edge(node_name, b_node_name, 1)
        if (j > 0):
          b_node_name = str(i)+"-"+str(j-1)
          if (a_graph.nodes.has_key(b_node_name)):
            b_node = a_graph.nodes[b_node_name]
            #print b_node.name
            a_graph.add_edge(node_name, b_node_name, 1)
        if (j < n):
          b_node_name = str(i)+"-"+str(j+1)
          if (a_graph.nodes.has_key(b_node_name)):
            b_node = a_graph.nodes[b_node_name]
            #print b_node.name
            a_graph.add_edge(node_name, b_node_name, 1)

def main():

    frame = tk.Tk()

    canvas = tk.Canvas(frame, bg="white", width=400, height=400)
    canvas.pack(expand=1, fill='both')

    print "created graph"
    MyGraph = Graph(canvas)
    obs_list = ([1,1], [3,0], [3,2],[2,3])
    make_grid(MyGraph, 5, 4, obs_list)
    connect_nodes(MyGraph, 5, 4)

    MyGraph.set_start("0-0")
    MyGraph.set_goal("4-2")

    MyGraph.BFS()

    frame.mainloop()


if __name__ == "__main__":
    main()
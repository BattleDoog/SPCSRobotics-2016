# Robot Programming
# graph display
# by Dr. Qin Chen
# May, 2016

import sys
import pdb
import Queue
import Tkinter as tk

class GraphDisplay(object):
    def __init__(self, graph, nodes_location, start_node=None, goal_node=None):
        self.node_dist = 60
        self.node_size = 20
        self.canvas = None
        self.graph = graph
        self.nodes_location = nodes_location
        self.start_node = start_node
        self.goal_node = goal_node
        self.display_graph()
        return

    def display_graph(self):
        frame = tk.Tk()
        self.canvas = tk.Canvas(frame, bg="white", width=400, height=300)
        self.canvas.pack(expand=1, fill='both')
        for node in self.nodes_location:
            if node[0] == self.start_node:
                self.draw_node(node, 'red')
            elif node[0] == self.goal_node:
                self.draw_node(node, 'green')
            else:
                self.draw_node(node, 'blue')
            # get list of names of connected nodes
            connected_nodes = self.graph[node[0]]
            # find location for each connected node and draw edge
            if connected_nodes:
                for connected_node in connected_nodes:
                    # step into node locations
                    for a_node in nodes_location:
                        if connected_node == a_node[0]:
                            self.draw_edge(node, a_node,'blue')

        shortest = next(self.bfs_paths(self.graph, self.start_node, self.goal_node))

        frame.mainloop()
        return
    
    def draw_node(self, node, n_color):
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
          return

    def bfs(graph, start):
        visited, queue = set(), [start]
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                queue.extend(graph[vertex] - visited)
        return visited

    def bfs_paths(graph, start, goal):
        queue = [(start, [start])]
        while queue:
            (vertex, path) = queue.pop(0)
            for next in graph[vertex] - set(path):
                if next == goal:
                    yield path + [next]
                else:
                    queue.append((next, path + [next]))


##############
# Data types used in this implementation: dictionary, set, list.
##############



nodeQueue = Queue.Queue()


graph = {'A': set(['B', 'C', 'D', 'F']),
       'B': set(['A', 'E']),
       'C': set(['A']),
       'D': set(['A', 'F']),
       'E': set(['B', 'F', 'G']),
       'F': set(['A', 'D', 'E']),
       'G': set(['E'])}
       
nodes_location = [('A', [2,1]),
                ('B', [4,1]),
                ('C', [1,2]),
                ('D', [3,2]),
                ('E', [5,2]),
                ('F', [2,3]),
                ('G', [4,3])]

display = GraphDisplay(graph, nodes_location, 'A', 'G')
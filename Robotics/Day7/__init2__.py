Lab7 - Graph and graph search(BFS, DFS)

 
Starter programs:
. session2_graph_starter.py displays a graph. The node locations on screen(on a grid setting) have to be given to the program. There
is no edge cost associated with each edge.


Assignments of this Lab:

IMPLEMENT graphs, BFS
. Understand the starter file and the included graphics class. Implement a graphical BFS.

GRID GRAPH and SEARCH
. Use session2_graph_starter.py program. Manually populate graph(nodes and edges) using grid data given
 by TA in the lab. Name nodes to reflect node location on the grid.

. Write a program which takes input of dimension of a grid and location of obstacles on the grid. This program
  generates a graph object with the given grid info. (optional) 

ADDITIONAL SEARCH
.Implement DFS (optional)

GRID NAVIGATION (optional)
.Think about how to translate search result(a sequence of nodes/intersections, (0-0),(0-1),...) to a sequence of
 commands(forward, turn left, turn right,...) to guide hamster in grid navigation.
 Implement this translation by a program. (optional)

UNFINISHED PROJECTS:
. Hamster trash cleaning
. Implementation of collision checking



Minimum requirements for grid navigation(to be finished by end of Week 2):
1. generate graph from given grid dimension and obstacle locations
2. search graph and find a path from any given start and goal
3. have hamster execute plan on grid

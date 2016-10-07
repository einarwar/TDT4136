import matplotlib.pyplot as plt
import numpy as np
import sys

#Function that imports a textfile and finds dimensions
def get_content_from_file(filename):
    content =  np.genfromtxt(filename, dtype='str', comments='@')
    rows = len(content)
    cols = len(content[0])
    return content, rows, cols

#Nodeclass with properties
class Node:
    def __init__(self, x, y, cost, terrain):
        self.parent = None
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.cost = cost
        self.terrain = terrain
        
#Makes list of nodes from the textfile import        
def generate_list_of_nodes(board):
    nodes = []
    for (i, row) in enumerate(board):
        for (j, node) in enumerate(row):
            if node == 'w':
                cost = 100
                terrain = 'Water'
            elif node == 'm':
                cost = 50
                terrain = 'Mountains'
            elif node == 'f':
                cost = 10
                terrain = 'Forest'
            elif node == 'g':
                cost = 5
                terrain = 'Grasslands'
            elif node == 'r':
                cost = 1
                terrain = 'Roads'
            n = Node(i,j, cost, terrain)
            nodes.append(n)                
    return nodes

#Algorithm class
class Astar:
    def __init__(self, board, rows, cols, start_loc, end_loc, filename):
        self.open = []
        self.closed = set()
        self.nodes = generate_list_of_nodes(board)
        self.start = Node(start_loc[0], start_loc[1], cost=0, terrain='Start')
        self.end = Node(end_loc[0], end_loc[1], cost=0, terrain='End' )
        self.rows = rows
        self.cols = cols
        self.filename = filename
        
    #Calculates manhattan distance from node to end (h-cost)
    def calc_h(self, node):
        return np.abs(node.x - self.end.x) + np.abs(node.y - self.end.y)
    
    #Returns a node based on x,y position
    def get_node(self, x, y):
        return self.nodes[x * self.cols + y] #2d indexing of 1d array
        
    #Gets the adjacent nodes. Need to check that we dont go out of the grid        
    def get_adjacent_nodes(self, node):
        
        nodes = []
        #Up
        if node.y < (self.cols - 1):
            nodes.append(self.get_node(node.x, node.y+1))
        #Down
        if node.y > 0:
            nodes.append(self.get_node(node.x, node.y-1))
        #left
        if node.x > 0:
            nodes.append(self.get_node(node.x-1, node.y))
        #Right
        if node.x < (self.rows - 1):
            nodes.append(self.get_node(node.x+1, node.y))
        return nodes
   
    #Updates the costs and parent of an adjancent node 
    def update_node(self, adj, node):
        adj.g = (node.g + adj.cost) #Change from task 1
        adj.h = self.calc_h(adj)
        adj.parent = node
        adj.f = adj.g + adj.h
        
    #Function that gets the path by seeing who is whos parent, starting with the end
    def get_path(self):
        path_nodes = []
        node = self.end
        total_cost = node.cost
        while node.parent is not self.start:
            node = node.parent
            total_cost += node.cost
            path_nodes.append((node.x, node.y))
        return path_nodes, total_cost

    #Smooth plot function to show board, colors are kinda bad tho
    def numpy_imshow_solved(self, path_nodes):
        i = 0
        j = 0
        board = np.zeros((self.rows, self.cols))
        for node in self.nodes:
            board[i,j] = node.cost

            j += 1
            if j == self.cols:
                i += 1
                j = 0
        #Colors the tiles, and adds a dotted path-line from start to end
        plt.scatter([i[1] for i in path_nodes], [i[0] for i in path_nodes], color='red', s=40)
        plt.scatter([self.start.y, self.end.y], [self.start.x, self.end.x], color='green', s=40)
        plt.imshow(board, interpolation='nearest')
        plt.title(self.filename)
        plt.colorbar()
        plt.show()

    #Mostly same as task 1
    def go(self):
        self.open.append((self.start.f, self.start))
        while len(self.open):
            self.open.sort(reverse=True)
            _, current = self.open.pop()

            self.closed.add(current)
            if (current.x,current.y) == (self.end.x, self.end.y):
                self.end.parent = current
                
                best_path, total_cost = self.get_path()
                self.numpy_imshow_solved(best_path)
                print 'Found a path with cost {}'.format(total_cost)
                break
            
            adj_nodes = self.get_adjacent_nodes(current)
            for adj_node in adj_nodes:
                if adj_node not in self.closed:
                    if (adj_node.f, adj_node) in self.open:
                        if adj_node.g > current.g + adj_node.cost: #Changed in task 2
                            self.update_node(adj_node, current)
                    else:
                        self.update_node(adj_node, current)
                        self.open.append((adj_node.f, adj_node))

def shortest_path(filename):
    content, rows, cols = get_content_from_file(filename)
    astar = Astar(content, rows, cols, (2,13), (6,12), filename = filename)
    astar.go()
 
if __name__ == '__main__':
    filename = sys.argv[1]
    shortest_path(filename)

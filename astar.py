import matplotlib.pyplot as plt
import numpy as np
import sys, os, time

def get_content_from_file(filename):
    content =  np.genfromtxt(filename, dtype='str', comments='@')
    rows = len(content)
    cols = len(content[0])
    return content, rows, cols
class Node:
    def __init__(self, x, y, isWall):
        self.isWall=isWall
        self.parent = None
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        
def generate_list_of_nodes(board):
    nodes = []
    n0 = None
    for (i, row) in enumerate(board):
        for (j, cell) in enumerate(row):
            isWall = False
            if cell == '#':
                isWall = True
            n = Node(i,j, isWall)
            if cell == 'A':
                start = Node(i,j, isWall=False)
            if cell == 'B':
                end = Node(i,j, isWall=False)
            nodes.append(n)
    return nodes, start, end

class Astar:
    def __init__(self, board, rows, cols):
        self.open = []
        self.closed = set()
        (self.nodes, self.start, self.end) = generate_list_of_nodes(board)
        self.rows = rows
        self.cols = cols

    def calc_costs(self, node):
        return 10 * np.abs(node.x - self.end.x) + np.abs(node.y - self.end.y)

    def get_node(self, x, y):
        return self.nodes[x * self.cols + y] #2d indexing of 1d array
        
            
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

    def update_node(self, adj, node):
        adj.g = node.g + 10
        adj.h = self.calc_costs(adj)
        adj.parent = node
        adj.f = adj.g + adj.h

    def print_board(self, current_loc, foundpath=False):
        sys.stdout.flush()
        line = '\r'
        i = 0
        for node in self.nodes:
            if node.isWall:
                line += '#'
            elif  (node.x, node.y) == (current_loc.x, current_loc.y):
                line += 'X'
            else:
                line += '-'
            i += 1
            if i == 20:
                i = 0
                line += '\n'
        sys.stdout.write('{}'.format(line))

    def get_path(self):
        path_nodes = []
        node = self.end
        while node.parent is not self.start:
            path_nodes.append((node.x, node.y))
            if node != None:
                node = node.parent


        return path_nodes

    def print_path(self, path_nodes):
        line = ''
        i = 0
        for node in self.nodes:
            if node.isWall:
                line+='#'
            elif (node.x, node.y) == (self.end.x, self.end.y):
                line += 'E'
            elif (node.x, node.y) in (path_nodes):
                line += 'o'
            elif (node.x, node.y) == (self.start.x, self.start.y):
                line += 'S'
            else:
                line += '-'
            i+=1
            if i == 20:
                i = 0
                line += '\n'
                sys.stdout.write('{}'.format(line))
                
    def go(self):
        self.open.append((self.start.f, self.start))
        while len(self.open):
            _, current = self.open.pop()
            self.print_board(current)
            time.sleep(0.01)
            self.open.sort(reverse=True)
            self.closed.add(current)
            if (current.x,current.y) == (self.end.x, self.end.y):
                print 'Found a path, exiting'
                self.end.parent = current
                self.print_path(self.get_path())
                break
            adj_nodes = self.get_adjacent_nodes(current)
            for adj_node in adj_nodes:
                self.open.sort(reverse=True)
                if not adj_node.isWall and adj_node not in self.closed:
                    if (adj_node.f, adj_node) in self.open:
                        if adj_node.g > current.g + 10:
                            self.update_node(adj_node, current)
                    else:
                        self.update_node(adj_node, current)
                        self.open.append((adj_node.f, adj_node))
        
def shortest_path(filename):
    content, rows, cols = get_content_from_file(filename)
    astar = Astar(content, rows, cols)
    astar.go()
        
if __name__ == '__main__':
    filename = sys.argv[1]
    shortest_path(filename)

    

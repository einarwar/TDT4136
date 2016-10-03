import matplotlib.pyplot as plt
import numpy as np
import sys, os, time

def get_content_from_file(filename):
    return np.genfromtxt(filename, dtype='str', comments='@')

class Node:
    def __init__(self, x, y, isWall):
        self.isWall=isWall
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        
    def calc_values(self, n0, goal):
        self.g = np.abs(self.x - n0[0]) + np.abs(self.y - n0[1]) #Manhattan distance
        self.h = np.abs(self.x - goal[0]) + np.abs(self.y - goal[1])
        self.f = self.g + self.h
        
def generate_list_of_nodes(board):
    nodes = []
    n0 = None
    for (i, row) in enumerate(board):
        for (j, cell) in enumerate(row):
            isWall = False
            if cell == '#':
                isWall = True
            n = Node(i, j, isWall)
            nodes.append(n)
            if cell == 'A':
                n0 = (i,j)
            elif cell == 'B':
                goal = (i,j)
    return nodes, n0, goal

if __name__ == '__main__':
    filename = sys.argv[1]
    content = get_content_from_file(filename)
    nodes, n0, goal = generate_list_of_nodes(content)
    nodes[1].calc_values(n0, goal)


#!/usr/bin/env python3

####### Modules
import sys
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy import integrate
import networkx as nx
import itertools

####### Code

def generate_random_color_hex():
    """Generate a random hexadecimal color."""
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    color_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    return color_hex

def generate_random_colors_hex(k):
    """Generate a list of k random hexadecimal colors."""
    colors_hex = []
    for _ in range(k):
        colors_hex.append(generate_random_color_hex())
    return colors_hex

N_x, N_y = 50, 50

p = float(input("p : "))

class Edge:
    def __init__(self, i, j) -> None:
        self.connectedness = stats.bernoulli.rvs(p,1-p)

class Node: 
    def __init__(self, i, j) -> None:
        self.edge = np.ndarray((4), dtype=object)
        self.edge[0] = Edge(i,i-1).connectedness
        self.edge[1] = Edge(i,i+1).connectedness
        self.edge[2] = Edge(j,j-1).connectedness
        self.edge[3] = Edge(j,j+1).connectedness

lattice = np.ndarray((N_x, N_y), dtype = object)

for i in range(N_x):
    for j in range(N_y):
        lattice[i,j] = Node(i,j)


G1 = nx.grid_2d_graph(N_x,N_y)
pos = {(x,y):(y,-x) for x,y in G1.nodes()}

ebunch = []

for i in range(N_x):
    for j in range(N_y):
        if (lattice[i,j].edge[0]==0): 
            ebunch.append(((i,j), (i-1,j)))
        
        if (lattice[i,j].edge[1]==0): 
            ebunch.append(((i,j), (i+1,j)))
        
        if (lattice[i,j].edge[2]==0): 
            ebunch.append(((i,j), (i,j-1)))        
        
        if (lattice[i,j].edge[3]==0): 
            ebunch.append(((i,j), (i,j+1)))

G1.remove_edges_from(ebunch)

nx.draw(G1,
        node_color='lightgreen',
        node_size=10,
        pos=pos,
        with_labels = False)
 
plt.rcParams["figure.figsize"] = (80,80)
plt.savefig("Graph.png",dpi=400)
plt.close


sub_graphs = [G1.subgraph(cc) for cc in nx.connected_components(G1)]

colorlist = generate_random_colors_hex(len(sub_graphs))

for index, sg in enumerate(sub_graphs):
    nx.draw_networkx(sg, pos = pos, node_size=10, edge_color = colorlist[index], node_color = colorlist[index],with_labels = False)

plt.rcParams["figure.figsize"] = (80,80)
plt.savefig("Graph1.png",dpi=400)
plt.close

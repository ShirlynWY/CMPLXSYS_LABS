#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 22:17:39 2021

@author: shirlynw
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pycxsimulator
from pylab import *

N = 100
m = 2
minload = 20
maxload = 100

numsims = 100
timesteps = 100
numfail_array = np.zeros([1, numsims])
isend = 0;
def initialize():
    global g, failed_nodes, numfail_array, isend
    failed_nodes = []
    isend = 0
    g = nx.barabasi_albert_graph(N, m)
    g.pos = nx.spectral_layout(g)
    nx.set_node_attributes(g, 0, 'state') # 0: running, 1: failed
    nx.set_node_attributes(g, 0, 'max')
    nx.set_node_attributes(g, 0, 'load')

    # plt.figure()
    # nx.draw_networkx(g, g.pos, with_labels = False, node_size = 50) # draw network
    # plt.show()
    for a in g._node:
        g._node[a]['max'] = np.random.normal(100, 10)
        curr_max = g._node[a]['max']
        g._node[a]['load'] = np.random.uniform(minload, maxload) / 100 * curr_max
        
    failed_ind = np.random.randint(0, N-1)
    g._node[failed_ind]['load'] = g._node[failed_ind]['max'] * 1.1
    g._node[failed_ind]['state'] = 1

    # deg_seq = [d for n, d in g.degree()]
    # max_deg = max(deg_seq)
    # hist1 = np.histogram(deg_seq, bins = range(0,max_deg))
    
    # plt.figure()
    # plt.hist(deg_seq, bins = range(0,max_deg))
    # plt.title('Degree histogram')
    
        
    # plt.figure()
    # plt.plot(hist1[1][1:], hist1[0], 'b^')
    # plt.title('Number of nodes vs degree')
    
    # plt.figure()
    # logbins = np.log(range(0,max_deg))
    # # logbins[0] = 0
    # tempbins = logbins[1:]
    # plt.hist(np.log(deg_seq), bins = tempbins)
    # plt.title('(Log) degree histogram')
    
    
    # plt.figure()
    # plt.plot(hist1[1][1:], np.log( hist1[0]), 'b^')
    # plt.title('Log(# of nodes) vs degree')
    # plt.show()
def update():
    global g, failed_nodes, numfail_array, isend
    for a in g._node:
        curr_max = g._node[a]['max']
        curr_load = g._node[a]['load']
        if curr_load > curr_max:
            g._node[a]['state'] = 1
            temp_deg = 0
            # g.degree[a]
            # burden = curr_load / temp_deg
            alive_nb = 0;
            for n in g.neighbors(a):
                if g._node[n]['state'] ==0:
                    alive_nb +=1
            if alive_nb ==0:
                # print('No neighbors are alive. ')
                isend = 1
            else:
                burden = curr_load / alive_nb
                for n in g.neighbors(a):
                    if g._node[n]['state'] ==0:
                        g._node[n]['load'] += burden
                
            g._node[a]['load'] = 0     
            failed_nodes.append(a)
    return isend
# =============================================================================
# def observe():
#     global g, failed_nodes, numfail_array
#     cla()
#     nx.draw(g, cmap = cm.Wistia, vmin = 0, vmax = 2,
#             node_color = [g._node[i]['state'] for i in g._node],
#             pos = g.pos)
# =============================================================================

# pycxsimulator.GUI().start(func=[initialize, observe, update])

for i in range(0,numsims):        # loop over all simulations
    initialize()                  # initialize each simulation
    for j in range(1,timesteps):  # loop over the timesteps for that simulation
        isend = update()                  # update
        if isend ==1:
            break
    temp = len(failed_nodes) 
    numfail_array[0][i] = temp     # store the resulting simulation in prevarray

oned_num = numfail_array[0]
plt.figure()
# plt.plot(range(len(numfail_array[0])), numfail_array[0], linewidth = 2,)
# hist1 = np.histogram(oned_num, bins = 'auto')
plt.hist(oned_num, bins = range(N))
# print(list(range(1,N)))
# plt.ylim([0, 12])
plt.xlabel("Size of Blackout")
plt.ylabel("Number of simulations")
mtitle = 'Size of blackout histogram, min load =  ' + str(minload) 
plt.title(mtitle)
plt.show(block=True)
print('Blackout size in all simulations:')
print(numfail_array)
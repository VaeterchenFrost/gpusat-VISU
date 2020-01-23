# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 18:22:48 2020

@author: Martin
"""
import json
import networkx as nx
import matplotlib.pyplot as plt
fig = plt.figure(dpi=100, figsize=(12,8))

"""
Adding one edge s->t to the dictionary d.
e.g.
if '2' in g41['edges'] : g41['edges']['2'].append('1000001')
else : g41['edges']['2'] = ['1000001']
"""
def add_edge(d, s, t):
    d.append((s,t))
    
    
    
g41 = {}
g41['edges'] = []
g41['labels'] = {}

g41['labels']['2'] = "bag 2\n[ 1 2 5 ]"
g41['labels']['1000001'] = """bag 2\nid | v1 v2 || n Sol
------------------
  0|  0  0   ||    0    
  1|  1  0   ||    1    
  2|  0  1   ||    1    
  3|  1  1   ||    2    
------------------
           sum: 4"""
add_edge(g41['edges'], '2', '1000001') 

g41['labels']['4'] = "bag 4\n[ 2 3 8 ]"
g41['labels']['1000002'] = """bag 4\nid | v2 v8 || n Sol
------------------
  0|  0  0   ||    1    
  1|  1  0   ||    2    
  2|  0  1   ||    1    
  3|  1  1   ||    1    
------------------
           sum: 5"""
add_edge(g41['edges'], '4', '1000002')   

add_edge(g41['edges'], '2', '4')

result = json.dumps(g41, indent = 2, sort_keys=True)

with open("demofile.json", "w") as f:
    f.write(result)

g41in = json.loads(result)

print("g41in ", g41in)

G = nx.DiGraph(directed=True)

#for (u,v) in g41in['edges']: G.add_edge(u, v)
G.add_edges_from(g41in['edges'])
#G.add_nodes_from(g41in['nodes'])

#print(result)

print("edges=", G.edges())
pos=nx.spring_layout(G, scale=0.2) # positions for all nodes

nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size=5000, alpha=0.1)
nx.draw_networkx_edges(G, pos, g41in['edges'])
nx.draw_networkx_labels(G, pos, g41['labels'], 12)#, bbox = dict(fc="red", ec="black", boxstyle="circle", lw=3))
plt.axis('on')
plt.margins(0.3, 0.3)
plt.tick_params('both')
plt.show()

#nx.draw(G)




















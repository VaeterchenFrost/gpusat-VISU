# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:40:01 2020

@author: Martin
"""

from graphviz import Digraph, Graph

G = Graph(strict=True,
                         engine='circo',
                         graph_attr={'fontsize': '20'},
                         node_attr={'fontcolor': 'black',
                                    'penwidth': '2.2'})
G.edges(({'1', '4'}, {'1', '6'}, {'4', '6'}))
print(G.pipe('plain').decode('ascii'))
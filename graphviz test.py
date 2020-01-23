# structs_revisited.py - http://www.graphviz.org/pdf/dotguide.pdf Figure 12
"""<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                           <TR><TD PORT="f1" BGCOLOR="gray">first</TD></TR>
                           <TR><TD PORT="f2">second</TD></TR>
                           <TR><TD PORT="e">third</TD></TR>
              </TABLE>>"""
from graphviz import Digraph

s = Digraph('structs', filename='structs_revisited.gv',
            node_attr={'shape': 'plaintext'})

s.node('struct1', """<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0">
                           <TR><TD BGCOLOR="gray">first</TD><TD PORT="f1"></TD><TD>second</TD></TR>
                       </TABLE>>""")
s.attr('node', shape='record')
s.attr('edge', arrowType='halfopen', splines= 'line')

s.node('struct2', r'{<f0> bag 2|{{id|0}|{v1|0}|{ v2|0}|{ nSol|0}}|sum: 4}', fontcolor='green')
s.node('struct3', r'hello\nworld |{ b |{c|<here> d|e}| f}| g | h')

s.edges([('struct1:f1', 'struct2:f0'), ('struct1:f1', 'struct3:here')])

with open("gvtest.dot","w") as f:
    f.write(s.__str__())
    
s.render(view=True, format='png')
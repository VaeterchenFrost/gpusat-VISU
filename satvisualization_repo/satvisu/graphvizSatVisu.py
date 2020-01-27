# structs_revisited.py - http://www.graphviz.org/pdf/dotguide.pdf Figure 12
"""building a graphoutput from satsolver runs.
"""
"""<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
    <TR><TD PORT="f1" BGCOLOR="gray">first</TD></TR>
    <TR><TD PORT="f2">second</TD></TR>
    <TR><TD PORT="e">third</TD></TR>
    </TABLE>>
    s.node('sol4',r'{<f0> bag 2|{{id|0}|{v1|0}|{ v2|0}|{ nSol|0}}|sum: 4}',fontcolor='green')
"""


from graphviz import Digraph
import numpy as np

s = Digraph('structs', filename='structs_revisited.gv',
            node_attr={'shape': 'rect'})


def texit():
    """raises SystemExit(1)"""
    raise SystemExit(1)
    
def trimR(string, len=1):
    return string[:-1]


def bagNode(head, tail, anchor="anchor", headcolor="white",
            tableborder=0, cellborder=0, cellspacing=0):
    """HTML format with 'head' as the first label, then appending further labels.
    After the 'head' there is an (empty) anchor for edges with a name tag. e.g.
    <<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
    <TR>
    <TD BGCOLOR="gray">first</TD><TD PORT="f1"></TD><TD>second</TD>
    </TR>
    </TABLE>>
    """
    result = """<<TABLE BORDER=\"{}\" CELLBORDER=\"{}\" CELLSPACING=\"{}\">
              <TR><TD BGCOLOR=\"{}\">{}</TD>""".format(tableborder, cellborder, cellspacing, headcolor, head)
    result += "<TD PORT=\"" + anchor + "\"></TD>"""

    if isinstance(tail, str):
        result += "<TD>" + tail + "</TD>"
    else:
        for label in tail:
            result += "<TD>" + label + "</TD>"

    result += "</TR></TABLE>>"
    return result


def solutionNode(solutionTable, toplabel="", bottomlabel=""):
    """Fill the node from the 2D 'solutionTable' (columnbased!).
    Optionally add a line above and/or below the table.

    Example structure for four columns:
    |----------|
    | toplabel |
    ------------
    |v1|v2|v3|v4|
    |0 |1 |0 |1 |
    |1 |1 |0 |0 |
    ...
    ------------
    | botlabel |
    |----------|
    """
    result = "<anchor> " + toplabel
    result += "|"

    if len(solutionTable) == 0:
        return result + "empty" + "|" + bottomlabel

    result += "{"                                       # insert table

    for i, column in enumerate(solutionTable):
        result += "{"                                   # start column
        for row in column[:-1]:
            result += str(row) + "|"
        for row in column[-1:]:
            result += str(row) 
        result += "}"
        if i != len(solutionTable)-1:                   # sep. between columns 
            result += "|"

    return "{" + result + "}"

s.node('bag4', bagNode("bag 4", "[2 3 8]"), fontsize="24")
s.node('bag3', bagNode("bag 3", "[2 4 8]"))
s.node('join1', bagNode("Join", "2~3"))
s.node('bag2', bagNode("bag 2", "[1 2 5]"))
s.node('bag1', bagNode("bag 1", "[1 2 4 6]"))
s.node('bag0', bagNode("bag 0", "[1 4 7]"))

s.attr('node', shape='record')

s.node(
    'sol4',
    r'{<f0> bag 2|{{id|0}|{v1|0}|{ v2|0}|{ nSol|0}}|sum: 4}',
    fontcolor='green')
s.node('hi', r'hello\nworld |{ b |{c|<here> d|e}| f}| g | h')

s.edges([('bag4:anchor', 'bag3:anchor'), ('bag2:anchor', 'join1:anchor'),
         ('bag3:anchor', 'join1:anchor'), ('join1:anchor', 'bag1:anchor'),
         ('bag1:anchor', 'bag0:anchor')])

with open("gvtest.dot", "w") as f:
    f.write(s.__str__())

s.render(view=True, format='png')

import pytest

def test_solutionNode():
    return 0
    
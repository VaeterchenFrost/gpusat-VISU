# structs_revisited.py - http://www.graphviz.org/pdf/dotguide.pdf Figure 12
"""building a graphoutput from satsolver runs.
<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
    <TR><TD PORT="f1" BGCOLOR="gray">first</TD></TR>
    <TR><TD PORT="f2">second</TD></TR>
    <TR><TD PORT="e">third</TD></TR>
    </TABLE>>
    s.node('sol4',r'{<f0> bag 2|{{id|0}|{v1|0}|{ v2|0}|{ nSol|0}}|sum: 4}',
    fontcolor='green')
"""

from graphviz import Digraph
import numpy as np


def bagNode(head, tail, anchor="anchor", headcolor="white",
            tableborder=0, cellborder=0, cellspacing=0):
    """HTML format with 'head' as the first label, then appending
    further labels.
    After the 'head' there is an (empty) anchor for edges with a name tag. e.g.
    <<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
    <TR>
    <TD BGCOLOR="gray">first</TD><TD PORT="f1"></TD><TD>second</TD>
    </TR>
    </TABLE>>
    """
    result = """<<TABLE BORDER=\"{}\" CELLBORDER=\"{}\" CELLSPACING=\"{}\">
              <TR><TD BGCOLOR=\"{}\">{}</TD>""".format(
        tableborder, cellborder, cellspacing, headcolor, head)
    result += "<TD PORT=\"" + anchor + "\"></TD>"""

    if isinstance(tail, str):
        result += "<TD>" + tail + "</TD>"
    else:
        for label in tail:
            result += "<TD>" + label + "</TD>"

    result += "</TR></TABLE>>"
    return result


def solutionNode(solutionTable, toplabel="", bottomlabel="", transpose=False):
    """Fill the node from the 2D 'solutionTable' (columnbased!).
    Optionally add a line above and/or below the table.

    solutionTable : 2D-arraylike, entries get converted to str

    toplabel : string, placed above the table

    bottomlabel : string, placed below the table

    transpose : bool, wether to transpose the solutionTable before processing

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
    result = ""
    if toplabel:
        result += toplabel + "|"

    if len(solutionTable) == 0:
        result += "empty"
    else:
        if transpose:
            solutionTable = np.transpose(solutionTable)
        result += "{"                                       # insert table

        for i, column in enumerate(solutionTable):
            result += "{"                                   # start column
            for row in column[:-1]:
                result += str(row) + "|"
            for row in column[-1:]:
                result += str(row)
            result += "}"
            if i < len(solutionTable) - 1:          # sep. between columns
                result += "|"
        result += "}"                                       # close table
    if len(bottomlabel) > 0:
        result += "|" + bottomlabel

    return "{" + result + "}"


def main():
    _filename = 'g41Digraph'

    s = Digraph('structs', filename=_filename, strict=True,
                node_attr={'shape': 'box', 'fillcolor': 'yellow', 'style': "rounded,filled"})

    s.node('bag4', bagNode("bag 4", "[2 3 8]", headcolor='green'))
    s.node('bag3', bagNode("bag 3", "[2 4 8]"))
    s.node('join1', bagNode("Join", "2~3"))
    s.node('bag2', bagNode("bag 2", "[1 2 5]"))
    s.node('bag1', bagNode("bag 1", "[1 2 4 6]"))
    s.node('bag0', bagNode("bag 0", "[1 4 7]"))

    s.attr('node', shape='record')
    # s.node('etest', solutionNode([["id", "0"], ["v1", "1"],
    #                               ["v2", "2"], ["v3", "4"],
    #                               ["nSol", "0"]], "top", "bottom", True))

    s.node('sol2', solutionNode([["id", "v1", "v2", "n Sol"],
                                 [0, 0, 0, 0], [1, 1, 0, 1], [2, 0, 1, 1],
                                 [3, 1, 1, 2]], "sol bag 2", "sum: 4", True))
    s.node('sol4', solutionNode([["id", "v2", "v8", "n Sol"],
                                 [0, 0, 0, 1], [1, 1, 0, 2], [2, 0, 1, 1],
                                 [3, 1, 1, 1]], "sol bag 4", "sum: 5", True))
    s.node('sol3', solutionNode([["id", "v2", "v4", "n Sol"],
                                 [0, 0, 0, 1], [1, 1, 0, 2], [2, 0, 1, 2],
                                 [3, 1, 1, 3]], "sol bag 3", "sum: 8", True))
    s.node('solJoin1', solutionNode([["id", "v1", "v2", "v4", "n Sol"],
                                     [0, 0, 0, 0, 0],
                                     [1, 1, 0, 0, 1],
                                     [2, 0, 1, 0, 2],
                                     [3, 1, 1, 0, 4],
                                     [4, 0, 0, 1, 0],
                                     [5, 1, 0, 1, 2],
                                     [6, 0, 1, 1, 3],
                                     [7, 1, 1, 1, 6]],
                                    "sol Join 2~3", "sum: 18", True))
    s.node('sol1', solutionNode([["id", "v1", "v4", "n Sol"],
                                 [0, 0, 0, 2], [1, 1, 0, 9], [2, 0, 1, 3],
                                 [3, 1, 1, 6]], "sol bag 1", "sum: 20", True))
    s.node('sol0', solutionNode([["id", "v1", "v4", "v7", "n Sol"],
                                 [0, 0, 0, 0, 2],
                                 [1, 1, 0, 0, 0],
                                 [2, 0, 1, 0, 0],
                                 [3, 1, 1, 0, 0],
                                 [4, 0, 0, 1, 2],
                                 [5, 1, 0, 1, 9],
                                 [6, 0, 1, 1, 3],
                                 [7, 1, 1, 1, 6]],
                                "sol bag 0", "sum: 22", True))

    s.edges(
        [('bag4:anchor', 'bag3:anchor'), ('bag2:anchor', 'join1:anchor'),
         ('bag3:anchor', 'join1:anchor'), ('join1:anchor', 'bag1:anchor'),
         ('bag1:anchor', 'bag0:anchor'),
         ('bag4:anchor', 'sol4:anchor'), ('bag3:anchor', 'sol3:anchor'),
         ('bag2:anchor', 'sol2:anchor'), ('bag1:anchor', 'sol1:anchor'),
         ('bag0:anchor', 'sol0:anchor'), ('join1:anchor', 'solJoin1:anchor')])

    s.edge('bag0:anchor', 'sol0:anchor', color="green:red;0.25:blue")

    with open("example41.dot", "w") as file:
        file.write(s.__str__())

    s.render(view=True, format='png', filename=_filename)


if __name__ == "__main__":
    main()                                      # Call Mainroutine

# s.node(
#     'sol4',
#     r'{<f0> bag 2|{{id|0}|{v1|0}|{ v2|0}|{ nSol|0}}|sum: 4}',
#     fontcolor='green')
# s.node('hi', r'hello\nworld |{ b |{c|<here> d|e}| f}| g | h')
# ('bag1:anchor', 'etest:anchor')

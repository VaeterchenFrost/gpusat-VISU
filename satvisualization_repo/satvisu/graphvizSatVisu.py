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

from graphviz import Digraph, Graph, RENDERERS
import numpy as np
import json
import sys
import io


def read_json(json_data):
    """
    Read json data into a callable object.
    Throws error if the parsed object has length 0.

    Parameters
    ----------
    json_data : String or io.TextIOWrapper
        The object to be read from.

    Returns
    -------
    result : JSON
        The parsed json.

    """
    if isinstance(json_data, str):
        result = json.loads(json_data)
    elif isinstance(json_data, io.TextIOWrapper):
        result = json.load(json_data)
    else:
        print("read_json called on ", type(json_data))
        result = json_data
    assert len(result) > 0, "Please input a valid JSON resource!"
    return result


def baseStyle(graph, node):
    graph.node(node, fillcolor='white', penwidth="1.0")


def emphasiseNode(graph, node, _fillcolor="yellow", _penwidth="2.5"):
    if _fillcolor:
        graph.node(node, fillcolor=_fillcolor)
    if _penwidth:
        graph.node(node, penwidth=_penwidth)


def styleHideNode(graph, node):
    graph.node(node, style="invis")


def styleHideEdge(graph, s, t):
    graph.edge(s, t, style="invis")


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


def main(infile):
    print(RENDERERS)
    visudata = read_json(infile)
    # print("READS>>>\n", json.dumps(visudata))

    tdGraph = visudata["treeDecJson"]
    TIMELINE = visudata["tdTimeline"]

    bagpre = tdGraph["bagpre"]
    joinpre = "Join %d~%d"
    solpre = "sol%d"
    soljoinpre = "solJoin%d~%d"
    lastSol = ""
    _filename = 'g41DigraphProgress%d'

    s = Digraph(
        'structs',
        filename=_filename,
        strict=True,
        graph_attr={
            'dpi': '250',
            'margin': '0,0.5'},
        # edge_attr={
        #     'minlen': '5'},
        node_attr={
            'shape': 'box',
            'fillcolor': 'white',
            'style': "rounded,filled",
            'margin': '0.11,0.01'})

    # -----------Iterate labeldict ---------------

    for item in tdGraph["labeldict"]:
        bagname = bagpre % str(item["id"])
        s.node(bagname, bagNode(bagname, item["list"]))

    s.edges([(bagpre % str(first), bagpre % str(second))
             for (first, second) in tdGraph["edgearray"]])
    # s.attr('edge', minlen="1")

    # >>>>>>>>>>>>Iterate TIMELINE FORWARD>>>>>>>>>>>>>
    """
    for i, node in enumerate(TIMELINE):
        if i > 0:
            prevhead = TIMELINE[i - 1][0]
            baseStyle(s, bagpre % prevhead
                      if isinstance(prevhead, int) else joinpre % tuple(prevhead))
            if lastSol:
                baseStyle(s, lastSol)

        # if len(node) < 1: raise IndexError("Error within Timeline - found
        # len=0")

        if len(node) > 1:
            # solution to be displayed
            id_inv_bags = node[0]
            if isinstance(id_inv_bags, int):
                lastSol = solpre % id_inv_bags
                s.node(lastSol, solutionNode(*(node[1])), shape='record')
                emphasiseNode(s, lastSol)
                s.edge(bagpre % id_inv_bags, lastSol)

            else:  # joined node with 2 bags
                suc = TIMELINE[i + 1][0]
                print('joining ', node[0], ' to ', suc)  # get the joined bags
                # solution
                id_inv_bags = tuple(id_inv_bags)
                lastSol = soljoinpre % id_inv_bags
                s.node(lastSol, solutionNode(*(node[1])), shape='record')
                emphasiseNode(s, lastSol)
                s.edge(joinpre % id_inv_bags, lastSol)
                # edges
                for child in id_inv_bags:             # basically "remove" current
                    # TODO check where 2 args are possibly occuring
                    s.edge(
                        bagpre % child
                        if isinstance(child, int) else joinpre % child,
                        bagpre % suc
                        if isinstance(suc, int) else joinpre % suc,
                        style='invis',
                        constraint='false')
                    s.edge(bagpre % child if isinstance(child, int)
                           else joinpre % child,
                           joinpre % id_inv_bags)
                s.edge(joinpre % id_inv_bags, bagpre % suc
                       if isinstance(suc, int) else joinpre % suc)

        emphasiseNode(s, bagpre % node[0]
                      if isinstance(node[0], int) else joinpre % tuple(node[0]))

        # s.pipe(format='dot')
        # print(s.pipe(format='json').decode('utf-8'))
        # s.render(view=False, format='dot', filename=_filename % i)
        """
    for i, node in enumerate(TIMELINE):                 # Create the positions
        if len(node) > 1:
            # solution to be displayed
            id_inv_bags = node[0]
            if isinstance(id_inv_bags, int):
                lastSol = solpre % id_inv_bags
                s.node(lastSol, solutionNode(*(node[1])), shape='record')

                s.edge(bagpre % id_inv_bags, lastSol)

            else:  # joined node with 2 bags
                suc = TIMELINE[i + 1][0]
                print('joining ', node[0], ' to ', suc)  # get the joined bags
                # solution
                id_inv_bags = tuple(id_inv_bags)
                lastSol = soljoinpre % id_inv_bags
                s.node(lastSol, solutionNode(*(node[1])), shape='record')

                s.edge(joinpre % id_inv_bags, lastSol)
                # edges
                for child in id_inv_bags:             # basically "remove" current
                    # TODO check where 2 args are possibly occuring
                    s.edge(
                        bagpre % child
                        if isinstance(child, int) else joinpre % child,
                        bagpre % suc
                        if isinstance(suc, int) else joinpre % suc,
                        style='invis',
                        constraint='false')
                    s.edge(bagpre % child if isinstance(child, int)
                           else joinpre % child,
                           joinpre % id_inv_bags)
                s.edge(joinpre % id_inv_bags, bagpre % suc
                       if isinstance(suc, int) else joinpre % suc)

    # <<<<<<<<<<<Iterate TIMELINE BACKWARDS<<<<<<<<<<<<<<<<<<<
    for i, node in enumerate(TIMELINE[::-1]):       # Cut and emphazise
        id_inv_bags = node[0]
        print(i, ":Reverse traversing on", id_inv_bags)

        if i > 0:                                   # Delete previous emphasis
            prevhead = TIMELINE[len(TIMELINE) - i][0]
            bag = (bagpre % prevhead
                   if isinstance(prevhead, int) else joinpre % tuple(prevhead))
            baseStyle(s, bag)
            if lastSol:
                styleHideNode(s, lastSol)
                styleHideEdge(s, bag, lastSol)
                lastSol = ""

        if len(node) > 1:
            # solution to be displayed

            if isinstance(id_inv_bags, int):
                lastSol = solpre % id_inv_bags
                emphasiseNode(s, lastSol)
                s.edge(bagpre % id_inv_bags, lastSol)

            else:  # joined node with 2 bags
                id_inv_bags = tuple(id_inv_bags)
                lastSol = soljoinpre % id_inv_bags

                emphasiseNode(s, lastSol)

        emphasiseNode(s, bagpre % id_inv_bags
                      if isinstance(id_inv_bags, int) else joinpre % id_inv_bags)
        s.render(
            view=True, format='png', filename=_filename %
            (len(TIMELINE) - i))


def manual():
    # example input:
    tdGraph = {
        "bagpre": "bag %s",
        "edgearray":
        [
            [1, 0],
            [2, 1],
            [3, 1],
            [4, 3]
        ],
        "labeldict":
        {
            "0": ["[1 4 7]"],
            "1": ["[1 2 4 6]"],
            "2": ["[1 2 5]"],
            "3": ["[2 4 8]"],
            "4": ["[2 3 8]"]
        }
    }

    TIMELINE = [
        [0],
        [1],
        [2],
        [
            2,
            [
                [
                    ["id", "v1", "v2", "n Sol"],
                    [0, 0, 0, 0],
                    [1, 1, 0, 1],
                    [2, 0, 1, 1],
                    [3, 1, 1, 2]
                ],
                "sol bag 2",
                "sum: 4",
                True
            ]
        ],
        [3],
        [4],
        [
            4,
            [
                [
                    ["id", "v2", "v8", "n Sol"],
                    [0, 0, 0, 1],
                    [1, 1, 0, 2],
                    [2, 0, 1, 1],
                    [3, 1, 1, 1]
                ],
                "sol bag 4",
                "sum: 5",
                True
            ]
        ],
        [
            3,
            [
                [
                    ["id", "v2", "v4", "n Sol"],
                    [0, 0, 0, 1],
                    [1, 1, 0, 2],
                    [2, 0, 1, 2],
                    [3, 1, 1, 3]
                ],
                "sol bag 3",
                "sum: 8",
                True
            ]
        ],
        [
            [2, 3],
            [
                [
                    ["id", "v1", "v2", "v4", "n Sol"],
                    [0, 0, 0, 0, 0],
                    [1, 1, 0, 0, 1],
                    [2, 0, 1, 0, 2],
                    [3, 1, 1, 0, 4],
                    [4, 0, 0, 1, 0],
                    [5, 1, 0, 1, 2],
                    [6, 0, 1, 1, 3],
                    [7, 1, 1, 1, 6]
                ],
                "sol Join 2~3",
                "sum: 18",
                True
            ]
        ],
        [
            1,
            [
                [
                    ["id", "v1", "v4", "n Sol"],
                    [0, 0, 0, 2],
                    [1, 1, 0, 9],
                    [2, 0, 1, 3],
                    [3, 1, 1, 6]
                ],
                "sol bag 1",
                "sum: 20",
                True
            ]
        ],
        [
            0,
            [
                [
                    ["id", "v1", "v4", "v7", "n Sol"],
                    [0, 0, 0, 0, 2],
                    [1, 1, 0, 0, 0],
                    [2, 0, 1, 0, 0],
                    [3, 1, 1, 0, 0],
                    [4, 0, 0, 1, 2],
                    [5, 1, 0, 1, 9],
                    [6, 0, 1, 1, 3],
                    [7, 1, 1, 1, 6]
                ],
                "sol bag 0",
                "sum: 22",
                True
            ]
        ]
    ]


def endresult():
    _filename = 'g41Digraph'
    # graph_attr={'size':'8,12!'} , graph_attr={'splines':'false'}
    s = Digraph(
        'structs',
        filename=_filename,
        strict=True,
        graph_attr={
            'dpi': '300'},
        node_attr={
            'shape': 'box',
            'fillcolor': 'white',
            'style': "rounded,filled"})

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
         ('bag4:anchor', 'sol4'), ('bag3:anchor', 'sol3'),
         ('bag2:anchor', 'sol2'), ('bag1:anchor', 'sol1'),
         ('bag0:anchor', 'sol0'), ('join1:anchor', 'solJoin1')])

    s.edge('bag0:anchor', 'sol0', color="green:red;0.55:blue")
    emphasiseNode(s, 'bag0')
    with open("example41.dot", "w") as file:
        file.write(s.__str__())

    s.render(view=True, format='png', filename=_filename)


def incidence():

    r_clause = 10
    r_vars = 8
    clausetag = "c_%d"
    vartag = "v_%d"

    colors = ["#0073a1", "#b14923", "#244320", "#b1740f", "#a682ff", '#004066',
              '#0d1321', '#da1167', '#604909', '#0073a1', '#b14923', '#244320',
              '#b1740f', '#a682ff']

    g_incid = Graph(strict=True, graph_attr={'splines': 'false', 'dpi': '300',
                                             'nodesep': '0.5', 'fontsize': '20'},  # ortho
                    edge_attr={'penwidth': '2.2', 'dir': 'back', 'arrowtail': 'none'})

    with g_incid.subgraph(name='cluster_clause', edge_attr={'style': 'invis'},
                          node_attr={'style': 'rounded,filled', 'fillcolor': 'white'}) as clauses:
        clauses.attr(label='clauses')
        clauses.edges([(clausetag % (i + 1), clausetag % (i + 2))
                       for i in range(r_clause - 1)])

    g_incid.attr(
        'node',
        shape='diamond',
        fontcolor='black',
        penwidth='2.2',
        style='dotted')
    with g_incid.subgraph(name='cluster_ivar', edge_attr={'style': 'invis'}, node_attr={'style': 'dotted'}) as ivars:
        ivars.attr(label='variables')
        ivars.edges([(vartag % (i + 1), vartag % (i + 2))
                     for i in range(r_vars - 1)])
        for i in range(r_vars):
            g_incid.node(vartag %
                         (i + 1), vartag %
                         (i + 1), color=colors[(i + 1) %
                                               len(colors)])

    g_incid.attr('edge', constraint="false")
    EDGELIST = [[1, [1, 4, 6]], [2, [1, -5]], [3, [-1, 7]], [4, [2, 3]], [5, [2, 5]],
                [6, [2, -6]], [7, [3, -8]], [8, [4, -8]], [9, [-4, 6]], [10, [-4, 7]]]
    # (1,) for clause (2,) for variable

    for clause in EDGELIST:
        for var in clause[1]:
            if var >= 0:
                g_incid.edge(clausetag % clause[0],
                             vartag % var,
                             color=colors[var % len(colors)])
            else:
                g_incid.edge(clausetag % clause[0],
                             vartag % -var,
                             color=colors[-var % len(colors)],
                             arrowtail='odot',
                             # style='dotted'
                             )
            # color=sns.xkcd_rgb[k[(var * 100) % len(k)]]) # yellow

    # timeline for incidence emphasis
    # s.node('bag4', bagNode("bag 4", "[2 3 8]", headcolor='green'))
    # s.node('bag3', bagNode("bag 3", "[2 4 8]"))
    # s.node('join1', bagNode("Join", "2~3"))
    # s.node('bag2', bagNode("bag 2", "[1 2 5]"))
    # s.node('bag1', bagNode("bag 1", "[1 2 4 6]"))
    # s.node('bag0', bagNode("bag 0", "[1 4 7]"))
    TIMELINE = (None, None,
                [1, 2, 5],
                None,
                [2, 3, 8],
                [2, 4, 8],
                [1, 2, 4],  # JOIN

                [1, 2, 4, 6],
                [1, 4, 7]
                )

    # make edgelist variable-based (varX, clauseY), ...
    import itertools

    tr = list(
        map(lambda y: list(map(lambda x: (x, y[0]), y[1])), EDGELIST))

    var_cl_list = list(itertools.chain.from_iterable(tr))  # flatten
    # print('var_cl_list', var_cl_list)

    bodybaselen = len(g_incid.body)
    for i, variables in enumerate(TIMELINE):    # all timesteps

        # reset highlighting
        g_incid.body = g_incid.body[:bodybaselen]
        if variables is None:
            g_incid.render(
                view=True,
                format='png',
                filename='incidenceGraph%d' %
                i)
            continue
        # print(len(g_incid.body))

        emp_clause = list(set([a[1] for a in list(filter(lambda var_cl:
                                                         abs(var_cl[0]
                                                             ) in variables,
                                                         var_cl_list))]))

        emp_var = list(set([abs(a[0]) for a in list(
            filter(lambda var_cl: var_cl[1] in emp_clause, var_cl_list))]))
        print(i, 'emp_clause ', emp_clause)
        print(i, 'emp_var ', emp_var)

        for var in emp_var:
            _vartag = vartag % abs(var)
            _style = 'solid,filled' if var in variables else 'dotted,filled'
            g_incid.node(_vartag, _vartag, style=_style, fillcolor='yellow')

        for cl in emp_clause:
            g_incid.node(clausetag % cl, clausetag % cl, fillcolor='yellow')

        for edge in var_cl_list:
            (var, clause) = edge

            _style = 'solid' if clause in emp_clause else 'dotted'
            _vartag = vartag % abs(var)

            # if i > 0 and (abs(var) not in variables) and (
            #         abs(var) in TIMELINE[i - 1]):
            #     g_incid.node(_vartag, _vartag, style='dotted')

            if var >= 0:

                g_incid.edge(clausetag % clause,
                             _vartag,
                             color=colors[var % len(colors)],
                             style=_style)
            else:
                g_incid.edge(clausetag % clause,
                             _vartag,
                             color=colors[-var % len(colors)],
                             arrowtail='odot',
                             style=_style
                             )
        # print(g_incid.body)
        # body – Iterable of verbatim lines to add to the graph body.

        g_incid.render(
            view=True,
            format='png',
            filename='incidenceGraph%d' %
            i)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog='graphvizSatVisu.py',
        description='Visualizing Dynamic Programming on Treedecompositions.')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r', encoding='UTF-8'))

    infile = parser.parse_args().file
    main(infile)                                      # Call Mainroutine
    # incidence()

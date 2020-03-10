# structs_revisited.py - http://www.graphviz.org/pdf/dotguide.pdf Figure 12
"""building a graphoutput from satsolver runs.

@author: Martin Röbke
"""

from graphviz import Digraph, Graph
import numpy as np
import json
import io
import itertools


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
    # print(RENDERERS)
    visudata = read_json(infile)
    # print("READS>>>\n", json.dumps(visudata))

    tdGraph = visudata["treeDecJson"]
    TIMELINE = visudata["tdTimeline"]

    bagpre = tdGraph["bagpre"]
    joinpre = "Join %d~%d"
    solpre = "sol%d"
    soljoinpre = "solJoin%d~%d"
    lastSol = ""
    _filename = 'results\\g41DigraphProgress%d'

    s = Digraph(
        'structs',
        filename=_filename,
        strict=True,
        graph_attr={
            'dpi': '250',
            'margin': '0,0.5'},

        node_attr={
            'shape': 'box',
            'fillcolor': 'white',
            'style': "rounded,filled",
            'margin': '0.11,0.01'})

    # -----------Iterate labeldict ---------------

    for item in tdGraph["labeldict"]:
        bagname = bagpre % str(item["id"])
        s.node(bagname, bagNode(bagname, item["labels"]))

    s.edges([(bagpre % str(first), bagpre % str(second))
             for (first, second) in tdGraph["edgearray"]])

    # >>>>>>>>>>>>Iterate TIMELINE FORWARD>>>>>>>>>>>>>

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

    for i, node in enumerate(TIMELINE[::-1]):       # Cut and hide emphasis
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

        emphasiseNode(s,
                      bagpre %
                      id_inv_bags if isinstance(
                          id_inv_bags,
                          int) else joinpre %
                      id_inv_bags)
        s.render(
            view=False, format='png', filename=_filename %
            (len(TIMELINE) - i))

    # Prepare Incidence graph Timeline

    _edgelist = list(
        map(lambda x: [x['id'], x['list']], visudata["clausesJson"]))

    _timeline = []
    for step in TIMELINE:
        if len(step) < 2:
            _timeline.append(None)
        elif isinstance(step[0], int):
            _timeline.append(
                next(
                    (item.get('items') for item in tdGraph['labeldict'] if item['id'] == step[0])))
        else:
            # Join operation - no clauses involved in computation
            _timeline.append(None)

    col = ["#0073a1", "#b14923", "#244320", "#b1740f", "#a682ff", '#004066',
           '#0d1321', '#da1167', '#604909', '#0073a1', '#b14923', '#244320',
           '#b1740f', '#a682ff']

    incidence(
        EDGELIST=_edgelist,
        TIMELINE=_timeline,
        numVars=tdGraph['numVars'],
        colors=col)

    primalSet = set(itertools.chain.from_iterable(
        map(lambda x: (itertools.combinations(map(abs, x[1]), 2)), _edgelist)))

    primal(
        EDGELIST=primalSet,
        TIMELINE=_timeline,
        numVars=tdGraph['numVars'],
        colors=col)


def primal(EDGELIST, TIMELINE, numVars, colors):
    """

    Parameters
    ----------
    EDGELIST : Iterable of: [int, int]
        All edges between variables that occur in one or more clauses together.
        BOTH edges (x, y) and (y, x) could be in the EDGELIST.

    TIMELINE : Iterable of: None | [int...]
        None if no variables get highlighted in this step.
        Else the 'timeline' provides the set of variables that are
        in the bag(s) under consideration. This function computes all other
        variables that are involved in this timestep using the 'edgelist'.

    numVars : int
        Count of variables that are used in the clauses.

    colors : Iterable of color
        Colors to use for the graph parts.

    Returns
    -------
    None, but outputs the files with the graphs for each timestep.

    """
    # print('primal using edgelist:\n', EDGELIST, "\ntimeline\n", TIMELINE)

    vartag = "v_%d"
    _filename = 'results\\primalGraph%d'
    g_primal = Graph(strict=True,
                     graph_attr={'dpi': '300',
                                 'nodesep': '0.5', 'fontsize': '20'},
                     node_attr={'fontcolor': 'black',
                                'penwidth': '2.2'})

    for (s, t) in EDGELIST:
        g_primal.edge(vartag % s, vartag % t)

    g_primal.render(
        view=False,
        format='png',
        filename='primalGraphStart')
    
    bodybaselen = len(g_primal.body)
    for i, variables in enumerate(TIMELINE, start=1):    # all timesteps
        
        # reset highlighting
        g_primal.body = g_primal.body[:bodybaselen]
        if variables is None:
            g_primal.render(
                view=False,
                format='png',
                filename=_filename % i)
            continue

         # TODO

        g_primal.render(
            view=False,
            format='png',
            filename= _filename % i)
    


def incidence(EDGELIST=([1, [1, 4, 6]], [2, [1, -5]], [3, [-1, 7]], [4, [2, 3]], [5, [2, 5]],
                        [6, [2, -6]], [7, [3, -8]], [8, [4, -8]], [9, [-4, 6]], [10, [-4, 7]]),
              TIMELINE=(None, None, None,
                        [1, 2, 5],
                        None, None,
                        [2, 3, 8], [2, 4, 8],
                        None,   # Join
                        [1, 2, 4, 6], [1, 4, 7]),
              numVars=8, colors=("#0073a1", "#b14923", "#244320")):

    print('incidence using edgelist:\n', EDGELIST, "\ntimeline\n", TIMELINE)
    clausetag = "c_%d"
    vartag = "v_%d"

    g_incid = Graph(strict=True, graph_attr={'splines': 'false', 'dpi': '300',
                                             'nodesep': '0.5', 'fontsize': '20'},
                    edge_attr={'penwidth': '2.2', 'dir': 'back', 'arrowtail': 'none'})

    with g_incid.subgraph(name='cluster_clause', edge_attr={'style': 'invis'},
                          node_attr={'style': 'rounded,filled', 'fillcolor': 'white'}) as clauses:
        clauses.attr(label='clauses')
        clauses.edges([(clausetag % (i + 1), clausetag % (i + 2))
                       for i in range(len(EDGELIST) - 1)])

    g_incid.attr('node', shape='diamond', fontcolor='black',
                 penwidth='2.2',
                 style='dotted')
    with g_incid.subgraph(name='cluster_ivar', edge_attr={'style': 'invis'}, node_attr={'style': 'dotted'}) as ivars:
        ivars.attr(label='variables')
        ivars.edges([(vartag % (i + 1), vartag % (i + 2))
                     for i in range(numVars - 1)])
        for i in range(numVars):
            g_incid.node(vartag %
                         (i + 1), vartag %
                         (i + 1), color=colors[(i + 1) %
                                               len(colors)])

    g_incid.attr('edge', constraint="false")

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

    # make edgelist variable-based (varX, clauseY), ...

    vcmapping = map(lambda y: map(lambda x: (x, y[0]), y[1]), EDGELIST)

    var_cl_iter = tuple(itertools.chain.from_iterable(vcmapping))  # flatten
    # print('var_cl_iter', var_cl_iter)
    # ~ var_cl_iter [(1, 1), (4, 1), (6, 1), (1, 2), (-5, 2), (-1, 3), (7, 3), (2, 4),
    #~             (3, 4), (2, 5), (5, 5), (2, 6), (-6, 6), (3, 7), (-8, 7), (4, 8),
    # ~             (-8, 8), (-4, 9), (6, 9), (-4, 10), (7, 10)]

    bodybaselen = len(g_incid.body)
    for i, variables in enumerate(TIMELINE, start=1):    # all timesteps

        # reset highlighting
        g_incid.body = g_incid.body[:bodybaselen]
        if variables is None:
            g_incid.render(
                view=False,
                format='png',
                filename='results\\incidenceGraph%d' %
                i)
            continue

        emp_clause = {var_cl[1] for var_cl in
                      filter(lambda var_cl, s=variables: abs(var_cl[0]) in s, var_cl_iter)}

        emp_var = {abs(var_cl[0]) for var_cl in
                   filter(lambda var_cl, s=emp_clause: var_cl[1] in s, var_cl_iter)}

        for var in emp_var:
            _vartag = vartag % abs(var)
            _style = 'solid,filled' if var in variables else 'dotted,filled'
            g_incid.node(_vartag, _vartag, style=_style, fillcolor='yellow')

        for cl in emp_clause:
            g_incid.node(clausetag % cl, clausetag % cl, fillcolor='yellow')

        for edge in var_cl_iter:
            (var, clause) = edge

            _style = 'solid' if clause in emp_clause else 'dotted'
            _vartag = vartag % abs(var)

            if var >= 0:
                g_incid.edge(clausetag % clause,
                             _vartag,
                             color=colors[var % len(colors)],
                             style=_style)
            else:                                       # negated variable
                g_incid.edge(clausetag % clause,
                             _vartag,
                             color=colors[-var % len(colors)],
                             arrowtail='odot',
                             style=_style)

        g_incid.render(
            view=False,
            format='png',
            filename='results\\incidenceGraph%d' % i)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog='graphvizSatVisu.py',
        description='Visualizing Dynamic Programming on Treedecompositions.')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r', encoding='UTF-8'))

    _infile = parser.parse_args().file
    main(_infile)                                      # Call Mainroutine
    # incidence()

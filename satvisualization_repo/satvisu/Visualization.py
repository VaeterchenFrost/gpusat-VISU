# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:49:00 2020

@author: Martin Röbke

Visualization for dynamic programming on tree decompositions.

See also
https://github.com/daajoe/GPUSAT
and
https://github.com/hmarkus/dp_on_dbs


"""

import json
import io
import itertools

from graphviz import Digraph, Graph


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


def flatten(iterable):
    """ Flatten at first level.

    Turn ex=[[1,2],[3,4]] into
    [1, 2, 3, 4]
    and [ex,ex] into
    [[1, 2], [3, 4], [1, 2], [3, 4]]
    """
    return itertools.chain.from_iterable(iterable)


class Visualization:
    """Holds and processes the information needed to provide dot-format
    and image output for the visualization
    of dynamic programming on tree decomposition.
    """

    def __str__(self):
        """String representation"""
        return (
            self.__class__.__name__ +
            "(folder='" +
            self.outfolder +
            "', tdFile='" +
            self.td_file +
            "', primalFile='" +
            self.primal_file +
            "', incFile='" +
            self.inc_file +
            "')")

    def __init__(self, infile, outfolder, tdFile="TDStep",
                 primalFile="PrimalGraphStep",
                 incFile="IncidenceGraphStep"):
        """Copy needed fields from arguments and create additional constants"""
        self.inspectJson(infile)
        self.outfolder = outfolder
        self.td_file = tdFile
        self.primal_file = primalFile
        self.inc_file = incFile
        self.colors = ['#0073a1', '#b14923', '#244320', '#b1740f', '#a682ff',
                       '#004066', '#0d1321', '#da1167', '#604909', '#0073a1',
                       '#b14923', '#244320', '#b1740f', '#a682ff']

        self.joinpre = "Join %d~%d"
        self.solpre = "sol%d"
        self.soljoinpre = "solJoin%d~%d"
        self.clausetag = "c_"
        self.vartag = "v_"
        self.primal_splines = 'ortho'
        self.tree_dec_digraph = None
        print(self)

    def getVisuOutputFolder(self):
        return self.outfolder

    @staticmethod
    def baseStyle(graph, node):
        graph.node(node, fillcolor='white', penwidth="1.0")

    @staticmethod
    def emphasiseNode(graph, node, _fillcolor="yellow", _penwidth="2.5"):
        if _fillcolor:
            graph.node(node, fillcolor=_fillcolor)
        if _penwidth:
            graph.node(node, penwidth=_penwidth)

    @staticmethod
    def styleHideNode(graph, node):
        graph.node(node, style="invis")

    @staticmethod
    def styleHideEdge(graph, s, t):
        graph.edge(s, t, style="invis")

    @staticmethod
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

    @staticmethod
    def solutionNode(
            solution_table,
            toplabel="",
            bottomlabel="",
            transpose=False):
        """Fill the node from the 2D 'solution_table' (columnbased!).
        Optionally add a line above and/or below the table.

        solution_table : 2D-arraylike, entries get converted to str

        toplabel : string, placed above the table

        bottomlabel : string, placed below the table

        transpose : bool, wether to transpose the solution_table before
        processing

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

        if len(solution_table) == 0:
            result += "empty"
        else:
            if transpose:
                solution_table = list(zip(*solution_table))
            result += "{"                                       # insert table

            for i, column in enumerate(solution_table):
                result += "{"                                   # start column
                for row in column[:-1]:
                    result += str(row) + "|"
                for row in column[-1:]:
                    result += str(row)
                result += "}"
                if i < len(solution_table) - 1:          # sep. between columns
                    result += "|"
            result += "}"                                       # close table
        if len(bottomlabel) > 0:
            result += "|" + bottomlabel

        return "{" + result + "}"

    def inspectJson(self, infile):
        """Readout and preprocess the needed data from the input.
        """
        visudata = read_json(infile)
        print("Reading from ", infile)

        print("Found keys ", visudata.keys())

        self.tree_dec = visudata["treeDecJson"]
        self.timeline = visudata["tdTimeline"]
        self.bagpre = self.tree_dec["bagpre"]
        self.edgelist = list(
            map(lambda x: [x['id'], x['list']], visudata["clausesJson"]))

    def setupTreeDecGraph(self):
        """Create self.tree_dec_digraph"""
        self.tree_dec_digraph = Digraph(
            'structs',
            strict=True,
            graph_attr={'rankdir': 'BT'},
            node_attr={
                'shape': 'box',
                'fillcolor': 'white',
                'style': "rounded,filled",
                'margin': '0.11,0.01'})

    def basicTDG(self):
        """Create first structure in treeDecGraph."""
        for item in self.tree_dec["labeldict"]:
            bagname = self.bagpre % str(item["id"])
            self.tree_dec_digraph.node(bagname,
                                       self.bagNode(bagname, item["labels"]))

        self.tree_dec_digraph.edges([(self.bagpre % str(first), self.bagpre % str(
            second)) for (first, second) in self.tree_dec["edgearray"]])

    def forwardIterateTDG(self, joinpre=None, solpre=None, soljoinpre=None):
        """Create the final positions of all nodes with solutions.
        The arguments are optional"""
        tdg = self.tree_dec_digraph                 # shorten name

        if joinpre is None:
            joinpre = self.joinpre
        if solpre is None:
            solpre = self.solpre
        if soljoinpre is None:
            soljoinpre = self.soljoinpre

        for i, node in enumerate(
                self.timeline):                 # Create the positions
            if len(node) > 1:
                # solution to be displayed
                id_inv_bags = node[0]
                if isinstance(id_inv_bags, int):
                    last_sol = solpre % id_inv_bags
                    tdg.node(last_sol, self.solutionNode(
                        *(node[1])), shape='record')

                    tdg.edge(self.bagpre % id_inv_bags, last_sol)

                else:  # joined node with 2 bags
                    suc = self.timeline[i + 1][0]
                    # get the joined bags
                    print('joining ', node[0], ' to ', suc)
                    # solution
                    id_inv_bags = tuple(id_inv_bags)
                    last_sol = soljoinpre % id_inv_bags
                    tdg.node(last_sol, self.solutionNode(
                        *(node[1])), shape='record')

                    tdg.edge(joinpre % id_inv_bags, last_sol)
                    # edges
                    for child in id_inv_bags:             # basically "remove" current
                        # TODO check where 2 args are possibly occuring
                        tdg.edge(
                            self.bagpre % child
                            if isinstance(child, int) else joinpre % child,
                            self.bagpre % suc
                            if isinstance(suc, int) else joinpre % suc,
                            style='invis',
                            constraint='false')
                        tdg.edge(self.bagpre % child if isinstance(child, int)
                                 else joinpre % child,
                                 joinpre % id_inv_bags)
                    tdg.edge(joinpre % id_inv_bags, self.bagpre % suc
                             if isinstance(suc, int) else joinpre % suc)

    def backwardsIterateTDG(self, view=False, joinpre=None,
                            solpre=None, soljoinpre=None):
        """Cut the single steps back and update emphasis acordingly."""
        tdg = self.tree_dec_digraph     # shorten name
        last_sol = ""

        if joinpre is None:
            joinpre = self.joinpre
        if solpre is None:
            solpre = self.solpre
        if soljoinpre is None:
            soljoinpre = self.soljoinpre

        for i, node in enumerate(reversed(self.timeline)):
            id_inv_bags = node[0]
            print(i, ":Reverse traversing on", id_inv_bags)

            if i > 0:                              # Delete previous emphasis
                prevhead = self.timeline[len(self.timeline) - i][0]
                bag = (
                    self.bagpre %
                    prevhead if isinstance(
                        prevhead,
                        int) else joinpre %
                    tuple(prevhead))
                self.baseStyle(tdg, bag)
                if last_sol:
                    self.styleHideNode(tdg, last_sol)
                    self.styleHideEdge(tdg, bag, last_sol)
                    last_sol = ""

            if len(node) > 1:
                # solution to be displayed

                if isinstance(id_inv_bags, int):
                    last_sol = solpre % id_inv_bags
                    self.emphasiseNode(tdg, last_sol)
                    tdg.edge(self.bagpre % id_inv_bags, last_sol)
                else:  # joined node with 2 bags
                    id_inv_bags = tuple(id_inv_bags)
                    last_sol = soljoinpre % id_inv_bags
                    self.emphasiseNode(tdg, last_sol)

            self.emphasiseNode(tdg,
                               self.bagpre %
                               id_inv_bags if isinstance(
                                   id_inv_bags,
                                   int) else joinpre %
                               id_inv_bags)
            _filename = self.outfolder + self.td_file + '%d'
            tdg.render(
                view=view, format='svg', filename=_filename %
                (len(self.timeline) - i))

    def treeDecTimeline(self, view=False):

        self.setupTreeDecGraph()

        # -----------Iterate labeldict ---------------
        self.basicTDG()
        # >>>>>>>>>>>>Iterate TIMELINE FORWARD>>>>>>>>>>>>>
        self.forwardIterateTDG()
        # <<<<<<<<<<<Iterate TIMELINE BACKWARDS<<<<<<<<<<<<<<<<<<<
        self.backwardsIterateTDG(view=view)

        # Prepare Incidence graph Timeline

        _timeline = []
        for step in self.timeline:
            if len(step) < 2:
                _timeline.append(None)
            elif isinstance(step[0], int):
                _timeline.append(
                    next(
                        (item.get('items') for item in self.tree_dec['labeldict']
                         if item['id'] == step[0])))
            else:
                # Join operation - no clauses involved in computation
                _timeline.append(None)

        _primalSet = tuple(set(elem) for elem in flatten(
            map(lambda x: (itertools.combinations(map(abs, x[1]), 2)), self.edgelist)))

        self.primal(
            TIMELINE=_timeline,
            primalSet=_primalSet
        )

        self.incidence(
            TIMELINE=_timeline,
            numVars=self.tree_dec['numVars'],
            colors=self.colors, view=view)

    def primal(self, TIMELINE, primalSet, view=False):
        """
        Creates the primal graph emphasized for the given timeline.

        Parameters
        ----------
        primalSet : Iterable of: {int, int}
            All edges between variables that occur in one or more clauses together.
            BOTH edges (x, y) and (y, x) could be in the EDGELIST.

        TIMELINE : Iterable of: None | [int...]
            None if no variables get highlighted in this step.
            Else the 'timeline' provides the set of variables that are
            in the bag(s) under consideration. This function computes all other
    variables that are involved in this timestep using the 'edgelist'.

        colors : Iterable of color
            Colors to use for the graph parts.

        Returns
        -------
        None, but outputs the files with the graph for each timestep.

        """
        _filename = self.outfolder + self.primal_file + '%d'

        vartagN = self.vartag + '%d'    # "v_%d"

        g_primal = Graph(strict=True,
                         graph_attr={'splines': self.primal_splines,
                                     'fontsize': '20'},
                         node_attr={'fontcolor': 'black',
                                    'penwidth': '2.2'})

        for (s, t) in primalSet:
            g_primal.edge(vartagN % s, vartagN % t)

        bodybaselen = len(g_primal.body)
        for i, variables in enumerate(TIMELINE, start=1):    # all timesteps

            # reset highlighting
            g_primal.body = g_primal.body[:bodybaselen]

            if variables is None:
                g_primal.render(
                    view=view,
                    format='svg',
                    filename=_filename % i)
                continue

            for var in variables:
                g_primal.node(
                    vartagN %
                    var,
                    fillcolor='yellow',
                    style='filled')

            adjacent = {
                edge.difference(variables).pop() for edge in primalSet if len(
                    edge.difference(variables)) == 1}

            for var in adjacent:
                g_primal.node(
                    vartagN %
                    var,
                    color='green',
                    style='dotted,filled')

            g_primal.render(
                view=view,
                format='svg',
                filename=_filename % i)

    def incidence(self, TIMELINE, numVars, colors, view=False):
        """
        Creates the incidence graph emphasized for the given timeline.

        Parameters
        ----------
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
        None, but outputs the files with the graph for each timestep.

        """
        _filename = self.outfolder + self.inc_file + '%d'

        clausetagN = self.clausetag + '%d'
        vartagN = self.vartag + '%d'

        g_incid = Graph(strict=True,
                        graph_attr={'splines': 'false', 'ranksep': '0.2',
                                    'nodesep': '0.5', 'fontsize': '16',
                                    'compound': 'true'},
                        edge_attr={'penwidth': '2.2', 'dir': 'back',
                                   'arrowtail': 'none'})

        with g_incid.subgraph(name='cluster_clause',
                              edge_attr={'style': 'invis'},
                              node_attr={'style': 'rounded,filled',
                                         'fillcolor': 'white'}) as clauses:
            clauses.attr(label='clauses')
            clauses.edges([(clausetagN % (i + 1), clausetagN % (i + 2))
                           for i in range(len(self.edgelist) - 1)])

        g_incid.attr('node', shape='diamond', fontcolor='black',
                     penwidth='2.2',
                     style='dotted')
        with g_incid.subgraph(name='cluster_ivar',
                              edge_attr={'style': 'invis'},
                              node_attr={'style': 'dotted'}) as ivars:
            ivars.attr(label='variables')
            ivars.edges([(vartagN % (i + 1), vartagN % (i + 2))
                         for i in range(numVars - 1)])
            for i in range(numVars):
                g_incid.node(vartagN %
                             (i + 1), vartagN %
                             (i + 1), color=colors[(i + 1) %
                                                   len(colors)])

        g_incid.attr('edge', constraint="false")
        # invis distance between clusters: minlen
        g_incid.edge(clausetagN % 1, vartagN % 1, ltail='cluster_clause',
                     lhead='cluster_ivar', minlen='3', style='invis')
        for clause in self.edgelist:
            for var in clause[1]:
                if var >= 0:
                    g_incid.edge(clausetagN % clause[0],
                                 vartagN % var,
                                 color=colors[var % len(colors)])
                else:
                    g_incid.edge(clausetagN % clause[0],
                                 vartagN % -var,
                                 color=colors[-var % len(colors)],
                                 arrowtail='odot')  # style='dotted'

        # make edgelist variable-based (varX, clauseY), ...

        vcmapping = map(
            lambda y: map(
                lambda x: (
                    x,
                    y[0]),
                y[1]),
            self.edgelist)

        var_cl_iter = tuple(flatten(vcmapping))  # flatten
        #  var_cl_iter [(1, 1), (4, 1), (6, 1), (1, 2), (-5, 2), (-1, 3), (7, 3), (2, 4),
        #             (3, 4), (2, 5), (5, 5), (2, 6), (-6, 6), (3, 7), (-8, 7), (4, 8),
        #             (-8, 8), (-4, 9), (6, 9), (-4, 10), (7, 10)]

        bodybaselen = len(g_incid.body)
        for i, variables in enumerate(TIMELINE, start=1):    # all timesteps

            # reset highlighting
            g_incid.body = g_incid.body[:bodybaselen]
            if variables is None:
                g_incid.render(
                    view=view,
                    format='svg',
                    filename=_filename % i)
                continue

            emp_clause = {
                var_cl[1] for var_cl in filter(
                    lambda var_cl, s=variables: abs(var_cl[0]) in s,
                    var_cl_iter)}

            emp_var = {abs(var_cl[0]) for var_cl in filter(
                lambda var_cl, s=emp_clause: var_cl[1] in s, var_cl_iter)}

            for var in emp_var:
                _vartag = vartagN % abs(var)
                _style = 'solid,filled' if var in variables else 'dotted,filled'
                g_incid.node(
                    _vartag,
                    _vartag,
                    style=_style,
                    fillcolor='yellow')

            for cl in emp_clause:
                g_incid.node(
                    clausetagN %
                    cl,
                    clausetagN %
                    cl,
                    fillcolor='yellow')

            for edge in var_cl_iter:
                (var, clause) = edge

                _style = 'solid' if clause in emp_clause else 'dotted'
                _vartag = vartagN % abs(var)

                if var >= 0:
                    g_incid.edge(clausetagN % clause,
                                 _vartag,
                                 color=colors[var % len(colors)],
                                 style=_style)
                else:                                       # negated variable
                    g_incid.edge(clausetagN % clause,
                                 _vartag,
                                 color=colors[-var % len(colors)],
                                 arrowtail='odot',
                                 style=_style)

            g_incid.render(
                view=view,
                format='svg',
                filename=_filename % i)


if __name__ == "__main__":
    import argparse
    PARSER = argparse.ArgumentParser(
        prog='graphvizSatVisu.py',
        description='Visualizing Dynamic Programming on Treedecompositions.')
    PARSER.add_argument('infile', nargs='?',
                        type=argparse.FileType('r', encoding='UTF-8'))
    PARSER.add_argument('outfolder')

    ARGS = PARSER.parse_args()
    INFILE = ARGS.infile
    OUTFOLDER = ARGS.outfolder
    if not OUTFOLDER:
        OUTFOLDER = "outfolder"
    OUTFOLDER = OUTFOLDER.replace("\\", "/")
    if not OUTFOLDER.endswith('/'):
        OUTFOLDER += '/'

    VISU = Visualization(INFILE, OUTFOLDER, tdFile="TDStep",
                         primalFile="PrimalGraphStep",
                         incFile="IncidenceGraphStep")
    VISU.treeDecTimeline()

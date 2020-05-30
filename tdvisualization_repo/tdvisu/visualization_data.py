# -*- coding: utf-8 -*-
"""
Visualization Data

Created on Sat May 30 22:51:00 2020

@author: Martin Röbke

Copyright (C) 2020  Martin Röbke

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.
    If not, see https://www.gnu.org/licenses/gpl-3.0.html

"""


from dataclasses import dataclass, field
from typing import List, Union


@dataclass()
class IncidenceGraphData:
    """Class for holding different parameters for the incidence graph."""
    edges: list
    subgraph_name_one: str = 'clauses'
    subgraph_name_two: str = 'variables'
    var_name_one: str = ''
    var_name_two: str = ''
    infer_primal: bool = False
    infer_dual: bool = False
    primal_file: str = 'PrimalGraphStep'
    inc_file: str = 'IncidenceGraphStep'
    dual_file: str = 'DualGraphStep'
    fontsize: int = 16
    second_shape: str = 'diamond'
    column_distance: float = 0.5


@dataclass()
class GeneralGraphData:
    """Class for holding different parameters for the general graph."""
    edges: list
    graph_name: str = 'graph'
    subgraph_name_two: str = 'variables'
    var_name_one: str = ''
    var_name_two: str = ''
    infer_primal: bool = False
    infer_dual: bool = False
    fontsize: int = 16
    second_shape: str = 'diamond'
    column_distance: float = 0.5


@dataclass
class VisualizationData:
    """Class for holding different parameters for Visualization."""
    incidence_graph: Union[IncidenceGraphData, bool] = False
    general_graph: Union[GeneralGraphData, bool] = False
    colors: List = field(default_factory=lambda: ['#0073a1', '#b14923', '#244320', '#b1740f', '#a682ff',
                                                  '#004066', '#0d1321', '#da1167', '#604909', '#0073a1',
                                                  '#b14923', '#244320', '#b1740f', '#a682ff'])


if __name__ == "__main__":
    incid = IncidenceGraphData([])
    gen = GeneralGraphData([])
    data = VisualizationData(colors=['red', 'blue'])
    print(data)

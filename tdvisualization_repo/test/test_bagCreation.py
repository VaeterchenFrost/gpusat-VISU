# -*- coding: utf-8 -*-
""" Testing visualization.py"""

import unittest
from tdvisu.visualization import Visualization

__author__ = "Martin Röbke <martin.roebke@tu-dresden.de>"
__status__ = "development"
__date__ = "20 April 2020"


SOLUTIONTABLE1 = [["id", "0"], ["v1", "1"],
                  ["v2", "2"], ["v3", "4"],
                  ["nSol", "0"]]

SOLUTIONTABLEINT = [["id", 0], ["v1", 1],
                    ["v2", 2], ["v3", 4],
                    ["nSol", 0]]

SOLUTIONTABLEFLOAT = [["id", 0.1], ["v1", 1.],
                      ["v2", 2.2222], ["v3", 4.4],
                      ["nSol", 0.1]]


class TestSolutionNode(unittest.TestCase):
    def test_solutionNodeEmpty(self):
        result = Visualization.solution_node([])
        self.assertEqual(result, "{empty}")

    def test_solutionNodeEmptyTopLabel(self):
        result = Visualization.solution_node([], "top")
        self.assertEqual(result, "{top|empty}")

    def test_solutionNodeEmptyBottomLabel(self):
        result = Visualization.solution_node([], "", "bottom")
        self.assertEqual(result, "{empty|bottom}")

    def test_solutionNodeTranspose(self):
        result = Visualization.solution_node(
            SOLUTIONTABLE1, "top", "bottom", transpose=True)
        self.assertEqual(
            result, "{top|{{id|v1|v2|v3|nSol}|{0|1|2|4|0}}|bottom}")

    def test_solutionNodeFullTable(self):
        result = Visualization.solution_node(SOLUTIONTABLE1)
        self.assertEqual(result, "{{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}}")

        result = Visualization.solution_node(SOLUTIONTABLE1, "top", "bottom")
        self.assertEqual(
            result, "{top|{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}|bottom}")

    def test_solutionNodeLine(self):
        solutionTable = [["id"], ["v1"],
                         ["v2"], ["v3"],
                         ["nSol"]]
        result = Visualization.solution_node(solutionTable)
        self.assertEqual(result, "{{{id}|{v1}|{v2}|{v3}|{nSol}}}")

        result = Visualization.solution_node(solutionTable, "top", "bottom")
        self.assertEqual(result, "{top|{{id}|{v1}|{v2}|{v3}|{nSol}}|bottom}")

    def test_solutionNodeNumbers(self):
        result = Visualization.solution_node(SOLUTIONTABLEINT)
        self.assertEqual(result, "{{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}}")

        result = Visualization.solution_node(SOLUTIONTABLEFLOAT)
        self.assertEqual(
            result, "{{{id|0.1}|{v1|1.0}|{v2|2.2222}|{v3|4.4}|{nSol|0.1}}}")


if __name__ == '__main__':
    unittest.main()

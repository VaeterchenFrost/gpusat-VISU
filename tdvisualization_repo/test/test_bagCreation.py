""" Testing visualization.py
"""

import unittest
from tdvisu.visualization import Visualization


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
        result = Visualization.solutionNode([])
        self.assertEqual(result, "{empty}")

    def test_solutionNodeEmptyTopLabel(self):
        result = Visualization.solutionNode([], "top")
        self.assertEqual(result, "{top|empty}")

    def test_solutionNodeEmptyBottomLabel(self):
        result = Visualization.solutionNode([], "", "bottom")
        self.assertEqual(result, "{empty|bottom}")

    def test_solutionNodeTranspose(self):
        result = Visualization.solutionNode(
            SOLUTIONTABLE1, "top", "bottom", transpose=True)
        self.assertEqual(
            result, "{top|{{id|v1|v2|v3|nSol}|{0|1|2|4|0}}|bottom}")

    def test_solutionNodeFullTable(self):
        result = Visualization.solutionNode(SOLUTIONTABLE1)
        self.assertEqual(result, "{{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}}")

        result = Visualization.solutionNode(SOLUTIONTABLE1, "top", "bottom")
        self.assertEqual(
            result, "{top|{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}|bottom}")

    def test_solutionNodeLine(self):
        solutionTable = [["id"], ["v1"],
                         ["v2"], ["v3"],
                         ["nSol"]]
        result = Visualization.solutionNode(solutionTable)
        self.assertEqual(result, "{{{id}|{v1}|{v2}|{v3}|{nSol}}}")

        result = Visualization.solutionNode(solutionTable, "top", "bottom")
        self.assertEqual(result, "{top|{{id}|{v1}|{v2}|{v3}|{nSol}}|bottom}")

    def test_solutionNodeNumbers(self):
        result = Visualization.solutionNode(SOLUTIONTABLEINT)
        self.assertEqual(result, "{{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}}")

        result = Visualization.solutionNode(SOLUTIONTABLEFLOAT)
        self.assertEqual(
            result, "{{{id|0.1}|{v1|1.0}|{v2|2.2222}|{v3|4.4}|{nSol|0.1}}}")


if __name__ == '__main__':
    unittest.main()

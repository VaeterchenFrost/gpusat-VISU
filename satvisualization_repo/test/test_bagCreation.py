""" Testing graphvizSatVisu.py
"""


import satvisu.graphvizSatVisu as gv
solutionTable1 = [["id", "0"], ["v1", "1"],
                  ["v2", "2"], ["v3", "4"],
                  ["nSol", "0"]]

solutionTableInt = [["id", 0], ["v1", 1],
                    ["v2", 2], ["v3", 4],
                    ["nSol", 0]]
solutionTableFloat = [["id", 0.1], ["v1", 1.],
                      ["v2", 2.2222], ["v3", 4.4],
                      ["nSol", 0.1]]


def test_solutionNodeEmpty():
    result = gv.solutionNode([])
    assert result == "{<anchor> empty}"


def test_solutionNodeEmptyTopLabel():
    result = gv.solutionNode([], "top")
    assert result == "{<anchor> top|empty}"


def test_solutionNodeEmptyBottomLabel():
    result = gv.solutionNode([], "", "bottom")
    assert result == "{<anchor> empty|bottom}"


def test_solutionNodeTranspose():
    result = gv.solutionNode(solutionTable1, "top", "bottom", transpose=True)
    assert result == "{<anchor> top|{{id|v1|v2|v3|nSol}|{0|1|2|4|0}}|bottom}"


def test_solutionNodeFullTable():
    result = gv.solutionNode(solutionTable1)
    assert result == "{<anchor> {{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}}"
    result = gv.solutionNode(solutionTable1, "top", "bottom")
    assert result == "{<anchor> top|{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}|bottom}"


def test_solutionNodeLine():
    solutionTable = [["id"], ["v1"],
                     ["v2"], ["v3"],
                     ["nSol"]]
    result = gv.solutionNode(solutionTable)
    assert result == "{<anchor> {{id}|{v1}|{v2}|{v3}|{nSol}}}"
    result = gv.solutionNode(solutionTable, "top", "bottom")
    assert result == "{<anchor> top|{{id}|{v1}|{v2}|{v3}|{nSol}}|bottom}"


def test_solutionNodeNumbers():
    result = gv.solutionNode(solutionTableInt)
    assert result == "{<anchor> {{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}}"
    result = gv.solutionNode(solutionTableFloat)
    assert result == "{<anchor> {{id|0.1}|{v1|1.0}|{v2|2.2222}|{v3|4.4}|{nSol|0.1}}}"

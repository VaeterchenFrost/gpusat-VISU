""" Testing graphvizSatVisu.py
"""


import satvisu.graphvizSatVisu as gv


def test_solutionNodeEmpty():
    result = gv.solutionNode([])
    assert result == "{<anchor> |empty}"


def test_solutionNodeEmptyTopLabel():
    result = gv.solutionNode([], "top")
    assert result == "{<anchor> top|empty}"


def test_solutionNodeEmptyBottomLabel():
    result = gv.solutionNode([], "", "bottom")
    assert result == "{<anchor> |empty|bottom}"


def test_solutionNodeFullTable():
    solutionTable = [["id", "0"], ["v1", "1"],
                     ["v2", "2"], ["v3", "4"],
                     ["nSol", "0"]]
    result = gv.solutionNode(solutionTable)
    assert result == "{<anchor> |{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}}"
    result = gv.solutionNode(solutionTable, "top", "bottom")
    assert result == "{<anchor> top|{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}|bottom}"

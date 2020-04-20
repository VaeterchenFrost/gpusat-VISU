""" Testing graphvizSatVisu.py
"""


import satvisu.graphvizSatVisu as gv
SOLUTIONTABLE1 = [["id", "0"], ["v1", "1"],
                  ["v2", "2"], ["v3", "4"],
                  ["nSol", "0"]]

SOLUTIONTABLEINT = [["id", 0], ["v1", 1],
                    ["v2", 2], ["v3", 4],
                    ["nSol", 0]]
SOLUTIONTABLEFLOAT = [["id", 0.1], ["v1", 1.],
                      ["v2", 2.2222], ["v3", 4.4],
                      ["nSol", 0.1]]


def test_solutionNodeEmpty():
    result = gv.solutionNode([])
    assert result == "{empty}"


def test_solutionNodeEmptyTopLabel():
    result = gv.solutionNode([], "top")
    assert result == "{top|empty}"


def test_solutionNodeEmptyBottomLabel():
    result = gv.solutionNode([], "", "bottom")
    assert result == "{empty|bottom}"


def test_solutionNodeTranspose():
    result = gv.solutionNode(SOLUTIONTABLE1, "top", "bottom", transpose=True)
    assert result == "{top|{{id|v1|v2|v3|nSol}|{0|1|2|4|0}}|bottom}"


def test_solutionNodeFullTable():
    result = gv.solutionNode(SOLUTIONTABLE1)
    assert result == "{{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}}"
    result = gv.solutionNode(SOLUTIONTABLE1, "top", "bottom")
    assert result == "{top|{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}|bottom}"


def test_solutionNodeLine():
    solutionTable = [["id"], ["v1"],
                     ["v2"], ["v3"],
                     ["nSol"]]
    result = gv.solutionNode(solutionTable)
    assert result == "{{{id}|{v1}|{v2}|{v3}|{nSol}}}"
    result = gv.solutionNode(solutionTable, "top", "bottom")
    assert result == "{top|{{id}|{v1}|{v2}|{v3}|{nSol}}|bottom}"


def test_solutionNodeNumbers():
    result = gv.solutionNode(SOLUTIONTABLEINT)
    assert result == "{{{id|0}|{v1|1}|{v2|2}|{v3|4}|{nSol|0}}}"
    result = gv.solutionNode(SOLUTIONTABLEFLOAT)
    assert result == "{{{id|0.1}|{v1|1.0}|{v2|2.2222}|{v3|4.4}|{nSol|0.1}}}"

""" Testing graphvizSatVisu.py
"""

import pytest
import satvisu.graphvizSatVisu


def test_mytest():
    with pytest.raises(SystemExit):
        satvisu.graphvizSatVisu.texit()

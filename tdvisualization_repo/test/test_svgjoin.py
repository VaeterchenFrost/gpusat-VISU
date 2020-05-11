# -*- coding: utf-8 -*-
""" Testing svgjoin.py"""

import unittest
from unittest_expander import expand, foreach
from tdvisu.svgjoin import append_svg, new_height

__author__ = "Martin Röbke <martin.roebke@tu-dresden.de>"
__status__ = "development"
__date__ = "9 May 2020"

        
class TestNewHeight(unittest.TestCase):
    """Test the new_height method in svgjoin"""
    def test_newheight(self):
        
        self.assertEqual(True,True)

class TestSvgJoin(unittest.TestCase):
    """Test the append_svg method in svgjoin"""
    pass

if __name__ == '__main__':
    unittest.main()

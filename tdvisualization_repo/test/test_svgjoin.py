# -*- coding: utf-8 -*-
"""Testing svgjoin.py"""

import unittest
from random import randint
from unittest_expander import expand, foreach, param, paramseq
from tdvisu.svgjoin import new_height

__author__ = "Martin Röbke <martin.roebke@tu-dresden.de>"
__status__ = "development"
__date__ = "9 May 2020"

MIN = 5
MAX = 1e6
BASE = randint(40, 240)


def randomized(lower=MIN, upper=MAX):
    return randint(lower, upper)


def rand_smaller(number):
    return randomized(upper=number - 1)


def rand_larger(number):
    return randomized(lower=number + 1)


@expand
class TestNewHeight(unittest.TestCase):
    """Test the new_height method in svgjoin"""
    # Sizes considered for image-dimensions
    test_parameters = [
        # no baseline
        param({'h_one_': BASE, 'h_two_': BASE},
              expected=(0, BASE)).label('same'),
        param({'h_one_': BASE, 'h_two_': rand_smaller(BASE)},
              expected=(0, BASE)).label('smaller'),
        param({'h_one_': BASE, 'h_two_': BASE + 1},
              expected=(0, BASE + 1)).label('larger'),
        param({'h_one_': BASE, 'h_two_': BASE + 10},
              expected=(0, BASE + 10)).label('even larger'),
        # scale same size
        param({'h_one_': BASE, 'h_two_': rand_smaller(BASE), 'v_bottom': 0, 'v_top': 1},
              expected=(0, BASE)).label('small->same size'),
        param({'h_one_': BASE, 'h_two_': rand_larger(BASE), 'v_bottom': 0, 'v_top': 1},
              expected=(0, BASE)).label('large->same size'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 0, 'v_top': 1},
              expected=(0, BASE)).label('same size->same size')
    ]

    @foreach(test_parameters)
    def test_newheight(self, kargs, expected):
        if isinstance(kargs, dict):
            self.assertEqual(new_height(**kargs), expected)


class TestSvgJoin(unittest.TestCase):
    """Test the append_svg method in svgjoin"""
    pass


if __name__ == '__main__':
    import sys
    def run_tests(*test_case_classes):
        suite = unittest.TestSuite(
            unittest.TestLoader().loadTestsFromTestCase(cls)
            for cls in test_case_classes)
        unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    # run selected tests:
    run_tests(TestNewHeight)

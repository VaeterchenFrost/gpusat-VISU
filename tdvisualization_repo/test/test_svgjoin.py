# -*- coding: utf-8 -*-
"""Testing svgjoin.py"""

import unittest
from random import randint
from unittest_expander import expand, foreach, param, paramseq
from tdvisu.svgjoin import f_transform

__author__ = "Martin Röbke <martin.roebke@tu-dresden.de>"
__status__ = "development"
__date__ = "9 May 2020"

# Sizes considered for image-dimensions
MIN = 5
MAX = 1e6
BASE = randint(20, 3000)
last_random = None


def randomized(lower=MIN, upper=MAX):
    return randint(lower, upper)


def rand_larger(number):
    global last_random
    last_random = randomized(lower=number + 1)
    return last_random


def rand_smaller(number):
    global last_random
    last_random = randomized(upper=number - 1)
    return last_random


@expand
class TestNewHeight(unittest.TestCase):
    """Test the transform method in svgjoin"""

    test_parameters = [
        # no baseline
        param({'h_one_': BASE, 'h_two_': BASE},
              expected=(0, BASE, 1)).label('same'),
        param({'h_one_': BASE, 'h_two_': rand_smaller(BASE)},
              expected=(0, BASE, 1)).label('smaller'),
        param({'h_one_': BASE, 'h_two_': BASE + 1},
              expected=(0, BASE + 1, 1)).label('larger'),
        param({'h_one_': BASE, 'h_two_': BASE + 10},
              expected=(0, BASE + 10, 1)).label('even larger'),
        # scale same size
        param({'h_one_': BASE, 'h_two_': rand_smaller(BASE), 'v_bottom': 0, 'v_top': 1},
              expected=(0, BASE, BASE / last_random)).label('small->same size'),
        param({'h_one_': BASE, 'h_two_': rand_larger(BASE), 'v_bottom': 0, 'v_top': 1},
              expected=(0, BASE, BASE / last_random)).label('large->same size'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 0, 'v_top': 1},
              expected=(0, BASE, 1)).label('same size->same size'),
        # neutral
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 0},
              expected=(0, BASE, 1)).label('neutral v_bot=0'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_top': 1},
              expected=(0, BASE, 1)).label('neutral v_top=1'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 0, 'scale2': 1},
              expected=(0, BASE, 1)).label('neutral v_bot=0'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_top': 1, 'scale2': 1},
              expected=(0, BASE, 1)).label('neutral v_top=1'),
        # move without scale
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 0.5},
              expected=(0.5 * BASE, 1.5 * BASE, 1)).label('move up 0.5'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 1},
              expected=(BASE, 2 * BASE, 1)).label('move up 1'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': -0.5},
              expected=(-0.5 * BASE, 1.5 * BASE, 1)).label('move down 0.5'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': -1},
              expected=(-BASE, 2 * BASE, 1)).label('move down 1'),
        # just scale
        param({'h_one_': BASE, 'h_two_': BASE, 'scale2': 1},
              expected=(0, BASE, 1)).label('scale 1'),
        param({'h_one_': BASE, 'h_two_': BASE, 'scale2': 2},
              expected=(0, 2 * BASE, 2)).label('scale 2'),
        param({'h_one_': BASE, 'h_two_': 0.1 * BASE, 'scale2': 0.1},
              expected=(0, BASE, 0.1)).label('scale 2'),
        # move + scale
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 0.5, 'scale2': 1},
              expected=(0.5 * BASE, 1.5 * BASE, 1)).label('move up 0.5 s1'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 0.5, 'scale2': 2},
              expected=(0.5 * BASE, 2.5 * BASE, 2)).label('move up 0.5 scale=2'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 1, 'scale2': 1},
              expected=(BASE, 2 * BASE, 1)).label('move up 1 s1'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 1, 'scale2': 2},
              expected=(BASE, 3 * BASE, 2)).label('move up 1 scale=2'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': -0.5, 'scale2': 1},
              expected=(-0.5 * BASE, 1.5 * BASE, 1)).label('move down 0.5 s1'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': -0.5, 'scale2': 3},
              expected=(-0.5 * BASE, 3 * BASE, 3)).label('move down 0.5 scale=3'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': -1, 'scale2': 1},
              expected=(-BASE, 2 * BASE, 1)).label('move down 1 s1'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': -1, 'scale2': 0.5},
              expected=(-BASE, 2 * BASE, 0.5)).label('move down 1 scale=0.5')
    ]

    @foreach(test_parameters)
    def test_newheight(self, kargs, expected):
        if isinstance(kargs, dict):
            self.assertEqual(f_transform(**kargs), expected)


class TestSvgJoin(unittest.TestCase):
    """Test the append_svg method in svgjoin"""
    pass


if __name__ == '__main__':
    import sys

    def run_tests(*test_case_classes):
        suite = unittest.TestSuite(
            unittest.TestLoader().loadTestsFromTestCase(cls)
            for cls in test_case_classes)
        unittest.TextTestRunner(stream=sys.stdout, verbosity=1).run(suite)
    # run selected tests:
    run_tests(TestNewHeight)

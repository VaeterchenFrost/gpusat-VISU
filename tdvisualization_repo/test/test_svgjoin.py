# -*- coding: utf-8 -*-
"""Testing svgjoin.py"""

import unittest
from random import randint
from benedict import benedict
from unittest_expander import expand, foreach, param

from tdvisu.svgjoin import f_transform, append_svg

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
        # moving centerline: v_bot=v_top
        param({'h_one_': BASE, 'h_two_': 0.5 * BASE, 'v_bottom': 0.5, 'v_top': 0.5},
              expected=(0.25 * BASE, BASE, 1)).label('centerline 0.5'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 0, 'v_top': 0},
              expected=(-0.5 * BASE, 1.5 * BASE, 1)).label('centerline 0 (0)'),
        param({'h_one_': 2 * BASE, 'h_two_': BASE, 'v_bottom': 0, 'v_top': 0},
              expected=(-0.5 * BASE, 2.5 * BASE, 1)).label('centerline 0 (1)'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': -0.1, 'v_top': -0.1},
              expected=(-0.6 * BASE, 1.6 * BASE, 1)).label('centerline -0.1'),
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
            result = f_transform(**kargs).values()
            for pos, (actual, expected) in enumerate(zip(result, expected)):
                self.assertAlmostEqual(actual, expected,
                                       msg="(Problem on index %d)" % pos)


class TestSvgJoin(unittest.TestCase):
    """Test the append_svg method in svgjoin"""

    def test_simple_join(self):
        """Combine two example svg images to a new one - compare to result."""
        with open('IncidenceGraphStep11.svg') as file1:
            im_1 = benedict.from_xml(file1.read())
            with open('PrimalGraphStep11.svg') as file2:
                im_2 = benedict.from_xml(file2.read())
                result = append_svg(im_1, im_2)
                result['svg']['@preserveAspectRatio'] = "xMinYMin"
                # to write:
                # with open('result_simple_join.svg', "w") as file:
                #     result.to_xml(output=file, pretty=True)
                with open('result_simple_join.svg', 'r') as expected:
                    self.assertEqual(
                        result, benedict.from_xml(
                            expected.read()))


if __name__ == '__main__':
    import sys

    def run_tests(*test_case_classes):
        suite = unittest.TestSuite(
            unittest.TestLoader().loadTestsFromTestCase(cls)
            for cls in test_case_classes)
        unittest.TextTestRunner(stream=sys.stdout, verbosity=1).run(suite)
    # run selected tests:
    run_tests(TestNewHeight, TestSvgJoin)

# -*- coding: utf-8 -*-
"""Testing svgjoin.py 
Might want to consider using unittest.TestCase.assertAlmostEqual in some cases.
"""

import unittest
from random import randint
from benedict import benedict
from unittest_expander import expand, foreach, param

from tdvisu.svgjoin import f_transform, append_svg

__author__ = "Martin Röbke <martin.roebke@tu-dresden.de>"
__status__ = "development"
__date__ = "27 May 2020"

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

    test_parameters_default = [
        param({'h_one_': BASE, 'h_two_': BASE},
              expected={'vertical_snd': 0.0, 'vertical_fst': 0.0, 'combine_height': BASE,
                        'scale2': 1}).label('Only heights (same)'),
        param({'h_one_': BASE, 'h_two_': 2 * BASE},
              expected={'vertical_snd': 0.0, 'vertical_fst': 0.0, 'combine_height': 2 * BASE,
                        'scale2': 1}).label('Only heights (larger)'),
        param({'h_one_': BASE, 'h_two_': 0.5 * BASE},
              expected={'vertical_snd': 0.0, 'vertical_fst': 0.0, 'combine_height': BASE,
                        'scale2': 1}).label('Only heights (smaller)'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': None},
              expected={'vertical_snd': 0.0, 'vertical_fst': 0.0, 'combine_height': BASE,
                        'scale2': 1}).label('Default v_bottom'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': None, 'v_top': None},
              expected={'vertical_snd': 0.0, 'vertical_fst': 0.0, 'combine_height': BASE,
                        'scale2': 1}).label('Default v_bottom&v_top'),
        param({'h_one_': BASE, 'h_two_': BASE, 'scale2': 1},
              expected={'vertical_snd': 0.0, 'vertical_fst': 0.0, 'combine_height': BASE,
                        'scale2': 1}).label('Default scale2')]
    
    test_parameters_moving = [
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 1, 'v_top': 0},
              expected={'vertical_snd': 0.0, 'vertical_fst': 0.0, 'combine_height': BASE,
                        'scale2': 1}).label('static'),
        param({'h_one_': BASE, 'h_two_': BASE, 'v_bottom': 0, 'v_top': 1},
              expected={'vertical_snd': 0.0, 'vertical_fst': 0.0, 'combine_height': BASE,
                        'scale2': 1}).label("switched bottom and top -> "
                                            "should switch automatically!"),
        param({'h_one_': BASE, 'h_two_': rand_smaller(BASE), 'v_bottom': 1, 'v_top': 0},
              expected={'vertical_snd': BASE-last_random, 'vertical_fst': 0.0, 'combine_height': BASE,
                        'scale2': BASE/last_random}).label('scale up to BASE'),
        param({'h_one_': BASE, 'h_two_': rand_larger(BASE), 'v_bottom': 1, 'v_top': 0},
              expected={'vertical_snd': BASE-last_random, 'vertical_fst': 0.0, 'combine_height': BASE,
                        'scale2': BASE/last_random}).label('scale down to BASE'),
    ]

    @foreach(test_parameters_default)
    def test_parameters_default(self, kargs, expected):
        if isinstance(kargs, dict):
            result = f_transform(**kargs)
            self.assertEqual(result, expected)

    @foreach(test_parameters_moving)
    def test_parameters_moving(self, kargs, expected):
        if isinstance(kargs, dict):
            result = f_transform(**kargs)
            self.assertEqual(result, expected)


class TestSvgJoin(unittest.TestCase):
    """Test the append_svg method in svgjoin"""

    def test_simple_join(self):
        """Combine two example svg images to a new one - compare to result."""
        with open('IncidenceGraphStep11.svg') as file1:
            im_1 = benedict.from_xml(file1.read())
            with open('PrimalGraphStep11.svg') as file2:
                im_2 = benedict.from_xml(file2.read())
                result = append_svg(im_2, im_1,0,1)
                result['svg']['@preserveAspectRatio'] = "xMinYMin"
                # to write:
                with open('result_simple_join.svg', "w") as file:
                    result.to_xml(output=file, pretty=True)
                # with open('result_simple_join.svg', 'r') as expected:
                #     self.assertEqual(result, benedict.from_xml(expected.read()))


if __name__ == '__main__':
    import sys

    def run_tests(*test_case_classes):
        suite = unittest.TestSuite(
            unittest.TestLoader().loadTestsFromTestCase(cls)
            for cls in test_case_classes)
        unittest.TextTestRunner(stream=sys.stdout, verbosity=1).run(suite)
    # run selected tests:
    run_tests(TestNewHeight, TestSvgJoin)

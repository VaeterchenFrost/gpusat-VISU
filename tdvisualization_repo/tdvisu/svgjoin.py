# -*- coding: utf-8 -*-
"""Load and manipulate svg images. Could also be streamed as string."""

import re
import logging
from benedict import benedict
from typing import Tuple

__author__ = "Martin Röbke <martin.roebke@tu-dresden.de>"
__status__ = "development"
__version__ = "0.1"
__date__ = "29 April 2020"

LOGGER = logging.getLogger(__name__)


def append_svg(first_dict: dict, snd_dict: dict,
               centerpad: float = 0., v_bottom=None, v_top=None) -> dict:
    """
    Modifies the first of two xml-svg dictionary containing a viewbox to
    append the second svg to the right of the first image.
    The second svg should only have ONE group 'g'.

    The value of the viewBox attribute is a list of four numbers:
        min-x, min-y, width and height.
        The numbers separated by whitespace and/or a comma,
        which specify a rectangle in user space which is mapped to the
        bounds of the viewport established for the associated SVG element.

    See also <https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox>

    Parameters
    ----------
    first_dict : dict
        Dictionary with key 'svg' including one or more 'g' elements and a
        '@viewBox' attribute.
    snd_dict : dict
        Dictionary with key 'svg' including one 'g' element and a '@viewBox' attribute.
    centerpad : float, optional
        Additional padding in units between the two images. The default is 0.
    v_baseline : float, optional
        Vertical baseline for the second image relative to the size of the first.
        The baseline adjusts the relative height (0->bottom, 1->top) and could
        even be negative or greater than one.

    Returns
    -------
    dict
        The extended result in the first_dict.

    """

    # indices
    WIDTH = 2
    HEIGHT = 3
    first_svg = first_dict['svg']
    second_svg = snd_dict['svg']

    # get viewbox
    pattern = re.compile(r'\s*,\s*|\s+')
    viewbox1 = re.split(pattern, first_svg['@viewBox'])
    viewbox2 = re.split(pattern, second_svg['@viewBox'])
    h_displacement = float(viewbox1[WIDTH]) + centerpad
    # adjust viewbox of first svg
    viewbox1[WIDTH] = str(
        h_displacement + float(viewbox2[WIDTH]))

    (v_displacement, combine_height) = new_height(
        viewbox1[HEIGHT], viewbox2[HEIGHT], v_bottom, v_top)
    viewbox1[HEIGHT] = str(combine_height)

    first_svg['@viewBox'] = ' '.join(viewbox1)
    # drop width,height
    first_svg.pop("@width", None)
    first_svg.pop("@height", None)
    # move second image group next to first
    transform = second_svg['g'].get('@transform', '')
    if transform:
        transform += ' '
    # v_displacement goes top->bottom, so negative w.r.t. "height"
    transform += 'translate(%f %f)' % (h_displacement, -v_displacement)
    second_svg['g']['@transform'] = transform
    # add group to list of 'g'
    if isinstance(first_svg['g'], list):
        first_svg['g'].append(second_svg['g'])
    else:
        first_svg['g'] = [first_svg['g'], second_svg['g']]

    return first_dict


def new_height(h_one_, h_two_, v_bottom=None,
               v_top=None, scale2=None) -> Tuple[float, float]:
    """
    Calculate vertical position of second image.
    The scale is in units from
    0: bottom of first image
    1: top of first image


               ----------v_top
    ---------1 |        |
    |       |  |        |
    | first |  | second |
    |       |  |        |
    ---------0 |        |
               ----------v_bottom


    Parameters
    ----------
    h_one_ : float-like
        Height of the first image.
    h_two_ : float-like
        Height of the second image.
    v_bottom : float or str, optional
        DESCRIPTION. The default is None.
    v_top : float or str, optional
        DESCRIPTION. The default is None.
    scale2: float, optional
        Scale the second image. Only used if either v_bottom or v_top is None.

    Returns
    -------
    Tuple[float, float]
        v_displacement, combine_height.

    """
    # cast to float
    h_one = float(h_one_)
    h_two = float(h_two_)
    # normalize values
    if v_bottom == 'bottom':
        v_bottom = 0
    elif v_bottom == 'center':
        v_bottom = 0.5
    elif v_bottom == 'top':
        v_bottom = 1
    elif v_bottom == -float('inf'):
        v_bottom = 0
    elif v_bottom == float('inf'):
        v_bottom = 1
    if v_top == 'bottom':
        v_top = 0
    elif v_top == 'center':
        v_top = 0.5
    elif v_top == 'top':
        v_top = 1
    elif v_top == -float('inf'):
        v_top = 0
    elif v_top == float('inf'):
        v_top = 1   
    # exceptions (special case None)
    if v_top is not None and v_bottom == v_top:
        LOGGER.warning("The values of 'v_top', 'v_bottom' are both interpreted "
                       "as %f - skipping vertical adjustment!", v_top, exc_info=1)
        v_bottom = v_top = None
    # calc v_displacement
    if v_bottom is not None:
        displacement = v_bottom * h_one
    # calc combine_height

    return (0, max(h_one, h_two))


def main():
    with open('test/TDStep1.svg') as file:
        tdstep = benedict.from_xml(file.read())
    with open('test/PrimalGraphStep1.svg') as file:
        primal = benedict.from_xml(file.read())
    with open('test/IncidenceGraphStep1.svg') as file:
        incid = benedict.from_xml(file.read())

    padding = 40
    result = append_svg(tdstep, incid, padding)
    result = append_svg(result, primal, padding)
    # https://css-tricks.com/scale-svg/#article-header-id-1
    result['svg']['@preserveAspectRatio'] = "xMinYMin"
    with open("benedict.svg", "w") as file:
        result.to_xml(output=file, pretty=True)


if __name__ == "__main__":
    main()

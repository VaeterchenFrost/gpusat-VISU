# -*- coding: utf-8 -*-
"""Load and manipulate svg images. Could also be streamed as string."""

import re
import logging
from benedict import benedict
from typing import Tuple

__author__ = "Martin Röbke <martin.roebke@tu-dresden.de>"
__status__ = "development"
__version__ = "0.2"
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

    (v_displacement, combine_height, scale2) = f_transform(
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


def f_transform(h_one_, h_two_, v_bottom=None,
                v_top=None, scale2=None) -> Tuple[float, float, float]:
    """
    Calculate vertical position of second image.
    The scale is in units from
    0: bottom of first image
    1: top of first image
    v_displacement is the difference of both baselines (bottom).


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
    Tuple[float, float, float]
        v_displacement, combine_height, scale2.

    """
    if scale2 is None:
        scale2 = 1
    v_displacement = 0
    # cast to float
    h_one = float(h_one_)
    h_two = float(h_two_)
    # normalize values
    conversion = {'bottom': 0, 'center': 0.5, 'top': 1,
                  -float('inf'): 0, float('inf'): 1}
    v_bottom = conversion.get(v_bottom, v_bottom)
    v_top = conversion.get(v_top, v_top)
    # cases (special case None)

    # same value
    if v_top is not None and v_bottom == v_top:
        LOGGER.warning("The values of 'v_top', 'v_bottom' are both interpreted "
                       "as %f - skipping vertical adjustment!", v_top, exc_info=1)
        v_bottom = v_top = None

    if v_bottom is not None:
        if v_top is not None:
            if v_bottom > v_top:  # swap
                v_top, v_bottom = v_bottom, v_top
            # scaling
            scale2 = (v_top - v_bottom) * h_one / h_two
            # height
        v_displacement = v_bottom * h_one
    elif v_top is not None:  # v_bottom now None
        size2 = h_two * scale2
        v_displacement = h_one * v_top - size2

    size2 = h_two * scale2
    combine_height = (max(h_one, v_displacement + size2) -
                      min(0, v_displacement))

    return (v_displacement, combine_height, scale2)


def main():
    # with open('test/TDStep1.svg') as file:
    #     tdstep = benedict.from_xml(file.read())
    # with open('test/PrimalGraphStep1.svg') as file:
    #     primal = benedict.from_xml(file.read())
    # with open('test/IncidenceGraphStep1.svg') as file:
    #     incid = benedict.from_xml(file.read())

    # padding = 40
    # result = append_svg(tdstep, incid, padding)
    # result = append_svg(result, primal, padding)
    padding = 40
    num_images = 14
    folder = "generalgraphNoDijkstra/"
    resultname = folder + "generalgraph%d.svg"
    names = [folder + 'TDStep%d.svg', folder + 'graph%d.svg']

    for step in range(1, num_images + 1):
        # first - needs at least two images
        with open(names[0] % step) as file:
            im_1 = benedict.from_xml(file.read())
        with open(names[1] % step) as file:
            im_2 = benedict.from_xml(file.read())
        result = append_svg(im_1, im_2, padding)
        # rest:
        for name in names[2:]:
            with open(name % step) as file:
                image = benedict.from_xml(file.read())
            result = append_svg(result, image, padding)

        # https://css-tricks.com/scale-svg/#article-header-id-1
        result['svg']['@preserveAspectRatio'] = "xMinYMin"
        with open(resultname % step, "w") as file:
            result.to_xml(output=file, pretty=True)


if __name__ == "__main__":
    main()

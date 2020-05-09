# -*- coding: utf-8 -*-
"""
Load and manipulate svg images. Could also be streamed as string.
Created on 2020-04-29 13:15:38

@author: Martin Röbke
"""

import re
from benedict import benedict


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
    result['svg']['@preserveAspectRatio'] = "xMinYMin"
    with open("benedict.svg", "w") as file:
        result.to_xml(output=file)


def append_svg(first_dict: dict, snd_dict: dict, centerpad: float = 0., v_baseline:float=1.) -> dict:
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
    displacement = float(viewbox1[WIDTH]) + centerpad
    # adjust viewbox of first svg
    viewbox1[WIDTH] = str(
        displacement + float(viewbox2[WIDTH]))

    viewbox1[HEIGHT] = str(
        max(float(viewbox1[HEIGHT]), float(viewbox2[HEIGHT])))

    first_svg['@viewBox'] = ' '.join(viewbox1)
    # drop width,height
    first_svg.pop("@width", None)
    first_svg.pop("@height", None)
    # move second image group next to first
    transform = second_svg['g'].get('@transform', '')
    if transform:
        transform += ' '
    transform += 'translate(%f)' % (displacement)
    second_svg['g']['@transform'] = transform
    # add group to list of 'g'
    if isinstance(first_svg['g'], list):
        first_svg['g'].append(second_svg['g'])
    else:
        first_svg['g'] = [first_svg['g'], second_svg['g']]

    return first_dict


if __name__ == "__main__":
    main()

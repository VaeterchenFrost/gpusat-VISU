# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:31:12 2020
Example setup.py:
    https://github.com/python/mypy/edit/master/setup.py
    https://github.com/xflr6/graphviz/blob/master/setup.py

@author: Martin Röbke
"""

import io
from setuptools import setup
tests_require = ['unittest_expander']
description = "Visualizing dynamic programming on tree decompositions."

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Multimedia :: Graphics :: Presentation'
]

setup(name="tdvisu",
      version="0.4",
      description=description,
      url="https://github.com/VaeterchenFrost/gpusat-VISU",
      author="Martin Röbke",
      author_email="martin.roebke@mailbox.tu-dresden.de",
      license='GPLv3',
      packages=['tdvisu'],
      platforms='any',
      install_requires=['graphviz', 'psycopg2', 'python-benedict'],
      extras_require={'test': tests_require},
      # long_description=io.open('README.txt', encoding='utf-8').read(),
      classifiers=classifiers,
      keywords='graph visualization dynamic-programming msol-solver')

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:31:12 2020

@author: Martin Röbke
"""

from setuptools import setup

setup(name="tdvisu",
      version="0.3",
      description="Visualizing dynamic programming on tree decompositions.",
      url="https://github.com/VaeterchenFrost/gpusat-VISU",
      author="Martin Röbke",
      author_email="Martin.Roebke@mailbox.tu-dresden.de",
      packages=['tdvisu'],
      install_requires=[
          'pygraphviz','psycopg2','python-benedict'
      ],
      zip_safe=False)

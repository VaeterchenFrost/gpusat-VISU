# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:52:35 2020

@author: Martin
"""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

img=mpimg.imread("incidenceGraph.png")
plt.axis("off")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6,12), dpi=600, frameon=False, tight_layout=True)
for elem in (ax1, ax2):
    elem.axes.get_xaxis().set_visible(False)
    elem.axes.get_yaxis().set_visible(False)
print(fig.get_size_inches())
ax1.imshow(img)
ax2.imshow(mpimg.imread("g41Digraph.png"))

plt.show()

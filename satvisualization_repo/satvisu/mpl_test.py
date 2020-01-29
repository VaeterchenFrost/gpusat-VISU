# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:52:35 2020

@author: Martin
"""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

if __name__=="__main__":
    img=mpimg.imread("incidenceGraph.png")
    _figsize=(img.shape[1]/50, img.shape[0]/100)
    plt.axis("off")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=_figsize, dpi=300, frameon=False, tight_layout=True)
    for elem in (ax1, ax2):
        elem.axes.get_xaxis().set_visible(False)
        elem.axes.get_yaxis().set_visible(False)
    print(fig.get_size_inches())
    ax1.imshow(img)
    ax2.imshow(mpimg.imread("g41Digraph.png"))
    
    plt.savefig("combined")
    
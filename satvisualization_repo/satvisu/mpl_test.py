# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:52:35 2020

@author: Martin
"""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

if __name__ == "__main__":
    num = 8  # 0-8
    img1 = mpimg.imread("g41DigraphProgress%d.png" % num)
    img2 = mpimg.imread("incidenceGraph%d.png" % num)
    _figsize = (max(img1.shape[1], img2.shape[1]) /
                100, max(img1.shape[0], img1.shape[0]) / 200)

    for i in range(num, -1, -1):
        img1 = mpimg.imread("g41DigraphProgress%d.png" % i)
        img2 = mpimg.imread("incidenceGraph%d.png" % i)

        plt.axis("off")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=_figsize,
                                       dpi=250, frameon=False, tight_layout=False)
        for elem in (ax1, ax2):
            elem.axis('off')
        fig.patch.set_visible(False)

        print(fig.get_size_inches())
        ax1.imshow(img1)
        ax2.imshow(img2)

        plt.savefig("combined%d" % i)

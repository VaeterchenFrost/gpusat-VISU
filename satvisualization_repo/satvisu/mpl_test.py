# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:52:35 2020

@author: Martin
"""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

if __name__ == "__main__":

    readfolder = "results31Test\\"
    writefolder = "results\\"
    num = 6

    img1 = mpimg.imread(readfolder + "g41DigraphProgress%d.png" % num)
    img2 = mpimg.imread(readfolder + "incidenceGraph%d.png" % num)
    img3 = mpimg.imread(readfolder + "primalGraph%d.png" % num)
    _figsize = ((img1.shape[1] + img2.shape[1] + img3.shape[1]) / 300 * 2.54,
                max(img1.shape[0], img2.shape[0], img3.shape[0]) / 300 * 2.54)

    for i in range(num, 0, -1):
        img1 = mpimg.imread(readfolder + "g41DigraphProgress%d.png" % i)
        img2 = mpimg.imread(readfolder + "incidenceGraph%d.png" % i)
        img3 = mpimg.imread(readfolder + "primalGraph%d.png" % i)

        plt.axis("off")
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=_figsize,
                                            dpi=300, frameon=False, tight_layout=False)
        for elem in (ax1, ax2, ax3):
            elem.axis('off')
        fig.patch.set_visible(False)

        print(fig.get_size_inches())
        ax1.imshow(img1)
        ax2.imshow(img2)
        ax3.imshow(img3)

        plt.savefig(writefolder + "combined%d" % i)

# Bachelor Thesis
Visualization for [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) on [tree decompositions](https://en.wikipedia.org/wiki/Tree_decomposition).

Main work in this repo will be done in [Bachelor](https://github.com/VaeterchenFrost/gpusat-VISU/tree/master/Bachelor) .

The Kolloquium talk can be found [here](https://github.com/VaeterchenFrost/gpusat-VISU/blob/e88aa38986548c59924b097b447dad6d9371eba4/Beamer-intro/beamer-intro/PresentationBa.pdf) .

The discussed sourcecode can be found via [GitHub TDVisu](https://github.com/VaeterchenFrost/tdvisu/).

# Task definition

Dynamic programming algorithms can be used to solve combinatorial problems such as SAT, Model Counting, and various graph problems.


The algorithms exploit structural properties in the given problem instance and solve the problem faster if for example the treewidth of a graph representation is small, since they usually run exponentially in the treewidth and polynomially in the size of the input instance. In fact, recent research showed that implementations of dynamic programming algorithms can also compete with modern solvers and even outperform them in projected model counting. 

Unfortunately, those algorithms are fairly hard to implement. While recent approaches have also investigated on allowing for easier implementations of dynamic programming algorithms on tree decompositions, implementations are still incredibly error prone, in particular, since they often involve bit fiddling and low level operations to make them run efficiently. Investigate how to automatically visualize dynamic programming algorithms based on existing implementations. Integrate your tool into at least one existing implementation, explain details on your implementation, how the visualization works, and show how this can be used for debugging algorithms.

------------------------


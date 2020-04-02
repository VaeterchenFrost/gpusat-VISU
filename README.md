# gpusat-VISU
Visualization API for GPUSAT

# Using
Graphviz2.38

pygraphviz-1.5-py3.7

# How to use
Run the python file with the above dependencies installed:
[visualization.py](https://github.com/VaeterchenFrost/gpusat-VISU/blob/master/satvisualization_repo/satvisu/visualization.py)

The input JSON might be produced with help of running [gpusat](https://github.com/VaeterchenFrost/GPUSAT) with option preprocessing disabled (-p).


**visualization.py** takes two parameters, the json-**infile** to read from, and optionally one **outputfolder**.
With both arguments a call from IPython might look like this:

```python
runfile(
'C:/Users/Martin/Documents/GitHub/gpusat-VISU/satvisualization_repo/satvisu/visualization.py', 
args='visugpusat.json examplefolder', 
wdir='C:/Users/Martin/Documents/GitHub/gpusat-VISU/satvisualization_repo/satvisu')
```

It produces 3 kinds of graphs suffixed with a running integer to represent timesteps:

+ *TDStep* the tree decomposition with solved nodes
+ *PrimalGraphStep* the primal graph with currently active variables
+ *IncidenceGraphStep* the bipartite incidence graph with active clauses/variables

Currently the graphs are images encoded in resolution independent **.svg files** (see https://www.lifewire.com/svg-file-4120603)


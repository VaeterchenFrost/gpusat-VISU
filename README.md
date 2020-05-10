# gpusat-VISU
Visualization API for [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) on [tree decompositions](https://en.wikipedia.org/wiki/Tree_decomposition).

# Using
[Alubbock:Graphviz](https://anaconda.org/alubbock/graphviz) (or [Graphviz (>=2.38)](https://graphviz.gitlab.io/download/))

[python-benedict](https://pypi.org/project/python-benedict/)

[for dpdb: psycopg2 (2.8.5)](https://www.psycopg.org/docs/index.html)

# How to install

After downloading the latest verion, go to the source-directory. 

With [Conda](https://docs.conda.io/en/latest/) on the system installed, the dependencies for this project can be automatically installed in a new environment:

Open a conda-command prompt with admin-privileges and run the commands
```shell
conda env create -f .\environment.yml
```
to create the environment with basic dependencies
```shell
conda activate tdvisu
```
to activate the environment
```shell
dot.exe -c
```
to register the plugins
```shell
python .\setup.py install
```
to install the project in the environment
```shell
python .\tdvisu\visualization.py -h
```
to confirm the visualization finds all dependencies.
```shell
python -m unittest
```
to run all tests.


# How to use
Run the python file with the above dependencies installed:
[visualization.py](https://github.com/VaeterchenFrost/gpusat-VISU/blob/master/satvisualization_repo/satvisu/visualization.py)

The input JSON is for example produced with help of running [gpusat](github.com/VaeterchenFrost/GPUSAT) and *--visufile filename* (optionally disabling preprocessing with *-p*.

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


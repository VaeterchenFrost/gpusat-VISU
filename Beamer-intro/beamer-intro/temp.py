
from graphviz import Digraph

def usage():
    g = Digraph('UsageCourcelle', strict=True, encoding="UTF8",
                node_attr={'fontsize':'20', 'fontcolor':'black', 'shape':'rect', 'fontname':'Arial'},
                graph_attr={'rankdir':'LR', 'splines':'ortho'},
                edge_attr={'minlen':'2'})
    g.edge('dev', 'MSO', constraint='false', minlen='1')
    g.node('inst', 'input to problem')
    g.node('problem', 'problem-encoding')
    g.node('dev', 'developer', style='rounded')
    g.node('MSO', 'MSO Solver')
    g.node('sol', 'solution')
    g.edges([('inst', 'MSO'),('problem', 'MSO'),('MSO', 'sol')])
    
    g.render(view=True, format='png')

def main(): 
    g = Digraph('Theory around #SAT Solving', strict=True, encoding="UTF8",
                node_attr={'fontsize':'20', 'fontcolor':'blue', 'fontname':'Arial'},
                graph_attr={'rankdir':'TB'},
                edge_attr={'color':'#e08e22'})
    
    
    g.node('MSOL', r'Monadic second-order logic')
    g.node('Courcelle', r"Courcelle's theorem")
    g.node('CT', "- every graph property \n"
           "- definable in the monadic second-order logic of graphs\n"
           "- can be decided in linear time on graphs\n"
           "- of bounded treewidth", fontsize='24', fontcolor='black',shape='box',style='rounded')
    g.node('SOL', "Second-order logic")
    g.node('FOL', "First-order logic")
    g.node('PropCal', "Propositional logic")
    
    g.edges([('FOL', 'SOL' ), ('PropCal', 'FOL'), ('FOL', 'MSOL'), ('MSOL', 'SOL')])
    g.edge('Courcelle', 'CT', dirType='both', penwidth='3.0', color='red', style='dashed')
    g.edge('MSOL', 'Courcelle', minlen='2')
    g.render(view=True, format='png')

if __name__=="__main__":
    main() 
    #usage()
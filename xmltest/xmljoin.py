# -*- coding: utf-8 -*-
"""
Load and manipulate svg images. Could also be streamed as string.
Created on Mon Apr 27 22:18:54 2020

@author: Martin Röbke
"""

from benedict import benedict


def main():
    with open('TDStep1.svg') as f1:
        r1=benedict.from_xml(f1.read())
    with open('PrimalGraphStep1.xml') as f2:
        r2=benedict.from_xml(f2.read())
    with open('IncidenceGraphStep1.svg') as f3:
        r3=benedict.from_xml(f3.read())
        
    x1,x2,x3=[r['svg']['@viewBox'].split() for r in (r1,r2,r3)]
    print(x1,x2,x3)
    x2[2] = float(x1[2]) + float(x2[2])
    x3[2] = x2[2] + float(x3[2])
    print(x1,x2,x3)
    import json
    with open("dicts.txt", mode="a") as f:
        f.write(json.dumps(json.loads(str(r1).replace("'",'"')),indent=2))
        f.write(json.dumps(json.loads(str(r2).replace("'",'"')),indent=2))
        f.write(json.dumps(json.loads(str(r3).replace("'",'"')),indent=2))
                


if __name__=="__main__": main()

# Second version of the JSON format used to describe MSOL visualization on tree decompositions

Changelog: 16.04.

- removed **clausesJson** (now "incidenceGraph")
- added **generalGraph** (e.g. for problems like vertex cover)
    - has a "graphName"
    - "varName" defaulting to just the number
    - "edges" (assumed undirected) as pairs of vertices
- added **incidenceGraph** (e.g. for problems with sat-clauses)
    - names for both partitions, defaulting to 'clauses' and 'variables'
    - naming-format for nodes in both partitions defaulting to just the number
    - current default behaviour was to infer the primal graph from the clauses\
        now controlled by the flags **inferPrimal** and **inferDual**


```perl
{
    "incidenceGraph" : false or
    {
    	Optional("subgraphNameOne" : STR, default='clauses'),
    	Optional("subgraphNameOne" : STR, default='variables'),

    	Optional("varNameOne" : STR, default='%d'),
    	Optional("varNameTwo" : STR, default='%d'),

        Optional("inferPrimal" : BOOLEAN, default=false),
        Optional("inferDual" : BOOLEAN, default=false),

        "edges" : [
            {"id" : INT (subgraphOneId), 
            "list" : [INT...]
            }
            ...
        ]
    },

    "generalGraph" : false or
    {
        "graphName" : STR,

        Optional("varName" : STR, default='%d'),

        "edges" : [
            [INT, INT],
            ...
        ]
    },

    "tdTimeline" : 
    [
        [INT (bagId)] or 
        [INT (bagId) or [INT(bagId), INT(bagId)], 
            [[
                [(firstrow)...],
                [(secondrow)...],
                ...
            ]
            ,STR (header)
            ,STR (footer)
            ,BOOL (transpose)
            ]
        ]
        ...
    ],

    "treeDecJson" : 
    {
        "bagpre" : STR,
        "edgearray" : 
            [[INT, INT]...],
        "labeldict" : 
            [
                {
                    "id" : INT (bagId),
                    "items" : [ INT... ],
                    "labels" : [ STR... ]
                }
                ...
            ],
         "numVars" : INT
    }

}

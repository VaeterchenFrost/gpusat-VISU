# First version of the JSON format used to describe SharpSat visualization on tree decompositions

```perl
{
    "clausesJson" : 
    [
        {"id" : INT (clauseId), 
        "list" : [INT...]
        }
        ...
    ],
    "tdTimeline" : 
    [
        [INT (bagId)] OR 
        [INT (bagId) OR [INT(bagId), INT(bagId)], 
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

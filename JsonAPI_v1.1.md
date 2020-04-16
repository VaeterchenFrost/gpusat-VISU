# Second version of the JSON format used to describe MSOL visualization on tree decompositions

Changelog: 

- added 


```perl
{
    "incidenceGraph" : false OR
    {
    	"subgraphNameOne" : STR,
    	"subgraphNameTwo" : STR,

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

    "generalGraph" : false OR
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

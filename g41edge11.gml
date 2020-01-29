Creator	"yFiles"
Version	"2.16"
graph
[
	hierarchic	1
	label	""
	directed	1
	node
	[
		id	0
		label	"bag 2"
		graphics
		[
			x	441.5
			y	62.5
			w	15.0
			h	15.0
			type	"ellipse"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 2"
			fontSize	12
			fontName	"Dialog"
			anchor	"w"
		]
		LabelGraphics
		[
			text	"[ 1 2 5 ]"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
	]
	node
	[
		id	1
		label	"bag 2"
		graphics
		[
			x	445.0
			y	118.0
			w	30.0
			h	30.0
			type	"star8"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 2"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
		LabelGraphics
		[
			text	"id | v1 v2 || n Sol
------------------
  0|  0  0   ||    0    
  1|  1  0   ||    1    
  2|  0  1   ||    1    
  3|  1  1   ||    2    
------------------
           sum: 4"
			fontSize	12
			fontName	"Dialog"
			model	"sandwich"
			anchor	"s"
		]
	]
	node
	[
		id	2
		label	"bag 4"
		graphics
		[
			x	117.5
			y	7.5
			w	15.0
			h	15.0
			type	"ellipse"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 4"
			fontSize	12
			fontName	"Dialog"
			anchor	"w"
		]
		LabelGraphics
		[
			text	"[ 2 3 8 ]"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
	]
	node
	[
		id	3
		label	"bag 4"
		graphics
		[
			x	53.0
			y	63.0
			w	30.0
			h	30.0
			type	"star8"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 4"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
		LabelGraphics
		[
			text	"id | v2 v8 || n Sol
------------------
  0|  0  0   ||    1    
  1|  1  0   ||    2    
  2|  0  1   ||    1    
  3|  1  1   ||    1    
------------------
           sum: 5"
			fontSize	12
			fontName	"Dialog"
			model	"sandwich"
			anchor	"s"
		]
	]
	node
	[
		id	4
		label	"bag 3"
		graphics
		[
			x	181.5
			y	62.5
			w	15.0
			h	15.0
			type	"ellipse"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 3"
			fontSize	12
			fontName	"Dialog"
			anchor	"w"
		]
		LabelGraphics
		[
			text	"[ 2 4 8 ]"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
	]
	node
	[
		id	5
		label	"bag 3"
		graphics
		[
			x	178.0
			y	118.0
			w	30.0
			h	30.0
			type	"star8"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 3"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
		LabelGraphics
		[
			text	"id | v2 v4 || n Sol
------------------
  0|  0  0   ||    1    
  1|  1  0   ||    2    
  2|  0  1   ||    2    
  3|  1  1   ||    3    
------------------
           sum: 8"
			fontSize	12
			fontName	"Dialog"
			model	"sandwich"
			anchor	"s"
		]
	]
	node
	[
		id	6
		label	"Join 2~3"
		graphics
		[
			x	312.0
			y	200.0
			w	30.0
			h	30.0
			type	"star8"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"Join 2~3"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
		LabelGraphics
		[
			text	"id | v1 v2 v4 || n Sol
---------------------
  0|  0  0  0   ||    0    
  1|  1  0  0   ||    1    
  2|  0  1  0   ||    2    
  3|  1  1  0   ||    4    
  4|  0  0  1   ||    0    
  5|  1  0  1   ||    2    
  6|  0  1  1   ||    3    
  7|  1  1  1   ||    6    
---------------------
              sum: 18"
			fontSize	12
			fontName	"Dialog"
			model	"sandwich"
			anchor	"n"
		]
	]
	node
	[
		id	7
		label	"bag 1"
		graphics
		[
			x	311.5
			y	341.5
			w	15.0
			h	15.0
			type	"ellipse"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 1"
			fontSize	12
			fontName	"Dialog"
			anchor	"w"
		]
		LabelGraphics
		[
			text	"[ 1 2 4 6 ]"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
	]
	node
	[
		id	8
		label	"bag 1"
		graphics
		[
			x	247.0
			y	397.0
			w	30.0
			h	30.0
			type	"star8"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 1"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
		LabelGraphics
		[
			text	"id | v1 v4 || n Sol
------------------
  0|  0  0   ||    2    
  1|  1  0   ||    9    
  2|  0  1   ||    3    
  3|  1  1   ||    6    
------------------
           sum: 20"
			fontSize	12
			fontName	"Dialog"
			model	"sandwich"
			anchor	"s"
		]
	]
	node
	[
		id	9
		label	"bag 0"
		graphics
		[
			x	375.5
			y	397.5
			w	15.0
			h	15.0
			type	"ellipse"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 0"
			fontSize	12
			fontName	"Dialog"
			anchor	"w"
		]
		LabelGraphics
		[
			text	"[ 1 4 7 ]"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
	]
	node
	[
		id	10
		label	"bag 0"
		graphics
		[
			x	376.0
			y	440.0
			w	30.0
			h	30.0
			type	"star8"
			fill	"#CCCCFF"
			outline	"#000000"
		]
		LabelGraphics
		[
			text	"bag 0"
			fontSize	12
			fontName	"Dialog"
			anchor	"e"
		]
		LabelGraphics
		[
			text	"id | v1 v4 v7 || n Sol
---------------------
  0|  0  0  0   ||    2    
  1|  1  0  0   ||    0    
  2|  0  1  0   ||    0    
  3|  1  1  0   ||    0    
  4|  0  0  1   ||    2    
  5|  1  0  1   ||    9    
  6|  0  1  1   ||    3    
  7|  1  1  1   ||    6    
---------------------
              sum: 22"
			fontSize	12
			fontName	"Dialog"
			model	"sandwich"
			anchor	"s"
		]
	]
	edge
	[
		source	0
		target	1
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	2
		target	3
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	4
		target	5
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	0
		target	6
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	4
		target	6
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	7
		target	8
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	9
		target	10
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	7
		target	9
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	6
		target	7
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	2
		target	4
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
]

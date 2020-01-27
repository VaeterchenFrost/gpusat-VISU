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
			x	441.2126984126984
			y	62.8505859375
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
			x	444.9626984126984
			y	118.201171875
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
			x	117.64206349206349
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
			x	53.362698412698414
			y	62.8505859375
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
			x	181.92142857142858
			y	62.8505859375
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
			x	178.17142857142858
			y	118.201171875
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
			x	311.5670634920635
			y	118.201171875
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
			anchor	"s"
		]
	]
	node
	[
		id	7
		label	"bag 1"
		graphics
		[
			x	311.5670634920635
			y	341.9658203125
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
			x	247.2876984126984
			y	397.31640625
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
			x	375.8464285714286
			y	397.31640625
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
			x	375.8464285714286
			y	439.81640625
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
		edgeAnchor
		[
			xSource	0.5
			ySource	0.8625
			yTarget	-1.0
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
			Line
			[
				point
				[
					x	117.64206349206349
					y	7.5
				]
				point
				[
					x	113.89206349206349
					y	32.3505859375
				]
				point
				[
					x	53.362698412698414
					y	32.3505859375
				]
				point
				[
					x	53.362698412698414
					y	62.8505859375
				]
			]
		]
		edgeAnchor
		[
			xSource	-0.5
			ySource	0.8625
			yTarget	-1.0
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
		edgeAnchor
		[
			xSource	-0.5
			ySource	0.8625
			yTarget	-1.0
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
			Line
			[
				point
				[
					x	441.2126984126984
					y	62.8505859375
				]
				point
				[
					x	437.4626984126984
					y	87.701171875
				]
				point
				[
					x	319.0670634920635
					y	87.701171875
				]
				point
				[
					x	311.5670634920635
					y	118.201171875
				]
			]
		]
		edgeAnchor
		[
			xSource	-0.5
			ySource	0.8625
			xTarget	0.5
			yTarget	-0.6395833333333333
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
			Line
			[
				point
				[
					x	181.92142857142858
					y	62.8505859375
				]
				point
				[
					x	185.67142857142858
					y	87.701171875
				]
				point
				[
					x	304.0670634920635
					y	87.701171875
				]
				point
				[
					x	311.5670634920635
					y	118.201171875
				]
			]
		]
		edgeAnchor
		[
			xSource	0.5
			ySource	0.8625
			xTarget	-0.5
			yTarget	-0.6395833333333333
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
			Line
			[
				point
				[
					x	311.5670634920635
					y	341.9658203125
				]
				point
				[
					x	307.8170634920635
					y	366.81640625
				]
				point
				[
					x	247.2876984126984
					y	366.81640625
				]
				point
				[
					x	247.2876984126984
					y	397.31640625
				]
			]
		]
		edgeAnchor
		[
			xSource	-0.5
			ySource	0.8625
			yTarget	-1.0
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
		edgeAnchor
		[
			ySource	1.0
			yTarget	-1.0
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
			Line
			[
				point
				[
					x	311.5670634920635
					y	341.9658203125
				]
				point
				[
					x	315.3170634920635
					y	366.81640625
				]
				point
				[
					x	375.8464285714286
					y	366.81640625
				]
				point
				[
					x	375.8464285714286
					y	397.31640625
				]
			]
		]
		edgeAnchor
		[
			xSource	0.5
			ySource	0.8625
			yTarget	-1.0
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
		edgeAnchor
		[
			ySource	1.0
			yTarget	-1.0
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
			Line
			[
				point
				[
					x	117.64206349206349
					y	7.5
				]
				point
				[
					x	121.39206349206349
					y	32.3505859375
				]
				point
				[
					x	181.92142857142858
					y	32.3505859375
				]
				point
				[
					x	181.92142857142858
					y	62.8505859375
				]
			]
		]
		edgeAnchor
		[
			xSource	0.5
			ySource	0.8625
			yTarget	-1.0
		]
	]
]

(* ::Package:: *)

(* todo: check that graph is connected. Check that junction graph is not a singleton *)

BeginPackage["Bulatov`treeDecomposition`",{"Bulatov`common`"}];

findTreeDecomposition::usage="findTreeDecomposition[g] returns tree decomposition of Graph g, as {bags,adjPairs} where adjPairs contains pairs of adjacent bags"

checkTreeDecomposition::usage=
"checkTreeDecomposition[g,decomposition] returns True if given tree decomposition is valid, otherwise returns false and prints the properties that are violated"

getTreeCost::usage="getTreeCost[decomp] gives number of basic operations needed to evaluate decomp *)"

getTreeWidth::usage="getTreeWidth[decomp] gives width of decomp. It is an upper bound on tree width of original graph."

findTreeDecompositionHeuristics::usage="findTreeDecompositionHeuristic gives list of valid primary and list of valid secondary heuristics"


Options[findTreeDecomposition]=
{
PrimaryHeuristic->"minfill",
SecondaryHeuristic->"canonical",
UseCombinatoricaSpanningTree->True
};


findTreeDecomposition::unprimary="Unknown value of primary heuristc";
findTreeDecomposition::unsecondary="Unknown value of secondary heuristc";


Begin["`Private`"]

(* map vertices to indices in adjacency matrix and back *)
vert2idx[verts_List]:=Flatten[Position[V,Alternatives@@verts]];
idx2vert[idx_List]:=V[[idx]];

(* gets all pairs of sets that intersect *)
intersectingPairs[bags_List]:=Module[{cands,result},
	cands=Outer[List,bags,bags,1]//fl1;
	Select[cands,#[[1]]!=#[[2]]&&!disjoint[#[[1]],#[[2]]]&&OrderedQ[#]&]
];

(* maximum spanning tree *)
makeSpanningBagTree[bags_]:=Module[{jtree,edgeCandidates,bestEdge,lens},
	acyclicEdges[ed_]:=Select[ed,AcyclicGraphQ[Graph[UndirectedEdge@@@(jtree\[Tilde]{#})]]&];

	findHeaviestEdge[ed_]:=(
		lens=\[LeftBracketingBar]#[[1]]\[Intersection]#[[2]]\[RightBracketingBar]&/@ed;
		If[lens=={},{},ed[[Last@Ordering@lens]]]
	);

	(* adds pair of bags with largest intersection to tree, removes cyclical candidates *)
	growTree[]:=(
		bestEdge=findHeaviestEdge[edgeCandidates];
		jtree=jtree\[Tilde]{bestEdge};
		edgeCandidates=edgeCandidates\[Backslash]{bestEdge};
		edgeCandidates=acyclicEdges[edgeCandidates];
	);
	edgeCandidates=intersectingPairs[bags];
	jtree={};
	While[edgeCandidates!={},growTree[]];
	Sort[jtree]
];

(* uses combinatorica to find maximum weight spanning tree *)
maxWeightSpanTree[edges_List,weights_List]:=Module[{nums,nodes,nums2nodes,nodes2nums,numEdges,combgraph,wCombGraph,combTree},
	Block[{Element},Needs["Combinatorica`"]];
	$ContextPath=DeleteCases[$ContextPath,"Combinatorica`"];

	nodes=Union[fl1@edges];
	nums=Range[\[LeftBracketingBar]nodes\[RightBracketingBar]];
	nums2nodes=Thread[nums->nodes];
	nodes2nums=Reverse/@nums2nodes;
	numEdges=edges/.nodes2nums;
	combGraph=Combinatorica`FromUnorderedPairs[numEdges];
	wCombGraph=Combinatorica`SetEdgeWeights[combGraph,numEdges,weights];
	combTree=Combinatorica`MaximumSpanningTree[wCombGraph];
	Combinatorica`ToUnorderedPairs[combTree]/.nums2nodes
];

makeSpanningBagTreeComb[bags_]:=Module[{},
	edgeCandidates=intersectingPairs[bags];
	edgeWeights=Length[#[[1]]\[Intersection]#[[2]]]&/@edgeCandidates;
	Sort[maxWeightSpanTree[edgeCandidates,edgeWeights]]
];

(* selects smallest item given list of partial orders *)
(* selectSmallest[{1,2,3},{1,1,1},{1,1,2}] gives 1,2 *)
selectSmallest[items_,orders__]:=(
	ordList=Transpose[{orders}];
	Assert[Length[items]==Length[ordList]];
	best=First@Sort@ordList;
	poses=Position[ordList,_?(#==best&)];
	Sort[Extract[items,poses]]
)

(* get vertices adjacent to given vertex or vertex set, not including the set *)
touchingVerts[{}]:=V;
touchingVerts[v_List]:=( 
	vArr=SparseArray[vert2idx[v]->ConstantArray[1,\[LeftBracketingBar]v\[RightBracketingBar]],\[LeftBracketingBar]V\[RightBracketingBar]];
	idx2vert[Cases[ArrayRules[(adjMat.vArr)(1-vArr)],HoldPattern[{x_}->_?Positive]->x]]
);
touchingVerts[v_Integer]:=touchingVerts[{v}];

connComps[v_]:=ConnectedComponents[Subgraph[g,v]];

(*** Heuristics used to break ties during elimination ***)

(* approximates the number of cycles going through each point *)
computeAccumulation[mat_]:=( 
	r=Max@Eigenvalues@N@mat;
	Diagonal[Inverse[IdentityMatrix[Length[mat]]-mat/(r*1.1)]]//Normal
);

gridCentralRow[k_]:=(Table[k(Floor[k/2])+j,{j,1,k}]);
gridCentralCol[k_]:=(Table[k j+Floor[k/2]+1,{j,0,k-1}]);

primary={"minfill","mincut","canonical","grid","eccentricity","random"};
secondary={"accumulation","eccentricity","canonical","random"};
findTreeDecompositionHeuristics={primary,secondary};


findTreeDecomposition[gr_Graph,OptionsPattern[]]:=(
	g=gr;
	V=VertexList[g];
	adjMat=AdjacencyMatrix[g];
	elimed={};
	jnodes={};

	method=OptionValue[PrimaryHeuristic];
	tieBr=OptionValue[SecondaryHeuristic];
	useCombSpanTree=OptionValue[UseCombinatoricaSpanningTree];

	(* how to pick among vertices that give equal fill *)
	Which[
		tieBr=="canonical",tieBreaker=V,
		tieBr=="accumulation",tieBreaker=computeAccumulation[adjMat][[Ordering[V]]],
		tieBr=="eccentricity",tieBreaker=VertexEccentricity[g,#]&/@V,
		tieBr=="random",tieBreaker=RandomSample[V],
		True,Message[findTreeDecomposition::unsecondary];Return[Null]
	];

	Which[
		method=="minfill",While[\[LeftBracketingBar]elimed\[RightBracketingBar]<\[LeftBracketingBar]V\[RightBracketingBar],minFillEliminate[]],

		(* Recursively subdivides Graph using GraphUtilies`MinCut and eliminates the boundary of cut using minfill *)
		method=="mincut",While[\[LeftBracketingBar]elimed\[RightBracketingBar]<\[LeftBracketingBar]V\[RightBracketingBar],minCutEliminate[]],

		(* eliminates in order of VertexList[g] *)
		method=="canonical",elimVertex/@Range[\[LeftBracketingBar]V\[RightBracketingBar]],

		(* experimental methods for grids *)
		method=="grid",
		k=Floor[Sqrt[Length[V]]];
		row=gridCentralRow[k];
		col=gridCentralCol[k]\[Backslash]row;
		rowOrd=Ordering[VertexEccentricity[g,#]&/@row];
		colOrd=Ordering[VertexEccentricity[g,#]&/@col];
		elimVertex/@row[[rowOrd]];
		elimVertex/@col[[colOrd]];
		While[\[LeftBracketingBar]elimed\[RightBracketingBar]<\[LeftBracketingBar]V\[RightBracketingBar],minFillEliminate[]],

		method=="eccentricity",
		elimVertex/@Ordering[VertexEccentricity[g,#]&/@V],

		method=="random",
		elimVertex/@RandomSample[V],

		True,Message[findTreeDecomposition::unprimary];Return[Null]
	];
	(*Assert[Length[jnodes]>1,"degenerate tree decomposition with no edges"];*)
	jnodes=Sort[Select[jnodes,Not[isBagRedundant[#]]&]];
	jedges=If[useCombSpanTree,makeSpanningBagTreeComb[jnodes],makeSpanningBagTree[jnodes]];
	{jnodes,jedges}
);

(* check if bag is contained inside any other bag *)
isBagRedundant[bag_]:=anyTrue[b\[Element]jnodes,(b!=bag)\[And](bag\[Subset]b)];
elimVertex[v_]:=( 
	(*Print[Length[V\[Backslash]elimed]];*)
	Assert[!(v\[Element]elimed),"Duplicate elimination"];
	comps=connComps[V\[Backslash]elimed];
	ourComp=Select[comps,v\[Element]#&]//First;
	boundary=touchingVerts[ourComp];
	AppendTo[jnodes,boundary\[Union]{v}];
	AppendTo[elimed,v];
);

(* returns negative number of edges in bag created for each member of verts *)
getFillValues[{}]:={};
getFillValues[verts_List]:=( 
	Assert[ValueQ[elimed]];
	If[elimed=={},Return[ConstantArray[0,\[LeftBracketingBar]verts\[RightBracketingBar]]]];
	elimArr=SparseArray[vert2idx[elimed]->ConstantArray[1,\[LeftBracketingBar]elimed\[RightBracketingBar]],\[LeftBracketingBar]V\[RightBracketingBar]];
	getFillSingleVert[v_]:=( 
		vArr=SparseArray[vert2idx[{v}]->1,\[LeftBracketingBar]V\[RightBracketingBar]];
		touchArr=adjMat.vArr;
		cliqueArr=elimArr touchArr+vArr;
		-cliqueArr.adjMat.cliqueArr/2
	);
	getFillSingleVert/@verts
);

minFillEliminate[]:=( 
	frontier=touchingVerts[elimed];
	Assert[frontier!={},"Either nothing left to eliminate or graph not connected"];
	fillVals=getFillValues[frontier];
	tieVals=tieBreaker[[frontier]];
	elimVertex[First[selectSmallest[frontier,fillVals,tieVals,frontier]]]
);

minCutEliminate[]:=( 
	Assert[V\[Backslash]elimed!={},"nothing left to eliminate"];
	comps=ConnectedComponents[Subgraph[g,V\[Backslash]elimed]];
	largestComp=First[Sort[comps,Length[#1]>=Length[#2]&]];
	If[\[LeftBracketingBar]largestComp\[RightBracketingBar]<4,minFillEliminate[],minCutElimComp[largestComp]]
);

(* Splits components into 2 and eliminates the boundary in minfill order *)
Needs["GraphUtilities`"];
$ContextPath=DeleteCases[$ContextPath,"Combinatorica`"|"GraphUtilities`"];
minCutElimComp[comp_]:=( 
	children=GraphUtilities`MinCut[Subgraph[g,comp],2];
	children=Sort[children,Length[#1]<=Length[#2]&];
	compBoundary=touchingVerts[children[[1]]]\[Intersection]children[[2]];
	remainBoundary=compBoundary;
	While[remainBoundary!={},
		fillVals=getFillValues[remainBoundary];
		tieVals=tieBreaker[[remainBoundary]];
		cands=selectSmallest[remainBoundary,fillVals,tieVals];
		elimVertex[First[cands]];
		remainBoundary=remainBoundary\[Backslash]elimed;
	];
);

(* checks that "jnodes/jedges" forms a junction tree of g *)
checkTreeDecomposition[g_,{jnodes_,jedges_}]:=(
	isok=True;

	existNodes=Union[VertexList[g]];
	coveredNodes=Union[Flatten[jnodes]];
	prop=(existNodes===coveredNodes);
	If[!prop,Print["checkTreeDecomposition: violates variable preservation for ",existNodes\[Backslash]coveredNodes];isok=False];

	existFactors=Union[List@@@EdgeList[g]];
	coveredFactors=Union[Select[existFactors,anyTrue[bag\[Element]jnodes,#\[Subset]bag]&]];
	prop=(existFactors===coveredFactors);
	If[!prop,Print["checkTreeDecomposition: violates factor preservation for ",existFactors\[Backslash]coveredFactors];isok=False];

    isSeparator[{i_,j_}]:=\[LeftBracketingBar]ConnectedComponents[Subgraph[g,V\[Backslash](i\[Intersection]j)]]\[RightBracketingBar]>1;
    separatingEdges=Select[jedges,isSeparator[#]&];
	prop=(Union[separatingEdges]===Union[jedges]);
	If[!prop,Print["checkTreeDecomposition: violates running intersection for ",jedges\[Backslash]separatingEdges];isok=False];

	gg=Graph[jnodes,UndirectedEdge@@@jedges];
	prop=ConnectedGraphQ[gg];
	If[!prop,Print["checkTreeDecomposition: tree not connected, have following cc sizes ",Length/@ConnectedComponents[gg]];isok=False];

	(* following check can subsume the previous two if we allow Junction Forests *)
	seps=Intersection@@@jedges;
	sepCount[x_]:=Length@Select[seps,x\[Element]#&];
	bagCount[x_]:=Length@Select[jnodes,x\[Element]#&];
	vars=Union@Flatten@jedges;
	counts=table[x\[Element]vars,bagCount[x]-sepCount[x]];
	failures=Extract[vars,Position[counts,_?(#!=1&)]];
	failures=={};
	If[!prop,Print["checkTreeDecomposition: generalized running intersection violated for ",failures];isok=False];

	(* data structure checks *)
	If[!allTrue[e\[Element]jedges,OrderedQ[e]],Print["checkTreeDecomposition: some edge is not ordered"];isok=False];
	If[!allTrue[e\[Element]jnodes,OrderedQ[e]],Print["checkTreeDecomposition: some node is not ordered"];isok=False];
	If[!OrderedQ[jedges],Print["checkTreeDecomposition: edges are not ordered"];isok=False];
	If[!OrderedQ[jnodes],Print["checkTreeDecomposition: nodes are not ordered"];isok=False];
	If[Union[fl1@jedges]!=jnodes,Print["nodes and edges don't match"];isok=False];

	isok
);

(* gives number of basic operations needed to evaluate given tree decomposition *)
getTreeCost[{nodes_List,edges_List}]:=(
	edgeCost[{a_,b_}]:=2^\[LeftBracketingBar]a\[Intersection]b\[RightBracketingBar](2^\[LeftBracketingBar]a\[Backslash]b\[RightBracketingBar]+2^\[LeftBracketingBar]b\[Backslash]a\[RightBracketingBar]);
	sum[e\[Element]edges,edgeCost[e]]
);

(* gives tree width (size of largest bag) of given tree decomposition *)
getTreeWidth[{nodes_List,edges_List}]:=(
	bags=fl1[edges];
	Max[Length/@bags]
)

End[]
EndPackage[]







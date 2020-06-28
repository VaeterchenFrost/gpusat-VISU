(* ::Package:: *)

BeginPackage["Bulatov`common`"]

Tilde::usage="Tilde[a,b] is equivalent to Join[a,b]"
Element::usage="Element[a,b_List] is equivalent to MemberQ[b,a] (custom redefinition)"
NotMyElement::usage="NotElement[a,b_List] is equivalent to !MemberQ[b,a]"
Subset::usage="Subset[a,b] is equivalent to a\[Intersection]b==a"
NotSubset::usage=""
BracketingBar::usage="BracketingBar[a] is Length[a]"
disjoint::usage="disjoint[a,b] returns True if intersection of a and b is empty"
intersect::usage="like Intersection, but preserves original order"
fl1::usage="flatten one level of list"
idx::usage="position of first occurence of element or -1 if doesn't occur"

table::usage="table[a\[Element]list,expr] is equivalent to Table[expr,{a,list}]"
prod::usage="prod[var\[Element]list,expr] is equivalent to Times@@table[a\[Element]list,expr]"
sum::usage="sum[var\[Element]list,expr] is equivalent to Plus@@table[a\[Element]list,expr]"
anyTrue::usage="anyTrue[var\[Element]list,expr] checks if expression is true for any value of var in list"
allTrue::usage="allTrue[var\[Element]list,expr] checks if expression is true for all values of var in list"

SetAttributes[sum,HoldAll];
SetAttributes[prod,HoldAll];
SetAttributes[table,HoldAll];
SetAttributes[anyTrue,HoldAll];
SetAttributes[allTrue,HoldAll];

Begin["Private`"]
Tilde[x__]:=Join[x];
Unprotect[Element,NotElement];
(* clear Combinatorica definitions conflicting *)
Element[x_,list_List]:=MemberQ[list,x];
NotElement[x_,list_List]:=Not[Element[x,list]];
Protect[Element,NotElement];
Subset[a_List,b_List]:=(a\[Intersection]b==a);
NotSubset[a_List,b_List]:=Not[Subset[a,b]];
Backslash[a_List,b_List]:=(Complement[a,b]);
BracketingBar[a_List]:=Length[a];
disjoint[A_,B_]:=Length[A\[Intersection]B]==0;
intersect[a_,b_]:=Select[a,MemberQ[b,#]&];
fl1[lst_]:=Flatten[lst,1];
idx[lst_,item_]:=If[MemberQ[lst,item],Position[lst,item][[1,1]],-1];

table[var_\[Element]lis_,expr_]:=ReleaseHold[Hold[expr]/.HoldPattern[var]->#]&/@lis;
prod[var_\[Element]lis_,expr_]:=Times@@table[var\[Element]lis,expr];
sum[var_\[Element]lis_,expr_]:=Plus@@table[var\[Element]lis,expr];
anyTrue[var_\[Element]lis_,expr_]:=LengthWhile[lis,Not[TrueQ[ReleaseHold[Hold[expr]/.HoldPattern[var]->#]]]&]<Length[lis];
allTrue[var_\[Element]lis_,expr_]:=LengthWhile[lis,TrueQ[ReleaseHold[Hold[expr]/.HoldPattern[var]->#]]&]==Length[lis];

End[]
EndPackage[]










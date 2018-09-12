member(a).
member(b).
member(c).
member(X) :- \+mc(X),fail.
member(X).
member(X) :- \+sk(X),!,fail.
member(X).
like(a,rain).
like(a,snow).
like(a,X) :- \+ like(b,X).
like(b,X) :- like(a,X),!,fail.
like(b,X).
mc(X):- like(X,rain),!,fail.
mc(X).
sk(X):- \+like(X,snow),!,fail.
sk(X).
g(X):-member(X),mc(X),\+sk(X),!.

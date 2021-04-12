# golang-mini-compiler
A compiler front-end for Golang implemented using Python Lex and YACC (PLY) that handles the switch and loop constructs of Golang

Optimizations implemented:
* Constant folding and constant propagation
* Packing temporaries (removing all unnecesary temp variables from TAC)
* Dead code elimination (Naive approach using leaders/basic blocks in TAC and building a basic CFG)

Command to run till IC Optimization Step:

 ```
 export PATH=$PATH:/your-path-here/golang-mini-compiler
 go-compile <path-to-filename.go>
 ```
 
 



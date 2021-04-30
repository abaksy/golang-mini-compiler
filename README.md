# golang-mini-compiler
A compiler front-end for Golang implemented using Python Lex and YACC (PLY) that handles the switch and loop constructs of Golang

## Optimizations implemented:
* Constant folding and constant propagation
* Packing temporaries (removing all unnecesary temp variables from TAC)

## Code Structure
* src/lexer.py - Generates Lex tokens from the input source file
* src/parser.py - Takes a stream of tokens as input from ```lexer.py``` and runs the LALR parser logic (rules and actions) on the tokens (outputs the three address code)
* src/optimize_tac.py - Runs the above mentioned optimizations on the generated Three Address Code from the parser
* src/code.py - Contains class definitions for Three Address Code and AST nodes
* src/symboltable.py - Contains class definition for SymbolTable

Command to run till IC Optimization Step:

 ```
 export PATH=$PATH:/your-path-here/golang-mini-compiler
 go-compile <path-to-filename.go>
 ```
 
 



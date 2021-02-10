%{
  #include <stdio.h>
  #include <stdlib.h>
  #include <string.h>
  #define YYSTYPE char *
  int yylex();
  void yyerror(char *);
  void lookup(char *,int,char,char*,char* );
  //void insert(char *,int,char,char*,char* );
  void update(char *,int,char *);
  void search_id(char *,int );
  extern FILE *yyin;
  extern int yylineno;
  extern char *yytext;
  typedef struct symbol_table
  {
    int line;
    char name[31];
    char type;
    char *value;
    char *datatype;
  }ST;
  int struct_index = 0;
  ST st[10000];
  char x[10];
%}

%start S 
//Tokens for keywords
%token BREAK CASE CHAN CONST CONTINUE DEFAULT DEFER ELSE FT FOR FUNC GO GOTO IF IMPORT INTRF MAP PKG RANGE RETURN SELECT STRUCT SWITCH TYPE VAR
//Tokens for relational operators
%token T_lt T_le T_ge T_gt T_eqeq T_neq 
//Tokens for arithmetic operators
%token T_plus T_min T_mul T_div T_mod
//Tokens for logical operators
%token T_and T_not T_or
//Tokens for assignment operator
%token T_as 
//Tokens for Identifier
%token ID INT_LITERAL FLOAT_LITERAL


//Defining associativity rules for operators
%left T_lt T_gt
%left T_plus T_min T_mul T_div T_mod

%%



%%
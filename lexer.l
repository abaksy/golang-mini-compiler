%option noyywrap
%{
    #include<stdio.h>
    #include<string.h>
    #include "y.tab.h"
%}
letter  [a-zA-Z_]
decimal_digit   [0-9]

%%

"break"     {return BREAK;}
"case"      {return CASE;}
"chan"      {return CHAN;}
"const"     {return CONST;}
"continue"  {return CONTINUE;}
"default"   {return DEFAULT;}
"defer"     {return DEFER;}
"else"      {return ELSE;}
"fallthrough"   {return FT;}
"for"       {return FOR;}
"func"      {return FUNC;}
"go"        {return GO;}
"goto"      {return GOTO;}
"if"        {return IF;}
"import"    {return IMPORT;}
"interface" {return INTRF;}
"map"       {return MAP;}
"package"   {return PKG;}
"range"     {return RANGE;}
"return"    {return RETURN;}
"select"    {return SELECT;}
"struct"    {return STRUCT;}
"switch"    {return SWITCH;}
"type"      {return TYPE;}
"var"       {printf("var\n");return VAR;}

{letter}({letter}|{decimal_digit})*   {return ID;}
{decimal_digit}+    {return INT_LITERAL;}
{decimal_digit}+.{decimal_digit}+   {return FLOAT_LITERAL;}

"<"     {return T_lt;}
">"     {return T_gt;}
"<="    {return T_le;}
">="    {return T_ge;}
"=="    {return T_eqeq;}
"!="    {return T_neq;}

"="     {return T_as;}

"+"     {return T_plus;}
"-"     {return T_min;}
"*"     {return T_mul;}
"/"     {return T_div;}
"%"     {return T_mod;}

"++"    {return T_incr;}
"--"    {return T_decr;}
"!"     {return T_not;}
"||"    {return T_or;}
"&&"    {return T_and;}

.   {return yytext[0];}

%%


%option noyywrap
%{
    #include<stdio.h>
    #include<string.h>
%}
start \/\*
end \*\/
%%

    /* Rule for single line comment */
\/\/(.*)    ;
    /* Rule for multi line comment */
{start}(.|\n)*{end}    ;

%%

int main()
{
    extern FILE* yyin;
    extern FILE* yyout;
    yyin = fopen("sample_ip/input.go", "r");
    yyout = fopen("sample_ip/input_nocomments.go", "w");
    yylex();
    return 0;
}

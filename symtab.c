#include<stdio.h>
#include<stdlib.h>
#include<string.h>


typedef struct symbol_table_entry{
    int line_no;
    char name[50];
    char type[50];
    char value[100];
};
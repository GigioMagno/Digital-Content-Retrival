#ifndef _SSTACK_
#define _SSTACK_

#include <stdio.h>
#include <stdlib.h>

struct record {
	int *memaddr;				//memory address of node of the bst
	struct record *next;
};

typedef struct record record;

record *create_record(int *mem);
record *push(record **top, int *addr);
record *pop(record **top);
// int *top(record *tos);
int is_empty(record *top);
void print_stack(record *top);
void print_stack2(record *top);

#endif
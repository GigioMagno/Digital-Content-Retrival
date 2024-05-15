#ifndef _READ_POSTINGS_
#define _READ_POSTINGS_

#include <stdio.h>
#include <stdlib.h>

struct list
{
	long long int doc_ID;
	struct list *next;
};

typedef struct list list;

void print_list(list *l);
void free_list(list *l);
void add_id(list **l, long long int ID);

#endif
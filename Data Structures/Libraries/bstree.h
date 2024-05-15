#ifndef _BINARY_SEARCH_TREE_
#define _BINARY_SEARCH_TREE_


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct node
{
	char *searchKey;
	struct node *left;
	struct node *right;
};

typedef struct node node;

node *create_node(char *searchKey);
void add_node(node **root, node *newnode);
void print_tree(node *root);
node *get_minimum(node **root);
node *get_maximum(node **root);
void delete_node(node **root, char* searchKey);


#endif

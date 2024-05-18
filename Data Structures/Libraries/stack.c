#include "stack.h"


record *create_record(int *mem){
	record *r = (record*)malloc(sizeof(record));
	r->memaddr=mem;
	r->next = NULL;
	return r;
}

// int *top(record *tos){
// 	return *(tos->memaddr);
// }

record *push(record **top, int *addr){

	if (*top == NULL) //stack is empty
	{
		*top = create_record(addr);
		return *top;
	}

	record *newtop = create_record(addr); //top of stack
	newtop->next = *top;
	*top = newtop;
	return *top;			//add to the stack in O(1)

}

//new element -> old list

record *pop(record **top) {
    if (*top == NULL) {
        return NULL;    // the stack is empty
    }

    record *head = *top;    // save the current top
    *top = (*top)->next;    // move the top to the next element
    head->next = NULL;      // detach the popped element from the stack
    return head;
}

void print_stack2(record *top){

	if (top == NULL)
	{
		return;
	}
	int i = 0;
	while(top != NULL) {
		printf("%d-%p\n", i, top->memaddr);
		i++;
		top = top->next;
	}

}

void print_stack(record *top){

	if (top == NULL)
	{
		return;
	}
	int i = 0;
	while(top != NULL) {
		printf("%d-%d-%p\n", i, *(top->memaddr), top->memaddr);
		i++;
		top = top->next;
	}

}


int is_empty(record *top){
	if (top == NULL)
	{
		return 1;
	}
	return 0;
}
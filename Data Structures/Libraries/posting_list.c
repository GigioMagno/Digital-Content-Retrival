#include "posting_list.h"

void add_id(list **l, long long int ID) {
    // Crea un nuovo nodo
    list *new_node = (list *)malloc(sizeof(list));
    if (new_node == NULL) {
        printf("Memoria insufficiente\n");
        return;
    }

    new_node->doc_ID = ID;
    new_node->next = NULL;

    // Se la lista è vuota, il nuovo nodo diventa la testa della lista
    if (*l == NULL) {
        *l = new_node;
        return;
    }

    // Altrimenti, trova l'ultimo nodo e aggiungi il nuovo nodo
    list *current = *l;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = new_node;
}

void print_list(list *l) {
    while (l != NULL) {
        printf("%lld ---> ", l->doc_ID);
        l = l->next;
    }
    printf("NULL\n");
}

void free_list(list *l) {
    list *temp;
    while (l != NULL) {
        temp = l;
        l = l->next;
        free(temp);
    }
}
#include "btree.h"

node *create_node(char *searchKey){
    node *n = malloc(sizeof(node)); // Alloca memoria per il nuovo nodo
    n->searchKey = strdup(searchKey); // Alloca memoria per la chiave e copiala
    n->left = NULL;
    n->right = NULL;
    return n;
}

void add_node(node **root, node *newnode){
    if (*root == NULL){
        *root = newnode;
        return;
    }
    if (strcmp(newnode->searchKey, (*root)->searchKey) < 0){
        add_node(&((*root)->left), newnode);
        return;
    }
    if (strcmp(newnode->searchKey, (*root)->searchKey) > 0){
        add_node(&((*root)->right), newnode);
        return;
    }
}

void print_tree(node *root){
    if (root == NULL){
        return;
    }

    printf("%s\n", root->searchKey); // Stampiamo il valore del nodo corrente

    print_tree(root->left); // Visitiamo il sottoalbero sinistro
    print_tree(root->right); // Visitiamo il sottoalbero destro
}

node *get_minimum(node **root){

	if (*root == NULL)
	{
		return NULL;	//Albero vuoto
	}
	if ((*root)->left == NULL)
	{
		return *root;			//se l'albero ha un solo nodo
	}
	node *current = *root;
	while(current->left != NULL)
		current = current->left;
	return current;
}

node *get_maximum(node **root){

    if (*root == NULL)
    {
        return NULL;    //Albero vuoto
    }
    if ((*root)->right == NULL)
    {
        return *root;           //se l'albero ha un solo nodo
    }
    node *current = *root;
    while(current->right != NULL)
        current = current->right;
    return current;
}

void delete_node(node **root, char* searchKey) {
    if (*root == NULL) {
        return; // L'albero è vuoto o il nodo non è stato trovato
    }

    if (strcmp(searchKey, (*root)->searchKey) < 0) { // Sinistra
        delete_node(&((*root)->left), searchKey);
    } else if (strcmp(searchKey, (*root)->searchKey) > 0) { // Destra
        delete_node(&((*root)->right), searchKey);
    } else { // Nodo da eliminare trovato
        if ((*root)->left == NULL && (*root)->right == NULL) { // Caso 1: nodo senza figli
            free(*root);
            *root = NULL;
        } else if ((*root)->left == NULL) { // Caso 2: nodo con un solo figlio destro
            node *temp = *root;
            *root = (*root)->right;
            free(temp);
        } else if ((*root)->right == NULL) { // Caso 3: nodo con un solo figlio sinistro
            node *temp = *root;
            *root = (*root)->left;
            free(temp);
        } else { // Caso 4: nodo con entrambi i figli
            node *successor_parent = *root;
            node *successor = (*root)->right;
            while (successor->left != NULL) {
                successor_parent = successor;
                successor = successor->left;
            }
            if (successor_parent != *root) {
                successor_parent->left = successor->right;
            } else {
                successor_parent->right = successor->right;
            }
            (*root)->searchKey = strdup(successor->searchKey); // Copia la chiave del successore nel nodo corrente
            free(successor); // Libera la memoria del successore
        }
    }
}

// void check_delete(node **parent, node **child, char *searchKey);
// void check_delete(node **parent, node **child, char *searchKey){

//  node *_parent_ = *parent;
//  node *_child_ = *child;

//  if (_child_->right != NULL && _child_->left == NULL)
//  {
//      _parent_->right = _child_->right;
//      free(child);
//  } else if (_child_->right == NULL && _child_->left != NULL)
//  {
//      _parent_->left = _child_->left;
//      free(child);
//  } else if (_child_->right != NULL && _child_->left != NULL)
//  {
//      node *minimum = get_minimum(&(_child_->right));
//      minimum->left = _child_->left;
//      _child_->right->left = minimum->right;
//      minimum->right = _child_->right;
//      free(_child_);
//      _parent_->left = minimum;
//  }
//  //non sono alla fine dell'albero, ma sono all'interno.
// }

//strcmp(_child_->searchKey,searchKey)==0 
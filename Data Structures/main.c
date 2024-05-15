#include <stdio.h>
#include <stdlib.h>
#include "bstree.h"


int main(int argc, char const *argv[]){
    node *root = NULL;
    add_node(&root, create_node("ciao"));
    add_node(&root, create_node("ciaooo"));
    add_node(&root, create_node("a"));
    add_node(&root, create_node("b"));
    add_node(&root, create_node("c"));
    add_node(&root, create_node("d"));
    add_node(&root, create_node("co"));
    add_node(&root, create_node("due"));
    add_node(&root, create_node("dodo"));
    add_node(&root, create_node("dino"));
    add_node(&root, create_node("aino"));
    add_node(&root, create_node("duedue"));
    add_node(&root, create_node("carciofo"));
    print_tree(root);
    printf("////////////\n");
    // delete_node(&root, "ciao");
    // delete_node(&root, "co");
    delete_node(&root, "due");
    // delete_node(&root, "dodo");
    // delete_node(&root, "dino");
    // delete_node(&root, "aino");
    // delete_node(&root, "c");
    // delete_node(&root, "D");
    //delete_node(&root, "d");
    print_tree(root);
    return 0;
}
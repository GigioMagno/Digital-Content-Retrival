#include <stdio.h>
#include <stdlib.h>
#include "bstree.h"
#include "posting_list.h"

#define SIZE 50

node *create_nodes_bst(char *filename, int *len);
node *create_nodes_bst(char *filename, int *len){   //len contiene il numero di parole da inserire nell'albero

    char buf[SIZE]; //Alloco spazio per una parola da 50 lettere (molto abbondante)
    node *node_set = (node *)malloc(sizeof(node)*SIZE);
    *len = 0;
    int size = SIZE;
    FILE *f = fopen(filename, "r");

    while(fgets(buf, size, f)) {
        if (atoll(buf)==0)
        {   
            (*len)++;   //parola trovata           

            if ((*len)>=size)
            {
                size*=2;
                node_set = realloc(node_set, size*sizeof(node));
            }
            buf[strlen(buf)-1] = '\0';
            node_set[(*len)-1] = *create_node(buf);
            node_set[(*len)-1].posting = NULL;
        } else {
            add_id(&(node_set[(*len)-1].posting), atoll(buf));
        }

    }
    fclose(f);
    return realloc(node_set, (*len)*sizeof(node));
}



int main(int argc, char const *argv[]){
    FILE *f = fopen("finale.txt", "w");
    int words = 0;
    node *node_set = create_nodes_bst("postings.txt", &words);

    // for (int i = 0; i < words; ++i)
    // {
    //     printf("%s:\n", node_set[i].searchKey);
    //     print_list(node_set[i].posting);
    //     printf("\n");
    // }
    node *root = NULL;
    for (int i = 0; i < words; ++i)
    {
        add_node(&root, &node_set[i]);
    }
    printf("albero ok\n");
    print_tree(root, f);



    // node *root = NULL;
    // add_node(&root, create_node("ciao"));
    // add_node(&root, create_node("ciaooo"));
    // add_node(&root, create_node("a"));
    // add_node(&root, create_node("b"));
    // add_node(&root, create_node("c"));
    // add_node(&root, create_node("d"));
    // add_node(&root, create_node("co"));
    // add_node(&root, create_node("due"));
    // add_node(&root, create_node("dodo"));
    // add_node(&root, create_node("dino"));
    // add_node(&root, create_node("aino"));
    // add_node(&root, create_node("duedue"));
    // add_node(&root, create_node("carciofo"));
    // print_tree(root, f);
    fclose(f);
    // printf("////////////\n");
    // // delete_node(&root, "ciao");
    // // delete_node(&root, "co");
    // delete_node(&root, "due");
    // // delete_node(&root, "dodo");
    // // delete_node(&root, "dino");
    // // delete_node(&root, "aino");
    // // delete_node(&root, "c");
    // // delete_node(&root, "D");
    // //delete_node(&root, "d");
    // print_tree(root);

    // list *initial_node = NULL;
    
    // add_id(&initial_node, 2);
    // add_id(&initial_node, 1);
    // add_id(&initial_node, 4);
    // add_id(&initial_node, 23);
    // add_id(&initial_node, 22);
    
    // print_list(initial_node);
    
    // free_list(initial_node);
    return 0;
}
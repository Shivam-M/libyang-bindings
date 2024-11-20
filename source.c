#include <libyang/libyang.h>


void print_node(struct lyd_node* node) {
    if (node == NULL) {
        return;
    }
    
    const char* name = node->schema->name; // improper?
    const char* value = lyd_get_value(node);
    if (name && value) {
        printf("%s: %s\n", name, value);
    } else {
        printf("Couldn't print value of the node.\n");
    }
}

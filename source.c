#include <libyang/libyang.h>


void print_nodes_recursively(struct lyd_node* node, char* xpath_prefix) {
    char xpath[256];
    const char *value;
    struct lyd_node* child;

    while (node) {
        sprintf(xpath, "%s/%s", xpath_prefix ? xpath_prefix : "", node->schema->name);

        value = lyd_get_value(node);
        if (value) {
            printf("%s = %s\n", xpath, value);
        }

        child = lyd_child(node);
        if (child) {
            print_nodes_recursively(child, xpath);
        }

        node = node->next;
    }
}


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

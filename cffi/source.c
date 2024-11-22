#include <libyang/libyang.h>

struct node_info {
    char* xpath;
    const char* value;
};

struct lyd_node* get_differences(struct lyd_node* first_node, struct lyd_node* second_node) {
    struct lyd_node* diff_node;
    lyd_diff_tree(first_node, second_node, 0, &diff_node);
    return diff_node;
}

struct node_info get_node_info(struct lyd_node* node) {
    struct node_info info = { lyd_path(node, 0, NULL, 0), lyd_get_value(node) };
    return info;
}


void print_nodes_recursively(struct lyd_node* node) {
    struct lyd_node* child;

    while (node) {
        struct node_info ni = get_node_info(node);

        if (ni.value) {
            printf("%s = %s\n", ni.xpath, ni.value);
        }

        child = lyd_child(node);
        if (child) {
            print_nodes_recursively(child);
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


void test() {
    return;
}
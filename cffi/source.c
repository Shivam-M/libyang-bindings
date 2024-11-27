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


struct lyd_node* get_sibling(struct lyd_node* node) {
    return node->next;
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


struct lyd_node* get_next_node(struct lyd_node* node) {
    struct lyd_node* child = lyd_child(node);
    struct lyd_node* current_node = node;
    if (child) return child;
    
    while (current_node) {
        if (current_node->next) return current_node->next;
        current_node = (struct lyd_node*)current_node->parent;
    }

    return NULL;
}


struct lyd_node* get_node_at_xpath(struct lyd_node* node, char* xpath) {
    if (!node || !xpath) return NULL;
    struct ly_set* set;

    lyd_find_xpath(node, xpath, &set);

    if (set && set->count > 0) {
        return set->dnodes[0];
    }

    return NULL;
}


void test() {
    return;
}
#include <libyang/libyang.h>

struct lyd_node* get_differences(struct lyd_node* first_node, struct lyd_node* second_node) {
    struct lyd_node* diff_node;
    lyd_diff_tree(first_node, second_node, 0, &diff_node);
    return diff_node;
}

struct lyd_node* get_sibling(struct lyd_node* node) {
    return node->next;
}

void print_nodes_recursively(struct lyd_node* node) {
    struct lyd_node* child;

    while (node) {
        char* xpath = lyd_path(node, 0, NULL, 0);
        const char* value = lyd_get_value(node);

        if (value) {
            printf("%s = %s\n", xpath, value);
        }

        free(xpath);

        child = lyd_child(node);
        if (child) {
            print_nodes_recursively(child);
        }

        node = node->next;
    }
}

void print_node(struct lyd_node* node) {
    if (node == NULL) return;
    
    const char* name = node->schema->name; // improper?
    const char* value = lyd_get_value(node);
    if (name && value) {
        printf("%s: %s\n", name, value);
    } else {
        printf("Couldn't print value of the node.\n");
    }
}

struct lyd_node* get_next_node(struct lyd_node* node) {
    if (node == NULL) return NULL;

    struct lyd_node* child = lyd_child(node);
    if (child) return child;

    while (node) {
        if (node->next) return node->next;
        node = (struct lyd_node*)node->parent;
    }

    return NULL;
}

struct lyd_node* get_node_at_xpath(struct lyd_node* node, char* xpath) {
    if (node == NULL || xpath == NULL) return NULL;
    struct ly_set* set;
    struct lyd_node* found_node = NULL;

    lyd_find_xpath(node, xpath, &set);

    if (set && set->count > 0) {
        found_node = set->dnodes[0];
    }

    ly_set_free(set, NULL);

    return found_node;
}

void get_list_keys_from_data_node(const struct lyd_node* data_node) {
    const struct lysc_node* schema_node = data_node->schema;
    
    if (schema_node->nodetype == LYS_LIST) {
        const struct lysc_node_list* list_schema = (const struct lysc_node_list*)schema_node;
        const struct lysc_node* child = list_schema->child;

        while (child) {
            if (child->nodetype == LYS_LEAF) {
                if (child->flags & LYS_KEY) {
                    printf("- key: %s\n", child->name);
                }
            }
            child = child->next;
        }
    } else {
        printf("not list");
    }
}

void test() {
    return;
}

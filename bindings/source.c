#include <libyang/libyang.h>
#include <cjson/cJSON.h>

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

char* evaluate_differences(struct lyd_node* first_node, struct lyd_node* second_node, struct lyd_node* diff_node) {
    struct lyd_node* current_node = diff_node;
    cJSON* changes = cJSON_CreateObject();

    while (current_node) {
        char* xpath = lyd_path(current_node, LYD_PATH_STD, NULL, 0);
        const char* value_first = lyd_get_value(get_node_at_xpath(first_node, xpath));
        const char* value_second = lyd_get_value(get_node_at_xpath(second_node, xpath));
        const char* value_diff = lyd_get_value(current_node);

        if (!value_diff || (value_first && value_second && strcmp(value_first, value_second) == 0)) {
            current_node = get_next_node(current_node);
            free(xpath);
            continue;
        }

        cJSON* change = cJSON_CreateObject();

        if (value_first) {
            cJSON_AddStringToObject(change, "action", "removed");
            cJSON_AddStringToObject(change, "old_value", value_first);
        }

        if (value_second) {
            cJSON_AddStringToObject(change, "action", "created");
            cJSON_AddStringToObject(change, "new_value", value_second);
        }

        if (value_first && value_second) {
            // cJSON_ReplaceItemInObject(change, "action", cJSON_CreateString("changed"));
            cJSON_DeleteItemFromObject(change, "action");
            cJSON_AddStringToObject(change, "action", "changed");
        }

        cJSON_AddItemToObject(changes, xpath, change);

        free(xpath);
        current_node = get_next_node(current_node);
    }

    char* changes_str = cJSON_Print(changes);
    cJSON_Delete(changes);
    return changes_str;
}

struct ly_set* get_list_keys_from_data_node(const struct lyd_node* data_node) {
    const struct lysc_node* schema_node = data_node->schema;
    
    if (schema_node->nodetype == LYS_LIST) {
        const struct lysc_node_list* list_schema = (const struct lysc_node_list*)schema_node;
        const struct lysc_node* child = list_schema->child;
        struct ly_set* key_set = NULL;

        ly_set_new(&key_set);

        while (child) {
            if (child->nodetype == LYS_LEAF) {
                if (child->flags & LYS_KEY) {
                    ly_set_add(key_set, child->name, 0, NULL);
                }
            }
            child = child->next;
        }
        return key_set;
    } else {
        printf("not list");
    }
    return NULL;
}

void free_list_keys(struct ly_set* key_set) {
    if (key_set) {
        for (uint32_t i = 0; i < key_set->count; i++) {
            free(key_set->objs[i]);
        }
        ly_set_free(key_set, NULL);
    }
}

void test() {
    return;
}

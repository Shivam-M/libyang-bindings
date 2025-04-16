#include <libyang/libyang.h>
#include <cjson/cJSON.h>
#include <stdbool.h>

struct lyd_node* get_differences(struct lyd_node* first_node, struct lyd_node* second_node) {
    struct lyd_node* diff_node;
    lyd_diff_tree(first_node, second_node, 0, &diff_node);  // 0x01 get defaults
    return diff_node;
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

    struct lyd_node* found_node = NULL;
    lyd_find_path(node, xpath, 0, &found_node);

    return found_node;
}

const char* get_node_metadata(struct lyd_node* node, const char* key) {
    struct lyd_meta* meta = node->meta;
    while (meta) {
        const char* name = meta->name;
        if (name && (strcmp(name, key) == 0)) return meta->value._canonical;
        meta = meta->next;
    }
    return NULL;
}

struct diff_result {
    const char* operation;
    const char* old_value;
    const char* new_value;
};

struct diff_result get_diff_result(struct lyd_node* node) {
    struct diff_result difference = {0};
    const char* operation = get_node_metadata(node, "operation");

    if (!operation) return difference;

    if (strcmp(operation, "create") == 0) {
        difference.operation = "created";
        difference.new_value = lyd_get_value(node);
    } else if (strcmp(operation, "replace") == 0) {
        difference.operation = "changed";
        difference.old_value = get_node_metadata(node, "orig-value");
        difference.new_value = lyd_get_value(node);
    } else if (strcmp(operation, "delete") == 0) {
        difference.operation = "removed";
        difference.old_value = lyd_get_value(node);
    }

    return difference;
}

cJSON* create_change(const char* operation, const char* old_value, const char* new_value) {
    cJSON* change = cJSON_CreateObject();
    cJSON_AddStringToObject(change, "action", operation);
    if (old_value) cJSON_AddStringToObject(change, "old_value", old_value);
    if (new_value) cJSON_AddStringToObject(change, "new_value", new_value);
    return change;
}

void evaluate_node_and_children(struct lyd_node* node, cJSON* changes, const char* parent_operation, bool skip_containers_and_lists) {
    struct diff_result difference = get_diff_result(node);
    const char* operation = difference.operation ? difference.operation : parent_operation;

    // list/container with no operation but children might have changed
    if (!operation) {
        struct lyd_node* child = lyd_child(node);
        while (child) {
            evaluate_node_and_children(child, changes, parent_operation, skip_containers_and_lists);
            child = child->next;
        }
        return;
    }

    char* node_path = lyd_path(node, LYD_PATH_STD, NULL, 0);
    const char* node_value = lyd_get_value(node);
    struct lyd_node* child = lyd_child(node);

    if (node_value && strcmp(operation, "created") == 0) {
        cJSON* change = create_change(operation, NULL, node_value);
        cJSON_AddItemToObject(changes, node_path, change);
    } else if (node_value && strcmp(operation, "changed") == 0) {
        cJSON* change = create_change(operation, difference.old_value, node_value);
        cJSON_AddItemToObject(changes, node_path, change);
    } else if (node_value && strcmp(operation, "removed") == 0) {
        cJSON* change = create_change(operation, node_value, NULL);
        cJSON_AddItemToObject(changes, node_path, change);
    }  else if (child) {
        // list/container has been removed or created - make optional
        if (!skip_containers_and_lists && operation && (strcmp(operation, "created") == 0 || strcmp(operation, "removed") == 0)) {
            cJSON* change = create_change(operation, NULL, NULL);
            cJSON_AddItemToObject(changes, node_path, change);
        }

        while (child) {
            evaluate_node_and_children(child, changes, operation, skip_containers_and_lists);
            child = child->next;
        }
    }

    free(node_path);
}

char* evaluate_differences(struct lyd_node* diff_node, bool skip_containers_and_lists) {
    cJSON* changes = cJSON_CreateObject();

    if (diff_node) {
        evaluate_node_and_children(diff_node, changes, NULL, skip_containers_and_lists);

        struct lyd_node* sibling = diff_node->next;
        while (sibling) {
            evaluate_node_and_children(sibling, changes, NULL, skip_containers_and_lists);
            sibling = sibling->next;
        }
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
            if ((child->nodetype == LYS_LEAF) && (child->flags & LYS_KEY)) {
                ly_set_add(key_set, child->name, 0, NULL);
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
        // for (uint32_t i = 0; i < key_set->count; i++) {
        //     free(key_set->objs[i]);
        // }
        ly_set_free(key_set, NULL);
    }
}

void test() {
    return;
}

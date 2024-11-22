struct node_info {
    char* xpath;
    const char* value;
};

struct node_info get_node_info(struct lyd_node* node);
struct lyd_node* get_differences(struct lyd_node* first_node, struct lyd_node* second_node);
void print_node(struct lyd_node* node);
void print_nodes_recursively(struct lyd_node* node);

void test();
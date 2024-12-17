typedef enum {
    LY_SUCCESS,
    LY_EMEM,
    LY_ESYS,
    LY_EINVAL,
    LY_EEXIST,
    LY_ENOTFOUND,
    LY_EINT,
    LY_EVALID,
    LY_EDENIED,
    LY_EINCOMPLETE,
    LY_ERECOMPILE,
    LY_ENOT,
    LY_EOTHER,
    LY_EPLUGIN = 128
} LY_ERR;


struct ly_ctx;
LY_ERR ly_ctx_new(const char *, uint16_t, struct ly_ctx **);
void ly_ctx_destroy(struct ly_ctx *);
int ly_ctx_set_searchdir(struct ly_ctx *, const char *);

struct lys_module* ly_ctx_load_module(struct ly_ctx *, const char *, const char *, const char **);

typedef enum {
    LYD_UNKNOWN,
    LYD_XML,
    LYD_JSON,
    LYD_LYB
} LYD_FORMAT;

struct ly_in;
struct ly_out;
typedef uint8_t ly_bool;
void ly_in_free(struct ly_in *, ly_bool);
void ly_out_free(struct ly_out *, void(*)(void *arg), ly_bool);
ly_bool lyd_node_should_print(const struct lyd_node *node, uint32_t options);
LY_ERR ly_in_new_memory(const char *, struct ly_in **);
LY_ERR ly_in_new_filepath(const char *, size_t, struct ly_in **);
LY_ERR ly_in_new_fd(int, struct ly_in **);
LY_ERR ly_in_new_file(FILE *, struct ly_in **);
LY_ERR ly_out_new_memory(char **, size_t, struct ly_out **);
LY_ERR ly_out_new_filepath(const char *, struct ly_out **);
LY_ERR ly_out_new_file(FILE *, struct ly_out **);
LY_ERR ly_out_new_fd(int, struct ly_out **);


LY_ERR lyd_parse_data(const struct ly_ctx *, struct lyd_node *, struct ly_in *, LYD_FORMAT, uint32_t, uint32_t, struct lyd_node **);


#define LYD_PARSE_STRICT ...

#define LY_CTX_DISABLE_SEARCHDIR_CWD ...
#define LY_CTX_EXPLICIT_COMPILE ...
#define LY_CTX_LEAFREF_EXTENDED ...
#define LY_CTX_SET_PRIV_PARSED ...
#define LY_CTX_NO_YANGLIBRARY ...

LY_ERR ly_ctx_get_yanglib_data(const struct ly_ctx *, struct lyd_node **, const char *, ...);


typedef enum {
    LYD_PATH_STD,
    LYD_PATH_STD_NO_LAST_PRED
} LYD_PATH_TYPE;

char* lyd_path(const struct lyd_node *, LYD_PATH_TYPE, char *, size_t);

const char * lyd_get_value(const struct lyd_node *);
struct lyd_node* lyd_child(const struct lyd_node *);


typedef enum {
   LYS_OUT_UNKNOWN,
   LYS_OUT_YANG,
   LYS_OUT_YANG_COMPILED,
   LYS_OUT_YIN,
   LYS_OUT_TREE
} LYS_OUTFORMAT;

LY_ERR lys_print_module(struct ly_out *, const struct lys_module *, LYS_OUTFORMAT, size_t, uint32_t);


LY_ERR lys_find_xpath(const struct ly_ctx *, const struct lysc_node *, const char *, uint32_t, struct ly_set **);
void ly_set_free(struct ly_set *, void(*)(void *obj));

struct ly_set {
	uint32_t size;
	uint32_t count;
    union {
        struct lyd_node **dnodes;
        struct lysc_node **snodes;
        void **objs;
    };
};

LY_ERR lyd_find_target(const struct ly_path *path, const struct lyd_node *tree, struct lyd_node **match );

struct lysc_node_list {
    struct lysc_node *child;
    struct lysc_must *musts;
    struct lysc_when **when;
    struct lysc_node_action *actions;
    struct lysc_node_notif *notifs;
    struct lysc_node_leaf ***uniques;
    uint32_t min;
    uint32_t max;
    ...;
};

struct lysc_node_leaflist {
    struct lysc_must *musts;
    struct lysc_when **when;
    struct lysc_type *type;
    const char *units;
    struct lyd_value **dflts;
    uint32_t min;
    uint32_t max;
    ...;
};

struct lysp_node_list {
    struct lysp_restr *musts;
    struct lysp_when *when;
    const char *key;
    struct lysp_tpdf *typedefs;
    struct lysp_node_grp *groupings;
    struct lysp_node *child;
    struct lysp_node_action *actions;
    struct lysp_node_notif *notifs;
    struct lysp_qname *uniques;
    uint32_t min;
    uint32_t max;
    ...;
};


struct lyd_node {
    uint32_t hash;
    uint32_t flags;
    const struct lysc_node *schema;
    struct lyd_node_inner *parent;
    struct lyd_node *next;
    struct lyd_node *prev;
    struct lyd_meta *meta;
    void *priv;
};


struct lysc_node {
    uint16_t nodetype;
    uint16_t flags;
    struct lys_module *module;
    struct lysc_node *parent;
    struct lysc_node *next;
    struct lysc_node *prev;
    const char *name;
    const char *dsc;
    const char *ref;
    struct lysc_ext_instance *exts;
    void *priv;
    ...;
};


LY_ERR lyd_new_term(struct lyd_node *, const struct lys_module *, const char *, const char *, uint32_t, struct lyd_node **);
LY_ERR lyd_new_inner(struct lyd_node *, const struct lys_module *, const char *, ly_bool, struct lyd_node **);
LY_ERR lyd_new_list(struct lyd_node *, const struct lys_module *, const char *, uint32_t, struct lyd_node **node, ...);

////////////////////////////
void get_list_keys_from_data_node(const struct lyd_node* data_node);
void print_node(struct lyd_node* node);
void print_nodes_recursively(struct lyd_node* node);

struct lyd_node* get_differences(struct lyd_node* first_node, struct lyd_node* second_node);
struct lyd_node* get_next_node(struct lyd_node* node);
struct lyd_node* get_node_at_xpath(struct lyd_node* node, char* xpath);
struct lyd_node* get_sibling(struct lyd_node* node);

void test();

//////////////////////////// LIBYANG DECLARATIONS

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

#define LYD_VALUE_FIXED_MEM_SIZE 24

#define LYS_NODE_HASH_COUNT 4

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
LY_ERR ly_set_add(struct ly_set *set, const void *object, ly_bool list, uint32_t *index_p);
LY_ERR ly_set_new(struct ly_set **set_p);

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


struct lyd_meta {
    struct lyd_node *parent;
    struct lyd_meta *next;
    struct lysc_ext_instance *annotation;
    const char *name;
    struct lyd_value value;
};


struct lyd_value {
    const char *_canonical;
    const struct lysc_type *realtype;

    union {
        int8_t boolean;
        int64_t dec64;
        int8_t int8;
        int16_t int16;
        int32_t int32;
        int64_t int64;
        uint8_t uint8;
        uint16_t uint16;
        uint32_t uint32;
        uint64_t uint64;
        struct lysc_type_bitenum_item *enum_item;
        struct lysc_ident *ident;
        struct ly_path *target;
        struct lyd_value_union *subvalue;
        void *dyn_mem;
        uint8_t fixed_mem[LYD_VALUE_FIXED_MEM_SIZE];
    };
};

typedef enum {
    LY_TYPE_UNKNOWN = 0,
    LY_TYPE_BINARY,
    LY_TYPE_UINT8,
    LY_TYPE_UINT16,
    LY_TYPE_UINT32,
    LY_TYPE_UINT64,
    LY_TYPE_STRING,
    LY_TYPE_BITS,
    LY_TYPE_BOOL,
    LY_TYPE_DEC64,
    LY_TYPE_EMPTY,
    LY_TYPE_ENUM,
    LY_TYPE_IDENT,
    LY_TYPE_INST,
    LY_TYPE_LEAFREF,
    LY_TYPE_UNION,
    LY_TYPE_INT8,
    LY_TYPE_INT16,
    LY_TYPE_INT32,
    LY_TYPE_INT64
} LY_DATA_TYPE;

#define LY_DATA_TYPE_COUNT 20

struct lysc_type {
    const char *name;
    struct lysc_ext_instance *exts;
    struct lyplg_type *plugin;
    LY_DATA_TYPE basetype;
    uint32_t refcount;
};

struct lysc_node_leaf {
    union {
        struct lysc_node node;

        struct {
            uint16_t nodetype;
            uint16_t flags;
            uint8_t hash[LYS_NODE_HASH_COUNT];
            struct lys_module *module;
            struct lysc_node *parent;
            struct lysc_node *next;
            struct lysc_node *prev;
            const char *name;
            const char *dsc;
            const char *ref;
            struct lysc_ext_instance *exts;
            void *priv;
        };
    };

    struct lysc_must *musts;
    struct lysc_when **when;
    struct lysc_type *type;

    const char *units;
    struct lyd_value *dflt;
};

// enum lyd_diff_op {
//     LYD_DIFF_OP_CREATE,
//     LYD_DIFF_OP_DELETE,
//     LYD_DIFF_OP_REPLACE,
//     LYD_DIFF_OP_NONE
// };

LY_ERR lyd_new_term(struct lyd_node *, const struct lys_module *, const char *, const char *, uint32_t, struct lyd_node **);
LY_ERR lyd_new_inner(struct lyd_node *, const struct lys_module *, const char *, ly_bool, struct lyd_node **);
LY_ERR lyd_new_list(struct lyd_node *, const struct lys_module *, const char *, uint32_t, struct lyd_node **node, ...);

void lyd_free_all(struct lyd_node *node);
void lyd_free_tree(struct lyd_node *node);

struct lyd_node * lyd_parent(const struct lyd_node *node);
LY_ERR lyd_change_term(struct lyd_node *term, const char *val_str);
LY_ERR lyd_validate_all(struct lyd_node **tree, const struct ly_ctx *ctx, uint32_t val_opts, struct lyd_node **diff);
LY_ERR lyd_validate_module(struct lyd_node **tree, const struct lys_module *module, uint32_t val_opts, struct lyd_node **diff);

LY_ERR lyd_print_all(struct ly_out *out, const struct lyd_node *root, LYD_FORMAT format, uint32_t options);
LY_ERR lyd_print_tree(struct ly_out *out, const struct lyd_node *root, LYD_FORMAT format, uint32_t options);

LY_ERR lyd_find_path(const struct lyd_node *ctx_node, const char *path, ly_bool output, struct lyd_node **match);

// not exported?
// LY_ERR lyd_diff_get_op(const struct lyd_node *diff_node, enum lyd_diff_op *op);
// void lyd_diff_find_meta(const struct lyd_node *node, const char *name, struct lyd_meta **meta, struct lyd_attr **attr);

// struct lyd_meta* lyd_find_meta (const struct lyd_meta *first, const struct lys_module *module, const char *name);

#define LYD_PRINT_WITHSIBLINGS  0x01
#define LYD_PRINT_KEEPEMPTYCONT 0x04
#define LYD_PRINT_WD_MASK       0xF0
#define LYD_PRINT_WD_EXPLICIT   0x00
#define LYD_PRINT_WD_TRIM       0x10
#define LYD_PRINT_WD_ALL        0x20
#define LYD_PRINT_WD_ALL_TAG    0x40
#define LYD_PRINT_WD_IMPL_TAG   0x80

//////////////////////////// cJSON DECLARATIONS

#define cJSON_False 0
#define cJSON_True 1
#define cJSON_NULL 2
#define cJSON_Number 3
#define cJSON_String 4
#define cJSON_Array 5
#define cJSON_Object 6
#define cJSON_Raw 7

typedef struct cJSON {
    struct cJSON *next;
    struct cJSON *prev;
    struct cJSON *child;

    int type;
    char *valuestring;
    int valueint;
    double valuedouble;

    char *string;
} cJSON;

struct cJSON* cJSON_CreateObject(void);
void cJSON_AddStringToObject(struct cJSON *object, const char *name, const char *string);
void cJSON_ReplaceItemInObject(struct cJSON *object, const char *name, struct cJSON *newitem);
void cJSON_DeleteItemFromObject(struct cJSON *object, const char *name);
void cJSON_AddItemToObject(struct cJSON *object, const char *name, struct cJSON *item);
char* cJSON_Print(const struct cJSON *item);
void cJSON_Delete(struct cJSON *item);

//////////////////////////// OTHER DECLARATIONS

void free(void *ptr);

//////////////////////////// CUSTOM DECLARATIONS

struct ly_set* get_list_keys_from_data_node(const struct lyd_node* data_node);
struct lyd_node* get_differences(struct lyd_node* first_node, struct lyd_node* second_node);
struct lyd_node* get_next_node(struct lyd_node* node);
struct lyd_node* get_node_at_xpath(struct lyd_node* node, char* xpath);

char* evaluate_differences(struct lyd_node* diff_node, bool skip_containers_and_lists);
void free_list_keys(struct ly_set* key_set);
void print_node(struct lyd_node* node);
void print_nodes_recursively(struct lyd_node* node);
void test();

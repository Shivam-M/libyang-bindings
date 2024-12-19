import os
from bindings import _test
from bindings._test import ffi
from typing import Union


def str2c(py_string):
    return ffi.new("char []", py_string.encode("utf-8")) if py_string is not None else ffi.NULL

def c2str(c_string, free=False):
    py_string = ffi.string(c_string).decode("utf-8") if c_string != ffi.NULL else None
    if (free and py_string):
        _test.lib.free(c_string)
    return py_string


class Module:
    def __init__(self, data, context) -> None:
        self._data = data
        self._context = context

    def print(self, output=os.sys.stdout):
        ly_out = ffi.new("struct ly_out**")
        _test.lib.ly_out_new_fd(output.fileno(), ly_out)
        _test.lib.lys_print_module(ly_out[0], self._data, _test.lib.LYS_OUT_TREE, 0, 0)


class Context:
    def __init__(self) -> None:
        context_pointer = ffi.new("struct ly_ctx**")
        _test.lib.ly_ctx_new(ffi.NULL, _test.lib.LY_CTX_NO_YANGLIBRARY, context_pointer)
        self._data = context_pointer[0]

    # def __del__(self):
    #     self.free()

    def free(self):
        if self._data:
            _test.lib.ly_ctx_destroy(self._data)
            self._data = None

    def test(self):
        _test.lib.test()
    
    def add_search_path(self, search_path: str):
        _test.lib.ly_ctx_set_searchdir(self._data, str2c(search_path))
    
    def load_module(self, module_path: str) -> Module:
        return Module(_test.lib.ly_ctx_load_module(self._data, str2c(module_path), ffi.NULL, ffi.NULL), self)
    
    def load_data(self, data_path: str):
        top_node = ffi.new("struct lyd_node**")
        ly_in = ffi.new("struct ly_in**")
        data_format = _test.lib.LYD_JSON if data_path.endswith("json") else _test.lib.LYD_XML

        _test.lib.ly_in_new_filepath(str2c(data_path), 0, ly_in)
        _test.lib.lyd_parse_data(self._data, ffi.NULL, ly_in[0], data_format, 0, 0, top_node)
        _test.lib.ly_in_free(ly_in[0], 0)

        return Node(top_node[0], self)

    def resolve_type(self):
        pass

    def get_differences(self, first_node, second_node):
        return Node(_test.lib.get_differences(first_node._data, second_node._data), self)

    def evaluate_differences(self, first_node, second_node, diff_node):
        changes = {}
        for node in diff_node.get_following_nodes():
            xpath = node._xpath
            value_first = first_node.get_value_at_xpath(xpath)
            value_second = second_node.get_value_at_xpath(xpath)
            changes[xpath] = {}

            if value_first:
                changes[xpath]["action"] = "removed"
                changes[xpath]["old_value"] = value_first

            if value_second:
                changes[xpath]["action"] = "created"
                changes[xpath]["new_value"] = value_second

            if value_first and value_second:
                changes[xpath]["action"] = "changed"

            if value_first == value_second:
                del changes[xpath]
        return changes
    
    ## move create/add methods to leaflistnode
    def create_list_node(self, parent, name, values):
        list_node = ffi.new("struct lyd_node**")
        _test.lib.lyd_new_list(parent._data, ffi.NULL, str2c(name), 0, list_node, *[str2c(value) for value in values])
        return Node(list_node[0], self)

    def create_inner_node(self, parent, name):
        inner_node = ffi.new("struct lyd_node**")
        _test.lib.lyd_new_inner(parent._data, ffi.NULL, str2c(name), 0, inner_node)
        return Node(inner_node[0], self)

    def create_terminal_node(self, parent, name, value):
        terminal_node = ffi.new("struct lyd_node**")
        _test.lib.lyd_new_term(parent._data, ffi.NULL, str2c(name), str2c(value), 0, terminal_node)
        return Node(terminal_node[0], self)



class Node:
    def __init__(self, data, context: Context) -> None:
        self._data = data
        self._context = context
    
    # def __del__(self):
    #     self.free()

    def free(self):
        if self._data:
            if self.is_root():
                # print(f"Attempt to free: {self}")
                _test.lib.lyd_free_all(self._data)
                self._data = None

    def is_root(self):
        return self._data.parent == ffi.NULL

    def __setattr__(self, name: str, value: str):
        # if name in self.__dict__.keys():
        if name.startswith('_'):  # TODO: change this
            self.__dict__[name] = value
        else:
            _test.lib.lyd_change_term(self.__getattr__(name)._data, str2c(value))

    def __getattr__(self, name: str):
        match name:
            case "_name":
                return c2str(self._data.schema.name).replace('-', '_').lower()
            case "_xpath":
                return c2str(_test.lib.lyd_path(self._data, 0, ffi.NULL, 0), free=True)  # store instead?
            case "_value":
                return c2str(_test.lib.lyd_get_value(self._data))
            case "_parent":
                if parent_node_data := _test.lib.lyd_parent(self._data):
                    return Node(parent_node_data, self._context)
                return
            case _:
                for node in self.get_children():
                    if name == node._name:
                        return node
                raise Exception("child does not exist...")

    def __getitem__(self, name: Union[str, tuple]):
        key_set = _test.lib.get_list_keys_from_data_node(self._data)
        list_keys = []

        for x in range(key_set.count):
            list_keys.append(c2str(ffi.cast("char*", key_set.objs[x])))

        _test.lib.ly_set_free(key_set, ffi.NULL)

        if isinstance(name, (int, str)):
            name = (str(name),)

        constructed_xpath = f"{self._name}"
        for i, key in enumerate(name):
            if i >= len(list_keys):
                raise Exception("too many keys")
            constructed_xpath += f"[{list_keys[i]}='{key}']"

        return self._parent.get_node_at_xpath(constructed_xpath)

    def __str__(self):
        return f"{self._xpath} = {self._value}"

    def get_list_keys(self):
        _test.lib.get_list_keys_from_data_node(self._data)

    def print(self):
        _test.lib.print_node(self._data)

    def get_following_nodes(self):
        next_node = self._data
        while (next_node):
            if next_node := _test.lib.get_next_node(next_node):
                yield Node(next_node, self._context)

    def get_node_at_xpath(self, xpath):
        return Node(_test.lib.get_node_at_xpath(self._data, str2c(xpath)), self._context)

    def get_value_at_xpath(self, xpath):
        node = self.get_node_at_xpath(xpath)
        return node._value if node else None

    def get_children(self):
        child = _test.lib.lyd_child(self._data)
        while child:
            yield Node(child, self._context)
            child = _test.lib.get_sibling(child)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self._data == other._data


class LeafNode(Node):
    def __init__(self, data, context: Context) -> None:
        super(data, context)
    
    def set_value(self, value: str):
        pass


class LeafListNode(Node):
    def __init__(self, data, context: Context) -> None:
        super(data, context)

    def __iter__(self):
        yield None


class ContainerNode(Node):
    def __init__(self, data, context: Context) -> None:
        super(data, context)

    def __iter__(self):
        yield None


class Test:
    def print_nodes_recursively(node: Node):
        _test.lib.print_nodes_recursively(node._data)

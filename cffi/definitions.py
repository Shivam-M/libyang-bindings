import os
import _test as _test
from _test import ffi as ffi


def str2c(py_string, encode=True):
    if py_string is None:
        return ffi.NULL 
    if encode:
        py_string = py_string.encode("utf-8")
    return ffi.new("char []", py_string)


def c2str(c_string, decode=True):
    if c_string == ffi.NULL:
        return None
    c_string = ffi.string(c_string)
    if decode:
        c_string = c_string.decode("utf-8")
    return c_string


class Module:
    def __init__(self, data, context) -> None:
        self._data = data
        self._context = context

    def print(self):
        ly_out = ffi.new("struct ly_out**")
        _test.lib.ly_out_new_fd(os.sys.stdout.fileno(), ly_out)
        _test.lib.lys_print_module(ly_out[0], self._data, _test.lib.LYS_OUT_TREE, 0, 0);


class Context:
    def __init__(self) -> None:
        context_pointer = ffi.new("struct ly_ctx**")
        _test.lib.ly_ctx_new(ffi.NULL, _test.lib.LY_CTX_NO_YANGLIBRARY, context_pointer)
        self._data = context_pointer[0]
    
    def add_search_path(self, search_path: str):
        _test.lib.ly_ctx_set_searchdir(self._data, str2c(search_path))
    
    def load_module(self, module_path: str):
        return Module(_test.lib.ly_ctx_load_module(self._data, str2c(module_path), ffi.NULL, ffi.NULL), self)
    
    def load_data(self, data_path: str):
        top_node = ffi.new("struct lyd_node**")
        ly_in = ffi.new("struct ly_in**")
        data_format = _test.lib.LYD_JSON if data_path.endswith("json") else _test.lib.LYD_XML

        _test.lib.ly_in_new_filepath(str2c(data_path), 0, ly_in)
        _test.lib.lyd_parse_data(self._data, ffi.NULL, ly_in[0], data_format, 0, 0, top_node)

        return Node(top_node[0], self)


class Node:
    def __init__(self, data, context: Context) -> None:
        self._data = data
        self._context = context
    
    def __getattr__(self, name: str):
        match name:
            case "_xpath":
                return c2str(_test.lib.lyd_path(self._data, 0, ffi.NULL, 0))
            case "_value":
                return c2str(_test.lib.lyd_get_value(self._data))
            case "_parent":
                return None

    def __del__(self):
        pass


class LeafNode:
    def __init__(self, data, context: Context) -> None:
        super(data, context)
    
    def set_value(self, value: str):
        pass


class LeafListNode:
    def __init__(self, data, context: Context) -> None:
        super(data, context)

    def __iter__(self):
        yield None


class ContainerNode:
    def __init__(self, data, context: Context) -> None:
        super(data, context)

    def __iter__(self):
        yield None


class Test:
    def print_nodes_recursively(node: Node):
        _test.lib.print_nodes_recursively(node._data)

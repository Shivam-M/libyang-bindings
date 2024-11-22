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


class Context:
    def __init__(self) -> None:
        context_pointer = ffi.new("struct ly_ctx**")
        _test.lib.ly_ctx_new(ffi.NULL, _test.lib.LY_CTX_NO_YANGLIBRARY, context_pointer)
        self._data = context_pointer[0]
    
    def add_search_path(self, path):
        _test.lib.ly_ctx_set_searchdir(self._data, str2c(path))
    
    def load_module(self, module):
        _test.lib.ly_ctx_load_module(self._data, str2c(module), ffi.NULL, ffi.NULL)
    
    def load_data(self, data_path):
        top_node = ffi.new("struct lyd_node**")
        ly_in = ffi.new("struct ly_in**")
        data_format = _test.lib.LYD_JSON if data_path.endswith("json") else _test.lib.LYD_XML

        _test.lib.ly_in_new_filepath(str2c(data_path), 0, ly_in)
        _test.lib.lyd_parse_data(self._data, ffi.NULL, ly_in[0], data_format, 0, 0, top_node)

        return Node(top_node[0])


class Node:
    def __init__(self, data) -> None:
        self._data = data
    
    def __getattr__(self, name: str):
        match name:
            case "_xpath":
                return c2str(_test.lib.lyd_path(self._data, 0, ffi.NULL, 0))
            case "_value":
                return c2str(_test.lib.lyd_get_value(self._data))
            case "_parent":
                return None


class Test:
    def print_nodes_recursively(node: Node):
        _test.lib.print_nodes_recursively(node._data)

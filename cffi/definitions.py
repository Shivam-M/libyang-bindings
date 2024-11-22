from typing import Any
import cffi._test
import cffi._test.ffi as ffi


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
        self._data = None
    
    def load_module(self, module):
        pass
    
    def load_data(self, data):
        pass


class Node:
    def __init__(self) -> None:
        self._data = None
    
    def __getattribute__(self, name: str) -> Any:
        match name:
            case "_xpath":
                return c2str(cffi._test.lyd_path(self._data, 0, cffi._test.ffi.NULL, 0))
            case "_value":
                return c2str(cffi._test.lyd_get_value(self._data))

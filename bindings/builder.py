from cffi import FFI

ffi = FFI()

with open("header.h", "r") as header:
    ffi.cdef(header.read())

with open("source.c", "r") as source:
    ffi.set_source("_test", source.read(), libraries=["yang"], library_dirs=["/usr/local/lib"], include_dirs=["/usr/local/include"], extra_compile_args=["-g"])

ffi.compile()
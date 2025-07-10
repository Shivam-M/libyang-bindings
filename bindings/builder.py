import os
from cffi import FFI

HEADER_FILE = "header.h"
SOURCE_FILE = "source.c"
OBJECT_NAME = "_test"
OBJECT_FILE = f"{OBJECT_NAME}.o"

def needs_rebuild() -> bool:
    if not os.path.exists(OBJECT_FILE):
        return True
    last_compiled_time = os.path.getmtime(OBJECT_FILE)
    latest_modified_time = max(os.path.getmtime(HEADER_FILE), os.path.getmtime(SOURCE_FILE))
    return latest_modified_time > last_compiled_time

def build() -> None:
    ffi = FFI()

    with open(HEADER_FILE, "r") as header:
        ffi.cdef(header.read())

    with open(SOURCE_FILE, "r") as source:
        ffi.set_source(
                    OBJECT_NAME,
                    source.read(),
                    libraries=["yang", "cjson"],
                    library_dirs=["/usr/local/lib"],
                    include_dirs=["/usr/local/include"],
                    extra_compile_args=["-g"])

    ffi.compile()

if os.environ.get("FORCE_REBUILD", False) or needs_rebuild():
    build()
else:
    print("skip: build")

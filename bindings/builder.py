import os
from cffi import FFI

HEADER_FILE = "header.h"
SOURCE_FILE = "source.c"
OBJECT_NAME = "_test"
OBJECT_FILE = f"{OBJECT_NAME}.o"

def get_env(env_var: str) -> list:
    return [v.strip() for v in os.getenv(env_var, "").split(":") if v.strip()]

LIBYANG_LIB_DIRS = get_env("EXTRA_LIBYANG_LIB_DIRS") + ["/usr/local/lib"]
LIBYANG_INCLUDE_DIRS = get_env("EXTRA_LIBYANG_INCLUDE_DIRS") + ["/usr/local/include"]
LIBYANG_LINK_ARGS = [f"-Wl,-rpath,{path}" for path in LIBYANG_LIB_DIRS]

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
                    library_dirs=LIBYANG_LIB_DIRS,
                    include_dirs=LIBYANG_INCLUDE_DIRS,
                    extra_link_args=LIBYANG_LINK_ARGS,
                    extra_compile_args=["-g"])

    ffi.compile()

if os.environ.get("FORCE_REBUILD", False) or needs_rebuild():
    build()
else:
    print("skip: build")

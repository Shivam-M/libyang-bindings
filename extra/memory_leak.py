import sys
from cffi import FFI

ffi = FFI()

ffi.cdef(
    """
    void* malloc(size_t size);
    """
)

C = ffi.dlopen(None)

def create_memory_leak(allocate):
    for _ in range(5):
        if allocate:
            print("Allocating...")
            ptr = C.malloc(1024)
            ptr = ffi.NULL
        else:
            print("Doing nothing.")


if __name__ == "__main__":
    create_memory_leak(len(sys.argv) > 1)

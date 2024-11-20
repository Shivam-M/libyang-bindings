import libyang
import os


os.environ["YANGPATH"] = "/home/shivam/libyang-cffi-playground"

ctx = libyang.Context()

module = ctx.load_module('example')

if module:
    print("** load_module: worked")
else:
    print("** load_module: fail")

print("** module name:", module)

for x in module:
    for y in x.iter_tree():
        print(y)

try:
    DATA_FILE = "example_data.xml"
    data_tree = ctx.parse_data_file(open(DATA_FILE, "r+"), fmt="xml")
    print("** parse_data_file:", DATA_FILE)
except libyang.util.LibyangError as e:
    print(f"** parse_data_file: {e}")
    exit(1)

for node in data_tree:
    print(f"Node name: {node.schema().name()}, Value: {node.print_mem(fmt='json')}")
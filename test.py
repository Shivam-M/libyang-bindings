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


DATA_FILE = "example_data.json"
data_tree = ctx.parse_data_file(open(DATA_FILE, "r+"), fmt=DATA_FILE.split('.')[-1])
print("** parse_data_file:", DATA_FILE)


for node in data_tree:
    print(f"Node name: {node.schema().name()}, Value: {node.print_mem(fmt='json')}")
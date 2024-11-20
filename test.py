import libyang
import os
from typing import Optional
from libyang.data import DNode


os.environ["YANGPATH"] = "/home/shivam/libyang-cffi-playground/yang"

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


DATA_FILE_1 = "data/example_data.json"
DATA_FILE_2 = "data/example_data_2.xml"

def load_data_tree(file_path: str) -> Optional[DNode]:
    return ctx.parse_data_file(open(file_path, 'r'), fmt=file_path.split('.')[-1])

data_tree_1 = load_data_tree(DATA_FILE_1)
data_tree_2 = load_data_tree(DATA_FILE_2)


# calculate diff with built-in libyang method
diffs = data_tree_1.diff(data_tree_2)
if diffs:
    print("differences:")
    for diff in diffs:
        xpath = diff.path()
        print(f"xpath: {xpath}")
        print(f"  diff info: {diff.print_mem(fmt='json')}")
else:
    print(f"{DATA_FILE_1} and {DATA_FILE_2} are the same")


# calculate diff using own worse method
def get_nodes_with_values(data_tree: Optional[DNode]) -> dict:
    node_values = {}
    for node in data_tree:
        xpath = node.path()
        value = node.print_mem(fmt='json')
        node_values[xpath] = value
    return node_values

nodes_values_1 = get_nodes_with_values(data_tree_1)
nodes_values_2 = get_nodes_with_values(data_tree_2)

differences = []
for xpath in set(nodes_values_1.keys()).union(nodes_values_2.keys()):
    if (value_1 := nodes_values_1.get(xpath)) != (value_2 := nodes_values_2.get(xpath)):
        differences.append({
            'xpath': xpath,
            'value_1': value_1,
            'value_2': value_2
        })

if differences:
    print("differences: ")
    for difference in differences:
        print(f"xpath: {difference['xpath']}")
        print(f" 1. {DATA_FILE_1}: {difference['value_1']}")
        print(f" 2. {DATA_FILE_2}: {difference['value_2']}")
else:
    print(f"{DATA_FILE_1} and {DATA_FILE_2} are the same")

import _test

def print_nodes_with_custom_c_function(data_tree: Optional[DNode]):
    for node in data_tree:
        node_cdata = _test.ffi.cast("struct lyd_node *", node.cdata) # don't mix with libyang-cffi?
        _test.lib.print_node(node_cdata)

def print_all_nodes_in_tree_with_custom_c_function(data_tree: Optional[DNode]):
    data_tree_cdata = _test.ffi.cast("struct lyd_node *", data_tree.cdata)
    _test.lib.print_nodes_recursively(data_tree_cdata)


print('*', DATA_FILE_1)
# print_nodes_with_custom_c_function(data_tree_1)
print_all_nodes_in_tree_with_custom_c_function(data_tree_1)
print('\n *', DATA_FILE_2)
# print_nodes_with_custom_c_function(data_tree_2)
print_all_nodes_in_tree_with_custom_c_function(data_tree_2)
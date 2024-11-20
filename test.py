import libyang
import os


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

def load_data_tree(file_path):
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
def get_nodes_with_values(data_tree):
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

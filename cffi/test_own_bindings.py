import os
from definitions import Context, Test

os.environ["YANGPATH"] = "/home/shivam/libyang-cffi-playground/yang"
context = Context()

for path in os.environ.get("YANGPATH", "").split(":"):
    context.add_search_path(path)

context.load_module("example")

data_tree = context.load_data("/home/shivam/libyang-cffi-playground/data/example_data.json")

Test.print_nodes_recursively(data_tree)

# for (xpath, value) in data_tree._parent.get_all_xpaths_and_values():
#    print(f"{xpath} = {value}")
import os
from definitions import Context, Test

os.environ["YANGPATH"] = "yang"
context = Context()

for path in os.environ.get("YANGPATH", "").split(":"):
    context.add_search_path(path)

example_module = context.load_module("example")

print(example_module.print())

data_tree_1 = context.load_data("data/example_data.json")
data_tree_2 = context.load_data("data/example_data_2.xml")

Test.print_nodes_recursively(data_tree_1)

print("**")

Test.print_nodes_recursively(data_tree_2)

# for (xpath, value) in data_tree._parent.get_all_xpaths_and_values():
#    print(f"{xpath} = {value}")
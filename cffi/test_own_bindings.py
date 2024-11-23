import os
import json
from definitions import Context, Test

YANG_PATHS = "yang"
context = Context()

for path in YANG_PATHS.split(":"):
    context.add_search_path(path)

example_module = context.load_module("example")
example_module.print()

DATA_FILE_3 = "data/example_data_3.json"
DATA_FILE_3B = "data/example_data_3b.xml"

data_tree_1 = context.load_data(DATA_FILE_3)
data_tree_2 = context.load_data(DATA_FILE_3B)

# Test.print_nodes_recursively(data_tree_1)

print("\n*", DATA_FILE_3)
for node in data_tree_1.get_following_nodes():
    if node._value:
        print(f"{node._xpath} = {node._value}")

print("\n*", DATA_FILE_3B)
for node in data_tree_2.get_following_nodes():
    if node._value:
        print(f"{node._xpath} = {node._value}")

print(f"\n* updates from {DATA_FILE_3} -> {DATA_FILE_3B}:")
diff_tree = context.get_differences(data_tree_1, data_tree_2)
for node in diff_tree.get_following_nodes():
    if node._value:
        print(f"{node._xpath} = {node._value}")

differences = context.evaluate_differences(data_tree_1, data_tree_2, diff_tree)
# print(json.dumps(differences, indent=4))

print(f"\n* differences from {DATA_FILE_3} -> {DATA_FILE_3B}: ")
for xpath, change in differences.items():
    action = change["action"]
    if action == "changed":
        print(f"{xpath} = \t CHANGED: {change["old_value"]} -> {change["new_value"]}")
    elif action == "removed":
        print(f"{xpath} = \t REMOVED: {change["old_value"]}")
    elif action == "created":
        print(f"{xpath} = \t CREATED: {change["new_value"]}")

# return something like
# { xpath: {
#     action: created,
#     new_value: 123
#  },
#   xpath2: {
#     action: removed,
#     old_value: 123
#   },
#   xpath3: {
#     action: modified,
#     old_value: 123,
#     new_value: 321
#   }
# }

# Test.print_nodes_recursively(data_tree_2)

# for (xpath, value) in data_tree._parent.get_all_xpaths_and_values():
#    print(f"{xpath} = {value}")
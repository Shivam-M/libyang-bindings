import json
from bindings.definitions import Context, Test

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

def print_differences(differences):
    for xpath, change in differences.items():
        action = change["action"]
        if action == "changed":
            print(f"{xpath} = \t\u001b[37;43m\u001b[30m CHANGED \033[0m {change["old_value"]} -> {change["new_value"]}")
        elif action == "removed":
            print(f"{xpath} = \t\u001b[37;41m\u001b[30m REMOVED \033[0m {change["old_value"]}")
        elif action == "created":
            print(f"{xpath} = \t\u001b[37;42m\u001b[30m CREATED \033[0m {change["new_value"]}")

print(f"\n* differences from {DATA_FILE_3} -> {DATA_FILE_3B}: ")
diff_tree = context.get_differences(data_tree_1, data_tree_2)
differences = context.evaluate_differences(data_tree_1, data_tree_2, diff_tree)
# print(json.dumps(differences, indent=4))
print_differences(differences)

print(f"\n* [C method] differences from {DATA_FILE_3} -> {DATA_FILE_3B}: ")
differences_c = json.loads(Test.evaluate_differences_c(data_tree_1, data_tree_2, diff_tree))
# print(json.dumps(differences_c, indent=4))
print_differences(differences_c)

assert differences == differences_c

access_list_node = data_tree_2.get_node_at_xpath("/example:interface/access-list")
new_rule = context.create_list_node(access_list_node, "rule", ["7.7.7.7"])
# context.create_terminal_node(new_rule, "action", "DENY")  # todo: build automatically based on schema
new_rule.action = "ALLOW"

if new_rule in access_list_node.get_children():
    print("\n* node was added")

print("\n* updated access-list:")
for rule in access_list_node.get_children():
    endpoint = rule.get_value_at_xpath("endpoint")
    action = rule.get_value_at_xpath("action")
    print(endpoint, action)

print("\n* get list item from leaf-list: ")
specific_rule = data_tree_2.access_list.rule["7.7.7.7"]
[child.print() for child in specific_rule.get_children()]

DATA_FILE_4 = "data/example_data_4.xml"
data_tree_4 = context.load_data(DATA_FILE_4)

print("\n*", DATA_FILE_4)
for node in data_tree_4.get_following_nodes():
    if node._value:
        print(f"{node._xpath} = {node._value}")

print("\n* get multi-key item from leaf-list: ")
specific_neighbour = data_tree_4.neighbour["1.1.1.2", "VRF_2", "GigabitEthernet2"]
specific_neighbour.state = "DOWN"
specific_neighbour.information = "Hello"
[child.print() for child in specific_neighbour.get_children()]

new_neighbour = context.create_list_node(data_tree_4, "neighbour", ["1.1.1.4", "VRF_4", "GigabitEthernet4"])

if new_rule in access_list_node.get_children():
    print("\n* node was added")

print(f"\n* updated {DATA_FILE_4}")
for node in data_tree_4.get_following_nodes():
    if node._value:
        print(f"{node._xpath} = {node._value}")

print(f"\n* dump xml tree {DATA_FILE_4}")
data_tree_4.print_tree()

print("\n* node types: ")
print(f"{data_tree_4._type=}")
print(f"{new_neighbour._type=}")
print(f"{specific_rule.get_child_by_name("endpoint")._type=}")

# Move to using __del__ and/or ffi.gc:
# data_tree_1.free()
# data_tree_2.free()
# data_tree_4.free()
# diff_tree.free()
# context.free()

# Test.print_nodes_recursively(data_tree_2)

# for (xpath, value) in data_tree._parent.get_all_xpaths_and_values():
#    print(f"{xpath} = {value}")
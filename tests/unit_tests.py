import pytest
from bindings.definitions import Context


@pytest.fixture
def context():  # TODO: free
    context = Context()
    context.add_search_path("yang")
    context.load_module("example")
    return context


def test_change_node_value(context):
    # Arrange
    data_tree = context.load_data("data/example_data_3b.xml")
    interface = data_tree  # TODO: Change so first node isn't classed as the "root"

    # Act
    interface.name = "TenGigabitEthernet99"

    # Assert
    assert interface.name == "TenGigabitEthernet99"


def test_create_node_value(context):
    # Arrange
    data_tree = context.load_data("data/example_data_4.xml")
    interface = data_tree

    # Act
    interface.mtu = 1234

    # Assert
    assert interface.mtu == "1234"  # TODO: Add type casting based on data type in schema


def test_differences_exact_match(context):
    # Arrange
    data_tree_1 = context.load_data("data/example_data_3b.xml")
    data_tree_2 = context.load_data("data/example_data_3b.json")

    # Act
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    differences = context.evaluate_differences(data_tree_1, data_tree_2, diff_tree)

    # Assert
    assert differences == {}


def test_differences_changed_removed_created(context):
    # Arrange
    data_tree_1 = context.load_data("data/example_data_3.xml")
    data_tree_2 = context.load_data("data/example_data_3b.xml")

    # Act
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    differences = context.evaluate_differences(data_tree_1, data_tree_2, diff_tree)

    # Assert
    assert differences == {
        "/example:interface/access-list/rule[endpoint='1.1.1.1']/action": {
           "action": "changed",
           "new_value": "DENY",
           "old_value": "ALLOW"
       },
       "/example:interface/access-list/rule[endpoint='2.2.2.2']/action": {
           "action": "changed",
           "new_value": "ALLOW",
           "old_value": "DENY"
       },
       "/example:interface/access-list/rule[endpoint='3.3.3.3']/action": {
           "action": "removed",
           "old_value": "DEFAULT"
       },
       "/example:interface/access-list/rule[endpoint='3.3.3.3']/endpoint": {
           "action": "removed",
           "old_value": "3.3.3.3"
       },
       "/example:interface/access-list/rule[endpoint='5.5.5.5']/action": {
           "action": "created",
           "new_value": "DEFAULT"
       },
       "/example:interface/access-list/rule[endpoint='5.5.5.5']/endpoint": {
           "action": "created",
           "new_value": "5.5.5.5"
       }
   }


def test_retrieve_list_element_single_key(context):
    # Arrange
    data_tree = context.load_data("data/example_data_3b.xml")

    # Act
    rule = data_tree.access_list.rule["1.1.1.1"]

    # Assert
    assert rule.action == "DENY"


def test_retrieve_list_element_multiple_keys(context):
    # Arrange
    data_tree = context.load_data("data/example_data_4.xml")

    # Act
    first_neighbour = data_tree.neighbour["1.1.1.2", "VRF_2", "GigabitEthernet2"]
    second_neighbour = data_tree.neighbour["1.1.1.3", "VRF_3", "GigabitEthernet3"]

    # Assert
    assert first_neighbour.state == "UP"
    assert second_neighbour.state == "DOWN"


def test_create_list_element_single_key(context):
    # Arrange
    data_tree = context.load_data("data/example_data_3b.xml")

    # Act
    access_list = data_tree.access_list
    rule = access_list.create("rule", "7.7.7.7")

    # Assert
    assert rule in access_list.get_children()
    assert rule.action == "DEFAULT"


def test_create_list_element_multiple_keys(context):
    # Arrange
    data_tree = context.load_data("data/example_data_4.xml")

    # Act
    neighbour = data_tree.create("neighbour", ["1.1.1.4", "VRF_4", "GigabitEthernet4"])
    neighbour.state = "UP"
    neighbour.information = "This was created at runtime"

    # Assert
    assert neighbour in data_tree.get_children()
    assert neighbour.state == "UP"
    assert neighbour.information == "This was created at runtime"

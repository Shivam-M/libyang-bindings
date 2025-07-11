import pytest
from bindings.definitions import Context, EasyLoad


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
    assert interface.mtu == 1234


def test_cast_node_value(context):
    # Arrange
    data_tree = context.load_data("data/example_data_2.xml")
    interface = data_tree

    # Act
    interface.shutdown = "false"

    # Assert
    assert interface.shutdown == False


def test_retrieve_node_xpath(context):
    # Arrange
    data_tree = context.load_data("data/example_data_3b.xml")
    interface = data_tree

    # Act
    xpath = interface.access_list._xpath

    # Assert
    assert xpath == "/example:interface/access-list"


def test_differences_exact_match(context):
    # Arrange
    data_tree_1 = context.load_data("data/example_data_3b.xml")
    data_tree_2 = context.load_data("data/example_data_3b.json")

    # Act
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    differences = context.evaluate_differences(diff_tree)

    # Assert
    assert differences == {}


def test_differences_changed_removed_created(context):
    # Arrange
    data_tree_1 = context.load_data("data/example_data_3.xml")
    data_tree_2 = context.load_data("data/example_data_3b.xml")

    # Act
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    differences = context.evaluate_differences(diff_tree, skip_containers_and_lists=True)

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
       },
       "/example:interface/neighbour[address='1.1.1.3'][vrf='VRF_3'][interface='GigabitEthernet3']/names/name[id='0']/name": {
            "action": "changed",
            "new_value": "Ned Flanders",
            "old_value": "Ned",
        },
        "/example:interface/neighbour[address='1.1.1.3'][vrf='VRF_3'][interface='GigabitEthernet3']/names/name[id='1']/id": {
            "action": "created",
            "new_value": "1",
        },
        "/example:interface/neighbour[address='1.1.1.3'][vrf='VRF_3'][interface='GigabitEthernet3']/names/name[id='1']/name": {
            "action": "created",
            "new_value": "Maude Flanders",
        }
   }


def test_differences_changed_removed_created_include_containers_and_lists(context):
    # Arrange
    data_tree_1 = context.load_data("data/example_data_3.xml")
    data_tree_2 = context.load_data("data/example_data_3b.xml")

    # Act
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    differences = context.evaluate_differences(diff_tree)

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
       "/example:interface/access-list/rule[endpoint='3.3.3.3']": {
            "action": "removed",
        },
       "/example:interface/access-list/rule[endpoint='3.3.3.3']/action": {
           "action": "removed",
           "old_value": "DEFAULT"
       },
       "/example:interface/access-list/rule[endpoint='3.3.3.3']/endpoint": {
           "action": "removed",
           "old_value": "3.3.3.3"
       },
       "/example:interface/access-list/rule[endpoint='5.5.5.5']": {
            "action": "created",
        },
       "/example:interface/access-list/rule[endpoint='5.5.5.5']/action": {
           "action": "created",
           "new_value": "DEFAULT"
       },
       "/example:interface/access-list/rule[endpoint='5.5.5.5']/endpoint": {
           "action": "created",
           "new_value": "5.5.5.5"
       },
       "/example:interface/neighbour[address='1.1.1.3'][vrf='VRF_3'][interface='GigabitEthernet3']/names/name[id='0']/name": {
            "action": "changed",
            "new_value": "Ned Flanders",
            "old_value": "Ned",
        },
        "/example:interface/neighbour[address='1.1.1.3'][vrf='VRF_3'][interface='GigabitEthernet3']/names/name[id='1']": {
            "action": "created",
        },
        "/example:interface/neighbour[address='1.1.1.3'][vrf='VRF_3'][interface='GigabitEthernet3']/names/name[id='1']/id": {
            "action": "created",
            "new_value": "1",
        },
        "/example:interface/neighbour[address='1.1.1.3'][vrf='VRF_3'][interface='GigabitEthernet3']/names/name[id='1']/name": {
            "action": "created",
            "new_value": "Maude Flanders",
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
    access_list.rule
    rule = access_list.create("rule", "7.7.7.7")

    # Assert
    assert rule in access_list.get_children()
    assert rule.action == "DEFAULT"


def test_append_list_element_single_key(context):  # same as create
    # Arrange
    data_tree = context.load_data("data/example_data_3b.xml")

    # Act
    access_list = data_tree.access_list
    rule = access_list.rule.append("7.7.7.7")

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


def test_append_list_element_multiple_keys(context):
    # Arrange
    data_tree = context.load_data("data/example_data_4.xml")

    # Act
    neighbours = data_tree.neighbour
    neighbour = neighbours.append(["1.1.1.4", "VRF_4", "GigabitEthernet4"])
    neighbour.information = "Some information about this neighbour"

    # Assert
    assert neighbour in neighbours
    assert neighbour.state == "DOWN"
    assert neighbour.information == "Some information about this neighbour"


def test_quick_load_extract_yang_from_json():
    # Arrange & Act
    module = EasyLoad.try_to_extract_module_from_json("data/example_data_3.json")

    # Assert
    assert module == "example"


def test_quick_load_extract_yang_from_xml():
    # Arrange & Act
    module = EasyLoad.try_to_extract_module_from_xml("data/example_data_3.xml")

    # Assert
    assert module == "example"


def test_quick_load_extract_yang_with_wrong_filetype():
    # Arrange, Act & Assert
    assert EasyLoad.try_to_extract_module_from_json("data/example_data_3.xml") == None
    assert EasyLoad.try_to_extract_module_from_xml("data/example_data_3.json") == None


def test_quick_load_single():
    # Arrange
    data_tree = EasyLoad.load("data/example_data_4.xml")
    interface = data_tree

    # Act
    interface.name = "TenGigabitEthernet0/0/0"

    # Assert
    assert interface.name == "TenGigabitEthernet0/0/0"


def test_quick_load_multiple():
    # Arrange
    data_tree_1 = EasyLoad.load("data/example_data_2.xml")
    data_tree_2 = EasyLoad.load("data/example_data_3.json")

    # Act
    data_tree_1.mtu = 2002
    data_tree_2.mtu = 2002

    # Assert
    assert data_tree_1.mtu == data_tree_2.mtu


def test_quick_load_append():
    # Arrange
    data_tree_1 = EasyLoad.load("data/example_data_3.xml")

    # Act
    data_tree_2 = data_tree_1._context.load_data("data/example_data_3b.json")

    # Assert
    assert data_tree_1.mtu == data_tree_2.mtu


def test_quick_load_parity():
    # Arrange
    data_tree_1 = EasyLoad.load("data/example_data_3b.xml")
    data_tree_2 = EasyLoad.load("data/example_data_3b.json")

    # Act
    context = data_tree_1._context  # 2 different contexts
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    differences = context.evaluate_differences(diff_tree)

    # Assert
    assert differences == {}


def test_quick_load_single_when_given_module():
    # Arrange
    data_tree = EasyLoad.load("data/example_data_3b.xml", module="example")
    interface = data_tree

    # Act
    interface.name = "FastEthernet4"

    # Assert
    assert interface.name == "FastEthernet4"

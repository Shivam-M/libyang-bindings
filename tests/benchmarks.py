from timeit import timeit
from bindings.definitions import Context
from ipaddress import IPv4Network

CALL_COUNT = 100
BENCHMARKS = {}

def benchmark(method):
    def wrapper():
        context = create_context()
        return method(context)
    BENCHMARKS[method.__name__] = wrapper
    return wrapper

def create_context():
    context = Context()
    context.add_search_path("yang")
    context.load_module("example")
    return context


@benchmark
def benchmark_load_context(context):
    _ = context


@benchmark
def benchmark_single_creation(context):
    data_tree = context.load_data("data/example_data_4.xml")
    data_tree.mtu = 9000


@benchmark
def benchmark_single_addition(context):
    data_tree = context.load_data("data/example_data_3b.xml")
    data_tree.access_list.create("rule", "192.168.1.1")


@benchmark
def benchmark_additions(context):
    data_tree = context.load_data("data/example_data_3b.xml")
    for address in IPv4Network("192.168.1.0/24").hosts():
        data_tree.access_list.create("rule", str(address)).action = "ALLOW"


@benchmark
def benchmark_children_retrievals(context):
    data_tree = context.load_data("data/example_data_5.xml")
    for rule in data_tree.access_list.get_children():
        _ = rule.endpoint
        _ = rule.action


@benchmark
def benchmark_xpath_node_retrievals(context):
    data_tree = context.load_data("data/example_data_5.xml")
    for address in IPv4Network("192.168.1.0/24").hosts():
        rule = data_tree.get_node_at_xpath(f"/example:interface/access-list/rule[endpoint='{address}']")
        _ = rule.endpoint
        _ = rule.action


@benchmark
def benchmark_xpath_value_retrievals(context):
    data_tree = context.load_data("data/example_data_5.xml")
    for address in IPv4Network("192.168.1.0/24").hosts():
        _ = data_tree.get_value_at_xpath(f"/example:interface/access-list/rule[endpoint='{address}']/endpoint")
        _ = data_tree.get_value_at_xpath(f"/example:interface/access-list/rule[endpoint='{address}']/action")


@benchmark
def benchmark_list_keys_retrievals(context):
    data_tree = context.load_data("data/example_data_4.xml")
    data_tree.neighbour.get_list_keys()


@benchmark
def benchmark_get_differences(context):
    data_tree_1 = context.load_data("data/example_data_2.xml")
    data_tree_2 = context.load_data("data/example_data_5.xml")
    _ = context.get_differences(data_tree_1, data_tree_2)


@benchmark
def benchmark_evaluate_differences(context):
    data_tree_1 = context.load_data("data/example_data_2.xml")
    data_tree_2 = context.load_data("data/example_data_5.xml")
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    _ = context.evaluate_differences(data_tree_1, data_tree_2, diff_tree)


@benchmark
def benchmark_evaluate_differences_c(context):
    data_tree_1 = context.load_data("data/example_data_2.xml")
    data_tree_2 = context.load_data("data/example_data_5.xml")
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    _ = context.evaluate_differences(data_tree_1, data_tree_2, diff_tree, c_version=True)


@benchmark
def benchmark_retrieve_leaf(context):
    data_tree_1 = context.load_data("data/example_data_3.xml")
    data_tree_1.name = "FastEthernet24"
    _ = data_tree_1.name


if __name__ == "__main__":
    print(f"* {CALL_COUNT=}")
    print(f"{"- name -":-<42} total ----- average -")
    for name, method in BENCHMARKS.items():
        time_taken = timeit(method, number=CALL_COUNT)
        print(f"{name: <40} {time_taken:.6f}s | {time_taken / CALL_COUNT:.8f}s")
    print("-" * 64)

from timeit import timeit
from bindings.definitions import Context
from ipaddress import IPv4Network

CALL_COUNT = 100
BENCHMARKS = {}

def benchmark(method):
    BENCHMARKS[method.__name__] = method
    return method


def create_context():
    context = Context()
    context.add_search_path("yang")
    context.load_module("example")
    return context


@benchmark
def benchmark_load_context():
    create_context()


@benchmark
def benchmark_single_creation():
    data_tree = create_context().load_data("data/example_data_4.xml")
    data_tree.mtu = 9000


@benchmark
def benchmark_single_addition():
    data_tree = create_context().load_data("data/example_data_3b.xml")
    data_tree.access_list.create("rule", "192.168.1.1")


@benchmark
def benchmark_additions():
    data_tree = create_context().load_data("data/example_data_3b.xml")

    for address in IPv4Network("192.168.1.0/24").hosts():
        data_tree.access_list.create("rule", str(address)).action = "ALLOW"


@benchmark
def benchmark_children_retrievals():
    data_tree = create_context().load_data("data/example_data_5.xml")

    for rule in data_tree.access_list.get_children():
        _ = rule.endpoint._value
        _ = rule.action._value


@benchmark
def benchmark_xpath_node_retrievals():
    data_tree = create_context().load_data("data/example_data_5.xml")

    for address in IPv4Network("192.168.1.0/24").hosts():
        rule = data_tree.get_node_at_xpath(f"/example:interface/access-list/rule[endpoint='{address}']")
        _ = rule.endpoint._value
        _ = rule.action._value


@benchmark
def benchmark_xpath_value_retrievals():
    data_tree = create_context().load_data("data/example_data_5.xml")

    for address in IPv4Network("192.168.1.0/24").hosts():
        _ = data_tree.get_value_at_xpath(f"/example:interface/access-list/rule[endpoint='{address}']/endpoint")
        _ = data_tree.get_value_at_xpath(f"/example:interface/access-list/rule[endpoint='{address}']/action")


@benchmark
def benchmark_list_keys_retrievals():
    data_tree = create_context().load_data("data/example_data_4.xml")
    data_tree.neighbour.get_list_keys()


@benchmark
def benchmark_get_differences():
    context = create_context()
    data_tree_1 = context.load_data("data/example_data_2.xml")
    data_tree_2 = context.load_data("data/example_data_5.xml")
    _ = context.get_differences(data_tree_1, data_tree_2)


@benchmark
def benchmark_evaluate_differences():
    context = create_context()
    data_tree_1 = context.load_data("data/example_data_2.xml")
    data_tree_2 = context.load_data("data/example_data_5.xml")
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    _ = context.evaluate_differences(data_tree_1, data_tree_2, diff_tree)


if __name__ == "__main__":
    print(f"* {CALL_COUNT=}")
    print(f"{"- name -":-<42} total ----- average -")
    for name, method in BENCHMARKS.items():
        time_taken = timeit(method, number=CALL_COUNT)
        print(f"{name: <40} {time_taken:.6f}s | {time_taken / CALL_COUNT:.8f}s")
    print("-" * 64)

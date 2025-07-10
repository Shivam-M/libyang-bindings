import os
import inspect
from functools import wraps, partial
from timeit import timeit
from bindings.definitions import Context, EasyLoad
from ipaddress import IPv4Network

CALL_COUNT = int(os.environ.get("CALL_COUNT", 100))
benchmarks = {}


def benchmark(method=None, skip=False):
    if method is None:
        return partial(benchmark, skip=skip)

    if skip:
        print(f"skip:  {method.__name__}")
        return None

    @wraps(method)
    def wrapper():
        if len(inspect.signature(method).parameters) == 0:
            return method()
        context = create_context()
        return method(context)

    benchmarks[method.__name__] = wrapper
    return wrapper


def create_context():
    context = Context()
    context.add_search_path("yang")
    context.load_module("example")
    return context


@benchmark
def benchmark_overhead():
    pass


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


@benchmark(skip=True)
def benchmark_additions_validate_each(context):
    data_tree = context.load_data("data/example_data_3b.xml")
    for address in IPv4Network("192.168.1.0/24").hosts():
        data_tree.access_list.create("rule", str(address)).action = "ALLOW"


@benchmark
def benchmark_additions_validate_once(context):
    data_tree = context.load_data("data/example_data_3b.xml")
    context.validate_after_list_creation = False
    for address in IPv4Network("192.168.1.0/24").hosts():
        data_tree.access_list.create("rule", str(address)).action = "ALLOW"
    context.validate(data_tree._data)


def benchmark_node_xpath_retrieval(context):
    for _ in range(100):
        data_tree = context.load_data("data/example_data_3b.xml")
        access_list = data_tree.access_list
        _ = access_list._xpath


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
    _ = context.evaluate_differences(diff_tree)


@benchmark
def benchmark_evaluate_differences_skip(context):
    data_tree_1 = context.load_data("data/example_data_2.xml")
    data_tree_2 = context.load_data("data/example_data_5.xml")
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    _ = context.evaluate_differences(diff_tree, skip_containers_and_lists=True)


@benchmark
def benchmark_retrieve_leaf(context):
    data_tree_1 = context.load_data("data/example_data_3.xml")
    data_tree_1.name = "FastEthernet24"
    _ = data_tree_1.name


@benchmark
def benchmark_quick_load_single_creation():
    data_tree = EasyLoad.load("data/example_data_4.xml")
    data_tree.mtu = 9000


if __name__ == "__main__":
    print(f"* {CALL_COUNT=}")
    print(f"{"- name -":-<42} total ----- average -")
    for name, method in benchmarks.items():
        time_taken = timeit(method, number=CALL_COUNT)
        print(f"{name: <40} {time_taken:.6f}s | {time_taken / CALL_COUNT:.8f}s")
    print("-" * 64)

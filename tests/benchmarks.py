from timeit import timeit
from bindings.definitions import Context
from ipaddress import IPv4Network

CALL_COUNT = 100
BENCHMARKS = {}

def benchmark(method):
    BENCHMARKS[method.__name__] = method
    return method


def context():
    context = Context()
    context.add_search_path("yang")
    context.load_module("example")
    return context


@benchmark
def benchmark_load_context():
    context()


@benchmark
def benchmark_single_addition():
    data_tree = context().load_data("data/example_data_3b.xml")
    data_tree.access_list.create("rule", "192.168.1.1")


@benchmark
def benchmark_large_additions():
    data_tree = context().load_data("data/example_data_3b.xml")

    for address in IPv4Network("192.168.1.0/24").hosts():
        data_tree.access_list.create("rule", str(address)).action = "ALLOW"


@benchmark
def benchmark_large_retrievals():
    data_tree = context().load_data("data/example_data_5.xml")

    for rule in data_tree.access_list.get_children():
        _ = rule.endpoint
        _ = rule.action


if __name__ == "__main__":
    print(f"* {CALL_COUNT=}")
    print(f"{"- name -":-<42} total ----- average -")
    for name, method in BENCHMARKS.items():
        time_taken = timeit(method, number=CALL_COUNT)
        print(f"{name: <40} {time_taken:.6f}s | {time_taken / CALL_COUNT:.8f}s")
    print("-" * 64)

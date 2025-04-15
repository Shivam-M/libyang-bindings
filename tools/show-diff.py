#!/usr/bin/env python3

import argparse
import os
import json
from bindings.definitions import Context, Test

def validate_file(filename):
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(f"File does not exist: {filename}")
    return filename

def parse_args():
    parser = argparse.ArgumentParser(description="Compare two data files (XML or JSON) using a YANG model")
    parser.add_argument("file1", type=validate_file, help="first input file (XML or JSON)")
    parser.add_argument("file2", type=validate_file, help="second input file (XML or JSON)")
    parser.add_argument("yang_model", type=str, help="name of the YANG model to use")
    parser.add_argument("--skip-containers", action="store_true", help="exclude list and container nodes from the diff")
    parser.add_argument("--dump-dictionary", action="store_true", help="print out the dictionary of changes")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    context = Context()
    context.add_search_path("yang")
    context.load_module(args.yang_model)

    data_tree_1 = context.load_data(args.file1)
    data_tree_2 = context.load_data(args.file2)
    diff_tree = context.get_differences(data_tree_1, data_tree_2)
    differences = context.evaluate_differences(diff_tree, args.skip_containers)

    if args.dump_dictionary:
        print(json.dumps(differences, indent=2))

    Test.print_differences(differences)

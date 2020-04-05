#!/usr/bin/env python

import argparse
import timeit
import hashlib


RAND_SIZE = 10 * 2 ** 20  # 10 megs
NUM_ITERATIONS = 10000


def main(contents: bytes, n: int = NUM_ITERATIONS):
    for algo in sorted(hashlib.algorithms_available):
        print(f"Testing {algo}")
        global_ns = globals()
        global_ns["algo"] = algo
        global_ns["contents"] = contents
        t = timeit.Timer(
            "h.update(contents)",
            "import hashlib; h = hashlib.new(algo)",
            globals=global_ns,
        )
        try:
            time = t.timeit(number=n)
            print(
                f"{n} iterations took {time:.4}s with an avg of {(time / n):.4e}s per loop"
            )
        except Exception:
            t.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmarks the built-in Python hash algorithms"
    )
    parser.add_argument(
        "-n", default=NUM_ITERATIONS, help="number of iterations to run"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="name of file to hash")
    group.add_argument("-c", "--contents", help="contents to hash")
    options = parser.parse_args()

    contents: bytes = bytes()
    if options.file:
        with open(options.file, "rb") as f:
            contents = f.read()
    elif options.contents:
        contents = options.contents

    main(contents=contents)

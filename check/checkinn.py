#!/usr/bin/env python

import sys


def _usage():
    print(format("Usage: %s inn", sys.argv[0]))


def _check_n11(inn):
    n11 = ((7 * int(inn[0]) + 2 * int(inn[1]) + 4 * int(inn[2]) +
            10 * int(inn[3]) + 3 * int(inn[4]) + 5 * int(inn[5]) +
            9 * int(inn[6]) + 4 * int(inn[7]) + 6 * int(inn[8]) +
            8 * int(inn[9])) % 11) % 10
    return (n11 == int(inn[10]))


def _check_n12(inn):
    n12 = ((3 * int(inn[0]) + 7 * int(inn[1]) + 2 * int(inn[2]) +
            4 * int(inn[3]) + 10 * int(inn[4]) + 3 * int(inn[5]) +
            5 * int(inn[6]) + 9 * int(inn[7]) + 4 * int(inn[8]) +
            6 * int(inn[9]) + 8 * int(inn[10])) % 11) % 10
    return (n12 == int(inn[11]))


def check_inn(inn):
    return (_check_n11(inn) and _check_n12(inn))

if __name__ == "__main__":
    try:
        check_inn(sys.argv[1])
    except IndexError:
        _usage()

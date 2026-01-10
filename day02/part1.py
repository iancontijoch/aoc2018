from __future__ import annotations

import argparse
import os.path
from collections import Counter

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    twos, threes = 0, 0
    for line in lines:
        cnt = Counter(line)
        if 2 in cnt.values():
            twos += 1
        if 3 in cnt.values():
            threes += 1

    return twos * threes


INPUT_S = '''\
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
'''
EXPECTED = 12


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

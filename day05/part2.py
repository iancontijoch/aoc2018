from __future__ import annotations

import argparse
import os.path
from string import ascii_lowercase

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    shortest_len = 10 ** 6

    def reduce(s: str) -> str:
        lst = list(s)
        flag = True
        while flag:
            flag = False
            for (i, a), b in zip(enumerate(lst), lst[1:]):
                # check if it's opposite-case letters and remove if so
                if abs(ord(a) - ord(b)) == 32:
                    del lst[i:i+2]
                    flag = True
                    break
        return ''.join(lst)

    for line in lines:
        for c in ascii_lowercase:
            reduced_line = reduce(
                ''.join(
                    [x for x in line if x not in (c, c.upper())],
                ),
            )
            shortest_len = min(shortest_len, len(reduced_line))

    return shortest_len


INPUT_S = '''\
dabAcCaCBAcCcaDA
'''
EXPECTED = 4


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

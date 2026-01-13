from __future__ import annotations

import argparse
import os.path
from string import ascii_lowercase

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    line = s.strip()
    shortest_len = 10 ** 6

    def reduce(s: str) -> int:
        stack: list[str] = []
        for ch in s:
            if stack and abs(ord(stack[-1]) - ord(ch)) == 32:
                stack.pop()
            else:
                stack.append(ch)
        return len(stack)

    for c in ascii_lowercase:
        size = reduce(''.join([ch for ch in line if ch.lower() != c]))
        shortest_len = min(shortest_len, size)

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

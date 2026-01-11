from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    def can_cancel(c1: str, c2: str) -> bool:
        return c1 != c2 and c1.upper() == c2.upper()

    for line in lines:
        while True:
            if not any(
                can_cancel(c1, c2)
                for c1, c2 in itertools.pairwise(line)
            ):
                return len(line)
            for (i, c1), (j, c2) in itertools.pairwise(enumerate(line)):
                if can_cancel(c1, c2):
                    line = line[:i] + line[i+1:j] + line[j+1:]
                    break
    return 0


INPUT_S = '''\
dabAcCaCBAcCcaDA
'''
EXPECTED = 10


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

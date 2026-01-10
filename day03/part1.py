from __future__ import annotations

import argparse
import itertools
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    spans = []
    for line in lines:
        m = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
        if m is None:
            raise ValueError
        _, x0, y0, l, w = map(int, m.groups())
        span = {
            (x, y)
            for x in range(x0, x0 + l)
            for y in range(y0, y0 + w)
        }
        spans.append(span)

    u = set()
    for s1, s2 in itertools.combinations(spans, r=2):
        u |= s1 & s2
    return len(u)


INPUT_S = '''\
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
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

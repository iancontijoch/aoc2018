from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    seen = {0}
    total = 0

    nums = itertools.cycle(
        int(n_s)
        for line in lines
        for n_s in line.split(', ')
    )

    for n in nums:
        total += n
        if total in seen:
            return total
        seen.add(total)
    return 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('+1, -2, +3, +1', 2),
        ('+1, -1', 0),
        ('+3, +3, +4, -2, -4', 10),
        ('-6, +3, +8, +5, -6', 5),
        ('+7, +7, -2, -7, -4', 14),
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

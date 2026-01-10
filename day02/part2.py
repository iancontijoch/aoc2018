from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    lines = s.splitlines()
    for s1, s2 in itertools.combinations(lines, r=2):
        diffs = set(enumerate(s1)) - set(enumerate(s2))
        if len(diffs) == 1:
            i = list(diffs)[0][0]
            return s1[:i] + s1[i+1:]
    return 'fail'


INPUT_S = '''\
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
'''
EXPECTED = 'fgij'


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

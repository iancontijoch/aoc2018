from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def dist(x0: int, y0: int,  x1: int, y1: int) -> int:
    return abs(x0 - x1) + abs(y0 - y1)


def compute(s: str, max_dist: int) -> int:
    lines = s.splitlines()
    coords = {}
    for i, line in enumerate(lines):
        x, y = map(int, line.split(', '))
        coords[(x, y)] = i

    bx, by = support.bounds(coords)
    points = coords.keys()
    valid_pts = []

    for y in range(0, by.max):
        for x in range(0, bx.max):
            dists = {pt: dist(x, y, *pt) for pt in points}
            total_dist = sum(dists.values())
            if total_dist < max_dist:
                valid_pts.append((x, y))

    return len(valid_pts)


INPUT_S = '''\
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
'''
EXPECTED = 16
MAX_DIST = 32


@pytest.mark.parametrize(
    ('input_s', 'max_dist', 'expected'),
    (
        (INPUT_S, MAX_DIST, EXPECTED),
    ),
)
def test(input_s: str, max_dist: int, expected: int) -> None:
    assert compute(input_s, max_dist) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 10_000))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

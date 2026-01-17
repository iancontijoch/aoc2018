from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def dist(x0: int, y0: int,  x1: int, y1: int) -> int:
    return abs(x0 - x1) + abs(y0 - y1)


def compute(s: str) -> int:
    lines = s.splitlines()
    coords = {}
    for i, line in enumerate(lines):
        x, y = map(int, line.split(', '))
        coords[(x, y)] = i

    bx, by = support.bounds(coords)
    points = coords.keys()
    closest = defaultdict(int)
    areas = []

    for y in range(0, by.max):
        for x in range(0, bx.max):
            dists = {pt: dist(x, y, *pt) for pt in points}
            min_dist = min(dists.values())
            closest_nodes = [
                coords[pt]
                for pt, v in dists.items()
                if v == min_dist
            ]
            if len(closest_nodes) == 1:
                closest[(x, y)] = closest_nodes[0]

    for i, _ in enumerate(coords):
        area = [coord for coord, node in closest.items() if i == node]
        for pt in area:
            if pt[0] in (bx.min, bx.max) or pt[1] in (by.min, by.max):
                area = []
        if area:
            areas.append(len(area))

    return max(areas)


INPUT_S = '''\
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
'''
EXPECTED = 17


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

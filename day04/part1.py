from __future__ import annotations

import argparse
import datetime
import os.path
import re
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    todo, events = [], []
    guard_id = None
    for line in lines:
        timestamp_s, rest = line.split('] ')
        m = re.search(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', timestamp_s)
        if m is None:
            raise ValueError
        year, month, day, hour, minute = map(int, m.groups())
        ts = datetime.datetime(year, month, day, hour, minute)
        events.append((ts, rest))

    for ts, rest in sorted(events, key=lambda x: x[0]):
        if 'Guard' in rest:
            guard_id = int(rest.split()[1][1:])
            action = 'begin'
        elif 'asleep' in rest:
            action = 'sleep'
        elif 'wakes' in rest:
            action = 'wakes'
        else:
            raise ValueError
        todo.append((ts, guard_id, action))

    sleep_durations: defaultdict[int, int] = defaultdict(int)
    sleep_ranges: defaultdict[
        int,
        list[tuple[tuple[int, int], range]],
    ] = defaultdict(list)

    if guard_id is None:
        raise ValueError

    for i, (ts, gid, action) in enumerate(todo):
        if action == 'sleep':
            if gid is None:
                raise ValueError
            wake_ts = todo[i+1][0]
            sleep_durations[gid] += wake_ts.minute - ts.minute
            sleep_ranges[gid].append(
                ((ts.year, ts.day), range(ts.minute, wake_ts.minute)),
            )

    sleepiest_guard = max(sleep_durations.items(), key=lambda x: x[1])[0]
    sleeps = sleep_ranges[sleepiest_guard]

    mins_days = defaultdict(set)
    for rng_day, rng in sleeps:
        for rng_minute in rng:
            mins_days[rng_minute].add(rng_day)

    return (
        sleepiest_guard * sorted(
            mins_days.items(),
            key=lambda x: -len(x[1]),
        )[0][0]
    )


INPUT_S = '''\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
'''
EXPECTED = 240


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

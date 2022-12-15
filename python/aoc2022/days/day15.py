import parse
from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, LpBinary, value, PULP_CBC_CMD
from tqdm import tqdm


def day15():
    test = False
    if test:
        target = 10
        with open('../input/test15.txt', 'r') as f:
            data = f.read().splitlines()
    else:
        target = 2000000
        with open('../input/input15.txt', 'r') as f:
            data = f.read().splitlines()
    bounds = {'left': 0, 'right': 2 * target, 'up': 0, 'down': 2 * target}
    beacons = []
    sensors = []
    dists = {}
    limits = {'left': 1e10, 'right': -1e10, 'up': 1e10, 'down': -1e10}
    format_string = 'Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}'
    for row in data:
        sx, sy, bx, by = parse.parse(format_string, row)
        sensors.append((sx, sy))
        beacons.append((bx, by))
        dist = manhattan((sx, sy), (bx, by))
        limits['left'] = min(limits['left'], sx - dist)
        limits['right'] = max(limits['right'], sx + dist)
        limits['up'] = min(limits['up'], sy - dist)
        limits['down'] = max(limits['down'], sy + dist)
        dists[(sx, sy)] = dist

    m = measure(target, sensors, beacons, dists, limits)

    print('Part 1:', m)

    f = tune(sensors, dists, bounds)

    print('Part 2:', f)


def manhattan(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def measure(target, sensors, beacons, dists, limits):
    intervals = []
    count = 0
    for s in sensors:
        d = abs(s[1] - target)
        width = 2 * dists[s] + 1 - 2 * d
        if width > 0:
            intervals.append([s[0] - (width // 2), s[0] + (width // 2)])
    for x in tqdm(range(limits['left'], limits['right'] + 1)):
        if any(inter[0] <= x <= inter[1] for inter in intervals) and (x, target) not in beacons:
            count += 1
    return count


def tune(sensors, dists, limits):
    prob = LpProblem("Tuning", LpMinimize)
    x = LpVariable("x", 0, limits['right'], LpInteger)
    y = LpVariable("y", 0, limits['down'], LpInteger)
    prob += 4000000 * x + y
    i = 0
    for s in sensors:
        e1 = LpVariable(f'E1s{i}', 0, 1, LpBinary)
        e2 = LpVariable(f'E2s{i}', 0, 1, LpBinary)
        e3 = LpVariable(f'E3s{i}', 0, 1, LpBinary)
        e4 = LpVariable(f'E4s{i}', 0, 1, LpBinary)
        prob += (x - s[0]) + (y - s[1]) + 40000000 * e1 >= dists[s] + 1
        prob += (s[0] - x) + (y - s[1]) + 40000000 * e2 >= dists[s] + 1
        prob += (x - s[0]) + (s[1] - y) + 40000000 * e3 >= dists[s] + 1
        prob += (s[0] - x) + (s[1] - y) + 40000000 * e4 >= dists[s] + 1
        prob += e1 + e2 + e3 + e4 == 3
        i += 1
    prob.solve(PULP_CBC_CMD(msg=False))
    return int(value(prob.objective))

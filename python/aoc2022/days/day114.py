import time

from aoc2022.days.day9 import sign
import pyxel

colors = {'#': 10, 'O': 2, '.': 0}
cave = dict()
limits = {'left': 10000, 'right': 0, 'down': 0}

def day114():
    with open('../input/input14.txt', 'r') as f:
        data = f.read().splitlines()

    for line in data:
        wall = []
        for pair in line.split(' -> '):
            x, y = int(pair.split(',')[0]), int(pair.split(',')[1])
            wall.append((x, y))
        for i in range(len(wall) - 1):
            start = wall[i]
            end = wall[i + 1]
            if start[0] == end[0]:
                x = start[0]
                for y in range(start[1], end[1] + sign(end[1] - start[1]), sign(end[1] - start[1])):
                    cave[(x, y)] = '#'
            else:
                y = start[1]
                for x in range(start[0], end[0] + sign(end[0] - start[0]), sign(end[0] - start[0])):
                    cave[(x, y)] = '#'

    for k in cave.keys():
        x, y = k
        limits['left'] = min(limits['left'], x)
        limits['right'] = max(limits['right'], x)
        limits['down'] = max(limits['down'], y)

    pyxel.init(500 + limits['down'] + 3 - (500 - limits['down'] - 2), limits['down'] + 3, fps=120, capture_sec=400)
    for y in range(0, limits['down'] + 2):
        for x in range(500 - limits['down'] - 2, 500 + limits['down'] + 3):
            if (x, y) in cave.keys() and cave[(x, y)] == '#':
                pyxel.pset(x - (500 - limits['down'] - 2), y, colors['#'])
    for x in range(500 - limits['down'] - 2, 500 + limits['down'] + 3):
        pyxel.pset(x - (500 - limits['down'] - 2), y + 1, colors['#'])
    pyxel.run(refresh, draw)


def refresh():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


def draw():
    sand = (500, 0)
    can_fall = True
    while can_fall:
        if (500, 0) in cave.keys():
            break
        if (sand[0], sand[1] + 1) not in cave and sand[1] + 1 < limits['down'] + 2:
            sand = (sand[0], sand[1] + 1)
        elif (sand[0] - 1, sand[1] + 1) not in cave and sand[1] + 1 < limits['down'] + 2:
            sand = (sand[0] - 1, sand[1] + 1)
        elif (sand[0] + 1, sand[1] + 1) not in cave and sand[1] + 1 < limits['down'] + 2:
            sand = (sand[0] + 1, sand[1] + 1)
        else:
            cave[sand] = 'O'
            can_fall = False
        pyxel.pset(sand[0] - (500 - limits['down'] - 2), sand[1], colors['O'])

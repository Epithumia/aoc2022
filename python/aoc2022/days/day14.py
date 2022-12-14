from aoc2022.days.day9 import sign


def day14():
    with open('../input/input14.txt', 'r') as f:
        data = f.read().splitlines()

    cave = dict()
    limits = {'left': 10000, 'right': 0, 'down': 0}

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

    abyss = False
    while not abyss:
        sand = (500, 0)
        can_fall = True
        while can_fall:
            if sand[0] < limits['left'] or sand[0] > limits['right'] or sand[1] > limits['down']:
                abyss = True
                break
            if (sand[0], sand[1] + 1) not in cave:
                sand = (sand[0], sand[1] + 1)
            elif (sand[0] - 1, sand[1] + 1) not in cave:
                sand = (sand[0] - 1, sand[1] + 1)
            elif (sand[0] + 1, sand[1] + 1) not in cave:
                sand = (sand[0] + 1, sand[1] + 1)
            else:
                cave[sand] = 'O'
                can_fall = False

    score1 = 0
    for v in cave.values():
        if v == 'O':
            score1 += 1

    print('Part 1:', score1)

    full = False
    while not full:
        sand = (500, 0)
        can_fall = True
        while can_fall:
            if (500, 0) in cave.keys():
                full = True
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

    score2 = 0
    for v in cave.values():
        if v == 'O':
            score2 += 1

    print('Part 2:', score2)

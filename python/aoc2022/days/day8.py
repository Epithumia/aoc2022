def day8():
    with open('../input/input8.txt', 'r') as f:
        data = f.read()

    forest_map = []
    visible_map = []

    for index_r, row in enumerate(data.splitlines()):
        maprow = []
        visiblerow = []
        for index_c, col in enumerate(row):
            maprow.append(int(col))
            if index_c == 0 or index_r == 0:
                visiblerow.append(1)
            else:
                visiblerow.append(0)
        forest_map.append(maprow)
        visible_map.append(visiblerow)

    width = len(forest_map[0])
    height = len(forest_map)

    for i in range(1, height - 1):
        curmaxl = 0
        curmaxr = 0
        for j in range(1, width - 1):
            if forest_map[i][j - 1] > curmaxl:
                curmaxl = forest_map[i][j - 1]
            if curmaxl < forest_map[i][j]:
                visible_map[i][j] = 1
            if forest_map[(height - 1) - i][(width - 1) - (j - 1)] > curmaxr:
                curmaxr = forest_map[(height - 1) - i][(width - 1) - (j - 1)]
            if curmaxr < forest_map[(height - 1) - i][(width - 1) - j]:
                visible_map[(height - 1) - i][(width - 1) - j] = 1

    for j in range(1, width - 1):
        curmaxl = 0
        curmaxr = 0
        for i in range(1, height - 1):
            if forest_map[i - 1][j] > curmaxl:
                curmaxl = forest_map[i - 1][j]
            if curmaxl < forest_map[i][j]:
                visible_map[i][j] = 1
            if forest_map[(height - 1) - (i - 1)][(width - 1) - j] > curmaxr:
                curmaxr = forest_map[(height - 1) - (i - 1)][(width - 1) - j]
            if curmaxr < forest_map[(height - 1) - i][(width - 1) - j]:
                visible_map[(height - 1) - i][(width - 1) - j] = 1

    best = 0
    for i in range(height):
        for j in range(width):
            score = view(i, j, forest_map)
            if score > best:
                best = score

    print('Part 1: ', sum([sum([col for col in row]) for row in visible_map]))
    print('Part 2: ', best)


def view(i, j, forest_map):
    scorerl = 0
    scorerr = 0
    scorecl = 0
    scorecr = 0
    for r in range(1, i + 1):
        if forest_map[i - r][j] < forest_map[i][j]:
            scorerl += 1
        else:
            scorerl += 1
            break
    for r in range(1, len(forest_map) - i):
        if forest_map[i + r][j] < forest_map[i][j]:
            scorerr += 1
        else:
            scorerr += 1
            break
    for c in range(1, j + 1):
        if forest_map[i][j - c] < forest_map[i][j]:
            scorecl += 1
        else:
            scorecl += 1
            break
    for c in range(1, len(forest_map) - j):
        if forest_map[i][j + c] < forest_map[i][j]:
            scorecr += 1
        else:
            scorecr += 1
            break

    return scorerl * scorerr * scorecr * scorecl

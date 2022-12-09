def day9():
    with open('../input/input9.txt', 'r') as f:
        data = f.read().splitlines()

    # print(visited)
    print('Part 1: ', rope(data, 2))

    print('Part 2: ', rope(data, 10))


def rope(moves, length):
    visited = {}
    pos = [[0, 0] for _ in range(length)]
    visited[str(pos[length - 1])] = 1

    for move in moves:
        direction, dist = move.split(' ')
        dist = int(dist)
        for _ in range(dist):
            if direction == 'U':
                pos[0][1] += 1
            if direction == 'D':
                pos[0][1] += -1
            if direction == 'L':
                pos[0][0] += -1
            if direction == 'R':
                pos[0][0] += 1
            for i in range(1, length):
                pos[i] = follow(pos[i - 1], pos[i])
            visited[str(pos[length - 1])] = 1
    return len(visited)


def follow(pos_h, pos_t):
    if pos_h == pos_t:
        return pos_t
    if pos_h[0] == pos_t[0]:  # Same X
        if pos_h[1] - pos_t[1] > 1:
            pos_t[1] += (pos_h[1] - pos_t[1]) - 1
        elif pos_h[1] - pos_t[1] < -1:
            pos_t[1] += (pos_h[1] - pos_t[1]) + 1
        return pos_t
    if pos_h[1] == pos_t[1]:  # Same Y
        if pos_h[0] - pos_t[0] > 1:
            pos_t[0] += pos_h[0] - pos_t[0] - 1
        elif pos_h[0] - pos_t[0] < -1:
            pos_t[0] += pos_h[0] - pos_t[0] + 1
        return pos_t
    # Diagonal
    if abs(pos_h[1] - pos_t[1]) > abs(pos_h[0] - pos_t[0]) and abs(pos_h[1] - pos_t[1]) > 1:  # move Y first
        pos_t[0] += pos_h[0] - pos_t[0]
        return follow(pos_h, pos_t)
    elif abs(pos_h[1] - pos_t[1]) < abs(pos_h[0] - pos_t[0]) and abs(pos_h[0] - pos_t[0]) > 1:  # move X first
        pos_t[1] += pos_h[1] - pos_t[1]
        return follow(pos_h, pos_t)
    elif abs(pos_h[1] - pos_t[1]) == abs(pos_h[0] - pos_t[0]) > 1:  # move both
        if pos_h[0] > pos_t[0]:
            pos_t[0] += pos_h[0] - pos_t[0] - 1
        else:
            pos_t[0] += pos_h[0] - pos_t[0] + 1
        if pos_h[1] > pos_t[1]:
            pos_t[1] += pos_h[1] - pos_t[1] - 1
        else:
            pos_t[1] += pos_h[1] - pos_t[1] + 1
        return follow(pos_h, pos_t)
    return pos_t

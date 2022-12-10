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
    dx = abs(pos_h[0] - pos_t[0])
    dy = abs(pos_h[1] - pos_t[1])
    vx = sign(pos_h[0] - pos_t[0]) * int(((dx >= 1) and (dy > 1)) or (dx > 1))
    vy = sign(pos_h[1] - pos_t[1]) * int(((dx > 1) and (dy >= 1)) or (dy > 1))
    pos_t[0] += vx
    pos_t[1] += vy
    return pos_t


def sign(x):
    return (x > 0) - (x < 0)

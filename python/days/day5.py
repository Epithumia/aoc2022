def day5():
    with open('../input/input5.txt', 'r') as f:
        data = f.read().split('\n')[:-1]

    c = [list(reversed([d[4 * i + 1] if d[4 * i + 1] != ' ' else None for d in data[:8]])) for i in range(9)]
    crates9k = [[x for x in row if x is not None] for row in c]
    crates9k1 = [[x for x in row if x is not None] for row in c]
    moves = [(int(row.split(' ')[1]), int(row.split(' ')[3]) - 1, int(row.split(' ')[5]) - 1) for row in data[10:]]

    for m in range(len(moves)):
        qty, src, dst = moves[m]
        crates9k[dst].extend([crates9k[src].pop() for _ in range(qty)])
        crates9k1[dst].extend(list(reversed([crates9k1[src].pop() for _ in range(qty)])))

    print('Part 1: ', ''.join([c[-1] for c in crates9k]))
    print('Part 2: ', ''.join([c[-1] for c in crates9k1]))

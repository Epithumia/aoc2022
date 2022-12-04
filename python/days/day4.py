def day4():
    with open('../input/input4.txt', 'r') as f:
        data = f.read().split('\n')[:-1]
        pairs = [(n.split(',')[0], n.split(',')[1]) for n in data]

    nb_idle_elves = 0
    nb_over_elves = 0

    for pair in pairs:
        f, p = overlap(pair[0], pair[1])
        nb_idle_elves += f
        nb_over_elves += p

    print('Part 1: ', nb_idle_elves)
    print('Part 2: ', nb_over_elves)


def overlap(pair1, pair2):
    full = partial = 0
    n = pair1.split('-')
    n1, n2 = int(n[0]), int(n[1])
    m = pair2.split('-')
    m1, m2 = int(m[0]), int(m[1])
    if ((n1 <= m1 <= n2) and (n1 <= m2 <= n2)) or ((m1 <= n1 <= m2) and (m1 <= n2 <= m2)):
        full = 1
    if ((n1 <= m1 <= n2) or (n1 <= m2 <= n2)) or ((m1 <= n1 <= m2) or (m1 <= n2 <= m2)):
        partial = 1
    return full, partial

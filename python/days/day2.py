def day2():
    with open('../input/input2.txt', 'r') as f:
        data = f.read().split('\n')
        round1 = 0
        round2 = 0
        for row in data:
            if len(row) > 0:
                m = row.split(' ')
                round1 += score(m[0], m[1])
                round2 += strategize(m[0], m[1])
    print('Part 1: ', round1)
    print('Part 2: ', round2)


def score(p1: str, p2: str) -> int:
    if p1 == 'A':
        if p2 == 'X':
            return 1 + 3
        if p2 == 'Y':
            return 2 + 6
        if p2 == 'Z':
            return 3 + 0
    if p1 == 'B':
        if p2 == 'X':
            return 1 + 0
        if p2 == 'Y':
            return 2 + 3
        if p2 == 'Z':
            return 3 + 6
    if p1 == 'C':
        if p2 == 'X':
            return 1 + 6
        if p2 == 'Y':
            return 2 + 0
        if p2 == 'Z':
            return 3 + 3
    return 0


def strategize(p1: str, p2: str) -> int:
    if p1 == 'A':
        if p2 == 'X':
            return 3 + 0
        if p2 == 'Y':
            return 1 + 3
        if p2 == 'Z':
            return 2 + 6
    if p1 == 'B':
        if p2 == 'X':
            return 1 + 0
        if p2 == 'Y':
            return 2 + 3
        if p2 == 'Z':
            return 3 + 6
    if p1 == 'C':
        if p2 == 'X':
            return 2 + 0
        if p2 == 'Y':
            return 3 + 3
        if p2 == 'Z':
            return 1 + 6
    return 0

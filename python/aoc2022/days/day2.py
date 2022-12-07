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
    results = {'A': {'X': 1 + 3, 'Y': 2 + 6, 'Z': 3 + 0},
               'B': {'X': 1 + 0, 'Y': 2 + 3, 'Z': 3 + 6},
               'C': {'X': 1 + 6, 'Y': 2 + 0, 'Z': 3 + 3}
               }
    if p1 in results and p2 in results[p1]:
        return results[p1][p2]
    return 0


def strategize(p1: str, p2: str) -> int:
    results = {'A': {'X': 3 + 0, 'Y': 1 + 3, 'Z': 2 + 6},
               'B': {'X': 1 + 0, 'Y': 2 + 3, 'Z': 3 + 6},
               'C': {'X': 2 + 0, 'Y': 3 + 3, 'Z': 1 + 6}
               }
    if p1 in results and p2 in results[p1]:
        return results[p1][p2]
    return 0

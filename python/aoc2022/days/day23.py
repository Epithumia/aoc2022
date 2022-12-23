from collections import defaultdict


def day23():
    with open('../input/input23.txt', 'r') as f:
        data = f.read().splitlines()

    elves = dict()
    move_list = ['N', 'S', 'W', 'E']

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '#':
                elves[(i, j)] = Elf(i, j)

    stopped = False
    for _ in range(10):
        elves, move_list, stopped = do_round(elves, move_list)

    n, s, w, e = get_bounds(elves)

    score = 0
    for x in range(n, s + 1):
        for y in range(w, e + 1):
            if (x, y) not in elves.keys():
                score += 1

    print('Part 1:', score)

    r = 10
    while not stopped:
        elves, move_list, stopped = do_round(elves, move_list)
        r += 1

    print('Part 2:', r)


def get_bounds(elves):
    n = 1e7
    s = -n
    w = 1e7
    e = -w
    for elf in elves.keys():
        n = min(n, elves[elf].x)
        s = max(s, elves[elf].x)
        w = min(w, elves[elf].y)
        e = max(e, elves[elf].y)

    return n, s, w, e


def do_round(elves, move_list):
    targets = defaultdict(lambda: 0)
    for e in elves.keys():
        elves[e].plan_move(elves, move_list)
        targets[elves[e].next_pos] += 1

    new_elves = dict()
    stopped = True
    for e in elves.keys():
        if targets[elves[e].next_pos] <= 1:
            elves[e].do_move()
            if elves[e].has_moved:
                stopped = False
        else:
            elves[e].cancel_move()
        new_elves[(elves[e].x, elves[e].y)] = elves[e]

    move = move_list[0]
    move_list = move_list[1:]
    move_list.append(move)

    return new_elves, move_list, stopped


class Elf(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next_pos = (x, y)
        self.has_moved = False

    def plan_move(self, elves, move_list):
        self.has_moved = False
        moves = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1), 'NW': (-1, -1), 'NE': (-1, 1), 'SW': (1, -1),
                 'SE': (1, 1)}
        neighbors = dict()
        for m in moves.keys():
            if (self.x + moves[m][0], self.y + moves[m][1]) in elves.keys():
                neighbors[m] = elves[(self.x + moves[m][0], self.y + moves[m][1])]
        if len(neighbors) == 0 or len(neighbors) == 8:
            return False
        do_move = True
        for move in move_list:
            if do_move and move == 'N':
                if 'N' not in neighbors.keys() and 'NE' not in neighbors.keys() and 'NW' not in neighbors.keys():
                    self.next_pos = self.next_pos[0] + moves['N'][0], self.next_pos[1] + moves['N'][1]
                    do_move = False
            if do_move and move == 'S':
                if 'S' not in neighbors.keys() and 'SE' not in neighbors.keys() and 'SW' not in neighbors.keys():
                    self.next_pos = self.next_pos[0] + moves['S'][0], self.next_pos[1] + moves['S'][1]
                    do_move = False
            if do_move and move == 'E':
                if 'E' not in neighbors.keys() and 'NE' not in neighbors.keys() and 'SE' not in neighbors.keys():
                    self.next_pos = self.next_pos[0] + moves['E'][0], self.next_pos[1] + moves['E'][1]
                    do_move = False
            if do_move and move == 'W':
                if 'W' not in neighbors.keys() and 'SW' not in neighbors.keys() and 'NW' not in neighbors.keys():
                    self.next_pos = self.next_pos[0] + moves['W'][0], self.next_pos[1] + moves['W'][1]
                    do_move = False
        return not do_move

    def do_move(self):
        if self.x != self.next_pos[0] or self.y != self.next_pos[1]:
            self.has_moved = True
        self.x = self.next_pos[0]
        self.y = self.next_pos[1]

    def cancel_move(self):
        self.next_pos = (self.x, self.y)

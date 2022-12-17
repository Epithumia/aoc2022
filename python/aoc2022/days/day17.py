bar = [[1, 1, 1, 1]]
plus = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
jay = [[1, 1, 1], [0, 0, 1], [0, 0, 1]]
ell = [[1], [1], [1], [1]]
squ = [[1, 1], [1, 1]]

block_order = [bar, plus, jay, ell, squ]


def day17():
    with open('../input/input17.txt', 'r') as f:
        moves = f.read().splitlines()[0]

    period = dodge(moves, 20220, detect=True)  # Find how long the repeat period is

    print('Part 1:', dodge(moves, 2022, period))
    print('Part 2:', dodge(moves, 1_000_000_000_000, period))


def dodge(moves, count, period=0, detect=False):
    if period > 0:
        lim = count % period
        s_lim = dodge(moves, lim, 0)
        nb = count // period
        s_mod = dodge(moves, 2 * period, 0) - dodge(moves, period, 0)
        return s_lim + s_mod * nb
    cave = [[2, 2, 2, 2, 2, 2, 2]]
    block_index = 0
    move_index = 0
    if detect:
        seen = dict()
    for co in range(count):
        if detect:
            if (block_index, move_index, str(cave[-1])) not in seen:
                seen[(block_index, move_index, str(cave[-1]))] = co
            else:
                return co - seen[(block_index, move_index, str(cave[-1]))]
        r = Rock(block_order[block_index], len(cave) + 3)
        block_index = (block_index + 1) % len(block_order)
        for _ in range(r.height + 3):
            cave.append([0, 0, 0, 0, 0, 0, 0])

        while r.can_fall:
            # Move left/right
            m = moves[move_index]
            move_index = (move_index + 1) % len(moves)
            r.slide(m)
            if check_valid_future(r, cave):
                r.move()
            else:
                r.cancel_move()

            # Fall down
            r.can_fall = True
            r.fall()
            if check_valid_future(r, cave):
                r.move()
            else:
                r.cancel_move()
                r.can_fall = False

        for px, py in r.positions:
            cave[py][px] = 2

        while True:
            if any([x == 2 for x in cave[-1]]):
                break
            cave = cave[:-1]

    return len(cave) - 1  # Don't count the ground


def check_valid_future(r, cave):
    if any([(px > 6 or px < 0 or py == 0) for px, py in r.future]):
        return False
    if any([cave[py][px] == 2 for px, py in r.future]):
        return False
    return True


class Rock(object):
    def __init__(self, shape, height):
        self.shape = shape
        x_init = 2
        positions = dict()
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x] == 1:
                    positions[(x_init + x, y + height)] = 1
        self.positions = positions
        self.future = positions
        self.height = len(shape)
        self.can_fall = True

    def fall(self):
        new_pos = dict()
        for px, py in self.positions.keys():
            new_pos[(px, py - 1)] = 1
        self.future = new_pos

    def slide(self, direction):
        new_pos = dict()
        for px, py in self.positions.keys():
            if direction == '<':
                new_pos[(px - 1, py)] = 1
            else:
                new_pos[(px + 1, py)] = 1
        self.future = new_pos

    def move(self):
        self.positions = self.future

    def cancel_move(self):
        self.future = self.positions

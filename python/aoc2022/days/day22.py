import re

NETS = {
    'A': [[0, 0, 1, 0], [1, 1, 1, 1], [0, 0, 1, 0]],
    'B': [[0, 1, 0, 0], [1, 1, 1, 1], [1, 0, 0, 0]],
    'C': [[0, 0, 1, 0], [1, 1, 1, 1], [0, 1, 0, 0]],
    'D': [[0, 0, 0, 1], [1, 1, 1, 1], [0, 1, 0, 0]],
    'E': [[1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1]],
    'F': [[1, 1, 0, 0], [0, 1, 1, 1], [0, 0, 1, 0]],
    'G': [[1, 1, 0, 0], [0, 1, 1, 1], [0, 0, 0, 1]],
    'H': [[1, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 1]],
    'I': [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 1, 1]],
    'J': [[0, 0, 0, 1], [1, 1, 1, 1], [0, 0, 0, 1]],
    'K': [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]
}

BLOCK_LINKS = {
    'G': {
        (1, 'E'): (3, 3),
        (1, 'W'): (5, 3),
        (1, 'S'): (6, 0),
        (1, 'N'): (2, 0),
        (2, 'E'): (3, 0),
        (2, 'W'): (5, 2),
        (2, 'S'): (1, 0),
        (2, 'N'): (4, 1),
        (3, 'E'): (6, 2),
        (3, 'W'): (2, 0),
        (3, 'S'): (1, 1),
        (3, 'N'): (4, 0),
        (4, 'E'): (6, 3),
        (4, 'W'): (2, 3),
        (4, 'S'): (3, 0),
        (4, 'N'): (5, 0),
        (5, 'E'): (6, 0),
        (5, 'W'): (2, 2),
        (5, 'S'): (4, 0),
        (5, 'N'): (1, 1),
        (6, 'E'): (3, 2),
        (6, 'W'): (5, 0),
        (6, 'S'): (4, 1),
        (6, 'N'): (1, 0)
    },
    'I': {
        (1, 'S'): (4, 0),
        (4, 'N'): (1, 0),
        (1, 'N'): (2, 2),
        (2, 'N'): (1, 2),
        (1, 'W'): (3, 3),
        (3, 'N'): (1, 1),
        (1, 'E'): (6, 2),
        (6, 'E'): (1, 2),
        (2, 'S'): (5, 2),
        (5, 'S'): (2, 2),
        (2, 'W'): (6, 1),
        (6, 'S'): (2, 3),
        (2, 'E'): (3, 0),
        (3, 'W'): (2, 0),
        (3, 'S'): (5, 3),
        (5, 'W'): (3, 1),
        (3, 'E'): (4, 0),
        (4, 'W'): (3, 0),
        (4, 'S'): (5, 0),
        (5, 'N'): (4, 0),
        (4, 'E'): (6, 1),
        (6, 'N'): (4, 3),
        (5, 'E'): (6, 0),
        (6, 'W'): (5, 0)
    }
}


def day22():
    with open('../input/input22.txt', 'r') as f:
        data = f.read().splitlines()

    size = 50  # Test: 4, Real: 50
    board_map = data[:-2]
    board = []
    for row in range(len(board_map)):
        board_row = []
        for col in range(len(board_map[row])):
            tile = Tile(row, col, board_map[row][col])
            board_row.append(tile)
        board.append(board_row)

    for row in range(len(board)):
        for col in range(len(board[row])):
            board[row][col].set_neighbors(board)

    moves = separate_number_chars(data[-1])

    r, c = find_start(board)

    facing = 0

    for m in moves:
        r, c, facing = do_move(m, r, c, facing, board)

    print('Part 1:', 1000 * (r + 1) + 4 * (c + 1) + facing)

    board.clear()
    for row in range(len(board_map)):
        board_row = []
        for col in range(len(board_map[row])):
            tile = Tile(row, col, board_map[row][col])
            board_row.append(tile)
        board.append(board_row)

    mapping_key = identify_net(board, size)
    mapped_net = mapping(mapping_key)

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col].tile_type != ' ':
                board[row][col].mapping_block = mapped_net[row // size][col // size]

    boards = split_board(board, size)

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col].tile_type != ' ':
                board[row][col].set_cube_neighbors(boards, BLOCK_LINKS[mapping_key[0]])

    r, c = find_start(board)

    facing = 0

    for m in moves:
        r, c, facing = do_move(m, r, c, facing, board)

    print('Part 2:', 1000 * (r + 1) + 4 * (c + 1) + facing)


def split_board(board, size):
    boards = [None, None, None, None, None, None]
    for row in range(6):
        for col in range(6):
            try:
                sub_board = extract(board, row, col, size)
                if sub_board[0][0].mapping_block > 0:
                    boards[sub_board[0][0].mapping_block - 1] = sub_board
            except IndexError:
                pass
    return boards


def extract(board, row, col, size):
    sub_board = []
    for r in range(size):
        sub_row = []
        for c in range(size):
            sub_row.append(board[row * size + r][col * size + c])
        sub_board.append(sub_row)
    return sub_board


def mapping(code):
    net_code = code[0]
    net = NETS[net_code]
    rot = int(code[1])
    mapped_net = []
    i = 1
    for row in net:
        mapped_row = []
        for col in row:
            if col == 1:
                mapped_row.append(i)
                i += 1
            else:
                mapped_row.append(0)
        mapped_net.append(mapped_row)
    for _ in range(rot):
        mapped_net = rotate(mapped_net)
    return mapped_net


def do_move(m, r, c, f, board):
    if m == 'L':
        f = (f - 1) % 4
        return r, c, f
    if m == 'R':
        f = (f + 1) % 4
        return r, c, f
    m = int(m)
    while m > 0:
        m -= 1
        if f == 0:
            if board[r][c].e.tile_type == '#':
                return r, c, f
            fx = (f + board[r][c].ef) % 4
            cx = board[r][c].e.col
            rx = board[r][c].e.row
        elif f == 2:
            if board[r][c].w.tile_type == '#':
                return r, c, f
            fx = (f + board[r][c].wf) % 4
            cx = board[r][c].w.col
            rx = board[r][c].w.row
        elif f == 1:
            if board[r][c].s.tile_type == '#':
                return r, c, f
            fx = (f + board[r][c].sf) % 4
            rx = board[r][c].s.row
            cx = board[r][c].s.col
        else:
            if board[r][c].n.tile_type == '#':
                return r, c, f
            fx = (f + board[r][c].nf) % 4
            rx = board[r][c].n.row
            cx = board[r][c].n.col
        f = fx
        r = rx
        c = cx
    return r, c, f


def find_start(board):
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c].tile_type == '.':
                return r, c


def separate_number_chars(s):
    res = re.split(r'([-+]?\d+\.\d+)|([-+]?\d+)', s.strip())
    res_f = [r.strip() for r in res if r is not None and r.strip() != '']
    return res_f


def identify_net(board, size):
    net = []
    for r in range(6):
        net_r = []
        for c in range(6):
            try:
                if board[r * size][c * size].tile_type == ' ':
                    net_r.append(0)
                else:
                    net_r.append(1)
            except IndexError:
                net_r.append(0)
        net.append(net_r)

    n_l = 6
    n_r = 0
    n_u = 6
    n_d = 0
    for r in range(6):
        for c in range(6):
            if net[r][c] == 1:
                n_r = max(n_r, c)
                n_l = min(n_l, c)
                n_u = min(n_u, r)
                n_d = max(n_d, r)

    short_net = []
    for row in net[n_u:n_d + 1]:
        short_net.append(row[n_l:n_r + 1])

    net = {i + '0' for i in NETS if NETS[i] == short_net}
    if len(net) == 0:
        net = {i + '3' for i in NETS if NETS[i] == rotate(short_net)}
    else:
        return net.pop()
    if len(net) == 0:
        net = {i + '2' for i in NETS if NETS[i] == rotate(rotate(short_net))}
    else:
        return net.pop()
    if len(net) == 0:
        net = {i + '1' for i in NETS if NETS[i] == rotate(rotate(rotate(short_net)))}
    else:
        return net.pop()
    if len(net) == 0:
        return None
    return net.pop()


def rotate(mat):
    temp = zip(*mat[::-1])
    return [list(elem) for elem in temp]


class Tile(object):
    def __init__(self, r, c, tile_type):
        self.n = None
        self.s = None
        self.w = None
        self.e = None
        self.nf = 0
        self.sf = 0
        self.wf = 0
        self.ef = 0
        self.row = r
        self.col = c
        self.tile_type = tile_type
        self.mapping_block = 0

    def set_neighbors(self, board):
        if self.tile_type == ' ':
            return
        r = self.row
        c = self.col
        while self.n is None:
            r = r - 1
            if r < 0:
                r = len(board) - 1
            try:
                if board[r][c].tile_type != ' ':
                    self.n = board[r][c]
                    board[r][c].s = self
            except IndexError:
                pass
        r = self.row
        c = self.col
        while self.s is None:
            r = r + 1
            if r >= len(board):
                r = 0
            try:
                if board[r][c].tile_type != ' ':
                    self.s = board[r][c]
                    board[r][c].n = self
            except IndexError:
                pass
        r = self.row
        c = self.col
        while self.w is None:
            c = c - 1
            if c < 0:
                c = len(board[r]) - 1
            try:
                if board[r][c].tile_type != ' ':
                    self.w = board[r][c]
                    board[r][c].e = self
            except IndexError:
                pass
        r = self.row
        c = self.col
        while self.e is None:
            c = c + 1
            if c >= len(board[r]):
                c = 0
            try:
                if board[r][c].tile_type != ' ':
                    self.e = board[r][c]
                    board[r][c].w = self
            except IndexError:
                pass

    def set_cube_neighbors(self, boards, board_links):
        self_board = boards[self.mapping_block - 1]
        self_r = self_c = -1
        for r in range(len(self_board)):
            for c in range(len(self_board)):
                if self_board[r][c].row == self.row and self_board[r][c].col == self.col:
                    self_r = r
                    self_c = c
                    break
        # Find north neighbor
        if self.n is None:
            if self_r - 1 >= 0:
                self.n = self_board[self_r - 1][self_c]
                self_board[self_r - 1][self_c].s = self
            else:
                target_block, rotation = board_links[(self.mapping_block, 'N')]
                target_board = boards[target_block - 1]
                if 4 - rotation == 1:
                    target_board = rotate(target_board)
                elif 4 - rotation == 2:
                    target_board = rotate(rotate(target_board))
                elif 4 - rotation == 3:
                    target_board = rotate(rotate(rotate(target_board)))
                self.n = target_board[len(self_board) - 1][self_c]
                self.nf = rotation

        # Find south neighbor
        if self.s is None:
            if self_r + 1 < len(self_board):
                self.s = self_board[self_r + 1][self_c]
                self_board[self_r + 1][self_c].n = self
            else:
                target_block, rotation = board_links[(self.mapping_block, 'S')]
                target_board = boards[target_block - 1]
                if 4 - rotation == 1:
                    target_board = rotate(target_board)
                elif 4 - rotation == 2:
                    target_board = rotate(rotate(target_board))
                elif 4 - rotation == 3:
                    target_board = rotate(rotate(rotate(target_board)))
                self.s = target_board[0][self_c]
                self.sf = rotation

        # Find west neighbor
        if self.w is None:
            if self_c - 1 >= 0:
                self.w = self_board[self_r][self_c - 1]
                self_board[self_r][self_c - 1].e = self
            else:
                target_block, rotation = board_links[(self.mapping_block, 'W')]
                target_board = boards[target_block - 1]
                if 4 - rotation == 1:
                    target_board = rotate(target_board)
                elif 4 - rotation == 2:
                    target_board = rotate(rotate(target_board))
                elif 4 - rotation == 3:
                    target_board = rotate(rotate(rotate(target_board)))
                self.w = target_board[self_r][len(self_board) - 1]
                self.wf = rotation

        # Find east neighbor
        if self.e is None:
            if self_c + 1 < len(self_board):
                self.e = self_board[self_r][self_c + 1]
                self_board[self_r][self_c + 1].w = self
            else:
                target_block, rotation = board_links[(self.mapping_block, 'E')]
                target_board = boards[target_block - 1]
                if 4 - rotation == 1:
                    target_board = rotate(target_board)
                elif 4 - rotation == 2:
                    target_board = rotate(rotate(target_board))
                elif 4 - rotation == 3:
                    target_board = rotate(rotate(rotate(target_board)))
                self.e = target_board[self_r][0]
                self.ef = rotation

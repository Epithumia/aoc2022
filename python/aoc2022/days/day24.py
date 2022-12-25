from collections import defaultdict
import heapq as heap
from functools import cache

cave = defaultdict(lambda: '#')


def day24():
    with open('../input/input24.txt', 'r') as f:
        data = f.read().splitlines()

    height = len(data)
    width = len(data[0])

    # cave = defaultdict(lambda: '#')

    for r in range(1, height - 1):
        for c in range(1, width - 1):
            cave[(r - 1, c - 1)] = data[r][c]

    width -= 2
    height -= 2

    p, c = dijkstra((0, 0, 1), width, height, (height - 1, width - 1))

    cost = 1e10

    for row, col, m in c.keys():
        if (row, col) == (height - 1, width - 1):
            cost = min(c[(row, col, m)], cost)

    print('Part 1:', cost + 1)

    p, c = dijkstra((height - 1, width - 1, cost + 2), width, height, (0, 0))
    cost2 = 1e10

    for row, col, m in c.keys():
        if (row, col) == (0, 0):
            cost2 = min(c[(row, col, m)], cost2)

    p, c = dijkstra((0, 0, cost + 1 + cost2 + 2), width, height, (height - 1, width - 1))
    cost3 = 1e10

    for row, col, m in c.keys():
        if (row, col) == (height - 1, width - 1):
            cost3 = min(c[(row, col, m)], cost3)

    print('Part 2:', cost + 1 + cost2 + 1 + cost3 + 1)


def print_cave(minute, w, h):
    for r in range(-1, h + 1):
        for c in range(-1, w + 1):
            print(get_spot(r, c, minute, cave, w, h), end='')
        print('')


def get_neighbors(row, col, minute, w, h):
    neighbors = []
    up = get_spot(row - 1, col, minute, w, h)
    if up == '.':
        neighbors.append((row - 1, col, minute))
    down = get_spot(row + 1, col, minute, w, h)
    if down == '.':
        neighbors.append((row + 1, col, minute))
    left = get_spot(row, col - 1, minute, w, h)
    if left == '.':
        neighbors.append((row, col - 1, minute))
    right = get_spot(row, col + 1, minute, w, h)
    if right == '.':
        neighbors.append((row, col + 1, minute))
    still = get_spot(row, col, minute, w, h)
    if still == '.':
        neighbors.append((row, col, minute))
    return neighbors


@cache
def get_spot(row, col, minute, w, h):
    if (row == -1 and col == 0) or (row == h and col == w - 1):
        return '.'
    if row <= -1 or row >= h or col <= -1 or col >= w:
        return '#'
    if minute == 0:
        return cave[(row, col)]
    a = get_spot((row - minute) % h, col, 0, w, h)
    if a != 'v':
        a = ''
    b = get_spot((row + minute) % h, col, 0, w, h)
    if b != '^':
        b = ''
    c = get_spot(row, (col - minute) % w, 0, w, h)
    if c != '>':
        c = ''
    d = get_spot(row, (col + minute) % w, 0, w, h)
    if d != '<':
        d = ''
    res = a + b + c + d
    if len(res) == 0:
        return '.'
    if len(res) == 1:
        return res
    return str(len(res))


def dijkstra(starting_node, width, height, end_node):
    visited = set()
    parents_map = {}
    pq = []
    node_costs = defaultdict(lambda: float('inf'))
    node_costs[starting_node] = 1
    heap.heappush(pq, (1, starting_node))

    while pq:
        _, node = heap.heappop(pq)
        visited.add(node)

        r, c, m = node

        for adj_node in get_neighbors(r, c, m + 1, width, height):
            if adj_node in visited:
                continue

            new_cost = node_costs[node] + 1
            if node_costs[adj_node] > new_cost:
                parents_map[adj_node] = node
                node_costs[adj_node] = new_cost
                heap.heappush(pq, (new_cost, adj_node))
            ra, ca, _ = adj_node
            if (ra, ca) == end_node:
                return parents_map, node_costs

    return parents_map, node_costs

from collections import defaultdict
from typing import Tuple
import heapq as heap


def day12():
    with open('../input/input12.txt', 'r') as f:
        data = f.read().splitlines()

    jungle_map = JungleMap(data)

    print('Part 1:', jungle_map.explore('reach')[1])
    print('Part 2:', jungle_map.explore('hike')[1])


class JungleMap(object):
    def __init__(self, data):
        dmap = []
        i = 0
        self.candidates = []
        for row in data:
            r = []
            j = 0
            for point in row:
                if point == 'S':
                    point = 'a'
                    self.start = (i, j)
                if point == 'E':
                    point = 'z'
                    self.end = (i, j)
                if point == 'a':
                    self.candidates.append((i, j))
                r.append(point)
                j += 1
            dmap.append(r)
            i += 1
        self.map = dmap

        self.adj = dict()

        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                self.adj[(row, col)] = self.get_neighbors((row, col))

    def get_neighbors(self, point: Tuple[int, int]):
        neighbors = []
        if point[0] > 0 and (ord(self.map[point[0] - 1][point[1]]) - 1 <= ord(self.map[point[0]][point[1]])):
            neighbors.append((point[0] - 1, point[1]))
        if point[1] > 0 and (ord(self.map[point[0]][point[1] - 1]) - 1 <= ord(self.map[point[0]][point[1]])):
            neighbors.append((point[0], point[1] - 1))
        if point[0] < len(self.map) - 1 and (
                ord(self.map[point[0] + 1][point[1]]) - 1 <= ord(self.map[point[0]][point[1]])):
            neighbors.append((point[0] + 1, point[1]))
        if point[1] < len(self.map[0]) - 1 and (
                ord(self.map[point[0]][point[1] + 1]) - 1 <= ord(self.map[point[0]][point[1]])):
            neighbors.append((point[0], point[1] + 1))
        return neighbors

    def explore(self, mode='reach'):
        if mode == 'reach':
            paths, costs = self.dijkstra(self.start)
            return paths[self.end], costs[self.end]
        path = None
        min_cost = 1e7
        for point in self.candidates:
            paths, costs = self.dijkstra(point)
            if costs[self.end] < min_cost:
                min_cost = costs[self.end]
                path = paths[self.end]
        return path, min_cost

    def dijkstra(self, starting_node):
        visited = set()
        parents_map = {}
        pq = []
        node_costs = defaultdict(lambda: float('inf'))
        node_costs[starting_node] = 0
        heap.heappush(pq, (0, starting_node))

        while pq:
            _, node = heap.heappop(pq)
            visited.add(node)

            for adj_node in self.adj[node]:
                if adj_node in visited:
                    continue

                new_cost = node_costs[node] + 1
                if node_costs[adj_node] > new_cost:
                    parents_map[adj_node] = node
                    node_costs[adj_node] = new_cost
                    heap.heappush(pq, (new_cost, adj_node))

        return parents_map, node_costs

from collections import defaultdict
from itertools import permutations
import parse
import heapq as heap

from tqdm import tqdm

valves = dict()
key_valves = dict()
key_valves_ids = dict()
opened = dict()
elephant_opened = dict()
gain_map = dict()
cache = dict()


def day16():
    with open('../input/input16.txt', 'r') as f:
        data = f.read().splitlines()

    format_string = 'Valve {} has flow rate={:d}; tunne{} lea{} to valv{} {}'
    for row in data:
        vals = parse.parse(format_string, row)
        neigh = []
        for n in vals[5].split(', '):
            neigh.append(n)
        node = Valve(vals[0], vals[1], neigh)
        valves[node.id] = node
        if node.capacity > 0 or node.id == 'AA':
            key_valves[node.id] = node
            key_valves_ids[node.id] = 1
    key_valves_ids['AA'] = 1

    for valve in valves.values():
        paths, costs = dijkstra(valve)
        valve.costs = costs
        valve.paths = paths

    depressurize()
    sorted_gain_keys = sorted(gain_map, key=gain_map.get)
    sorted_gains = list({x: gain_map[x]} for x in sorted_gain_keys)
    best = gain_map[sorted_gain_keys[-1]]
    print('Part 1:', sorted_gains[-1])

    opened.clear()
    gain_map.clear()
    team_depressurize(best=best)
    sorted_gain_keys = sorted(gain_map, key=gain_map.get)
    print('Part 2:', sorted_gain_keys[-1], gain_map[sorted_gain_keys[-1]])


def dijkstra(starting_node):
    visited = set()
    parents_map = {}
    pq = []
    node_costs = defaultdict(lambda: float('inf'))
    node_costs[starting_node.id] = 0
    heap.heappush(pq, (0, starting_node.id))

    while pq:
        _, node = heap.heappop(pq)
        node = valves[node]
        visited.add(node.id)

        for adj_node in node.neighbors:
            adj_node = valves[adj_node]
            if adj_node.id in visited:
                continue

            new_cost = node_costs[node.id] + 1
            if node_costs[adj_node.id] > new_cost:
                parents_map[adj_node.id] = node.id
                node_costs[adj_node.id] = new_cost
                heap.heappush(pq, (new_cost, adj_node.id))

    return parents_map, node_costs


def score_valves(minutes=30):
    s = 0
    for v in opened:
        valve = key_valves[v]
        if opened[v] <= minutes:
            s += (minutes - opened[v]) * valve.capacity
    if len(elephant_opened) > 0:
        for v in elephant_opened:
            valve = key_valves[v]
            if elephant_opened[v] <= minutes:
                s += (minutes - elephant_opened[v]) * valve.capacity
    return s


def potential(op, el, rem):
    s = 0
    maxop = 0
    maxel = 0
    for v in op:
        valve = key_valves[v]
        if op[v] <= 26:
            s += (26 - op[v]) * valve.capacity
            maxop = max(maxop, op[v])
    for v in el:
        valve = key_valves[v]
        if el[v] <= 26:
            s += (26 - el[v]) * valve.capacity
            maxel = max(maxel, el[v])
    k = 0
    for v in rem:
        valve = key_valves[v]
        s += (26 - max(maxel, maxop) - k // 2) * valve.capacity
        k += 1
    return s


def depressurize(cost=0, parent='AA'):
    opened[parent] = cost
    if len(key_valves) == len(opened) or cost > 30:
        actual = dict()
        for k in opened.keys():
            if opened[k] <= 30:
                actual[k] = opened[k]
        gain_map[str(actual)] = score_valves()
        return None
    for v in key_valves:
        if v not in opened.keys():
            valve = key_valves[v]
            new_cost = cost + valve.costs[parent] + 1  # move and open
            depressurize(new_cost, v)
            opened.popitem()
    return None


def team_depressurize(cost=0, parent='AA', cost_ele=0, parent_ele='AA', prev_parent=None, prev_ele_par=None, best=0):
    if parent is not None:
        prev_parent = parent
        opened[parent] = cost
        key_valves_ids.pop(parent, None)
    if parent_ele is not None:
        prev_ele_par = parent_ele
        elephant_opened[parent_ele] = cost_ele
        key_valves_ids.pop(parent_ele, None)
    if (len(key_valves) + 1 == len(opened) + len(elephant_opened)) or (cost >= 26 and cost_ele >= 26):
        actual = dict()
        for k in opened.keys():
            if opened[k] <= 26:
                actual[k] = opened[k]
        for k in elephant_opened.keys():
            if elephant_opened[k] <= 26:
                actual[k] = elephant_opened[k]
        gain_map[str(actual)] = score_valves(26)
        return gain_map[str(actual)]
    keys = list(k for k in key_valves_ids.keys())
    if len(keys) == 1:
        keys.append(None)
    fpairs = list(permutations(keys, 2))
    pairs = fpairs
    if cost == 0 and cost_ele == 0:
        pairs = tqdm(pairs)
    for v_hum, v_ele in pairs:
        pot = potential(opened, elephant_opened, key_valves_ids)
        if pot > best:
            parent = prev_parent
            parent_ele = prev_ele_par
            if v_hum is not None:
                valve_h = key_valves[v_hum]
                new_cost = cost + valve_h.costs[parent] + 1  # move and open
            else:
                prev_parent = parent
                new_cost = cost
            if v_ele is not None:
                valve_e = key_valves[v_ele]
                new_cost_ele = cost_ele + valve_e.costs[parent_ele] + 1  # move elephant and open
            else:
                prev_ele_par = parent_ele
                new_cost_ele = cost_ele
            cache_key = 'o:' + str(opened) + '/e:' + str(elephant_opened) + '/k:' + str(key_valves_ids)
            if cache_key in cache:
                score = cache[cache_key]
            else:
                score = team_depressurize(new_cost, v_hum, new_cost_ele, v_ele, prev_parent, prev_ele_par, best)
            best = max(best, score)
            if v_hum is not None:
                i, _ = opened.popitem()
                key_valves_ids[i] = 1
            if v_ele is not None:
                i, _ = elephant_opened.popitem()
                key_valves_ids[i] = 1

    return best


class Valve:
    def __init__(self, id, capacity, neighbors):
        self.id = id
        self.capacity = capacity
        self.neighbors = neighbors
        self.paths = {}
        self.costs = {}

    def update_neighbors(self):
        for neighbor in self.neighbors:
            if self.id not in valves[neighbor].neighbors:
                valves[neighbor].neighbors.append(self.id)

    def __repr__(self):
        return 'ID: ' + str(self.id) + ', flow: ' + str(self.capacity) + ', neighbors: ' + str(self.neighbors) + \
            '\npaths: ' + str(self.paths) + '\ncosts: ' + str(self.costs) + '\n'

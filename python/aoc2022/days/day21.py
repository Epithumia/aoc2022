from tqdm import tqdm
from parse import parse
from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, LpBinary, value, PULP_CBC_CMD
import sympy as sym


def day21():
    with open('../input/input21.txt', 'r') as f:
        data = f.read().splitlines()

    monkeys = {'root': Monkey()}

    for row in data:
        slone = '{}: {:d}'
        smult = '{}: {} * {}'
        sadd = '{}: {} + {}'
        ssub = '{}: {} - {}'
        sdiv = '{}: {} / {}'
        res = parse(slone, row)
        if res is not None:
            if res[0] not in monkeys:
                monkey = Monkey()
                monkey.update('lone', res[1])
                monkeys[res[0]] = monkey
            else:
                monkeys[res[0]].update('lone', res[1])
        res = parse(smult, row)
        if res is not None:
            if res[0] not in monkeys:
                monkey = Monkey()
                monkeys[res[0]] = monkey
            if res[1] not in monkeys:
                monkey = Monkey()
                monkeys[res[1]] = monkey
            if res[2] not in monkeys:
                monkey = Monkey()
                monkeys[res[2]] = monkey
            monkeys[res[0]].update('mult', monkeys[res[1]], monkeys[res[2]])
        res = parse(sdiv, row)
        if res is not None:
            if res[0] not in monkeys:
                monkey = Monkey()
                monkeys[res[0]] = monkey
            if res[1] not in monkeys:
                monkey = Monkey()
                monkeys[res[1]] = monkey
            if res[2] not in monkeys:
                monkey = Monkey()
                monkeys[res[2]] = monkey
            monkeys[res[0]].update('div', monkeys[res[1]], monkeys[res[2]])
        res = parse(sadd, row)
        if res is not None:
            if res[0] not in monkeys:
                monkey = Monkey()
                monkeys[res[0]] = monkey
            if res[1] not in monkeys:
                monkey = Monkey()
                monkeys[res[1]] = monkey
            if res[2] not in monkeys:
                monkey = Monkey()
                monkeys[res[2]] = monkey
            monkeys[res[0]].update('add', monkeys[res[1]], monkeys[res[2]])
        res = parse(ssub, row)
        if res is not None:
            if res[0] not in monkeys:
                monkey = Monkey()
                monkeys[res[0]] = monkey
            if res[1] not in monkeys:
                monkey = Monkey()
                monkeys[res[1]] = monkey
            if res[2] not in monkeys:
                monkey = Monkey()
                monkeys[res[2]] = monkey
            monkeys[res[0]].update('sub', monkeys[res[1]], monkeys[res[2]])

    print('Part 1:', int(monkeys['root'].eval()))

    monkeys['humn'].update('humn')

    print('Part 2:', int(monkeys['root'].solve(monkeys['humn']).atoms().pop()))


class Monkey(object):
    def __init__(self):
        self.val1 = None
        self.val2 = None
        self.monkey_type = 'unknown'

    def update(self, monkey_type='unknown', val1=None, val2=None):
        self.val1 = val1
        self.val2 = val2
        self.monkey_type = monkey_type

    def eval(self):
        if self.monkey_type == 'humn':
            return sym.var('x')
        if self.monkey_type == 'lone':
            return self.val1
        v1 = self.val1.eval()
        v2 = self.val2.eval()
        if self.monkey_type == 'mult':
            return v1 * v2
        if self.monkey_type == 'div':
            return v1 / v2
        if self.monkey_type == 'add':
            return v1 + v2
        if self.monkey_type == 'sub':
            return v1 - v2

    def solve(self, human):
        return sym.solveset(self.val1.eval() - self.val2.eval(), human.eval())

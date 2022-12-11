monkeys = []


def day11():
    with open('../input/input11.txt', 'r') as f:
        data = f.read().split('\n')

    for m in range(len(data) // 7):
        monkeys.append(Monkey(data[7 * m:(7 * m + 7)]))

    for _ in range(20):
        for monkey in monkeys:
            monkey.turn()

    monkey_business = [monkey.activity for monkey in monkeys]
    monkey_business.sort(reverse=True)
    print('Part 1:', monkey_business[0] * monkey_business[1])

    monkeys.clear()
    worry = 1
    for m in range(len(data) // 7):
        monkeys.append(Monkey(data[7 * m:(7 * m + 7)]))
        worry *= monkeys[m].test

    for _ in range(10000):
        for monkey in monkeys:
            monkey.turn(worry)

    monkey_business = [monkey.activity for monkey in monkeys]
    monkey_business.sort(reverse=True)
    print('Part 2:', monkey_business[0] * monkey_business[1])


class Monkey(object):

    def __init__(self, data):
        self.id = int(data[0].split(':')[0].split(' ')[1])
        self.items = [int(val) for val in data[1].split(':')[1].split(',')]
        op = data[2].split('new = old ')[1]
        self.oper = op.split(' ')[0]
        self.val = op.split(' ')[1]
        self.test = int(data[3].split('by')[1])
        self.t = int(data[4].split('monkey')[1])
        self.f = int(data[5].split('monkey')[1])
        self.activity = 0

    def __repr__(self):
        s = f"Monkey {self.id}, holding {str(self.items)}\nOperation : new = old {self.oper} {self.val}\n"
        s += f"If level divisible by {self.test}"
        s += f"\n- then pass to Monkey {self.t}, else:\n- pass to Monkey {self.f}\n"
        s += f"Its activity level is: {self.activity}\n"
        return s

    def turn(self, worry=None):
        for _ in range(len(self.items)):
            self.inspect()
            self.get_bored(worry)
            self.pass_item()

    def inspect(self):
        self.activity += 1
        if self.val == 'old':
            val = self.items[0]
        else:
            val = int(self.val)
        if self.oper == '+':
            self.items[0] = self.items[0] + val
        else:
            self.items[0] = self.items[0] * val

    def get_bored(self, worry=None):
        if worry is None:
            self.items[0] = self.items[0] // 3
        else:
            self.items[0] = self.items[0] % worry

    def pass_item(self):
        if self.items[0] % self.test == 0:
            monkeys[self.t].receive(self.items.pop(0))
        else:
            monkeys[self.f].receive(self.items.pop(0))

    def receive(self, item):
        self.items.append(item)
